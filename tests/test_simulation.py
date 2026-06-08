import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from darknessalp.models import MissionConfig
from darknessalp.simulation import optimize_mission, simulate_magnetic_exposure


class SimulationTests(unittest.TestCase):
    def test_exposure_score_is_positive(self) -> None:
        score = simulate_magnetic_exposure(
            MissionConfig(altitude_km=500.0, inclination_deg=51.6, duration_s=600.0, step_s=10.0)
        )
        self.assertGreater(score, 0.0)

    def test_lower_altitude_has_higher_field_exposure(self) -> None:
        low_score = simulate_magnetic_exposure(
            MissionConfig(altitude_km=400.0, inclination_deg=51.6, duration_s=600.0, step_s=10.0)
        )
        high_score = simulate_magnetic_exposure(
            MissionConfig(altitude_km=700.0, inclination_deg=51.6, duration_s=600.0, step_s=10.0)
        )
        self.assertGreater(low_score, high_score)

    def test_optimizer_returns_requested_grid_point(self) -> None:
        result = optimize_mission(
            altitudes_km=[400.0, 700.0],
            inclinations_deg=[0.0, 90.0],
            duration_s=600.0,
            step_s=10.0,
        )
        self.assertIn(result.altitude_km, [400.0, 700.0])
        self.assertIn(result.inclination_deg, [0.0, 90.0])


if __name__ == "__main__":
    unittest.main()
