import unittest

from darknessalp import gmst


class TestGmst(unittest.TestCase):
    def test_j2000(self):
        self.assertAlmostEqual(gmst(2451545.0), 280.4606, places=3)

    def test_one_sidereal_day_later(self):
        self.assertAlmostEqual(gmst(2451545.0 + 0.9972696), 280.4606, 2)


if __name__ == "__main__":
    unittest.main()
