# Vibe-Skill-Ops 本地升级评估报告 v1.2.0

> 评估对象:Vibe-Coding Skill 全家桶(本地测试版 v1.2.0,31 skills)
> 评估日期:2026-08-07
> 仓库位置:`/home/yuchen_wang/workspace/vibe-skill-ops`(本地,未推送上游)

---

## 第一部分 全家桶全景介绍

### 1.1 定位

**Vibe-Coding Skill 全家桶**是运行在 Hermes Agent 上的一套自治理 skill 体系——用文档化的
路由、纪律与治理规则,把"AI 写代码"组织成可预测、可约束、可复盘的生产流程。它不是软件,
不包含任何可执行程序;它的全部载体是 31 个 SKILL.md 文档,通过 Hermes 的 skill 加载机制生效。

**四层组织路由**(v1.2 重构后)是它的骨架:

```
L1  组织形态   团队(轻量项目)              企业(大型项目)
              ┌──────────────┐           ┌──────────────┐
L2  开发模式   │ 助手 │ 全盘  │            │ 助手 │ 全盘  │
              └──────────────┘           └──────────────┘
L3  细分场景   四格场景表(路由表,不新增文档)
L4  执行 skill 具体 skill(dev-assistant / quick-dev / dev-team / vibe-coding …)
      ↕ 技术分类 hub 下移为二级索引(dev-core / dev-stack / dev-infra / dev-agent / dev-ai)
```

**路由优先级**:先问"什么规模的活"(L1)→ 再问"谁主导"(L2)→ 落场景(L3)→ 执行 skill(L4)→ 按需进技术索引。

### 1.2 设计哲学(四条底线)

| # | 原则 | 含义 |
|---|------|------|
| 1 | **增强不是依赖** | 全家桶失效时,Agent 退化为普通模式,工作仍可继续 |
| 2 | **自动化不是免责** | 每个自动动作都有人工确认阈值,最终决定权在用户 |
| 3 | **少即是多** | 上下文窗口只放契约层(description),不放全文;总被跳过的步骤应简化而非强推 |
| 4 | **证据优于想象** | 走样日志、Triage 准确率日志、ROI 看板驱动文档迭代,而非作者直觉 |

### 1.3 31 个 skill 全景清单

| 层级 | 数量 | 内容 |
|------|------|------|
| L1 总目录 | 1 | `vibe-coding-hub`(四层路由 + 全局机制 + 降级协议) |
| 技术二级索引 | 5 | dev-core / dev-stack / dev-infra / dev-agent / dev-ai |
| L3 自建 skill | 25 | 见下表 |

**25 个 L3 自建 skill 按类型划分**:

| 类型 | 数量 | Skill | 调用方式 |
|------|------|-------|----------|
| `tool` | 9 | snapshot-notes、plan-workflow 关联工具类:project-scaffold、vibe-code-search、vibe-mcp-connect、security-audit、project-tracker-dashboard、china-env-adapt、global-experience | 按需显式调用 |
| `workflow` | 9 | dev-assistant、quick-dev、requirement-clarify、plan-workflow、agent-loop、agent-collab、agent-workspace、knowledge-extraction、release-management | 阶段推进式调用 |
| `policy` | 5 | karpathy-coding-dscpln、vibe-terminal-safe、agent-permissions、frontend-design-policy、cost-agent | 自动注入上下文 |
| `meta` | 2 | fallback-general-dev、vibe-skills-gov-patterns | 系统级自动触发 |

> 注:类型标签以 frontmatter `metadata.hermes.type` 为准;tool/workflow 边界以各 skill
> frontmatter 标注为准,上表为分类示意(plan-workflow/global-experience 等核心 workflow
> 归 workflow 类)。

**主流程四选一**(L4 层执行入口):

| Skill | 定位 | 适用 |
|-------|------|------|
| `dev-assistant` | 副驾驶协议(助手模式) | 用户主导开发,团队·轻/企业·重双参数 |
| `quick-dev` | 轻量全包(团队·全盘) | 非项目随手做/脚本/一次性任务 |
| `vibe-coding` | 单人 5 步 MVP 流程 | 单人做完整项目 |
| `dev-team` | 多Agent开发团队 | 企业·全盘大型项目 |

### 1.4 核心机制清单(v1.0.0 正式版已具备)

