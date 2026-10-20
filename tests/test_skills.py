#!/usr/bin/env python3
"""Static checks for the skill repository.

These tests validate the parts of a skill that can be checked without a
model: frontmatter, descriptions, references, README consistency, and
Markdown list formatting. The known-bad fixture calls the production
validator, so the test proves the validator discriminates.
"""

from pathlib import Path
import itertools
import re

import pytest

SKILLS_ROOT = Path(__file__).parents[1]
README_PATH = SKILLS_ROOT / "README.md"
ROUTING_DOCS_PATH = SKILLS_ROOT / "tests" / "routing" / "README.md"
MAX_DESCRIPTION_CHARS = 300
MAX_BODY_WORDS = 900
MAX_SECTION_WORDS = 250
DUPLICATE_GRAM_SIZE = 8
PORTABLE_PATH_PATTERNS = [".agents/", "/tmp/opencode"]
ALLOWED_DUPLICATED_SENTENCES = [
    "If a request falls outside these bounds, refuse or hand off.",
    "Sources and adaptations: references/provenance.md.",
]
EXPECTED_SKILLS = {
    "context-budget",
    "independent-review",
    "readme-authoring",
    "tools-and-security",
    "verification",
    "workflow-patterns",
}
OPENCODE_PATHS = [
    ".opencode/skills/<name>/SKILL.md",
    ".claude/skills/<name>/SKILL.md",
    ".agents/skills/<name>/SKILL.md",
    "~/.config/opencode/skills/<name>/SKILL.md",
    "~/.claude/skills/<name>/SKILL.md",
    "~/.agents/skills/<name>/SKILL.md",
]
BANNED_CLAIMS = [
    r"opencode/skill(?!s)",
    r"skillshare (add|eject|import|manifest)",
    r"opencode commit",
    r"commit tool",
    r"signed report",
    r"apply_patch is not",
    r"rewind tool",
    r"irreversible",
    r"cost nothing",
    r"false fall",
    r"a a ",
    r"skills name",
    r"pass/fate",
    r"Nothing depends",
    r"HEAD~5",
]
BANNED_SAMPLES = {
    r"opencode/skill(?!s)": "opencode/skill",
    r"skillshare (add|eject|import|manifest)": "skillshare add",
    r"opencode commit": "opencode commit",
    r"commit tool": "commit tool",
    r"signed report": "signed report",
    r"apply_patch is not": "apply_patch is not",
    r"rewind tool": "rewind tool",
    r"irreversible": "irreversible",
    r"cost nothing": "cost nothing",
    r"false fall": "false fall",
    r"a a ": "a a ",
    r"skills name": "skills name",
    r"pass/fate": "pass/fate",
    r"Nothing depends": "Nothing depends",
    r"HEAD~5": "HEAD~5",
}


def clean_scalar(raw: str, label: str) -> str:
    raw = raw.strip()
    if raw.startswith(('"', "'")):
        quote = raw[0]
        assert raw.endswith(quote) and len(raw) >= 2, (
            f"{label}: unterminated quote in {raw!r}"
        )
        return raw[1:-1]
    return raw


def parse_frontmatter(text: str) -> dict[str, object]:
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    end = text.find("\n---\n", 4)
    assert end != -1, "SKILL.md frontmatter is not closed"
    data: dict[str, object] = {}
    lines = text[4:end].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        key, separator, value = line.partition(":")
        assert separator, f"invalid frontmatter line: {line!r}"
        key = key.strip()
        value = value.strip()
        if key == "metadata" and not value:
            children: dict[str, str] = {}
            index += 1
            while index < len(lines) and lines[index].startswith((" ", "\t")):
                child = lines[index].strip()
                if child:
                    child_key, child_separator, child_value = child.partition(":")
                    assert child_separator, f"invalid metadata line: {child!r}"
                    children[child_key.strip()] = clean_scalar(
                        child_value, f"metadata {child_key.strip()}"
                    )
                index += 1
            data["metadata"] = children
            continue
        if value in {">", ">-", "|", "|-"}:
            parts = []
            index += 1
            while index < len(lines) and lines[index].startswith((" ", "\t")):
                parts.append(lines[index].strip())
                index += 1
            value = " ".join(parts)
        else:
            value = clean_scalar(value, key)
            index += 1
        data[key] = value
    return data


def skill_dirs() -> list[Path]:
    return sorted(
        directory
        for directory in SKILLS_ROOT.iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    )


def body_text(text: str) -> str:
    end = text.find("\n---\n", 4)
    assert end != -1, "SKILL.md frontmatter is not closed"
    return text[end + 5:]


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", " ", text, flags=re.S)


def normalized_words(text: str) -> list[str]:
    text = strip_code_blocks(text)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return text.split()


