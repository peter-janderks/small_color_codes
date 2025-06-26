from typing import List
import stim
from d3_color_codes._noise import NoiseModel

def encoding_circuit(circ: stim.Circuit, qubits: List[int]) -> stim.Circuit:
    
    """basis 'X" to prep |+> and 'Z' to prep |0>"""
    circ.append("R", qubits)
    circ.append("TICK")
    circ.append("H", [qubits[0], qubits[1], qubits[3]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[0],qubits[4]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[1], qubits[2]])
    circ.append("TICK")
    circ.append("CNOT",[qubits[3], qubits[5]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[0], qubits[6]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[3], qubits[4]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[1], qubits[5]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[0], qubits[2]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[5], qubits[6]])
    circ.append("TICK")
    return circ


def verification_circuit(circ: stim.Circuit, qubits) -> stim.Circuit:

    circ.append("CNOT", [qubits[4], qubits[7]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[2], qubits[7]])
    circ.append("TICK")
    circ.append("CNOT", [qubits[5], qubits[7]])
    circ.append("TICK")
    circ.append("MZ", [qubits[7]])
    circ.append("TICK")

    return circ

def data_logical_initilization( qubits: List, per: float, basis: str) -> stim.Circuit:
    circ = stim.Circuit()
    circ = encoding_circuit(circ, qubits)
    circ = verification_circuit(circ, qubits)
    if basis == "X":
        for q in qubits:
            circ.append("H", q)
            circ.append("TICK")
    noise_model = NoiseModel.ionq_depolarizing(p=float(per))
    noisy_circ = noise_model.noisy_circuit(circ)
    return noisy_circ

def ancilla_logical_initilization(ancilla_qubits: List, per: float, basis) -> stim.Circuit:
    circ = stim.Circuit()
    circ = encoding_circuit(circ, ancilla_qubits)
    circ = verification_circuit(circ, ancilla_qubits)
    if basis == "X":
        for q in ancilla_qubits:
            circ.append("H", q)
            circ.append("TICK")
    noise_model = NoiseModel.ionq_depolarizing(p=float(per))
    noisy_circ = noise_model.noisy_circuit(circ)
    return noisy_circ

def steane_ec_x_stabilizers(per, detectors: bool = False) -> stim.Circuit:
    circ = stim.Circuit()
    qubits = [i for i in range(8, 15)]
    for i,j in zip(qubits, range(0, 7)):
        circ.append("CNOT", [j,i])
        circ.append("TICK")
    for i in qubits:
        circ.append("H")
        circ.append("TICK")
    circ.append("MZ", [i for i in qubits])
    if detectors:
        circ.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-3), stim.target_rec(-4)])
        circ.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-5), stim.target_rec(-6)])
        circ.append("DETECTOR", [stim.target_rec(-7), stim.target_rec(-5), stim.target_rec(-3), stim.target_rec(-1)])
    circ.append("TICK")
    noise_model = NoiseModel.ionq_depolarizing(p=float(per))
    noisy_circ = noise_model.noisy_circuit(circ)
    return noisy_circ

def steane_ec_z_stabilizers(per, detectors: bool = False) -> stim.Circuit:
    circ = stim.Circuit()
    qubits = [i for i in range(8, 15)]
    for i,j in zip(qubits, range(0, 7)):
        circ.append("CNOT", [i, j])
        circ.append("TICK")
    for i in qubits:
        circ.append("H", i)
        circ.append("TICK")

    circ.append("MZ", qubits)
    if detectors:
        circ.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-3), stim.target_rec(-4)])
        circ.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-5), stim.target_rec(-6)])
        circ.append("DETECTOR", [stim.target_rec(-7), stim.target_rec(-5), stim.target_rec(-3), stim.target_rec(-1)])
    circ.append("TICK")
    noise_model = NoiseModel.ionq_depolarizing(p=float(per))
    noisy_circ = noise_model.noisy_circuit(circ)
    return noisy_circ

def final_measurements(per, basis = "Z"):
    #TODO other basis
    circ = stim.Circuit()
    data_qubits = [i for i in range(7)]
    circ.append("MZ", data_qubits)

    circ.append("DETECTOR", [stim.target_rec(-1*j) for j in [1,2,3,4]]),#8,9,10,11]])
    circ.append("DETECTOR", [stim.target_rec(-1*j) for j in [1,2,5,6]]),#8,9,12,13]])
    circ.append("DETECTOR", [stim.target_rec(-1*j) for j in [7,5,3,1]])#14,12,10,8]])
    circ.append("OBSERVABLE_INCLUDE", [stim.target_rec(-7),
               stim.target_rec(-6), stim.target_rec(-5)], 0)
    noise_model = NoiseModel.ionq_depolarizing(p=float(per))
    noisy_circ = noise_model.noisy_circuit(circ)

    return noisy_circ


if __name__ == "__main__":
    pass
#    circ = logical_0_initilization([i for i in range(8)])
 #   print(circ)