# 4th Quantum Collective Knowledge Hackathon, Oxford, 15 March 2019

* [Eventbrite](https://www.eventbrite.com/e/quantum-computing-hackathon-for-the-space-sector-tickets-53387460331)
* [Collective Knowledge Slack](https://join.slack.com/t/collective-knowledge/shared_invite/enQtNTc3NDEyODAwODgzLTFkNGFmZjJlNDg4MmYwYTUxZWU3ZWFkZmE0ZGVlMThmNWVkNjdiNzMxYmQxZmUzMzQ4YjRiMGVlZjU4YWJkNWU) (#quantum)
* [Presentation slides](https://docs.google.com/presentation/d/1B_3vh0rleKA9HNubEv2x0DfuqqkOqVulWO6N_82dLvY)


1. [Getting started](#getting_started)
    1. [Option A: native installation](#getting_started_native)
    1. [Option B: using a Docker container](#getting_started_docker) (**only use if Option A fails**)
1. [Workflow overview](#workflow_overview)
1. [Problems](#problems)
    1. [Problem 0](#problem0)
    1. [Problem 1](#problem1)
    1. [Problem 2](#problem2)
    1. [Problem 3](#problem3)
    1. [Problem 4](#problem4)
    1. [Problem 5](#problem5)
1. [Sharing solutions](#sharing_solutions)


<a name="getting_started"></a>
# Getting started

<a name="getting_started_native"></a>
## Option A - native installation
With this option, you will install software directly on your computer.

### Installing Python 3.6

Check your Python 3 version:
```
$ python3 --version
```
If you already have Python 3.6.x installed, skip the following section.

#### Ubuntu/Debian
```
$ sudo apt-get install python3 python3-pip
```

#### MacOS X
First, install **[brew](https://brew.sh)** if missing. Then:
```
$ brew update
$ brew unlink python
$ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
$ export PATH=/usr/local/opt/python/bin:$PATH
```
**NB:** We advise you to add the last line into your `.bashrc` config file to avoid having to repeat it in every new terminal window.

#### Windows
Use the [official](https://www.python.org/downloads/windows) downloads and instructions.


### Installing Qiskit and other dependencies to userspace
```
$ python3 -m pip install marshmallow==2.15.0 qiskit==0.7 pandas==0.23.4 sklearn --user
```

### Obtaining the hackathon repository

Choose a directory where you would like to place the [hackathon repository](https://github.com/riverlane/HiddenStateHackathon),
change to that directory and run:
```
$ git clone https://github.com/riverlane/HiddenStateHackathon
```
In what follows, we refer to files in this repository (e.g. `evaluate.py`), so make sure you stay in that directory.

Alternatively, you can download this repository as a [zip](https://github.com/riverlane/HiddenStateHackathon/archive/master.zip) file.
We suggest sticking to using `git`, however, as we may need to provide updates during the hackathon (which you will then be able to obtain via `git pull`).

### Playing with quantum circuit design

To help you learn how quantum circuits work, we have provided a [primer Qiskit program](https://github.com/riverlane/HiddenStateHackathon/blob/master/qiskit_primer.py):
```
$ python3 qiskit_primer.py
```
Feel free to modify it to study the effects of applying quantum circuits to initial states.

### Installing the [Collective Knowledge](http://cknowledge.org) framework (CK) with the Quantum CK repository

1. Follow [these instructions](https://github.com/ctuning/ck#installation).
2. Pull the `ck-quantum` repository and its dependencies:
```
$ ck pull repo:ck-quantum
```

<a name="getting_started_docker"></a>
## Option B - using Docker

With this option, you will obtain all the software in a Docker container tailor-made for this hackathon.

**NB:** The container is over 1 GB, so even if you are comfortable with using Docker we suggest
to stick to [Option A](#getting_started_native) and use [Option B](#getting_started_docker) only as a backup. 

You can check how to install Docker on your system [here](https://docs.docker.com/install).

### Build your Docker image
```
$ docker build --tag hackathon.20190315 https://raw.githubusercontent.com/ctuning/ck-quantum/master/docker/hackathon.20190315/Dockerfile
```

### Run a container from this Docker image
```
$ docker run -it --publish 3355:3344 hackathon.20190315
```

Please note that some commands will have to be run differently if you are using a Docker container.


<a name="workflow_overview"></a>
## Workflow overview

The task repository contains several `*.pyz` files specifying each problem to
solve.  Each of these contains a set of training data - quantum state vectors
labelled by a parity (-1 or 1).  For each problem, you are asked to compose a
quantum circuit which, when applied to each state vector in a test set, can
predict the correct parity label as accurately as possible.

In the first session of the day, we will help you set up your computers and walk through solving [Problem 0](#problem0).
We will also show you how to [share your solutions](#sharing_solutions) by using [Collective Knowledge](http://cknowledge.org).
Next, you will be free to attempt the remaining Problems 1-5 on your own. Each problem is outlined below.

To test your solutions, use `evaluate.py` e.g. as follows:
```
$ python3 evaluate.py --fun discrete_solver --stats --problem discrete_problem1 -n 4
```
This runs your function `discrete_solver` on `discrete_problem1`, using 4 vectors for the training set.
Specific details are outlined below for each problem.

If you use the non-quantum solutions like `classical_svm`, you may want to use more training examples.
The parameter `-n` controls this.

To build quantum circuits, we will use the [Qiskit](https://qiskit.org/) simulator.
Further documentation and examples can be found [here](https://qiskit.org/documentation/summary_of_quantum_operations.html).

For a good overview of quantum circuits and logic gates, check this
[wikipedia page](https://en.wikipedia.org/wiki/Quantum_logic_gate).

<a name="problems"></a>
## Problems

<a name="problem0"></a>
### Problem 0 (`discrete_problem0`)

Number of qubits: 1

There are two state vectors labelled by `1` and `-1`. We need to apply to the
single qubit a quantum circuit that will transform its state to one that will
retrieve the correct labels when measured.

You can look at `manual_solver.py` in the
[`example_solutions`](https://github.com/riverlane/HiddenStateHackathon/tree/master/example_solutions)
directory, and try to come up with a circuit that does this.
(**Hint:** Applying a [Hadamard gate](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate) to
each state should do this.)

To run the solver, type the command:
```
$ python3 evaluate.py --fun manual_solver --problem discrete_problem0
```

<a name="problem1"></a>
### Problem 1 (`discrete_problem1`)

Number of qubits: 2

Now we have two qubits!
The circuit consists of only two gates, one gate for each qubit.
We promise the gates are combinations of [X](https://en.wikipedia.org/wiki/Quantum_logic_gate#Pauli-X_gate) and [H](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate). Your job is to work out which ones.

You can look at `manual_solver.py`, and try to come up with a circuit that does this.
To run this solver, type the command:
```
$ python3 evaluate.py --fun manual_solver --problem discrete_problem1
```

Alternatively, you could look at `discrete_solver.py`, which can help automate the decision.
To run this solver, type the command:
```
$ python3 evaluate.py --fun discrete_solver --problem discrete_problem1
```

<a name="problem2"></a>
### Problem 2 (`discrete_problem2`)

Number of qubits: 2

Now there are multiple gates for each qubit. You will need to try interacting the qubits with one another using
[CNOT gates](https://en.wikipedia.org/wiki/Controlled_NOT_gate).
CNOT gates are only applied to neighbouring qubits, e.g. `qubit_0` -> `qubit_1`, `qubit_1` -> `qubit_0`, `qubit_1` -> `qubit_2`.
You can also use H, X and Y gates.

You can look at `manual_solver.py` and try to come up with a circuit which does this.
To run the solver, type the command:
```
$ python3 evaluate.py --fun manual_solver --problem discrete_problem2
```

It will probably be too annoying and difficult to try all combinations manually.
Try modifying `discrete_solver.py` to include the extra gates needed.
To run this solver, type the command:
```
$ python3 evaluate.py --fun discrete_solver --problem discrete_problem2
```

<a name="problem3"></a>
### Problem 3 (`discrete_problem3`)

Number of qubits: 4

A larger problem with a 2 qubit gate.
There is a single 1-qubit gate (H, X, or Y) on each qubit to start, and then a single CNOT gate linking 2
neighbouring qubits.

You will need to restrict the search to only circuits with 5 gates that have this structure.

You can modify `discrete_solver.py` to begin, but you will notice that the number of combinations is extremely large and so the solver will take a very long time to run. You should write your own solver which exploits the structure given above to reduce the number of circuit possibilities.

In order to do so, you need to know how we have produced the training and test data. We began with a quantum state on which we made a measurement. For the initial states we have chosen, this measurement is always equal to +/-1, and so this gave us a label. We then applied some quantum circuit to the original state to give the quantum state that we are giving you as data.

Therefore, the circuits you have been finding so far are 'undoing' the effect of the circuit we applied in order to get back to the original state. You can now use the information above about the circuit we applied to construct the inverse circuit. You will find it useful to know that all of H, X, Y and CNOT are self-inverse - the effect of each can be 'undone' by applying the same gate again. You will need to think carefully about how to invert a circuit which consists of multiple gates - in which order should the inverse gates be applied?

To run this solver, type the command:
```
$ python3 evaluate.py --fun <SOLVER_FUNCTION> --problem discrete_problem3
```
substituting `<SOLVER_FUNCTION>` for your own.


<a name="problem4"></a>
### Problem 4 (`continuous_problem4`)

Number of qubits: 4

In this problem, we have used gates that we have not considered before – rotation gates. Each gate is parameterised by an angle, which can have any value from 0 to 2 pi. These gates perform rotations of the qubit state in the Bloch sphere.

This problem is based on a "state preperation circuit" for [VQE](https://github.com/ctuning/ck-quantum/wiki/VQE-and-You) used in quantum chemistry.
The circuit is called the [Hardware Efficient Ansatz](https://github.com/ctuning/ck-quantum/wiki/Quantum-Ansatz-Circuits#research-proposal-investigate-the-hardware-efficient-ansatz).
You should use `continuous_solver.py` for this and larger continuous problems, since we are now trying to find a circuit which is a function of continuously varying parameters and not just discrete combinations of fixed gates.
You can try to optimise some parameters, i.e. circuit depth and minimise parameters.

To run this solver, type the command:
```
$ python3 evaluate.py --fun continuous_solver --problem continuous_problem4
```

<a name="problem5"></a>
### Problem 5 (`continuous_problem5`)

Number of qubits: 6

In order to solve this problem you will need to invert the circuit we are giving explicitly:

![problem 5 circuit](https://i.ibb.co/DDLJcF8/Screen-Shot-2019-01-24-at-18-00-17.png)

You need to optimise the rotation parameters. The angles are given above as 0, but can be anything from 0 to 2pi.
You can try and use `continuous_solver.py` but it will not be very efficient. You should make your own function that exploits the structure shown above.

To run this solver, type the command:
```
$ python3 evaluate.py --fun <SOLVER_FUNCTION> --stats --problem continuous_problem5
```
substituting `<SOLVER_FUNCTION>` for your own.


<a name="sharing_solutions"></a>
## Using Collective Knowledge (CK) for viewing and sharing solutions

The main type of objects that CK works with is called a "CK entry".
A "CK entry" is a directory with metadata, optional data and optional code.

You will use CK to:
1. Convert your solutions into CK experiment entries.
1. View your own experiment entries using "the CK dashboard" in the local mode.
1. Upload your CK experiment entries to the [cKnowledge.org](http://cKnowledge.org) server.
1. View everyone's solutions on the common CK dashboard on the server.

### Storing an experiment entry locally

Each run of `evaluate.py` creates a `.json` output file in the current directory.
In order to be counted as a solution, it will have to be first "stored" as a CK entry:
```
$ ck store_experiment qml [--json_file=<json_file_name>] [--team=<schroedinger-cat-herders>]
```

An experiment entry is stored together with the team name.
If you do not specify the JSON file to upload, this command will prompt you to choose one from the current directory.
You can either supply the team name from the command line using the `--team` option or enter it interactively when prompted.

### Viewing your solutions stored locally (WITHOUT DOCKER)

To view your local experiment entries on a local dashboard:
```
$ ck display dashboard --scenario=hackathon.20190315
```
This command will open a browser page and turn itself into a server to that page.
You can leave this server command running in its own terminal and open a new one.
Or you can kill it when the page loads and reclaim the terminal - it's up to you.

### Viewing your solutions stored locally (WITH DOCKER)

To view your local experiment entries on a local dashboard, just follow
[the link to the local dashboard](http://localhost:3355/?template=dashboard&scenario=hackathon.20190315) .

After some loading time you should see your local experiments displayed as data points in your browser.

### Uploading your solutions to the server

In order for your solution to count in the competition, you will have to upload
your best results to the server:
```
$ ck upload qml [ <experiment entries> ]
```

If you do not specify the entries to upload, this command will prompt you to
choose one from a list.  Please note that your competition points will depend
on who uploads their solution to the server faster.  (It is the time on the
server during the upload that counts, not the local time during the run on your
machine.) So please upload as soon as you are ready.

### Viewing all the shared solutions on the server

Visit the [common dashboard](http://cknowledge.org/dashboard/hackathon.20190315).

## That's all folks!

... but you are more than welcome to try our [1st open QCK challenge](https://www.linkedin.com/pulse/first-open-quantum-collective-knowledge-challenge-anton-lokhmotov/)!
