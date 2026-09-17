import unittest
from math import pi

from darknessalp.local_to_ecef import local_to_ecef


class TestLocalToEcef(unittest.TestCase):
    def test_radial_at_equator_greenwich(self):
        x, y, z = local_to_ecef((1.0, 0.0, 0.0), pi / 2, 0.0)
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 0.0)
        self.assertAlmostEqual(z, 0.0)

    def test_south_and_east_at_equator_greenwich(self):
        self.assertAlmostEqual(local_to_ecef((0, 1.0, 0), pi / 2, 0)[2], -1.0)
        self.assertAlmostEqual(local_to_ecef((0, 0, 1.0), pi / 2, 0)[1], 1.0)


if __name__ == "__main__":
    unittest.main()
