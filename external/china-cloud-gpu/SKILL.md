---
name: china-cloud-gpu
description: Cloud GPU租赁与AI生成API方案。当用户在国内无本地GPU、需要跑AI画图/视频生成/模型训练时使用。覆盖AutoDL按量租用、阿里云万相API、云厂商GPU价格对比。
version: 1.0.0
tags:
  - cloud-gpu
  - autodl
  - alibaba-cloud
  - gpu-rental
  - ai-generation
  - comfyui
  - china
---

# China Cloud GPU

国内无本地GPU时的替代方案：按量租GPU跑ComfyUI，或直接调API。

## When to Use

- 用户在国内，comfyui hardware_check 返回 `verdict: cloud`（无GPU）
- 需要租GPU跑 AI画图/视频生成/模型训练
- 对比云GPU价格方案

## Two Paths

### Path A: GPU租赁 → 跑 ComfyUI（灵活，推荐AutoDL）

| 平台 | 推荐卡 | 显存 | 价格 | 特点 |
|------|--------|------|------|------|
| **AutoDL** | RTX 3090 | 24GB | ~1元/时 | 按分钟计费，关机停费 |
| AutoDL | RTX 4090 | 24GB | ~1.5-2元/时 | 比3090快30%+ |
| 阿里云 EGS | A10 | 24GB | ~3214元/月 | 包月贵，不建议个人用 |

**AutoDL快速上手：**
1. 注册 autodl.com → 送1个月会员
2. 充值（10块够跑很久）
3. 控制台→租用新实例→选GPU→选PyTorch镜像→开机
4. 拿SSH信息给Agent→Agent装ComfyUI
5. 用完关机→停止计费

**AutoDL存储机制（重要）：**
- `/root/autodl-tmp`: **实例数据盘**，50GB默认，**可写**，关机保留15天
- `/root` (overlay): 系统盘，~30GB，**可写**，容器重启丢失
- `/autodl-pub`: 公共仓库，7TB但**只读**！不能存放模型
- `/autodl-pub/data`: AutoFS挂载，同样**只读**
- 文件存储（网盘）：20GB免费，跨实例共享，按GB/天计费
- 不同实例数据盘不互通，但网盘相通

**⚠️ 大模型磁盘限制**：50GB数据盘放不下 Wan 2.1 T2V-14B（~65GB总大小，每个分片~9-10GB）。需要≥100GB数据盘或换用更小模型（如 Wan 1.3B ~5GB，CogVideoX 5B ~12GB）。

**GPU选型速查（VRAM门槛）：**
| 任务 | 最低显存 | 推荐 |
|------|----------|------|
| SD 1.5 | 6GB | 8GB+ |
| SDXL | 8GB | 12GB+ |
| Flux | 12GB | 16GB+ |
| 视频生成 | 16GB | **24GB** (3090起) |

### Path B: API调用 → 直接调视频/图片API

| API | 模型 | 单价 | 免费额度 |
|-----|------|------|----------|
| 阿里云百炼 | wan2.7-t2v (720p) | 0.6元/秒 | ✅ 新用户有 |
| 阿里云百炼 | wanx2.1-t2v-turbo (720p) | 0.24元/秒 | ✅ 200秒 |
| 阿里云百炼 | happyhorse-1.1 (720p) | 0.54元/秒(6折) | ✅ 10秒 |

**万相计费规则：输入不计费，输出按视频秒数计费。费用=单价×秒数。**

## 阿里云万相视频模型完整价格（华北2北京）

### 文生视频
| 模型 | 分辨率 | 单价 |
|------|--------|------|
| wanx2.1-t2v-turbo | 480P/720P | 0.24元/秒 |
| wanx2.1-t2v-plus | 720P | 0.70元/秒 |
| wan2.7-t2v | 720P | 0.6元/秒 |
| wan2.6-t2v | 1080P | 1.0元/秒 |
| happyhorse-1.1 (6折) | 720P | 0.54元/秒 |

### 图生视频
| 模型 | 分辨率 | 单价 |
|------|--------|------|
| wan2.7-i2v (有声) | 720P | 0.6元/秒 |
| wan2.6-i2v-flash | 720P | 0.3元/秒 |
| wan2.2-kf2v-flash | 480P | 0.10元/秒 |

## 阿里云服务器个人最低价（2026）
| 类型 | 配置 | 价格 |
|------|------|------|
| 轻量秒杀 | 2核2G | 38元/年 |
| ECS经济型 | 2核2G 3M | 99元/年 |
| ECS通用u1 | 2核4G 5M | 199元/年 |

## Agent操作AutoDL流程

1. 用户创建AutoDL实例→开机
2. 用户分享SSH信息(host/port/password)
3. Agent SSH进入→装ComfyUI+模型→配置完成
4. 用户用完→手动关机（Agent不能操控AutoDL控制台）
