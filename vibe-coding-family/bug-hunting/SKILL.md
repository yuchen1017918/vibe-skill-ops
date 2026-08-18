---
name: bug-hunting
description: |-
  缺陷猎手——bug 全生命周期管理：发现（三角色对抗）→编号入档→三层修复（短期止血能用/空闲根治还技术债）→哨兵防复活→回归测试→bug 记忆。
  三态追踪：活跃 active / 不活跃 dormant / 已灭绝 extinct，哨兵报警=复活回到活跃。
  当用户说"记bug"、"bug追踪"、"缺陷管理"、"这个bug又出现了"、"回归测试"、"大更新后检查"、"配哨兵"时加载。
  触发词：bug追踪、记bug、缺陷、回归测试、哨兵、bug复活、技术债、根治、防复发。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, bug, regression, sentinel, quality, memory]
    related_skills: [systematic-debugging, vuln-memory, snapshot-notes, project-tracker-dashboard, doubt-driven-development, code-review]
---

# Bug Hunting（缺陷猎手）

**来源融合**：danpeg/bug-hunt（三角色对抗发现）+ lohani-mohit/shipcheck（双审查回归）+ RRFRRF/project-memory-skill（bug queue）+ chris-short/respect-the-oracle（哨兵测试纪律）。

**与全家桶分工**（不重叠，各管一段）：
- `systematic-debugging`：**单个 bug 怎么修**（四相流程+防御验证三原则）→ 本 skill 修 bug 时调它
- 本 skill：**全部 bug 怎么管**（发现/编号/记忆/哨兵/防复活/回归）
- `vuln-memory`：安全漏洞记忆（CWE 分类）；本 skill 的 bug 档案=功能缺陷（含安全，不止安全）
- `snapshot-notes`：项目状态快照；bug 档案=bug 级专用记忆（跨会话可查）
- `project-tracker-dashboard`：看板渲染 .vibe/bugs/ 成三区面板

## 1️⃣ Bug 编号与档案

- 目录 `.vibe/bugs/`，文件 `BUG-NNN.md`，NNN 从 001 递增，**编号终身制**（修复/灭绝后不回收）
- 档案模板见 §7。**每个 bug 一个档案**：症状/定位/修复/哨兵/时间线/教训
- 跨会话稳定：任何会话都能凭编号查到完整历史

## 2️⃣ 三态状态机

```
发现 ──→ 活跃 active ──L2修复──→ 不活跃 dormant ──L3根治+哨兵──→ 已灭绝 extinct
                ↑                        │                              │
                └────── 哨兵报警=复活 ─────┘（复活次数+1，回活跃）       └─ 观察期 30 天哨兵未触发
```

| 状态 | 含义 | 处理 |
|------|------|------|
| **active 活跃** | 刚发现/修复中/复活 | 按 §4 三层修复 |
| **dormant 不活跃** | 短期修复已上，哨兵监视中，等根治 | 排队等空闲根治 |
| **extinct 已灭绝** | 根治完成+哨兵守满 30 天观察期 | 归档，不删除 |
| **resurrected 复活** | 哨兵报警，bug 回来了 | 复活次数+1，回 active 继续修 |

## 3️⃣ 发现机制（三角色对抗 — bug-hunt 精华，可选委派）

普通发现（测试失败/报错）直接入档。**主动扫雷**用三角色（delegate_task 3 个隔离子 agent，只传结构化发现，互相看不到推理）：

| 角色 | 任务 | 评分激励 |
|------|------|----------|
| **Hunter 猎人** | 扫代码报出所有可能的 bug | +1/+5/+10（低/中/高严重），激励多报 |
| **Skeptic 怀疑者** | 逐条反驳假阳性 | 驳倒假阳性得分；**误杀真 bug 扣 2 倍**（校准谨慎） |
| **Referee 裁判** | 独立读代码做最终裁决 | 对称 +1/-1，精确优先 |

支持分支 diff 模式：只扫 `git diff <feature>..<base>` 变更的文件（读全文非 diff，保证质量）。

## 4️⃣ 三层修复策略

