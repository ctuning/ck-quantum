## Installation (on Ubuntu)

### Install global prerequisites, Python3 and its pip (Python2 is also supported)

```
$ sudo apt-get install python3 python3-pip
```

### Install Collective Knowledge

```
$ sudo pip3 install ck
```


## Installation (on MacOS)

### Install Python3 and its pip (Python2 is also supported)

```
$ brew update
$ brew reinstall python
```

```
$ pip install ck
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
$ ck pull repo:ck-env
$ ck pull repo:ck-quantum
$ ck pull repo:ck-rigetti
$ ck pull repo:ck-qiskit
```

### Detect a Python interpreter (interactively choose one if there are several options)
```
$ ck detect soft:compiler.python
```


### Install this CK repository with all its dependencies (other CK repos to reuse artifacts)

```
$ ck install package:tool-hackathon
```

### Install pyQuil

```
$ ck install package:lib-pyquil-1.9.0
```

### Run a demo program (press Enter if prompted)

```
$ ck run program:pyquil-demo
...

    * tmp-stdout.tmp

      Number of games: 10
      Q's winning average: 1.0
      Picard's flip-decision average: 0.5
```

### Run VQE

```
$ ck run program:rigetti-vqe
```

### Benchmark VQE

```
$ ck benchmark program:rigetti-vqe --repetitions=3 \
  --record --record_repo=local --record_uoa=<email>[-<plaform>] \
  --tags=qck,hackathon-2018_06_15,<email>,<platform>,<minimizer_method> \
  --env.RIGETTI_QUANTUM_DEVICE=<platform> \
  --env.VQE_MINIMIZER_METHOD=<minimizer_method> \
  --env.VQE_SAMPLE_SIZE=<sample_number> \
  --env.VQE_MAX_ITERATIONS=<max_iterations>
```
where:
- `email`: a valid email address;
- `platform`: `8Q-Agave` or `QVM`;
- `minimizer_method`: `my_melder_nead` or `my_cobyla` or `my_minimizer` (as defined in [optimizers.py](https://github.com/ctuning/ck-quantum/blob/master/package/tool-hackathon/hackathon-src/hackathon/optimizers.py) installed under e.g. `$CK_TOOLS/hackathon-1.0-linux-64/lib/hackathon`);
- `sample_size`: e.g. `100` (but no more than 200 please);
- `max_iterations`: e.g. `80` (or another cut-off point);
