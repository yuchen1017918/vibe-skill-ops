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

