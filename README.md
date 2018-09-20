## Installation (on Ubuntu)

### Install global prerequisites, Python3 and its pip (Python2 is not supported)

```
$ sudo apt-get install python3 python3-pip
```

### Install Collective Knowledge

```
$ sudo python3 -m pip install ck
```


## Installation (on MacOS)

### Install Python3 and its pip (Python2 is not supported)

```
$ brew update
$ brew reinstall python
```

```
$ python3 -m pip install ck
```

## Common part of the workflow installation

### Pull CK repositories

```
$ ck pull repo:ck-quantum
```
This pulls several repositories: `ck-env`, `ck-qiskit` and `ck-rigetti`.


### Run a couple of tests that will install some common dependencies

Run the following to install the software dependencies (accept most defaults by pressing `Enter`/`Return`) and run a simple QISKit test:
```
$ ck run program:qiskit-demo --cmd_key=hello
```

Run the same Qiskit test, but this time remotely (to test the connection with IBM QuantumExperience). Provide your API Token when asked:
```
$ ck run program:qiskit-demo --cmd_key=hello --env.CK_IBM_BACKEND=ibmq_qasm_simulator
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
