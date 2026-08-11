# WSL Sessions: MCP Server Setup Summary (2026-07-21)

## Session 1: Time Server (First MCP)

### Commands
```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d_%H%M%S)
pip install mcp
hermes config set mcp_servers.time.command uvx
hermes config set mcp_servers.time.args '["mcp-server-time"]'
# Fix args with Python yaml.dump
```

### Result
- 2 tools: get_current_time, convert_time
- ✅ CLI works. WebUI session didn't get tools injected.

## Session 2: SQLite + Filesystem + Time (Full Setup)

### Final config
```yaml
mcp_servers:
  time:
    command: uvx
    args:
    - mcp-server-time
  sqlite:
    command: uvx
    args:
    - mcp-server-sqlite
    - --db-path
    - /home/yuchen_wang/workspace/test.db
  filesystem:
    command: npx
    args:
    - -y
    - '@modelcontextprotocol/server-filesystem'
    - /home/yuchen_wang/workspace
```

### SQLite (6 tools)
- Works immediately with `uvx`, no heavy downloads
- Tools: read_query, write_query, create_table, list_tables, describe_table, append_insight
- **Definitive test**: `hermes chat -q "创建students表，插入3条数据，查询分数>80" --yolo`
- Verification: `sqlite3 test.db "SELECT * FROM students"` confirmed data

### Filesystem (14 tools)
- First run slow (~60s) due to npx downloading Node packages
- Tools include: move_file, directory_tree, create_directory, get_file_info, list_allowed_directories
- Allows specifying which directories the server can access

### Key Learnings
1. **args format bug**: `hermes config set` stores args as JSON string, must fix with Python yaml.dump
2. **Full restart required**: MCP tools discovered at process startup, not /reset
3. **Uniquely-MCP tasks are the best verification**: SQLite queries prove MCP is working because built-in tools can't do SQL
4. **Model may prefer built-in tools**: Agent used `date` instead of `mcp_time_get_current_time` for simple time queries
5. **Community skills need clawhub/ prefix**: `hermes skills install clawhub/<name>`
6. **Security scanner blocks dangerous patterns**: curl|sh, echo|exec blocked permanently even with --force
