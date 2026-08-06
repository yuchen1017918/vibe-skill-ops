---
name: china-env-adapt
description: |
  国内环境实战适配 skill：镜像源自动检测与切换（pip/npm/maven/docker）、
  网络超时重试策略（针对国内 CDN 不稳定）、合规性检查
  （敏感词/数据出境/开源协议）。作为 project-scaffold 的可选子模块，
  当用户在国内网络环境开发、pip/npm 安装超时、docker pull 失败、
  或需要合规检查时加载。触发词：国内、镜像、超时、换源、合规。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    type: tool
    tags: [vibe-coding, china, mirror, network, compliance, proxy]
    related_skills: [vibe-coding-hub, project-scaffold, china-cloud-gpu, china-mcp-services, dev-infra-hub]
---

# 国内环境实战适配（China Env Adapt）

**核心问题**：国内网络访问海外源不稳定（pip/npm/docker/github），下载超时、失败率高。
**方案**：自动检测与切换镜像源 + 超时重试策略 + 合规检查。作为 `project-scaffold` 的可选子模块。

## 1️⃣ 镜像源速查表

### pip（Python）
```bash
# 阿里云（推荐，国内最快）
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# 清华
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
# 中科大
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/

# 单次使用
pip install <pkg> -i https://mirrors.aliyun.com/pypi/simple/
```

### npm（Node）
```bash
# 淘宝镜像（npmmirror）
npm config set registry https://registry.npmmirror.com
# 验证
npm config get registry
```

### Maven（Java）
```xml
<!-- ~/.m2/settings.xml 或项目 pom.xml -->
<mirror>
  <id>aliyun</id>
  <mirrorOf>central</mirrorOf>
  <url>https://maven.aliyun.com/repository/central</url>
</mirror>
```

### Docker
```bash
# /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
# 生效
sudo systemctl restart docker
```

### Git/GitHub（clone 加速）
```bash
# ghproxy 镜像（README/下载场景）
git clone https://ghproxy.net/https://github.com/<owner>/<repo>.git
# 或直接走镜像站
git clone https://gitclone.com/github.com/<owner>/<repo>.git
```

### HuggingFace（模型下载）
```bash
# 环境变量指向 hf-mirror
export HF_ENDPOINT=https://hf-mirror.com
```

## 2️⃣ 自动检测与切换流程

```
1. 检测当前源状态：
   pip config get global.index-url
   npm config get registry
   cat /etc/docker/daemon.json 2>/dev/null | grep registry-mirrors
2. 判断是否国内环境：
   - 默认源访问超时（>10s）或失败 → 判定为国内网络
   - 或用户明确告知国内环境
3. 按需切换：
   - 安装失败 → 切镜像源重试
   - docker pull 失败 → 切 registry-mirrors
   - git clone 超时 → 用 ghproxy 前缀
4. 记录切换结果（写入项目 .snapshots/ 或全局经验库）
```

## 3️⃣ 网络超时重试策略

| 场景 | 策略 |
|------|------|
| 单次命令超时 | 重试 3 次，间隔 3s/5s/10s（递增退避） |
| 大文件下载（模型/镜像） | 断点续传优先（wget -c / aria2），超时上限 300s |
| 持续失败（3 次全败） | 切换镜像源 → 重试 → 仍失败则提示用户手动处理 |
| 下载速度慢 | 换更优镜像（阿里→清华→中科大轮换测试） |
| SSL 证书错误 | 检查系统时间（常见！date 错误导致证书验证失败） |

```bash
# 超时重试示例（pip）
for i in 1 2 3; do
  pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && break
  echo "第 $i 次失败，3s 后重试"; sleep 3
done

# 大文件断点续传（wget）
wget -c --timeout=60 --tries=5 https://.../model.bin
```

## 4️⃣ 合规性检查（上线前）

### 敏感词检查
```bash
# 扫描代码/文档中的敏感词（示例关键词表）
grep -rnE "敏感词1|敏感词2|违禁词" src/ docs/ README.md 2>/dev/null
```
> 合规检查点：政治敏感/违法内容/版权侵权/隐私泄露（真实信息脱敏）

### 数据出境检查
| 检查项 | 动作 |
|--------|------|
| 用户数据是否发送到境外服务器 | 确认 API 端点位置 |
| 是否使用境外云服务存数据 | 评估合规风险（个保法） |
| 跨境传输是否加密 | 必须 TLS，敏感数据需评估 |

### 开源协议检查
```bash
# 检查项目依赖的许可证
pip-licenses / license-checker / go-licenses
# 确认：MIT/Apache-2.0/BSD 可商用；GPL 需开源衍生代码
```

### 合规输出
```markdown
# 合规检查报告
- 敏感词：✅ 通过 / ⚠️ 发现 N 处（已修复）
- 数据出境：✅ 无跨境传输 / ⚠️ 需评估
- 开源协议：✅ 全部兼容 / ⚠️ GPL 依赖需注意
- 结论：✅ 可上线 / ⚠️ 需处理后再上线
```

## 5️⃣ 与全家桶衔接

| Skill | 协作关系 |
|-------|----------|
| `project-scaffold` | **作为其可选子模块**：初始化项目时自动检测国内环境并配置镜像源 |
| `china-cloud-gpu` | 国内 GPU 租赁 + AI 生成 API（本 skill 管网络层，它管算力层） |
| `china-mcp-services` | 国内可用 MCP 服务（本 skill 管镜像/网络，它管服务配置） |
| `vibe-terminal-safe` | 命令执行安全（镜像源切换属于 🟡 受限操作，需授权） |
| `rollback-backup` | 合规检查通过后才发布，发布失败回滚 |
| `global-experience` | 换源/重试经验可沉淀到全局经验库 |

## ⚠️ 核心原则

1. **先测后换**：不是所有环境都慢，先测当前源再决定是否切换。
2. **最小改动**：只改出问题的源，不全局替换（如只给单次命令加 -i）。
3. **镜像有风险**：非官方镜像可能滞后/被篡改，生产环境优先官方源 + 校验 hash。
4. **记录备查**：换源决策记录到 .snapshots/，方便回滚。

## 快速排障

| 症状 | 处理 |
|------|------|
| pip 安装超时 | 切阿里云源重试（§1） |
| npm install 卡住 | 切 npmmirror（§1） |
| docker pull 失败 | 配置 registry-mirrors（§1） |
| git clone 超时 | ghproxy 前缀（§1） |
| 下载到一半断了 | wget -c 断点续传（§3） |
| SSL 证书报错 | 检查系统时间（date） |
| 换源后仍失败 | 换另一个源轮换测试；或检查代理设置 |
