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

# Local settings

selector=[
]

selector2=[
    {'name':'Platform', 'key':'_platform'},
    {'name':'Team', 'key':'_team'},
    {'name':'Minimizer method', 'key':'_minimizer_method'}
]

selector3=[
]

metrics_selector_s=[
    {'name':'Fun Key', 'key':'__fun_key', 'values':['fun','fun_exact','fun_validated']},
    {'name':'Time Key', 'key':'__time_key', 'values':['total_q_shots','total_q_seconds','total_seconds']},
    {'name':'Delta', 'key':'__delta', 'config':{'type':'number','min':0,'step':0.05}},
    {'name':'Prob', 'key':'__prob', 'config':{'type':'number','min':0,'max':1,'step':0.1}}
]

dimensions=[
    {"key":"experiment", "name":"Experiment number", "view_key":"__number"},
    {"key":"__energies", "name":"Energy convergence", "view_key":"__energies"},
    {"key":"__fevs", "name":"Function evaluation", "view_key":"__fevs"},
    {"key":"_point", "name":"Point", "view_key":"_point"},
    {"key":"fun", "name":"fun", "view_key":"fun"},
    {"key":"fun_exact", "name":"fun_exact", "view_key":"fun_exact"},
    {"key":"fun_validated", "name":"fun_validated", "view_key":"fun_validated"},
    {"key":"total_q_seconds", "name":"total_q_seconds", "view_key":"total_q_seconds"},
    {"key":"total_q_shots", "name":"total_q_shots", "view_key":"total_q_shots"},
    {"key":"total_seconds", "name":"total_seconds", "view_key":"total_seconds"},
]

metrics_dimensions=[
    {"key":"experiment", "name":"Experiment number", "view_key":"__number"},
    {"key":"_point", "name":"Point", "view_key":"_point"},
    {"key":"__energies", "name":"Energy", "view_key":"__energies"},
    {"key":"T_ave", "name":"T_ave", "view_key":"T_ave"},
    {"key":"_sample_number", "name":"Sample number", "view_key":"_sample_number"},
    {"key":"__times", "name":"Time", "view_key":"__times"},
    {"key":"t_ave", "name":"t_ave", "view_key":"t_ave"},
]

view_cache=[
]

table_view=[
    {"key":"_platform", "name":"Platform"},
    {"key":"_team", "name":"Team"},
    {"key":"_minimizer_method", "name":"Minimizer method"},
    {"key":"_sample_number", "name":"Sample number"},
    {"key":"_max_iterations", "name":"Max iterations"},
    {"key":"_point", "name":"Point"},
    {"key":"_repetition_id", "name":"Repetition ID"},
    {"key":"fun", "name":"fun", "format":"%.3f"},
    {"key":"fun_exact", "name":"fun_exact", "format":"%.3f"},
    {"key":"fun_validated", "name":"fun_validated", "format":"%.3f"},
    {"key":"nfev", "name":"nfev"},
    {"key":"nit", "name":"nit"},
    {"key":"success", "name":"success"},
    {"key":"total_q_seconds", "name":"total_q_seconds", "format":"%.3f"},
    {"key":"total_q_shots", "name":"total_q_shots"},
    {"key":"total_seconds", "name":"total_seconds", "format":"%.3f"},
    {"key":"_minimizer_src", "name":"Minimizer Source"},
]

metrics_table_view=[
    {"key":"_platform", "name":"Platform"},
    {"key":"_team", "name":"Team"},
    {"key":"_minimizer_method", "name":"Minimizer method"},
    {"key":"_sample_number", "name":"Sample number"},
    {"key":"_max_iterations", "name":"Max iterations"},
    {"key":"_point", "name":"Point"},
    {"key":"T_ave", "name":"T_ave", "format":"%.3f"},
    {"key":"T_err", "name":"T_err", "format":"%.3f"},
    {"key":"num_repetitions", "name":"num_repetitions"},
    {"key":"s", "name":"s", "format":"%.3f"},
    {"key":"s_err", "name":"s_err", "format":"%.3f"},
    {"key":"t_ave", "name":"t_ave", "format":"%.3f"},
    {"key":"t_err", "name":"t_err", "format":"%.3f"},
]

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
# TBD: action description

