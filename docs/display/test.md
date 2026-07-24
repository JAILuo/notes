https://chatgpt.com/share/6a62babc-6614-83ee-855e-be21eb3dc6b9

- 





如果继续沿着 **First Principle** 往下推导，**VSync（Vertical Synchronization，垂直同步）** 不是为了让画面更流畅，而是为了回答一个更基础的问题：

> **Buffer 已经画好了，到底什么时候才能切换到屏幕？**

------

# 回顾一下

我们已经有了：

- Single Buffer → 会发生 Tearing
- Double Buffer → 避免了 CPU/GPU 和 Display 同时访问同一块 Buffer
- Triple Buffer → 避免 GPU 经常等待

但是，现在又出现了一个新的问题。

------

# 一个新的问题

假设：

Display 正在扫描屏幕。

注意，**显示器并不是一瞬间把整张图片显示出来**。

它通常是：

```
第一行
↓

第二行
↓

第三行
↓

...

↓

最后一行
```

一行一行扫描（Scan Out）。

整个过程可能需要：

```
16.67 ms（60 Hz）
```

------

# 如果这时候交换 Buffer 呢？

假设：

Display 已经扫描到屏幕中间：

```
██████████████
██████████████
██████████████
-----------------
□□□□□□□□□□□□□□
□□□□□□□□□□□□□□
□□□□□□□□□□□□□□
```

突然：

GPU：

> Frame 已经画好了！

于是系统：

Swap Buffer。

那么：

Display 后半部分：

开始读取：

新的 Buffer。

于是：

用户看到：

```
旧画面
旧画面
旧画面
----------------
新画面
新画面
新画面
```

这就是：

**Screen Tearing（画面撕裂）**。

注意：

**即使使用 Double Buffer，也可能发生 Tearing。**

因为：

问题已经不是：

CPU 在写。

而是：

**Buffer 在错误的时间进行了交换。**

------

# 第一性原理

于是新的问题变成：

> **什么时候交换 Buffer 才安全？**

答案就是：

**不要在扫描过程中交换。**

而要等：

Display：

扫描完整张图片。

准备重新扫描下一帧的时候。

这一个时间点。

叫：

**Vertical Blank（VBlank）**

或者：

**Vertical Blanking Interval（垂直消隐期）**。

------

# 什么是 VSync？

VSync：

就是规定：

> **Buffer 只能在 Vertical Blank 期间交换。**

例如：

```
Display：

扫描 Frame A

↓

扫描结束

↓

VBlank

↓

Swap

↓

开始扫描 Frame B
```

由于：

新的扫描，

从第一行开始。

因此：

整个屏幕：

全部来自：

同一个 Buffer。

不会：

上半旧。

下半新。

于是：

没有 Tearing。

------

# 为什么叫 Vertical？

因为：

最早 CRT 显示器：

电子枪：

就是：

```
第一行

↓

第二行

↓

...

↓

最后一行
```

画完以后。

电子枪：

需要：

重新回到：

第一行。

这一段时间：

叫：

Vertical Blank。

虽然今天：

LCD、

OLED

已经没有电子枪。

但是：

Display Controller：

仍然保持：

类似的扫描方式。

因此：

VBlank、

VSync

这些名字一直保留到了今天。

------

# 如果 GPU 太快呢？

例如：

GPU：

```
200 FPS
```

Display：

```
60 Hz
```

GPU：

每：

5ms

画好一帧。

但是：

Display：

16.67ms

才允许：

Swap。

于是：

GPU：

只能等待：

下一次：

VBlank。

因此：

GPU：

可能：

200 FPS。

最后：

用户：

看到：

60 FPS。

------

# 如果 GPU 太慢呢？

另一种情况：

GPU：

30 FPS。

Display：

60 Hz。

到了：

VBlank。

GPU：

还没画好。

怎么办？

只能：

继续显示：

上一帧。

于是：

Frame：

重复。

