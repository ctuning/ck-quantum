# Paris Quantum Computing Hackathon, 27 January 2019

* [Meetup](https://www.meetup.com/Paris-Quantum-Computing-Technologies/events/256367871) (**upcoming!**)
* Slides (link to Riverlane's slides) - Dropbox shared for reading?

## Getting started (ideally done BEFORE the day of the Hackathon to save the precious competition time - feedback welcome)

### Install Python 3.6 if it's missing

On Ubuntu:
```
$ sudo apt-get install python3 python3-pip
```

On a Mac:

Install [brew](https://brew.sh) if it is missing.
Then use **brew** to install Python 3.6:

```
$ brew update
$ brew unlink python
$ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
$ export PATH=/usr/local/opt/python/bin:$PATH   # we suggest to put this into your .bashrc config file to avoid repeating in every terminal window
```

### Install qiskit and its dependencies (reinstall marshmallow 2.15.0 on OSX to avoid being drowned in warnings)
```
$ python3 -m pip install marshmallow==2.15.0 qiskit==0.7 --user
```

### Install [Collective Knowledge](http://cknowledge.org) framework

Follow [these instructions](https://github.com/ctuning/ck#installation)

### Clone Riverlane's task repository
```
$ git clone https://github.com/riverlane/paris
```

## The hackathon workflow

### Running evaluate.py (insert multiple examples)

The task repository contains a number of files specifying each problem to solve. Each of these contains a set of
training data - quantum state vectors labelled by a parity (-1 or 1). It is your job to compose a quantum circuit which, when
applied to each state vector in a test set, can accurately obtain the correct parity label.

In the first session of the day we will prepare your computers and walk through problem D0. The function manual_solver
is related to this, and can be found in the
[example_solutions](https://github.com/riverlane/paris/tree/master/example_solutions) directory.

Next you will be free to attempt the discrete (D#) and continuous (C#) problem sets. We recommend starting with the
`discrete_solver` and `continuous_solver` functions, respectively.

In order to test your solutions, use `evaluate.py`. A example use is `python3 evaluate.py --fun discrete_solver --stats
--problem discrete_problem1 -n 4`. This runs your function `discrete_solver` on discrete problem 1, using 4 vectors for the training set.

If you use the non-quantum solutions like `classical_svm` you may want to use more training examples. The parameter -n controls this.

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
