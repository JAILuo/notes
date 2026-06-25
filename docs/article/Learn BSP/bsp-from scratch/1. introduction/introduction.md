# introduction

记录：

- 学习该系列的内容：[从零开始的BSP之路](https://mp.weixin.qq.com/s/lXqWC58aODnpJc8qRD-6sA)

    分析它的相关经验

- 自己折腾的内容





# 几个观点

1. 驱动开发的本质：

    理解硬件协议 → 理解 SoC 控制器 IP 设计 → 理解内核抽象模型 → 落地到驱动实现

2. BSP 的能力

    真正的 BSP 的能力，并不是只会改 dts，而在于：

    当你在使用官方驱动时遇到问题、文档描述不够清晰、某个功能性能与预期不一致时，你有能力回到控制器本身，结合芯片手册，对问题进行系统性地插接与分析。

    我们负责的时底层软件，但底层软件并不是孤立存在的。当我们能够**把芯片手册、驱动实现、内核子系统、实际行为，这几层逻辑串起来**时，也就具备了独立定位与解决问题的能力

    > 对于这部分，结合自己的经验还是回归到状态机的理论。
    >
    > - 芯片手册描述的是对应 SoC 支持的硬件功能以及各种特性（比如说 SDMMC 流控、内存地址空间）（硬件也是状态机，某一些功能特性使得芯片运行时通过不同的状态迁移走到了不同的状态）
    > - 驱动描述的是如何利用软件控制硬件（Unix的机制与策略分离，下面类似）
    > - 内核子系统体现这一款 OS kernel 对于这个外设、资源提出了怎样的设计考虑
    >     - 抽象：把一个复杂的问题变成一个能被人处理的形式：比如如何简化写驱动的工作
    >     - 分解：拆分成小问题，找到各自的联系：比如怎么，性能、安全、功耗有综合的考量
    >     - 模式识别：识别到这个设计和哪些之前见到过的设计类似？
    > - 实际行为：整个硬件到软件的走的数据flow都清晰（状态机）





# RK3399

- ARMv8

    - 2 × Cortex-A72 + 4 × Cortex-A53
        - [ARM Cortex-A72 MPCore Processor Technical Reference Manual](https://developer.arm.com/documentation/100095/0003/?lang=en)
        - [ARM Cortex-A53 MPCore Processor Technical Reference Manual](https://docs.arduino.cc/resources/datasheets/cortexa53.pdf)

    > 那这里能玩什么呢？
    >
    > 



