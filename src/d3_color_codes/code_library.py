from ldpc.code_util import compute_code_distance
from d3_color_codes.steane_ecc_circuits import SteaneECCircuits
import numpy as np
from mqt.qecc.codes.css_code import CSSCode


H = np.zeros((3, 7), dtype=np.int8)
H[0, [0, 1, 3, 4]] = 1
H[1, [1, 2, 4, 5]] = 1
H[2, [3, 4, 5, 6]] = 1

n7_k1_d3 = CSSCode(3, Hx=H, Hz=H, n=7)

H = np.zeros((6, 16), dtype=np.int8)
H[0, [0, 1, 3, 4]] = 1
H[1, [1, 2, 4, 5, 7, 8]] = 1
H[2, [3, 4, 6, 7, 10, 11]] = 1
H[3, [7, 8, 11, 12, 14, 15]] = 1
H[4, [10, 11, 13, 14]] = 1
H[5, [5, 8, 9, 12]] = 1
n16_k4_d3 = CSSCode(6, Hx=H, Hz=H, n=16)


Hx = np.zeros((6, 18), dtype=np.int8)
# in the first row of the matrix, there should be 1 at indices 0, 1, 4, 5
Hx[0, [0, 1, 3, 4, 6, 7]] = 1
Hx[1, [4, 5, 7, 8, 10, 11]] = 1
Hx[2, [6, 7, 9, 10, 12, 13]] = 1
Hx[3, [10, 11, 13, 14, 16, 17]] = 1
Hx[4, [12, 13, 15, 16, 0, 1]] = 1
Hx[5, [16, 17, 1, 2, 4, 5]] = 1
n18_k6_d3 = CSSCode(3, Hx=Hx, Hz=Hx, n=18)


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

print(n20_k4_d4_pauli.Hx * n20_k4_d4_pauli.Lz[0].T % 2)
# logicals = n20_k4_d4_pauli._compute_logical(Hx, Hz)

H = np.zeros((8, 20))
H[0, [0, 1, 3, 4, 7, 8]] = 1
H[1, [1, 2, 4, 5, 18, 19]] = 1
H[2, [2, 5, 6, 9]] = 1
H[3, [4, 5, 8, 9, 11, 12]] = 1
H[4, [7, 8, 10, 11, 14, 15]] = 1
H[5, [10, 13, 14, 17]] = 1
H[6, [11, 12, 15, 16, 18, 19]] = 1
H[7, [14, 15, 17, 18, 0, 1]] = 1

n20_k4_d4 = CSSCode(4, Hx=H, Hz=H, n=20)
logicals = n20_k4_d4._compute_logical(Hx, Hz)


H = np.zeros((6, 16), dtype=np.int8)
H[0, [0, 2, 3, 6]] = 1
H[1, [1, 4, 5, 7]] = 1
H[2, [3, 4, 6, 7, 8, 9, 11, 12]] = 1
H[3, [8, 10, 11, 14]] = 1
H[4, [9, 12, 13, 15]] = 1
H[5, [0, 1, 3, 4, 11, 12, 14, 15]] = 1
n16_k4_d4 = CSSCode(4, Hx=H, Hz=H, n=16)


H = np.zeros((9, 27), dtype=np.int8)
H[0, [0, 1, 3, 4, 6, 7]] = 1
H[1, [4, 5, 7, 8, 10, 11]] = 1
H[2, [6, 7, 9, 10, 12, 13]] = 1
H[3, [10, 11, 13, 14, 16, 17]] = 1
H[4, [12, 13, 15, 16, 18, 19]] = 1
H[5, [16, 17, 19, 20, 22, 23]] = 1
H[6, [18, 19, 21, 22, 24, 25]] = 1
H[7, [22, 23, 25, 26, 1, 0]] = 1
H[8, [24, 25, 1, 2, 4, 5]] = 1

n27_k9_d3 = CSSCode(3, Hx=H, Hz=H, n=27)


H = np.zeros((5, 12), dtype=np.int8)
H[0, [0, 1, 4, 5]] = 1
H[1, [1, 2, 5, 6, 9, 10]] = 1
H[2, [2, 3, 6, 7]] = 1
H[3, [4, 5, 8, 9]] = 1
H[4, [6, 7, 10, 11]] = 1


total_ones = 2*np.sum(H)
print(total_ones, '12_2_3')

n12_k2_d3 = CSSCode(3, Hx=H, Hz=H, n=12)

Hx = np.zeros((5, 12), dtype=np.int8)
Hz = np.zeros((5, 12), dtype=np.int8)

Hx[0, [0, 2, 4, 5]] = 1
Hx[1, [0, 1, 2, 3]] = 1
Hx[2, [2, 3, 5, 6, 8, 9]] = 1
Hx[3, [6, 7, 9, 11]] = 1
Hx[4, [8, 9, 10, 11]] = 1

Hz[0, [0, 1, 2, 3]] = 1
Hz[1, [1, 3, 6, 7]] = 1
Hz[2, [2, 3, 5, 6, 8, 9]] = 1
Hz[3, [4, 5, 8, 10]] = 1
Hz[4, [8, 9, 10, 11]] = 1
n12_k2_d3_pauli = CSSCode(3, Hx=Hx, Hz=Hz, n=12)
total_ones = np.sum(Hx) + np.sum(Hz)
print(total_ones, '12_2_3 pauli')

code_dict = {
    "7_1_3": n7_k1_d3,
    "16_4_3": n16_k4_d3,
    "18_6_3": n18_k6_d3,
    "16_4_4": n16_k4_d4,
    "27_9_3": n27_k9_d3,
    "12_2_3": n12_k2_d3,
    "20_4_4": n20_k4_d4,
    "20_4_4_pauli": n20_k4_d4_pauli
}


def get_noiseless_circuits(code_parameters: str = "7_1_3", basis: str = "Z") -> SteaneECCircuits:
    return SteaneECCircuits(
        x_parity_check_matrix=code_dict[code_parameters].Hx,
        z_parity_check_matrix=code_dict[code_parameters].Hz,
        x_logicals=code_dict[code_parameters].Lx,
        z_logicals=code_dict[code_parameters].Lz,
        file_prefix=f"circuit_blocks/{code_parameters}_",
        basis=basis
    )
