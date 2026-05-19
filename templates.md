# Video Master — 详细模板库

来源：GitHub Top-5 仓库（按 Stars 排序），汇总所有提示词模板。

---

## Template 01 — 电影追逐 Cinematic Action Chase

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Kling 3.0（人物追逐）/ Sora 2（车辆/大场面）

```
Model: Kling 3.0
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls and startled vendors. Steam rises from food carts.
Neon signs fracture in every puddle.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.
```

**注释：**
- `tactical jacket` 具体服装胜过"a woman running"
- `rain-soaked night market` 湿地 + 霓虹 = 视觉复杂度
- `neon signs fracture in every puddle` 反光提示，模型会渲染
- `Action Run` 使用精确预设名，而非"dramatic camera"
- `Cold blue shadows, warm amber market light` 双色调，避免泛泛的"cinematic"

**变体：**
- 更真实手持感：`Handheld` + `shaky, documentary urgency`
- 飞车追逐：Sora 2 + `Car Chasing` 预设
- 竖版/社媒：9:16，保持 Action Run，注明`close framing, face visible`

---

## Template 02 — 产品商业 Product UGC Showcase

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Nano Banana Pro（静帧）/ Kling 3.0（视频动画）

```
Model: Kling 3.0 (video) / Nano Banana Pro (image)
Aspect: 16:9 | Duration: 5s | Style: Cinematic commercial

A matte black insulated travel mug, minimal design, no branding.
Placed on a raw concrete countertop beside a morning window.
Camera: Robo Arm arcing slowly from the base up and around to the lid.
Hot coffee pours in — steam rises in a slow macro close-up.
A hand wraps around the mug. Camera: Dolly In to hands + warmth detail.
Style: Cinematic commercial. Warm neutral tones, soft diffused natural light. 16:9.
Sound: gentle liquid pour, soft ceramic texture.
```

**注释：**
- `matte black insulated travel mug, minimal design, no branding` 精确材质 + 颜色 + 造型（避免品牌名）
- `Robo Arm arcing slowly from the base up and around to the lid` 告诉模型精确路径，非"orbit"泛称
- `Hot coffee pours in — steam rises` 主角时刻：微距质感 + 蒸汽 = 视觉回报
- `Sound: gentle liquid pour` 音效维度（Kling 3.0 原生支持）

**常见错误：**
- 写品牌名（"A Nike sneaker"）→ 被过滤。改用外观描述："a white athletic sneaker with a minimal swoosh-like logo"
- 未指定背景表面 → 产品悬浮在虚空，显得廉价

---

## Template 03 — 恐怖氛围 Horror Atmosphere

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Kling 3.0（人物恐怖）/ Wan 2.5（风格化超自然）

```
Model: Kling 3.0
Aspect: 4:3 | Duration: 8s | Style: VHS

A woman unlocks the door to her apartment. Steps inside. Everything looks normal.
She sets down her keys. Turns toward the kitchen.
Camera: slow Dolly In toward the hallway mirror at the end.
The mirror shows the room — but the couch is against the wrong wall.
She hasn't moved. The reflection has.
Camera: Dutch Angle as she realizes.
Style: VHS. Desaturated greens, practical light only, slight scan lines. 4:3.
Apply Horror Face preset in the mirror reflection.
```

**关键技巧：**
- 不描述血腥细节，描述氛围（"dread", "something is wrong"）→ 不触发内容过滤
- 4:3 比例 → 增加幽闭感
- `Dutch Angle as she realizes` → 镜头即心理
- `Apply Horror Face preset` → 让平台 VFX 预设处理恐怖效果

---

## Template 04 — 时尚大片 Fashion Editorial

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Soul 2.0 / Nano Banana Pro（最高清晰度）/ Kling 3.0（视频）

### 身份块（Soul ID）
```
The Soul ID character — angular jawline, dark skin, close-cropped natural hair.
Wearing a structured black wool overcoat, wide-leg trousers, white minimalist sneakers.
Silver chain necklace. Hands in pockets.
```

