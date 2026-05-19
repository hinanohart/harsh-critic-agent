# harsh-critic-agent

> A battle-hardened final-quality-gate subagent for Claude Code. Blocks false
> approvals with statistical sanity checks, a post-publication adversarial
> pass, and anti-pattern detection.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Claude Code Agent](https://img.shields.io/badge/Claude%20Code-subagent-8A2BE2.svg)](https://docs.claude.com/en/docs/claude-code/sub-agents)
[![Attribution: Yeachan Heo](https://img.shields.io/badge/attribution-Yeachan%20Heo-informational)](./NOTICE)

---

## What this is

A single-file [Claude Code subagent](https://docs.claude.com/en/docs/claude-code/sub-agents)
that acts as the **final quality gate** for plans, code, and public-facing
releases. Drop it into `~/.claude/agents/` and invoke with
`@harsh-critic` (or via `Agent(subagent_type="harsh-critic", …)`).

It rejects false approvals cold by combining four passes most single-prompt
reviewers skip:

1. **Statistical Sanity** — sample size, confidence intervals, control
   validity, multi-seed reproducibility, hardcoded thresholds.
2. **Post-Publication Adversarial Review** — README commands run cleanly,
   figures regenerable from data, no dangling references, honest competitor
   comparison.
3. **Anti-Pattern Detection** — frame-hopping, n=3 illusion, manufactured
   certainty, sunk-cost protection, narrative-fit bias.
4. **Case-Study Anchors** — 6 real-world failures from published research
   and OSS releases that the agent cites when current work matches the
   pattern.

---

## What makes this different

`harsh-critic-agent` is a **derivative work** (MIT) of the excellent
[`critic.md`](https://github.com/Yeachan-Heo/oh-my-claudecode) in
Yeachan Heo's *oh-my-claudecode*. The upstream agent is already very good at:

- Pre-commitment predictions
- Multi-perspective review (security / new-hire / ops)
- Gap analysis
- Self-audit + realist check

This fork adds the missing half — **what hits you after publication**:

| Pass | Upstream `critic.md` | `harsh-critic-agent` |
|------|----------------------|----------------------|
| Role framing | ✅ | ✅ (retained) |
| Pre-commitment | ✅ | ✅ (retained) |
| Multi-perspective | ✅ | ✅ extended: reviewer / 48-hour-hindsight / downstream user |
| Gap analysis | ✅ | ✅ extended: "what is the author NOT talking about?" |
| Statistical sanity (n, CI, control, seeds) | — | ✅ Phase 6 (7 sub-checks) |
| Post-publication adversarial | — | ✅ Phase 7 (6 sub-checks) |
| Anti-pattern detection | — | ✅ Phase 8 (8 patterns) |
| Case-study anchors | — | ✅ 6 annotated real failures |
| Japanese translation | — | ✅ `agents/harsh-critic.ja.md` |

If your work is research, benchmarks, or a public OSS release, the four added
passes are where the reviewer will find your weak spots in the first 30
minutes. The agent pre-emptively simulates that hostile 30-minute read.

---

## Install

### Option 1 — user-level (global)

```bash
mkdir -p ~/.claude/agents
curl -L -o ~/.claude/agents/harsh-critic.md \
  https://raw.githubusercontent.com/hinanohart/harsh-critic-agent/main/agents/harsh-critic.md
```

### Option 2 — project-level

```bash
mkdir -p .claude/agents
curl -L -o .claude/agents/harsh-critic.md \
  https://raw.githubusercontent.com/hinanohart/harsh-critic-agent/main/agents/harsh-critic.md
```

### Option 3 — Japanese version

```bash
curl -L -o ~/.claude/agents/harsh-critic.md \
  https://raw.githubusercontent.com/hinanohart/harsh-critic-agent/main/agents/harsh-critic.ja.md
```

Claude Code auto-discovers agents in these directories on the next start.

---

## Usage

### From a conversation

```text
@harsh-critic please audit PLAN.md before I execute it
```

### From another agent / code

```python
Agent(
    description="Final gate on release plan",
    subagent_type="harsh-critic",
    prompt="Review RELEASE-v1.0.md. Public-facing — apply Phase 7."
)
```

### Recommended invocation points

- Before merging a PR that changes a migration, security code, or API
  contract.
- Before tagging a public release (triggers Phase 7).
- Before submitting a paper, preprint, or benchmark to the public
  (triggers Phase 6 + 7).
- When you notice yourself opening "just one more angle" on a decided
  plan (triggers Phase 8 / frame-hopping check).

---

## Example output

```text
VERDICT: REVISE

Overall Assessment: Core approach is sound; two claims rest on insufficient
statistical evidence, one figure disagrees with its underlying JSON, and an
auto-tautology control inflates one headline number.

Pre-Commitment Predictions vs Actual Findings:
  - Predicted: n-size issue in Table 2, stale README command, missing
    ablation for depth parameter.
  - Found: n-size issue confirmed (Table 2, n=3). README command works.
    New surprise: layer-20 control is patched at layer 20 (auto-tautology,
    CS-2 pattern).

Critical Findings:
1. Table 2 "70% accuracy" (paper.md:214) rests on n=3 trials.
   - Confidence: HIGH
   - Phase: Phase 6/S1 — coin-flip p=0.125 under null.
   - Fix: re-run at n≥30 OR re-label claim as "preliminary".

2. Figure 3 delta -0.92 (main.tex:287) contradicts fig3.json:147 (-2.11).
   - Confidence: HIGH
   - Phase: Phase 7/P2 — figures must regenerate from raw data.
   - Fix: replace prose number with symbolic reference to JSON.

…
```

See [`examples/example-review-output.md`](./examples/example-review-output.md)
for a full review.

---

## Design philosophy

- **False approvals cost 10-100× false rejections.** A courteous reviewer is
  a liability.
- **Every finding needs evidence.** `file:line`, quoted text, or data path.
  Opinions are not findings.
- **Statistical handwaving is a CRITICAL finding.** Not a stylistic preference.
- **Anti-patterns are the author's blind spots.** Name them explicitly; the
  author cannot see them alone.

The full philosophy is embedded in the prompt itself — see
[`agents/harsh-critic.md`](./agents/harsh-critic.md).

---

## Documentation

- [`docs/CASE_STUDIES.md`](./docs/CASE_STUDIES.md) — six annotated real-world
  failures referenced by the agent.
- [`docs/STATISTICAL_THINKING.md`](./docs/STATISTICAL_THINKING.md) — the
  Phase-6 reasoning in plain language, with code snippets for Wilson CI,
  bootstrap, permutation test, Fisher's exact.
- [`CHANGELOG.md`](./CHANGELOG.md)
- [`NOTICE`](./NOTICE) — upstream attribution

---

## Credit

This agent would not exist without the upstream
[`oh-my-claudecode`](https://github.com/Yeachan-Heo/oh-my-claudecode) by
**Yeachan Heo**. The role framing, investigation protocol skeleton, and
output-format structure are his. See [`NOTICE`](./NOTICE) for the exact
heritage and the list of substantive additions.

If you like this, star the upstream project too.

---

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Pull requests that add case-study
anchors from real failures (with public post-mortems) are especially welcome.

## Security

See [`SECURITY.md`](./SECURITY.md). The agent is a Markdown prompt file; it
has no network access and no code execution surface of its own.

Note that the `disallowedTools: Write, Edit` line in the frontmatter is
**prompt-enforced, not harness-enforced** — the LLM chooses to comply.
For destructive-command protection at the harness level, install
[`claude-safety-guard`](https://pypi.org/project/claude-safety-guard/) as
a PreToolUse hook alongside this agent.

## License

MIT — see [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE).
