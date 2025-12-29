import os
from cirq import NoiseModel
import numpy as np
import stim
from dataclasses import dataclass


def stim_circ_from_file(file_name: str) -> str:
    """Helper function to read a file and return its content."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, "r") as f:
        return stim.Circuit(str(f.read()))


@dataclass
class NoisySteaneECCircuits:
    """Dataclass to hold the noisy circuits for the Steane error correction code."""
    data_logical_init: stim.Circuit
    ancilla_logical_0_init: stim.Circuit
    ancilla_logical_plus_init: stim.Circuit
    steane_ec_z_stabilizers: stim.Circuit
    steane_ec_x_stabilizers: stim.Circuit
    final_measurements: stim.Circuit


class SteaneECCircuits:
    def __init__(self, x_parity_check_matrix, z_parity_check_matrix, x_logicals, z_logicals, file_prefix: str = "", basis: str = "Z"):
        self.n_qubits = x_parity_check_matrix.shape[1]
        self.x_parity_check_matrix = x_parity_check_matrix
        self.z_parity_check_matrix = z_parity_check_matrix
        if basis == 'Z':
            self.logicals = z_logicals
            self.data_logical_init = stim_circ_from_file(
                file_prefix + "data_logical_0_encoding.txt")
        elif basis == 'X':
            self.logicals = x_logicals
            self.data_logical_init = stim_circ_from_file(
                file_prefix + "data_logical_plus_encoding.txt")

        self.ancilla_logical_0_init = stim_circ_from_file(
            file_prefix + "ancilla_logical_0_encoding.txt")
        self.ancilla_logical_plus_init = stim_circ_from_file(
            file_prefix + "ancilla_logical_plus_encoding.txt")
        self.steane_ec_z_stabilizers = self.gen_steane_ec_z_stabilizers()
        self.steane_ec_x_stabilizers = self.gen_steane_ec_x_stabilizers()
        self.final_measurements = self.gen_final_measurements(basis)

    def gen_steane_ec_z_stabilizers(self) -> stim.Circuit:
        circ = stim.Circuit()
        qubits = [i for i in range(self.n_qubits, 2*self.n_qubits)]
        for i, j in zip(range(0, self.n_qubits), qubits):
            circ.append("CNOT", [i, j])
            circ.append("TICK")

        circ.append("MZ", qubits)
        for row in self.z_parity_check_matrix:
            circ.append("DETECTOR", [stim.target_rec(-1*self.n_qubits + j)
                        for j in np.where(row == 1)[0]])
        circ.append("TICK")
        return circ

    def gen_steane_ec_x_stabilizers(self) -> stim.Circuit:
        circ = stim.Circuit()
        qubits = [i for i in range(self.n_qubits, 2*self.n_qubits)]
        for i, j in zip(qubits, range(0, self.n_qubits)):
            circ.append("CNOT", [i, j])
            circ.append("TICK")
        for i in qubits:
            circ.append("H", i)
            circ.append("TICK")
        circ.append("MZ", [i for i in qubits])
        for row in self.x_parity_check_matrix:
            circ.append("DETECTOR", [stim.target_rec(-1*self.n_qubits + j)
                        for j in np.where(row == 1)[0]])
        circ.append("TICK")
        return circ

    def gen_final_measurements(self, basis: str = 'Z') -> stim.Circuit:
        circ = stim.Circuit()
        circ.append("TICK")
        if basis == 'X':
            pcm = self.x_parity_check_matrix
            for i in range(self.n_qubits):
                circ.append("H", i)
                circ.append("TICK")
        else:
            pcm = self.z_parity_check_matrix
        circ.append("MZ", [i for i in range(self.n_qubits)])
        for row in pcm:
            circ.append("DETECTOR", [stim.target_rec(-1*self.n_qubits + j)
                                     for j in np.where(row == 1)[0]])
        for i, row in enumerate(self.logicals):
            circ.append("OBSERVABLE_INCLUDE", [stim.target_rec(-1*self.n_qubits + j)
                                               for j in np.where(row == 1)[0]], i)

        return circ

    def add_noise_to_circuits(self, noise_model: NoiseModel):
        """Adds noise to all circuits in the SteaneCodeCircuits dataclass."""
        return NoisySteaneECCircuits(
            **{
                k: noise_model.noisy_circuit(v)
                for k, v in self.__dict__.items()
                if isinstance(v, stim.Circuit)
            }
        )