def section_word_counts(text: str) -> dict[str, int]:
    body = strip_code_blocks(body_text(text))
    parts = body.split("\n## ")
    counts: dict[str, int] = {"<intro>": len(parts[0].split())}
    for part in parts[1:]:
        title = part.splitlines()[0].strip()
        counts[title] = len(part.split())
    return counts


def validate_structure(directory: Path) -> None:
    skill_file = directory / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    description = frontmatter.get("description", "")
    assert isinstance(description, str) and description, (
        f"{skill_file}: missing description"
    )
    assert len(description) <= MAX_DESCRIPTION_CHARS, (
        f"{skill_file}: description length {len(description)} > {MAX_DESCRIPTION_CHARS}"
    )
    body = body_text(text)
    assert re.search(r"(?m)^## Non-goals\s*$", body), (
        f"{skill_file}: missing '## Non-goals' section"
    )
    body_words = len(strip_code_blocks(body).split())
    assert body_words <= MAX_BODY_WORDS, (
        f"{skill_file}: body has {body_words} words > {MAX_BODY_WORDS}"
    )
    for title, count in section_word_counts(text).items():
        assert count <= MAX_SECTION_WORDS, (
            f"{skill_file}: section '{title}' has {count} words > {MAX_SECTION_WORDS}"
        )
    for pattern in PORTABLE_PATH_PATTERNS:
        assert pattern not in body, (
            f"{skill_file}: project-local path {pattern!r} in portable skill body"
        )
    references_dir = directory / "references"
    if references_dir.is_dir():
        for reference in sorted(references_dir.glob("*.md")):
            relative = f"references/{reference.name}"
            assert relative in text, (
                f"{skill_file}: {relative} exists but is not cited from the body"
            )


def assert_no_duplicate_doctrine(bodies: dict[str, str]) -> None:
    allowed_sentences = [
        normalized_words(sentence) for sentence in ALLOWED_DUPLICATED_SENTENCES
    ]
    grams: dict[str, set[str]] = {}
    for name, body in bodies.items():
        words = normalized_words(body)
        allowed_word_indexes: set[int] = set()
        for sentence_words in allowed_sentences:
            for index in range(max(0, len(words) - len(sentence_words) + 1)):
                if words[index : index + len(sentence_words)] == sentence_words:
                    allowed_word_indexes.update(
                        range(index, index + len(sentence_words))
                    )
        grams[name] = {
            " ".join(words[index : index + DUPLICATE_GRAM_SIZE])
            for index in range(max(0, len(words) - DUPLICATE_GRAM_SIZE + 1))
            if all(
                word_index not in allowed_word_indexes
                for word_index in range(index, index + DUPLICATE_GRAM_SIZE)
            )
        }
    for first, second in itertools.combinations(sorted(grams), 2):
        shared = sorted(grams[first] & grams[second])
        assert not shared, (
            f"duplicated doctrine shared by {first} and {second}: {shared}"
        )


def referenced_paths(text: str) -> set[str]:
    paths = set()
    for match in re.finditer(r"(?:references|scripts)/[\w./-]+", text):
        paths.add(match.group(0).rstrip(".,;:)"))
    return paths


def check_markdown_lists(path: Path, text: str) -> None:
    in_code_block = False
    in_list = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            in_list = False
            continue
        if in_code_block:
            continue
        if not stripped:
            in_list = False
            continue
        if re.match(r"^(?:-|\*|\d+\.)\s+", line):
            in_list = True
            continue
        if in_list:
            if line.startswith((" ", "\t")):
                continue
            if line.startswith(("#", ">", "|")):
                in_list = False
                continue
            raise AssertionError(
                f"{path}:{line_number}: list continuation must be indented: {line!r}"
            )


def validate_skill_dir(directory: Path) -> None:
    skill_file = directory / "SKILL.md"
    assert skill_file.is_file(), f"{skill_file}: missing"
    text = skill_file.read_text(encoding="utf-8")
    assert "\u2014" not in text, f"{skill_file}: contains em dash (U+2014); use -- instead"
    frontmatter = parse_frontmatter(text)
    name = frontmatter.get("name", "")
    assert name == directory.name, (
        f"{skill_file}: frontmatter name {name!r} != directory {directory.name!r}"
    )
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name), (
        f"{skill_file}: invalid skill name {name!r}"
    )
    description = frontmatter.get("description", "")
    assert description, f"{skill_file}: missing description"
    assert len(description) <= 1024, (
        f"{skill_file}: description length {len(description)} > 1024"
    )
    for relative_path in referenced_paths(text):
        assert (directory / relative_path).is_file(), (
            f"{skill_file}: referenced file does not exist: {relative_path}"
        )
    check_markdown_lists(skill_file, text)
    metadata = frontmatter.get("metadata")
    assert isinstance(metadata, dict), f"{skill_file}: missing metadata block"
    assert metadata.get("opencode/slash") == "true", (
        f"{skill_file}: metadata opencode/slash must be 'true'"
    )


