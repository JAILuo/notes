## 分析strcpy()和strdup()

- 源代码实现
- 各种特点
- 哪个使用更好
- 具体例子

好的，让我来仔细分析一下 `strcpy` 和 `strdup`。

#### strcpy
`strcpy` 是 C 语言中的一个字符串操作函数，用于将一个字符串复制到另一个字符串数组中。其代码为：

```c
// strcpy 的源代码实现
char *strcpy(char *dest, const char *src) {
    char *save = dest;
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src?
    }
    *dest = '\0';
    return save;
}
```
`strcpy` 的特点：

- `strcpy` 需要手动确保目标字符串数组有足够的空间来存储源字符串，否则可能导致缓冲区溢出的问题。
- `strcpy` 不会自动分配内存，需要手动管理内存的分配和释放。
- 如果源字符串是一个常量字符串，如 "tom"，那么不能直接使用 `strcpy` 来赋值，因为常量字符串是只读的，需要分配足够的内存来存储该字符串。

#### strdup
`strdup` 是一个非标准函数，它并不是所有的 C 编译器都支持，但是它非常常见，并且在很多系统上都有实现。`strdup` 用于复制一个字符串，并返回一个指向新分配的内存空间的指针，其中存储了复制的字符串。`strdup` 的特点：

```C
// strdup 的源代码实现
char *strdup(const char *str) {
    size_t len = strlen(str) + 1; // 计算字符串长度，包括字符串结束符 \0
    char *new_str = (char *)malloc(len); // 分配足够的内存空间
    if (new_str == NULL) {
        return NULL; // 内存分配失败
    }
    strcpy(new_str, str); // 将源字符串复制到新分配的内存空间中
    //或者用memcpy(new, str, len); 
    return new_str;
}
```

- `strdup` 会自动分配足够的内存来存储复制的字符串，不需要手动管理内存的分配和释放。
- `strdup` 返回的指针指向的内存需要手动释放，使用完毕后应该调用 `free` 函数来释放内存。

#### 哪个使用更好
在一般情况下，使用 `strdup` 更加安全和方便。因为它会自动分配足够的内存来存储复制的字符串，避免了缓冲区溢出的问题，也简化了内存管理。但需要注意的是，并非所有的 C 编译器都支持 `strdup` 函数，如果需要在跨平台或者特定环境下使用，可能需要考虑兼容性。

