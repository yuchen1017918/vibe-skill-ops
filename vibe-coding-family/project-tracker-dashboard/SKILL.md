---
name: project-tracker-dashboard
description: |
  HTML 可视化项目跟踪版 skill：把项目状态（任务/进度/阶段/快照）渲染成
  深色主题 Web 看板，手机友好，从 .snapshots/ 和 plan 自动生成。
  当用户说"项目可视化"、"看板"、"进度面板"、"HTML跟踪"、
  "可视化项目"、或想把当前项目状态变成网页查看时加载。
  配套 plan-workflow（计划）+ snapshot-notes（状态）→ 本 skill 做可视化。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, dashboard, html, visual, tracking, progress, kanban]
    related_skills: [vibe-coding-hub, snapshot-notes, plan-workflow, rollback-backup, hermes-web-dashboard]
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

## 📊 看板模块（7 块）

| 模块 | 内容 | 数据来源 |
|------|------|----------|
| ① 项目概要 | 名称/技术栈/当前阶段/最后更新 | SNAPSHOT.md 概要 |
| ② 任务进度 | 任务列表 + ✅⬜ + 完成百分比 | PLAN-*.md |
| ③ 阶段甘特 | Phase 0-5 进度条 | SNAPSHOT.md 已完成/进行中 |
| ④ Bug 统计 | 🔴🟠🟡🔵 数量 + 趋势 | test-report-*.md |
| ⑤ 关键决策 | 决策表（选择/理由/替代） | SNAPSHOT.md 关键决策 |
| ⑥ 坑与解法 | 踩坑时间线 | SNAPSHOT.md 坑与解法 |
| ⑦ 下一步 | 待办清单（按优先级） | PLAN.md 待办 |

## 🎨 深色主题模板（核心）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📊 项目跟踪 - {项目名}</title>
<style>
  :root {
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #e6edf3; --dim: #8b949e;
    --green: #3fb950; --yellow: #d29922; --red: #f85149; --blue: #58a6ff;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; padding:16px; }
  .wrap { max-width:1100px; margin:0 auto; }
  h1 { font-size:1.4rem; margin-bottom:4px; }
  .sub { color:var(--dim); font-size:.85rem; margin-bottom:20px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:12px; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:16px; }
  .card h2 { font-size:1rem; margin-bottom:12px; color:var(--blue); }
  .task { display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid #21262d; }
  .task:last-child { border-bottom:none; }
  .dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
  .done .dot { background:var(--green); }
  .doing .dot { background:var(--yellow); }
  .todo .dot { background:#30363d; }
  .task .name { flex:1; font-size:.88rem; }
  .done .name { color:var(--dim); text-decoration:line-through; }
  .bar { height:8px; background:#21262d; border-radius:4px; overflow:hidden; margin-top:8px; }
  .bar i { display:block; height:100%; background:var(--green); border-radius:4px; }
  .badge { display:inline-block; padding:2px 8px; border-radius:10px; font-size:.75rem; margin-right:4px; }
  .b-red { background:rgba(248,81,73,.15); color:var(--red); }
  .b-yellow { background:rgba(210,153,34,.15); color:var(--yellow); }
  .b-green { background:rgba(63,185,80,.15); color:var(--green); }
  .footer { margin-top:24px; color:var(--dim); font-size:.75rem; text-align:center; }
</style>
</head>
<body>
<div class="wrap">
  <h1>📊 {项目名}</h1>
  <div class="sub">🔄 当前阶段：{阶段} ｜ 最后更新：{时间} ｜ 技术栈：{栈}</div>
  <div class="grid">
    <!-- 任务进度卡片 -->
    <div class="card">
      <h2>✅ 任务进度（{done}/{total} · {pct}%）</h2>
      <div class="bar"><i style="width:{pct}%"></i></div>
      {任务列表 HTML}
    </div>
    <!-- 阶段甘特卡片 -->
    <div class="card">
      <h2>📈 阶段进度</h2>
      {阶段列表 HTML}
    </div>
    <!-- Bug 统计卡片 -->
    <div class="card">
      <h2>🐛 Bug 统计</h2>
      <span class="badge b-red">🔴 阻断 {blocker}</span>
      <span class="badge b-yellow">🟠 严重 {critical}</span>
      <span class="badge b-yellow">🟡 轻微 {minor}</span>
      <span class="badge b-green">🔵 优化 {suggestion}</span>
    </div>
    <!-- 下一步卡片 -->
    <div class="card">
      <h2>⏭ 下一步</h2>
      {下一步列表 HTML}
    </div>
    <!-- 关键决策卡片 -->
    <div class="card">
      <h2>🧠 关键决策</h2>
      {决策列表 HTML}
    </div>
    <!-- 坑与解法卡片 -->
    <div class="card">
      <h2>⚠️ 坑与解法</h2>
      {坑列表 HTML}
    </div>
  </div>
  <div class="footer">由 project-tracker-dashboard 自动生成 · {生成时间}</div>
</div>
</body>
</html>
```

## 🐍 生成脚本（Python，零依赖）

```python
#!/usr/bin/env python3
"""从 .snapshots/ 生成项目跟踪看板。用法：python3 gen_tracker.py <项目根>"""
import json, re, sys
from pathlib import Path
from datetime import datetime

def parse_snapshot(snap_path: Path) -> dict:
    """解析 SNAPSHOT.md 为结构化数据（概要/已完成/进行中/决策/坑）"""
    text = snap_path.read_text(encoding="utf-8") if snap_path.exists() else ""
    return {"raw": text}

def parse_plan(plan_dir: Path) -> list:
    """解析 PLAN-*.md 提取任务列表"""
    tasks = []
    for f in sorted(plan_dir.glob("PLAN-*.md")):
        text = f.read_text(encoding="utf-8")
        for line in text.splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(✅|⬜|🔄)\s*\|", line)
            if m:
                tasks.append({"id": m.group(1), "name": m.group(2).strip(),
                              "priority": m.group(3).strip(), "dep": m.group(4).strip(),
                              "accept": m.group(5).strip(), "status": m.group(6)})
    return tasks

def render(data: dict) -> str:
    """渲染 HTML（按 §模板）"""
    # 简版：实际生成时填充各模块
    return "<!DOCTYPE html>..."  # 完整模板见上文

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    snap = parse_snapshot(root / ".snapshots" / "SNAPSHOT.md")
    tasks = parse_plan(root / ".snapshots" / "plans")
    data = {"snapshot": snap, "tasks": tasks, "generated": datetime.now().isoformat()}
    out = root / "tracker"
    out.mkdir(exist_ok=True)
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "index.html").write_text(render(data), encoding="utf-8")
    print(f"✅ 看板已生成: {out / 'index.html'}")

if __name__ == "__main__":
    main()
```

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
| `plan-workflow` | 看板任务列表来自 plans/PLAN-*.md |
| `dev-team` | 开发完成后用看板展示交付成果 |
| `agent-loop` | 自动循环中定期重新生成看板（进度可视化） |
| `hermes-web-dashboard` | 通用 Web 面板模式；本 skill 是项目跟踪专用版 |
| `rollback-backup` | 看板生成前的数据备份（可选） |

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
