"""Gates against numbers from outside this repository.

If one of these fails, the physics is wrong, not the test. Each cites
where its number comes from.
"""
import unittest

import numpy as np

from darknessalp import (
    background, detector, field, frames, geometry, orbit, source)
from darknessalp.constants import R_EARTH_KM, R_EQUATOR_KM


class TestPublishedNumbers(unittest.TestCase):
    def test_suzaku_like_geometry_matches_yamamoto(self):
        """Yamamoto+ 2020 report (B_perp L)^2 ~ 1e4-1e5 T^2 m^2."""
        coeffs = field.load_igrf(2010.0)
        t = np.arange(0, 5700, 300.0)
        time = frames.times("2010-01-01T00:00:00", t)
        r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + 570.0, 0.0, 31.0,
                                         0.0, 0.0, 0.0)  # Suzaku-like
        r, _ = orbit.propagate(r0, v0, t)
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

    def test_conversion_probability_matches_yamamoto(self):
        """Yamamoto+ 2020 eq. 2.13: 2.45e-21 (g/1e-10)^2 (BL/T m)^2."""
        self.assertAlmostEqual(
            geometry.conversion_probability(100.0, 1e-10) / 2.45e-17, 1.0,
            delta=0.003)

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
        for alt, minutes in ((420.0, 92.97), (500.0, 94.6)):
            self.assertAlmostEqual(orbit.period_s(R_EQUATOR_KM + alt) / 60,
                                   minutes, delta=0.1)

    def test_sun_synchronous_inclination_gives_the_solar_rate(self):
        """An SSO precesses 360 deg/yr = 0.9856 deg/day."""
        r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + 500.0, 0.0, 97.4,
                                         0.0, 0.0, 0.0)
        t = np.arange(0.0, 2 * 86400.0, 60.0)
        r, v = orbit.propagate(r0, v0, t)
        h = np.cross(r, v)
        node = np.degrees(np.unwrap(np.arctan2(h[:, 0], -h[:, 1])))
        rate = np.polyfit(t / 86400.0, node, 1)[0]
        self.assertAlmostEqual(rate, 0.9856, delta=0.01)

    def test_viability_gate_by_hand(self):
        """Notebook/2026-09-25-viability-by-hand: bounds to counts to gap."""
        g_max, f_over_tau = 0.47e-10, 4.0e-3  # DHV22, NTH21, GeV^-1, Gyr^-1
        d_gc, k_mean, t_day = 1.27e23, 8.3e3, 23400.0  # Block C
        i_line = source.line_intensity(d_gc, 7.0, 1.0, 1 / f_over_tau)
        prob = geometry.conversion_probability(k_mean**0.5, g_max)
        grasp = detector.grasp_cm2sr() * 0.5
        signal = i_line * prob * grasp * t_day
        self.assertAlmostEqual(signal / 2.2e-5, 1.0, delta=0.05)

        window = 2 * detector.resolution_fwhm_kev(3.5) / 2.355
        cxb = background.cxb_intensity(3.5) * window * grasp * t_day
        b_day = 2 * cxb  # flat particle proxy at the CXB level
        ratio = 1.28 * (187 * b_day) ** 0.5 / (187 * signal)
        self.assertAlmostEqual(ratio / 3.8e5, 1.0, delta=0.15)  # Block D
        self.assertGreater(ratio**2 * 5.0e6, 1e17)  # cm^2 sr s to close


if __name__ == "__main__":
    unittest.main()
