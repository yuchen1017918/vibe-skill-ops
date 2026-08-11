---
name: git-workflow
description: |
  OpenClaw Git 工作流技能。
  
  当用户提及以下任务时使用：
  - 提交代码或文档
  - 推送到远程仓库
  - 管理多个 Git 仓库
  - 查看 Git 状态
  
  核心能力:
  - 自动检测文件变更
  - 自动生成提交信息
  - 自动推送到远程仓库
  - 多仓库管理
license: MIT
compatibility: |
  需要以下环境：
  - Git 已安装
  - 已配置 Git 用户信息
  - 已配置远程仓库
  
  支持平台:
  - OpenClaw ✅
  - Claude Code ✅
metadata:
  author: OpenClaw 实战团队
  version: 1.0.0
  category: git-workflow
  tags: [git, version-control, automation]
  created: 2026-02-26
---

# Git 工作流技能

## 核心指令

### 第零步：分支策略与提交纪律（v1.1 新增 — 参考 addyosmani/agent-skills）

**Trunk-Based 推荐**：主分支（main/master）保持可发布，功能用短生命周期分支（≤2 天），频繁合并回主分支——小步快跑，避免长期分支的合并地狱。

**Save Point Pattern（存档点）**：像游戏存档一样命名提交点，任何时刻可回溯：
```bash
# 每个逻辑单元一个存档点(而不是攒一堆一起提交)
git commit -m "feat: 缓存清理 scan 命令"     # 一个功能=一个存档
git commit -m "fix: 修复空列表除零"          # 一个修复=一个存档
git tag savepoint/clean-scan                 # 关键节点打标, 回溯容易
git checkout savepoint/clean-scan            # 随时回到存档点
```

**Atomic Commits（原子提交）**：
- 一次提交只做一件事（一个 bug/一个功能/一个重构）
- 混合提交（"修 bug + 加功能 + 改格式"）= 无法回溯/无法 cherry-pick
- 提交前 `git diff` 自查：有没有混入无关改动？

### 第一步：检测文件变更
```bash
# 检查 Git 状态
git status

# 查看变更文件
git diff --name-only
```

### 第二步：添加文件
```bash
# 添加所有变更
git add .

# 或添加指定文件
git add <file1> <file2>
```

### 第三步：生成提交信息
根据变更内容自动生成提交信息：

```bash
# 提交信息格式
<type>: <description>

# 类型说明
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### 第四步：提交并推送
```bash
# 提交
git commit -m "提交信息"

# 推送
git push
```

## 示例

### 示例 1: 分析完成后自动提交
**触发**: 分析任务完成

**操作**:
1. 检测新生成的文件
2. 添加到 Git
3. 生成提交信息
4. 提交并推送

**提交信息示例**:
```
feat: 完成股票分析

- 分析 000657 中钨高新
- 生成三高股票筛选报告
- 保存到 Stock-Analysis 仓库
```

### 示例 2: 多仓库管理
**触发**: 需要提交到多个仓库

**操作**:
1. 识别文件所属仓库
2. 分别提交到对应仓库
3. 分别推送

**仓库示例**:
- Jarvis: 记忆、配置
- Stock-Analysis: 股票分析代码
- Amazon-Analyzer: 亚马逊运营工具

## 故障排除

### 错误 1: Git 未配置
**错误消息**: "Please tell me who you are"

**解决方案**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 错误 2: 推送失败
**错误消息**: "Authentication failed"

**解决方案**:
1. 检查 Git 凭据
2. 使用 Token 代替密码
3. 配置 SSH Key

### 错误 3: 冲突
**错误消息**: "CONFLICT (content)"

**解决方案**:
1. 查看冲突文件
2. 手动解决冲突
3. 标记为解决
   ```bash
   git add <resolved_file>
   ```
4. 完成提交
   ```bash
   git commit
   ```

## 最佳实践

### 提交频率
- 小改动：随时提交
- 大功能：功能完成后提交
- 每日结束：提交当日工作

### 提交信息
- 清晰简洁
- 使用现在时
- 首字母大写
- 不超过 50 字符

### 分支管理
- main/master: 主分支
- feature/*: 功能分支
- fix/*: 修复分支
- docs/*: 文档分支
