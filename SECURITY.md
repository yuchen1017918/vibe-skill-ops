# Security Policy

[中文](SECURITY.zh-CN.md) | English

## Security model: Three-Layer Defense

Vibe-Skill-Ops is **Markdown documentation (skills)** — it executes no code, but it **guides agents that write code**. So the security focus is: make the guided agent write secure code, rather than becoming an attack surface itself.

| Layer | Mechanism | Cost | Trigger |
|-------|-----------|------|---------|
| **L1 Silent discipline** | 8 coding disciplines injected (`code-security`): SQL parameterization / secrets in env vars / output escaping / command list args / path allowlists / exception logging / empty-collection checks / input validation | Zero (on by default) | Active whenever coding |
| **L2 Light scanning** | Commit gate: semgrep incremental diff + dependency audit (`security-audit`) | Low | Task wrap-up / commit |
| **L3 Deep scanning** | Full scan + closed-loop rescan; AI review engine (`open-code-review`) | High (on demand) | Explicit user request |

**🔴 Non-negotiable red lines** (never disable, under any circumstances):
1. Secrets must go through environment variables — no hardcoding.
2. SQL must be parameterized — no string concatenation.
3. User input/output must be escaped — no raw HTML splicing.
4. Dangerous commands must have a confirmation gate (authorization gate, see `reverse-ops` Scope Gate).

## Reporting a vulnerability

Found a security issue (in the family docs themselves, or a systematic flaw in code the family guides agents to write):

- **Regular issues**: open a GitHub Issue with a `[SECURITY]` title prefix, describing: impact scope / reproduction / suggested fix.
- **High severity / urgent** (secret leaks, command injection, auth bypass): **do NOT open a public Issue** — contact the maintainer directly first (see the GitHub profile), then follow up with a public Issue after the fix.

Include in your report:
1. Affected version
2. Reproduction steps (minimal example)
3. Impact analysis (who is affected, how severe)
4. Suggested fix (if any)

## Handling process

1. Confirm the vulnerability → reply to the reporter within 24h.
2. Fix → commit passes the dual gate (hook blocks regressions).
3. Postmortem → the vulnerability is archived into `vuln-memory` by CWE category (counterexample → positive example + lesson) to prevent recurrence.
4. Disclosure → after the fix is merged, publish the vulnerability description + fix notes.

## Known limits (honest statement)

- **Reliability ceiling**: the family's "security" depends on the agent's instruction-following ability — docs cannot force an agent to obey disciplines, only constrain + scan + review. **Tool detection is a fallback; discipline is the real defense.**
- **Scanner boundaries** (tested): semgrep has 0 rule hits for PowerShell; secret detection is weak (does not recognize `sk-`/`ghp_` formats); bare Python function XSS/command injection does not trigger — these rely on L1 discipline as the backstop.
- **Out of scope**: code outside the family, and penetration testing of unauthorized systems (the latter is governed by the `reverse-ops` authorization gate — unauthorized = no ACT).

## Dependency security

The family itself has zero dependencies (pure Markdown); external skill copies under `external/` are for distribution reference only, with security responsibility resting with their upstreams. Install tools (ocr/semgrep, etc.) only from official channels with pinned versions.
