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
$ ck pull repo:ck-quantum
$ ck pull repo:ck-env
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
