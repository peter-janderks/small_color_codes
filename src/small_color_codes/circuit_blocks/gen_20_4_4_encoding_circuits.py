from mqt.qecc.circuit_synthesis.state_prep import gate_optimal_prep_circuit, heuristic_prep_circuit, heuristic_verification_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
from small_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit

import numpy as np
import webbrowser


H = np.zeros((8, 20))
H[0, [0, 1, 3, 4, 7, 8]] = 1
H[1, [1, 2, 4, 5, 18, 19]] = 1
H[2, [2, 5, 6, 9]] = 1
H[3, [4, 5, 8, 9, 11, 12]] = 1
H[4, [7, 8, 10, 11, 14, 15]] = 1
H[5, [10, 13, 14, 17]] = 1
H[6, [11, 12, 15, 16, 18, 19]] = 1
H[7, [14, 15, 17, 18, 0, 1]] = 1


flag_bool = True
n_qubits = 20
code = CSSCode(4, Hx=H, Hz=H, n=n_qubits)
sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)

circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=flag_bool, max_covering_sets=1e7)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("20_4_4_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 20)
with open("20_4_4_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=flag_bool, max_covering_sets=1e7)


data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("20_4_4_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 20)
with open("20_4_4_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
