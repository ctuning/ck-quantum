from scipy.optimize import minimize
import random
import numpy as np

def my_nelder_mead( func, x0, my_args=(), my_options=None ):    # a non-stochastic minimizer for comparison
    "Nelder-Mead optimizer from SciPy library"

    return minimize( func, x0, method='Nelder-Mead', options=my_options, args=my_args )


def my_cobyla( func, x0, my_args=(), my_options=None ):         # another non-stochastic minimizer for comparison
    "COBYLA optimizer from SciPy library"

    return minimize( func, x0, method='COBYLA', options=my_options, args=my_args )


def my_random_sampler( func, x0, my_args=(), my_options=None ):
    "Simple optimiser: samples randomly and returns the minimum - used here as an example"

    my_options      = my_options or {}
    points          = my_options.get('maxfev', 30)              # by default perform 30 function evaluations
    num_parameters  = len(x0)                                   # get number of parameters needed for objective function

    flist = []
    xlist = []
    for i in range(points):
        x = [random.random() for i in range(num_parameters)]    # initialise parameters randomly from uniform distribution
        fnew = func(x, my_args)
        flist.append(fnew)
        xlist.append(x)

    min_idx = np.argmin(flist)
    best_x  = xlist[min_idx]
    fmin    = flist[min_idx]

    minimizer_output = { 'fun' : fmin, 'nfev' : points, 'nit' : points, 'x' : best_x }

    return minimizer_output


def my_minimizer( func, x0, my_args=(), my_options=None ):
    "Your own attempt at writing a stochastic minimizer"

    current_func_value = func(x0, my_args)

    minimizer_output = { 'fun' : current_func_value, 'nfev' : 1, 'nit' : 1, 'x' : x0 }

    return minimizer_output

