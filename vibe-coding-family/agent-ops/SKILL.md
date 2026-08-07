---
name: agent-ops
description: |
  多Agent基础设施 skill（v1.3 合并自 agent-workspace + agent-collab）：
  工位工作区（每个Agent专属 MEMORY/PLAN/EXPERIENCE）+ 平级协作协议
  （协作对+三步闭环+证据验证）。当启用 dev-team / 多Agent协作、
  子Agent需要直接配合或需要工位记忆时加载。
  触发词：工位、工作区、多Agent协作、协作协议、子Agent配合。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, multi-agent, workspace, collab, cubicle, teamwork]
    related_skills: [vibe-coding-hub, dev-team, agent-loop, agent-permissions, snapshot-notes]
---

# 多Agent基础设施（Agent Ops）

**v1.3 合并产物**:由 `agent-workspace`(工位)+ `agent-collab`(协作)合并而成。
多Agent场景的两个底座——"每个人有自己的工位"和"人与人能直接协作"——一份文档管完。

## 🪑 一、工位工作区

### 目录结构

```
<项目根>/
├── .snapshots/               # 🔒 团队共享记忆(snapshot-notes,不变)
├── agents/                   # 多Agent工作区
│   ├── spec-writer/          # 工位:每人一个
│   │   ├── MEMORY.md         #   工作记忆
│   │   ├── PLAN.md           #   个人规划
│   │   └── EXPERIENCE.md     #   经验/踩坑
│   ├── coder/
│   ├── tester/
│   └── bug-fixer/
└── ...项目文件
```

### 共享 vs 工位

| 维度 | `.snapshots/`(共享) | `agents/<name>/`(工位) |
|------|---------------------|------------------------|
| 级别 | 团队级 | Agent 个人级 |
| 内容 | 项目状态、团队计划 | 个人记忆、规划、经验 |
| 变更者 | snapshot-notes / plan | 各 Agent 自己 |
| 边界 | 所有 Agent 可读 | 自己的可读写,他人工位不写 |

### 子Agent 工作规范

1. **开工前**:读自己 MEMORY.md + PLAN.md 恢复上下文
2. **工作中**:重要发现 → MEMORY.md;踩坑 → EXPERIENCE.md
3. **阶段完成**:更新 PLAN.md + 同步团队状态到 .snapshots/SNAPSHOT.md
4. **交接时**:写清"上次做到/下次继续"

## 🤝 二、平级协作协议

> 不是所有协作都经主Agent中转。子Agent之间可直接协作,但必须守协议,主Agent保留终审。

### 常用协作对

| 协作对 | 场景 |
|--------|------|
| tester ↔ bug-fixer | 测出Bug → 修复 → 回归 |
| coder ↔ tester | 编码 → 测试反馈 → 调整 |
| spec-writer ↔ coder | 规范歧义澄清 |
| coder ↔ coder | 模块接口对接 |

### 三步闭环(缺失任何一步 = 协作失败)

```
Step 1 发起方写「协作请求」:请求方/接收方/问题(附上下文)/期望产出/验收标准/优先级
Step 2 接收方写「协作响应」:处理结果/产出(含路径)/验证证据(测试数/运行输出)/遗留问题
Step 3 发起方验证闭环:重新测试 → ✅ 关闭 或 ❌ 升级主Agent;经验写 EXPERIENCE.md
```

### 协作规则(必须遵守)

1. **文件不冲突**:双方不同时写同一文件;需要 → 串行
2. **证据必带**:响应必须带验证证据,不接受"我觉得修好了"
3. **职责不越界**:bug-fixer 只修Bug不重构;发现对方职责问题 → 发起请求而非直接改
4. **升级机制**:❌ 或 2 轮未闭环 → 升级主Agent
5. **回归必做**:任何修复由 tester 重跑相关测试
6. **主Agent 终审**:协作结果最终由主Agent验收

> 完整权限矩阵见 `agent-permissions`(文件系统权限/命令分级/安全红线)。

## 🚀 激活流程

```
1. 主Agent 检查 agents/ 是否已有;没有 → 按团队角色建工位
2. 每个工位初始化三件套(模板)
3. 主Agent 告知每个子Agent 其工位路径
4. 子Agent 工作前后读写工位;协作走三步闭环
```

## ⚠️ 边界规则

- **工位不替代快照**:团队状态永远写 .snapshots/,工位只存个人视角
- **协作≠失控**:平级协作只交换专业信息,最终验收在主Agent
- **协作≠越权**:tester 不修码、bug-fixer 不重构
- **工位随 git 走**:建议提交(涉密可 .gitignore);角色减少 → 工位归档不删除

## 🔗 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `dev-team` | 4 子Agent 自动获得工位(spec-writer/coder/tester/bug-fixer) |
| `agent-loop` | agent-loop 管"指挥循环",本 skill 管"工位+平级协作"——协作发生在循环内部 |
| `agent-permissions` | 权限矩阵:谁可以做什么/访问什么 |
| `snapshot-notes` | 团队共享记忆 + 协作结果同步 |

## 快速排障

| 症状 | 处理 |
|------|------|
| 工位文件丢失 | 重新初始化模板,历史在 git 可恢复 |
| Agent 忘记写工位 | 主Agent 委派提示词强制要求读写工位路径 |
| 协作响应无证据 | 退回,要求补测试数/运行输出 |
| 双方改同一文件 | 升级主Agent,切串行 |
| 协作 2 轮未闭环 | 升级主Agent(走 agent-loop 决策路由) |
