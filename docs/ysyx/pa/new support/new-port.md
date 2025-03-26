## Introduction

由于之前一直 nommu-Linux 只是做了个大概，这里重新再开，补充一些之前的日志。

然后进一步做下去。





## UART 

这个一直比较困难的问题：怎么选，是要写 UART 的驱动来适配自己模拟的硬件，还是模拟一个 Linux 内部支持的UART？

还是模拟一个比较好的硬件？我觉得两者不冲突？不过，选后者吧。

根据你的代码和现象，问题主要出在**输入处理机制**和**状态寄存器更新逻辑**。以下是关键问题分析及修复方案：

---

### **问题1：FIFO输入路径未被正确触发**
你在代码中使用`/tmp/nemu-serial`作为FIFO输入管道，但**没有外部程序向该管道写入数据**，导致输入队列始终为空。而旧代码直接读取`stdin`，因此输入有效。

#### **修复方法**：
**方案1**：改用标准输入直接填充FIFO队列（推荐）
```c
#ifdef CONFIG_SERIAL_INPUT_FIFO
#include <termios.h>
static struct termios orig_term;

// 设置非阻塞输入和禁用回显
static void disable_terminal_echo() {
    struct termios new_term;
    tcgetattr(STDIN_FILENO, &orig_term);
    new_term = orig_term;
    new_term.c_lflag &= ~(ICANON | ECHO);
    new_term.c_cc[VMIN] = 0; // 非阻塞读取
    new_term.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &new_term);
    fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);
}

// 填充队列的逻辑修改为直接读取stdin
static inline uint8_t serial_rx_ready_flag() {
    char buf[256];
    ssize_t n = read(STDIN_FILENO, buf, sizeof(buf));
    if (n > 0) {
        for (int i = 0; i < n; i++) {
            serial_enqueue(buf[i]);
        }
    }
    return (f == r ? 0 : LSR_RX_READY);
}

// 初始化时设置终端
static void init_fifo() {
    disable_terminal_echo();
    atexit(restore_terminal); // 退出时恢复
}
#else
...
#endif
```

**方案2**：手动通过其他终端写入FIFO文件（仅调试用） 
在另一个终端运行：
```bash
tail -f /tmp/nemu-serial
```
然后在该终端输入内容（回车后生效）。

---

### **问题2：LSR状态寄存器未正确更新**
旧代码中`IsKBHit()`直接检测输入缓冲区，而FIFO版本仅在`serial_rx_ready_flag()`中被动读取。需要确保**每次读取LSR时更新RX状态**。

#### **修复方法**：
修改`serial_io_handler`中LSR的处理逻辑：
```c
case LSR_OFFSET:
  if (!is_write) {
    // 强制更新RX状态
    serial_rx_ready_flag(); 
    uint8_t lsr = LSR_TX_READY | LSR_FIFO_EMPTY;
    if (f != r) lsr |= LSR_RX_READY;
    serial_base[5] = lsr;
  }
  break;
```

---

### **问题3：输出未及时刷新**
旧代码使用`fflush(stderr)`确保字符立即输出，而FIFO版本缺少此操作。

#### **修复方法**：
在写操作后强制刷新：
```c
case CH_OFFSET:
  if (is_write) {
    putc(serial_base[0], stderr);
    fflush(stderr); // 确保立即输出
  } else {
    ...
  }
  break;
```

---

### **完整修复代码**
整合上述修复后的关键代码：
```c
#ifdef CONFIG_SERIAL_INPUT_FIFO
#include <termios.h>
static struct termios orig_term;

static void restore_terminal() {
    tcsetattr(STDIN_FILENO, TCSANOW, &orig_term);
}

static void disable_terminal_echo() {
    struct termios new_term;
    tcgetattr(STDIN_FILENO, &orig_term);
    new_term = orig_term;
    new_term.c_lflag &= ~(ICANON | ECHO);
    new_term.c_cc[VMIN] = 0;
    new_term.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &new_term);
    fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);
}

static inline uint8_t serial_rx_ready_flag() {
    char buf[256];
    ssize_t n = read(STDIN_FILENO, buf, sizeof(buf));
    if (n > 0) {
        for (int i = 0; i < n; i++) {
            int next = (r + 1) % QUEUE_SIZE;
            if (next != f) {
                queue[r] = buf[i];
                r = next;
            }
        }
    }
    return (f != r) ? LSR_RX_READY : 0;
}

static void init_fifo() {
    disable_terminal_echo();
    atexit(restore_terminal);
}
#endif

static void serial_io_handler(uint32_t offset, int len, bool is_write) {
  assert(len == 1);
  switch (offset) {
    case CH_OFFSET:
      if (is_write) {
          putc(serial_base[0], stderr);
          fflush(stderr); // 确保输出立即刷新
      } else {
          serial_base[0] = serial_dequeue();
      }
      break;
    case LSR_OFFSET:
      if (!is_write) {
          serial_rx_ready_flag(); // 强制更新输入状态
          uint8_t lsr = LSR_TX_READY | LSR_FIFO_EMPTY;
          if (f != r) lsr |= LSR_RX_READY;
          serial_base[5] = lsr;
      }
      break;
  }
}
```

---

### **验证步骤**
1. **编译运行**：应用上述修改后重新编译模拟器。
2. **输入测试**：
   - 启动模拟器和Linux内核。
   - 在控制台输入字符（如`ls`），观察是否正常回显并执行。
3. **输出连贯性**：检查内核启动日志是否连续无重复。

---

### **为何旧代码有效？**
旧代码通过`ReadKBByte`直接读取`stdin`，且`IsKBHit()`实时检测输入状态，能更快响应。而FIFO版本依赖外部写入管道，未正确绑定到实际输入源，导致输入路径断裂。通过将FIFO输入源改为`stdin`并正确设置终端属性，可修复此问题。







## error

```bash
configure: error: 
*** LIBRARY_PATH shouldn't contain the current directory when
*** building gcc. Please change the environment variable
*** and run configure again.

```

也不知道为什么会影响，这个 `LIBRARY_PATH` 不是和**库文件**相关的吗？为什么报错说包含了当前目录？

直接想法就是避开？

```bash
# 临时取消 LIBRARY_PATH
unset LIBRARY_PATH

# 然后运行 configure 和编译
./configure
make
```



