function! Term_Exit(job, ec)
	py3 startup.on_csound_close()
endfunction	

function! Term_Start(cmd)
	rightbelow call term_start(a:cmd , {"vertical": 0, "term_name": "csound_terminal", "exit_cb": "Term_Exit"})
	tmap <silent><buffer> <M-j> <c-w>:bw!<cr>
	map  <silent><buffer> <M-j> :bw!<cr>
endfunction

nmap <silent> <M-j> :py3 startup.start_single_orc()<cr>
nmap <silent> <M-r> :py3 startup.reload_modules()<cr>
