import unittest
from math import atan2, degrees, pi, sqrt

from darknessalp import circular_orbit
from darknessalp.constants import MU_EARTH_KM3_S2, R_EARTH_KM


def node_deg(t_s, alt_km, inc_deg):
    r, v = circular_orbit(t_s, alt_km, inc_deg)
    hx = r[1] * v[2] - r[2] * v[1]
    hy = r[2] * v[0] - r[0] * v[2]
    return degrees(atan2(hx, -hy))


class TestCircularOrbit(unittest.TestCase):
    def test_period_at_iss_altitude(self):
        a = R_EARTH_KM + 420.0
        period = 2 * pi * sqrt(a**3 / MU_EARTH_KM3_S2)
        self.assertAlmostEqual(period / 60, 92.8, places=1)
        # polar, so the J2 node drift does not move the repeat point
        r0, _ = circular_orbit(0.0, 420.0, 90.0)
        r1, _ = circular_orbit(period, 420.0, 90.0)
        for x0, x1 in zip(r0, r1):
            self.assertAlmostEqual(x0, x1, delta=5.0)

    def test_radius_and_speed(self):
        r, v = circular_orbit(1234.0, 420.0, 51.6, 40.0, 70.0)
        self.assertAlmostEqual(sqrt(sum(x * x for x in r)), 6791.2, 6)
        self.assertAlmostEqual(sqrt(sum(x * x for x in v)), 7.66, 2)

    def test_max_latitude_is_inclination(self):
        z_max = max(circular_orbit(t, 420.0, 51.6)[0][2]
                    for t in range(0, 6000, 10))
        self.assertAlmostEqual(z_max / 6791.2, 0.7837, places=3)

    def test_sun_synchronous_node_rate(self):
        drift = node_deg(86400.0, 500.0, 97.4) - node_deg(0.0, 500.0, 97.4)
        self.assertAlmostEqual(drift, 0.9856, delta=0.01)

    def test_iss_node_regresses_west(self):
        drift = node_deg(86400.0, 420.0, 51.6) - node_deg(0.0, 420.0, 51.6)
        self.assertAlmostEqual(drift, -5.0, delta=0.2)


if __name__ == "__main__":
    unittest.main()
