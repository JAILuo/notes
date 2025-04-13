## Motivation

STM32的bootROM 和 内部的flash理解，flash是ROM吗？

我知道厂商的boot loader是放在bootROM（manual说的system memory）的，比如选择从ROM启动，处理器将描述ROM的那个地址空间映射到复位地址0x00000000（具体来说，在芯片层面上，这是怎么做映射的？可以做拓展讲解！！！），具体这里面的程序（bootloader）就可能是监听你的串口有没有发送开始的信号（比如是0XF1），如果是，然后就开始从串口接受hex文件。（就是网上的IAP下载工具原理是吧？），接收到的固件程序就逐个地刷到flash memory上（就是manual上的user flash）。

为什么叫BootROM，厂商刷进去的，不能改的？

我记得还有一种特别的bootloader：CPU上电后，会将0x00000000映射到system memeory那个区域，然后具体再在这里去判断boot0、boot1的组成的启动方式，由此再判断是从flash memory还是从system memeory，还是从SRAM启动。（少部分固件是用这种方式，芯片手册也没有讲）

综上，上面是我的理解和一些问题，请专业高质量地回答！！！我想要在这方面做得更好！



## notes

您对STM32的BootROM和内部Flash的理解基本正确，但需要更专业的细节补充和修正。以下是分层技术解析：

**一、BootROM与Flash的物理特性**

1. **BootROM（System Memory）**：
- 本质是Mask ROM（掩膜ROM），属于OTP（One-Time Programmable）存储器
- 由ST工厂通过光刻工艺固化程序，物理上不可修改
- 典型容量：2-32KB（依具体型号而定，如STM32F1系列为2KB）
- 包含厂商预置的Bootloader程序（如USART/I2C/USB DFU等协议栈）

2. **内部Flash（User Flash）**：
- 属于NOR Flash存储器，支持多次擦写（典型耐久度：10^4~10^5次）
- 通过FPEC（Flash Program/Erase Controller）模块管理
- 地址范围通常为0x08000000~0x0807FFFF（512KB型号）
- 分为主存储区（Main Memory）和选项字节（Option Bytes）

**二、地址映射机制（硬件层面）**
1. **启动阶段重映射**：
- 芯片复位时，根据BOOT引脚状态选择启动源：
  - BOOT0=0: 从Main Flash启动（0x08000000→0x00000000）
  - BOOT0=1, BOOT1=0: 从System Memory启动（0x1FFF0000→0x00000000）
  - BOOT1=1: 从SRAM启动（0x20000000→0x00000000）

- 实现原理：通过芯片内部的地址重映射控制器（Remap Controller）
  ```c
  // 硬件级伪代码示意
  if(RESET){
      uint32_t boot_source = GPIO_ReadBootPins();
      switch(boot_source){
          case BOOT_FROM_FLASH:
              MemoryRemap(0x08000000, 0x00000000, 256KB);
              break;
          case BOOT_FROM_SYSTEM:
              MemoryRemap(0x1FFF0000, 0x00000000, 16KB);
              break;
          //...
      }
  }
  ```

2. **执行流程**：
- 复位后CPU首先从0x00000000读取初始SP和PC值
- 该地址实际指向重映射后的存储区域
- 执行厂商Bootloader时会初始化时钟、外设等基础硬件

**三、IAP实现深度解析**
1. **标准IAP流程**：
- 厂商Bootloader通过USART1接收YMODEM协议数据包
- 数据校验通过后调用系统编程函数写入Flash：
  ```c
  void STM32_WriteFlash(uint32_t addr, uint8_t *data, uint32_t len){
      FLASH_Unlock();
      FLASH_ClearFlag(FLASH_FLAG_EOP | FLASH_FLAG_PGERR);
      for(int i=0; i<len; i+=2){
          FLASH_ProgramHalfWord(addr+i, *(uint16_t*)(data+i));
      }
      FLASH_Lock();
  }
  ```
- 关键安全机制：
  - 选项字节写保护（RDP级别）
  - Flash擦除前双重校验
  - 中断向量表重定向

2. **高级启动模式**：
- 部分型号（如STM32H7）支持灵活启动配置：
  - Dual-Bank启动（支持AB分区切换）
  - Secure Boot（加密固件验证）
  - XIP（Execute In Place）模式直接从QSPI Flash执行

**四、芯片级地址映射实现**
1. **硬件总线矩阵**：
- Cortex-M内核通过AHB总线矩阵连接存储区域
- 重映射操作实质是修改总线矩阵的地址解码规则
- 典型总线矩阵配置：
  ```
  [AHB Bus Matrix]
  | Master       | Slave           | Access Path       |
  |--------------|-----------------|-------------------|
  | Cortex-M Core| Flash Interface | 0x00000000-0x1FFFFFFF |
  | DMA1         | SRAM            | 0x20000000-0x3FFFFFFF |
  | USB OTG      | FSMC            | 0x60000000-0x9FFFFFFF |
  ```

2. **动态重映射示例**：
- 某些型号支持运行时重映射（如STM32F4的MEMRMP寄存器）：
  ```c
  // 在用户代码中动态切换映射
  SYSCFG_MemoryRemapConfig(SYSCFG_MemoryRemap_SRAM);
  // 此时0x00000000将指向SRAM区域
  ```

**五、进阶开发建议**
1. **自定义Bootloader开发**：
- 需处理中断向量表重定位：
  ```c
  SCB->VTOR = FLASH_BASE | VECT_TAB_OFFSET;
  ```
- 实现安全固件验证（如SHA-256签名校验）
- 支持多协议升级（USB CDC/ETH/CAN-FD等）

2. **Flash优化技巧**：
- 使用半字/字编程提高写入速度
- 利用Flash加速模块（如ART Accelerator）
- 合理规划Flash分页（Page/Sector布局）

3. **调试技巧**：
- 通过DBGMCU_CR寄存器冻结Bootloader执行
- 使用JTAG/SWD接口直接读写System Memory区域
- 分析选项字节（OPTCR寄存器）的写保护状态

**六、特殊案例解析**
部分型号（如STM32L0系列）存在隐藏启动模式：
- 通过特定GPIO序列进入ROM DFU模式
- 系统存储器中包含USB-PID伪装功能（模拟U盘）
- 时钟树自动适配特性（无需外部晶振即可启动）

建议结合具体型号参考以下文档：
- AN2606: STM32 microcontroller system memory boot mode
- PM0081: STM32F10xxx Flash programming manual
- AN3155: USART protocol used in STM32 bootloader

这种硬件级的设计使得STM32在工业控制领域具备极高的可靠性，开发者需深入理解存储架构才能充分发挥其潜力。