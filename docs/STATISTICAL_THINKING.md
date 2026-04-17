# Statistical Thinking Pack

Phase 6 of `harsh-critic` is the statistical sanity pass. This document
explains each sub-check in plain language, shows why it matters, and gives
a small, copy-pastable recipe so you can verify the agent's finding
yourself.

All code examples use the Python standard library and NumPy only.

---

## S1 — Sample size sanity

**The question.** Is the sample size large enough to support the claim?

**Quick tests.**

- If the claim is "directional" (A is better than B), a reasonable
  minimum is n ≥ 30 per condition with an effect size measurement
  (Cohen's d or equivalent). Below that, frame the result as
  *preliminary* or *hypothesis-generating*.
- "3 out of 3 positive" is **not** strong signal. Under a 50/50 null,
  the probability is 0.5³ = 0.125 — one in eight by chance.

**Wilson 95% confidence interval for a proportion** (more honest than
the normal approximation for small n):

```python
import math

def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))

# Example: 14/15 successes.
print(wilson_ci(14, 15))   # (0.698, 0.996)
```

14/15 looks like 93.3%, but the 95% CI spans from 69.8% up to 99.6%. A
headline of "93.3% accuracy" without that interval is misleading.

---

## S2 — Point estimate vs confidence interval

**The question.** When the work reports a Δ (difference, improvement,
effect), does it come with a CI, an SE, or a permutation test?

**Why it matters.** Point estimates hide their own uncertainty. A Δ of
+0.05 with a 95% bootstrap CI of [-0.12, +0.22] is indistinguishable
from zero. The same Δ with CI [+0.02, +0.08] is solid.

**Bootstrap CI.**

```python
import random

def bootstrap_delta_ci(
    treatment: list[float],
    control: list[float],
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 42,
) -> tuple[float, float, float]:
    rng = random.Random(seed)
    deltas = []
    for _ in range(n_boot):
        t = [rng.choice(treatment) for _ in treatment]
        c = [rng.choice(control) for _ in control]
        deltas.append(sum(t) / len(t) - sum(c) / len(c))
    deltas.sort()
    lo = deltas[int(n_boot * (alpha / 2))]
    hi = deltas[int(n_boot * (1 - alpha / 2))]
    point = sum(treatment) / len(treatment) - sum(control) / len(control)
    return (point, lo, hi)
```

A CI containing zero means "indistinguishable from noise." Flagging such
a result as "significant improvement" is a CRITICAL finding.

---

## S3 — Baseline / control validity

**The question.** Is the control actually independent of the treatment?

**Classic traps.**

- Patching layer X and measuring at layer X (see CS-2).
- Randomized control but `seed=42` fixed across every condition (the
  "randomness" cancels).
- Control trained on the same data with the same augmentations; labels
  leaked through a shared tokenizer cache.
- Single-sided A/B where only converting users are counted as the
  denominator.

**Rule.** If you cannot name the mechanism that makes the control blind
to the treatment, the control is broken.

---

## S4 — Multi-seed / multi-model reproducibility

**The question.** Does the result persist when you change the random
seed or the model?

**Why it matters.** A single-seed result can be a local fluctuation. A
single-model result can be a model-family idiosyncrasy.

**Cheap test: seed sign-stability.**

```python
import statistics

def sign_stable(deltas: list[float]) -> bool:
    # True if all runs agree on the sign of the effect.
    signs = {1 if d > 0 else (-1 if d < 0 else 0) for d in deltas}
    signs.discard(0)
    return len(signs) == 1
```

Demand at least three seeds with agreeing signs before interpreting a
directional claim. Demand at least two model families before claiming
generality.

---

## S5 — Numerical anomaly detection

**The question.** Do the numbers themselves look plausible?

**Smells.**

- Exactly `0.0` or exactly `1.0` across every perturbation → experiment
  likely short-circuited, silently skipped, or constant-returning.
- Suspiciously round numbers like exactly `90.0%` → hardcoded value.
- Massive outliers without a diagnostic → noise, bug, or data corruption.

**Example.** In HaluEval, every perturbation returning exactly `0.0`
(all metrics identical) is a "failed experiment with a passing exit
code" rather than a real measurement.

---

## S6 — Label provenance

**The question.** Who or what produced the labels, and could it have
introduced a circular dependency?

**Red flags.**

- LLM-as-judge with a single judge from the same model family as the
  system under evaluation.
- Self-consistency where the evaluator is the evaluated.
- Human labels from annotators who also wrote the prompts.

**Rule.** Prefer majority vote from heterogeneous judges (different
model families, or a mixed panel of human + model). When a single
judge must be used, report the expected bias and sample a 5-10% human-
audit slice.

---

## S7 — Hardcoded thresholds without sensitivity analysis

**The question.** When the work uses "magnitude > 0.1" or "p < 0.05,"
does it show the result is robust to nearby thresholds?

**Why it matters.** A single threshold can be cherry-picked. If the
conclusion flips at 0.09 or 0.11, the claim does not travel.

**Small sensitivity recipe.**

```python
def sensitivity_table(
    evaluate,               # callable: threshold -> metric
    thresholds: list[float],
) -> list[tuple[float, float]]:
    return [(t, evaluate(t)) for t in thresholds]

table = sensitivity_table(my_eval, [0.05, 0.10, 0.15, 0.20])
for t, m in table:
    print(f"threshold={t:.2f}  metric={m:.3f}")
```

If the metric rises from 0.1 → 0.2 by threshold tuning, that is a
smoking gun. Document the table; the agent will ask for it.

---

## Permutation test (a reliable default)

When in doubt, use a permutation test. It has almost no assumptions
about the underlying distribution.

```python
import random

def permutation_p_value(
    treatment: list[float],
    control: list[float],
    n_perm: int = 10_000,
    seed: int = 42,
) -> float:
    rng = random.Random(seed)
    observed = sum(treatment) / len(treatment) - sum(control) / len(control)
    pool = treatment + control
    count = 0
    n_t = len(treatment)
    for _ in range(n_perm):
        rng.shuffle(pool)
        new_t = pool[:n_t]
        new_c = pool[n_t:]
        delta = sum(new_t) / n_t - sum(new_c) / len(new_c)
        if abs(delta) >= abs(observed):
            count += 1
    return (count + 1) / (n_perm + 1)
```

Report the permutation p-value alongside the bootstrap CI. A result that
survives both is much harder to attack.

---

## What the agent actually does with these

When `harsh-critic` encounters a quantitative claim, it runs through
S1 … S7 in order, cites the specific sub-check in the finding
("Phase 6 / S2 — CI includes 0"), and recommends one of:

- **Re-run at larger n** (S1 failure)
- **Add CI / permutation test** (S2 failure)
- **Fix control** (S3 failure)
- **Add multi-seed** (S4 failure)
- **Investigate anomaly** (S5 failure)
- **Switch to majority-vote / heterogeneous judges** (S6 failure)
- **Add sensitivity table** (S7 failure)

That list is intentionally small, concrete, and actionable. You should
be able to address any finding in a day's work or less.