### 动作块
```
She walks slowly toward camera down an empty concrete corridor.
Camera: Dolly Out — retreating as she advances, never quite letting her fill the frame.
Style: Cinematic. High contrast, desaturated cool tones, single overhead strip light
casting a hard shadow. 2.35:1 anamorphic.
```

### 合并版（无 Soul ID）
```
Model: Kling 3.0
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

A woman with angular jawline, dark skin, and close-cropped natural hair walks slowly
toward camera down an empty concrete corridor. She wears a structured black wool overcoat,
wide-leg trousers, white minimalist sneakers. Silver chain necklace. Hands in pockets.
Camera: Dolly Out — retreating as she advances.
Style: Cinematic. High contrast, desaturated cool tones, single overhead strip light. 2.35:1.
```

**规则：** 身份块 = 外观+服装；动作块 = 动作+镜头。混用会导致面部漂移。

---

## Template 05 — 科幻特效 Sci-Fi VFX

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Sora 2（大场面物理）/ Kling 3.0（角色驱动）/ Wan 2.5（风格化）

```
Model: Sora 2
Aspect: 2.35:1 | Duration: 10s | Style: Cinematic

A battle-worn space station corridor, emergency lighting, debris floating in zero gravity.
A soldier in heavy tactical armor pulls herself along a handrail, rifle raised.
Ahead — a sealed blast door, sparking at the seams. She plants a charge and pushes back.
Camera: FPV Drone drifting just ahead of her through the corridor as the charge detonates.
Style: Cinematic, cold steel blue, high contrast. 2.35:1 anamorphic.
Apply Plasma Explosion preset at the detonation moment.
```

**错误：** 不要叠加多个 VFX 预设（Plasma + Portal + Glitch）→ 模型崩溃。每次生成只用一个。

---

## Template 06 — 人物登场 Portrait Character Intro

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Kling 3.0 视频 / Soul 2.0 或 Nano Banana Pro 参考图

### 合并版
```
Model: Kling 3.0
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

A weathered man in his late 40s stands at the edge of a rain-soaked harbour dock at night.
Salt-and-pepper stubble, worn leather jacket, collar turned up against the driving rain.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon.
Camera: slow Dolly In from medium-wide to medium close-up.
Style: Cinematic. Crushed blacks, single sodium-vapour key light from the right,
cold blue fill. 2.35:1 anamorphic.
```

---

## Template 07 — 风景大景 Landscape Establishing Shot

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Veo 3.1（自然/写实）/ Sora 2（物理特效）/ Wan 2.5（绘画风格）

```
Model: Veo 3.1
Aspect: 16:9 | Duration: 10s | Style: Cinematic natural

Open ocean at dusk. The horizon is dark with an approaching storm.
Waves are already running ahead of it — three-meter swells, grey-green water.
Camera: Timelapse Landscape as the storm front advances, sky darkening fast.
Lightning inside the clouds. Then the first rain hits the surface.
Style: Cinematic, natural grade, no artificial treatment. 16:9.
```

**关键：** 风景提示词必须描述"会发生什么变化"而非静态描述。天气移动、光线变化、潮汐涨落 = 视频而非图片。

---

## Template 08 — 喜剧社媒 Comedy Social Media

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Kling 3.0（台词/配音）/ Minimax Hailuo 2.3（肢体喜剧）

```
Model: Kling 3.0
Aspect: 9:16 | Duration: 8s | Style: Cinematic

A man sits at a desk staring at his laptop, dead-eyed.
He takes a long sip of coffee, blinks slowly, sets the mug down.
He says flatly: "This is fine."
Behind him through the window — a building is on fire, fire trucks arriving.
He doesn't turn around.
Camera: static, locked-off, medium shot. No movement.
Style: Cinematic, bright office lighting, high-key, neutral tones. 9:16.
```

**技巧：** 喜剧 = 静止镜头 + 背景对比 + deadpan timing。台词用引号触发 Kling 3.0 口型同步。

---

## Template 09 — 浪漫亲密 Romantic Intimate

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Kling 3.0（配音）/ Kling 2.6（无音效情绪场景）

