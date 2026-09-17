"""Command-line entry point for the Yamamoto Suzaku geometry validation."""

from __future__ import annotations

import argparse
import json

from darknessalp.yamamoto.validation import validate_observation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a Suzaku state table and validate the geomagnetic ALP regressor."
    )
    parser.add_argument("--obsid", default="101002010")
    parser.add_argument("--xis", type=int, default=0)
    parser.add_argument("--data-root", default="data/suzaku")
    parser.add_argument("--output-root", default="outputs")
    parser.add_argument("--cadence-s", type=float, default=60.0)
    parser.add_argument("--q-per-m", type=float, default=0.0)
    parser.add_argument("--initial-intervals", type=int, default=32)
    parser.add_argument("--max-intervals", type=int, default=256)
    parser.add_argument("--relative-tolerance", type=float, default=0.01)
    parser.add_argument(
        "--max-samples",
        type=int,
        help="Limit rows for smoke tests; omit for the full observation.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    summary = validate_observation(
        args.obsid,
        data_root=args.data_root,
        output_root=args.output_root,
        xis=args.xis,
        cadence_s=args.cadence_s,
        q_per_m=args.q_per_m,
        initial_intervals=args.initial_intervals,
        max_intervals=args.max_intervals,
        relative_tolerance=args.relative_tolerance,
        max_samples=args.max_samples,
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["acceptance"]["vertical_slice_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

