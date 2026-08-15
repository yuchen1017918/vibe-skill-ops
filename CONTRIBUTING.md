# Contributing to Vibe-Skill-Ops

[中文](CONTRIBUTING.zh-CN.md) | English

Thank you for considering contributing to Vibe-Skill-Ops! The family's core philosophy is **Simplicity First** — every new skill adds to the always-loaded context cost, so adding is much harder than removing. The rules below keep the family growing without losing control.

## Hard gates for new skills (all four required)

1. **Contract layer ≤5 lines** — `description` is the only part that is always visible. It must contain: trigger words / negative triggers / type / dependencies / key rules. Over 5 lines gets rejected.
2. **7-day cooling period** — new skills first live in the cooling zone (see `vibe-skills-gov-patterns`). If not loaded for 30 days, they are auto-deprecated (file kept to avoid breaking cross-references).
3. **Composability proof** — you must prove the capability **cannot be composed from existing skills**. If 2–3 existing skills combined cover 80%, the answer is no.
4. **Conflict simulation** — run trigger-conflict tests: will your new triggers steal words from existing skills? What is the arbitration priority?

## Contract layer template

```yaml
---
name: your-skill
description: |
  <One line: what it does> + <when to use>.
  Triggers: <word1>, <word2>.
version: 1.0.0
metadata:
  hermes:
    type: tool | workflow | policy | meta
    related_skills: [related skill list]
---
```

## Modifying existing skills

- Every rule change needs a Changelog entry: **why it exists, what pain it solves**.
- Stay honest: document whether something is a *convention* or *enforced*.
- Structural changes (merge/deprecate) follow the `skill-family-maintenance` flow: keep the primary name and absorb content → mark the absorbed one deprecated → repo-wide reference replacement (excluding the merger and deprecated files) → update hub counts/scenario tables.

## Submitting & PRs

1. Fork + feature branch (follow `git-workflow`: atomic commits, save points, trunk-based).
2. Pass the dual gate before committing: `code-security` discipline self-check + `security-audit` scan (commits get blocked by the hook).
3. PR description must state: pain → approach → verification results (real run output, not paper claims).
4. Pass `open-code-review` before merge.

## What is NOT welcome

- ❌ A "skill about X" — the description must have clear trigger conditions.
- ❌ Duplicate variants of existing capabilities — search first (use `vibe-code-search`).
- ❌ One-off scripts in the family — one-off tasks go through `quick-dev`; only promote after the approach is proven.
- ❌ SKILL.md over 300 lines — details go into `references/`; the body must be readable in 30 seconds.

## Style

- Language: SKILL.md bodies are primarily Chinese (for Chinese users); key mechanism terms keep their English originals.
- Bilingual docs: English `README.md` (default) + Chinese `README.zh-CN.md`, with LANG links at the top.
- Evidence first: any "tested" / "verified" claim must be backed by real run output. No fabrication.

Questions first: open an Issue to discuss before opening a big PR. Thanks!