#### 具体例子
下面是使用 `strcpy` 和 `strdup` 的具体例子：

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char source[] = "Hello";
    char dest1[20];
    char *dest2;

    // 使用 strcpy
    strcpy(dest1, source);
    printf("strcpy: %s\n", dest1);

    // 使用 strdup
    dest2 = strdup(source);
    printf("strdup: %s\n", dest2);

    // 释放 strdup 分配的内存
    free(dest2);

    return 0;
}
```

在上面的例子中，我们首先使用 `strcpy` 将源字符串复制到目标字符串数组中，然后使用 `strdup` 复制源字符串并返回一个指向新分配内存的指针，最后需要手动释放 `strdup` 分配的内存。





#### 使用strcpy()和memcpy)()的分析和总结

**`strcpy`和`memcpy`都是C语言中用于复制内存块的函数**，但它们之间有一些重要的区别。

- `strcpy`函数的原型如下：

    ```c
    char *strcpy(char *dest, const char *src);
    ```

    `strcpy`函数会将`src`指向的字符串复制到`dest`指向的字符串中，直到遇到字符串结束符`\0`。**这意味着`strcpy`只能用于复制C风格的字符串。**

- `memcpy`函数的原型如下：

    ```c
    void *memcpy(void *dest, const void *src, size_t n);
    ```

    `memcpy`函数会从`src`指向的内存地址开始，复制`n`个字节的数据到`dest`指向的内存地址中。它是一种通用的内存复制函数，可以用于复制任意类型的内存块，不仅限于C风格的字符串。

- 下面是`memcpy`函数的源代码实现：

    ```c
    void *memcpy(void *dest, const void *src, size_t n) {
        char *d = dest;
        const char *s = src;
        while (n--) {
            *d++ = *s++;
        }
        return dest;
    }
    ```

    **`memcpy`函数的好处是它可以用于复制任意类型的内存块，而不仅仅是字符串。另外，由于`memcpy`是按字节进行复制的，因此它更适合于复制二进制数据或者自定义数据结构。**

    **总结：`strcpy`适用于C风格的字符串复制，而`memcpy`适用于通用的内存块复制。**







## 分析strncpy()和strlcpy()

`strncpy` 和 `strlcpy` 都是用于字符串复制的函数，但它们在实现细节上有一些重要的区别。

#### strncpy

```c
char *strncpy(char *dest, const char *src, size_t n) {
    size_t i;
    for (i = 0; i < n && src[i] != '\0'; i++) {
        dest[i] = src[i];
    }
    for ( ; i < n; i++) {
        dest[i] = '\0';
    }
    return dest;
}
```

- 功能：`strncpy` 函数会将源字符串 `src` 的前 `n` 个字符复制到目标字符串 `dest` 中。

- 解析：如果 `src` 的长度小于 `n`，则剩余的部分会用空字符 `\0` 填充。**如果 `src` 的长度大于 `n`，则 `dest` 不会以空字符 `\0` 结尾。**

#### strlcpy

```c
size_t strlcpy(char *dest, const char *src, size_t size) {
    size_t src_len = strlen(src);
    size_t copy_len = (size <= 0) ? 0 : (size - 1);
    if (copy_len < src_len) {
        memcpy(dest, src, copy_len);
        dest[copy_len] = '\0';
    } else {
        memcpy(dest, src, src_len);
        dest[src_len] = '\0';
    }
    return src_len;
}
```

- 功能：`strlcpy` 函数会将源字符串 `src` 的前 `size-1` 个字符复制到目标字符串 `dest` 中，并始终确保 `dest` 以空字符 `\0` 结尾。

如果 `src` 的长度大于 `size-1`，则会截断 `src`，并在 `dest` 的末尾添加空字符 `\0`。如果 `src` 的长度小于 `size-1`，则会完整复制 `src` 并在 `dest` 的末尾添加空字符 `\0`。

##### 总结

`strncpy` 存在缺陷，容易导致目标字符串不以空字符 `\0` 结尾，而 `strlcpy` 则更安全，始终确保目标字符串以空字符 `\0` 结尾。**因此，通常建议使用 `strlcpy` 来避免 `strncpy` 的潜在问题。**





## 分析malloc()和calloc()

> **到时候具体参见FreeRTOS的内部实现**

`malloc`和`calloc`函数都是C语言中用于动态分配内存的函数，它们在内存管理中起着非常重要的作用。下面我将对它们进行详细介绍。

### `malloc`函数

#### 背景
`malloc`函数用于在堆上分配指定大小的内存块。它是C标准库中的函数，可以帮助程序在运行时动态分配内存，以满足程序在编译时无法确定的内存需求。

#### 原型
```c
void *malloc(size_t size);
```

`malloc`函数接受一个`size`参数，表示需要分配的内存块大小，单位是字节。它返回一个指向分配内存块起始地址的指针，如果分配失败则返回`NULL`。

#### 源码实现
`malloc`函数的具体实现可能因平台和编译器而异，通常会调用底层的内存分配函数（如`brk`、`sbrk`或`mmap`）来获取内存。它会在堆上寻找足够大小的空闲内存块，然后将该内存块标记为已使用，并返回其起始地址。

#### 使用
```c
int *ptr = (int *)malloc(10 * sizeof(int));
if (ptr != NULL) {
    // 内存分配成功，可以使用ptr指针访问分配的内存块
    // ...
    free(ptr);  // 使用完毕后记得释放内存
}
```

### `calloc`函数

#### 背景
`calloc`函数也用于在堆上分配内存，但它与`malloc`不同之处在于，`calloc`会在分配内存的同时将内存块的内容初始化为零。

#### 原型
```c
void *calloc(size_t num, size_t size);
```

`calloc`函数接受两个参数，`num`表示需要分配的元素个数，`size`表示每个元素的大小（单位是字节）。它返回一个指向分配内存块起始地址的指针，如果分配失败则返回`NULL`。

#### 源码实现
`calloc`函数的实现通常会调用底层的内存分配函数（如`brk`、`sbrk`或`mmap`），然后将分配的内存块内容初始化为零。

#### 使用
```c
int *ptr = (int *)calloc(10, sizeof(int));
if (ptr != NULL) {
    // 内存分配成功，ptr指向的内存块已被初始化为零
    // ...
    free(ptr);  // 使用完毕后记得释放内存
}
```

### 注意事项
- 使用`malloc`和`calloc`分配的内存块在使用完毕后应该通过`free`函数进行释放，以避免内存泄漏。
- 在使用分配的内存时要小心避免出现内存越界、重复释放、未初始化等问题，这些问题容易导致程序运行时错误。

总的来说，`malloc`和`calloc`函数是C语言中动态内存分配的重要工具，程序员需要谨慎使用并遵循内存管理的最佳实践。

> 在free掉一部分空间之后,到底要不要将指向NULL





在Linux的x86体系结构上，`malloc`函数的具体实现通常是由C标准库提供的。在GNU C库（glibc）中，`malloc`函数的实现是由`malloc`子系统负责的。下面是一个简化的伪代码示例，展示了`malloc`函数的可能实现方式：

```c
// 伪代码示例：简化的malloc函数实现

