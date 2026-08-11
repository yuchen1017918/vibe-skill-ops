---
name: dev-memory
description: |
  开发级记忆库（架构参考 TencentDB Agent Memory 分层思想）：记忆开发中的细节教训
  ——API 用法坑、框架特性、调试细节、性能优化、项目特定知识。按 Atom→Topic→Core
  三层组织，按需召回，索引常驻详情按需加载。与 vuln-memory（漏洞级）互补：
  本库记"开发细节坑"，漏洞库记"安全漏洞"。当用户说"记住这个开发坑"、
  "这个API怎么用"、"之前怎么解决的"、"查一下开发经验"时加载。
  触发词：开发记忆、dev-memory、开发坑、API用法、调试经验、项目知识。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, memory, dev, experience, tencentdb, learning]
    related_skills: [vuln-memory, global-experience, snapshot-notes, snapshot-notes, vibe-code-search]
---

# Dev Memory（开发级记忆库）

**目的**：开发中的细节教训（API 坑/框架特性/调试细节/性能优化）修完就忘 = 反复查文档。
每次踩坑 → 沉淀为 Atom 条目 → 按需召回 → **不重复查、不重复踩**。

**架构参考：TencentDB Agent Memory**（腾讯开源，MIT）：
- **分层沉淀**：Atom（单条教训）→ Scenario（按主题/项目组织）→ Core（高频常驻）
- **按需召回**：索引常驻（小），详情用到才加载（省 token）
- **资产化**：教训条目 + 可复用片段（snippets）+ 项目知识

## 📂 记忆库结构（~/.vibe/dev-memory/）

```
~/.vibe/dev-memory/
├── SKILL.md            # 使用说明 + 主题索引（常驻，~300 token）
├── index.md            # 全量条目清单（Atom 索引：主题/项目/最近）
├── cheatsheet.md       # Core：高频避坑速查（常驻，~20 行）
└── topics/             # Scenario：按主题组织（按需加载）
    ├── python/         # 语言/框架维度
    │   ├── asyncio.md
    │   └── pandas.md
    ├── hermes/         # 工具/平台维度
    ├── web/            # 前端/后端
    ├── windows-wsl/    # 跨系统坑
    └── <project>/      # 项目特定知识（可选）
        └── webterminal.md
```

## 1️⃣ 沉淀流程（踩坑后必做 — 5 步，几十 token）

```
1. 判断层级: 是"安全漏洞"→ vuln-memory; 是"开发细节坑"→ 本库
2. 归类: 按主题 → topics/<category>.md(已有) 或建新章(新主题)
3. 条目格式(Atom 模板):
   ## <主题> <一句话教训>(日期, 项目)
   ### 场景     <什么场景踩到>
   ### 细节教训  <具体 API/参数/行为坑>
   ### 解决/正例 <怎么解决, 关键代码>
   ### 关键词    <检索标签: asyncio, timeout, 死锁>
4. 更新 index.md(新增条目一行: 主题/项目/日期)
5. 若高频(3 次+同主题)→ 提炼进 cheatsheet.md
```

**触发时机**：
- 调试解决了一个怪坑 → 沉淀（debug 后自动）
- 发现 API/框架的奇怪行为 → 沉淀
- 用户说"记住这个"、"这个坑记一下" → 手动沉淀
- 项目收尾 → 项目特定知识归档（topics/<project>/）

## 2️⃣ 按需召回（默认路径）

| 时机 | 动作 | token |
|------|------|-------|
| 开始开发/调试 | 读 `cheatsheet.md`（高频避坑） | 小 |
| 遇到具体问题 | 按主题加载 `topics/<category>.md` 或 grep 关键词 | 按需 |
| 新项目启动 | 查 index.md 看相关项目历史 | 小 |
| 写码中 | 涉及某 API → 查对应主题条目 | 按需 |

```bash
# 快速检索
grep -i "asyncio" ~/.vibe/dev-memory/topics/*.md   # 按关键词跨主题
grep -rn "WebTerminal" ~/.vibe/dev-memory/          # 按项目
```

## 3️⃣ 分层说明（对照 TencentDB）

| TencentDB 层 | 本库对应 | 内容 |
|-------------|---------|------|
| L1 Atom | topics/ 单条目 | 一条具体教训（场景/细节/解决） |
| L2 Scenario | topics/ 主题目录 | 按语言/平台/项目组织的知识块 |
| L3 Core/Persona | cheatsheet.md | 高频模式（3 次+同主题提炼） |

## 4️⃣ 与全家桶记忆体系分工

| 记忆 | 记什么 | 例 |
|------|--------|-----|
| **`dev-memory`（本库）** | 开发细节教训（API/框架/调试） | "xterm 4.19 与 fit 插件不兼容" |
| `vuln-memory` | 安全漏洞（反例→正例） | "SQL 拼接注入 CWE-089" |
| `global-experience` | 跨项目模式/方法论（架构级） | "先验证后落地,最小改动优先" |
| `snapshot-notes` | 项目进行状态（在哪） | "v1.3 已合并,待发布" |
| `snapshot-notes` | 通用萃取闭环 → global-experience | 任务完成自动萃取 |

> 判定口诀：**安全 → vuln-memory;API/细节坑 → dev-memory;架构/模式 → global-experience;项目状态 → snapshot-notes。**

## 5️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| 条目膨胀 | 月度复盘（cost-agent 联动）：90 天未命中的条目归档 index.md 备注 |
| 和 global-experience 重复 | 细节/事实 → 本库；模式/方法论 → global-experience；跨界互引一句 |
| 检索不到 | grep 关键词 + index.md 全量；关键词列写全（含英文别名） |
| 主题混乱 | 主题目录只增不删；新主题建章时更新 SKILL.md 索引 |