def detect(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out('TBD: action description')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

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
        
    # FIXME: Switch to 'ck-quantum-hackathon-20181006' for the event.
    repo_uoa = 'ck-quantum-hackathons'

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
            tags = r['dict']['tags']

            skip = False
            # FIXME: Get the team name.
            team_tags = [ tag for tag in tags if tag.startswith('team-') ]
            email_tags = [ tag for tag in tags if tag.find('@')!=-1 ]
            if len(team_tags) > 0:
                team = team_tags[0][0:7]
            elif len(email_tags) > 0:
                team = email_tags[0]
            else:
                print('[Warning] Cannot determine team name for experiment in: \'%s\'' % r['path'])
                team = 'team-default'

            if skip:
                print('[Warning] Skipping experiment with bad tags:')
                print(tags)
                continue
        
            # For each point.    
            for point in r['points']:
                point_file_path = os.path.join(r['path'], 'ckp-%s.0001.json' % point)
                with open(point_file_path) as point_file:
                    point_data_raw = json.load(point_file)
                characteristics_list = point_data_raw['characteristics_list']
                num_repetitions = len(characteristics_list)
                data = [
                    {
                        # features
                        'platform': characteristics['run'].get('vqe_input', {}).get('q_device_name', 'unknown').lower(),
                        # choices
                        'minimizer_method': characteristics['run'].get('vqe_input', {}).get('minimizer_method', 'n/a'),
                        'minimizer_options': characteristics['run'].get('vqe_input', {}).get('minimizer_options', {'maxfev':-1}),
                        'minimizer_src': characteristics['run'].get('vqe_input', {}).get('minimizer_src', ''),
                        'sample_number': characteristics['run'].get('vqe_input', {}).get('sample_number','n/a'),
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
                    'platform', 'team', 'minimizer_method', 'sample_number', 'max_iterations', 'point', 'repetition_id'
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
                    tmp_max_iterations = list(datum.get('minimizer_options',{'maxfev':-1}).values())
                    datum['max_iterations'] = tmp_max_iterations[0] if len(tmp_max_iterations)>0 else -1
                    for key in index:
                        datum['_' + key] = datum[key]
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
                if df_prev.index.levels[:-2]==df_curr.index.levels[:-2]: # if the indices match for all but the last two levels
                    if df_prev.index.levels[-2]!=df_curr.index.levels[-2]: # if the experiments are different
                        if df_prev['minimizer_src'].values==df_curr['minimizer_src'].values: # if the minimizer source is the same
                            print('[Info] Merging experiment:')
                            print(df_curr.index.levels)
                            print('[Info] into:')
                            print(df_prev.index.levels)
                            print('[Info] as:')
        #                     df_curr.index = df_prev.index.copy() # TODO: increment repetition_id
                            df_curr.index = pd.MultiIndex.from_tuples([(x[0],x[1],x[2],x[3],x[4],x[5],x[6]+1) for x in df_prev.index])
                            print(df_curr.index.levels)
                            print
                        else:
                            print('[Warning] Cannot merge experiments as the minimizer source is different:')
        #                     print('------------------------------------------------------------------------')
                            print(df_prev.index.levels)
        #                     print(df_prev['minimizer_src'].values[0])
        #                     print
        #                     print('------------------------------------------------------------------------')
                            print(df_curr.index.levels)
        #                     print(df_curr['minimizer_src'].values[0])
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
        'total_seconds']

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

        row['_minimizer_src'] = {
            'title': 'Show',
            'cmd': record['_minimizer_src']
           }

        table.append(row)

    # prepare metrics data
    df_m = merge_experimental_results(df)

    metrics_data = []
    names_no_repetitions = df_m.index.names[:-1]

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

    return {
        'return':0,

        'full_selector':selector,
        'full_selector2':selector2,
        'full_selector3':selector3,
        'full_dimensions':dimensions,
        'full_table_view':table_view,

        'metrics_selector':selector,
        'metrics_selector2':selector2,
        'metrics_selector3':selector3,
        'metrics_selector_s':metrics_selector_s,
        'metrics_dimensions':metrics_dimensions,
        'metrics_table_view':metrics_table_view,
        }
        
