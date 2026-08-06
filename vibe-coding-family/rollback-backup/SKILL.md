---
name: rollback-backup
description: |
  部署回滚与备份恢复 skill：上线前的备份策略、部署后的验证、
  出问题时的回滚流程、数据恢复步骤。补全"部署→验证→回滚"闭环。
  当用户说"上线"、"部署"、"出问题了"、"回滚"、"备份"、
  "恢复"、或项目准备发布时加载。
  触发词：回滚、rollback、备份、backup、恢复、restore、上线出问题。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: workflow
    tags: [vibe-coding, rollback, backup, restore, deploy, release, recovery]
    related_skills: [vibe-coding-hub, dev-infra-hub, github-actions, git-workflow, snapshot-notes]
---

# 部署回滚与备份恢复（Rollback & Backup）

**核心闭环**：备份 → 部署 → 验证 → （出问题？）回滚 → 恢复验证。

```
部署前         部署中        部署后
  │             │             │
  ▼             ▼             ▼
备份当前版本 → 部署新版本 → 验证（健康检查+冒烟测试）
                                │
                    ✅ 正常 → 完成（旧备份保留N天）
                    ❌ 异常 → 回滚到备份 → 验证恢复 → 记录根因
```

## 1️⃣ 部署前：备份策略（必须）

**备份三件套**，缺一不可：
| 备份项 | 内容 | 方式 |
|--------|------|------|
| **代码版本** | 当前 release 的 git tag/commit | `git tag backup-YYYYMMDD-HHMM`（部署前打tag） |
| **数据库** | 当前 schema + 数据 | `pg_dump` / `mysqldump` / `sqlite .backup` |
| **配置/环境** | .env / 配置文件（脱敏） | 复制到 `backups/<日期>/`（密钥脱敏） |

**备份目录约定**：
```
<项目根>/backups/
├── 2026-08-06-1500/          # 每次部署前的备份
│   ├── CODE.tag              # git tag 名
│   ├── DB.dump               # 数据库备份
│   └── CONFIG.env            # 配置（脱敏）
└── LATEST                   # 指向最新备份的链接
```

**备份验证**：备份完成后必须验证可恢复（`pg_restore --list` 或恢复到一个临时库测试）。

## 2️⃣ 部署中：部署清单

1. 确认代码版本（git status 干净 + 目标 commit）
2. 执行备份（§1 三件套）
3. 应用新版本（部署命令按项目）
4. 数据库迁移（如有）：先备份再迁移，迁移脚本需可回滚
5. 记录部署时间戳到 `.snapshots/SNAPSHOT.md`

## 3️⃣ 部署后：验证（5 分钟健康检查）

| 检查项 | 命令/方式 | 通过标准 |
|--------|-----------|----------|
| 健康检查 | `curl -f http://localhost:PORT/health` | HTTP 200 |
| 冒烟测试 | 跑核心流程 1-2 个 | 主功能正常 |
| 日志 | `tail -f` 关键日志 | 无 ERROR 堆积 |
| 数据库 | 简单查询 | 数据完整 |
| 依赖 | `pip check` / `npm ls` | 无冲突 |

**全部通过 → 部署完成**；任一失败 → 进入 §4 回滚。

## 4️⃣ 回滚流程（出问题时执行）

```
1. 立即停止新版本服务（或切换流量）
2. 确认备份存在（backups/LATEST）
3. 恢复代码：git checkout <backup-tag> 或 git revert
4. 恢复数据库：从 DB.dump 恢复（注意：如有迁移需先回滚迁移）
5. 恢复配置：从 CONFIG.env 恢复
6. 重启服务 + 跑 §3 验证
7. 记录：根因 + 回滚耗时 + 影响范围 → SNAPSHOT.md + EXPERIENCE.md
```

### 回滚决策表
| 情况 | 回滚方式 |
|------|----------|
| 代码问题（新代码有Bug） | `git checkout` 旧 tag + 重新部署 |
| 数据库迁移出错 | 先回滚迁移（`alembic downgrade`），再恢复数据 |
| 配置错误 | 恢复备份的 CONFIG.env，重启 |
| 依赖冲突 | `pip install` 旧版本 / `npm ci` 按 lockfile |
| 完全失控 | 停机维护 → 全量恢复 → 排查根因后再上线 |

## 5️⃣ 备份保留策略

| 备份类型 | 保留时长 | 说明 |
|----------|----------|------|
| 最近 3 次部署备份 | 永久（短期） | 随时可回滚 |
| 每日备份 | 7 天 | 防数据丢失 |
| 每周备份 | 30 天 | 防长期问题 |
| 每月备份 | 永久（长期） | 合规/审计 |

## 6️⃣ 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `dev-infra-hub` | 部署组的"最后一步"：cloud-deployment 部署完 → 本 skill 负责验证+回滚 |
| `git-workflow` | 代码回滚基于 git tag/revert，git 状态要干净 |
| `snapshot-notes` | 部署/回滚事件记录到 `.snapshots/SNAPSHOT.md` |
| `agent-loop` | 自动开发模式下部署失败 → 走回滚流程 → 记录后继续 |
| `database-migration` | 迁移回滚的具体执行（alembic downgrade） |
| `monitoring-observability` | 部署后监控告警接入，异常自动触发回滚评估 |

## ⚠️ 核心原则

1. **先备份再部署**：没有备份的部署就是赌博。
2. **备份必须可验证**：不能恢复的备份等于没有备份。
3. **回滚要快**：5 分钟决策窗口，超过就回滚而不是修。
4. **回滚不是失败**：是标准流程的一环，记录根因改进。
5. **密钥不入备份**：CONFIG.env 必须脱敏，密钥单独安全存储。

## 快速排障

| 症状 | 处理 |
|------|------|
| 备份文件损坏 | 立即重做备份；用上一份备份恢复 |
| 回滚后数据不一致 | 恢复数据库 + 检查迁移版本（alembic current） |
| 找不到备份 | 检查 backups/LATEST；git 历史里找旧 tag |
| 回滚后仍报错 | 环境问题 → 检查依赖版本，或回退到更早备份 |
| 部署新版本没备份 | 立即停下，先备份再继续 |
