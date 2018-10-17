import scipy.optimize


def my_cobyla( func, x0, my_args=(), my_options=None ):
    "Stock COBYLA optimizer from SciPy library"

    return scipy.optimize.minimize( func, x0, method='COBYLA', options=my_options, args=my_args )
