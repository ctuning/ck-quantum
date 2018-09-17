#
# Collective Knowledge (checking and installing software)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon, leo@dividiti.com
#

# ck benchmark program:rigetti-vqe --repetitions=3 --record --record_repo=local --record_uoa=lg4_again3 --tags=hackathon-again,lg4,QVM,my_cobyla --env.RIGETTI_QUANTUM_DEVICE=QVM --env.VQE_MINIMIZER_METHOD=my_cobyla --env.VQE_SAMPLE_SIZE=1 --env.VQE_MAX_ITERATIONS=80  --skip_freq

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 


import os
from pprint import pprint


def init(i):

    return {'return':0}


def list_deployables(i):

    print('list_deployables() was called with the following arguments: {}\n'.format(i))

    data_uoa = i.get('data_uoa', 'template_optimizer')

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


def deploy(i):

    print('deploy() was called with the following arguments: {}\n'.format(i))

    optimizer_name  = i.get('optimizer')

    if not optimizer_name:
        available_optimizers = list_deployables({ 'data_uoa': 'template.optimizer' })['dir_names']
        return {'return': 1, 'error': "--optimizer is an obligatory parameter.\nPlease try again with one of the following values: {}".format(available_optimizers)}

    soft_data_uoa   = 'deployed.' + optimizer_name

    ck.out("Creating soft:{} code-containing CK entry from a template".format(soft_data_uoa))
    ## ck cp soft:template.optimizer soft:deployed.optimizer
    #
    cp_adict = {    'action':           'cp',
                    'module_uoa':       'soft',
                    'data_uoa':         'template.optimizer',
                    'new_module_uoa':   'soft',
                    'new_data_uoa':     soft_data_uoa
    }
    r=ck.access( cp_adict )
    if r['return']>0: return r

    deployed_soft_entry_path = r['path']
    python_file_name = r['dict']['customize']['soft_file_universal']

    ck.out("Activating soft:{} CK entry as 'deployed'".format(soft_data_uoa))
    ## ck update soft:deployed.optimizer --tags=deployed
    #
    update_adict = {'action':           'update',
                    'module_uoa':       'soft',
                    'data_uoa':         soft_data_uoa,
                    'tags':             'deployed'
    }
    r=ck.access( update_adict )
    if r['return']>0: return r

    ck.out("Creating an environment entry that sets up the paths for the soft:{} CK entry".format(soft_data_uoa))
    ## ck detect soft --tags=vqe,optimizer,lib,deployed --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    ## ck detect soft:deployed.optimizer --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    #
    detect_adict = {'action':           'detect',
                    'module_uoa':       'soft',
                    'data_uoa':         soft_data_uoa,
                    'extra_tags':       optimizer_name,
                    'full_path':        os.path.join(deployed_soft_entry_path, 'python_code', optimizer_name, python_file_name),
    }
    r=ck.access( detect_adict )
    if r['return']>0: return r

    return r


def cleanup(i):

    ck.out("Removing the detected env entries")
    ## ck clean env --tags=optimizer,deployed
    #
    clean_adict = { 'action':           'clean',
                    'module_uoa':       'env',
                    'tags':             'optimizer,deployed',
                    'f':                'yes',
    }
    r=ck.access( clean_adict )
    if r['return']>0: return r

    ck.out("Removing the deployed soft entries")
    ## ck rm soft:* --tags=vqe,optimizer,lib,deployed
    #
    rm_adict = {    'action':           'rm',
                    'module_uoa':       'soft',
                    'data_uoa':         '*',
                    'tags':             'vqe,optimizer,lib,deployed',
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
        timestamp   = r['iso_datetime'].split('.')[0].replace(':', '_')     # cut to seconds' resolution

    username    = os.getlogin()
    opti_method = i.get('opti_method', 'my_cobyla')
    sample_size = i.get('sample_size', 1)
    repetitions = i.get('repetitions', 3)
    max_iter    = i.get('max_iter', 80)

    remote_bool = i.get('remote', '') == 'yes'      # whether to record the experiment remotely or locally
    (record_repo, remote_repo) = ('remote-ck', 'ck-quantum-hackathons') if remote_bool else ('local', '')

    provider    = i.get('provider', 'rigetti').lower()              # 'rigetti' or 'ibm'
    hw_bool     = i.get('hardware', '') == 'yes'
    dev_bool    = i.get('dev', '') == 'yes'

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
        'rigetti' : {
            False : 'rigetti-vqe',
            True : 'rigetti-vqe2',
        },
        'ibm' : {
            False : 'qiskit-vqe',
            True : 'qiskit-vqe',
        },
    }[provider][dev_bool]

    record_uoa  = '{}__{}_{}_{}samples_{}'.format(timestamp, username, opti_method, sample_size, q_device)

    ck.out('Will be recording into {}{}:experiment:{}\n'.format(record_repo, '/{}'.format(remote_repo) if remote_repo else '', record_uoa))

    benchmark_adict = {'action':                'benchmark',
                'module_uoa':                   'program',
                'data_uoa':                     program,
                'repetitions':                  repetitions,
                'record':                       'yes',
                'record_repo':                  record_repo,
                'record_uoa':                   record_uoa,
                'record_experiment_repo':       remote_repo,
                'tags':                         'post-hackathon,{},{},{}'.format(q_device, username, opti_method),
                'env.VQE_MINIMIZER_METHOD':     opti_method,
                'env.VQE_SAMPLE_SIZE':          sample_size,
                'env.VQE_MAX_ITERATIONS':       max_iter,
                'env.VQE_QUANTUM_BACKEND':      q_device,
                'skip_freq':                    'yes',
    }

    r=ck.access( benchmark_adict )

    return r
