---
name: vibe-coding-hub
description: |
  Vibe-Coding Skill 全家桶 L1 总目录 — 四层组织路由入口。
  当用户提到 vibe coding、快速开发 MVP、迭代式写代码、skill 全家桶、
  或需要"这个开发任务该用哪个 skill"时，先加载本 skill。
  四层路由：L1 组织形态(团队/企业) → L2 开发模式(助手/全盘) → L3 四格场景 → L4 执行 skill。
version: 1.1.0
author: Hermes Agent (基于真实 GitHub 项目 + 本地 skill 库整合)
license: MIT
metadata:
  hermes:
    tags: [vibe-coding, hub, directory, workflow, family, dev]
    related_skills: [dev-core-hub, dev-stack-hub, dev-infra-hub, dev-agent-hub, dev-ai-hub, vibe-coding, dev-team, snapshot-notes, project-init, agent-ops, release-ops, agent-loop, agent-permissions, global-experience, china-env-adapt, fallback-general-dev, dev-assistant, quick-dev, requirement-clarify]
---

# Vibe-Coding Skill 全家桶（L1 总目录 v1.1.0 — 四层组织路由）

你是全家桶的**总目录页**。四层组织路由结构（v1.2 重构 — 组织形态驱动，替代旧三层）：

```
L1  组织形态   团队(轻量项目)              企业(大型项目)
              ┌──────────────┐           ┌──────────────┐
L2  开发模式   │ 助手 │ 全盘  │            │ 助手 │ 全盘  │
              └──────────────┘           └──────────────┘
L3  细分场景   场景模板表（四格场景，见下方四格场景表）
L4  执行 skill 具体 skill（含 dev-assistant / quick-dev / dev-team…）
      ↕ 技术分类 hub 下移为二级索引（dev-core/stack/infra/agent/ai，按需进入）
```

**路由优先级**：先问"什么规模的活"(L1 组织形态)，再问"谁主导"(L2 开发模式)，
然后落场景(L3)，最后才是具体 skill(L4)和技术索引。

**本层只路由，不罗列 L3/L4 细节。**

## 🗂 技术分类索引（v1.2 下移 — 二级索引，非路由主层）

> 旧三层结构中的 L2 分类目录，v1.2 起**下移为二级索引**：先走组织路由（L1→L2→L3），
> 落到具体场景后，再按技术类型进对应分类目录找 skill。

| 技术索引 | 管什么 | 进入时机 |
|---------|--------|----------|
| `dev-core-hub` | 主流程四选一 + 编码纪律 + 调试 + 测试 + 版本控制 | 落到场景后需要编码/调试/测试/提交时 |
| `dev-stack-hub` | 编程语言 + 前端/UI + 数据库 + 移动端 + 游戏引擎 + Web3 | 技术栈已确定 |
| `dev-infra-hub` | 终端安全 + 容器 + MCP 生态 + 部署/DevOps + 安全 | 跑命令/容器/MCP/部署上线/安全审查 |
| `dev-agent-hub` | Agent 编排 + AI 编码器委派 + 代码搜索 + skill 治理 | 多Agent协作/委派外部编码器/大项目检索/治理 |
| `dev-ai-hub` | 模型训练/微调 + 推理部署 + 提示词/RAG + 多模态 | 项目涉及 AI/ML 功能时 |

> 技术栈纪律摘要(v1.3):进入技术索引后,只加载对应技术段的**纪律摘要 ≤5 条**(首行),
> 不全文加载。技术栈由 project-init 嗅探写入 .vibe/stack.yaml 自动激活。

## 🏷 技能类型标签（v3.2 新增 — L3 四类划分）

所有 L3 skill 的 frontmatter `metadata.hermes.type` 标注类型，决定调用方式：

