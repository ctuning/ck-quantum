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

    # Get current timestamp
    r=ck.get_current_date_time({})
    if r['return']>0: return r
    timestamp   = r['iso_datetime']
    timestamp_s = timestamp.split('.')[0]   # cut to the seconds' resolution

    username    = os.getlogin()
    opti_method = i.get('opti_method', 'my_cobyla')
    sample_size = i.get('sample_size', 1)
    repetitions = i.get('repetitions', 3)
    q_device    = i.get('q_device', 'QVM')
    max_iter    = i.get('max_iter', 80)
    record_repo = i.get('record_repo', 'local')
    remote_repo = 'ck-quantum-hackathons' if record_repo!='local' else ''

    record_uoa  = '{}_{}_{}_{}samples_{}'.format(timestamp_s, username, opti_method, sample_size, q_device)

    print('Will be recording into {}:experiment:{}\n'.format(record_repo, record_uoa))

    benchmark_adict = {'action':                'benchmark',
                'module_uoa':                   'program',
                'data_uoa':                     'rigetti-vqe',
                'repetitions':                  repetitions,
                'record':                       'yes',
                'record_repo':                  record_repo,
                'record_uoa':                   record_uoa,
                'record_experiment_repo':       remote_repo,    # 'upload' for remote
                'tags':                         'post-hackathon,{},{},{}'.format(q_device, username, opti_method),
                'env.RIGETTI_QUANTUM_DEVICE':   q_device,
                'env.VQE_MINIMIZER_METHOD':     opti_method,
                'env.VQE_SAMPLE_SIZE':          sample_size,
                'env.VQE_MAX_ITERATIONS':       max_iter,
                'skip_freq':                    'yes',
    }

    r=ck.access( benchmark_adict )

    return r
