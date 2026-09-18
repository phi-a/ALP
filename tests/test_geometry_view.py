import unittest

import numpy as np

from darknessalp import geometry, kinematics


class TestGeometryView(unittest.TestCase):
    def test_limb_angles_at_420_km(self):
        r = np.array([6791.2, 0.0, 0.0])
        n = np.array([[-1.0, 0, 0], [1.0, 0, 0], [0, 1.0, 0]])
        np.testing.assert_allclose(geometry.limb_angle(r, n),
                                   [-69.74, 110.26, 20.26], atol=0.01)
        ring = geometry.limb_directions(r, 12)
        sep = kinematics.angle_between(ring, np.tile([-1.0, 0, 0], (12, 1)))
        np.testing.assert_allclose(sep, 69.74, atol=0.01)

    def test_umbra(self):
        r = np.array([[-7000.0, 0, 0], [7000.0, 0, 0], [-7000.0, 6500.0, 0]])
        sun = np.tile([1.0, 0, 0], (3, 1))
        np.testing.assert_array_equal(geometry.in_umbra(r, sun),
                                      [True, False, False])

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
