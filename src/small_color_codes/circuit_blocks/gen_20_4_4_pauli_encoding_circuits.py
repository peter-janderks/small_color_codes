from mqt.qecc.circuit_synthesis.state_prep import gate_optimal_prep_circuit, heuristic_prep_circuit, heuristic_verification_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
from small_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit

import numpy as np
import webbrowser


Hx = np.zeros((8, 20))
Hx[0, [0, 1, 4, 5, 7, 8]] = 1
Hx[1, [1, 2, 5, 6, 18, 19]] = 1
Hx[2, [4, 7, 10, 11]] = 1
Hx[3, [5, 6, 8, 9, 12, 13]] = 1
Hx[4, [7, 8, 11, 12, 14, 15]] = 1
Hx[5, [12, 13, 15, 16, 18, 19]] = 1
Hx[6, [14, 15, 17, 18, 0, 1]] = 1
Hx[7, [16, 19, 2, 3]] = 1

Hz = np.zeros((8, 20))
Hz[0, [0, 1, 4, 5, 7, 8]] = 1
Hz[1, [1, 2, 5, 6, 18, 19]] = 1
Hz[2, [2, 3, 6, 9]] = 1
Hz[3, [5, 6, 8, 9, 12, 13]] = 1
Hz[4, [7, 8, 11, 12, 14, 15]] = 1
Hz[5, [10, 11, 14, 17]] = 1
Hz[6, [12, 13, 15, 16, 18, 19]] = 1
Hz[7, [14, 15, 17, 18, 0, 1]] = 1
n20_k4_d4_pauli = CSSCode(4, Hx=Hx, Hz=Hz, n=20)
sp_circ = heuristic_prep_circuit(
    n20_k4_d4_pauli, optimize_depth=False, zero_state=True)

circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True, find_coset_leaders=True, max_covering_sets=1e7)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("20_4_4_pauli_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 20)
with open("20_4_4_pauli_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(
    n20_k4_d4_pauli, optimize_depth=False, zero_state=False)
circ = heuristic_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True, max_covering_sets=1e7)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("20_4_4_pauli_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 20)
with open("20_4_4_pauli_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
