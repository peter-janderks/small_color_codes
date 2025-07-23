from mqt.qecc.circuit_synthesis.state_prep import gate_optimal_prep_circuit, heuristic_prep_circuit, heuristic_verification_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
from d3_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit
import qiskit
import stim

import numpy as np


Hx = np.zeros((6, 16), dtype=np.int8)
Hx[0, [0, 1, 3, 4]] = 1
Hx[1, [1, 2, 4, 5, 7, 8]] = 1
Hx[2, [3, 4, 6, 7, 10, 11]] = 1
Hx[3, [7, 8, 11, 12, 14, 15]] = 1
Hx[4, [10, 11, 13, 14]] = 1
Hx[5, [5, 8, 9, 12]] = 1

code = CSSCode(3, Hx=Hx, Hz=Hx, n=16)
sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("16_4_3_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 16)
with open("16_4_3_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=False)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("16_4_3_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 16)
with open("16_4_3_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
