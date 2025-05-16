import math


def _condition_if(condition, if_true, if_false):
    return if_true if condition else if_false

def _func_round(num: int | float):
    return round(num)

_func_min = min

_func_max = max

_func_abs = abs

_func_sqrt = math.sqrt

_func_ceil = math.ceil

CONTEXT  = {
    'MIN': _func_min,
    'MAX': _func_max,
    'ROUND': _func_round,
    'ABS': _func_abs,
    'IF': _condition_if,
    'SQRT': _func_sqrt,
    'CEIL': _func_ceil
}
