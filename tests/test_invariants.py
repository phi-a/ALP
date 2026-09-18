"""Physical invariants: things that must hold whatever the inputs."""
import unittest

import numpy as np

from darknessalp import (
    dynamics, field, frames, geometry, kinematics, orbit, pointing)
from darknessalp.constants import MU_EARTH_KM3_S2


class TestOrbitInvariants(unittest.TestCase):
    def test_two_body_conserves_energy_and_angular_momentum(self):
        r0, v0 = orbit.circular_orbit(0.0, 420.0, 51.6)
        t = np.arange(0, 5600, 100.0)
        r, v = orbit.propagate(r0[0], v0[0], t, acceleration=dynamics.two_body)
        speed2 = np.sum(v * v, axis=1)
        radius = np.linalg.norm(r, axis=1)
        energy = speed2 / 2 - MU_EARTH_KM3_S2 / radius
        h = np.cross(r, v)
        self.assertLess(np.ptp(energy) / abs(energy[0]), 1e-9)
        self.assertLess(np.ptp(np.linalg.norm(h, axis=1)) / np.linalg.norm(
            h[0]), 1e-9)

    def test_j2_conserves_energy_and_polar_angular_momentum(self):
        # J2 is conservative and axisymmetric: h_z is the constant, not |h|
        r0, v0 = orbit.circular_orbit(0.0, 420.0, 51.6)
        t = np.arange(0, 5600, 100.0)
        r, v = orbit.propagate(r0[0], v0[0], t)
        h_z = np.cross(r, v)[:, 2]
        self.assertLess(np.ptp(h_z) / abs(h_z[0]), 1e-9)


class TestAttitudeInvariants(unittest.TestCase):
    def test_body_axes_stay_orthonormal(self):
        n = np.array([[1.0, 0, 0], [0.3, -0.5, 0.81]])
        rot = kinematics.look_at(n)
        bore = kinematics.boresight(rot)
        rad = kinematics.radiator_normal(rot)
        np.testing.assert_allclose(np.linalg.norm(bore, axis=1), 1.0)
        np.testing.assert_allclose(np.linalg.norm(rad, axis=1), 1.0)
        np.testing.assert_allclose(np.sum(bore * rad, axis=1), 0.0,
                                   atol=1e-12)

    def test_steering_never_exceeds_the_rate(self):
        t = np.arange(0, 600, 10.0)
        start = kinematics.look_at([1.0, 0, 0])
        desired = kinematics.look_at(np.tile([0, 0, 1.0], (len(t), 1)))
        cmd, _, _ = kinematics.steer(desired, t, 1.5, start=start)
        step = np.degrees((cmd[1:] * cmd[:-1].inv()).magnitude())
        self.assertLessEqual(step.max(), 1.5 * 10.0 + 1e-9)


class TestFieldInvariants(unittest.TestCase):
    def setUp(self):
        self.coeffs = field.load_igrf(2027.0)

    def test_field_magnitude_is_frame_independent(self):
        time = frames.times("2027-05-01T00:00:00", 0.0)
        r_eci = np.array([[5000.0, 3000.0, 3500.0]])
        b_ecef = field.igrf_field(frames.eci_to_ecef(r_eci, time),
                                  self.coeffs)
        b_eci = field.igrf_field_eci(r_eci, time, self.coeffs)
        self.assertAlmostEqual(np.linalg.norm(b_ecef),
                               np.linalg.norm(b_eci), places=15)

    def test_truncation_converges_with_degree(self):
        r = np.array([[6791.2, 0.0, 0.0]])
        full = field.igrf_field(r, self.coeffs, lmax=13)
        errors = [np.linalg.norm(field.igrf_field(r, self.coeffs, lmax=n)
                                 - full) for n in (1, 4, 8, 12)]
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])))


class TestGeometryInvariants(unittest.TestCase):
    def setUp(self):
        self.coeffs = field.load_igrf(2027.0)
        self.time = frames.times("2027-05-01T00:00:00", 0.0)[0]
        self.r = orbit.circular_orbit(0.0, 420.0, 51.6)[0][0]

    def test_occultation_agrees_with_the_limb_angle(self):
        rng = np.random.default_rng(0)
        n = rng.normal(size=(200, 3))
        n /= np.linalg.norm(n, axis=1, keepdims=True)
        _, occulted = geometry.path_end_km(self.r, n)
        np.testing.assert_array_equal(occulted,
                                      geometry.limb_angle(self.r, n) < 0)

    def test_integral_is_linear_in_the_field(self):
        # doubling every coefficient must double the amplitude
        doubled = tuple(2 * c for c in self.coeffs)
        up = self.r / np.linalg.norm(self.r)
        one = geometry.los_field_integral(self.r, up, self.time, self.coeffs,
                                          lmax=1)["amplitude_tm"][0]
        two = geometry.los_field_integral(self.r, up, self.time, doubled,
                                          lmax=1)["amplitude_tm"][0]
        self.assertAlmostEqual(two / one, 2.0, places=9)

    def test_amplitude_does_not_depend_on_the_ray_ordering(self):
        rng = np.random.default_rng(1)
        n = rng.normal(size=(8, 3))
        n /= np.linalg.norm(n, axis=1, keepdims=True)
        order = rng.permutation(8)
        a = geometry.los_field_integral(self.r, n, self.time, self.coeffs,
                                        lmax=1)["amplitude_tm"]
        b = geometry.los_field_integral(self.r, n[order], self.time,
                                        self.coeffs, lmax=1)["amplitude_tm"]
        np.testing.assert_allclose(a[order], b)

    def test_cone_average_recovers_the_boresight_in_a_smooth_field(self):
        n = pointing.sky_target("gc")
        dirs, w = geometry.cone_directions(n, 10.0, 3)
        on_axis = geometry.los_field_integral(self.r, n, self.time,
                                              self.coeffs, lmax=1)
        cone = geometry.los_field_integral(self.r, dirs, self.time,
                                           self.coeffs, lmax=1)
        average = float(w @ cone["amplitude_tm"])
        self.assertAlmostEqual(average / on_axis["amplitude_tm"][0], 1.0,
                               delta=0.35)


if __name__ == "__main__":
    unittest.main()
