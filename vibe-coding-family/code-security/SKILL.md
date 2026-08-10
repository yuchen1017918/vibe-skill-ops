---
name: code-security
description: |
  AI 编码安全三层防线（架构参考 Qoder Security）：①静默纪律（写码默认，免费）
  ②轻量扫描（任务收尾建议，只扫增量 diff）③深度扫描（用户说"深度扫描"才跑，
  全量+闭环重扫）。写码 agent 与审查 agent 分离，报告前验证可达性。
  当用户说"安全扫描"、"扫漏洞"、"深度扫描"、"检查这段代码的安全性"、
  "/security-scan"、或写完代码要防 SQLi/XSS/密钥泄露时加载。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: policy
    tags: [vibe-coding, security, semgrep, owasp, SAST, policy]
    related_skills: [security-audit, vibe-coding-hub, dev-core-hub, code-review, git-workflow]
---

# Code Security（三层安全防线）

**架构参考：Qoder Security（阿里）三层模型。原则：默认轻、深度按需、不打断。**

```
第一层 · 静默纪律（默认，免费）→ 生成即合规
第二层 · 轻量扫描（任务收尾建议）→ 只扫增量，快速验证
第三层 · 深度扫描（用户主动）→ 全量 + 返工 + 闭环重扫
```

## 第一层 · 静默纪律（默认 — 生成即合规）

本 skill 为 **policy 类型**：8 条纪律随写码任务**自动注入**，Agent 每次生成代码前都"看见"安全规则，不需要用户说一个字。

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

**静默钩子（可选安装，零 token）**：pre-commit hook 在本地跑 gitleaks + semgrep，高危 ERROR 直接挡下 commit——与用户说不说、Agent 记不记得完全无关。模板见 `references/pre-commit.yaml`（`.pre-commit-config.yaml` 可直接用）或裸 hook 见 §5。

> 效果：**生成即合规**——扫描只是验证，不是兜底。

## 第二层 · 轻量扫描（任务收尾建议 — 快速验证）

编码任务**自然断点**（写完代码 / 准备提交）时，Agent **主动建议**（不需用户提醒，用户 yes 才跑）：

```bash
git diff | semgrep scan --config auto --json -   # 只扫增量改动（便宜快）
gitleaks detect --source . --redact              # 密钥泄露（快）
```

**Qoder 四原则（本层核心，减少误报 + 提高准确率）：**

1. **写码 agent 与审查 agent 分离**：不"检查我自己刚写的"——以独立审查者视角看 diff；大改动可委派子 agent 审查
2. **扫描与验证分离**：semgrep 命中 → **先验证可达性**（漏洞路径真的能触发？）→ 才报给用户。不可达的丢弃，不打扰
3. **只扫增量**：不扫全项目，token 成本低
4. **结果并入提交闸门**：扫描干净才允许 commit；有问题 → 修复 → 重扫（见 §3 闭环）

## 第三层 · 深度扫描（用户主动 — 扫描 → 返工 → 重扫）

**只有用户不放心、明确说"深度扫描"/"deep scan"时执行**（默认不跑，省 token）：

```bash
semgrep scan --config auto .                     # 全量语义扫描
semgrep scan --config p/owasp-top-ten src/       # OWASP 规则集
gitleaks detect --source . --report-format json  # git 全历史密钥
pip-audit / npm audit                            # 依赖 CVE（按项目语言）
# 可选：CodeQL 数据流分析（跨文件污点源→危险 sink 链式漏洞）
codeql database create /tmp/db --language=python --source-root .
codeql database analyze /tmp/db --format=sarif-latest --output=out.sarif
```

**闭环流程（不留安全债）：**

```
深度扫描 → 报告（位置 + CWE + 可达性验证） → 返工修复 → 重扫验证 → 干净才提交
```

## 触发方式

| 方式 | 行为 | token 成本 |
|------|------|-----------|
| 写码时（默认） | 第一层纪律自动生效（静默，policy 注入） | ≈0（固定常驻） |
| 任务收尾（自动建议） | 第二层轻量扫描建议，用户 yes 才跑 | 低（只扫 diff） |
| 用户说"深度扫描" | 第三层全量扫描 + 闭环重扫 | 高（按需） |
| `/security-scan` | 三层按需手动触发 | 按层 |

## 裸 pre-commit hook（不想装框架时）

```bash
# .git/hooks/pre-commit（chmod +x）
#!/bin/sh
git diff --cached --name-only -z | xargs -0 -r semgrep scan --config auto --json - 2>/dev/null \
  | grep -q '"ERROR"' && { echo "❌ 高危漏洞，提交已阻止"; exit 1; }
gitleaks protect --staged --redact || exit 1
```

## 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `security-audit` | 提交前六维闸门（权限/密钥/依赖/日志等全维度清单）；本 skill 三层是它的扫描执行器 |
| `code-review` | review 管质量维度，本 skill 管安全维度，互补 |
| `vibe-terminal-safe` | 高危命令终端层拦截；本 skill 管代码层 |
| `dev-core-hub` | 主流程编码阶段加载；提交闸门 = 第一层 hook + 第二层建议 + security-audit 六维 |
| `global-experience` | 扫描到的漏洞模式沉淀为经验，下次生成时自动避坑 |

## 快速排障

| 症状 | 处理 |
|------|------|
| semgrep 装不上 | `pip install semgrep -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| 扫描太慢 | 用第二层只扫 diff；全量仅深度扫描时 |
| 误报太多 | 验证可达性后再报（§2 原则 2）；`.semgrepignore` 排除生成目录 |
| 规则不匹配语言 | `--config p/python` 等按语言选规则集 |
| 存量代码一堆漏洞 | 先修本次改动引入的（增量），存量排期建 issue |

> 注意：扫描工具不能 100% 消除漏洞——高危模块（认证/支付/用户数据）建议人工复核或深度扫描。
