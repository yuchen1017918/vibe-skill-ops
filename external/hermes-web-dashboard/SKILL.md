---
name: hermes-web-dashboard
description: Build self-contained dark-theme web dashboards for Hermes — log viewers, process monitors, status panels. Python stdlib HTTP backend + vanilla HTML/CSS/JS frontend, zero npm deps, mobile-first responsive, port-forwarded for phone access, nohup-integrated into start_hermes.sh.
---

# Hermes Web Dashboard 构建模式

> 当用户需要构建日志查看器、进程监控、状态面板等本地 Web 仪表盘时使用。

## 架构约定

```
project-dir/              ← 自包含目录，一个项目一个文件夹
├── server.py             ← Python HTTP 后端（纯标准库，零依赖）
├── index.html            ← 前端页面
├── 图标.ico              ← favicon
└── README.md
```

后端使用 `http.server.BaseHTTPRequestHandler`，不用 Flask/FastAPI。前端纯 HTML/CSS/JS，CDN 加载 Chart.js 等库，不需要 npm。

## 后端模板

```python
#!/usr/bin/env python3
import http.server, json, os, time
from pathlib import Path
from urllib.parse import urlparse

PORT = int(os.environ.get("XXX_PORT", "8900"))
BIND = os.environ.get("XXX_BIND", "0.0.0.0")
HERE = Path(__file__).parent.resolve()
HTML_FILE = HERE / "index.html"
FAVICON_FILE = HERE / "图标.ico"

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass  # 静默控制台

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, content, status=200):
        body = content.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type):
        try:
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self._send_json({"error": "file not found"}, 404)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send_html(HTML_FILE.read_text(encoding="utf-8"))
        elif path == "/favicon.ico":
            self._send_file(FAVICON_FILE, "image/x-icon")
        elif path == "/health":
            self._send_json({"status": "ok"})
        # ... 自定义 API 路由 ...
        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    server = http.server.HTTPServer((BIND, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
```

## 前端深色主题 CSS 变量

```css
:root {
  --bg: #0d1117; --panel-bg: #161b22; --border: #30363d;
  --text: #c9d1d9; --dim: #8b949e; --accent: #58a6ff;
  --green: #3fb950; --yellow: #d2991d; --orange: #db6d28; --red: #f85149;
}
```

## 移动端优化

- Canvas 图表必须用 `position:absolute` wrapper，不用 `flex:1`（高度塌陷不渲染）
- 表格列用 `m-hide` 类 + `@media (max-width:768px) { .m-hide { display:none } }`
- viewport: `width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no`
- 触控按钮最小 44px，手机用 `display:none` 隐藏次要列
- 图表移动端纵向堆叠

## 部署到 start_hermes.sh

```bash
PORT=8900
if lsof -ti:$PORT > /dev/null 2>&1; then
    echo "服务已在运行 (端口 $PORT)"
else
    nohup python3 ~/workspace/<project>/server.py > ~/.hermes/<name>.log 2>&1 &
    sleep 1
    lsof -ti:$PORT > /dev/null 2>&1 && echo "启动成功: http://localhost:$PORT"
fi
```

## 端口转发（手机访问）

PowerShell 脚本 `port_forward_hermes.ps1` 需 UTF-8 BOM 编码，否则中文乱码导致语法错误。防火墙用"删后加"避免中文匹配：

```powershell
$ports = @(8787, 8899, 8900, 9119)
$wslIP = (wsl -e hostname -I).Trim().Split()[0]
foreach ($port in $ports) {
    netsh interface portproxy delete v4tov4 listenport=$port listenaddress=0.0.0.0 2>$null
    netsh interface portproxy add v4tov4 listenport=$port listenaddress=0.0.0.0 connectport=$port connectaddress=$wslIP
    # 防火墙: 删旧 + 加新
    netsh advfirewall firewall delete rule name="Hermes-${port}" > $null 2>&1
    netsh advfirewall firewall add rule name="Hermes-${port}" dir=in action=allow protocol=TCP localport=$port > $null
}
```

## 关停服务

```bash
kill $(lsof -ti:$PORT)
```

