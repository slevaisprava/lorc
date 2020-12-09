import time
import gc

import numpy as np
import matplotlib.pyplot as plt
import my_module

def line_curve(values, times, curves):
    values = np.array(values, dtype=np.float)
    times = np.array(times, dtype=np.int32)
    curves = np.array(curves, dtype=np.float)
    return my_module.line_curve(values, times, curves)

def line(values, times):
    values = np.array(values, dtype=np.float)
    times = np.array(times, dtype=np.int32)
    return my_module.line_line(values, times)

t1 = time.time()
a = line_curve([0, 12,0]*4, [10], [-5,5]*10)
#a = line([0, 12, 0,0]*2, [10,20,20])

plt.plot(a)
plt.show()

