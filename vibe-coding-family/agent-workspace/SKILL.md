---
name: agent-workspace
description: |
  ⚠️ v1.3 deprecated — 由 agent-ops 取代（合并了工位+协作）。文件保留防交叉引用。
  多Agent工位工作区 skill：在项目根目录建立多Agent工作区，
  每个Agent一个专属工位文件夹，存自己的工作记忆、规划、经验。
  .snapshots/ 保持共享记忆规划不变（团队级），工位是个人级（Agent级）。
  当启用 dev-team / 多Agent协作时自动激活。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, multi-agent, workspace, cubicle, memory, dev-team]
    related_skills: [vibe-coding-hub, dev-team, multi-agent-config-manager, snapshot-notes, plan-workflow]
---

# 多Agent工位工作区（Agent Workspace）

**核心思想**：多Agent协作时，项目根目录建一个工作区文件夹，**每个Agent一个工位**，
工位里存自己的工作记忆、规划、经验。工位是**个人私有**的，`.snapshots/` 是**团队共享**的。

```
<项目根>/
├── .snapshots/               # 🔒 共享记忆（snapshot-notes，团队级，不变）
│   ├── SNAPSHOT.md           # 团队项目状态
│   └── plans/                # 团队计划
├── agents/                   # 🆕 多Agent工作区（本 skill）
│   ├── spec-writer/          # 工位 1：规范编写Agent
│   │   ├── MEMORY.md         #   个人工作记忆
│   │   ├── PLAN.md           #   个人任务规划
│   │   └── EXPERIENCE.md     #   个人经验/踩坑
│   ├── coder/                # 工位 2：编码Agent
│   ├── tester/               # 工位 3：测试Agent
│   └── bug-fixer/            # 工位 4：修Bug Agent
└── ...项目文件
```

## 层级：共享 vs 工位

| 维度 | `.snapshots/`（共享） | `agents/<name>/`（工位） |
|------|----------------------|--------------------------|
| 级别 | 团队级 | Agent 个人级 |
| 内容 | 项目状态、团队计划 | 个人记忆、个人规划、个人经验 |
| 可见性 | 所有 Agent 可读 | 仅属主 Agent（其他可读不写） |
| 用途 | 跨对话恢复项目上下文 | 跨任务保持 Agent 角色一致性 |
| 变更者 | snapshot-notes / plan-workflow | 各 Agent 自己 |

## 📁 工位目录结构（每 Agent 一个）

```
agents/<role-name>/
├── MEMORY.md        # 工作记忆：角色上下文、任务历史、重要事实
├── PLAN.md          # 个人规划：当前任务拆解、进度、下一步
└── EXPERIENCE.md    # 经验库：踩坑记录、成功模式、领域知识
```

### MEMORY.md（工作记忆）
```markdown
# 工位记忆 — <Agent角色名>

## 角色
- 职责：<一句话>
- 输入：<需要什么>
- 输出：<产出什么>

## 当前任务
- 任务：<在做什么>
- 上下文：<重要背景>

## 重要事实
- <从任务中学到的关键事实>

## 交接状态
- 上次做到：<X>
- 下次继续：<Y>
```

### PLAN.md（个人规划）
```markdown
# 工位规划 — <Agent角色名>

## 当前计划
| # | 任务 | 依赖 | 状态 |
|---|------|------|------|
| 1 | <任务> | - | ⬜ |

## 执行顺序
1 → 2 → 3

## 变更记录
| 日期 | 变更 |
|------|------|
```

### EXPERIENCE.md（经验库）
```markdown
# 工位经验 — <Agent角色名>

## 踩坑记录
| 坑 | 症状 | 解法 |
|----|------|------|
| <坑> | <现象> | <解法> |

## 成功模式
- <可复用的做法>

## 领域知识
- <角色特有的知识>
```

## 🚀 激活流程（多Agent任务启动时）

```
1. 主Agent 检查项目根目录是否已有 agents/ 工作区
2. 没有 → 创建 agents/，按团队角色建工位：
   mkdir -p agents/{spec-writer,coder,tester,bug-fixer}
3. 每个工位初始化 MEMORY.md / PLAN.md / EXPERIENCE.md（模板）
4. 主Agent 告知每个子Agent 其工位路径
5. 子Agent 每次工作前后读写自己的工位
```

## 🔄 子Agent 工作规范

1. **开工前**：读自己的 `MEMORY.md` + `PLAN.md`，恢复个人上下文。
2. **工作中**：重要决策/发现 → 记入 `MEMORY.md`；踩坑 → 记入 `EXPERIENCE.md`。
3. **阶段性完成**：更新 `PLAN.md` 进度；同步团队状态到 `.snapshots/SNAPSHOT.md`。
4. **交接时**：写清 `MEMORY.md` 的交接状态（上次做到/下次继续）。

## 🤝 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `dev-team` | 4 子Agent 自动获得工位（spec-writer/coder/tester/bug-fixer） |
| `multi-agent-config-manager` | 兼容其 agents/ 工作区，扩展为工位三件套 |
| `snapshot-notes` | `.snapshots/` 团队共享不变，工位是其个人级补充 |
| `plan-workflow` | 团队计划在 .snapshots/plans/，个人规划在工位 PLAN.md |
| `agent-project-manager` | 集中式管理项目，工位管 Agent 个人 |

## ⚠️ 边界规则

- **工位不替代快照**：团队状态永远写 `.snapshots/`，工位只存个人视角。
- **工位不跨 Agent**：coder 不写 tester 的工位；需要传递 → 写团队快照。
- **工位权限**：自己的工位可读写；他人工位禁止访问（详见 `agent-permissions` 权限矩阵）。
- **工位随 git 走**：建议提交，保留个人演进轨迹（如涉密可 .gitignore）。
- **角色增减**：团队加 Agent → 加工位；减 Agent → 工位归档不删除（历史可查）。

## 快速排障

| 症状 | 处理 |
|------|------|
| 工位文件丢失 | 重新初始化模板；历史在 git 里可恢复 |
| Agent 忘记写工位 | 主Agent 在委派提示词中强制要求读写工位路径 |
| 工位内容膨胀 | 经验库定期整理，只留高价值；细节指向文档 |
| 工位和快照冲突 | 个人经验进工位，团队状态进快照，不混写 |
