Shell 最好的特性就是只调用程序，因此我们只要找到合适的替代程序即可（甚至自己编写）

有些问题使用合适的工具就会迎刃而解，而具体选择哪个工具则不是那么重要。

最重要的是，现在有了 GPT，学会使用 GPT 更加重要。



## Shell 脚本

- 特殊变量

    - `$0` - 脚本名
    - `$1` 到 `$9` - 脚本的参数。 `$1` 是第一个参数，依此类推。
    - `$@` - 所有参数
    - `$#` - 参数个数
    - `$?` - 前一个命令的返回值
    - `$$` - 当前脚本的进程识别码
    - `!!` - 完整的上一条命令，包括参数。常见应用：当你因为权限不足执行命令失败时，可以使用 `sudo !!` 再尝试一次。
    - `$_` - 上一条命令的最后一个参数。如果你正在使用的是交互式 shell，你可以通过按下 `Esc` 之后键入 . 来获取这个值。

    更详细：[Special Characters (tldp.org)](https://tldp.org/LDP/abs/html/special-chars.html)





## Shell 工具

### 查看命令的用法

- `man`

- `-h`、`--help`

- [tldr pages](https://tldr.sh/)

    





### 查找文件：`find...`

程序员们面对的最常见的重复任务就是查找文件或目录。所有的类 UNIX 系统都包含一个名为 [`find`](https://man7.org/linux/man-pages/man1/find.1.html) 的工具，它是 shell 上用于查找文件的绝佳工具。`find` 命令会递归地搜索符合条件的文件，例如：

```bash
# 查找所有名称为src的文件夹
find . -name src -type d
# 查找所有文件夹路径中包含test的python文件
find . -path '*/test/*.py' -type f
# 查找前一天修改的所有文件
find . -mtime -1
# 查找所有大小在500k至10M的tar.gz文件
find . -size +500k -size -10M -name '*.tar.gz'
```

除了列出所寻找的文件之外，find 还能对所有查找到的文件进行操作。这能极大地简化一些单调的任务。

```bash
# 删除全部扩展名为.tmp 的文件
find . -name '*.tmp' -exec rm {} \;
# 查找全部的 PNG 文件并将其转换为 JPG
find . -name '*.png' -exec convert {} {}.jpg \;
```

**尽管 `find` 用途广泛，它的语法却比较难以记忆**。例如，为了查找满足模式 `PATTERN` 的文件，您需要执行 `find -name '*PATTERN*'` (如果您希望模式匹配时是不区分大小写，可以使用 `-iname` 选项）

您当然可以使用 alias 设置别名来简化上述操作，但 shell 的哲学之一便是寻找（更好用的）替代方案。 记住，shell 最好的特性就是您只是在调用程序，因此您只要找到合适的替代程序即可（甚至自己编写）。

例如，[`fd`](https://github.com/sharkdp/fd) 就是一个更简单、更快速、更友好的程序，它可以用来作为 `find` 的替代品。它有很多不错的默认设置，例如输出着色、默认支持正则匹配、支持 unicode 并且我认为它的语法更符合直觉。以模式 `PATTERN` 搜索的语法是 `fd PATTERN`。

大多数人都认为 `find` 和 `fd` 已经很好用了，但是有的人可能想知道，我们是不是可以有更高效的方法，例如不要每次都搜索文件而是通过编译索引或建立数据库的方式来实现更加快速地搜索。

这就要靠 [`locate`](https://man7.org/linux/man-pages/man1/locate.1.html) 了。 `locate` 使用一个由 [`updatedb`](https://man7.org/linux/man-pages/man1/updatedb.1.html) 负责更新的数据库，在大多数系统中 `updatedb` 都会通过 [`cron`](https://man7.org/linux/man-pages/man8/cron.8.html) 每日更新。这便需要我们在速度和时效性之间作出权衡。而且，`find` 和类似的工具可以通过别的属性比如文件大小、修改时间或是权限来查找文件，`locate` 则只能通过文件名。 [这里](https://unix.stackexchange.com/questions/60205/locate-vs-find-usage-pros-and-cons-of-each-other) 有一个更详细的对比。





### 查找代码：`grep...`

查找文件是很有用的技能，但是很多时候您的目标其实是查看文件的内容。一个最常见的场景是您希望查找具有某种模式的全部文件，并找它们的位置。

为了实现这一点，很多类 UNIX 的系统都提供了 [`grep`](https://man7.org/linux/man-pages/man1/grep.1.html) 命令，它是用于对输入文本进行匹配的通用工具。它是一个非常重要的 shell 工具，我们会在后续的数据清理课程中深入的探讨它。

`grep` 有很多选项，这也使它成为一个非常全能的工具。

- 其中我经常使用的有 `-C` ：获取查找结果的上下文（Context）；
- `-v` 将对结果进行反选（Invert），也就是输出不匹配的结果。举例来说， `grep -C 5` 会输出匹配结果前后五行。
- 当需要搜索大量文件的时候，使用 `-R` 会递归地进入子目录并搜索所有的文本文件。
- `-n` 显示行号



一些替代品：[ack](https://beyondgrep.com/), [ag](https://github.com/ggreer/the_silver_searcher) 和 [rg](https://github.com/BurntSushi/ripgrep)。它们都特别好用，但是功能也都差不多，我比较常用的是 ripgrep (`rg`) ，因为它速度快，而且用法非常符合直觉。例子如下：

```
# 查找所有使用了 requests 库的文件
rg -t py 'import requests'
# 查找所有没有写 shebang 的文件（包含隐藏文件）
rg -u --files-without-match "^#!"
# 查找所有的foo字符串，并打印其之后的5行
rg foo -A 5
# 打印匹配的统计信息（匹配的行和文件的数量）
rg --stats PATTERN
```

与 `find`/`fd` 一样，重要的是你要知道有些问题使用合适的工具就会迎刃而解，而具体选择哪个工具则不是那么重要。