def readme_skill_names(text: str) -> set[str]:
    lines = text.splitlines()
    header_index = None
    for index, line in enumerate(lines):
        if "| Skill |" in line and "Loads when" in line:
            header_index = index
            break
    assert header_index is not None, "README: skill table header not found"
    readme_names = set()
    for line in lines[header_index + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = line.strip().strip("|").split("|")
        assert len(cells) >= 2, f"README: skill row has too few columns: {line!r}"
        assert cells[1].strip(), f"README: empty 'Loads when' cell: {line!r}"
        first_cell = cells[0].strip()
        match = (
            re.match(r"\*\*([a-z0-9-]+)\*\*", first_cell)
            or re.match(r"\[([a-z0-9-]+)\]", first_cell)
            or re.match(r"([a-z0-9-]+)", first_cell)
        )
        assert match, f"README: could not parse skill row: {line!r}"
        readme_names.add(match.group(1))
    return readme_names


def validate_readme_skill_names(text: str) -> None:
    names = readme_skill_names(text)
    assert names == EXPECTED_SKILLS, f"README table mismatch: {sorted(names)}"


def assert_no_banned_claims(text: str, label: str) -> None:
    for pattern in BANNED_CLAIMS:
        assert not re.search(pattern, text), f"{label}: banned claim matches {pattern!r}"


def test_expected_skill_directories() -> None:
    assert {directory.name for directory in skill_dirs()} == EXPECTED_SKILLS


def test_real_skills_pass_validator() -> None:
    for directory in skill_dirs():
        validate_skill_dir(directory)


def test_known_bad_skill_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-skill"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: good-skill\n"
        "description: A skill whose name does not match its directory.\n"
        "---\n"
        "# Bad skill\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="frontmatter name"):
        validate_skill_dir(bad_skill)


def test_known_good_temp_skill_passes_validator(tmp_path: Path) -> None:
    good_skill = tmp_path / "good-skill"
    good_skill.mkdir()
    (good_skill / "SKILL.md").write_text(
        "---\n"
        "name: good-skill\n"
        "description: A valid temporary skill.\n"
        "metadata:\n"
        '  opencode/slash: "true"\n'
        "---\n"
        "# Good skill\n",
        encoding="utf-8",
    )
    validate_skill_dir(good_skill)


def test_missing_slash_metadata_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "no-slash"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: no-slash\n"
        "description: A valid skill without slash metadata.\n"
        "---\n"
        "# No slash command\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="missing metadata block"):
        validate_skill_dir(bad_skill)


def test_top_level_slash_metadata_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "top-level-slash"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: top-level-slash\n"
        "description: A skill with slash metadata at the top level.\n"
        'opencode/slash: "true"\n'
        "---\n"
        "# Wrong nesting\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="missing metadata block"):
        validate_skill_dir(bad_skill)


def test_unterminated_metadata_quote_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-quote"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: bad-quote\n"
        "description: A skill with an unterminated metadata quote.\n"
        "metadata:\n"
        '  opencode/slash: "true\n'
        "---\n"
        "# Bad quote\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="unterminated quote"):
        validate_skill_dir(bad_skill)


def test_readme_table_matches_skill_directories() -> None:
    validate_readme_skill_names(README_PATH.read_text(encoding="utf-8"))


def test_readme_table_rejects_wrong_skill() -> None:
    bad_readme = (
        "| Skill | Loads when |\n"
        "|---|---|\n"
        "| **verification** | tests |\n"
    )
    with pytest.raises(AssertionError, match="README table mismatch"):
        validate_readme_skill_names(bad_readme)


def test_bad_description_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-description"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: bad-description\n"
        "description: " + "x" * 1025 + "\n"
        "---\n"
        "# Bad description\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="description length"):
        validate_skill_dir(bad_skill)


def test_missing_reference_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-reference"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: bad-reference\n"
        "description: A skill with a missing reference.\n"
        "---\n"
        "See references/missing.md.\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="referenced file does not exist"):
        validate_skill_dir(bad_skill)


def test_unindented_list_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-list"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: bad-list\n"
        "description: A skill with a broken list.\n"
        "---\n"
        "- first item\n"
        "continuation at column zero\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="list continuation must be indented"):
        validate_skill_dir(bad_skill)


def test_em_dash_fails_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-dash"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: bad-dash\n"
        "description: A skill with a dash.\n"
        "---\n"
        "Use an em dash \u2014 like this.\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="em dash"):
        validate_skill_dir(bad_skill)


@pytest.mark.parametrize("pattern", BANNED_CLAIMS)
def test_banned_claims_checker_rejects_known_bad(pattern: str) -> None:
    with pytest.raises(AssertionError, match="banned claim"):
        assert_no_banned_claims(
            f"prefix {BANNED_SAMPLES[pattern]} suffix", "fixture"
        )


def test_readme_lists_opencode_paths() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    for path in OPENCODE_PATHS:
        assert path in readme, f"README: missing OpenCode path {path}"
    assert ".opencode/skills/<repo>" not in readme, (
        "README: invented repo-specific OpenCode path"
    )


def test_docs_do_not_contain_banned_claims() -> None:
    documents = [README_PATH]
    documents.extend(directory / "SKILL.md" for directory in skill_dirs())
    documents.extend(sorted(SKILLS_ROOT.glob("*/references/*.md")))
    for document in documents:
        assert_no_banned_claims(document.read_text(encoding="utf-8"), str(document))


def test_real_skills_pass_structure_validator() -> None:
    for directory in skill_dirs():
        validate_structure(directory)


def test_real_skills_have_no_duplicate_doctrine() -> None:
    bodies = {
        directory.name: body_text((directory / "SKILL.md").read_text(encoding="utf-8"))
        for directory in skill_dirs()
    }
    assert_no_duplicate_doctrine(bodies)


def test_long_description_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "long-description"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: long-description\n"
        "description: " + "x" * (MAX_DESCRIPTION_CHARS + 1) + "\n"
        "---\n"
        "# Long description\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="description length"):
        validate_structure(bad_skill)


def test_missing_non_goals_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "no-non-goals"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: no-non-goals\n"
        "description: A skill without non-goals.\n"
        "---\n"
        "# No non-goals\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="Non-goals"):
        validate_structure(bad_skill)


def test_oversized_body_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "big-body"
    bad_skill.mkdir()
    filler = " ".join(["word"] * (MAX_BODY_WORDS + 1))
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: big-body\n"
        "description: A skill with an oversized body.\n"
        "---\n"
        "# Big body\n\n"
        f"{filler}\n\n"
        "## Non-goals\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="words >"):
        validate_structure(bad_skill)


def test_oversized_section_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "big-section"
    bad_skill.mkdir()
    filler = " ".join(["word"] * (MAX_SECTION_WORDS + 1))
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: big-section\n"
        "description: A skill with an oversized section.\n"
        "---\n"
        "# Big section\n\n"
        f"## Big section\n\n{filler}\n\n"
        "## Non-goals\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="section 'Big section'"):
        validate_structure(bad_skill)


def test_local_path_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "local-path"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: local-path\n"
        "description: A skill with a project-local path.\n"
        "---\n"
        "# Local path\n\n"
        "Write plans to /tmp/opencode/plan.md.\n\n"
        "## Non-goals\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="project-local path"):
        validate_structure(bad_skill)


def test_uncited_reference_fails_structure_validator(tmp_path: Path) -> None:
    bad_skill = tmp_path / "uncited-reference"
    bad_skill.mkdir()
    references = bad_skill / "references"
    references.mkdir()
    (references / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
    (bad_skill / "SKILL.md").write_text(
        "---\n"
        "name: uncited-reference\n"
        "description: A skill with an uncited reference.\n"
        "---\n"
        "# Uncited reference\n\n"
        "## Non-goals\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="not cited from the body"):
        validate_structure(bad_skill)


def test_duplicate_doctrine_checker_rejects_shared_gram() -> None:
    sentence = "the quick brown fox jumps over the lazy dog backwards"
    first = f"# A\n\n{sentence}\n\n## Non-goals\n"
    second = f"# B\n\n{sentence}\n\n## Non-goals\n"
    with pytest.raises(AssertionError, match="duplicated doctrine"):
        assert_no_duplicate_doctrine({"skill-a": first, "skill-b": second})


def test_duplicate_doctrine_checker_allows_standard_refusal() -> None:
    refusal = "If a request falls outside these bounds, refuse or hand off."
    first = f"# A\n\nShared tail: {refusal}\n\n## Non-goals\n"
    second = f"# B\n\nShared tail: {refusal}\n\n## Non-goals\n"
    assert_no_duplicate_doctrine({"skill-a": first, "skill-b": second})


def test_skill_testing_levels_documented() -> None:
    text = ROUTING_DOCS_PATH.read_text(encoding="utf-8")
    lowered = text.lower()
    for level in ("routing", "live", "reconstruction"):
        assert level in lowered, f"{ROUTING_DOCS_PATH}: missing {level} level"
