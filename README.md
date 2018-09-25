# Hackaton with London Quantum Computing Meetup

* [6 October 2018](https://www.meetup.com/London-Quantum-Computing-Meetup/events/254156028/) (**"sold out"!**)

## Preparation before the hackathon (this will win you valuable time on the day!)

### Obtain your IBM Quantum Experience API token

Please register at [Quantum Experience](https://quantumexperience.ng.bluemix.net/qx/signup) and copy your API token from the ["Advanced"](https://quantumexperience.ng.bluemix.net/qx/account/advanced) tab (click on the "Regenerate" button first).

### Follow the instructions to [install CK-QISKit](https://github.com/ctuning/ck-qiskit)



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

#### Edit the deployed ansatz plugin
```
$ vi `ck plugin_path vqe --type=ansatz`
```
**NB:** The ansatz plugin is written in Python with QISKit.

### TODO: Review and send us the results of your experiments
```
$ ck list local:experiment:*                                # the list of all of your experimental entries
$ ck find local:experiment:*                                # where the directories are located
$ ck list_points local:experiment:my_experiment_1
$ ck transfer misc local:experiment:my_experiment_256 --target_server_uoa=remote-ck --target_repo_uoa=ck-quantum-hackathon-20181006  # share your best result with us
```
