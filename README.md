# Vibe-Skill-Ops

**给 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的可插拔增强技能包** —— 42 个经过实战验证的 skill,装完你的 Agent 立刻会:自动路由干活、写码自带安全纪律、跨会话记住上下文、质量审查把关。

> 兼容: Hermes Agent ✅ · Claude Code ✅ · Codex ✅ · OpenClaw ✅
> 版本: **v1.2.0** · 协议: MIT · 生态: Vibe Coding / AI 开发

---

## 🎯 它解决你的什么麻烦？

| 不用全家桶的麻烦 | 装完之后 |
|-----------------|---------|
| 😩 每次开新项目都要重新教 agent"按我的流程来",它总在问"接下来干嘛" | **一句话触发**:说"按全家桶流程来"或"做个 MVP",agent 自动路由到对应 skill,15 秒锁定开工 |
| 😰 写代码靠自觉,密钥硬编码、SQL 注入、危险命令,上线前才发现 | **8 条静默纪律 + 提交闸门**:写码默认安全,commit 前自动扫描,实测拦截 SQLi |
| 😵 换新会话/换平台,项目上下文全丢,重新解释一遍 | **快照 + 双层记忆**:说"继续上次"秒级恢复;踩过的坑自动沉淀,下次不重踩 |
| 🤯 代码质量没人把关,review 靠肉眼 | **AI 审查引擎**:一个命令行级审查,12 秒发现 2 个高危 bug(DeepSeek 实测) |
| 💸 token 越花越多,不知道花在哪 | **成本看板 + 渐进式披露**:机制按需加载,常驻上下文最小化,周报告诉你钱去哪了 |

> 三句话: **装完即用,不装也不亏**(全家桶是增强不是依赖,失效时自动退回普通模式);**机制按需加载**(不是全部塞进上下文);**每删一个 skill 系统都不会崩**(大道至简)。

---

## ⚡ 3 秒安装

### 方式一:快捷提示词(推荐)

把下面这句**发给你的 AI Agent**(Hermes Agent / Claude Code / Codex…),它会自动读取教程并完成安装:

> 💬 `https://yuchen1017918.github.io/vibe-skill-ops/Tutorial.md，帮我下载安装这个 vibe-coding skill 全家桶。`

### 方式二:手动安装

```bash
# 1. Clone
git clone https://github.com/yuchen1017918/vibe-skill-ops.git /tmp/vibe-skill-ops

# 2. Install: copy the family into Hermes skills dir (default profile)
mkdir -p ~/.hermes/skills
cp -r /tmp/vibe-skill-ops/vibe-coding-family ~/.hermes/skills/

# 3. Verify
find ~/.hermes/skills/vibe-coding-family -name SKILL.md | wc -l   # 42 (29 active + 6 hub + 7 deprecated)

# 4. Use: 直接开始开发任务 —— agent 自动通过 vibe-coding-hub 路由
#    (或说 "按全家桶流程来" / "make an MVP" / "继续上次")
```

**装完后你的 Agent 多长这样**: 你说"帮我写个脚本" → 走 quick-dev;说"组队开发" → 走 dev-team 流水线;说"发布" → 走 release-ops(自动备份+回滚预案);说"继续上次" → 快照恢复上下文。

---

## 🖼 长什么样?(装前 vs 装后)

```
  装前(原生 Hermes Agent)              装后(+ 全家桶 42 个 skill)
  ┌─────────────────────────┐        ┌──────────────────────────────┐
  │ 用户: "做个 XX"           │        │ 用户: "做个 XX"                │
  │ Agent: "好的,从哪里开始?" │  ───▶  │ Agent: 自动路由 15 秒锁定方案    │
  │ 你:  (手动教流程...)      │        │   ├ 需求模糊? → 澄清访谈        │
  │                         │        │   ├ 写码 → 8 条纪律自动生效       │
  │ 每次项目重复劳动          │        │   ├ 写完 → 审查引擎把关          │
  │ 换会话 = 全部重来         │        │   ├ 发布 → 备份+回滚预案         │
  │ 密钥靠自觉,坑靠回忆       │        │   └ 收尾 → 经验自动沉淀          │
  │                         │        │ 用户: "继续上次" → 秒级恢复       │
  └─────────────────────────┘        └──────────────────────────────┘
```

---

## 📦 它是什么?(30 秒版)

**Vibe-Skill-Ops 是一组 Markdown skill 文档 + 路由体系**,装在 Hermes Agent 的 skills 目录后,把你的 Agent 从"每句话都要教的工具"升级成"自己知道该用什么方法干活"的工程助手。

- **四层路由**: 组织形态(团队/企业)→ 开发模式(助手/全盘)→ 场景 → 执行 skill —— 不再按"技术类型"猜,按"规模+谁主导"路由
- **五大能力线**: 主流程(vibe-coding/dev-team) · 安全三层防线 · 双层记忆(开发/漏洞) · 质量闸门(AI 审查) · 并行与路由
- **优雅降级**: 全家桶出任何问题,Agent 退回原生模式照常工作 —— 它是增强,不是依赖
- **可扩展**: 支持把自己的工作流蒸馏成用户自定义 skill,与全家桶融合共存(见 `workflow-distillation`)

> ⚠️ 边界声明:这是 **Markdown 文档(skill)**,不是可执行软件。没有后台进程。"自动触发"指 Agent 加载 skill 后按约定执行,可靠性上限 = Agent 的指令遵循能力。

---

## 🗺 架构一览