| 类型 | 含义 | 调用方式 | 自建 L3 示例 |
|------|------|----------|--------------|
| `tool` | 做一件具体事，有明确输入输出 | 按需显式调用 | snapshot-notes / security-audit / project-scaffold / china-env-adapt |
| `workflow` | 管一段流程，有阶段和状态 | 阶段推进式调用 | plan-workflow / agent-loop / knowledge-extraction |
| `policy` | 注入纪律/约束，持续生效 | 自动注入上下文 | karpathy-coding-dscpln / vibe-terminal-safe / agent-permissions / frontend-design-policy / cost-agent |
| `meta` | 管其他 skill 的行为 | 系统级自动触发 | fallback-general-dev / vibe-skills-gov-patterns |

> 27 个自建 L3 全量标注：tool 11 个 / workflow 8 个 / policy 6 个 / meta 2 个（v1.3 合并 3 组净减 3；v1.2 安全线新增 code-security；v1.3 新增 open-code-review 审查引擎 + vuln-memory 漏洞记忆 + dev-memory 开发记忆 + reverse-ops 逆向路由）。
> 已合并 deprecated（文件保留防交叉引用）：project-scaffold+plan-workflow → project-init；
> agent-workspace+agent-collab → agent-ops；release-management+rollback-backup → release-ops。

## 🚀 四层路由流程（v1.2 — 组织形态驱动）

```
用户需求
  │
  ▼
L1 组织形态判定：团队 or 企业？
  │  判定三维：模块数(1-2=团队,3+=企业) / 专业角色需求 / 交付周期(天级=团队,周月级=企业)
  │  辅助：Triage 复杂度清单（Step 0）—— L0 裸奔（快进快出）、L1 团队、L2 企业
  ▼
L2 开发模式判定：助手 or 全盘？
  │  助手：用户是司机（主导方向）→ dev-assistant
  │  全盘：用户是老板（给方向、看进度）→ 看组织形态
  ▼
L3 四格场景（见下方四格场景表）→ 落具体工作形态
  │
  ▼
L4 执行 skill（dev-assistant / quick-dev / dev-team / vibe-coding…）
  │
  ▼
技术二级索引（dev-core/stack/infra/agent/ai，按需进入找具体语言/工具 skill）
```

## ⚡ 一句话画像（v1.3 新增 — 路由压缩，四层体验压缩为三层）

> 四层决策链过长?**一句话画像**锁定 L1+L2,后续反驳只更新画像,不重走路由。

```
【组织】【主导】【类型】【技术】
  团队     助手     局部实现    Python
  企业     全盘     Bug修复     TS/React
                   …
```

**使用方式**:
1. 任务到达 → 15 秒内填出画像(组织/主导 两问定 L1+L2,类型/技术 两问定 L3/索引)
2. 画像即路由:【团队·助手】→ dev-assistant 轻档;【团队·全盘】→ quick-dev / vibe-coding
3. 用户反驳 → **只更新画像字段**,不重新走完整判定
4. 画像写入工作记忆(会话内),同类型后续任务直接复用

## 🚀 默认路径化（v1.3 新增 — 常见任务免判断直走）

| 用户说 | 免判断直走 | 不经过的判定 |
|--------|-----------|--------------|
| "帮我看看"/"帮我review"/"这bug怎么改" | dev-assistant L3 档 | L1/L2 判定省略 |
| "随手做个"/"写个脚本" | quick-dev L1 档 | L1/L2 判定省略 |
| "新建项目"/"做个计划" | project-init | L1/L2 判定省略 |
| "发布"/"回滚" | release-ops | L1/L2 判定省略 |
| "组队开发"/"自动开发" | dev-team | 仅确认规模(企业级) |
| "用codex干活"/"让claude code写" | dev-agent-hub → codex-agent / claude-code | 仅外部编码器委派;验证纪律照常 |

> 边界感:默认路径只在**无歧义**时生效;触发词打架 → 走触发词治理仲裁。

## 🧭 复杂度分层（v3.3 — 先判复杂度，再走组织路由）

### Step 0：复杂度评估（Triage，v3.4 升级 — 判定清单替代主观判断）

