import inspect

def hello(): # this is the wrapper to scipy minimizer
    
    return "Have a good hackathon"


def get_min_func_src_code():
    lines = inspect.getsource(hello)
    return lines



