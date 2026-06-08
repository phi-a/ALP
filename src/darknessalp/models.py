from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MissionConfig:
    altitude_km: float
    inclination_deg: float
    duration_s: float = 5400.0
    step_s: float = 10.0
    magnetic_weight_power: float = 2.0


@dataclass(slots=True)
class OptimizationResult:
    altitude_km: float
    inclination_deg: float
    score: float

