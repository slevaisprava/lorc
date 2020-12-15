import time
import gc
import numpy as np
import matplotlib.pyplot as plt
import my_module


def env(values, times, curves):
    values = np.array(values, dtype=np.float)
    times = np.array(times, dtype=np.int32)
    curves = np.array(curves, dtype=np.float)
    return my_module.env(values, times, curves)

def cycle_env1(values, times, curves):
    values = np.array(values, dtype=np.float)
    times = np.array(times, dtype=np.int32)
    curves = np.array(curves, dtype=np.float)
    return my_module.cycle_env(values, times, curves)

#t1 = time.time()
#a = line_curve([0, 12,0], [1000000], [5])
#print(time.time()-t1)

t1 = time.time()
b = cycle_env1([5, 12, 0]*5, [1000], [5,5]*6)
#print(time.time()-t1, np.max(b))

plt.plot(b)
plt.show()
gc.collect()
#