| 机制 | 版本 | 作用 |
|------|------|------|
| 复杂度 Triage | v1.0.0 | 5 题是/否清单 → L0/L1/L2;动态校准 |
| 成本意识 | v1.0.0 | 每任务 token 预估;`/simple` 降级族;成本周报 + ROI 看板 |
| 确认交互契约 SLA | v1.0.0 | 阻塞型/通知型/批量型三级确认;`/focus` 免打扰 |
| 触发词治理 | v1.0.0 | 命名空间规则 + 冲突仲裁(31 skills) |
| 懒加载契约层 | v1.0.0 | description=契约(≤10 行),正文按需加载 |
| 执行走样日志 | v1.0.0 | 检查点自检,偏差落盘 `~/.vibe/drift/` |
| 新手梯度 v2 | v1.0.0 | 按已掌握概念数渐进披露 |
| 兼容性声明 | v1.0.0 | `requires` 版本检查 + versions.lock |
| 快照健康度检查 | v1.5 | 🟢🟡🟠🔴 冲突四分类,人工确认对齐 |
| 心跳熔断器 | v1.4 | CLOSED/OPEN/HALF-OPEN 状态机 + 处置矩阵 |
| 知识萃取 | v1.1 | 事后 5-Whys 复盘,四元素质量门 |
| 安全审计 | v1.1 | 提交前六维扫描,🔴 规则不可降级 |
| 元治理 | v1.4 | 事件驱动审计 + 30 天冷静期 |

### 1.5 核心工作流

```
用户需求 → L1 组织形态判定(团队/企业)
        → L2 开发模式判定(助手/全盘)
        → L3 四格场景表落位
        → L4 执行 skill
        → 技术二级索引(按需)
        → 完成后:快照记状态 / 知识萃取沉淀 / 走样自检
```

---

## 第二部分 结构变更计划(三层 → 四层)

### 2.1 变更动因(为什么必须改)

1. **普通开发掉进缝隙**:"非项目随手做"在旧三层里没有明确路线——
   - `dev-team` 自己的决策树写着:修单个 Bug → ❌ 不用、写单个脚本 → 简化分支、技术调研 → ❌ 不用;
   - 但全家桶没有给出"那该找谁"的答案;
   - `vibe-coding` 5 步流程面向"产品/MVP",对随手做太重;
   - L0 快进快出只定义"别用重的",没定义"用什么"。

2. **助手模式完全空白**:旧结构只有"全盘接手"思维(dev-team/vibe-coding),缺少
   "用户主导、Agent 副驾驶"这一维度——而这是日常开发中最常见的使用方式。

3. **组织形态缺失**:旧三层按"技术类型"(核心/栈/基础设施/Agent/AI)路由,
   没有"这个活是多大规模"的维度;用户必须先想清楚技术栈才能路由,
   而"规模+主导者"才是需求的第一性属性。

### 2.2 变更方案

| 变更 | 旧(三层) | 新(四层) |
|------|----------|----------|
| 路由主维度 | 技术类型 | 组织形态(团队/企业)→ 开发模式(助手/全盘) |
| L2 分类目录 | 5 个技术 hub(路由主层) | 下移为**技术二级索引**(按需进入) |
| 场景模板 | 场景模板表(9 行) | **四格场景表**(团队·助手/团队·全盘/企业·助手/企业·全盘)+ 通用场景 |
| 主流程 | 两选一(vibe-coding / dev-team) | **四选一**(dev-assistant / quick-dev / vibe-coding / dev-team) |
| 新增 skill | — | dev-assistant(助手协议)+ quick-dev(团队全盘)+ requirement-clarify(澄清访谈) |

### 2.3 影响面分析

| 对象 | 影响 | 处理 |
|------|------|------|
| 存量 28 个 skill | **零删除、零重写** | 全部保留,只改路由引用 |
| 5 个技术 hub | 定位从"L2 路由主层"→"技术二级索引" | 仅描述与进入时机更新,目录内容不动 |
| vibe-coding | 归位为"团队·全盘·单人 MVP"重档 | 不删除,重新归类 |
| dev-team | 归位为"企业·全盘" | 不删除,不再被小任务误用 |
| README / Tutorial / index.html | 数量与结构描述需同步 | v1.2.0 已同步 README,教程页待下轮 |
| 触发词治理 | 28 → 31 个 skill | 已同步 |

### 2.4 风险与应对

