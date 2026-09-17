import unittest

from darknessalp import load_igrf, magnetic_latitude


class TestMagneticLatitude(unittest.TestCase):
    def test_geographic_poles(self):
        coeffs = load_igrf(2027.0)
        north = magnetic_latitude((0.0, 0.0, 7000.0), coeffs)
        south = magnetic_latitude((0.0, 0.0, -7000.0), coeffs)
        self.assertAlmostEqual(north, 80.9, places=1)
        self.assertAlmostEqual(north, -south)


if __name__ == "__main__":
    unittest.main()
