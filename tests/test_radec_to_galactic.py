import unittest

from darknessalp import radec_to_galactic


class TestRadecToGalactic(unittest.TestCase):
    def test_north_galactic_pole(self):
        _, b = radec_to_galactic(192.85948, 27.12825)
        self.assertAlmostEqual(b, 90.0, places=4)

    def test_galactic_centre(self):
        l, b = radec_to_galactic(266.405, -28.936)
        self.assertLess(min(l, 360.0 - l), 0.01)
        self.assertAlmostEqual(b, 0.0, places=2)


if __name__ == "__main__":
    unittest.main()
