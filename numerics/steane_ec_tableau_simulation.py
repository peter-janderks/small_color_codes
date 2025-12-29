#!/usr/bin/env python3

import argparse
import os
from typing import List
from small_color_codes.code_library import get_noiseless_circuits
from small_color_codes.steane_ecc_circuits import SteaneECCircuits

from small_color_codes.lut import LutDecoder
import numpy as np
from small_color_codes.circuit_utils._noise import NoiseModel
import stim
import sinter
import webbrowser
import time
import hashlib


def initialize_until_succes(circ: stim.Circuit, s: stim.TableauSimulator) -> tuple[stim.TableauSimulator, int]:
    n_iterations = 1
    while True:
        s.do(circ)

        if all(x == False for x in s.current_measurement_record()[-1*circ.num_measurements:]):
            break
        else:
            n_iterations += 1

    return (s, n_iterations)


def get_detector_and_observable_values(measurement_record: List[bool], circ: stim.Circuit) -> List[int]:
    detector_values = []
    observable_values = []

    for op in circ:
        if op.name == "DETECTOR":
            detector_values.append(
                sum(measurement_record[i.value] for i in op.targets_copy()) % 2)
        if op.name == "OBSERVABLE_INCLUDE":
            observable_values.append(
                [sum(measurement_record[i.value] for i in op.targets_copy()) % 2])
    return detector_values, observable_values


def simulate_steane_ec(
        noisy_circuits: SteaneECCircuits,
        decoder: LutDecoder) -> stim.TableauSimulator:
    syndrome = []
    observable_values = []
    s = stim.TableauSimulator()
    s, n_1 = initialize_until_succes(noisy_circuits.data_logical_init, s)
    s, n_2 = initialize_until_succes(
        noisy_circuits.ancilla_logical_plus_init, s)
    s.do(noisy_circuits.steane_ec_z_stabilizers)
    new_syndrome, new_obersavable_value = get_detector_and_observable_values(
        s.current_measurement_record(), noisy_circuits.steane_ec_z_stabilizers)
    syndrome.extend(new_syndrome)

    s, _ = initialize_until_succes(noisy_circuits.ancilla_logical_0_init, s)
    observable_values.extend(new_obersavable_value)
    s.do(noisy_circuits.steane_ec_x_stabilizers)
    new_syndrome, new_obersavable_value = get_detector_and_observable_values(
        s.current_measurement_record(), noisy_circuits.steane_ec_x_stabilizers)
    syndrome.extend(new_syndrome)

    s.do(noisy_circuits.final_measurements)
    new_syndrome, new_observable_value = get_detector_and_observable_values(
        s.current_measurement_record(), noisy_circuits.final_measurements)
    syndrome.extend(new_syndrome)
    observable_values.extend(new_observable_value)
    predictions = decoder.decode(np.array(syndrome))

    logical_errors = []

    for prediction, observable_value in zip(predictions, observable_values):

        logical_errors.append(prediction != observable_value[0])

    return logical_errors, observable_value[0]


def calculate_logical_error_rate(per: float,
                                 code: str,
                                 n_trials: int = 1000,
                                 n_errors: int = 100,
                                 basis: str = 'Z',
                                 max_error_weight: int = 3) -> float:
    noiseless_circuits = get_noiseless_circuits(code, basis=basis)
    number_of_logicals = noiseless_circuits.final_measurements.num_observables

    logical_errors = [0 for _ in range(number_of_logicals + 1)]
    noisy_circuits = noiseless_circuits.add_noise_to_circuits(
        NoiseModel.ionq_depolarizing(per))

    circ = stim.Circuit()

    circ += noiseless_circuits.data_logical_init
    circ += noiseless_circuits.ancilla_logical_plus_init
    circ += noisy_circuits.steane_ec_z_stabilizers
    circ += noiseless_circuits.ancilla_logical_0_init
    circ += noisy_circuits.steane_ec_x_stabilizers
    circ += noisy_circuits.final_measurements
    decoder = LutDecoder(circ.detector_error_model(),
                         max_error_weight=max_error_weight)
    total_uncorrected = 0
    for trials in range(n_trials):
        lers, uncorrected = simulate_steane_ec(
            noisy_circuits,
            decoder
        )
        for i in range(number_of_logicals):
            logical_errors[i] += lers[i]
        total_uncorrected += uncorrected

        logical_errors[-1] += int(sum(lers) > 0)
        if logical_errors[-1] == n_errors:
            print('stopping early')
            break
    print(total_uncorrected, 'uncorrected errors in', trials+1, 'trials')
    return trials+1, logical_errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--per', type=float)
    parser.add_argument('--n_trials', type=int, default=1000,
                        help='Number of trials to run for each error rate')
    parser.add_argument('--n_errors', type=int, default=100,
                        help='Number of errors to simulate for each error rate')
    parser.add_argument('--code', type=str,
                        choices=['16_4_3', '18_6_3', '16_4_4', '7_1_3', '27_9_3', '12_2_3', '20_4_4', '20_4_4_pauli'], default='steane')
    parser.add_argument('--save_file', type=str, nargs='+',
                        default='out/circuits')
    parser.add_argument('--basis', type=str, default='Z',)
    parser.add_argument('--max_error_weight', type=int, default=3,
                        help='Maximum error weight for the decoder')
    args = parser.parse_args()

    start_time = time.time()

    trials, lers = calculate_logical_error_rate(
        args.per, n_trials=args.n_trials, n_errors=args.n_errors, code=args.code, basis=args.basis)

    end_time = time.time()

    print('per:', args.per, 'trials:', trials,
          'lers:', lers, 'ler:', lers[-1]/trials,
          'k:', args.code.split('_')[1])
    metadata_dict = {k: v for k, v in vars(args).items() if (
        k != 'save_file' and k != 'n_trials' and k != 'n_errors')}
    metadata_dict['k'] = int(args.code.split('_')[1])
    strong_id_string = str(args.code) + str(args.per) + \
        str(args.basis) + str(args.max_error_weight)
    strong_id_hash = hashlib.sha256(
        strong_id_string.encode('utf-8')).hexdigest()

    test = sinter.TaskStats(
        strong_id=strong_id_hash,
        shots=trials,
        errors=lers[-1],
        decoder="lut",
        json_metadata=metadata_dict,
        seconds=end_time - start_time,
    )

    # Load existing data if file exists
    file_name = f"{args.save_file[0]}.csv"
    if os.path.exists(file_name):

        with open(file_name, "a") as f:
            f.write(test.to_csv_line() + "\n")
    else:

        with open(file_name, "w") as f:
            f.write(sinter.CSV_HEADER + "\n")
            f.write(test.to_csv_line() + "\n")
        existing_data = dict()
