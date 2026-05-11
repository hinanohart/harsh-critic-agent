"""Structural tests for the harsh-critic agent prompt files.

These tests guard against prompt-drift. The agent's value comes from its
specific structure (phases 1-9, sub-checks S1-S7 / P1-P6 / A1-A8, case
studies CS-1 to CS-6). Silently losing a phase during an edit would
degrade the agent without breaking any visible surface; these tests catch
that class of regression.

No external dependencies — standard library only.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"
DOCS_DIR = ROOT / "docs"

EN_AGENT = AGENTS_DIR / "harsh-critic.md"
JA_AGENT = AGENTS_DIR / "harsh-critic.ja.md"
CASE_STUDIES = DOCS_DIR / "CASE_STUDIES.md"
STAT_DOC = DOCS_DIR / "STATISTICAL_THINKING.md"


# ---------- helpers ----------------------------------------------------------


def read(path: Path) -> str:
    assert path.exists(), f"expected file to exist: {path}"
    return path.read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    assert m, "agent file must begin with YAML frontmatter delimited by ---"
    block = m.group(1)
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def assert_all_present(text: str, needles: Iterable[str], label: str) -> None:
    missing = [n for n in needles if n not in text]
    assert not missing, f"{label}: missing tokens {missing}"


# ---------- frontmatter ------------------------------------------------------


def test_english_agent_frontmatter_required_fields() -> None:
    fm = extract_frontmatter(read(EN_AGENT))
    assert fm.get("name") == "harsh-critic"
    assert fm.get("model") == "opus"
    assert fm.get("license") == "MIT"
    # NOTE: ``disallowedTools`` is a frontmatter *hint*, not a runtime
    # sandbox — Claude Code's subagent spec uses a ``tools:`` allowlist.
    # This test asserts the YAML string is present (so the hint continues
    # to be shipped) but does NOT claim Write/Edit are enforced at the
    # harness level. SECURITY.md explains the gap explicitly.
    assert "Write" in fm.get("disallowedTools", "")
    assert "Edit" in fm.get("disallowedTools", "")


def test_japanese_agent_frontmatter_required_fields() -> None:
    fm = extract_frontmatter(read(JA_AGENT))
    assert fm.get("name") == "harsh-critic"
    assert fm.get("model") == "opus"
    assert fm.get("license") == "MIT"


def test_both_agents_have_matching_version() -> None:
    en = extract_frontmatter(read(EN_AGENT)).get("version")
    ja = extract_frontmatter(read(JA_AGENT)).get("version")
    assert en is not None and en == ja, (
        f"version mismatch between locales: en={en!r} ja={ja!r}"
    )


# ---------- phases -----------------------------------------------------------


REQUIRED_EN_PHASES = [
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 5.5",
    "Phase 6",
    "Phase 7",
    "Phase 8",
    "Phase 9",
]


def test_english_agent_contains_all_phases() -> None:
    assert_all_present(read(EN_AGENT), REQUIRED_EN_PHASES, "english agent")


def test_japanese_agent_contains_all_phases() -> None:
    assert_all_present(read(JA_AGENT), REQUIRED_EN_PHASES, "japanese agent")


# ---------- sub-checks -------------------------------------------------------


STAT_SUBCHECKS = ["(S1)", "(S2)", "(S3)", "(S4)", "(S5)", "(S6)", "(S7)"]
PUB_SUBCHECKS = ["(P1)", "(P2)", "(P3)", "(P4)", "(P5)", "(P6)"]
ANTI_PATTERNS = [
    "(A1)",
    "(A2)",
    "(A3)",
    "(A4)",
    "(A5)",
    "(A6)",
    "(A7)",
    "(A8)",
]


def test_english_agent_contains_all_statistical_subchecks() -> None:
    assert_all_present(read(EN_AGENT), STAT_SUBCHECKS, "english agent / S*")


def test_english_agent_contains_all_post_publication_subchecks() -> None:
    assert_all_present(read(EN_AGENT), PUB_SUBCHECKS, "english agent / P*")


def test_english_agent_contains_all_anti_patterns() -> None:
    assert_all_present(read(EN_AGENT), ANTI_PATTERNS, "english agent / A*")


def test_japanese_agent_contains_all_subchecks() -> None:
    ja = read(JA_AGENT)
    assert_all_present(ja, STAT_SUBCHECKS, "japanese agent / S*")
    assert_all_present(ja, PUB_SUBCHECKS, "japanese agent / P*")
    assert_all_present(ja, ANTI_PATTERNS, "japanese agent / A*")


# ---------- case-study cross-references --------------------------------------


CASE_STUDIES_IDS = ["CS-1", "CS-2", "CS-3", "CS-4", "CS-5", "CS-6"]


def test_case_studies_doc_contains_all_ids() -> None:
    assert_all_present(read(CASE_STUDIES), CASE_STUDIES_IDS, "CASE_STUDIES.md")


def test_english_agent_references_all_case_studies() -> None:
    assert_all_present(read(EN_AGENT), CASE_STUDIES_IDS, "english agent / CS-*")


def test_japanese_agent_references_all_case_studies() -> None:
    assert_all_present(read(JA_AGENT), CASE_STUDIES_IDS, "japanese agent / CS-*")


# ---------- statistical doc cross-references ---------------------------------


def test_statistical_doc_covers_all_subchecks() -> None:
    text = read(STAT_DOC)
    for sub in ("S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        assert sub in text, f"STATISTICAL_THINKING.md missing section for {sub}"


# ---------- attribution ------------------------------------------------------


def test_license_attributes_upstream_author() -> None:
    license_text = read(ROOT / "LICENSE")
    assert "Yeachan Heo" in license_text
    assert "harsh-critic-agent contributors" in license_text
    assert "MIT" in license_text


def test_notice_explains_derived_elements() -> None:
    notice = read(ROOT / "NOTICE")
    assert "Yeachan Heo" in notice
    assert "oh-my-claudecode" in notice
    # Guard against NOTICE becoming a bare stub.
    assert len(notice.splitlines()) >= 10


def test_readme_links_to_upstream() -> None:
    readme = read(ROOT / "README.md")
    assert "oh-my-claudecode" in readme
    assert "Yeachan Heo" in readme


# ---------- guard against regression to the old prompt -----------------------


def test_english_agent_is_extended_not_bare_upstream() -> None:
    """
    The whole point of this fork is the statistical pack, post-publication
    pass, anti-pattern detection, and case studies. If any of those core
    differentiators disappeared from the agent, this fork has no reason to
    exist. Guard explicitly.
    """
    text = read(EN_AGENT)
    differentiators = [
        "Statistical Sanity",
        "Post-Publication",
        "Anti-Pattern",
        "Case_Study_Anchors",
    ]
    missing = [d for d in differentiators if d not in text]
    assert not missing, (
        "english agent lost core differentiators (fork has no reason to "
        f"exist without them): {missing}"
    )