用户：

感觉：

卡顿。

这也是：

为什么：

游戏：

掉帧以后。

感觉：

一卡一卡。

------

# Triple Buffer 为什么常和 VSync 一起出现？

Double Buffer：

如果：

GPU：

刚画好。

Display：

没到：

VBlank。

GPU：

等待。

Triple Buffer：

GPU：

继续画：

下一帧。

因此：

GPU：

利用率：

更高。

所以：

很多现代图形系统：

都是：

```
Triple Buffer

+

VSync
```

一个：

解决：

GPU 等待。

一个：

解决：

什么时候交换。

------

# Linux DRM 中对应什么？

如果以后学习：

DRM/KMS。

你会发现：

有一个非常重要的概念：

**Page Flip。**

Page Flip：

其实就是：

交换：

Front Buffer。

但是：

DRM：

不会：

立即：

Flip。

而是：

等待：

下一次：

VBlank。

因此：

你会看到：

很多 API：

都有：

```
DRM_MODE_PAGE_FLIP_EVENT
```

或者：

```
drmWaitVBlank()
```

它们本质上：

都在等待：

VBlank。

------

# Android 又对应什么？

Android：

SurfaceFlinger：

每次：

合成：

新的 Frame。

最终：

也是：

等待：

Display 的：

VSync Signal。

所以：

Android：

常说：

```
Choreographer

↓

VSync

↓

SurfaceFlinger

↓

HWC
```

这里：

VSync：

就是：

整个系统：

统一的：

"开始显示下一帧" 的节拍器。

应用、SurfaceFlinger 和硬件显示管线都会围绕这个节拍工作，尽量保证每一帧都能在合适的时机提交和显示。

------

# 从 First Principle 总结

整个显示系统的发展可以串成一条完整的逻辑链：

```
Single Buffer
        │
        ▼
CPU/GPU 写 与 Display 读 冲突
        │
        ▼
Screen Tearing
        │
        ▼
Double Buffer
        │
        ▼
交换 Buffer 的时机错误
        │
        ▼
Screen Tearing
        │
        ▼
VSync
        │
        ▼
GPU 等待 VBlank
        │
        ▼
GPU 利用率下降
        │
        ▼
Triple Buffer
```

所以，**VSync 的本质不是“限制帧率”，也不是“提高流畅度”**。它真正解决的是一个时序问题：

> **让 Display Controller 只在完成当前帧扫描之后，才切换到新的 Frame Buffer。**

这样，显示器一次扫描的整张画面始终来自同一个 Buffer，从而避免了画面撕裂。这也是后续 Linux DRM/KMS、Android SurfaceFlinger 以及现代 GPU 显示管线都围绕 VBlank 和 VSync 设计提交与显示时序的根本原因。



Explain why display must be synchronized



这是整个 Display 系列里**最核心的问题之一**。

实际上，我甚至建议不要把这一章命名为 **VSync**，而是叫：

> **为什么 Display 必须同步（Why Display Must Be Synchronized）？**

因为 **VSync 只是同步的一种实现机制**，而**同步（Synchronization）**才是第一性原理。

------

# 从 First Principle 开始

假设整个世界只有两个角色：

```
CPU/GPU
    │
    ▼
画 Frame

Display Controller
    │
    ▼
读 Frame
```

他们共享一块 Frame Buffer。

于是：

一个负责**生产（Produce）**。

一个负责**消费（Consume）**。

这是不是很熟悉？

其实它就是一个经典的**生产者-消费者（Producer-Consumer）**问题。

------

# 如果不同步，会发生什么？

假设：

CPU 正在画：

```
Frame B
```

Display：

正在读：

```
Frame A
```

突然：

CPU：

修改了一半。

Display：

也读了一半。

最后：

Display 得到的是：

```
Frame A（前半）

+

Frame B（后半）
```

用户看到：

画面撕裂。

为什么？

因为：

**Display 读取的数据，不再属于同一个时间点。**

