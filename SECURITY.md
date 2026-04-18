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

## Honest framing of the Write/Edit restriction

The agent frontmatter declares `disallowedTools: Write, Edit`. Claude
Code's documented subagent frontmatter supports a `tools:` allowlist, not
a `disallowedTools:` denylist. In practice the prevailing Claude Code
releases are tolerant of the key, but **the Write/Edit block is
prompt-enforced, not harness-enforced** — the LLM chooses to comply with
the instruction in `<Constraints>`.

That means:

- A sufficiently aggressive prompt-injection payload in the reviewed
  material could, in principle, cause the model to call Write or Edit
  against the wishes of the agent prompt. The constraint in
  `<Constraints>` telling the model to treat reviewed content as DATA,
  not instructions, is our strongest defence; the frontmatter key is a
  hint, not a lock.
- The "Bash for verification only" guidance is likewise behavioural.
  Defence in depth: install `claude-safety-guard` alongside this agent
  so Bash calls that actually do destructive work are blocked at the
  hook layer.

This framing is deliberate. Treat the agent as *well-behaved by
convention*, not *sandboxed by construction*.

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
