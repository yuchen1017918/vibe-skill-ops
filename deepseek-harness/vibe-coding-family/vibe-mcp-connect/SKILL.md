---
name: vibe-mcp-connect
description: 官方 filesystem/git MCP 接入 Hermes 的配置说明。当需要 MCP 文件操作、 MCP 版本控制、或想让 Agent 通过 MCP 获得隔离的文件/git 能力时加载。 附官方 README 参考（references/）。
family-type: tool
family-version: 1.0.0
---

# 官方 MCP 接入（Vibe-Coding 版）

官方 `modelcontextprotocol/servers`（⭐89k）提供 filesystem / git / shell 等 MCP server，
让 Agent 获得**受控、可审计**的文件和版本控制能力。本 skill 说明如何在 Hermes 中接入。

## 为什么 vibe-coding 需要 MCP

- **隔离安全**：MCP filesystem 限制访问目录（白名单 roots），防止误删项目外文件。
- **可审计**：git MCP 的 diff/commit 操作有明确工具边界。
- **组合能力**：filesystem + git + code-search 组合 = vibe-coding 基础设施。

## 1. 官方 filesystem MCP

功能：读/写文件、目录遍历、glob 搜索、edit 文件（带破坏性提示）。

配置（Hermes `~/.hermes/config.yaml`）：

```yaml
mcp:
  servers:
    filesystem:
      command: npx
      args:
        - "-y"
        - "@modelcontextprotocol/server-filesystem"
        - "/workspace"        # ← 允许访问的目录（可多个，可加 ro 只读）
```

安装方式（npx 拉取）：`npm install -g @modelcontextprotocol/server-filesystem` 或
Docker：`docker run --rm -i -v /workspace:/projects mcp/filesystem`。

## 2. 官方 git MCP

功能：`git_status`、`git_diff_unstaged`、`git_diff_staged`、`git_diff`、`git_commit`、
`git_add`、`git_reset`、`git_log`、`git_create_branch`、`git_checkout`、`git_show`、`git_branch`。

配置（Hermes）：

```yaml
mcp:
  servers:
    git:
      command: uvx
      args: ["mcp-server-git", "--repository", "/workspace"]
```

安装：`pip install mcp-server-git` 或 `uvx mcp-server-git`（推荐，无需预装）。

## 3. 官方 shell MCP（可选，隔离执行）

配置：

```yaml
mcp:
  servers:
    shell:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-shell"]
```

> 生产环境必须配置命令白名单，禁止高危命令（详见 `vibe-terminal-safe`）。

## 4. Hermes 配置与验证

1. 编辑 `~/.hermes/config.yaml`（或 `hermes config` 命令），加 `mcp.servers` 段。
2. 重启 Hermes 会话，用 `hermes mcp list` 或工具列表确认 server 已连接。
3. 连通性测试：让 Agent 调用一次 `list_allowed_directories`（filesystem）或 `git_status`（git）。
4. 失败排查：查看 MCP 日志（`hermes logs`），确认命令路径/依赖存在。

> 详细配置与故障排查见 `hermes-mcp-setup` skill。

## 5. 参考文档

- `references/filesystem-README.md` — 官方 filesystem MCP 完整说明（工具表、权限控制）
- `references/git-README.md` — 官方 git MCP 完整说明（12 个工具、安装配置）

来源：https://github.com/modelcontextprotocol/servers/tree/main/src/{filesystem,git}

## 快速排障

| 症状 | 处理 |
|------|------|
| npx 找不到包 | 国内网络用镜像：`npm config set registry https://registry.npmmirror.com` |
| uvx 未安装 | `pip install uv` 或改用 pip 安装 mcp-server-git |
| 权限拒绝 | filesystem 只允许配置的 roots 目录，把项目路径加入 args |
| 连接失败 | 检查 config.yaml 语法（yaml 缩进）、重启会话 |
