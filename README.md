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

### Minimal CK installation

The minimal installation requires:

* Python 2.7 or 3.3+ (the limitation is mainly due to unit tests)
* Git command line client

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via `pip` with `sudo` to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

## Common part of the installation

### Detect a Python interpreter (interactively choose one if there are several options)
```
$ ck detect soft:compiler.python
```


### Install this CK repository with all its dependencies (other CK repos to reuse artifacts)

```
$ ck pull repo:ck-quantum
$ ck install package:tool-hackathon
```

### Install pyQuil

```
$ ck pull repo:ck-rigetti
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