| 风险 | 应对 |
|------|------|
| 四层路由增加决策负担 | L1/L2 判定各给三维/两分支,辅助 Triage 复杂度清单;L0 直接裸奔 |
| 技术 hub 下移后"找不到语言 skill" | 技术索引仍常驻 hub 表格,单点直达表保留 18 条直达 |
| 新增 3 个 skill 文档膨胀 | L3 是路由表不新增文档;dev-assistant/quick-dev 均为单文档协议 |
| 兼容性断裂(旧引用 v3.x) | 兼容性声明保留 requires 机制;versions.lock 月度快照 |

---

## 第三部分 升级的具体内容

### 3.1 v1.1.0(本地测试版第一轮)

| 变更 | 类型 | 内容 |
|------|------|------|
| **requirement-clarify**(新建) | workflow | 编码前主动访谈 3-5 轮(目标/边界/技术/验收),产出 `.snapshots/DECISIONS.md`;每轮 ≤4 题防官僚;L1 压缩 1-2 轮;用户叫停转假设 |
| **fallback-general-dev**(升级 1.0.0→1.1.0) | meta | 新增**升降双链**:失败先升级(重试→换思路→换工具→升级模型→网络搜索→深度研究,每级 1-2 次),穷尽才降级(🟡/🟠/🔴);每级记录 escalation.log,成功级反馈知识萃取 |
| dev-core-hub | 索引 | 路由表新增 requirement-clarify 行 |
| vibe-coding-hub | 路由 | 版本 1.0.0→1.1.0;场景模板新增"需求澄清/方向对齐";单点直达新增 2 行;类型计数 22→23;触发词 28→29 |

### 3.2 v1.2.0(本地测试版第二轮,结构重构)

#### 3.2.1 新建 skill(2 个)

**dev-assistant(副驾驶协议,workflow)**
- 核心比喻:用户=司机,Agent=副驾驶,不抢方向盘
- 五原则:① 用户是司机(不擅自扩范围)② 每次改动可回退(git 底线)③ 解释而非代劳(教育倾向)④ 高频小确认(不做大访谈)⑤ 主动指出风险(看到坑要喊)
- 六种工作形态:局部实现 / Bug 定位修复 / 代码审查(diff 级,🔴🟠🟡🔵 分级) / 答疑(带证据) / 小重构(行为不变铁律) / 写测试文档草稿
- 规模双参数:团队·轻(当前文件+高频确认)/ 企业·重(项目画像+阶段确认);升级信号明确
- 边界:协议非方法论;决策权在用户;"你来定"时升级全盘

**quick-dev(轻量全包,workflow)**
- 定位:非项目开发的**正常流程**(不是降级/保底)
- 四步循环:目标一句话 → 最小实现 → 验证(能跑/结果对)→ 收尾(1-2 句摘要+可选沉淀)
- 轻量工作区:直接当前目录干,不强制 PRD/快照/计划文档
- 内置升级判定:超 3 文件/多模块/长期维护/DB schema/生产敏感 → 转 dev-team 或 vibe-coding

#### 3.2.2 hub 四层路由重构(vibe-coding-hub 1.1.0→1.2.0)

| 改动点 | 旧 | 新 |
|--------|----|----|
| 标题/版本 | 三层渐进式披露 v1.1.0 | **四层组织路由 v1.2.0** |
| 结构图 | 三层(L1 目录→L2 分类→L3 skill) | 四层(L1 组织形态→L2 开发模式→L3 场景→L4 skill)+ 技术索引下移 |
| L2 分类目录 | 路由主层 | **技术分类索引**(二级,非路由主层) |
| 路由流程 | 三层流程 | **四层流程**(L1 三维判定 + L2 谁主导) |
| Step 1 | 类型判定(技术树) | **组织形态判定**(模块数/专业角色/交付周期) |
| Step 2 | — | **开发模式判定**(助手 or 全盘) |
| 场景模板 | 9 行表 | **四格场景表**(2×2)+ 通用场景 7 行 |
| 类型计数 | 23 | 25(tool 9 / workflow 9 / policy 5 / meta 2) |
| 触发词计数 | 29 | 31 |
| 单点直达 | 16 行 | 18 行(+副驾驶 / 随手做) |
| 全局底线 #1 | 两选一 | **四选一** |
| description | 三层路由 | **四层组织路由**(契约层同步) |

#### 3.2.3 dev-core-hub 主流程四选一

- 主流程表:`vibe-coding / dev-team` 两行 → **dev-assistant / quick-dev / vibe-coding / dev-team 四行 + fallback 兜底行**
- 选择规则 #1:改为"先判组织路由"
- description 同步为"技术二级索引"定位

