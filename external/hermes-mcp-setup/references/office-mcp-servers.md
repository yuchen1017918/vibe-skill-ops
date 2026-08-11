# 办公 MCP 服务器选项

调研于 2026-07-27。覆盖 Notion、Google Workspace、Airtable 三个主流办公 MCP。

---

## 1. Notion MCP（官方）

- **包**: `@notionhq/notion-mcp-server` (npm, v2.5.1)
- **命令**: `npx -y @notionhq/notion-mcp-server`
- **环境变量**: `OPENAPI_MCP_HEADERS={"Authorization":"Bearer ntn_...","Notion-Version":"2025-09-03"}`
- **Token 获取**: notion.so/profile/integrations → 创建 Internal Integration → 复制 Secret
- **国内可用**: ✅ 无需科学上网
- **工具**: 搜索页面、读取/创建/更新页面和数据库、管理 block 内容
- **仓库**: github.com/makenotion/notion-mcp-server

### Hermes 配置

```yaml
mcp_servers:
  notion:
    command: npx
    args:
      - "-y"
      - "@notionhq/notion-mcp-server"
    env:
      OPENAPI_MCP_HEADERS: '{"Authorization":"Bearer ntn_YOUR_TOKEN","Notion-Version":"2025-09-03"}'
    timeout: 30
```

---

## 2. Google Workspace MCP

- **包**: `workspace-mcp` (PyPI, uvx)
- **命令**: `uvx workspace-mcp`
- **OAuth**: 需要 Google Cloud Console 创建 OAuth 2.0 凭据
- **环境变量**: `GOOGLE_OAUTH_CLIENT_ID` + `GOOGLE_OAUTH_CLIENT_SECRET`
- **国内可用**: ❌ 需要科学上网（Google 服务被墙）
- **覆盖**: Gmail、Calendar、Drive、Docs、Sheets、Slides、Forms、Tasks、Chat
- **仓库**: github.com/taylorwilsdon/google_workspace_mcp

### 备选方案

- `@dguido/google-workspace-mcp` (npx) — 更轻量，仅 Drive/Calendar/Gmail
- `pm990320/google-workspace-mcp` — 95+ 工具，多账户支持

---

## 3. Airtable MCP

- **包**: `airtable-mcp-server` (npm)
- **命令**: `npx airtable-mcp-server`
- **环境变量**: `AIRTABLE_API_KEY`
- **Token 获取**: airtable.com/create/tokens → Personal Access Token
  - 必需 scope: `schema.bases:read`, `data.records:read`
  - 可选 scope: `schema.bases:write`, `data.records:write`
- **国内可用**: ✅ 无需科学上网
- **仓库**: github.com/domdomegg/airtable-mcp-server

### Hermes 配置

```yaml
mcp_servers:
  airtable:
    command: npx
    args:
      - "airtable-mcp-server"
    env:
      AIRTABLE_API_KEY: "pat_YOUR_TOKEN"
    timeout: 30
```

---

## 与本地办公技能的互补关系

| 场景 | 工具 |
|------|------|
| 本地 WPS/Office 文档创建编辑 | `xlsx`/`docx`/`powerpoint`/`pdf` 技能 |
| 本地文档深度分析 | `doc-deep-analysis` 技能 |
| 云协作/远程数据 | Notion MCP / Airtable MCP |
| 邮件+日历+云端文档 | Google Workspace MCP（需科学上网） |

MCP 办公服务器是**云端能力的延伸**，不替代本地办公技能。
