import unittest

from darknessalp import earth_limb_angle


class TestEarthLimbAngle(unittest.TestCase):
    def test_nadir_and_zenith_at_420_km(self):
        r = (6791.2, 0.0, 0.0)
        self.assertAlmostEqual(earth_limb_angle(r, (-1.0, 0.0, 0.0)), -69.74, 1)
        self.assertAlmostEqual(earth_limb_angle(r, (1.0, 0.0, 0.0)), 110.26, 1)

    def test_horizon(self):
        self.assertAlmostEqual(
            earth_limb_angle((6791.2, 0.0, 0.0), (0.0, 1.0, 0.0)), 20.26, 1)


if __name__ == "__main__":
    unittest.main()
