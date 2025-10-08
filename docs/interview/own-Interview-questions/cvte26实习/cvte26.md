## 笔试

### 算法

- 200以内的素数求和

- 一个投色子游戏，6个人表示6个点，每个人手上10元，投到哪个点，除了这个点的人以外，都要给这个点的人1元，如果下次还是这个人，那就翻倍给1→2→4....如果有人的钱小于等于0，记录为出局，记录第一个出局的。。。





### 选择

- C语言复杂指针

    函数指针、数组指针、混起来考。

    好像收到是一个指向含有10个元素的数组的指针，还有一个函数指针，不记得了。

- 循环链表

    - 知道一个节点，可以向两边遍历？
    - 尾节点的下一个是头节点？
    - 链表遍历的，找节点

- `strlen` 和 `sizeof`

    记得`strlen` 计算字符串的长度，不包括末尾的空字符 `\0`。

    `sizeof` 计算空间大小。

- Linux 文件/目录？

    `chmod`、`chown`？

    什么权限的的 rwx，用户、群组用户、其他？u（user）、g（group）、o（others）

    r：4，w：2，x：1 `bits：0x100、0x010、0x001`

    比如：`drwxrwxr-x`，问问 deepseek

    从左到右：ugo，各占3个bit，第一个d（directory）不看。

- `bootcmd` 的作用？

    不太记得文问的什么了，按自己的来：启动内核、初始化memory controller？传递参数、下载内核到 memory中。。。

- 文件复制的命令

    `cd`、`dd `、`>` 重定向的。视频面试题





> 问对物理内存和虚拟内存地址之间的了解，还有二者之间如何映射的。

自己的回答：

首先对于物理内存，是计算机系统的实际硬件内存（DDR（DRAM）、SRAM），内存芯片，实际用来存储程序和数据。

对于现代的计算机系统来说，物理内存地址空间都是统一编址的，比如从0到4GiB。

另外，计算机系统一般都不会直接访问物理地址的，为了安全和一些多道程序加载（防止各个进程互相影响）的问题，所以会使用虚拟内存地址。

其通过一个映射机制或者说数据结构来将物理地址和虚拟地址联系起来。

现代的 arch 几乎都选择的是 **分页机制**，实际就是 radix tree（基数树），维护一个页表。

但实际这个页表维护的就是一个数学函数 *f(n)* 一个地址映射到另一个地址。

具体怎么实现的，不同 arch 有不同的寄存器，但大同小异。

比如 RISC-V 的 `satp(Supervisor Address Translation and Protection)` 寄存器、x86 的 `cr3` 寄存器 ARM 的 `TTBR0(Translation Table Base Register)` 寄存器。。。

映射到核心机制就在于 MMU，一个硬件模块，做在了 CPU 内部，当然现代的 MMU 为了加速，里面其实还有个叫 TLB`(Translation Lookaside Buffer`) 的寄存器，当成MMU 的缓存，由时间局部性和空间局部性原理，存储常用的页表，就是虚拟内存如何映射到物理内存的。

具体过就是：

1. 虚拟地址拆分为页号（VPN）和页内偏移量（Offset）。

