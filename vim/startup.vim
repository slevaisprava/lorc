function! Term_Exit(job, ec)
	py3 startup.pr1()
endfunction	

function! Term_Start()
	rightbelow call term_start( "csound -m0d -odac --orc /dev/shm/sample.orc", { "vertical": 0, "term_name": "csound_terminal", "exit_cb": "Term_Exit" })
	tmap <silent><buffer> <M-j> <c-w>:bw!<cr>
	map  <silent><buffer> <M-j> :bw!<cr>
endfunction

nmap <silent> <M-j> :silent py3 startup.pr()<cr>
nmap <silent> <M-r> :py3 startup.reload_modules()<cr>
