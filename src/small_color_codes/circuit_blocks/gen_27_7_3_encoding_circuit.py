import webbrowser
from mqt.qecc.circuit_synthesis.state_prep import heuristic_prep_circuit, gate_optimal_verification_circuit, heuristic_verification_circuit
from small_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit
from small_color_codes.steane_ecc_circuits import SteaneECCircuits
from small_color_codes.circuit_utils._noise import NoiseModel
import numpy as np
from mqt.qecc.codes.css_code import CSSCode
import os


H = np.zeros((9, 27), dtype=np.int8)
H[0, [0, 1, 3, 4, 6, 7]] = 1
H[1, [4, 5, 7, 8, 10, 11]] = 1
H[2, [6, 7, 9, 10, 12, 13]] = 1
H[3, [10, 11, 13, 14, 16, 17]] = 1
H[4, [12, 13, 15, 16, 18, 19]] = 1
H[5, [16, 17, 19, 20, 22, 23]] = 1
H[6, [18, 19, 21, 22, 24, 25]] = 1
H[7, [22, 23, 25, 26, 1, 0]] = 1
H[8, [24, 25, 1, 2, 4, 5]] = 1

code = CSSCode(3, Hx=H, Hz=H, n=27)


sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)

circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True)


data_circuit = qiskit_to_stim_circuit(circ, 0)

with open("27_9_3_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 27)
with open("27_9_3_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("27_9_3_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 27)
with open("27_9_3_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
webbrowser.open(data_circuit.to_crumble_url())
