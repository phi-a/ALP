import unittest

import numpy as np

from darknessalp import dynamics, orbit


def node_deg(r, v):
    h = np.cross(r, v)
    return np.degrees(np.arctan2(h[:, 0], -h[:, 1]))


class TestOrbit(unittest.TestCase):
    def test_period_and_radius(self):
        self.assertAlmostEqual(orbit.period_s(420.0) / 60, 92.8, places=1)
        r, v = orbit.circular_orbit([0.0, 1234.0], 420.0, 51.6, 40.0, 70.0)
        np.testing.assert_allclose(np.linalg.norm(r, axis=1), 6791.2)
        np.testing.assert_allclose(np.linalg.norm(v, axis=1), 7.66, atol=0.01)

    def test_max_latitude_is_inclination(self):
        r, _ = orbit.circular_orbit(np.arange(0, 6000, 10.0), 420.0, 51.6)
        self.assertAlmostEqual(r[:, 2].max() / 6791.2, 0.7837, places=3)

    def test_sun_synchronous_node_rate(self):
        r, v = orbit.circular_orbit([0.0, 86400.0], 500.0, 97.4)
        drift = np.diff(node_deg(r, v))[0]
        self.assertAlmostEqual(drift, 0.9856, delta=0.01)

    def test_propagate_matches_two_body_period(self):
        r0, v0 = orbit.circular_orbit(0.0, 420.0, 90.0)
        t = np.array([0.0, orbit.period_s(420.0)])
        r, _ = orbit.propagate(r0[0], v0[0], t, acceleration=dynamics.two_body)
        np.testing.assert_allclose(r[1], r[0], atol=1e-3)

    def test_j2_acceleration_direction(self):
        a = dynamics.j2_acceleration(np.array([[7000.0, 0.0, 0.0]]))[0]
        self.assertLess(a[0], 0.0)  # extra pull toward the equator bulge
        self.assertAlmostEqual(a[1], 0.0)
        self.assertAlmostEqual(a[2], 0.0)


if __name__ == "__main__":
    unittest.main()
