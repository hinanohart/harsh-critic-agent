# Changelog

All notable changes to this project are documented here. Versions follow
[Semantic Versioning](https://semver.org/). Entries follow
[Keep a Changelog](https://keepachangelog.com/).

## [v1.0.1] - 2026-05-19

### Changed
- Re-tagged from MIT-licensed HEAD. Previous tag `v1.0.0` (2026-04..05) was cut while the repository carried an Apache-2.0 license; the project has since relicensed to MIT. No code changes from `v1.0.0` other than the LICENSE file update. This patch release exists so that `pip install` / version-pinned consumers receive the same MIT-licensed source that the current `main` provides.

## [1.0.0] — 2026-04-18

### Added

- Initial public release as a derivative work of
  [`oh-my-claudecode/critic`](https://github.com/Yeachan-Heo/oh-my-claudecode)
  by Yeachan Heo.
- `agents/harsh-critic.md`: English agent prompt with four original
  passes from upstream (pre-commitment / verification / multi-perspective
  / gap analysis) plus four new passes.
- **Phase 6 — Statistical Sanity Pass** with seven sub-checks (S1 … S7):
  sample size, point-estimate-vs-CI, control validity, multi-seed
  reproducibility, numerical anomaly detection, label provenance,
  sensitivity analysis.
- **Phase 7 — Post-Publication Adversarial Pass** with six sub-checks
  (P1 … P6): README executable, figures regenerable from data, dangling
  references, competitor-comparison honesty, dead-weight images, parallel
  audit.
- **Phase 8 — Anti-Pattern Detection** with eight patterns (A1 … A8):
  frame-hopping, n=3 illusion, manufactured certainty, sunk-cost
  protection, moving goalpost, selective reporting, premature
  abstraction, narrative-fit bias.
- **Case Study Anchors** (CS-1 … CS-6) drawn from real OSS release and
  research-code failures and their corrections.
- `agents/harsh-critic.ja.md`: full Japanese translation of the agent.
- `docs/CASE_STUDIES.md`: six annotated real-world failures referenced
  by the agent.
- `docs/STATISTICAL_THINKING.md`: plain-language explanations of each
  Phase-6 sub-check with copy-pastable Wilson CI / bootstrap /
  permutation recipes.
- `examples/example-review-output.md`: reference review output showing
  every section of the output format.
- `tests/test_agent_structure.py`: seventeen structural tests that guard
  against prompt drift and ensure both locales stay in sync.
- GitHub Actions CI: prompt structural tests, markdownlint, link
  checker, CodeQL.
- Dependabot for GitHub Actions.
- `NOTICE` file documenting the MIT heritage and derived elements.

### Attribution

- Role framing, four-phase skeleton, multi-perspective matrix, gap
  analysis, output format, and failure-modes list are retained from the
  upstream `critic.md` by Yeachan Heo (MIT, 2025). See `NOTICE`.