2. 然后MMU通过VPN查找页表，获取对应PFN。

    > 一些细节不展开
    >
    > 1. 页表由多个物理页（称为**页表页**）组成，每个页表页存储固定数量的页表项（PTE）。
    >
    > - **页表页的物理存储与容量**
    >
    >     - **页表页大小**：通常与物理内存页大小一致（如4KB）。
    >     - **页表项大小**：在RISC-V中，每个PTE占用**8字节**。
    >     - **每页表页的PTE数量**：即每个页表页可存储512个PTE。
    >
    > - **多级页表的层级结构**
    >
    >     在RISC-V Sv39中，虚拟地址被划分为三级页号（VPN[2], VPN[1], VPN[0]）和12位页内偏移（Offset）。
    >
    >     - **页表层级**：
    >         - **第一级页表**：由`satp`寄存器指向根页表页，通过VPN[2]索引到第二级页表页的基址。
    >         - **第二级页表**：通过VPN[1]索引到第三级页表页的基址。
    >         - **第三级页表（叶子页表）**：通过VPN[0]索引到最终的PTE，该PTE指向物理页帧号（PFN）。
    >     - **每个层级的页表均为独立的物理页**，因此三级页表可能占用3个物理页（最简情况）。
    >     - **实际场景**：若虚拟地址空间稀疏，高层页表可能共享部分页表页以减少内存占用。
    >
    > ------
    >
    > 2. **页表项（PTE）的结构**
    >
    > 每个PTE包含以下关键字段（以RISC-V为例）：
    >
    > - **物理页帧号（PFN）**：占据高位，指向目标物理页的基址。
    > - **控制位与权限位**：占据低位，包括：
    >     - **Valid**（有效位）：1表示该PTE已映射到物理内存。
    >     - **Read/Write/eXecute**（R/W/X）：权限控制位。
    >     - **User**（U位）：1表示用户态进程可访问。
    >     - **其他标志**：如Accessed（访问位）、Dirty（脏位）等。
    >
    > ----
    >
    > 3. **叶子PTE与非叶子PTE**
    >
    >     - **叶子PTE**：位于最底层（第三级）的PTE，其PFN直接指向物理页帧，**权限位控制该页的访问规则**。
    >     - **非叶子PTE**：位于高层（第一、二级）的PTE，其PFN指向下一级页表页的基址，**权限位通常无效（仅Valid位有意义）。**
    >
    >     **示例**：
    >
    >     - 若第三级PTE的R/W/X位为`R=1, W=0, X=0`，则该页可读但不可写、不可执行。
    >     - 若用户态进程尝试写入该页，MMU会触发权限错误异常（如Store/AMO Access Fault）。

3. PFN + Offset = 物理地址。

3. **缺页处理**：若页表项无效（未加载或权限不足），触发缺页中断，操作系统将数据从磁盘加载到物理内存，更新页表。

另外，现代的进程是建立在分页机制上的，os 为每个进程提供抽象内存空间，主要是隔离不同的进程、有保护性。具体就是通过页表权限位实现内存隔离（如用户态与内核态隔离），同时支持共享内存（如多个进程共享代码段）。





一些提高性能的设计：

- **零拷贝优化**：写时复制（Copy-on-Write）技术减少内存冗余（如fork进程）。
- **高性能场景**：通过大页（Huge Pages）减少TLB Miss，提升数据库性能。





## 一面技术面

### 问答

- **进程、线程区别**
- **进程间通信**
- **智能指针**
- **中断处理流程**
- **线程安全**
- **进程间通信**
- **malloc 和 new**
- **野指针和内存泄露**
- **I2C 和 SPI 和 UART的时序**



### 算法

两字符串计算和：”123“ + “321”  = 444 

一开始的版本：

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 1000

int main() {
    char str1[MAX_LEN], str2[MAX_LEN];
    long long num1, num2;

    fgets(str1, sizeof(str1), stdin);
    fgets(str2, sizeof(str2), stdin);

    str1[strcspn(str1, "\n")] = '\0';
    str2[strcspn(str2, "\n")] = '\0';

    char *endptr1 = NULL, *endptr2 = NULL;
    num1 = strtoll(str1, &endptr1, 10);
    num2 = strtoll(str2, &endptr2, 10);

    printf("%lld\n", num1 + num2);

    return 0;
}

```

但之后又说，字符串很长怎么办。

直接改成大数：

```C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LEN 1000

static void reverse(char *str) {
    int n = strlen(str);
    for (int i = 0; i < n / 2; i++) {
        char temp = str[i];
        str[i] = str[n - i - 1];
        str[n - i - 1] = temp;
    }
}

