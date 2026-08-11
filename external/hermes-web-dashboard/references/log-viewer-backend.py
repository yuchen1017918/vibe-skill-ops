#!/usr/bin/env python3
"""双面板日志查看器后端 — 纯标准库，零外部依赖"""
import http.server, json, os, time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("LOG_VIEWER_PORT", "8899"))
BIND = os.environ.get("LOG_VIEWER_BIND", "0.0.0.0")
HERE = Path(__file__).parent.resolve()
HTML_FILE = HERE / "index.html"
FAVICON_FILE = HERE / "图标.ico"

LOG_FILES = {
    "gateway": Path.home() / ".hermes" / "logs" / "gateway.log",
    "web": Path.home() / ".hermes" / "webui" / "bootstrap-8787.log",
}

def read_tail(filepath, cursor, max_lines):
    if not filepath.exists():
        return {"lines": [], "next_cursor": 0, "error": f"文件不存在: {filepath}"}
    try:
        stat = filepath.stat()
        if cursor > stat.st_size:
            cursor = 0
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            new_cursor = stat.st_size
            if cursor == 0:
                # 反向读取最后 max_lines 行（高效，适合大文件）
                chunk_size, blocks, remaining = 4096, [], max_lines + 1
                pos = stat.st_size
                while pos > 0 and remaining > 0:
                    read_size = min(chunk_size, pos)
                    pos -= read_size; f.seek(pos)
                    chunk = f.read(read_size)
                    blocks.append(chunk)
                    remaining -= chunk.count("\n")
                tail = "".join(reversed(blocks))
                lines = [l for l in tail.split("\n") if l][-max_lines:]
            else:
                f.seek(cursor)
                if cursor != 0:
                    f.readline()
                lines = [l.rstrip("\n\r") for l in f if l.rstrip("\n\r")]
                new_cursor = f.tell()
        return {"lines": lines, "next_cursor": new_cursor, "file_size": stat.st_size, "error": None}
    except Exception as e:
        return {"lines": [], "next_cursor": cursor, "error": str(e)}

# Handler 类参考 hermes-web-dashboard SKILL.md 模板
