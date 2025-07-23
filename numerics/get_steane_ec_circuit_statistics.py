

from d3_color_codes.code_blocks.steane_code import noiseless_7_1_3_code_circuits
import stim
import numpy as np


def stim_circ_statistics(circ: stim.Circuit):
    """Prints the number of qubits, measurements, and ticks in a stim circuit."""
    n_resets = 0
    n_hadamards = 0
    n_cnots = 0
    for op in circ:

        if op.name == "R":
            n_resets += len(op.targets_copy())
        if op.name == "H":
            n_hadamards += 1
        if op.name == "CX":
            n_cnots += 1
    print(n_resets, 'resets')
    print(n_hadamards, 'hadamards')
    print(n_cnots, 'CNOTs')
    print(circ.num_qubits, 'qubits')
    print(circ.num_measurements, 'measurements')
    print(circ.num_ticks, 'ticks')


def get_steane_ec_circuit_statistics(code):
    if code == "16_4_3":
        noiseless_circuits = noiseless_7_1_3_code_circuits()

    circ = stim.Circuit()
    circ += noiseless_circuits.ancilla_logical_plus_init
    circ += noiseless_circuits.steane_ec_z_stabilizers
    circ += noiseless_circuits.ancilla_logical_0_init
    circ += noiseless_circuits.steane_ec_x_stabilizers
    stim_circ_statistics(circ)

# def get_shor_ec_circuit_statistics(code):
 #   pass

# BB30_4_5


def create_css_matrices(l, m, A_terms, B_terms):
    """Create CSS code matrices H_X and H_Z."""

    I_ell = np.identity(l, dtype=int)
    I_m = np.identity(m, dtype=int)
    A = 0
    for i in range(len(A_terms)):
        xp = np.kron(np.roll(I_ell, A_terms[i][0], axis=1), I_m)
        yp = np.kron(I_ell, np.roll(I_m, A_terms[i][1], axis=1))
        A += np.dot(xp, yp)

    B = 0
    for i in range(len(B_terms)):
        xp = np.kron(np.roll(I_ell, B_terms[i][0], axis=1), I_m)
        yp = np.kron(I_ell, np.roll(I_m, B_terms[i][1], axis=1))
        B += np.dot(xp, yp)

    # H_X and H_Z
    H_X = np.hstack((A, B))
    H_Z = np.hstack((B.T, A.T))
    return H_X, H_Z


# first code [[30,4,5]] by https://arxiv.org/abs/2503.22071
l1, m1 = 5, 3
# polynomials, written as [(x,y),(x,y),...]
# ['x0', 'x1'],['y0', 'y1', 'u2']

A1 = [(0, 0), (1, 0)]
B1 = [(0, 0), (0, 1), (2, 2)]

H_X1, H_Z1 = create_css_matrices(l1, m1, A1, B1)

print(H_X1, H_Z1)
# get_steane_ec_circuit_statistics("16_4_3")
# get_shor_ec_circuit_statistics("")
