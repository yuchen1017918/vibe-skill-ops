---
name: systematic-debugging
description: |-
  4 阶段根因调试：先理解再修（错误三分支→根因调查→模式分析→假设验证→实施）。
  v1.2 防御验证三原则：Defense-in-Depth 多层校验 / Verification Gate 验证门 / Root Cause Tracing 根因回溯。
  当遇到任何 Bug、测试失败、意外行为、或声称修复/完成前需要验证时加载。
  触发词：调试、bug、测试失败、根因、定位问题、修不好。
version: 1.2.0
author: Hermes Agent (adapted from obra/superpowers, claudekit-skills)
license: MIT
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [vibe-code-search, code-review, security-audit]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

**Stop-the-Line Rule**（v1.1 新增 — 参考 addyosmani/agent-skills）：发现生产缺陷（或怀疑有），**先停止流水线修，不带着 bug 继续开发**。带病迭代 = 错误放大，返工指数增长。

**错误三分支 triage 表**（接到错误先分类再动手）：

| 错误类型 | 特征 | 处理 |
|---------|------|------|
| 构建错误 | 编译/依赖/语法 | 修配置/依赖/语法，先看构建日志头部 |
| 测试错误 | 断言失败/测试挂 | 先看是测试错还是代码错（测试错→修测试，代码错→修代码） |
| 运行时错误 | 崩溃/异常/性能 | 拿完整堆栈+复现步骤，定位根因再修 |

> 三分支共享同一原则：**拿真实错误，不臆测**。

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- 修完写回归测试（证明修复 + 防复发，见下「With tests」）

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## 防御与验证三原则（v1.2 新增 — claudekit 精华）

四相流程之上，叠加三条"让 bug 不可能发生"的原则。定位：Phase 4 修完之后还要过这三道闸。

### 1. Defense-in-Depth Validation（多层防御验证）

修一个由非法数据引起的 bug 时，只在一处加校验不够——单点校验会被其他代码路径/重构/mock 绕过。
**原则：在数据经过的每一层都验证，让 bug 结构性不可能发生。**

四层校验（分层各抓不同 case）：

| 层 | 位置 | 抓什么 |
|----|------|--------|
| L1 入口校验 | API 边界/函数入口 | 明显的非法输入（空值/类型/不存在） |
| L2 业务逻辑校验 | 操作执行前 | 数据对本次操作是否有意义 |
| L3 环境守卫 | 上下文/配置 | 特定环境下的危险组合 |
| L4 调试日志 | 各层失败时 | 其他层都漏了时的最后线索 |

### 2. Verification Gate（验证门 — 声称完成前必过）

**没有验证证据的完成声明是撒谎，不是效率。**

```
BEFORE 声称任何状态/成功：
1. IDENTIFY: 哪条命令能证明这个声明？
2. RUN: 完整执行（fresh, 不拿旧结果）
3. READ: 看全输出 + exit code + 失败数
4. VERIFY: 输出真的支持声明吗？
   - 不支持 → 如实报告实际状态+证据
   - 支持 → 带着证据声明
5. 然后才能声明
```

| 声称 | 需要 | 不算数 |
|------|------|--------|
| 测试通过 | 测试命令输出: 0 failures | 上次跑过 / "应该能过" |
| Lint 干净 | Lint 输出: 0 errors | 抽查 / 外推 |
| 构建成功 | 构建命令 exit 0 | Lint 过了 / 日志看着行 |
| Bug 已修 | 原始症状复现命令通过 | 改了代码 / 假设已修 |

### 3. Root Cause Tracing（根因回溯 — 修在源头不在症状处）

Bug 常在调用栈深处显形，本能是在出错处修——那是治标。
**原则：沿调用链向上回溯，找到原始触发器，在源头修。**（Phase 1 §5 Trace Data Flow 的强化版）

```
症状:  Error: git init failed in /path/xxx
直接原因: await execFileAsync('git', ['init'], { cwd: projectDir })
追问:  谁传了错的 projectDir？→ 上游函数 → 直到找到"错值从哪进入"
修法:  在源头修（+ 顺手加 L1 入口校验 = defense-in-depth 闭环）
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Common Library-Specific Pitfalls

See `references/python-async-pitfalls.md` for aiohttp, asyncio, and Python version quirks
encountered during debugging sessions. Load with `skill_view(name='systematic-debugging', file_path='references/python-async-pitfalls.md')`.

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With tests (bugfix 回归测试)

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