**执行方式**：逐题回答 是/否，按分支走。不要凭"感觉"分级。

```
问题 1：是否只涉及单个文件的纯内容修改（文案/注释/常量值）？
  ├─ 是 → 问题 2
  └─ 否 → 进入 L1 判定（问题 3）

问题 2：该文件是否被其他文件 import/引用？
  ├─ 是 → 升级 L1（边界不清）
  └─ 否 → L0 快进快出

问题 3：是否涉及数据库 schema / API 契约 / 配置文件格式变更？
  ├─ 是 → 直接 L2
  └─ 否 → 问题 4

问题 4：是否涉及 3 个以上模块的联动修改？
  ├─ 是 → L2
  └─ 否 → 问题 5

问题 5：是否涉及生产敏感操作（支付/权限/安全相关）？
  ├─ 是 → L2 + 强制 security-audit
  └─ 否 → L1（固定三件事：明确边界 → 步骤追踪 → 完成前验证）
```

| 级别 | 处理方式 |
|------|----------|
| **L0 微小改动** | 跳过 plan-workflow，直接 tool 级快进快出，不上全套 |
| **L1 中等功能** | 三件事：明确边界 → 步骤追踪 → 完成前验证 |
| **L2 高风险/核心链路** | 完整流程：dev-team + agent-loop + plan-workflow，买确定性 |

> 误判护栏：L0 任务中途发现牵连（import 链/多文件）→ 立即升级 L1/L2，不硬撑。
> 校准机制：任务完成后记录"实际耗时 vs 初始判定"（见 snapshot-notes 复杂度校准），
> 同类任务多次低估 → 自动提升该类型级别。

### Step 0.5：成本意识 + /simple 智能降级（v3.5 升级）

```
【成本提示】workflow 型任务开始时评估：本次预计触发几个 skill，预估 token 消耗范围。
- 判定 L0/L1 → 不加载 plan-workflow / agent-loop 全套
- 记录 ~/.vibe/metrics/usage.log（skill 名/调用次数/预估 token），月度复盘
- 提交动作时：未过 security-audit/code-security 纪律 → 追加 ~/.vibe/metrics/security-drift.log（时间/原因），cost-agent 周报消费（v1.3 度量闭环）
```

**/simple 智能降级**（v3.5 — 从"一刀切"到"可配置策略"）：

| 策略 | 跳过内容 | 保留内容 |
|------|----------|----------|
| `/simple` | 全套精简 | 只跑核心链路 |
| `/simple-no-recall` | 经验主动召回 | Triage + 安全审计 |
| `/simple-no-design` | 设计系统校验 | 召回 + 审计 |
| `/simple-no-audit` | 安全审计（降 Level 1） | 召回 + 设计 |
| `/simple-once` | 本次会话生效，下次恢复 | — |

- 自定义策略：用户可配置 `~/.vibe/simple-config.yml`（如"跳过召回但保留审计"）
- 策略推荐：成本提示时按任务类型主动推荐（UI 调整 → `/simple-no-design`；纯文案 → `/simple`）
- `/focus 30m` 免打扰窗口对通知型确认自动生效

### Step 1：组织形态判定（L1 — 团队 or 企业）

```
判定三维（不必全满足，多数满足即定）：
  1. 模块数：1-2 个 = 团队；3+ 个 = 企业
  2. 专业角色：只需通用开发 = 团队；要专门架构/运维/安全 = 企业
  3. 交付周期：天级 = 团队；周/月级 = 企业
辅助：Triage 复杂度清单（Step 0）—— L0 裸奔（快进快出）、L1 团队、L2 企业
```

### Step 2：开发模式判定（L2 — 助手 or 全盘）

```
谁主导？
  ├─ 用户主导（司机）→ 助手模式 → dev-assistant（团队·轻 / 企业·重 双参数）
  └─ 用户给方向、看进度（老板）→ 全盘模式 → 按组织形态选：
       ├─ 团队·全盘 → quick-dev（随手做）或 vibe-coding（单人 MVP 项目）
       └─ 企业·全盘 → dev-team（完整多Agent流水线）
```

