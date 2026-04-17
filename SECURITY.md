# Security policy

## Scope

`harsh-critic-agent` is a Markdown prompt file plus supporting
documentation and tests. It performs no network calls, spawns no
subprocesses, and has no secret-management surface of its own. The only
realistic security concerns are:

1. **Prompt-injection payloads** accidentally committed to the agent
   prompt that would subvert the reviewing behaviour when loaded into
   Claude Code.
2. **Malicious pull requests** attempting to insert instructions that
   cause the agent to rubber-stamp work instead of gating it.
3. **Supply-chain concerns** in the GitHub Actions workflows
   (third-party actions, pinned commit SHAs).

All actions in `.github/workflows/` are pinned to full commit SHAs to
mitigate (3). Dependabot keeps them current.

## Reporting a vulnerability

If you believe you have found a security issue — for example, a prompt
modification that causes the agent to behave unsafely — please do not
open a public issue.

Email: `hinanohart@gmail.com`

I'll acknowledge receipt within 72 hours and aim to publish a fix
within 14 days, or sooner if the issue is severe.

## Out of scope

- Behaviour of the downstream LLM invoking the agent (Claude, other).
  The agent is a prompt; the LLM is the runtime. Runtime issues
  should be reported to the relevant LLM vendor.
- Issues in `oh-my-claudecode` upstream. Please report those to the
  upstream project.
