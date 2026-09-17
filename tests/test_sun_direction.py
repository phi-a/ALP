import unittest
from datetime import datetime
from math import sqrt

from darknessalp import julian_date, sun_direction


class TestSunDirection(unittest.TestCase):
    def test_march_equinox_2026(self):
        x, y, z = sun_direction(julian_date(datetime(2026, 3, 20, 14, 46)))
        self.assertAlmostEqual(sqrt(x * x + y * y + z * z), 1.0)
        self.assertGreater(x, 0.999)
        self.assertLess(abs(z), 0.005)

    def test_june_solstice_2026(self):
        _, _, z = sun_direction(julian_date(datetime(2026, 6, 21, 8, 24)))
        self.assertAlmostEqual(z, 0.3978, places=2)


if __name__ == "__main__":
    unittest.main()
