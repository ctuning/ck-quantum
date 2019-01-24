#
# CK program template
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os
import json

def run():

    print("CK_ENV_COMPILER_PYTHON_FILE=" + os.environ.get('CK_ENV_COMPILER_PYTHON_FILE',''))
    print("CK_QUANTUM_PARIS_DIR=" + os.environ.get('CK_QUANTUM_PARIS_DIR',''))

    output_path = os.environ.get('CK_QUANTUM_PARIS_OUTPUT')
    print("CK_QUANTUM_PARIS_OUTPUT=" + output_path)
    with open(output_path) as output_file:
        output_raw = json.load(output_file)
        print(str(output_raw))

    return 0

if __name__ == '__main__':
  exit(run())
