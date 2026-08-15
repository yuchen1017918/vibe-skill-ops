---
name: vibe-skills-gov-patterns
description: Skill 治理模式：吸收 Vibe-Skills / VCO 一类大规模 skill OS 的治理精华 （Primary route、promotion metadata、replay ledger、destructive gate、proof bundle）， 防止全家桶 skill 数量增长后互相冲突。当用户提到 skill sprawl、promotion gate、 多个 skill 争抢控制权、治理/路由时加载。
family-type: meta
family-version: 1.5.0
---

# Vibe-Skills 治理模式（Skill 全家桶防冲突）

来源：https://github.com/Undermybelt/hermes-skills （`skills/software-development/vibe-skills-gov-patterns`，MIT）

目标
- 吸收外部 skill OS 的治理方法，不引入第二控制面。
- 让 Hermes 在 skill 数量增长后，仍保持低冲突、可验证、可冻结。
- **本全家桶的护城河**：hub 目录 + 子 skill 按阶段介入，不互相抢权。

## 何时用

- 需要设计 skill promotion / freeze / destructive gate
- 全家桶/本地 skill 数量增长，出现"多个同类 skill 同时触发"
- 需要把"大量 skills 如何不互撞"落入 Hermes 路由与治理

## 默认立场

1. Learn + Absorb，非 direct-install。
2. 先做安全审查，再决定是否隔离安装。
3. 不把外部 runtime 当 Hermes 第二 orchestrator。
4. 只吸收能降低未来 steering 的治理件。

## 高价值可迁移件（全家桶已落地）

1. **Primary route first**
   - 先选一条主路由（vibe-coding-hub），再让 specialist（子 skill）只在阶段内介入。
   - 避免多个同类 skill 同时争抢控制权。✅ 本全家桶：hub 负责总流程，子 skill 按阶段加载。

2. **Route 后再定执行级别**
   - 先决定"谁负责"，再决定规模：单代理 / 多步串行 / 可并行子任务。

3. **Promotion metadata**
   - 至少记录：promotion_eligible、contract_complete、destructive、snapshot_required、rollback_possible。
   - 没这些字段，不要谈自动 promotion。

4. **Replay-ledger-first**
   - 没有 replay / evidence ledger 的 adaptive routing 建议，不进入 promotion 讨论。
   - 先有证据，再有升格。

5. **Destructive prompt gate**
   - 对 delete / overwrite / reset / purge 类提示，单独打 destructive 标签。
   - destructive 命中时，不走无提示自动派发，需要确认 + 快照 + 回退条件三件套。
   - ✅ 对应本全家桶 `vibe-terminal-safe` 的禁止命令清单。

6. **Proof bundle / execution manifest**
   - done 不能只靠自然语言，要有测试、产物、验证路径、执行摘要等可检查证据。
   - ✅ 对应 `karpathy-coding-dscpln` 的 Goal-Driven Execution。

7. **Workspace memory plane**
   - 可吸收"单控制面 + workspace 共享记忆"思想，但 Hermes 内 memory truth source 单一。

## Hermes 落地规则

- 路由层：一个主 skill 负责总流程；specialist 仅作为阶段辅助，不夺全局调度权。
- 治理层：promotion 必须 evidence-backed；destructive 默认保守；good skill freeze，
  middling 渐进修，bad 立即 patch 或停用。
- 记忆层：用户显式指令 > repo truth > memory policy > candidate advice。

## 不该照搬的东西

- 直接改写真实 host root 的安装器。
- 第二套 runtime authority。
- 未清洗即导入的上游 contract 名词与巨型 policy 面。
- 用"live degraded result"继续冒充完成。

## 🧪 压力测试与迭代记录（v1.1 新增 — 防止全家桶僵化）

**目的**：规则越多，互相冲突风险越高。给每条规则"为什么存在"的证明，
长期未触发或频繁被覆盖的规则自动标记待废弃。

### 场景冲突模拟（加载新 Skill / 更新规则时强制）

```
1. 列出与改动相关的既有 skill（related_skills + tags 交集）
2. 模拟 2-3 个典型场景（新需求 / 疑难 Bug / 多Agent协作）：
   - 新规则触发时，谁还同时触发？→ 会不会抢控制权？
   - 两个规则对同一场景给相反指令？→ 记录冲突
3. 冲突解决：修改措辞加限定条件 / 明确优先级（Primary route 优先）/
   无法调和 → 废弃新规则
4. 模拟结果写入 skill 的变更记录
```

### 迭代记录（Changelog，每条规则必须留痕）

