## 🐍 生成脚本（Python，零依赖）

```python
#!/usr/bin/env python3
"""从 .snapshots/ + .vibe/bugs/ 生成项目跟踪看板。用法：python3 gen_tracker.py <项目根>"""
import json, re, sys
from pathlib import Path
from datetime import datetime

SEV = {"blocker": ("🔴 阻断", "b-red"), "critical": ("🟠 严重", "b-red"),
       "minor": ("🟡 轻微", "b-yellow"), "suggestion": ("🔵 优化", "b-blue")}
ZONES = [("active", "🔥 活跃（修复中）", "#f85149"),
         ("dormant", "💤 不活跃（哨兵监视，待根治）", "#d29922"),
         ("extinct", "💀 已灭绝（根治+观察期满）", "#3fb950")]

def parse_snapshot(snap_path: Path) -> dict:
    text = snap_path.read_text(encoding="utf-8") if snap_path.exists() else ""
    return {"raw": text}

def parse_plan(plan_dir: Path) -> list:
    tasks = []
    if not plan_dir.exists():
        return tasks
    for f in sorted(plan_dir.glob("PLAN-*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(✅|⬜|🔄)\s*\|", line)
            if m:
                tasks.append({"id": m.group(1), "name": m.group(2).strip(),
                              "priority": m.group(3).strip(), "dep": m.group(4).strip(),
                              "accept": m.group(5).strip(), "status": m.group(6)})
    return tasks

def parse_bugs(bug_dir: Path) -> list:
    """解析 .vibe/bugs/BUG-*.md（bug-hunting 档案格式）→ 结构化列表"""
    bugs = []
    if not bug_dir.exists():
        return bugs
    for f in sorted(bug_dir.glob("BUG-*.md")):
        text = f.read_text(encoding="utf-8")
        meta = {}
        m = re.search(r"<!--\s*bug-meta(.*?)-->", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                mm = re.match(r"\s*([^:]+):\s*(.+)", line)
                if mm:
                    meta[mm.group(1).strip()] = mm.group(2).strip()
        title_m = re.match(r"#\s*BUG-(\d+)\s*(.*)", text)
        # 四阶段进度：定位(有章节)/止血(已上)/根治(有日期)/哨兵(有位置)
        prog = 0
        prog += 1 if "## 定位过程" in text else 0
        prog += 1 if re.search(r"##\s*短期修复[\s\S]*?状态:\s*已上", text) else 0
        prog += 1 if re.search(r"##\s*根治方案[\s\S]*?日期:\s*\d{4}-\d{2}-\d{2}", text) else 0
        prog += 1 if re.search(r"##\s*哨兵[\s\S]*?位置:", text) else 0
        status = meta.get("状态", "active")
        if status == "resurrected":
            status = "active"  # 复活归活跃区显示
        bugs.append({
            "id": title_m.group(1) if title_m else f.stem.replace("BUG-", ""),
            "title": title_m.group(2).strip() if title_m else f.stem,
            "status": status,
            "severity": meta.get("严重级", "minor"),
            "found": meta.get("发现", "?"),
            "resurrections": int(meta.get("复活次数", "0") or 0),
            "prog": prog,  # 0-4
        })
    return bugs

def render_bug_panel(bugs: list) -> str:
    """渲染三区 bug 面板 HTML"""
    if not bugs:
        return '<div class="card wide"><h2>🐛 Bug 追踪</h2><p style="color:var(--dim)">暂无 bug 档案（.vibe/bugs/ 为空）</p></div>'
    parts = ['<div class="card wide"><h2>🐛 Bug 追踪面板 <span style="color:var(--dim);font-size:.8rem">共 {n} 个</span></h2>'.format(n=len(bugs))]
    for zone, label, color in ZONES:
        zone_bugs = [b for b in bugs if b["status"] == zone]
        parts.append(f'<div class="bug-zone"><h3 style="color:{color}">{label} · {len(zone_bugs)}</h3>')
        if not zone_bugs:
            parts.append('<p style="color:var(--dim);font-size:.85rem">—</p>')
        for b in zone_bugs:
            sev_label, sev_cls = SEV.get(b["severity"], ("❓", "b-blue"))
            res_badge = f'<span class="badge b-purple">🧟 复活×{b["resurrections"]}</span>' if b["resurrections"] > 0 else ""
            bar_w = int(b["prog"] / 4 * 100)
            parts.append(
                f'<div class="bug-item">'
                f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">'
                f'<b>BUG-{b["id"]}</b><span style="font-size:.85rem">{b["title"]}</span>'
                f'<span class="badge {sev_cls}">{sev_label}</span>{res_badge}'
                f'<span style="color:var(--dim);font-size:.75rem;margin-left:auto">发现 {b["found"]}</span></div>'
                f'<div class="bar" style="margin-top:4px"><i style="width:{bar_w}%"></i></div>'
                f'<div style="color:var(--dim);font-size:.7rem">定位→止血→根治→哨兵 {b["prog"]}/4</div>'
                f'</div>')
        parts.append('</div>')
    parts.append('</div>')
    return "\n".join(parts)

def render_tasks(tasks: list) -> str:
    if not tasks:
        return '<p style="color:var(--dim)">无任务（.snapshots/plans/ 为空）</p>'
    done = sum(1 for t in tasks if t["status"] == "✅")
    pct = int(done / len(tasks) * 100)
    rows = []
    for t in tasks:
        cls = "done" if t["status"] == "✅" else ("doing" if t["status"] == "🔄" else "todo")
        rows.append(f'<div class="task {cls}"><span class="dot"></span>'
                    f'<span class="name">#{t["id"]} {t["name"]} <span style="color:var(--dim);font-size:.75rem">{t["priority"]}</span></span>'
                    f'<span>{t["status"]}</span></div>')
    return (f'<div class="bar"><i style="width:{pct}%"></i></div>'
            f'<div style="color:var(--dim);font-size:.75rem;margin:4px 0 8px">{done}/{len(tasks)} · {pct}%</div>'
            + "\n".join(rows))

def render(data: dict) -> str:
    name = data.get("name", "项目")
    stage = data.get("stage", "—")
    ts = data.get("generated", "")
    bugs_html = render_bug_panel(data["bugs"])
    tasks_html = render_tasks(data["tasks"])
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📊 项目跟踪 - {name}</title>
<style>
:root {{ --bg:#0d1117; --card:#161b22; --border:#30363d; --text:#e6edf3; --dim:#8b949e;
  --green:#3fb950; --yellow:#d29922; --red:#f85149; --blue:#58a6ff; --purple:#bc8cff; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--text); font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; padding:16px; }}
.wrap {{ max-width:1100px; margin:0 auto; }}
h1 {{ font-size:1.4rem; margin-bottom:4px; }}
.sub {{ color:var(--dim); font-size:.85rem; margin-bottom:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:12px; }}
.card {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:16px; }}
.card.wide {{ grid-column:1/-1; }}
.card h2 {{ font-size:1rem; margin-bottom:12px; color:var(--blue); }}
.task {{ display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid #21262d; }}
.task:last-child {{ border-bottom:none; }}
.dot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}
.done .dot {{ background:var(--green); }}
.doing .dot {{ background:var(--yellow); }}
.todo .dot {{ background:#30363d; }}
.task .name {{ flex:1; font-size:.88rem; }}
.done .name {{ color:var(--dim); text-decoration:line-through; }}
.bar {{ height:8px; background:#21262d; border-radius:4px; overflow:hidden; margin-top:8px; }}
.bar i {{ display:block; height:100%; background:var(--green); border-radius:4px; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:10px; font-size:.75rem; }}
.b-red {{ background:rgba(248,81,73,.15); color:var(--red); }}
.b-yellow {{ background:rgba(210,153,34,.15); color:var(--yellow); }}
.b-green {{ background:rgba(63,185,80,.15); color:var(--green); }}
.b-blue {{ background:rgba(88,166,255,.15); color:var(--blue); }}
.b-purple {{ background:rgba(188,140,255,.15); color:var(--purple); }}
.bug-zone {{ margin-top:10px; }}
.bug-zone h3 {{ font-size:.9rem; margin-bottom:6px; }}
.bug-item {{ padding:8px 0; border-bottom:1px solid #21262d; }}
.bug-item:last-child {{ border-bottom:none; }}
.footer {{ margin-top:24px; color:var(--dim); font-size:.75rem; text-align:center; }}
</style></head><body><div class="wrap">
<h1>📊 {name}</h1>
<div class="sub">🔄 当前阶段：{stage} ｜ 最后更新：{ts} ｜ 技术栈：{data.get("stack","—")}</div>
<div class="grid">
{bugs_html}
<div class="card"><h2>✅ 任务进度</h2>{tasks_html}</div>
<div class="card"><h2>🧠 关键决策</h2><p style="color:var(--dim)">见 .snapshots/SNAPSHOT.md</p></div>
<div class="card"><h2>⚠️ 坑与解法</h2><p style="color:var(--dim)">见 .snapshots/SNAPSHOT.md</p></div>
<div class="card"><h2>⏭ 下一步</h2><p style="color:var(--dim)">见 .snapshots/plans/PLAN-*.md</p></div>
</div>
<div class="footer">由 project-tracker-dashboard 自动生成 · {ts}</div>
</div></body></html>"""

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    snap = parse_snapshot(root / ".snapshots" / "SNAPSHOT.md")
    tasks = parse_plan(root / ".snapshots" / "plans")
    bugs = parse_bugs(root / ".vibe" / "bugs")
    # 项目名/阶段从 SNAPSHOT.md 第一行提取
    name, stage, stack = root.name, "—", "—"
    for line in snap["raw"].splitlines()[:10]:
        mm = re.match(r"#\s+(.+)", line)
        if mm:
            name = mm.group(1).strip()
            break
    data = {"name": name, "stage": stage, "stack": stack,
            "snapshot": snap, "tasks": tasks, "bugs": bugs,
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M")}
    out = root / "tracker"
    out.mkdir(exist_ok=True)
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (out / "index.html").write_text(render(data), encoding="utf-8")
    print(f"✅ 看板已生成: {out / 'index.html'}（bug {len(bugs)} 个）")

if __name__ == "__main__":
    main()
```
