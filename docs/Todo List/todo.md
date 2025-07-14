## 搭建 Linux 下 MCU 开发环境

https://blog.csdn.net/ldl617/article/details/120307412





## 移植Linux 到 GD32/STM32 上

主要是想为协会的 GD32 开发板做一些比较好玩的东西，还有是因为看了阅马场的Linux驱动第一期的内容，可以直接将 Linux 跑在自己的 MCU 上！！

留个坑。

可以参考 [b站全网首发 纯手写 RISC-V CPU虚拟机 juicevm 在esp32 上运行linux5.0](https://www.bilibili.com/video/BV11b4y167Z6/?spm_id_from=333.1387.homepage.video_card.click&vd_source=ecc99d78ae961113010161a48a475a35)

[来了来了，用单片机 ESP32-S3 跑 RISC-V 模拟器运行 Linux，这次启动只要 8 秒 | Architecting Life](https://xujiwei.com/blog/2024/08/run-linux-on-esp32s3/)

[xhackerustc/uc-rv32ima: Run Linux on MCUs such as ESP32C3 with RISC-V emulator](https://github.com/xhackerustc/uc-rv32ima)



因为 GD32 不带有 MMU，所以怎么模拟？

> 移植Linux到GD32这类没有MMU（内存管理单元）的设备上，通常需要使用Linux的Flat Memory Model（平面内存模型）或者使用特定的内存管理技术来模拟MMU的功能。以下是一些基本步骤和考虑因素：
>
> 1. **选择Linux内核版本**：
>    - 选择一个支持RISC-V架构且不需要MMU的Linux内核版本。Linux 5.0版本是一个很好的起点，因为它包含了对RISC-V的支持。
>
> 2. **配置内核**：
>    - 在内核配置中，需要禁用所有与MMU相关的选项，因为GD32没有MMU。这包括但不限于：
>      - `CONFIG_MMU` 应该被禁用。
>      - 相关的内存管理选项也应该被禁用或配置为适合平面内存模型。
>
> 3. **内存布局**：
>    - 设计一个适合GD32的内存布局。在没有MMU的情况下，所有的代码、数据和堆栈通常都位于一个单一的连续的地址空间内。
>
> 4. **虚拟内存模拟**：
>    - 如果需要使用虚拟内存，可以考虑使用软件模拟的方法。例如，可以使用固定大小的页表来模拟虚拟内存，但这会牺牲性能。
>
> 5. **驱动程序和硬件支持**：
>    - 确保所有需要的驱动程序都可用，并且已经为GD32进行了适配。这可能包括串口、网络、存储等驱动。
>
> 6. **文件系统和应用程序**：
>    - 选择一个适合嵌入式设备的文件系统，如FAT32、ext4等，并确保所有应用程序都已针对没有MMU的环境进行了优化。
>
> 7. **调试和测试**：
>    - 使用JTAG或其它调试工具进行系统的调试和测试。确保系统稳定运行，并且所有功能都按预期工作。
>
> 8. **性能优化**：
>    - 由于没有MMU，系统的性能可能会受到影响。需要对代码进行优化，以减少内存碎片和提高效率。
>
> 9. **参考项目**：
>    - 参考类似项目，如juicevm在ESP32上运行Linux的案例。虽然ESP32和GD32在硬件上有所不同，但是移植Linux的过程和挑战是相似的。
>
> 10. **社区和文档**：
>     - 利用Linux社区和相关文档，如Linux内核的文档和邮件列表，获取帮助和最佳实践。
>
> 移植Linux到没有MMU的设备是一个复杂的过程，需要对内核有深入的了解，并且需要耐心地调试和优化。如果你不熟悉这个过程，可能需要花费一些时间来学习相关的知识，或者寻求社区的帮助。



我记得有个 ucLinux？

[ucLinux 开发简述](https://www.bilibili.com/video/BV1tySFY2EyE/?spm_id_from=333.1387.homepage.video_card.click&vd_source=ecc99d78ae961113010161a48a475a35)



[c - Possible to implement MMU functionality in software with GCC? - Stack Overflow](https://stackoverflow.com/questions/74847127/possible-to-implement-mmu-functionality-in-software-with-gcc)





还记得那个李述铜的课程吗？实际上是模拟一块 RISC-V MCU？

[Cortex-M MCU Emulation with Renode | Interrupt](https://interrupt.memfault.com/blog/intro-to-renode#what-is-renode)





发现一个很不错的东西！！

[johnnywei499/linux-for-microcontroller: A complete project that can run Linux-3.12.74 on a microcontroller, and the hardware development environment is easily accessible.](https://github.com/johnnywei499/linux-for-microcontroller)





## 2024.12.7

完成了 NEMU 初步启动 nommu-Linux 后，下一步的学习计划。

大致可以分为以下几部分：

- 开始补充项目

    - OS 内核及相关子系统设计及相关功能（这里应该将kernel 和 system programing 分开的，但之后再说吧）
        - xv6 的设计实现
        - [jhbdream/armv8_os: a simple armv8 operating os for study](https://github.com/jhbdream/armv8_os)
        - rcore
        - jyy lab
        - 剩余就是 市面上成熟的 OS：Linux、FreeRTOS、Zephyr...
    - 硬件/软件项目尽量全打通，尽量带驱动

- 刷课

    尽量补充知识面

    - jyy os





- 可选

    nemu 添加更多内容

    - plic

    - 模拟器浮点扩展

        可以对比实现 navy 的浮点实现（固定点数）和 RV32F/D 扩展？

    - cache

        nemu 的memory 设计是怎么样的

        [RISC-V Base Cache Management Operation ISA Extensions](https://lists.riscv.org/g/tech-cmo-archived-2022/attachment/865/0/cmobase-v0.5.1.pdf)

        [icspa-public-guide/ch/ch_pa-3-1_cache.md at master · ics-nju-wl/icspa-public-guide](https://github.com/ics-nju-wl/icspa-public-guide/blob/master/ch/ch_pa-3-1_cache.md)

        [计算机系统基础综合实践 NEMU PA3 | aa10n's blog](https://aa10n.github.io/计算机系统基础/NEMUPA3/)

        [计算机系统基础实验——Cache的模拟 - 简书](https://www.jianshu.com/p/90019724f95e)

        [NEMU PA3 必做任务1及选做任务1 实验思路分享_nemupa3-CSDN博客](https://blog.csdn.net/Kingwell_/article/details/142312585)

        [[mmu/cache\]-ARMV8-aarch64的虚拟内存(mmu/tlb/cache)介绍-概念扫盲 - 哔哩哔哩](https://www.bilibili.com/read/cv33615873/?opus_fallback=1)

        实在不行，可以放弃这个，做一个cache模拟器。

        [【计组实验】构建32位Cache模拟器(C语言) - 知乎](https://zhuanlan.zhihu.com/p/637144163)

        [CSAPP | Lab5-Cache Lab 深入解析 - 知乎](https://zhuanlan.zhihu.com/p/484657229)

        或许可以做完 CSAPP的 cache 后将其添加进 nemu？

    - 深入 MMU

        [Lab 4: RISC-V 虚拟内存管理 - 知乎](https://zhuanlan.zhihu.com/p/456799846)

    - 物理内存保护 PMU

        [RISC-V架构——物理内存属性和物理内存保护_riscv pma-CSDN博客](https://blog.csdn.net/weixin_42031299/article/details/133892479)
    
        或者，不同模式下访问的寄存器权限
    
    - 多核的模拟器
    
        先入门多核处理器









