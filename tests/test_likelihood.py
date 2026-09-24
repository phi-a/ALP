import unittest

import numpy as np

from darknessalp import likelihood


class TestFisher(unittest.TestCase):
    def test_single_template_is_root_n(self):
        mu = np.array([[100.0, 400.0], [900.0, 1600.0]])
        sigma = likelihood.profiled_sigma(mu, [], mu)
        self.assertAlmostEqual(sigma, 1 / np.sqrt(mu.sum()), places=12)

    def test_two_templates_by_hand(self):
        mu = np.array([2.0, 4.0])
        s, z = np.array([1.0, 1.0]), np.array([1.0, -1.0])
        info = likelihood.fisher([s, z], mu)
        np.testing.assert_allclose(info, [[0.75, 0.25], [0.25, 0.75]])

    def test_orthogonal_nuisance_costs_nothing(self):
        mu = np.ones(4)
        s, z = np.array([1.0, 1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0, 1.0])
        self.assertAlmostEqual(likelihood.information_fraction(s, [z], mu),
                               1.0)

    def test_collinear_nuisance_removes_everything(self):
        rng = np.random.default_rng(0)
        mu = np.ones(50)
        s = rng.uniform(1.0, 2.0, 50)
        z = s * (1 + 1e-6 * rng.normal(size=50))
        self.assertLess(likelihood.information_fraction(s, [z], mu), 1e-6)

    def test_gaussian_upper_limit(self):
        self.assertAlmostEqual(float(likelihood.upper_limit(1.0)), 1.2816,
                               places=4)
        self.assertAlmostEqual(float(likelihood.upper_limit(2.0, 0.95)),
                               3.2897, places=4)


class TestFit(unittest.TestCase):
    """Signal injection: bias and coverage of the profiled error."""

    def test_recovers_injected_amplitude_with_coverage(self):
        rng = np.random.default_rng(7)
        t = np.linspace(0.0, 2 * np.pi, 60)
        k = 1 + 0.8 * np.cos(t)                    # kernel-like
        z1 = np.ones_like(t)                       # constant background
        z2 = 1 + 0.5 * np.sin(t)                   # a confounder
        theta, beta = 15.0, (400.0, 200.0)
        mu = theta * k + beta[0] * z1 + beta[1] * z2
        sigma = likelihood.profiled_sigma(k, [z1, z2], mu)
        hits, estimates = 0, []
        for _ in range(400):
            counts = rng.poisson(mu)
            fit = likelihood.fit_amplitudes(counts, [k, z1, z2], mu)
            estimates.append(fit[0])
            hits += abs(fit[0] - theta) < sigma
        bias = np.mean(estimates) - theta
        self.assertLess(abs(bias), 0.15 * sigma)
        self.assertGreater(hits / 400, 0.62)
        self.assertLess(hits / 400, 0.74)


if __name__ == "__main__":
    unittest.main()
