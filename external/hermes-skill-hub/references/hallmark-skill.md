# Nutlope/hallmark — 已安装来源清单

来源：https://github.com/Nutlope/hallmark
作者：Hassan El Mghari（Nutlope，知名 AI 开发者），Together AI 出品
Star：11.1k+（2026-08），MIT 协议
安装：2026-08-11，codeload tarball 整仓下载后提取 skills/hallmark/（非 hub 安装，skill_manage 可改）

## 已安装（creative/ 分类）

位置：`~/.hermes/skills/creative/hallmark/`（107 文件、976KB）
- `SKILL.md`（67KB）：主流程——设计上下文门禁 → genre 检测 → 宏结构选择 → 主题轮换 → 懒加载规则集 → preview → build → 58 门禁 slop test
- `references/`（24 个顶层规则文件 + 5 个子目录）：
  - 顶层：typography / color / motion / layout-and-space / copy / anti-patterns / slop-test（58 门禁）/ microinteractions / interaction-and-states（8 态）/ responsive / structure / component-cookbook（50 组件原型索引）/ macrostructures（21 宏结构索引）/ custom-theme / design-md / export-formats / contract / assets / hero-enrichment / custom-craft / imagery-kit / preview-examples / floating-nav / study
  - 子目录：macrostructures/（21 个单宏文件）、components/（组件原型）、genres/（editorial / modern-minimal / atmospheric / playful）、themes/（主题规格）、verbs/（audit / redesign）

## 核心机制（评估要点速查）

| 机制 | 说明 |
| --- | --- |
| 四个动词 | `default`（新建）/ `audit`（打分不编辑）/ `redesign`（边界内重设计）/ `study`（从 URL/截图提取设计 DNA，不抄像素） |
| 58 个 slop-test 门禁 | 交付前逐项检查（假 chrome 边框、编造指标、斜体标题、transition:all、Inter 默认字体…） |
| 21 命名主题 + 21 宏结构 | catalog 轮换；主题三轴（paper band / display style / accent hue）强制相邻输出至少一轴不同 |
| 多样化规则 | 读 `.hallmark/log.json` 项目记忆，宏结构/主题/导航原型连续不重样——防"模板换皮" |
| 六轴自批判 | 交付前 P/H/E/S/R/V 打 1-5 分，<3 强制重做，stamp 进 CSS 注释 |
| 设计上下文门禁 | 必问 Audience/Use case/Tone（"干净现代"不算 tone） |
| 8 态纪律 | 交互组件必须覆盖 default/hover/focus-visible/active/disabled/loading/error/success + 8 态 demo 页验证 |

## 与全家桶协作（设计质量线）

| 层 | 工具 | 职责 |
| --- | --- | --- |
| 持续约束 | frontend-design-policy | 每次生成自动自查，防跑偏（已补 hallmark 精华：5 条新 AI 味识别项 + 8 态纪律 + 协作登记） |
| 重型执行 | hallmark | 新建/审计/重设计/提取 DNA，反模板完整工作流 |
| 动效细节 | emil-design-eng + animate + review-animations | 缓动/时长/物理 |
| 参考库 | popular-web-designs | 54 套真实设计系统 |

## 使用姿势（Hermes 适配）

- 说「用 hallmark 设计落地页」→ 会先问 Audience/Use case/Tone（可回 "go ahead" 让它推断并明示推断结论）
- 「hallmark audit <目标>」→ 反模式清单打分，不改代码
- 「hallmark study <截图/URL>」→ 提取 DNA 复用结构不抄像素；URL 模式原设计用 WebFetch，Hermes 用 web_extract 代替
- `study` 的 design.md 输出有安全护栏：URL 模式需 attestation（来源是用户自己的/公开参考才可落盘）

## 更新方法

```bash
cd /tmp && timeout 90 curl -sL -m 80 -o hallmark.tar.gz "https://codeload.github.com/Nutlope/hallmark/tar.gz/refs/heads/main"
tar xzf hallmark.tar.gz
rm -rf ~/.hermes/skills/creative/hallmark
cp -r /tmp/hallmark-main/skills/hallmark ~/.hermes/skills/creative/hallmark
```

## 坑

- 仓库根有 `site/`（演示站，17MB tarball 的一部分）——只提取 `skills/hallmark/`，不要整仓铺进技能库
- SKILL.md 里 `../../site/css/tokens.css` 等引用是给人看的注释，装进 Hermes 后无实际作用，不影响功能
- frontmatter 是 name/description/version 三字段，Hermes 兼容（skill_view 验证通过，setup_needed=false）
