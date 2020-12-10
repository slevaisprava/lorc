import numpy as np
from numba.pycc import CC
from numba import njit
from numba.typed import List


cc = CC('my_module')


@cc.export('line_line', 'f8[:](f8[:], i4[:], f8[:])')
def line_line(values, times, curves):
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
        b = mn + a;
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

#@cc.export('line_curve', 'f8[:](f8[:], i4[:], f8[:])')
#def line_curve(values, times, curves):
#    times = _justify_arrays(values, times)
#    curves = _justify_arrays(values, curves)
#    table = List()
#    i = 0
#    for time in times:
#        arr = np.linspace(values[i], values[i+1], time)
#        if curves[i] != 0:
#            arr = make_curves(arr, curves[i])
#        table.append(arr)
#        i += 1
#    return _flate(table)
#@njit
#def make_curves(arr, curve):
#    mn = np.min(arr)
#    mx = np.max(arr)
#    if mn != mx:
#        grow = np.exp(curve)
#        a = (mx - mn)/(1.0 - grow)
#        b = mn + a;
#        arr = b - (a * np.power(grow, (arr - mn)/(mx - mn)))
#    return arr
#@njit
#def _flate(table):
#    res = np.empty(_calc_res_size(table))
#    i = 0
#    k = 0
#    for arr in table:
#        j = 0
#        for val in arr:
#            if k == 0 or j != 0:
#                res[i] = val
#                i += 1
#            j += 1
#        k += 1
#    return res
#
#
#@njit
#def _calc_res_size(table):
#    res_size = 0
#    for arr in table:
#        res_size += arr.size
#    return res_size - (len(table)-1)


if __name__ == "__main__":
    cc.verbose = True
    cc.compile()
