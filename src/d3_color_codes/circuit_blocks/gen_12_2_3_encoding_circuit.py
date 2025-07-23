import webbrowser
from mqt.qecc.circuit_synthesis.state_prep import heuristic_prep_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
from d3_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit
import qiskit
import stim

import numpy as np


H = np.zeros((5, 12), dtype=np.int8)
H[0, [0, 1, 4, 5]] = 1
H[1, [1, 2, 5, 6, 9, 10]] = 1
H[2, [2, 3, 6, 7]] = 1
H[3, [4, 5, 8, 9]] = 1
H[4, [6, 7, 10, 11]] = 1

code = CSSCode(3, Hx=H, Hz=H, n=12)


sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("12_2_3_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 12)
with open("12_2_3_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

webbrowser.open(data_circuit.to_crumble_url())

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)
data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("12_2_3_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))
ancilla_circuit = qiskit_to_stim_circuit(circ, 12)
with open("12_2_3_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
