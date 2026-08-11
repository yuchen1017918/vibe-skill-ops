---
name: codex-agent
description: |
  主Agent(Hermes)调用 OpenAI Codex CLI 执行编码任务的完整工作流：功能开发、重构、
  PR审查、批量bug修复。本机已配置 DeepSeek provider（国内可用），含实测验证过的命令、
  后台监控、并行 worktree、坑与排障。当用户说「用codex干活」「让codex写代码」
  「委派编码给codex」时使用。触发词：codex、OpenAI CLI 编码代理。
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [Coding-Agent, Codex, OpenAI, DeepSeek, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent, vibe-coding-hub]
---

# Codex Agent 调用手册（Hermes → Codex）

把编码任务委派给 [Codex CLI](https://github.com/openai/codex)（OpenAI 自主编码代理）。
本 skill 记录**本机实测验证过**的完整流程与坑，适合国内环境（DeepSeek 后端）。

## 1️⃣ 本机环境事实（2026-08 实测）

| 项 | 值 |
|----|-----|
| 版本 | codex-cli **0.147.0**（npm 全局安装） |
| 可执行文件 | `~/.npm-global/bin/codex`（已在 `~/.bashrc` PATH） |
| 模型后端 | **DeepSeek**（`~/.codex/config.toml` 配置，model=`deepseek-chat`） |
| API key | 环境变量 `DEEPSEEK_API_KEY`（已在 bashrc export，来源宿主环境变量文件） |
| 沙箱 | bubblewrap 0.6.1 已装（原生沙箱生效） |

配置模板（~/.codex/config.toml）：
```toml
model = "deepseek-chat"
model_provider = "deepseek"

[model_providers.deepseek]
name = "DeepSeek"
base_url = "https://api.deepseek.com/v1"
env_key = "DEEPSEEK_API_KEY"
```

## 2️⃣ 前置检查（每次调用前快速确认）

```bash
which codex || npm install -g @openai/codex --registry=https://registry.npmmirror.com
export DEEPSEEK_API_KEY=$(grep '^DEEPSEEK_API_KEY=' ~/.hermes/.env | cut -d= -f2-)  # 若 bashrc 已 export 可跳过
```

- **必须在 git 仓库内运行** — Codex 拒绝在非 git 目录运行。临时任务：
  `cd $(mktemp -d) && git init -q`
- 交互式命令必须 `pty=true`（Codex 是交互式终端应用）

## 3️⃣ 调用模式

### 一次性任务（exec，推荐）
```bash
# 普通一次性（只读沙箱，需审批写操作）
codex exec "给 settings 页加暗色模式开关"          # workdir=项目目录
# 全自动（沙箱内自动批准工作区改动）
codex exec --full-auto "重构 auth 模块，提交时注明"
# 快速粗暴（无沙箱无审批，慎用）
codex exec --yolo "修掉这个 bug"
```

### 后台长任务（必须 background=true 监控）
```bash
# 启动（workdir=项目目录, background=true, pty=true）
codex exec --full-auto "把 batch 处理逻辑改成异步队列"
# 监控
process(action="poll", session_id="<id>")    # 状态+新输出
process(action="log", session_id="<id>")     # 完整输出
process(action="submit", session_id="<id>", data="yes")  # 若 codex 提问
process(action="kill", session_id="<id>")    # 需要时终止
```

### 并行任务（git worktree）

> 完整 worktree 指南见 `git-worktree` skill（命令/陷阱/场景映射）。此处是 codex 视角速记：
```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main
# 每个 worktree 起一个后台 codex
codex exec --full-auto "修复 issue #78: <描述>"   # workdir=/tmp/issue-78, background=true
codex exec --full-auto "修复 issue #99: <描述>"   # workdir=/tmp/issue-99, background=true
# 完成后推送+建 PR
git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."
# 清理
git worktree remove /tmp/issue-78
```

### PR 审查
```bash
# 安全方式：clone 到临时目录再审查
REVIEW=$(mktemp -d) && git clone <repo> $REVIEW && cd $REVIEW && gh pr checkout 42
codex review --base origin/main          # workdir=$REVIEW, pty=true
# 批量审查多个 PR
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'
codex exec "审查 PR #86: git diff origin/main...origin/pr/86"   # 每个 PR 一个后台进程
gh pr comment 86 --body "<审查结果>"
```

## 4️⃣ 验证（委派后必须做）

- Codex 完成标志：exec 输出含 `tokens used` 行
- 检查实际产物：`git status` / `git diff --stat` / 文件变更
- 代码质量抽查：读关键 diff，确认改动合理
- **子代理自报不可全信**：codex 说"完成"不等于正确，验证文件真的改了、测试能跑

## 5️⃣ 坑与排障（实测）

| 症状 | 原因 | 处理 |
|------|------|------|
| `wire_api = "chat" is no longer supported` | Codex ≥0.147 移除 chat wire API | **不要写 wire_api 字段**，默认 responses；DeepSeek 实测兼容 |
| `Model metadata for deepseek-chat not found` | 自定义 provider 无模型元数据 | warning 无害，fallback metadata 运行 |
| `Could not find bubblewrap on PATH` | 沙箱依赖缺失 | `sudo apt install bubblewrap`；缺失时用捆绑版不阻塞 |
| `Error loading configuration: ...` | config.toml 语法/字段错 | 按 §1 模板检查 |
| npm 12 报 `EBADDEVENGINES` | npm 12.0.2 检查 devEngines（node ^22.22.1 vs v24） | 只影响 `npm config get` 类命令，**install 正常**，忽略即可 |
| 命令找不到 codex | PATH 未含 ~/.npm-global/bin | `export PATH="$HOME/.npm-global/bin:$PATH"`（bashrc 已加） |
| 非 git 目录报错 | Codex 强制 git repo | `mktemp -d && git init` |
| 任务卡住 | 长任务/等待审批 | 后台模式 + process poll/log；需要时 submit 回答或 kill |
| DeepSeek 额度/限流 | API 侧 | 检查 key 余额；换 model（deepseek-v4 系列） |

## 6️⃣ 使用原则

1. **exec 优先**：一次性任务用 `codex exec`，跑完干净退出
2. **后台+监控**：长任务必配 `background=true` + process 监控
3. **pty=true**：交互模式/需要 codex 提问回答时
4. **git repo 必须**：临时任务先 `git init`
5. **--full-auto 用于构建**：自动批准沙箱内工作区改动；`--yolo` 仅限可信环境
6. **验证产物**：codex 说完成 ≠ 真完成，检查 git diff 和测试
7. **并行 OK**：worktree 多开互不干扰

## 7️⃣ 与全家桶衔接（v2.1 — 融合到 vibe-skill-ops 索引）

本 skill 是全家桶「AI 编码器委派」的外部工具之一，由 `dev-agent-hub`（L2 智能体与治理层）注册路由：

- **委派前**：先走全家桶主流程确认（`vibe-coding-hub` 一句话画像：团队/企业 × 助手/全盘）。用户说"用 codex 干活"默认路径 → `dev-agent-hub` → 本 skill
- **委派中**：任务边界、验收标准写清楚（同全家桶 `agent-permissions` 权限观）；codex 的沙箱/审批纪律 = `vibe-terminal-safe` 白名单哲学的 CLI 侧对应
- **委派后**：产物必须按 §4 验证 + 走全家桶 `security-audit`（提交前扫描）与 `release-ops`（发布/回滚），**不接受"codex 说完成了"作为完成证据**
- **与 claude-code 并列**：同属外部编码器委派族（`related_skills: [claude-code]`），按用户指定选择，不互相替代