```
Model: Kling 3.0
Aspect: 16:9 | Duration: 8s | Style: Cinematic

Two people on a rooftop terrace at dusk, city glowing below them.
They've been talking for hours — coffee cups empty, leaning close.
A long pause. She looks at him.
Camera: Arc slowly around both of them, city blurring behind.
He reaches over and tucks a strand of hair behind her ear.
Style: Cinematic. Golden hour warm tones, shallow depth of field. 16:9.
Ambient: quiet city hum, distant traffic, gentle wind.
```

---

## Template 10 — 舞蹈音乐 Dance Music Performance

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

**推荐模型：** Minimax Hailuo 2.3（最佳流体动作）/ Kling 3.0（配音演出）

```
Model: Minimax Hailuo 2.3
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A dancer in a white flowing dress performs alone in a vast black studio.
A single overhead spotlight. She moves through contemporary choreography —
slow arms, sudden explosive turns, floor work.
Camera: 360 Orbit tightening toward her as movement intensifies.
Overhead shot as she collapses to the floor in the final beat.
Style: Cinematic. Pure black and white contrast. 16:9.
Apply Glow Trace preset — her movement leaves a trail of white light.
```

**规则：** 不要用具体舞蹈术语（pirouette, plié）→ 模型无法执行。描述能量和身体位置。

---

## Template 11-13 — TVC 三大叙事模型

**来源：** Ethanxwang/tvc-director ★186

### 11. 产品电影化拆解 (Cinematic Product Breakdown)

产品是唯一主角，纯影棚，多 Phase 微电影。

```
[Nano Banana Pro 图片] + [Seedance 2.0 视频]

Phase 1 (0-5s): 极慢产品拆解动画，零件悬浮，金属磨砂纹理微距
镜头: 推镜头→极微距旋转→悬浮凝视
光影: 低调影棚光，侧光勾勒轮廓

Phase 2 (5-10s): 爆发旋转→俯冲穿越
镜头: 高速旋转+急推
光影: 光随旋转流动

Phase 3 (10-15s): 产品归位，完整形态，Hero Shot
镜头: 慢拉，产品居中，logo渐显
```

### 12. 品牌世界穿梭 (Brand World Crosscut)

品牌世界 ←Match Cut→ 产品世界交替。

```
Phase 1: [极限运动世界] — 跳伞者旋转，GoPro 第一视角，湛蓝天空
Match Cut: 旋转动作 → 产品旋转 (同轴)

Phase 2: [产品影棚] — 相机/手表/运动装备，侧光，微距质感
Match Cut: 产品角度 → 使用者视角

Phase 3: [品牌世界] — 雪地/沙漠/盘山公路，环境匹配产品属性
```

**适用：** 运动相机（跳伞/潜水）、越野车（沙漠）、户外装备

### 13. 生活方式短片 (Lifestyle Film)

产品始终待在品牌世界中，不跳出去做影棚特写。

```
[产品穿戴/使用状态全程]

Scene 1: 清晨街道，慢跑者，跑鞋低角度追拍，路面湿反光
Scene 2: 慢动作侧面，鞋底接触地面瞬间
Scene 3: 跑者跨越楼梯，仰拍+浅景深突出鞋
Hero Shot 结尾: 停步，低角度，产品特写，品牌信息渐入
```

---

## Template 14-15 — Seedance 多角色定位

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

### 14. 多角色锚定 Multi-Character Anchor

生成前先画俯视空间地图：
```
[俯视图]
●A (左1/3, 前景)    ●B (右1/3, 中景)
         ■ 道具/物体 (中央)
```

然后写 prompt：
```
Two characters in a rain-soaked alley at night.
Character A — [外观描述]. Positioned frame-left, foreground, facing right.
Character B — [外观描述]. Positioned frame-right, mid-ground, facing left.
A [道具] lies on the ground between them, center-frame.
Camera: static medium two-shot, equal framing.
Style: Cinematic. Sodium-vapour overhead, long shadows.
```

### 15. 单角色精确定位 Single-Character Position

