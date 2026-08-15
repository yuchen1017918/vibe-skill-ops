---
name: reverse-ops
description: 逆向/渗透/安全研究操作路由（轻量版，借鉴 zhaoxuya520/reverse-skill 14.7K stars）： 任务类型→方法论→工具链 路由 + 授权范围闸门（Scope Gate）+ 工具按需检查 + 证据链。 仅限授权目标（自己的应用/CTF/靶场/用户明确授权的系统）。当用户说"逆向"、 "反编译"、"渗透测试"、"CTF"、"抓包"、"分析这个APK/二进制/JS"时加载。 触发词：逆向、反编译、渗透、CTF、抓包、APK分析、二进制分析、JS逆向。
family-type: tool
family-version: 1.0.0
---

# Reverse Ops（逆向/渗透/安全研究路由）

**来源借鉴**：zhaoxuya520/reverse-skill（14.7K stars）——"安全技能路由包"：
AI 自动路由 + 按需自举工具链 + 自动进化经验库。本 skill 是**轻量版**，只留全家桶需要的三件套：
**Scope Gate（授权闸门）+ 任务路由 + 工具检查**。

## 0️⃣ Scope Gate（授权范围闸门 — 最高优先级，行动前必查）

> **授权未确认，禁止对目标 ACT。** 借鉴 reverse-skill：`auth.status=granted` 才行动。

**每次接逆向/渗透/扫描任务，先回答 4 问：**

| # | 问题 | 未通过 |
|---|------|--------|
| 1 | 目标是谁的？（自己的应用/公司授权系统/CTF 靶场/公开漏洞环境） | ❌ 拒接或要求用户确认授权 |
| 2 | 范围明确吗？（具体域名/IP/APK/二进制，不是"随便看看"） | ❌ 先让用户限定范围 |
| 3 | 方法合规吗？（不 DoS/不破坏数据/不越权访问） | ❌ 收敛方法 |
| 4 | 记录留存？（发现的问题报告给谁） | ❌ 先定报告对象 |

**授权确认后**：先记一行 `授权范围: 目标/范围/方法/边界`（可放 ~/.vibe/reverse-ops/ 或项目 NOTES），再动手。

> ⚠️ 未授权目标（别人的网站/未授权系统）→ **拒绝执行**并说明原因，这是红线不是建议。

## 1️⃣ 任务路由（轻量版 — 只覆盖常用场景）

| 任务 | 方法论 | 工具链 | 入口 |
|------|--------|--------|------|
| **APK/Android 逆向** | 解包→反编译→分析→(Hook) | jadx / apktool / Frida | `jadx -d out app.apk` |
| **二进制分析** | 侦察→反汇编→符号恢复 | Ghidra(头)/ radare2 / strings / file | `r2 -A binary` |
| **前端 JS 逆向** | 定位签名→加密还原→Node 补环境 | DevTools CDP / AST 工具 | 定位加密函数→Node 复现 |
| **Web 渗透** | 侦察→扫描→验证 | nmap / nuclei / sqlmap(接 security-scanner) | `nmap -sV target` |
| **CTF** | 按题目类型走流程 | 看题→分析→flag | 分类型处理(逆向/pwn/web/crypto) |
| **抓包/协议** | 捕获→分析→重放 | tcpdump / Burp / curl | `tcpdump -i any -w cap.pcap` |

**路由执行契约**（借鉴 reverse-skill 的 CRITICAL）：
- 接到任务**立即执行**（路由→工具检查→行动），**不允许只回复"已读/理解了"**
- 不确定用哪个工具 → 看上表 → 输出路由分析 → 直接开始
- 路由无法命中 → 说明情况 + 提议补充方法论，**禁止硬塞到不匹配的工具**

## 2️⃣ 工具检查（按需自举，禁止猜路径）

```bash
# 常用工具速查(缺失才装,装了的别重复装)
for t in jadx apktool frida r2 ghidra nmap nuclei sqlmap tcpdump curl; do
  which $t >/dev/null 2>&1 && echo "✅ $t" || echo "❌ $t (需要时按需安装)"
done
# 安装(按需,不一次性全装): 
#   pip install frida-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
#   apt install jadx 或下载 release; r2: apt install radare2; nmap: apt install nmap
```

**原则**：只装当前任务需要的工具；装了的工具不重复装（效率）。

## 3️⃣ 证据链（Evidence → Finding → Path）

每步记录（写报告时引用，防"查无实据"）：
```
[证据] 命令输出/截图/文件 hash → [发现] 具体漏洞/结论 → [路径] 从哪一步得出
```
- 发现漏洞 → 走 `vuln-memory` 沉淀（反例→正例+教训）
- 踩到开发坑 → 走 `dev-memory` 沉淀
- 报告 → 按需用 docs-generator 思路产出（重点：脱敏，不泄露目标细节）

## 4️⃣ 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `agent-permissions` | 权限矩阵(谁有权做什么)+ 本 skill 的授权闸门(这次行动是否合法) |
| `security-scanner` | 部署后外部扫描(nmap/nuclei/sslscan)——本 skill 的 Web 渗透工具同源 |
| `code-security` | 自己代码的安全(写码侧)；本 skill 是别人的代码(分析侧) |
| `security-audit` | 提交前六维闸门(产出侧)；本 skill 是输入侧(分析) |
| `vuln-memory` / `dev-memory` | 发现沉淀：漏洞→vuln-memory；开发坑→dev-memory |

## 5️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| 工具没装 | 上表检查→按需装(只装任务需要的) |
| 授权不明确 | 停下问用户：目标/范围/方法/边界(4 问) |
| 逆向卡住 | 换工具链(如 jadx 失败→apktool 解包看 smali)；或缩小范围 |
| 结果无法验证 | 证据链回查：哪一步的哪个输出得出该结论 |
| 报告泄露敏感 | 脱敏：目标域名/IP/密钥打码后再交付 |

> 注意：本 skill 是**方法论路由**不是工具教程——具体工具用法按需查文档/参考对应社区 skill；
> 攻击性操作（渗透/exploit）仅限授权环境，红线见 §0。
