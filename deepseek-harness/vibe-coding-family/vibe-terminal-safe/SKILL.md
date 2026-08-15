---
name: vibe-terminal-safe
description: 安全受控终端 skill：vibe-coding 迭代时的命令执行规范。 当需要运行 build / test / npm install / pip install / 执行脚本时加载。 核心：命令白名单、禁止高危命令、超时控制、报错迭代。 v1.1 新增：安全模式（skill 报错≥3次时仅只读命令）。
family-type: policy
family-version: 1.3.0
---

# 安全受控终端（Vibe-Coding 版）

Vibe-coding 需要频繁执行构建/测试命令，但**不能裸奔**。本 skill 定义受控终端规范，
参考官方 MCP shell server 的"受控执行"思路。

## 核心规则

### 0. 风险分级（v1.3 新增 — 命令按破坏力分级）

| 级别 | 类别 | 示例 | 处置 |
|------|------|------|------|
| 🟢 Level 0 只读 | `ls` / `git status` / `grep` / `cat` | 直接执行 |
| 🟡 Level 1 局部写 | `touch` / `mkdir` / `cp` / `git add` / `npm install` | 直接执行 + 记审计 |
| 🟠 Level 2 破坏性写 | `rm` / `mv` / `chmod` / `chown` / `git reset --hard` | 拦截 + 说明理由，用户确认后执行 |
| 🔴 Level 3 系统级 | `sudo` / `mkfs` / `dd` / `fdisk` / `docker system prune` / `git push --force` | 硬拦截，必须用户明确确认 |

> 与 §7 硬拦截器的分工：本表是**分级判定标准**（决策层），`harden-shell.sh` 是**执行拦截**（强制层）。
> Level 2+ 的拦截与审计由硬拦截器落地；分级表让 Agent 在执行前先判断命令属于哪一级。

### 1. 命令白名单（默认允许）

| 类别 | 示例 |
|------|------|
| 构建 | `npm run build`, `npm run dev`, `make`, `cargo build`, `go build` |
| 测试 | `npm test`, `pytest`, `go test`, `cargo test`, `jest` |
| 安装 | `npm install`, `pip install`, `uv pip install` |
| 查看 | `git status`, `git diff`, `git log`, `ls`, `cat`（小文件） |
| 脚本 | 运行项目内的 `*.py` / `*.sh` / `*.js`（先快速审查内容） |

### 2. 禁止命令（默认拒绝，除非用户明确要求）

- ❌ `rm -rf`（尤其根目录、家目录、项目根）
- ❌ `sudo` 提权命令
- ❌ `mkfs`、`dd`、`fdisk`、`shutdown`、`reboot`、`kill -9`（进程树）
- ❌ 清空/覆盖数据库：`DROP TABLE`、`TRUNCATE`、`redis-cli flushall`
- ❌ `git push --force`、`git reset --hard`（无确认）
- ❌ 下载并直接执行未知脚本：`curl xxx | bash`

### 3. 执行前检查（Checklist）

```
□ 命令是否在白名单？
□ 是否涉及破坏性操作（删/改/覆盖）？
□ 工作目录是否正确（pwd）？
□ 是否需要先看 package.json / requirements.txt 确认脚本？
□ 超时设置是否合理（构建用 300s+）？
```

### 4. 执行中规范

- 构建/测试用 `timeout=300` 或后台执行 `background=true, notify_on_complete=true`。
- 服务类进程（dev server）用 `background=true`，配 `watch_patterns` 监听启动完成。
- 报错时：**先拿完整错误信息**（不要只看最后一行），再定位根因修复。
- 禁止无限重试：同一命令失败 3 次必须换思路。

### 5. 执行后迭代（vibe-coding 闭环）

```
改代码 → 跑 build/test → 拿到真实报错 → 基于报错修复 → 再跑 → 通过后 git commit
```

每一轮都必须走 `git-workflow` 做 diff/commit，防改崩回滚。

### 6. 安全模式（v1.1 新增 — 降级逃生）

**触发条件**：同一 skill 执行报错 ≥3 次 / L1 降级协议激活 / 用户明确要求。

**模式规则**：
```
🛡️ 安全模式（只读）：
  - 允许：git status/diff/log、ls、read_file、search_files、测试运行（只读）
  - 禁止：所有写操作（rm/mkdir/install/commit/push）
  - 动作：保存当前状态 → 输出问题报告 → 等用户决策
```

**退出条件**：用户确认修复方向 / 问题根因已定位 / 切换正确 skill。

```
安全模式流程：
1. 触发（报错≥3次 / 降级激活）
2. 停止所有写命令（仅只读）
3. 保存状态到 .snapshots/（快照笔记）
4. 输出报告：失败命令/报错摘要/根因分析/修复建议
5. 等用户决策后再恢复
```

### 7. 命令白名单硬拦截（v1.2 新增 — 宪法代码化）

**目的**：不靠"自觉"，用脚本真正拦截高危命令 + 记录审计。

```bash
# 加载硬拦截器（本 skill 附带 scripts/harden-shell.sh）
source ~/.hermes/skills/vibe-coding-family/vibe-terminal-safe/scripts/harden-shell.sh

# 之后用 vibe_cmd 执行命令（高危自动拦截，写操作自动审计）
vibe_cmd "npm test"          # ✅ 正常执行
vibe_cmd "rm -rf src/"        # 🛡️ 被拦截 + 记审计
vibe_cmd "git commit -m x"    # ✅ 执行 + 记审计（写操作）
```

**审计日志**：所有被拦截命令 + 写操作记录到 `<项目根>/.snapshots/audit.log`：
```
2026-08-06 15:30:00 BLOCKED [rm -rf] rm -rf src/
2026-08-06 15:32:10 WRITE [git commit] git commit -m "feat: x"
```

**硬拦截 vs prompt 提醒**：
| 层 | 作用 |
|----|------|
| prompt 规则（§2） | 软约束：AI 自己判断 |
| 硬拦截器（§7） | 硬约束：命令真正被拦截 + 留痕 |

## 报错处理模板

```bash
# 1. 拿到完整报错
npm run build 2>&1 | tail -50        # 或 pytest -x 2>&1 | tail -50

# 2. 定位根因（不要臆测）
grep -n "ERROR\|Error\|failed" <输出文件> | head -20

# 3. 修复后重跑，通过再提交
git add -A && git commit -m "fix: ..."
```

## 与 MCP shell 的关系

官方 `modelcontextprotocol/servers` 提供 shell MCP server（受控 shell），
配置见 `vibe-mcp-connect` skill。本 skill 是 Agent 内置 terminal 工具的使用规范，
两者可共存：MCP shell 用于隔离环境，内置 terminal 用于日常迭代。

## 快速排障

| 症状 | 处理 |
|------|------|
| 权限不足 | 检查是否为文件属主，不用 sudo 硬来，改用用户目录安装 |
| 依赖冲突 | `pip install -r requirements.txt --upgrade` 或重建 venv |
| 端口占用 | `lsof -i :端口` 找占用进程，确认后 kill（非 kill -9） |
| 构建超时 | 后台执行 + notify，或分段构建 |
