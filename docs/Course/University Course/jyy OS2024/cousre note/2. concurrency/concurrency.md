只记录部分。



## 多处理器编程

<img src="pic/image-20241110231300436.png" alt="image-20241110231300436" style="zoom:50%;" />

- 证明共享内存

    > **==DEMO==**
    >
    > **并发线程模型**：**并发线程能够读写共享的 heap 堆区**。除此之外，每个线程持有局部变量的副本。Mosaic 不会自动在每条语句之后进行线程调度：我们需要手工插入 `sys_sched`。







## 并发控制：互斥（1）

<img src="pic/image-20241118211713662.png" alt="image-20241118211713662" style="zoom:50%;" />

怎么应对？



### 阻止并发（并行）的发生

什么叫互斥？什么叫并发？

> **Concurrent** means happening at the same time

”要求整个世界有小段时间只属于自己，任何人都不能打断“

”人想象成线程，多线程想象成物理世界“

- **互斥** (互相排斥)：阻止并发

<img src="pic/image-20241118211611213.png" alt="image-20241118211611213" style="zoom:50%;" />

**那如何实现互斥？**

单核实现互斥：关中断

<img src="pic/image-20241118214211804.png" alt="image-20241118214211804" style="zoom:50%;" />

> ###### **==DEMO==**
>
> **Stop-the-world 实现互斥**：对于操作系统上的应用程序，关闭中断是不能容忍的：这会使微小的 bug 或是恶意的程序破坏计算机的运行。操作系统正是因为统治了中断，才实现了对应用程序的管理。**在操作系统内核的实现中，关闭中断是一个常见的操作。**
>
> ```C
> // Clear FL_IF in the CPU.
> // Interrupt disabled.
> asm volatile("cli");
>                                                                                                                         
> // Set FL_IF in the CPU.
> // Interrupt enabled.
> asm volatile("sti");
> 
> ```

