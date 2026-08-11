# AutoDL MCP Server Setup

## Source

https://github.com/ygh11231/autodl-mcp-server

## Tools (20 total)

- Instance: list, get, stop, start, delete, set_replicas
- Container: list, stop, get_events
- GPU: get_gpu_stock, list_images, get_regions
- SSH: connect, disconnect, run_command, upload_file, download_file, check_gpu, check_logs, list_connections

## Hermes Config

```yaml
mcp_servers:
  autodl:
    command: python3
    args:
    - /home/yuchen_wang/workspace/autodl-mcp-server/server.py
    env:
      AUTODL_API_TOKEN: "eyJh..."
```

Command to set:

```bash
hermes config set mcp_servers.autodl.command python3
hermes config set mcp_servers.autodl.args '["/path/to/server.py"]'
hermes config set mcp_servers.autodl.env.AUTODL_API_TOKEN "<token>"
```

Then fix args format (Step 3 in hermes-mcp-setup SKILL.md).

## MCP SDK Requirement

**Must use MCP 1.x** (NOT 2.0.0). The server uses `@app.list_tools()` which was removed in 2.x.

```bash
pip install "mcp>=1.0,<2.0"
```

## Token

Get from [AutoDL 控制台](https://www.autodl.com) → 设置 → 开发者 Token.
Token is a JWT with `aud: "develop_api"`. **Sent as raw token — no "Bearer" prefix.**

Token expiration: "登录超时，请重新登录" = expired, get a fresh one.
Permission issue: "无当前资源访问权限" = account has no API deployments yet. GPU stock queries still work.

Verify token (GPU stock — always works if token valid):

```bash
# Token is sent WITHOUT "Bearer " prefix — raw JWT in Authorization header
curl -s --max-time 10 -X POST "https://api.autodl.com/api/v1/dev/machine/region/gpu_stock" \
  -H "Authorization: <raw_token_here>" \
  -H "Content-Type: application/json" \
  -d '{"region_sign":"westDC2","cuda_v_from":117,"cuda_v_to":128}'
# Returns "code": "Success" with GPU inventory if token OK

# Deployments list (only works if account has API deployments):
curl -s --max-time 10 "https://api.autodl.com/api/v1/dev/deployment/list" \
  -H "Authorization: <raw_token_here>" \
  -H "Content-Type: application/json"
```

## Verification

```bash
cd /path/to/autodl-mcp-server
python3 -c "
import asyncio, os
os.environ['AUTODL_API_TOKEN'] = '<token>'
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command='python3', args=['server.py'], env=os.environ)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f'{len(tools.tools)} tools loaded')
            result = await session.call_tool('autodl_list_instances', {})
            print(result.content[0].text[:200])

asyncio.run(main())
"
```

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `AuthorizeFailed` / `登录超时` | Token expired | Get new token from AutoDL 控制台 → 开发者 Token |
| `BadRequest: 无当前资源访问权限` | Account has no API deployments | Normal for new accounts — GPU stock queries still work. Create a deployment via API or web console first. |
| `Connection closed` during initialize | MCP 2.0 installed | `pip install "mcp>=1.0,<2.0"` |
| Git clone timeout | GitHub blocked | Use `ghproxy.com` mirror or `--depth 1` clone |
| Token format: use RAW token, NOT `Bearer` prefix | AutoDL API expects raw JWT in `Authorization` header | Send token directly: `Authorization: eyJh...` — not `Authorization: Bearer eyJh...` |
