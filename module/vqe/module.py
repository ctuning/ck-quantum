#
# Collective Knowledge (checking and installing software)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon, leo@dividiti.com
#

# ck benchmark program:rigetti-vqe --repetitions=3 --record --record_uoa=lg4_again3 --tags=hackathon-again,lg4,QVM,my_cobyla --env.RIGETTI_QUANTUM_DEVICE=QVM --env.VQE_MINIMIZER_METHOD=my_cobyla --env.VQE_SAMPLE_SIZE=1 --env.VQE_MAX_ITERATIONS=80  --skip_freq

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel)

hackathon_date          = '20181006'    # TODO: change this to None after the event
hackathon_tag           = 'hackathon-{}'.format(hackathon_date if hackathon_date else 'dev')
hackathon_remote_repo   = 'ck-quantum-hackathon-{}'.format(hackathon_date) if hackathon_date else 'ck-quantum-hackathons'

import os
import sys
from pprint import pprint


def init(i):

    vqe_plugin_directory = os.path.join( os.path.dirname(__file__), '..', '..', 'env', 'vqe_utils' )
    sys.path.append( vqe_plugin_directory )    # allow this module to import vqe_utils

    return {'return':0}


def list_deployables(i):

    print('list_deployables() was called with the following arguments: {}\n'.format(i))

    data_uoa = i.get('data_uoa', 'template.optimizer')

    load_adict = {  'action':           'load',
                    'module_uoa':       'soft',
                    'data_uoa':         data_uoa,
    }
    r=ck.access( load_adict )
    if r['return']>0: return r

    template_soft_entry_path = r['path']
    python_code_common_path = os.path.join(template_soft_entry_path, 'python_code')

    dir_names = [dir_name for dir_name in (os.listdir( python_code_common_path )) if os.path.isdir( os.path.join( python_code_common_path, dir_name ) ) ]

    if i.get('out')=='con':
        ck.out("{}".format(dir_names))

    return {'return': 0, 'dir_names': dir_names}


def deploy_optimizer(i):

    i.update({'type' : 'optimizer'})

    return deploy(i)


def deploy_ansatz(i):

    i.update({'type' : 'qiskit.ansatz'})

    return deploy(i)


def deploy(i):

    print('deploy() was called with the following arguments: {}\n'.format(i))

    plugin_type     = i.get('type', 'optimizer')

    selected_value  = i.get('value')
    template_uoa    = 'template.' + plugin_type
    dir_names       = list_deployables({ 'data_uoa': template_uoa })['dir_names']

    if not selected_value:      # Acquire it interactively
        select_adict = {'action': 'select_string',
                        'module_uoa': 'misc',
                        'options': dir_names,
                        'default': '',
                        'question': 'Please select the value for {}'.format(plugin_type),
        }
        r=ck.access( select_adict )
        if r['return']>0:
            return r
        else:
            idx = r.get('selected_index', -1)
            if idx<0:
                return {'return':1, 'error':'selection number {} is not recognized'.format(idx)}
            else:
                selected_value = dir_names[idx]

    deployed_uoa    = 'deployed.' + selected_value

    ck.out("Creating soft:{} code-containing CK entry from a template".format(deployed_uoa))
    ## ck cp soft:template.optimizer soft:deployed.optimizer
    #
    cp_adict = {    'action':           'cp',
                    'module_uoa':       'soft',
                    'data_uoa':         template_uoa,
                    'new_module_uoa':   'soft',
                    'new_data_uoa':     deployed_uoa,
    }
    r=ck.access( cp_adict )
    if r['return']>0: return r

    deployed_soft_entry_path = r['path']
    python_file_name = r['dict']['customize']['soft_file_universal']

    ck.out("Activating soft:{} CK entry as 'deployed'".format(deployed_uoa))
    ## ck update soft:deployed.optimizer --tags=deployed
    #
    update_adict = {'action':           'update',
                    'module_uoa':       'soft',
                    'data_uoa':         deployed_uoa,
                    'tags':             'deployed',
    }
    r=ck.access( update_adict )
    if r['return']>0: return r

    ck.out("Removing all the 'inactive' alternaitves")
    for dir_name in dir_names:
        if dir_name!=selected_value:
            dir_path = os.path.join(deployed_soft_entry_path, 'python_code', dir_name)
            os.system("rm -rf {}".format(dir_path))     # FIXME: dangerous, look at other options

    ck.out("Creating an environment entry that sets up the paths for the soft:{} CK entry".format(deployed_uoa))
    ## ck detect soft --tags=vqe,optimizer,lib,deployed --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    ## ck detect soft:deployed.optimizer --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    #
    detect_adict = {'action':           'detect',
                    'module_uoa':       'soft',
                    'data_uoa':         deployed_uoa,
                    'extra_tags':       selected_value,
                    'full_path':        os.path.join(deployed_soft_entry_path, 'python_code', selected_value, python_file_name),
    }
    r=ck.access( detect_adict )
    if r['return']>0: return r

    return r


