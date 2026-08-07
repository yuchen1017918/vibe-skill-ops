# Vibe-Skill-Ops

A self-governing skill system for Vibe Coding on [Hermes Agent](https://github.com/NousResearch/hermes-agent) — a four-layer organization routing framework (team/enterprise × assistant/owner) with complexity Triage, confirmation SLAs, knowledge extraction, and cost-aware governance.

> **Vibe-Coding Skill 全家桶** — Hermes Agent 上自治理的 Vibe Coding skill 体系:四层组织路由、确认 SLA、知识萃取、成本感知治理。

---

## What it is / What it is NOT

| ✅ It IS | ❌ It is NOT |
|----------|-------------|
| A set of Markdown skill documents (SKILL.md) with routing & workflow conventions | An executable program or standalone framework |
| A "workbook + routing table" for the main agent | A system with its own daemon processes |
| Conventions that *enhance* agent behavior once loaded | Platform-level enforcement (nothing stops you from bypassing it) |
| Runs on Hermes primitives (`terminal` / `delegate_task` / `skill_view`) | Bundles its own runtime / sandbox / scheduler |

**The most important sentence:** words like "auto-trigger", "self-healing", and "circuit breaker" mean **"after loading this skill, the agent follows the documented convention"** — NOT "a background process is monitoring the system". This family is a documentation system; its reliability ceiling equals the agent's instruction-following ability. Hence the philosophy: **"Enhancement, not dependency. Automation, not impunity."**

---

## Architecture

```
vibe-coding-family/
├── vibe-coding-hub/            # L1: entry hub — Triage → decision tree → scenario templates
├── dev-core-hub/               # L2: core dev (code/debug/test/commit/security audit)
├── dev-stack-hub/              # L2: tech stack (languages/frontend/DB/game engines)
├── dev-infra-hub/              # L2: infra (terminal/containers/MCP/deploy/security)
├── dev-agent-hub/              # L2: agent orchestration & governance
├── dev-ai-hub/                 # L2: AI/ML (training/inference/RAG/multimodal)
└── 22 self-built L3 skills     # tool ×9 / workflow ×6 / policy ×5 / meta ×2
```

All L3 skills carry a `metadata.hermes.type` tag defining how they are invoked:

| Type | Meaning | Example |
|------|---------|---------|
| `tool` | A concrete task with input/output | snapshot-notes, security-audit, china-env-adapt |
| `workflow` | A staged process | plan-workflow, agent-loop, knowledge-extraction |
| `policy` | Standing discipline, injected when relevant | karpathy-coding-dscpln, frontend-design-policy, cost-agent |
| `meta` | Governs other skills | fallback-general-dev, vibe-skills-gov-patterns |

---

## Core Mechanisms

| Mechanism | Version | What it does |
|-----------|---------|--------------|
| **Complexity Triage** | v1.0.0 | 5-question yes/no checklist → L0/L1/L2; project-context weighting; dynamic calibration from actual cost/retry data |
| **Cost awareness** | v1.0.0 | Token estimate per workflow task; `/simple` family of degradation policies; cost-agent weekly report + ROI dashboard; observer-exemption accounting |
| **Confirmation SLA** | v1.0.0 | Blocking / Notify / Batch confirmation tiers with timeouts; `/focus 30m` do-not-disturb; per-user preference learning |
| **Trigger governance** | v1.0.0 | Namespace rules + conflict arbitration for 28 skills; context-bound triggers & negative triggers |
| **Snapshot health check** | v1.5 | Conflict classification 🟢🟡🟠🔴 vs git (source of truth); manual-confirm alignment; cross-device sync (optional) |
| **Circuit breaker** | v1.4 | CLOSED/OPEN/HALF-OPEN state machine; timeout tiers; error-type disposition matrix; agent trust chain |
| **Knowledge extraction** | v1.1 | Post-incident 5-Whys review; 4-element quality gate; human review hook; verification loop |
| **Security audit** | v1.1 | 6-dimension pre-commit scan; rule tiers (🔴 never degrade); false-positive feedback loop |
| **Meta-governance** | v1.4 | Event-driven audits (conflict matrix / fallback loop detection / permission recursion); 30-day deprecation cooling period |
| **Lazy-load contract layer** | v1.0.0 | Description = contract (≤10 lines); body = detail (load on demand); prevents context crowding |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yuchen1017918/vibe-skill-ops.git

# 2. Install: copy the family into Hermes skills dir (default profile)
cp -r vibe-skill-ops/vibe-coding-family ~/.hermes/skills/

# 3. Use: just start a dev task — the agent auto-routes via vibe-coding-hub
#    (or say "按全家桶流程来" / "make an MVP" / "继续上次")
```

Requires a Hermes Agent installation with the skills/ plugin layout.

---

## Version History

| Version | Theme | Highlights |
|---------|-------|-----------|
| v3.1 | Foundation | 3-layer disclosure, 18 self-built L3 skills, fallback protocol |
| v3.2 | System governance | L1 decision tree, L2 boundary declarations, skill type tags, scenario templates |
| v3.3 | Self-healing | Complexity Triage, snapshot health check, security audit, heartbeat, experience recall |
| v3.4 | Constraints & boundaries | Triage checklist, conflict-classified alignment, circuit breaker state machine, cost awareness |
| v3.5 | Cognitive enhancement | knowledge-extraction, confirmation SLA, project-context weighting, smart /simple, meta-governance |
| v1.0.0 | Official release | Promoted from internal v3.6: trigger governance, lazy-load contract layer, execution-drift log, progressive-disclosure v2, compatibility contract |
| v1.1.0 | Local beta | requirement-clarify (proactive interview → DECISIONS.md), fallback escalation chain (upgrade-then-degrade) |
| v1.2.0 | Local beta | Four-layer organization routing (team/enterprise × assistant/owner), dev-assistant copilot protocol, quick-dev lightweight flow (31 skills) |
| v1.3.0 | Local beta | 大道至简: merged 3 skill pairs (project-init/agent-ops/release-ops, 22 active L3), one-line profile routing, default-path execution, intervention depth L0-L4, escalation ceiling, evidence consumption, contract layer ≤5 lines |

---

## Design Philosophy

1. **Enhancement, not dependency** — losing the family degrades the agent to plain mode; work continues.
2. **Automation, not impunity** — every auto action has a human-confirmation threshold; the final say belongs to the user.
3. **Less is more** — context windows hold contracts, not full documents; a step that is always skipped should be simplified, not enforced harder.
4. **Evidence over imagination** — execution-drift logs, triage-accuracy logs, and ROI dashboards drive documentation iteration instead of author intuition.

---

## Contributing

- New skills must carry the contract layer (trigger / negative_trigger / type / deps / key_rule).
- Every rule change needs a Changelog entry: why it exists, which pain point it solves.
- Run scenario conflict simulation before promoting a new rule (see `vibe-skills-gov-patterns`).
- Keep it honest: document what is convention vs. what is enforced.

## License

MIT © 2026 yuchen1017918
