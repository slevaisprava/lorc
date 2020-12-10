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

def line(values, times, curves):
    values = np.array(values, dtype=np.float)
    times = np.array(times, dtype=np.int32)
    curves = np.array(curves, dtype=np.float)
    return my_module.line_line(values, times, curves)

#t1 = time.time()
#a = line_curve([0, 12,0], [1000000], [5])
#print(time.time()-t1)

t1 = time.time()
b = line([0, 12, 0], [1000000], [5])
print(time.time()-t1, np.max(b))

plt.plot(b)
plt.show()
#
