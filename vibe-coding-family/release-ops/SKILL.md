---
name: release-ops
description: |
  发布与回滚一体化 skill（v1.3 合并自 release-management + rollback-backup）：
  SemVer版本 + CHANGELOG + tag + 发布检查清单 + 备份三件套 + 部署验证 + 回滚流程。
  当用户说"发布"、"发版本"、"打tag"、"上线"、"部署"、"出问题了"、
  "回滚"、"备份"、"恢复"时加载。
  触发词：发布、发版本、打tag、上线、部署、回滚、备份、恢复。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, release, version, rollback, backup, deploy, semver, changelog]
    related_skills: [vibe-coding-hub, dev-core-hub, git-workflow, security-audit, snapshot-notes]
---

# 发布与回滚一体化（Release Ops）

**v1.3 合并产物**:由 `release-management`(发布)+ `rollback-backup`(回滚)合并而成。
发布和回滚是同一流程的两面——**先备份再发布,出问题可回滚**,一份文档管完整闭环。

## 1️⃣ 语义化版本(SemVer)

```
X.Y.Z  │ patch=修Bug(兼容) │ minor=新功能(兼容) │ major=破坏性变更
```

| 变更类型 | 版本变动 |
|----------|----------|
| 修Bug(不破坏) | patch +1 |
| 新功能(兼容) | minor +1,patch 归零 |
| 破坏性变更 | major +1,minor/patch 归零 |
| 预发布 | 加后缀:1.2.0-rc.1 / beta.2 |

## 2️⃣ 发布流程(6 步 + 检查清单)

```
1. 分支准备:从 main 切 release/x.y.z
2. 冻结功能:只修Bug不加法
3. 更新版本号:所有 manifest 一致(package.json / pyproject.toml / Cargo.toml)
4. 写 CHANGELOG(见 §5)
5. 打 tag:git tag -a vX.Y.Z -m "release X.Y.Z"
6. 发布产物(构建/打包/部署)
```

**发布前检查清单**:
- [ ] 所有测试通过(单元+集成)
- [ ] 无 TODO/FIXME 残留
- [ ] 版本号所有声明处一致
- [ ] CHANGELOG 已写
- [ ] 密钥无泄露(.env 不入库)
- [ ] **备份已完成(§3,发布前必做)**
- [ ] security-audit 通过(生产敏感变更强制)

## 3️⃣ 备份三件套(发布前必做)

| 备份项 | 内容 | 方式 |
|--------|------|------|
| **代码版本** | 当前 release 的 git tag/commit | `git tag backup-YYYYMMDD-HHMM` |
| **数据库** | schema + 数据 | `pg_dump` / `mysqldump` / `sqlite .backup` |
| **配置/环境** | .env / 配置文件(脱敏) | 复制到 `backups/<日期>/` |

```
<项目根>/backups/
├── 2026-08-07-1500/   CODE.tag + DB.dump + CONFIG.env(脱敏)
└── LATEST             # 指向最新备份
```

> **备份必须可验证**(能恢复的备份才算备份)。保留策略:近 3 次永久 / 每日 7 天 / 每周 30 天 / 每月永久。

## 4️⃣ 部署验证 + 回滚

### 部署后 5 分钟健康检查

| 检查项 | 通过标准 |
|--------|----------|
| 健康检查 `curl -f localhost:PORT/health` | HTTP 200 |
| 冒烟测试 | 核心流程 1-2 个正常 |
| 日志 | 无 ERROR 堆积 |
| 数据库 | 简单查询完整 |
| 依赖 `pip check` / `npm ls` | 无冲突 |

**全部通过 → 完成;任一失败 → 回滚(5 分钟决策窗口,超过就回滚而不是修)**

### 回滚流程

```
1. 停止新版本服务(或切换流量)
2. 确认备份存在(backups/LATEST)
3. 恢复代码:git checkout <backup-tag>
4. 恢复数据库:从 DB.dump 恢复(迁移先 alembic downgrade)
5. 恢复配置:CONFIG.env
6. 重启 + 跑 §4 健康检查
7. 记录:根因 + 回滚耗时 + 影响范围 → SNAPSHOT.md + EXPERIENCE.md
```

### 回滚决策表

| 情况 | 方式 |
|------|------|
| 代码Bug | git checkout 旧 tag + 重新部署 |
| 迁移出错 | 先 alembic downgrade,再恢复数据 |
| 配置错误 | 恢复 CONFIG.env,重启 |
| 依赖冲突 | pip install 旧版本 / npm ci 按 lockfile |
| 完全失控 | 停机维护 → 全量恢复 → 排查根因再上线 |

## 5️⃣ CHANGELOG 规范(Keep a Changelog 风格)

```markdown
## [1.2.0] - 2026-08-07
### Added     新功能
### Changed   修改
### Fixed     修复
### Deprecated / Removed / Security
```

## ⚠️ 核心原则

1. **版本有语义**:版本号传达变更类型,不是随机数字
2. **先备份再部署**:没有备份的部署就是赌博;备份必须可验证
3. **回滚要快**:5 分钟决策窗口,超过就回滚而不是修
4. **回滚不是失败**:是标准流程的一环,记录根因改进
5. **测试是门槛**:测试不过不发布;密钥不入备份

## 🔗 与全家桶衔接

| Skill | 协作 |
|-------|------|
| `git-workflow` | 分支/tag/revert 基础 |
| `security-audit` | 生产变更发布前强制扫描 |
| `snapshot-notes` | 发布/回滚事件记录 |
| `dev-core-hub` | 测试通过才允许发布 |
| `agent-loop` | 自动开发模式下发布是最后一环,验证通过才打 tag |

## 快速排障

| 症状 | 处理 |
|------|------|
| 版本号改乱 | 以最高版本为准,重新对齐所有声明处 |
| 忘了 CHANGELOG | 从 git log 提取变更生成 |
| tag 推错 | `git tag -d` 本地 + `git push origin :refs/tags/<tag>` 删远程 |
| 发布后发现Bug | 立即 patch 版本修复,不回滚 major |
| 找不到备份 | 检查 backups/LATEST;git 历史找旧 tag |
| 回滚后数据不一致 | 恢复数据库 + 检查迁移版本(alembic current) |
