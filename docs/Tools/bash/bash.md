执行命令

- 命令从哪里来？

    ```bash
    echo $PATH
    find here
    
    which gcc
    ```





$?：上一个命令执行的结果



输入重定向

- <

- here documents

    grep test<<EOFF

    > 最终输入EOFF，就会退出。



输出重定向

- `>`

- `>|`

    防止 `set -c` 的不允许覆写。

- `>>`

    追加到结尾





管道

命名管道（mkfifo）、匿名管道（|，多个程序组合）

比如：网站访问log：格式：IP--data--url--协议--port

找出访问数量排名前十的IP

```bash
cat xx.log | cut -d'' -f1 | sort | uniq -c | sort -n | head -n 10
```





文本处理

正则表达式

a[0-9]? 

a[0-9]*

a[0-9]+

a[0-9]{2,#3}

a[0-9]{3,}



优先级：重复>连接>或

通过加括号可以该优先级，实际上就是捕获组。



比如：Linux 内核找到read 系统调用实现：

`SYSCALL_.*\(read`



grep 常用选项：

控制匹配：

```
-i -v -x
```

- -i：忽略大小写
- -v：打印不匹配指定模式的行
- -x：打印和模式完全匹配的行





```
-o -n -c -A -q
```

- -o：

- -n：打印行号

- -c：

- -A：打印匹配的行和后几行（通过参数控制后几行）

    ```bash
    grep -e 'example' -A2 -n sample.txt
    ```

- -q

    不进行任何输出，只是看匹配是否成功，匹配成功，$?为0

    ```
    grep -e 'example' -A2 -n -q sample.txt
    echo $?
    0
    
    grep -e 'no' -A2 -n sample.txt
    echo $?
    1
    ```

    





sed：流编辑器。格式：[addr]X[options]

这个名字和工作原理比较相关，逐行地读取输入文件的内容。

常用命令：

- append
- change
- insert
- delete
- replace



例子：

删除文件的第一行到第三行：（delete命令）

```bash
sed -e '1,3d' demo_sed.txt
```

将第一行的first替换成大写的：（replace）

```bash
sed -e '1s/first/FIRST/g' demo_sed.txt
```

修改第一行的内容：（change）

```bash
sed -e '1c\line one' demo_sed.txt
```

append、insert 插入，是在行首、行尾插入。



还有一些别的选项：-n、-i

因为sed默认不会对原程序进行修改，要修改原文件的，用 `-i`。

-n：禁用打印全部行的行为

```bash
sed -e '1,3p' demo_sed.txt
```











awk：强大的文本处理工具，另一种编程语言。













