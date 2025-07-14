## Books

《软件调试》第二版 张银奎

《Cortex-M3 编程指南》



## Example

[通过qemu+gdb实现跨架构调试 - 刘跑跑 - 博客园 (cnblogs.com)](https://www.cnblogs.com/liuhanxu/p/16245816.html)

- 窗口1：启动 a.out
    通过 qemu-aarch64 运行交叉编译的 a.out, 并指定 gdb 调试端口号为1234，然后等待 gdb 远程连接。

    ```bash
    lhx@ubuntu:~/test/qemu$ qemu-aarch64 -g 1234 ./a.out
    Hello World !
    ```

    > - `-g 1234`：这个选项用于指定 QEMU 模拟器的调试端口。`-g` 后面跟的数字是 TCP 端口号，这里指定为 1234。当使用这个选项时，QEMU 会在启动时监听指定的端口，允许调试器（如 gdb）连接到这个端口进行远程调试。

- 窗口2：gdb 远程调试
    通过 gdb-multiarch 启动 a.out，这里 a.out 用于读取和远程端一致的调试符号信息。连接上远程端口号后，便可以进行设断点、查看寄存器、反汇编等一系列调试操作。

    > 1. `gdb-multiarch -q a.out`：
    >     - `gdb-multiarch` 是一个支持多种架构的 GNU 调试器（GDB）版本，它允许你调试为不同架构编译的程序。
    >     - `-q` 选项使 GDB 在启动时不加载任何初始化脚本文件，这在自动化脚本中很有用，因为它可以减少启动时间。
    > 2. `(gdb) target remote localhost:1234`：
    >     - `target remote` 命令告诉 GDB 连接到一个远程目标进行调试。
    >     - `localhost:1234` 指定了远程目标的地址和端口，这里是本地主机上的 1234 端口。这通常与 QEMU 使用 `-g 1234` 选项启动时指定的调试端口相匹配。

    ```assembly
    lhx@ubuntu:~/test/qemu$ ls
    a.out  hello.c
    @ubuntu:~/test/qemu$ gdb-multiarch -q a.out 
    Reading symbols from a.out...
    (gdb) target remote localhost:1234
    Remote debugging using localhost:1234
    0x0000000000400558 in _start ()
    (gdb) b main
    Breakpoint 1 at 0x4006d4: file hello.c, line 10.
    (gdb) c
    Continuing.
    
    Breakpoint 1, main () at hello.c:10
    10	  hello();
    (gdb) s
    hello () at hello.c:5
    5	  printf("Hello World !\n");
    (gdb) n
    6	}
    (gdb) info registers 
    x0             0xe                 14
    x1             0x1                 1
    x2             0x0                 0
    x3             0x48bf00            4767488
    x4             0xfbad2a84          4222429828
    x5             0x21a               538
    x6             0x10                16
    x7             0x7f7f7f7f7f7f7f7f  9187201950435737471
    x8             0x40                64
    x9             0x3fffffff          1073741823
    x10            0x20000000          536870912
    x11            0x10000             65536
    x12            0x48b000            4763648
    x13            0x410               1040
    x14            0x0                 0
    x15            0x48c738            4769592
    x16            0x40b998            4241816
    x17            0x416fc0            4288448
    x18            0x0                 0
    x19            0x400db8            4197816
    x20            0x400e80            4198016
    x21            0x0                 0
    x22            0x400280            4194944
    x23            0x489030            4755504
    x24            0x18                24
    x25            0x48b000            4763648
    x26            0x48b000            4763648
    x27            0x451000            4526080
    x28            0x0                 0
    x29            0x4000800260        274886296160
    x30            0x4006c0            4196032
    sp             0x4000800260        0x4000800260
    pc             0x4006c0            0x4006c0 <hello+20>
    cpsr           0x60000000          1610612736
    fpsr           0x0                 0
    fpcr           0x0                 0
    
    (gdb) bt
    #0  hello () at hello.c:6
    #1  0x00000000004006d8 in main () at hello.c:10
    (gdb) disassemble hello
    Dump of assembler code for function hello:
       0x00000000004006ac <+0>:	stp	x29, x30, [sp, #-16]!
       0x00000000004006b0 <+4>:	mov	x29, sp
       0x00000000004006b4 <+8>:	adrp	x0, 0x451000 <_nl_locale_subfreeres+552>
       0x00000000004006b8 <+12>:	add	x0, x0, #0x3e8
       0x00000000004006bc <+16>:	bl	0x407350 <puts>
       0x00000000004006c0 <+20>:	nop
       0x00000000004006c4 <+24>:	ldp	x29, x30, [sp], #16
       0x00000000004006c8 <+28>:	ret
    End of assembler dump.
    (gdb) c
    Continuing.
    [Inferior 1 (process 1) exited normally]
    (gdb) 
    ```

    