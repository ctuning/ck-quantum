import numpy as np
from hackathon import optimizers as optimizers
import inspect


def ttot(t,s,p):
    R = np.ceil(np.log(1-p)/np.log(1-s))
    return t*R

# Total time to solution (as defined in ttot(t,s,p)), calculated from data and returning errors
def total_time(ts, n_succ, n_tot, p):
    if n_succ == 0:
        return tuple([*[np.nan]*4,0,0])
    t_ave = np.mean(ts)
    t_err = np.std(ts)/len(ts)**0.5       # Standard error for t
    if n_succ == n_tot:
        return t_ave,t_err,t_ave,t_err,1,0     # Always works so return time per run. Also prevents np.log(0) in code that follows.
    s = float(n_succ)/n_tot
    s_err = (s*(1-s)/float(n_tot))**0.5   # Standard error for s (using binomial dist)
    Tave = ttot(t_ave,s,p)
    T_serr = ttot(t_ave,s+s_err,p)
    T_serr2 = ttot(t_ave,s-s_err,p)
    Terr = (( (T_serr2 - T_serr)/2.)**2 + (t_err*Tave/float(t_ave)) ** 2 ) ** 0.5  # Error in total error assuming t and s independent
    return Tave, Terr, t_ave, t_err, s, s_err

def benchmark_code(vqe_entry, N = 100, solution = 0., delta = 1e-1, p=0.95):
    n_succ = 0
    out_list = []
    n_samples_list = []
    for i in range(N):
        out, n_samples = vqe_entry()  # 'out' is the global minimum 'found' by the participant's code, 'n_samples' is the number of samples they used in total throughout the optimisation procedure
        if abs(out-solution) <= delta:
            n_succ += 1
        out_list.append(out)
        n_samples_list.append(n_samples)
    Tave, Terr, t_ave, t_err, s, s_err = total_time(n_samples_list, n_succ, N, p)
    # The key metric is is Tave (which has error +/- Terr to 1 stdev), but we'll return everything to be stored anyway
    return Tave, Terr, t_ave, t_err, s, s_err, out_list, n_samples_list


def get_min_func_src_code():    # Utility function

    lines = inspect.getsource(optimizers.my_minimizer)
    return lines

