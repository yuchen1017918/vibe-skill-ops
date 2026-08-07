# Vibe-Skill-Ops

A self-governing skill system for Vibe Coding on [Hermes Agent](https://github.com/NousResearch/hermes-agent) — a four-layer organization routing framework (team/enterprise × assistant/owner), slimmed down by the **大道至简 (Great Simplicity)** philosophy: token × quality is a product, not a trade-off.

> **Vibe-Coding Skill 全家桶 v1.1.0** — Hermes Agent 上自治理的 Vibe Coding skill 体系:四层组织路由、大道至简、确认 SLA、知识萃取、成本感知治理。

---

## 大道至简（Great Simplicity）—— 本版本的设计核心

**token × 质量 = 乘积最优,不是取舍。**

- token 消耗 ≈ 加载的机制量;质量 ≈ 机制**被遵循**的程度
- 机制越多 → 加载越贵(token ↑)且走样越多(质量 ↓)= **双输**
- 机制越少 → 加载便宜(token ↓)且执行越准(质量 ↑)= **双赢**

**落地动作(减法优先)**:

| 动作 | 效果 |
|------|------|
| 合并 3 组重叠 skill(6 → 3) | 加载决策变少、触发词歧义消除 |
| 契约层压缩至 ≤5 行 | 常驻上下文减半(约 155 行) |
| 一句话画像 + 默认路径化 | 四层路由体验压缩为三层,15 秒锁定 |
| 30 天未加载 → deprecated | 从索引移除(文件保留防交叉引用) |
| 证据消费(周报一句话洞察 + 月报强制决策) | 用数据驱动删减,不靠作者直觉 |

**三条设计铁律**:
1. **增强不是依赖** — 全家桶失效时,Agent 退化为普通模式,工作仍可继续。
2. **自动化不是免责** — 每个自动动作都有人工确认阈值;最终决定权在用户。
3. **删掉一个 skill 试试系统会不会崩溃** — 简化不是偷懒,是唯一同时优化 token 与质量的路。

---

## 结构整改 —— 四层组织路由(v1.1.0 起)

> 旧三层按"技术类型"路由,需要先想清楚技术栈才能路由;新四层按**组织形态 + 开发模式**路由,
> 需求的第一性属性是"规模 + 谁主导",不是语言。

```
L1  组织形态   团队(轻量项目)              企业(大型项目)
              ┌──────────────┐           ┌──────────────┐
L2  开发模式   │ 助手 │ 全盘  │            │ 助手 │ 全盘  │
              └──────────────┘           └──────────────┘
L3  细分场景   四格场景表(路由表,不新增文档)
L4  执行 skill 具体 skill(dev-assistant / quick-dev / vibe-coding / dev-team)
      ↕ 技术分类 hub 下移为二级索引(dev-core / dev-stack / dev-infra / dev-agent / dev-ai)
```

**路由压缩**:一句话画像【组织】【主导】【类型】【技术】15 秒锁定 L1+L2;
**默认路径化**:5 个常见场景免判断直走(帮我看看→dev-assistant / 随手做→quick-dev / 新建项目→project-init / 发布回滚→release-ops / 组队→dev-team)。

## Architecture

```
vibe-coding-family/
├── vibe-coding-hub/            # L1: entry hub — 四层组织路由 + 一句话画像 + 全局机制
├── dev-core-hub/               # L2 索引: core dev (主流程四选一/编码/调试/测试/提交)
├── dev-stack-hub/              # L2 索引: tech stack (语言/前端/DB/游戏引擎)
├── dev-infra-hub/              # L2 索引: infra (终端/容器/MCP/部署/安全)
├── dev-agent-hub/              # L2 索引: agent 编排与治理
├── dev-ai-hub/                 # L2 索引: AI/ML (训练/推理/RAG/多模态)
└── 22 个路由内 L3 skills        # tool ×7 / workflow ×8 / policy ×5 / meta ×2
    └── 另有 6 个 deprecated 保留文件(文件保留防交叉引用,不进路由)
```

L3 skills 的 frontmatter `metadata.hermes.type` 标签定义调用方式:

| Type | Meaning | Example |
|------|---------|---------|
| `tool` | A concrete task with input/output | snapshot-notes, security-audit, china-env-adapt |
| `workflow` | A staged process | project-init, agent-ops, release-ops, agent-loop |
| `policy` | Standing discipline, injected when relevant | karpathy-coding-dscpln, frontend-design-policy, cost-agent |
| `meta` | Governs other skills | fallback-general-dev, vibe-skills-gov-patterns |

**v1.1.0 合并成果**(6 个 skill → 3 个,净减 3):

| 合并 | 产物 | 增量价值 |
|------|------|----------|
| project-scaffold + plan-workflow | **project-init** | + 技术栈背景嗅探(stack-detect 无感化 → .vibe/stack.yaml) |
| agent-workspace + agent-collab | **agent-ops** | 工位三件套 + 协作三步闭环一份管 |
| release-management + rollback-backup | **release-ops** | 发布+回滚同一流程两面(先备份再发布) |

---

## Core Mechanisms

| Mechanism | Version | What it does |
|-----------|---------|--------------|
| **Complexity Triage** | v1.0.0 | 5-question yes/no checklist → L0/L1/L2; dynamic calibration from actual cost/retry data |
| **One-line profile routing** | v1.1.0 | 【组织】【主导】【类型】【技术】15s 锁定 L1+L2;反驳只更新画像不重走路由 |
| **Default-path execution** | v1.1.0 | 5 常见场景免判断直走;触发词打架 → 走仲裁 |
| **Intervention depth L0-L4** | v1.1.0 | dev-assistant 分档:答疑→指路→草稿→副驾驶→代驾;跨文件变更阻塞型确认 |
| **Escalation ceiling** | v1.1.0 | fallback 升级 ≤6 步硬限;第 3 步提示;第 6 步人工介入;5 分钟循环检测 |
| **Evidence consumption** | v1.1.0 | cost-agent 周报一句话洞察 + 月报强制决策三问 |
| **Merge review** | v1.1.0 | 触发词重叠 >50% / 30 天未加载 / 一方总引用 → 合并候选;新增 skill 7 天冷静期 |
| **Cost awareness** | v1.0.0 | Token estimate per workflow task; `/simple` degradation; cost-agent weekly report + ROI dashboard |
| **Confirmation SLA** | v1.0.0 | Blocking / Notify / Batch confirmation tiers with timeouts; `/focus 30m` do-not-disturb |
| **Trigger governance** | v1.0.0 | Namespace rules + conflict arbitration for 28 skills; context-bound triggers & negative triggers |
| **Snapshot health check** | v1.5 | Conflict classification 🟢🟡🟠🔴 vs git (source of truth); manual-confirm alignment |
| **Circuit breaker** | v1.4 | CLOSED/OPEN/HALF-OPEN state machine; timeout tiers; error-type disposition matrix |
| **Knowledge extraction** | v1.1 | Post-incident 5-Whys review; 4-element quality gate; human review hook |
| **Security audit** | v1.1 | 6-dimension pre-commit scan; rule tiers (🔴 never degrade); false-positive feedback loop |
| **Meta-governance** | v1.4 | Event-driven audits; 30-day deprecation cooling period |
| **Lazy-load contract layer** | v1.1.0 | Description = contract (≤5 lines); body = detail (load on demand); prevents context crowding |

---

## Quick Start

### 方式一：快捷提示词（推荐，Agent 自动安装）

把下面这句**发给你的 AI Agent**（Hermes Agent / Claude Code / Codex…），它会自动读取教程并完成安装：

> 💬 `https://yuchen1017918.github.io/vibe-skill-ops/Tutorial.md，帮我下载安装这个 vibe-coding skill 全家桶。`

### 方式二：手动安装

```bash
# 1. Clone
git clone https://github.com/yuchen1017918/vibe-skill-ops.git /tmp/vibe-skill-ops

# 2. Install: copy the family into Hermes skills dir (default profile)
mkdir -p ~/.hermes/skills
cp -r /tmp/vibe-skill-ops/vibe-coding-family ~/.hermes/skills/

# 3. Verify
find ~/.hermes/skills/vibe-coding-family -name SKILL.md | wc -l   # 34 (28 active + 6 deprecated)

# 4. Use: just start a dev task — the agent auto-routes via vibe-coding-hub
#    (or say "按全家桶流程来" / "make an MVP" / "继续上次")
```

Requires a Hermes Agent installation with the skills/ plugin layout.

---

## Version History

| Version | Theme | Highlights |
|---------|-------|-----------|
| v3.1 | Foundation | 3-layer disclosure, 18 self-built L3 skills, fallback protocol |
| v3.2 | System governance | L1 decision tree, L2 boundary declarations, skill type tags, scenario templates |
| v3.3 | Self-healing | Complexity Triage, snapshot health check, security audit, experience recall |
| v3.4 | Constraints & boundaries | Triage checklist, conflict-classified alignment, circuit breaker, cost awareness |
| v3.5 | Cognitive enhancement | knowledge-extraction, confirmation SLA, project-context weighting, smart /simple, meta-governance |
| v1.0.0 | Official release | Promoted from internal v3.6: trigger governance, lazy-load contract layer, execution-drift log, compatibility contract |
| **v1.1.0** | **Official release (current)** | **大道至简 + 结构整改。整合内部迭代 v1.1–v1.3:requirement-clarify 澄清访谈;四层组织路由(团队/企业 × 助手/全盘);dev-assistant 副驾驶协议(介入深度 L0-L4);quick-dev 轻量全包(Triage 执行器);合并 3 组 skill(project-init / agent-ops / release-ops,28 路由内 skill);一句话画像 + 默认路径化;升降天花板;证据消费;契约层 ≤5 行** |

---

## Design Philosophy

1. **大道至简 (Great Simplicity)** — token × 质量是乘积不是取舍;机制越少,加载越便宜且执行越准。删掉一个 skill 试试系统会不会崩溃。
2. **Enhancement, not dependency** — losing the family degrades the agent to plain mode; work continues.
3. **Automation, not impunity** — every auto action has a human-confirmation threshold; the final say belongs to the user.
4. **Evidence over imagination** — execution-drift logs, triage-accuracy logs, and ROI dashboards drive documentation iteration instead of author intuition.

---

## Contributing

- New skills must carry the contract layer (trigger / negative_trigger / type / deps / key_rule), ≤5 lines.
- New skills need a 7-day cooling period and must prove they cannot be composed from existing skills (see `vibe-skills-gov-patterns`).
- Every rule change needs a Changelog entry: why it exists, which pain point it solves.
- Run scenario conflict simulation before promoting a new rule.
- Keep it honest: document what is convention vs. what is enforced.

## License

MIT © 2026 yuchen1017918
