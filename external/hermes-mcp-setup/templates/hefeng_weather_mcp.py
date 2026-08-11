#!/usr/bin/env python3
"""和风天气 MCP Server — 精简、可靠
用法: 在 Hermes config.yaml 中配置为 stdio MCP server
  mcp_servers:
    hefeng-weather:
      command: python3
      args: [path/to/this/file]
      env:
        HEFENG_API_KEY: your_key
        HEFENG_API_HOST: your_host.qweatherapi.com
      timeout: 30
"""

import json, sys, os
import urllib.request, urllib.parse

API_KEY = os.environ.get("HEFENG_API_KEY", "")
API_HOST = os.environ.get("HEFENG_API_HOST", "ma6fr9h7hd.re.qweatherapi.com")

# 常用中国城市 LocationID 映射 — 可根据需要扩展
CITY_IDS = {
    "北京": "101010100", "北京市": "101010100", "beijing": "101010100",
    "上海": "101020100", "上海市": "101020100", "shanghai": "101020100",
    "广州": "101280101", "广州市": "101280101", "guangzhou": "101280101",
    "深圳": "101280601", "深圳市": "101280601", "shenzhen": "101280601",
    "杭州": "101210101", "杭州市": "101210101", "hangzhou": "101210101",
    "成都": "101270101", "成都市": "101270101", "chengdu": "101270101",
    "武汉": "101200101", "武汉市": "101200101", "wuhan": "101200101",
    "南京": "101190101", "南京市": "101190101", "nanjing": "101190101",
    "重庆": "101040100", "重庆市": "101040100", "chongqing": "101040100",
    "天津": "101030100", "天津市": "101030100", "tianjin": "101030100",
    "苏州": "101190401", "苏州市": "101190401", "suzhou": "101190401",
    "西安": "101110101", "西安市": "101110101", "xian": "101110101",
    "长沙": "101250101", "长沙市": "101250101", "changsha": "101250101",
    "青岛": "101120201", "青岛市": "101120201", "qingdao": "101120201",
    "郑州": "101180101", "郑州市": "101180101", "zhengzhou": "101180101",
    "大连": "101070201", "大连市": "101070201", "dalian": "101070201",
    "厦门": "101230201", "厦门市": "101230201", "xiamen": "101230201",
    "宁波": "101210401", "宁波市": "101210401", "ningbo": "101210401",
    "无锡": "101190201", "无锡市": "101190201", "wuxi": "101190201",
    "合肥": "101220101", "合肥市": "101220101", "hefei": "101220101",
    "福州": "101230101", "福州市": "101230101", "fuzhou": "101230101",
    "济南": "101120101", "济南市": "101120101", "jinan": "101120101",
    "昆明": "101290101", "昆明市": "101290101", "kunming": "101290101",
    "贵阳": "101260101", "贵阳市": "101260101", "guiyang": "101260101",
    "南宁": "101300101", "南宁市": "101300101", "nanning": "101300101",
    "海口": "101310101", "海口市": "101310101", "haikou": "101310101",
    "三亚": "101310201", "三亚市": "101310201", "sanya": "101310201",
    "哈尔滨": "101050101", "哈尔滨市": "101050101", "haerbin": "101050101",
    "长春": "101060101", "长春市": "101060101", "changchun": "101060101",
    "沈阳": "101070101", "沈阳市": "101070101", "shenyang": "101070101",
    "石家庄": "101090101", "石家庄市": "101090101", "shijiazhuang": "101090101",
    "太原": "101100101", "太原市": "101100101", "taiyuan": "101100101",
    "兰州": "101160101", "兰州市": "101160101", "lanzhou": "101160101",
    "乌鲁木齐": "101130101", "乌鲁木齐市": "101130101", "wulumuqi": "101130101",
    "拉萨": "101140101", "拉萨市": "101140101", "lasa": "101140101",
    "呼和浩特": "101080101", "呼和浩特市": "101080101", "huhehaote": "101080101",
    "银川": "101170101", "银川市": "101170101", "yinchuan": "101170101",
    "西宁": "101150101", "西宁市": "101150101", "xining": "101150101",
    "南昌": "101240101", "南昌市": "101240101", "nanchang": "101240101",
    "香港": "101320101", "hongkong": "101320101",
    "澳门": "101330101", "macau": "101330101",
    "台北": "101340101", "taipei": "101340101",
}

def resolve_location(location: str) -> str:
    """解析城市名为LocationID或坐标"""
    if location in CITY_IDS:
        return CITY_IDS[location]
    for name, lid in CITY_IDS.items():
        if name in location or location in name:
            return lid
    if "," in location:
        return location
    if location.replace(".","").isdigit():
        return location
    return "101010100"

