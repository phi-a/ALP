import unittest
from math import cos, sin, sqrt

from darknessalp import schmidt_legendre


class TestSchmidtLegendre(unittest.TestCase):
    def test_degree_two_closed_forms(self):
        theta = 0.7
        c, s = cos(theta), sin(theta)
        p, dp = schmidt_legendre(2, theta)
        self.assertAlmostEqual(p[1][0], c)
        self.assertAlmostEqual(p[1][1], s)
        self.assertAlmostEqual(p[2][0], (3 * c * c - 1) / 2)
        self.assertAlmostEqual(p[2][1], sqrt(3) * s * c)
        self.assertAlmostEqual(p[2][2], sqrt(3) / 2 * s * s)
        self.assertAlmostEqual(dp[1][0], -s)
        self.assertAlmostEqual(dp[2][0], -3 * s * c)
        self.assertAlmostEqual(dp[2][2], sqrt(3) * s * c)

    def test_derivative_by_finite_difference(self):
        h = 1e-5
        p_plus, _ = schmidt_legendre(13, 1.1 + h)
        p_minus, _ = schmidt_legendre(13, 1.1 - h)
        _, dp = schmidt_legendre(13, 1.1)
        for n in range(14):
            for m in range(n + 1):
                fd = (p_plus[n][m] - p_minus[n][m]) / (2 * h)
                self.assertAlmostEqual(dp[n][m], fd, places=5)


if __name__ == "__main__":
    unittest.main()