## 图表（Chart.js）

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4/dist/chart.umd.min.js"></script>
```

Canvas 容器模式（避免 flex 下高度 0）：

```html
<div class="chart-canvas-wrap" style="flex:1;position:relative;min-height:0">
  <canvas style="position:absolute;top:0;left:0;width:100%;height:100%"></canvas>
</div>
```

更新用 `chart.update('none')` 跳过动画以减少闪烁。

## 分屏布局 + 可拖动分割线

左右分屏是统一监控面板的标准布局（左=仪表盘+进程，右=日志）：

**CSS**：
```css
.split{display:flex;height:100vh}
.left-panel{width:50%;min-width:220px;overflow:hidden}
.right-panel{flex:1;min-width:220px;overflow:hidden}
.resizer{width:4px;cursor:col-resize;background:var(--border);flex-shrink:0;position:relative;z-index:10}
.resizer:hover,.resizer.active{background:var(--accent)}
.resizer::after{content:'';position:absolute;top:0;left:-4px;right:-4px;bottom:0}

@media(max-width:768px){.split{flex-direction:column}.resizer{display:none}}
```

**HTML**：
```html
<div class="split">
  <div class="left-panel"><!-- 仪表盘+进程 --></div>
  <div class="resizer" id="resizer"></div>
  <div class="right-panel"><!-- 日志 --></div>
</div>
```

**JS 拖拽**（support mouse + touch，范围 20%~65%）：

```js
(function(){
  const r=$('resizer'), l=r.previousElementSibling; let d=false;
  function down(e){d=true;r.classList.add('active');document.body.style.cursor='col-resize';e.preventDefault()}
  function move(e){if(!d)return;const x=e.touches?e.touches[0].clientX:e.clientX;l.style.width=Math.max(20,Math.min(65,x/r.parentElement.offsetWidth*100))+'%'}
  function up(){d=false;r.classList.remove('active');document.body.style.cursor=''}
  r.addEventListener('mousedown',down);document.addEventListener('mousemove',move);document.addEventListener('mouseup',up);
  r.addEventListener('touchstart',down,{passive:false});document.addEventListener('touchmove',move,{passive:false});document.addEventListener('touchend',up);
})();
```

⚠️ `$()` 如果是函数声明会自动 hoist；如果是 `const $ = ...` 必须放在 IIFE 之前，否则 `$('resizer')` 返回 null → `.previousElementSibling` 抛 TypeError 导致整页脚本崩溃（进程表、图表、日志全部停摆）。

## cmd.exe 从 WSL Python 调用陷阱

Python `subprocess.run` 在 WSL 内调用 `cmd.exe` 时，工作目录继承 WSL 的 UNC 路径（`\\wsl.localhost\...`），`cmd.exe` 不支持导致 stdout 为空。

**修复** — 设置 `cwd="/mnt/c/Users/<username>"` + netsh 前加 `chcp 65001 >nul &&` 避免 GBK 编码：

```python
def run_cmd(cmd, timeout=8):
    if cmd.startswith("cmd.exe"):
        r = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout,
                           cwd="/mnt/c/Users/77630")
        stdout = r.stdout.decode("utf-8", errors="replace").strip()
    else:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        stdout = r.stdout.strip()
    return {"ok": r.returncode == 0, "stdout": stdout}
```

## nohup + wsl.exe 生命周期陷阱

Windows 任务计划程序通过 `wsl.exe bash -c "nohup python3 server.py &"` 启动服务时，**wsl.exe 退出会终止整个 WSL 会话**，`nohup` 也保不住子进程。

**修复** — 独立启动脚本等待端口就绪后再退出：

```bash
#!/bin/bash
cd /path/to/project
nohup python3 server.py > /path/to/log 2>&1 &
for i in $(seq 1 10); do
  sleep 0.5
  curl -s http://127.0.0.1:PORT/health >/dev/null 2>&1 && exit 0
done
exit 1
```

任务计划程序参数：`bash /path/to/start.sh`（不用 `wsl.exe bash -c "..."`）

## 参考实现

- `references/combined-monitor-server.py` — 统一后端模板（进程+日志+终端三合一）
- `references/port-diag-server.py` — 端口诊断后端（cmd.exe + portproxy 检测）
- `references/log-viewer-backend.py` — 双面板日志查看器后端（反向读取大文件优化）
- `references/monitor-backend.py` — 进程硬件监控后端（psutil + kill/run API）
