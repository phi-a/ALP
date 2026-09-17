import csv
import json
from pathlib import Path

import numpy as np

import darknessalp.yamamoto.cohort as cohort
from darknessalp.yamamoto.archive import PRIMARY_COHORT
from darknessalp.yamamoto.schema import ProductStatus


def test_weighted_aggregation_uses_exposure_and_published_bins():
    rows = [
        {
            "obsid": "a",
            "field": "Lockman Hole",
            "primary": True,
            "b_perp_l_tm": 105.0,
            "b_perp_l_squared_t2m2": 10000.0,
            "exposure_s": 1.0,
            "screen_pass": True,
        },
        {
            "obsid": "b",
            "field": "Lockman Hole",
            "primary": True,
            "b_perp_l_tm": 106.0,
            "b_perp_l_squared_t2m2": 12000.0,
            "exposure_s": 3.0,
            "screen_pass": True,
        },
    ]
    _, bins = cohort._aggregate_fields(rows)
    first = bins[0]
    assert first["sample_count"] == 2
    assert np.isclose(first["calculated_mean_t2m2"], 11500.0)
    assert np.isclose(first["normalized_exposure_fraction"], 1.0)


def _write_cached_observation(output_root: Path, obsid: str):
    obsdir = output_root / f"yamamoto_{obsid}"
    obsdir.mkdir(parents=True)
    summary = {
        "sample_count": 1,
        "gti_exposure_s": 80400.0,
        "valid_integral_fraction": 1.0,
        "converged_fraction": 1.0,
        "bgcrs_crosscheck": {"pass": True},
        "b_perp_l_squared_t2m2": {
            "minimum": 11025.0,
            "p05": 11025.0,
            "median": 11025.0,
            "p95": 11025.0,
            "maximum": 11025.0,
        },
        "quality_flag_counts": {},
    }
    (obsdir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
    with (obsdir / "frame_state.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "b_perp_l_tm",
                "b_perp_l_squared_t2m2",
                "exposure_s",
                "yamamoto_screen_pass",
                "integration_converged",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "b_perp_l_tm": 105.0,
                "b_perp_l_squared_t2m2": 11025.0,
                "exposure_s": 60.0,
                "yamamoto_screen_pass": True,
                "integration_converged": True,
            }
        )
    (obsdir / "provenance.json").write_text("{}", encoding="utf-8")
    return summary


def test_cohort_continues_after_missing_observation(monkeypatch, tmp_path):
    first, second = PRIMARY_COHORT[:2]
    observations = (first, second) + PRIMARY_COHORT[2:]
    ready_path = tmp_path / "source.fits"
    ready_path.write_bytes(b"source")

    def status(item, **_):
        if item.obsid == second.obsid:
            return ProductStatus(
                item.obsid,
                item.field,
                item.primary,
                "missing",
                None,
                None,
                (),
                None,
                None,
                None,
                "EHK",
            )
        return ProductStatus(
            item.obsid,
            item.field,
            item.primary,
            "ready",
            0,
            str(ready_path),
            (str(ready_path),),
            item.expected_ra_deg,
            item.expected_dec_deg,
            0.0,
            "",
        )

    monkeypatch.setattr(cohort, "inspect_products", status)
    monkeypatch.setattr(cohort, "_cache_is_current", lambda *args, **kwargs: True)
    cached = _write_cached_observation(tmp_path, first.obsid)
    result = cohort.validate_cohort(
        observations,
        output_root=tmp_path,
        observation_limit=2,
    )
    assert result["primary_accepted_count"] == 1
    assert result["primary_ready_count"] == 1
    assert result["failures"][0]["obsid"] == second.obsid
    assert not result["acceptance"]["cohort_complete"]


def test_cache_rejects_changed_settings_or_sources(tmp_path):
    obs = PRIMARY_COHORT[0]
    source = tmp_path / "source"
    source.write_bytes(b"one")
    product = ProductStatus(
        obs.obsid,
        obs.field,
        True,
        "ready",
        0,
        str(source),
        (str(source),),
        obs.expected_ra_deg,
        obs.expected_dec_deg,
        0.0,
        "",
    )
    out = tmp_path / "out"
    out.mkdir()
    (out / "summary.json").write_text("{}", encoding="utf-8")
    (out / "frame_state.csv").write_text("a\n", encoding="utf-8")
    settings = cohort._settings(
        cadence_s=60,
        q_per_m=0,
        initial_intervals=32,
        max_intervals=256,
        relative_tolerance=0.01,
        max_samples=None,
    )
    provenance = {
        **settings,
        "forms_git_revision": "abc",
        "sources": {
            "cadence_s": 60,
            "ehk_sha256": cohort._sha256(source),
            "event_sha256": {str(source): cohort._sha256(source)},
        },
    }
    (out / "provenance.json").write_text(json.dumps(provenance), encoding="utf-8")
    assert cohort._cache_is_current(out, product, settings, "abc")
    source.write_bytes(b"two")
    assert not cohort._cache_is_current(out, product, settings, "abc")