## 🚀 四格场景表（v1.2 — L3 细分场景）

> 场景 = 预设 skill 组合 + 入口指令。先定组织形态(团队/企业)与开发模式(助手/全盘)，
> 再落四格中的场景。L3 是**路由表**，不新增独立文档；具体执行看 L4 skill。

| | 🧑💻 助手(用户=司机) | 🧑💼 全盘(用户=老板) |
|---|---|---|
| **🏠 团队**<br>(轻量项目) | `dev-assistant`(轻参数)<br>局部实现·Bug定位·审查·答疑·小重构·写草稿<br>入口:"帮我看看"/"帮我review"/"帮我实现XX" | `quick-dev`(随手做) / `vibe-coding`(单人MVP)<br>小工具·脚本·迷你交付·一次性任务<br>入口:"随手做个"/"写个脚本";"做个MVP" |
| **🏢 企业**<br>(大型项目) | `dev-assistant`(重参数)<br>模块开发·系统重构·架构建议·跨模块审查·性能优化<br>入口:"帮我重构"/"帮我优化" | `dev-team`(完整流水线)<br>Phase 0-5·乙方交付·验收驱动<br>入口:"组队开发"/"自动开发"/"dev-team" |

**通用场景**(跨四格，按需加载)：

| 场景 | 加载的 skill 组合 | 入口指令 |
|------|------------------|----------|
| 需求澄清/方向对齐(全盘模式前置) | `requirement-clarify` + `project-init` | "先问清楚" / "grill me" / 模糊需求 |
| 疑难 Bug | `systematic-debugging` + `vibe-code-search` | "有 Bug" / "调试" |
| 新建项目/初始化+计划 | `project-init`（v1.3 合并，含嗅探） | "新建项目" / "脚手架" / "做个计划" |
| 跨对话恢复进度 | `snapshot-notes` | "继续上次" / "别丢上下文" |
| 发布/打版本/回滚 | `release-ops`（v1.3 合并）+ `security-audit` | "发布" / "打版本" / "回滚" |
| 安全扫描/防漏洞 | `code-security` + `security-audit`（提交闸门） | "扫漏洞" / "安全检查" / 提交前 |
| 漏洞记忆/防重复踩坑 | `vuln-memory`（漏洞沉淀→生成避坑） | "记住这个漏洞" / "踩坑记录" / 扫描后自动 |
| 开发记忆/开发坑 | `dev-memory`（开发细节教训沉淀→按需召回） | "记住这个开发坑" / "API怎么用" / "之前怎么解决的" |
| 逆向/渗透/安全研究 | `reverse-ops`（授权闸门+任务路由，轻量版借鉴 reverse-skill） | "逆向" / "反编译" / "渗透" / "CTF" / "抓包" |
| 审查代码/Review | `open-code-review`（执行引擎）+ `code-review`（方法论） | "审查代码" / "review" / "审查PR" |
| 国内环境适配 | `china-env-adapt` + `project-scaffold` | "换源" / "国内环境" |
| 路由失败/兜底 | `fallback-general-dev`（自动触发） | 无需指令 |

### 单点直达（场景模板外的专项需求）

