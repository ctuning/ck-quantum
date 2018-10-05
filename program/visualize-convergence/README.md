# A progress monitoring tool for ck run vqe

This tool provides a text-mode graph for showing the progress of CK VQE optimisation runs.

## USAGE

```
./graph.py [PATH]
```

Normally this is run without the PATH option. This runs `ck load program:qiskit-vqe --out=json` to find the ck run output file, and monitors it for updates and resets. This program can be run before or after your `ck run vqe` command, and does not need to be restarted for new runs.

The PATH option overrides this file location mechanism.

## UI

The top half displays the energy that your optimiser has achieved as a function of iteration. The current run is shown as a filled dot, and prior runs are shown as unfilled dots.

The stats window shows some relatively self-explanatory metastatistics about your optimisation progress.

# Software used

This program uses asciiplot/AP by mfouesneau, available at https://github.com/mfouesneau/asciiplot. The version contained here has been ported to Pytohn3 using the 2to3 tool.
