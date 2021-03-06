#
# Collective Knowledge ()
#
#
#
#
# Developer:
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel)

import os
import sys
import json
import re

import pandas as pd
import numpy as np


##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}


##############################################################################
# get raw data for repo-widget

def get_raw_data(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    repo_uoa = 'ck-quantum-hackathon-20181006'

    def get_experimental_results(repo_uoa, tags='qck', module_uoa='experiment'):
        r = ck.access({'action':'search', 'repo_uoa':repo_uoa, 'module_uoa':module_uoa, 'tags':tags})
        if r['return']>0:
            print('Error: %s' % r['error'])
            exit(1)
        experiments = r['lst']

        dfs = []
        for experiment in experiments:
            data_uoa = experiment['data_uoa']
            r = ck.access({'action':'list_points', 'repo_uoa':repo_uoa, 'module_uoa':module_uoa, 'data_uoa':data_uoa})
            if r['return']>0:
                print('Error: %s' % r['error'])
                exit(1)

            # Get all the parameters from meta.json -> "meta"
            mmeta       = r['dict']['meta']

            team        = mmeta.get('team', r['dict'].get('team', 'team-default') )
            molecule    = mmeta.get('hamiltonian', 'Hydrogen')
            vendor      = mmeta.get('provider', 'IBM')

            # For each point.
            for point in r['points']:
                point_file_path = os.path.join(r['path'], 'ckp-%s.0001.json' % point)
                with open(point_file_path) as point_file:
                    point_data_raw = json.load(point_file)
                choices = point_data_raw['choices']
                characteristics_list = point_data_raw['characteristics_list']
                num_repetitions = len(characteristics_list)
                data = [
                    {
                        # features
                        'platform': characteristics['run'].get('vqe_input', {}).get('q_device_name', 'unknown').lower(),
                        'molecule': molecule,
                        'vendor': vendor,
                        # choices
                        'minimizer_method': characteristics['run'].get('vqe_input', {}).get('minimizer_method', 'n/a'),
                        'minimizer_options': characteristics['run'].get('vqe_input', {}).get('minimizer_options', {'maxfev':-1}),
                        'minimizer_src': characteristics['run'].get('vqe_input', {}).get('minimizer_src', ''),
                        'ansatz_method': characteristics['run'].get('vqe_input', {}).get('ansatz_method', ''),
                        'ansatz_src': characteristics['run'].get('vqe_input', {}).get('ansatz_src', ''),
                        'sample_number': characteristics['run'].get('vqe_input', {}).get('sample_number','n/a'),
                        'max_iterations': choices['env'].get('VQE_MAX_ITERATIONS', -1),
                        # statistical repetition
                        'repetition_id': repetition_id,
                        # runtime characteristics
                        'run': characteristics['run'],
                        'report': characteristics['run'].get('report', {}),
                        'vqe_output': characteristics['run'].get('vqe_output', {}),
                    }
                    for (repetition_id, characteristics) in zip(range(num_repetitions), characteristics_list)
                    if len(characteristics['run']) > 0
                ]

                index = [
                    'platform', 'team', 'minimizer_method', 'sample_number', 'max_iterations', 'point', 'repetition_id', 'molecule', 'ansatz_method', 'vendor'
                ]

                for datum in data:
                    datum['team'] = team
                    datum['point'] = point
                    datum['success'] = datum.get('vqe_output',{}).get('success',False)
                    datum['nfev'] = np.int64(datum.get('vqe_output',{}).get('nfev',-1))
                    datum['nit'] = np.int64(datum.get('vqe_output',{}).get('nit',-1))
                    datum['fun'] = np.float64(datum.get('vqe_output',{}).get('fun',0))
                    datum['fun_validated'] = np.float64(datum.get('vqe_output',{}).get('fun_validated',0))
                    datum['fun_exact'] = np.float64(datum.get('vqe_output',{}).get('fun_exact',0))
                    datum['total_seconds'] = np.float64(datum.get('report',{}).get('total_seconds',0))
                    datum['total_q_seconds'] = np.float64(datum.get('report',{}).get('total_q_seconds',0))
                    datum['total_q_shots'] = np.int64(datum.get('report',{}).get('total_q_shots',0))
                    datum['max_iterations'] = np.int64(datum.get('max_iterations',-1))
                    for key in index:
                        datum['_' + key] = datum[key]
                    datum['_ansatz_src'] = datum['ansatz_src']
                    datum['_minimizer_src'] = datum['minimizer_src']

                # Construct a DataFrame.
                df = pd.DataFrame(data)
                df = df.set_index(index)
                # Append to the list of similarly constructed DataFrames.
                dfs.append(df)
        if dfs:
            # Concatenate all thus constructed DataFrames (i.e. stack on top of each other).
            result = pd.concat(dfs)
            result.sort_index(ascending=True, inplace=True)
        else:
            # Construct a dummy DataFrame the success status of which can be safely checked.
            result = pd.DataFrame(columns=['success'])
        return result

    # Merge experimental results from the same team with the same parameters
    # (minimizer_method, sample_number, max_iterations) and minimizer source.
    def merge_experimental_results(df):
        dfs = []
        df_prev = None
        for index, row in df.iterrows():
            # Construct a DataFrame.
            df_curr = pd.DataFrame(row).T
            # Check if this row is similar to the previous row.
            if df_prev is not None: # if not the very first row
                if df_prev.index.levels[:5]==df_curr.index.levels[:5]: # if the indices match for all but the last two levels
                    if df_prev.index.levels[5]!=df_curr.index.levels[5]: # if the experiments are different
                        if df_prev['minimizer_src'].values==df_curr['minimizer_src'].values and df_prev['ansatz_src'].values==df_curr['ansatz_src'].values: # if the minimizer and ansatz sources are the same
                            print('[Info] Merging experiment:')
                            print(df_curr.index.levels)
                            print('[Info] into:')
                            print(df_prev.index.levels)
                            print('[Info] as:')
        #                     df_curr.index = df_prev.index.copy() # TODO: increment repetition_id
                            df_curr.index = pd.MultiIndex.from_tuples([(x[0],x[1],x[2],x[3],x[4],x[5],x[6]+1,x[7],x[8],x[9]) for x in df_prev.index])
                            print(df_curr.index.levels)
                            print
                        else:
                            print('[Warning] Cannot merge experiments as the minimizer or ansatz sources are different (previous vs current):')
                            print(df_prev.index.levels)
                            print
                            print(df_curr.index.levels)
                            print
        #             else:
        #                 print('[Info] Keeping experiments separate:')
        #                 print(df_prev.index.levels)
        #                 print(df_curr.index.levels)
        #                 print
            # Append to the list of similarly constructed DataFrames.
            dfs.append(df_curr)
            # Prepare for next iteration.
            df_prev = df_curr

        # Concatenate all thus constructed DataFrames (i.e. stack on top of each other).
        result = pd.concat(dfs)
        result.index.names = df.index.names
        result.sort_index(ascending=True, inplace=True)

        return result

    # prepare table
    df = get_experimental_results(repo_uoa=repo_uoa)

    table = []

    def to_value(i):
        if type(i) is np.ndarray:
            return i.tolist()

        if isinstance(i, np.int64):
            return int(i)

        return i

    props = [
        '_platform',
        '_team',
        '_minimizer_method',
        '_sample_number',
        '_max_iterations',
        '_point',
        '_repetition_id',
        'fun',
        'fun_exact',
        'fun_validated',
        'nfev',
        'nit',
        'success',
        'total_q_seconds',
        'total_q_shots',
        'total_seconds',
        '_ansatz_method',
        '_vendor',
        '_molecule',
    ]

    for record in df.to_dict(orient='records'):
        row = {}
        for prop in props:
            row[prop] = to_value(record.get(prop, ''))

        energies = [ iteration['energy'] for iteration in record['report']['iterations'] ]
        fevs = list(range(len(energies)))
        last_energy = energies[-1]
        minimizer_method = record.get('_minimizer_method', '')
        last_fev = row['nfev']-1 if minimizer_method=='my_cobyla' or 'my_nelder_mead' else row['nfev']

        row['__energies'] = energies
        row['__fevs'] = fevs

        row['##data_uid'] = "{}:{}".format(record['_point'], record['_repetition_id'])

        row['_ansatz_src'] = {
            'title': record.get('_ansatz_method','Show'),
            'cmd': record['_ansatz_src']
           }

        row['_minimizer_src'] = {
            'title': record.get('_minimizer_method','Show'),
            'cmd': record['_minimizer_src']
           }

        table.append(row)

    # prepare metrics data
    df_m = merge_experimental_results(df)

    metrics_data = []
    names_no_repetitions = [ n for n in df_m.index.names if n != 'repetition_id' ]

    for index, group in df_m.groupby(level=names_no_repetitions):
        runs = []

        for run in group['run']:
            run_t = {}
            run_t['report'] = run['report']
            run_t['vqe_input'] = run['vqe_input']
            run_t['vqe_output'] = run['vqe_output']
            runs.append(run_t)

        data = {}
        data['runs'] = runs
        data['num_repetitions'] = len(group)

        meta = {}
        meta.update({ k : v for (k, v) in zip(names_no_repetitions, index) })

        for key in names_no_repetitions:
            data['_' + key] = to_value(meta[key])

        data['##data_uid'] = to_value(meta['point'])

        metrics_data.append(data)

    return {'return':0, 'full_table':table, 'metrics_table':metrics_data}


##############################################################################
# get raw config for repo widget

def get_raw_config(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    data_config = cfg['data_config']
    data_config['return'] = 0

    return data_config
