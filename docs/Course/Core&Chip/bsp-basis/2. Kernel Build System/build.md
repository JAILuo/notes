# Kernel Build System

> 在初期Linux是通过`Makefile`来编译，但是随着系统复杂度的提升，编译体系的复杂度也随着提升。于是在2.6版本，Linux采用了`Kbuild`机制，将编译做成了一个更加科学的系统。
>
> 这套系统现在不仅用在Linux内核编译，许多项目都在使用例如：`uboot`、`buildroot`等。所以了解和学会使用这套编译系统对于日常开发尤其是嵌入式领域是非常有必要的。
>
> Linux编译系统，也有的文章会把它简称为Kbuild子系统，内核文档中将其称为：`Kernel Build System`，我觉得官方的名称更准确一些。因为Kbuild同样也是一个编译机制，并不能代表整个编译系统，放在一起容易混淆。

Kernel Build System 组成：`Kconfig`+ `Kbuild`，各自的作用：

`Kconfig` 将配置以菜单的形式列出来供用户选择，`Kbuild` 则是将用户选择的配置的整理并生成 `.config` 配置文件用于之后的镜像编译。



## 1. Kconfig

这部分主要关注的是语法，作为一种比较构建描述语言，主要用来定义 Config symbols 的文件。它的主要作用有：

1. 组织内核各个子目录配置符号与依赖项
2. 将配置项生成`.config`文件，作为内核编译的直接输入

另外，日常基本使用的都是 `make menuconfig`，所以简单看看文章中的梳理流程：

> `menuconfig`是 Linux 内核构建系统中最常用的配置工具。它是一个基于 `ncurses`库的文本用户界面 (TUI)，解析`Kconfig`允许用户在终端环境下搜索和配置内核。
>
> 当执行`make menuconfig`时： 
>
> 1. `Makefile`调用`scripts/kconfig/mconf`
> 2. `mconf`加载顶层 `Kconfig`文件
> 3. 递归解析所有 `source "subdir/Kconfig"`语句
> 4. 显示 `ncurses`界面
> 5. 5 用户保存后调用 `conf`生成`.config`和`autoconf.h`



### `source` 和 `command`

额外插一点：关于这个 `source` 和 `command` 命令：

移植看着各种文档中都是直接使用的 `source` 和构建脚本的 `command -v` 确认程序命令，好像内部的东西自己似乎一直都没有了解过？问问 Gemini，额外见文章最后部分。







# Other

主要存放学习过程中遇到的一些想法或者问题。

## `source` & `command`

**这二者不是硬盘上的独立可执行文件（比如 `/bin/ls`），而是 Shell（比如 Bash）的“内建命令”（Built-in Commands）。** 

这意味着它们是由 Shell 程序本身直接解释执行的，用来改变 Shell 自身的行为和状态。

------

### 一、 `source` 命令：打破“子进程隔离”

在理解 `source` 之前，我们必须先理解 Linux 终端里执行脚本的默认逻辑：**子 Shell（Subshell）机制**。

#### 1. 常规执行 (`./script.sh` 或 `bash script.sh`)

当你普通地运行一个脚本时，当前的 Shell 会**fork 出一个新的子进程（子 Shell）**来执行这个脚本。

- **结果：** 脚本在这个独立的子房间里运行，它可以定义一堆环境变量，但一旦脚本执行完毕，子 Shell 销毁，**里面所有的变量和环境修改都会随之灰飞烟灭**，完全不会影响你当前的父 Shell。

#### 2. 使用 `source` 执行 (`source script.sh` 或 `. script.sh`)

`source` 的核心作用是：**拒绝创建子进程，强行把脚本里的每一行代码“吸入”到当前的 Shell 环境中逐行执行。**

- **结果：** 脚本里定义的所有环境变量、路径 (`$PATH`)、函数，全都会直接留在你当前的终端里。

#### 🧪 实验对比验证

假设我们有一个脚本 `env_setup.sh`，里面只有一行代码：

```Bash
export MY_CORECHIP_VAR="Hello_QEMU"
```

- **普通执行：**

    ```Bash
    $ ./env_setup.sh
    $ echo $MY_CORECHIP_VAR
    # (输出为空，因为变量随着子进程死掉了)
    ```