| 需求 | 直达 |
|------|------|
| 跑 build/test | `dev-infra-hub` → `vibe-terminal-safe` |
| 大项目定位代码 | `dev-agent-hub` → `vibe-code-search` |
| 拆分任务/做计划 | `dev-core-hub` → `project-init`（v1.3 合并） |
| 需求澄清/先问清楚 | `dev-core-hub` → `requirement-clarify` |
| 副驾驶/帮我看看 | `dev-core-hub` → `dev-assistant`（助手模式） |
| 随手做/写脚本 | `dev-core-hub` → `quick-dev`（团队·全盘） |
| 项目可视化/看板 | `dev-core-hub` → `project-tracker-dashboard` |
| 跨项目经验沉淀 | `dev-agent-hub` → `global-experience` |
| 多Agent工位+协作 | `dev-agent-hub` → `agent-ops`（v1.3 合并） |
| 无人自动开发 | `dev-agent-hub` → `agent-loop`（配合 dev-team） |
| 权限/职责/安全红线 | `dev-agent-hub` → `agent-permissions` |
| AI/ML 训练或推理 | `dev-ai-hub` → `huggingface-hub` / `vllm` |
| 部署/上线/回滚 | `dev-infra-hub` → `cloud-deployment` + `release-ops` |
| 建定时任务 | `dev-infra-hub` → `hermes-cron-patterns` |
| 需要 MCP 文件/git 能力 | `dev-infra-hub` → `vibe-mcp-connect` |
| Python 项目 | `dev-stack-hub` → `python3` + `py` |
| Web UI 设计 | `dev-stack-hub` → `frontend-design` |

## 🚨 通用降级协议（v3.1 新增 — 路由失效时自救）

```
当 L1/L2 路由失败、skill 加载异常、或不知道用哪个 skill 时：
1. 自动加载 fallback-general-dev（三步基本盘：写代码→git→测试）
2. 具体 skill 执行报错 ≥3 次 → 激活 vibe-terminal-safe 安全模式（仅只读命令）
3. 降级事件记录到 .snapshots/ + 输出降级报告
4. 不陷入死循环：最多降级 2 层，仍失败 → 保存状态等用户
```

> 全家桶是"增强"不是"依赖"：路由失效也能继续干活。

## 🎯 触发词治理（v3.6 新增 — 33 个 skill 的信号仲裁）

**目的**：多个 skill 抢同一个关键词（"继续"→snapshot？"复盘"→knowledge？），
没有仲裁机制会全加载（上下文爆炸）或随机选（行为不可预测）。

**命名空间规则**：
| 类型 | 词 | 归属 |
|------|-----|------|
| 全局保留词 | "全家桶"、"按流程"、/simple、/focus、/mode | hub / meta skill 独占 |
| 场景保留词 | "发布"、"MVP"、"疑难 Bug" | 场景模板独占 |
| 自由竞争词 | "快照"、"审计"、"熔断" | L3 skill 可用 |

**冲突仲裁优先级**（多 skill 触发词同时命中时）：
1. 场景模板 > 单个 skill（"发布"优先命中 release 场景模板，而非 security-audit）
2. workflow > tool（"计划"优先 plan-workflow，而非 project-scaffold）
3. 最近使用 > 历史记录
4. 仍不确定 → **显式消歧**：列出候选让用户选，或 /all 全加载

**上下文增强**（触发词不是死匹配）：
- **触发词+上下文绑定**：knowledge-extraction"复盘"仅"任务完成且 git diff 非空"时生效；cost-agent"成本"仅"会话 token > 3K"时生效
- **负向触发词**：security-audit 遇"草稿/测试/临时"不触发；任何 skill 定义 negative_trigger 防误触发

## 📦 懒加载与契约层规范（v3.6 新增 — 防上下文挤占）

**原则**：description 是**契约层**（≤5 行，v1.3 从 ≤10 行压缩，常驻可见）；正文是**细节层**（按需读取，用完即释放）。

**契约层必须包含**（写进 frontmatter description）：
```
trigger: 触发词（合并后 ≤3 个核心词）
negative_trigger: 负向触发词（防误触发）
type: 类型标签
deps: 依赖 skill（进入该阶段时懒加载）
key_rule: 一条必须记住的核心规则
```

> v1.3 大道至简：契约层压缩至 ≤5 行，31 skill × 5 行 ≈ 155 行常驻（较原 310 行减半）。

**加载策略**：
- 初始：只读契约层（skills_list / description），**不全文加载**
- 进入具体阶段 → 按 deps 懒加载细节层（skill_view 正文）
- 细节用完即压缩为摘要，不常驻上下文

