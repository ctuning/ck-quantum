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

hackathon_date          = None # TODO: change this to '20181006' just before the event
hackathon_tag           = 'hackathon-{}'.format(hackathon_date if hackathon_date else 'dev')
hackathon_remote_repo   = 'ck-quantum-hackathon-{}'.format(hackathon_date) if hackathon_date else 'ck-quantum-hackathons'

import getpass
import os
import sys
from pprint import pprint


def init(i):
    """
    Not to be called directly. Sets the path to the vqe_plugin.
    """

    vqe_plugin_directory = os.path.join( os.path.dirname(__file__), '..', '..', 'env', 'vqe_utils' )
    sys.path.append( vqe_plugin_directory )    # allow this module to import vqe_utils

    return {'return':0}


def list_deployables(i):
    """
    Input:  {
                data_uoa            - name of the template soft entry
            }

    Output: {
                dir_names           - full list of deployables within the given template soft entry
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    data_uoa = i.get('data_uoa', 'template.optimizer')

    load_adict = {  'action':           'load',
                    'module_uoa':       'soft',
                    'data_uoa':         data_uoa,
    }
    r=ck.access( load_adict )
    if r['return']>0: return r

    template_soft_entry_path = r['path']
    python_code_common_path = os.path.join(template_soft_entry_path, 'python_code')

    # gather all the subdirectories of python_code_common_path
    dir_names = [dir_name for dir_name in (os.listdir( python_code_common_path )) if os.path.isdir( os.path.join( python_code_common_path, dir_name ) ) ]

    if i.get('out')=='con':
        ck.out("{}".format(dir_names))

    return {'return': 0, 'dir_names': dir_names}


def deploy_optimizer(i):
    """
    Specialization of deploy() method where type='optimizer'.
    Input:  {
                (value)             - which deployable to deploy
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    i.update({'type' : 'optimizer'})

    return deploy(i)


def deploy_ansatz(i):
    """
    Specialization of deploy() method where type='qiskit.ansatz'.
    Input:  {
                (value)             - which deployable to deploy
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    i.update({'type' : 'qiskit.ansatz'})

    return deploy(i)


def deploy(i):
    """
    Input:  {
                type                - either 'optimizer' or 'qiskit.ansatz'
                (value)             - which deployable to deploy
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

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
            selected_value = r['selected_value']

    deployed_uoa    = 'deployed.' + selected_value

    # ck.out("Creating soft:{} code-containing CK entry from a template".format(deployed_uoa))
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

    deployed_soft_cid = '{}:{}:{}'.format(r['repo_uoa'], r['module_uoa'], r['data_uoa'])

    deployed_soft_entry_path = r['path']
    python_file_name = r['dict']['customize']['soft_file_universal']
    python_plugin_full_path = os.path.join(deployed_soft_entry_path, 'python_code', selected_value, python_file_name)

    # ck.out("Activating soft:{} CK entry as 'deployed'".format(deployed_uoa))
    ## ck update soft:deployed.optimizer --tags=deployed
    #
    update_adict = {'action':           'update',
                    'module_uoa':       'soft',
                    'data_uoa':         deployed_uoa,
                    'tags':             'deployed',
    }
    r=ck.access( update_adict )
    if r['return']>0: return r

    # ck.out("Removing all the 'inactive' alternaitves")
    for dir_name in dir_names:
        if dir_name!=selected_value:
            dir_path = os.path.join(deployed_soft_entry_path, 'python_code', dir_name)
            ck.delete_directory( {'path': dir_path} )

    # ck.out("Creating an environment entry that sets up the paths for the soft:{} CK entry".format(deployed_uoa))
    ## ck detect soft --tags=vqe,optimizer,lib,deployed --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    ## ck detect soft:deployed.optimizer --extra_tags=optimizer.custom --full_path=/Users/lg4/CK/local/soft/deployed.optimizer/python_code/optimizer.custom/custom_optimizer.py
    #
    detect_adict = {'action':           'detect',
                    'module_uoa':       'soft',
                    'data_uoa':         deployed_uoa,
                    'extra_tags':       selected_value,
                    'full_path':        python_plugin_full_path,
    }
    r=ck.access( detect_adict )
    if r['return']>0: return r

    deployed_env_cid = '{}:{}:{}'.format('local', 'env', r['env_data_uoa'])

    if i.get('out')=='con':
        ck.out( "Deployed soft entry:    {}".format(deployed_soft_cid) )
        ck.out( "Deployed env entry:     {}".format(deployed_env_cid) )
        ck.out( "Editable python source: {}".format(python_plugin_full_path))

    return { 'return': 0, 'deployed_soft_cid': deployed_soft_cid, 'deployed_env_cid': deployed_env_cid, 'full_path': python_plugin_full_path }


def plugin_path(i):
    """
    Input:  {
                type                - either 'optimizer' or 'ansatz'
             }

    Output: {
                full_path           - full path to the plugin python file to be edited
                plugin_dir          - dirname(full_path)
                plugin_filename     - basename(full_path)

                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    plugin_type     = i.get('type', 'optimizer')

    search_adict = {'action':           'search',
                    'module_uoa':       'env',
                    'data_uoa':         '*',
                    'tags':             'deployed,{}'.format(plugin_type),
    }
    r=ck.access( search_adict )
    if r['return']>0: return r

    lst_len = len(r['lst'])
    if lst_len != 1:
        return {'return':1, 'error':'Expecting a single {} plugin, but found {}'.format(plugin_type, lst_len)}

    data_uoa = r['lst'][0]['data_uoa']

    load_adict = {  'action':           'load',
                    'module_uoa':       'env',
                    'data_uoa':         data_uoa,
    }
    r=ck.access( load_adict )
    if r['return']>0: return r

    full_path       = r['dict']['customize']['full_path']
    plugin_dir      = os.path.dirname( full_path )
    plugin_filename = os.path.basename( full_path )

    if i.get('out')=='con':
        ck.out( full_path )

    return {'return': 0, 'full_path': full_path, 'plugin_dir': plugin_dir, 'plugin_filename': plugin_filename}


def cleanup(i):
    """
    Input:  {
                (type)              - either 'optimizer' or 'ansatz' to only cleanup one plugin
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    plugin_type     = i.get('type')
    tags            = ['vqe', 'deployed']

    if plugin_type:
        tags.append( plugin_type )

    ## ck rm *:* --tags=vqe,deployed
    #
    rm_adict = {    'action':           'rm',
                    'repo_uoa':         'local',
                    'module_uoa':       '*',
                    'data_uoa':         '*',
                    'tags':             ','.join( tags ),
    }
    r=ck.access( rm_adict )
    if r['return']>0: return r

    if i.get('out')=='con':
        ck.out("Removed deployed soft and env entries for {} plugins".format( plugin_type if plugin_type else 'optimizer and ansatz') )

    return {'return': 0}


def run(i):
    """
    Input:  {
                (sample_size)       - number of "shots" to use in each quantum program execution
                (max_iterations)    - a (soft) limit on the number of optimizer's iterations
                (repetitions)       - a number of times to run the whole optimizer convergence experiment (for stats)
                (provider)          - 'ibm' (default) or 'rigetti'
                (device)            - which simulator or quantum device to run the whole experiment on (interactive by default)
                (timestamp)         - when the experiment was started (normally generated automatically)
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    timestamp   = i.get('timestamp')

    if not timestamp:       # Get current timestamp:
        r=ck.get_current_date_time({})
        if r['return']>0: return r
        timestamp   = r['iso_datetime'].split('.')[0].replace(':', '_').replace('-', '_')   # cut to seconds' resolution

    username       = getpass.getuser()
    sample_size    = i.get('sample_size', 100)
    max_iterations = i.get('max_iterations', 80)
    repetitions    = i.get('repetitions', 3)

    provider    = i.get('provider', 'ibm').lower()              # 'ibm' (default) or 'rigetti'
    q_device      = i.get('device')

    if not q_device:
        device_options = {
            'ibm':      ['local_qasm_simulator', 'ibmq_qasm_simulator', 'ibmqx4'],
            'rigetti':  ['QVM', '8Q-Agave'],
        }[provider]

        select_adict = {'action': 'select_string',
                        'module_uoa': 'misc',
                        'options': device_options,
                        'default': '0',
                        'question': 'Please select the target device',
        }
        r=ck.access( select_adict )
        if r['return']>0:
            return r
        else:
            q_device = r['selected_value']

    program     = {
        'ibm':      'qiskit-vqe',
        'rigetti':  'rigetti-vqe2',
    }[provider]

    opath_adict = { 'action':       'plugin_path',
                    'module_uoa':   'vqe',
                    'type':         'optimizer',
    }
    r=ck.access( opath_adict )
    if r['return']>0: return r
    optimizer_tag   = os.path.basename( r['plugin_dir'] )

    apath_adict = { 'action':       'plugin_path',
                    'module_uoa':   'vqe',
                    'type':         'ansatz',
    }
    r=ck.access( apath_adict )
    if r['return']>0: return r
    ansatz_tag      = os.path.basename( r['plugin_dir'] )

    record_uoa  = '{}-{}-{}-{}-{}-samples.{}-repetitions.{}'.format(username, timestamp, q_device, ansatz_tag, optimizer_tag, sample_size, repetitions)
    record_cid  = 'local:experiment:{}'.format(record_uoa)

    ck.out('Will be recording the results into {}\n'.format(record_cid))

    load_adict = {  'action':           'load',
                    'module_uoa':       'program',
                    'data_uoa':         program,
    }
    r=ck.access( load_adict )
    if r['return']>0: return r

    program_entry_path  = r['path']
    stream_file_path    = os.path.join( program_entry_path, 'tmp', 'vqe_stream.json')

    try:
        os.remove( stream_file_path )   # the data is appended to it by each iteration, so this file has to be cleaned-up before benchmarking
    except OSError:
        pass

    benchmark_adict = {'action':                'benchmark',
                'module_uoa':                   'program',
                'data_uoa':                     program,
                'repetitions':                  repetitions,
                'record':                       'yes',
                'record_repo':                  'local',
                'record_uoa':                   record_uoa,
                'tags':                         ','.join(['qck', 'quantum', hackathon_tag, username, q_device, ansatz_tag, optimizer_tag]),
                'env.VQE_SAMPLE_SIZE':          sample_size,
                'env.VQE_MAX_ITERATIONS':       max_iterations,
                'env.VQE_QUANTUM_BACKEND':      q_device,
                'skip_freq':                    'yes',
    }

    r=ck.access( benchmark_adict )
    if r['return']>0: return r

    ck.out('The results have been recorded into {}\n'.format(record_cid))

    return r


def pick_an_experiment(i):
    """
    Input:  {
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    search_adict = {'action':       'search',
                    'repo_uoa':     'local',
                    'module_uoa':   'experiment',
                    'data_uoa':     '*',
                    'tags':         'qck',
    }
    r=ck.access( search_adict )
    if r['return']>0: return r

    all_experiment_names = [ '{repo_uoa}:{module_uoa}:{data_uoa}'.format(**entry_dict) for entry_dict in r['lst']]

    number_of_experiments = len(all_experiment_names)
    select_adict = {'action': 'select_string',
                    'module_uoa': 'misc',
                    'options': all_experiment_names,
                    'default': str(number_of_experiments-1),
                    'question': 'Please select the experiment entry',
    }
    r=ck.access( select_adict )
    if r['return']>0:
        return r
    else:
        cid = r['selected_value']

    return {'return':0, 'cid': cid}


def upload(i):
    """
    Input:  {
                (cids[])            - CIDs of entries to upload (interactive by default)
                (team)              - team name to be added to meta_data on upload (interactive by default)
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    cids                = i.get('cids')
    team_name           = i.get('team')
    update_meta_dict    = { 'team': team_name } if team_name else {}

    if len(cids)==0:
        r=ck.access( {'action': 'pick_an_experiment', 'module_uoa': 'vqe'} )

        if r['return']>0: return r
        cids = [ r['cid'] ]

    if not team_name:
        r = ck.inp({'text': "Your team name: "})
        team_name = r['string']

    transfer_adict = {  'action':               'transfer',
                        'module_uoa':           'misc',
                        'cids':                 cids,                       # 'ck transfer' will perform its own cids->xcids parsing
                        'target_server_uoa':    'remote-ck',
                        'target_repo_uoa':      hackathon_remote_repo,
                        'update_meta_dict':     update_meta_dict,           # extra meta data added during the transfer
    }
    r=ck.access( transfer_adict )
    if r['return']>0: return r

    ck.out('Uploaded by {}'.format(team_name))
    return {'return': 0}


def time_to_solution(i):
    """
    Input:  {
                (cids[])            - CIDs of entries to compute the TTS metric for (interactive by default)
                (delta)             - delta parameter of TTS metric
                (prob)              - probability parameter of TTS metric
                (which_fun)         - 'fun_exact', 'fun_validated' or 'fun'
                (which_time)        - 'total_q_shots' or 'total_q_seconds'
                (show_more)         - more verbose if 'yes'
            }

    Output: {
                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

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
        return { 'return': 1, 'error': "Cannot parse CID '{}'".format(cid) }
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


def list_registered_emails(i):
    """
    Input:  {
            }

    Output: {
                emails              - a sorted list of unique registered email addresses

                return              - return code =  0, if successful
                                                  >  0, if error
                (error)             - error text if return > 0
            }
    """

    entry_address = {
        'repo_uoa':         'remote-ck',
        'module_uoa':       'experiment',
        'data_uoa':         'quantum_coin_flip',
        'remote_repo_uoa':  'ck-quantum-hackathons',    # TODO: this may need changing in future
    }

    list_points_adict = {   'action': 'list_points' }
    list_points_adict.update( entry_address )
    r=ck.access( list_points_adict )
    if r['return']>0: return r

    point_ids = r['points']

    emails = []
    for point_id in point_ids:
        load_point_adict = {    'action':           'load_point',
                                'point':            point_id,
        }
        load_point_adict.update( entry_address )
        r=ck.access( load_point_adict )
        if r['return']>0: return r

        email = r['dict']['0001']['characteristics_list'][0]['run']['email']

        emails.append(email)

    emails = sorted(set(emails))

    if i.get('out')=='con':
        ck.out("Unique registered emails:")
        for email in emails:
            ck.out('- ' + email)

    return {'return': 0, 'emails': emails }
