---
name: git-worktree
description: |
  多工作区并行开发：一个 git 仓库多个工作区（git worktree add/list/remove），
  每个工作区独立分支互不干扰，多 Agent/外部编码器/审查/实验/发布并行。
  当用户说"并行开发"、"多分支同时干"、"别污染主工作区"、"给codex一个独立目录"、
  "worktree" 时加载。
  触发词：worktree、多工作区、并行开发、独立目录、多分支。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, git, parallel, worktree, multi-agent]
    related_skills: [codex-agent, agent-ops, dev-team, release-ops, open-code-review, git-workflow, dev-core-hub]
---

# Git Worktree（多工作区并行开发）

**核心思想**：一个 git 仓库可以有多个工作目录（worktree），每个 checkout 不同分支，
共享 `.git` 对象库——**同时开多个分支干活，互不干扰，无需 stash/切分支，可多进程并行**。

## 1️⃣ 核心命令（5 个）

```bash
git worktree add <path> <branch>              # 新工作区检出已有分支
git worktree add -b <new-branch> <path> <base> # 新分支+新工作区(最常用)
git worktree list                             # 列出所有工作区(路径/分支/HEAD)
git worktree remove <path>                    # 移除(需先提交/清理, 加 --force 强删)
git worktree prune                            # 清理已删除目录的失效元数据
```

**并行标准姿势**（N 个任务 → N 个 worktree + N 个进程）：
```bash
git worktree add -b feat/issue-78 /tmp/issue-78 main   # 每个任务一个分支+目录
git worktree add -b feat/issue-99 /tmp/issue-99 main
# 每个 worktree 起独立进程(如 codex -p 或 agent 工位), 并行干活
```

## 2️⃣ 全家桶场景映射

| 场景 | worktree 用法 | 关联 skill |
|------|--------------|-----------|
| **外部编码器委派** | 每个任务一个 worktree,主工作区零污染;codex 在独立目录干活 | `codex-agent` / `claude-code` |
| **多 Agent 并行** | 每个 Agent 一个 worktree + 独立分支,互不锁文件 | `agent-ops` / `dev-team` |
| **PR 审查** | check out 到独立 worktree 审查,不污染正在开发的区 | `open-code-review` / `code-review` |
| **实验/spike** | 一次性 worktree,验证后丢弃(remove --force),主区干净 | `spike` |
| **hotfix 并行** | hotfix 分支 worktree + 主开发分支同时进行,互不阻塞 | `git-workflow` |
| **发布** | 发布分支独立 worktree,验证打包不干扰主开发 | `release-ops` |

## 3️⃣ 与 codex-agent 配合（实测模式）

```bash
# 批量修 bug: 每个 issue 一个 worktree + 一个后台 codex
for issue in 78 99; do
  git worktree add -b fix/issue-$issue /tmp/issue-$issue main
  cd /tmp/issue-$issue && codex exec --full-auto "fix issue #$issue" &
done
wait
# 验证 → 合并 → 清理
for issue in 78 99; do git worktree remove /tmp/issue-$issue; done
```

## 4️⃣ 陷阱表（必读）

| 陷阱 | 后果 | 解法 |
|------|------|------|
| **同一分支被两个 worktree 检出** | 报错 `already checked out` | 并行任务必须用**不同分支**(-b 新建) |
| worktree 有未提交改动就 remove | 报错,删不掉 | 先 commit/stash,或 `remove --force`(丢改动) |
| 删除分支前没移除 worktree | 分支删不掉 | 先 `git worktree remove`,再 `git branch -D` |
| 主工作区想 remove | 删不掉(初始工作区) | 不能删;只删附加的 worktree |
| 忘记 prune | worktree list 残留脏数据 | 定期 `git worktree prune` |
| worktree 里 git 操作路径混淆 | 改错仓库 | 每个 worktree 内用相对路径,先 `pwd` 确认 |

## 5️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| `already checked out` | 换分支: `git worktree add -b 新分支 路径 基线` |
| remove 报脏 | 检查 status,先 commit/stash;确实不要 → `--force` |
| 找不到 worktree 目录 | `git worktree list` 看真实路径 |
| 多进程并行冲突 | 每个 worktree 用独立分支 + 独立输出文件(日志/报告分开) |
