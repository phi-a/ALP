from __future__ import annotations

from math import cos, radians, sin, sqrt

from .models import MissionConfig, OptimizationResult

EARTH_RADIUS_M = 6_371_000.0
EARTH_MU_M3_S2 = 3.986_004_418e14
EARTH_DIPOLE_MOMENT_A_M2 = 7.94e22
MU0_OVER_4PI = 1.0e-7


def norm(vector: tuple[float, float, float]) -> float:
    x, y, z = vector
    return sqrt(x * x + y * y + z * z)


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(vector: tuple[float, float, float], scalar: float) -> tuple[float, float, float]:
    return (vector[0] * scalar, vector[1] * scalar, vector[2] * scalar)


def circular_orbit_state(
    altitude_km: float,
    inclination_deg: float,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    radius_m = EARTH_RADIUS_M + altitude_km * 1_000.0
    speed_m_s = sqrt(EARTH_MU_M3_S2 / radius_m)
    inclination_rad = radians(inclination_deg)

    position = (radius_m, 0.0, 0.0)
    velocity = (
        0.0,
        speed_m_s * cos(inclination_rad),
        speed_m_s * sin(inclination_rad),
    )
    return position, velocity


def gravity_acceleration(position: tuple[float, float, float]) -> tuple[float, float, float]:
    radius = norm(position)
    factor = -EARTH_MU_M3_S2 / (radius**3)
    return scale(position, factor)


def rk4_step(
    position: tuple[float, float, float],
    velocity: tuple[float, float, float],
    dt_s: float,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    a1 = gravity_acceleration(position)
    p2 = add(position, scale(velocity, 0.5 * dt_s))
    v2 = add(velocity, scale(a1, 0.5 * dt_s))

    a2 = gravity_acceleration(p2)
    p3 = add(position, scale(v2, 0.5 * dt_s))
    v3 = add(velocity, scale(a2, 0.5 * dt_s))

    a3 = gravity_acceleration(p3)
    p4 = add(position, scale(v3, dt_s))
    v4 = add(velocity, scale(a3, dt_s))

    a4 = gravity_acceleration(p4)

    position_next = add(
        position,
        scale(
            add(add(velocity, scale(add(v2, v3), 2.0)), v4),
            dt_s / 6.0,
        ),
    )
    velocity_next = add(
        velocity,
        scale(
            add(add(a1, scale(add(a2, a3), 2.0)), a4),
            dt_s / 6.0,
        ),
    )
    return position_next, velocity_next


def dipole_magnetic_field_t(position: tuple[float, float, float]) -> tuple[float, float, float]:
    radius = norm(position)
    radius_hat = scale(position, 1.0 / radius)
    dipole_axis = (0.0, 0.0, 1.0)

    axis_projection = dot(dipole_axis, radius_hat)
    first_term = scale(radius_hat, 3.0 * axis_projection)
    shape_term = (
        first_term[0] - dipole_axis[0],
        first_term[1] - dipole_axis[1],
        first_term[2] - dipole_axis[2],
    )
    magnitude = MU0_OVER_4PI * EARTH_DIPOLE_MOMENT_A_M2 / (radius**3)
    return scale(shape_term, magnitude)


def simulate_magnetic_exposure(config: MissionConfig) -> float:
    if config.step_s <= 0.0:
        raise ValueError("step_s must be positive")
    if config.duration_s <= 0.0:
        raise ValueError("duration_s must be positive")

    position, velocity = circular_orbit_state(
        altitude_km=config.altitude_km,
        inclination_deg=config.inclination_deg,
    )

    steps = max(1, int(config.duration_s / config.step_s))
    accumulated_score = 0.0

    for _ in range(steps):
        field_t = dipole_magnetic_field_t(position)
        field_strength = norm(field_t)
        accumulated_score += (field_strength**config.magnetic_weight_power) * config.step_s
        position, velocity = rk4_step(position, velocity, config.step_s)

    return accumulated_score


def optimize_mission(
    altitudes_km: list[float],
    inclinations_deg: list[float],
    duration_s: float = 5400.0,
    step_s: float = 10.0,
    magnetic_weight_power: float = 2.0,
) -> OptimizationResult:
    best_result: OptimizationResult | None = None

    for altitude_km in altitudes_km:
        for inclination_deg in inclinations_deg:
            score = simulate_magnetic_exposure(
                MissionConfig(
                    altitude_km=altitude_km,
                    inclination_deg=inclination_deg,
                    duration_s=duration_s,
                    step_s=step_s,
                    magnetic_weight_power=magnetic_weight_power,
                )
            )
            candidate = OptimizationResult(
                altitude_km=altitude_km,
                inclination_deg=inclination_deg,
                score=score,
            )
            if best_result is None or candidate.score > best_result.score:
                best_result = candidate

    if best_result is None:
        raise ValueError("at least one altitude and one inclination are required")

    return best_result


def default_altitudes_km() -> list[float]:
    return [400.0, 500.0, 600.0, 700.0]


def default_inclinations_deg() -> list[float]:
    return [0.0, 28.5, 51.6, 70.0, 90.0, 98.0]
