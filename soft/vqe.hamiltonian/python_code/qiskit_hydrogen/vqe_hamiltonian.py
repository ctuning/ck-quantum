#!/usr/bin/env python3

"""
    Hydrogen molecule

    Originally packaged with Qiskit's VQE implementation:

    https://github.com/Qiskit/qiskit-terra/blob/master/test/performance/H2/H2Equilibrium.txt
"""

label_to_hamiltonian_coeff = {
    "ZZ":    0.011279956224107712,
    "II":   -1.0523760606256514,
    "ZI":    0.39793570529466216,
    "IZ":    0.39793570529466216,
    "XX":    0.18093133934472627,
}

classical_energy = -1.8572746704950887
