---
name: vibe-code-search
description: 代码语义搜索 skill：大项目 vibe-coding 时不用把全部代码塞进上下文， 通过语义检索/结构化搜索定位目标代码。当项目规模大、需要找特定函数/类/ 报错相关代码时加载。覆盖内置搜索工具 + 真实可用的 MCP 代码搜索方案。 v1.1 新增：经验检索钩子——遇到报错/性能瓶颈时自动查全局经验库。
family-type: tool
family-version: 1.4.0
---

# 代码语义搜索（Vibe-Coding 版）

Vibe-coding 最大的坑：把整个项目塞进上下文，token 爆炸、上下文漂移。
正确姿势：**按需检索**，只把相关代码片段读入上下文。

## 一、内置工具优先（零依赖，先用这些）

| 需求 | 工具 | 示例 |
|------|------|------|
| 找文件名 | `search_files(target='files')` | `search_files(pattern='*utils*', target='files')` |
| 内容检索 | `search_files(pattern='...', target='content')` | 找函数名/报错关键字 |
| 读取文件 | `read_file(path, offset, limit)` | 分页读大文件 |
| 目录结构 | `search_files(target='files')` | 看项目结构 |

```python
# 找报错关键字在哪些文件出现
search_files(pattern="ModuleNotFoundError|ImportError", path="src/", output_mode="files_only")
# 找函数定义
search_files(pattern="def (parse|render|handle)", path="src/", file_glob="*.py")
```

## 二、大项目语义搜索（MCP 方案）

当内置 grep 不够（不知道关键词、跨语言、找相似实现）时，接入语义搜索 MCP。
**真实可用的开源方案**（经核查 GitHub 存在）：

| 项目 | 特点 | 接入方式 |
|------|------|----------|
| `zilliztech/claude-context` ⭐12k | Code search MCP for Claude Code，整库做上下文 | MCP stdio |
| `MinishLab/semble` ⭐5.8k | 快速代码搜索，比 grep+read 省 99% token | MCP stdio |
| `oraios/serena` ⭐27k | 语义检索 + 编辑的 MCP 工具包 | MCP stdio |
| `upstash/context7` ⭐60k | 代码文档检索，LLM/AI 编辑器用 | MCP/API |

接入方法：按 `hermes-mcp-setup` skill 在 `~/.hermes/config.yaml` 配置
`mcp.servers.<name>`，例如：

```yaml
mcp:
  servers:
    context7:
      command: npx
      args: ["-y", "@upstash/context7-mcp"]
```

> ⚠️ 网上流传的 `anthropics/mcp-code-search` 仓库经核查为 404 不存在，
> 用上表真实项目替代。

## 三、搜索策略（由轻到重）

```
1. 先 grep 关键字/文件名（内置工具，秒级）        ← 90% 场景够用
2. 再读目标文件上下文（read_file 分页）           ← 理解实现
3. 仍找不到 → 语义检索 MCP（context7/semble）     ← 大项目兜底
4. 最后才考虑全文读入（仅小项目 <1k 行）
```

## 四、Vibe-coding 上下文管理

- 单次读入上下文控制在项目总规模的 10% 以内。
- 用 `read_file(offset, limit)` 分页，不 `cat` 整个大文件。
- 每个文件读完做摘要笔记（写到 `docs/context-notes.md`），后续不再重读。
- 报错定位：先搜报错关键字所在文件，再读周边代码。

## 五、整仓打包与外部文档（v1.4 新增 — claudekit repomix/docs-seeker 精华）

检索的反面是**打包**：有些场景不需要"找"，需要"整个喂给另一个 agent"。

### 整仓打包送子 agent（Repomix 模式）

`delegate_task` 子 agent 无会话历史，需要完整项目上下文时，别让子 agent 自己漫游文件系统——先打包：

```bash
# 方案 A: Repomix CLI（npx，无需全局安装）
npx repomix --output /tmp/proj.xml --include "src/**,*.md" --exclude "node_modules,dist" /path/to/proj
# 方案 B: 轻量自制（<50 文件的小仓/子目录）
find src -name "*.py" -exec sh -c 'echo "===== $1 ====="; cat "$1"' _ {} \; > /tmp/proj-bundle.txt
```

