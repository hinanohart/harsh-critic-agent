# Case Studies

Six real-world failures the `harsh-critic` agent references by ID (CS-1 …
CS-6). Each is annotated with the pattern, the evidence, and the fix, so
that when the agent cites `CS-X` in a review, you can look up the matching
real situation.

Every case study here is drawn from a public post-mortem or a documented
self-correction the author has agreed to share. No private information is
reproduced.

---

## CS-1 — the n=3 illusion

**Pattern.** An author reports "3 prompts all positive" and treats it as
strong signal.

**Reality.** Under the null hypothesis that each trial is an independent
coin flip at p=0.5, the probability of three positives in a row is
0.5³ = 0.125. You get three positives by chance in roughly one in eight
studies. That is indistinguishable from noise, not "strong signal."

**Evidence in the wild.** Author's own yuragi project (v0.3.0) initially
reported three positive prompts as "strong evidence for the Sach-stability
hypothesis." Bootstrap confidence interval over the same three trials
included zero. Claim retracted and relabelled "preliminary."

**Fix.**

- Treat n=3 as hypothesis-generating, not hypothesis-confirming.
- Run at n ≥ 30 for any directional claim, or frame the three trials as a
  pilot and explicitly pre-register the confirmatory n.
- Report Wilson or bootstrap CI alongside the point estimate.

**Agent response.** `harsh-critic` tags Phase 6 / S1 (sample size sanity) as
CRITICAL for any claim below the required n, and recommends language
demotion to "preliminary."

---

## CS-2 — the auto-tautology control

**Pattern.** An intervention is applied at layer X, and the "control" is
measured at layer X.

**Reality.** If you edit layer 20 and look at layer 20's effect, the
control condition is not independent of the treatment — it is the same
measurement. You will always see "10/10 control preserved" because there
is nothing left to perturb.

**Evidence in the wild.** A public whitebox probing experiment placed a
causal intervention in layers 18-22 and used layer 20 as its control.
The "10/10 preservation" was flagged by a review pass as
structurally impossible evidence.

**Fix.**

- Control layers must fall outside the intervention window. In the real
  case: L3 (very-early) and L23 (post-phase2) replaced L20.
- Document the control layer index in the experiment README at the same
  level as the treatment index.
- Add an assertion at load time that `control_layers ∩ treatment_layers
  = ∅`.

**Agent response.** `harsh-critic` flags Phase 6 / S3 (baseline/control
validity) as CRITICAL and demands re-labelling of the original result as
"layer-self-preservation artifact" until a proper control is run.

---

## CS-3 — the fabricated chart

**Pattern.** A README or paper contains a figure whose values are
hand-typed or hard-coded, rather than regenerated from a raw-data file.

**Reality.** A reader who cares enough to re-run the numbers will find the
discrepancy in minutes. The credibility hit is not proportional to the
size of the error; any mismatch costs trust.

**Evidence in the wild.** A mosaic project's README claimed "38.4%
diversity" as its differentiating metric. The underlying `metrics.json`
read 42.4%. A reviewer diff'd the two and filed an issue. The whole
README had to be audited line-by-line.

**Fix.**

- Every chart must regenerate from a pinned raw-data JSON committed in
  the repository.
- Every numeric claim in prose must be a symbolic reference to a file,
  not a manually transcribed number. Use a build step that injects values
  from JSON into the document at render time.
- Add a CI check that compares prose numbers against the source JSON.

**Agent response.** `harsh-critic` flags Phase 7 / P2 (figures
regenerable from data) as CRITICAL for any public-facing doc where a
prose number cannot be traced to a source file.

---

## CS-4 — frame-hopping disease

**Pattern.** After the plan has already been approved, the author keeps
opening "just one more angle" instead of executing.

**Reality.** This is a symptom of completion anxiety combined with
sunk-cost protection. The author has invested enough in the exploration
that shipping feels like "losing" the optionality. A new angle is
emotionally safer than a release.

