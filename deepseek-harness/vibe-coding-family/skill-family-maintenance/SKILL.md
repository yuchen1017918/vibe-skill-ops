---
name: skill-family-maintenance
description: 全家桶维护 runbook：token 优化双管齐下（渐进披露瘦身 + skills 合并废弃） + 合并执行规范（references 转移/sed 排除规则/计数口径）。 当用户说"token 减少"、"瘦身全家桶"、"合并 skill"、"废弃 skill"、 "渐进式披露"时加载。2026-08-11 v2.0 实战沉淀（hub -23%、全文 -7.3K 字符）。 触发词：token减少、瘦身、合并skill、废弃skill、渐进披露。
family-type: tool
family-version: 1.0.0
---

# Skill Family Maintenance（全家桶维护 runbook）

**定位**：全家桶的"维护操作手册"——token 优化与 skill 合并的实战流程。
治理决策（合并候选判定/废弃冷静期）在 `vibe-skills-gov-patterns`；
发布/同步在 `hermes-skill-publishing`；本 skill 是执行细节。

## 1️⃣ Token 优化双管齐下（用户方向，v2.0 实测）

**① skills 合并废弃减少字数 + ② 增强渐进式披露**。实测：全文 166,425 → 159,148 字符（-7,277，~3.6K tokens）；常驻 hub 14.8K → 11.4K（-23%）。

### 渐进式披露瘦身（低风险，先做）

**原理**：description 契约层已压到 ≤5 行后，最大常驻源是 hub 全文 + 大 skill 全文。
把"机制说明"和"模板/示例"移 references/，正文只留路由必需 + 一行指引。

| 动作 | 例（实测） | 收益 |
|------|-----------|------|
| hub 机制章节 → references/ 留指引行 | 执行走样/确认契约/新手梯度/兼容性/来源 → `references/route-mechanisms.md` | 14.8K → 11.4K（-23%） |
| 大 skill 模板/脚本 → references/ | project-tracker-dashboard 的 HTML 模板 + Python 脚本 | 7.8K → 3.1K（-60%） |
| 大 skill 细节 → references/ | snapshot-notes 模板、agent-loop 信任链 | 各 -0.4~1.1K |

**执行要点**：
1. 用 Python 按 `## ` 章节切分精确提取（execute_code + read_file 重建纯文本），不手工大段拷贝
2. 移动后**必须留一行指引**（`> 机制说明移 references/xxx.md，需要时再加载`）——否则 Agent 不知道机制还在，等于删功能
3. 大 skill 只移"模板/示例/细节"，核心流程留正文
4. 移动后验证 frontmatter 完整 + 章节数正常 + references 文件就位

## 2️⃣ Skills 合并执行规范 v2.0（含 4 条防坑）

候选判定（决策在 vibe-skills-gov-patterns）：触发词重叠 / 一方职责被另一方覆盖 / 管同一生命周期
（实测：snapshot-notes+knowledge-extraction 都管"任务后沉淀"；agent-loop+agent-ops 都管"Agent 协作"）。

