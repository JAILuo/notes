## 入门使用

[linux - Tmux的超绝便利 （基础篇） - Solomon's 技术专栏](https://segmentfault.com/a/1190000018032072)

[终端神器tmux：多任务管理大师](https://www.bilibili.com/video/BV1ML411h7tF/?spm_id_from=333.788.recommend_more_video.0&vd_source=ecc99d78ae961113010161a48a475a35)

[如何在 Tmux 中使用剪贴板进行复制和粘贴 (linux-console.net)](https://cn.linux-console.net/?p=15192)

#### 概念区分

`tmux` 层级顺序：server > session > window > pane

- Server：是整个 `tmux` 的后台服务。有时候更改配置不生效，就要使用 `tmux kill-server` 来重启 `tmux`。
- Session：是 `tmux` 的所有会话。我之前就错把这个session当成窗口用，造成了很多不便。一般只要保存**一个**session就足够了。
- Window：相当于一个工作区，包含很多分屏，可以针对每种任务分一个Window。如下载一个Window，编程一个window。
- Pane：是在Window里面的小分屏。最常用也最好用。

> 这里可以理解为 server 就是一个后台进程；session 就是平常用的一个终端 `ctrl + alt + t`；window 就相当于在终端里按 `ctrl + shift` 生成的一个新的窗口，pane 就能在 window 中分好几个小屏。

#### 基本操作

- **常用外部命令**

    ```bash
    #启动新session：
    $ tmux [new -s 会话名 -n 窗口名]
    
    #恢复session：
    $ tmux at [-t 会话名]
    
    #列出所有sessions：
    $ tmux ls
    
    #关闭session：
    $ tmux kill-session -t 会话名
    
    #关闭整个tmux服务器：
    $ tmux kill-server
    
    ```

- **`tmux` 常用内部命令**

    > 所谓 **内部命令**，就是进入 `tmux` 后，并按下 **前缀键** 后的命令，一般前缀键为`Ctrl+b`。

    - other
        - 刷新配置文件：`<前缀键>r`
        - 下载和更新Plugins：`<前缀键>I`

    - Session 会话:
        - **启动新会话: `<前缀键>:new<回车>`**
        - 列出所有会话: `<前缀键>s`
        - 重命名当前会话: `<前缀键>$`
    - Window 窗体：
        - **关闭当前Window: `<前缀键>&`**
        - **创建新Window: `<前缀键>c`**
        - 列出所有Windows: `<前缀键>w`
        - 后一个Window: `<前缀键>n`
        - 前一个Window: `<前缀键>p`
        - 重命名当前Window: `<前缀键>,`
        - 修改当前Window位置（序号）：`.`
    - Pane 小面板：
        - **关闭当前Pane: `<前缀键>x`**
        - **左右分割Pane: `<前缀键>%`**
        - **上下分割Pane: `<前缀键>"`**
        - 最大化/最小化 Pane: `<前缀键>z`
        - 显示每个Pane的编号，可以按下数字键选中Pane: `<前缀键>q`
        - 与上一个窗格交换位置: `<前缀键>{`
        - 与下一个窗格交换位置: `<前缀键>}`





## 个人配置: `~/tmux.conf`

目前只有一部分

```bash
bind-key c new-window -c "#{pane_current_path}"
bind-key % split-window -h -c "#{pane_current_path}"
bind-key '"' split-window -c "#{pane_current_path}"

# 配色
set -g default-terminal "xterm-256color"

# 前缀键 ctrl+b 重定向到 ctrl+]
unbind C-b
set-option -g prefix C-]
bind C-] send-prefix

# 启用鼠标(Tmux v2.1)
set -g mouse on

```







## Bugs

#### vim 配色和 tmux 中不一致

当你在使用 `tmux` 时遇到 Vim 配色问题，这通常是因为 `tmux` 和 Vim 之间的颜色设置不匹配。以下是一些可能的解决方案：

1. **确保 `TERM` 环境变量一致**：无论是在 `tmux` 内还是 `tmux` 外，都应该使用相同的 `TERM` 值，如 `xterm-256color`。你可以在 `~/.bashrc` 或 `~/.zshrc` 中设置 `export TERM="xterm-256color"`，然后在 `.tmux.conf` 中设置 `set -g default-terminal "xterm-256color"`。（**==解决==**）

2. **开启 TrueColor 支持**：如果你的终端模拟器支持 TrueColor（24-bit color），确保 `tmux` 和 Vim 都开启了 TrueColor 支持。在 `.tmux.conf` 中添加以下配置：
   
   ```sh
   set-option -ga terminal-overrides ",*256col*:Tc"
   ```
   在 `.vimrc` 中添加：
   ```vim
   if has("termguicolors")
   set termguicolors
   endif
   ```
   这将允许 Vim 使用真彩色。
   
3. **使用 `tmux` 的 `-2` 选项**：这个选项强制 `tmux` 假设终端支持 256 种颜色。你可以在 `.bashrc` 或 `.zshrc` 中添加别名 `alias tmux='tmux -2'` 来实现这一点。

4. **检查 `.vimrc` 配置**：确保 `.vimrc` 文件中包含了正确的颜色设置，例如设置 `set t_Co=256` 来启用 256 色模式。

5. **更新 `tmux` 和 Vim**：如果你的 `tmux` 或 Vim 版本过旧，可能不支持某些颜色特性。确保两者都是最新版本。

6. **使用 `tmux` 插件**：有些插件，如 `tmux-colors-solarized`，可以帮助解决颜色问题。

7. **验证终端和 `tmux` 的版本**：确保你的终端模拟器和 `tmux` 都支持所需的颜色特性，并且版本兼容。

8. **使用脚本测试颜色支持**：使用如 `24-bit-color.sh` 脚本来测试你的终端是否支持 TrueColor。

如果上述方法仍然不能解决你的问题，可能需要进一步检查你的具体配置或考虑在 `tmux` 社区寻求帮助。