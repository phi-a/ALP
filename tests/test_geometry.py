import numpy as np

from darknessalp.yamamoto.geometry import (
    integrate_transverse_field,
    ray_intersects_earth,
    ray_sphere_exit_distance,
)


def test_ray_sphere_exit_radially_outward():
    assert np.isclose(ray_sphere_exit_distance([2, 0, 0], [1, 0, 0], 5), 3)


def test_ray_intersection_distinguishes_nadir_and_zenith():
    assert ray_intersects_earth([7000, 0, 0], [-1, 0, 0])
    assert not ray_intersects_earth([7000, 0, 0], [1, 0, 0])


def test_uniform_transverse_field_matches_analytic_integral():
    field = lambda _: np.array([0.0, 2e-6, 0.0])
    result = integrate_transverse_field(
        [7000, 0, 0],
        [1, 0, 0],
        field,
        outer_radius_re=2.0,
        initial_intervals=4,
        max_intervals=8,
    )
    expected = 2e-6 * (2 * 6371.2 - 7000) * 1000
    assert result.converged
    assert np.isclose(result.magnitude_tm, expected)


def test_parallel_field_integrates_to_zero():
    field = lambda _: np.array([3e-5, 0.0, 0.0])
    result = integrate_transverse_field(
        [7000, 0, 0],
        [1, 0, 0],
        field,
        outer_radius_re=2.0,
        initial_intervals=4,
        max_intervals=8,
    )
    assert result.magnitude_tm == 0.0


def test_sign_changing_field_cancels():
    midpoint = (2 * 6371.2 + 7000) / 2

    def field(position):
        sign = -1.0 if position[0] < midpoint else 1.0
        return np.array([0.0, sign * 1e-6, 0.0])

    result = integrate_transverse_field(
        [7000, 0, 0],
        [1, 0, 0],
        field,
        outer_radius_re=2.0,
        initial_intervals=64,
        max_intervals=256,
        relative_tolerance=0.02,
    )
    assert result.magnitude_tm < 0.1

