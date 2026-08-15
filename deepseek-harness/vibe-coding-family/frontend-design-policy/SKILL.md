---
name: frontend-design-policy
description: 前端审美约束 policy：强制 UI 设计克制、颜色规范、信息密度控制， 防止多轮迭代后风格跑偏、出现"AI 味"（渐变轰炸/Emoji 堆砌/布局混乱）。 当项目涉及前端 UI、Web 页面、组件开发时自动注入。 触发词：UI、界面、前端设计、审美、样式、Design Token、页面太丑。
family-type: policy
family-version: 1.1.0
---

# 前端审美约束（Frontend Design Policy）

**目的**：AI 默认生成的 UI 有固定"AI 味"（渐变轰炸、Emoji 堆砌、卡片套卡片）。
本 policy 是持续生效的约束：每次生成/修改 UI 时自动检查，防止风格跑偏。

## 🚫 必须避免（AI 味清单）

- 过度渐变（超过 2 处大面积渐变）
- Emoji 堆砌（图标用图标库，不用 emoji 凑数；正文 emoji 最多 1 个/屏）
- 卡片套卡片（嵌套层级 >3）
- 彩虹色按钮、无意义重阴影
- 花哨装饰动画（>500ms 或非交互触发）
- 圆角/间距无统一规范（必须走 token）
- 假浏览器/手机/IDE 边框（re-drawn chrome：URL 胶囊+红绿灯点、手机壳、代码窗口标题栏）
- 斜体标题（heading/display 必须 roman，强调用字重/颜色/下划线）
- 编造指标（"+47% 转化率"、"50,000+ 用户"——无真实数据就占位符）
- 多余 section 编号标签（"01 · THE TOUR" eyebrow，除非用户明确要求章节编号）
- 连续页面/组件复用同一结构（同 hero→3 特性→CTA→footer 节奏=模板换皮，须轮换宏结构/配色/导航形态）

## ✅ 必须坚持

### 1. 布局克制
- 一屏一个核心行动点（CTA），不抢焦点
- 留白充足：块间距 ≥ 内容内边距
- 对齐一致：元素对齐到网格线

### 2. 颜色规范
- 主色 1 个 + 辅助色 ≤2 个 + 语义色（成功/警告/错误）
- 深色主题（本项目惯例）：背景 3 档灰阶层次分明
- 对比度满足 WCAG AA（正文 ≥4.5:1）

### 3. 信息密度控制
- 概览页/看板：核心指标卡片 4-6 个，不堆砌
- 表格：默认隐藏次要列，可展开
- 数字：千分位、单位、合理精度

### 4. Design Token（项目初始化时注入）
- project-scaffold 初始化时同步建立 UI 规范文件
- 颜色/间距/圆角/字号全部走 token（CSS variables / Tailwind config）
- 禁止组件内硬编码颜色值

### 5. 组件状态完整（8 态纪律）
- 交互组件必须覆盖 8 态：default / hover / :focus-visible / :active / disabled / loading / error / success
- 交付时附 8 态 demo 页（.preview.html 竖排渲染各状态）验证，确认后删除

## 🔄 检查时机（自动）

| 时机 | 动作 |
|------|------|
| 每次生成/修改 UI 组件 | 对照"必须避免"清单自查 |
| 多轮迭代（>5 轮）后 | 全局视觉一致性检查（风格是否跑偏） |
| 项目初始化 | 注入 Design Token 基础规范 |

## 🏛 设计系统契约 v2.0（v1.1 升级 — 从"防跑偏"到"保一致"）

**目的**：审美约束从防御性（禁 AI 味）升级为建设性（保证与项目设计系统一致）。

### 三层约束（优先级从高到低）

1. **项目级 `.vibe/design.yml`**（最高优先级）
   ```yaml
   design_system:
     source: "figma://file/xxx"      # 或本地路径
     tokens: "./design-tokens.json"  # 颜色/间距/圆角/字号 token
     forbidden: ["gradient-text", "emoji-in-button", "box-shadow-heavy"]
     max_colors: 5
     component_lib: "shadcn"         # 优先用项目已注册组件库，不从头写
   ```

2. **团队级 `~/.hermes/design-standards/`**
   - 团队通用规范；项目级未配置时 fallback 到这里

3. **全局级（内置于本 skill）**
   - 仅保留"绝对禁区"（闪烁动画、自动播放音频、颜色对比度不达标）

### 跑偏检测（多轮迭代后强制）

- 每轮迭代后，对比当前输出与 `.vibe/design.yml` 的符合度
- 符合度 < 80% → **阻断**，要求说明偏离理由
- 符合度 80-95% → 警告，记录理由
- 符合度 > 95% → 通过

### "AI 味"量化指标（可检测，替代主观判断）

| 指标 | 触发阈值 |
|------|----------|
| 渐变使用次数 | > 3 处 |
| Emoji 用作图标 | 连续 3 个组件 |
| border-radius 不一致 | 出现 ≥3 种不同值 |
| 卡片嵌套层级 | > 3 |
| 颜色数量 | > 5（含 token 外硬编码） |

## 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `frontend-design` | 设计原则管"怎么做好看"，本 policy 管"别犯 AI 味" |
| `hallmark` | 反模板完整工作流（21 主题+21 宏结构+58 slop 门禁+多样化轮换），本 policy 是持续注入的轻量约束，hallmark 是重型按需执行器 |
| `project-scaffold` | 初始化时注入 Design Token 规范 |
| `popular-web-designs` | 参考真实设计系统（Stripe/Linear），不凭空造 |
| `dev-stack-hub` | 前端相关任务路由入口 |
