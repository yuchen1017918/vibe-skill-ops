---
name: plan-workflow
description: |
  ⚠️ v1.3 deprecated — 由 project-init 取代（合并了骨架+计划+嗅探）。文件保留防交叉引用。
  计划工作流 skill：把用户需求拆分为可执行任务，写成结构化计划，
  并把计划持久化到项目根目录 .snapshots/plans/ 文件夹。
  当用户说"做个计划"、"拆分任务"、"规划一下"、"写个方案"、
  "列个待办"、或接手复杂多步任务时加载。
  与 snapshot-notes 配合：快照管状态，计划管任务。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, plan, task, breakdown, workflow, roadmap]
    related_skills: [vibe-coding-hub, snapshot-notes, dev-team, vibe-coding, project-scaffold]
---

# 计划工作流（Plan Workflow）

**核心闭环**：需求 → 任务拆分 → 结构化计划 → **存入项目根目录 .snapshots/plans/** → 逐步执行 → 更新计划。

## 📁 存储位置

```
<项目根>/
├── .snapshots/
│   ├── SNAPSHOT.md        # 项目状态快照（snapshot-notes 维护）
│   └── plans/             # ← 计划文件夹（本 skill 维护）
│       ├── PLAN-<日期>.md # 当前计划（每次更新覆盖）
│       └── archive/       # 历史计划归档
```

> 为什么放项目根目录：计划跟随项目走、随 git 走、跨对话可恢复，不依赖对话上下文。

## 🔄 工作流步骤

### Step 1: 需求确认
- 理解用户需求，1-2 句话复述确认
- 判断规模：小型（<5 任务）→ 精简计划；中大型 → 完整计划

### Step 2: 任务拆分（WBS）
把需求拆成可执行任务，遵循：
- **原子性**：每个任务可独立完成、可验证
- **依赖排序**：标出前置任务（先 A 后 B）
- **MoSCoW 分级**（中大型项目）：Must / Should / Could / Won't
- **验收标准**：每个任务有明确的"完成 = 什么"

### Step 3: 写计划文件
按模板生成 `PLAN-<日期>.md`，存入 `.snapshots/plans/`。

### Step 4: 执行与更新
- 按依赖顺序执行任务（配合 dev-team / vibe-coding 主流程）
- 每完成一个任务：更新计划中的 ✅ 状态
- 计划变更：更新而非重写，保留"变更记录"

### Step 5: 计划完成
- 全 ✅ 后归档到 `.snapshots/plans/archive/`
- 更新 `SNAPSHOT.md`（快照笔记）反映新状态

## 📝 计划模板

```markdown
# 计划 — <项目/任务名>

## 目标
<一句话：这次要达成什么>

## 任务列表
| # | 任务 | 优先级 | 依赖 | 验收标准 | 状态 |
|---|------|--------|------|----------|------|
| 1 | <任务> | Must | - | <完成=什么> | ⬜ |
| 2 | <任务> | Must | 1 | <完成=什么> | ⬜ |
| 3 | <任务> | Should | 2 | <完成=什么> | ⬜ |

## 执行顺序
1 → 2 → 3（标注可并行任务）

## 风险与依赖
- <风险点 / 外部依赖 / 待确认事项>

## 变更记录
| 日期 | 变更 | 原因 |
|------|------|------|
| <日期> | 初始计划 | - |

## 交接提示
- <接手者最需要知道的>
```

## 🧭 规模分支

### 小型任务（<5 个，快速）
精简计划：目标 + 任务表（#/任务/验收/状态）+ 执行顺序。直接写 PLAN 文件。

### 中大型任务（≥5 个，完整）
完整计划 + 建议接入 `dev-team`（有 MoSCoW/断点续传）或 `vibe-coding` 主流程。

## 🤝 与全家桶衔接

| Skill | 协作方式 |
|-------|----------|
| `snapshot-notes` | 快照管"项目状态"，计划管"任务清单"，互为补充 |
| `dev-team` | dev-team 的 Phase 0 文档发现会读 `.snapshots/`，计划可直接衔接 |
| `project-scaffold` | 新项目初始化时建好 `.snapshots/plans/` 目录 |
| `vibe-coding` | 5 步流程中的 Build 阶段按计划执行 |
| `plan`（L3） | 本 skill 是"计划工作流"，`plan` skill 是"写 markdown 计划文件"的底层工具 |

## 快速排障

| 症状 | 处理 |
|------|------|
| 任务拆太细 | 合并到"一次可交付"粒度，不拆到每行代码 |
| 任务有隐藏依赖 | 写计划时问"这个任务需要先有什么" |
| 计划过期 | 每次执行前检查 PLAN 文件，先更新再动手 |
| 找不到 plans 目录 | `mkdir -p .snapshots/plans/` 创建 |
