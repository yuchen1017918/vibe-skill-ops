# addyosmani/agent-skills 精华补充（按需加载，不膨胀正文）

> 来源：https://github.com/addyosmani/agent-skills（✅ 已验证真实）
> 使用：涉及对应主题时加载本节相关条目，其余跳过。已并入正文的精华不重复收录
> （五轴审查→code-review / Stop-the-Line→systematic-debugging / 垂直切片→karpathy-coding-dscpln /
> Threat Model→security-audit / Save Point→git-workflow / ADR→project-init）。

## 一、设计/架构类

| 精华 | 一句话 | 联动 |
|------|--------|------|
| **Hyrum's Law** | 所有可见行为都是契约（用户会依赖你的任何行为，包括 bug）——改"内部实现"前评估可见影响 | api-development |
| **One-Version Rule** | API 不做破坏性升级：加新端点/新参数，保留旧行为，弃用再移除 | api-testing-contracts |
| **Chesterton's Fence** | 拆/删代码前先理解它为什么存在（栅栏不拆除非知道它的用途） | simplify-code |
| **Preserve Behavior Exactly** | 重构 = 纯行为保持，改前测试锁定行为，改后 diff 验证无行为变化 | simplify-code / karpathy |
| **Code Is a Liability** | 代码是负债不是资产——能删就删，新功能优先考虑不加代码的解法 | deprecation-and-migration |
| **Compulsory vs Advisory 废弃** | 废弃分强制（必须迁移）和建议（可暂留）两级，迁移计划从设计时开始 | release-ops |

## 二、工程流程类

| 精华 | 一句话 | 联动 |
|------|--------|------|
| **Gated Workflow** | Specify 阶段不写码（闸门）——规格未冻结前禁止进入实现 | project-init / superpowers |
| **Spec 模板字段** | Objective / Stack / Commands / Boundaries（规格必备四字段） | project-init |
| **依赖图先行** | 排任务前先画依赖图（谁依赖谁），再定顺序 | kanban-orchestrator / project-init |
| **Checkpoint 检查点** | 任务 1-3 后强制校验（方向对不对），不闷头跑完全部 | agent-loop / kanban-orchestrator |
| **Task Sizing** | 任务粒度标准：能 1 天内完成、可独立验证、边界清晰 | project-init |
| **Prove-It Pattern** | 修 bug 先写失败测试证明 bug 存在，再修到测试绿 | test-driven-development |
| **Test State, Not Interactions** | 测状态结果不测调用序列（防脆弱测试） | test-driven-development |
| **DAMP > DRY** | 测试里可读性优先于去重（Descriptive And Meaningful Phrases） | test-driven-development |

## 三、性能/质量类

| 精华 | 一句话 | 联动 |
|------|--------|------|
| **Performance Budget** | 预算先行：定指标上限（如 LCP < 2.5s），超预算 = 不合并 | python-performance |
| **Core Web Vitals 目标表** | LCP ≤2.5s / INP ≤200ms / CLS ≤0.1（Web 性能基线） | performance-testing |
| **Measure→Identify→Fix→Verify** | 性能优化四步：先测量→定位→修复→验证，不凭感觉优化 | python-performance |
| **先定义 "working" 再插桩** | 加日志/指标前先明确"正常"长什么样，再决定观测什么 | monitoring-observability |

## 四、上线/流程类

| 精华 | 一句话 | 联动 |
|------|--------|------|
| **Pre-Launch Checklist** | 上线前六维检查：代码质量/安全/性能/可访问性/基础设施/文档 | release-ops |
| **Staged Rollout + 回滚阈值** | 分阶段放量（1%→10%→100%），定义回滚触发阈值 | release-ops |
| **Quality Gate Pipeline** | CI 质量门禁：未过测试/审查/安全检查 = 不合并不部署 | github-actions |
| **CI 失败反馈回 agent** | CI 失败不是"告诉用户"而是"拿回错误修好再推" | github-actions / agent-loop |
| **预览部署 + Feature Flags** | 新功能先预览环境 + Flag 控制，全量上线前可随时关 | release-ops |

## 五、AI 协作/设计类

| 精华 | 一句话 | 联动 |
|------|--------|------|
| **6 条行为准则** | Surface Assumptions（表面假设）/ Manage Confusion（管理困惑）/ Push Back（推回）/ Enforce Simplicity（强制简单）/ Scope Discipline（范围纪律）/ Verify Don't Assume（验证不假设） | vibe-skills-gov-patterns |
| **Avoid the AI Aesthetic** | 防"AI 味"设计：避免千篇一律的渐变/圆角/emoji 排版，用克制真实的设计 | frontend-design-policy |
| **WCAG 2.1 AA 落地** | 可访问性基线：对比度 4.5:1、键盘可达、aria 标注 | frontend-design |
| **want vs should want** | 用户说"想要 X"时区分：真需求 X vs 底层动机 Y（访谈技巧） | requirement-clarify |
| **95% 置信度停止** | 需求访谈：连续确认到 95% 置信就停，不无限追问 | requirement-clarify |
