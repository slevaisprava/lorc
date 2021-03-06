function! Term_Exit(job, ec)
	py3 startup.on_csound_close()
	echo
endfunction	

function! Term_Start(cmd)
	rightbelow call term_start(a:cmd , {"vertical": 0, "term_name": "csound_terminal", "exit_cb": "Term_Exit"})
	tmap <silent><buffer> <M-x> <c-w>:bw!<cr>
	map  <silent><buffer> <M-x> :bw!<cr>
endfunction

nmap <silent> <M-x> :echo 'WIP...'\|silent py3 startup.start_single_orc()<cr>
nmap <silent> <M-r> :py3 startup.reload_modules()<cr>
