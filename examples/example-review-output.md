# Example `@harsh-critic` review output

A hypothetical plan review, illustrating every section of the output format.
The input plan describes a proposed research release with a benchmark
table, a README demo command, and a headline "2× speedup" claim.

---

```text
VERDICT: REVISE

Overall Assessment
------------------
Core approach is sound and the code builds cleanly. Two headline claims
rest on statistical evidence too thin to survive peer review; one figure
disagrees with its underlying JSON; and the README's hero command is
stale after last week's CLI refactor.

Pre-Commitment Predictions vs Actual Findings
---------------------------------------------
  Predicted:
    - n-size issue in the "2× speedup" claim.
    - Stale README command after the recent refactor.
    - Missing ablation on the quantization bit-width.
  Found:
    - n-size issue confirmed (Table 2, n=3 per condition).
    - Stale README command confirmed (`bench --mode=fast` removed in
      commit 4f7a12b, still quoted in README.md:87).
    - New surprise: Figure 3 mismatches fig3.json by 1.19 units
      (see Critical #2). Quantization ablation was present and clean.

Critical Findings (blocks execution)
------------------------------------
1. Table 2 "2× speedup" (paper.md:214) rests on n=3 trials per condition.
   - Confidence: HIGH
   - Phase: Phase 6 / S1 — coin-flip p=0.125 under null; no CI reported.
   - Why this matters: a hostile reviewer will flag this as "preliminary,
     not a published headline claim."
   - Fix: re-run at n ≥ 30 with matched seeds, OR re-label as
     "preliminary 3-trial pilot" and move the 2× figure out of the
     abstract.

2. Figure 3 "delta = -0.92" (main.tex:287) contradicts fig3.json:147
   ("delta": -2.11).
   - Confidence: HIGH
   - Phase: Phase 7 / P2 — figures must regenerate from raw data.
   - Why this matters: matches CS-6 pattern exactly; review credibility
     cost is disproportionate to the error size.
   - Fix: replace the prose number with a `\csvautotabular`-style macro
     that reads from fig3.json at build time. Add a CI check that greps
     prose numbers and validates them against JSON.

Major Findings (significant rework)
-----------------------------------
1. README.md:87 demo command `bench --mode=fast` was removed in commit
   4f7a12b (2026-04-14).
   - Phase: Phase 7 / P1 — README commands must run cleanly.
   - Fix: replace with the current `bench run --profile=fast` syntax and
     add a CI step that executes the README block in a Docker container.

2. Control condition for Section 4.3 uses the same seed (42) across all
   treatment arms.
   - Phase: Phase 6 / S3 — randomized control is not actually
     randomized.
   - Fix: sample per-arm seeds from a pinned `seeds.json` committed to
     the repository.

Minor Findings (suboptimal but functional)
------------------------------------------
1. CHANGELOG.md is 48 entries deep with no version headers; consider
   adopting Keep-a-Changelog format.

Statistical Sanity Notes
------------------------
  - Sample size: n=3 per condition, insufficient for a directional
    "2× speedup" claim.
  - CI / permutation test: absent throughout Table 2.
  - Control validity: suspect (shared seed across arms).
  - Multi-seed reproducibility: single-seed; sign-stability unverified.

Post-Publication Adversarial Notes
----------------------------------
  - README commands run cleanly: NO — 1 stale command (Major #1).
  - Figures match data: NO — Figure 3 mismatch (Critical #2).
  - Dangling references: 1 — section "§4.2 Discussion" is referenced
    from §3.4 but no §4.2 exists in this draft.

Anti-Patterns Detected (Phase 8)
--------------------------------
  - A3 (manufactured certainty): abstract uses "definitively
    outperforms"; evidence supports "suggests an improvement".
    Recommendation: soften to "shows a promising improvement of X%
    (95% CI …)".
  - No other Phase-8 patterns detected.

What's Missing
--------------
  - No sensitivity analysis for the 0.1 magnitude threshold (Section 4.2).
  - No seed-stability report (Section 4.3).
  - No mention of failure modes or cases where the method underperforms
    the baseline.

Multi-Perspective Notes
-----------------------
  - Security / Executor / Reviewer: a reviewer running `bench --mode=fast`
    will hit a command-not-found error within the first minute.
  - New-hire / Stakeholder / 48-hour hindsight: the 2× headline will be
    the first thing someone screenshots; it must survive Twitter-level
    scrutiny.
  - Ops / Skeptic / Downstream user: JSON/prose mismatch is the kind of
    thing cited in retraction notes. Fix before publication, not after.

Verdict Justification
---------------------
Two Critical findings block execution: the 2× claim is statistically
unsupported at the stated n, and Figure 3 contradicts its own data
file. Once those are fixed and the two Major findings (stale README,
shared-seed control) are resolved, this plan should move to
ACCEPT-WITH-RESERVATIONS pending a second pass.

Open Questions (low-confidence, speculative, or unverified)
-----------------------------------------------------------
  - I could not verify whether the "2× speedup" number is reproducible
    across hardware; the plan does not specify the benchmarking
    machine. Worth documenting.
  - Section 5 claims a "negligible memory overhead"; I did not audit
    the memory profiler output and cannot confirm.
```

---

## Notes on this example

- Every finding carries a **Phase reference** (e.g., `Phase 6 / S1`). This
  lets you trace the reasoning back to the agent prompt in
  [`agents/harsh-critic.md`](../agents/harsh-critic.md) and lets you
  contest individual findings by their rule.

- Every Critical and Major finding carries a **fix**. You should be able
  to act on every one of them within a day.

- The `Pre-Commitment Predictions vs Actual Findings` block is the most
  valuable part. The "new surprise" entries are where the agent did its
  job — a reviewer who only finds what they expected to find is not
  adding value.

- **The agent said so** is never a valid defense on your side. If you
  disagree with a finding, cite evidence back. The agent is wrong
  sometimes; calibration is a two-way street.
