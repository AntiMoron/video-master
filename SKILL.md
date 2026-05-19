---
name: video-master
description: Use when generating high-quality commercial or hyper-realistic AI video prompts for Seedance 2.0, Higgsfield (Kling 3.0, Sora 2, Veo 3.1, Minimax), or any AI video platform. Triggers on: product ad, TVC, UGC video, cinematic video, brand film, short drama, music video, AI video prompt, Seedance, Higgsfield, 商业视频, 视频提示词, 拟真人视频.
---

# Video Master — 商业视频提示词大师

生成高质量商业化、拟真人 AI 视频提示词。数据来自 GitHub Top-5 仓库（按 Stars 排序）。

**Sources (by stars):**
1. `MemeCalculate/moyin-creator` ★3569 — 影视生产级工具，Seedance 2.0 全流程
2. `ArcReel/ArcReel` ★2262 — AI 视频工作台，Seedance / Veo 3.1 / Grok
3. `Ethanxwang/tvc-director` ★186 — TVC 广告创意导演，Nano Banana + Seedance
4. `AKCodez/higgsfield-claude-skills` ★123 — 19 个 Higgsfield Claude 技能
5. `OSideMedia/higgsfield-ai-prompt-skill` ★74 — MCSLA 公式，20 子技能，17 模板

---

## 核心公式：MCSLA

每条视频提示词必须包含这 5 层（来源：OSideMedia ★74）：

```
Model · Camera · Subject · Look · Action
模型   · 运镜   · 主体   · 风格 · 动作
```

**格式模板：**
```
Model: [Kling 3.0 / Sora 2 / Veo 3.1 / Seedance 2.0 / Minimax Hailuo 2.3]
Aspect: [16:9 / 9:16 / 2.35:1] | Duration: [5s/8s/10s] | Style: [Cinematic]

[主体描述 — 具体服装、面貌、位置]
[场景 — 地点、天气、氛围]
Camera: [具体运镜预设名称]
[核心动作 — 一个清晰的动作beat]
Style: [色调、光影、画面感]. [比例].
[Sound: 音效描述（仅 Kling 3.0）]
```

**2 秒钩子原则：** 前 2 秒必须抓住注意力。硬规则：每条 prompt 开头必须有明确的视觉冲击。

---

## 速查：平台 × 模型选择

| 使用场景 | 推荐模型 | 平台 |
|---------|---------|------|
| 人物/角色一致性 + 对话 | Kling 3.0 | Higgsfield |
| 大场面/物理特效/太空 | Sora 2 | Higgsfield |
| 自然风景/写实环境 | Veo 3.1 | Higgsfield / ArcReel |
| 舞蹈/流体动作 | Minimax Hailuo 2.3 | Higgsfield |
| 风格化/超现实 | Wan 2.7 | Higgsfield |
| 产品图/4K 静帧 | Nano Banana Pro | Higgsfield / TVC Director |
| 全流程批量 + 中文 | Seedance 2.0 | 即梦/Higgsfield |

---

## 17 类提示词模板

详细模板 → `templates.md`

| # | 类型 | 关键词触发 |
|---|------|-----------|
| 01 | 电影追逐 Cinematic Action Chase | 追逃/跑酷/飞车 |
| 02 | 产品商业 Product UGC Showcase | 产品广告/开箱/电商 |
| 03 | 恐怖氛围 Horror Atmosphere | 恐怖/悬疑/惊悚 |
| 04 | 时尚大片 Fashion Editorial | 时尚/大片/lookbook |
| 05 | 科幻特效 Sci-Fi VFX | 科幻/赛博朋克/爆炸 |
| 06 | 人物登场 Portrait Character Intro | 角色/人物/肖像 |
| 07 | 风景大景 Landscape Establishing | 风景/自然/航拍 |
| 08 | 喜剧社媒 Comedy Social Media | 搞笑/TikTok/短视频 |
| 09 | 浪漫亲密 Romantic Intimate | 爱情/婚礼/情侣 |
| 10 | 舞蹈音乐 Dance Music Performance | 舞蹈/MV/演出 |
| 11 | TVC 产品电影化 | 品牌广告/产品拆解 |
| 12 | TVC 品牌世界穿梭 | 极限运动/越野 |
| 13 | TVC 生活方式短片 | 穿戴产品/跑鞋/手表 |
| 14 | Seedance 多角色锚定 | 双人/多人场景 |
| 15 | Seedance 单角色定位 | 精确人物位置 |
| 16 | 文字叠加 Text Overlay | 字幕/标语/Speech Bubble |
| 17 | 电商广告 12 钩子 | 产品落地页/DTC广告 |

