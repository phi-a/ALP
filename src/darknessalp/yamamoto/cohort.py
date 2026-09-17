"""Resumable four-field Yamamoto geometry-cohort validation."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from darknessalp.yamamoto import __version__
from darknessalp.yamamoto.archive import (
    DEFAULT_COHORT,
    PAPER_URL,
    PUBLISHED_BINS,
    THESIS_EXPOSURE_KS,
    THESIS_URL,
    inspect_products,
    prepare_observation,
    validate_manifest,
)
from darknessalp.yamamoto.schema import ProductStatus, SuzakuObservation
from darknessalp.yamamoto.validation import _git_revision, validate_observation

COHORT_UNITS = {
    "exposure_s": "s",
    "b_perp_l_tm": "T m",
    "b_perp_l_squared_t2m2": "T2 m2",
    "normalized_exposure_fraction": "dimensionless",
    "target_separation_deg": "deg great-circle",
}
EXPOSURE_MATCH_TOLERANCE_KS = 0.1


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None):
    fields = fieldnames or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as stream:
        if not fields:
            return
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _settings(
    *,
    cadence_s: float,
    q_per_m: float,
    initial_intervals: int,
    max_intervals: int,
    relative_tolerance: float,
    max_samples: int | None,
) -> dict:
    return {
        "analysis_version": __version__,
        "field_model": "IGRF-13",
        "field_lmax": 13,
        "outer_boundary_re": 6.0,
        "q_per_m": q_per_m,
        "integration_initial_intervals": initial_intervals,
        "integration_max_intervals": max_intervals,
        "integration_relative_tolerance": relative_tolerance,
        "cadence_s": cadence_s,
        "max_samples": max_samples,
    }


def _cache_is_current(
    output_dir: Path,
    product: ProductStatus,
    settings: dict,
    forms_revision: str | None,
) -> bool:
    paths = [
        output_dir / "summary.json",
        output_dir / "provenance.json",
        output_dir / "frame_state.csv",
    ]
    if product.status != "ready" or not all(path.is_file() for path in paths):
        return False
    try:
        provenance = json.loads(paths[1].read_text(encoding="utf-8"))
        sources = provenance["sources"]
        checks = {
            "analysis_version": provenance.get("analysis_version"),
            "field_model": provenance.get("field_model"),
            "field_lmax": provenance.get("field_lmax"),
            "outer_boundary_re": provenance.get("outer_boundary_re"),
            "q_per_m": provenance.get("q_per_m"),
            "integration_initial_intervals": provenance.get(
                "integration_initial_intervals"
            ),
            "integration_max_intervals": provenance.get("integration_max_intervals"),
            "integration_relative_tolerance": provenance.get(
                "integration_relative_tolerance"
            ),
            "cadence_s": sources.get("cadence_s"),
            "max_samples": provenance.get("max_samples"),
        }
        return (
            checks == settings
            and provenance.get("forms_git_revision") == forms_revision
            and sources.get("ehk_sha256") == _sha256(product.ehk_path)
            and sources.get("event_sha256")
            == {path: _sha256(path) for path in product.event_paths}
        )
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
        return False


def _read_rows(path: Path, observation: SuzakuObservation) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8") as stream:
        for raw in csv.DictReader(stream):
            try:
                value = float(raw["b_perp_l_tm"])
                squared = float(raw["b_perp_l_squared_t2m2"])
                exposure = float(raw["exposure_s"])
            except (KeyError, TypeError, ValueError):
                continue
            if not np.isfinite([value, squared, exposure]).all():
                continue
            rows.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "primary": observation.primary,
                    "b_perp_l_tm": value,
                    "b_perp_l_squared_t2m2": squared,
                    "exposure_s": exposure,
                    "screen_pass": str(raw.get("yamamoto_screen_pass", "")).lower()
                    == "true",
                    "integration_converged": str(
                        raw.get("integration_converged", "")
                    ).lower()
                    == "true",
                }
            )
    return rows


def _weighted_quantile(values, weights, quantiles=(0.05, 0.5, 0.95)) -> list[float]:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if not len(values) or weights.sum() <= 0:
        return [np.nan] * len(quantiles)
    order = np.argsort(values)
    values, weights = values[order], weights[order]
    centers = (np.cumsum(weights) - 0.5 * weights) / weights.sum()
    return [float(np.interp(q, centers, values)) for q in quantiles]


def _aggregate_fields(sample_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    field_rows: list[dict] = []
    bin_rows: list[dict] = []
    for field, published in PUBLISHED_BINS.items():
        rows = [
            row
            for row in sample_rows
            if row["primary"] and row["field"] == field and row["screen_pass"]
        ]
        values = np.asarray([row["b_perp_l_tm"] for row in rows])
        squared = np.asarray([row["b_perp_l_squared_t2m2"] for row in rows])
        weights = np.asarray([row["exposure_s"] for row in rows])
        p05, median, p95 = _weighted_quantile(squared, weights)
        field_rows.append(
            {
                "field": field,
                "sample_count": len(rows),
                "screened_exposure_s": float(weights.sum()),
                "b2_weighted_p05_t2m2": p05,
                "b2_weighted_median_t2m2": median,
                "b2_weighted_p95_t2m2": p95,
            }
        )
        edges = published["edges_tm"]
        means = published["means_t2m2"]
        for index, expected in enumerate(means):
            lower, upper = edges[index], edges[index + 1]
            in_bin = (values >= lower) & (
                values <= upper if index == len(means) - 1 else values < upper
            )
            bin_weight = float(weights[in_bin].sum())
            calculated = (
                float(np.average(squared[in_bin], weights=weights[in_bin]))
                if bin_weight > 0
                else None
            )
            relative = (
                abs(calculated - expected) / expected if calculated is not None else None
            )
            bin_rows.append(
                {
                    "field": field,
                    "bin_index": index + 1,
                    "lower_tm": lower,
                    "upper_tm": upper,
                    "published_mean_t2m2": expected,
                    "calculated_mean_t2m2": calculated,
                    "relative_difference": relative,
                    "within_15_percent": bool(relative <= 0.15)
                    if relative is not None
                    else False,
                    "sample_count": int(in_bin.sum()),
                    "exposure_s": bin_weight,
                    "normalized_exposure_fraction": (
                        bin_weight / weights.sum() if weights.sum() else 0.0
                    ),
                }
            )
    return field_rows, bin_rows


def _plot_distributions(sample_rows: list[dict], path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5))
    for ax, field in zip(axes.flat, PUBLISHED_BINS):
        rows = [
            row
            for row in sample_rows
            if row["primary"] and row["field"] == field and row["screen_pass"]
        ]
        values = np.asarray([row["b_perp_l_tm"] for row in rows])
        weights = np.asarray([row["exposure_s"] for row in rows])
        edges = np.asarray(PUBLISHED_BINS[field]["edges_tm"], dtype=float)
        if len(values) and weights.sum():
            limits = (min(values.min(), edges.min()), max(values.max(), edges.max()))
            bins = np.linspace(*limits, 32)
            ax.hist(
                values,
                bins=bins,
                weights=weights / weights.sum(),
                color="#4472c4",
                alpha=0.8,
            )
        for edge in edges:
            ax.axvline(edge, color="#b23a48", linewidth=0.8, alpha=0.75)
        ax.set_title(field)
        ax.set_xlabel(r"$|\int B_\perp ds|$ [T m]")
        ax.set_ylabel("Normalized exposure fraction")
        ax.grid(alpha=0.2)
    fig.suptitle("Suzaku geomagnetic conversion regressor by field")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def validate_cohort(
    observations: tuple[SuzakuObservation, ...] = DEFAULT_COHORT,
    *,
    data_root: str | Path = "data/suzaku",
    output_root: str | Path = "outputs",
    acquire: bool = False,
    force: bool = False,
    cadence_s: float = 60.0,
    q_per_m: float = 0.0,
    initial_intervals: int = 32,
    max_intervals: int = 256,
    relative_tolerance: float = 0.01,
    max_samples: int | None = None,
    observation_limit: int | None = None,
) -> dict:
    """Validate all ready observations and write a failure-isolated cohort package."""

    manifest_summary = validate_manifest(observations)
    if observation_limit is not None and observation_limit < 1:
        raise ValueError("observation_limit must be positive")
    selected_observations = (
        observations[: int(observation_limit)]
        if observation_limit is not None
        else observations
    )
    statuses = [
        (
            prepare_observation(item, data_root=data_root)
            if acquire
            else inspect_products(item, data_root=data_root)
        )
        for item in selected_observations
    ]
    status_by_obsid = {item.obsid: item for item in statuses}
    output_root = Path(output_root)
    cohort_dir = output_root / "yamamoto_cohort"
    cohort_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for observation, status in zip(selected_observations, statuses):
        manifest_rows.append(
            {
                **observation.to_dict(),
                "inclusion_status": (
                    "primary" if observation.primary else "supplemental"
                ),
                "product_status": status.status,
                "xis": status.xis,
                "ehk_path": status.ehk_path,
                "event_paths": ";".join(status.event_paths),
                "observed_ra_deg": status.observed_ra_deg,
                "observed_dec_deg": status.observed_dec_deg,
                "target_separation_deg": status.target_separation_deg,
                "rejection_reason": status.rejection_reason,
            }
        )
    _write_csv(cohort_dir / "manifest_status.csv", manifest_rows)
    (cohort_dir / "manifest_status.json").write_text(
        json.dumps(
            {
                "manifest_validation": manifest_summary,
                "thesis": THESIS_URL,
                "paper": PAPER_URL,
                "units": {"coordinates": "deg ICRS", **COHORT_UNITS},
                "observations": manifest_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import forms
    from forms.bricks.mag import load_igrf_model

    forms_root = Path(forms.__file__).resolve().parents[3]
    forms_revision = _git_revision(forms_root)
    settings = _settings(
        cadence_s=cadence_s,
        q_per_m=q_per_m,
        initial_intervals=initial_intervals,
        max_intervals=max_intervals,
        relative_tolerance=relative_tolerance,
        max_samples=max_samples,
    )
    model = None
    observation_rows: list[dict] = []
    sample_rows: list[dict] = []
    failures: list[dict] = []
    aggregate_flag_counts: Counter[str] = Counter()

    for observation in selected_observations:
        product = status_by_obsid[observation.obsid]
        obs_output = output_root / f"yamamoto_{observation.obsid}"
        if product.status != "ready":
            failures.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "status": product.status,
                    "reason": product.rejection_reason,
                }
            )
            observation_rows.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "primary": observation.primary,
                    "product_status": product.status,
                    "analysis_status": "not_run",
                    "cache_reused": False,
                    "xis": product.xis,
                    "sample_count": 0,
                    "gti_exposure_s": 0.0,
                    "thesis_exposure_ks": THESIS_EXPOSURE_KS.get(
                        observation.obsid
                    ),
                    "exposure_difference_ks": None,
                    "exposure_match": False,
                    "valid_integral_fraction": 0.0,
                    "converged_fraction": 0.0,
                    "b2_p05_t2m2": None,
                    "b2_median_t2m2": None,
                    "b2_p95_t2m2": None,
                    "acceptance_pass": False,
                    "reason": product.rejection_reason,
                }
            )
            continue

        cache_reused = not force and _cache_is_current(
            obs_output, product, settings, forms_revision
        )
        try:
            if cache_reused:
                summary = json.loads(
                    (obs_output / "summary.json").read_text(encoding="utf-8")
                )
            else:
                if model is None:
                    model = load_igrf_model()
                summary = validate_observation(
                    observation.obsid,
                    data_root=data_root,
                    output_root=output_root,
                    xis=product.xis,
                    cadence_s=cadence_s,
                    q_per_m=q_per_m,
                    initial_intervals=initial_intervals,
                    max_intervals=max_intervals,
                    relative_tolerance=relative_tolerance,
                    max_samples=max_samples,
                    loaded_igrf_model=model,
                )
                provenance_path = obs_output / "provenance.json"
                provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
                provenance["max_samples"] = max_samples
                provenance_path.write_text(
                    json.dumps(provenance, indent=2), encoding="utf-8"
                )
            acceptance = bool(
                summary["valid_integral_fraction"] == 1.0
                and summary["converged_fraction"] >= 0.99
                and summary["bgcrs_crosscheck"]["pass"]
            )
            thesis_exposure = THESIS_EXPOSURE_KS.get(observation.obsid)
            exposure_difference = (
                summary["gti_exposure_s"] / 1000.0 - thesis_exposure
                if thesis_exposure is not None
                else None
            )
            exposure_match = bool(
                exposure_difference is None
                or abs(exposure_difference) <= EXPOSURE_MATCH_TOLERANCE_KS
            )
            acceptance = acceptance and exposure_match
            distribution = summary["b_perp_l_squared_t2m2"]
            aggregate_flag_counts.update(summary.get("quality_flag_counts", {}))
            observation_rows.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "primary": observation.primary,
                    "product_status": product.status,
                    "analysis_status": "complete",
                    "cache_reused": cache_reused,
                    "xis": product.xis,
                    "sample_count": summary["sample_count"],
                    "gti_exposure_s": summary["gti_exposure_s"],
                    "thesis_exposure_ks": thesis_exposure,
                    "exposure_difference_ks": exposure_difference,
                    "exposure_match": exposure_match,
                    "valid_integral_fraction": summary["valid_integral_fraction"],
                    "converged_fraction": summary["converged_fraction"],
                    "b2_p05_t2m2": distribution["p05"],
                    "b2_median_t2m2": distribution["median"],
                    "b2_p95_t2m2": distribution["p95"],
                    "acceptance_pass": acceptance,
                    "reason": "" if acceptance else "numerical acceptance failed",
                }
            )
            sample_rows.extend(
                _read_rows(obs_output / "frame_state.csv", observation)
            )
        except Exception as exc:
            failures.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "status": "analysis_failed",
                    "reason": str(exc),
                }
            )
            observation_rows.append(
                {
                    "obsid": observation.obsid,
                    "field": observation.field,
                    "primary": observation.primary,
                    "product_status": product.status,
                    "analysis_status": "failed",
                    "cache_reused": False,
                    "xis": product.xis,
                    "sample_count": 0,
                    "gti_exposure_s": 0.0,
                    "thesis_exposure_ks": THESIS_EXPOSURE_KS.get(
                        observation.obsid
                    ),
                    "exposure_difference_ks": None,
                    "exposure_match": False,
                    "valid_integral_fraction": 0.0,
                    "converged_fraction": 0.0,
                    "b2_p05_t2m2": None,
                    "b2_median_t2m2": None,
                    "b2_p95_t2m2": None,
                    "acceptance_pass": False,
                    "reason": str(exc),
                }
            )

    field_rows, bin_rows = _aggregate_fields(sample_rows)
    _write_csv(cohort_dir / "cohort_summary.csv", observation_rows)
    _write_csv(cohort_dir / "field_summary.csv", field_rows)
    _write_csv(cohort_dir / "published_bin_comparison.csv", bin_rows)
    _plot_distributions(sample_rows, cohort_dir / "field_distributions.png")

    primary_rows = [row for row in observation_rows if row["primary"]]
    ready_primary = sum(row["product_status"] == "ready" for row in primary_rows)
    accepted_primary = sum(row["acceptance_pass"] for row in primary_rows)
    compared_bins = [row for row in bin_rows if row["sample_count"] > 0]
    bin_acceptance = bool(
        compared_bins
        and len(compared_bins) == len(bin_rows)
        and all(row["within_15_percent"] for row in compared_bins)
    )
    quality_counts = Counter()
    for row in observation_rows:
        if row["reason"]:
            quality_counts[row["reason"]] += 1
    complete = (
        observation_limit is None
        and ready_primary == 23
        and accepted_primary == 23
    )
    summary = {
        "cohort": "Yamamoto four-field geometry cohort",
        "manifest": manifest_summary,
        "settings": settings,
        "observation_limit": observation_limit,
        "units": COHORT_UNITS,
        "provenance": {
            "thesis": THESIS_URL,
            "paper": PAPER_URL,
            "forms_version": forms.__version__,
            "forms_git_revision": forms_revision,
            "analysis_version": __version__,
            "field_model": "IGRF-13",
            "lockman_count_discrepancy": manifest_summary[
                "paper_lockman_count_note"
            ],
        },
        "primary_ready_count": ready_primary,
        "primary_accepted_count": accepted_primary,
        "primary_required_count": 23,
        "failures": failures,
        "failure_reason_counts": dict(quality_counts),
        "quality_flag_counts": dict(sorted(aggregate_flag_counts.items())),
        "field_summary": field_rows,
        "published_bin_comparison": bin_rows,
        "acceptance": {
            "cohort_complete": complete,
            "all_published_bins_within_15_percent": bin_acceptance,
            "pass": complete and bin_acceptance,
            "criterion": (
                "all 23 primary observations ready and numerically accepted; "
                "GTI exposure within 0.1 ks of the thesis; every populated "
                "published bin mean within 15 percent"
            ),
        },
        "artifacts": {
            "manifest": "manifest_status.csv",
            "manifest_json": "manifest_status.json",
            "observations": "cohort_summary.csv",
            "fields": "field_summary.csv",
            "bins": "published_bin_comparison.csv",
            "figure": "field_distributions.png",
        },
    }
    (cohort_dir / "cohort_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary
