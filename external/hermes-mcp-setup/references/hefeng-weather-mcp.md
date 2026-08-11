# 和风天气 MCP Server 配置

## 关键教训

### ❌ 不要用魔搭 (ModelScope) MCP 托管
和风天气的 API Key 是直接的和风凭据，不是魔搭 MCP 项目。直接走和风原生 API。

### ❌ 不要用公共 API 端点
`devapi.qweather.com`、`api.qweather.com` 返回 "Invalid Host" 403。
和风从 2026 年起要求每个帐号使用**专属 API Host**。

### ✅ API Host 在哪里找
**不在项目页面**！去：https://console.qweather.com/setting
格式：`xxx.yyy.qweatherapi.com`（如 `ma6fr9h7hd.re.qweatherapi.com`）

### ❌ npm 包不可靠
`hefeng-mcp-weather` (npm) 能启动但 API Host 配置有问题。
`hefeng-mcp-server` (npm) API 也不通。
→ **自己写 Python MCP server 最可靠**。

### ❌ 城市查询 API 可能不可用
和风免费/基础订阅可能不包含 `/v2/city/lookup`（城市名→LocationID）。
→ **内置城市 ID 映射表**是最实用的方案。覆盖 43 个主要城市，支持中文名、拼音、经纬度、LocationID。

## 可用的 npm MCP 包（备选）
- `hefeng-mcp-weather` — GitHub: shanggqm/hefeng-mcp-weather，支持 `--apiKey` 和 `--apiUrl`
- `hefeng-mcp-server` — npmx.dev，同样参数
- `hefeng-weather-mcp` — PyPI v0.3.0
- `qweather-mcp-server` — PyPI，需要 JWT 认证（非简单 API Key）

## 最终配置 (config.yaml)
```yaml
mcp_servers:
  hefeng-weather:
    command: python3
    args:
    - /home/yuchen_wang/workspace/hefeng_weather_mcp.py
    env:
      HEFENG_API_KEY: ef7755...
      HEFENG_API_HOST: ma6fr9h7hd.re.qweatherapi.com
    timeout: 30
```

## 可用工具
| 工具 | 功能 | 参数 |
|------|------|------|
| `get_weather` | 实时天气 + 3/7/15天预报 | location, forecast_days |
| `get_air_quality` | 空气质量 AQI | location |
| `get_city_id` | 城市名→LocationID | location |
