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



那怎么做？之前还没实现原子性的时候，单核怎么做的互斥：关中断，加到这里来。

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

> 无论实现什么，先认为是对的，先写一个测试用例？
>
> 实现一个自旋锁，相比实现一个自旋锁的test driver 不那么重要。？？





### 7.2 操作系统内核中的 (半) 无锁互斥：Read-Copy-Update 🌶️

**在真正的操作系统中实现互斥，其实没有那么简单。**

> 要真正在操作系统内核中用起来，还要考虑很多。
>
> Scalability(伸缩性、延展性...): 性能的新维度
>
> - 严谨的统计很难
>     - CPU 动态功耗
>     - 系统中的其他进程
>     - 超线程
>     - NUMA
>     - ……
>
> [Benchmarking crimes](https://gernot-heiser.org/benchmarking-crimes.html) by Gernot Heiser

假如采用上面的那种方案实现互斥：自旋 + 关中断。

首先，自旋锁的缺点，scalability 非常差，每次需要并发控制的时候，内核就卡在那里不动，如果时间很长，极大地浪费了硬件资源。

再者，关中断同样也不能关太长，关 1 秒的中断，就忽略了很多的时钟中断（就假如10ms来一个，100个），在这些时钟中断，操作系统内核会切换到别的线程，那这样很多线程/任务耗费的时间很长，极大影响性能。

综上，在内核中，上面这种方案尤其自旋锁，只能用在很短的临界区（比如并发的数据结构，往一个链表里添加一个元素、按键按下键码放队列），临界几乎不拥堵，要迅速结束。

![image-20250109213447063](pic/image-20250109213447063.png)

> - Kernel 里有 ~180K 个并发控制函数调用！
>
>     自旋锁当然不 scale
>
>     [An Analysis of Linux Scalability to Many Cores | USENIX](https://www.usenix.org/conference/osdi10/analysis-linux-scalability-many-cores)

怎么办？

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

现在考虑在多核的应用程序中，自旋带来的性能问题

- 性能问题 (1)

    除了进入临界区的线程，其他处理器上的线程都在**空转**

    - 争抢锁的处理器越多，利用率越低
    - 如果临界区较长，不如把处理器让给其他线程

- 性能问题 (2)

    应用程序不能关中断……

    - 持有自旋锁的线程被切换
    - 导致 100% 的资源浪费
    - (如果应用程序能 “告诉” 操作系统就好了)

想想，如果在64核的64个线程对一个资源进行抢占，有一个抢到了，那剩下的 63 个怎么做？空转？一直浪费啊！

没法进入临界区进行计算，那最自然的想法是什么？既然一直在这等着不行，那就不等了？去做有意义的计算？

回想计算机状态机模型，如果状态一直卡在这里，怎么办？还是应用程序？只能 `syscall`。（也就是互斥锁）

把这种锁放到 kernel 实现就好啦，因为 kernel 有能力做上下文切换呀，能切换别的线程。

![image-20250109220653328](pic/image-20250109220653328.png)

> 这个 OJ 例子还是挺形象的哈哈，又比如等成绩的时候，别等了，本来就啥也干不了，去做别的。

> 想到之前学习 `FreeRTOS` 的互斥锁了，既然等不到，那就用 `mutex_acquire` 放弃这个任务，去做别的线程的任务吧。有点类似。

模型：

<img src="pic/image-20250109221906985.png" alt="image-20250109221906985" style="zoom: 67%;" />

我觉得这个图已经形象地描述了。

所以一套配套操作，和自旋锁的都挺类似

```c
mutex_lock()	// acquire
mutex_unlock()	// release
```







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

> 对于嵌入式操作系统来说，应该提出不自旋会更加自然点，比如在单核上的 `FreeRTOS`，遇到数据竞争，某个线程遇到锁，第一反应应该是让这个线程睡眠？这样相对不影响性能？也就是上面那个应用程序的互斥锁。

在多核处理器中。对于应用程序，仅仅靠原子指令即可实现互斥，因为不允许关中断。但如果是操作系统内核，那有原子指令还不够，因为中断也能影响到程序的状态迁移，（回想上面的例子，）因此还需要关中断。



>  这个时候感觉会不会内容稍微多了点？可以将 OS 课分成 OS 内核和 OS 应用两门课？



## 调试理论与实践

> - 并发编程：不能相信自己
>
>     -  并发 bug 的触发需要：
>         - 编译器 + 编译选项 + 特别的机器 + 特别的运气
>     -  内存模型：[专家也做不对](https://github.com/seL4/seL4/pull/199)
>     -  测试全对
>         - Online Judge 被拒绝 
>
> - 初学者：如果可以，只用 “绝对正确” 的实现
>
>     自带一切 barrier 的函数
>
>     - `atomic_xchg`
>     - `pthread_mutex_lock`
>
> 正好的例子，对我们初学者来说，就用业界成熟做好的库。



### 听故事

硬件bug [Original Pentium FDIV flaw e-mail](https://faculty.lynchburg.edu/~nicely/pentbug/bugmail1.html)

软件bug。

> “...attempted to convert large, unexpected 64-bit floating point numbers representing horizontal velocity into 16-bit integers. This resulted in an overflow error, causing the onboard computer to crash.”





### 调试理论

>  听老师好好讲就行这节课。下面都是ppt的内容。





程序/软件是人类需求在信息世界的投影。

- “软件” 的两层含义
    - 人类需求在信息世界的投影
        - 理解错需求 → bug
    - 计算过程的精确 (数学) 描述
        - 实现错误 → bug

- 调试为什么困难？
    - Bug 的触发经历了漫长的过程
    - 可观测的现象未必能直接对应到 root cause 上





==需求 → 设计 → 代码 (**Fault/bug**) → 执行 (**Error**) → 失败 (**Failure**)==

- 我们只能观测到 failure (可观测的结果错)，但是我们犯错的是 fault
- 我们可以检查状态的正确性 (但非常费时)
- 无法预知 bug 在哪里 (每一行 “看起来” 都挺对的)
- 人总是 “默认” (不默认，浪费的时间就太多了)



> **调试理论：如果我们能判定任意程序状态的正确性，那么给定一个 failure，我们可以通过二分查找定位到第一个 error 的状态，此时的代码就是 fault (bug)。**

其实从很久之前就学会用这种思想了。在程序出错之前加一条 log。不断二分，总能找到bug。 



进一步推论

- 为什么我们喜欢 “单步调试”？
    - 从一个假定正确的状态出发
    - 每个语句的行为有限，容易判定是否是 error。我们对每一条语句执行的后果/状态迁移应该都是明白的。
    - single step(step in)、step over(step out)
- 为什么调试理论看起来很没用？
    - “判定状态正确” 非常困难
    - (是否在调试 DP 题/图论算法时陷入时间黑洞？)

>  **观察状态机执行的两个基本工具**
>
>  - `printf` → 自定义 log 的 trace
>     
>     - 灵活可控、能快速定位问题大概位置、适用于大型软件
>     - 无法精确定位、大量的 logs 管理起来比较麻烦
>     
>     让 LLM 帮我们 `printf` 调试
>     
>  - `gdb` → 指令/语句级 trace
>     
>     - 精确、指令级 定位、任意**查看程序内部状态**
>     - 耗费大量时间



- **总结**

    遇到 “任何问题” 时候，先 self-check（遇到问题心里默念/问自己）：

    1. 是怎样的程序 (状态机) 在运行？

        > 能不能将整个状态机打出来看？就像 `make -nB` 那样

    2. 我们遇到了怎样的 failure？

    3. 我们能从状态机的运行中从易到难得到什么信息？（`printf`、`gdb`....）

    4. 如何二分检查这些信息和 error 之间的关联？





### 调试一切

#### example0

**万能方法：假设你遇到的问题是别人也遇到的：StackOverflow、GPT、Google...**

```bash
bash: curl: command not found 
```

```bash
fatal error: 'sys/cdefs.h': No such file or directory #include <sys/cdefs.h> 
```

````bash
/usr/bin/ld: cannot find -lgcc: No such file or directory 
````

```bash
make[2]: *** run: No such file or directory.  Stop. Makefile:31: recipe for target 'run' failed 
```

- 但如果这是一个全新的问题？或者说第一个解决上述问题并分享到网上的人是怎么做的？别人是怎么想的？

    一切都是状态机，将状态机的某一侧面打开，看 `error`。

    如上面：大部分 Error 和 Failure 都比较接近

    - 出错时，使用 `perror` 打印日志，这个 `error message` 已经缩短了 `failure` 和 `error` 的距离，去进一步解决。

    再进一步，还是找不到原因？

    - **出错原因报告不准确**
    - 程序执行的过程看不到
        - 那我们想办法 “看到” 状态机的执行过程就好了！（将状态机拆开）

    > - 理解状态机执行：不是 “调试”，也是 “调试” 
    >     - `ssh`：使用 `-v` 选项检查日志   `verbose`
    >     - `gcc`：使用 `-v` 选项打印各种过程
    >     - `make`：使用 `-nB` 选项查看完整命令历史
    >
    > - 调试：不仅是 “调试器”
    >     - Profiler: `perf` - “采样” 状态机
    >     - Trace: `strace` - 追踪系统调用



#### example1：`sys/cdefs.h: No such file or directory`

- (这看起来是用 `perror()` 打印出来的！)
- 问题分析
    - `#include` = 复制粘贴，自然会经过路径解析
    - 明明 `/usr/include/x86_64-linux-gnu/sys/cdefs.h` 是存在的 (`man 1 locate`) 
- 两种方法
    - 日志 --verbose
    - strace，直接看访问过的文件！

简单尝试下老师课上的操作：万能头文件怎么工作的：

```bash
strace -f g++ a.cc 2>&1 | vim -

vim:
:%!grep \.h
:%!grep -v ENOENT
:%!grep open
```

牛啊，又一次感受到UNIX工具的厉害

> LLM
>
> - **`strace` 命令**：
>     - `strace` 是一个强大的调试工具，可以跟踪进程的系统调用和信号。它可以帮助你理解程序在运行时与操作系统交互的细节。
>     - `-f` 选项用于跟踪所有被 `g++` 创建的子进程的系统调用。这对于编译过程特别有用，因为 `g++` 会创建多个子进程来处理不同的编译步骤。
>
> - `2>&1`
>
>     将标准错误重定向到标准输出，确保所有输出都通过管道传递。
>
> - `| vim -`
>
>     - `|`：管道符号，将前一个命令的输出作为下一个命令的输入。
>     - `vim -`：在 Vim 中打开标准输入的内容。`-` 表示从标准输入读取数据。
>
> - `:%!grep`
>
>     - `:%!grep` 是一个 Vim 命令，用于对当前编辑的文件的所有行（`%` 表示当前文件的所有行）应用 `grep` 命令，并将结果替换当前文件的内容。
>     - 这个命令非常有用，可以快速过滤文件内容，只保留匹配特定模式的行。
>     - `:%` 是一个 Vim 范围指定符，表示当前文件的所有行。
>     - `:%!command` 表示对当前文件的所有行应用 `command`，并将结果替换当前文件的内容。
>     - `:%grep command` 表示在当前文件的所有行中查找匹配 `command` 的行，并将结果保存在临时文件中。
>
>     > - **`!`**：在 Vim 命令中，`!` 用于表示“过滤”或“替换”操作。具体来说，`:%!command` 表示对当前文件的所有行应用 `command`，并将 `command` 的输出结果替换当前文件的内容。
>     > - **没有 `!`**：如果没有 `!`，则表示不进行替换操作，而是将结果保存在快速修复列表中，不修改当前文件的内容。

- 总结
    1. **确认文件存在**：使用 `locate` 或 `find` 确认文件确实存在。
    2. **检查编译器搜索路径**：使用 `gcc -v` 或 `clang -v` 查看编译器的搜索路径。
    3. **使用 `strace`**：跟踪编译器执行时访问的文件，确认是否尝试访问了正确的路径。
    4. **显式指定路径**：如果需要，使用 `-I` 选项显式指定搜索路径。





#### example2：real bug

- 装了 100 台一模一样的机器，但有一台出问题了
    - 名字叫 “pm” 的 Kernel thread 占用 100% CPU
    - LLM 有非常好的解题直觉

> 还是记住这句话：everything is state machine。或者用更好记的一句话，冤有头债有主，遇到 bug肯定有债主，肯定是哪里导致 CPU 出问题的。
>
> 用 `sudo perf top` 
>
> 通过 `perf` 工具采样状态机，每一个采样点，看到底是哪一个函数占用时间，在每一个采样点进行 `backtrace` 打印当前线程调用堆栈。->  发现 `xhci` ：USB subsystem -> 找到了被插烂了的 USB 接口，短路了，导致电源管理出了问题。。 

怎么做到的？

everything is state machine。

会使用相关的工具



#### example3

![image-20250110185657629](pic/image-20250110185657629.png)

通过报错信息知道，这是代码打印出来的报错信息，那能不能找到这条报错信息在哪里？因为这是一个 Ubuntu 的安装镜像，所以能不能解开，然后直接搜索或者 `grep`？最后找到了一处地方（shell脚本），通读/调试上下文代码，知道这部分代码是用来扫描系统所有的磁盘，找到一个安装磁盘就安装。肯定有原因为什么没找到磁盘。怎么解决？进一步看手册，强行指定一个设备安装/别的方法





#### summary

上面这些例子先抛开各种各样的前置基础知识不谈，我是一个初学者，我遇到的问题别人肯定也遇到过。但是我们需要一个比较好的或者比较 principal approach（everything is state machine），出错了一定是自己的问题，我们能解决它，它一定是有原因的，一步步地去解决问题，扩充自己的基础知识。

> 实际上我觉得整个调试理论不单单能用在软件，生活中的给方面应该都能用？题外话。

再回到调试程序。我们依旧需要 [RTFM: Top (Debugging with GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) 

> 又一次提醒自己该读读手册了，总能发现一些很好玩的东西。

- 否则我们甚至不知道 `gdb` 有多强大

Cheat Sheet 里没有的功能

- Text UI (我已经默认启动)
- Stack, optimized code, macros, ...
- Reverse execution
- Record and replay
- Scheduler

> 又一个例子：状态机回溯？逆着状态机的执行流。

只要你想这个东西，那这个东西为什么没有，为什么不可以有？那应该有才对？

> ![image-20250110191752496](pic/image-20250110191752496.png)
>
> 当我第一次看到这段话的时候，我其实并没有意识他究竟想告诉我什么，简单地认识了一个结论：AI Copilot 能够帮我把事情做得更好。
>
> 自从高中以来都是习惯接受别人传授的知识，学习技术总是会去看别人的总结/教程，总是想着别人嚼烂了揉碎了告诉我，从来没想过为什么我不能去阅读第一手的资料。（当然，我觉得初学者都是从这个阶段过来的，那之后呢？没有这种能力不一直要等着别人？）
>
> 在做 PA 的时候已经或多或少告诉自己应该接受一手的知识，应该搜集各种资料独立完成，但在昨晚一部分之后，不知是以前的习惯使然还是自己的惰性太强，导致又有点变回之前的状况，总是被迫用肌肉记忆完成各种任务。
>
> 这里老师给了一个提醒，AI Copilot 或许能够充当这么一个观察者，或者说监督者的角色。copilot 或许能够记录我们刚才做过的事情，他能帮我们总结或者给出一些建议来提醒我们是不是能做得更好。或许未来总会有这个发明的出现？或许这就是一个项目？或许可以尝试下，新的发明往往都是由这样的想法铸造而成。
>
> 另外对于自己来说，趁现在还年轻，可以顶着肌肉记忆或者趁着肌肉记忆还没实现的时候，去学习新的内容。
>
> > 这里想起来之前自己的一些看法：不喜欢折腾和学习新的技术，现在看来其实是不矛盾的，学习新的技术可能解决的是同样的问题，但某一天这就能用在别的地方，最终怎么解决/分析问题，是凭着你那个时候的具体情况具体分析的。所以，去学吧！





### 调试理论的应用

**需求 → 设计 → 代码 → Fault → Error → Failure**

从上面这对于我们设计给出三个相对重要的建议：

1. **==需求 → 设计 → 代码 → Fault==** → Error → Failure

    - **写好代码**：不要在写代码的时候忘记需求和设计

        这里我的体会是：多花一些时间在自己的设计和需求分析上，想想自己以前写代码都是吭哧吭哧无脑上头写，遇到bug了，一直调，解决不了就问 AI，查资料，凭着自己的直觉一往无前，但自己的直觉又往往没有老师那么好。

        其实我可以先在纸上或者 markdown 简单写写整个的流程，自己心里应该有个底的，或许代码写的少了，项目做的少。

    - 不言自明 (Self-explanatory)

        - 能通过字面知道需求 (流程)

    - 不言自证 (Self-evident)

        - 能通过字面确认代码和需求一致

    **代码首先是给人看到，其次才是机器执行的**

    > **一个评判标准**
    >
    > - AI 是否能正确理解/维护你的代码: [toybox](http://git.nju.edu.cn/jyy/toybox)
    >
    > > Programs are meant to be read by humans and only incidentally for computers to execute. (Donald E. Knuth)

2. 需求 → 设计 → 代码 → **==Fault → Error==** → Failure

    - **做好测试**：未测代码永远是错的
        - 残酷的现实：相信自己写不对代码
        - LLM 一样经常犯 “傻” 错

    > Small Scope Hypothesis
    >
    > If a system does not have a counterexample (i.e., an error or a bug) for a certain property within a small scope (a limited size or configuration), then it is unlikely to have a counterexample in a larger scope. (Daniel Jackson)
    >
    > **==TODO==**

    实际上我对这部分的内容，实际上并不是特别地了解，大家一直在说的测试驱动开发（TDD）我也不懂，自己的经历也就只是在做 PA 的时候，自己实现一个函数功能，然后用这个函数，看看有没达成想要的效果？（比如 `strcpy`、`strcmp`等）不过很多时候都是借助 GPT 来帮助我写这个东西。所以这里留坑，准备去看看相关的书籍。 **==TODO==**

    

3. 需求 → 设计 → 代码 → Fault → **==Error → Failure==**

    - 多写断言

        ：把代码中的 “隐藏性质” 写出来

        - Error 暴露的越晚，调试越困难
        - 追溯导致 assert failure 的变量值 (slice) 通常可以快速定位到 bug

    > “There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies” (Tony Hoare)

    其实说来惭愧，做 PA 的时候一直都知道要多写断言，但是只有在想起来的时候才会做，并没有把这个当作一个习惯，之后养成习惯吧。

    ![image-20250111210424564](pic/image-20250111210424564.png)

    > 以往都是先学了某个东西的性质，然后充分应用他的性质来实各种各样的功能，但是现在，我实现得不正确，正确的性质自然也就不满足，自然也就需要上面这些看起来傻里傻气的断言来帮助我找出 bugs。

    有些 “明显” 的断言，写起来会彻底破坏代码的可读性

    ```C
    assert(first(obj) <= ptr && ptr < last(obj)); *ptr = 1; // Assumes ptr is valid. 
    ```

    - 但如果有这样的断言，你就不用担心数组越界了！

        Bad practice: `int elements[MaxN + 100];`

    - 一个神奇的编译选项

        ```C
        -fsanitize=address
        ```

        Address Sanitizer; asan “动态程序分析”

    这种事情编译器应该由编译器做，不然每次都加，真得很麻烦。





## 并发控制：同步（1）

同步是什么？这个东西是干啥的？

回想：并发控制的要求？互斥实现的是什么？

互斥保证了我们的原子性，但是想要调控两份代码执行的顺序关系还是做不到的。



**Synchronization：控制并发：使得 “两个或两个以上随时间变化的量在变化过程中==保持一定的相对关系==”**

还是记住方法：

- 线程 = 我们自己
- 共享内存 = 物理空间



### 线程同步

#### example1：演奏音乐

- 演奏音乐中的同步
    - 每个乐手都是一个 “线程”
    - 节拍 *i*  到达 → 演奏 n~i~

```C
void T_player() {
    while (!end) {
        wait_next_beat(); // 同步，等待指挥发出节拍指令
        play_next_note(); // 演奏对应节拍
    }
}
```



#### example2：约会

两人约定几点几分同时在 xxx 地点见面。

如果某人先到了，那他就得一直等另一个人（当然也可以去玩别的东西，但是到约定时间，必须出现在那里）。





#### example3：更进一步

**在某个瞬间达到 “互相已知” 的状态**

- NPY: 等我洗个头就出门
- NPY: 等我打完这局游戏就来
- 舍友：等我修好这个 bug 就吃饭
- 导师：等我出差回来就讨论这个课题
- join(): 等所有线程结束就继续

- “先到先等”，在条件达成的瞬间再次恢复并行

    同时开始出去玩/吃饭/讨论



#### 状态机视角

挺清晰的图，两个线程都在初始的某个状态上，哪怕之后不断状态迁移，做了很多别的事情，

但并发控制（同步）就要求我们在之后又回到统一的状态上（再次恢复并行），再回看之前的例子应该也挺好理解的。

![image-20250112110354311](pic/image-20250112110354311.png)

在某一个时刻：

所有的 players 都完成了第 n 拍（处于相同的状态）

然后指挥下达命令：打 n+1 拍

（可能有人（线程）会走神，会抢拍（经历复杂的调度，多核都做各自的事情，但最终回到同一状态））

所有人第 n+1 拍完成（处于相同的状态，只是拍子数 + 1）

![image-20250112111059315](pic/image-20250112111059315.png)

```c
void T_player() {
	while (!end) {
		wait_next_beat();
		play_next_note();
	}
}
void T_conductor() {
	while (!end) {
		wait_next_beat();
		release(); 
	}
} 
// release() 之后，player 都会演奏下一拍
// 伪代码
```

有了具体例子辅助理解，接着就到了怎么实现同步。还是以怎么实现演奏音乐为例：怎么等待下一个拍？

其实刚开始我觉得自旋应该就能解决问题的，就比如加个 if 判断看是否收到了指挥的命令，没收到就一直空转自旋，但这样会不会太慢？

> 其实还真是：我想的 if 判断就是同步条件，也就是同步的关键，但是为什么不用 while？

- 线程有先后，先来先等待

```c
void wait_next_beat() {
retry:
	if (!next_beat_has_come) {
		goto retry;
	}
}
```





### 生产者-消费者问题与条件变量(⭐)

> ”99% 的实际并发问题都可以用生产者-消费者模型来解决“，eg. 将算法并行化
>
> ”条件变量能解决 100% 的并发问题“



- Producer 和 Consumer 共享一个缓冲区
    - Producer (生产数据)：如果**缓冲区**有空位，放入；否则等待
    - Consumer (消费数据)：如果**缓冲区**有数据，取走；否则等待

```c
void produce(Object obj); 
Object consume();
```

**==同步，关键在于实现同步的条件。等到某一个条件成立时才能做某事==**



进一步简化：

```c
void produce() { printf("("); } 
void consume() { printf(")"); } 
```

- 生产 = 打印左括号 (push into buffer)    放入缓冲区

- 消费 = 打印右括号 (pop from buffer)    从缓冲区中取出

- 在 `printf` 前后增加代码，使得打印的括号序列满足

    **缓冲区未满：可以打印左括号**

    **缓冲区有货：可以打印右括号**

    - 一定是某个合法括号序列的前缀
    - 括号嵌套的深度不超过 n
        - n=3：`((())())(((` 合法
        - n=3：`(((())))`, `(()))` 不合法

```C
void produce() {
    wait_until(括号深度 < n) {
        printf("(");
    }
}

void consume() {
    wait_until(括号深度 > 0) {
        printf(")");
    }
}
```



#### version1

```C
int n, depth = 0;
void T_produce() {
    while (1) {
retry:
        mutex_lock(&lk);
        int ready = (depth < n);
        mutex_unlock(&lk);
        if (!ready) goto retry;

        // context switch
        // assert(depth < n);

        mutex_lock(&lk);
        printf("(");
        depth++;
        mutex_unlock(&lk);
    }
}

void T_consume() {
    while (1) {
retry:
        mutex_lock(&lk);
        int ready = (depth > 0);
        mutex_unlock(&lk);
        if (!ready) goto retry;

        // assert(depth > 0);

        mutex_lock(&lk);
        printf(")");
        depth--;
        mutex_unlock(&lk);
    }
}
```

why wrong？

挺好理解的，还是之前的那样，第 8 行的 ready 是一个共享资源来的，没对它加锁，自然就有可能读到的是旧的 ready（刚好第 8 行后上下文切换、来中断，因为还没有更新缓冲区，导致别的线程的第 13 到 第 16 行的代码就会将缓冲区填满，这个时候 11 行的 assert 就有问题）。

只要存在多个消费者，那就会在并发的时候影响到 ready 的值。

也很容易解决，其实就是 5 到 8 行对 ready 锁的时间不够长，将整个 produce 的操作都变成原子的，都锁住。



#### version2

```C
#define CAN_PRODUCE (depth < n)
#define CAN_CONSUME (depth > 0)

void T_produce() {
    while (1) {
retry:
        mutex_lock(&lk);
        if (!CAN_PRODUCE) {
            mutex_unlock(&lk);
            goto retry;
        }

        // The check of sync condition (depth < n) is within
        // the same critical section. As long as we safely
        // protected the shared state, this condition should
        // always hold at this point.
        assert(depth < n);

        printf("(");
        depth++;

        // And at this point, the condition (depth > 0) is
        // satisfied. However, a consumer could proceed with
        // checking depth only if the lock is released.
        mutex_unlock(&lk);
    }
}

void T_consume() {
    while (1) {
retry:
        mutex_lock(&lk);
        if (!CAN_CONSUME) {
            mutex_unlock(&lk);
            goto retry;
        }

        assert(depth > 0);

        printf(")");
        depth--;

        mutex_unlock(&lk);
    }
}

```

由此得出这个万能模型，关键在于怎么换这个同步条件。

进一步，OS 开发者将上面的内容改进变成了用条件变量来实现生产者-消费者模型。







#### conditional variable

对于上面的实现，最大的问题就是线程浪费 `cpu`，依然自旋空转。

> 如果 生产者已经放慢了资源到缓冲区，但是消费者还没有消费完，那生产者就一直自旋在那了。

进一步上面观察上面特征：同步条件 + 自旋。 

回想前几课的内容，既然空转浪费资源，那就你睡去吧，让别人（线程）来做。

另外，同步条件 -> 变量



具体来说，在同步条件不成立的时候（依然解锁锁），不使用 retry，而是等到条件满足某人将我唤醒，醒来之后再上锁。

```C
mutex_lock(&lk);
while (!CAN_PRODUCE) {
    mutex_unlock(&lk);
    wait_for_someone_wake_me_up();
    mutex_lock(&lk);	
}
```

- 把条件用一个变量来替代：`CAN_PRODUCE`  -> `cond_t cv`
- 条件不满足时等待，条件满足时唤醒：`wait_for_someone_wake_me_up` + `mutex_lock`  -> `cond_wait`

```C
mutex_t lk = MUTEX_INIT();
cond_t cv = COND_INIT();

#define CAN_PRODUCE (depth < n)
#define CAN_CONSUME (depth > 0)
void T_produce() {
    while (1) {
        mutex_lock(&lk);
        while (!CAN_PRODUCE) {
            cond_wait(&cv, &lk);
            // We are here if the thread is being waked up, with
            // the mutex being acquired. Then we check once again,
            // and move out of the loop if CAN_PRODUCE holds.
        }

        // We still hold the mutex--and we check again.
        assert(CAN_PRODUCE);

        printf("(");
        depth++;

        cond_broadcast(&cv);
        mutex_unlock(&lk);
    }
}
void T_consume() {
    while (1) {
        mutex_lock(&lk);
        while (!CAN_CONSUME) {
            cond_wait(&cv, &lk);
        }

        printf(")");
        depth--;

        cond_broadcast(&cv);
        mutex_unlock(&lk);
    }
}

```

 ```C
 cond_wait(&cv, &lk)； // 对于这个同步条件cv不成立，进入睡眠模式，进入等待，同时释放锁lk，被唤醒后又重新上锁
 
 //有人在等待我的条件，我将他唤醒
 cond_signal(&cv);  // Wake up a (random) thread
 cond_broadcast(&cv);  // Wake up all threads
 ```



- **条件变量的正确打开方式**

    **使用 while 循环和 broadcast**

    - **总是在唤醒后再次检查同步条件**
    - **总是唤醒所有潜在可能被唤醒的人**

    ```C
    mutex_lock(&mutex);
    while (!COND) {
      wait(&cv, &mutex);
    }
    assert(cond);
    
    ...
    
    mutex_unlock(&mutex);
    
    ```

    只要有我对共享资源做了一些改动，我都叫醒这个世界的所有人（线程）去检查一下自己的同步条件（广播），如果条件满足了，那就可以去执行了。

> 这里还有一个版本：使用的是 `if` 和 `cond_signal` 去实现生产者-消费者模型，但是需要两个条件变量，具体为什么，简单就是：每一个线程都有自己同步条件。每一个线程同步条件不一样。（两类不同的线程：生产者、消费者）
>
> 详细内容看教材：[第 30 章 - Condition Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf)

**==可以记住这种代码模板写法，总能解决并发问题==**





### 同步机制的应用

解决同步问题的核心：弄清楚同步条件。



#### 并行计算：实现计算图

如果用多处理器并行编程完成很大的**计算任务**，首先要做的就是将任务分成若干步：计算任务构成有向无环图

> 配合例子和图（算素数表）：
>
> <img src="pic/image-20250114215612517.png" alt="image-20250114215612517" style="zoom: 67%;" />

- (u,v)∈E(*u*,*v*)∈*E* 表示 v*v* 要用到前 u*u* 的值

- **只要调度器 (生产者) 分配任务效率够高，算法就能并行**

    > 这是物理内存分配的想法吗？这个调度器怎么实现？很重要。

```C
void T_worker() {
    while (1) {
        consume().run();
    }
}
void T_scheduler() {
    while (!jobs.empty()) {
        for (auto j : jobs.find_ready()) {
            produce(j);
        }
    }
}
```



- **实现**

    - 生产者-消费者模型

        生产者遍历计算图，消费者实际做计算。（以素数表为例，遍历时间几微秒，计算时间几秒，就很好）

        生产者遍历后，将一个个任务放至缓冲区中。每一个消费者 worker 就去缓冲区中取任务计算。

        **==只要能将任务分解成有向无环图的形式，用一个生产者，多个消费者即可实现多任务并行。==**

        ```c++
        // author: kimi
        
        #include <stdio.h>
        #include <stdlib.h>
        #include <pthread.h>
        #include <queue>
        #include <vector>
        #include <mutex>
        #include <condition_variable>
        
        std::queue<int> jobs;
        std::mutex mtx;
        std::condition_variable cv;
        bool done = false;
        
        void produce(int job) {
            std::lock_guard<std::mutex> lock(mtx);
            jobs.push(job);
            cv.notify_one();
        }
        
        int consume() {
            std::unique_lock<std::mutex> lock(mtx);
            cv.wait(lock, [] { return !jobs.empty() || done; });
            if (jobs.empty()) {
                return -1; // 表示没有更多任务
            }
            int job = jobs.front();
            jobs.pop();
            return job;
        }
        
        void T_worker() {
            while (1) {
                int job = consume();
                if (job == -1) {
                    break;
                }
                // 执行任务
                printf("Processing job: %d\n", job);
                // 模拟计算时间
                sleep(1);
            }
        }
        
        void T_scheduler() {
            for (int i = 0; i < 10; ++i) {
                produce(i);
            }
            done = true;
            cv.notify_all();
        }
        
        int main() {
            const int num_workers = 4;
            std::vector<pthread_t> workers(num_workers);
        
            for (int i = 0; i < num_workers; ++i) {
                pthread_create(&workers[i], NULL, (void *(*)(void *))T_worker, NULL);
            }
        
            T_scheduler();
        
            for (int i = 0; i < num_workers; ++i) {
                pthread_join(workers[i], NULL);
            }
        
            return 0;
        }
        ```

        1. **生产者（T_scheduler）**：
            - 生成 10 个任务，并将它们放入任务队列中。
            - 设置 `done` 标志为 `true`，表示没有更多任务。
            - 通知所有等待的消费者线程。
        2. **消费者（T_worker）**：
            - 从任务队列中获取任务。
            - 如果任务队列为空且 `done` 标志为 `true`，则退出循环。
            - 处理任务，模拟计算时间。
        3. 关键点
            - **生产者-消费者模型**：生产者负责生成任务并放入任务队列，消费者从任务队列中获取任务并执行。
            - **条件变量**：用于线程间的同步，确保消费者线程在任务队列为空时等待，生产者线程在生成任务后通知消费者线程。
            - **互斥锁**：保护共享资源（任务队列）的访问，确保线程安全。

    

    > more example：线程池
    >
    > 每一个 worker 就是一个工作的线程，把一个个小的任务放到线程池，然后线程池有个调度器，调度器再将这些任务再分给 worker。

    

    **当然还能用条件变量实现同步**

    - 条件变量

        为每一个计算节点都设置一个条件变量

        ```C++
        // kimi 
        // 主要看逻辑
        
        #include <iostream>
        #include <vector>
        #include <queue>
        #include <mutex>
        #include <condition_variable>
        #include <thread>
        #include <functional>
        #include <unordered_map>
        #include <list>
        
        // 任务节点
        struct Task {
            int id;
            std::function<void()> func;
            std::vector<int> dependencies;
            int ready_count = 0;
        };
        
        // 计算图
        class ComputeGraph {
        public:
            void addTask(int id, std::function<void()> func, const std::vector<int>& dependencies) {
                tasks[id] = {id, func, dependencies, 0};
                for (int dep : dependencies) {
                    task_dependencies[dep].push_back(id);
                }
            }
        
            void run() {
                // 初始化就绪任务队列
                for (auto& [id, task] : tasks) {
                    if (task.dependencies.empty()) {
                        ready_tasks.push(id);
                    }
                }
        
                // 启动调度线程
                scheduler_thread = std::thread(&ComputeGraph::scheduler, this);
        
                // 启动工作线程
                for (int i = 0; i < num_workers; ++i) {
                    workers.push_back(std::thread(&ComputeGraph::worker, this));
                }
        
                // 等待调度线程结束
                scheduler_thread.join();
        
                // 等待工作线程结束
                for (auto& worker : workers) {
                    worker.join();
                }
            }
        
        private:
            std::unordered_map<int, Task> tasks;
            std::unordered_map<int, std::list<int>> task_dependencies;
            std::queue<int> ready_tasks;
            std::mutex mtx;
            std::condition_variable cv;
            bool done = false;
            std::vector<std::thread> workers;
            std::thread scheduler_thread;
            int num_workers = 4;
        
            void scheduler() {
                while (!ready_tasks.empty()) {
                    int task_id = ready_tasks.front();
                    ready_tasks.pop();
        
                    // 通知工作线程
                    cv.notify_one();
                }
        
                // 设置 done 标志，通知所有工作线程
                done = true;
                cv.notify_all();
            }
        
            void worker() {
                while (1) {
                    std::unique_lock<std::mutex> lock(mtx);
                    cv.wait(lock, [this] { return !ready_tasks.empty() || done; });
        
                    if (done && ready_tasks.empty()) {
                        break;
                    }
        
                    int task_id = ready_tasks.front();
                    ready_tasks.pop();
                    lock.unlock();
        
                    // 执行任务
                    tasks[task_id].func();
        
                    // 更新依赖关系
                    for (int dependent_id : task_dependencies[task_id]) {
                        std::lock_guard<std::mutex> lock(mtx);
                        tasks[dependent_id].ready_count++;
                        if (tasks[dependent_id].ready_count == tasks[dependent_id].dependencies.size()) {
                            ready_tasks.push(dependent_id);
                        }
                    }
                }
            }
        };
        
        void task1() {
            std::cout << "Task 1" << std::endl;
        }
        
        void task2() {
            std::cout << "Task 2" << std::endl;
        }
        
        void task3() {
            std::cout << "Task 3" << std::endl;
        }
        
        void task4() {
            std::cout << "Task 4" << std::endl;
        }
        
        int main() {
            ComputeGraph graph;
        
            // 添加任务
            graph.addTask(1, task1, {});
            graph.addTask(2, task2, {1});
            graph.addTask(3, task3, {1});
            graph.addTask(4, task4, {2, 3});
        
            // 运行计算图
            graph.run();
        
            return 0;
        }
        ```

        

    - example





#### 场景：动态规划 

> 还有哪些场景并行加速？
>

![image-20250114164832957](pic/image-20250114164832957.png)

如果一个算法的后一步完全依赖于前一步，那这个算法就不好并行的。所以要将这个有向无环图做得很宽很宽的，要足够宽。

> 这就有个问题，怎么看这个并行之后的性能和没并行的性能差异？通过什么工具？什么指标？



一个面试问题：多处理器很普及的情况下，怎么将一个问题并行加速？

第一反应 应该是 了解计算图是什么，它的结构是什么，它的切分方法。

> 来自 AI：
>
> 1. **计算图的概念**
>    
>    - 计算图是一种用于表示计算过程的有向图。在图中，节点（顶点）通常表示操作（如加法、乘法等）或者变量（输入、中间结果、输出等），边表示数据的流向。例如，在深度学习中，一个简单的神经网络的前向传播过程可以表示为计算图。假设有一个两层的神经网络，输入层有一个节点 \( x \)，隐藏层有一个节点 \( h \)，输出层有一个节点 \( y \)。其中隐藏层节点 \( h \) 的计算是 \( h = W_1x + b_1 \)，输出层节点 \( y \) 的计算是 \( y = W_2h + b_2 \)。这里 \( W_1, W_2, b_1, b_2 \) 是权重和偏置参数。那么计算图中会有节点 \( x, h, y \) 以及对应的权重和偏置节点，边表示数据从输入层流向隐藏层，再从隐藏层流向输出层。
>    - 计算图在数据流编程模型中非常重要。它能够清晰地描述数据是如何在各个操作之间流动的，以及各个操作之间的依赖关系。这种图结构使得并行计算和自动微分等操作变得方便。例如，在自动微分中，通过计算图可以很容易地应用链式法则来计算梯度，因为图的结构已经明确了操作的顺序和依赖关系。
>    
> 2. **切分计算图**
>
>    - 任务划分：根据计算图的结构，将计算任务划分到不同的处理器上。可以采用几种常见的切分方法：
>        - **按节点划分**：将计算图中的节点（操作）分配给不同的处理器。例如，在深度学习的神经网络前向传播计算图中，可以将不同层的操作分配到不同的处理器。如果是一个有 10 层的神经网络，可以将前 5 层的操作分配给处理器 1，后 5 层的操作分配给处理器 2。但是这种方法需要考虑数据传输的开销，因为不同层之间可能需要传输数据。
>        - **按边划分**：如果计算图中的边代表数据传输，可以考虑按照数据传输的路径来划分任务。例如，在一个数据流图中，数据从节点 A 流向节点 B，再流向节点 C。可以将 A 到 B 的数据处理和传输分配给一个处理器，B 到 C 的处理和传输分配给另一个处理器。这种方法适用于数据传输和处理紧密相关的场景。
>        - **区域划分**：对于一些具有空间局部性的计算图，如图像处理中的像素操作计算图，可以按照图像的区域来划分任务。将图像分成多个区域，每个处理器负责一个区域内的像素操作。这种方法可以减少数据传输，因为相邻像素之间的操作往往有数据局部性。
>    - **负载均衡**：在切分计算图时，要尽量保证各个处理器的负载均衡。如果一个处理器分配到的任务量过大，而其他处理器任务量过小，会导致处理器之间等待，降低整体效率。可以通过估算每个操作的计算复杂度来分配任务。例如，在一个计算图中，有些操作是简单的加法，有些操作是复杂的矩阵求逆。可以将计算复杂度高的操作适当分散到不同的处理器上，使每个处理器的计算时间大致相当。
>
> 3. **处理数据传输和同步**
>
>    - 数据传输优化
>
>        ：在多处理器并行计算中，数据传输是一个关键问题。当计算图被切分到不同的处理器后，处理器之间可能需要传输数据。可以采用以下方法优化数据传输：
>
>        - **减少传输量**：只传输必要的数据。例如，在矩阵乘法并行计算中，如果将矩阵 A*A* 的不同行分配给不同的处理器，那么每个处理器只需要传输它所负责行相关的数据，而不是整个矩阵 A*A*。
>        - **使用高效传输协议**：在分布式计算环境中，可以使用 MPI（Message Passing Interface）等高效的通信协议来传输数据。MPI 提供了丰富的通信操作，如点对点通信、集体通信（如广播、归约等），可以针对不同的数据传输需求选择合适的通信操作。
>
>    - **同步机制**：为了保证计算的正确性，需要在处理器之间进行同步。可以使用互斥锁、信号量、屏障（Barrier）等同步原语。例如，在计算图中，如果一个操作依赖于多个其他操作的结果，可以在这些操作执行完毕后，通过屏障同步，确保所有依赖的操作都完成后，再执行当前操作。在多线程环境下，可以使用互斥锁来控制对共享资源（如计算图中的中间结果存储区）的访问，防止数据竞争。
>
> 2. **计算图所属的知识领域**
>    
>    - **数据结构与算法**：计算图本身是一种数据结构，它用图的形式来组织数据和操作。在数据结构中，图是一种基本的数据结构，包括有向图和无向图等类型。计算图是图的一种应用形式。从算法角度来看，对计算图的操作，如遍历（用于前向传播计算结果或者后向传播计算梯度）、拓扑排序（确定操作的执行顺序，特别是在有依赖关系的操作中）等都涉及到算法知识。例如，拓扑排序算法可以用于确定在计算图中各个节点（操作）的执行顺序，确保在执行一个操作之前，其依赖的所有操作都已经完成。
>    - **计算机体系结构和操作系统**：当涉及到多线程计算图时，就像题目中提到的使用互斥锁来实现计算图的计算，这就和操作系统中的线程同步机制相关。互斥锁是操作系统提供的一种同步原语，用于保证在多线程环境下对共享资源的互斥访问。在计算图的多线程实现中，通过在不同的线程中对互斥锁进行 acquire（获取）和 release（释放）操作，来控制计算图中各个节点（操作）的执行顺序，确保数据的一致性和操作的正确性。这体现了操作系统在多线程编程和资源管理方面的知识。
>    - **并行计算和分布式计算**：在大规模的计算任务中，如深度学习训练，计算图可以分布在多个处理器或者多台机器上进行并行计算。这就涉及到并行计算中的任务划分、数据传输、负载均衡等知识。例如，在分布式训练中，计算图的不同部分可能在不同的机器上执行，需要通过网络通信来传输数据，并且要合理地划分计算图的任务到各个机器上，以提高计算效率。
>    
> 2. **利用多处理器架构特性**
>    
>    - **多核处理器优化**：对于多核处理器，可以利用线程库（如 POSIX 线程库 pthreads）来创建多个线程，并将计算图的任务分配给不同的线程。每个线程可以在一个核心上执行，从而实现并行加速。同时，要考虑到缓存一致性问题。在多核处理器中，每个核心有自己的缓存，当多个线程访问共享数据时，可能会导致缓存不一致。可以通过合理的数据分配和访问模式来减少缓存不一致的影响。例如，尽量让线程访问本地缓存中的数据，减少跨核心的缓存访问。
>    - **分布式系统优化**：在分布式系统中，可以利用多台机器的处理器资源。可以使用分布式计算框架（如 Apache Hadoop、Apache Spark 等）来管理计算任务。这些框架提供了任务调度、数据存储和管理等功能。例如，在 Spark 中，可以将计算图的任务定义为 RDD（Resilient Distributed Dataset）操作，Spark 会自动将这些操作分配到不同的节点上执行，并且处理节点之间的数据传输和任务调度。同时，要考虑到网络带宽和延迟对分布式计算的影响，合理地设计数据存储和传输策略。
>    
> 3. **总结**
>    
>    - 计算图是一种强大的工具，用于表示和管理复杂的计算过程。它跨越了数据结构与算法、计算机体系结构和操作系统、并行计算和分布式计算等多个知识领域。通过合理地构建和操作计算图，可以实现高效的计算，特别是在深度学习等需要大量计算的领域。在多线程环境下，利用互斥锁等同步机制来控制计算图的执行，是确保计算正确性的重要手段。

> 来自 AI：
>
> 1. 任务分解
>
>     将大任务分解为多个小任务是并行化的第一步。这些小任务可以是独立的，也可以存在依赖关系。任务分解的目标是确保每个任务的计算量大致相等，以实现负载均衡。
>
>     - 示例：矩阵乘法
>
>         假设你需要计算两个矩阵的乘积 \( C = A \times B \)。可以将矩阵 \( A \) 和 \( B \) 分解为多个子矩阵，每个子矩阵的乘积可以并行计算。
>
>         ```c
>         void matrix_multiply_parallel(float *A, float *B, float *C, int N) {
>             #pragma omp parallel for
>             for (int i = 0; i < N; i++) {
>                 for (int j = 0; j < N; j++) {
>                     C[i * N + j] = 0;
>                     for (int k = 0; k < N; k++) {
>                         C[i * N + j] += A[i * N + k] * B[k * N + j];
>                     }
>                 }
>             }
>         }
>         ```
>
> 2. 使用并行编程模型
>
>     选择合适的并行编程模型可以大大简化并行化的复杂性。常见的并行编程模型包括：
>
>     - **OpenMP**：用于多线程并行编程，支持 C、C++ 和 Fortran。
>
>     - **MPI**：用于分布式内存并行编程，适用于高性能计算集群。
>
>     - **CUDA**：用于 NVIDIA GPU 的并行编程，适用于高性能计算和机器学习。
>
>     - **Intel TBB**：用于多核 CPU 的并行编程，提供高级并行算法和数据结构。
>
>     - 示例：OpenMP
>
>         使用 OpenMP 可以轻松地将循环并行化：
>
>         ```c
>         #include <omp.h>
>         
>         void compute() {
>             #pragma omp parallel for
>             for (int i = 0; i < N; i++) {
>                 // 计算任务
>             }
>         }
>         ```
>
>
> 3. 负载均衡
>
>     确保每个处理器的负载大致相等，以避免某些处理器过载而其他处理器闲置。负载均衡可以通过静态或动态调度实现。
>
>     - **静态调度**：在任务开始前，将任务均匀分配给每个处理器。
>     - **动态调度**：在运行时根据处理器的负载情况动态分配任务。
>
>     - 示例：动态调度
>
>         使用 OpenMP 的动态调度：
>
>         ```c
>         #include <omp.h>
>         
>         void compute() {
>             #pragma omp parallel for schedule(dynamic)
>             for (int i = 0; i < N; i++) {
>                 // 计算任务
>             }
>         }
>         ```
>
>
> 4. 减少通信开销
>
>     在并行计算中，通信开销是一个主要的性能瓶颈。尽量减少处理器之间的通信，或者使用高效的通信算法和库。
>
>     - **局部性优化**：确保每个处理器访问的数据尽可能局部化，减少内存访问延迟。
>     - **批量通信**：将多个小的通信操作合并为一个大的通信操作，减少通信开销。
>
>     - 示例：批量通信
>
>         使用 MPI 进行批量通信：
>
>         ```c
>         #include <mpi.h>
>         
>         void communicate() {
>             MPI_Request requests[10];
>             MPI_Status statuses[10];
>         
>             for (int i = 0; i < 10; i++) {
>                 MPI_Isend(data[i], count, MPI_INT, dest, tag, MPI_COMM_WORLD, &requests[i]);
>             }
>         
>             MPI_Waitall(10, requests, statuses);
>         }
>         ```
>
>
> 5. 使用并行算法
>
>     选择适合并行化的算法可以显著提高性能。例如，分治算法、归并排序、快速排序等都可以并行化。
>
>     - 示例：并行归并排序
>
>         使用 OpenMP 实现并行归并排序：
>
>         ```c
>         #include <omp.h>
>         
>         void merge_sort_parallel(int *array, int left, int right) {
>             if (left < right) {
>                 int mid = (left + right) / 2;
>                 #pragma omp parallel sections
>                 {
>                     #pragma omp section
>                     {
>                         merge_sort_parallel(array, left, mid);
>                     }
>                     #pragma omp section
>                     {
>                         merge_sort_parallel(array, mid + 1, right);
>                     }
>                 }
>                 merge(array, left, mid, right);
>             }
>         }
>         ```
>
>
> 6. 利用硬件特性
>
>     充分利用多处理器硬件的特性，如多核 CPU、GPU、FPGA 等，可以进一步提高并行计算的效率。
>
>     - **多核 CPU**：使用 OpenMP 或 Intel TBB 进行多线程并行编程。
>     - **GPU**：使用 CUDA 或 OpenCL 进行并行计算。
>     - **FPGA**：使用硬件描述语言（HDL）进行定制化并行计算。
>
>     - 示例：CUDA
>
>         使用 CUDA 进行并行计算：
>
>          ```c
>         __global__ void vector_add(int *a, int *b, int *c, int n) {
>             int index = threadIdx.x + blockIdx.x * blockDim.x;
>             if (index < n) {
>                 c[index] = a[index] + b[index];
>             }
>         }
>         int main() {
>             int n = 1024;
>             int *a, *b, *c;
>             int *d_a, *d_b, *d_c;
>             
>             // 分配主机内存
>             a = (int *)malloc(n * sizeof(int));
>             b = (int *)malloc(n * sizeof(int));
>             c = (int *)malloc(n * sizeof(int));
>             
>             // 分配设备内存
>             cudaMalloc((void **)&d_a, n * sizeof(int));
>             cudaMalloc((void **)&d_b, n * sizeof(int));
>             cudaMalloc((void **)&d_c, n * sizeof(int));
>             
>             // 初始化数据
>             for (int i = 0; i < n; i++) {
>                 a[i] = i;
>                 b[i] = i;
>             }
>             
>             // 从主机复制数据到设备
>             cudaMemcpy(d_a, a, n * sizeof(int), cudaMemcpyHostToDevice);
>             cudaMemcpy(d_b, b, n * sizeof(int), cudaMemcpyHostToDevice);
>         
>             // 启动内核
>             int threadsPerBlock = 256;
>             int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;
>             vector_add<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);
>             
>             // 从设备复制数据到主机
>             cudaMemcpy(c, d_c, n * sizeof(int), cudaMemcpyDeviceToHost);
>             
>             // 释放设备内存
>             cudaFree(d_a);
>             cudaFree(d_b);
>             cudaFree(d_c);
>             
>             // 释放主机内存
>             free(a);
>             free(b);
>             free(c);
>             return 0;
>         }
>          ```





#### 习题/面试题

对于这种上面的方法不好解决的方法，去想同步条件是什么。

<img src="pic/image-20250114204356246.png" alt="image-20250114204356246" style="zoom: 67%;" />

> **奇怪的同步问题**：我们可以构造出 “奇怪” 的同步条件，例如有三种线程，分别死循环打印 `<`、`>`、`_`。如何同步这些线程，使得屏幕上看到的总是 `<><_` 和 `><>_` 的组合？而只要我们能列出同步条件，就可以直接使用条件变量解决。

观察，看看各个字符出现的位置，都知道要想着找同步条件是什么：每种字符出现的位置的要求。

什么时候能打印 `<`？在开头/ `_`、`>` 后面。

什么时候能打印 `>`？在开头/ `_`、`<` 后面。

什么时候能打印 `_`？出现在最后一个字符。

老师给出的进一步总结：需要知道一个打印的 history。

由当前的状态（历史）来看未来什么可以做什么不可以做？状态机！





### Summary

再次回顾，什么叫同步？记住那个演奏音乐的例子。简单理解就是大家回到同一起跑线，一起等拍。

每一个人都有自己继续的条件。





## 并发控制：同步（2）

### 信号量

#### 使用互斥锁实现同步



#### **使用互斥锁实现计算图**







### 使用信号量实现同步





### 信号量、条件变量、同步









## 真实世界的并发编程







## 并发bugs



## 应对并发bugs







