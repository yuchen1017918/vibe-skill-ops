---
name: hermes-skill-hub
description: 从 Skills Hub（clawhub/skills.sh/official/github 等）发现、评估、安装 skill 的标准工作流：search/inspect/install 精确语法、identifier 解析坑、安装前评估、安装后依赖验证。当用户说「找skill」「装skill」「部署skill」「查一下有没有好用的xxx skill」「搜索skill」时触发。
version: 1.2.0
metadata:
  category: devops
  capabilities:
    - Hub skill 搜索与预检（inspect）
    - identifier 与显示名解析
    - 安装前质量/依赖评估
    - 安装后 pip 依赖验证与脚本实测
    - 外部 GitHub 推荐清单真实性验证与精华提取
---

# Hermes Skill Hub 发现与部署

从 Hub 搜索、评估、安装 skill 的完整流程（v0.20.0 已验证）。
与 `skill-mcp-installer` 互补：本 skill 侧重「Hub skill 的搜索评估与安装验证」，MCP 安装流程见 skill-mcp-installer。

## 关键命令（已验证语法）

```bash
hermes skills search <query>                     # 默认搜全部来源
hermes skills search <query> --source clawhub --limit 20   # 指定来源
hermes skills inspect clawhub/<identifier>       # 安装前预检 SKILL.md 预览
hermes skills install "<显示名>" --yes           # 安装（--yes 跳过交互确认）
hermes skills list | grep <name>                 # 验证已安装
```

## 坑：identifier 与显示名

- search 结果里的 `identifier`（如 `a-stock-picker`）**不能直接**用于 inspect/install
- 裸 identifier 报错：`No exact match ... Did you mean one of these? <显示名> — <identifier>`
- 正确用法：**`source/identifier`**（如 `clawhub/a-stock-picker`）或 **中文显示名**（如 `"A股三层选股模型"`，含空格须加引号）
- `--all-sources` 参数**不存在**（v0.20.0 报 unrecognized arguments）→ 用 `--source all` 或直接省略（默认 all）
- `hermes skills install` 默认交互确认，卡在 `Confirm [y/N]` → 必须加 `--yes`

## 外部 GitHub 推荐清单评估（v1.1 新增 — 用户转发的社区推荐）

用户常转发一份"精选 skill 推荐"（含仓库链接/安装命令/描述/组合建议）。**整合前必须先验证真实性**——社区清单普遍含 404 幻觉链接或地址笔误（实测 7 个推荐：2 个地址错误：clone 命令 owner 与正文不一致、仓库 owner 笔误）。`"保证真实" 的措辞不可信`。

```bash
# 1. 批量验证仓库存在（无 token 即可，公开数据）
for repo in owner/repo1 owner/repo2 ...; do
  curl -s -m 10 "https://api.github.com/repos/$repo" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if 'full_name' in d else '❌ '+d.get('message',''))"
done

# 2. 交叉检查：安装命令里的 clone URL 是否与正文仓库 owner 一致（实测正文 mage0535、clone 却写 magicwe → 笔误）
# 3. 404 的推荐用搜索找真实仓库：https://api.github.com/search/repositories?q=<概念>+skill
#    （实测 headroom-skill：推荐 owner 404，搜到真实仓库 owner 不同但同名）
# 4. 顺带看目录结构确认 skill 清单与推荐描述一致（如 /contents/skills）
```

**评估输出（给用户的规划方案，用户说"先不要动手"时交付即停，等批准）**：
1. **验证表**：每个推荐 ✅/❌ + 地址纠错（含 star 数与真实描述）
2. **精华提取表**：来源 / 精华点 / 一句话价值——只提可借鉴的概念，不照抄实现
3. **优化方案表**：借鉴点 / 现有对应（先盘点自家 skill 是否已有同功能）/ 差距 / 优化动作 / 优先级（P1/P2/P3）
4. **明确"不吸收项 + 理由"**：平台特性（进程隔离、全自动 yolo）、与自家哲学冲突（如人工确认阈值）、规模不匹配、功能重复——避免为借鉴而借鉴

> 记忆教训：整合外部推荐前用 GitHub API 逐一验证（HTTP 200），勿直接相信"保证真实"的措辞。

