import unittest
from math import cos, radians, sin

from darknessalp import (
    angular_separation, earth_limb_directions, fov_axes, project_to_fov)


class TestProjectToFov(unittest.TestCase):
    def setUp(self):
        self.n = (1.0, 0.0, 0.0)
        self.x, self.y = fov_axes(self.n)

    def test_axes_are_orthonormal_and_y_is_up(self):
        self.assertEqual(self.y, (0.0, 0.0, 1.0))
        self.assertEqual(self.x, (0.0, 1.0, 0.0))  # x, y, n right-handed

    def test_offsets_preserve_angle(self):
        v = (cos(radians(7)), 0.0, sin(radians(7)))
        px, py = project_to_fov(v, self.n, self.x, self.y)
        self.assertAlmostEqual(px, 0.0)
        self.assertAlmostEqual(py, 7.0)
        self.assertAlmostEqual(angular_separation(v, self.n), 7.0)

    def test_limb_ring_sits_at_earth_angular_radius(self):
        r = (6791.2, 0.0, 0.0)
        nadir = (-1.0, 0.0, 0.0)
        for v in earth_limb_directions(r, 12):
            self.assertAlmostEqual(angular_separation(v, nadir), 69.74, 1)


if __name__ == "__main__":
    unittest.main()
