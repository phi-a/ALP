"""End-to-end run of the whole ritual, with its answers pinned.

This is the test that notices when a change to any one topic quietly
moves the result. Recompute and update the pins deliberately, never to
make the test pass.
"""
import unittest

import numpy as np

from darknessalp import frames, kinematics, orbit, pointing, sim
from darknessalp.constants import R_EQUATOR_KM

EPOCH = "2027-05-01T00:00:00"
CADENCE_S, DURATION_S = 600.0, 86400.0
ALT_KM, INC_DEG = 420.0, 51.6


def run_scenario():
    """Return (table, mode_index, slewing) for the reference schedule."""
    t = np.arange(0.0, DURATION_S, CADENCE_S)
    r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + ALT_KM, 0.0, INC_DEG,
                                     0.0, 0.0, 0.0)
    r, v = orbit.propagate(r0, v0, t, gravity="j2")
    time = frames.times(EPOCH, t)
    rules = [("umbra", pointing.mode("gc")),
             ("always", pointing.mode("anti_sun"))]
    index, modes = pointing.select(rules, pointing.conditions(time, r))
    desired = pointing.attitudes(modes, index, time, r, v)
    attitude, _, slewing = kinematics.steer(desired, t, 1.5,
                                            mode_index=index)
    boresight = kinematics.boresight(attitude)
    return sim.state_table(EPOCH, t, r, boresight, lmax=1), index, slewing


class TestScenarioRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table, cls.index, cls.slewing = run_scenario()
        cls.sky = (~cls.table["occulted"] & (cls.index == 0)
                   & ~cls.slewing)

    def test_duty_cycle(self):
        self.assertEqual(len(self.table["t_s"]), 144)
        self.assertEqual(int(self.table["umbra"].sum()), 54)
        self.assertEqual(int(self.table["occulted"].sum()), 57)
        self.assertEqual(int(self.slewing.sum()), 30)
        self.assertEqual(int(self.sky.sum()), 39)

    def test_conversion_kernel(self):
        amp = self.table["amp_tm"][self.sky]
        self.assertAlmostEqual(float(np.median(amp)), 76.79, delta=0.05)
        self.assertAlmostEqual(float(amp.max()), 158.30, delta=0.05)

    def test_fov_gradient(self):
        ratio = (self.table["k_fov_t2m2"] / self.table["k_t2m2"])[self.sky]
        self.assertAlmostEqual(float(np.median(ratio)), 1.016, delta=0.002)
        self.assertAlmostEqual(float(ratio.max()), 1.313, delta=0.005)

    def test_halo_column_over_the_aperture(self):
        d_ratio = (self.table["d_fov_gevcm2"] / self.table["d_gevcm2"])
        dk = self.table["dk_fov_gevcm2_t2m2"]
        dk_ratio = dk / (self.table["d_fov_gevcm2"] * self.table["k_fov_t2m2"])
        self.assertAlmostEqual(float(np.median(d_ratio[self.sky])), 0.641,
                               delta=0.002)
        self.assertAlmostEqual(float(np.median(dk_ratio[self.sky])), 0.995,
                               delta=0.002)

    def test_background_confounding(self):
        k = self.table["k_t2m2"][self.sky]
        rho_rc = np.corrcoef(k, self.table["cutoff_gv"][self.sky])[0, 1]
        rho_limb = np.corrcoef(k, self.table["limb_deg"][self.sky])[0, 1]
        self.assertAlmostEqual(rho_rc, 0.907, delta=0.005)
        self.assertAlmostEqual(rho_limb, -0.987, delta=0.005)

    def test_run_is_deterministic(self):
        again, _, _ = run_scenario()
        np.testing.assert_array_equal(again["amp_tm"],
                                      self.table["amp_tm"])


if __name__ == "__main__":
    unittest.main()
