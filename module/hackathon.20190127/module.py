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

#default_repo_uoa = ''
#default_repo_uoa = 'local'
default_repo_uoa = 'ck-quantum-hackathon-20190127'


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

    selected_repo_uoa = i.get('repo_uoa', default_repo_uoa)

    def get_experimental_results(repo_uoa=selected_repo_uoa, tags='qck,hackathon-20190127', module_uoa='experiment'):
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

                if i.get('out')=='con':
                    ck.out( "Loading  {}:experiment:{}  point_id={} (recorded {})".format(repo_uoa, data_uoa, point_id, entry_modification_utc_human) )

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
                        'training_accuracy': np.float64(characteristics['run'].get('training_accuracy',1e6)),
                        'training_time': np.float64(characteristics['run'].get('training_time',0.0)),
                        'training_vectors_limit': np.int64(characteristics['run'].get('training_vectors_limit') or -1),
                        'solution_function_name': characteristics['run'].get('solution_function_name',''),
                        'source_code': characteristics['run'].get('source_code',''),
                        'circuit_str': characteristics['run'].get('circuit_str',''),
                        'test_accuracy': np.float64(characteristics['run'].get('test_accuracy',0.0)),

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
    df = get_experimental_results()

    df.reset_index(inplace=True, drop=True)     # remove the index as it is in the way of complex grouping

    ## Sorting in place allows us to preserve this order as the initial order in the output
    df.sort_values(['problem_name', 'test_accuracy', 'timestamp_epoch_secs'], ascending=[True, False, True], inplace=True)
    df['rank'] = df.groupby('problem_name').cumcount()+1

    df['seconds_since_start'] = df['timestamp_epoch_secs']-df['timestamp_epoch_secs'].min()

#    from IPython.display import display
    pd.options.display.max_columns = len(df.columns)
    pd.options.display.max_rows = len(df.index)
#    display(df)

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
        'training_vectors_limit',
        'training_time',
        'training_accuracy',
        'solution_function_name',
        'source_code',
        'circuit_str',
        'test_accuracy',
        'rank',

        'team',
        'timestamp_epoch_secs',
        'timestamp_utc_human',
        'seconds_since_start',

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
