v = '''
	kindex_v{0}, kstart_v{0}, kstrum_v{0}	init 0
	kp2_v{0},  kcnt_v{0}, ktempo_v{0} init 1
	if metro:k(divz(ktempo_v{0}, abs(kp2_v{0}), 0)) == 1 then
		if kp2_v{0} < 0 kgoto Pause_v{0}
                ktime_v{0} = timeinsts:k()/p3
{1}
		kdx_v{0} = 0
		while kdx_v{0} < kcnt_v{0} do
		        ktime_v{0} += kstart_v{0}/p3
{2}
		        event "i", {3}, kstart_v{0}, {4}
			kstart_v{0} += kstrum_v{0}
			kdx_v{0} += 1
		od
		kstart_v{0} = 0
		kindex_v{0} += 1
		Pause_v{0}:
	endif
'''

e = '''
	kindex_v{0}, kstart_v{0}, kstrum_v{0}	init 0
	kp2_v{0},  kcnt_v{0}, ktempo_v{0} init 1
	if metro:k(divz(ktempo_v{0}, abs(kp2_v{0}), 0)) == 1 then
		if kp2_v{0} < 0 kgoto Pause_v{0}
                ktime_v{0} = timeinsts:k()/p3
{1}
		kdx_v{0} = 0
		while kdx_v{0} < kcnt_v{0} do
		        ktime_v{0} += kstart_v{0}/p3
		        if ktime_v{0} > 1 then
		        	goto VPause_v{0}
		        endif
{2}
		        event "i", {3}, kstart_v{0}, {4}
			kstart_v{0} += kstrum_v{0}
			kdx_v{0} += 1
		od
		VPause_v{0}:
		kstart_v{0} = 0
		kindex_v{0} += 1
		Pause_v{0}:
	endif
'''