// 定义内存块的头部结构
struct block_header {
    size_t size;  // 内存块大小
    bool free;    // 是否空闲
    // 其他元数据...
};

// 伪代码中的全局变量，指向堆的起始地址
void *heap_start;

// 初始化堆
void init_heap() {
    // 使用brk或mmap等系统调用初始化堆
    heap_start = // 初始化堆的起始地址
    // 其他初始化操作...
}

// 分配内存的伪代码实现
void *malloc(size_t size) {
    // 如果堆未初始化，则先初始化堆
    if (heap_start == NULL) {
        init_heap();
    }

    // 在堆上寻找足够大小的空闲内存块
    struct block_header *block = find_free_block(size);
    if (block != NULL) {
        // 将内存块标记为已使用
        block->free = false;
        return (void *)(block + 1);  // 返回内存块起始地址（跳过头部结构）
    } else {
        // 未找到足够大小的空闲内存块，调用底层的内存分配函数（如brk、sbrk或mmap）来获取内存
        // 分配内存并返回内存块起始地址
        // ...
    }
}

// 释放内存的伪代码实现
void free(void *ptr) {
    // 将内存块标记为空闲
    struct block_header *block = (struct block_header *)ptr - 1;
    block->free = true;
    // 其他操作...
}
```

以上是一个简化的伪代码示例，实际的`malloc`函数实现会更加复杂，涉及到内存对齐、内存碎片整理、线程安全等方面的问题。





## 分析memcpy()、memcpy()、memset()







## IO函数总结

#### 相关概念

##### 什么是IO

> I：input（从外部设备(键盘、鼠标...)将数据输入到内存中）
> o：output（从内存将数据拷贝到输出设备(显示器...)上）
> 
> 
>
> 更进一步:
> Linux下一切皆文件
> 输入：从文件将数据输入到内存中
> 输出：从内存将数据拷贝到文件中

##### 标准IO和文件IO

> 1. **标准IO（stdin和stdout）**：
>
>    - 标准输入（stdin）是指**程序默认从键盘获取输入的流**，通常使用scanf函数来读取标准输入中的数据。
>    - 标准输出（stdout）是指**程序默认向屏幕输出结果的流**，通常使用printf函数将结果输出到标准输出中。
>    - 特点：
>        - 可以跨平台使用, Linux、Windows等上都可以用
>        - 库函数: stdio.h ：scanf、printf
>        - 有缓冲机制
>        - 通过文件流指针来操作
>        - 一般用普通文件的操作
>
> 2. **文件I/O**：
>
>    - 文件I/O 是指**程序与文件进行交互的输入输出操作**。程序可以打开一个文件，从文件中读取数据（输入），或者将数据写入文件（输出）。
>    - 通过使用fopen函数来打开文件，使用fread和fwrite函数来读写文件。
>    - 特点
>
>        - 文件描述符（非负的整数）
>        - 无缓冲机制
>        - 系统调用
>        - 一般用于设备文件的操作
>
>
> 3. **区别：**
>    - 标准输入输出是程序与用户交互的方式，通常用于从键盘读取输入和向屏幕输出结果。
>    - 文件I/O是程序与文件进行交互的方式，通常用于读取和写入文件中的数据。
>
> **总的来说，标准输入输出用于与用户进行交互，而文件I/O用于与文件进行交互。**

##### **文件类型**

> 1. **普通文件 -**
>
>     > 1. **ASCII码文件 (文本文件)：使用fegts、fputs函数读写**
>     >
>     > 2. **二进制文件：用fread、fwrite函数读写**
>
> 2. 目录文件 d
> 3. 块设备文件 b
> 4. 字符设备文件 c
> 5. 链接文件 l
> 6. 管道文件 p
> 7. 套接字文件 （socket）s

##### 系统调用

> - C语言中的IO操作最终会调用操作系统提供的系统调用来实现。
>
> - 系统调用是操作系统提供的接口，用于进行底层硬件的输入输出操作。

##### 缓冲区

> 1. 理解
>
>     > 可以当成内存中的一块区域，用于临时存储数据。当进行IO操作的时候, 数据首先被写入到缓冲区，然后在适当的时机才会被刷新到文件或设备中。
>
> 2. 作用
>
>     > **缓冲区有效减少对底层系统调用的频繁操作，从而提高IO性能**。例如，当使用printf函数打印数据时，
>     >
>     > 数据首先被写入到缓冲区，而不是立即被发送到标准输出设备。这样可以将多个小的输出操作合并成一个大的输出操作，减少了频繁的IO操作，提高了效率。
>
> 3. 类型
>
>     > 1. 全缓存：当缓冲区满、程序结束、强制刷新缓冲区时会刷新缓冲区
>     >
>     >     > **常用在缓冲区满了才写进文件**
>     >
>     > 2. 行缓存：当缓冲区满、程序运行结束、强制刷新缓冲区、遇到换行符时会刷新缓冲区
>     >
>     >     > **换行才写进文件**
>     >
>     > 3. 不缓存：没有缓存区，直接输出
>     >
>     >     > **数据立即写入文件**
>
> 4. 补充
>
>     > 程序运行起来之后，会默认打开三个文件，
>     >
>     > 标准输入、标准输出、标准出错，
>     >
>     > 对应的流指针分别为stdin、stdout、stderror

##### 流和FILE指针

> 1. 流是一种抽象的概念，**它可用来表示数据的传输或处理过程**。
>
>     - 流通常被用于表示数据的输入、输出或处理
>     - 流可以是单向的，即只能进行读取或写入操作，也可以是双向的，即可以进行读取和写入操作。
>
> 2. 文件流
>
>     - 文件流是**与文件相关联的数据流**。在 C 语言中，可以使用标准库中的函数（如 `fopen`、`fclose`、`fread`、`fwrite` 等）来创建文件流，并进行文件的读取和写入操作。
>     - 文件流可以是文本模式的，也可以是二进制模式的，这取决于打开文件时使用的模式。
>     - 文件流与文件相关，他提给开发者一个抽象的接口，使得我们能通过文件流来操作文件的数据。
>
> 3. 产生
>
>     在计算机中，文件是**以字节的形式存储在内存**上的。
>
>     当我们使用 `fopen` 函数打开一个文件时，操作系统会为该文件创建一个文件流，并返回一个指向该文件流的指针FILE。
>
>     接着，我们可以使用这个指针来进行文件的读取和写入操作，而这些操作实际上是通过文件流来进行的。







##### C 中使用 gets() 提示 warning: this program uses gets(), which is unsafe.

-  分类 [编程技术](https://www.runoob.com/w3cnote_genre/code)

C 中使用 gets() ，编译时会出现如下警告：

```
warning: this program uses gets(), which is unsafe.
```

gets() 不安全是因为你给了他一个缓冲区，但是你却没有告诉它这个缓冲区到底有多大，也不知道输入的内容到底有多大，输入的内容可能超出缓冲区的结尾，引起你的程序崩溃。

解决方法可以使用 fgets 替代：

```c
char buffer[bufsize];
fgets(buffer, bufsize, stdin);
```

实例：

```c
// 使用 gets()
char buffer[4096];
gets(buffer);
 
