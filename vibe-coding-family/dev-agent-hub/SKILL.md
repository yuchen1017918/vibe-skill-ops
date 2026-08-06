---
name: dev-agent-hub
description: |
  全家桶 L2 目录 — 智能体与治理层。覆盖：Agent 编排、AI 编码器委派、
  代码搜索/上下文、文档化、skill 治理。当任务涉及多Agent协作、
  委派外部编码器、大项目代码检索、或 skill 数量治理时，
  先加载本目录定位对应 L3 skill。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vibe-coding, hub, agent, orchestration, ai-coding, governance]
    related_skills: [vibe-coding-hub, multi-agent-config-manager, vibe-code-search, vibe-skills-gov-patterns]
---

# 智能体与治理层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**Agent 协作与生态治理**。
具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：多Agent编排、AI 编码器委派、代码搜索/上下文、文档化、skill 治理
- ❌ **不管**：Agent 要写的业务代码 → `dev-core-hub`；Agent 要部署的环境 → `dev-infra-hub`；AI 模型训练/推理 → `dev-ai-hub`
- 🔄 **协作点**：Agent 产出代码后交 `dev-core-hub` 审查测试；Agent 涉及模型能力时交 `dev-ai-hub`

## 🧭 子层路由

### Agent 编排（多Agent协作）
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `multi-agent-config-manager` | 多代理编排引擎：任务分解/分支执行/验证审核/返工 | 深度研究、项目协作、多Agent（主） |
| `agent-loop` | 自动开发指挥循环：子Agent汇报→主Agent指挥→无人值守，定期汇报/重大决策询问 | 自动开发、无人值守（主） |
| `agent-collab` | 平级协作协议：tester↔bug-fixer 等协作对，三步闭环（请求→响应→验证） | 两个Agent直接配合时（主） |
| `agent-permissions` | 权限规范：职责边界/文件权限矩阵/命令分级/安全红线 | 多Agent任务启动时（自动） |
| `agent-workspace` | 多Agent工位：每人一个文件夹存记忆/规划/经验 | 启用多Agent协作时（自动） |
| `subagent-driven-development` | 用 delegate_task 子代理执行计划（2 阶段审查） | 委派子任务 |
| `devops/kanban-orchestrator` | 看板编排：任务拆解/专家角色/并发约定 | 看板驱动开发 |
| `devops/kanban-worker` | 看板执行者：陷阱/边界/并发冲突规避 | 看板任务执行 |
| `langgraph` | 图编排 LLM 工作流 | 复杂 Agent 状态机 |

> 注：`agent-orchestrate`（多代理编排模式）已并入 `multi-agent-config-manager`，不再单独列出。

### AI 编码器委派（外部工具）
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `claude-code` | 委派编码给 Claude Code CLI | 用 Claude Code |
| `codex` | 委派编码给 Codex CLI | 用 Codex |
| `opencode` | 委派编码给 OpenCode CLI | 用 OpenCode |

### 代码搜索与上下文
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `vibe-code-search` | 内置 grep → 分页读 → 语义 MCP 兜底 | 大项目定位代码（主） |
| `snapshot-notes` | 项目内嵌快照：跨对话工作记忆，写 .snapshots/ | 阶段完成/重要决策/新会话恢复上下文 |
| `global-experience` | 跨项目经验库：踩坑/模式全局共享（~/.hermes/experience/） | 项目沉淀/跨项目复用（主） |
| `agent-project-manager` | 集中式项目状态管理（STATUS.md/甘特图） | 多项目集中管理 |
| `code-wiki` | 生成 wiki + Mermaid 图 | 代码文档化 |
| `knowledge-extraction` | 知识萃取：任务/异常后自动复盘（5 Whys）+ 模式沉淀 | 任务完成/异常后（v3.5 新增，自动触发） |

> 注：`github/codebase-inspection`（LOC 统计）与 `vibe-code-search` 重叠，已废弃引用。

### Skill 治理
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `vibe-skills-gov-patterns` | Skill 治理：防互撞、promotion/destructive gate | skill 变多、路由冲突（主） |
| `devops/hermes-skill-hub` | 从 Skills Hub 发现/评估/安装 skill | 找新 skill |
| `skill-creator` | 创建/修改/改进 skill | 写新 skill |

## 选择规则

1. **先定编排方式**：深度研究/多Agent → `multi-agent-config-manager`；简单委派 → `subagent-driven-development`。
2. **外部编码器**：只在用户明确要求用 Claude Code/Codex/OpenCode 时加载。
3. **代码检索优先**：项目大先用 `vibe-code-search`，不要全文塞上下文。
4. **治理按需**：skill 数量增长或路由冲突时才加载治理 skill。

## 全局底线

- 子Agent 任务必须写明目标、验收标准、输出格式（delegate_task 规范）。
- 外部编码器输出要验证（自报成功≠真成功），关键产物回读确认。
- 单一控制面：主流程唯一，不引入第二 orchestrator。