```markdown
## 规则变更记录
| 日期 | 规则 | 为什么加 | 解决的痛点 | 触发次数 | 状态 |
|------|------|----------|------------|----------|------|
| 2026-08-06 | 复杂度分层 Triage | 防止微小改动上全套流程 | Token 浪费/进度拖慢 | - | active |
```

**skill 分类与保鲜**（v1.2 升级 — 区分高频/保险/元，防误杀救命 skill）：

| 类型 | 定义 | 保鲜策略 |
|------|------|----------|
| 高频型 | 日常触发（snapshot-notes、vibe-coding） | 90 天未触发 → 🟡 黄色告警 → 检查是否路由失效 |
| 保险型 | 触发一次就救命（rollback-backup、security-audit） | 180 天未触发 → 🔵 蓝色提示 → 运行一次模拟演练 |
| 元型 | 系统级（fallback-general-dev、vibe-skills-gov-patterns） | 永不自动废弃，每季度人工 review |

**场景冲突模拟的范围控制**（v1.2）：
- 不是"全量模拟"，而是"影响面模拟"——只模拟与被更新 skill 有直接依赖关系（related_skills）的 skill
- 模拟结果只标记"冲突风险等级"，不阻塞发布（避免过度保守）

**废弃流程**（v1.2 — 30 天冷静期）：
```
1. 标记待废弃 → 写入 ~/.vibe/deprecation/
2. 30 天冷静期 → 期间如果被触发，自动取消标记
3. 冷静期结束 → 归档到 ~/.vibe/archive/，保留 1 年可恢复
```

## 🔗 合并审查机制（v1.5 — 大道至简的执行器）

**目的**：skill 数量增长 = 加载决策变多 + 触发词打架。**合并优先于新增**。

**季度合并审查**（每季度或用户主动触发,由 cost-agent 月报的"证据消费"驱动）：

| 信号 | 判定 | 动作 |
|------|------|------|
| 触发词重叠 >50% | 两个 skill 抢同一批关键词 | 合并候选 |
| 30 天未加载（高频型） | 没人用 | 标记 deprecated（走废弃流程） |
| 一方总被另一方引用 | A 的职责被 B 覆盖 | 合并候选(A→B) |

**合并执行规范**（v1.3 已执行 3 组）：
```
1. 新建合并 skill:吸收双方核心 + 新增整合价值(如 project-init 吸收嗅探)
2. 被合并方:description 加 ⚠️ deprecated 标注 + 从索引移除
3. 文件保留(防交叉引用破坏),不物理删除
4. 路由表/触发词/类型计数/README 全量同步
5. 合并后验证:全量索引零缺失零重复
```

**新增 skill 门槛**（v1.5 — 防回潮）：
- 必须证明:无法由现有 skill 组合实现(组合尝试过)
- 必须指明与哪些现有 skill 触发词冲突,冲突已解决
- 7 天冷静期:先写草案不注册,7 天后再决定是否转正

> 合并不是损失:是让"该用哪个"的答案更少、更清晰。

## 🪞 元治理审查 v2.0（v1.4 升级 — 事件驱动，而非时间驱动）

**目的**：治理 skill 本身的 bug（误分类/规则冲突/环路）会导致系统性失效。
**v2.0 核心变更**：取消"每月自动运行"（文档体系下没人触发=僵尸流程），改为**事件驱动**。

| 触发事件 | 自动执行的审查项 |
|----------|------------------|
| 新增/修改 skill 后 | policy 冲突矩阵（只扫描与被改 skill 相关的约束） |
| fallback-general-dev 被触发后 | fallback 环路检测（检查是否进入循环） |
| 用户/Agent 输入 `/governance-check` | governance 自检 |
| 权限相关操作失败 3 次后 | 权限递归审计 |

**审查输出**（不是报告文件，而是结构化摘要）：
- ≤20 行，直接插入当前对话上下文，供即时处理
- 无异常时零输出（不打扰）
- 必须包含**置信度**（高/中/低）；置信度低 → 强制建议人工复核

**审查者的诚实性**：
- 承认单机环境无法做到真正的第三方审查——审查由当前 Agent 实例执行
- 缓解：审查逻辑独立成章节（本 skill），审查结果带置信度，低置信度强制人工

## 全家桶应用检查（验收）

- 是否减少 skill 冲突？→ hub 目录 + 按阶段加载 ✅
- 是否让 promotion 更可证？→ 每轮改动 diff + commit ✅
- 是否把 destructive 动作挡在更早处？→ 终端白名单 + destructive gate ✅
- 是否未引入第二控制面？→ 单一 hub 总路由 ✅
