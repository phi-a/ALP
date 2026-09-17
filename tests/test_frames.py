import unittest

import numpy as np

from darknessalp import frames


class TestFrames(unittest.TestCase):
    def test_times_and_decimal_year(self):
        t = frames.times("2027-01-01T00:00:00", [0.0, 86400.0])
        self.assertEqual(len(t), 2)
        self.assertAlmostEqual(frames.decimal_year(t)[0], 2027.0, places=4)

    def test_eci_ecef_round_trip(self):
        t = frames.times("2027-05-01T00:00:00", 0.0)
        v = np.array([[7000.0, 1000.0, -500.0]])
        back = frames.ecef_to_eci(frames.eci_to_ecef(v, t), t)
        np.testing.assert_allclose(back, v, atol=1e-6)

    def test_ecef_rotates_with_earth(self):
        t = frames.times("2027-05-01T00:00:00", [0.0, 6 * 3600.0])
        v = np.array([[7000.0, 0.0, 0.0], [7000.0, 0.0, 0.0]])
        lon = frames.spherical(frames.eci_to_ecef(v, t))[1]
        self.assertAlmostEqual((lon[0] - lon[1]) % 360, 90.0, delta=0.5)

    def test_galactic_centre(self):
        v = frames.galactic_vector(0.0, 0.0)
        ra = np.degrees(np.arctan2(v[0, 1], v[0, 0])) % 360
        self.assertAlmostEqual(ra, 266.405, places=2)
        l, b = frames.to_galactic(v)
        self.assertLess(min(l[0], 360 - l[0]), 1e-3)

    def test_sun_at_equinox(self):
        s = frames.sun_vector(frames.times("2026-03-20T14:46:00", 0.0))
        self.assertGreater(s[0, 0], 0.999)
        self.assertLess(abs(s[0, 2]), 0.005)


if __name__ == "__main__":
    unittest.main()
