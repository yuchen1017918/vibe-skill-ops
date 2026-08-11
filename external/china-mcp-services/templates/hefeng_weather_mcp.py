#!/usr/bin/env python3
"""和风天气 MCP Server — 精简、可靠
模板用法：替换 HEFENG_API_KEY 和 HEFENG_API_HOST 环境变量
"""

import json, sys, os
import urllib.request, urllib.parse

API_KEY = os.environ.get("HEFENG_API_KEY", "")
API_HOST = os.environ.get("HEFENG_API_HOST", "")

# 常用中国城市 LocationID 映射 (40+ cities)
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
    "合肥": "101220101", "合肥市": "101220101", "hefei": "101220101",
    "福州": "101230101", "福州市": "101230101", "fuzhou": "101230101",
    "济南": "101120101", "济南市": "101120101", "jinan": "101120101",
    "昆明": "101290101", "昆明市": "101290101", "kunming": "101290101",
    "哈尔滨": "101050101", "哈尔滨市": "101050101", "haerbin": "101050101",
    "沈阳": "101070101", "沈阳市": "101070101", "shenyang": "101070101",
    "三亚": "101310201", "三亚市": "101310201", "sanya": "101310201",
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
    return "101010100"  # default Beijing

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
    loc_id = resolve_location(location)
    if forecast_days == "now":
        data = call_api("/v7/weather/now", {"location": loc_id})
        if data.get("code") != "200":
            return f"查询失败: {data}"
        n = data["now"]
        return (f"📍 {location}\n"
                f"🌡️ 温度: {n['temp']}°C (体感 {n['feelsLike']}°C)\n"
                f"🌤️ 天气: {n['text']}\n"
                f"💨 {n['windDir']} {n['windScale']}级\n"
                f"💧 湿度: {n['humidity']}% | 能见度: {n['vis']}km\n"
                f"🕐 {n['obsTime']}")
    else:
        data = call_api(f"/v7/weather/{forecast_days}", {"location": loc_id})
        if data.get("code") != "200":
            return f"查询失败: {data}"
        lines = [f"📍 {location} — {forecast_days}预报:"]
        for d in data.get("daily", []):
            lines.append(f"  {d['fxDate']} | {d['textDay']}/{d['textNight']} | "
                        f"{d['tempMin']}~{d['tempMax']}°C")
        return "\n".join(lines)

def get_air_quality(location: str):
    loc_id = resolve_location(location)
    data = call_api("/v7/air/now", {"location": loc_id})
    if data.get("code") != "200":
        return f"查询失败(可能需要额外订阅): {data}"
    a = data["now"]
    return (f"📍 {location} AQI: {a['aqi']} ({a['category']})\n"
            f"PM2.5: {a['pm2p5']} | PM10: {a['pm10']}")

TOOLS = {
    "get_weather": {
        "description": "查询天气: location=城市名/经纬度/LocationID, forecast_days=now|3d|7d|15d",
        "params": {"location": "string", "forecast_days": "string"},
        "handler": get_weather
    },
    "get_air_quality": {
        "description": "查询空气质量AQI",
        "params": {"location": "string"},
        "handler": get_air_quality
    },
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
            print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{
                "protocolVersion":"2024-11-05",
                "capabilities":{"tools":{}},
                "serverInfo":{"name":"hefeng-weather","version":"1.0"}
            }}), flush=True)
        elif method == "notifications/initialized":
            pass
        elif method == "tools/list":
            tl = [{"name":k,"description":v["description"],
                   "inputSchema":{"type":"object","properties":{
                       p:{"type":t,"description":p} for p,t in v["params"].items()
                   }}} for k,v in TOOLS.items()]
            print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{"tools":tl}}), flush=True)
        elif method == "tools/call":
            tn = req["params"]["name"]
            args = req["params"].get("arguments",{})
            tool = TOOLS.get(tn)
            if not tool:
                r = f"未知工具: {tn}"
            else:
                try:
                    r = tool["handler"](**args)
                except Exception as e:
                    r = f"错误: {e}"
            print(json.dumps({"jsonrpc":"2.0","id":rid,"result":{
                "content":[{"type":"text","text":str(r)}]
            }}), flush=True)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
