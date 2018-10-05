# A progress monitoring tool for ck run vqe

This tool provides a text-mode graph for showing the progress of CK VQE optimisation runs.

## USAGE

```
ck run program:visualize-convergence
```

This program helps to visually monitor the convergence of your `ck run vqe` runs.
It can be run before or after your `ck run vqe` command, and does not need to be restarted for new runs.


## UI

The top half displays the energy that your optimiser has achieved as a function of iteration. The current run is shown as a filled dot, and prior runs are shown as unfilled dots.

The stats window shows some relatively self-explanatory metastatistics about your optimisation progress.

To exit the program, press 'q'.

# Software used

This program uses asciiplot/AP by mfouesneau, available at https://github.com/mfouesneau/asciiplot. The version contained here has been ported to Pytohn3 using the 2to3 tool.
