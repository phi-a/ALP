import unittest

from darknessalp import galactic_to_radec, radec_to_galactic


class TestGalacticToRadec(unittest.TestCase):
    def test_galactic_centre(self):
        ra, dec = galactic_to_radec(0.0, 0.0)
        self.assertAlmostEqual(ra, 266.405, places=2)
        self.assertAlmostEqual(dec, -28.936, places=2)

    def test_round_trip(self):
        l, b = radec_to_galactic(*galactic_to_radec(57.0, 22.0))
        self.assertAlmostEqual(l, 57.0)
        self.assertAlmostEqual(b, 22.0)


if __name__ == "__main__":
    unittest.main()
