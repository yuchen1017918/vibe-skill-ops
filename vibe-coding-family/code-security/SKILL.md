---
name: code-security
description: |
  AI 编码安全 skill：写码时安全纪律 + Semgrep 漏洞扫描 + AI 增量 diff 审查。
  融合 semgrep/skills（官方）+ SkillSemgrep（中文指令）+ trailofbits/skills（深度审计）
  + Argus/Semgrep-Guardian MCP（实时拦截可选）。当用户说"安全扫描"、"扫漏洞"、
  "检查这段代码的安全性"、"code-security"、或写完代码要防 SQL注入/XSS/密钥泄露时加载。
  触发词：安全扫描、扫漏洞、安全检查、code-security、漏洞审查。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, security, semgrep, codeql, owasp, SAST, code-scan]
    related_skills: [security-audit, vibe-coding-hub, dev-core-hub, code-review, git-workflow]
---

# Code Security（写码安全 + 漏洞扫描）

**目的**：AI 生成代码速度快但易带漏洞（SQLi/XSS/命令注入/硬编码密钥/路径穿越 = OWASP Top10）。
本 skill 把三道防线合为一体：**写码时约束 → 生成后扫描 → 增量审查**。
能力来源：semgrep/skills（官方知识库 + 扫描）、SkillSemgrep（中文指令）、
trailofbits/skills（diff 审查 + CodeQL 深度审计）、Argus/Guardian（MCP 实时拦截）。

## 1️⃣ 安装（国内可用，一次装好）

```bash
pip install semgrep --index-url https://pypi.tuna.tsinghua.edu.cn/simple   # 核心扫描器
pip install gitleaks --index-url https://pypi.tuna.tsinghua.edu.cn/simple # 密钥泄露检测
semgrep --version   # 验证 ≥1.80
```

> 可选：`codeql` CLI（深度审计）、`uvx argus`（MCP 扫描器，见 §6）。

## 2️⃣ 写码时安全纪律（生成代码前内置约束）

> 写码/修码时**先过这 8 条**，生成时就合规，事后少修：

| # | 纪律 | 反例 → 正例 |
|---|------|-------------|
| 1 | 密钥永不硬编码 | `api_key="sk-..."` → 环境变量/.env |
| 2 | SQL 永远参数化 | f-string 拼 SQL → 占位符 `?` / ORM |
| 3 | 输出永远转义 | `innerHTML=userInput` → 转义/白名单 |
| 4 | 命令拼接禁用 | `os.system(f"rm {f}")` → `subprocess` 列表参数 |
| 5 | 鉴权在服务端 | 前端隐藏 → 后端校验 + 角色校验 |
| 6 | 路径防穿越 | `open(user_path)` → 规范化 + 白名单目录 |
| 7 | 输入永远校验 | 直接信任 → 类型/长度/白名单校验 |
| 8 | 密码/敏感态哈希存储 | 明文 → bcrypt/argon2 |

## 3️⃣ 扫描已生成代码（生成后扫描）

```bash
# 全项目扫描（自动选规则，覆盖 OWASP Top10）
semgrep scan --config auto .

# 指定 OWASP 规则集
semgrep scan --config p/owasp-top-ten src/

# 只扫本次改动（快）
git diff HEAD | semgrep scan --config auto --json -

# 密钥泄露（git 全历史）
gitleaks detect --source . --report-format json --redact
```

**输出解读**（semgrep 结果含）：
- 漏洞位置（文件:行号）+ CWE 编号（如 CWE-89 SQLi）
- 严重级别（ERROR/WARNING）+ 修复建议
- 结论：🔴 高危漏洞存在 → 修复后重扫；🟢 无 → 进入提交闸门

**中文指令触发**（兼容 SkillSemgrep 用法）：
- "安全扫描这个项目" → 跑 `semgrep scan --config auto .`
- "扫这个文件有没有漏洞" → `semgrep scan --config auto <file>`
- "检查这段代码" → 直接贴代码，Agent 按 §2 八条 + 已知漏洞模式脑检，再跑扫描器验证

## 4️⃣ 增量审查（AI 改动 diff，trailofbits diff-security-review）

> AI 每次改动可能引入新漏洞——**只审增量**，比全量快且准：

```bash
# 审查未提交改动
git diff | semgrep scan --config auto --json -

# 审查上次提交（AI 刚生成的 commit）
git diff HEAD~1 | semgrep scan --config auto --json -

# PR 场景：审查分支 vs main
git diff origin/main...HEAD | semgrep scan --config auto --json -
```

**增量审查流程**：
```
1. 拿到 AI 改动 diff（git diff --stat 看范围）
2. 对 diff 跑 semgrep（只扫改动行，不是全项目）
3. 人工/Agent 逐条看：新引入的漏洞必须修，旧漏洞不背锅
4. 修复 → 重扫 → 干净才提交
```

## 5️⃣ 深度审计（可选，CodeQL）

```bash
# 需要 codeql CLI + 数据库构建（重，仅关键模块用）
codeql database create /tmp/db --language=python --source-root .
codeql database analyze /tmp/db --format=sarif-latest --output=out.sarif
```

> 用途：认证/支付/用户数据模块上线前深度审计。日常用 §3/§4 的 semgrep 就够。

## 6️⃣ MCP 实时拦截（可选，生成即扫描）

| 方案 | 启动 | 说明 |
|------|------|------|
| **Semgrep Guardian**（官方） | 文档 https://semgrep.dev/docs/guardian | 生成文件自动扫描，漏洞不修不让过（闭环最强） |
| **Argus**（开源） | `uvx argus scan .`（CLI）或接 MCP | SAST/DAST/SCA/Secrets/IaC 多合一，SARIF 输出 |

> 日常手动流程用 §3 命令即可；要"生成即拦截"再接入 MCP（配置见 `hermes-mcp-setup`）。

## 7️⃣ 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `security-audit` | **本 skill 管"代码漏洞扫描"；security-audit 管"提交前六维闸门"**（权限/密钥/依赖/日志等全维度清单）。扫描发现漏洞 → security-audit 汇总 → 修复 → 重扫 → commit |
| `code-review` | review 管质量维度，本 skill 管安全维度，互补 |
| `vibe-terminal-safe` | 高危命令终端层拦截；本 skill 管代码层 |
| `dev-core-hub` | 主流程编码阶段加载；commit 前置=本 skill 扫描 + security-audit 双闸门 |
| `global-experience` | 扫描到的漏洞模式沉淀为经验，下次生成时自动避坑 |

## 8️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| semgrep 装不上 | 国内用 tuna 镜像；或 `pipx install semgrep` |
| 扫描太慢 | 缩小范围：`src/` 子目录 / 只扫 diff（§4） |
| 误报太多 | 加 `.semgrepignore`（生成目录/第三方代码）；`--exclude-rule` 排除具体规则 |
| 规则不匹配语言 | `--config p/python` 等按语言选规则集 |
| 扫描到一堆旧代码漏洞 | 先修本次改动引入的（§4 增量），存量漏洞排期（可建 issue） |

> 注意：扫描工具不能 100% 消除漏洞——高危模块（认证/支付/用户数据）建议人工复核。