```
[角色名] — [外观]. Standing at [位置: frame-left/center/right], 
[距离: foreground/mid-ground/background], [姿态: facing camera/profile/back].
[接触点: hand on [物体], leaning against [表面], seated on [物体]].
```

---

## Template 16 — 文字叠加 Text Overlay

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

### 标语/品牌标语
```
Model: Kling 3.0
Aspect: 9:16 | Duration: 5s | Style: Cinematic commercial

[背景视觉描述]
Camera: slow Dolly In.
Text overlay: "[品牌标语]" — bold, centered, white sans-serif, appears at 1s,
fades in over 0.5s, holds for 3s.
Style: Cinematic. [色调]. 9:16.
```

### 对话字幕
```
Subtitle sync: Character says "[台词]" at 2s mark.
Subtitle appears bottom-center, white text, dark background strip, 
24pt font, holds for 2.5s.
```

---

## Template 17 — 电商广告 12 钩子

**来源：** AKCodez/higgsfield-claude-skills ★123

| 钩子 | 适用 | 2秒内发生 |
|------|------|---------|
| 产品戏剧性落入画面 | 奢侈品/新品发布 | 暗背景 + 产品带运动模糊下落 + 光影剧变 |
| ASMR质感微距 | 服装/美妆/食品 | 极限特写 → 手指划过揭示产品名 |
| 前后对比 | 美容/整理/健身 | 分屏 或 quick transition：问题态 → 解决态 |
| 直视镜头打招呼 | UGC/网红/快消 | 模特/创作者正面看镜头 + 手势停顿 |
| 开箱揭露 | 高端包装/礼品 | 手打开包装盒 → 产品在光中显现 |
| 色系瀑布 | 多色产品/系列 | 产品排列旋转展示所有颜色变体 |
| 成分爆炸 | 天然美妆/功能食品 | 原料从中心向外爆散 |
| 问题-解决snap | DTC/功能性产品 | 文字叠加"问题:" → 切换 → 产品"解决" |
| 手持使用预告 | 工具/配件/服装 | 手持产品展示核心功能 2秒内 |
| 生活方式激励 | 生活方式品牌/美食 | 美好场景 + 产品自然融入 |
| 限量稀缺信号 | 限定款/闪购 | 文字叠加"Limited Drop" + 产品发光 |
| 创作者真实反应 | UGC广告 | 开箱 + 创作者惊喜表情 + 产品揭示 |

---

## Before → After 提示词改写示例

**来源：** OSideMedia/higgsfield-ai-prompt-skill ★74

### 改写 1：模糊→精确（动作类）

❌ 差：
```
A cool action scene in a city at night with a woman running and cameras moving dramatically.
```

✅ 强：
```
Model: Kling 3.0
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls. Steam rises from food carts, neon signs fracture in puddles.
Camera: Action Run — low behind her, matching pace.
She slides under a closing metal gate without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.
```

**改变了什么：** 命名摄像预设、具体环境细节、主动动词（sprints/slides/weaving）、明确色调。

---

### 改写 2：图生视频重描述→运动优先

❌ 差（重新描述图片中所有静态内容）：
```
A beautiful woman with long dark hair and brown eyes wearing a red silk dress
is standing on a balcony with a city behind her at sunset. The sky is orange
and pink with some clouds. She looks elegant.
```

✅ 强（只描述变化的部分）：
```
Starting from the provided image as the first frame.
Her hair lifts gently in the evening breeze. She turns her head slowly to the right,
eyes narrowing slightly as if recognizing someone below.
Camera: slow Dolly In toward her profile.
Wind catches the dress fabric. City lights begin flickering on in the distance.
Style: Cinematic, warm golden hour, shallow depth of field.
```

**原则：** 图生视频时只描述"将要发生变化的内容"，不重复图片中已有的静态信息。

---

### 改写 3：废话词→可观测控制

❌ 差：
```
An epic cinematic masterpiece shot of a stunning detective in a breathtaking
noir setting. Ultra-realistic 8K quality. Award-winning cinematography.
```

✅ 强：
```
Model: Kling 3.0
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
Camera: slow Dolly In from medium-wide to medium close-up.
Style: Cinematic. Crushed blacks, single sodium-vapour key light from the right,
cold blue fill, 2.35:1 anamorphic.
```

