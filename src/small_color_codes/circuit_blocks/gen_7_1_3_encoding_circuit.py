import webbrowser
from mqt.qecc.circuit_synthesis.state_prep import gate_optimal_prep_circuit, heuristic_prep_circuit, heuristic_verification_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
from small_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit
import qiskit
import stim

import numpy as np


H = np.zeros((3, 7), dtype=np.int8)
H[0, [0, 1, 3, 4]] = 1
H[1, [1, 2, 4, 5]] = 1
H[2, [3, 4, 5, 6]] = 1

code = CSSCode(3, Hx=H, Hz=H, n=7)


sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("7_1_3_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 7)
with open("7_1_3_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)
data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("7_1_3_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))
ancilla_circuit = qiskit_to_stim_circuit(circ, 7)
with open("7_1_3_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
