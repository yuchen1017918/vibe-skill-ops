---
name: project-tracker-dashboard
description: HTML 可视化项目跟踪版 skill：把项目状态（任务/进度/阶段/快照）渲染成 深色主题 Web 看板，手机友好，从 .snapshots/ 和 plan 自动生成。 当用户说"项目可视化"、"看板"、"进度面板"、"HTML跟踪"、 "可视化项目"、或想把当前项目状态变成网页查看时加载。 配套 project-init（计划）+ snapshot-notes（状态）→ 本 skill 做可视化。
family-type: tool
family-version: 1.1.0
---

# HTML 可视化项目跟踪（Project Tracker Dashboard）

**核心闭环**：项目数据（.snapshots/ + plans/）→ 生成自包含 HTML 看板 → 浏览器/手机查看 → 随时刷新。

```
.snapshots/SNAPSHOT.md  ─┐
.snapshots/plans/PLAN-*.md ─┼→ 读取 → 渲染 → index.html（深色主题看板）
agents/*/PLAN.md        ─┘               ├─ 任务进度（✅⬜ + 百分比）
                                        ├─ 阶段状态（Phase 甘特）
                                        ├─ Bug 统计（🔴🟠🟡🔵）
                                        └─ 关键决策/坑（时间线）
```

## 📁 输出结构

```
<项目根>/tracker/
├── index.html        ← 自包含看板（单文件，零依赖）
└── data.json         ← 项目数据快照（由脚本生成，看板读取）
```

## 🚀 生成流程

```
1. 读取项目状态：
   - .snapshots/SNAPSHOT.md → 阶段/决策/坑/关键文件
   - .snapshots/plans/PLAN-*.md → 任务列表（#/优先级/依赖/状态）
   - docs/dev-team/test-report-*.md（如有）→ Bug 统计
2. 生成 data.json（结构化数据）
3. 渲染 index.html（深色主题，见 §模板）
4. 可选：python -m http.server 起本地服务 / 端口转发到手机
```

## 📊 看板模块（8 块）

| 模块 | 内容 | 数据来源 |
|------|------|----------|
| ① 项目概要 | 名称/技术栈/当前阶段/最后更新 | SNAPSHOT.md 概要 |
| ② 任务进度 | 任务列表 + ✅⬜ + 完成百分比 | PLAN-*.md |
| ③ 阶段甘特 | Phase 0-5 进度条 | SNAPSHOT.md 已完成/进行中 |
| ④ Bug 追踪面板 | 三区（🔥活跃/💤不活跃/💀已灭绝）+ 编号归类 + 三层修复进度条 + 复活次数 | .vibe/bugs/BUG-*.md |
| ⑤ 关键决策 | 决策表（选择/理由/替代） | SNAPSHOT.md 关键决策 |
| ⑥ 坑与解法 | 踩坑时间线 | SNAPSHOT.md 坑与解法 |
| ⑦ 下一步 | 待办清单（按优先级） | PLAN.md 待办 |

> ④ Bug 追踪面板 v1.1 升级（联动 `bug-hunting`）：不再是统计数字，读 `.vibe/bugs/BUG-*.md` 渲染完整三区面板——活跃（修复中/复活）/不活跃（哨兵监视待根治）/已灭绝（根治+观察期满），每卡显示编号、严重级徽章、三层修复进度（定位→止血→根治→哨兵）、复活次数。bug 档案由 `bug-hunting` skill 维护，看板只读渲染。

## 🎨 深色主题模板 + 🐍 生成脚本

> 模板与脚本已移 `references/`（v1.4 渐进披露瘦身，按需加载）：`references/template.html`（深色主题核心）+ `references/generator.py`（Python 零依赖生成脚本）。需要生成看板时加载。

## 📱 查看方式

| 方式 | 命令 | 场景 |
|------|------|------|
| 直接打开 | `open tracker/index.html`（或浏览器双击） | 本机快速看 |
| 本地服务 | `python3 -m http.server 8080 -d tracker` | 局域网共享 |
| 手机访问 | WSL 端口转发到 Windows 局域网（见 `wsl-port-forward`） | 手机随时看 |

## 🔄 更新频率

| 时机 | 动作 |
|------|------|
| 每个阶段完成 | 重新生成看板（数据变了） |
| 用户说"更新看板" | 重跑生成脚本 |
| 每日（长跑项目） | cron 定时重生成 |
| 发布前 | 生成最终版看板归档 |

## 🤝 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `snapshot-notes` | 看板数据源：SNAPSHOT.md 提供阶段/决策/坑 |
| `project-init` | 看板任务列表来自 plans/PLAN-*.md |
| `dev-team` | 开发完成后用看板展示交付成果 |
| `agent-ops` | 自动循环中定期重新生成看板（进度可视化） |
| `bug-hunting` | Bug 档案生产者（.vibe/bugs/）；本 skill 只读渲染三区面板 |
| `hermes-web-dashboard` | 通用 Web 面板模式；本 skill 是项目跟踪专用版 |
| `release-ops` | 看板生成前的数据备份（可选） |

## ⚠️ 核心原则

1. **数据从 .snapshots/ 来**：看板是"状态的可视化"，不手动编辑。
2. **单文件零依赖**：index.html 自包含，纯 HTML/CSS/JS，无需 npm。
3. **手机友好**：响应式布局（grid auto-fit），手机上也能看。
4. **深色主题**：默认深色，降低长时间查看疲劳。
5. **随时可刷新**：数据变化 → 重跑脚本即可。

## 快速排障

| 症状 | 处理 |
|------|------|
| 看板空白 | 检查 .snapshots/SNAPSHOT.md 是否存在、data.json 是否生成 |
| 任务列表为空 | 检查 .snapshots/plans/PLAN-*.md 格式（表格行） |
| 手机打不开 | 检查端口转发（wsl-port-forward）；确认 http.server 在跑 |
| 中文乱码 | 确认 meta charset="UTF-8" + Python 写入 encoding="utf-8" |
| 刷新不更新 | 浏览器缓存 → Ctrl+F5；或加 Cache-Control: no-cache |
