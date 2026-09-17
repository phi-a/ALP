from pathlib import Path

import numpy as np
from astropy.io import fits

from darknessalp.yamamoto.suzaku import (
    gti_bin_centers,
    load_suzaku_states,
    merge_gti_intervals,
    mission_time,
)

OBS_ID = "101002010"
DATA_ROOT = Path("data/suzaku")


def test_gti_bins_preserve_exposure():
    gti = np.array([[0.0, 125.0], [200.0, 260.0]])
    centers, exposure, indices = gti_bin_centers(gti, cadence_s=60)
    assert np.isclose(exposure.sum(), 185.0)
    assert np.all((centers >= gti[indices, 0]) & (centers <= gti[indices, 1]))


def test_merge_gti_intervals_unions_overlap_and_adjacency():
    merged = merge_gti_intervals(
        np.array([[0.0, 60.0], [120.0, 180.0]]),
        np.array([[30.0, 90.0], [90.0, 120.0], [240.0, 300.0]]),
    )
    assert np.array_equal(merged, np.array([[0.0, 180.0], [240.0, 300.0]]))
    assert np.isclose(np.diff(merged, axis=1).sum(), 240.0)


def test_mission_time_matches_archived_jd():
    path = DATA_ROOT / OBS_ID / f"ae{OBS_ID}.att"
    with fits.open(path) as hdul:
        row = hdul[1].data[0]
        epoch = mission_time(float(row["TIME"]), hdul[1].header)
    archived_clock = (
        f"{int(row['YYYYMMDD']):08d}{int(row['HHMMSS']):06d}"
    )
    assert epoch.utc.strftime("%Y%m%d%H%M%S") == archived_clock
    # The archived JD was generated with a pre-2006 leap-second file and is
    # exactly one second ahead. The standards-based TT conversion is canonical.
    assert np.isclose(
        (float(row["JD"]) - float(epoch.utc.jd)) * 86400.0,
        1.0,
        atol=1e-4,
    )


def test_archived_states_preserve_gti_exposure_and_pointing():
    states, metadata = load_suzaku_states(OBS_ID, data_root=DATA_ROOT)
    assert states
    assert abs(metadata["sample_exposure_s"] - metadata["gti_exposure_s"]) < 1e-6
    assert metadata["event_file_count"] == 3
    assert abs(metadata["gti_exposure_s"] / 1000.0 - 80.4) < 0.1
    valid = [state for state in states if state.data_valid]
    assert len(valid) / len(states) > 0.99
    assert abs(np.median([state.foc_ra_deg for state in valid]) - 162.9) < 1.0
    assert abs(np.median([state.foc_dec_deg for state in valid]) - 57.3) < 1.0
    for state in valid[:10]:
        assert np.isclose(np.linalg.norm(state.boresight_gcrf), 1.0)
        assert 6300.0 < np.linalg.norm(state.position_gcrf_km) < 7500.0


def test_multi_file_gti_recovers_108001010_thesis_exposure():
    _, metadata = load_suzaku_states("108001010", data_root=DATA_ROOT)
    assert metadata["event_file_count"] == 3
    assert metadata["raw_gti_count"] > metadata["gti_count"]
    assert abs(metadata["gti_exposure_s"] / 1000.0 - 38.8) < 0.1
