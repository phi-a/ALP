import unittest

import numpy as np

from darknessalp import field

R = 6371.2


def point(lat_deg, lon_deg, r=R):
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)
    return np.array([[r * np.cos(lat) * np.cos(lon),
                      r * np.cos(lat) * np.sin(lon), r * np.sin(lat)]])


class TestField(unittest.TestCase):
    def setUp(self):
        self.c = field.load_igrf(2027.0)

    def test_coefficients(self):
        g, _ = field.load_igrf(2025.0)
        self.assertEqual(g[1, 0], -29350.0)
        g, _ = self.c
        self.assertAlmostEqual(g[1, 0], -29350.0 + 2 * 12.6)
        with self.assertRaises(ValueError):
            field.load_igrf(2031.0)

    def test_legendre_closed_forms(self):
        th = np.array([0.7])
        p, dp = field.schmidt_legendre(2, th)
        c, s = np.cos(0.7), np.sin(0.7)
        self.assertAlmostEqual(p[2, 0, 0], (3 * c * c - 1) / 2)
        self.assertAlmostEqual(p[2, 1, 0], np.sqrt(3) * s * c)
        self.assertAlmostEqual(dp[2, 2, 0], np.sqrt(3) * s * c)

    def test_surface_magnitudes_and_saa(self):
        mag = lambda la, lo: np.linalg.norm(field.igrf_field(point(la, lo),
                                                             self.c)) * 1e9
        self.assertAlmostEqual(mag(0, 0), 31900, delta=300)
        self.assertAlmostEqual(mag(90, 0), 56600, delta=300)
        self.assertLess(mag(-25, -50), 23000)

    def test_matches_legacy_igrf13_at_2020(self):
        c = field.load_igrf(2020.0)
        b = field.igrf_field(point(45.0, -75.0, R + 420.0), c)[0]
        lat, lon = np.radians(45.0), np.radians(-75.0)
        b_r = (b[0] * np.cos(lat) * np.cos(lon) + b[1] * np.cos(lat)
               * np.sin(lon) + b[2] * np.sin(lat))
        b_p = -b[0] * np.sin(lon) + b[1] * np.cos(lon)
        self.assertAlmostEqual(b_r * 1e9, -40999.0, delta=10)
        self.assertAlmostEqual(b_p * 1e9, -3172.9, delta=3)

    def test_dipole_equals_degree_one(self):
        r = np.array([[4000.0, 3000.0, 4500.0], [-6000.0, 1000.0, 2000.0]])
        np.testing.assert_allclose(field.dipole_field(r, self.c),
                                   field.igrf_field(r, self.c, lmax=1))

    def test_magnetic_coords(self):
        north = field.magnetic_latitude(np.array([[0.0, 0.0, 7000.0]]), self.c)
        self.assertAlmostEqual(north[0], 80.9, places=1)
        self.assertAlmostEqual(field.cutoff_rigidity(0.0, R), 14.9)
        self.assertAlmostEqual(field.cutoff_rigidity(45.0, R), 3.725)
        self.assertAlmostEqual(field.l_shell(0.0, R), 1.0)


if __name__ == "__main__":
    unittest.main()
