# Paris Quantum Computing Hackathon, 27 January 2019

* [Meetup](https://www.meetup.com/Paris-Quantum-Computing-Technologies/events/256367871) (**upcoming!**)
* Slides (link to Riverlane's slides) - Dropbox shared for reading?
* [Task Repository](https://github.com/riverlane/paris)

## Getting started (ideally done BEFORE the day of the Hackathon to save the precious competition time - feedback welcome)

1. Install python3
1. Install qiskit and its dependencies (reinstall marshmallow 2.15.0 on OSX to avoid being drowned in warnings)
1. A quick test to see that qiskit simulator works
1. Install CK

## The hackathon workflow

### Running evaluate.py (insert multiple examples)

The task repository contains a number of files specifying each problem to solve. Each of these contains a set of
training data - quantum state vectors labelled by a parity. It is your job to compose a quantum circuit which, when
applied to each state vector in a test set, can accurately obtain the correct parity label.

In the first session of the day we will prepare your computers and walk through problem D0. The function manual_solver
is related to this, and can be found in the
[example_solutions](https://github.com/riverlane/paris/tree/master/example_solutions) directory.

Next you will be free to attempt the discrete (D#) and continuous (C#) problem sets. We recommend starting with the
`discrete_solver` and `continuous_solver` functions, repsectively.

In order to test your solutions, use `evaluate.py`. A example use is `python evaluate.py --fun discrete_solver --stats
--problem problem1 --n 4`. This runs your function `discrete_solver` on problem 1, using 4 vectors for the training set.

If you use the non-quantum solutions like `train_svm` you may want to use more training examples. the parameter --n
controls this.

### Problem 0

Number of qubits: 1

This is a single qubit problem.
There are 2 state vectors labelled by 1 and -1. We need to apply a quantum circuit to each qubit which transforms their
state to one which retrieves the correct labels when measured.
Applying a Hadamard gate to each state should do this.

You can look at `manual_solver.py` and try to come up with a circuit which does this.
To run the solver type the command: `python3 evaluate.py --fun manual_solver --stats --problem discrete_problem0`

### Problem 1

Number of qubits: 2

Now we have two qubits!
The circuit consists of only 2 gates, one gate for each qubit.
We promise the gates are combinations of X and H - it's your job to work out which ones.

You can look at `manual_solver.py` and try to come up with a circuit which does this.
To run the solver type the command: `python3 evaluate.py --fun manual_solver --stats --problem discrete_problem1`

Alternatively you could look at `discrete_solver.py`, which can help automate the decision.
To run this solver type the command: `python3 evaluate.py --fun discrete_solver --stats --problem discrete_problem1`

### Problem 2

Number of qubits: 2

Now there are multiple gates for each qubit. You will need to try interacting the qubits with one another using
CNOT gates.
CNOT gates are only applied to neighbouring qubits, e.g. qubit_0 -> qubit_1, qubit_1 -> qubit_2.
Other gate combinations you can use: H, X, Y.

You can look at `manual_solver.py` and try to come up with a circuit which does this.
To run the solver type the command: `python3 evaluate.py --fun manual_solver --stats --problem discrete_problem2`

It will probably be too annoying and difficult to manually try all combinations. Try modifying `discrete_solver.py`.
To run this solver type the command: `python3 evaluate.py --fun discrete_solver --stats --problem discrete_problem2`

### Problem 3

Number of qubits: 4

A larger problem with a 2 qubit gate.
There is a single 1-qubit gate (H, X, or Y) on each qubit to start, and then a single CNOT gate linking 2
neighbouring qubits.

You will need to restrict the search to only circuits with 5 gates that have this structure.

You can modify `discrete_solver.py` to begin, but you will notice that this will not be optimal, so you should create
your own function.
To run this solver type the command: `python3 evaluate.py --fun <SOLVER_FUNCTION> --stats --problem discrete_problem3`,
substituting <SOLVER_FUNCTION> for your own.

### Problem 4

Number of qubits: 4

This problem is based on a "state preperation circuit" for VQE - used in quantum chemistry.
The circuit is called the Hardware Efficent Ansatz and you can see it in `continuous_solver.py`.
You should use the `continuous_solver.py` for this and larger continuous problems.
You can try to optimise some parameters, i.e. circuit depth and minimize parameters.

To run this solver type the command: `python3 evaluate.py --fun continuous_solver --stats --problem continuous_problem4`

### Problem 5

Number of qubits: 6

In order to solve this problem you will need to invert the circuit we are giving explicitly:

                                                      ┌───────┐┌───┐
qr_0: |0>─────────────────────────────────────────────┤ Ry(0) ├┤ H ├
                                             ┌───────┐└───────┘└─┬─┘
qr_1: |0>────────────────────────────────────┤ Rx(0) ├───────────┼──
                                    ┌───────┐└───────┘           │
qr_2: |0>───────────────────────────┤ Rx(0) ├────────────────────┼──
                           ┌───────┐└───────┘                    │
qr_3: |0>──────────────────┤ Rz(0) ├─────────────────────────────┼──
                  ┌───────┐└───────┘                             │
qr_4: |0>─────────┤ Rx(0) ├──────────────────────────────────────┼──
         ┌───────┐└───────┘                                      │
qr_5: |0>┤ Rz(0) ├───────────────────────────────────────────────■──
         └───────┘

You need to optimise the rotation parameters. The angles are given above as 0, but it can be anything from 0 to 2pi.
You can try and use `continuous_solver.py` but it will not be very efficient. You should make your own function.

To run this solver type the command: To run this solver type the command: `python3 evaluate.py --fun <SOLVER_FUNCTION>
--stats --problem continuous_problem5`, substituting <SOLVER_FUNCTION> for your own.


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

Visit [Shared dashboard page](http://cknowledge.org/dashboard/hackathon.20190127) (**upcoming!**)