**测试标准：** 每个词是否能被摄像机测量？"Epic"无法测量，"sodium-vapour key light"可以。

---

### 改写 4：镜头汤→单一运镜

❌ 差：
```
Camera does a dramatic FPV drone shot while also orbiting the subject
and then crash zooming into their face with a dolly zoom effect.
```

✅ 强：
```
Camera: FPV Drone — sweeping through the zero-gravity corridor ahead of the soldier,
debris drifting past on both sides.
```

**规则：** 每次生成只用一个镜头运动。需要四个镜头 = 生成四条视频，后期拼接。

---

## Seedance 2.0 API 调用参考

**来源：** zhanghaonan777/Seedance2-skill ★67

```bash
export ARK_API_KEY="your-api-key-here"

# 文生视频
python3 scripts/seedance.py create --prompt "提示词" --ratio 16:9 --duration 5 --wait --download ~/Desktop

# 图生视频（首帧）
python3 scripts/seedance.py create --prompt "提示词" --image img.jpg --ratio adaptive --duration 5 --wait --download ~/Desktop

# 首帧 + 尾帧
python3 scripts/seedance.py create --prompt "提示词" --image first.jpg --last-frame last.jpg --ratio adaptive --wait --download ~/Desktop

# 视频参考（运镜复制）
python3 scripts/seedance.py create --prompt "提示词" --video motion_ref.mp4 --wait --download ~/Desktop

# 音频同步（节拍匹配）
python3 scripts/seedance.py create --prompt "提示词" --audio bgm.mp3 --wait --download ~/Desktop

# 草稿预览（低成本先看效果）
python3 scripts/seedance.py create --prompt "提示词" --image img.jpg --draft true --wait --download ~/Desktop

# 离线推理（便宜50%，适合批量不急用）
python3 scripts/seedance.py create --prompt "提示词" --service-tier flex --wait --download ~/Desktop
```

**模型 ID：**
| 模型 | ID |
|------|-----|
| Seedance 2.0（默认） | `doubao-seedance-2-0-260128` |
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` |
| Seedance 1.0 Pro | `doubao-seedance-1-0-pro-250528` |

---

## 中文镜头词汇完整库

**来源：** zhanghaonan777/Seedance2-skill ★67

| 类别 | 关键词 |
|------|--------|
| 景别 | 大远景、远景、全景、中景、近景、特写、大特写 |
| 运镜 | 推镜头、拉镜头、摇镜头、移镜头、跟拍、环绕拍摄、航拍、手持跟拍、希区柯克变焦 |
| 角度 | 平视、俯拍、仰拍、低角度、鸟瞰视角、鱼眼镜头、第一人称视角、主观视角 |
| 节奏 | 慢动作、快切、延时摄影、一镜到底、升格拍摄、硬切、卡点 |
| 焦点 | 浅景深、深景深、焦点转移、虚化背景、选择性对焦 |
| 转场 | 淡入淡出、叠化、划变、闪白、闪黑、跳切、匹配剪辑、遮挡转场、形变转场 |
| 构图 | 三分法、黄金分割、引导线构图、框中框、对称构图、负空间留白、前景遮挡 |

**场景→运镜速查：**
| 场景 | 推荐运镜 |
|------|---------|
| 静物特写 | 缓推、推镜头、浅景深、微距 |
| 大场景 | 拉镜头、航拍、鸟瞰视角、长焦压缩 |
| 人物奔跑 | 跟拍、手持跟拍、运动模糊 |
| 惊悚/悬疑 | 希区柯克变焦、低角度、荷兰角、闪黑 |
| 产品展示 | 环绕拍摄、推镜头、焦点转移、微距 |
| 战斗/高燃 | 环绕摇镜快切、仰拍、慢动作、抽帧、速度线 |
| 情绪/文艺 | 浅景深、淡入淡出、叠化、负空间留白、胶片颗粒 |
| 高级广告 | 匹配剪辑、形变转场、移轴、镜头光晕 |
