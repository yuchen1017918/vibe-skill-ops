# Vibe-Skill-Ops 全家桶安装教程（Agent 版）

> 本教程写给 **AI Agent**（Hermes Agent / Claude Code / Codex / 其他支持 skill 目录的 Agent）。
> 目标：把 vibe-coding skill 全家桶（**v1.3.0,36 个活跃 skill**）安装到目标 Agent 的 skill 目录。
>
> 用户可以直接把下面的提示词发给 Agent，Agent 会按本教程执行：
> `请参考 https://yuchen1017918.github.io/vibe-skill-ops/Tutorial.md，帮我下载并安装这个 vibe-coding skill 全家桶。`
> （GitHub Pages 未启用前，用 raw 地址：`https://raw.githubusercontent.com/yuchen1017918/vibe-skill-ops/main/Tutorial.md`）

---

## 一、这是什么

`vibe-coding-family` 是运行在 Hermes Agent 上的**自治理 Vibe Coding skill 体系**（v1.1.0 正式版）：

- **四层组织路由**：L1 组织形态（团队/企业）→ L2 开发模式（助手/全盘）→ L3 四格场景 → L4 执行 skill
- **大道至简**：token × 质量乘积最优——合并 3 组重叠 skill、契约层 ≤5 行、一句话画像路由、30 天未加载自动 deprecated
- **核心机制**：复杂度 Triage、确认交互契约（Confirmation SLA）、介入深度 L0-L4、升降天花板、证据消费、知识萃取、成本治理
- **形态**：全部是标准 Markdown SKILL.md（带 YAML frontmatter），**不是可执行程序**
- **规模**：6 个目录 skill + 22 个 L3 skill = **28 个路由内 skill**；另附 6 个 deprecated 保留文件（防交叉引用,不进路由,可安全忽略）

> 安装后用户使用：发需求 → Agent 按触发词加载 hub → 四层路由（一句话画像）→ 落到具体 skill 流程。

## 二、安装前置条件

- Agent 平台支持 `~/.hermes/skills/` 目录结构（Hermes Agent 原生支持）
- 目标目录存在：`mkdir -p ~/.hermes/skills`（没有就创建）
- 网络可访问 `github.com`（国内环境可用 ghproxy 加速，见 §五）

## 三、下载安装（3 步）

### 方式 A：git clone（推荐）

```bash
# 1. 下载仓库
git clone https://github.com/yuchen1017918/vibe-skill-ops.git /tmp/vibe-skill-ops

# 2. 复制全家桶到 skills 目录（注意是 vibe-coding-family 子目录,整目录复制含 deprecated 保留文件）
mkdir -p ~/.hermes/skills
cp -r /tmp/vibe-skill-ops/vibe-coding-family ~/.hermes/skills/

# 3. 验证
ls ~/.hermes/skills/vibe-coding-family/                          # 44 个 SKILL.md（36 活跃 = 30 路由内 + 6 hub，8 个 deprecated 描述带 ⚠️ 标注）
find ~/.hermes/skills/vibe-coding-family -name SKILL.md | wc -l   # 应为 44
```

### 方式 B：下载 zip（无 git 环境）

```bash
cd /tmp
curl -L -o vibe-skill-ops.zip https://github.com/yuchen1017918/vibe-skill-ops/archive/refs/heads/main.zip
unzip -o vibe-skill-ops.zip
mkdir -p ~/.hermes/skills
cp -r /tmp/vibe-skill-ops-main/vibe-coding-family ~/.hermes/skills/
# 验证同上
```

## 四、验证安装（必须做）

1. **目录完整**：44 个 `SKILL.md`（上一步 wc -l 应为 44；其中 30 个在路由内、6 个 hub、8 个 deprecated 描述带 ⚠️ 标注）
2. **frontmatter 合法**：每个 SKILL.md 开头有 `---` 包裹的 YAML（name / description / version / metadata.hermes.type）
3. **Agent 识别**：重启会话后，技能列表出现 `vibe-coding-hub` 及 30 个路由内 skill（Hermes 用 `skills_list` 查看）
4. **自检**：加载 `vibe-coding-hub`，应看到「L1 总目录 v1.1.0 — 四层组织路由」

**未通过验证 → 不要声称安装成功**，先看 §六 排障。

## 五、国内网络加速

```bash
# git clone 慢 → ghproxy 前缀
git clone https://ghproxy.net/https://github.com/yuchen1017918/vibe-skill-ops.git /tmp/vibe-skill-ops

# 或 zip 走镜像
curl -L -o vibe-skill-ops.zip https://ghproxy.net/https://github.com/yuchen1017918/vibe-skill-ops/archive/refs/heads/main.zip
```

## 六、常见故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| 技能列表没有新 skill | 目录位置不对 / 未重启会话 | 确认复制到 `~/.hermes/skills/vibe-coding-family`；重启会话 |
| skill 加载报 frontmatter 解析失败 | 复制损坏 / 编码问题 | 重新 clone；确认文件 UTF-8 编码 |
| 与旧版重名冲突 | 之前装过旧版本 | 先 `rm -rf ~/.hermes/skills/vibe-coding-family` 再装 |
| 版本过旧 | 仓库已更新 | 重新执行 §三 覆盖（自定义修改先备份） |
| clone 超时 | 国内网络 | 用 §五 镜像前缀 |
| deprecated skill 被加载 | 触发词命中保留文件 | 无碍：description 首行 ⚠️ 标注指向替代 skill,Agent 会自动转正 |

## 七、安装完成后第一件事（Agent 必做）

1. 读取 L1 总目录：`vibe-coding-hub` 的 SKILL.md
2. 向用户说明：**「全家桶 v1.1.0 安装完成，共 28 个路由内 skill，可以开始 vibe coding 了」**
3. 提示用户可查看网页版介绍：`https://yuchen1017918.github.io/vibe-skill-ops/`

## 八、更新与卸载

```bash
# 更新（覆盖式）
cd /tmp/vibe-skill-ops && git pull
cp -r vibe-coding-family ~/.hermes/skills/

# 卸载
rm -rf ~/.hermes/skills/vibe-coding-family
```

---

*本仓库：https://github.com/yuchen1017918/vibe-skill-ops · MIT License · v1.1.0*
