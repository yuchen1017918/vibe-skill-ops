# Custom MCP Server Fallback (国内网络 uvx/npx 超时应对)

当 `uvx`/`npx` 首次下载超时（国内无科学上网，PyPI/npm 极慢），**立即切换策略**：检查本地已有的 Python 库，自写 MCP 服务器。

## 三步决策流程

```
用户请求某 MCP 功能
  ├─ uvx <pkg> 能否在 60s 内启动？
  │   ├─ YES → 正常流程 (hermes config set → fix args → restart)
  │   └─ NO / TIMEOUT →
  │       ├─ pip3 list | grep -i <keyword>   # 检查本地已有库
  │       ├─ 有库？→ 自写 MCP (零下载)
  │       └─ 无库？→ pip3 install (通常比 uvx 快，因为不走 uv 缓存层)
  │           └─ 仍超时？→ 告知用户需手动安装
```

## 自写 MCP 服务器模式

### 1. 检查本地库

```bash
python3 -c "import <lib>; print(<lib>.__version__)" 2>&1
pip3 list 2>/dev/null | grep -iE "<keyword>"
```

### 2. 使用模板

从 `templates/mcp_server_template.py` 复制骨架，只改 TOOLS 字典和 handler 函数。

### 3. 测试（无需配置 Hermes）

用 `execute_code` + `subprocess` 直接测试 stdin/stdout 交互：

```python
import subprocess, json

proc = subprocess.Popen(
    ['python3', '/path/to/server.py'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
proc.stdin.write(json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize",...}) + "\n")
proc.stdin.write(json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/list",...}) + "\n")
proc.stdin.flush()
# ... read stdout
```

### 4. 配置 Hermes

```bash
hermes config set mcp_servers.<name>.command python3
hermes config set mcp_servers.<name>.args '["/path/to/server.py"]'
# 然后 fix args 格式 (Python yaml)
```

## 真实案例：PDF 解析

### 问题
用户要求下载安装 PDF 解析 MCP。尝试了：
- `uvx --from "mcp-pdf" mcp-pdf` → 超时 60s
- `uvx pdf-tools-mcp` → 超时 120s
- `npx -y @mcpcn/mcp-pdf-reader` → 无输出（下载慢）

### 发现
`pip3 list | grep pymupdf` → **pymupdf 1.28.0 已安装！**

### 方案
用 `templates/mcp_server_template.py` 模板，基于 pymupdf 自写 MCP 服务器，7 个工具：

| 工具 | pymupdf API |
|------|------------|
| `read_pdf_text` | `page.get_text("text")` |
| `get_pdf_info` | `doc.metadata`, `doc.page_count` |
| `extract_pdf_tables` | `page.find_tables()` |
| `extract_pdf_images` | `page.get_images(full=True)` |
| `search_pdf` | `page.search_for(query)` |
| `get_pdf_toc` | `doc.get_toc()` |
| `convert_page_to_image` | `page.get_pixmap(matrix=...)` |

### 结果
- 零网络下载，秒级完成
- 功能覆盖：文本提取、元信息、表格、图片、搜索、目录、页面转图片
- 配置完成后立即可用（需重启 Hermes）

## 常见可用库速查

| 需求 | 本地可能已有 | 检查命令 |
|------|------------|---------|
| PDF | `pymupdf` (fitz), `pdfplumber`, `PyPDF2` | `pip3 list \| grep -iE "mupdf\|pdf"` |
| 图片 | `PIL` (Pillow), `opencv-python` | `pip3 list \| grep -iE "pillow\|cv2"` |
| Excel | `openpyxl`, `pandas`, `xlrd` | `pip3 list \| grep -iE "openpyxl\|pandas\|xlrd"` |
| Word | `python-docx` | `pip3 list \| grep docx` |
| 网络 | `requests`, `httpx`, `aiohttp` | `pip3 list \| grep -iE "requests\|httpx\|aiohttp"` |
| 数据库 | `sqlite3` (stdlib), `psycopg2`, `pymysql` | `python3 -c "import sqlite3"` |
