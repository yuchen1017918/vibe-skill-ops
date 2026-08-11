# emilkowalski/skills — 已安装来源清单

来源：https://github.com/emilkowalski/skills
作者：Emil Kowalski（Vercel 设计工程师 / Sonner、Vaul 库作者，animations.dev）
安装：2026-08-11，curl raw.githubusercontent.com 手动安装（非 hub 安装，skill_manage 可改）

## 已安装（creative/ 分类）

| skill | 位置 | 文件 | 说明 |
| --- | --- | --- | --- |
| emil-design-eng | creative/emil-design-eng/ | SKILL.md (27KB) | UI 打磨哲学主技能（动画决策框架/组件细节/审查清单） |
| animate | creative/animate/ | SKILL.md (11.5KB) + RECIPES.md (8KB) | 动画构建 7 步决策序列，13 个现成配方（按钮/下拉/tooltip/modal/drawer/toast 等） |
| review-animations | creative/review-animations/ | SKILL.md (8KB) + STANDARDS.md (9.8KB) | 10 条硬标准严格审查，强制 Before/After/Why 表格 + Block/Approve 结论 |

## 仓库其余未装（按需再拉）

- **apple-design** — 苹果 WWDC 设计原则 → web（13KB 级）
- **animation-vocabulary** — 动效术语反查表（13KB，独立无依赖，最值得补）
- improve-animations / find-animation-opportunities — 代码库级动画审计/机会发现
- pick-ui-library / prototype / ask-sonner — React 生态选型与 Sonner 指南（对非 React 用户价值低）

## 更新方法

```bash
BASE="https://raw.githubusercontent.com/emilkowalski/skills/main"
curl -sL -m 30 -o /tmp/x_SKILL.md "$BASE/skills/<name>/SKILL.md"  # 依赖文件（RECIPES.md 等）同理
# 先 wc -c 与 GitHub API size 字段比对，一致后 cp 覆盖 ~/.hermes/skills/creative/<name>/
# 用 GitHub API get_file_contents(path=skills/<name>) 确认依赖文件清单
```

## 要点

- frontmatter 仅 name+description 即兼容 Hermes；Claude 生态额外字段（disable-model-invocation: true）被容忍（实测正常加载）
- 三个 skill 协同：animate 写 → review-animations 审 → emil-design-eng 底层哲学；与 frontend-design-policy（防 AI 味）互补不冲突
