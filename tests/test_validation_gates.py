"""Gates against numbers from outside this repository.

If one of these fails, the physics is wrong, not the test. Each cites
where its number comes from.
"""
import unittest

import numpy as np

from darknessalp import background, field, frames, geometry, orbit
from darknessalp.constants import R_EARTH_KM


class TestPublishedNumbers(unittest.TestCase):
    def test_suzaku_like_geometry_matches_yamamoto(self):
        """Yamamoto+ 2020 report (B_perp L)^2 ~ 1e4-1e5 T^2 m^2."""
        coeffs = field.load_igrf(2010.0)
        t = np.arange(0, 5700, 300.0)
        time = frames.times("2010-01-01T00:00:00", t)
        r, _ = orbit.circular_orbit(t, 570.0, 31.0)   # Suzaku-like
        rng = np.random.default_rng(0)
        amplitudes = []
        for k in range(len(t)):
            n = rng.normal(size=(40, 3))
            n /= np.linalg.norm(n, axis=1, keepdims=True)
            res = geometry.los_field_integral(r[k], n, time[k], coeffs,
                                              lmax=1, n_steps=80)
            amplitudes.append(res["amplitude_tm"][~res["occulted"]])
        k2 = np.concatenate(amplitudes) ** 2
        self.assertGreater(np.median(k2), 1e4)
        self.assertLess(np.median(k2), 1e5)
        self.assertGreater(np.mean((k2 > 1e4) & (k2 < 1e5)), 0.4)

    def test_hand_calculation_of_the_surface_integral(self):
        """B_0 R_E / 2 ~ 100 T m, the Stage 3 paper estimate."""
        coeffs = field.load_igrf(2027.0)
        b0 = np.linalg.norm(field.dipole_moment(coeffs)) * 1e-9
        self.assertAlmostEqual(b0 * R_EARTH_KM * 1e3 / 2, 100.0, delta=20.0)

    def test_igrf_reproduces_published_surface_values(self):
        """NOAA/IGRF: ~32 uT at the equator, ~57 uT at the pole."""
        coeffs = field.load_igrf(2027.0)
        equator = np.array([[R_EARTH_KM, 0.0, 0.0]])
        pole = np.array([[0.0, 0.0, R_EARTH_KM]])
        self.assertAlmostEqual(
            np.linalg.norm(field.igrf_field(equator, coeffs)) * 1e9,
            31900, delta=400)
        self.assertAlmostEqual(
            np.linalg.norm(field.igrf_field(pole, coeffs)) * 1e9,
            56600, delta=400)

    def test_stormer_cutoff_at_the_equator(self):
        """Stormer: 14.9 GV vertical cut-off at the magnetic equator."""
        self.assertAlmostEqual(field.cutoff_rigidity(0.0, R_EARTH_KM), 14.9)

    def test_cxb_rate_in_the_darkness_cone(self):
        """De Luca & Molendi 2004 over 12 cm^2 x 0.0955 sr, 50% masked."""
        self.assertAlmostEqual(background.cxb_rate(6.0, 0.0955), 9.9,
                               delta=0.5)

    def test_orbital_periods(self):
        """ISS ~92.97 min at 420 km; 94.6 min at 500 km."""
        self.assertAlmostEqual(orbit.period_s(420.0) / 60, 92.97, delta=0.1)
        self.assertAlmostEqual(orbit.period_s(500.0) / 60, 94.6, delta=0.1)

    def test_sun_synchronous_inclination_gives_the_solar_rate(self):
        """An SSO precesses 360 deg/yr = 0.9856 deg/day."""
        r, v = orbit.circular_orbit([0.0, 86400.0], 500.0, 97.4)
        h = np.cross(r, v)
        node = np.degrees(np.arctan2(h[:, 0], -h[:, 1]))
        self.assertAlmostEqual(np.diff(node)[0], 0.9856, delta=0.01)


if __name__ == "__main__":
    unittest.main()
