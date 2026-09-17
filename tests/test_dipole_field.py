import unittest
from math import sqrt

from darknessalp import dipole_field, igrf_field, load_igrf


class TestDipoleField(unittest.TestCase):
    def setUp(self):
        self.coeffs = load_igrf(2027.0)

    def test_matches_igrf_degree_one(self):
        r = (4000.0, 3000.0, 4500.0)
        for a, b in zip(dipole_field(r, self.coeffs),
                        igrf_field(r, self.coeffs, lmax=1)):
            self.assertAlmostEqual(a, b, places=15)

    def test_inverse_cube(self):
        r1 = (6371.2, 0.0, 0.0)
        r2 = (12742.4, 0.0, 0.0)
        b1 = sqrt(sum(x * x for x in dipole_field(r1, self.coeffs)))
        b2 = sqrt(sum(x * x for x in dipole_field(r2, self.coeffs)))
        self.assertAlmostEqual(b1 / b2, 8.0)


if __name__ == "__main__":
    unittest.main()
