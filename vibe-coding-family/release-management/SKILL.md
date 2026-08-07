---
name: release-management
description: |
  ⚠️ v1.3 deprecated — 由 release-ops 取代（合并了发布+回滚）。文件保留防交叉引用。
  通用发布与版本管理 skill：语义化版本（SemVer）、CHANGELOG 维护、
  发布流程、tag 管理、发布检查清单。语言无关，适用任何项目。
  当用户说"发布"、"发版本"、"打tag"、"版本号"、"CHANGELOG"、
  "semver"、"release"、"上线新版本"时加载。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, release, version, semver, changelog, tag, publish]
    related_skills: [vibe-coding-hub, git-workflow, rollback-backup, dev-core-hub, python-package-release]
---

# 通用发布与版本管理（Release Management）

**核心思想**：发布不是"跑一下命令"，而是有纪律的流程——版本号有语义、变更有人看、
发布可追溯、出问题可回滚。语言无关，Python/Node/Go/Rust 通用。

## 1️⃣ 语义化版本（SemVer）规则

```
X.Y.Z
│ │ └─ patch：Bug修复、小改动（向后兼容）
│ └─── minor：新功能（向后兼容）
└───── major：破坏性变更（不兼容）
```

| 阶段 | 版本示例 | 说明 |
|------|----------|------|
| 初始开发 | 0.1.0 | 首个可运行版本 |
| 正式版 | 1.0.0 | 首个稳定版 |
| 新功能 | 1.1.0 | 加了功能 |
| 修Bug | 1.1.1 | 只修问题 |
| 破坏性变更 | 2.0.0 | API 不兼容 |

**版本号决策表**：
| 变更类型 | 版本变动 |
|----------|----------|
| 修Bug（不破坏） | patch +1 |
| 新功能（兼容） | minor +1，patch 归零 |
| 破坏性变更 | major +1，minor/patch 归零 |
| 预发布 | 加后缀：1.2.0-rc.1 / 1.2.0-beta.2 |

## 2️⃣ 发布流程（6 步）

```
1. 分支准备：从 main 切 release/x.y.z 分支
2. 冻结功能：只修Bug不加法（feature freeze）
3. 更新版本号：package.json / pyproject.toml / Cargo.toml 等
4. 写 CHANGELOG：记录本次变更（见 §3）
5. 打 tag：git tag vX.Y.Z（带注释）+ git push --tags
6. 发布产物：构建/打包/部署（按项目）
```

**发布检查清单（发布前逐项确认）**：
- [ ] 所有测试通过（单元+集成）
- [ ] 无 TODO/FIXME 残留
- [ ] 版本号已更新（所有声明处一致）
- [ ] CHANGELOG 已写（用户可见的变更）
- [ ] 密钥无泄露（.env 不入库）
- [ ] 依赖锁文件已更新（lockfile）
- [ ] 备份已完成（配合 rollback-backup）
- [ ] 发布说明已准备（给用户/团队看的摘要）

## 3️⃣ CHANGELOG 规范（Keep a Changelog 风格）

```markdown
# Changelog

## [1.2.0] - 2026-08-06
### Added
- 新功能：用户导入导出
### Changed
- 重构认证模块
### Fixed
- 修复 #42 空指针崩溃
### Removed
- 移除废弃的旧 API

## [1.1.0] - 2026-07-20
...
```

**类型标签**：Added（新增）/ Changed（修改）/ Deprecated（弃用）/ Removed（移除）/ Fixed（修复）/ Security（安全）

## 4️⃣ Git tag 管理

| 命令 | 用途 |
|------|------|
| `git tag -a v1.2.0 -m "release 1.2.0"` | 打带注释的 tag |
| `git tag -l "v*"` | 列出所有版本 tag |
| `git push origin v1.2.0` | 推送单个 tag |
| `git checkout v1.2.0` | 切到发布版本（回滚用） |
| `git describe --tags` | 看当前最近 tag |

**tag 命名规范**：`v<major>.<minor>.<patch>`（如 v2.1.0），不重复。

## 5️⃣ 发布策略选择

| 场景 | 策略 |
|------|------|
| 快速迭代/MVP | 直接打 tag 发布（每次有完整测试） |
| 稳定服务 | 预发布流程：rc → beta → stable |
| 破坏性变更 | 先 deprecation 通知，再 major 发布 |
| 多环境 | dev → staging → prod 逐级发布 |

## 6️⃣ 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `git-workflow` | 发布基于 git 分支/tag 管理 |
| `rollback-backup` | 发布前备份，发布失败回滚 |
| `python-package-release` | Python 项目的具体打包发布（本 skill 的 Python 落地） |
| `dev-core-hub` | 测试通过后才允许发布（联动 test-driven-development） |
| `snapshot-notes` | 发布事件记录到 .snapshots/SNAPSHOT.md |
| `agent-loop` | 自动开发模式下发布是最后一环，验证通过才打 tag |

## ⚠️ 核心原则

1. **版本有语义**：版本号变化传达变更类型，不是随机数字。
2. **变更可追溯**：每个版本都有 CHANGELOG 记录。
3. **发布可回滚**：发布前必有备份（rollback-backup）。
4. **测试是门槛**：测试不过不发布。
5. **一次一个版本**：不跨版本混功能。

## 快速排障

| 症状 | 处理 |
|------|------|
| 版本号改乱了 | 以最高版本为准，重新对齐所有声明处 |
| 忘了写 CHANGELOG | 从 git log 提取变更生成 |
| tag 推错了 | `git tag -d` 删除本地 + `git push origin :refs/tags/<tag>` 删远程 |
| 发布后发现Bug | 立即 patch 版本（x.y.z+1）修复，不回滚 major |
| 多语言版本号不一致 | 检查所有 manifest 文件（package.json/pyproject.toml/Cargo.toml） |
