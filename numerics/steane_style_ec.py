import stim
import sinter
from small_color_codes._noise import NoiseModel
import numpy as np
from typing import List
from stimbposd import SinterDecoder_BPOSD
import sys
import matplotlib.pyplot as plt

from sinter import Decoder, CompiledDecoder
from typing import Dict

from small_color_codes.sinter_lut import SinterLutDecoder


def encoding_circuit(basis: str, qubits) -> stim.Circuit:
    """basis 'X" to prep |+> and 'Z' to prep |0>"""
    circ = stim.Circuit()
    circ.append("R", qubits, tag="no_noise")
    circ.append("TICK")
    circ.append("H", [qubits[0], qubits[1], qubits[3]], tag="no_noise")
    circ.append("I", [qubits[2], qubits[4],
                qubits[5], qubits[6]], tag="no_noise")
    circ.append("TICK")
    circ.append("CNOT", [qubits[0], qubits[4], qubits[1],
                qubits[2], qubits[3], qubits[5]], tag="no_noise")
    circ.append("I", [qubits[6]], tag="no_noise")
    circ.append("TICK")
    circ.append("CNOT", [qubits[0], qubits[6], qubits[3],
                qubits[4], qubits[1], qubits[5]], tag="no_noise")
    circ.append("I", [qubits[2]], tag="no_noise")
    circ.append("TICK")
    circ.append("CNOT", [qubits[0], qubits[2],
                qubits[5], qubits[6]], tag="no_noise")
    circ.append("I", [qubits[1], qubits[3], qubits[4]], tag="no_noise")
    circ.append("TICK")
    if basis == "X":
        circ.append("H", qubits, tag="no_noise")
        circ.append("TICK")
    return circ


decoder_settings = {
    "max_bp_iters": 1,
    "bp_method": "minimum_sum",
    "osd_order": 0,
    "osd_method": "osd0"}


def sinter_decoders() -> Dict[str, Decoder]:
    return {"bposd": SinterDecoder_BPOSD(**decoder_settings), "lut": SinterLutDecoder()}


def steane_ec_x_stabilizers(circ: stim.Circuit, detectors: bool = False) -> stim.Circuit:
    qubits = [i for i in range(7, 14)]

    circ += encoding_circuit("Z", qubits)
    for i, j in zip(range(7, 14), range(0, 7)):
        circ.append("CNOT", [i, j])
        circ.append("TICK")
    circ.append("H", [i for i in range(7, 14)])
    circ.append("TICK")
    circ.append("MZ", [i for i in range(7, 14)])
    if detectors:
        # , stim.target_rec(-10), stim.target_rec(-24)])
        circ.append("DETECTOR", [
                    stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-3), stim.target_rec(-4)])
        # , stim.target_rec(-9), stim.target_rec(-23)])
        circ.append("DETECTOR", [
                    stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-5), stim.target_rec(-6)])
        circ.append("DETECTOR", [
                    stim.target_rec(-7), stim.target_rec(-5), stim.target_rec(-3), stim.target_rec(-1)])
    circ.append("TICK")
    return circ


def steane_ec_z_stabilizers(circ: stim.Circuit, detectors: bool) -> stim.Circuit:
    qubits = [i for i in range(7, 14)]
    circ += encoding_circuit("X", qubits)
    for i, j in zip(range(0, 7), qubits):
        circ.append("CNOT", [i, j])
        circ.append("TICK")
    circ.append("MZ", qubits)
    if detectors:
        # , stim.target_rec(-10), stim.target_rec(-24)])
        circ.append("DETECTOR", [
                    stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-3), stim.target_rec(-4)])
        # , stim.target_rec(-9), stim.target_rec(-23)])
        circ.append("DETECTOR", [
                    stim.target_rec(-1), stim.target_rec(-2), stim.target_rec(-5), stim.target_rec(-6)])
        circ.append("DETECTOR", [
                    stim.target_rec(-7), stim.target_rec(-5), stim.target_rec(-3), stim.target_rec(-1)])
    return circ


def build_circuit():
    circ = stim.Circuit()
    circ.append_from_stim_program_text("""
    QUBIT_COORDS(0, 1) 0
    QUBIT_COORDS(0, 2) 1
    QUBIT_COORDS(1, 0) 2
    QUBIT_COORDS(1, 1) 3
    QUBIT_COORDS(1, 2) 4
    QUBIT_COORDS(2, 1) 5
    QUBIT_COORDS(2, 2) 6""")
    data_qubits = [i for i in range(7)]
    circ = encoding_circuit("Z", data_qubits)
    circ = steane_ec_x_stabilizers(circ, detectors=True)
    circ = steane_ec_z_stabilizers(circ, detectors=True)

    circ.append("MZ", data_qubits)

    circ.append("DETECTOR", [stim.target_rec(-1*j)
                for j in [1, 2, 3, 4]]),  # 8,9,10,11]])
    circ.append("DETECTOR", [stim.target_rec(-1*j)
                for j in [1, 2, 5, 6]]),  # 8,9,12,13]])
    circ.append("DETECTOR", [stim.target_rec(-1*j)
                for j in [7, 5, 3, 1]])  # 14,12,10,8]])
    circ.append("OBSERVABLE_INCLUDE", [stim.target_rec(-7),
                                       stim.target_rec(-6), stim.target_rec(-5)], 0)

    return circ


if __name__ == "__main__":
    def build_noisy_circuit(per):
        circ = build_circuit()
        noise_model = NoiseModel.ionq_depolarizing(p=float(per))
        noisy_circuit = noise_model.noisy_circuit(circ)

        return noisy_circuit

    test_circuit = build_noisy_circuit(1e-4)
    print("distance:", len(test_circuit.search_for_undetectable_logical_errors(dont_explore_detection_event_sets_with_size_above=100,
                                                                               dont_explore_edges_with_degree_above=100,
                                                                               dont_explore_edges_increasing_symptom_degree=False)))

    min_p = -4
    max_p = -2
    tasks = [
        sinter.Task(
            circuit=build_noisy_circuit(p),
            json_metadata={'p': p}
        )
        for p in np.logspace(min_p, max_p, 10)
    ]

    collected_stats: List[sinter.TaskStats] = sinter.collect(
        num_workers=10,
        tasks=tasks,
        decoders=['bposd', 'lut'],
        max_shots=1_000_000,
        max_errors=100,
        custom_decoders=sinter_decoders(),
        print_progress=True,
    )

    fig, ax = plt.subplots(1, 1)
    sinter.plot_error_rate(
        ax=ax,
        stats=collected_stats,
        x_func=lambda stat: stat.json_metadata['p'],
        group_func=lambda stat: stat.decoder,
        plot_args_func=lambda index, curve_id: {'color': 'red'
                                                if curve_id == 'bposd'
                                                else 'blue'}

    )
    ax.plot(
        [10**min_p, 10**max_p],
        [10**min_p, 10**max_p],
        linestyle='--',
        color='black',
        label='y=x'
    )

    ax.set_xlim(10**min_p, 10**max_p)
    ax.loglog()
    ax.set_title("Steane Code Steane Style Error Correction")
    ax.text(
        1e-6, 2e-3,
        f"max_bp_iters: {decoder_settings['max_bp_iters']}\nosd_order: {decoder_settings['osd_order']}",
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
    )
    ax.set_xlabel("Phyical Error Rate")
    ax.set_ylabel("Logical Error Rate per Round")
    ax.grid(which='major')
    ax.grid(which='minor')
    ax.legend()
    fig.set_dpi(120)  # Show it bigger
    plt.show()
