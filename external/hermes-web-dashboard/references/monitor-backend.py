#!/usr/bin/env python3
"""Hermes 进程硬件监控后端 — psutil 必需"""
import http.server, json, os, signal, subprocess, threading, time
from pathlib import Path
from urllib.parse import urlparse
import psutil

PORT = int(os.environ.get("MONITOR_PORT", "8900"))
BIND = os.environ.get("MONITOR_BIND", "0.0.0.0")
HERE = Path(__file__).parent.resolve()
FAVICON_FILE = HERE / "图标.ico"

HERMES_PATTERNS = ["hermes", "bootstrap.py", "hermes-webui", "hermes-log-server", "hermes-monitor"]

def find_hermes_processes():
    procs = []
    for p in psutil.process_iter(["pid","name","cmdline","cpu_percent","memory_percent","memory_info","create_time","status"]):
        try:
            info = p.info
            cmdline = " ".join(info.get("cmdline") or [])
            if not any(pat.lower() in (info.get("name","")+" "+cmdline).lower() for pat in HERMES_PATTERNS):
                continue
            mem = info.get("memory_info")
            procs.append({
                "pid": info["pid"], "name": info["name"], "cmdline": cmdline[:200],
                "cpu_percent": round(info.get("cpu_percent") or 0, 1),
                "mem_percent": round(info.get("memory_percent") or 0, 1),
                "mem_rss_mb": round(mem.rss/1024/1024, 1) if mem else 0,
                "mem_vms_mb": round(mem.vms/1024/1024, 1) if mem else 0,
                "status": info.get("status","?"), "create_time": info.get("create_time", 0),
                "running_seconds": round(time.time()-(info.get("create_time") or time.time()), 0),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(procs, key=lambda x: x["cpu_percent"], reverse=True)

def get_system_stats():
    cpu_pct = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu": {"percent": round(cpu_pct,1), "count": psutil.cpu_count()},
        "memory": {"total_gb": round(mem.total/1024**3,1), "used_gb": round(mem.used/1024**3,1),
                   "percent": round(mem.percent,1), "available_gb": round(mem.available/1024**3,1),
                   "swap_percent": round(swap.percent,1)},
        "disk": {"total_gb": round(disk.total/1024**3,1), "used_gb": round(disk.used/1024**3,1),
                 "percent": round(disk.percent,1)},
        "uptime_seconds": round(time.time()-psutil.boot_time(),0),
    }

# API routes: GET /api/all → {stats, processes}, POST /api/kill → {"pid":N},
#              POST /api/run → {"cmdline":"..."}
# Handler 类参考 hermes-web-dashboard SKILL.md 模板
