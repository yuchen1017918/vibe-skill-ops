# 官方 MCP 工具参考（filesystem + git）

> 完整官方 README 见 /workspace/vibe-coding-family/mcp-ref/ 或
> https://github.com/modelcontextprotocol/servers/tree/main/src/{filesystem,git}

## Filesystem MCP 工具表

| 工具 | 只读 | 幂等 | 破坏性 | 说明 |
|------|------|------|--------|------|
| `read_text_file` | ✅ | – | – | 读文本（支持 head/tail） |
| `read_media_file` | ✅ | – | – | 读媒体文件 |
| `read_multiple_files` | ✅ | – | – | 批量读 |
| `list_directory` | ✅ | – | – | 列目录 |
| `list_directory_with_sizes` | ✅ | – | – | 列目录带大小 |
| `directory_tree` | ✅ | – | – | 目录树 |
| `search_files` | ✅ | – | – | 搜索文件 |
| `get_file_info` | ✅ | – | – | 文件元数据 |
| `list_allowed_directories` | ✅ | – | – | 查看允许目录 |
| `create_directory` | – | ✅ | – | 建目录（重复=no-op） |
| `write_file` | – | ✅ | ✅ | 写文件（覆盖） |
| `edit_file` | – | – | ✅ | 编辑（重放可能失败/重复） |
| `move_file` | – | – | ✅ | 移动（删源） |

**目录访问控制**：命令行参数指定允许目录，或通过 MCP Roots 动态替换。
未指定目录时 server 初始化报错；至少需要一个允许目录。

## Git MCP 工具表（12 个）

| 工具 | 说明 |
|------|------|
| `git_status` | 工作树状态 |
| `git_diff_unstaged` | 未暂存变更（context_lines 可选） |
| `git_diff_staged` | 已暂存变更 |
| `git_diff` | 分支/提交间差异 |
| `git_commit` | 提交（返回 hash） |
| `git_add` | 暂存文件 |
| `git_reset` | 取消暂存 |
| `git_log` | 提交日志（支持时间过滤：ISO/相对日期） |
| `git_create_branch` | 建分支 |
| `git_checkout` | 切分支 |
| `git_show` | 查看某提交内容 |
| `git_branch` | 列分支（local/remote/all，支持 contains） |

## 安装速查

```bash
# filesystem（Node）
npm install -g @modelcontextprotocol/server-filesystem
npx -y @modelcontextprotocol/server-filesystem /workspace

# git（Python，推荐 uvx）
pip install mcp-server-git        # 或：uvx mcp-server-git --repository <path>
python -m mcp_server_git --repository <path>

# docker
docker run --rm -i -v /workspace:/projects mcp/filesystem
docker run --rm -i -v /workspace:/workspace mcp/git
```

## Hermes 配置模板

```yaml
mcp:
  servers:
    filesystem:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    git:
      command: uvx
      args: ["mcp-server-git", "--repository", "/workspace"]
```
