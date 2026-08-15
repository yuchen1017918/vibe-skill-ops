---
name: project-init
description: 项目初始化与规划 skill（v1.3 合并自 project-scaffold + plan-workflow）： 一键建骨架（标准目录+依赖+git+快照+宪法）+ 技术栈背景嗅探 + 任务拆分计划。 当用户说"新建项目"、"初始化项目"、"做个计划"、"拆分任务"、 "规划一下"、"脚手架"时加载。 触发词：新建项目、初始化、脚手架、做计划、拆分任务、规划。
family-type: workflow
family-version: 1.0.0
---

# 项目初始化与规划（Project Init）

**v1.3 合并产物**:由 `project-scaffold`(骨架)+ `plan-workflow`(计划)+ stack-detect(技术栈嗅探)合并而成。
一次加载解决"从零到有、从有到计划"两件事,少 2 个 skill 文档、少 2 次加载决策。

## 🚀 一、初始化骨架

### 标准骨架(以 Python 为例)

```
<project>/
├── src/<package>/          # 源码包
│   ├── __init__.py
│   ├── main.py
│   └── config.py           # 配置读环境变量,不硬编码
├── tests/test_main.py      # 测试
├── docs/                   # SPEC.md / ARCH.md(dev-team 生成)
├── .snapshots/             # SNAPSHOT.md + plans/ + DECISIONS.md
├── .vibe-rules.md          # 宪法代码化(模板见下)
├── .vibe/stack.yaml        # 技术栈画像(嗅探产物)
├── .env.example            # 密钥占位,真实密钥绝不入库
├── .gitignore
├── requirements.txt        # 或 pyproject.toml
└── README.md
```

### ADR 决策记录模板（v1.1 新增 — 参考 addyosmani/agent-skills，写入 .snapshots/DECISIONS.md）

每个**非平凡架构决策**留一条 ADR（决策留痕，防"为什么这么设计"失忆）：

```markdown
## ADR-<序号>: <决策标题>
- 状态: Proposed | Accepted | Deprecated    # 决策生命周期
- 日期: YYYY-MM-DD
- 背景 (Context):   为什么需要这个决策？问题/约束是什么？
- 决策 (Decision):  选了什么方案？
- 备选 (Alternatives): 没选什么？为什么？
- 影响 (Consequences): 这带来什么代价/收益？(含迁移成本)
```

> 规则：**Match existing convention first**——新决策先查项目已有惯例，没有才创新；
> ADR 不是所有决策都写，只写影响架构/接口/数据格式的非平凡决策（联动 doubt-driven-development 判定）。

### 初始化流程(10 步)

```
1. 确认项目名 + 技术栈(有要求记录;没有 → 嗅探或默认)
2. 创建目录结构
3. 生成依赖配置(requirements.txt / package.json / go.mod)
4. 生成 .gitignore(.env、__pycache__、node_modules 等)
5. 生成 .env.example
6. git init + 首次 commit
7. 初始化 .snapshots/SNAPSHOT.md + plans/ 目录
8. 生成 .vibe-rules.md(宪法)
9. 生成 README.md
10. 输出初始化摘要
```

### .vibe-rules.md(宪法模板)

```markdown
# Vibe-Coding 项目规则
1. 主流程唯一:一次只走一个主流程(dev-assistant/quick-dev/vibe-coding/dev-team),不叠加。
2. 改前看 git,改后 diff,重要改动 commit。
3. 终端过白名单:禁 rm -rf / sudo / mkfs / dd(除非用户明确要求)。
4. 报错不臆测:跑命令拿真实输出。
5. 大项目不全文塞上下文:用 vibe-code-search 检索。
## 项目状态
- 技术栈:<填写>
- 当前阶段:<Phase X>
- 状态快照:.snapshots/SNAPSHOT.md
- 项目计划:.snapshots/plans/PLAN-*.md
## 安全红线
- 密钥只在 .env(gitignore),绝不硬编码。
- 高危命令需用户明确授权。
```

### 技术栈变体速查

| 栈 | 骨架要点 |
|----|----------|
| Python | `src/<pkg>/` + `pyproject.toml` 或 `requirements.txt` + `pytest` |
| TypeScript/Node | `src/` + `package.json` + `tsconfig.json` + `vitest` |
| Go | `cmd/` + `internal/` + `go.mod` |
| Web 前端 | `src/` + `vite.config.ts` + `package.json` |
| FastAPI 后端 | `app/main.py` + `app/routers/` + `alembic/` |

## 🔍 二、技术栈背景嗅探(stack-detect 无感化)

**不做独立检测步骤**——初始化时**背景嗅探**特征文件,用户无感:

```
特征文件 → 推断技术栈:
  package.json + tsconfig.json  → TypeScript/Node
  pyproject.toml / requirements.txt → Python
  go.mod                        → Go
  vite.config.ts                → Web 前端(Vite)
  app/ + alembic/               → FastAPI 后端
```

- 嗅探结果写入 `.vibe/stack.yaml`(test runner / build 工具 / 语言)
- 自动激活对应技术二级索引:`dev-stack-hub` 对应语言段(加载纪律摘要 ≤5 条,不全文)
- 用户提到"帮我写个接口"时,Agent 已知道这是 Java 还是 Go 项目,直接走对应索引

## 📋 三、计划工作流(WBS)

### 核心闭环

```
需求 → 任务拆分(WBS)→ 写 PLAN-<日期>.md → 逐步执行 → 更新 ✅ → 完成归档
```

### WBS 规则
- **原子性**:每个任务可独立完成、可验证
- **依赖排序**:标出前置任务
- **MoSCoW 分级**(中大型):Must / Should / Could / Won't
- **验收标准**:每个任务有"完成 = 什么"

### 计划模板

```markdown
# 计划 — <项目/任务名>
## 目标
<一句话>
## 任务列表
| # | 任务 | 优先级 | 依赖 | 验收标准 | 状态 |
|---|------|--------|------|----------|------|
| 1 | <任务> | Must | - | <完成=什么> | ⬜ |
## 执行顺序
1 → 2 → 3(标注可并行)
## 风险与依赖
## 变更记录
| 日期 | 变更 | 原因 |
## 交接提示
```

### 规模分支
- **小型**(<5 任务):精简计划(目标+任务表+顺序),直接写 PLAN 文件
- **中大型**(≥5):完整计划 + 建议接 dev-team / vibe-coding 主流程

## 🔗 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `requirement-clarify` | 模糊需求先澄清(DECISIONS.md)→ 本 skill 初始化 + 计划 |
| `snapshot-notes` | .snapshots/ 持续维护 |
| `china-env-adapt` | 国内环境自动配镜像源(可选子模块) |
| `git-workflow` | 首次 commit + 后续提交规范 |
| `dev-team` / `vibe-coding` | 初始化完成后交主流程 |

## 快速排障

| 症状 | 处理 |
|------|------|
| 项目名非法字符 | kebab-case(`my-project`),包名 snake_case |
| 任务拆太细 | 合并到"一次可交付"粒度 |
| 计划过期 | 每次执行前先更新 PLAN 再动手 |
| 嗅探猜错技术栈 | 用户纠正后更新 .vibe/stack.yaml,不再自动猜 |