// 使用 fgets() 替换 gets()
char buffer[4096];
fgets(buffer, (sizeof buffer / sizeof buffer[0]), stdin);
```



#### printf家族

- printf：
    - 用于格式化输出到标准输出流（屏幕）。它接受一个格式化字符串和对应的参数列表，根据格式化字符串的指示将参数输出到屏幕上。例如，`printf("Hello, %s!\n", "world")`将会输出`Hello, world!`到屏幕上。
- printf族成员：sprintf、fprintf、snprintf等
    - sprintf：将格式化的数据写入字符串
    - fprintf：将格式化的数据写入文件
    - snprintf：将格式化的数据写入字符串，并限制输出的字符数





#### scanf家族
- scanf：
    - 用于从标准输入流（键盘）读取数据并按照指定格式进行解析。它接受一个格式化字符串和对应的参数列表，根据格式化字符串的指示从输入流中读取数据并将其存储到参数中。例如，`scanf("%d", &num)`将会从键盘上读取一个整数并将其存储到变量`num`中。
- scanf族成员：sscanf、fscanf等
    - sscanf：从字符串中读取格式化的数据
    - fscanf：从文件中读取格式化的数据







- 重点看看lcthw的练习26 27的内容 

- 终止程序和显示警告的问题 （关于防御性编程的问题）







## fprintf()函数

#### 基本

函数原型：

```c
int fprintf(FILE *stream, const char *format, ...);
```

函数作用：

将格式化的数据写入到指定的文件流 `stream` 中。

参数说明：

- `stream`：指向 FILE 对象的指针，表示要写入数据的文件流。
- `format`：格式化字符串，用于指定输出的格式。
- `...`：可变参数列表，用于指定要输出的数据。

返回值：

成功返回写入的字符数（不包括字符串结尾的空字符），失败返回负数。

源码实现：

```c
int fprintf(FILE *stream, const char *format, ...) {
  va_list arg;
  int done;

  va_start(arg, format);
  done = vfprintf(stream, format, arg);
  va_end(arg);

  return done;
}
```

`fprintf()` 函数实际上是调用了 `vfprintf()` 函数，只是将可变参数列表封装成了一个 `va_list` 对象传递给了 `vfprintf()` 函数。

使用场景：

`fprintf()` 函数常用于将格式化的数据写入到文件中，可以用于日志记录、输出调试信息等场景。同时，也可以将数据输出到标准输出流 `stdout` 或标准错误流 `stderr` 中，用于命令行程序的输出。

```C
#include <stdio.h>

