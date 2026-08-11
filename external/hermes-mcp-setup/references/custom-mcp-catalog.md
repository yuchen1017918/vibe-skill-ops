# Custom Python MCP Server Catalog

Six zero-dependency, pure-Python-stdlib MCP servers proven working in Hermes.
Each implements the MCP JSON-RPC protocol directly (no `mcp` SDK needed),
making them immune to `uvx`/`npx` network issues and SDK version conflicts.

All files live at `~/workspace/*_mcp.py` and are configured in `config.yaml` as:
```yaml
mcp_servers:
  <name>:
    command: python3
    args:
    - /home/yuchen_wang/workspace/<file>.py
    timeout: 10
```

## 1. calculator_mcp.py — Math + Unit Conversion (2 tools)

- `calc(expression)` — Safe eval with math functions: sqrt, sin, cos, tan, log, abs, round, ceil, floor, pi, e, pow
- `unit_convert(value, from_unit, to_unit)` — Length (km/m/cm/mm/mi/ft/in), weight (kg/g/lb/oz), temp (C/F/K), data (B/KB/MB/GB/TB)

## 2. translate_mcp.py — Translation + Language Detection (2 tools)

- `translate(text, target_lang, source_lang)` — Uses free MyMemory API. Supports zh/en/ja/ko/fr/de/es/ru/ar/pt/it. Falls back to built-in dictionary for common words.
- `detect_language(text)` — Unicode-based detection for CJK, Cyrillic, Arabic, Latin scripts.

## 3. hash_tools_mcp.py — Hash & Encoding Utilities (9 tools)

- `md5(text)` / `sha256(text)` / `sha1(text)` — Cryptographic hashes
- `base64_encode(text)` / `base64_decode(encoded)` — Base64
- `url_encode(text)` / `url_decode(encoded)` — URL encoding
- `uuid_gen()` — Random UUID v4
- `timestamp()` — Unix timestamp + UTC time

## 4. text_tools_mcp.py — Text Processing (7 tools)

- `word_count(text)` — Word/char/line counts
- `regex_search(text, pattern)` — Find all regex matches
- `regex_replace(text, pattern, replacement)` — Regex substitution
- `case_convert(text, mode)` — upper/lower/title/capitalize/snake/camel
- `diff_text(text1, text2)` — Unified diff
- `json_format(text)` — Format/validate JSON
- `text_stats(text)` — Unique words, average length, etc.

## 5. image_info_mcp.py — Image Metadata (2 tools)

- `image_info(path)` — Format, dimensions, file size for PNG/JPEG/GIF/BMP/WebP. Pure binary header parsing, no Pillow needed.
- `list_images(directory)` — List image files with sizes in a directory.

## 6. file_ops_mcp.py — File Operations (6 tools)

- `file_search(directory, pattern)` — Recursive glob search
- `file_stat(path)` — Size, type, permissions, timestamps
- `find_duplicates(directory, min_size)` — MD5-based duplicate detection
- `directory_tree(directory, max_depth)` — Tree view
- `file_head(path, lines)` — Read first N lines
- `disk_usage(directory)` — Total size + file count

## 7. mysql_mcp.py — MySQL Database Access (4 tools)

**Dependency**: `mysql-connector-python` (pip install mysql-connector-python)

- `mysql_query(query, host?, database?)` — Execute SQL SELECT query, returns JSON array
- `mysql_list_tables(database?)` — List tables with row counts via information_schema
- `mysql_describe_table(table, database?)` — Show column definitions (DESCRIBE)
- `mysql_show_databases()` — List all accessible databases

