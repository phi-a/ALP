import unittest
from math import cos, radians, sin, sqrt

from darknessalp import igrf_field, load_igrf

R = 6371.2


def point(lat_deg, lon_deg, r=R):
    lat, lon = radians(lat_deg), radians(lon_deg)
    return (r * cos(lat) * cos(lon), r * cos(lat) * sin(lon), r * sin(lat))


class TestIgrfField(unittest.TestCase):
    def setUp(self):
        self.coeffs = load_igrf(2027.0)

    def magnitude_nt(self, lat, lon):
        b = igrf_field(point(lat, lon), self.coeffs)
        return sqrt(sum(x * x for x in b)) * 1e9

    def test_surface_magnitudes(self):
        self.assertAlmostEqual(self.magnitude_nt(0, 0), 31900, delta=300)
        self.assertAlmostEqual(self.magnitude_nt(90, 0), 56600, delta=300)

    def test_south_atlantic_anomaly_is_weakest(self):
        saa = self.magnitude_nt(-25, -50)
        self.assertLess(saa, 23000)
        self.assertLess(saa, self.magnitude_nt(-25, 100))

    def test_matches_legacy_at_2020(self):
        # legacy numpy IGRF-13 (B_r, B_phi) at 45 N, 75 W, 420 km
        coeffs = load_igrf(2020.0)
        lat, lon = radians(45.0), radians(-75.0)
        bx, by, bz = igrf_field(point(45.0, -75.0, R + 420.0), coeffs)
        b_r = (bx * cos(lat) * cos(lon) + by * cos(lat) * sin(lon)
               + bz * sin(lat))
        b_p = -bx * sin(lon) + by * cos(lon)
        self.assertAlmostEqual(b_r * 1e9, -40999.0, delta=10)
        self.assertAlmostEqual(b_p * 1e9, -3172.9, delta=3)


if __name__ == "__main__":
    unittest.main()
