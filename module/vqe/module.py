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


def init(i):

    return {'return':0}


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

    print('Will be recording into {}{}:experiment:{}\n'.format(record_repo, '/{}'.format(remote_repo) if remote_repo else '', record_uoa))

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
