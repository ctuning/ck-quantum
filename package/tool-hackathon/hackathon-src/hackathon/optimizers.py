from scipy.optimize import minimize
import random
import numpy as np

def my_nelder_mead( func, x0, my_args=(), my_options=None ):    # a non-stochastic minimizer for comparison

    return minimize( func, x0, method='Nelder-Mead', options=my_options, args=my_args )


def my_cobyla( func, x0, my_args=(), my_options=None ):         # another non-stochastic minimizer for comparison

    return minimize( func, x0, method='COBYLA', options=my_options, args=my_args )


def my_minimizer( func, x0, my_args=(), my_options=None ):      # your own take!
	# Simple optimiser: samples randomly and returns the minimum
	num_parameters = len(x0)                                        # get number of parameters needed for objective function
	points = 10                                                 	# evaluate the objective function at 10 points
	flist = []
	xlist = []
	for i in range(points):
		x = [random.random() for i in range(num_parameters)]    # initialise parameters randomly from uniform distribution
		fnew = func(x, my_args)
		flist.append(fnew)
		xlist.append(x)
	minidx = np.argmin(flist)
	best_x = xlist[minidx]
	fmin = flist[minidx]
	minimizer_output = { 'fun' : fmin, 'nfev' : points, 'nit' : points, 'x' : best_x }

	return minimizer_output



