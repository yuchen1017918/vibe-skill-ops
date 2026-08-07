---
name: project-scaffold
description: |
  ⚠️ v1.3 deprecated — 由 project-init 取代（合并了骨架+计划+嗅探）。文件保留防交叉引用。
  项目脚手架初始化 skill：从零创建新项目时一键生成
  标准目录结构 + 依赖配置 + git 初始化 + .snapshots 快照目录。
  当用户说"新建项目"、"初始化项目"、"start new project"、
  "脚手架"时加载。支持 Python/TypeScript/Go 等主流栈。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, scaffold, init, project, template, boilerplate]
    related_skills: [vibe-coding-hub, snapshot-notes, git-workflow, dev-core-hub]
---

# 项目脚手架（Project Scaffold）

**问题**：每次新建项目都重复造轮子——目录结构、依赖配置、git、快照目录。
**方案**：一键初始化标准骨架，让开发直接进入业务逻辑。

## 📁 标准骨架（以 Python 为例）

```
<project-name>/
├── src/<package>/          # 源码包
│   ├── __init__.py
│   ├── main.py             # 入口
│   └── config.py           # 配置（读环境变量，不硬编码）
├── tests/                  # 测试
│   └── test_main.py
├── docs/                   # 文档
│   ├── SPEC.md             # 需求规范（dev-team 生成）
│   └── ARCH.md             # 架构（dev-team 生成）
├── .snapshots/             # ← 快照目录（snapshot-notes 使用）
│   └── SNAPSHOT.md
├── .vibe-rules.md          # ← 宪法代码化（v1.1 新增）
├── .env.example            # 环境变量模板
├── .gitignore
├── requirements.txt        # 或 pyproject.toml
└── README.md
```

## 🚀 初始化流程

```
1. 确认项目名 + 技术栈（Python/TS/Go/…）
2. 创建目录结构（标准骨架）
3. 生成依赖配置（requirements.txt / package.json / go.mod）
4. 生成 .gitignore（含 .env、__pycache__、node_modules 等）
5. 生成 .env.example（占位密钥，真实密钥绝不入库）
6. 初始化 git：git init + 首次 commit
7. 初始化 .snapshots/SNAPSHOT.md（快照笔记 skill 的初始快照）
8. 生成 .vibe-rules.md（宪法代码化，见下方模板）
9. 生成 README.md（项目名 + 一句话 + 运行方式）
10. 输出初始化摘要
```

### .vibe-rules.md（宪法代码化模板，v1.1 新增）

项目根目录自动生成，作为 AI 每次加载时的强制上下文（配合全家桶 L1 宪法）：

```markdown
# Vibe-Coding 项目规则（.vibe-rules.md）

> 本文件是项目的"宪法"——任何 Agent 在本项目工作时必须遵守。

## 全局底线
1. **主流程唯一**：一次只走 vibe-coding（单人）或 dev-team（团队），不叠加。
2. **改前看 git，改后 diff，重要改动 commit**（防改崩回滚）。
3. **终端过白名单**：禁 rm -rf / sudo / mkfs / dd（除非用户明确要求）。
4. **报错不臆测**：跑命令拿真实输出，小步迭代，不一次性大规模重写。
5. **大项目不全文塞上下文**：用 vibe-code-search 检索。

## 项目状态
- 技术栈：<填写>
- 当前阶段：<Phase X>
- 状态快照：.snapshots/SNAPSHOT.md（每次更新）
- 项目计划：.snapshots/plans/PLAN-*.md

## 安全红线
- 密钥只在 .env（已 gitignore），绝不硬编码。
- 高危命令需用户明确授权。
- 文件写操作记录到 .snapshots/audit.log。
```

### 国内环境可选子模块（v1.1 新增）

国内网络环境下，自动检测并配置镜像源（详见 `china-env-adapt` skill）：

```
检测：pip config get / npm config get registry / 测速
命中国内环境 → 自动执行：
  - pip → 阿里云源
  - npm → npmmirror
  - git clone → ghproxy 前缀
  - docker → registry-mirrors
记录换源决策到 .snapshots/（可回滚）
```

触发条件：`pip install` 超时 / `npm install` 卡住 / `git clone` 失败 / 用户明确国内环境。
非国内环境跳过此模块，不画蛇添足。

## 📄 模板速查

### Python 依赖（requirements.txt 最小集）
```
# 根据项目需要添加，不要预装不需要的
# fastapi / flask / requests / pydantic / pytest / ruff
```

### .gitignore 核心
```
.env
__pycache__/
*.pyc
.venv/
node_modules/
dist/
build/
*.log
```

### .env.example
```
# 复制为 .env 并填入真实值，.env 已在 .gitignore 中
# API_KEY=
# DATABASE_URL=
```

### 初始快照（SNAPSHOT.md）
```markdown
# 项目快照 — <项目名>

## 概要
- 一句话：<待填写>
- 技术栈：<待填写>
- 当前阶段：初始化完成
- 最后更新：<时间戳>

## 已完成 ✅
- [x] 项目脚手架初始化

## 进行中 🔄
- [ ] <第一个任务>

## 下一步 ⏭
1. <待定>
```

## 🧭 技术栈变体

| 栈 | 骨架要点 |
|----|----------|
| Python | `src/<pkg>/` + `pyproject.toml` 或 `requirements.txt` + `pytest` |
| TypeScript/Node | `src/` + `package.json` + `tsconfig.json` + `vitest` |
| Go | `cmd/` + `internal/` + `go.mod` |
| Web 前端 | `src/` + `vite.config.ts` + `package.json` |
| FastAPI 后端 | `app/main.py` + `app/routers/` + `alembic/` |

## 与全家桶衔接

1. 初始化完成 → 交给 `vibe-coding`（单人）或 `dev-team`（团队）走主流程。
2. `.snapshots/` 由 `snapshot-notes` 持续维护。
3. 首次 commit 走 `git-workflow` 规范。

## 快速排障

| 症状 | 处理 |
|------|------|
| 项目名有非法字符 | 用 kebab-case（`my-project`），包名用 snake_case |
| 依赖冲突 | 用 venv（Python）或 nvm（Node）隔离环境 |
| 初始化时 git 报错 | 检查 user.name/email 已配置（git-workflow 排障） |