def plugin_path(i):

    plugin_type     = i.get('type', 'optimizer')

    ## ck search soft --tags=deployed,optimizer
    #
    search_adict = {'action':           'search',
                    'module_uoa':       'soft',
                    'tags':             'deployed,'+plugin_type,
    }
    r=ck.access( search_adict )
    if r['return']>0: return r

    items_found = len(r['lst'])
    if items_found!=1:
        return {'return':1, 'error':'the number of deployed {} plugins was {}, expecting 1'.format(plugin_type, items_found)}

    deployed_soft_entry_path = r['lst'][0]['path']
    python_file_name = 'custom_{}.py'.format(plugin_type)

    editable_file_path = os.path.join(deployed_soft_entry_path, 'python_code', '*', python_file_name)

    if i.get('out')=='con':
        ck.out(editable_file_path)

    return {'return': 0, 'editable_file_path': editable_file_path}


def cleanup(i):

    ck.out("Removing the deployed soft and env entries")
    ## ck rm *:* --tags=vqe,deployed
    #
    rm_adict = {    'action':           'rm',
                    'repo_uoa':         'local',
                    'module_uoa':       '*',
                    'data_uoa':         '*',
                    'tags':             'vqe,deployed',
    }
    r=ck.access( rm_adict )
    if r['return']>0: return r

    return {'return': 0}


def run(i):

    print('run() was called with the following arguments: {}\n'.format(i))

    timestamp   = i.get('timestamp')

    if not timestamp:       # Get current timestamp:
        r=ck.get_current_date_time({})
        if r['return']>0: return r
        timestamp   = r['iso_datetime'].split('.')[0].replace(':', '_').replace('-', '_')   # cut to seconds' resolution

    username    = os.getlogin()
    sample_size = i.get('sample_size', 100)
    repetitions = i.get('repetitions', 3)
    max_iter    = i.get('max_iter', 80)

    provider    = i.get('provider', 'ibm').lower()              # 'ibm' (default) or 'rigetti'
    hw_bool     = i.get('hardware', '') == 'yes'

    q_device    = {
        'rigetti' : {
            False : 'QVM',
            True :  '8Q-Agave',
        },
        'ibm' : {
            False : 'local_qasm_simulator',
            True :  'ibmq_qasm_simulator',
        },
    }[provider][hw_bool]

    program     = {
        'ibm':      'qiskit-vqe',
        'rigetti':  'rigetti-vqe2',
    }[provider]

    record_uoa  = '{}--{}-{}-{}samples-{}reps'.format(username, timestamp, q_device, sample_size, repetitions)
    record_cid  = 'local:experiment:{}'.format(record_uoa)

    ck.out('Will be recording the results into {}\n'.format(record_cid))

    benchmark_adict = {'action':                'benchmark',
                'module_uoa':                   'program',
                'data_uoa':                     program,
                'repetitions':                  repetitions,
                'record':                       'yes',
                'record_repo':                  'local',
                'record_uoa':                   record_uoa,
                'tags':                         ','.join([hackathon_tag, q_device, username]),
                'env.VQE_SAMPLE_SIZE':          sample_size,
                'env.VQE_MAX_ITERATIONS':       max_iter,
                'env.VQE_QUANTUM_BACKEND':      q_device,
                'skip_freq':                    'yes',
    }

    r=ck.access( benchmark_adict )
    if r['return']>0: return r

    ck.out('The results have been recorded into {}\n'.format(record_cid))

    return r