int main() {
    FILE *file = fopen("output.txt", "w"); // 打开一个文件用于写入
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    int num1 = 10;
    double num2 = 3.14;
    char str[] = "Hello, World!";

    fprintf(file, "Integer: %d, Float: %f, String: %s\n", num1, num2, str);

    fclose(file); // 关闭文件流

    return 0;
}
```

#### 流









## 调试宏

#### 常用

> 以后再不断扩充

```c
#ifndef __dbg_h__
#define __dbg_h__

#include <stdio.h>
#include <errno.h>
#include <string.h>
 
/*
** 通过实现一系列转换来处理错误
** 任何时候发生了错误，你的函数都会跳到执行清理和返回错误代码的“error:”区域。
** 你可以使用check宏来检查错误代码，打印错误信息，然后跳到清理区域。
** 你也可以使用一系列日志函数来打印出有用的调试信息。 
*/

#ifdef NDEBUG
#define debug(M, ...)
#else
#define debug(M, ...) fprintf(stderr, "DEBUG %s:%d:%s: " M "\n", __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#endif

#define clean_errno() (errno == 0 ? "None" : strerror(errno))

#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:%s: errno: %s) " M "\n", __FILE__, __LINE__, __func__, clean_errno(), ##__VA_ARGS__)

#define log_warn(M, ...) fprintf(stderr, "[WARN] (%s:%d:%s: errno: %s) " M "\n", __FILE__, __LINE__, __func__, clean_errno(), ##__VA_ARGS__)

#define log_info(M, ...) fprintf(stderr, "[INFO] (%s:%d:%s) " M "\n", __FILE__, __LINE__, __func__, ##__VA_ARGS__)

#define check(A, M, ...) if(!(A)) { log_err(M, ##__VA_ARGS__); errno=0; goto error; }

#define sentinel(M, ...) { log_err(M, ##__VA_ARGS__); errno=0; goto error; }

