---
name: dev-ai-hub
description: 全家桶 L2 目录 — AI/ML 开发层。覆盖：模型训练/微调、推理部署、 提示词工程、RAG、音频/图像/语音模型、评估。当项目涉及 AI/ML 功能（训练模型、本地推理、RAG、LLM 应用）时， 先加载本目录定位对应 L3 skill。
family-type: tool
family-version: 1.0.0
---

# AI/ML 开发层（L2 目录）

承接 `vibe-coding-hub`（L1）。本层管**AI/ML 开发**：从模型获取、训练微调、
推理部署、到 LLM 应用开发。具体细节在 L3 skill 里，这里只做路由。

## 🧱 边界声明（v1.1 — 我管什么 / 不管什么）

- ✅ **管**：模型获取、训练/微调、推理部署、LLM 应用开发、多模态
- ❌ **不管**：普通业务编码 → `dev-core-hub`；技术栈常规开发 → `dev-stack-hub`；模型服务的基础设施运维 → `dev-infra-hub`
- 🔄 **协作点**：微调/推理产出的模型接入应用 → `dev-stack-hub` / `dev-core-hub`；GPU/部署 → `dev-infra-hub`

## 🧭 子层路由

### 模型获取与数据集
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `mlops/huggingface-hub` | hf CLI：搜索/下载/上传模型与数据集 | 找模型/数据（主） |

### 训练与微调
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `mlops/training/axolotl` | YAML 配置 LLM 微调（LoRA/DPO/GRPO） | 微调开源模型 |
| `mlops/training/trl-fine-tuning` | TRL：SFT/DPO/PPO/GRPO/奖励建模 | RLHF 全流程 |
| `mlops/training/unsloth` | 2-5x 加速 LoRA/QLoRA 微调，省显存 | 显存受限微调 |
| `mlops/evaluation/weights-and-biases` | W&B：实验日志/扫描/模型注册表 | 实验追踪 |
| `mlops/evaluation/lm-evaluation-harness` | lm-eval-harness：MMLU/GSM8K 基准评测 | 模型评测 |

### 推理与部署
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `mlops/inference/vllm` | vLLM 高吞吐推理 + OpenAI API + 量化 | 服务化部署（主） |
| `mlops/inference/llama-cpp` | llama.cpp 本地 GGUF 推理 | 本地小模型 |
| `mlops/inference/outlines` | 结构化 JSON/regex/Pydantic 输出 | 约束生成 |
| `mlops/inference/obliteratus` | abliterate 模型拒绝行为 | 模型行为调整 |

### LLM 应用开发
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `mlops/prompt-engineering` | 结构化提示词/少样本/思维链/RAG 技术 | LLM 应用（主） |
| `mlops/offline-rag-pipeline` | 离线 RAG：本地 embedding + 向量库 | 本地知识库 | 
| `research/llm-wiki` | Karpathy LLM Wiki：编译型知识库（raw 源+知识页+SCHEMA/index/log 导航，非 RAG） | 研究知识库/领域笔记（主） |
| `mlops/instructor` | Pydantic 校验的 LLM 结构化抽取 | 数据抽取 |
| `mlops/research/dspy` | DSPy 声明式 LM 程序 + 自动优化 | 复杂 LM 流程 |
| `mlops/ollama-project-dev` | Ollama 项目开发/调试/审计/重构 | Ollama 应用 |

### 多模态模型
| Skill | 作用 | 加载时机 |
|-------|------|----------|
| `mlops/models/audiocraft` | MusicGen 文生乐 / AudioGen 文生声 | 音频生成 |
| `mlops/models/segment-anything` | SAM 零样本图像分割 | 图像分割 |
| `mlops/stable-diffusion` | Stable Diffusion 文生图 | 图像生成 |
| `mlops/whisper` | Whisper 语音识别/转录（99 语言） | 语音转写 |

## 选择规则

1. **先定任务**：训练/微调 → 训练组；推理部署 → 推理组；LLM 应用 → 应用组。
2. **模型获取先行**：任何 ML 项目先 `huggingface-hub` 找模型/数据。
3. **微调路径**：显存受限 → `unsloth`；全流程 RLHF → `trl-fine-tuning`；配置化 → `axolotl`。
4. **部署路径**：高吞吐服务 → `vllm`；本地小模型 → `llama-cpp`。
5. **RAG 应用**：`offline-rag-pipeline` + `prompt-engineering` 组合。

## 全局底线

- ML 实验先记录（W&B），再跑大规模训练。
- 本地推理注意显存/内存占用（`ollama-project-dev` 有 VRAM 安全序列化指南）。
- 模型下载优先 hf-mirror（国内环境），避免网络超时。
