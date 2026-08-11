# Cross-Session Snapshot Pattern for Large Audits

When a pre-release audit is too large to complete in one conversation (iteration budget exhaustion, long runtimes), use this 4-segment snapshot format to persist progress across sessions.

## When to Use

- Audit targets 25+ bugs across 10+ files
- Agent iteration budget (40 rounds) will be exhausted before completion
- User wants to split work across multiple conversation sessions

## The 4-Segment Snapshot Template

Output this exact format at the end of EVERY session (or sub-agent completion):

```
===== 可跨对话持久化存档快照 =====

【1. 全局v1.0.0版本替换完整变更总表】
| # | 文件路径 | 原始旧文本 | 替换后版本 | 代码行号 |
|---|----------|------------|-----------|----------|

【2. 已修复Bug分级总台账】
| # | 严重等级 | 文件路径 | 问题简述 | 落地修复方案 |
|---|----------|----------|----------|--------------|

【3. 剩余未修复待办Bug分级清单】
Category A【严重阻断运行】：
- 文件:行号 | 问题简述
Category B【边界异常崩溃】：
- ...
Category C【功能逻辑缺陷】：
- ...
Category D【规范兼容性优化】：
- ...

【4. 当前校验锚点（命令执行完整输出）】
cd /path/to/project
python -c "..." 
pip install -e . && <cli> --version

===== 快照存档结束 =====
```

## Sub-Agent Sharding Strategy

For iteration budget management, split work into independent sub-agents by priority category:

| Sub-Agent | Priority | Category | Max files per run |
|-----------|----------|----------|-------------------|
| A | Highest | 严重阻断运行 (crash-level) | 6 |
| B | High | 边界异常崩溃 (edge-case) | 4 |
| C | Medium | 功能逻辑缺陷 (logic bugs) | 3 per subfolder |
| D | Low | 规范兼容性 (compliance) | All after A/B/C done |

### Rules

1. **Sequential activation**: Run sub-agents A→B→C→D, never in parallel
2. **Sub-agent isolation**: Each sub-agent has its own iteration counter, not sharing the global 40-round pool
3. **Sub-agent limit**: 25 local iterations per sub-agent max; stop and output snapshot on reaching limit
4. **Category C sharding**: Process one subfolder at a time (e.g., `llm_agent/` then `storage/` then `utils/`)
5. **Snapshot after each sub-agent**: Force output of the full 4-segment snapshot after every sub-agent completes

## Resume Protocol (New Session)

1. Copy the last snapshot into `PAST_RUN_SNAPSHOT` variable
2. Load the master prompt (with snapshot embedded)
3. Agent parses snapshot, identifies completed vs pending items
4. Resume from the next pending sub-agent in priority order
5. Skip all already-fixed items in the snapshot

## Validation Trigger

Only run validation commands (Segment 4) AFTER all sub-agents A/B/C/D are fully complete. Running mid-stream is wasted cycles.
