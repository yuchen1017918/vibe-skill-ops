# Contributing to Vibe-Skill-Ops(中文)

[English](CONTRIBUTING.md) | 中文

感谢你考虑为 Vibe-Skill-Ops 做贡献!全家桶的核心哲学是**大道至简** —— 每一个新 skill 都在增加常驻上下文的成本,所以新增比删减难得多。以下规则保证全家桶在增长的同时不失控。

## 新增 skill 的硬性门槛(四条,缺一不可)

1. **契约层 ≤5 行** — description 是唯一常驻可见的部分。必须包含:触发词(trigger)/ 负触发词(negative_trigger)/ 类型(type)/ 依赖(deps)/ 关键规则(key_rule)。超过 5 行会被打回。
2. **7 天冷静期** — 新 skill 先在 `vibe-skills-gov-patterns` 的冷却区试用,30 天未加载自动 deprecated(文件保留防交叉引用)。
3. **组合性证明** — 必须证明该能力**无法由现有 skill 组合而成**。如果 2-3 个现有 skill 拼起来能做 80%,那答案是不新增。
4. **冲突模拟** — 运行场景冲突测试:你的新触发词会不会和现有 skill 抢词?冲突仲裁优先级是什么?

## 契约层模板

```yaml
---
name: your-skill
description: |
  <一句话:做什么> + <触发场景>。
  触发词:<词1>、<词2>。
version: 1.0.0
metadata:
  hermes:
    type: tool | workflow | policy | meta
    related_skills: [相关 skill 列表]
---
```

## 修改现有 skill

- 每个规则变更都需要 Changelog 条目:**为什么存在、解决什么痛点**。
- 保持诚实:文档里要写明"这是惯例(convention)"还是"这是强制(enforced)"。
- 结构变更(合并/废弃)走 `skill-family-maintenance` 流程:保留主名吸收内容 → 被吸收方标 deprecated → 全库 sed 引用替换(排除合并方与 deprecated)→ 更新 hub 计数/场景表。

## 提交与 PR

1. Fork + 功能分支(遵循 `git-workflow`:原子提交、存档点、Trunk-Based)
2. 提交前过双闸门:code-security 纪律自查 + security-audit 扫描(commit 会被 hook 拦)
3. PR 描述写清:痛点 → 方案 → 验证结果(真实运行输出,不是纸面)
4. 合并前过 `open-code-review` 审查

## 什么是不欢迎的

- ❌ 一个"关于 X 的 skill" —— description 必须有明确触发条件
- ❌ 重复已有能力的变体 —— 先搜再写(用 `vibe-code-search`)
- ❌ 一次性脚本塞进全家桶 —— 一次性任务走 `quick-dev`,沉淀验证后才考虑升级
- ❌ 超过 300 行的 SKILL.md —— 细节进 references/,正文保持可 30 秒读完

## 风格

- 语言:SKILL.md 用中文为主(面向中文用户),关键机制词保留英文原词
- README 双语文档:英文 `README.md`(默认)+ 中文 `README.zh-CN.md`,顶部 LANG 互链
- 证据优先:任何"实测""已验证"必须有真实运行输出支撑,禁止编造

有问题先开 Issue 讨论,不要直接开 PR 大改。谢谢!