static char* add_strings(const char *num1, const char *num2) {
    int len1 = strlen(num1);
    int len2 = strlen(num2);
    int max_len = (len1 > len2) ? len1 : len2;

    // 创建可修改的副本并反转
    char *n1 = strdup(num1);
    char *n2 = strdup(num2);
    reverse(n1);
    reverse(n2);

    // 结果缓冲区（多一位用于进位）
    char *result = (char*)malloc(max_len + 2);
    int carry = 0;
    int index = 0;

    for (int i = 0; i < max_len; i++) {
        int digit1 = (i < len1) ? (n1[i] - '0') : 0;
        int digit2 = (i < len2) ? (n2[i] - '0') : 0;
        int sum = digit1 + digit2 + carry;

        carry = sum / 10;
        result[index++] = (sum % 10) + '0';
    }

    // 处理最高位进位
    if (carry > 0) {
        result[index++] = carry + '0';
    }

    result[index] = '\0';
    reverse(result);  // 恢复正确顺序

    free(n1);
    free(n2);
    return result;
}

int main() {
    char num1[MAX_LEN], num2[MAX_LEN];

    // 读取输入（假设无前导空格和非法字符）
    fgets(num1, sizeof(num1), stdin);
    fgets(num2, sizeof(num2), stdin);

    num1[strcspn(num1, "\n")] = '\0';
    num2[strcspn(num2, "\n")] = '\0';

    char *result = add_strings(num1, num2);
    printf("%s\n", result);
    free(result);

    return 0;
}