> 新 skill 必须带契约层；存量 skill 逐步补齐（优先核心 workflow）。
> 这也是"少即是多"的落地：上下文窗口里永远只放契约，不放全文。

## 📉 执行走样日志（v3.6 新增 — 文档被遵循的证据）

**目的**：全家桶设计了很多精巧机制（熔断器/冲突四分类/信任链），但没有任何机制知道 Agent 实际执行时走了多少样。没有执行数据，文档迭代只能靠"作者想象"。

**原理**：不监控（无后台进程），而是**检查点自检**。

- **定义检查点**：关键 workflow skill（agent-loop / plan-workflow / release-management）在文档中定义 2-4 个检查点：
  ```yaml
  # agent-loop 预期路径示例
  checkpoints:
    - step: "委派前"
      verify: "是否生成 Trust Token？"
    - step: "子Agent返回后"
      verify: "是否执行了回归/交叉/渐进验证之一？"
    - step: "异常时"
      verify: "是否进入 OPEN 状态？"
  ```
- **自检时机**：snapshot-notes 会话摘要中，Agent 自检"本次是否走了预期路径"；
  knowledge-extraction 复盘阶段检查"实际执行 vs 规范"偏差
- **落盘**：偏差写入 `~/.vibe/drift/`（轻量文本，不建复杂 schema）
- **月度汇总**（用户主动要求时）："agent-loop 加载 12 次，3 次未执行验证步骤 → 该步骤设计太复杂，建议简化"

> 目的不是追责，而是**用执行数据指导文档简化**——某步骤总被跳过，说明它该删或该拆。
> 这是"少即是多"的证据闭环：不是让文档更厚，而是让文档被遵循的证据更可见。

## 📋 确认交互契约 v1.0（v3.5 新增 — 人工确认的 UX 契约）

**目的**：全家桶多处要求"人工确认"，但缺少统一交互契约 → 确认疲劳（习惯性点"是"）或确认逃避（直接 /simple 跳过）。以下契约统一所有确认场景（快照对齐/终端命令/审计放行）。

| 类型 | 适用场景 | 行为 | 超时策略 | UX |
|------|----------|------|----------|-----|
| **阻塞型 Blocking** | 🔴 双向漂移、🔴 系统级终端命令 | 必须等用户输入 YES/NO | 10 分钟无响应 → abort，状态存 `~/.vibe/pending/` | 高亮红色横幅 + diff 预览 |
| **通知型 Notify** | 🟡 快照超前、🟠 git 超前 | 推送通知，30 秒无回复按默认策略 | 默认：🟡=否（不应用快照）、🟠=是（更新基线） | 右下角轻量提示，可展开 |
| **批量型 Batch** | 同类冲突 ≥3 个 | 合并为一个确认单 | 列出影响文件数 + 预估风险 | 选项：全部应用/逐条审查/全部跳过 |

**免打扰窗口**：
- `/focus 30m` → 30 分钟内通知型确认自动按默认策略执行
- 阻塞型仍强制弹出（可延迟到 focus 结束后）

> 原则：阻塞型守住数据安全底线，通知型保效率，批量型防疲劳。

## 🌱 新手梯度 v2.0（v3.6 升级 — 连续梯度，不是阶梯跳跃）

**目的**：v1.0 按"对话次数"切换会出"第 11 次悬崖"（突然面对 28 个 skill 全量复杂度）。
v2.0 改按**已掌握概念数**，且每层都有缓冲。

**梯度分层**（按"成功完成过完整流程"的 skill 数，不是加载过）：
| 已掌握 | 模式 | 暴露内容 |
|--------|------|----------|
| 0-3 个 | 极简 | 3 入口：vibe-coding / fix-bug / new-project |
| 4-6 个 | 基础 | + snapshot-notes、plan-workflow |
| 7-10 个 | 标准 | + Triage、security-audit |
| 11-15 个 | 进阶 | + agent-loop、knowledge-extraction |
| 16+ 个 | 完整 | 全部暴露 |