## 外部 skill 集合 × 本地全家桶：重叠度对比 + 精华提取（v1.3 新增 — 实测 addyosmani/agent-skills 24 个）

用户拿外部知名 skill 集合（如 addyosmani/agent-skills、mattpocock/skills）问「哪些和全家桶重叠/哪些有用」时，**不要直接安装**。先做重叠度对比 + 精华提取（用户偏好：合并去重、最小侵入、三层渐进披露）：

1. **建立本地对照**：先 skill_view 全家桶 hub（vibe-coding-hub + dev-core/agent/infra/stack/ai-hub），列出「本地已有能力清单」（主流程/纪律/调试/测试/git/编排/搜索/治理/infra）
2. **批量拉取外部 SKILL.md 画像**：`curl https://api.github.com/repos/<owner>/<repo>/contents/skills` 拿目录清单 → 循环 curl raw 下载到 /tmp → 用脚本提取每个的 frontmatter description + `##/###` 标题结构（不逐篇精读，一次脚本出全貌）
3. **逐项分类**：每个外部 skill → ①重叠（本地有同类）②全新（本地没有）
4. **重叠项提精华**：只提取本地**没有**的精华点（例：五轴审查法/垂直切片/Hyrum's Law/Stop-the-Line Rule/Prove-It Pattern/Threat Model First），落地方案 = **patch 并入现有 skill，不新建文件**
5. **全新项定级**：P0（方法论级空缺，例：doubt-driven-development 对抗审查、context-engineering 上下文分层）→ 建议新增 L3；P1/P2（如 ADR/废弃迁移/上线就绪度）→ 精华并入现有 skill 或 references 挂载
6. **交付物**：对比表（重叠/精华/全新/价值分级）+ 落地方案，等用户批准再执行（用户说「先不要动手」时交付即停）

本会话实例（addyosmani/agent-skills 24 个 skill 的完整对比结论）见 `references/addyosmani-agent-skills.md`。

## 从 GitHub 直接安装（非 Hub 源）（v1.2 新增 — 实测 emilkowalski/skills）

部分高质量 skill 集合（如 skills.sh 生态的 emilkowalski/skills）不在 clawhub，`npx skills@latest add` 是 Claude 生态 CLI，Hermes 用不了。手动安装路径（2026-08 已验证）：

```bash
# 1. 评估：GitHub API 读 README + skills/ 目录清单，逐个 skill 读 SKILL.md 判断质量
#    （实测 emil-design-eng 27KB / animate 11.5KB / review-animations 8KB，全是可执行规则非空壳）

# 2. 下载：优先 curl raw.githubusercontent.com（git clone 国内网络常卡死，见下方坑）
BASE="https://raw.githubusercontent.com/<owner>/<repo>/main"
curl -sL -m 30 -o <name>_SKILL.md "$BASE/skills/<name>/SKILL.md"

# 3. 依赖文件必查：SKILL.md 里相对路径引用的 md（如 animate→RECIPES.md、
#    review-animations→STANDARDS.md）必须同目录拉取，否则加载后引用悬空。
#    用 GitHub API get_file_contents(path=skills/<name>) 列目录确认依赖清单

# 4. 安装位置：~/.hermes/skills/<category>/<name>/SKILL.md（与同族 skill 放一起，
#    UI/动效 → creative/；直接 cp 即可，无需 hermes skills install）

# 5. 校验：skills_list(category=...) 能见 + skill_view(name) 正常加载，确认依赖文件被关联

# 6. 完整性校验：curl 下载后 wc -c 与 GitHub API 返回的 size 字段比对（实测 5 文件全部一致）
```

**坑：管道吞掉 git 退出码** — `git clone ... 2>&1 | tail -5; echo "EXIT:$?"` 里 `$?` 是 `tail` 的退出码不是 git 的；clone 被网络卡死/timeout 杀掉时管道仍报成功（实测：输出 "Cloning into..." + EXIT:0，目录却不存在）。验证 git 结果用 `echo "${PIPESTATUS[0]}"` 或干脆不加管道。

**frontmatter 兼容性**：只要 name+description 即可被 Hermes 识别；Claude 生态额外字段（如 `disable-model-invocation: true`）被容忍不破坏解析（实测 review-animations 正常加载）。装完的 skill 是手动 cp 的（非 hub 安装），skill_manage 可正常修改。

