import unittest

import numpy as np

from darknessalp import background, kinematics, pointing


class TestPointingAndBackground(unittest.TestCase):
    def test_named_and_radec_targets(self):
        gc = pointing.target("gc")
        self.assertAlmostEqual(np.linalg.norm(gc), 1.0)
        v = pointing.target("0,90")
        np.testing.assert_allclose(v, [0, 0, 1.0], atol=1e-12)

    def test_fixed_inertial_and_feasible(self):
        n = pointing.fixed_inertial([1.0, 0, 0], 3)
        self.assertEqual(n.shape, (3, 3))
        r = np.array([6791.2, 0, 0])
        ok = pointing.feasible(r, np.array([[1.0, 0, 0], [-1.0, 0, 0]]),
                               np.array([0, 1.0, 0]))
        np.testing.assert_array_equal(ok, [True, False])

    def test_look_at_and_slew(self):
        rot = kinematics.look_at([0, 1.0, 0])
        np.testing.assert_allclose(kinematics.boresight(rot), [0, 1.0, 0],
                                   atol=1e-12)
        self.assertAlmostEqual(
            kinematics.angle_between([[1.0, 0, 0]], [[0, 1.0, 0]])[0], 90.0)
        self.assertAlmostEqual(kinematics.slew_time_s(90.0), 120.0)

    def test_backgrounds(self):
        self.assertAlmostEqual(background.cxb_intensity(1.0), 11.6)
        self.assertAlmostEqual(background.cxb_rate(6.0, 0.0955), 9.9, 1)
        self.assertAlmostEqual(background.nxb_proxy(10.0), 1.0)
        self.assertGreater(background.nxb_proxy(2.0), 1.0)
        self.assertGreater(background.grxe_brightness(0, 0),
                           background.grxe_brightness(90, 0))
        names = [s[0] for s in background.sources_in_cone(
            pointing.target("gc"))]
        self.assertIn("GX 3+1", names)
        self.assertNotIn("Sco X-1", names)


if __name__ == "__main__":
    unittest.main()
