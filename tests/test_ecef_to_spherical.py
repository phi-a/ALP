import unittest

from darknessalp import ecef_to_spherical


class TestEcefToSpherical(unittest.TestCase):
    def test_axes(self):
        self.assertEqual(ecef_to_spherical((0.0, 0.0, 7000.0)),
                         (90.0, 0.0, 7000.0))
        lat, lon, r = ecef_to_spherical((0.0, -7000.0, 0.0))
        self.assertEqual((lat, lon, r), (0.0, -90.0, 7000.0))


if __name__ == "__main__":
    unittest.main()
