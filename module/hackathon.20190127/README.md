# 3rd Quantum Collective Knowledge Hackathon, Paris, 27 January 2019

* [Meetup](https://www.meetup.com/Paris-Quantum-Computing-Technologies/events/256367871) (**upcoming!**)
* Slides (link to Riverlane's slides) - Dropbox shared for reading?


1. [Getting started](#getting_started)
1. [Workflow overview](#workflow_overview)
1. [Problems](#problems)
  1. [Problem 0](#problem0)
  1. [Problem 1](#problem1)

<a name="getting_started"></a>
## Getting started

### Installing Python (>=3.6)

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
$ export PATH=/usr/local/opt/python/bin:$PATH # we suggest to put this into your .bashrc config file to avoid repeating in every terminal window
```

#### Windows
Use [the official downloads and instructions](https://www.python.org/downloads/windows).


### Installing Qiskit and its dependencies to userspace
```
$ python3 -m pip install marshmallow==2.15.0 qiskit==0.7 sklearn --user
```

### Cloning the hackathon task repository
```
$ git clone https://github.com/riverlane/paris
```

### Installing the [Collective Knowledge](http://cknowledge.org) framework (CK) with the Quantum CK repository

1. Follow [these instructions](https://github.com/ctuning/ck#installation).
2. Pull the `ck-quantum` repository and its dependencies:
```
$ ck pull repo:ck-quantum
```

<a name="workflow_overview"></a>
## Workflow overview

The task repository contains several `*.pyz` files specifying each problem to
solve.  Each of these contains a set of training data - quantum state vectors
labelled by a parity (-1 or 1).  For each problem, you are asked to compose a
quantum circuit which, when applied to each state vector in a test set, can
predict the correct parity label as accurately as possible.

In the first session of the day, we will prepare your computers and walk through [Problem 0](#problem0).
Next, you will be free to attempt the remaining Problems 1-5 on your own. Each problem is outlined below.

To test your solutions, use `evaluate.py` e.g. as follows:
```
python3 evaluate.py --fun discrete_solver --stats --problem discrete_problem1 -n 4
```
This runs your function `discrete_solver` on `discrete_problem1`, using 4 vectors for the training set.
Specific details are outlined below for each problem.

If you use the non-quantum solutions like `classical_svm`, you may want to use more training examples.
The parameter `-n` controls this.

To build quantum circuits, we will use the [Qiskit](https://qiskit.org/) simulator.
Further documentation and examples can be found [here](https://qiskit.org/documentation/summary_of_quantum_operations.html).

<a name="problems"></a>
## Problems

<a name="problem0"></a>
### Problem 0 (`discrete_problem0`)

Number of qubits: 1

There are two state vectors labelled by `1` and `-1`. We need to apply to the
single qubit a quantum circuit that will transform its state to one that will
retrieve the correct labels when measured.

You can look at `manual_solver.py` in the
`[example_solutions](https://github.com/riverlane/paris/tree/master/example_solutions)`
directory, and try to come up with a circuit that does this. (**Hint:**
Applying a [Hadamard
gate](https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_(H)_gate) to
each state should do this.)

To run the solver, type the command:
```
python3 evaluate.py --fun manual_solver --problem discrete_problem0
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
python3 evaluate.py --fun manual_solver --problem discrete_problem1
```

Alternatively, you could look at `discrete_solver.py`, which can help automate the decision.
To run this solver, type the command:
```
python3 evaluate.py --fun discrete_solver --problem discrete_problem1
```

### Problem 2

Number of qubits: 2

Now there are multiple gates for each qubit. You will need to try interacting the qubits with one another using
CNOT gates.
CNOT gates are only applied to neighbouring qubits, e.g. qubit_0 -> qubit_1, qubit_1 -> qubit_2.
Other gate combinations you can use: H, X, Y.

You can look at `manual_solver.py` and try to come up with a circuit which does this.
To run the solver type the command: `python3 evaluate.py --fun manual_solver --problem discrete_problem2`

It will probably be too annoying and difficult to manually try all combinations. Try modifying `discrete_solver.py` to include the extra gates needed.
To run this solver type the command: `python3 evaluate.py --fun discrete_solver --problem discrete_problem2`

### Problem 3

Number of qubits: 4

A larger problem with a 2 qubit gate.
There is a single 1-qubit gate (H, X, or Y) on each qubit to start, and then a single CNOT gate linking 2
neighbouring qubits.

You will need to restrict the search to only circuits with 5 gates that have this structure.

You can modify `discrete_solver.py` to begin, but you will notice that the number of combinations is extremely large and so the solver will take a very long time to run. You should write your own solver which exploits the structure given above to reduce the number of circuit possibilities.

In order to do so, you will need to know how we have produced the training and test data. We began with a quantum state on which we made a measurement. For the initial states we have chosen, this measurement is always equal to +/-1, and so this gives us a label. We then applied some quantum circuit to the original state to give the quantum state that we are giving you as data.

Therefore, the circuits you have been finding so far are 'undoing' the effect of the circuit we applied in order to get back to the original state. You can now use the information above about the circuit we applied to construct the inverse circuit. You will find it useful to know that all of H, X, Y and CNOT are self-inverse - the effect of each can be 'undone' by applying the same gate again. You will need to think carefully about how to invert a circuit which consists of multiple gates - in which order should the inverse gates be applied? 

To run this solver type the command: `python3 evaluate.py --fun <SOLVER_FUNCTION> --problem discrete_problem3`,
substituting `<SOLVER_FUNCTION>` for your own.

### Problem 4

Number of qubits: 4

In this problem, we have used gates that we have not considered before – rotation gates. Each gate is parameterised by an angle, which can have any value from 0 to 2 pi. These gates perform rotations of the qubit state in the Bloch sphere.

This problem is based on a "state preperation circuit" for VQE - used in quantum chemistry.
The circuit is called the Hardware Efficent Ansatz and you can see it in `continuous_solver.py`.
You should use the `continuous_solver.py` for this and larger continuous problems as we are now trying to find a circuit which is a function of continuously varying parameters and not just discrete combinations of fixed gates.
You can try to optimise some parameters, i.e. circuit depth and minimize parameters.

To run this solver type the command: `python3 evaluate.py --fun continuous_solver --problem continuous_problem4`

### Problem 5

Number of qubits: 6

In order to solve this problem you will need to invert the circuit we are giving explicitly:

![problem 5 circuit](https://i.ibb.co/DDLJcF8/Screen-Shot-2019-01-24-at-18-00-17.png)

You need to optimise the rotation parameters. The angles are given above as 0, but it can be anything from 0 to 2pi.
You can try and use `continuous_solver.py` but it will not be very efficient. You should make your own function that exploits the structure shown above.

To run this solver type the command: To run this solver type the command: `python3 evaluate.py --fun <SOLVER_FUNCTION>
--stats --problem continuous_problem5`, substituting `<SOLVER_FUNCTION>` for your own.


## Using CK (Collective Knowledge framework) for viewing and sharing the solutions

The main type of object that CK works with is called a "CK entry".
A "CK entry" is a directory with meta-data, optional data and optional code.

You will use CK tools to:
1. convert your solutions into CK experiment entries
1. look at your own entries using "CK Dashboard" in local mode
1. upload your CK experiment entries to the shared server and
1. view everybody's results using a shared CK dashboard on the server.

### Storing an experiment entry locally

Each run of evaluate.py leaves a .JSON output file in the current directory.
In order to be counted as a solution, viewed in context of others and uploaded
it will have to be first "stored" as a CK entry:

```
$ ck store_experiment qml --json_file=<json_file_name> [--team=<schroedinger-cat-herders>]
```

A CK experiment entry is stored together with the team name.
You can either supply it from the command line or enter it interactively at a prompt.

### Viewing the locally stored experiments

To see the local experimental entries on a diagram:
```
$ ck display dashboard --scenario=hackathon.20190127
```
This command will open a browser page and will turn itself into a server to that page.
You can leave this server command running in its own terminal and open a new one.
Or you can kill it when the page loads and reclaim the terminal - your choice.

### Uploading the results to the common shared server

In order for your solution to count in the competition, you will have to upload
your best results to the server:
```
$ ck upload qml [ <experiment entries> ]
```
If you don't specify the entries to upload, this command will prompt you to choose one from a list.
Please note that your competition points will depend on who uploads their solution to the server faster
(the uploading timestamp counts, not the running timestamp). So upload as soon as you are ready.

### Viewing the remotely shared experiments

Visit the [Shared Dashboard page](http://cknowledge.org/dashboard/hackathon.20190127)