```
1. 吸收方加"合并自"说明 + 吸收核心内容（snapshot-notes v2.0 加知识萃取章节）
2. 被吸收方 description 首行 ⚠️ deprecated 标注 + 指向替代
3. 文件保留（防交叉引用破坏），不物理删除
4. references 转移：被合并方 references/ → 吸收方 references/（改名标注来源，
   如 agent-loop/references/trust-chain.md → agent-ops/references/agent-loop-extra.md）
5. 全库引用替换用 Python 按行处理，必须排除两类文件 + 按行跳过历史叙事：
   - 排除文件：吸收方（含"合并自"说明，误替换破坏合并记录）+ 所有 deprecated 文件
   - **按行 skip 规则**（2026-08-15 实测踩坑）：行内出现 `合并自`/`合并产物`/`已合并`/`deprecated`/`防交叉引用`/`合并进本` → 跳过（历史叙事必须保留原旧名）
   - 其余 active 文件的活跃指引行替换旧名→新名
   - **误伤案例**（替换后必须人工复核 diff，本次 4 处语病）：
     a) skill-family-maintenance 自身"实测：snapshot-notes+knowledge-extraction 都管…"（合并证据行）
     b) "如 agent-loop/references/trust-chain.md → agent-ops/…"（references 迁移指引示例）
     c) vibe-coding-hub "已合并 deprecated"清单的续行（> 开头，不含"已合并"字样但属同一清单）
     d) 语义对比行："计划优先 plan-workflow，而非 project-scaffold" → 替换成"project-init 而非 project-init"语病
6. 替换后检查吸收方 related_skills 是否重复（sed 副作用：agent-loop→agent-ops 后 hub 里 agent-ops 出现两次，需手动去重）+ **自引用清理**（被合并方并入吸收方后 related_skills 可能出现吸收方自引用，删掉）
7. **合并后零引用验证（必须）**：跑 `scripts/verify-family-health.py` 确认活跃 skill 的 related_skills 与正文活跃指引零引用 deprecated。2026-08-15 实测发现此前 3 组合并遗留 7 个活跃 skill 共 42 处引用未更新（agent-collab/agent-loop/agent-workspace→agent-ops、plan-workflow/project-scaffold→project-init、rollback-backup→release-ops）——sed 排除规则没拦住"活跃文件里的活跃指引行"，必须事后脚本验证
8. hub 计数/触发词/场景表/类型标签全量同步
9. 合并后 diff -rq 宿主 vs 仓库 + 全量索引零缺失零重复
```

**计数口径**：路由内 L3 / hub / deprecated 三数并列（如 30 路由内 + 6 hub + 8 deprecated = 44 目录）；
README 结构图计数发布时必过时，每次同步核对。
**数字口径变更 = 全库扫描**（2026-08-15 实测）：旧数字（42/29/28/27 等）不止在 README——Tutorial、PROMO、index.html(含 JS i18n 字典)、assets/*.svg 文本节点、hub 内部计数示例（"31 skill × 5 行"）、DSH 版副本全都要 grep 更新；EVALUATION 类历史档案例外（顶部加"历史档案"声明保留旧口径）。

## 3️⃣ 可继续压的候选（未做，按需）

- agent-permissions(5K) / vibe-skills-gov-patterns(5K) 细节 references 化
- description 从 ~250 字符压到 150（保守，达标不强制）
- hub 触发词治理表 ~1.5K 精简为"冲突仲裁优先级"3 条，完整表移 references

## 4️⃣ 多 Harness 适配分发（dsh 适配版维护）

全家桶除 Hermes 原生格式外，维护 DeepSeek Harness (dsh) 适配版（2026-08-15 落地，36 skills）：

- 转换脚本：仓库根 `scripts/convert-dsh.py`（幂等，单一真相源）
- **改任意 Hermes 版 skill 后必须重跑**：
  `python3 scripts/convert-dsh.py ~/.hermes/skills/vibe-coding-family deepseek-harness/vibe-coding-family`
- DSH 格式要点/转换规则/开发坑：见 `references/dsh-skill-format.md`
- 新增 skill 自动进入 DSH 版（非 deprecated 即转换）；deprecated 自动排除
- 提交前验证：SKILL.md 数量 = active 数、description 全部 ≤500、无 deprecated 残留、name 与目录一致

## 快速排障

| 症状 | 处理 |
|------|------|
| 移动章节后没留指引 | Agent 不知道机制还在 → 每次移动必须留 `> 机制说明移 references/...` 行 |
| sed 替换破坏"合并自"说明 | 替换时排除吸收方 + deprecated 文件 + **按行 skip 历史叙事**（合并自/已合并/deprecated 等词） |
| 替换后出现语病（"project-init 而非 project-init"） | 语义对比行（"X 优先 A，而非 B"）替换前先看语境，人工复核 diff |
| hub related_skills 重复/自引用 | sed 副作用 → 替换后 grep 检查吸收方数组去重 + 删自引用 |
| 计数对不上 | 三口径并列核对（路由内/hub/deprecated）+ README 同步 |
| 合并后活跃 skill 仍引用 deprecated | **跑 `scripts/verify-family-health.py`**（frontmatter/零 deprecated 引用/触发词冲突/Jaccard/悬空引用/计数 6 项一键查） |
