#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#

import os

##############################################################################

def version_cmd(i):

    full_path       = i.get('full_path')
    plugin_name     = os.path.basename( os.path.dirname( full_path ) )
    plugin_suffix   = plugin_name.split('.', 1)[1]

    return {'return':0, 'cmd':'', 'version': plugin_suffix }


##############################################################################

def setup(i):
    """
    Input:  {
                cus/full_path       - the path of the found python file (or directory if "soft_can_be_dir")

                cus/soft_can_be_dir - set to "yes" if you are looking for a directory, not a regular file

                cus/required_depth  - how many EXTRA STEPS to ascend (in addition to the 1 for a regular file and 0 for a directory)

                env                 - environment variables that we are supposed to fill in (passed by reference)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    cus                     = i.get('customize',{})
    full_path               = cus.get('full_path','')
    soft_can_be_dir_bool    = cus.get('soft_can_be_dir', '')=='yes'
    type_dependent_depth    = 0 if soft_can_be_dir_bool else 1
    total_depth             = cus.get('required_depth', 0) + type_dependent_depth

    # Ascend as many steps as required:
    #
    path_lib                = full_path
    for _ in range(total_depth):
        path_lib            = os.path.dirname( path_lib )

    # Detect the platform:
    #
    hosd                    = i['host_os_dict']
    tosd                    = i['target_os_dict']
    winh                    = hosd.get('windows_base','')

    # Extend PYTHONPATH depending on the platform:
    #
    env                     = i['env']
    env['PYTHONPATH']       = path_lib + ( ';%PYTHONPATH%' if winh=='yes' else ':${PYTHONPATH}')

    return {'return':0, 'bat':''}