```

比较简单，AI解析即可。

> ### **大数加法算法详解（字符串实现法）**
>
> ---
>
> #### **一、为什么需要大数加法？**
> 常规的整数类型（如 `int`、`long`）有存储上限：
> - `int` 最大约 21亿（32位）
> - `unsigned long long` 最大约 18艾（64位）
>
> 当处理 **超过 10^100 位** 的数字（如密码学、天体物理计算）时，必须使用字符串模拟手工计算。
>
> ---
>
> #### **二、手工加法原理回顾**
> 以 `123 + 4567` 为例：
> ```
>   0123
> + 4567
> -------
>   4690
> ```
> **手工步骤**：
> 1. 个位对齐（3+7=10，写0进1）
> 2. 十位相加（2+6+1=9）
> 3. 百位相加（1+5=6）
> 4. 千位补4
>
> **核心规律**：
> - **从右向左** 逐位相加
> - **进位** 需要传递到高位
>
> ---
>
> #### **三、算法实现步骤分解**
>
> ##### **步骤 1：字符串反转**
> **为什么反转？**  
> 计算机无法直接从字符串末尾开始处理，反转后：
> - 个位存储在索引0位置
> - 高位索引递增
> ```
> 原数字："123"   → 反转后："321"
> 原数字："4567"  → 反转后："7654"
> ```
>
> **代码实现**：
> ```c
> void reverse(char *str) {
>     int n = strlen(str);
>     for (int i = 0; i < n/2; i++) {
>         char temp = str[i];
>         str[i] = str[n - i - 1];
>         str[n - i - 1] = temp;
>     }
> }
> ```
>
> ---
>
> ##### **步骤 2：逐位相加**
> **核心逻辑**：
> ```c
> for 每一位 i:
>     当前位和 = num1[i] + num2[i] + 进位
>     当前位结果 = 和 % 10
>     新进位 = 和 / 10
> ```
>
> **边界处理**：
>
> - 两数字长度不同时，短的数字高位补0
> - 最高位计算后仍有进位要处理
>
> **代码片段**：
> ```c
> int max_len = max(len1, len2);
> for (int i = 0; i < max_len; i++) {
>     int digit1 = (i < len1) ? num1[i] - '0' : 0;
>     int digit2 = (i < len2) ? num2[i] - '0' : 0;
>     int sum = digit1 + digit2 + carry;
>     
>     carry = sum / 10;
>     result[index++] = (sum % 10) + '0';
> }
> ```
>
> > 这里多解释一点：
> >
> > - 这行代码使用三元运算符。 如果 `i` 小于 `len1`，则 `digit1` 被赋值为 `num1[i] - '0'` 的值；否则， `digit1` 被赋值为 0。
> > - `num1[i]` 访问字符串 `num1` 的第 `i` 个字符。
> > - `'0'` 是字符 '0' 的 ASCII 值。 从字符数字中减去 '0' 可以将其转换为相应的整数值。 例如，`'5' - '0'` 的结果是整数 `5`。
> > - 本质上，如果 `i` 还在 `num1` 的长度范围内，这行代码从 `num1` 中提取第 `i` 位数字，并将其转换为整数。 如果 `i` 超出了 `num1` 的长度范围，则 `digit1` 被赋值为 0，这相当于在较短的数字字符串前补 0。
>
> ---
>
> ##### **步骤 3：处理最高位进位**
> 示例：`999 + 1 = 1000`
> ```c
> if (carry > 0) {
>     result[index++] = carry + '0';
> }
> ```
>
> ---
>
> ##### **步骤 4：反转结果恢复顺序**
> 之前的计算是从低位到高位，最终结果需要反转：
> ```
> 计算结果缓冲区："0001" → 反转后 → "1000"
> ```
>
> ---
>
> #### **四、完整代码注释解析**
> ```c
> #include <stdio.h>
> #include <string.h>
> #include <stdlib.h>
> 
> #define MAX_LEN 1000
> 
> // 反转字符串函数
> static void reverse(char *str) {
>     int n = strlen(str);
>     for (int i = 0; i < n / 2; i++) {
>         char temp = str[i];
>         str[i] = str[n - i - 1];
>         str[n - i - 1] = temp;
>     }
> }
> 
> // 大数加法核心函数
> static char* add_strings(const char *num1, const char *num2) {
>     int len1 = strlen(num1);
>     int len2 = strlen(num2);
>     int max_len = (len1 > len2) ? len1 : len2;
> 
>     // 创建可修改副本并反转
>     char *n1 = strdup(num1);  // 复制num1
>     char *n2 = strdup(num2);  // 复制num2
>     reverse(n1);              // 反转后个位在索引0
>     reverse(n2);
> 
>     // 结果缓冲区：多申请2字节（进位和结束符）
>     char *result = (char*)malloc(max_len + 2);
>     int carry = 0;  // 进位值
>     int index = 0;  // 结果写入位置
> 
>     for (int i = 0; i < max_len; i++) {
>         // 获取当前位的数字，超出长度补0
>         int digit1 = (i < len1) ? (n1[i] - '0') : 0;
>         int digit2 = (i < len2) ? (n2[i] - '0') : 0;
>         int sum = digit1 + digit2 + carry;
> 
>         carry = sum / 10;             // 计算进位
>         result[index++] = (sum % 10) + '0';  // 当前位结果
>     }
> 
>     // 处理最高位进位（如999+1=1000）
>     if (carry > 0) {
>         result[index++] = carry + '0';
>     }
> 
>     result[index] = '\0';  // 字符串结束符
>     reverse(result);        // 反转恢复正确顺序
> 
>     // 释放临时内存
>     free(n1);
>     free(n2);
>     return result;
> }
> 
> int main() {
>     char num1[MAX_LEN], num2[MAX_LEN];
> 
>     // 读取输入（假设输入合法）
>     fgets(num1, sizeof(num1), stdin);
>     fgets(num2, sizeof(num2), stdin);
> 
>     // 去除换行符
>     num1[strcspn(num1, "\n")] = '\0';
>     num2[strcspn(num2, "\n")] = '\0';
> 
>     char *result = add_strings(num1, num2);
>     printf("Result: %s\n", result);
>     free(result);  // 释放结果内存
> 
>     return 0;
> }
> ```
>
> ---
>
> #### **五、关键问题与优化**
>
> ##### **1. 时间复杂度分析**
> - **反转操作**：O(n)
> - **逐位相加**：O(max(m,n))
> - **总体复杂度**：O(n) ，线性时间效率
>
> ##### **2. 内存管理要点**
> - 使用 `strdup()` 复制字符串后必须 `free()`
> - 结果字符串需要手动 `malloc()` 和 `free()`
>
> ##### **3. 边界测试案例**
> | 测试用例         | 预期结果 | 说明             |
> | ---------------- | -------- | ---------------- |
> | "0" + "0"        | "0"      | 零值处理         |
> | "999" + "1"      | "1000"   | 最高位进位       |
> | "123456" + "789" | "124245" | 不同长度数字相加 |
>
> ##### **4. 扩展优化方向**
> - **前导零处理**：结果中去除前导零（如 "000123" → "123"）
> - **负数支持**：增加符号位判断和减法逻辑
> - **性能优化**：预计算长度，避免多次 `strlen()`
>

> ### **大数加法的优化实现方案**
>
> ---
>
> #### **一、替代算法分析**
> 基础的字符串反转法（时间复杂度 O(n)，空间复杂度 O(n)）已是最优理论复杂度，但可通过以下方法优化 **常数因子** 和 **实际内存占用**：
>
> ---
>
> #### **二、优化方案 1：免反转直接计算**
> **核心思想**：直接从字符串末尾开始计算，避免反转操作  
> **优势**：减少两次反转操作的时间，节省临时内存
>
> ```c
> char* add_strings_optimized(const char *num1, const char *num2) {
>     int i = strlen(num1) - 1;
>     int j = strlen(num2) - 1;
>     int max_len = (i > j) ? i+1 : j+1;
>     char *result = malloc(max_len + 2); // +1进位 +1结束符
>     int index = 0;
>     int carry = 0;
> 
>     // 从末位开始逐位相加
>     while (i >= 0 || j >= 0 || carry > 0) {
>         int digit1 = (i >= 0) ? num1[i--] - '0' : 0;
>         int digit2 = (j >= 0) ? num2[j--] - '0' : 0;
>         int sum = digit1 + digit2 + carry;
>         
>         result[index++] = (sum % 10) + '0';
>         carry = sum / 10;
>     }
> 
>     result[index] = '\0';
>     
>     // 反转结果（因为存储顺序是低位在前）
>     for (int k = 0; k < index/2; k++) {
>         char temp = result[k];
>         result[k] = result[index - k - 1];
>         result[index - k - 1] = temp;
>     }
>     
>     return result;
> }
> ```
>
> **性能对比**：  
> | 操作           | 原方案          | 优化方案  |
> | -------------- | --------------- | --------- |
> | 内存分配次数   | 3次 (n1,n2,res) | 1次 (res) |
> | 字符串反转次数 | 3次             | 1次       |
> | 代码行数       | 约 30 行        | 约 20 行  |
>
> ---
>
> #### **三、优化方案 2：预计算长度**
> **核心思想**：提前确定结果最大长度，一次性分配内存  
> **优势**：避免动态数组扩容开销
>
> ```c
> char* add_strings_prealloc(const char *num1, const char *num2) {
>     int len1 = strlen(num1);
>     int len2 = strlen(num2);
>     int max_len = (len1 > len2) ? len1 : len2;
>     
>     // 预分配内存（最大可能长度）
>     char *result = malloc(max_len + 2); // +1进位 +1结束符
>     int carry = 0;
>     int index = max_len + 1; // 从末尾向前填充
>     
>     result[index--] = '\0';
> 
>     for (int i = len1-1, j = len2-1; i >= 0 || j >= 0 || carry > 0; i--, j--) {
>         int digit1 = (i >= 0) ? num1[i] - '0' : 0;
>         int digit2 = (j >= 0) ? num2[j] - '0' : 0;
>         int sum = digit1 + digit2 + carry;
>         
>         carry = sum / 10;
>         result[index--] = (sum % 10) + '0';
>     }
> 
>     // 返回有效起始位置（跳过未使用的预分配空间）
>     return &result[index + 1];
> }
> ```
>
> **内存优化效果**：  
> - 原方案：`2*N + M`（N为输入长度，M为结果长度）  
> - 本方案：`M + 2`（精确控制内存占用）
>
> ---
>
> #### **四、优化方案 3：原地修改（输入可写时）**
> **前提条件**：允许修改输入字符串  
> **优势**：零额外内存分配（极端优化）
>
> ```c
> // 假设 num1 有足够空间存放结果（需提前扩容）
> void add_in_place(char *num1, char *num2) {
>     int len1 = strlen(num1);
>     int len2 = strlen(num2);
>     int max_len = (len1 > len2) ? len1 : len2;
>     int carry = 0;
>     int i = len1 - 1;
>     int j = len2 - 1;
>     int k = max_len;
> 
>     // 从末尾向前计算
>     while (i >= 0 || j >= 0 || carry > 0) {
>         int digit1 = (i >= 0) ? num1[i--] - '0' : 0;
>         int digit2 = (j >= 0) ? num2[j--] - '0' : 0;
>         int sum = digit1 + digit2 + carry;
>         
>         carry = sum / 10;
>         num1[k--] = (sum % 10) + '0';
>     }
> 
>     // 移动结果到起始位置
>     memmove(num1, &num1[k+1], max_len - k);
>     num1[max_len - k] = '\0';
> }
> ```
>
> **适用场景**：  
> - 嵌入式系统（内存严格受限）  
> - 高频调用场景（避免频繁内存分配）
>
> ---
>
> #### **五、复杂度对比与选型建议**
>
> | 方案           | 时间复杂度 | 空间复杂度 | 适用场景             |
> | -------------- | ---------- | ---------- | -------------------- |
> | 基础反转法     | O(n)       | O(2n + m)  | 教学演示、快速实现   |
> | 免反转直接计算 | O(n)       | O(m)       | 通用场景（推荐首选） |
> | 预计算长度     | O(n)       | O(m)       | 精确内存控制         |
> | 原地修改       | O(n)       | O(1)       | 内存极端受限环境     |
>
> **工程实践建议**：  
> 1. **常规开发**：选择 **免反转直接计算**（代码简洁、内存高效）  
> 2. **高频调用**：使用 **预计算长度** + 内存池（避免频繁 malloc）  
> 3. **嵌入式环境**：优先 **原地修改**（需确保输入缓冲区足够大）  
>
> ---
>
> #### **六、终极优化：SIMD 并行计算**
> **原理**：利用 CPU 的 SIMD 指令集（如 AVX-512）并行处理多位  
> **示例代码**（概念演示，需特定硬件支持）：
>
> ```c
> #include <immintrin.h>
> 
> void simd_add(const char *num1, const char *num2, char *result) {
>     // 将字符串转换为向量寄存器
>     __m512i v1 = _mm512_loadu_epi8(num1);
>     __m512i v2 = _mm512_loadu_epi8(num2);
>     
>     // SIMD 并行加法
>     __m512i sum = _mm512_add_epi8(v1, v2);
>     
>     // 处理进位（需要额外算法）
>     // ...
>     
>     _mm512_storeu_epi8(result, sum);
> }
> ```
>
> **性能提升**：  
> - 理论加速比：16 倍（512位寄存器 / 32位系统）  
> - 实现难度：极高（需手动处理跨字节进位链）  
>
> **适用场景**：  
> - 超大规模数值计算（如百万位加法）  
> - 高性能计算专用领域  
>
> ---
>
> ### **总结**  
> 大数加法的优化核心在于 **减少内存操作** 和 **利用硬件特性**。对于大多数应用场景，**免反转直接计算法** 是最佳选择，在保持代码简洁性的同时达到最优性能。特殊场景下可结合 SIMD 或原地修改技术实现极致优化。





















