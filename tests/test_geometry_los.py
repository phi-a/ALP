import unittest

import numpy as np

from darknessalp import field, frames, geometry
from darknessalp.constants import R_EARTH_KM

R0 = R_EARTH_KM + 420.0


class TestLosIntegral(unittest.TestCase):
    def setUp(self):
        self.c = field.load_igrf(2027.0)
        self.t = frames.times("2027-01-01T00:00:00", 0.0)[0]
        m = field.dipole_axis(self.c)
        e = np.cross(m, [0.0, 0.0, 1.0])
        e /= np.linalg.norm(e)
        self.r = frames.ecef_to_eci(R0 * e, self.t)[0]
        self.up = frames.ecef_to_eci(e, self.t)[0]
        self.north = frames.ecef_to_eci(m, self.t)[0]
        self.b0 = np.linalg.norm(field.dipole_moment(self.c)) * 1e-9

    def amplitude(self, n_hats, **kw):
        return geometry.los_field_integral(self.r, n_hats, self.t, self.c,
                                           lmax=1, **kw)

    def test_zenith_and_nadir_closed_forms(self):
        res = self.amplitude(np.stack([self.up, -self.up]), l_max_re=20.0,
                             n_steps=400)
        zenith = self.b0 * R_EARTH_KM * 1e3 / 2 * (R_EARTH_KM / R0) ** 2
        nadir = self.b0 * R_EARTH_KM * 1e3 / 2 * (1 - (R_EARTH_KM / R0) ** 2)
        np.testing.assert_allclose(res["amplitude_tm"], [zenith, nadir],
                                   rtol=0.01)
        np.testing.assert_array_equal(res["occulted"], [False, True])
        self.assertAlmostEqual(res["s_km"][1, -1], 420.0, places=6)

    def test_outer_radius_converges(self):
        near = self.amplitude(self.up)["amplitude_tm"][0]
        far = self.amplitude(self.up, l_max_re=20.0)["amplitude_tm"][0]
        self.assertGreater(near / far, 0.98)

    def test_reversal_shows_a_dip(self):
        lam = np.radians(15.0)
        start = R0 * (np.cos(lam) * self.up + np.sin(lam) * self.north)
        res = geometry.los_field_integral(start, -self.north, self.t, self.c,
                                          lmax=1)
        running = res["running_tm"][0]
        self.assertFalse(res["occulted"][0])
        self.assertTrue(np.any(np.diff(running) < 0))

    def test_phase_reduces_amplitude(self):
        coherent = self.amplitude(self.up)["amplitude_tm"][0]
        phased = self.amplitude(self.up, q_per_m=1e-6)["amplitude_tm"][0]
        self.assertLess(phased, coherent)

    def test_many_rays_one_call(self):
        dirs = np.stack([self.up, self.north, -self.up])
        res = self.amplitude(dirs)
        self.assertEqual(res["amplitude_tm"].shape, (3,))
        self.assertAlmostEqual(res["amplitude_tm"][1]
                               / res["amplitude_tm"][0], 2.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
