---
name: fallback-general-dev
description: |
  通用降级开发 skill：当 L1/L2 路由失败、skill 加载异常、或不知道该用哪个
  skill 时，自动加载本兜底方案（基础编码+git+测试）。保证系统在路由失效时
  仍能继续开发，不陷入"不知道该怎么办"的死循环。
  触发词：兜底、降级、fallback、路由失败、skill 加载失败、死循环。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: meta
    tags: [vibe-coding, fallback, degrade, resilience, general]
    related_skills: [vibe-coding-hub, vibe-terminal-safe, git-workflow, snapshot-notes]
---

# 通用降级开发（Fallback General Dev）

**核心思想**：全家桶是"增强"不是"依赖"。路由失败时，用**最朴素可靠的方式**继续开发——
不炫技、不复杂，保证基本盘（写代码 → git → 测试）不断。

## 🚨 触发条件（降级协议）

```
L1 路由失败（不知道该走哪个 L2）
L2 匹配失败（分类目录里找不到对应 skill）
skill 加载异常（skill_view 报错/内容损坏）
任务类型不在全家桶任何分类（新领域/边界场景）
→ 自动激活本 skill
```

## 📋 兜底工作流（三步基本盘）

```
1. 写代码    — 用最简单可靠的方式实现（按需求直接写，不套框架）
2. git 保护  — git init/status/diff/commit（防改崩）
3. 测试验证  — 跑得起来 + 核心路径走通（不追求覆盖率，先保证能跑）
```

### Step 1: 写代码（极简）
- 直接按需求实现，用标准库/最小依赖
- 目录结构从简：`src/` + `tests/`（有测试就写，没有先跑通）
- 不引入复杂架构（不需要 MVC/DDD，先能跑）

### Step 2: git 保护（必做）
```bash
git init（如无）
git status   # 改前看状态
git diff     # 改后看差异
git add -A && git commit -m "wip: <改动摘要>"   # 重要改动即提交
```
> 核心：每次改动都能回退，改崩了 git checkout 恢复。

### Step 3: 测试验证（务实）
```bash
# 能跑 + 核心路径通
python main.py / node app.js / go run .   # 启动验证
curl localhost:PORT/health                # 健康检查（如有 API）
pytest / npm test / go test               # 有测试就跑
```

## 🔄 降级分级

| 级别 | 触发 | 动作 |
|------|------|------|
| 🟡 L1 降级 | L2 路由失败 | 用本 skill 三步基本盘直接干活 |
| 🟠 L2 降级 | skill 加载异常 | 同上 + 记录异常（写入 .snapshots/） |
| 🔴 L3 降级 | 具体 skill 报错 3 次 | 激活 vibe-terminal-safe 安全模式（只读） |

## 📝 降级报告（完成后输出）

```markdown
# 降级报告
- 触发原因：<L1/L2/L3 什么失败>
- 降级级别：🟡/🟠/🔴
- 做了什么：<用三步基本盘完成了什么>
- 未用到的 skill：<原计划但失败的>
- 恢复建议：<下次如何避免降级（修 skill/补索引/更新路由）>
```

## 🤝 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `vibe-coding-hub` | L1 路由失败时激活本 skill（降级协议写入 L1） |
| `vibe-terminal-safe` | L3 报错 3 次 → 其"安全模式"接管（只读命令） |
| `git-workflow` | 兜底第二步用 git 保护 |
| `snapshot-notes` | 降级事件记录到 .snapshots/（可追溯） |
| `global-experience` | 降级原因/解法沉淀，避免下次再降级 |

## ⚠️ 核心原则

1. **能跑优先**：降级时不做完美主义，先保证基本盘不断。
2. **有记录**：降级不是偷偷发生，必须输出降级报告。
3. **有恢复路径**：降级后要能回到正常流程（修复路由/skill）。
4. **不破坏**：降级时只用安全操作，不做危险命令。

## 快速排障

| 症状 | 处理 |
|------|------|
| 不知道该用哪个 skill | 直接走本 skill 三步基本盘 |
| skill_view 报错 | 换另一个 skill；仍失败 → 降级 |
| 降级后还卡住 | 安全模式（只读）→ 保存状态 → 等用户 |
| 恢复后路由正常 | 输出降级报告，建议修复问题源 |