**掌握判定**：成功完成过一次完整流程（由 snapshot-notes 记录实际使用历史），
不是"加载过就算掌握"。

**手动覆盖**：
- `/mode beginner` / `/mode standard` / `/mode full`
- 覆盖后记住偏好，不再自动切换
- 概念首次出现仍必须附带"为什么我需要知道这个"（认知保护原则不变）

## 🔗 兼容性声明（v3.6 新增 — 防文档间语义断裂）

**目的**：hub v1.2 可能引用 agent-loop v1.4 的"信任令牌"，但用户若还是 v1.3（无该概念），
引用即悬空。版本不匹配 = Agent 读到"请按信任链验证"但 skill 里没有，直接懵掉。

**契约**：
- 每个 skill 的 frontmatter 可声明依赖（存量逐步补齐，新 skill 必须带）：
  ```yaml
  requires:
    hub: ">=3.4"      # 需要 vibe-coding-hub 最低版本
    skills:           # 依赖 skill 最低版本
      - name: agent-permissions
        version: ">=1.0"
  ```
- 加载 L3 前检查 requires；不匹配 → 提示"部分功能可能失效"，**不阻断**（符合增强不是依赖）
- 月度打快照 `vibe-coding-family/.vibe/versions.lock`（记录全家桶所有 skill 精确版本）
- `/rollback-family 3.5` → 按 versions.lock 回退到上一版本组合

## 🌱 大道至简（v1.3 — 设计哲学升级）

**token × 质量 = 乘积最优,不是取舍**:
- token 消耗 ≈ 加载的机制量;质量 ≈ 机制被遵循的程度
- 机制越多 → 加载越贵(token↑)且走样越多(质量↓)= **双输**
- 机制越少 → 加载便宜(token↓)且执行越准(质量↑)= **双赢**

**落地动作(减法)**:
1. 合并 3 组重叠 skill → 净减 3(加载决策变少、歧义消除)
2. 契约层 ≤5 行(常驻减半)
3. 一句话画像 + 默认路径化(判定次数减少)
4. 30 天未加载 → 标记 deprecated(从索引移除,文件保留)
5. 证据消费驱动删减(周报一句话洞察)

> 简化不是偷懒——是唯一同时优化 token 与质量的路。

## 全局底线（所有层通用）

1. **主流程唯一**：一次只走 `dev-assistant` / `quick-dev` / `vibe-coding` / `dev-team` 之一，不叠加。
2. **改前看 git，改后 diff，重要改动 commit**。
3. **终端过白名单**：禁 `rm -rf`/`sudo`/`mkfs`/`dd`（除非用户明确要求）。
4. **报错不臆测**，跑命令拿真实错误；小步迭代，不一次性大规模重写。
5. **大项目不全文塞上下文**，用 `vibe-code-search` 检索。

## 来源说明（真实可验证，2026-08-06 复核）

- 官方 MCP servers：https://github.com/modelcontextprotocol/servers （⭐89k）
- Hermes 主仓库：https://github.com/NousResearch/hermes-agent
- Aider：https://github.com/Aider-AI/aider （⭐30k+）
- OpenVibeCoding：https://github.com/TencentCloudBase/OpenVibeCoding
- vibekit：https://github.com/superagent-ai/vibekit
- Undermybelt/hermes-skills（1422 个 SKILL.md）：https://github.com/Undermybelt/hermes-skills
- RobinBeraud/hermes-skills：https://github.com/RobinBeraud/hermes-skills
- 其余为本地已装 skill（software-development / github / devops / mcp / creative 等分类）

> ⚠️ 已复核为 404 不存在的链接：`anthropics/mcp-code-search`、
> `wong2/mcp-server-typescript-check`、`joewing/mcp-server-python-linter`、
> `paul-gauthier/aider-chat`（正确名 Aider-AI/aider）等。