Config via env vars: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`

## 8. redis_mcp.py — Redis Cache/Queue/PubSub (6 tools)

**Dependency**: `redis` (pip install redis)

- `redis_get(key)` — Get value by key
- `redis_set(key, value, ttl?)` — Set key-value with optional TTL
- `redis_keys(pattern?)` — List keys matching glob pattern
- `redis_delete(keys)` — Delete keys by list
- `redis_info(section?)` — Server info (memory/clients/stats)
- `redis_publish(channel, message)` — Publish to channel

Config via env vars: `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`

## 9. rss_reader_mcp.py — RSS/Atom Feed Reader (3 tools)

**Dependency**: `feedparser` (pip install feedparser, pure Python)

- `rss_read(url, limit?)` — Parse feed, return title/entries/link/summary/date
- `rss_search(url, keyword, limit?)` — Case-insensitive search in titles and summaries
- `rss_list_feeds(urls, per_feed?)` — Parse multiple feeds, return latest entries from each

## 10. docker_mcp.py — Docker Container Management (6 tools)

**Dependency**: Docker CLI in PATH (`docker` or `docker.exe` for WSL)

- `docker_ps(all?)` — List running (or all) containers with name/image/status/ports
- `docker_images()` — List images with size and creation date
- `docker_logs(container, tail?)` — Get container logs
- `docker_start(container)` — Start a stopped container
- `docker_stop(container)` — Stop a running container
- `docker_stats(container?)` — CPU/memory/network usage snapshot

**⚠️ Critical pitfall**: Do NOT call `subprocess.run()` at module import time to detect the Docker command. Docker daemon may be stopped or slow, causing the MCP server to hang silently on startup. Use **lazy detection** — only probe for `docker`/`docker.exe` inside the handler function on first call, with try/except FileNotFoundError fallback:

```python
def docker(args):
    """Run docker with auto-detection on first call."""
    for cmd in ["docker", "docker.exe"]:
        try:
            r = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                raise Exception(r.stderr.strip())
            return r.stdout.strip()
        except FileNotFoundError:
            continue
    raise Exception("Docker not found. Is Docker Desktop running?")
```

## 11. playwright_mcp.py — Headless Browser Automation (5 tools)

**Dependency**: `playwright` (pip install playwright, then `playwright install chromium`)

- `playwright_navigate(url, wait_until?)` — Navigate to URL, return title + text preview
- `playwright_extract(selector?, strip?)` — Extract text content with optional CSS selector
- `playwright_screenshot(path?, full_page?)` — Full-page screenshot to file
- `playwright_click(selector, by_text?)` — Click element by CSS selector or text
- `playwright_fill(selector, value)` — Fill input field

**Note**: Browser is launched lazily (`sync_playwright().start()` on first tool call) to avoid startup overhead at MCP server initialization.

## MCP JSON-RPC Protocol (for extending)

The core loop that all these servers use (stdlib only, no FastMCP):

```python
for line in sys.stdin:
    req = json.loads(line)
    method, rid = req.get("method"), req.get("id")
    
    if method == "initialize":
        # Return capabilities
        print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{
            "protocolVersion":"2024-11-05",
            "capabilities":{"tools":{}},
            "serverInfo":{"name":"my-mcp","version":"1.0"}
        }}), flush=True)
    
    elif method == "tools/list":
        # Return tool definitions with JSON Schema params
        tools = [{"name": name, "description": desc,
                   "inputSchema": {"type":"object","properties": {...}}}
                 for name, (desc, params, handler) in TOOLS.items()]
        print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{"tools":tools}}), flush=True)
    
    elif method == "tools/call":
        # Execute tool and return result
        name = req["params"]["name"]
        args = req["params"].get("arguments", {})
        result = TOOLS[name]["handler"](**args)
        print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{
            "content":[{"type":"text","text":str(result)}]
        }}), flush=True)
    
    elif method == "notifications/initialized":
        pass  # No response needed
    
    sys.stdout.flush()
```

### Critical: JSON Schema types

Use `"string"`, `"number"`, `"integer"`, `"boolean"`, `"object"`, `"array"` — NOT `"float"` or `"int"`. DeepSeek and other strict providers reject `"float"`/`"int"` with HTTP 400.
