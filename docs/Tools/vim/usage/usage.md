## Version

基于 Ubuntu22.04 的自带版本 8.2。



## 一次操作多行

**使用可视块模式（Visual Block Mode）**:

- 首先，将光标移动到 int 的 i 字符上。
- 然后按 Ctrl + V 进入可视块模式。
- 使用方向键向下选择多行。
- 当你选择了所有需要添加 typedef 的行后，按 I（大写的 i）进入插入模式。
- 输入 typedef，然后按 Esc（或者按 Ctrl +     o 然后按 a 来移动到行尾）。
- 现在，typedef 应该已经添加到所有选中的行的开头。

比如：

int (*on) (void *self); 

int (*off) (void *self);

int (*get_state) (void *self);

在每一行的开头都要添加 typedef，具体操作如上。

**另外，这也可以快速写注释。**