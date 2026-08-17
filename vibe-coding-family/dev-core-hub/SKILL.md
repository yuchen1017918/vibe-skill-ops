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
    related_skills: [vibe-coding-hub, vibe-coding, dev-team, systematic-debugging, git-workflow]
---

# 开发核心层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**开发主链路**：从选主流程到编码、调试、测试、提交。
具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：主流程选择、编码工作流与纪律、调试、测试、Git 工作流、代码审查、项目初始化与规划、发布与看板
- ❌ **不管**：具体语言语法与框架 → `dev-stack-hub`；部署/容器/CI → `dev-infra-hub`；多Agent协作 → `dev-agent-hub`；模型训练 → `dev-ai-hub`
- 🔄 **协作点**：编码完成选框架 → `dev-stack-hub`；要部署上线 → `dev-infra-hub`；要多Agent并行 → `dev-agent-hub`

## 🎯 主流程（v1.2 — 四选一，先走组织路由）

> 与 hub 四格场景表对应：助手/全盘 × 团队/企业。先判组织形态与开发模式，再选主流程。

| Skill | 定位 | 加载时机 |
|-------|------|----------|
| `dev-assistant` | 副驾驶协议（助手模式）：局部实现/Bug定位/审查/答疑/小重构/写草稿 | 用户主导开发（用户=司机），团队·轻/企业·重双参数 |
| `quick-dev` | 轻量全包（团队·全盘）：四步循环，非项目随手做/小工具/脚本/一次性任务 | 随手做、写脚本、迷你交付（v1.2 新增） |
| `vibe-coding` | 单人 5 步流程：Idea→Research→PRD→TechDesign→Build | 单人做 MVP 项目（非随手做，是完整项目） |
| `dev-team` | 多Agent团队 v2.1：主Agent+4子Agent、3并发、双模式、断点续传 | 企业·全盘：中大型项目、全流程、批量并行 |
| `fallback-general-dev` | 降级兜底：路由失败时三步基本盘（写码→git→测试） | 路由失败/不知道用哪个skill（兜底，非正常流程） |

## 🧭 子层路由

### 编码工作流与纪律
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `code` | 通用编码工作流（规划→实现→验证→测试） | 结构化编码 |
| `code-review` | 系统性代码审查（安全/性能/可维护性）——方法论 | 提交前、PR 时 |
| `open-code-review` | AI 审查执行引擎（阿里 ocr CLI，DeepSeek 实测）：行级 bug/质量审查 | "审查代码"/"review"/"审查PR"（v1.3 新增，质量闸门执行器） |
| `security-audit` | 提交前安全审计：权限/加密/密钥/依赖六维扫描（v1.2 工具化：semgrep+gitleaks） | commit/PR 前（v3.3 新增，v1.2 **强制前置闸门**） |
| `code-security` | AI 编码安全三层防线（Qoder 架构）：①静默纪律(policy 默认注入) ②轻量扫描(增量 diff 建议) ③深度扫描(按需全量+闭环重扫) | 写完代码防漏洞/安全扫描/深度扫描（v1.2 新增） |
| `karpathy-coding-dscpln` | Karpathy 四原则：防过度设计、diff 蔓延 | refactor 前、迭代失控时 |
| `structured-code-remediation` | 多阶段代码整改运动 | 大规模修整时 |
| `python-project-refactoring` | 单体 Python 拆分层级架构 | Python 项目重构 |
| `api-development` | API 全生命周期开发编排 | 做 API 项目 |
| `cli-tool-building` | Click + Typer + Rich 专业 CLI 构建 | 做 CLI 工具 |
| `project-init` | 项目初始化+规划+技术栈嗅探（v1.3 合并自 scaffold+plan） | 新建项目/做计划（主） |
| `requirement-clarify` | 需求澄清访谈：编码前主动提问产出 DECISIONS.md | 模糊需求/编码前（v1.1 新增） |
| `release-ops` | 发布+回滚一体化：SemVer+CHANGELOG+tag+备份+回滚（v1.3 合并） | 发布/打版本/回滚（主） |
| `project-tracker-dashboard` | HTML 可视化项目跟踪看板（深色/手机友好） | 项目可视化/看板（主） |

**提交闸门记录（v1.3 — 度量闭环，三足鼎立地基）**：每次 commit 前，
未过 `security-audit` 六维/`code-security` 纪律 → **追加一行 `~/.vibe/metrics/security-drift.log`**（时间/原因），
cost-agent 周报消费——让"跳过安全"有可见成本；usage.log（token 角）/ triage-accuracy.log（质量角）同理由 hub Step 0.5、snapshot-notes 写入。

### 调试
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `systematic-debugging` | 4 阶段根因调试（先理解再修）+ 防御验证三原则（v1.2 复活+claudekit 精华） | 任何疑难 Bug |
| `rest-graphql-debug` | REST/GraphQL 状态码/auth/schema 排障 | 接口调试 |

### 测试
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `api-testing-contracts` | OpenAPI/Swagger 契约测试 | API 契约验证 |
| `webapp-testing` | 本地 Web 应用交互与测试工具包 | Web 应用测试 |
| `performance-testing` | Locust 压测等性能测试 | 性能验证 |

### 版本控制与协作
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `git-workflow` | diff/commit/push/多仓库管理 | 每轮迭代后 |
| `git-worktree` | 多工作区并行开发(多分支同时干/多Agent隔离) | "并行开发"/"worktree"(v1.3 新增) |
| `github/github-repo-management` | 仓库创建/fork/release | 仓库管理 |

## 选择规则

1. **先判组织路由**（v1.2）：用户主导 → `dev-assistant`（助手）；用户给方向 → 按规模选 `quick-dev`（团队·随手做）/ `vibe-coding`（团队·单人 MVP）/ `dev-team`（企业·全流程）。
2. **新建项目/做计划** → `project-init`（初始化+规划+嗅探一体，v1.3 合并）。
3. **调试优先**：疑难 Bug 先用 `systematic-debugging` 理解根因，再动手。
4. **测试配套**：API 用 `api-testing-contracts`，Web 用 `webapp-testing`，性能用 `performance-testing`；修 Bug 后按 `systematic-debugging` §With tests 写回归测试。
5. **版本保护**：所有改动前确认 git 状态，改动后 diff，重要改动 commit（`git-workflow`）。

## 全局底线（本层所有 skill 通用）

- 改前看 git 状态，改后 diff，重要改动 commit。
- 报错不臆测，跑命令拿真实错误；小步迭代，不一次性大规模重写。
- 修 Bug 先 `systematic-debugging` 理解根因，再动手。
