from mqt.qecc.circuit_synthesis.state_prep import  heuristic_prep_circuit, gate_optimal_verification_circuit
from mqt.qecc.codes.css_code import CSSCode
from d3_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit
import numpy as np


H = np.zeros((6, 16), dtype=np.int8)
H[0, [0, 2, 3, 6]] = 1
H[1, [1, 4, 5, 7]] = 1
H[2, [3, 4, 6, 7, 8, 9, 11, 12]] = 1
H[3, [8, 10, 11, 14]] = 1
H[4, [9, 12, 13, 15]] = 1
H[5, [0, 1, 3, 4, 11, 12, 14, 15]] = 1


code = CSSCode(4, Hx=H, Hz=H, n=16)
sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)
sp_circ.error_detection_code = True
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ,  flag_first_layer=True)


data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("16_4_4_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 16)
with open("16_4_4_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
sp_circ.error_detection_code = True
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("16_4_4_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 16)
with open("16_4_4_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
