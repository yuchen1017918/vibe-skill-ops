---
name: dev-infra-hub
description: |
  全家桶 L2 目录 — 基础设施层。覆盖：终端/构建、容器、MCP 生态、
  部署/DevOps、安全。当开发需要跑命令、容器、MCP、部署上线、
  安全审查时，先加载本目录定位对应 L3 skill。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vibe-coding, hub, infra, terminal, docker, mcp, devops, security]
    related_skills: [vibe-coding-hub, vibe-terminal-safe, vibe-mcp-connect, docker-management]
---

# 基础设施层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**开发环境与交付**：终端安全、容器、
MCP 能力、部署上线、安全审查。具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：终端/构建安全、容器、MCP 生态、部署/DevOps、安全
- ❌ **不管**：编码/调试/测试主链路 → `dev-core-hub`；语言框架 → `dev-stack-hub`；多Agent编排 → `dev-agent-hub`；模型训练/推理 → `dev-ai-hub`
- 🔄 **协作点**：代码可运行后进入本层做部署；部署前的测试在 `dev-core-hub`；模型服务的基础设施运维在这里

## 🧭 子层路由

### 终端/构建
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `vibe-terminal-safe` | 命令白名单、禁高危命令、构建测试执行 | 跑 build/test/install |

### 容器
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `docker-ops` | Docker 容器/镜像/网络快速操作 | 简单 Docker 操作 |
| `devops/docker-management` | Docker 全生命周期管理（Compose/优化/清理） | Docker 运维（主） |

### MCP 生态
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `vibe-mcp-connect` | 官方 filesystem/git MCP 接入 Hermes | 需要 MCP 文件/版本能力 |
| `hermes-mcp-setup` | MCP server 配置与排障（Hermes 内） | 配 MCP 报错（主） |
| `native-mcp` | 原生 MCP 客户端连接/注册（stdio/HTTP） | 接新 MCP 协议 |
| `fastmcp` | 用 FastMCP 框架快速构建 MCP server | 写 MCP server（Python 快） |
| `mcp-builder` | 高质量 MCP server 通用指南（Python/TS） | 写 MCP server（通用） |
| `mcp-server-authoring` | Python MCP server 标准模式 + Hermes 配置 | 写 Python MCP（主） |
| `mcp-server-pack` | 托管 MCP servers（filesystem/memory 等） | 部署托管 MCP |
| `skill-mcp-installer` | 一键安装 skill 和 MCP server | 安装技能/服务 |
| `mcporter` | mcporter CLI 管理 MCP | CLI 管理 MCP |

### 部署/DevOps
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `github-actions` | CI/CD workflow | 自动化构建 |
| `devops/kubernetes-ops` | K8s pod/deploy/service | K8s 部署 |
| `devops/terraform-iac` | Terraform IaC | 云资源管理 |
| `devops/ansible-automation` | Ansible 自动化 | 配置管理 |
| `devops/ci-cd-pipeline` | CI/CD 流水线 | 发布流水线 |
| `devops/cloud-deployment` | 云部署 | 上线部署 |
| `devops/aws-cloud` | AWS 资源 | AWS 环境 |
| `devops/china-cloud-gpu` | 国内GPU租赁 + AI生成API（无本地GPU时） | 国内环境跑AI画图/视频/训练 |
| `devops/china-mcp-services` | 国内可用 MCP：和风天气/高德/魔搭 | 国内网络配 MCP |
| `china-env-adapt` | 国内环境适配：镜像源切换/超时重试/合规检查 | 国内开发/安装超时/换源（主） |
| `devops/monitoring-observability` | Prometheus/Grafana | 监控告警 |
| `cost-agent` | 成本智能体：token 周报/告警/ROI 看板 | 问"token 花了多少"/消耗异常（v3.5 新增） |
| `release-ops` | 部署回滚+备份恢复：备份三件套→部署验证→回滚流程 | 上线/部署/出问题回滚（主） |

### Hermes 自动化基建
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `devops/hermes-cron-patterns` | Hermes cron 任务编写模式（约束/回退/定时） | 建定时任务 |
| `devops/hermes-log-monitor` | Hermes 日志实时监控面板（Gateway+WebUI 双栏） | 查 Hermes 日志 |

### 安全
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `security-scanner` | 自动化安全扫描与漏洞检测 | 上线前扫描 |
| `devops/penetration-testing` | 渗透测试：侦察/扫描/利用 | 深度安全评估 |
| `devops/python-security` | Python 代码安全 | Python 安全审查 |
| `devops/web-security` | Web 安全 | Web 安全审查 |
| `software-development/project-compliance-audit` | 6 维合规审计 | 项目合规检查 |

## 选择规则

1. **终端先行**：所有命令执行先过 `vibe-terminal-safe` 白名单。
2. **容器二选一**：简单操作 `docker-ops`，运维管理 `devops/docker-management`。
3. **MCP 分层**：接入用 `vibe-mcp-connect`/`hermes-mcp-setup`，开发用 `mcp-server-authoring`，
   托管用 `mcp-server-pack`。
4. **安全贯穿**：上线前必跑 `security-scanner` + 对应语言安全 skill。

## 全局底线

- 禁高危命令：`rm -rf`、`sudo`、`mkfs`、`dd`（除非用户明确要求）。
- MCP 服务器默认不可信，先审查再接入。
- 部署变更：先备份，小步灰度，禁止直接全量覆盖生产。
