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

## Non-root CK installation

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

## Test CK installation

```
$ ck version
```

## Common part of the workflow installation

### Pull CK repositories

```
$ ck pull repo:ck-quantum
$ ck pull repo:ck-env
$ ck pull repo:ck-qiskit
```

### Run a Qiskit test that will also install necessary components (agree with most defaults by pressing Return at the prompt)
```
$ ck run program:qiskit-demo --cmd_key=hello
```

### Deploy an optimizer plugin (one that just works)
```
$ ck deploy_optimizer vqe --value=optimizer.cobyla
```

### Deploy an ansatz plugin (one that just works)
```
$ ck deploy_ansatz vqe --value=ansatz.tiny1
```

### Benchmark Qiskit-VQE with the selected optimizer and ansatz
```
$ ck run vqe
```

## Tweaking of VQE

### Extra options of the "run" command
```
$ ck run vqe \
  --sample_size=100 \
  --max_iter=80 \
  --repetitions=3
```

## Working with deployable plugins

### See which plugins are deployed (both "soft" and "env" entries)
```
$ ck search --tags=deployed
```

### Remove all plugins
```
$ ck cleanup vqe
```

### Select an optimizer plugin to deploy
```
$ ck deploy_optimizer vqe
```

### Select an ansatz plugin to deploy
```
$ ck deploy_ansatz vqe
```

### Edit the deployed optimizer (written in python) or the deployed ansatz plugin (written in python using Qiskit)
```
$ vi `ck plugin_path vqe --type=optimizer`

$ vi `ck plugin_path vqe --type=ansatz`
```

### View and send us experimental results (unfinished)
```
$ ck list local:experiment:*
$ ck find local:experiment:*
$ ck list_points local:experiment:<email>
$ ck zip local:experiment:* --archive_name=$HOME/<email>.zip
```
