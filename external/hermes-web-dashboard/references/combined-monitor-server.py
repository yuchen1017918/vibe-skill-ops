#!/usr/bin/env python3
"""Combined Monitor Server — template for single-server multi-panel dashboards.
Serves: system stats (psutil), process list, log tailing, and a POST terminal API — all from one port.
"""

import http.server, json, os, re, signal, subprocess, time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import psutil

PORT = int(os.environ.get("PORT", "8900"))
BIND = "0.0.0.0"
HERE = Path(__file__).parent.resolve()

# ---- cmd.exe from WSL: must use cwd=/mnt/c/Users/<username> to avoid UNC path error ----
def run_cmd(cmd, timeout=8):
    if cmd.startswith("cmd.exe"):
        r = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout,
                           cwd="/mnt/c/Users/<YOUR_USERNAME>")
        stdout = r.stdout.decode("utf-8", errors="replace").strip()
    else:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        stdout = r.stdout.strip()
    return {"ok": r.returncode == 0, "stdout": stdout}

# ---- System stats (psutil) ----
def get_system_stats():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    swap = psutil.swap_memory()
    procs = []
    for p in psutil.process_iter(["pid","name","cpu_percent","memory_info","cmdline"]):
        try:
            pi = p.info
            cmd = " ".join(pi.get("cmdline") or [])
            if "hermes" in (pi.get("name","")+" "+cmd).lower():
                meminfo = pi.get("memory_info")
                procs.append({
                    "pid": pi["pid"], "name": pi["name"], "cmdline": cmd[:200],
                    "cpu_percent": round(pi.get("cpu_percent") or 0, 1),
                    "mem_rss_mb": round(meminfo.rss/1024/1024,1) if meminfo else 0
                })
        except: pass
    return {
        "cpu": {"percent": round(cpu,1), "count": psutil.cpu_count()},
        "memory": {"total_gb": round(mem.total/1024**3,1), "used_gb": round(mem.used/1024**3,1), "percent": round(mem.percent,1)},
        "disk": {"total_gb": round(disk.total/1024**3,1), "used_gb": round(disk.used/1024**3,1), "percent": round(disk.percent,1)},
        "swap_percent": round(swap.percent,1),
        "processes": sorted(procs, key=lambda x:x["cpu_percent"], reverse=True),
        "uptime_seconds": round(time.time()-psutil.boot_time(),0),
    }

# ---- Log tailing (reverse-read for large files) ----
LOG_FILES = {
    "gateway": Path.home()/".hermes"/"logs"/"gateway.log",
    "web": Path.home()/".hermes"/"webui"/"bootstrap-8787.log",
}

def read_tail(filepath, cursor, max_lines=500):
    if not filepath.exists():
        return {"lines":[],"next_cursor":0,"error":"not found"}
    try:
        size = filepath.stat().st_size
        if cursor > size: cursor = 0
        with open(filepath,"r",encoding="utf-8",errors="replace") as f:
            if cursor == 0:
                blocks=[]; pos=size; remain=max_lines+1
                while pos>0 and remain>0:
                    rsize=min(4096,pos); pos-=rsize; f.seek(pos)
                    blocks.append(f.read(rsize)); remain-=blocks[-1].count("\n")
                lines=[l for l in "".join(reversed(blocks)).split("\n") if l][-max_lines:]
            else:
                f.seek(cursor)
                if cursor!=0: f.readline()
                lines=[l.rstrip("\n\r") for l in f if l.strip()]
                cursor=f.tell()
        return {"lines":lines,"next_cursor":cursor if cursor else size,"file_size":size}
    except Exception as e:
        return {"lines":[],"next_cursor":cursor,"error":str(e)}

# ---- HTTP Handler ----
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _json(self,d,s=200):
        b=json.dumps(d,ensure_ascii=False).encode()
        self.send_response(s);self.send_header("Content-Type","application/json;charset=utf-8")
        self.send_header("Access-Control-Allow-Origin","*");self.send_header("Cache-Control","no-cache")
        self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)

    def do_GET(self):
        p=urlparse(self.path); q=parse_qs(p.query)
        if p.path=="/": self._json({"msg":"ok"})
        elif p.path=="/api/all": self._json(get_system_stats())
        elif p.path=="/api/tail":
            f=q.get("file",[None])[0]
            if f not in LOG_FILES: return self._json({"error":"bad file"},400)
            self._json(read_tail(LOG_FILES[f],int(q.get("cursor",[0])[0]),int(q.get("max_lines",[500])[0])))
        elif p.path=="/api/kill":
            try: os.kill(int(q.get("pid",[None])[0]),signal.SIGKILL); self._json({"ok":True})
            except Exception as e: self._json({"ok":False,"error":str(e)})
        elif p.path=="/health": self._json({"status":"ok"})
        else: self._json({"error":"not found"},404)

    def do_POST(self):
        if urlparse(self.path).path=="/api/terminal":
            l=int(self.headers.get("Content-Length",0))
            d=json.loads(self.rfile.read(l)) if l else {}
            term,c=d.get("term","wsl"),d.get("cmd","")
            if term=="powershell":
                r=subprocess.run(["powershell.exe","-NoProfile","-Command",c],capture_output=True,cwd="/mnt/c/Users/<YOUR_USERNAME>")
                ok,out,err=r.returncode==0,r.stdout.decode("utf-8","replace"),r.stderr.decode("utf-8","replace")
            elif term=="cmd":
                r=run_cmd(f'cmd.exe /c "chcp 65001 >nul && {c}"');ok,out,err=r["ok"],r["stdout"],r["stderr"]
            else:
                r=run_cmd(f'bash -c "{c}"');ok,out,err=r["ok"],r["stdout"],r["stderr"]
            self._json({"ok":ok,"stdout":out[-8000:],"stderr":err[-2000:]})
        else: self._json({"error":"not found"},404)

if __name__=="__main__":
    print(f"Serving on :{PORT}")
    http.server.HTTPServer((BIND,PORT),Handler).serve_forever()
