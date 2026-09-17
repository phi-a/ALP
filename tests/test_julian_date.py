import unittest
from datetime import datetime

from darknessalp import julian_date


class TestJulianDate(unittest.TestCase):
    def test_j2000(self):
        self.assertEqual(julian_date(datetime(2000, 1, 1, 12)), 2451545.0)

    def test_fraction_of_day(self):
        jd = julian_date(datetime(2027, 1, 1, 6))
        self.assertAlmostEqual(jd, 2461406.75)


if __name__ == "__main__":
    unittest.main()
