import unittest

import numpy as np
from scipy.spatial.transform import Rotation

from darknessalp import background, frames, kinematics, orbit, pointing
from darknessalp.constants import R_EQUATOR_KM


class TestTargets(unittest.TestCase):
    def setUp(self):
        self.t = np.arange(0, 600, 60.0)
        self.time = frames.times("2027-05-01T00:00:00", self.t)
        r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + 420.0, 0.0, 51.6,
                                         0.0, 0.0, 0.0)
        self.r, self.v = orbit.propagate(r0, v0, self.t, "point")

    def test_sky_targets(self):
        self.assertAlmostEqual(np.linalg.norm(pointing.sky_target("gc")), 1)
        np.testing.assert_allclose(pointing.sky_target("0,90"), [0, 0, 1.0],
                                   atol=1e-12)

    def test_orbit_based_directions(self):
        d = {s: pointing.target_direction(s, self.time, self.r, self.v)
             for s in ("zenith", "nadir", "velocity", "orbit_normal")}
        np.testing.assert_allclose(d["zenith"], -d["nadir"])
        dots = np.sum(d["velocity"] * d["zenith"], axis=1)
        np.testing.assert_allclose(dots, 0.0, atol=1e-9)
        dots = np.sum(d["orbit_normal"] * d["velocity"], axis=1)
        np.testing.assert_allclose(dots, 0.0, atol=1e-9)

    def test_bodies_and_field_rules(self):
        moon = pointing.target_direction("moon", self.time, self.r)
        np.testing.assert_allclose(np.linalg.norm(moon, axis=1), 1.0)
        sun = pointing.target_direction("sun", self.time, self.r)
        anti = pointing.target_direction("anti_sun", self.time, self.r)
        self.assertGreater(np.sum(sun[0] * -anti[0]), 0.999)
        b = np.tile([0.0, 0.0, 1.0], (len(self.t), 1))
        perp = pointing.target_direction("b_perp", self.time, self.r,
                                         self.v, b)
        np.testing.assert_allclose(np.sum(perp * b, axis=1), 0.0, atol=1e-9)
        self.assertTrue(np.all(np.sum(perp * self.r, axis=1) > 0))
        along = pointing.target_direction("b_along", self.time, self.r,
                                          self.v, b)
        self.assertTrue(np.all(np.sum(along * self.r, axis=1) >= 0))

    def test_mode_roll_puts_radiator_away_from_earth(self):
        m = pointing.mode("gc", roll="anti_earth")
        rot = pointing.desired_attitude(m, self.time, self.r, self.v)
        bore = kinematics.boresight(rot)
        np.testing.assert_allclose(bore, np.tile(pointing.sky_target("gc"),
                                                 (len(self.t), 1)), atol=1e-9)
        rad = kinematics.radiator_normal(rot)
        self.assertTrue(np.all(np.sum(rad * self.r, axis=1) > 0))

    def test_schedule_and_attitudes(self):
        conds = pointing.conditions(self.time, self.r)
        rules = [("umbra", pointing.mode("gc")),
                 ("always", pointing.mode("anti_sun", roll="anti_earth"))]
        index, modes = pointing.select(rules, conds)
        self.assertEqual(len(modes), 2)
        self.assertTrue(np.all(index[conds["umbra"]] == 0))
        rot = pointing.attitudes(modes, index, self.time, self.r, self.v)
        self.assertEqual(len(rot), len(self.t))
        with self.assertRaises(ValueError):
            pointing.select([("umbra", modes[0])],
                            {"umbra": np.zeros(3, bool)})


class TestSteering(unittest.TestCase):
    def test_rate_limited_slew(self):
        a = kinematics.look_at([1.0, 0, 0])
        b = kinematics.look_at([0, 1.0, 0])                # 90 deg away
        t = np.arange(0, 121, 10.0)
        desired = Rotation.concatenate([b] * len(t))
        cmd, err, slewing = kinematics.steer(desired, t, 1.5, start=a)
        self.assertAlmostEqual(err[0], 90.0)
        self.assertAlmostEqual(err[4], 30.0)               # 40 s at 1.5/s
        self.assertAlmostEqual(err[-1], 0.0)
        self.assertTrue(slewing[0] and not slewing[-1])
        np.testing.assert_allclose(kinematics.boresight(cmd[-1]),
                                   [[0, 1.0, 0]], atol=1e-9)


class TestBackground(unittest.TestCase):
    def test_backgrounds(self):
        self.assertAlmostEqual(background.cxb_intensity(1.0), 11.6)
        self.assertAlmostEqual(background.cxb_rate(6.0, 0.0955), 9.9, 1)
        self.assertAlmostEqual(background.nxb_proxy(10.0), 1.0)
        self.assertGreater(background.grxe_brightness(0, 0),
                           background.grxe_brightness(90, 0))
        names = [s[0] for s in background.sources_in_cone(
            pointing.sky_target("gc"))]
        self.assertIn("GX 3+1", names)
        self.assertNotIn("Sco X-1", names)


if __name__ == "__main__":
    unittest.main()
