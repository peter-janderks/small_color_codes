import unittest
from math import sqrt

import sinter

from numerics.memory_stats import combine_x_and_z


def make_stat(strong_id, basis, shots, errors, *, decoder="lut", max_error_weight=3):
    return sinter.TaskStats(
        strong_id=strong_id,
        shots=shots,
        errors=errors,
        decoder=decoder,
        json_metadata={
            "basis": basis,
            "code": "16_4_4",
            "k": 4,
            "max_error_weight": max_error_weight,
            "per": 0.001,
        },
    )


class CombineMemoryStatsTest(unittest.TestCase):
    def test_pools_each_basis_before_combining_rates_and_standard_errors(self):
        stats = [
            make_stat("z1", "Z", 100, 30),
            make_stat("x1", "X", 40, 2),
            make_stat("z2", "Z", 200, 90),
            make_stat("x2", "X", 60, 8),
        ]

        combined, = combine_x_and_z(stats)

        # X has 10 failures in 100 shots, and Z has 120 in 300.
        self.assertAlmostEqual(combined.error_rate, (0.1 + 0.4) / 4)
        self.assertAlmostEqual(
            combined.standard_error, sqrt(0.1 * 0.9 / 100 + 0.4 * 0.6 / 300) / 4
        )

    def test_reports_x_and_z_orphans_when_other_metadata_differs(self):
        stats = [
            make_stat("x", "X", 100, 10),
            make_stat("z", "Z", 300, 120, max_error_weight=4),
        ]

        with self.assertRaises(ValueError) as error:
            combine_x_and_z(stats)

        message = str(error.exception)
        self.assertRegex(message, r'missing Z basis for lut: .*"max_error_weight": 3')
        self.assertRegex(message, r'missing X basis for lut: .*"max_error_weight": 4')

    def test_requires_matching_decoders(self):
        stats = [
            make_stat("x", "X", 100, 10),
            make_stat("z", "Z", 300, 120, decoder="other"),
        ]

        with self.assertRaisesRegex(ValueError, "missing Z basis for lut"):
            combine_x_and_z(stats)
