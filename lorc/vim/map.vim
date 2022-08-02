function! Start_Csound_Term()
	w!
	rightbelow call term_start("./vim/csound.sh", {"vertical":0, "term_name":"csound_terminal"})
	tnoremap <silent><buffer><Esc> <C-W>:bw!<cr>
	noremap <silent><buffer><Esc> :bw!<cr> 
	tnoremap <silent><buffer>j <C-W>:bw!<cr>
	noremap <silent><buffer>j :bw!<cr> 
endfunction


map <buffer><silent><M-s> :call Start_Csound_Term()<cr>
map <silent><M-g> :silent exec "!tig --all" \| redraw!<cr>