#define check_mem(A) check((A), "Out of memory.")

#define check_debug(A, M, ...) if(!(A)) { debug(M, ##__VA_ARGS__); errno=0; goto error; }
 
#endif

```



**`error` 是一个标签，通常用于在 C 语言中标记错误处理代码的位置，以便在发生错误时跳转到相应的处理逻辑。**



#### 仔细分析

- **`debug(M, ...)`**

    ```c
    debug(M, ...) fprintf(stderr, "DEBUG %s:%d:%s: " M "\n", __FILE__, __LINE__, __func__, ##__VA_ARGS__)
        
    这个宏用于 打印调试信息。
        在调试模式下，它会将带有文件名和行号的调试信息打印到标准错误流中，格式为 "DEBUG 文件名:行号: 调试信息"。
    ```

- **`clean_errno()`**

    ```C
    #define clean_errno() (errno == 0 ? "None" : strerror(errno))
    
    这个宏用于清理错误号。
        它会检查全局变量 errno 是否为 0，如果是，则返回字符串 "None"，否则返回"对应错误号的描述字符串".
    ```
    
- **`log_err(M, ...)`**

    ```c
    #define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:%s: errno: %s) " M "\n", __FILE__, __LINE__, __func__, clean_errno(), ##__VA_ARGS__)
    
    这个宏用于打印错误信息。它会将带有文件名、行号和错误号的错误信息打印到标准错误流中，
        格式为 "[ERROR] (文件名:行号: errno: 错误描述) 错误信息"。
    ```

- **`log_warn(M, ...)`**

    ```C
    #define log_warn(M, ...) fprintf(stderr, "[WARN] (%s:%d:%s: errno: %s) " M "\n", __FILE__, __LINE__, __func__, clean_errno(), ##__VA_ARGS__)
    
    这个宏用于打印警告信息。它会将带有文件名、行号和错误号的警告信息打印到标准错误流中，
        格式为 "[WARN] (文件名:行号: errno: 错误描述) 警告信息"。
    ```

- `log_info(M, ...)`

    ```c
    #define log_info(M, ...) fprintf(stderr, "[INFO] (%s:%d:%s) " M "\n", __FILE__, __LINE__, __func__, ##__VA_ARGS__)
    
    这个宏用于"打印一般信息"。它会将带有文件名和行号的一般信息打印到标准错误流中，
        格式为 "[INFO] (文件名:行号) 一般信息"。
    ```

- `check(A, M, ...)`:

    ```c
    #define check(A, M, ...) if(!(A)) { log_err(M, ##__VA_ARGS__); errno=0; goto error; }
    
    这个宏用于"检查条件 A 是否为真"。
        如果条件为假，它会打印错误信息，清空错误号并跳转到标签 error 处。
    ```

- sentinel(M, ...)

    ```C
    #define sentinel(M, ...)  { log_err(M, ##__VA_ARGS__); errno=0; goto error; }
    
    这个宏用于"打印错误信息"，清空错误号并跳转到标签 error 处。
        它通常用于"标记程序中的错误情况"。
    ```

- `check_mem(A)`

    ```c
    #define check_mem(A) check((A), "Out of memory.")
    
    这个宏用于"检查内存分配是否成功"。
        如果分配失败，它会打印相应的错误信息，清空错误号并跳转到标签 error 处。
    ```

- `check_debug(A, M, ...)`

    ````c
    #define check_debug(A, M, ...) if(!(A)) { debug(M, ##__VA_ARGS__); errno=0; goto error; }
    
    这个宏类似于  `check(A, M, ...)`，但是在调试模式下会额外打印调试信息。
    ````



#### 预定义的宏

> 常见的

- `__FILE__` 代表当前源文件的文件名，它是一个字符串常量。
- `__LINE__` 代表当前所在的行号。
- `__func__` 代表当前所在的函数名。

- `__DATE__`：代表代码被编译的日期，格式为"MMM DD YYYY"。
- `__TIME__`：代表代码被编译的时间，格式为"HH:MM:SS"。
- `__STDC__`：当编译器遵循 ANSI 标准时，该宏被定义为 1。
- `__cplusplus`：当使用 C++ 编译器编译代码时，该宏被定义。