def call_api(path, params=None):
    params = params or {}
    params["key"] = API_KEY
    url = f"https://{API_HOST}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("Accept-Encoding", "gzip")
    with urllib.request.urlopen(req, timeout=15) as resp:
        import gzip
        data = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return json.loads(data)

def get_weather(location: str, forecast_days: str = "now"):
    """查询天气：location=城市名/经纬度/LocationID，forecast_days=now|3d|7d|15d"""
    loc_id = resolve_location(location)
    city_hint = f"{location}({loc_id})" if location not in (loc_id, "101010100") else location

    if forecast_days == "now":
        data = call_api("/v7/weather/now", {"location": loc_id})
        if data.get("code") != "200":
            return f"查询失败: {data}"
        n = data["now"]
        return (f"📍 {city_hint}\n"
                f"🌡️ 温度: {n['temp']}°C (体感 {n['feelsLike']}°C)\n"
                f"🌤️ 天气: {n['text']}\n"
                f"💨 {n['windDir']} {n['windScale']}级 ({n['windSpeed']}km/h)\n"
                f"💧 湿度: {n['humidity']}%\n"
                f"👁️ 能见度: {n['vis']}km\n"
                f"☁️ 云量: {n['cloud']}%\n"
                f"🕐 更新: {n['obsTime']}")
    else:
        data = call_api(f"/v7/weather/{forecast_days}", {"location": loc_id})
        if data.get("code") != "200":
            return f"查询失败: {data}"
        lines = [f"📍 {city_hint} — {forecast_days}预报:"]
        for d in data.get("daily", []):
            lines.append(f"  {d['fxDate']} | {d['textDay']}/{d['textNight']} | "
                        f"{d['tempMin']}~{d['tempMax']}°C | {d['windDirDay']}{d['windScaleDay']}级")
        return "\n".join(lines)

def get_city_id(location: str):
    """根据城市名获取LocationID"""
    loc_id = resolve_location(location)
    return f"{location} → LocationID: {loc_id}"

def get_air_quality(location: str):
    """查询空气质量AQI（需要订阅空气API）"""
    loc_id = resolve_location(location)
    data = call_api("/v7/air/now", {"location": loc_id})
    if data.get("code") != "200":
        return f"查询失败: {data}"
    a = data["now"]
    return (f"📍 {location} 空气质量\n"
            f"AQI: {a['aqi']} ({a['category']})\n"
            f"PM2.5: {a['pm2p5']} | PM10: {a['pm10']}\n"
            f"NO₂: {a['no2']} | SO₂: {a['so2']}\n"
            f"🕐 {a['pubTime']}")

TOOLS = {
    "get_weather": {
        "description": "查询中国城市天气。location=城市名(如'北京')/经纬度(如'116.41,39.92')/LocationID，forecast_days=now(实时)|3d|7d|15d",
        "params": {
            "location": {"type": "string", "description": "城市名、经纬度或LocationID"},
            "forecast_days": {"type": "string", "default": "now", "description": "now=实时, 3d/7d/15d=预报"}
        },
        "handler": get_weather
    },
    "get_city_id": {
        "description": "根据城市名查询和风天气LocationID",
        "params": {"location": {"type": "string", "description": "城市名，如'北京'"}},
        "handler": get_city_id
    },
    "get_air_quality": {
        "description": "查询城市空气质量AQI",
        "params": {"location": {"type": "string", "description": "城市名"}},
        "handler": get_air_quality
    }
}

def main():
    for line in sys.stdin:
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        rid = req.get("id")

        if method == "initialize":
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "hefeng-weather", "version": "1.0"}
            }}), flush=True)
        elif method == "notifications/initialized":
            pass
        elif method == "tools/list":
            tools_list = [{"name": k, "description": v["description"],
                          "inputSchema": {"type": "object", "properties": {
                              p: {"type": i.get("type","string"), "description": i.get("description","")}
                              for p, i in v["params"].items()
                          }}} for k, v in TOOLS.items()]
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"tools": tools_list}}), flush=True)
        elif method == "tools/call":
            tool_name = req["params"]["name"]
            arguments = req["params"].get("arguments", {})
            tool = TOOLS.get(tool_name)
            if not tool:
                result = f"未知工具: {tool_name}"
            else:
                try:
                    result = tool["handler"](**arguments)
                except Exception as e:
                    result = f"错误: {e}"
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": str(result)}]
            }}), flush=True)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
