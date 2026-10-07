https://chatgpt.com/share/6a62babc-6614-83ee-855e-be21eb3dc6b9



# 1. display pipeline

首先要做的是理解整个显示数据流。

这一条链，要做到闭着眼睛都画出来。

包括：每一层负责什么、为什么存在、输入是什么、输出是什么。

```txt
App
↓
SurfaceFlinger
↓
HWComposer
↓
DRM Atomic
↓
MSM DRM
↓
DPU
↓
DSI
↓
Panel
```





# 2. 理解硬件实现

这部分可能才是自己更想要去研究的什么vendor display controller

> 这部分可能并不能让我升职加薪，这只是自己的兴趣而已。
>
> 就像 《so good they can't ignore you》里想说的：
>
> **"不要追随热情，要培养稀缺技能，让热情随之而来"**
>
> 换句话解释说，就是：
>
> **"追随热情"是结果，不是起点。起点是：找到有市场需求的方向 → 投入刻意练习 → 获得稀缺技能 → 获得自主力和成就感 → 热情自然产生。**









```plain
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Plane     │───▶│   CRTC      │───▶│   Encoder   │───▶│  Connector  │───▶│   Panel     │
│  (图层)     │     │ (时序控制器) │    │  (信号编码)  │    │  (物理接口)  │    │  (物理屏幕)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

- **Plane（图层/平面）**：代表一个图像源，从 Framebuffer 读取像素数据，可进行裁剪、缩放、旋转、Alpha 混合。硬件通常支持多个 Plane（Primary + Overlay + Cursor），这就是**硬件叠加**的基础 。
- **CRTC（Cathode Ray Tube Controller）**：现代意义上的显示控制器，负责生成视频时序信号（HSYNC/VSYNC），将 Plane 的数据扫描输出 。
- **Encoder**：将 CRTC 的并行像素/时钟信号编码为特定协议（HDMI、DSI、LVDS、DisplayPort）。
- **Connector**：物理接口的抽象（HDMI 端口、MIPI DSI 等），管理热插拔和 EDID 。
- **Panel**：物理显示面板，接收信号并驱动行列驱动器发光。







# 鸡汤





