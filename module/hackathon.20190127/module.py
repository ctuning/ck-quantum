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
import time

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

    repo_uoa = '' # 'local' # 'ck-quantum-hackathon-20190127'

    def get_experimental_results(repo_uoa, tags='qck,hackathon-20190127', module_uoa='experiment'):
        r = ck.access({'action':'search', 'repo_uoa':repo_uoa, 'module_uoa':module_uoa, 'tags':tags})
        if r['return']>0:
            print('Error: %s' % r['error'])
            exit(1)
        experiments = r['lst']

        index = [
            'team', 'problem_index'
        ]

        dfs = []
        for experiment in experiments:
            data_uoa = experiment['data_uoa']
            r = ck.access({'action':'list_points', 'repo_uoa':repo_uoa, 'module_uoa':module_uoa, 'data_uoa':data_uoa})
            if r['return']>0:
                print('Error: %s' % r['error'])
                exit(1)

            # Get all the parameters from meta.json -> "meta"
            mmeta                   = r['dict']['meta']
            team                    = mmeta.get('team', 'UNKNOWN_TEAM')

            experiment_entry_path   = r['path']
            entry_modification_epoch_secs   = int( os.path.getmtime(experiment_entry_path) )
            entry_modification_utc_human    = time.asctime(time.gmtime( entry_modification_epoch_secs ))

            point_ids = r['points']

            for point_id in point_ids:
                load_point_adict = {    'action':           'load_point',
                                        'module_uoa':       module_uoa,
                                        'data_uoa':         data_uoa,
                                        'point':            point_id,
                }
                r=ck.access( load_point_adict )
                if r['return']>0: return r

                print("experiment_uoa={}, point_id={} :".format(data_uoa, point_id))
                point_data_raw = r['dict']['0001']
                choices = point_data_raw['choices']
                characteristics_list = point_data_raw['characteristics_list']
                num_repetitions = len(characteristics_list)

                data = [
                    {
                        # statistical repetition
                        'repetition_id': repetition_id,
                        # runtime characteristics
                        'problem_name': characteristics['run'].get('problem_name','problem_x'),
                        'problem_index': characteristics['run'].get('problem_index',-1),
                        'circuit_str': characteristics['run'].get('circuit_str',''),
                        'training_error': np.float64(characteristics['run'].get('training_error',1e6)),
                        'test_error': np.float64(characteristics['run'].get('test_error',1e6)),
                        'solution_function_name': characteristics['run'].get('solution_function_name',''),
                        'source_code': characteristics['run'].get('source_code',''),
                        'test_accuracy': np.float64(characteristics['run'].get('test_accuracy',0.0)),
                        'training_time': np.float64(characteristics['run'].get('training_time',0.0)),
                        'training_vectors_limit': np.int64(characteristics['run'].get('training_vectors_limit',-1)),

                        'team': team,
                        'timestamp_epoch_secs': entry_modification_epoch_secs,
                        'timestamp_utc_human': entry_modification_utc_human,

                        'success?': characteristics['run'].get('run_success','N/A'),
                    }
                    for (repetition_id, characteristics) in zip(range(num_repetitions), characteristics_list)
                    if len(characteristics['run']) > 0
                ]

                # Construct a DataFrame.
                df = pd.DataFrame(data)
                df = df.set_index(index, drop=False)
                # Append to the list of similarly constructed DataFrames.
                dfs.append(df)
        if dfs:
            # Concatenate all thus constructed DataFrames (i.e. stack on top of each other).
            result = pd.concat(dfs)
            result.sort_index(ascending=True, inplace=True)
        else:
            # Construct a dummy DataFrame the success status of which can be safely checked.
            result = pd.DataFrame(columns=['success?'])

        return result


    # prepare table
    df = get_experimental_results(repo_uoa=repo_uoa)

    df['score'] = 3.14
    from IPython.display import display
    pd.options.display.max_columns = len(df.columns)
    pd.options.display.max_rows = len(df.index)
    display(df)

    table = []

    def to_value(i):
        if type(i) is np.ndarray:
            return i.tolist()

        if isinstance(i, np.int64):
            return int(i)

        if isinstance(i, np.float64):
            return float(i)

        return i

    props = [
        'problem_name',
        'problem_index',
        'solution_function_name',
        'source_code',
        'training_vectors_limit',
        'circuit_str',
        'training_time',
        'training_error',
        'test_accuracy',
        'test_error',

        'team',
        'timestamp_epoch_secs',
        'timestamp_utc_human',

        'success?',
    ]

    for record in df.to_dict(orient='records'):
        row = {}
        for prop in props:
            row[prop] = to_value(record.get(prop, ''))

#        row['##data_uid'] = "{}:{}".format(record['_point'], record['_repetition_id'])

        row['source_code'] = {
            'title': record.get('solution_function_name','Show source'),
            'cmd': record['source_code'],
        }

        if record['circuit_str']:
            row['circuit_str'] = {
                'title': record.get('solution_circuit_name', 'Show circuit'),
                'cmd': record['circuit_str'],
            }
        else:
            row['circuit_str']='N/A'

        table.append(row)

    return {'return':0, 'table':table}


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
