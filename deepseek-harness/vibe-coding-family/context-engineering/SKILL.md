---
name: context-engineering
description: 上下文工程：5 层上下文层级（规则文件→规格→源码→错误输出→会话历史）+ 文件信任分级（Trusted/Verify/Untrusted）+ 预任务上下文加载策略。 大项目 token 优化核心——按层级喂上下文，不全文塞。 当大项目启动、token 超预算、或"上下文不够用/太乱"时加载。 触发词：上下文、context、token优化、喂上下文、信任分级。
family-type: tool
family-version: 1.0.0
---

# Context Engineering（上下文工程）

**来源**：addyosmani/agent-skills。
**核心**：上下文是**预算**不是垃圾场——按层级喂，按信任分级，不全文塞。
大项目 token 优化靠的不是压缩，是**喂什么、什么时候喂、信多少**。

## 1️⃣ 5 层上下文层级（优先级从高到低）

```
L1 规则文件   AGENTS.md / CLAUDE.md / .cursorrules   ← 最高优先, 最该信
L2 规格文档   需求/PRD/设计/ADR/接口契约
L3 源码       实际代码(按需检索, 不全文)
L4 错误输出   真实报错/日志/测试失败(最新鲜, 最可信)
L5 会话历史   之前说过的话(最易过时, 最不该当"事实")
```

**喂食策略**：
- **预任务加载**：任务开始前只喂 L1+L2（规则+规格），L3 按需检索（`vibe-code-search`），L4 出现时实时喂，L5 当参考不当依据
- **冲突裁决**：层越高越可信——L1 规则 vs L5 旧会话记忆 → 信 L1
- **budget 意识**：L1+L2 常驻 ≈ 1-2K token；L3 按需；L4 短；L5 压缩

## 2️⃣ 文件信任分级（Trusted / Verify / Untrusted）

| 级别 | 文件 | 处理 |
|------|------|------|
| **Trusted** | 规则文件、锁文件(lock)、官方规范 | 直接遵循,不质疑 |
| **Verify** | 生成的代码、第三方库代码、迁移脚本 | 用前验证(测试/跑通),不完全相信 |
| **Untrusted** | 用户输入、网络抓取、AI 生成的未验证代码 | 不直接执行/信任,先 sanitize+验证 |

> 与 code-security 呼应：Untrusted 输入默认不拼命令/不 eval/不过滤即用。

## 3️⃣ CLAUDE.md / AGENTS.md 模板（L1 规则文件怎么写）

```markdown
# 项目规则（L1 — 最高信任层）
## 目标: 一句话
## 技术栈: <从 .vibe/stack.yaml 读取>
## 命令:
- 构建: `npm run build`
- 测试: `npm test`
- 格式: `npx prettier --check .`
## 约束:
- 提交前过 security-audit（六维闸门）
- 终端白名单: 禁 rm -rf / sudo / mkfs
## 参考: <关键文档路径>
```

## 4️⃣ 预任务上下文加载清单（任务开始时 30 秒）

```
□ L1 规则文件已读(AGENTS.md/CLAUDE.md)? 
□ L2 规格/需求已明确(目标一句话)?
□ L3 代码入口已定位(用 vibe-code-search, 不全文读)?
□ L4 相关错误输出已备?
□ L5 旧会话只当参考(不当事实)?
```

## 5️⃣ 与全家桶衔接

| Skill | 分工 |
|-------|------|
| `project-init` | 初始化时生成 L1 规则文件 + L2 规格（本 skill 是它的"喂食方法论"） |
| `snapshot-notes` | L5 会话历史的持久化（快照替代记忆） |
| `vibe-code-search` | L3 源码的按需检索通道（大项目不全文塞） |
| `dev-assistant` | 副驾驶模式的上下文按需喂食 |

## 6️⃣ 快速排障

| 症状 | 处理 |
|------|------|
| 上下文溢出 | 检查是否喂了 L3 全文 → 改 vibe-code-search 按需 |
| 旧假设当事实 | L5 降级：旧会话记忆 → 验证后再信（联动 doubt-driven-development） |
| 规则冲突 | 层高者胜：L1 > L2 > L3 > L4 > L5 |
| 信任了不该信的 | Verify 级文件先跑测试；Untrusted 先 sanitize |
