# addyosmani/agent-skills 对比分析（2026-08-11 会话成果）

来源：https://github.com/addyosmani/agent-skills（★86K，Google Chrome 团队 Addy Osmani，26 个生产级工程 skills）
对比对象：Hermes 全家桶（vibe-coding-hub v1.1 + 5 个 L2 hub + 34 个 L3 skill）
方法：批量下载 24 个 SKILL.md → 脚本提取 description+标题结构 → 逐项分类对比

## 结论速览

- **重叠 14 个**（全家桶已有同类）→ 精华可 patch 并入现有 skill，不新建文件
- **全新 8 个**（全家桶没有）→ P0 两个（值得新增 L3）、P1 四个（并入/挂载）、P2 两个

## 一、重叠 skill → 全家桶缺的精华

| addyosmani | 全家桶对应 | 精华（本地没有的） |
|---|---|---|
| code-review-and-quality | code-review + open-code-review | 五轴审查法（正确性/可读性/架构/安全/性能）+ 先审测试再审代码 + Change Sizing |
| debugging-and-error-recovery | systematic-debugging | Stop-the-Line Rule + 测试/构建/运行时错误三分支 triage 表 |
| test-driven-development | test-driven-development | Prove-It Pattern（修 bug 先写失败测试证明存在）+ Test State, Not Interactions + DAMP>DRY |
| git-workflow-and-versioning | git-workflow + git-worktree | Trunk-Based 推荐 + Save Point Pattern + Atomic Commits 细则 |
| security-and-hardening | security-audit + code-security | Threat Model First + 三层边界系统（Always Do/Ask First/Never Do）+ OWASP Top10 逐条模式 |
| code-simplification | simplify-code | Chesterton's Fence（拆前先理解为何存在）+ Preserve Behavior Exactly |
| incremental-implementation | karpathy-coding-dscpln | 垂直切片 Vertical Slices + Contract-First Slicing + 未完成功能用 Feature Flags 藏 |
| api-and-interface-design | api-development + api-testing-contracts | Hyrum's Law（所有可见行为都是契约）+ One-Version Rule + 错误语义一致性 |
| performance-optimization | python-performance + performance-testing | Core Web Vitals 目标表 + Performance Budget + Measure→Identify→Fix→Verify |
| planning-and-task-breakdown | project-init + kanban-orchestrator | 依赖图先行 + Checkpoint 强制校验 + Task Sizing 标准 |
| frontend-ui-engineering | frontend-design + frontend-design-policy | Avoid the AI Aesthetic 具体手法 + WCAG 2.1 AA 落地清单 |
| ci-cd-and-automation | github-actions + ci-cd-pipeline | 质量门禁流水线 + CI 失败反馈回 agent + 预览部署/Feature Flags |
| spec-driven-development | superpowers + project-init | Gated Workflow（Specify 阶段闸门）+ Spec 模板字段清单 |
| using-agent-skills | vibe-skills-gov-patterns | 6 条行为准则（Surface Assumptions/Push Back/Verify Don't Assume…） |

## 二、全新 skill → 价值分级

| 级别 | skill | 精华 | 落地建议 |
|---|---|---|---|
| **P0** | doubt-driven-development | CLAIM→EXTRACT→DOUBT→RECONCILE→STOP 五步怀疑循环，新鲜上下文对抗审查防假设变"事实" | 新增 L3；全家桶有 delegate_task 可直接落地 Step 3 |
| **P0** | context-engineering | 5 层上下文层级（规则→规格→源码→错误输出→会话）+ CLAUDE.md 模板 + 文件信任分级（Trusted/Verify/Untrusted） | 新增 L3；补 project-init/snapshot-notes 上下文喂食方法论 |
| **P1** | source-driven-development | 官方文档为源：Detect Stack→Fetch Docs→Implement→Cite Sources | 并入现有 skill（呼应"报错不臆测"） |
| **P1** | documentation-and-adrs | ADR 模板（Status/Date/Context/Decision/Alternatives） | 并入 project-init 的 DECISIONS.md 章节 |
| **P1** | deprecation-and-migration | Code Is a Liability + Compulsory vs Advisory 废弃分级 | 补 release-ops 缺失的"退役旧系统" |
| **P1** | shipping-and-launch | Pre-Launch Checklist 六维（代码/安全/性能/可访问/基建/文档）+ Staged Rollout | 补 release-ops 的"上线就绪度" |
| **P1** | observability-and-instrumentation | 先定义 "working" 再插桩 + 日志/指标/追踪/告警四信号选型 | 补 monitoring-observability 的开发视角 |
| **P2** | interview-me | 一次一问+附猜测 + want vs should want + 95% 置信度停止 | requirement-clarify 访谈技巧升级 |

## 三、可参考的头部仓库（已验证真实）

| 仓库 | ★ | 结论 |
|---|---|---|
| obra/superpowers | 270K | 全家桶已覆盖同理念，不装 |
| mattpocock/skills | 213K | TS 实战视角有新意，可挑 engineering 分类 |
| multica-ai/andrej-karpathy-skills | 201K | 已有 karpathy-coding-dscpln，不装 |
| anthropics/skills | 168K | 官方 17 个，本地覆盖 90%+，不装 |
| VoltAgent/awesome-openclaw-skills | 52K | OpenClaw 系目录，当发现入口 |
| VoltAgent/awesome-agent-skills | 30K | 1000+ 目录，当发现入口 |
| MengTo/Skills | 4.6K | 设计向，中等价值 |

## 四、待办（等用户批准后执行）

1. 新增 2 个 L3：doubt-driven-development + context-engineering
2. patch 并入：五轴审查→code-review、Stop-the-Line→systematic-debugging、垂直切片→karpathy-coding-dscpln、Threat Model First→security-audit、Save Point→git-workflow、ADR→project-init
3. 其余精华合并为一个 references 文件挂对应 hub，按需加载
