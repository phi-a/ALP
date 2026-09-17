"""Geometry and transverse magnetic-field line-of-sight integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

EARTH_REFERENCE_RADIUS_KM = 6371.2

FieldFunction = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class FieldIntegral:
    """Result of a convergence-controlled transverse-field integral."""

    vector_tm: np.ndarray
    magnitude_tm: float
    magnitude_squared_t2m2: float
    exit_distance_km: float
    intervals: int
    relative_change: float
    converged: bool
    earth_intersection: bool


def _unit(vector) -> np.ndarray:
    value = np.asarray(vector, dtype=float).reshape(3)
    norm = float(np.linalg.norm(value))
    if not np.isfinite(norm) or norm == 0.0:
        raise ValueError("direction must be a finite nonzero 3-vector")
    return value / norm


def ray_sphere_exit_distance(
    position_km,
    direction,
    sphere_radius_km: float,
) -> float:
    """Return the forward distance at which a ray exits a centered sphere."""

    r = np.asarray(position_km, dtype=float).reshape(3)
    n = _unit(direction)
    radius = float(sphere_radius_km)
    if radius <= 0.0:
        raise ValueError("sphere_radius_km must be positive")
    r2 = float(r @ r)
    if r2 >= radius * radius:
        raise ValueError("ray origin must be inside the integration sphere")
    along = float(r @ n)
    discriminant = along * along + radius * radius - r2
    if discriminant < 0.0:
        raise ValueError("ray does not intersect the integration sphere")
    distance = -along + np.sqrt(discriminant)
    if distance <= 0.0:
        raise ValueError("integration-sphere intersection is not forward")
    return float(distance)


def ray_intersects_earth(
    position_km,
    direction,
    earth_radius_km: float = EARTH_REFERENCE_RADIUS_KM,
) -> bool:
    """Return whether the forward ray intersects a spherical Earth."""

    r = np.asarray(position_km, dtype=float).reshape(3)
    n = _unit(direction)
    along = float(r @ n)
    if along >= 0.0:
        return False
    closest2 = float(r @ r) - along * along
    return closest2 <= float(earth_radius_km) ** 2


def _integral_on_grid(
    position_km: np.ndarray,
    direction: np.ndarray,
    exit_distance_km: float,
    field_gcrf_t: FieldFunction,
    intervals: int,
    q_per_m: float,
) -> np.ndarray:
    s_km = np.linspace(0.0, exit_distance_km, intervals + 1)
    positions = position_km[None, :] + s_km[:, None] * direction[None, :]
    fields = np.asarray([field_gcrf_t(point) for point in positions], dtype=float)
    if fields.shape != positions.shape or not np.all(np.isfinite(fields)):
        raise ValueError("field_gcrf_t must return one finite 3-vector per position")
    transverse = fields - (fields @ direction)[:, None] * direction[None, :]
    phase = np.exp(-1j * float(q_per_m) * s_km * 1000.0)
    integrand = transverse.astype(complex) * phase[:, None]
    return np.trapezoid(integrand, s_km * 1000.0, axis=0)


def integrate_transverse_field(
    position_gcrf_km,
    direction_gcrf,
    field_gcrf_t: FieldFunction,
    *,
    outer_radius_re: float = 6.0,
    earth_radius_km: float = EARTH_REFERENCE_RADIUS_KM,
    q_per_m: float = 0.0,
    initial_intervals: int = 32,
    max_intervals: int = 256,
    relative_tolerance: float = 0.01,
) -> FieldIntegral:
    """Integrate the transverse field vector from a spacecraft to ``outer_radius_re``."""

    if initial_intervals < 2 or max_intervals < initial_intervals:
        raise ValueError("integration interval bounds are inconsistent")
    if relative_tolerance <= 0.0:
        raise ValueError("relative_tolerance must be positive")

    r = np.asarray(position_gcrf_km, dtype=float).reshape(3)
    n = _unit(direction_gcrf)
    intersects = ray_intersects_earth(r, n, earth_radius_km)
    if intersects:
        return FieldIntegral(
            vector_tm=np.full(3, np.nan + 0j),
            magnitude_tm=np.nan,
            magnitude_squared_t2m2=np.nan,
            exit_distance_km=np.nan,
            intervals=0,
            relative_change=np.nan,
            converged=False,
            earth_intersection=True,
        )

    exit_distance = ray_sphere_exit_distance(
        r, n, float(outer_radius_re) * float(earth_radius_km)
    )
    intervals = int(initial_intervals)
    previous = _integral_on_grid(
        r, n, exit_distance, field_gcrf_t, intervals, q_per_m
    )
    relative_change = np.inf
    current = previous

    while intervals < max_intervals:
        intervals = min(intervals * 2, max_intervals)
        current = _integral_on_grid(
            r, n, exit_distance, field_gcrf_t, intervals, q_per_m
        )
        scale = max(float(np.linalg.norm(current)), 1e-30)
        relative_change = float(np.linalg.norm(current - previous) / scale)
        if relative_change <= relative_tolerance:
            break
        previous = current

    magnitude = float(np.linalg.norm(current))
    return FieldIntegral(
        vector_tm=current,
        magnitude_tm=magnitude,
        magnitude_squared_t2m2=magnitude * magnitude,
        exit_distance_km=exit_distance,
        intervals=intervals,
        relative_change=relative_change,
        converged=relative_change <= relative_tolerance,
        earth_intersection=False,
    )

