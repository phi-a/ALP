import unittest

from darknessalp import ecef_to_eci, eci_to_ecef


class TestEciToEcef(unittest.TestCase):
    def test_quarter_turn(self):
        x, y, z = eci_to_ecef((1.0, 0.0, 2.0), 90.0)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, -1.0)
        self.assertEqual(z, 2.0)

    def test_round_trip(self):
        v = (1.0, 2.0, 3.0)
        back = ecef_to_eci(eci_to_ecef(v, 123.4), 123.4)
        for a, b in zip(v, back):
            self.assertAlmostEqual(a, b)


if __name__ == "__main__":
    unittest.main()
