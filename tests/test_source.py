import unittest

import numpy as np

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


if __name__ == "__main__":
    unittest.main()
