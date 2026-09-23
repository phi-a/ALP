import unittest

import numpy as np
from scipy.integrate import quad

from darknessalp import source
from darknessalp.source.halo import (
    KPC_CM, R_MAX_KPC, R_S_KPC, R_SUN_KPC, RHO_S_GEV_CM3)


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


class TestCab(unittest.TestCase):
    def test_unit_norm_and_mean(self):
        total = quad(source.cab_spectrum, 0.0, np.inf)[0]
        mean = quad(lambda e: e * source.cab_spectrum(e), 0.0, np.inf)[0]
        self.assertAlmostEqual(total, 1.0, places=8)
        self.assertAlmostEqual(mean, 0.238, places=8)

    def test_band_fraction(self):
        self.assertAlmostEqual(source.cab_band_fraction(0.0, np.inf), 1.0)
        self.assertAlmostEqual(source.cab_band_fraction(1.0, 10.0),
                               6.19e-4, delta=0.01e-4)
        self.assertAlmostEqual(source.cab_band_fraction(1.0, 10.0, 0.532),
                               0.110, delta=0.001)

    def test_flux_scales_with_delta_neff(self):
        self.assertAlmostEqual(source.cab_flux(1.14) / source.cab_flux(),
                               2.0)


if __name__ == "__main__":
    unittest.main()
