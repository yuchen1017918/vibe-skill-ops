# Hub 机制说明(按需加载,不常驻路由)

> 以下机制章节从 vibe-coding-hub 正文移出(v1.4 渐进披露瘦身)。
> 需要对应机制时按标题加载本节,其余跳过。

## 📉 执行走样日志（v3.6 新增 — 文档被遵循的证据）

**目的**：全家桶设计了很多精巧机制（熔断器/冲突四分类/信任链），但没有任何机制知道 Agent 实际执行时走了多少样。没有执行数据，文档迭代只能靠"作者想象"。

**原理**：不监控（无后台进程），而是**检查点自检**。

- **定义检查点**：关键 workflow skill（agent-loop / plan-workflow / release-management）在文档中定义 2-4 个检查点：
  ```yaml
  # agent-loop 预期路径示例
  checkpoints:
    - step: "委派前"
      verify: "是否生成 Trust Token？"
    - step: "子Agent返回后"
      verify: "是否执行了回归/交叉/渐进验证之一？"
    - step: "异常时"
      verify: "是否进入 OPEN 状态？"
  ```
- **自检时机**：snapshot-notes 会话摘要中，Agent 自检"本次是否走了预期路径"；
  knowledge-extraction 复盘阶段检查"实际执行 vs 规范"偏差
- **落盘**：偏差写入 `~/.vibe/drift/`（轻量文本，不建复杂 schema）
- **月度汇总**（用户主动要求时）："agent-loop 加载 12 次，3 次未执行验证步骤 → 该步骤设计太复杂，建议简化"

> 目的不是追责，而是**用执行数据指导文档简化**——某步骤总被跳过，说明它该删或该拆。
> 这是"少即是多"的证据闭环：不是让文档更厚，而是让文档被遵循的证据更可见。



---

## 📋 确认交互契约 v1.0（v3.5 新增 — 人工确认的 UX 契约）

**目的**：全家桶多处要求"人工确认"，但缺少统一交互契约 → 确认疲劳（习惯性点"是"）或确认逃避（直接 /simple 跳过）。以下契约统一所有确认场景（快照对齐/终端命令/审计放行）。

| 类型 | 适用场景 | 行为 | 超时策略 | UX |
|------|----------|------|----------|-----|
| **阻塞型 Blocking** | 🔴 双向漂移、🔴 系统级终端命令 | 必须等用户输入 YES/NO | 10 分钟无响应 → abort，状态存 `~/.vibe/pending/` | 高亮红色横幅 + diff 预览 |
| **通知型 Notify** | 🟡 快照超前、🟠 git 超前 | 推送通知，30 秒无回复按默认策略 | 默认：🟡=否（不应用快照）、🟠=是（更新基线） | 右下角轻量提示，可展开 |
| **批量型 Batch** | 同类冲突 ≥3 个 | 合并为一个确认单 | 列出影响文件数 + 预估风险 | 选项：全部应用/逐条审查/全部跳过 |

**免打扰窗口**：
- `/focus 30m` → 30 分钟内通知型确认自动按默认策略执行
- 阻塞型仍强制弹出（可延迟到 focus 结束后）

> 原则：阻塞型守住数据安全底线，通知型保效率，批量型防疲劳。



---

## 🌱 新手梯度 v2.0（v3.6 升级 — 连续梯度，不是阶梯跳跃）

**目的**：v1.0 按"对话次数"切换会出"第 11 次悬崖"（突然面对 28 个 skill 全量复杂度）。
v2.0 改按**已掌握概念数**，且每层都有缓冲。

**梯度分层**（按"成功完成过完整流程"的 skill 数，不是加载过）：
| 已掌握 | 模式 | 暴露内容 |
|--------|------|----------|
| 0-3 个 | 极简 | 3 入口：vibe-coding / fix-bug / new-project |
| 4-6 个 | 基础 | + snapshot-notes、plan-workflow |
| 7-10 个 | 标准 | + Triage、security-audit |
| 11-15 个 | 进阶 | + agent-loop、knowledge-extraction |
| 16+ 个 | 完整 | 全部暴露 |

**掌握判定**：成功完成过一次完整流程（由 snapshot-notes 记录实际使用历史），
不是"加载过就算掌握"。

**手动覆盖**：
- `/mode beginner` / `/mode standard` / `/mode full`
- 覆盖后记住偏好，不再自动切换
- 概念首次出现仍必须附带"为什么我需要知道这个"（认知保护原则不变）



---

## 🔗 兼容性声明（v3.6 新增 — 防文档间语义断裂）

**目的**：hub v1.2 可能引用 agent-loop v1.4 的"信任令牌"，但用户若还是 v1.3（无该概念），
引用即悬空。版本不匹配 = Agent 读到"请按信任链验证"但 skill 里没有，直接懵掉。

**契约**：
- 每个 skill 的 frontmatter 可声明依赖（存量逐步补齐，新 skill 必须带）：
  ```yaml
  requires:
    hub: ">=3.4"      # 需要 vibe-coding-hub 最低版本
    skills:           # 依赖 skill 最低版本
      - name: agent-permissions
        version: ">=1.0"
  ```
- 加载 L3 前检查 requires；不匹配 → 提示"部分功能可能失效"，**不阻断**（符合增强不是依赖）
- 月度打快照 `vibe-coding-family/.vibe/versions.lock`（记录全家桶所有 skill 精确版本）
- `/rollback-family 3.5` → 按 versions.lock 回退到上一版本组合



---

## 来源说明（真实可验证，2026-08-06 复核）

- 官方 MCP servers：https://github.com/modelcontextprotocol/servers （⭐89k）
- Hermes 主仓库：https://github.com/NousResearch/hermes-agent
- Aider：https://github.com/Aider-AI/aider （⭐30k+）
- OpenVibeCoding：https://github.com/TencentCloudBase/OpenVibeCoding
- vibekit：https://github.com/superagent-ai/vibekit
- Undermybelt/hermes-skills（1422 个 SKILL.md）：https://github.com/Undermybelt/hermes-skills
- RobinBeraud/hermes-skills：https://github.com/RobinBeraud/hermes-skills
- 其余为本地已装 skill（software-development / github / devops / mcp / creative 等分类）

> ⚠️ 已复核为 404 不存在的链接：`anthropics/mcp-code-search`、
> `wong2/mcp-server-typescript-check`、`joewing/mcp-server-python-linter`、
> `paul-gauthier/aider-chat`（正确名 Aider-AI/aider）等。
