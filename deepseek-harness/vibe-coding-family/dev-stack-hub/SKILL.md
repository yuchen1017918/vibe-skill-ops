---
name: dev-stack-hub
description: 全家桶 L2 目录 — 技术栈层。覆盖：编程语言、前端/UI、数据库、 移动端、游戏引擎。当项目确定技术栈后，先加载本目录 定位对应语言/框架的 L3 skill。
family-type: tool
family-version: 1.0.0
---

# 技术栈层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**语言与框架**：项目定了技术栈就到这里找对应 skill。
具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：编程语言、前端/UI、数据库、移动端、游戏引擎、Web3 的技术栈级 skill
- ❌ **不管**：主流程/编码纪律 → `dev-core-hub`；环境/容器/部署 → `dev-infra-hub`；多Agent → `dev-agent-hub`；AI/ML 专项 → `dev-ai-hub`
- 🔄 **协作点**：技术栈确定后才进本层；项目脚手架初始化在 `dev-core-hub`（`project-scaffold`）先做

## 🧭 子层路由

### 编程语言（通用）
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `python3` + `py` | Python 环境/依赖/脚本 + 语法可靠性规范 | Python 项目（主） |
| `typescript` | 类型安全 TypeScript | TS 项目 |
| `cpp` | 现代 C++17/20 | C++ 项目 |
| `rust` | 惯用 Rust（所有权规避） | Rust 项目 |
| `java-spring-boot` | Spring Boot 生产级应用 | Java 项目 |
| `php` | 规避类型杂耍陷阱 | PHP 项目 |
| `solidity` | Solidity 常见坑规避 | 智能合约 |
| `csharp-dotnetcore-natasha` | C# .NET Core + Natasha | .NET 项目 |
| `sql` | 关系数据库 schema/查询 | 数据库操作 |
| `nosql-databases` | Redis 等 NoSQL 操作 | NoSQL 操作 |
| `database-migration` | Alembic 数据库迁移 | schema 变更 |
| `data-science/data-engineering` | 数据工程：管道/清洗/ETL | 数据处理管线 |
| `data-science/advanced-data-analysis` | SQLAlchemy+ 高级数据分析 | 复杂数据分析 |
| `data-science/pandas-data-analysis` | pandas 数据分析 | DataFrame 处理 |
| `data-science/data-visualization` | 数据可视化（matplotlib/plotly） | 出图表 |
| `software-development/blockchain-web3` | Web3 开发：钱包/链交互/DApp | Web3 项目 |
| `software-development/defi-protocols` | DeFi 协议开发（Uniswap V3/Sushiswap） | DeFi 项目 |
| `python-code-quality` | ruff/black/isort 质量工具链 | Python 代码质量 |
| `python-performance` | Python 性能优化（先测后优） | Python 性能瓶颈 |
| `python-package-release` | Python 打包发布生命周期 | 发布 Python 包 |

### 前端/UI
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `frontend-design` | 有意图的视觉设计指南 | Web 界面设计 |
| `frontend-design-policy` | 审美约束：防 AI 味、克制布局/颜色/信息密度 | 前端 UI 开发（v3.3 新增，自动注入） |
| `web-artifacts-builder` | 多组件 Web 前端构建套件 | 复杂前端 |
| `software-development/static-site-editing` | 已有静态站定向修改 | 改现有站点 |
| `creative/claude-design` | 一次性 HTML artifact（落地页/原型） | 快速原型 |
| `creative/popular-web-designs` | 54 套真实设计系统 HTML/CSS | 抄优秀设计 |
| `flutter` | Flutter 构建/调试/发布 | Flutter 项目 |

### 移动端
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `ios-swift-dev` | Swift UIKit/SwiftUI | iOS 开发 |
| `react-native-mobile` | React Native 移动开发 | RN 项目 |

### 游戏引擎（三选一，按引擎加载）
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `unity-game-engine` | Unity + C#：MonoBehaviour/prefab/physics | Unity 项目 |
| `godot-game-engine` | Godot 4 + GDScript：节点/场景/信号 | Godot 项目 |
| `game-development` | Pygame/Ursina 2D/3D Python 游戏 | Python 游戏 |

### 桌面
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `win32-desktop-utils` | Win32 C++ 桌面工具 | Windows 桌面工具 |
| `smartide-dev` | SmartIDE 智能 IDE 开发工作流 | 智码 IDE |

## 选择规则

1. **先定语言**：项目用什么语言 → 加载对应语言 skill（如 `python3`）。
2. **再看框架**：有特定框架（Spring/Flutter/Unity）→ 加载框架 skill。
3. **数据层**：涉及数据库 → `sql` / `nosql-databases` / `database-migration`。
4. **UI 优先**：Web 项目先看 `frontend-design` 定视觉方向，再写代码。

## 全局底线

- 语言 skill 是"最佳实践 + 避坑"，不是替代主流程（vibe-coding/dev-team）。
- 涉及数据库 schema 变更：先备份/迁移计划，禁止直接 DROP。
