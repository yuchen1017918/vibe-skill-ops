---
name: workflow-distillation
description: |
  工作流蒸馏 skill：用户输入自己的工作流程（描述/步骤/文档/演示对话），
  agent 分析蒸馏成可复用的用户工作流 skill（含触发词/步骤/决策表/验证），
  注册进全家桶作为"用户自定义层"，与全家桶标准工作流融合共存——完全保留
  全家桶原本的工作流，用户的工作流优先。当用户说"把我的流程做成skill"、
  "记住我干活的方式"、"以后按这个流程来"、或提供流程描述/文档时加载。
  触发词：工作流蒸馏、把我流程做成skill、记住我干活的方式、自定义工作流、流程沉淀。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, workflow, distillation, skill-authoring, user-custom, fusion]
    related_skills: [vibe-coding-hub, requirement-clarify, skill-creator, context-engineering, snapshot-notes, dev-team, quick-dev]
---

# 工作流蒸馏（Workflow Distillation）— 用户工作流 → 可复用 skill，与全家桶融合

**目的**：用户描述自己干活的方式，agent 蒸馏成一套**可执行工作流 skill**，注册进全家桶
作为"用户自定义层"。全家桶标准工作流**原样保留**，用户工作流**叠加优先**——两者融合共存。

> 方法论参考：cangjie-skill（book-to-skill 蒸馏：并行提取/三重验证/RIA++ 构造/压力测试）
> + skill-creator（意图捕获/访谈）+ colleague-skill（从描述蒸馏可执行 skill 包）。
> 本 skill 的差异化 = **融合注册机制**：产物不是孤立 skill，而是与全家桶双向链接的用户层。

## 何时调用

- "把我的流程做成 skill" / "记住我干活的方式" / "以后按这个流程来"
- 用户提供工作流程描述（自然语言步骤 / 文档 / 往期对话记录 / 演示）
- 用户说"自定义工作流"、"流程沉淀"

## 核心原则：叠加不覆盖

| 原则 | 说明 |
|------|------|
| **不动全家桶** | 用户工作流放独立目录 `~/.hermes/skills/user-workflows/`，全家桶文件零修改 |
| **用户优先** | hub 场景表"用户自定义"区优先级最高：用户流程 > 标准流程 |
| **双向链接** | 生成的 skill related_skills 自动映射全家桶对应 skill（子步骤可调用标准 skill） |
| **验证后再用** | 压力测试（应调用/不应调用）通过才注册，防止乱触发 |

## 蒸馏流程（5 步）

### Step 1：结构化访谈（≤10 分钟，借鉴 requirement-clarify）

问清四件事（有答案就跳过，不重复问）：
1. **目标**：这个工作流最终产出什么？（一句话）
2. **步骤**：从头到尾的步骤序列？哪些是**必做**、哪些是**可跳过**？
3. **输入/输出**：每一步吃什么、吐什么？（格式/路径/工具）
4. **触发**：什么情况下该用这个流程？（用户会怎么说、什么场景）
5. **验证**：怎么知道做对了？（测试/检查/用户确认点）

> 来源可以是：对话历史（提取工具序列+用户纠正）、文档、演示记录、用户口述。

### Step 2：流程提取（借鉴 cangjie 阶段 1-2）

把访谈结果转成结构化流程：
- **步骤序列**：编号步骤 + 每步动作 + 输入输出 + 依赖工具
- **决策点**：流程里"如果 X 就走 A，否则走 B"的分支
- **验收标准**：每步/整体的通过条件
- **关键坑**：用户强调过的"别这样做"（从纠正中提取）

### Step 3：生成用户工作流 SKILL.md

用 RIA++ 简化模板写入 `~/.hermes/skills/user-workflows/<workflow-name>/SKILL.md`：

```markdown
---
name: <workflow-name>
description: |
  <用户工作流一句话>。步骤：<步骤摘要>。当<触发场景>时使用。
  触发词：<用户习惯的说法>。
version: 1.0.0
author: user-custom
metadata:
  hermes:
    type: workflow
    related_skills: [<自动映射的全家桶 skill>]
---
# <工作流名>（用户自定义）

## 触发时机
<什么时候用>

## 执行步骤（<N> 步）
### Step 1: <动作>
- 输入: <...> → 输出: <...>
- 工具: <...>
- 验收: <...>
### Step 2: ...
（决策点用表格或 if/else 标注）

## 关键坑（用户强调）
- <从用户纠正中提取的"别这样做">

## 与全家桶衔接
- 步骤 X 可调用 `vibe-coding`（标准开发流程）
- 步骤 Y 可调用 `release-ops`（标准发布流程）
```

**自动映射规则**（生成时检查步骤内容 → 加 related_skills）：
| 步骤特征 | 映射 |
|---------|------|
| 写代码/改代码 | `vibe-coding` / `dev-core-hub` |
| 调试/疑难 Bug | `systematic-debugging` |
| 发布/版本 | `release-ops` |
| 多 Agent 协作 | `agent-ops` / `dev-team` |
| 数据/分析 | `dev-ai-hub` |
| 安全相关 | `code-security` / `security-audit` |

### Step 4：融合注册（本 skill 核心差异化）

1. **hub 场景表**加"用户自定义"行（优先级最高区）：
   ```
   | 用户自定义 | `user-workflows/<name>`（用户层，优先于标准） | "<用户触发词>" |
   ```
2. **hub 计数**更新（28 → 29 + 用户层数量）
3. 生成的 skill 保留在 `user-workflows/`（不进全家桶目录，防冲突）
4. 告知用户：全家桶原有工作流**零改动**，用户流程已叠加

### Step 5：压力测试（借鉴 cangjie 阶段 4）

设计 3-5 条测试 prompt：
- **应调用**：触发词场景 → 应加载该用户流程
- **不应调用（诱饵）**：相似但不同的场景 → 不应加载（防止乱触发）
- **边界模糊**：模棱两可场景 → 判断是否符合触发条件

未通过的 → 回 Step 3 调整 description/触发词，不做表面修补。

## 交付

- 报告：产物路径 + 触发表 + 与全家桶衔接图（哪些步骤用了标准 skill）
- 演示：用 1 个真实触发词跑一遍（验证确实可用）
- 建议用户用 3 次真实任务后回来调优（联动 snapshot-notes 复盘）

## 质量红线

1. **不覆盖**：绝不修改全家桶已有 skill（只加用户层）
2. **触发词明确**：description 必须写清触发场景，不能是"一个关于 X 的 skill"
3. **验证前置**：测试通过才注册进 hub
4. **不凭记忆**：用户没给全流程时先访谈问清，不脑补步骤
5. **7 天冷静期**：新用户工作流先试用，稳定后才算正式（联动 vibe-skills-gov-patterns）

## 快速排障

| 症状 | 处理 |
|------|------|
| 用户流程太模糊 | 用具体例子引导：上次你是怎么做的？从哪步开始？ |
| 与全家桶 skill 重叠 | 保留用户流程（用户习惯优先），related_skills 指向标准版 |
| 触发词抢词 | 用户自定义层优先（hub 仲裁规则 0） |
| 流程太复杂 | 拆成 2-3 个原子流程，各自独立触发词 |
