# DeepSeek Harness (dsh) Skill 格式规范与转换

来源:官方仓库 `deepseek-ai/deepseek-harness`(2026-08-13 开源, Cordis 插件体系,"一切皆插件")
官方文档: `docs/subsystems/skills.zh.md`(中文) / `skills.md`(英文), 本地 clone 在 /tmp/dsh。

## 官方格式要点(转换依据)

| 项 | 规范 | 对全家桶的影响 |
|----|------|---------------|
| frontmatter | 只需 `name` + `description`;其他键解析为 metadata(无害) | `metadata.hermes` 可删可留, 建议替换为 `family-type`/`family-version` |
| name | kebab-case `^[a-z0-9]+(?:-[a-z0-9]+)*$` | 全家桶已合规 |
| description | 模型路由文本, **≤500 字符**(`catalogDescriptionMaxLength` 默认 500, 最小值 3);单行最优 | 全家桶 19 个超限(原最长 928) |
| 调用策略 | `disable-model-invocation: true`(模型不可调)/ `user-invocable: false`(用户不可调), 省略默认全开 | 默认不需要加 |
| 目录形式 | `<name>/SKILL.md`(目录包) 或 `<name>.md`(扁平) | 用目录包, 可带 references/scripts/assets |
| 资源 | resourceBase 按需解析, 不枚举目录 | references/scripts 一并拷贝即可 |

## 发现路径(rank 越小越优先)

```
100  <projectRoot>/.dsh/skills          # 项目级最高优先
200  <projectRoot>/.agents/skills
300  Config.customSkillDirs
400  <dshHome>/skills    (~/.dsh/skills)
500  <agentsHome>/skills (~/.agents/skills)
600  bundled
```

安装: `mkdir -p ~/.agents/skills && cp -r deepseek-harness/vibe-coding-family/* ~/.agents/skills/`
(注意: Deep Code 等工具也用 `~/.agents/skills` —— 一处安装多工具可见)

## 行为差异(Hermes vs dsh, 写入 README-dsh 的关键)

1. **无 hub 自动路由**: dsh 模型每步看到全部 skill 的 name+description, 自己选; `skill({ name })` 工具全文加载
   → 路由信息必须全部压进 description(触发词保留), hub 变成普通 skill
2. **无 policy 注入机制**: 纪律/设计约束类 skill 变"按需加载"(模型需要时自己调)
3. **meta 类无概念**: fallback-general-dev 等保留为普通 skill

## convert-dsh.py 转换规则(已在仓库 scripts/)

- description 压缩: 超 500 时保留 首句 + 触发词(前 200) + 负触发词(前 100) + type, `；` 拼接, 超限截断加 `…`
- **始终单行化**(`re.sub(r"\s+", " ")`)—— 即使 ≤500 也压缩换行, 目录 XML 转义渲染更干净
- deprecated 判断: 读 SKILL.md 前 800 字符含 "deprecated" 即跳过
- 附加 `family-type` / `family-version` frontmatter 键(DSH 解析为 metadata, 不报错)

## 开发坑(实测踩中)

1. **deprecated 判断必须在 makedirs 之前** —— 先建目录再 return None 会留空目录
2. **description 提取用正则** `re.search(r"description:\s*\|?\s*(.*?)(?=\n[a-z-]+:|\n---)", text, re.S)`
   —— 嵌套 YAML(frontmatter 里的 metadata 块)会把 `metadata:` 后的内容误并入 description, 必须从原文整体提取再压缩
3. **校验脚本**: name 与目录名一致 + kebab-case + description 单行 ≤500 + 无 deprecated 残留 + 正文 ≥100 字符
4. 复杂 shell 命令(含 `$(find)` 命令替换 + for 循环)会被 Hermes 安全拦截(exit -1 无输出)
   → 改用 execute_code Python 校验或 search_files/read_file 分步验证
5. 实测转换结果: 36 active(29 L3 + 6 hub + 1) + 跳过 8 deprecated, 最长 description 257 字符

## 上游资源

- 官网: https://deepseek.com/harness (developer preview, 中英)
- GitHub: https://github.com/deepseek-ai/deepseek-harness
- 生态: 0xsline/awesome-deepseek-harness、awesome-dsh-plugin/awesome-dsh-plugin(插件精选)
- Deep Code(@vegamo/deepcode-cli): 官方 API 文档确认支持 Agent Skills, 路径 `~/.agents/skills` + `./.deepcode/skills`