> 例外：不可屏蔽中断 NMI (Non-Maskable Interrupts) [Non Maskable Interrupt - OSDev Wiki](https://wiki.osdev.org/Non_Maskable_Interrupt)
>
> - 可以利用 NMI 实现错误监控
>     - 设置硬件定时触发
>     - 操作系统定时复位定时器
>     - 触发 timeout，执行 NMI 处理程序
>         - 例如，重启计算机
>
> 为什么会有这个不可屏蔽中断？
>
> 其实刚开始我对这个概念是很迷糊的，并没有具体大印象和概念，因为自己并不是对电脑特别的熟悉，毕竟是说从上大学才开始接触，学习完成PA，对软件和硬件有了一定对了解之后，其实计算机中的任何东西都是人造出来的，受到各种各样的因素软件和硬件都会有错误（当然现在的计算机软硬件可能相对完善），很多的错误情况在硬件和软件上都会通过各种方式来告知我们它坏了，而这种方式就是前人遇到了类似的问题，他们想出来了一种方案，最终实施到计算机上。
>
> NMI 或许就是这么一种方式（我只是这么方便理解，只是猜的）。所以我对 NMI 及中断处理程序 的理解其实也就是处理一些不可恢复极其重要的硬件故障错误以及让我们修复它，不然计算机就没法工作啦。比如芯片内部某处出现故障；内存条损坏，操作系统怎么能发现？ECC、奇偶校验？
> 这也就是为什么很多老式的机器上会有复位按键。
>
> 可能上面还是很迷糊，再举个例子，在嵌入式中挺有用的：在处理器因静电放电而陷入循环时。当常规中断关闭时，系统无法恢复错误状态，而NMI因其不可屏蔽性，可以通过来自看门狗定时器、协处理器或人工按钮的信号使处理器恢复工作状态。
>
> 再如：NMI处理程序可以处理如热事件或电源故障等情况，以防止损坏或确保在断电前将数据备份到非易失性存储。



那多处理器呢？

<img src="pic/image-20241118211902945.png" alt="image-20241118211902945" style="zoom:50%;" />



### 使用 load/store 实现互斥（）

主要是**Peterson 算法**。直接看看讲义和视频讲解吧。



### 在多处理器上实现互斥

<img src="pic/image-20241118212608893.png" alt="image-20241118212608893" style="zoom:50%;" />

需要意识到：**因为人类是“sequential creatures”，导致过去的很多设计是没有考虑并发的（多处理器、共享内存），而我们在共享内存上实现互斥的失败和成功尝试后，我们意识到软件需要和硬件协同工作，并在硬件原子指令基础上实现了基础版本的自旋锁。**

关键在于硬件实现，在 OS 课上可不用深究，不属于本门课的范围。

> 更多内容：
>
> [x86 - How are atomic operations implemented at a hardware level? - Stack Overflow](https://stackoverflow.com/questions/14758088/how-are-atomic-operations-implemented-at-a-hardware-level)
>
> [computer architecture - How does an atomic operation guarantee consistency from a hardware perspective? - Super User](https://superuser.com/questions/400786/how-does-an-atomic-operation-guarantee-consistency-from-a-hardware-perspective)
>
> [计算机原子（atomic）操作的实现原理解析 - 知乎](https://zhuanlan.zhihu.com/p/649646816)
>
> 这里可以总结为：
>
> Extra transistors in the chip to implement **special cache** and memory coherency and **bus synchronization procotols**. The long answer is way too long.
>
> 再进一步举例相关实现手段：
>
> 总线锁定、缓存锁定、相关缓存一致性协议、LL/SC（LR/SC（armv8的独占加载、独占存储））
>
> 具体怎么实现？我觉得这应该属于体系结构、多核处理器设计上的相关内容了，看看怎么对总线操作？
>
> [内存一致性(Memory Consistency) - 知乎](https://zhuanlan.zhihu.com/p/422848235)
>
> 可以再好好总结。。**==TODO==**



实现。

> 为 add/inc 等指令增加 lock 的前缀，处理器硬件会实现将这条指令实现为原子指令。

![image-20250108234540240](pic/image-20250108234540240.png)

提出这个自旋锁还是挺自然的，顺着之前上厕所的例子，厕所有人（线程1），我（线程2）就一直在门口等着呗？我就堵在这呗，什么时候线程1好了，我再进去上厕所呗。

> 看到这里总是会想着优化，这个线程堵了，OS 让 CPU 执行别的 线程，别浪费呀。有没有能不堵的方法？肯定有！互斥锁吗？在 `FreeRTOS` 里用过一点，但是是单核上的 MCU 的。

<img src="pic/image-20241118212545883.png" alt="image-20241118212545883" style="zoom: 50%;" />

终于，我们借助**计算机硬件提供的短时原子性**实现了多处理器间的互斥。







## 并发控制：互斥（2）

### 现实要求但有人不遵守

理想的实现以及效果。

![image-20250109120936754](pic/image-20250109120936754.png)

都得遵循这个规则。如果没有？忘记加锁、再加了一次？

![image-20250109120904253](pic/image-20250109120904253.png)



### 操作系统内核中的自旋锁

> 之前课上的例子是在应用程序上的实现互斥，因为应用程序不能关中断。
>
> 但别忘了，操作系统才是第一个并发程序，我们需要解决内核中怎么做到互斥以实现正确的并发，
>
> 只有操作系统为实际计算中的并发打下基础，应用程序才能直到如何管理多个线程和进程。

但我还可以接着之前应用程序的内容来实现内核相关的内容。有了lock，那就能保证互斥？对于内核来说？回想计算机状态机的模型：

![image-20250109122200699](pic/image-20250109122200699.png)

也就是说，能改变当前计算机的状态的，还有中断。

> - 操作系统接管了完整的计算机系统
>     - 每个处理器都并行 x++
>     - 每个处理器中断发生时执行 x += 1000000000
>     - (假想 x 是操作系统中的数据结构，例如进程表)
> - 如何正确实现 x 的原子访问？
>     - 仅仅自旋是不够的
>     - **因为还有中断**

lock() -> sum++ -> 中断来了 -> (有临界区，中断也想对sum++) -> (但是之前已经lock过，所以就死在这里了！deadlock)

> 中断的发明，由于 IO 比 CPU 慢很多，IO 做完了再告诉 CPU 来处理我相关的，它们是异步的。



那怎么做？单核怎么做的，加到这里来呗。关中断。

那也自然带来一个问题：是在lock前关中断还是lock后关中断？

自然是在 lock 前关中断，如果是在lock后，那在那一瞬间还是会来中断，依然会造成deadlock。

> `disable irq` -> `lock` -> `sum++` ->`enable irq`

有个问题，到最后的时候，变成了开中断，但如果在 `disable irq` 之前的 CPU 状态就是 关中断呢？

所以，需要保存中断状态！

> 哦，这就是我在 NEMU 移植 Linux 的时候看的 Linux kernel 代码里的 `arch/risc-v` 里看到的 `arch_local_save_flags` ？
>
> ```C
> #ifdef CONFIG_TRACE_IRQFLAGS_SUPPORT
> #define irqs_disabled()                 \
>     ({                      \
>         unsigned long _flags;           \
>         raw_local_save_flags(_flags);       \
>         raw_irqs_disabled_flags(_flags);    \
>     })
> #else /* !CONFIG_TRACE_IRQFLAGS_SUPPORT */
> #define irqs_disabled() raw_irqs_disabled()                                                                               
> #endif /* CONFIG_TRACE_IRQFLAGS_SUPPORT */
> //include/linux/irqflags.h
> 
> #define raw_local_save_flags(flags)         \                                                                             
>     do {                        \
>         typecheck(unsigned long, flags);    \
>         flags = arch_local_save_flags();    \
>     } while (0)
> // include/linux/irqflags.h
> 
> /* read interrupt enabled status */
> static inline unsigned long arch_local_save_flags(void)
> {
>     return csr_read(CSR_STATUS);
> }
> 
> /* unconditionally enable interrupts */
> static inline void arch_local_irq_enable(void)
> {
>     csr_set(CSR_STATUS, SR_IE);
> }
> // arch/riscv/include/asm/irqflags.h
> ```

<img src="pic/image-20250109130549323.png" alt="image-20250109130549323" style="zoom:50%;" />



无论实现什么，先认为是对的，先写一个测试用例？

实现一个自旋锁，相比实现一个自旋锁的test driver 不那么重要。？？



这里对 lock、自旋锁、原子指令、互斥等各种名词都快绕晕了，需要总结。

上面的 自旋锁实现 实际是基于原子指令的，再加上关中断，能正确实现互斥。

先记住这么一条：这么做是一种解决方案，肯定还有别的。


学习 xv6 的 spinlock。





### 7.2 操作系统内核中的 (半) 无锁互斥：Read-Copy-Update 🌶️

**在真正的操作系统中实现互斥，其实没有那么简单。**

> scalability

假如采用上面的那种方案实现互斥：自旋 + 关中断。

首先，自旋锁的缺点，scalability 非常差，每次需要并发控制的时候，内核就卡在那里不动，如果时间很长，极大地浪费了硬件资源。

再者，关中断同样也不能关太长，关 1 秒的中断，就忽略了很多的时钟中断（就假如10ms来一个，100个），在这些时钟中断，操作系统内核会切换到别的线程，那这样很多线程/任务耗费的时间很长，极大影响性能。

综上，在内核中，上面这种方案尤其自旋锁，只能用在很短的临界区（比如并发的数据结构，往一个链表里添加一个元素、按键按下键码放队列）

![image-20250109213447063](pic/image-20250109213447063.png)

怎么解决？[An Analysis of Linux Scalability to Many Cores | USENIX](https://www.usenix.org/conference/osdi10/analysis-linux-scalability-many-cores)

> - 许多操作系统内核对象具有 “**read-mostly**” 特点
>     - 路由表
>         - 每个数据包都要读
>         - 网络拓扑改变时才变更
>     - 用户和组信息
>         - 无时不刻在检查 (Permission Denied)
>         - 但几乎从不修改用户

读写不对称性

写时复制

多版本

读 不上锁，写 上锁







### 应用程序中的互斥

现在考虑在应用程序中，自旋带来的性能问题

- 性能问题 (1)

    除了进入临界区的线程，其他处理器上的线程都在空转

    - 争抢锁的处理器越多，利用率越低
    - 如果临界区较长，不如把处理器让给其他线程

- 性能问题 (2)

    应用程序不能关中断……

    - 持有自旋锁的线程被切换
    - 导致 100% 的资源浪费
    - (如果应用程序能 “告诉” 操作系统就好了)

想想，如果在64个线程对一个资源进行抢占，有一个抢到了，那剩下的 63 个怎么做？

没法进入临界区进行计算，那最自然的想法是什么？既然一直在这等着不行，那就不等了？去做有意义的计算？

回想计算机状态机模型，如果状态一直卡在这里，怎么办？还是应用程序？只能 `syscall`。（也就是互斥锁）

把这种锁放到 kernel 实现就好啦，因为 kernel 有能力做上下文切换呀，能切换别的线程。

![image-20250109220653328](pic/image-20250109220653328.png)

> 这个 OJ 例子还是挺形象的哈哈，又比如等成绩的时候，别等了，本来就啥也干不了，去做别的。

> 这就想到了之前学习 `FreeRTOS` 的互斥锁了，既然等不到，那就用 `mutex_acquire` 放弃这个任务，去做别的线程的任务吧。有点类似

模型：

<img src="pic/image-20250109221906985.png" alt="image-20250109221906985" style="zoom: 67%;" />

我觉得这个图已经形象地描述了。



#### `pthread Mutex Lock`  

> - 一个足够高性能的实现
>     - 具有相当不错的 scalability
>     - 更多线程争抢时也没有极为显著的性能下降
>
> - 使用方法：与自旋锁完全一致
>
>     ```C
>     pthread_mutex_t lock; 
>     pthread_mutex_init(&lock, NULL); 
>     pthread_mutex_lock(&lock); 
>     pthread_mutex_unlock(&lock); 
>     ```





#### Futex: Fast Userspace muTexes 🌶️

> 一般来说，我们上锁和解锁又会有 `syscall`，而这个不会，这种方法会把尽可能多的运算放到用户空间

- 小孩子才做选择。操作系统当然是全都要啦！

    - **性能优化的最常见技巧：**

        **考虑平均而不是极端情况**

        - **RCU 就用了这个思想！**

- Fast Path: 自旋一次

    - 一条原子指令，成功直接进入临界区

- Slow Path: 自旋失败

    - 请求系统调用 `futex_wait`
    - 请操作系统帮我达到自旋的效果
        - (实际上并不真的自旋)



怎么实现？

> - 比你想象的复杂
>    - 如果没有锁的争抢，Fast Path 不能调用 `futex_wake`
>     - 自旋失败 → 调用 `futex_wait`→ 线程睡眠
>        - 如果刚开始系统调用，自旋锁被立即释放？
>         - 如果任何时候都可能发生中断？
>
>      - 并发：水面下的冰山
>    - [LWN: A futex overview and update](https://lwn.net/Articles/360699/)
>     - [Futexes are tricky](https://cis.temple.edu/~giorgio/cis307/readings/futex.pdf) by Ulrich Drepper

关键在于用系统调用来实现这个？

**==TODO：留坑==**





#### 对比三种互斥手段

学习到了，在 AI 时代，使用良好的 prompt 学会科学地提问，总能大幅提高你的效率，但我认为我应该清楚我正在做什么，我有什么目的，能否清晰地描述出我的需求。

![image-20250109230621303](pic/image-20250109230621303.png)







简单总结：

我理解的是互斥是我们实现的终极目的，而锁是一种比较常用的手段。
在单核处理器中。无论是应用程序还是操作系统内核。以关中断为基础，实现自旋锁、互斥锁等锁，即可实现互斥；如果这种单核处理器还支持原子操作，那就可以用原子操作为基础，实现自旋锁、互斥锁等锁，由此来实现互斥。

> 这种场景对于嵌入式操作系统来说，应该提出不自旋会更加自然点，比如在单核上的 `FreeRTOS`，遇到数据竞争，某个线程遇到锁，第一反应应该是让这个线程睡眠？这样相对不影响性能点？

在多核处理器中。对于应用程序，仅仅靠原子指令即可实现互斥，因为不允许关中断。但如果是操作系统内核，那有原子指令还不够，因为中断也能影响到程序的状态迁移，因此还需要关中断。



这个时候感觉到会不会内容稍微多了点，可以将 OS 课分成 OS 内核和 OS 应用两门课？



## 调试理论与实践



## 并发控制：同步（1）



## 并发控制：同步（2）



## 真实世界的并发编程



## 并发bugs



## 应对并发bugs







