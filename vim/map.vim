function! TermHandler(job, ec)
	if a:ec == 0
		call Close_csound_term()
	endif	
endfunction	
function! Close_csound_term()
	if bufname() == "csound_terminal"
		bw!
	endif
endfunction	

function! Start_csound_term()
	w!
	rightbelow call term_start("./vim/csound.sh", {"vertical":0, "term_name":"csound_terminal", "exit_cb": "TermHandler"})
	map <silent><buffer><C-s> :call Close_csound_term()<cr> 
	map <silent><buffer><Esc> :call Close_csound_term()<cr> 
	tnoremap <silent><buffer><Esc> <C-W>:bw!<cr>
endfunction

map <buffer><silent><M-s> :call Start_csound_term()<cr>
imap <silent><buffer><M-s> <Esc>:call Start_csound_term()<cr>

map <M-g> :silent exec "!tig --all" \| redraw!<cr>
