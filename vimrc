set nocompatible

if has('win32')
    source $VIMRUNTIME/vimrc_example.vim
    source $VIMRUNTIME/mswin.vim
    behave mswin

    map ,t :tabnew <C-R>=expand("%:p:h") . "\\" <CR>
    map ,e :e <C-R>=expand("%:p:h") . "\\" <CR>
elseif has("unix")
    map ,t :tabnew <C-R>=expand("%:p:h") . "/" <CR>
    map ,e :e <C-R>=expand("%:p:h") . "/" <CR>
endif

if &t_Co > 2 || has("gui_running")
    syntax on
    set hlsearch
    set guioptions-=T
    set isk+=-,?,_
endif

set spell
map ,t :tabnew <C-R>=expand("%:p:h") . "/" <CR>
map ,e :e <C-R>=expand("%:p:h") . "/" <CR>

set fileformats=unix,dos,mac

set backspace=indent,eol,start

set nobackup
set writebackup

" search related settings
set history=100
set ignorecase
set smartcase
set wrapscan
set noincsearch

" display related settings
set title
set showcmd
set laststatus=2
set showmatch
set matchtime=2
set wildmenu
set wrap
set number

highlight LineNr ctermfg=darkyellow    
highlight NonText ctermfg=darkgrey
highlight Folded ctermfg=blue
highlight SpecialKey cterm=underline ctermfg=darkgrey
"highlight SpecialKey ctermfg=grey " 

set smartindent
set autoindent
set scrolloff=5

"colorscheme murphy

" complete type
set wildmode=longest,full

set statusline=[%L]\ %t\ %y%{'['.(&fenc!=''?&fenc:&enc).':'.&ff.']'}%r%m%=%c:%l/%L

set guioptions-=T
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" change window size
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <C-SPACE> :simalt ~x<CR>
map <A-SPACE> :simalt ~r<CR>

if has("autocmd")
    filetype plugin indent on
    autocmd BufEnter * lcd %:p:h "convert to current directory
endif

" Language Settings
set fileencodings=utf-8

"=======Tips=======
"   Edit another file in the same directory as the current file
"   uses expression to extract path from current file's path
"  (thanks Douglas Potts)
if has("unix")

else
endif

set guitablabel=%{tabpagenr()}.%t\ %m

" tab settings
set ts=4 sw=4
set softtabstop=4
set shiftwidth=4
set expandtab

language messages en
set iminsert=0
set imsearch=0

" source code style
set cino +=(0,W4
set cino +=:0

function LocalDiff2Depot()
    on
    diffthis
    !p4 print -o %.depot %
    vs
    e %.depot
    diffthis
endfunction

map ,d :call LocalDiff2Depot() <CR>

function LocalDiffToSVN()
    diffthis
    !svn cat % > %.head
    vs
    e %.head
    diffthis
endfunction

map ,s :call LocalDiffToSVN()<cr>

function LocalDiffToGIT()
    diffthis
    !python <folder>/ji.py cat % %.head 
    vs
    e %.head
    diffthis
endfunction

function LocalChangeList()
    !python <folder>/ji.py changelist > changelist.tmp
    e changelist.tmp
endfunction

map ,g :call LocalDiffToGIT()<cr>
map ,l :call LocalChangeList()<cr>


" quickfix settings, use cwindow to show the search result
" use h csqf to check the help
set cscopequickfix=s-,g-,d-,c-,t-,e-,f-,i-