要点：
- **格式**：XML 保留文件结构（AI 解析最稳）> Markdown > 纯文本
- **token 意识**：打包后先 `wc -c` 估 token（约 字符数/4），超 50K 先裁子目录
- **粒度**：只打包任务相关子目录 + 关键配置，不要全仓（node_modules 必排除）
- **场景**：委派大任务给子 agent、跨项目问"这个项目怎么做的"

### 外部文档搜索（llms.txt 标准）

查最新库/框架文档，**先试 `<site>/llms.txt`**（2025 年起的 LLM 友好文档索引标准，直出 markdown）：

```bash
curl -sL https://docs.astral.sh/llms.txt | head -50   # 类库文档索引
curl -sL https://nextjs.org/llms.txt                  # 框架文档
# 无 llms.txt 时降级: sitemap.xml → 找 docs 子域 → 常规搜索
```

优先级：官方 llms.txt > sitemap 定位文档页 > web_search。抓回来的文档同样按 §四 控制在 10% 上下文预算内。

## 六、经验检索钩子（v1.1 新增）

**目的**：让 global-experience 从"被动记录"变为"主动召回"——遇到问题时自动查经验库。

### 触发时机（自动）

| 触发场景 | 检索动作 |
|----------|----------|
| 报错（运行时报错/测试失败） | 用错误关键词检索经验库 |
| 性能瓶颈 | 用性能相关关键词检索 |
| 重复模式（似曾相识的代码） | 检索成功模式 |
| 技术选型 | 检索技术域经验 |

### 检索命令

```bash
# 按关键词检索（排除归档）
grep -rn "<关键词>" ~/.hermes/experience/ 2>/dev/null | grep -v archive/

# 命中后按 effectiveness_score 排序（高分优先）
grep -H "effectiveness_score" <命中文件> | sort -t: -k2 -rn
```

### 召回评分与过滤（v1.3 升级 — 防上下文污染）

**三维评分**（检索命中后排序）：

```
score = 0.4×文本匹配度 + 0.3×时效衰减 + 0.2×验证次数 + 0.1×作者信誉
- 文本匹配度：报错信息/关键词 与经验标题/标签的相似度（0~1）
- 时效衰减：越新越高（30 天内 1.0，每 90 天衰减 0.1，下限 0.3）
- 验证次数：成功复用次数（cap 5 次）
- 作者信誉：经验作者的历史被验证率（默认 0.5）
```

**召回后过滤**（严格）：
- 只注入 score > 0.7 的经验（低分不注入，仅记录）
- 最多注入 2 条，且必须来自不同 category（防同类型重复）
- 注入前缀："【经验召回】以下经验可能相关，仅供参考："

### 注入流程

```
1. 遇到报错/瓶颈 → 提取 2-3 个关键词
2. 检索经验库（上述命令）
3. 按三维评分排序，过滤 score > 0.7，取 Top 2（不同 category）
4. 注入上下文（带"仅供参考"前缀）
5. 未命中 → 解决问题后按 global-experience 沉淀（让下次受益）
6. 低分经验（score < 0.3）→ 不采用，标记"低分经验，仅供参考"
```

### 与 global-experience 分工

| 层 | 负责 |
|----|------|
| `global-experience` | 经验**记录**：模板/评分/归档 |
| `vibe-code-search` | 经验**召回**：触发/检索/注入（本钩子） |

> 排查顺序：先查项目快照（snapshot-notes）→ 再查全局经验库（本钩子）→ 最后才从头解决。

## 快速排障

| 症状 | 处理 |
|------|------|
| grep 不到但明明存在 | 可能是编码/大小写，加 `-i` 或搜子串 |
| 搜索太慢 | 限制 path 到 src/，排除 node_modules/build |
| 需要理解整个模块 | 先看入口文件 + README，再跟 import 链 |
