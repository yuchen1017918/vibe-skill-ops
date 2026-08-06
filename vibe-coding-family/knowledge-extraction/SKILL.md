---
name: knowledge-extraction
description: |
  知识萃取 skill：任务完成后自动从代码变更/报错/解决路径中识别可复用模式，
  转化为 global-experience 结构化条目，并驱动"萃取→验证→优化"闭环。
  与异常复盘联动：心跳熔断/故障后 24h 内自动执行 5 Whys 根因分析并萃取经验。
  当任务完成、异常发生、或需要"从这次经历学到什么"时加载。
  触发词：知识萃取、复盘、经验沉淀、post-incident、5 whys。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, knowledge, extraction, learning, review, post-incident]
    related_skills: [vibe-coding-hub, global-experience, agent-loop, snapshot-notes]
---

# 知识萃取（Knowledge Extraction）— 从实践中自动学习

**目的**：把"经验库"从"人工记录的笔记"升级为"系统自动生长的知识库"。
任务完成后自动识别模式 → 结构化沉淀 → 下次验证 → 越用越聪明。

## 🎯 萃取时机（自动触发）

| 时机 | 触发 |
|------|------|
| 任务完成（plan-workflow / agent-loop 收尾） | 回顾本次代码变更/报错/解决路径 |
| 异常发生后 24h 内 | 自动复盘 + 萃取根因经验 |
| 成功解决疑难 Bug | 提取"错误码→解法"模式 |

## 🔄 萃取流程

### Step 1：模式识别

分析：
- 代码变更（git diff）：新增了什么可复用模式？
- 报错信息：错误码/症状 → 解决路径是什么？
- 反复出现的操作：如"某 API 错误码需重试"、"某组件样式需覆盖"

识别候选模式，打标签：`#api-retry` / `#css-override` / `#dependency-trap` …

### Step 2：知识结构化

按 global-experience 模板写入（带 effectiveness_score 初评 + TTL）：

```markdown
## [YYYY-MM-DD] <模式一句话>
- **技术域**：<分类>
- **模式**：<可复用的做法>
- **症状/触发条件**：<什么情况下适用>
- **解法/做法**：<具体步骤>
- **验证命令**：<可复现的验证方式>
- **effectiveness_score**：0.7（初评，待验证）
- **验证次数**：0
- **TTL**：365d
- **来源**：<任务/异常 ID，可回溯>
```

> 门槛：score < 0.5 的模式不直接入库，先本地缓存（`.vibe/pending-experience/`），
> 二次确认后再入 global-experience——防经验库变垃圾堆。

### 质量门禁（v1.1 — 防"垃圾进，垃圾出"）

**每条经验必须包含四要素**（缺一不入库）：

```markdown
1. **触发条件 When**：精确到"什么报错信息 / 什么代码模式"
2. **解决方案 How**：可执行的步骤或代码片段
3. **验证命令 Verify**：一条可复现/验证的命令（如 `npm run test -- --grep="xxx"`）
4. **适用范围 Scope**：项目级 / 技术栈级 / 全局级（默认项目级，不得泛化）
```

**泛化升级流程**（防过度泛化）：
- 项目级经验被成功召回 3 次 → 可升级为技术栈级
- 技术栈级被成功召回 5 次 → 可升级为全局级
- 升级必须由用户或 governance 审查确认

**缓存清理**：
- score < 0.5 的缓存经验，7 天无确认 → 自动删除，不进入 global-experience

### 人工审核钩子（v1.1 — 人机协同，防"越用越乱"）

- **审核阈值**：萃取知识"匹配度 < 0.8"或"涉及核心业务逻辑" → 自动标记"待审核"，
  写入 `.snapshots/pending-knowledge/`
- **审核界面**：`project-tracker-dashboard` 增加"知识审核"看板，
  用户可一键"通过"或"拒绝"；拒绝时可选原因（过度泛化/错误关联），原因反馈给萃取模型
- **审核结果**：通过 → 入 global-experience；拒绝 → 删除并记录原因（防同类再犯）

### Step 3：验证闭环

- 下次遇到相似模式 → 自动召回（vibe-code-search 钩子）→ 应用 → 记录验证结果
- 验证成功：验证次数 +1，score 上调
- 验证失败：score 下调；30 天内同类异常再现 → 标记"未解决"并回到 Step 1

## 📋 异常后自动复盘（Post-Incident Review，与 agent-loop 联动）

异常发生后 24h 内（agent-loop 心跳熔断 / 用户报告）：

```
Step 1 信息聚合：异常报告 + 相关日志 + 当时 snapshot + git diff
                → .vibe/incidents/YYYY-MM/INC-{id}/
Step 2 5 Whys 引导：
  异常：<现象>
  Why 1：为什么？→ <答案>
  Why 2：为什么？→ <答案>
  …直到根因
Step 3 经验萃取：根因 → 结构化经验 → global-experience
   若根因是 skill 缺陷 → 创建 skill-patch 任务（改进全家桶自身）
Step 4 验证闭环：30 天内同类异常再现 → 标记"未解决"；
   未再现 → "已验证"，验证次数 +1
```

## 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `global-experience` | 萃取结果写入经验库（模板/评分/TTL） |
| `vibe-code-search` | 下次相似问题自动召回验证 |
| `agent-loop` | 异常触发复盘；复盘结果反馈指挥决策 |
| `snapshot-notes` | 复杂度校准/项目画像数据源 |
| `vibe-skills-gov-patterns` | 根因是 skill 缺陷时走治理流程 |

## 快速排障

| 症状 | 处理 |
|------|------|
| 萃取太多低价值经验 | 用 score 门槛过滤（<0.5 先缓存再确认） |
| 复盘被跳过 | agent-loop 异常后强制挂载，不可关闭 |
| 模式识别不准确 | 优先基于"已验证的报错+解决路径"，不猜 |
