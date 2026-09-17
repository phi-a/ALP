import unittest
from math import cos, radians, sin, sqrt

from darknessalp import load_igrf, los_field_integral
from darknessalp.constants import R_EARTH_KM

R0 = R_EARTH_KM + 420.0


def dipole_frame(coeffs):
    """Return dipole axis m, a magnetic-equator direction e, and B0 (T)."""
    gx, gy = coeffs[(1, 1)]
    gz = coeffs[(1, 0)][0]
    g = sqrt(gx * gx + gy * gy + gz * gz)
    m = (-gx / g, -gy / g, -gz / g)
    norm = sqrt(m[0] ** 2 + m[1] ** 2)
    return m, (m[1] / norm, -m[0] / norm, 0.0), g * 1e-9


class TestLosFieldIntegral(unittest.TestCase):
    def setUp(self):
        self.coeffs = load_igrf(2027.0)
        self.m, self.e, self.b0 = dipole_frame(self.coeffs)
        self.r = tuple(R0 * v for v in self.e)

    def test_zenith_at_magnetic_equator(self):
        # closed form B0 R_E^3 / (2 r0^2); truncate at 20 R_E
        expect = self.b0 * R_EARTH_KM * 1e3 / 2 * (R_EARTH_KM / R0) ** 2
        res = los_field_integral(self.r, self.e, 0.0, self.coeffs, lmax=1,
                                 l_max_re=20.0, n_steps=400)
        self.assertAlmostEqual(res["amplitude_tm"] / expect, 1.0, places=2)
        self.assertFalse(res["occulted"])

    def test_nadir_stops_at_surface(self):
        expect = self.b0 * R_EARTH_KM * 1e3 / 2 * (1 - (R_EARTH_KM / R0) ** 2)
        down = tuple(-v for v in self.e)
        res = los_field_integral(self.r, down, 0.0, self.coeffs, lmax=1)
        self.assertAlmostEqual(res["amplitude_tm"] / expect, 1.0, places=2)
        self.assertTrue(res["occulted"])
        self.assertAlmostEqual(res["s_km"][-1], 420.0, places=6)

    def test_outer_radius_converges(self):
        near = los_field_integral(self.r, self.e, 0.0, self.coeffs, lmax=1)
        far = los_field_integral(self.r, self.e, 0.0, self.coeffs, lmax=1,
                                 l_max_re=20.0)
        self.assertGreater(near["amplitude_tm"] / far["amplitude_tm"], 0.98)

    def test_reversal_cancels(self):
        # start at maglat 15 deg, look south along the axis: B_rho flips
        lam = radians(15.0)
        start = tuple(R0 * (cos(lam) * self.e[i] + sin(lam) * self.m[i])
                      for i in range(3))
        south = tuple(-v for v in self.m)
        res = los_field_integral(start, south, 0.0, self.coeffs, lmax=1)
        self.assertFalse(res["occulted"])
        # the running total must fall somewhere: that is the cancellation
        running = res["running_tm"]
        self.assertTrue(any(b < a for a, b in zip(running, running[1:])))

    def test_phase_reduces_amplitude(self):
        coherent = los_field_integral(self.r, self.e, 0.0, self.coeffs, 1)
        phased = los_field_integral(self.r, self.e, 0.0, self.coeffs, 1,
                                    q_per_m=1e-6)
        self.assertLess(phased["amplitude_tm"], coherent["amplitude_tm"])


if __name__ == "__main__":
    unittest.main()
