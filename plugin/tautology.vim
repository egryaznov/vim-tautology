if !has("python3")
    echohl WarningMsg
    echom  "vim-tautology requires the command 'python3' to be available on your system"
    echohl None
    finish
endif

if exists('g:tautology_dir')
    let s:path = get(g:, 'tautology_dir')
else
    let s:path = '~/.vim/plugged/vim-tautology'
endif

if exists('g:tautology_mark')
    let s:stain = get(g:, 'tautology_mark')
    " Avoid using # as a mark, this causes problems.
    if s:stain == '#'
        s:stain = '@'
    endif
else
    let s:stain = '@'
endif

if exists('g:tautology_window_size')
    let s:window = get(g:, 'tautology_window_size')
else
    let s:window = 30
endif

if exists('g:tautology_skip')
    let s:skip = get(g:, 'tautology_skip')
else
    let s:skip = 0
endif

if exists('g:tautology_stop_words')
    let s:stop_words = get(g:, 'tautology_stop_words')
else
    let s:stop_words = ['I', 'the', 'a', 'an', 'to', 'be', 'of', 'and', 'in', 'that', 'this', 'as']
endif

if exists('g:tautology_mappings')
    let s:mappings = get(g:, 'tautology_mappings')
    if s:mappings == 1
        vnoremap gz :TautologyMark<CR>
        vnoremap gZ :TautologyClear<CR>
    endif
endif

function! s:register_commands()
    command! -range -nargs=0 TautologyMark call s:tautology_mark()
    command! -range -nargs=0 TautologyClear call s:tautology_clear()
endfunction

function! s:tautology_clear()
    execute "'<,'>!python3" s:path . "/plugin/tautology.py --undo" "--mark" s:stain
endfunction

function! s:tautology_mark()
    execute "'<,'>!python3" s:path . "/plugin/tautology.py" "--mark" s:stain "--window" string(s:window) "--skip" string(s:skip) "--ban-list" join(s:stop_words, ' ')
endfunction

call s:register_commands()
