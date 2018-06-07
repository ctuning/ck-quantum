from scipy.optimize import minimize


def my_nelder_mead( func, x0, my_args=(), my_options=None ):    # a non-stochastic minimizer for comparison

    return minimize( func, x0, method='Nelder-Mead', options=my_options, args=my_args )


def my_cobyla( func, x0, my_args=(), my_options=None ):         # another non-stochastic minimizer for comparison

    return minimize( func, x0, method='COBYLA', options=my_options, args=my_args )


def my_minimizer( func, x0, my_args=(), my_options=None ):      # your own take!

    # Currently it does not optimize anything, just returns the input

    minimizer_output = { 'fun' : func(x0), 'nfev' : 1 }
    
    return minimizer_output



