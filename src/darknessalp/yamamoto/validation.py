"""End-to-end Yamamoto geometry validation and artifact generation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from darknessalp.yamamoto import __version__
from darknessalp.yamamoto.geometry import integrate_transverse_field
from darknessalp.yamamoto.schema import STATE_UNITS
from darknessalp.yamamoto.suzaku import load_suzaku_states

INTEGRAL_UNITS = {
    "b_integral_gcrf_x_tm_real": "T m",
    "b_integral_gcrf_y_tm_real": "T m",
    "b_integral_gcrf_z_tm_real": "T m",
    "b_integral_gcrf_x_tm_imag": "T m",
    "b_integral_gcrf_y_tm_imag": "T m",
    "b_integral_gcrf_z_tm_imag": "T m",
    "b_perp_l_tm": "T m",
    "b_perp_l_squared_t2m2": "T2 m2",
    "los_exit_distance_km": "km",
    "integration_relative_change": "dimensionless",
    "q_per_m": "1/m",
}


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_revision(path: str | Path) -> str | None:
    root = Path(path)
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        # Sandboxed users can trigger Git's dubious-ownership guard. Resolve a
        # normal checkout's HEAD without changing global safe.directory state.
        git_dir = root / ".git"
        head_path = git_dir / "HEAD"
        if not head_path.is_file():
            return None
        head = head_path.read_text(encoding="ascii").strip()
        if not head.startswith("ref: "):
            return head or None
        ref = head.removeprefix("ref: ")
        loose = git_dir / ref
        if loose.is_file():
            return loose.read_text(encoding="ascii").strip() or None
        packed = git_dir / "packed-refs"
        if packed.is_file():
            for line in packed.read_text(encoding="ascii").splitlines():
                if line and not line.startswith(("#", "^")):
                    revision, name = line.split(" ", 1)
                    if name == ref:
                        return revision
        return None


def _flag_counts(rows: list[dict]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        flags = str(row.get("quality_flags", ""))
        for flag in filter(None, flags.split("|")):
            counts[flag] += 1
    return dict(sorted(counts.items()))


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _plot_time(rows: list[dict], path: Path) -> None:
    valid = [row for row in rows if np.isfinite(row["b_perp_l_squared_t2m2"])]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    if valid:
        t0 = min(row["mission_time_tt_s"] for row in valid)
        segments: list[list[dict]] = [[valid[0]]]
        for left, right in zip(valid, valid[1:]):
            if right["mission_time_tt_s"] - left["mission_time_tt_s"] > 90.0:
                ax.axvspan(
                    (left["mission_time_tt_s"] - t0) / 3600.0,
                    (right["mission_time_tt_s"] - t0) / 3600.0,
                    color="0.85",
                    linewidth=0,
                )
                segments.append([])
            segments[-1].append(right)
        for segment in segments:
            ax.plot(
                [(row["mission_time_tt_s"] - t0) / 3600.0 for row in segment],
                [row["b_perp_l_squared_t2m2"] for row in segment],
                marker=".",
                markersize=3,
                linewidth=0.8,
                color="#1f77b4",
            )
    ax.axhspan(1e4, 1e5, color="#2a9d8f", alpha=0.12, label="Yamamoto typical range")
    ax.set_yscale("log")
    ax.set_xlabel("Elapsed time from first valid sample [hour]")
    ax.set_ylabel(r"$|\int B_\perp ds|^2$ [T$^2$ m$^2$]")
    ax.set_title("Suzaku 101002010 geomagnetic conversion regressor")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_histogram(rows: list[dict], path: Path) -> None:
    values = np.asarray(
        [
            row["b_perp_l_squared_t2m2"]
            for row in rows
            if np.isfinite(row["b_perp_l_squared_t2m2"])
        ]
    )
    fig, ax = plt.subplots(figsize=(7, 4.8))
    if len(values):
        bins = np.geomspace(max(values.min(), 1.0), values.max() * 1.001, 30)
        ax.hist(values, bins=bins, color="#4472c4", edgecolor="white")
    ax.axvspan(1e4, 1e5, color="#2a9d8f", alpha=0.12)
    ax.set_xscale("log")
    ax.set_xlabel(r"$|\int B_\perp ds|^2$ [T$^2$ m$^2$]")
    ax.set_ylabel("60 s samples")
    ax.set_title("Valid conversion-regressor distribution")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_covariates(rows: list[dict], path: Path) -> None:
    rows = [row for row in rows if np.isfinite(row["b_perp_l_squared_t2m2"])]
    fields = [
        ("cor2_gv", "COR2 [GV]"),
        ("latitude_deg", "Geodetic latitude [deg]"),
        ("longitude_deg", "Geodetic longitude [deg east]"),
        ("earth_limb_elevation_deg", "Earth-limb elevation [deg]"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharey=True)
    y = [row["b_perp_l_squared_t2m2"] for row in rows]
    for ax, (field, label) in zip(axes.flat, fields):
        ax.scatter([row[field] for row in rows], y, s=7, alpha=0.55)
        ax.set_xlabel(label)
        ax.set_yscale("log")
        ax.grid(alpha=0.2)
    axes[0, 0].set_ylabel(r"$|\int B_\perp ds|^2$ [T$^2$ m$^2$]")
    axes[1, 0].set_ylabel(r"$|\int B_\perp ds|^2$ [T$^2$ m$^2$]")
    fig.suptitle("Conversion regressor versus orbital background covariates")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def validate_observation(
    obsid: str = "101002010",
    *,
    data_root: str | Path = "data/suzaku",
    output_root: str | Path = "outputs",
    xis: int | None = 0,
    cadence_s: float = 60.0,
    q_per_m: float = 0.0,
    initial_intervals: int = 32,
    max_intervals: int = 256,
    relative_tolerance: float = 0.01,
    max_samples: int | None = None,
    loaded_igrf_model=None,
) -> dict:
    """Run the archived Suzaku geometry validation and write its artifacts."""

    import forms
    from forms.bricks.mag import geomagnetic_field, load_igrf_model

    states, source = load_suzaku_states(
        obsid, data_root=data_root, xis=xis, cadence_s=cadence_s
    )
    if max_samples is not None:
        states = states[: int(max_samples)]
    if not states:
        raise ValueError("the selected observation produced no state samples")

    model = loaded_igrf_model if loaded_igrf_model is not None else load_igrf_model()
    rows: list[dict] = []
    for state in states:
        row = state.to_dict()
        flags = list(filter(None, state.quality_flags.split("|")))
        if state.data_valid:
            def field(position):
                return geomagnetic_field(
                    position,
                    state.mjd2000_tt,
                    model="igrf13",
                    lmax=13,
                    loaded_model=model,
                    return_cartesian="gcrs",
                )

            result = integrate_transverse_field(
                state.position_gcrf_km,
                state.boresight_gcrf,
                field,
                outer_radius_re=6.0,
                q_per_m=q_per_m,
                initial_intervals=initial_intervals,
                max_intervals=max_intervals,
                relative_tolerance=relative_tolerance,
            )
            if result.earth_intersection:
                flags.append("earth_intersection_geometry")
            if not result.converged and not result.earth_intersection:
                flags.append("integration_not_converged")
            vector = result.vector_tm
            row.update(
                {
                    "b_integral_gcrf_x_tm_real": float(np.real(vector[0])),
                    "b_integral_gcrf_y_tm_real": float(np.real(vector[1])),
                    "b_integral_gcrf_z_tm_real": float(np.real(vector[2])),
                    "b_integral_gcrf_x_tm_imag": float(np.imag(vector[0])),
                    "b_integral_gcrf_y_tm_imag": float(np.imag(vector[1])),
                    "b_integral_gcrf_z_tm_imag": float(np.imag(vector[2])),
                    "b_perp_l_tm": result.magnitude_tm,
                    "b_perp_l_squared_t2m2": result.magnitude_squared_t2m2,
                    "los_exit_distance_km": result.exit_distance_km,
                    "integration_intervals": result.intervals,
                    "integration_relative_change": result.relative_change,
                    "integration_converged": result.converged,
                    "earth_intersection_geometry": result.earth_intersection,
                    "q_per_m": q_per_m,
                }
            )
        else:
            row.update(
                {
                    "b_integral_gcrf_x_tm_real": np.nan,
                    "b_integral_gcrf_y_tm_real": np.nan,
                    "b_integral_gcrf_z_tm_real": np.nan,
                    "b_integral_gcrf_x_tm_imag": np.nan,
                    "b_integral_gcrf_y_tm_imag": np.nan,
                    "b_integral_gcrf_z_tm_imag": np.nan,
                    "b_perp_l_tm": np.nan,
                    "b_perp_l_squared_t2m2": np.nan,
                    "los_exit_distance_km": np.nan,
                    "integration_intervals": 0,
                    "integration_relative_change": np.nan,
                    "integration_converged": False,
                    "earth_intersection_geometry": False,
                    "q_per_m": q_per_m,
                }
            )
        row["quality_flags"] = "|".join(dict.fromkeys(flags))
        row["yamamoto_screen_pass"] = bool(
            state.data_valid
            and state.saa == 0
            and state.cor2_gv >= 8.0
            and state.earth_limb_elevation_deg >= 5.0
            and state.day_earth_limb_elevation_deg >= 20.0
        )
        rows.append(row)

    output_dir = Path(output_root) / f"yamamoto_{obsid}"
    output_dir.mkdir(parents=True, exist_ok=True)
    table_path = output_dir / "frame_state.csv"
    _write_csv(table_path, rows)
    _plot_time(rows, output_dir / "field_integral_time.png")
    _plot_histogram(rows, output_dir / "field_integral_histogram.png")
    _plot_covariates(rows, output_dir / "field_integral_covariates.png")

    values = np.asarray(
        [
            row["b_perp_l_squared_t2m2"]
            for row in rows
            if np.isfinite(row["b_perp_l_squared_t2m2"])
        ]
    )
    screened_values = np.asarray(
        [
            row["b_perp_l_squared_t2m2"]
            for row in rows
            if row["yamamoto_screen_pass"]
            and np.isfinite(row["b_perp_l_squared_t2m2"])
        ]
    )
    converged = [row for row in rows if row["integration_converged"]]
    raw_median = float(np.median(values)) if len(values) else np.nan
    screened_median = (
        float(np.median(screened_values)) if len(screened_values) else np.nan
    )
    valid_fraction = len(values) / len(rows)
    converged_fraction = len(converged) / len(rows)
    geometry_scale_pass = bool(1e4 <= screened_median <= 1e5)
    numerical_pass = converged_fraction >= 0.99

    forms_root = Path(forms.__file__).resolve().parents[3]
    crosscheck_state = next(state for state in states if state.data_valid)
    handle = forms.FORMS()
    handle.time.sync(crosscheck_state.mjd2000_tt)
    handle.satellite.set_state([*crosscheck_state.position_gcrf_km, 0.0, 0.0, 0.0])
    handle.derive.advance()
    handle.derive.ensure("magnetic_field")
    bgcrs = handle.get_variable("BGCRS")
    handle_field = np.asarray([bgcrs.x, bgcrs.y, bgcrs.z], dtype=float)
    direct_field = geomagnetic_field(
        crosscheck_state.position_gcrf_km,
        crosscheck_state.mjd2000_tt,
        loaded_model=model,
        return_cartesian="gcrs",
    )
    crosscheck_difference = handle_field - direct_field
    crosscheck_abs = float(np.max(np.abs(crosscheck_difference)))
    crosscheck_rel = float(
        np.linalg.norm(crosscheck_difference) / np.linalg.norm(direct_field)
    )
    crosscheck_pass = crosscheck_abs <= 1e-15

    provenance = {
        "analysis_version": __version__,
        "forms_version": forms.__version__,
        "forms_module": str(Path(forms.__file__).resolve()),
        "forms_git_revision": _git_revision(forms_root),
        "analysis_git_revision": _git_revision(Path.cwd()),
        "field_model": "IGRF-13",
        "field_lmax": 13,
        "outer_boundary_re": 6.0,
        "q_per_m": q_per_m,
        "integration_initial_intervals": initial_intervals,
        "integration_max_intervals": max_intervals,
        "integration_relative_tolerance": relative_tolerance,
        "max_samples": max_samples,
        "units": {**STATE_UNITS, **INTEGRAL_UNITS},
        "sources": {
            **source,
            "ehk_sha256": _sha256(source["ehk_path"]),
            "event_sha256": {
                path: _sha256(path) for path in source["event_paths"]
            },
        },
    }
    summary = {
        "obsid": obsid,
        "sample_count": len(rows),
        "valid_integral_count": int(len(values)),
        "valid_integral_fraction": valid_fraction,
        "converged_count": len(converged),
        "converged_fraction": converged_fraction,
        "sample_exposure_s": float(sum(row["exposure_s"] for row in rows)),
        "gti_exposure_s": source["gti_exposure_s"],
        "b_perp_l_squared_t2m2": {
            "minimum": float(np.min(values)) if len(values) else None,
            "p05": float(np.quantile(values, 0.05)) if len(values) else None,
            "median": raw_median if len(values) else None,
            "p95": float(np.quantile(values, 0.95)) if len(values) else None,
            "maximum": float(np.max(values)) if len(values) else None,
        },
        "yamamoto_screen": {
            "criterion": "SAA == 0, COR2 >= 8 GV, ELV >= 5 deg, DYE_ELV >= 20 deg",
            "sample_count": int(len(screened_values)),
            "exposure_s": float(
                sum(row["exposure_s"] for row in rows if row["yamamoto_screen_pass"])
            ),
            "minimum_t2m2": (
                float(np.min(screened_values)) if len(screened_values) else None
            ),
            "median_t2m2": screened_median if len(screened_values) else None,
            "maximum_t2m2": (
                float(np.max(screened_values)) if len(screened_values) else None
            ),
        },
        "bgcrs_crosscheck": {
            "sample_id": crosscheck_state.sample_id,
            "maximum_absolute_difference_t": crosscheck_abs,
            "relative_vector_difference": crosscheck_rel,
            "pass": crosscheck_pass,
        },
        "quality_flag_counts": _flag_counts(rows),
        "acceptance": {
            "geometry_scale_pass": geometry_scale_pass,
            "numerical_convergence_pass": numerical_pass,
            "bgcrs_crosscheck_pass": crosscheck_pass,
            "vertical_slice_pass": (
                geometry_scale_pass and numerical_pass and crosscheck_pass
            ),
            "criterion": (
                "screened median in [1e4, 1e5] T2 m2, at least 99% of all rows "
                "converged, and direct field equals handle BGCRS"
            ),
        },
        "provenance_file": "provenance.json",
        "state_table": "frame_state.csv",
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary
