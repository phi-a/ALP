import unittest
from math import sqrt

from darknessalp import eci_to_ecef, field_eci, igrf_field, load_igrf


class TestFieldEci(unittest.TestCase):
    def test_magnitude_is_frame_independent(self):
        coeffs = load_igrf(2027.0)
        r = (5000.0, 3000.0, 3500.0)
        b_ecef = igrf_field(eci_to_ecef(r, 77.0), coeffs)
        b_eci = field_eci(r, 77.0, coeffs)
        self.assertAlmostEqual(sqrt(sum(x * x for x in b_ecef)),
                               sqrt(sum(x * x for x in b_eci)))
        self.assertAlmostEqual(b_ecef[2], b_eci[2])


if __name__ == "__main__":
    unittest.main()
