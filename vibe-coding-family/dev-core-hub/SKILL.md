---
name: dev-core-hub
description: |
  全家桶 L2 目录 — 开发核心层。覆盖：主流程（vibe-coding/dev-team）、
  编码工作流与纪律、调试、测试、版本控制。当开发任务进入
  编码/调试/测试/提交阶段时，先加载本目录定位对应 L3 skill。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vibe-coding, hub, core, coding, debugging, testing, git]
    related_skills: [vibe-coding-hub, vibe-coding, dev-team, systematic-debugging, test-driven-development, git-workflow]
---

# 开发核心层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**开发主链路**：从选主流程到编码、调试、测试、提交。
具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：主流程选择、编码工作流与纪律、调试、测试、Git 工作流、代码审查、项目初始化与规划、发布与看板
- ❌ **不管**：具体语言语法与框架 → `dev-stack-hub`；部署/容器/CI → `dev-infra-hub`；多Agent协作 → `dev-agent-hub`；模型训练 → `dev-ai-hub`
- 🔄 **协作点**：编码完成选框架 → `dev-stack-hub`；要部署上线 → `dev-infra-hub`；要多Agent并行 → `dev-agent-hub`

## 🎯 主流程（先选一个，Primary route first）

| Skill | 定位 | 加载时机 |
|-------|------|----------|
| `vibe-coding` | 单人 5 步流程：Idea→Research→PRD→TechDesign→Build | 中小型项目、快速 MVP |
| `dev-team` | 多Agent团队 v2.1：主Agent+4子Agent、3并发、双模式、断点续传 | 中大型项目、全流程、批量并行（用户偏好优先） |
| `fallback-general-dev` | 降级兜底：路由失败时三步基本盘（写码→git→测试） | 路由失败/不知道用哪个skill（兜底） |

## 🧭 子层路由

### 编码工作流与纪律
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `code` | 通用编码工作流（规划→实现→验证→测试） | 结构化编码 |
| `code-review` | 系统性代码审查（安全/性能/可维护性） | 提交前、PR 时 |
| `security-audit` | 提交前安全审计：权限/加密/密钥/依赖六维扫描 | commit/PR 前（v3.3 新增） |
| `karpathy-coding-dscpln` | Karpathy 四原则：防过度设计、diff 蔓延 | refactor 前、迭代失控时 |
| `simplify-code` | 并行 4-Agent 清理近期代码改动 | 代码变复杂时 |
| `structured-code-remediation` | 多阶段代码整改运动 | 大规模修整时 |
| `python-project-refactoring` | 单体 Python 拆分层级架构 | Python 项目重构 |
| `api-development` | API 全生命周期开发编排 | 做 API 项目 |
| `cli-tool-building` | Click + Typer + Rich 专业 CLI 构建 | 做 CLI 工具 |
| `project-scaffold` | 项目脚手架：标准目录+依赖+git+快照初始化 | 新建项目（主） |
| `plan-workflow` | 任务拆分→写计划→存 .snapshots/plans/ | 复杂多步任务（主） |
| `release-management` | 通用发布/版本管理：SemVer+CHANGELOG+tag+发布清单 | 发布/打版本（主） |
| `project-tracker-dashboard` | HTML 可视化项目跟踪看板（深色/手机友好） | 项目可视化/看板（主） |
| `spike` | 一次性实验验证想法 | 技术选型验证前 |

### 调试
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `systematic-debugging` | 4 阶段根因调试（先理解再修） | 任何疑难 Bug |
| `python-debugpy` | pdb REPL + debugpy 远程调试 (DAP) | Python 调试 |
| `node-inspect-debugger` | Node --inspect + CDP 调试 | Node.js 调试 |
| `rest-graphql-debug` | REST/GraphQL 状态码/auth/schema 排障 | 接口调试 |

### 测试
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `test-driven-development` | RED-GREEN-REFACTOR 强制 TDD | 测试驱动开发 |
| `api-testing-contracts` | OpenAPI/Swagger 契约测试 | API 契约验证 |
| `webapp-testing` | 本地 Web 应用交互与测试工具包 | Web 应用测试 |
| `dogfood` | Web 应用探索式 QA：找 Bug、证据、报告 | 上线前 QA |
| `performance-testing` | Locust 压测等性能测试 | 性能验证 |

### 版本控制与协作
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `git-workflow` | diff/commit/push/多仓库管理 | 每轮迭代后 |
| `github/github-auth` | HTTPS token / SSH / gh CLI 登录 | 首次连 GitHub |
| `github/github-pr-workflow` | 分支→PR→CI→合并全流程 | 提 PR |
| `github/github-issues` | issue 创建/分诊/标签 | 管理 issue |
| `github/github-code-review` | PR diff 审查 + 行内评论 | PR 审查 |
| `github/github-repo-management` | 仓库创建/fork/release | 仓库管理 |

## 选择规则

1. **先选主流程**：中小型/快速 MVP → `vibe-coding`；中大型/全流程/批量并行 → `dev-team`（用户偏好）。
2. **新建项目** → `project-scaffold` 初始化；复杂多步任务 → `plan-workflow` 先拆解成计划。
3. **调试优先**：疑难 Bug 先用 `systematic-debugging` 理解根因，再动手。
4. **测试配套**：严谨项目用 `test-driven-development`，API 用 `api-testing-contracts`，Web 用 `webapp-testing`/`dogfood`。
5. **版本保护**：所有改动前确认 git 状态，改动后 diff，重要改动 commit（`git-workflow`）。

## 全局底线（本层所有 skill 通用）

- 改前看 git 状态，改后 diff，重要改动 commit。
- 报错不臆测，跑命令拿真实错误；小步迭代，不一次性大规模重写。
- 修 Bug 先 `systematic-debugging` 理解根因，再动手。
