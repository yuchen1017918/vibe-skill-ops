# 和风天气 MCP 配置指南

## 概述

和风天气（QWeather）是中国气象数据服务商。通过 MCP Server 可以在 Hermes 中查询实时天气、逐时/逐日预报。

## 前置条件

1. 注册和风天气账号：https://id.qweather.com/#/register
2. 在控制台创建项目：https://console.qweather.com
3. 创建凭据（API KEY 类型）：项目 → 凭据 → 添加 API KEY 凭据
4. 订阅所需的 API 产品（免费订阅即可满足基本需求）

## 关键信息收集

从和风控制台收集以下 3 项：

| 信息 | 位置 | 示例 |
|------|------|------|
| **API Key** | 项目 → 凭据 → 点击凭据详情 | `ef77558053fe4c669d9a934a95aad840` |
| **API Host** | 项目 → 设置 → API Host | `https://abc123.qweatherapi.com` |
| **Project ID** | 项目列表 | `3BKUHFHUTW` |

⚠️ **API Host 是最容易忽略的**：和风不是用统一的 `devapi.qweather.com`，而是每个项目分配独立 Host。

## Hermes 配置

### 推荐包：`hefeng-mcp-server`

支持 `--apiUrl` 参数传入项目专属 API Host：

```yaml
mcp_servers:
  hefeng-weather:
    command: npx
    args:
      - -y
      - hefeng-mcp-server@latest
      - --apiKey=<你的API Key>
      - --apiUrl=<你的API Host>
    timeout: 30
```

### 不推荐：`hefeng-mcp-weather`

该包**不支持** `--apiUrl` 参数，会导致 403 "Invalid Host" 错误。

## 配置命令

```bash
# 备份
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d_%H%M%S)

# Python 写入（避免 hermes config set 的 args 格式问题）
python3 -c "
import yaml
with open('/home/yuchen_wang/.hermes/config.yaml') as f:
    c = yaml.safe_load(f)
c['mcp_servers']['hefeng-weather'] = {
    'command': 'npx',
    'args': [
        '-y',
        'hefeng-mcp-server@latest',
        '--apiKey=<KEY>',
        '--apiUrl=<HOST>'
    ],
    'timeout': 30
}
with open('/home/yuchen_wang/.hermes/config.yaml', 'w') as f:
    yaml.dump(c, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print('Done')
"
```

## 验证测试

### 1. 直接测试 API（隔离 MCP 层）

```bash
# 如果正确，返回 JSON 天气数据
curl -s --compressed \
  "https://<你的API Host去掉https://>/v7/weather/now?location=101010100&key=<API Key>" \
  | python3 -m json.tool
```

如果返回 `{"error":{"title":"Invalid Host"}}` → API Host 错误或 Key 未绑定此 Host。

### 2. 测试 MCP Server

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test():
    params = StdioServerParameters(
        command='npx',
        args=['-y', 'hefeng-mcp-server@latest',
              '--apiKey=<KEY>', '--apiUrl=<HOST>']
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f'Tools: {[t.name for t in tools.tools]}')
            
            result = await session.call_tool('get-weather', {
                'location': '北京',
                'type': 'now'
            })
            print(result.content[0].text)

asyncio.run(test())
```

### 3. 重启 Hermes 后测试

```bash
hermes chat -q "北京现在天气怎么样？" --yolo
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `403 Invalid Host` | 用了公共端点而非项目专属 Host | 去控制台复制项目 API Host |
| `403 UNAUTHORIZED` | API Key 错误或未绑定到项目 | 检查凭据是否正确创建并绑定 |
| `404 record not found` | 在魔搭上搜了和风项目的 Project ID | 这是原生 API 不是魔搭 MCP，用 npx 方式配 |
| MCP tools 被发现但调用失败 | API 层问题（Key/Host） | 先用 curl 直接测试 API |

## 可用工具

`hefeng-mcp-server` 提供：

- `get-weather` — 获取天气预报
  - `location`: 城市名、经纬度 或 Location ID
  - `type`: `now`（实时）/ `hourly`（逐时）/ `daily`（逐日）
  - 支持逐时：24h / 72h / 168h
  - 支持逐日：3d / 7d / 10d / 15d / 30d
