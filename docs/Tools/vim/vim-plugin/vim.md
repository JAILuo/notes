## 插件

[🦄 vim-plug 的安装和使用 - 前端和Node学习笔记 - SegmentFault 思否](https://segmentfault.com/a/1190000018089782)

[Vim Awesome](https://vimawesome.com/)

[vim插件快速安装](https://www.subingwen.cn/linux/vimplus/)

[NeoVim coc.nvim enter key doesn't work to autocomplete - Super User](https://superuser.com/questions/1734914/neovim-coc-nvim-enter-key-doesnt-work-to-autocomplete)

[使用clangd为vim配置代码补全](https://www.bilibili.com/video/BV16B4y187n1/?spm_id_from=333.337.search-card.all.click&vd_source=ecc99d78ae961113010161a48a475a35)

[Language servers · neoclide/coc.nvim Wiki (github.com)](https://github.com/neoclide/coc.nvim/wiki/Language-servers#ccobjective-c)

[neoclide/coc.nvim: Nodejs extension host for vim & neovim, load extensions like VSCode and host language servers. (github.com)](https://github.com/neoclide/coc.nvim)







## 关于网络被墙

### GitHub镜像站的了解

[VIM-Plug安装插件时，频繁更新失败，或报端口443被拒绝等_vimplug国内镜像-CSDN博客](https://blog.csdn.net/htx1020/article/details/114364510) 

> 改用镜像站

[GitHub镜像 - 最优网址 | 镜像站汇总 (sockstack.cn)](https://www.sockstack.cn/github)







## defx

```bash
" =============> defx 配置 <============= "
" the defx
" Define mappings
"cnoreabbrev sf Defx -listed -new
"      \ -columns=indent:mark:icon:icons:filename:git:size
"      \ -buffer-name=tab`tabpagenr()`<CR>
nnoremap <silent>sf :<C-u>Defx -listed -resume
      \ -columns=indent:mark:icon:icons:filename:git:size
      \ -buffer-name=tab`tabpagenr()`
      \ `expand('%:p:h')` -search=`expand('%:p')`<CR>
nnoremap <silent>fi :<C-u>Defx -new `expand('%:p:h')` -search=`expand('%:p')`<CR>

autocmd FileType defx call s:defx_my_settings()
	function! s:defx_my_settings() abort
	  " Define mappings
	  nnoremap <silent><buffer><expr> <CR>
	  \ defx#do_action('open')
	  nnoremap <silent><buffer><expr> yy
	  \ defx#do_action('copy')
	  nnoremap <silent><buffer><expr> dd
	  \ defx#do_action('move')
	  nnoremap <silent><buffer><expr> pp
	  \ defx#do_action('paste')
	  nnoremap <silent><buffer><expr> l
	  \ defx#do_action('open')
	  nnoremap <silent><buffer><expr> <Right>
	  \ defx#do_action('open')
	  nnoremap <silent><buffer><expr> E
	  \ defx#do_action('open', 'vsplit')
	  nnoremap <silent><buffer><expr> n
	  \ defx#do_action('open', 'pedit')
	  nnoremap <silent><buffer><expr> i
	  \ defx#do_action('open', 'choose')
	  nnoremap <silent><buffer><expr> o
	  \ defx#do_action('open_or_close_tree')
	  nnoremap <silent><buffer><expr> K
	  \ defx#do_action('new_directory')
	  nnoremap <silent><buffer><expr> N
	  \ defx#do_action('new_file')
	  nnoremap <silent><buffer><expr> M
	  \ defx#do_action('new_multiple_files')
	  nnoremap <silent><buffer><expr> C
	  \ defx#do_action('toggle_columns',
	  \                'mark:indent:icon:filename:type:size:time')
	  nnoremap <silent><buffer><expr> S
	  \ defx#do_action('toggle_sort', 'time')
	  nnoremap <silent><buffer><expr> dD
	  \ defx#do_action('remove')
	  nnoremap <silent><buffer><expr> a
	  \ defx#do_action('rename')
	  nnoremap <silent><buffer><expr> !
	  \ defx#do_action('execute_command')
	  nnoremap <silent><buffer><expr> x
	  \ defx#do_action('execute_system')
	  nnoremap <silent><buffer><expr> YY
	  \ defx#do_action('yank_path')
	  nnoremap <silent><buffer><expr> .
	  \ defx#do_action('toggle_ignored_files')
	  nnoremap <silent><buffer><expr> ;
	  \ defx#do_action('repeat')
	  nnoremap <silent><buffer><expr> h
	  \ defx#do_action('cd', ['..'])
	  nnoremap <silent><buffer><expr> <Left>
	  \ defx#do_action('cd', ['..'])
	  nnoremap <silent><buffer><expr> ~
	  \ defx#do_action('cd')
	  nnoremap <silent><buffer><expr> q
	  \ defx#do_action('quit')
	  nnoremap <silent><buffer><expr> <Space>
	  \ defx#do_action('toggle_select') . 'j'
	  nnoremap <silent><buffer><expr> m
	  \ defx#do_action('toggle_select') . 'j'
	  nnoremap <silent><buffer><expr> vv
	  \ defx#do_action('toggle_select_all')
	  nnoremap <silent><buffer><expr> *
	  \ defx#do_action('toggle_select_all')
	  nnoremap <silent><buffer><expr> j
	  \ line('.') == line('$') ? 'gg' : 'j'
	  nnoremap <silent><buffer><expr> k
	  \ line('.') == 1 ? 'G' : 'k'
	  nnoremap <silent><buffer><expr> <C-l>
	  \ defx#do_action('redraw')
	  nnoremap <silent><buffer><expr> <C-g>
	  \ defx#do_action('print')
	  nnoremap <silent><buffer><expr> cd
	  \ defx#do_action('change_vim_cwd')
	endfunction

call defx#custom#column('icon', {
      \ 'directory_icon': '▸',
      \ 'opened_icon': '▾',
      \ 'root_icon': ' ',
      \ })
call defx#custom#column('git', 'indicators', {
  \ 'Modified'  : 'M',
  \ 'Staged'    : '✚',
  \ 'Untracked' : '✭',
  \ 'Renamed'   : '➜',
  \ 'Unmerged'  : '═',
  \ 'Ignored'   : '☒',
  \ 'Deleted'   : '✖',
  \ 'Unknown'   : '?'
  \ })

```

这段代码是 Vim 编辑器中 `defx` 插件的配置。`defx` 是一个文件浏览器插件，它提供了一个侧边栏来浏览文件和目录。下面是对这段配置的总结：

1. **定义快捷键**:
   - `sf` 和 `fi` 是两个快捷键，用于在 Vim 中打开 `defx` 窗口。`sf` 用于列出当前目录下的文件，`fi` 用于在当前目录下新建一个 `defx` 窗口。

2. **自定义 `defx` 窗口**:
   - 当文件类型为 `defx` 时，自动调用 `s:defx_my_settings` 函数来设置一些自定义的快捷键。

3. **快捷键映射**:
   - 映射了多个快捷键到 `defx` 的动作，例如：
     - `<CR>`（回车键）：打开选中的文件或目录。
     - `yy`：复制选中的文件或目录。
     - `dd`：移动选中的文件或目录。
     - `pp`：粘贴文件或目录。
     - `l` 或 `<Right>`：以水平分割的方式打开选中的文件。
     - `E`：以垂直分割的方式打开选中的文件。
     - `n`：以新标签页的方式打开选中的文件。
     - `i`：选择文件或目录进行操作。
     - `o`：打开或关闭目录树。
     - `K`：新建目录。
     - `N`：新建文件。
     - `M`：新建多个文件。
     - `C`：切换列的显示。
     - `S`：根据时间排序。
     - `dD`：删除文件或目录。
     - `a`：重命名选中的文件或目录。
     - `!`：执行命令。
     - `x`：执行系统命令。
     - `YY`：复制文件路径。
     - `.`：切换忽略文件的显示。
     - `;`：重复上一次操作。
     - `h` 或 `<Left>`：返回上一级目录。
     - `~`：切换到用户主目录。
     - `q`：退出 `defx`。
     - `<Space>` 或 `m`：切换选中状态。
     - `vv` 或 `*`：选中或取消选中所有文件。
     - `j` 和 `k`：在 `defx` 窗口中上下移动。
     - `<C-l>`：刷新 `defx` 窗口。
     - `<C-g>`：打印当前选中的文件或目录信息。
     - `cd`：更改 Vim 的当前工作目录。

4. **自定义列显示**:
   - 定义了 `icon` 列的图标，以及 `git` 列的状态指示符。

5. **自定义 Git 状态图标**:
   - 为不同的 Git 状态定义了不同的图标，例如：
     - Modified（已修改）：`M`
     - Staged（已暂存）：`✚`
     - Untracked（未跟踪）：`✭`
     - Renamed（已重命名）：`➜`
     - Unmerged（未合并）：`═`
     - Ignored（已忽略）：`☒`
     - Deleted（已删除）：`✖`
     - Unknown（未知）：`?`





## Universal Ctags

### 简介

`ctags` 是一个用于生成源代码标签的工具，可以帮助程序员在代码中快速定位函数、变量、结构体等定义的位置。以下是 `ctags` 的基本用法：

1. **生成标签文件**：
   在代码目录下执行以下命令生成标签文件：
   
   ```bash
   ctags -R .
   ```
   这将在当前目录及其子目录中生成一个名为 `tags` 的标签文件。
   
2. **在编辑器中使用**：
   - **Vim**：在 Vim 中使用标签，可以通过 `Ctrl+]` 快捷键跳转到定义，`Ctrl+t` 返回上一次跳转的位置。
   - **Emacs**：在 Emacs 中使用标签，可以使用 `M-.` 跳转到定义，`M-*` 返回上一次跳转的位置。

3. **其他用法**：
   
   - 使用 `-f` 参数指定生成的标签文件名：`ctags -R -f mytags .`
   - 使用 `-a` 参数追加标签到现有标签文件：`ctags -R -a .`

### 示例
假设有一个 C 语言项目的目录结构如下：
```
project/
├── src/
│   ├── main.c
│   └── utils.c
└── include/
    ├── utils.h
    └── common.h
```

在 `project` 目录下执行以下命令生成标签文件：
```bash
ctags -R .
```

然后在编辑器中打开 `main.c` 文件，使用快捷键跳转到 `utils.h` 中定义的函数，可以方便地查看函数定义。

























