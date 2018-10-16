import numpy as np
import json


# See https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
#
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


def get_first_callable( namespace ):
    "return the first callable function in the given namespace"

    callable_names = [ attrib_name for attrib_name in dir(namespace) if callable(getattr(namespace, attrib_name)) ]

    top_level_methods = len(callable_names)

    if top_level_methods==1:
        return callable_names[0]
    else:
        raise Exception("Expecting exactly one top level function in '{}', but found {} ({}). Please refactor your code". \
                format(namespace.__name__, top_level_methods, callable_names))


def cmdline_parse_and_report(num_params, q_device_name_default, q_device_name_help, minimizer_options_default='{}', start_param_value_default=0.0):

    import argparse
    import json
    import custom_optimizer     # the file will be different depending on the plugin choice

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--start_param_value', '--start-param-value',
                            default=start_param_value_default, help="Initial value of each optimized parameter")

    arg_parser.add_argument('--start_params', '--start-params',
                            type=float, nargs=num_params, help="Initial values of optimized parameters")

    arg_parser.add_argument('--sample_number', '--sample-number', '--shots',
                            default=100, type=int, help="Number of repetitions of each individual quantum run")

    arg_parser.add_argument('--q_device_name', '--q-device-name',
                            default=q_device_name_default, help=q_device_name_help)

    arg_parser.add_argument('--max_func_evaluations', '--max-func-evaluations',
                            default=100, type=int, help="Minimizer's upper limit on the number of function evaluations")

    arg_parser.add_argument('--minimizer_options', '--minimizer-options',
                            default=minimizer_options_default, help="A dictionary in JSON format to be passed to the minimizer function")

    args = arg_parser.parse_args()

    start_param_value       = args.start_param_value
    start_params_default    = np.random.randn( num_params ) if start_param_value == 'random' else [ float(start_param_value) ] * num_params

    start_params            = args.start_params or start_params_default
    sample_number           = args.sample_number
    q_device_name           = args.q_device_name
    max_func_evaluations    = args.max_func_evaluations
    minimizer_options       = json.loads( args.minimizer_options )
    minimizer_method        = get_first_callable( custom_optimizer )

    # We only know how to limit the number of iterations for certain methods,
    # so will introduce this as a "patch" to their minimizer_options dictionary:
    #
    if max_func_evaluations:
        minimizer_options_update = {
            'my_nelder_mead':   {'maxfev':  max_func_evaluations},
            'my_cobyla':        {'maxiter': max_func_evaluations},
            'my_random_sampler':{'maxfev':  max_func_evaluations},
            'my_minimizer':     {'maxfev':  max_func_evaluations},
            }.get(minimizer_method, {})

        minimizer_options.update( minimizer_options_update )

    print("Using start_params = '%s'"           % str(start_params) )
    print("Using shots (sample_number) = %d"    % sample_number)
    print("Using q_device_name = '%s'"          % q_device_name)
    print("Using minimizer_method = '%s'"       % minimizer_method)
    print("Using max_func_evaluations = %d"     % max_func_evaluations)         # this parameter may influence the next one
    print("Using minimizer_options = '%s'"      % str(minimizer_options) )

    minimizer_function = getattr(custom_optimizer, minimizer_method)   # minimizer_method is a string/name, minimizer_function is an imported callable

    return start_params, sample_number, q_device_name, minimizer_method, minimizer_options, minimizer_function


def ttot(t,s,p):
    R = np.ceil(np.log(1-p)/np.log(1-s))
    return t*R


# Total time to solution (as defined in ttot(t,s,p)), calculated from data and returning errors
def total_time(ts, n_succ, n_tot, p):
    if n_succ == 0:
        return np.nan, np.nan, np.nan, np.nan, 0, 0
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


def benchmark_list_of_runs(list_of_runs, delta, prob, which_fun_key, which_time_key, show_more=False, verbose=True):
    "Perform benchmarking on the already collected JSON file from an experiment: CK entry"

    if verbose:
        print("benchmark_list_of_runs:  delta={}, prob={}, which_fun_key={}, which_time_key={}\n".format(delta, prob, which_fun_key, which_time_key))

    num_repetitions = len(list_of_runs)
    if num_repetitions:
        first_run_input     = list_of_runs[0]['vqe_input']
        classical_energy    = first_run_input['classical_energy']
        minimizer_method    = first_run_input['minimizer_method']
        minimizer_src       = first_run_input['minimizer_src']
        ansatz_method       = first_run_input.get('ansatz_method')
        ansatz_src          = first_run_input.get('ansatz_src')

        n_succ              = 0
        list_selected_times = []

        if verbose:
            print("experiment_file: Goal={}, Minimizer={}, Minimizer_source:\n{}\n\n{}\n{}\n".format(classical_energy, minimizer_method, '-'*100, minimizer_src, '='*100))
            if ansatz_method and ansatz_src:
                print("Ansatz={}, Ansatz_source:\n{}\n{}".format(ansatz_method, ansatz_src, '-'*100))

        for run in list_of_runs:
            vqe_output      = run['vqe_output']
            report          = run['report']

            fun             = float(vqe_output['fun'])
            fun_validated   = float(vqe_output['fun_validated'])
            fun_exact_present   = 'fun_exact' in vqe_output
            fun_exact       = float(vqe_output['fun_exact']) if fun_exact_present else None     # may not be defined for a particular implementation
            fun_selected    = float(vqe_output[which_fun_key])

            q_seconds       = report['total_q_seconds']
            q_shots         = report['total_q_shots']
            time_selected   = report[which_time_key]

            if verbose:
                abs_diff    = abs( fun_selected - classical_energy )
                hit_bool    = abs_diff < delta
                fun_exact_str = 'fun_exact={:.4f}, '.format(fun_exact) if fun_exact_present else ''
                print("fun_participant={:.4f}, fun_validated={:.4f}, {}Qtime={:.2f}sec, Qshots={}, abs_diff={:.4f} {}" \
                    .format(fun, fun_validated, fun_exact_str, q_seconds, q_shots, abs_diff, '(hit)' if hit_bool else '(miss)'))

            if hit_bool:
                n_succ += 1

            list_selected_times.append(time_selected)

        Tave, Terr, t_ave, t_err, s, s_err = total_time(list_selected_times, n_succ, num_repetitions, prob)
        if verbose:
            if show_more:
                print("\nn_succ={}, Tave={:.4f}, Terr={:.4f}, t_ave={:.4f}, t_err={:.4f}, s={:.4f}, s_err={:.4f}\n\n".format(n_succ, Tave, Terr, t_ave, t_err, s, s_err))
            else:
                print("\nn_succ={}, Tave={:.4f}\n\n".format(n_succ, Tave))

        return classical_energy, minimizer_method, minimizer_src, n_succ, Tave, Terr, t_ave, t_err, s, s_err

