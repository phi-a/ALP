import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from darknessalp import dynamics, frames, orbit
from darknessalp.constants import J2, MU_EARTH_KM3_S2, R_EQUATOR_KM

A_ISS = R_EQUATOR_KM + 420.0

# external-style OEM: header comments, two segments on different frames,
# day-of-year epochs, acceleration columns, a covariance block
EXTERNAL_OEM = """CCSDS_OEM_VERS = 2.0
COMMENT written by hand in the GMAT / CCSDS 502.0-B-3 layout
CREATION_DATE = 2027-120T12:00:00
ORIGINATOR = TEST

META_START
COMMENT first segment
OBJECT_NAME = ISS
OBJECT_ID = 1998-067A
CENTER_NAME = EARTH
REF_FRAME = EME2000
TIME_SYSTEM = UTC
START_TIME = 2027-121T00:00:00.000
USEABLE_START_TIME = 2027-121T00:00:00.000
USEABLE_STOP_TIME = 2027-121T00:01:00.000
STOP_TIME = 2027-121T00:01:00.000
INTERPOLATION = HERMITE
INTERPOLATION_DEGREE = 7
META_STOP

COMMENT state vectors with accelerations
2027-121T00:00:00.000 6798.137 0.000 0.000 0.000 4.747 5.994 -0.009 0 0
2027-121T00:01:00.000 6790.595 284.586 359.340 -0.251 4.740 5.985 -0.009 0 0

COVARIANCE_START
EPOCH = 2027-121T00:00:00.000
COV_REF_FRAME = RTN
1.0e-3
1.0e-6 1.0e-3
1.0e-6 1.0e-6 1.0e-3
1.0e-9 1.0e-9 1.0e-9 1.0e-6
1.0e-9 1.0e-9 1.0e-9 1.0e-9 1.0e-6
1.0e-9 1.0e-9 1.0e-9 1.0e-9 1.0e-9 1.0e-6
COVARIANCE_STOP

META_START
OBJECT_NAME = ISS
OBJECT_ID = 1998-067A
CENTER_NAME = EARTH
REF_FRAME = ICRF
TIME_SYSTEM = UTC
START_TIME = 2027-05-01T00:02:00.000
STOP_TIME = 2027-05-01T00:02:00.000
META_STOP
2027-05-01T00:02:00.000 6768.020 568.198 717.483 -0.502 4.719 5.958
"""


def node_deg(r, v):
    h = np.cross(r, v)
    return np.degrees(np.unwrap(np.arctan2(h[:, 0], -h[:, 1])))


def node_rate_deg_day(a_km, inc_deg, days=2.0):
    """Return the fitted node rate of a J2 propagation."""
    r0, v0 = orbit.elements_to_state(a_km, 0.0, inc_deg, 0.0, 0.0, 0.0)
    t = np.arange(0.0, days * 86400.0, 60.0)
    r, v = orbit.propagate(r0, v0, t)
    return np.polyfit(t / 86400.0, node_deg(r, v), 1)[0]


class TestElements(unittest.TestCase):
    def test_circular_state(self):
        r, v = orbit.elements_to_state(A_ISS, 0.0, 51.6, 40.0, 0.0, 70.0)
        self.assertAlmostEqual(np.linalg.norm(r), A_ISS)
        self.assertAlmostEqual(np.linalg.norm(v),
                               np.sqrt(MU_EARTH_KM3_S2 / A_ISS))
        self.assertAlmostEqual(float(np.dot(r[0], v[0])), 0.0, places=9)

    def test_angles_place_the_state(self):
        r, v = orbit.elements_to_state(A_ISS, 0.0, 51.6, 0.0, 0.0, 0.0)
        np.testing.assert_allclose(r[0], [A_ISS, 0.0, 0.0], atol=1e-9)
        s = np.sqrt(MU_EARTH_KM3_S2 / A_ISS)
        i = np.radians(51.6)
        np.testing.assert_allclose(v[0], [0.0, s * np.cos(i), s * np.sin(i)],
                                   atol=1e-12)

    def test_eccentric_apsides_and_vis_viva(self):
        a, e = 8000.0, 0.1
        r, v = orbit.elements_to_state(a, e, 30.0, 10.0, 20.0, [0.0, 180.0])
        radius = np.linalg.norm(r, axis=1)
        np.testing.assert_allclose(radius, [a * (1 - e), a * (1 + e)])
        np.testing.assert_allclose(
            np.sum(v * v, axis=1), MU_EARTH_KM3_S2 * (2 / radius - 1 / a))


