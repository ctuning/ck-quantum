import random
import numpy as np


def my_minimizer( func, x0, my_args=(), my_options=None ):
    "Your own attempt at writing a stochastic minimizer"

    current_func_value = func(x0, my_args)

    minimizer_output = { 'fun' : current_func_value, 'nfev' : 1, 'nit' : 1, 'x' : x0 }

    return minimizer_output