------

# 什么叫同步？

同步其实只有一句话：

> **保证消费者读取的数据，是一个完整、一致的数据。**

注意。

这里完全没有 Display。

数据库。

网络。

文件系统。

都一样。

例如：

数据库正在更新：

```
余额：

1000

↓

500
```

如果另一线程：

读到：

```
余额：

7??
```

显然：

数据已经损坏。

所以：

数据库：

需要：

Lock。

事务。

MVCC。

全部都是：

Synchronization。

Display：

也是一样。

------

# Display 为什么更特殊？

因为：

Display Controller：

不像 CPU。

它不会：

等。

Display：

有自己的节奏。

例如：

60Hz。

意味着：

每：

16.67ms。

必须开始扫描：

下一帧。

无论：

CPU：

准备好了没有。

Display：

都会：

继续。

因此：

Display：

是：

**一个实时消费者（Real-Time Consumer）。**

CPU/GPU：

则是：

**一个速度变化的生产者（Variable-Speed Producer）。**

于是：

两者天然：

不同步。

------

# 什么时候才叫同步？

假设：

Display：

正在扫描：

```
Line 1

↓

Line 2

↓

...

↓

Line 1080
```

CPU：

绝不能：

中途：

把 Buffer：

换掉。

必须：

等：

Display：

扫描完成。

然后：

一起：

开始：

下一帧。

于是：

形成：

```
CPU 完成 Frame

↓

等待

↓

Display 扫描结束

↓

一起进入下一 Frame
```

这就是：

Synchronization。

------

# 为什么叫 VSync？

VSync：

只是：

Synchronization：

在显示系统中的实现。

它规定：

> **Buffer 只能在 Vertical Blank（垂直消隐期）交换。**

为什么？

因为：

这个时候：

Display：

没有：

读取任何 Pixel。

所以：

交换：

安全。

------

# 为什么 Android 整个系统都围绕 VSync？

很多人以为：

只有：

屏幕：

需要：

VSync。

其实：

不是。

例如：

Android：

一个 APP：

调用：

```
drawRect()
```

真正过程：

```
App

↓

RenderThread

↓

SurfaceFlinger

↓

Hardware Composer

↓

Display
```

如果：

App：

120FPS。

SurfaceFlinger：

90FPS。

Display：

60Hz。

每个人：

都按自己的节奏。

最后：

一定：

乱掉。

于是：

Android：

让所有模块：

都跟着：

同一个：

VSync Pulse。

像乐队里的指挥一样：

```
        VSync
          │
 ┌────────┼────────┐
 │        │        │
App   SurfaceFlinger   Display
```

大家听同一个节拍。

于是：

整个系统：

保持同步。

------

# 从更高的角度理解

Display 并不是特殊的。

它其实属于：

计算机里：

非常经典的一类问题：

```
Producer

↓

Shared Buffer

↓

Consumer
```

只不过：

Consumer：

是：

Display。

Producer：

是：

CPU/GPU。

Synchronization：

就是：

保证：

Consumer：

永远读取：

一份：

完整、

一致、

稳定的数据。

------

# 用一句话总结

如果让我用一句 First Principle 来定义 Display Synchronization，我会写成：

> **Display 必须同步，不是因为显示器需要 VSync，而是因为显示本质上是一个生产者（CPU/GPU）与消费者（Display Controller）共享 Frame Buffer 的系统。只有同步，消费者才能读取到同一时刻生成的一整帧数据，而不是混合了多个时间点的数据。**

因此，**VSync、Double Buffer、Triple Buffer、Page Flip、BufferQueue** 看似是不同层的软件和硬件机制，本质上都在回答同一个问题：

> **如何让生产者和消费者在不同速度下安全地交接一帧完整的数据。**

这也是为什么我认为，在 Display 系列中，应该先讲**“为什么必须同步”**，再讲 **VSync**。这样读者理解的就不是一个新名词，而是整个显示系统设计背后的根本原因。



