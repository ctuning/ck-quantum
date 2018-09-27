# Hackaton with London Quantum Computing Meetup

* [6 October 2018](https://www.meetup.com/London-Quantum-Computing-Meetup/events/254156028/) (**"sold out"!**)

## Preparation before the hackathon (this will save you time on the day!)

1. Please register at [Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (click on the "Regenerate" button first).
1. Follow [CK-QISKit instructions](https://github.com/ctuning/ck-qiskit).

## Run QISKit-VQE once

First, deploy a VQE ansatz and optimizer plugins that should just work:
```
$ ck deploy_optimizer vqe --value=optimizer.cobyla
$ ck deploy_ansatz vqe --value=ansatz.tiny1
```

Then, launch VQE with the deployed optimizer and ansatz:
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

#### Visualize the ansatz circuit
```
$ ck run program:visualize-ansatz
$ open `ck find program:visualize-ansatz`/ansatz_circuit.png
```

#### Edit the deployed ansatz plugin
```
$ vi `ck plugin_path vqe --type=ansatz`
```
**NB:** The ansatz plugin is written in Python with QISKit.


## Review the results (e.g. using time-to-solution parametric metric)
```
$ ck search local:experiment:*                                                          # the list of all of your experimental entries
$ ck find local:experiment:*                                                            # where the experiment directories are located
$ ck time_to_solution vqe --delta=0.015 --prob=0.95                                     # TTS (pick the experiment entry interactively)
OR
$ ck time_to_solution vqe local:experiment:my_experiment_10 --delta=0.015 --prob=0.8    # TTS (supply the experiment from command line)
```

## Send us the results of your experiments
```
$ ck upload vqe                                                                     # upload (pick the experiment entry interactively)
OR
$ ck upload vqe local:experiment:my_experiment_5 local:experiment:my_experiment_13  # upload (supply the experiment from command line)
```
