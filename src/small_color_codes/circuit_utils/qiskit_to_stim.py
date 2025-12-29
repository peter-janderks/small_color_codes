import qiskit
import stim


def qiskit_to_stim_circuit(qc: qiskit.QuantumCircuit, q_increment: int) -> stim.Circuit:
    """Convert a Qiskit circuit to a Stim circuit.

    Args:
        qc: The Qiskit circuit to convert.
    """
    single_qubit_gate_map = {
        "h": "H",
        "x": "X",
        "y": "Y",
        "z": "Z",
        "s": "S",
        "sdg": "S_DAG",
        "sx": "SQRT_X",
        "measure": "MR",
    }
    stim_circuit = stim.Circuit()
    n_two_qubit_gates = 0
    n_gates = 0
    final_measurements = set()
    stim_circuit.append("R", [q_increment + i for i in range(qc.num_qubits)])
    stim_circuit.append("TICK")
    for gate in qc:
        op = gate.operation.name
        qubit = qc.find_bit(gate.qubits[0])[0] + q_increment
        n_gates += 1
        if op in single_qubit_gate_map:
            if op == "measure":
                final_measurements.add(qubit)
            else:
                stim_circuit.append(
                    single_qubit_gate_map[op], [qubit])
                stim_circuit.append("TICK")

        elif op == "cx":
            target = qc.find_bit(gate.qubits[1])[0] + q_increment
            stim_circuit.append("CX", [qubit, target])
            stim_circuit.append("TICK")
            n_two_qubit_gates += 1
        else:
            msg = f"Unsupported gate: {op}"
            raise ValueError(msg)

    for q in final_measurements:
        stim_circuit.append("M", [q])
    stim_circuit.append("TICK")
    print(f"Number of two-qubit gates: {n_two_qubit_gates}")
    print(f"Total number of gates: {n_gates}")
    return stim_circuit
