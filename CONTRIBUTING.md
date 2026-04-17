# Contributing

Thanks for considering a contribution. This project is a prompt-engineering
artifact, so contributions have a slightly different shape than typical
code projects.

## What is welcome

1. **New case-study anchors** (highest value). A single well-documented
   real-world failure teaches more than pages of generic advice. New
   entries must come from public post-mortems or author-confirmed self-
   reports and follow the existing structure in `docs/CASE_STUDIES.md`
   (Pattern / Reality / Evidence in the wild / Fix / Agent response).

2. **New anti-patterns** for Phase 8. Propose as a PR adding an `A9` /
   `A10` / … entry with a concrete signal the agent can look for, why
   it matters, and at least one case study where the pattern caused
   a real failure.

3. **New statistical sub-checks** for Phase 6. Must be actionable within
   a day's work for the author under review. Include a Python recipe in
   `docs/STATISTICAL_THINKING.md`.

4. **Translations**. New locales can live alongside the existing
   `harsh-critic.ja.md`. Run `pytest tests/` to confirm your translation
   has all phases, sub-checks, and case-study IDs.

5. **Bug fixes**: typos, broken links, outdated references, tests that
   should fail but don't.

## What is discouraged

- Removing sub-checks without a documented case for why they are
  harmful. Even rarely-fired sub-checks have a prevention role.
- Adding new phases without evidence of a real failure mode they
  prevent. Prompts drift toward bloat; resist.
- Changing the verdict vocabulary (`REJECT / REVISE / ACCEPT-WITH-
  RESERVATIONS / ACCEPT`). Downstream users script against these names.
- Softening language in the prompt. The harshness is a feature, not a
  bug. Praise-padding is the main failure mode `harsh-critic` was built
  to resist.

## Process

1. Open an issue first for anything larger than a typo fix. The existing
   issue template asks for the motivating failure and the proposed
   change.
2. PRs must keep both `harsh-critic.md` and `harsh-critic.ja.md` in sync
   (the structural tests will fail otherwise).
3. Run the tests locally:

   ```bash
   python -m pip install pytest
   python -m pytest tests/ -v
   ```

4. Add a line to `CHANGELOG.md` under an `## [Unreleased]` section.
5. Keep commits small and descriptive. Prefer multiple focused commits
   over one omnibus.

## Development environment

No runtime dependencies for the agent itself. For running tests you only
need `python>=3.10` and `pytest`.

## Code of conduct

By participating in this project you agree to abide by
[`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## License

By submitting a contribution you agree that your contribution is licensed
under the terms of [`LICENSE`](./LICENSE) (MIT).