#### 3.2.4 README 同步

| 位置 | 改动 |
|------|------|
| 英文描述 | three-layer → **four-layer organization routing (team/enterprise × assistant/owner)** |
| 中文描述 | 三层路由 → **四层组织路由** |
| 触发词治理 | 28 skills → **31 skills** |
| 版本时间线 | + v1.1.0 / v1.2.0 本地测试版两行 |

### 3.3 验证结果

- ✅ 宿主技能库 31 个 skill 全部注册健康(frontmatter 无损,`readiness: available`)
- ✅ 仓库与宿主同步:31 个 skill 目录 + README + LICENSE + .gitignore + index.html + Tutorial.md
- ✅ 引用一致性:类型计数 25、触发词 31、四格场景表、单点直达 18 行
- ✅ git 本地 commit:`83154ea`(skill)+ `26250c2`(README),**未推送上游**

---

## 第四部分 后续计划(候选)

| 版本 | 内容 | 优先级 |
|------|------|--------|
| v1.3.0 | ✅ **已完成(大道至简)**:见下方第五部分 | — |
| v1.4.0 | Greenfield/Brownfield 双模式声明 / 设计澄清管道(轻量版) | P3 |
| 远期 | Skill 市场生态协议(skill.yaml 标准化 + 沙箱 + 社区验证) | 需平台支撑 |

---

## 第五部分 v1.3.0 升级记录(大道至简)

> 主题:token × 质量乘积最优。**不是取舍,是减法**——机制越少,token 越省且质量越高。

### 5.1 合并执行(核心瘦身,净减 3)

| 合并 | 产物 | 吸收的增量价值 |
|------|------|----------------|
| project-scaffold + plan-workflow | **project-init** | + 技术栈背景嗅探(stack-detect 无感化 → .vibe/stack.yaml) |
| agent-workspace + agent-collab | **agent-ops** | 工位三件套 + 协作三步闭环一份管 |
| release-management + rollback-backup | **release-ops** | 发布+回滚同一流程两面(先备份再发布) |

- 6 个被合并 skill:description 加 ⚠️ deprecated,文件保留防交叉引用
- L3:25 → **22**(tool 7 / workflow 8 / policy 5 / meta 2);路由内 skill:31 → **28**
- 契约层压缩:≤10 行 → **≤5 行**(31×5≈155 行常驻,较原减半)

### 5.2 路由压缩与默认路径

- **一句话画像**【组织】【主导】【类型】【技术】:15 秒锁定 L1+L2,反驳只更新画像不重走路由
- **默认路径化**:5 个常见场景免判断直走(帮我看看→dev-assistant L3 / 随手做→quick-dev L1 / 新建项目→project-init / 发布回滚→release-ops / 组队→dev-team)

### 5.3 机制边界修正(评审建议落地)

| 改动 | 来源 | 内容 |
|------|------|------|
| dev-assistant v1.1 | qwen+kimi | 介入深度 L0-L4(答疑→指路→草稿→副驾驶→代驾)+ 扩范围三色判定 + 跨文件变更阻塞型确认 |
| quick-dev v1.1 | kimi | 收编 Triage 执行器:5 项量化指标(文件≤3/无依赖/无DB/无跨模块/≤30min)→ L0 极速/L1 标准 + 转正钩子 |
| fallback v1.2 | kimi | 升降天花板:升级 ≤6 步硬限、第 3 步提示、第 6 步人工介入;循环检测(5 分钟加载≥2 次→中止) |
| cost-agent v1.2 | kimi | 证据消费:周报"一句话洞察"(走样 Top + Triage 误判 + 行动建议)+ 月报强制决策三问 |
| vibe-skills-gov-patterns v1.5 | kimi | 合并审查机制:触发词重叠>50%/30 天未加载/一方总引用 → 合并候选;新增 skill 7 天冷静期门槛 |
| 设计哲学 | 用户 | "少即是多"升级为**大道至简**:token×质量乘积最优 |

### 5.4 验证与仓库状态

- ✅ 宿主技能库 34 个 skill 目录(28 路由内 + 6 deprecated)全部健康
- ✅ 引用一致性:类型计数 22、触发词 28、四格场景/单点直达/技术索引同步
- ✅ 本地 commit:`59d997b`(v1.3.0)未推送上游

---

*本报告为本地评估用,对应仓库 `/home/yuchen_wang/workspace/vibe-skill-ops` 当前状态。*