def pick_an_experiment(i):

    search_adict = {'action':       'search',
                    'repo_uoa':     'local',
                    'module_uoa':   'experiment',
                    'data_uoa':     '*',
    }
    r=ck.access( search_adict )
    if r['return']>0: return r

    all_experiment_names = [ '{repo_uoa}:{module_uoa}:{data_uoa}'.format(**entry_dict) for entry_dict in r['lst']]

    select_adict = {'action': 'select_string',
                    'module_uoa': 'misc',
                    'options': all_experiment_names,
                    'default': '',
                    'question': 'Please select the experiment entry to upload',
    }
    r=ck.access( select_adict )
    if r['return']>0:
        return r
    else:
        idx = r.get('selected_index', -1)
        if idx<0:
            return {'return':1, 'error':'selection number {} is not recognized'.format(idx)}
        else:
            cid = all_experiment_names[idx]

    return {'return':0, 'cid': cid}


def upload(i):

    # print('upload() was called with the following arguments: {}\n'.format(i))

    cids    = i.get('cids')

    if len(cids)==0:
        r=ck.access( {'action': 'pick_an_experiment', 'module_uoa': 'vqe'} )

        if r['return']>0: return r
        cids = [ r['cid'] ]

    transfer_adict = {  'action':               'transfer',
                        'module_uoa':           'misc',
                        'cids':                 cids,                       # 'ck transfer' will perform its own cids->xcids parsing
                        'target_server_uoa':    'remote-ck',
                        'target_repo_uoa':      hackathon_remote_repo,
    }
    r=ck.access( transfer_adict )
    if r['return']>0: return r

    ck.out('Uploaded.')
    return {'return': 0}


def time_to_solution(i):

    # print('time_to_solution() was called with the following arguments: {}\n'.format(i))

    from vqe_utils import benchmark_list_of_runs

    delta       = float( i.get('delta', 0.15) )
    prob        = float( i.get('prob', 0.90) )
    which_fun   = i.get('which_fun', 'fun_validated')
    which_time  = i.get('which_time', 'total_q_shots')
    show_more   = i.get('show_more', '')=='yes'

    cids        = i.get('cids',[])

    if len(cids)>0:
        cid = cids[0]
    else:
        r=ck.access( {'action': 'pick_an_experiment', 'module_uoa': 'vqe'} )
        if r['return']>0: return r
        cid = r['cid']

    r=ck.parse_cid({'cid': cid})
    if r['return']>0:
        print("Cannot parse CID '{}'".format(cid))
    else:
        repo_uoa    = r.get('repo_uoa','')
        module_uoa  = r.get('module_uoa','')
        data_uoa    = r.get('data_uoa','')

    load_point_adict = {    'action':           'load_point',
                            'repo_uoa':         repo_uoa,
                            'module_uoa':       module_uoa,
                            'data_uoa':         data_uoa,
    }
    r=ck.access( load_point_adict )
    if r['return']>0: return r

    characteristics_list    = r['dict']['0001']['characteristics_list']
    list_of_runs            = [char['run'] for char in characteristics_list]

    benchmark_list_of_runs(list_of_runs, delta, prob, which_fun, which_time, show_more)

    return {'return': 0}
