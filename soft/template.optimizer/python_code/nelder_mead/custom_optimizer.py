import scipy.optimize


def my_nelder_mead( func, x0, my_args=(), my_options=None ):
    "Stock Nelder-Mead optimizer from SciPy library"

    return scipy.optimize.minimize( func, x0, method='Nelder-Mead', options=my_options, args=my_args )