class TestPropagate(unittest.TestCase):
    def test_point_mass_closes_after_one_period(self):
        r0, v0 = orbit.elements_to_state(A_ISS, 0.0, 90.0, 0.0, 0.0, 0.0)
        t = np.array([0.0, orbit.period_s(A_ISS)])
        r, _ = orbit.propagate(r0, v0, t, gravity="point")
        np.testing.assert_allclose(r[1], r[0], atol=1e-3)

    def test_max_latitude_is_inclination(self):
        r0, v0 = orbit.elements_to_state(A_ISS, 0.0, 51.6, 0.0, 0.0, 0.0)
        r, _ = orbit.propagate(r0, v0, np.arange(0, 6000, 10.0), "point")
        sin_lat = r[:, 2] / np.linalg.norm(r, axis=1)
        self.assertAlmostEqual(sin_lat.max(), np.sin(np.radians(51.6)),
                               places=4)

    def test_j2_node_regression_matches_the_secular_rate(self):
        n = np.sqrt(MU_EARTH_KM3_S2 / A_ISS**3)
        secular = (-1.5 * n * J2 * (R_EQUATOR_KM / A_ISS) ** 2
                   * np.cos(np.radians(51.6)))
        expected = np.degrees(secular) * 86400.0
        self.assertAlmostEqual(node_rate_deg_day(A_ISS, 51.6) / expected,
                               1.0, delta=0.01)

    def test_custom_acceleration_matches_the_named_model(self):
        r0, v0 = orbit.elements_to_state(A_ISS, 0.0, 51.6, 0.0, 0.0, 0.0)
        t = np.arange(0, 3000, 60.0)
        named, _ = orbit.propagate(r0, v0, t, gravity="point")
        custom, _ = orbit.propagate(r0, v0, t, gravity=dynamics.two_body)
        np.testing.assert_array_equal(named, custom)

    def test_zero_time_returns_the_initial_state(self):
        r0, v0 = orbit.elements_to_state(A_ISS, 0.0, 51.6, 0.0, 0.0, 0.0)
        r, v = orbit.propagate(r0, v0, 0.0)
        np.testing.assert_array_equal(r, r0)
        np.testing.assert_array_equal(v, v0)

    def test_j2_acceleration_direction(self):
        a = dynamics.j2_acceleration(np.array([[7000.0, 0.0, 0.0]]))[0]
        self.assertLess(a[0], 0.0)  # extra pull toward the equator bulge
        self.assertAlmostEqual(a[1], 0.0)
        self.assertAlmostEqual(a[2], 0.0)


class TestOem(unittest.TestCase):
    def setUp(self):
        r0, v0 = orbit.elements_to_state(A_ISS, 0.0, 51.6, 0.0, 0.0, 0.0)
        self.t = np.arange(0.0, 600.0, 60.0)
        self.time = frames.times("2027-05-01T00:00:00", self.t)
        self.r, self.v = orbit.propagate(r0, v0, self.t)
        self.tmp = TemporaryDirectory()
        self.path = Path(self.tmp.name) / "darkness.oem"

    def tearDown(self):
        self.tmp.cleanup()

    def test_kvn_header(self):
        orbit.write_oem(self.path, self.time, self.r, self.v)
        lines = self.path.read_text().splitlines()
        self.assertEqual(lines[0], "CCSDS_OEM_VERS = 2.0")
        for key in ("CENTER_NAME = EARTH", "REF_FRAME = GCRF",
                    "TIME_SYSTEM = UTC", "META_START", "META_STOP",
                    "START_TIME = 2027-05-01T00:00:00.000000"):
            self.assertIn(key, lines)
        self.assertEqual(len(lines[-1].split()), 7)

    def test_gcrf_round_trip(self):
        orbit.write_oem(self.path, self.time, self.r, self.v)
        time, r, v = orbit.read_oem(self.path)
        np.testing.assert_allclose(r, self.r, atol=1e-6)
        np.testing.assert_allclose(v, self.v, atol=1e-9)
        np.testing.assert_allclose((time - self.time).sec, 0.0, atol=1e-6)

    def test_eme2000_round_trip(self):
        orbit.write_oem(self.path, self.time, self.r, self.v, "EME2000")
        first = self.path.read_text().splitlines()[-len(self.t)].split()
        moved = np.linalg.norm(np.array(first[1:4], float) - self.r[0])
        self.assertGreater(moved, 1e-4)      # the bias moves LEO ~1 m
        _, r, v = orbit.read_oem(self.path)
        np.testing.assert_allclose(r, self.r, atol=1e-6)
        np.testing.assert_allclose(v, self.v, atol=1e-9)

    def test_external_layout(self):
        self.path.write_text(EXTERNAL_OEM)
        time, r, v = orbit.read_oem(self.path)
        self.assertEqual(r.shape, (3, 3))
        self.assertEqual(v.shape, (3, 3))
        np.testing.assert_allclose((time - self.time[0]).sec,
                                   [0.0, 60.0, 120.0], atol=1e-6)
        eme = np.array([[6798.137, 0.0, 0.0], [6790.595, 284.586, 359.340]])
        np.testing.assert_allclose(r[:2], frames.eme2000_to_gcrf(eme),
                                   atol=1e-9)
        np.testing.assert_allclose(r[2], [6768.020, 568.198, 717.483])
        np.testing.assert_allclose(v[2], [-0.502, 4.719, 5.958])

    def test_rejects_other_centre(self):
        self.path.write_text(EXTERNAL_OEM.replace(
            "CENTER_NAME = EARTH", "CENTER_NAME = MARS BARYCENTER", 1))
        with self.assertRaises(ValueError):
            orbit.read_oem(self.path)


if __name__ == "__main__":
    unittest.main()
