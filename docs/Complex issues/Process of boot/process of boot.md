> 这里简单讲一下关于这类芯片启动流程：
>
> Boot ROM 位于芯片内部的起始地址0x00000000处，大小为96KB。这个区域包含了启动引导程序，它负责从指定的启动设备（如 SD 卡、eMMC、NAND Flash 等）加载操作系统或应用程序的镜像，并将其复制到 RAM(外部的 DDR) 中，然后跳转到镜像的入口点开始执行。
>
> > 上面这个过程涉及到读取存储设备上的 IVT（Image Vector Table）、Boot Data 和 DCD（Device Configuration Data）等信息，这些信息告诉 Boot ROM 如何加载和验证镜像文件。
>
> 这里也有个问题，从指定的启动设备加载镜像，怎么加载？CPU 怎么读取这部分程序做到的？这部分bootROM程序究竟写了什么？搬运指令？
>
> ***==own version, not official version.==***

这里大家可能会有点想法，这个 MPU 的内部也有 SRAM 和ROM 呀，这和前面的 MCU 又有什么区别？为什么不能像 MCU 那样将代码下载到ROM里，然后data 放到 RAM 里呢？

这里我们就暂且认为，MPU 这边一般要运行比较大的程序，使用一些比较复杂的硬件设备（memory controller），所以在启动的时候需要一些代码来初始化他们，而由于成本问题，CPU core 已经很贵了，如果还在里面将能跟上 CPU 速度 的 SRAM 扩大容量，成本自然受不了。所以，MPU内部的 ROM 也被较为 bootROM 用于存放启动代码、内部 SRAM 用作缓冲、低功耗保存到一些数据等等。再进一步深入就有了 multi-stage bootloader

那我们说的 MCU(STM32) 有没有像 bootROM 一样的这种东西呢？可以说有他这种功能的器件，就是系统存储器，一般用于的是串口下载代码的功能的。

> 这个问题其实也合理的，这里留坑，总结成另一篇文章。 
>
> ###### **==DOTO==**
>
> MPU 的 bootROM 放的是系统启动时所需的初始化代码，当系统上电或者复位的时候，MPU 从 bootROM 开始执行，执行一些基本的初始化：设置时钟、初始化内存控制器等等；然后它负责将从指定的启动设备加载镜像，并复制到 DDR 中。
>
> 这里又有一个问题了，那 MCU-STM32 那便是怎么启动的呢？他有没有像 MPU 那样的带有 bootROM 的呢？实际上是有的，这就不得不说到STM32的启动模式了，如下文：
>
> [【ARM Cortex-M开发实战指南(基础篇)】第3章 Cortex-M启动流程详解(GCC版) - BruceOu的博客](https://blog.bruceou.cn/2022/11/3-detailed-explanation-of-cortex-m-startup-process-gcc-version/1889/)
>
> [深入理解MCU启动原理 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/652795256)