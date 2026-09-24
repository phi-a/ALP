import unittest

import numpy as np

from darknessalp import geometry, kinematics
from darknessalp.constants import (
    MU_EARTH_KM3_S2, R_EQUATOR_KM, R_SUN_KM)


class TestGeometryView(unittest.TestCase):
    def test_limb_angles_at_420_km(self):
        r = np.array([6791.2, 0.0, 0.0])
        n = np.array([[-1.0, 0, 0], [1.0, 0, 0], [0, 1.0, 0]])
        np.testing.assert_allclose(geometry.limb_angle(r, n),
                                   [-69.74, 110.26, 20.26], atol=0.01)
        ring = geometry.limb_directions(r, 12)
        sep = kinematics.angle_between(ring, np.tile([-1.0, 0, 0], (12, 1)))
        np.testing.assert_allclose(sep, 69.74, atol=0.01)

    def test_conical_shadow(self):
        d, au = 6800.0, 1.495978707e8
        edge = np.pi - np.arcsin(R_EQUATOR_KM / d)  # Sun centre on the limb
        r = np.array([[-d, 0, 0], [d, 0, 0], [-d, 6500.0, 0],
                      [d * np.cos(edge), d * np.sin(edge), 0]])
        s = geometry.shadow(r, np.tile([au, 0, 0], (4, 1)))
        np.testing.assert_array_equal(s["umbra"], [1, 0, 0, 0])
        np.testing.assert_array_equal(s["sunlit"], [0, 1, 1, 0])
        np.testing.assert_array_equal(s["penumbra"], [0, 0, 0, 1])
        self.assertAlmostEqual(s["lit_fraction"][3], 0.5, delta=0.02)

    def test_penumbra_lasts_seconds_in_leo(self):
        d = 6800.0
        phi = np.radians(np.linspace(105, 115, 20001))
        r = d * np.stack([np.cos(phi), np.sin(phi), 0 * phi], 1)
        s = geometry.shadow(r, np.array([1.495978707e8, 0, 0]))
        period = 2 * np.pi * np.sqrt(d**3 / MU_EARTH_KM3_S2)
        width = s["penumbra"].sum() * (phi[1] - phi[0]) / (2 * np.pi)
        sun_disk = 2 * np.arcsin(R_SUN_KM / 1.495978707e8)
        self.assertAlmostEqual(width * period,
                               sun_disk / (2 * np.pi) * period, delta=0.05)

    def test_projection_preserves_angle(self):
        n = np.array([1.0, 0, 0])
        x, y = geometry.fov_axes(n)
        v = geometry.offset_direction(3.0, 4.0, n, x, y)
        px, py = geometry.project(v, n, x, y)
        np.testing.assert_allclose([px[0], py[0]], [3.0, 4.0], atol=1e-9)
        self.assertAlmostEqual(kinematics.angle_between(v, n)[0], 5.0)

    def test_cone_quadrature(self):
        dirs, w = geometry.cone_directions(np.array([0, 0, 1.0]), 10.0, 3)
        self.assertAlmostEqual(w.sum(), 1.0)
        sep = kinematics.angle_between(dirs, np.tile([0, 0, 1.0],
                                                     (len(dirs), 1)))
        self.assertLessEqual(sep.max(), 10.0)


if __name__ == "__main__":
    unittest.main()
