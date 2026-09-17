import unittest

from darknessalp import radec_to_eci


class TestRadecToEci(unittest.TestCase):
    def test_poles_and_equinox(self):
        x, y, z = radec_to_eci(0.0, 0.0)
        self.assertEqual((x, y, z), (1.0, 0.0, 0.0))
        self.assertAlmostEqual(radec_to_eci(123.0, 90.0)[2], 1.0)
        self.assertAlmostEqual(radec_to_eci(90.0, 0.0)[1], 1.0)


if __name__ == "__main__":
    unittest.main()