- **source 执行：**

    ```Bash
    $ source env_setup.sh
    $ echo $MY_CORECHIP_VAR
    Hello_QEMU  # (变量成功留在了当前终端！)
    ```

**🎯 核心应用场景：**

这就是为什么你在编译代码或使用 SDK（就像你终端里的 `corechip_qemu_sdk`）之前，通常都需要 `source env.sh`。因为 SDK 需要修改你当前终端的 `$PATH`、设定交叉编译器的路径，如果不使用 `source`，环境配置根本无法生效。

*(注：在 Bash 中，有一个点 `.` 是 `source` 的同义词，比如 `. env_setup.sh` 效果完全一样。)*

------

### 二、 `command` 命令：看破伪装的“照妖镜”

`command` 命令的作用看起来有点绕：“执行一个命令并忽略 Shell 函数查找”。要理解它，你需要知道 Bash 执行命令时的**优先级查找顺序**。

当你敲下一个命令（比如 `ls`），Bash 其实是在按以下顺序找它：

1. **Alias（别名）**：比如你设置了 `alias ls='ls --color=auto'`。
2. **Function（Shell 函数）**：你自己定义的同名函数。
3. **Built-in（内建命令）**：比如 `cd`, `echo`, `source`。
4. **$PATH 中的外部命令**：去 `/usr/bin/` 等目录找真正的可执行文件。

#### 1. 痛点：命令被“绑架”了怎么办？

假设为了防止误删，你在 `.bashrc` 里写了一个函数或别名来“劫持” `rm` 命令：

```Bash
rm() {
    echo "危险操作！文件已被移动到回收站"
    mv "$@" /tmp/trash/
}
```

现在你敲 `rm test.c`，它会执行你的函数。但如果某一天，你**真的想调用系统最底层、最原始的那个 `/bin/rm`**，该怎么办？

#### 2. 破局：使用 `command`

`command` 的作用就是**强制跳过上面的第 1 步（别名）和第 2 步（函数）**，直接去执行内建命令或硬盘上的真实命令。

```bash
$ command rm test.c  # 这次不会触发函数，而是真正地调用了系统的 rm 删除了文件！
```

#### 3. 神级选项：`command -v` (比 `which` 更好用)

在写 Shell 脚本时，我们经常需要检查某个工具是否安装。很多人喜欢用 `which`：

```bash
if which gcc > /dev/null; then ...
```

但 `which` 其实是一个外部程序，每次调用都要开销进程，且有些精简版 Linux 没有装 `which`。

**更标准、更优雅的做法是使用 `command -v`：**

```bash
$ command -v gcc
/usr/bin/gcc
```

它不仅快（因为是内建的），还能准确识别出别名和函数，是编写高可靠性 Shell 脚本的必备技巧。比如再写SDK时，常常会这么写：

```BASH
if command -v gcc >/dev/null 2>&1; then
	...
fi
```

- `> /dev/null` 将标准输出（`command -v` 正常找到程序时输出的路径）丢弃。
- `2>&1` 将标准错误（例如 `gcc: command not found` 这类错误信息）**也**重定向到标准输出，而标准输出已经被重定向到 `/dev/null`，因此错误信息同样被丢弃。
- 最终效果：完全静默地检测命令是否存在，不影响屏幕输出。如果 `command -v` 成功（表示 `gcc` 存在），则执行后面的语句。而如果不使用 `2>&1`，当 `gcc` 不存在时，`command -v` 会输出一条错误信息到 stderr，可能会污染脚本的运行输出。

------

### 💎 总结对比

| **特性**     | **source (或 .)**                                | **command**                                       |
| ------------ | ------------------------------------------------ | ------------------------------------------------- |
| **本质定位** | 环境变量与上下文的**注入器**                     | 真实命令的**强制执行器**                          |
| **底层行为** | 在**当前** Shell 进程中读取并执行脚本代码。      | 绕过别名和函数，直接执行底层命令或可执行文件。    |
| **核心目的** | 让脚本中的变量、函数定义在当前终端**持久生效**。 | 避免同名函数/别名冲突，找回命令的**“本来面目”**。 |
| **常见用法** | `source ~/.bashrc` `source ./env_setup.sh`       | `command ls` `command -v python3`                 |