---

## 中文 Seedance 提示词公式（Jimeng/即梦）

> 所有发给 Seedance/即梦 的 prompt 必须是中文（来源：zhanghaonan777 ★67）

```
提示词 = 主体 + 运动，背景 + 运动，镜头 + 运动
```

**质量前缀：** `真人实拍，电影级摄影，真实皮肤毛孔质感`（拟真人必加）

**时间戳分镜（9秒以上）：**
```
0-3秒：[画面描述 + 镜头语言]
4-8秒：[画面描述 + 镜头语言]
9-12秒：[画面描述 + 镜头语言]
```

**技术参数前缀：** `2.35:1，24fps，15秒，霓虹高饱和冷暖对比`

**结尾禁止项：** `禁止：任何文字、字幕、LOGO 或水印`

---

## 2 秒钩子技巧 TOP-5（来源：AKCodez ★123）

| 钩子 | 效果 | Prompt 写法 |
|------|------|-----------|
| 极端特写→大场景 | 视觉冲击 | `Open with extreme macro close-up of [detail]. At 0.5s, whip cut to extreme wide shot.` |
| 黑屏→光爆 | 张力释放 | `Begin in pure black. At 0.8s, explosive light burst from [direction].` |
| 逆向运动 | 吸引大脑 | `Action moves backwards in first 2 seconds. [object] slides in reverse.` |
| 直视镜头 | 原始冲击 | `Close shot of eyes in low-light. At 0.8s, eyes snap open and lock on-camera.` |
| 极端色彩转变 | 感官冲击 | `Frame opens in cool desaturated blue-grey. At 0.6s, sudden shift to warm amber-gold.` |

---

## 运镜预设速查（Higgsfield 命名）

| 中文 | 英文预设 | 适用 |
|------|---------|------|
| 跟拍 | Action Run | 追逐/运动 |
| 慢推 | Dolly In | 人物/情感 |
| 慢拉 | Dolly Out | 分离/宏大 |
| 机械臂环绕 | Robo Arm | 产品展示 |
| 旋转台 | Lazy Susan | 产品360 |
| FPV无人机 | FPV Drone | 沉浸/追逐 |
| 轨道 | 360 Orbit | 人物/舞蹈 |
| 荷兰角 | Dutch Angle | 恐怖/心理 |
| 手持 | Handheld | 纪录/真实感 |
| 子弹时间 | Bullet Time | 高燃动作 |

---

## 画质锚定词库（来源：Ethanxwang TVC Director ★186 + zhanghaonan777 ★67）

| 目标风格 | 前置锚定词 | 结尾锚定词 |
|---------|-----------|-----------|
| 真人实拍 | `真人实拍，电影级摄影，8K超清分辨率` | `真实皮肤毛孔质感，自然光照` |
| 真人电影剧照 | `真人电影剧照质感，8K超清分辨率` | `真实皮肤纹理和毛发细节，电影级调色` |
| 3A游戏CG | `大师级CG渲染，8K超清分辨率` | `3A大作3D游戏风格` |
| 顶级CG引擎 | `虚幻引擎5渲染，8K超清分辨率` | `次表面散射皮肤，PBR材质，全局光照` |
| 好莱坞视效 | `超写实CG，电影级CG视效，8K超清分辨率` | `PBR材质，全局光照，电影级调色` |

---

## 导演风格快速引用

| 风格 | 视觉特征 | 适合 |
|------|---------|------|
| 王家卫风格 | 手持晃动、高饱和、抽帧、暧昧光影 | 情绪/都市爱情 |
| 诺兰风格 | IMAX画幅、实感质感、宏大叙事 | 科幻/史诗 |
| 扎克·施奈德风格 | 极致升格、高对比硬光、史诗感 | 战斗/英雄 |
| 新海诚风格 | 丁达尔光、超高饱和自然色 | 青春/治愈 |
| 韦斯·安德森风格 | 严格对称、糖果色、平移运镜 | 广告/复古趣味 |
| 黑色电影风格 | 高反差、百叶窗光影、烟雾 | 悬疑/犯罪 |

