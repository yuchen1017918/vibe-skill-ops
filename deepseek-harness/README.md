# Vibe-Skill-Ops — DeepSeek Harness 适配版

本目录是 [Vibe-Skill-Ops 全家桶](https://github.com/yuchen1017918/vibe-skill-ops) 的 **DeepSeek Harness (dsh) 格式适配版**。

由 `scripts/convert-dsh.py` 从 Hermes 版自动生成(单一真相源,改动 Hermes 版后重跑脚本即同步)。

## 格式差异(依据 deepseek-ai/deepseek-harness 官方文档 docs/subsystems/skills.zh.md)

| 项目 | Hermes 版 | DeepSeek Harness 版 |
|------|-----------|---------------------|
| frontmatter | `metadata.hermes.type` + 自定义字段 | `name` + `description`(DSH 只认这两个路由字段) |
| description | 无长度限制 | **≤500 字符**(catalogDescriptionMaxLength 默认 500) |
| 附加信息 | 完整保留 | 压缩为 `family-type` / `family-version`(DSH 解析为 metadata,不影响) |
| deprecated | 文件保留防交叉引用 | **不转换**(8 个 deprecated 已排除) |
| 正文 | 原样 | 原样(DSH 全文加载) |
| 资源目录 | references/scripts/templates/assets | 一并拷贝 |

**DSH 版共 37 个 skill**(30 L3 + 6 hub + 1 user-workflows 层),全部 description 单行化 + ≤500 字符。

## 安装

### 用户级(所有项目可用)

```bash
# 方式一: ~/.agents/skills/ (rank 500, agentsHome)
mkdir -p ~/.agents/skills
cp -r deepseek-harness/vibe-coding-family/* ~/.agents/skills/

# 方式二: ~/.dsh/skills/ (rank 400, dshHome)
mkdir -p ~/.dsh/skills
cp -r deepseek-harness/vibe-coding-family/* ~/.dsh/skills/
```

### 项目级(仅当前项目)

```bash
mkdir -p .agents/skills    # rank 200, 优先于用户级
cp -r deepseek-harness/vibe-coding-family/* .agents/skills/
```

### 发现优先级(rank 越小越优先)

```
100  <projectRoot>/.dsh/skills
200  <projectRoot>/.agents/skills
300  Config.customSkillDirs
400  <dshHome>/skills        (~/.dsh/skills)
500  <agentsHome>/skills     (~/.agents/skills)
600  bundled
```

## 与 Hermes 版的行为差异(重要)

1. **没有 hub 自动路由**:DSH 模型每一步都会看到所有 skill 的 `name` + `description`,由模型自行选择加载(DSH 的 `skill({ name })` 工具)。所以 DSH 版把路由信息全部压进了 description(触发词保留)。`vibe-coding-hub` 仍作为一个普通 skill 存在,但其"自动加载"职责由 DSH 的目录机制替代。
2. **policy 类 skill 变为按需加载**:Hermes 版里 policy(纪律/设计约束)会在相关时自动注入;DSH 没有注入机制,模型需要时自己加载。description 已注明"当写代码时应用"等触发场景。
3. **调用策略**(可选,默认全开):如需限制,在 frontmatter 加:
   ```yaml
   disable-model-invocation: true   # 模型不可调用(仅用户 / 命令)
   user-invocable: false            # 用户不可调用(仅模型)
   ```
4. **meta 类 skill**(fallback-general-dev / vibe-skills-gov-patterns):DSH 无 meta 概念,保留为普通 skill。

## 重新生成

```bash
python3 scripts/convert-dsh.py ~/.hermes/skills/vibe-coding-family deepseek-harness/vibe-coding-family
```

## 官方文档参考

- DeepSeek Harness: https://github.com/deepseek-ai/deepseek-harness
- Skills 子系统规范: `docs/subsystems/skills.md`(或 skills.zh.md)
- 官网: https://deepseek.com/harness