下一步是不是该梳理framebuffer、DRM KMS框架？梳理好！！



**是，但我建议不要直接进入 DRM/KMS。**

按照你整个 SoC 系列（AP → Baseband → DSP）的风格，你其实已经形成了一个固定的方法论：

> **First Principle → 暴露问题 → 演化出下一层架构。**

Display 也应该完全遵循这个规律。

实际上，到目前为止，我们已经推导出了：

```
Binary
    │
    ▼
Pixel
    │
    ▼
Frame
    │
    ▼
Frame Buffer
    │
    ▼
Double Buffer
    │
    ▼
Triple Buffer
    │
    ▼
Synchronization
    │
    ▼
VSync
```

那么下一步应该问什么？

不是：

> **什么是 DRM？**

而是：

> **现在已经有 FrameBuffer 和 Double Buffer 了，为什么 Linux 还要重新设计整个显示子系统？**

**这才是真正的 First Principle。**

------

# 我建议整个 Display 系列改成下面这样

## Part 1（已经完成）

> 为什么需要显示？

推导：

```
Binary
    ↓
Light
    ↓
Pixel
    ↓
Frame
    ↓
FrameBuffer
```

目标：

建立显示最底层物理模型。

------

## Part 2（已经完成）

> 为什么显示必须同步？

推导：

```
Single Buffer
    ↓
Tearing
    ↓
Double Buffer
    ↓
Triple Buffer
    ↓
Synchronization
    ↓
VSync
```

目标：

建立时间模型。

------

## Part 3（我认为这是最重要的一篇）

标题我建议：

> **为什么 Linux 放弃 Framebuffer（fbdev）？**

而不是：

> DRM/KMS

------

因为绝大多数文章都是：

```
fbdev

↓

DRM

↓

KMS

↓

Plane

↓

CRTC

↓

Connector
```

读者：

根本不知道：

为什么。

------

## 正确应该这样推导。

------

# 第一章

## 我们已经拥有 FrameBuffer。

例如：

```
CPU

↓

FrameBuffer

↓

Display Controller

↓

LCD
```

是不是已经够了？

其实：

够。

Linux 最早就是这样干的。

于是：

Linux：

出现：

fbdev。

------

这里可以讲：

```
/dev/fb0
```

以及：

Framebuffer Driver。

甚至：

做实践。

例如：

```
open("/dev/fb0");

mmap();

memcpy();

立即画一个矩形。
```

读者：

第一次：

真正：

控制：

屏幕。

这体验特别好。

------

# 第二章

然后：

马上问：

fbdev 有什么问题？

这里千万不要直接说：

API 老。

不是。

要说：

它解决不了现代 GPU。

为什么？

因为：

以前：

```
CPU

↓

FrameBuffer

↓

LCD
```

今天：

```
APP

↓

GPU

↓

Composition

↓

Display Controller
```

已经完全不同了。

------

然后继续。

举例。

如果：

两个 APP：

都要显示：

怎么办？

fbdev：

只有：

```
/dev/fb0
```

一块。

谁画？

------

继续。

视频播放器。

字幕。

鼠标。

游戏。

通知栏。

谁负责：

合成？

fbdev：

没有。

------

然后继续。

HDMI。

DP。

MIPI。

USB-C。

多个屏幕。

怎么办？

fbdev：

不会。

------

于是。

问题越来越多。

------

# 第三章

终于。

Linux 社区：

重新思考：

Display。

这里：

千万不要：

直接：

介绍：

DRM。

而是：

先问：

如果重新设计。

应该抽象什么？

例如。

Display：

到底有哪些东西？

不是：

Framebuffer。

而是：

```
GPU
↓

产生 Frame
Display Controller

↓

扫描 Buffer
Panel

↓

真正发光
HDMI

↓

输出
```

于是：

其实：

一个 Display：

至少：

包含：

