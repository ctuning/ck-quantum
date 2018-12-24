# 1st Open Quantum Collective Knowledge Challenge

We are excited to announce the 1st Open Quantum Collective Knowledge (QCK)
Challenge! In this challenge, you are invited to find the closest
approximation to the ground state energy of a chemical molecule by running the
hybrid (quantum+classical) VQE algorithm on either a physical device or a
software simulator.  Please read our engaging [VQE and
You](https://github.com/ctuning/ck-quantum/wiki/VQE-and-You) guide for more
information on VQE.

In each experiment, you can select the **target quantum device** to run
the experiment on, the **molecule** to work with (the task), the **optimizer
method** (the classical component of VQE), the **ansatz function** (the quantum
component of VQE), and tune some parameters of the above.

Once your experiment is completed, you can check the [Time-To-Solution
evaluation
metric](https://github.com/ctuning/ck-quantum/tree/master/module/challenge.vqe#check-the-time-to-solution-metric)
(the lower the better!), [upload your
results](https://github.com/ctuning/ck-quantum/tree/master/module/challenge.vqe#upload-your-experimental-results-to-quantum-collective-knowledge)
to the QCK server and finally view them on the [interactive QCK
dashboard](http://cknowledge.org/dashboard/challenge.vqe)!

Importantly, via the dashboard you can quickly check solutions contributed by
others and draw inspiration for further improvements. For example, you may notice that
someone else has made significant progress by using an interesting quantum
ansatz. You are invited, indeed encouraged, to combine that ansatz with your
own ideas e.g. on designing a classical optimizer!  That's what we mean by Quantum **Collective** Knowledge! (Please just provide a reference
if you build upon another solution.)

To the best of our knowledge, the 1st QCK Challenge is indeed the **first**
challenge of its kind.  Therefore, please treat it as work in progress, where
all comments and contributions are very welcome and valuable! If anything at
all is unclear or you spot a clear opportunity for improvement, please (please!
please!!) open a [GitHub issue](https://github.com/ctuning/ck-quantum/issues), or
join our [CK Slack workspace](https://collective-knowledge.slack.com)
`#quantum` channel) and ask your question there!

We are thrilled about collaboratively solving this and future challenges, and
thus making practical and scalable Quantum Computing a reality. Thank you so
much for joining us and... best of luck!

### Small print
- The 1st Open QCK challenged is brought to you by [dividiti](http://dividiti.com) and [Riverlane](http://riverlane.io), with generous support from [Innovate UK](http://innovateuk.org).
- All contributions to QCK are accepted under the [standard CK licence](https://github.com/ctuning/ck/blob/master/LICENSE.txt) (3-clause BSD).
- We gratefully acknowledge support of [IBM](https://www.research.ibm.com/ibm-q/) and [Rigetti](https://www.rigetti.com/) in preparing and running this challenge.
- You can use Rigetti's [Forest SDK](https://www.rigetti.com/forest) under their [terms](https://www.rigetti.com/sdk-terms) and [Quantum Cloud Services](https://www.rigetti.com/qcs) (QCS) under their [terms of service](https://www.rigetti.com/sites/default/files/2018-11/RigettiTermsOfService.pdf). In addition, Rigetti [kindly expand these terms](https://github.com/ctuning/ck-quantum/blob/master/module/challenge.vqe/Rigetti%20--%20Benchmarking%20License%20--%2018.12.16.pdf) to allow you to use QCK for the purpose of benchmarking and publicity in this challenge.
- You can use IBM's [Qiskit SDK](https://qiskit.org/) and [QX platforms](https://quantumexperience.ng.bluemix.net/qx) under their respective terms.


## Getting started

At the moment we are collaborating with IBM and Rigetti to provide access to their hardware and software platforms
for your experiments. As the challenge goes on, we may be able to support more providers.

### Installation instructions
| IBM Quantum Experience | Rigetti Forest |
|-|-|
| [Sign up](https://quantumexperience.ng.bluemix.net/qx/signup) and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (click on the "Regenerate" button first). | [Download the Forest SDK](https://www.rigetti.com/forest). |
| Follow [CK-Qiskit instructions](https://github.com/ctuning/ck-qiskit) to complete and test your setup. | Follow [CK-Rigetti instructions](https://github.com/ctuning/ck-rigetti) to complete and test your setup. Once you are done, do not kill the local QVM server - you will need it during VQE experiments as well! |

### Supported values

| Choice | IBM Quantum Experience | Rigetti Forest |
|-|-|-|
| `<provider>` | `ibm` | `rigetti` |
| `<device>` | `qasm_simulator` (local simulator),<br> `ibmq_qasm_simulator` (remote simulator),<br> `ibmqx4` (a 5-qubit remote device),<br> `ibmq_16_melbourne` (a 16-qubit remote device) | `QVM` (local simulator) |
| `<ansatz>` | `tiny1`, `tiny2`,<br> `universal3`, `universal4`,<br> `reduced_universal5`, `universal6`  | `tiny1`, `tiny2`<br> |
| `<optimizer>` | `cobyla`, `nelder_mead`,<br> `random_sampler`, `custom` | `cobyla`, `nelder_mead`,<br> `random_sampler`, `custom` |

## Select the VQE problem to solve - the Hamiltonian

The problem to be solved (Hydrogen or Helium) is defined by a Hamiltonian plugin, implemented as a standard CK environment.
You can pre-install one or both of them. If more than one is pre-installed, CK will interactively ask you to resolve the ambiguity
when launching the experiments.

Check which Hamiltonians are installed:
```
$ ck show env --tags=quantum,hamiltonian
```

To install a Hamiltonian, run:
```
$ ck detect soft --tags=quantum,hamiltonian
```
and interactively select from the menu.

Remove a Hamiltonian (Helium in this case):
```
$ ck clean env --tags=quantum,hamiltonian.helium
```


## Run VQE once

In order to run VQE we'll need point the system to one optimizer plugin and one ansatz plugin.
While the optimizer (being a classical component of VQE) is provider-neutral,
the ansatz function has to be written with a specific provider in mind.

Here is how to do deploy one plugin of each kind to get VQE running:
```
$ ck deploy_ansatz vqe --provider=<provider> --value=<ansatz>
$ ck deploy_optimizer vqe --value=<optimizer>
```

Then, launch VQE with the deployed optimizer and ansatz:
```
$ ck run vqe --provider=<provider> --device=<device> --repetitions=1
```

For example, to run VQE on Rigetti's local simulator, try:
```
$ ck deploy_optimizer vqe --value=cobyla
$ ck deploy_ansatz vqe --provider=rigetti --value=tiny2
$ ck run vqe --provider=rigetti --device=QVM --repetitions=1
```


## Easy VQE exploration via optimizer parameters

You can explore VQE by varying one or more of the following parameters:
```
$ ck run vqe \
--provider=<provider> \
--device=<device> \
--sample_size=<sample_size> \
--max_iterations=<max_iterations> \
--start_param_value=<start_param_value> \
--repetitions=<repetitions>
```
where:
- consult the table above for the supported values of `<provider>` and `<device>`.
- `<sample_size>`: the number of times to evaluate the Hamiltonian function on the quantum device ("sampling resolution") per optimizer iteration; by default, `100`.
- `<max_iterations>`: the maximum number of optimizer iterations ("iteration limit"); by default, `80`.
- `<start_param_value>`: the starting value of each optimizer's parameter (can be a float number or the word `random`); by default, `random`.
- `<repetitions>`: the number of times to repeat the experiment with the same parameters; by default, `3`.

Once you start you experiment you can [monitor the convergence process](#monitor).

<a name="monitor"></a>
## Monitor the convergence process

To monitor the convergence process, run an ASCII-graphics program in a separate terminal window:
```
$ ck run program:visualize-convergence --env.VQE_QUANTUM_PROVIDER=<provider>
```

## Monitor the convergence process (an ASCII-graphics program run in a separate terminal window)
```
$ ck run program:visualize-convergence --env.VQE_QUANTUM_PROVIDER=<provider>
```

## Check the Time-To-Solution metric

The goal of the challenge is to minimize the [Time-To-Solution](https://github.com/ctuning/ck-quantum/wiki/Measuring-Performance) metric (TTS).
As TTS is proportional to `sample_size`, exploring lower values of `sample_size` may be sensible.
At the same time, a low number of `repetitions` may make it hard to demonstrate solution convergence with a high probability.
For experiments to be uploaded, we recommend using at least 10 repetitions on the simulators and 3-5 repetitions on the hardware.

Run the following and select an experiment entry to compute TTS for:
```
$ ck time_to_solution vqe --delta=0.015 --prob=0.95
```

To compute TTS for a particular experiment, supply its entry name e.g.:
```
$ ck time_to_solution vqe --delta=0.015 --prob=0.8 \
local:experiment:anton-2018_10_05T12_18_19-local_qasm_simulator-ansatz.universal4-optimizer.cobyla-samples.100-repetitions.1
```


## Advanced VQE exploration via plugins

### Check which plugins are deployed (both `soft` and `env` entries)
```
$ ck search --tags=deployed
```

### Removing plugins

#### Removing all deployed plugins (unrestricted)
```
$ ck cleanup vqe
```

#### Removing all deployed optimizer plugins
```
$ ck cleanup vqe --type=optimizer
```

#### Removing all deployed ansatz plugins
```
$ ck cleanup vqe --type=ansatz
```

#### Removing all deployed ansatz plugins for the given provider
```
$ ck cleanup vqe --type=ansatz --provider=<provider>
```

### Working with optimizer plugins

#### Select an optimizer plugin to deploy
```
$ ck deploy_optimizer vqe
```

#### Locate and edit the deployed optimizer plugin (use your favourite text editor instead of `vi`)
```
$ ck plugin_path vqe --type=optimizer
$ vi `ck plugin_path vqe --type=optimizer`
```
**NB:** The optimizer plugin is written in Python.
It is expected to contain only one top-level function.
If you need more, please define them within the top-level one.

### Working with ansatz plugins

#### Select an ansatz plugin to deploy
```
$ ck deploy_ansatz vqe
```

#### Locate and edit the deployed ansatz plugin (use your favourite text editor instead of `vi`)
```
$ ck plugin_path vqe --type=ansatz
$ vi `ck plugin_path vqe --type=ansatz`
```
**NB:** The ansatz plugin is written in Python.
It is expected to contain only one top-level function.
If you need more, please define them within the top-level one.


#### Visualize the ansatz circuit (use your favourite image viewer instead of `display`)

**NB:** Currently only supported for IBM-compatible ansatz circuits.

**NB:** If unsure about the image viewer, try `eog` or `eom` on Linux, `open` on macOS.

```
$ ck run program:visualize-ansatz
$ display `ck find program:visualize-ansatz`/ansatz_circuit.png
```

## Locate the experimental results

You can list all your experimental entries and locate them on disk as follows:
```
$ ck search local:experiment:* --tags=qck
$ ck find local:experiment:*
```

## Upload your experimental results to Quantum Collective Knowledge

When you have an experiment you would like to share, run:
```
$ ck upload vqe --team=schroedinger-cat-herders
```
and select the experiment from the list. We recommend uploading all experiments on the hardware and most successful experiments on the simulators.

Alternatively, upload one or more experiments by using their entries e.g.:
```
$ ck upload vqe --team=bell-state-ringers \
local:experiment:my_experiment_5 local:experiment:my_experiment_13
```
