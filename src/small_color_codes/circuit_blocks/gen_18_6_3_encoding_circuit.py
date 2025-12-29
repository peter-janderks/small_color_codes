import webbrowser
from mqt.qecc.circuit_synthesis.state_prep import gate_optimal_prep_circuit, heuristic_prep_circuit, heuristic_verification_circuit, gate_optimal_verification_circuit
# from mqt.qecc.circuit_synthesis.synthesis_utils import qiskit_to_stim_circuit
from mqt.qecc.codes.css_code import CSSCode
import qiskit
import stim

import numpy as np
from small_color_codes.circuit_utils.qiskit_to_stim import qiskit_to_stim_circuit

Hx = np.zeros((6, 18), dtype=np.int8)
# in the first row of the matrix, there should be 1 at indices 0, 1, 4, 5
Hx[0, [0, 1, 3, 4, 6, 7]] = 1
Hx[1, [4, 5, 7, 8, 10, 11]] = 1
Hx[2, [6, 7, 9, 10, 12, 13]] = 1
Hx[3, [10, 11, 13, 14, 16, 17]] = 1
Hx[4, [12, 13, 15, 16, 0, 1]] = 1
Hx[5, [16, 17, 1, 2, 4, 5]] = 1
code = CSSCode(3, Hx=Hx, Hz=Hx, n=18)
print(code.Lx)

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=True)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True)
print(circ,)
data_circuit = qiskit_to_stim_circuit(circ, 0)
webbrowser.open(data_circuit.to_crumble_url())

with open("18_6_3_data_logical_0_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 18)
with open("18_6_3_ancilla_logical_0_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))

sp_circ = heuristic_prep_circuit(code, optimize_depth=False, zero_state=False)
circ = gate_optimal_verification_circuit(
    sp_circ=sp_circ, flag_first_layer=True)

data_circuit = qiskit_to_stim_circuit(circ, 0)
with open("18_6_3_data_logical_plus_encoding.txt", "w") as f:
    f.write(str(data_circuit))

ancilla_circuit = qiskit_to_stim_circuit(circ, 18)
with open("18_6_3_ancilla_logical_plus_encoding.txt", "w") as f:
    f.write(str(ancilla_circuit))
