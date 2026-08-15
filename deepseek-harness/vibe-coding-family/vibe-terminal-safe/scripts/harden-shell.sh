#!/usr/bin/env bash
# ============================================================
# vibe-terminal-safe 命令白名单硬拦截器
# 用法：source 此文件后，用 vibe_cmd 执行命令；或作为 bash 包装器
#   source harden-shell.sh && vibe_cmd "npm test"
# 高危命令被拦截，写操作记审计日志到 .snapshots/audit.log
# ============================================================

AUDIT_LOG="${VIBE_AUDIT_LOG:-$(pwd)/.snapshots/audit.log}"

# --- 高危命令模式（硬拦截） ---
DANGEROUS_PATTERNS=(
  'rm -rf'
  'rm -fr'
  'sudo '
  'mkfs'
  'dd if='
  'fdisk'
  'shutdown'
  'reboot'
  'kill -9'
  'DROP TABLE'
  'TRUNCATE'
  'flushall'
  'git push --force'
  'git reset --hard'
  'curl .*|.*bash'
  'wget .*|.*sh'
)

# --- 写操作命令（需记录审计） ---
WRITE_PATTERNS=(
  'mkdir'
  'touch'
  '>'
  '>>'
  'pip install'
  'npm install'
  'git commit'
  'git push'
  'cp '
  'mv '
  'sed -i'
  'python.*-m.*migrate'
)

vibe_cmd() {
  local cmd="$1"
  local blocked=0

  # 1. 高危命令拦截
  for pat in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$cmd" | grep -qE "$pat"; then
      echo "🛡️ [硬拦截] 高危命令被禁止: $pat" >&2
      echo "  cmd: $cmd" >&2
      echo "$(date '+%Y-%m-%d %H:%M:%S') BLOCKED [$pat] $cmd" >> "$AUDIT_LOG"
      return 1
    fi
  done

  # 2. 写操作审计
  for pat in "${WRITE_PATTERNS[@]}"; do
    if echo "$cmd" | grep -qE "$pat"; then
      mkdir -p "$(dirname "$AUDIT_LOG")"
      echo "$(date '+%Y-%m-%d %H:%M:%S') WRITE [$pat] $cmd" >> "$AUDIT_LOG"
      break
    fi
  done

  # 3. 执行
  eval "$cmd"
}

# 别名：vibe 命令入口
alias vibe=vibe_cmd

# 导出给子进程
export -f vibe_cmd
export AUDIT_LOG