**Evidence in the wild.** A plan received six consecutive REJECT verdicts
across different review sessions. The rejections kept citing new angles
to pursue; the original minimum-viable version was never shipped. The
author's own memory file eventually diagnosed this as a recurring anti-
pattern.

**Fix.**

- Enforce ship-first, extend-later. Ship the approved minimum; then
  open new angles as separate tickets.
- When a plan receives ≥3 REJECTs across sessions, inspect for frame-
  hopping specifically rather than treating each REJECT as
  independent.
- Set a hard "time since original approval" budget. If it exceeds N days
  without a release, escalate.

**Agent response.** `harsh-critic` applies Phase 8 / A1 and openly asks:
"Is the author avoiding shipping by exploring?"

---

## CS-5 — missing layer normalization

**Pattern.** Applying logit-lens (or any unembed-based probe) to
intermediate hidden states without the model's final layer norm.

**Reality.** In architectures like Pythia and GPTNeoX, only
`hidden_states[-1]` has been normalized by `final_layer_norm` (also known
as `ln_f`) before HuggingFace returns it. Earlier layers' hidden states
are raw. If you pipe a raw hidden state directly into the unembedding
matrix, the resulting "logits" live at a scale where the softmax
collapses toward a near-uniform distribution of roughly `ln(vocab_size) ≈
10.83`. Every early layer will then look "stable" for any token, because
all of them are indistinguishable from each other.

**Evidence in the wild.** A whitebox probe on Pythia-410m reported
"stable Sach prediction across all layers" until a reviewer pointed out
that the stability was an artifact of the missing norm. Applying `ln_f`
to every intermediate state eliminated the stability for early layers
and preserved it only for the layers where the phenomenon actually
existed.

**Fix.**

- Always apply the model's final layer norm to intermediate hidden
  states before unembedding when doing logit-lens style probing.
- Sanity-check: on a layer early enough to be far from the target
  distribution, the probe should look like noise, not like "stable
  prediction." If it looks stable there too, the norm is missing.
- Add a unit test that the probe on layer 0 of a random input is near
  uniform over the vocabulary.

**Agent response.** `harsh-critic` flags Phase 6 / S5 (numerical anomaly
detection) as MAJOR when "stable from very early layer" is reported, and
asks specifically whether `ln_f` was applied.

---

## CS-6 — the typo in a numeric claim

**Pattern.** A paper, README, or blog post contains a number that was
typed by a human ("Δ = +0.558") while the underlying data file shows a
different value ("+3.96").

**Reality.** Every manually transcribed number is a liability. Humans
mis-type, copy from the wrong row, round inconsistently, or forget to
update after a re-run. The first rigorous reader finds the mismatch.

**Evidence in the wild.** A paper claimed "+0.558" for a perturbation
whose JSON record read "+3.96". A critic pass caught it by extracting
every number from the prose and cross-referencing it against the source
JSON.

**Fix.**

- Drive every numeric claim in prose from the data file at render time.
  Options: LaTeX macros populated from JSON, Markdown templated through
  a build step, Quarto/ Jupyter book cross-refs.
- Add a CI step that scans the prose for digit patterns and validates
  each one against the source file.
- Keep a `numbers.json` (or similar) as the single source of truth and
  forbid hand-typed numbers in final documents.

**Agent response.** `harsh-critic` flags Phase 7 / P2 as MAJOR when it
cannot verify a prose number against a source file, and CRITICAL when
the number is a headline claim.

---

## Contributing a new case study

Pull requests adding `CS-7` onwards are welcome if:

- The case is drawn from a public post-mortem, a published retraction, or
  a self-reported failure the author is willing to share.
- No private or confidential information is reproduced.
- The entry follows the existing structure: **Pattern / Reality /
  Evidence in the wild / Fix / Agent response**.

Good case studies are worth more than good prose. A single concrete
failure teaches more than a page of general advice.
