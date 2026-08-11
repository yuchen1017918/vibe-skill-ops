---
name: china-mcp-services
description: "配置中国国内可用的 MCP 服务：和风天气、高德地图、魔搭托管。覆盖 API Host 发现、城市映射、国内网络限制等常见陷阱。"
version: 1.0.0
tags: [mcp, china, weather, geocoding, amap, hefeng, modelscope, 国内]
---

# 中国 MCP 服务配置

国内网络环境（无科学上网）下配置天气、地理编码、搜索等 MCP 服务。覆盖和风天气、高德地图两个主流服务，以及魔搭（ModelScope）托管的通用 MCP。

## 何时使用

- 配置天气 MCP（和风天气）
- 配置定位/地理编码 MCP（高德地图）
- 在国内环境下排查 MCP 连通性问题
- 用户提供了 API Key 但不知道如何填入 Hermes config

## 和风天气 MCP

### API Host 是关键

和风天气不使用统一域名（`devapi.qweather.com` / `api.qweather.com`），每个开发者有独立的 API Host：

**获取路径**：https://console.qweather.com/setting → 查看 API Host

格式如：`ma6fr9h7hd.re.qweatherapi.com`

> ⚠️ 公共地址（devapi.qweather.com 等）2026 年起逐步停用，必须用专属 Host。

### 认证方式

和风支持两种认证：
1. **API KEY**（简单）：URL 参数 `?key=xxx`，适合 MCP
2. **JWT**（安全）：Bearer token，需要公私钥对

MCP 场景用 API KEY 即可。

### 城市查询的坑

和风的 `/v2/city/lookup` 端点在很多订阅计划中不可用（返回 404）。解决方案：

- **内置城市 ID 映射**：MCP 服务器自带 40+ 中国城市的 LocationID 映射表
- **支持经纬度**：直接传 `lat,lon` 格式
- **支持 LocationID**：如 `101010100`（北京）

### 配置示例

```yaml
mcp_servers:
  hefeng-weather:
    command: python3
    args:
      - /path/to/hefeng_weather_mcp.py
    env:
      HEFENG_API_KEY: ef7755...
      HEFENG_API_HOST: ma6fr9h7hd.re.qweatherapi.com
    timeout: 30
```

### 可用工具

| 工具 | 功能 | 参数 |
|------|------|------|
| `get_weather` | 实时天气 + 预报 | location, forecast_days=now/3d/7d/15d |
| `get_air_quality` | 空气质量 AQI | location |
| `get_city_id` | 城市名→ID | location |

## 高德地图 MCP（定位/地理编码）

### 获取 API Key

1. 注册 https://lbs.amap.com/
2. 控制台 → 应用管理 → 创建应用
3. 添加 Key，服务平台选「Web 服务」
4. 个人开发者免费，5000次/天

### 配置方式

**方式一：高德官方 SSE MCP**
```yaml
mcp_servers:
  amap:
    url: https://mcp.amap.com/sse?key=你的高德Key
```

**方式二：自写 Python MCP + REST API**（更可控）
```yaml
mcp_servers:
  amap-geo:
    command: python3
    args: [/path/to/amap_geo_mcp.py]
    env:
      AMAP_API_KEY: xxx
    timeout: 15
```

### 核心功能

| 工具 | API | 说明 |
|------|-----|------|
| `maps_geo` | `/v3/geocode/geo` | 地址→经纬度 |
| `maps_regeocode` | `/v3/geocode/regeo` | 经纬度→地址（国家/省/市/区/街道） |
| `maps_ip_location` | `/v3/ip` | IP→省/市 |
| `maps_weather` | `/v3/weather/weatherInfo` | 天气查询 |
| `maps_search` | `/v3/place/text` | POI 关键词搜索 |

## 魔搭（ModelScope）MCP

### URL 格式

```
https://mcp.api-inference.modelscope.net/{服务ID}/mcp
```

服务 ID 是小写 hex 字符串（如 `557312d3729940`），不是项目名称。

### 现有可用魔搭 MCP

| 服务 | ID | 用途 |
|------|-----|------|
| fetch | `557312d3729940` | 网页抓取 |
| bing-cn | `785aa53b3e6448` | 必应搜索（国内版） |
| MiniMax | `e661dec931e44d` | MiniMax AI |
| edgeone | `6616803de9634c` | EdgeOne Pages |

### 添加新魔搭 MCP

```bash
hermes config set mcp_servers.<name>.url "https://mcp.api-inference.modelscope.net/<ID>/mcp"
hermes config set mcp_servers.<name>.timeout 30
```

## 国内网络注意事项

### 不可用的服务

| 服务 | 原因 |
|------|------|
| Nominatim (OpenStreetMap) | 被墙，超时 |
| Google Maps | 被墙 |
| 大部分 `api.openai.com` | 被墙 |

### 可用替代

| 需求 | 国际方案（不可用） | 国内替代 |
|------|-------------------|---------|
| 天气 | Open-Meteo | **和风天气** |
| 地理编码 | Nominatim | **高德地图** |
| 搜索 | Google Search | **Tavily** 或 **必应国内版**（魔搭） |
| AI 模型 | OpenAI/Anthropic | **DeepSeek** / **GLM** |

## MCP 配置通用坑

### args 必须是 list 不是 string

`hermes config set` 会把 args 存成 YAML string，MCP 客户端无法解析。用 Python 修复：

```python
import yaml
with open('/home/yuchen_wang/.hermes/config.yaml') as f:
    c = yaml.safe_load(f)
c['mcp_servers']['name']['args'] = ['arg1', 'arg2']  # 确保是 list
with open('/home/yuchen_wang/.hermes/config.yaml', 'w') as f:
    yaml.dump(c, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
```

### HTTP MCP 传认证

```yaml
mcp_servers:
  my-service:
    url: https://xxx/mcp
    headers:
      Authorization: Bearer sk-xxx
      X-API-Key: xxx
    timeout: 30
```

### 重启要求

MCP 服务器在 **Hermes 进程启动时** 发现。`/reset` 不够，需要完全重启进程（WebUI bootstrap.py 或 CLI 进程）。

### 验证三步曲

```bash
# 1. 直接测试 API
curl -s --compressed "https://xxx/v7/weather/now?location=101010100&key=xxx"

# 2. 验证配置
grep -A5 "mcp_server_name:" ~/.hermes/config.yaml

# 3. 重启后用 CLI 测试
hermes chat -q "查北京天气" --yolo
```

## 参考文件

- `references/hefeng-setup-session.md` — 和风天气 MCP 配置的完整回放
- `templates/hefeng_weather_mcp.py` — 和风天气 Python MCP 服务器模板
