---
name: open-code-review
description: |
  AI 代码审查执行引擎：调用阿里开源 Open Code Review（ocr CLI）对 Git 改动做
  行级精确审查（bug/安全/性能/质量），内置微调规则集（NPE/线程安全/XSS/SQLi），
  本机已实测（DeepSeek 后端，12s 发现 2 个高危 bug）。当用户说"审查代码"、
  "review 一下"、"审查 PR"、"检查这个 commit"、或写完代码要质量把关时加载。
  触发词：审查、review、代码审查、审查PR、审查commit。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, code-review, quality, LLM, alibaba]
    related_skills: [code-review, code-security, security-audit, dev-core-hub, git-workflow]
---

# Open Code Review（ocr — AI 代码审查引擎）

**来源**：阿里开源（Apache 2.0，12.5K stars），内部两年服务数万开发者、识别数百万缺陷。
**架构**：确定性管道（diff/代码搜索）+ LLM Agent + 内置微调规则集（NPE/线程安全/XSS/SQLi）。
**定位**：**质量维度审查执行引擎**——和安全维度（code-security 钩子）天然分工：hook 挡安全漏洞，ocr 审 bug/逻辑/质量。

## 1️⃣ 本机环境（2026-08 实测）

| 项 | 值 |
|----|-----|
| 版本 | open-code-review **1.8.10**（npm 全局） |
| 命令 | `$(npm prefix -g)/bin/ocr`（WSL 下 `which ocr` 可能不在 PATH，用绝对路径或加 PATH） |
| LLM | **DeepSeek**（内置 provider，`deepseek-v4-flash`），连接测试 ✓ |
| 实测 | 1 文件 12s / ~18.7K token，发现 2 个高危 bug（空列表除零/异常吞没），行级+修复建议 |

**安装（国内，allow-scripts 是 npm 新安全策略必需）：**
```bash
npm install -g --allow-scripts=@alibaba-group/open-code-review @alibaba-group/open-code-review --registry=https://registry.npmmirror.com
```

**LLM 配置（DeepSeek，一次配置永久生效）：**
```bash
export DEEPSEEK_API_KEY=$(grep '^DEEPSEEK_API_KEY=' ~/.hermes/.env | cut -d= -f2-)
$(npm prefix -g)/bin/ocr config set provider deepseek
$(npm prefix -g)/bin/ocr config set model deepseek-chat
$(npm prefix -g)/bin/ocr config set providers.deepseek.api_key "$DEEPSEEK_API_KEY"
$(npm prefix -g)/bin/ocr llm test   # 验证: Connection test successful
```

## 2️⃣ 审查模式

```bash
OCR=$(npm prefix -g)/bin/ocr
# workspace:未暂存+暂存+未跟踪改动(默认,快)
$OCR review --audience agent -b "业务上下文"
# 单 commit
$OCR review --commit HEAD --audience agent -b "上下文"
# 分支比较(PR 场景)
$OCR review --from main --to <branch> --audience agent -b "上下文"
# 预览(不烧 LLM,只看会审哪些文件)
$OCR review --preview
# JSON 结构化输出(适合 Agent 解析)
$OCR review --format json --audience agent
```

**关键参数：**
- `--audience agent`：**必须**，抑制进度 UI 只输出摘要（Agent 模式）
- `-b/--background "上下文"`：业务上下文注入，审查质量显著提升
- `--timeout <min>`（默认 10 分钟/文件）、`--concurrency <n>`（默认 8，限流时降）
- `--provider deepseek --model deepseek-v4-flash`：单次指定模型

## 3️⃣ 输出解读与分级

每条评论 = 文件:行号 + `[类型 · 级别]` + 描述 + **修复建议 diff**：
- 级别：**high**（bug/安全问题/明确错误）/ **medium**（上下文相关/风格性能）/ **low**（误报，静默丢弃）
- 类型：bug / security / performance / style 等

```markdown
## 审查结果（按优先级）
- 🟥 High: buggy.py:6-8 — 空列表除零 → 建议: if not prices: return 0
- 🟧 Medium: ...
```

**处理纪律**：High 必修（直接改/请用户确认）；Medium 视上下文；Low 丢弃不打扰。
`start_line/end_line` 为 0 时（定位失败）→ 读内容 + 查文件人工定位。

## 4️⃣ 自定义规则（项目级）

`<repo>/.opencodereview/rule.json`（或 `~/.opencodereview/rule.json`）：
```json
{
  "rules": [
    { "path": "**/*.py", "rule": "所有新方法必须校验关键参数", "merge_system_rule": true },
    { "path": "**/*.sql", "rule": "检查 SQL 注入风险和缺失闭合标签" }
  ]
}
```
优先级：`--rule <path>` > 项目 rule.json > 用户 rule.json > 内置默认。

## 5️⃣ 成本与频率（质量角的定价）

| 场景 | 建议 | token 成本 |
|------|------|-----------|
| 随手做（L0） | 不跑（脑检即可） | 0 |
| 常规提交（L1） | 提交前跑 workspace 或 commit 模式 | ~15-20K/文件 |
| PR/大改动 | `--from main --to branch` | 按 diff 大小 |
| 用户说"深度审查" | 全量 + 结合 code-security 第三层 | 高（按需） |

> 实测参考：1 个文件 ~18.7K token / 12s（DeepSeek 成本极低）。
> **先修再审**：commit 前 hook 已挡安全漏洞 → ocr 审剩下的质量 bug → 修复 → 重跑确认。

## 6️⃣ 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `code-review` | code-review 是**方法论**（怎么审）；本 skill 是**执行引擎**（用什么审）——方法论指导 + ocr 落地 |
| `code-security` | 安全维度：静默钩子挡高危漏洞（commit 时确定性）；ocr 审质量 bug —— **互不替代，并行跑** |
| `security-audit` | 提交前六维闸门汇总；ocr 结果并入审计报告 |
| `dev-core-hub` | 主流程编码纪律；提交前"质量 review + 安全 audit"双闸门 = ocr + security-audit |
| `git-workflow` | 审查通过是 commit/PR 前置条件 |

## 7️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| `ocr` 命令找不到 | WSL PATH 问题：用 `$(npm prefix -g)/bin/ocr` 或 `export PATH="$HOME/.npm-global/bin:$PATH"` |
| npm 装完没二进制 | postinstall 被拦 → 必须 `--allow-scripts=@alibaba-group/open-code-review` |
| llm test 失败 | 重配 provider/model/api_key（§1）；或环境变量 `OCR_LLM_URL/OCR_LLM_TOKEN/OCR_LLM_MODEL` |
| 限流（429） | `--concurrency 2` 降低并发 |
| 审查太慢 | 只审增量 diff（workspace 默认）或 `--commit` 单提交；`--timeout 5` 收紧 |
| 误报 | 按 high/medium/low 分级处理，low 丢弃；rule.json 加项目规则压误报 |

> 注意：ocr 是质量审查助手不是安全扫描器替代——安全漏洞靠 code-security 纪律 + hook；ocr 的 XSS/SQLi 规则是补充视角。
