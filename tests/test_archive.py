from pathlib import Path

import numpy as np
from astropy.io import fits

from darknessalp.yamamoto.archive import (
    DEFAULT_COHORT,
    PRIMARY_COHORT,
    inspect_products,
    select_event_product,
    select_event_products,
    validate_manifest,
)


def _write_minimal_products(
    root: Path,
    obsid: str,
    xis: int,
    ra=162.937,
    dec=57.256,
    mode="3x3",
):
    obsdir = root / obsid
    obsdir.mkdir(parents=True, exist_ok=True)
    columns = [
        fits.Column(name=name, format="D", array=np.array([0.0]))
        for name in ("TIME", "SAT_LAT", "SAT_LON", "SAT_ALT", "FOC_RA", "FOC_DEC")
    ]
    ehk = fits.BinTableHDU.from_columns(columns)
    ehk.header["OBS_ID"] = obsid
    ehk.header["RA_NOM"] = ra
    ehk.header["DEC_NOM"] = dec
    fits.HDUList([fits.PrimaryHDU(), ehk]).writeto(
        obsdir / f"ae{obsid}.ehk", overwrite=True
    )

    event_dir = obsdir / f"xis{xis}"
    event_dir.mkdir(exist_ok=True)
    events = fits.BinTableHDU.from_columns(
        [fits.Column(name="TIME", format="D", array=np.array([0.0]))],
        name="EVENTS",
    )
    events.header["OBS_ID"] = obsid
    gti = fits.BinTableHDU.from_columns(
        [
            fits.Column(name="START", format="D", array=np.array([0.0])),
            fits.Column(name="STOP", format="D", array=np.array([60.0])),
        ],
        name="GTI",
    )
    path = event_dir / f"ae{obsid}xi{xis}_0_{mode}_cl.evt"
    fits.HDUList([fits.PrimaryHDU(), events, gti]).writeto(path, overwrite=True)
    return path


def test_manifest_is_unique_and_has_locked_primary_counts():
    summary = validate_manifest()
    assert summary["primary_count"] == 23
    assert summary["supplemental_count"] == 1
    assert summary["field_counts"] == {
        "Lockman Hole": 9,
        "MBM16": 6,
        "SEP": 4,
        "NEP": 4,
    }
    assert len({item.obsid for item in DEFAULT_COHORT}) == len(DEFAULT_COHORT)
    assert "104002020" not in {item.obsid for item in PRIMARY_COHORT}


def test_event_selection_uses_xis_precedence(tmp_path):
    obs = PRIMARY_COHORT[0]
    _write_minimal_products(tmp_path, obs.obsid, 1)
    _write_minimal_products(tmp_path, obs.obsid, 0)
    xis, path = select_event_product(obs.obsid, tmp_path)
    assert xis == 0
    assert "xis0" in str(path)


def test_event_selection_keeps_all_standard_modes_and_excludes_timing(tmp_path):
    obs = PRIMARY_COHORT[0]
    _write_minimal_products(tmp_path, obs.obsid, 0, mode="3x3n066l")
    _write_minimal_products(tmp_path, obs.obsid, 0, mode="5x5n066l")
    _write_minimal_products(tmp_path, obs.obsid, 0, mode="timp002l")
    xis, paths = select_event_products(obs.obsid, tmp_path)
    assert xis == 0
    assert len(paths) == 2
    assert {("3x3" in path.name, "5x5" in path.name) for path in paths} == {
        (True, False),
        (False, True),
    }


def test_product_inspection_checks_target_coordinates(tmp_path):
    obs = PRIMARY_COHORT[0]
    _write_minimal_products(tmp_path, obs.obsid, 1)
    ready = inspect_products(obs, data_root=tmp_path)
    assert ready.status == "ready"
    assert ready.xis == 1
    assert ready.target_separation_deg < 0.01

    mismatch_obs = type(obs)(
        obs.obsid,
        obs.field,
        10.0,
        -10.0,
        obs.primary,
        obs.provenance,
        obs.inclusion_note,
    )
    mismatch = inspect_products(mismatch_obs, data_root=tmp_path)
    assert mismatch.status == "mismatch"
