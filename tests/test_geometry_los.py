import unittest

import numpy as np
from scipy.spatial.transform import Rotation

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
        # dipole on its equator: int B ds = b0 R_E/2 (R_E^2/r^2) between ends
        res = self.amplitude(np.stack([self.up, -self.up]), l_max_re=20.0,
                             n_steps=400, end_alt_km=0.0)
        zenith = self.b0 * R_EARTH_KM * 1e3 / 2 * (R_EARTH_KM / R0) ** 2
        nadir = self.b0 * R_EARTH_KM * 1e3 / 2 * (1 - (R_EARTH_KM / R0) ** 2)
        np.testing.assert_allclose(res["amplitude_tm"], [zenith, nadir],
                                   rtol=0.01)
        np.testing.assert_array_equal(res["occulted"], [False, True])
        self.assertAlmostEqual(res["s_km"][1, -1], 420.0, places=6)

    def test_nadir_ray_ends_at_the_opaque_shell(self):
        # Q23: keV X-rays converted below ~150 km are absorbed
        res = self.amplitude(-self.up, n_steps=400)
        r_end = R_EARTH_KM + 150.0
        nadir = (self.b0 * R_EARTH_KM * 1e3 / 2
                 * ((R_EARTH_KM / r_end) ** 2 - (R_EARTH_KM / R0) ** 2))
        self.assertAlmostEqual(res["amplitude_tm"][0] / nadir, 1.0, places=2)
        self.assertAlmostEqual(res["s_km"][0, -1], 270.0, places=6)
        self.assertTrue(res["occulted"][0])
        ground = self.amplitude(-self.up, n_steps=400, end_alt_km=0.0)
        self.assertAlmostEqual(res["amplitude_tm"][0]
                               / ground["amplitude_tm"][0], 0.62, places=2)

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

    def test_fov_hairline_cone_is_the_boresight(self):
        res = geometry.fov_field_integral(self.r, self.up, self.t, self.c,
                                          lmax=1, half_angle_deg=1e-3)
        boresight = self.amplitude(self.up)["amplitude_tm"][0]
        self.assertAlmostEqual(res["weights"].sum(), 1.0)
        self.assertAlmostEqual(res["amplitude_tm"][0], boresight)
        self.assertAlmostEqual(res["k_t2m2"] / boresight**2, 1.0, places=6)

    def test_fov_cone_differs_from_boresight(self):
        res = geometry.fov_field_integral(self.r, self.north, self.t,
                                          self.c, lmax=1, half_angle_deg=10.0)
        boresight = res["amplitude_tm"][0] ** 2
        self.assertGreater(abs(res["k_t2m2"] / boresight - 1.0), 1e-3)

    def test_step_count_converges_on_a_limb_ray(self):
        coarse = self.amplitude(self.north, n_steps=100)["amplitude_tm"][0]
        fine = self.amplitude(self.north, n_steps=800)["amplitude_tm"][0]
        self.assertAlmostEqual(coarse / fine, 1.0, delta=0.01)


class TestTransverseAmplitude(unittest.TestCase):
    """Block A checks on the bare integral, no IGRF."""

    def setUp(self):
        self.length = 1.0e7
        self.s = np.linspace(0.0, self.length, 4001)[None, :]
        self.n = np.array([[0.0, 0.0, 1.0]])

    def uniform(self, b0):
        b = np.zeros(self.s.shape + (3,))
        b[..., 0] = b0
        return b

    def test_uniform_field_gives_sinc_squared(self):
        # Raffelt & Stodolsky 1988; Yamamoto+ 2020 eq. 2.10
        b0, q = 3.0e-5, 3.0e-7
        amp = geometry.transverse_amplitude(self.uniform(b0), self.n,
                                            self.s, q)[0, -1]
        ql = q * self.length
        expected = (b0 * self.length) ** 2 * 2 * (1 - np.cos(ql)) / ql**2
        self.assertAlmostEqual(amp**2 / expected, 1.0, places=5)

    def test_zero_phase_is_the_plain_integral(self):
        amp = geometry.transverse_amplitude(self.uniform(3.0e-5), self.n,
                                            self.s)[0, -1]
        self.assertAlmostEqual(amp / (3.0e-5 * self.length), 1.0, places=9)

    def test_reversed_field_cancels(self):
        b = self.uniform(3.0e-5)
        b[:, self.s[0] > self.length / 2, 0] *= -1
        running = geometry.transverse_amplitude(b, self.n, self.s)[0]
        half = 3.0e-5 * self.length / 2
        self.assertAlmostEqual(running.max() / half, 1.0, places=3)
        self.assertLess(running[-1] / half, 1e-2)

    def test_field_along_the_ray_does_not_count(self):
        b = np.zeros(self.s.shape + (3,))
        b[..., 2] = 3.0e-5
        amp = geometry.transverse_amplitude(b, self.n, self.s)[0, -1]
        self.assertEqual(amp, 0.0)

    def test_rotating_the_frame_leaves_the_amplitude(self):
        phase = 2 * np.pi * self.s[0] / self.length
        b = np.stack([np.cos(phase), np.sin(phase), 0.5 + 0 * phase],
                     axis=-1)[None] * 3.0e-5
        rot = Rotation.random(random_state=7)
        plain = geometry.transverse_amplitude(b, self.n, self.s, 2e-7)
        turned = geometry.transverse_amplitude(
            rot.apply(b[0])[None], rot.apply(self.n), self.s, 2e-7)
        np.testing.assert_allclose(turned, plain, rtol=1e-9)
        self.assertGreater(plain[0, -1], 0.0)

    def test_probability_is_quadratic_in_the_coupling(self):
        p1 = geometry.conversion_probability(100.0, 1e-10)
        p3 = geometry.conversion_probability(100.0, 3e-10)
        self.assertAlmostEqual(p3 / p1, 9.0, places=9)


if __name__ == "__main__":
    unittest.main()