四种角色。

这里：

自然：

引出：

DRM：

对象模型。

------

# 第四章

这里：

终于：

介绍：

KMS。

为什么：

叫：

Kernel Mode Setting？

以前：

Mode Setting：

在哪里？

X Server。

为什么：

搬到：

Kernel？

这里：

又可以：

讲：

Linux：

历史。

这一章：

会特别自然。

------

# 第五章

这里：

整个：

DRM：

架构。

终于：

出来。

例如：

```
Userspace

↓

libdrm

↓

DRM ioctl

↓

DRM Core

↓

KMS

↓

Driver

↓

Display Controller
```

然后：

介绍：

五个对象。

```
Framebuffer

CRTC

Plane

Encoder

Connector
```

不是：

介绍。

而是：

回答：

为什么：

必须：

拆成：

五个对象。

例如：

为什么：

Framebuffer：

不能：

直接：

接：

Panel？

因为：

中间：

还有：

Display Controller。

为什么：

Connector：

独立？

因为：

HDMI。

DP。

MIPI。

eDP。

都只是：

输出方式。

这样：

整个：

抽象：

就自然了。

------

# 第六章

实践。

这里：

建议：

不要：

讲：

Android。

先：

Linux。

例如：

```
modetest
```

看看：

Plane。

Connector。

CRTC。

然后：

```
drm_info
```

然后：

```
kmscube
```

最后：

画：

一个：

Page Flip。

读者：

真正：

看到：

DRM：

在工作。

------

# 然后下一篇

才：

Android。

例如：

```
App

↓

Surface

↓

BufferQueue

↓

SurfaceFlinger

↓

HWC

↓

DRM/KMS
```

你会发现：

Android：

其实：

只是：

Linux Display Stack：

上面：

再加：

一层。

不是：

另一套东西。

------

# 我认为你的 Display 系列最终应该长这样（推荐）

```
Part 1
────────────────────────────
为什么需要显示？
Pixel
Resolution
Frame
Refresh
FrameBuffer

↓

Part 2
────────────────────────────
为什么显示必须同步？
Double Buffer
Triple Buffer
VSync
Page Flip（概念）

↓

Part 3
────────────────────────────
为什么 Linux 放弃 fbdev？
fbdev
/dev/fb0
Framebuffer Driver
为什么失败？
现代显示的新需求

↓

Part 4
────────────────────────────
Linux DRM/KMS
DRM Core
KMS
CRTC
Plane
Encoder
Connector
Atomic Modesetting
Atomic Commit

↓

Part 5
────────────────────────────
Android Graphics
Surface
GraphicBuffer
BufferQueue
SurfaceFlinger
HWC
VSYNC Source
Fence
Composition

↓

Part 6
────────────────────────────
Display Driver
MIPI DSI
DSI Host
Panel Driver
Bridge
Backlight
Boot Logo
Panel Bring-up
```

------

## 我还建议增加一个"桥梁篇"

这是我觉得目前大多数 Display 教程最缺失的一环，也是你的系列可以做出特色的地方。

单独写一篇：

> **移动 SoC 内部组成（六）：为什么 Linux 放弃 fbdev，并重新设计 DRM/KMS？**

这一篇**几乎不讲 API，不讲 ioctl，不讲结构体**，而是只回答：

- 为什么 `/dev/fb0` 在 1995 年是一个优秀设计？
- 为什么 GPU、多窗口、视频叠加、多显示器让它逐渐力不从心？
- Linux 内核开发者重新抽象显示系统时，为什么会得到 **Framebuffer、Plane、CRTC、Encoder、Connector** 这些对象？
- 为什么后来又从 Legacy KMS 演进到 **Atomic KMS**？

这样，读者阅读 DRM/KMS 时，不是在背对象模型，而是在理解**这些对象为什么必须存在**。这与前面 Baseband、DSP 系列一脉相承，也是你整个 SoC 系列最鲜明的特色。