本会话实例（emilkowalski/skills 安装清单与更新路径）见 `references/emilkowalski-skills.md`。

## 大型 skill 仓库批量安装（v1.4 新增 — 实测 Nutlope/hallmark 107 文件）

带重型 `references/` 知识库的 skill（hallmark 式：SKILL.md 只放流程+分发，细节全在 references/ 按需懒加载）**不能逐文件 curl**——用 codeload tarball 一次拉全，再整目录复制：

```bash
# 1. 下载整仓 tarball（git clone 国内网络卡死时此路可用，codeload 直连更稳）
cd /tmp && timeout 90 curl -sL -m 80 -o repo.tar.gz "https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main"
tar xzf repo.tar.gz          # 解出 <repo>-main/ 目录

# 2. 只提取 skill 目录（保留完整 references/ 树），整目录复制
rm -rf ~/.hermes/skills/<category>/<name>
cp -r /tmp/<repo>-main/skills/<name> ~/.hermes/skills/<category>/<name>

# 3. 校验：find 文件数 + du 体积 + skills_list 能见 + skill_view 的 linked_files 正确列出 references
```

**坑：重型懒加载 skill 必须整目录复制，禁止只拷 SKILL.md 或扁平化 references/**。
- 这类 skill（hallmark/addyosmani 风格）设计为 index-then-pick：SKILL.md 只写「读哪个 index → 只加载选中的那个文件」，references/ 下有子目录（macrostructures/components/genres/themes/verbs 等）
- 只拷 SKILL.md → 链接悬空，skill 加载报错；扁平化 references → 破坏懒加载索引结构
- 安装后验证 `skill_view` 的 linked_files 是否完整列出顶层 references 文件

**装完外部 skill 后对照本地 policy 补精华（闭环）**：hallmark 装完对照 frontend-design-policy 发现其缺 5 条可识别 AI 味（假 chrome 边框/斜体标题/编造指标/多余 section 编号/连续页面结构复用）+ 组件 8 态纪律 → 用 patch 最小改动补进 policy 并登记协作关系。外部 skill 的精华应回流本地 policy/skill，而不是只堆新文件。

本会话实例（Nutlope/hallmark 结构与设计质量线）见 `references/hallmark-skill.md`。

## 安装前评估（防装到垃圾/半成品）

1. `hermes skills inspect clawhub/<id>` 看 SKILL.md 预览：触发词、数据源、依赖、是否内嵌代码
2. **数据源国内可用性**（用户环境）：新浪/腾讯/东财/同花顺/AkShare 已验证可用；Yahoo/Google 系不稳 → 低优先
3. **依赖重量**：编排型 skill（依赖 N 个子 skill，如 a-stock-orchestrator 依赖 8 个）通常跳过；选功能单一的互补 skill
4. **与已有 skill 定位错开**（如已有实时监控 → 选选股/个股深研，形成闭环而非重复）

## 安装后依赖验证（防"装上但跑不了"）

```bash
# 1. grep SKILL.md 找 pip 依赖，逐个 import 验证；缺的用清华源装
python3 -c "import <pkg>" 2>&1
pip3 install <pkg> -q -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. SKILL.md 内嵌 Python 代码块 → 提取为 scripts/<name>.py
#    用真实调用实测（如个股采集传真实代码 600519）
python3 scripts/collect.py 600519

# 3. skill 引用的外部 skill 路径（如 ~/.agents/skills/xxx）不存在
#    → 把路径改指向本地提取脚本（patch 直接改 SKILL.md 文件）
```

## 注意

- **Hub 安装的 skill 受保护**：skill_manage 拒绝修改（not agent-created，created_by=None）；部署中确需修正文件（如改死路径）可用 `patch` 工具直接改 `~/.hermes/skills/<name>/SKILL.md`
- 本机 python 环境分裂：**系统 python3 = 3.10**，`pip3` 装包进 `~/.local/lib/python3.10`；**Hermes 本体 venv = hermes-env (3.11.15)**。skill 脚本一般用系统 python3 跑，依赖要装到 3.10
- Hub 安装的 skill 文件位于 `~/.hermes/skills/<name>/`，含 `_meta.json`（记录来源/哈希）