| 层 | 时机 | 动作 | 记录 |
|----|------|------|------|
| **L1 定位** | 接到 bug | `systematic-debugging` 四相：根因调查→模式分析→假设验证→实施 | 档案§定位过程 |
| **L2 短期修复** | 立即 | 最小改动止血，**能用就行**；代码标 `# BUG-NNN: band-aid` 注释 | 档案§短期修复+技术债标记 |
| **L3 根治** | **空闲时** | 全项目定位根源彻底修复还技术债，移除 band-aid，升级灭绝候选 | 档案§根治方案 |

> 铁律：L2 止血 ≠ 完事。每个 band-aid 都是欠条，空闲时还债（L3）。

## 5️⃣ 哨兵机制（防复活核心）

**每个 bug 根治后必须配 ≥1 个哨兵**，让 bug 复活即报警：

| 哨兵类型 | 示例 | 适用 |
|----------|------|------|
| 回归测试用例 | `tests/test_x.py::test_bug_001`（注释标 BUG-NNN） | 逻辑 bug |
| 防御校验 | 入口校验/断言（联动 systematic-debugging Defense-in-Depth） | 非法数据类 |
| 监控探针 | cron 脚本定期探活（复用 Hermes cron no_agent 看门狗模式） | 环境/服务类 |
| CI 检查 | lint/typecheck/构建闸门 | 编译/类型类 |

**哨兵纪律（respect-the-oracle 精华）**：哨兵必须测**真实行为**——禁止过拟合可见样本、禁止"测试绿了但功能坏"。哨兵测试自己也要被审查（测试错≠代码对）。

**复活循环**：哨兵报警 → 档案时间线记"复活" → 状态回 active → 继续修（复活次数+1）。复活说明哨兵抓住了，修复策略要换（L2 治标已失效，直接上 L3 或换根因假设）。

## 6️⃣ 回归测试约定（每次大更新后）

大功能/重构/发布前必做：

1. **全量哨兵跑测**：`.vibe/bugs/` 所有 active+dormant 的哨兵命令全跑
2. **双审查并行**（shipcheck 精华）：delegate_task 两个隔离审查员——
   - **Regression Hunter**："这个改动破坏了哪些已经工作的东西？"
   - **Change Reviewer**："它真做到了声明的事吗（含边界）？"
3. **三档裁决**（附 file:line 证据）：`SIGN OFF`（放行）/ `SIGN OFF WITH NITS`（小修放行）/ `DO NOT SHIP`（打回）
4. 失败项：新 bug 入档（新编号）或已灭绝 bug 复活（哨兵命中）

## 7️⃣ Bug 档案模板

```markdown
# BUG-NNN <一句话标题>
<!-- bug-meta
状态: active | dormant | extinct | resurrected
严重级: blocker | critical | minor | suggestion
发现: 2026-08-17
复活次数: 0
-->
## 症状
<现象 + 复现步骤 + 影响范围>
## 定位过程
<systematic-debugging 四相记录：根因假设→证据→结论>
## 短期修复 (L2)
- 日期: <YYYY-MM-DD>，状态: 已上
- 方案: <band-aid 描述，能用就行>
- 技术债: <欠了什么，L3 还>
## 根治方案 (L3)
- 日期: -（空闲时执行后填）
- 方案: <全项目定位根源后的彻底修复>
## 哨兵
- 类型: <回归测试/防御校验/监控探针/CI>
- 位置: <文件:函数 / 命令>
- 状态: 守夜中 / 已触发(复活)
## 时间线
- 2026-08-17 发现 → L2 修复 → ...
## 教训
<沉淀到 global-experience 的模式级教训>
```

## 8️⃣ 与看板联动

`project-tracker-dashboard` 读 `.vibe/bugs/*.md` 渲染 Bug 追踪面板：活跃/不活跃/已灭绝三区 + 编号归类 + 三层修复进度条（定位→止血→根治→哨兵）+ 复活次数徽章。

## 快速排障

| 症状 | 处理 |
|------|------|
| 编号冲突 | ls .vibe/bugs/ 取最大号+1，勿复用 |
| 哨兵误报 | 先修哨兵（测试本身错）再判复活；哨兵要测真行为 |
| L2 反复复活 | 说明根因假设错了，回 systematic-debugging Phase 1 重查 |
| 档案找不到 | 编号唯一终身制，grep .vibe/bugs/ 按关键词找 |
| 灭绝 bug 又现 | 哨兵守夜期不够/哨兵有盲区 → 复活次数+1，补更强的哨兵 |
