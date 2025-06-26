from typing import List
import stim 
from d3_color_codes.steane_code_code_blocks import data_logical_initilization, ancilla_logical_initilization, steane_ec_z_stabilizers, steane_ec_x_stabilizers, final_measurements
from d3_color_codes.lut import LutDecoder
import numpy as np
import matplotlib.pyplot as plt

def initialize_until_succes(circ: stim.Circuit, s: stim.TableauSimulator) -> tuple[stim.TableauSimulator, int]:
    n_iterations = 1
    while True:
        s.do(circ)
        if s.current_measurement_record()[-1] == False:
            break
        else:
            n_iterations += 1
        
    return(s, n_iterations)

def get_detector_and_observable_values(measurement_record: List[bool], circ: stim.Circuit) -> List[int]:
    detector_values = []
    observable_values = []

    for op in circ:
        if op.name == "DETECTOR":
            detector_values.append([sum(measurement_record[i.value] for i in op.targets_copy()) % 2])
        if op.name == "OBSERVABLE_INCLUDE":
            observable_values.append([sum(measurement_record[i.value] for i in op.targets_copy())% 2])
    return detector_values, observable_values

def simulate_steane_ec(data_logical_0_init: stim.Circuit,
                       ancilla_logical_0_init: stim.Circuit,
                       ancilla_logical_plus_init: stim.Circuit,
                       steane_ec_z_stabilizers: stim.Circuit,
                       steane_ec_x_stabilizers: stim.Circuit,
                       final_measurements: stim.Circuit,
                       decoder: LutDecoder) -> stim.TableauSimulator:
    syndrome = []
    observable_value = []
    s = stim.TableauSimulator()
    s, _ = initialize_until_succes(data_logical_0_init, s)
    s, _ = initialize_until_succes(ancilla_logical_0_init, s)
    s.do(steane_ec_z_stabilizers)
    new_syndrome, new_obersvable_value = get_detector_and_observable_values(s.current_measurement_record(), steane_ec_z_stabilizers)
    syndrome.extend(new_syndrome)
    s, _ = initialize_until_succes(ancilla_logical_plus_init, s)
    observable_value.extend(new_obersvable_value)
    s.do(steane_ec_x_stabilizers)
    s.do(final_measurements)
    new_syndrome, new_obersvable_value = get_detector_and_observable_values(s.current_measurement_record(), final_measurements)
    syndrome.extend(new_syndrome)
    observable_value.extend(new_obersvable_value)
    prediction = decoder.decode(np.array(syndrome))
    return(int(prediction[0] != observable_value[0][0]))

def calculate_logical_error_rate(per: float, n_trials: int = 1000) -> float:
    logical_errors = 0
    
    data_logical_0_init = data_logical_initilization([i for i in range(8)], per, "Z")
    ancilla_logical_0_init = ancilla_logical_initilization([i for i in range(8, 16)], per, "Z")
    ancilla_logical_plus_init = ancilla_logical_initilization([i for i in range(8, 16)], per, "X")
    measure_z_stabilizers = steane_ec_z_stabilizers(per, detectors=True)
    measure_x_stabilizers = steane_ec_x_stabilizers(per, detectors=False)
    measure_data_qubits = final_measurements(per, basis="Z")
    circ = stim.Circuit()
    circ += data_logical_0_init
    circ += ancilla_logical_0_init
    circ += measure_z_stabilizers
    circ += ancilla_logical_plus_init
    circ += measure_x_stabilizers
    circ += measure_data_qubits
    decoder = LutDecoder(circ.detector_error_model())

    for _ in range(n_trials):
        logical_errors += simulate_steane_ec(
            data_logical_0_init,
            ancilla_logical_0_init,
            ancilla_logical_plus_init,
            measure_z_stabilizers,
            measure_x_stabilizers,
            measure_data_qubits,
            decoder
        )  

    return logical_errors / n_trials

if __name__ == "__main__":
    lers = []
    pers = np.logspace(-3, -2, 10)
    for per in pers:
        ler = calculate_logical_error_rate(per, n_trials=10_000) 
        lers.append(ler)
    
    plt.plot(pers, pers, linestyle='--', color='gray', label='y = x')
    plt.plot(pers, lers, marker='o')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
