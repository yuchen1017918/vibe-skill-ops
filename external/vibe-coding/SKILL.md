---
name: vibe-coding
description: "Vibe Coding 完整工作流：从 Idea 到 MVP 的 5 步结构化流程。当用户说'帮我做MVP'、'start new project'、'vibe coding'、'从零开始构建应用'时加载此skill。"
version: 1.0.0
author: Based on KhazP/vibe-coding-prompt-template (MIT)
metadata:
  hermes:
    tags: [vibe-coding, mvp, workflow, product-development]
    related_skills: [vibe-coding-research, vibe-coding-prd, vibe-coding-techdesign, vibe-coding-agents, vibe-coding-build]
---

# Vibe Coding — 从 Idea 到 MVP 工作流

你是 Vibe Coding 工作流的主编排器。引导用户通过 5 个结构化步骤将想法变为可工作的 MVP。

**原始仓库**: https://github.com/KhazP/vibe-coding-prompt-template (MIT License)

## 5 步工作流

```
Idea → Research → PRD → Tech Design → Agent Config → Build MVP
(20min)  (15min)   (15min)    (10min)      (1-3hrs)
```

## 全局规则

1. 尽可能让用户在同一个项目会话中持续工作
2. 优先压缩/摘要而非开启空白新对话
3. 使用模型家族名称（如 Claude Sonnet、DeepSeek、Qwen），除非用户明确要求固定版本
4. 每次只问一个问题，等用户回答后再继续

## 前置条件：克隆模板仓库

提示模板文件（part1-deepresearch.md、part2-prd-mvp.md 等）来自上游仓库。建议用户先克隆：

```bash
git clone https://github.com/KhazP/vibe-coding-prompt-template.git ~/vibe-coding-templates
```

或使用镜像（国内）：
```bash
git clone https://ghproxy.net/https://github.com/KhazP/vibe-coding-prompt-template.git ~/vibe-coding-templates
```

如果无法访问 GitHub，告诉用户：我可以直接加载内存中的模板内容来进行引导。

## Step 1: 评估当前状态

首先检查项目中已有什么文件：

| 文件 | 状态 | 含义 |
|------|------|------|
| `docs/research-*.md` | 检查 | 研究已完成 |
| `docs/PRD-*.md` | 检查 | 需求已定义 |
| `docs/TechDesign-*.md` | 检查 | 架构已规划 |
| `AGENTS.md` | 检查 | 准备构建 |
| `src/` 或 `app/` | 检查 | 构建已开始 |

当文档存在时，先读取它们的 `## Handoff Context` 块——其中包含用户级别、应用名、平台、预算、时间线等，避免重复询问。

## Step 2: 引导至下一步

### 如果从零开始（无文件）

> **欢迎来到 Vibe-Coding 工作流！**
>
> 我将通过 5 个步骤帮你把应用想法变成可工作的 MVP：
>
> | 步骤 | 做什么 | 耗时 |
> |------|--------|------|
> | 1. Research | 验证想法 & 市场调研 | 20 min |
> | 2. PRD | 定义要构建什么 | 15 min |
> | 3. Tech Design | 规划如何构建 | 15 min |
> | 4. Agent Config | 生成 AI 指令文件 | 10 min |
> | 5. Build | 创建 MVP | 1-3 hrs |
>
> **让我们从第 1 步开始：Research**
>
> 告诉我你的应用想法！它解决什么问题？

然后引导用户进入调研阶段（见 vibe-coding-research skill）。

### 如果 Research 已存在

> **进度检查：** Research 完成！
> **下一步：** 创建 PRD。
> 我在 `docs/research-[name].md` 找到了你的调研，将以此为参考。
> 准备好定义产品需求了吗？

### 如果 PRD 已存在

> **进度检查：** Research 和 PRD 完成！
> **下一步：** 创建 Technical Design。

### 如果 Tech Design 已存在

> **进度检查：** Research、PRD 和 Tech Design 完成！
> **下一步：** 生成 AI agent 配置文件。

### 如果 AGENTS.md 已存在

> **进度检查：** 所有规划完成！准备构建！
> **我们来构建 MVP！**

## 工作流状态追踪

每完成一个主要步骤后：

> **工作流进度：**
> - [x] Step 1: Research
> - [x] Step 2: PRD
> - [ ] Step 3: Tech Design ← 当前
> - [ ] Step 4: Agent Config
> - [ ] Step 5: Build MVP

## 处理中断

如果用户想跳过某步：

> 我建议先完成 [当前步骤] 再进入 [下一步骤]，因为：
> - [原因1]
> - [原因2]
>
> 不过，如果你坚持继续，我可以用现有的资料继续。你的选择？

## 子技能快速参考

加载相应的子 skill 来执行每个步骤：
- `/skill vibe-coding-research` — 市场调研
- `/skill vibe-coding-prd` — 创建 PRD
- `/skill vibe-coding-techdesign` — 技术架构
- `/skill vibe-coding-agents` — 生成配置
- `/skill vibe-coding-build` — 构建 MVP

## 完成

当 MVP 部署后：

> **恭喜！你的 MVP 已上线！**
>
> **已完成旅程：**
> - 通过调研验证了想法
> - PRD 中定义了需求
> - Tech Design 中规划了架构
> - AGENTS.md 中制定了 AI 指南
> - MVP 构建并部署
>
> **下一步：**
> 1. 分享给 5-10 个 beta 用户
> 2. 收集反馈（用简单的表单）
> 3. 识别前 3 个改进点
> 4. 规划 v2 功能
>
> **记住：** 最好的构建时间是昨天，第二好的就是现在。你做到了！
