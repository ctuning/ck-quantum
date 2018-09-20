# Hackaton with London Quantum Computing Meetup

* [6 October 2018](https://www.meetup.com/London-Quantum-Computing-Meetup/events/254156028/) (**"sold out"!**)

# Obtain your IBM Quantum Experience API token

Please register at [Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (click on the "Regenerate" button first).

# Install prerequisites and workflows

## Install prerequisites
- Python 3 and [pip](https://pypi.org/project/pip/)
- [QISKit](https://qiskit.org/) (requires Python 3)
- [Collective Knowledge](https://cknowledge.org) (CK)

### Ubuntu
```
$ sudo apt-get install python3 python3-pip
$ sudo apt-get install libblas-dev liblapack-dev
$ sudo python3 -m pip install ck
```

### MacOS
```
$ brew update
$ brew reinstall python
$ python3 -m pip install ck
```

## Install workflows

### Pull CK repositories

```
$ ck pull repo:ck-quantum
```
**NB:** This pulls several dependent CK repositories: `ck-env`, `ck-qiskit` and `ck-rigetti`.

### Run a couple of tests that will install some common dependencies

Run the following to install the software dependencies (accept most defaults by pressing `Enter`/`Return`) and run a simple QISKit test on a local simulator:
```
$ ck run program:qiskit-demo --cmd_key=hello
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --
      The backends available for use are: ['ibmq_qasm_simulator', 'ibmqx2', 'ibmqx4', 'ibmqx5', 'local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      COMPLETED
      {'counts': {'00': 529, '11': 495}}


    * tmp-stderr.tmp



Execution time: 2.077 sec.
```

Run the same test, but this time remotely using [IBM Q Experience](https://quantumexperience.ng.bluemix.net/qx). When prompted, please provide [your API token](https://github.com/ctuning/ck-quantum#obtain-your-ibm-quantum-experience-api-token).

```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_BACKEND=ibmq_qasm_simulator
...
 (printing output files)

    * tmp-stdout.tmp

      -- Ignoring SSL errors.  This is not recommended --
      The backends available for use are: ['ibmq_qasm_simulator', 'ibmqx2', 'ibmqx4', 'ibmqx5', 'local_qasm_simulator', 'local_statevector_simulator', 'local_unitary_simulator']

      COMPLETED
      {'creg_labels': 'cr[2]', 'additionalData': {'seed': 1}, 'time': 0.00130243, 'counts': {'11': 495, '00': 529}, 'date': '2018-09-20T14:29:49.648Z'}


    * tmp-stderr.tmp



Execution time: 10.422 sec.
```


### Deploy an optimizer plugin (one that just works)
```
$ ck deploy_optimizer vqe --value=optimizer.cobyla
```

### Deploy an ansatz plugin (one that just works)
```
$ ck deploy_ansatz vqe --value=ansatz.tiny1
```

### Run QISKit-VQE once with the selected optimizer and ansatz
```
$ ck run vqe --repetitions=1
```

## Easy VQE exploration via optimizer parameters
```
$ ck run vqe --repetitions=10 --sample_size=100 --max_iter=80
```

## Advanced VQE exploration via plugins

### See which plugins are deployed (both `soft` and `env` entries)
```
$ ck search --tags=deployed
```

### Remove all plugins
```
$ ck cleanup vqe
```

### Working with optimizer plugins

#### Select an optimizer plugin to deploy
```
$ ck deploy_optimizer vqe
```

#### Edit the deployed optimizer
```
$ vi `ck plugin_path vqe --type=optimizer`
```
**NB:** The optimizer is written in Python.

### Working with ansatz plugins

#### Select an ansatz plugin to deploy
```
$ ck deploy_ansatz vqe
```

#### Edit the deployed ansatz plugin
```
$ vi `ck plugin_path vqe --type=ansatz`
```
**NB:** The ansatz plugin is written in Python with QISKit.

### TODO: View and send us experimental results
```
$ ck list local:experiment:*
$ ck find local:experiment:*
$ ck list_points local:experiment:<email>
$ ck zip local:experiment:* --archive_name=$HOME/<email>.zip
```
