---
name: cost-agent
description: |
  成本智能体 policy:每周一 token 消耗周报 + 实时告警 + ROI 看板 +
  证据消费(v1.2:走样/Triage 误判一句话洞察,月报强制决策)。
  当用户问"token 花了多少/哪个skill最费/本周消耗"时加载。
  触发词:成本、token消耗、周报、ROI、用量。
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: policy
    tags: [vibe-coding, cost, token, metrics, roi, dashboard]
    related_skills: [vibe-coding-hub, snapshot-notes, vibe-skills-gov-patterns]
---

# 成本智能体（Cost Agent）— 数据不躺着，要变成洞察和行动

**目的**：usage.log 只是记录，不是洞察。本 skill 把消耗数据变成周报/告警/ROI 决策。

## 📊 数据源

- `~/.vibe/metrics/usage.log`：skill 名/调用次数/预估 token（由 vibe-coding-hub Step 0.5 写入）
- `~/.vibe/metrics/triage-accuracy.log`：Triage 判定 vs 实际消耗（由 snapshot-notes 写入）
- `~/.vibe/metrics/security-drift.log`：安全走样（commit 前未过审计，由 hub Step 0.5/dev-core-hub 提交闸门写入，v1.3 新增）

## 📬 自动周报（每周一推送）

```
上周全家桶消耗：X token（≈$Y）
Top 3 开销：snapshot-notes (30%) / vibe-code-search (25%) / agent-loop (20%)
异常：周三某次 L0 任务实际消耗 12K token（超 L1 均值），建议检查 Triage 判定
建议：/simple 本周可节省预估 Z token，输入 /simple-once 试用
```

## 🚨 实时告警

- 单任务 token > 5K 且 Triage 判定为 L0 → 提示"该任务复杂度可能被低估"（反馈给 Triage 校准）
- 单日 token > 日均值 3 倍 → 提示"今日消耗异常，是否查看详情？"

## 📈 ROI 看板

- 每个 workflow 型 skill 记录：投入 token vs 产出（代码行数 / bug 修复数 / 时间节省）
- ROI 连续 2 周 < 0.5 的 skill → 黄色标记 → 建议 review 或替换（走 vibe-skills-gov-patterns）
- 看板数据由 vibe-skills-gov-patterns 月度治理会议消费

## 📈 证据消费（v1.2 — 数据要变成洞察和决策）

**目的**：走样日志/Triage 准确率日志躺在 ~/.vibe/drift/ 和 triage-accuracy.log 里没人看 = 没证据。
v1.2 起,周报/月报主动消费这些日志,驱动删减决策。

**周报加"一句话洞察"**（每周一推送,末尾固定段）：
```
【一句话洞察】
- 走样 Top 偏差：agent-loop 验证步骤被跳过 3 次（本周）→ 建议简化该步骤或改检查点
- Triage 误判：2 次 L0 判定实际消耗超 L1 均值 → 建议提升"脚本处理数据"类任务级别
- 安全走样（v1.3）：N 次提交未过安全审计（commit 前未跑 code-security 纪律/扫描）→ 建议安装 pre-commit hook 兜底（见 code-security references/pre-commit.yaml）
- 行动建议：下月删除/合并候选 [skill 名]（30 天未加载）
```

**月报强制决策**（每月最后一天,不输出洞察 = 违规）：
```
本月必答三问：
1. 哪些 skill 30 天未加载 → 标记 deprecated（vibe-skills-gov-patterns 执行）
2. 哪些机制步骤总被跳过 → 简化或删除（执行走样数据支撑）
3. 哪些合并候选 → 执行/否决（触发词重叠数据支撑）
4. 安全走样趋势（v1.3）：跳过审计次数上升？→ 默认纪律是否失效/hook 未装 → 落实 code-security 第一层或装 hook
```

**证据可消费性标准**：每条洞察必须 = 一句话发现 + 数据来源 + 行动建议；
不产出"看了等于没看"的原始数据堆。

## 🧮 观测者豁免与分层记账（v1.1 — 防自我测量递归）

**目的**：cost-agent 自身运行也耗 token；告警链可能递归（cost → knowledge → cost）。
不豁免的话，纸面消耗被放大，周报失真。

**豁免列表（不计入开发成本）**：
- cost-agent 自身的运行消耗
- vibe-skills-gov-patterns 的元治理审查消耗
- knowledge-extraction 的"复盘"类操作（属治理成本）

**分层记账**：
```
【开发成本】直接服务任务的 skill（project-init/vibe-coding/snapshot 等）
【治理成本】维持全家桶运转的 skill（cost-agent/governance/knowledge-extraction 复盘）
【总成本】开发 + 治理
周报默认展示"开发成本"，展开后显示"治理成本占比"
```

**递归阻断**：
- 任何 skill 在 1 分钟内被同一上游 skill 二次触发 → 标记"可能的递归调用" → 告警但不阻断
- 用户可配置 `max_governance_cost_ratio: 0.2`（治理成本 > 总成本 20% → 告警）

## 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `vibe-coding-hub` | Step 0.5 写入 usage.log；本 skill 消费 |
| `snapshot-notes` | 复杂度校准数据源；告警反馈 Triage 校准 |
| `vibe-skills-gov-patterns` | ROI 低的 skill 走治理流程（review/替换/废弃） |

## 快速排障

| 症状 | 处理 |
|------|------|
| usage.log 没数据 | 检查 Step 0.5 是否启用记录 |
| 周报没人看 | 接入通知渠道（Telegram/QQ）推送摘要 |
| 告警太吵 | 调阈值：单任务 5K→10K，单日 3x→5x |
