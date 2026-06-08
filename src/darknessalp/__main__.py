from __future__ import annotations

from .simulation import default_altitudes_km, default_inclinations_deg, optimize_mission


def main() -> None:
    result = optimize_mission(
        altitudes_km=default_altitudes_km(),
        inclinations_deg=default_inclinations_deg(),
    )
    print("Best coarse configuration:")
    print(f"  altitude_km={result.altitude_km:.1f}")
    print(f"  inclination_deg={result.inclination_deg:.1f}")
    print(f"  score={result.score:.6e}")


if __name__ == "__main__":
    main()

