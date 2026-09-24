import unittest

import astropy.units as u
import numpy as np
from astropy.cosmology import Planck18

from darknessalp import source
from darknessalp.source.halo import (
    KPC_CM, R_MAX_KPC, R_S_KPC, R_SUN_KPC, RHO_S_GEV_CM3)
from darknessalp.source.spectra import C_CM_S, GYR_S


class TestHalo(unittest.TestCase):
    def test_local_density(self):
        self.assertAlmostEqual(source.nfw_density(R_SUN_KPC), 0.4)

    def test_anticentre_closed_form(self):
        def f(x):
            return np.log(x / (1 + x)) + 1 / (1 + x)
        x0, x1 = R_SUN_KPC / R_S_KPC, (R_SUN_KPC + R_MAX_KPC) / R_S_KPC
        exact = RHO_S_GEV_CM3 * R_S_KPC * KPC_CM * (f(x1) - f(x0))
        self.assertAlmostEqual(source.column_density(180.0, 0.0)[()] / exact,
                               1.0, places=6)

    def test_axisymmetric_about_the_centre_direction(self):
        d = source.column_density([5.0, 0.0, -5.0], [0.0, 5.0, 0.0])
        np.testing.assert_allclose(d, d[0], rtol=1e-6)

    def test_centre_exceeds_anticentre(self):
        gc, anti = source.column_density([0.0, 180.0], [0.0, 0.0])
        self.assertGreater(gc / anti, 5.0)


class TestSpectra(unittest.TestCase):
    """Block B checks. Dror, Murayama & Rodd 2021 (DMR) is the reference."""

    @classmethod
    def setUpClass(cls):
        cls.d_sky = source.sky_column(3.0)          # GeV cm^-2 sr
        cls.t_u = Planck18.age(0).to_value(u.Gyr)

    def test_full_sky_column_matches_dmr(self):
        """DMR footnote 8: 2.7e32 eV cm^-2 sr for a canonical NFW."""
        self.assertAlmostEqual(self.d_sky / 2.7e23, 1.0, delta=0.03)

    def test_dm_density(self):
        self.assertAlmostEqual(source.dm_density_kev_cm3(), 1.26, delta=0.01)

    def test_line_units_by_hand(self):
        # I = share D / (2 pi m tau): Yamamoto+ 2020 eq. 2.2 with S -> D
        d, m, tau = 1e23, 7.0, 13.69
        by_hand = (d * u.GeV / u.cm**2 / (2 * np.pi * m * u.keV
                                          * tau * u.Gyr)).to_value(
            1 / (u.cm**2 * u.s))
        self.assertAlmostEqual(source.line_intensity(d, m, 1.0, tau)
                               / by_hand, 1.0, places=9)
        self.assertAlmostEqual(by_hand / 5.26e9, 1.0, delta=0.01)

    def test_line_is_narrow_before_the_detector(self):
        sigma = source.line_sigma_kev(7.0)
        self.assertAlmostEqual(sigma / 3.5, 5.5e-4, delta=0.1e-4)
        self.assertLess(sigma, 0.05 * 0.17)      # far below 170 eV FWHM

    def test_continuum_support(self):
        e = np.array([0.5, 3.4999, 3.5, 4.0, 10.0])
        i = source.continuum_intensity(e, 7.0, 1.0, 1e3)
        self.assertTrue(np.all(i[:2] > 0))
        np.testing.assert_array_equal(i[2:], 0.0)

    def test_continuum_is_the_yamamoto_power_law(self):
        # I = C E^1/2 f(x), x = m/2E, f = (Om + Ok/x + OL/x^3)^-1/2
        m = 7.0
        e = np.linspace(0.2, 0.999, 50) * m / 2
        x = m / (2 * e)
        f = (Planck18.Om0 + Planck18.Ok0 / x
             + Planck18.Ode0 / x**3) ** -0.5
        ratio = source.continuum_intensity(e, m, 1.0, 1e6) / (np.sqrt(e) * f)
        np.testing.assert_allclose(ratio, ratio[0], rtol=3e-3)
        coefficient = (C_CM_S / (4 * np.pi) * 2 ** 2.5
                       * source.dm_density_kev_cm3()
                       / (Planck18.H0.to_value(1 / u.s) * m**2.5
                          * 1e6 * GYR_S))
        self.assertAlmostEqual(ratio[0] / coefficient, 1.0, delta=3e-3)

    def test_energy_densities_match_dmr(self):
        """DMR sec. II: rho_MW ~ 2 rho_EG at tau >> t_U; the pair exceeds
        the CMB for tau below ~1e4 t_U."""
        m, tau = 7.0, 1e6
        e = np.linspace(1e-3, 1.0, 20001) * m / 2
        rho_eg = 4 * np.pi / C_CM_S * np.trapezoid(
            e * source.continuum_intensity(e, m, 1.0, tau), e)
        rho_mw = m / 2 * source.line_intensity(self.d_sky, m, 1.0, tau) \
            / C_CM_S
        self.assertAlmostEqual(rho_mw / rho_eg, 2.3, delta=0.2)
        tau_cmb = tau * (rho_eg + rho_mw) / 0.260e-3    # CMB: 0.26 eV cm^-3
        self.assertAlmostEqual(np.log10(tau_cmb / self.t_u), 4.0, delta=0.3)

    def test_todays_share_against_primordial(self):
        # more parents alive in the past: intensity rises with 1/tau faster
        # than linearly once tau ~ t_U
        e, m = 1.0, 7.0
        slow = source.continuum_intensity(e, m, 1.0, 1e4)[0] * 1e4
        fast = source.continuum_intensity(e, m, 1.0, 10.0)[0] * 10.0
        self.assertGreater(fast / slow, 1.5)


if __name__ == "__main__":
    unittest.main()