---

详细带注释模板、Before→After 改写示例、完整 Seedance API 调用 → `templates.md`

---

## Higgsfield 官方 API 生成视频

**脚本：** `generate.py`（两步流水线：Seedream v4 文生图 → Kling 2.1 Pro 图生视频）

### 快速开始

```bash
# 1. 设置凭证（来自 platform.higgsfield.ai → API Keys）
export HF_CREDENTIALS="KEY_ID:KEY_SECRET"

# 2. 生成视频（9:16 竖版，5秒）
python ~/.claude/skills/video-master/generate.py \
  --prompt "A developer opens his monthly OpenAI bill email. Eyes widen. He slumps back. Says flatly: 'There has to be a cheaper way.' Camera: static locked-off medium shot." \
  --image-prompt "A developer in his late 20s at a dark home office, three monitors glowing blue, looking at email on screen, shocked expression" \
  --aspect 9:16 --duration 5 --output ad_v1.mp4
```

### 所有选项

| 参数 | 说明 | 默认 |
|------|------|------|
| `--prompt` | 视频动作/内容描述（必填） | — |
| `--image-prompt` | 首帧静帧描述（可选，默认同 prompt） | — |
| `--aspect` | `9:16` / `16:9` / `1:1` / `4:3` | `9:16` |
| `--duration` | `5` 或 `10` 秒 | `5` |
| `--output` | 输出文件路径 | `output.mp4` |
| `--image-only` | 只生成首帧图片，不做视频 | false |
| `--image-url` | 跳过 Step 1，直接用已有图片做视频 | — |

### 模型说明（官方 API 可用）

| 用途 | 模型 | 备注 |
|------|------|------|
| 文生图（首帧） | `bytedance/seedream/v4/text-to-image` | 高质量静帧 |
| 图生视频 | `kling-video/v2.1/pro/image-to-video` | 稳定，5s/10s |
| 图生视频（备选） | `bytedance/seedance/v1/pro/image-to-video` | Seedance 风格 |
| 视频（实验） | `higgsfield-ai/dop/standard` | DoP 模型，可能支持文生视频 |

> Kling 3.0 / Sora 2 / Veo 3 仅在 Web backend（需 Clerk cookie，不稳定），不在官方 API。

---

## Higgsfield CLI — 订阅用户（支持 Kling 3.0 / Sora 2 / Veo 3）

**适用：** 有 higgsfield.ai 订阅（cloud.higgsfield.ai），可用全部最新模型。
**脚本：** `hf.py`（来源：clawdybotty/higgsfield-cli，Clerk JWT 认证）

### 一次性登录

```bash
python3 ~/.claude/skills/video-master/hf.py login
# 输入 higgsfield.ai 账号邮箱 + 密码 + 邮件验证码
# Session 保存在 ~/.config/hf/session.json，约 1 年有效
```

### 生成视频（Kling 3.0 文生视频）

```bash
python3 ~/.claude/skills/video-master/hf.py video \
  "A developer sits at a dark home office, three monitors glowing. Opens OpenAI bill email. Eyes widen. He slumps back. Says flatly: 'There has to be a cheaper way.' Camera: static locked-off medium shot." \
  --aspect-ratio 9:16 --duration 5 --sound on \
  --output chatgpttech_ad.mp4
```

### 所有视频选项

| 参数 | 说明 | 默认 |
|------|------|------|
| `--aspect-ratio` | `9:16` / `16:9` / `1:1` | `16:9` |
| `--duration` | `5` 或 `10` 秒 | `5` |
| `--sound` | `on` / `off` | `on` |
| `--start-image` | 参考首帧图片路径 | — |
| `--end-image` | 参考尾帧图片路径 | — |
| `--use-free-gens` | 用免费生成配额 | false |
| `--use-unlim` | 用无限生成配额 | false |
| `--output` | 输出 .mp4 路径 | 自动命名 |

### 可用 Web 模型（需订阅）

| 模型 | 特点 |
|------|------|
| `kling3_0` | Kling 3.0，当前默认，文生/图生视频 |
| 订阅后可通过 `hf.py models` 查看完整列表 | — |

> **注意：** Web backend 使用 Clerk JWT，session 约 1 年有效，但 Higgsfield 可能在更新后失效，需要重新 `hf.py login`。
