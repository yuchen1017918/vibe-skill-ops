---
name: vuln-memory
description: Vulnerability Memory 漏洞学习记忆库：把扫描/审查找出的漏洞结构化沉淀 （按 CWE 分类：反例→正例+教训），下次生成代码自动避坑，不重复踩坑。 架构参考 book-to-skill（结构化蒸馏 + 按需加载 + fold-in 更新）。 当 code-security/ocr/security-audit 发现漏洞、或用户说"记住这个漏洞"、 "这个坑别再犯"、"查一下之前踩过哪些安全坑"时加载。 触发词：漏洞记忆、vuln-memory、记住漏洞、安全坑、踩坑记录。
family-type: tool
family-version: 1.0.0
---

# Vulnerability Memory（漏洞学习记忆库）

**目的**：漏洞修完就忘 = 下次重复踩坑。把每次扫描/审查发现的漏洞**结构化沉淀**，
生成代码时自动参考——**同样的坑只踩一次**。

**架构参考：book-to-skill**（virgiliojr94/book-to-skill）：
- **结构化蒸馏**：不是摘要，是"反例→正例+教训"的可执行结构
- **按需加载**：SKILL.md 只有索引（小），具体 CWE 章节问到/用到才加载（省 token）
- **fold-in 更新**：新漏洞增量并入现有类型章节，不重写

## 📂 记忆库结构（~/.vibe/vuln-memory/）

```
~/.vibe/vuln-memory/
├── SKILL.md            # 心智模型 + 类型索引（常驻，~300 token）
├── index.md            # 全部漏洞清单（类型/计数/最近发现，全量扫描时读）
├── cheatsheet.md       # 决策规则表：写码时快速避坑（常驻，小）
├── patterns.md         # 反例→正例 通用对照（生成时参考）
└── cwes/
    ├── cwe-089-sqli.md       # SQL 注入（每类一个文件，按需加载）
    ├── cwe-079-xss.md        # XSS
    ├── cwe-798-hardcoded.md  # 硬编码密钥
    └── ...                   # 新类型自动建章
```

## 1️⃣ 沉淀流程（修复后必做 — 防知识流失）

发现漏洞 → 修复 → **fold-in 进记忆库**（3 步，几十 token）：

```
1. 解析扫描/审查输出(JSON: check_id / CWE / 路径:行号 / 消息 / 修复建议)
2. 归类: 按 CWE/类型 → 定位 cwes/<type>.md
   - 已有类型 → 追加一条(去重: 同模式不重复记)
   - 新类型 → 建新章节 + 更新 SKILL.md 索引
3. 条目格式(固定模板):
   ## <CWE-XXX> <类型名>(最近: YYYY-MM-DD, 来源: code-security/ocr)
   ### 反例(错)
   ```<lang>  <漏洞代码片段>
   ### 正例(对)
   ```<lang>  <修复后代码片段>
   ### 教训(一句话)
   <为什么犯 + 怎么避免>
```

**触发时机**（挂到已有机制上）：
- code-security 第二/三层扫描发现高危 → 修复后自动沉淀
- ocr review 发现 [bug/security · high] → 修复后沉淀（security 类进 vuln-memory，bug 类进 global-experience）
- security-audit 六维审计发现 → 沉淀
- 用户说"这个坑别再犯" → 手动沉淀

## 2️⃣ 生成时避坑（默认路径 — 自觉防坑）

| 时机 | 动作 | token |
|------|------|-------|
| 写码前 | 加载 `cheatsheet.md`（决策规则表，~20 行） | 小 |
| 写码中涉及敏感类型 | 按需加载对应 `cwes/<type>.md` 参考正例 | 按需 |
| 新项目启动 | 查 `index.md` 看历史高频漏洞 → 重点防 | 小 |
| 扫描/审查前 | 不用加载记忆（扫描器自己会找） | 0 |

> 效果：记忆库越用越聪明——写 SQL 前自动想起"上次 cwe-089 踩过 f-string 拼接"。

## 3️⃣ 查询与复盘

```bash
# 查某类型历史(全量)
grep -c "## CWE" ~/.vibe/vuln-memory/cwes/*.md   # 各类型计数
# 查高频漏洞
grep -l "来源: code-security" ~/.vibe/vuln-memory/cwes/*.md | head
```

**月度复盘**（cost-agent 月报联动）：高频漏洞类型 → 若同一类型反复出现 3 次+，
说明默认纪律失效 → 升级 code-security 第一层纪律或补 hook 规则。

## 4️⃣ 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `code-security` | 扫描+修复（发现源）；vuln-memory 是它的**记忆端**——闭环：扫→修→记→防 |
| `open-code-review` | 质量审查（发现源，security 类沉淀到本库） |
| `security-audit` | 六维审计（发现源） |
| `global-experience` | 通用经验 vs 本库安全专项：bug/架构经验 → global-experience；安全漏洞 → vuln-memory |
| `snapshot-notes` | 通用萃取闭环；本库是安全维度的结构化版 |

## 5️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| 记忆库膨胀 | 月度复盘：同类型 3 次+ → 升级纪律；90 天未命中的条目归档（移动 index.md 备注） |
| 重复条目 | fold-in 去重：同 CWE+同模式（相似反例代码）→ 跳过，只更新日期 |
| 找不到历史 | grep cwes/ 全量；index.md 有全量清单 |
| 和 global-experience 重复 | 安全漏洞只在 vuln-memory；通用经验只在 global-experience；跨界（安全+架构）→ 两边各记一句互引 |

> 注意：记忆库是**辅助防坑**，不是安全保证——扫描/hook 才是确定性兜底（工具不会忘，记忆会）。
