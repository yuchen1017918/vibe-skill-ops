---
name: quick-dev
description: |
  轻量全包开发 skill（团队·全盘）：非项目/随手做/小工具/脚本/迷你交付/
  一次性任务的正常流程。四步循环：目标一句话→最小实现→验证→收尾。
  不强制 PRD/快照/计划文档。当用户说"随手做个"、"写个脚本"、
  "帮我算一下"、"临时工具"、"一次性任务"时加载。
  超过 3 文件/多模块/长期维护 → 升级 dev-team 或 vibe-coding。
  触发词：随手做、小工具、脚本、一次性、临时、快速搞定。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, quick, script, tool, scratch, lightweight]
    related_skills: [vibe-coding-hub, dev-core-hub, vibe-terminal-safe, git-workflow, global-experience, fallback-general-dev]
---

# 轻量全包开发（Quick Dev — 团队·全盘）

**定位**：非项目开发的**正常流程**(不是降级、不是保底)。小工具、脚本、一次性任务、
随手做的活——有清晰路线可走,不用判断"我算不算项目"。

> 与 dev-team 的关系:dev-team 是"公司"(企业·全盘),本 skill 是"小团队全包"(团队·全盘)。
> 与 vibe-coding 的关系:vibe-coding 是单人做 MVP 项目(5 步流程),本 skill 是**非项目**随手做(不写 PRD/Research)。

## 🚨 触发时机

| 用户说 | 判定 |
|--------|------|
| "随手做个脚本" / "帮我算一下" / "临时工具" | ✅ 走本流程 |
| "做个 XX 工具" / "把这段数据转成 CSV" | ✅ 走本流程 |
| "做个 App / 网站 / 完整项目" | ❌ 转 vibe-coding 或 dev-team |
| "帮我重构这个项目" / "大型改造" | ❌ 转 dev-team(企业·全盘) |

## 🔄 四步循环

```
1. 目标一句话 ─→ 2. 最小实现 ─→ 3. 验证 ─→ 4. 收尾
   (说清要什么)    (不扩范围)    (能跑/结果对)  (摘要+可选沉淀)
```

### Step 1:目标一句话
- 用户需求压缩成一句话:"做什么 + 输入 + 期望输出"
- 确认歧义点(最多 1-2 个问题,不做大访谈)
- 明确边界:"不做 X"清单(防范围蔓延)

### Step 2:最小实现
- 直接写,不套框架、不预埋未来配置层(联动 karpathy-coding-dscpln)
- 标准库优先,最小依赖
- 目录从简:单文件或 src/ + 必要文件

### Step 3:验证
- 跑得起来 + 核心路径结果对(不追求覆盖率,先保证能跑)
- 用真实输入测试,不编造输出
- 报错 → 拿真实错误 → 修 → 再跑(联动 vibe-terminal-safe)

### Step 4:收尾
- 输出 1-2 句摘要:做了什么 + 怎么用 + 结果
- 可选:有价值的心得 → global-experience 沉淀(不强制)
- 可选:重要发现 → 记快照(不强制)
- 完成后不遗留 .snapshots/plans 等重文档

## ⚡ 轻量工作区

- **直接当前目录干**(不强制建项目结构)
- 需要 git 保护时:`git init`(可选)+ 改前 status/改后 diff
- 不写 DECISIONS.md / PLAN-*.md / SPEC.md(除非用户要求)

## 🚀 升级判定(内置,超出即转)

| 信号 | 动作 |
|------|------|
| 超过 3 个文件 / 多模块联动 | → 转 dev-team(企业·全盘)或 vibe-coding(单人项目) |
| 需要长期维护 / 会反复迭代 | → 转 dev-team + snapshot-notes(建项目) |
| 涉及数据库 schema / API 契约变更 | → 直接转 dev-team(需完整流程) |
| 生产敏感操作(支付/权限/安全) | → 转 dev-team + security-audit |

> 升级不是失败:是**任务变大了,路线跟着变**。提示用户"这个活超出了一次性范围,建议升级"。

## 🔗 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `vibe-terminal-safe` | Step 3 验证时的命令安全规范 |
| `git-workflow` | 改动可回退保护(可选但推荐) |
| `karpathy-coding-dscpln` | 最小实现纪律:不预埋、不抽象、不顺手改 |
| `global-experience` | 收尾的可选沉淀 |
| `fallback-general-dev` | **不冲突**:本 skill 是正常流程,fallback 是降级兜底(路由失败时) |
| `dev-team` | 升级目标(任务变大时) |

## ⚠️ 边界声明

- 本 skill **不做项目化**:不建 docs/dev-team、不写 PRD、不做多 Agent 编排
- 本 skill **不长期持有**:一次性交付,不留维护负担
- 判断"算不算项目"不需要用户纠结——**一句话目标清晰 + 单次交付 = 走这里**;再复杂就升级

## 快速排障

| 症状 | 处理 |
|------|------|
| 做着做着发现变大了 | 停下,按升级判定转 dev-team,把已有代码作为起点 |
| 用户想要完整项目 | 一开始就转 vibe-coding,不硬套本流程 |
| 没有 git 保护 | 至少改前备份原文件,或 git init 后提交 |
| 验证不过 | 拿真实报错 → 定位 → 修复 → 重跑(最多 3 次,超了换思路) |
