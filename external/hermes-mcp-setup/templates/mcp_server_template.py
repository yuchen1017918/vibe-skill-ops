#!/usr/bin/env python3
"""MCP Server Template — 最小可用的 Python MCP 服务器模板

直接复制、改 TOOLS 字典、运行即可。
纯 Python stdlib，无外部依赖。
"""

import json, sys


# ═══════════════════════════════════════════
# 在这里定义你的工具
# ═══════════════════════════════════════════

def my_tool(param1: str, param2: int = 0):
    """工具的描述（会作为 tool description 的一部分）"""
    return f"结果: param1={param1}, param2={param2}"


TOOLS = {
    "my_tool": {
        "description": "工具的描述文本 — 给 LLM 看的",
        # ⚠️ 类型必须用 JSON Schema 合法类型：
        #    "string" | "number" | "integer" | "boolean" | "object" | "array"
        #    不能用 "float" 或 "int" — 会导致 HTTP 400！
        "params": {"param1": "string", "param2": "integer"},
        "handler": my_tool,
    },
}


# ═══════════════════════════════════════════
# 下面部分是标准 MCP JSON-RPC 循环，一般不需要改
# ═══════════════════════════════════════════

def main():
    for line in sys.stdin:
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method")
        rid = req.get("id")

        if method == "initialize":
            print(json.dumps({
                "jsonrpc": "2.0", "id": rid,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "my-mcp", "version": "1.0"}
                }
            }), flush=True)

        elif method == "notifications/initialized":
            pass

        elif method == "tools/list":
            tools_list = [
                {
                    "name": k,
                    "description": v["description"],
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            p: {"type": t, "description": p}
                            for p, t in v["params"].items()
                        }
                    }
                }
                for k, v in TOOLS.items()
            ]
            print(json.dumps({
                "jsonrpc": "2.0", "id": rid,
                "result": {"tools": tools_list}
            }), flush=True)

        elif method == "tools/call":
            tool_name = req["params"]["name"]
            arguments = req["params"].get("arguments", {})
            tool = TOOLS.get(tool_name)

            if not tool:
                result = f"未知工具: {tool_name}"
            else:
                try:
                    # 类型转换
                    typed_args = {}
                    for k, v in arguments.items():
                        t = tool["params"].get(k, "string")
                        if t == "number":
                            typed_args[k] = float(v)
                        elif t == "integer":
                            typed_args[k] = int(v)
                        else:
                            typed_args[k] = str(v)

                    result = tool["handler"](**typed_args) if typed_args else tool["handler"]()
                except Exception as e:
                    result = f"错误: {e}"

            print(json.dumps({
                "jsonrpc": "2.0", "id": rid,
                "result": {"content": [{"type": "text", "text": str(result)}]}
            }), flush=True)

        sys.stdout.flush()


if __name__ == "__main__":
    main()
