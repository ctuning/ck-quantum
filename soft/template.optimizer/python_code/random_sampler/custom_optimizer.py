import random
import numpy as np


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