```
vibe-coding-family/
├── vibe-coding-hub/            # L1: entry hub — 四层组织路由 + 一句话画像 + 全局机制
├── dev-core-hub/               # L2 索引: core dev (主流程四选一/编码/调试/测试/提交)
├── dev-stack-hub/              # L2 索引: tech stack (语言/前端/DB/游戏引擎)
├── dev-infra-hub/              # L2 索引: infra (终端/容器/MCP/部署/安全)
├── dev-agent-hub/              # L2 索引: agent 编排与治理
├── dev-ai-hub/                 # L2 索引: AI/ML (训练/推理/RAG/多模态)
└── 29 个路由内 L3 skills        # tool ×14 / workflow ×7 / policy ×6 / meta ×2
    └── 另有 7 个 deprecated 保留文件(文件保留防交叉引用,不进路由)

external/                       # 被全家桶引用的外部 skill 副本(related_skills 依赖)
    └── 27 个(语言/平台/工具 skill;仅供仓库完整性/分发,不参与路由)
```

L3 skills 的 frontmatter `metadata.hermes.type` 标签定义调用方式:

| Type | Meaning | Example |
|------|---------|---------|
| `tool` | A concrete task with input/output | snapshot-notes, security-audit, china-env-adapt |
| `workflow` | A staged process | project-init, agent-ops, release-ops, workflow-distillation |
| `policy` | Standing discipline, injected when relevant | karpathy-coding-dscpln, frontend-design-policy, cost-agent |
| `meta` | Governs other skills | fallback-general-dev, vibe-skills-gov-patterns |

**四层路由**:

```
L1  组织形态   团队(轻量项目)              企业(大型项目)
              ┌──────────────┐           ┌──────────────┐
L2  开发模式   │ 助手 │ 全盘  │            │ 助手 │ 全盘  │
              └──────────────┘           └──────────────┘
L3  细分场景   四格场景表(路由表,不新增文档)
L4  执行 skill 具体 skill(dev-assistant / quick-dev / vibe-coding / dev-team)
      ↕ 技术分类 hub 下移为二级索引(dev-core / dev-stack / dev-infra / dev-agent / dev-ai)
```

---

## ⚙️ Core Mechanisms(机制表)

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
| **Trigger governance** | v1.0.0 | Namespace rules + conflict arbitration; context-bound triggers & negative triggers |
| **Snapshot health check** | v1.5 | Conflict classification 🟢🟡🟠🔴 vs git (source of truth); manual-confirm alignment |
| **Circuit breaker** | v1.4 | CLOSED/OPEN/HALF-OPEN state machine; timeout tiers; error-type disposition matrix |
| **Knowledge extraction** | v2.0 | 已并入 snapshot-notes:post-incident 5-Whys review + 经验结构化 |
| **Security audit** | v1.1 | 6-dimension pre-commit scan; rule tiers (🔴 never degrade); false-positive feedback loop |
| **Meta-governance** | v1.4 | Event-driven audits; 30-day deprecation cooling period |
| **Lazy-load contract layer** | v1.1.0 | Description = contract (≤5 lines); body = detail (load on demand); prevents context crowding |
| **User workflow layer** | v1.0 | 用户自定义工作流蒸馏 → 叠加优先于标准流程(workflow-distillation) |

> 术语太硬?一句话版:路由决定用哪个 skill(15 秒),纪律保证写码安全(零成本),记忆防止重复踩坑(自动沉淀),审查兜底质量(一个命令),机制按需加载(省 token)。

---

## 📜 Version History

| Version | Theme | Highlights |
|---------|-------|-----------|
| v3.1 | Foundation | 3-layer disclosure, 18 self-built L3 skills, fallback protocol |
| v3.2 | System governance | L1 decision tree, L2 boundary declarations, skill type tags, scenario templates |
| v3.3 | Self-healing | Complexity Triage, snapshot health check, security audit, experience recall |
| v3.4 | Constraints & boundaries | Triage checklist, conflict-classified alignment, circuit breaker, cost awareness |
| v3.5 | Cognitive enhancement | knowledge-extraction, confirmation SLA, project-context weighting, smart /simple, meta-governance |
| v1.0.0 | Official release | Promoted from internal v3.6: trigger governance, lazy-load contract layer, execution-drift log, compatibility contract |
| **v1.1.0** | **Official release** | **大道至简 + 结构整改。四层组织路由;dev-assistant 副驾驶协议;quick-dev 轻量全包;合并 3 组 skill;一句话画像;契约层 ≤5 行** |
| **v1.2.0** | **Official release (current)** | **安全×质量×记忆×并行四线增强。安全三层防线(hook 实测拦 SQLi);AI 审查引擎(12s 发现 2 高危 bug);双层记忆(vuln/dev)+ 度量闭环;git-worktree 并行 + reverse-ops 授权闸门;doubt-driven + context-engineering 方法论;工作流蒸馏(用户自定义层);全链路实战验证(CachePilot 裁判全 10 分)** |

---

## 🧭 Design Philosophy

1. **大道至简 (Great Simplicity)** — token × 质量是乘积不是取舍;机制越少,加载越便宜且执行越准。删掉一个 skill 试试系统会不会崩溃。
2. **Enhancement, not dependency** — losing the family degrades the agent to plain mode; work continues.
3. **Automation, not impunity** — every auto action has a human-confirmation threshold; the final say belongs to the user.
4. **Evidence over imagination** — execution-drift logs, triage-accuracy logs, and ROI dashboards drive documentation iteration instead of author intuition.

---

## 🤝 Contributing

- New skills must carry the contract layer (trigger / negative_trigger / type / deps / key_rule), ≤5 lines.
- New skills need a 7-day cooling period and must prove they cannot be composed from existing skills (see `vibe-skills-gov-patterns`).
- Every rule change needs a Changelog entry: why it exists, which pain point it solves.
- Run scenario conflict simulation before promoting a new rule.
- Keep it honest: document what is convention vs. what is enforced.

## License

MIT License — see [LICENSE](LICENSE).
