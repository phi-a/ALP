import unittest

import numpy as np

from darknessalp import detector


class TestEfficiency(unittest.TestCase):
    def test_window_matches_the_asr_statement(self):
        """Alpine+ 2025 p. 4796: >98 % transmission down to 1 keV."""
        self.assertGreater(detector.window_transmission(1.0), 0.98)
        self.assertLess(detector.window_transmission(1.0), 0.99)

    def test_silicon_from_nist_attenuation(self):
        """NIST Si mu/rho at 10 keV: 33.89 cm^2/g; 500 um absorbs 98 %."""
        self.assertAlmostEqual(detector.silicon_absorption(10.0), 0.981,
                               places=3)
        self.assertAlmostEqual(detector.silicon_absorption(10.0, 725.0),
                               0.9967, places=3)

    def test_edges_and_dead_layer(self):
        # thick silicon absorbs everything either side of its K edge; a
        # dead layer makes the edge visible
        below, above = detector.quantum_efficiency([1.83, 1.85])
        self.assertAlmostEqual(below, above, delta=2e-3)
        below, above = detector.quantum_efficiency([1.83, 1.85], dead_um=1.0)
        self.assertGreater(below - above, 0.3)
        al_below, al_above = detector.window_transmission([1.55, 1.57])
        self.assertGreater(al_below, al_above)     # Al K edge

    def test_resolution_reproduces_the_measured_width(self):
        """Alpine+ 2026 Table 2: 169 eV FWHM at Mn K-alpha."""
        self.assertAlmostEqual(detector.resolution_fwhm_kev(5.895), 0.169,
                               places=3)
        fano_only = detector.resolution_fwhm_kev(5.895, noise_fwhm_kev=0.0)
        self.assertAlmostEqual(fano_only, 0.120, places=3)

    def test_grasp(self):
        self.assertAlmostEqual(detector.grasp_cm2sr(), 1.145, places=3)


class TestCounts(unittest.TestCase):
    def setUp(self):
        self.e = np.linspace(1.0, 10.0, 1801)
        self.edges = np.linspace(0.0, 12.0, 49)

    def test_constant_sky_recovers_the_grasp(self):
        """Contract: an isotropic constant-brightness source gives
        I x A Omega x dE x dt with every efficiency set to one."""
        i0, dt = 3.0, 600.0
        counts = detector.expected_counts(
            self.e, np.full_like(self.e, i0), self.edges, [1.0], [dt],
            qe=np.ones_like(self.e), live=1.0, fwhm_kev=1e-6)
        expected = i0 * detector.grasp_cm2sr() * 9.0 * dt
        self.assertEqual(counts.shape, (1, 48))
        self.assertAlmostEqual(counts.sum() / expected, 1.0, places=9)

    def test_redistribution_conserves_counts(self):
        r = detector.redistribution([2.0, 5.9, 9.0], self.edges)
        np.testing.assert_allclose(r.sum(axis=1), 1.0, rtol=1e-9)

    def test_monochromatic_line_is_conserved_and_widened_by_age(self):
        e0, sigma_src = 3.5, 0.002
        line = np.exp(-0.5 * ((self.e - e0) / sigma_src) ** 2)
        young = detector.expected_counts(self.e, line, self.edges, [1.0],
                                         [1.0], fwhm_kev=0.169)
        old = detector.expected_counts(self.e, line, self.edges, [1.0],
                                       [1.0], fwhm_kev=0.198)
        self.assertAlmostEqual(old.sum() / young.sum(), 1.0, places=9)
        self.assertLess(old.max(), young.max())

    def test_losses_enter_once_and_linearly(self):
        flat = np.ones_like(self.e)
        full = detector.expected_counts(self.e, flat, self.edges, [1.0],
                                        [1.0], live=1.0, select=1.0)
        half = detector.expected_counts(self.e, flat, self.edges, [1.0],
                                        [1.0], live=0.5, select=0.8)
        self.assertAlmostEqual(half.sum() / full.sum(), 0.4, places=9)

    def test_samples_scale_with_probability_and_time(self):
        flat = np.ones_like(self.e)
        counts = detector.expected_counts(self.e, flat, self.edges,
                                          [1e-17, 2e-17], [600.0, 300.0])
        self.assertAlmostEqual(counts[1].sum() / counts[0].sum(), 1.0,
                               places=9)


if __name__ == "__main__":
    unittest.main()
