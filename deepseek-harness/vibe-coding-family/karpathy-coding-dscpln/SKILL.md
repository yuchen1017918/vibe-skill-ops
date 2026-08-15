---
name: karpathy-coding-dscpln
description: Karpathy 编码纪律 overlay：Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution 四原则。当进行非平凡代码改动、bugfix、refactor、review 前自检、 或担心过度设计/隐藏假设/diff 蔓延时加载。vibe-coding 迭代的刹车片。
family-type: policy
family-version: 1.0.0
---

# Karpathy Coding Discipline（Karpathy 编码纪律）

来源：https://github.com/Undermybelt/hermes-skills （`skills/software-development/karpathy-coding-dscpln`，MIT）

适用：
- 非平凡代码改动
- bugfix
- refactor
- review 前自检
- vibe-coding 迭代失控（diff 蔓延、过度设计）时的刹车片

## 四原则

### 1. Think Before Coding
- 先显式假设
- 有歧义则列解释，不要静默选一条
- 若更简单路径存在，要指出
- 若关键前提不明，停下查明

### 2. Simplicity First
- 只写完成任务所需最小代码
- 不预埋未来配置层
- 不为单次使用做抽象
- 若 200 行可成 50 行，重写

### 3. Surgical Changes
- 只改请求直接命中的面
- 不顺手美化邻近代码
- 不删与任务无关的旧代码
- 只清理由自己改动造成的 orphan

### 4. Goal-Driven Execution
- 把任务转成可验证目标
- bug -> 先造复现 / 验证，再修
- refactor -> 前后验证不变
- feature -> 定义成功标准与检查方式

## 五、增量实现纪律（v1.1 新增 — 参考 addyosmani/agent-skills）

1. **垂直切片优先**：按"用户可见功能"纵切（UI→逻辑→存储），不按水平层横切（先全部 Controller 再全部 Service）
2. **Contract-First Slicing**：每片先定接口契约（输入/输出/错误语义），再实现——契约即切片边界
3. **未完成功能用 Feature Flags 藏**：不半成品上主分支；Flag 关闭 = 对用户不可见
4. **Rule 3 兜底**：切不完的片宁可不交付，不交付半成品

## Hermes 化约束

- 默认吸收为行为 discipline，不必安装任何插件或外部 skill runtime
- 更适合并入 repo 局部 `AGENTS.md` / `CLAUDE.md` / docs 约束
- 若项目已有更强本地规则，以项目规则优先

## 与 vibe-coding 的关系

vibe-coding 追求快迭代，Karpathy 纪律防止"快"变成"乱"：
- vibe 迭代每轮改动前：过一遍 Think Before Coding（假设明确吗？）
- 改完 diff 检查：是不是 Surgical？有没有顺手乱改？
- 提交前自检：目标是可验证的吗？有没有过度设计？

## 最适合的吸收方式

1. repo 文档追加短规则
2. 作为 review checklist
3. 作为实现前自检模板
4. 作为 plan/verify 提示模板

## 不建议

- 不要把它扩成长篇流程官僚文档
- 不要在简单一行改动上过度套流程
- 不要把"谨慎"变成"停滞"
