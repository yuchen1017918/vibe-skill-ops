# 和风天气 MCP 配置回放

> 来源：2026-07-25 会话，用户 yuchen_wang 配置和风天气 MCP

## 原始输入

- 项目：天气MCP，ID `3BKUHFHUTW`
- 凭据：MCP天气工具专用KEY，ID `CNPKF7AX9E`
- API Key：`ef77558053fe4c669d9a934a95aad840`

## 关键发现

### 1. 不是魔搭 MCP

用户最初以为 `3BKUHFHUTW` 是魔搭 MCP 服务 ID，导致走了弯路。
魔搭 MCP ID 均为**小写 hex**（如 `557312d3729940`），`3BKUHFHUTW` 是和风项目 ID，不能直接用于魔搭。

### 2. API Host 才是关键

和风 API Host 在 **https://console.qweather.com/setting**，不是项目页面。
该用户的 API Host：`ma6fr9h7hd.re.qweatherapi.com`

### 3. 公共端点 403

`devapi.qweather.com` 和 `api.qweather.com` 返回 "Invalid Host" 403。
正确方式：**专属 Host + API Key**。

### 4. 城市查询不可用

`/v2/city/lookup` 在该订阅计划中返回 404。
解决：内置城市 ID 映射表，支持中文名/拼音/经纬度/LocationID。

## 最终配置

```yaml
mcp_servers:
  hefeng-weather:
    command: python3
    args:
      - /home/yuchen_wang/workspace/hefeng_weather_mcp.py
    env:
      HEFENG_API_KEY: ef77558053fe4c669d9a934a95aad840
      HEFENG_API_HOST: ma6fr9h7hd.re.qweatherapi.com
    timeout: 30
```

## 验证结果

```
hermes chat -q "用和风天气查一下深圳今天天气" --yolo
→ 深圳：阴天 33°C（体感37°C），成功 ✓
```

## 排查过程

1. 尝试 HTTP MCP → 魔搭 ID `3BKUHFHUTW` → 404
2. 尝试 public API host → 403 "Invalid Host"
3. 用户去 console.qweather.com/setting → 找到专属 Host
4. curl 直接测试 → 200 OK（北京 28°C 雾）
5. 尝试 npm MCP (`hefeng-mcp-weather`) → 403（包可能不使用 apiUrl）
6. 自写 Python MCP → 城市查询 404 → 加内置映射 → 成功
7. Hermes CLI 端到端测试 → ✅

## 高德地图 MCP（未完成，待用户获取 API Key）

高德地图 MCP 是定位/地理编码的最佳方案：
- 需注册 https://lbs.amap.com/ 获取 Web 服务 Key
- 官方 SSE MCP：`https://mcp.amap.com/sse?key=KEY`
- 功能：地理编码、逆地理编码、IP定位、POI搜索、路径规划、天气

Nominatim (OpenStreetMap) 在国内被墙，不可用。
