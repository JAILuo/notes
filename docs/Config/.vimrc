"" vim: ft=vim :
" =============> plugin install <============= "
call plug#begin('~/.vim/plugged')

Plug 'vim-airline/vim-airline'
Plug 'neoclide/coc.nvim', {'branch': 'release'}

Plug 'git://github.com/junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'git://github.com/junegunn/fzf.vim'

Plug 'git://github.com/Shougo/defx.nvim.git'
Plug 'git://github.com/roxma/nvim-yarp.git'
Plug 'git://github.com/roxma/vim-hug-neovim-rpc.git'
Plug 'git://github.com/kristijanhusak/defx-icons.git'
Plug 'git://github.com/esukram/vim-taglist'

Plug 'vhda/verilog_systemverilog.vim'
Plug 'rust-lang/rust.vim'

call plug#end()


" =============> theme config <============= "
packadd! dracula
syntax enable
colorscheme dracula

"" The "syntax on" command have to be before the "highlight ..." commands to make highlight working.
"" For more information, see :highlight and :syntax
syntax on

highlight Error NONE
highlight Comment cterm=italic guifg=#808080
"highlight Statement cterm=bold
"highlight String cterm=underline


" =============> File type-specific config <============= "
"" TODO: cinoptions
au FileType c,cpp       setlocal expandtab shiftwidth=4 softtabstop=4 tabstop=4 cinoptions=:0,g0,(0,w1
au FileType json        setlocal expandtab shiftwidth=2 softtabstop=2
au FileType vim         setlocal expandtab shiftwidth=2 softtabstop=2


" =============> Shortcut mappings <============= "
nnoremap <space>b :buffers<cr>:b<space>
nnoremap <space>B :buffers<cr>:b<space>
nnoremap <space>e :b#<cr>
nnoremap <space>E :b#<cr>
nnoremap <space>w :w<cr>
nnoremap <space>W :w<cr>
nnoremap <space>q :qa<cr>
nnoremap <space>Q :qa<cr>
nnoremap ZZ zz
inoremap jf <esc>
inoremap JF <esc>


" =============> basic config <============= "
set nocompatible
set encoding=utf-8
set nosmartindent autoindent cindent
set shiftwidth=4 softtabstop=4 tabstop=4
set laststatus=2 ruler title showmode cmdheight=1
set belloff=all noerrorbells novisualbell
set modeline modelines=6
set number
set nowrap
set incsearch hlsearch
set cursorline
setlocal noswapfile
set bufhidden=hide
set magic

" more complex plugin config
source ~/.vim-plugin-config


" =============> TODO <============= "
" 分屏跳转 ctrl + w + ... --> alt + w + ...

"" "jumpoptions=stack" is not supported in old Vim. (older than Vim 9.0.1921)
"set jumpoptions=stack
