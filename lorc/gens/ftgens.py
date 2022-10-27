import numpy as np
from numba import njit
from numba.pycc import CC

cc = CC("gen_functions")


@cc.export("env", "f8[:](f8[:], i4[:], f8[:])")
def env(values, times, curves):
    times = _justify_arrays(values, times)
    curves = _justify_arrays(values, curves)

    res_size = np.sum(times) - (times.size-1)
    res = np.empty(res_size)
    i = 0
    k = 0
    for time in times:
        res[k] = values[i]
        mn = values[i]
        mx = values[i+1]
        curve = curves[i]
        i += 1
        k += 1
        time -= 1
        for j in range(1, time):
            res[k] = j*(mx - mn)/time + mn
            res[k] = make_curves2(res[k], mn, mx, curve)
            k += 1
    res[res_size-1] = values[-1]
    return res


@njit
def make_curves2(val, mn, mx, curve):
    if mn != mx:
        grow = np.exp(curve)
        a = (mx - mn)/(1.0 - grow)
        b = mn + a
        val = b - (a * np.power(grow, (val - mn)/(mx - mn)))
    return val


@njit
def _justify_arrays(first, second):
    """ Изменяет длину второго массива (second) так, чтобы она стала 
        на единицу меньше первого. Первый массив (first) не изменяется.
    """
    if first.size - second.size < 1:
        second = second[:first.size-1]
    while first.size - second.size != 1:
        second = np.append(second, second[-1])
    return second


if __name__ == "__main__":
    cc.verbose = True
    cc.compile()
