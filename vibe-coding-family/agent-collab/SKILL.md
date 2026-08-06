---
name: agent-collab
description: |
  多Agent协作 skill：定义子Agent之间的平级协作协议——
  测试Agent与Bug修复Agent协作修Bug、编码与测试互相反馈、
  规范与编码澄清歧义等各协作对的协作指导。
  当多Agent任务中出现"需要两个Agent直接配合"（如测试发现Bug
  需要修复、编码需要测试反馈、接口对接）时加载。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, multi-agent, collaboration, peer, handoff, teamwork]
    related_skills: [vibe-coding-hub, dev-team, agent-loop, agent-workspace, multi-agent-config-manager]
---

# 多Agent协作（Agent Collab）

**核心思想**：不是所有协作都要经主Agent中转。两个子Agent之间可以**直接协作**，
但必须遵守统一协作协议，且主Agent保留最终把关权。

```
协作模型对比：

❌ 旧（星型，一切经主Agent）
   tester → 主Agent → bug-fixer → 主Agent → tester（每步中转，慢）

✅ 新（平级协作，协议约束）
   tester ←→ bug-fixer  直接协作（带上下文传递 + 证据验证）
   coder  ←→ tester     互相反馈
   协作结果 → 主Agent 最终验收
```

## 1️⃣ 协作对（常用场景）

> **前置检查（v1.1 新增）**：任何协作发起前，双方必须先做**状态对齐**——
> 读取 `.snapshots/SNAPSHOT_INDEX.json` 的 current 版本，比对自身任务上下文。
> 阶段不一致 → 先对齐再协作（详见 `snapshot-notes` 冲突检测流程），
> 避免基于过时状态盲目协作。

| 协作对 | 协作场景 | 协作内容 |
|--------|----------|----------|
| **tester ↔ bug-fixer** | 测试发现Bug → 修复 → 回归 | 测试报告（含失败用例/堆栈/期望vs实际）→ 修复 → 回归验证 |
| **coder ↔ tester** | 编码完成 → 测试反馈 → 调整 | 实现说明 → 测试发现的问题 → 编码修正 |
| **spec-writer ↔ coder** | 规范歧义 → 澄清 | 规范中模糊处 → 编码询问 → 规范补充 |
| **coder ↔ coder** | 模块接口对接 | 接口定义 → 实现契约 → 联调 |
| **tester ↔ spec-writer** | 测试发现规范问题 | 无法测试的验收标准 → 规范修订 |
| **bug-fixer ↔ coder** | 修复涉及架构 → 协商 | 根因在架构层 → 协商最小修复 vs 重构 |

## 2️⃣ 协作协议（三步闭环）

每次协作必须走完三步，任何一步缺失视为协作失败：

### Step 1: 发起方写「协作请求」（Request）
```markdown
## 🤝 协作请求
- **请求方**：<Agent角色>
- **接收方**：<Agent角色>
- **问题**：<具体问题，附上下文/文件路径/错误信息>
- **期望产出**：<接收方要交付什么>
- **验收标准**：<怎么判断协作成功>
- **优先级**：🔴 阻塞 / 🟠 严重 / 🟡 一般
```

### Step 2: 接收方处理并写「协作响应」（Response）
```markdown
## 🤝 协作响应
- **接收方**：<Agent角色>
- **处理结果**：✅ 已解决 / ⚠️ 部分解决 / ❌ 无法解决
- **产出**：<文件/代码/说明，含路径>
- **验证证据**：<运行结果/测试数/前后对比>
- **遗留问题**：<如有>
```

### Step 3: 发起方验证并闭环（Verify & Close）
```markdown
## ✅ 协作闭环
- **验证结果**：<重新测试/检查，真实结果>
- **是否解决**：✅ 是（关闭） / ❌ 否（升级给主Agent）
- **经验沉淀**：<写入 EXPERIENCE.md>
```

## 3️⃣ 协作规则（必须遵守）

1. **文件不冲突**：协作双方不得同时写同一文件；需要改同一文件 → 串行（先 A 后 B）。
2. **证据必带**：响应必须带验证证据（测试数/运行输出），不接受"我觉得修好了"。
3. **职责不越界**：bug-fixer 只修Bug不重构；coder 只按规范编码；发现对方职责问题 → 发起协作请求而非直接改。
4. **升级机制**：协作 ❌ 或 2 轮未闭环 → 升级给主Agent（写入汇报块）。
5. **回归必做**：任何修复必须由 tester 重新运行相关测试（协作闭环 Step 3）。
6. **主Agent 终审**：协作结果最终由主Agent验收，不绕过指挥循环。

## 4️⃣ 协作中的角色边界

> 完整权限矩阵见 `agent-permissions` skill（文件系统权限/命令分级/数据安全红线）。
> 以下为协作场景的快速边界速查：

| Agent | 可以做什么 | 不可以做什么 |
|-------|-----------|--------------|
| tester | 指出Bug、给失败用例、要求修复、验证修复 | ❌ 自己改源码（除非主Agent明确授权） |
| bug-fixer | 修Bug、回归测试、解释根因 | ❌ 借修复重构、改测试预期不说明理由 |
| coder | 按规范实现、响应测试反馈 | ❌ 跳过测试直接交付 |
| spec-writer | 澄清规范、补充验收标准 | ❌ 改架构不更新文档 |

## 5️⃣ 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `agent-loop` | agent-loop 管"指挥循环"，agent-collab 管"平级协作"。协作发生在循环内部：派发→（可选平级协作）→汇报 |
| `agent-workspace` | 协作经验写入双方工位 `EXPERIENCE.md`；协作上下文在工位间传递 |
| `dev-team` | 4 子Agent 之间的协作对（§1）由本 skill 提供协议 |
| `snapshot-notes` | 协作结果同步到 `.snapshots/SNAPSHOT.md`（团队可见） |
| `multi-agent-config-manager` | 深度研究分支协作同样适用三步协议 |

## 6️⃣ 协作触发判断

```
子Agent 工作遇到问题：
  ├─ 自己能解决 → 自己处理（不协作）
  ├─ 需要另一个Agent的专业知识 → 发起协作请求（三步闭环）
  ├─ 需要主Agent决策（方向性/跨模块）→ 走 agent-loop 询问路由
  └─ 协作 2 轮未闭环 → 升级给主Agent
```

## ⚠️ 边界与安全

- **协作≠失控**：平级协作只交换专业信息，最终验收仍在主Agent。
- **协作≠越权**：tester 不修码、bug-fixer 不重构、coder 不越规范。
- **文件锁**：同一文件同一时刻只有一个写者。
- **证据链**：每个协作响应必须可验证（测试数/运行输出）。
- **防串扰**：协作消息通过主Agent转发或在共享文档中进行，不直接修改对方工位。

## 快速排障

| 症状 | 处理 |
|------|------|
| 协作请求无人响应 | 主Agent 检查接收方是否空闲；超时则转发 |
| 协作响应无证据 | 退回，要求补测试数/运行输出 |
| 双方改同一文件冲突 | 升级主Agent，切串行 |
| 协作 2 轮未闭环 | 升级主Agent（走 agent-loop 决策路由） |
| 协作经验丢失 | 写入双方工位 EXPERIENCE.md + 团队 SNAPSHOT.md |
