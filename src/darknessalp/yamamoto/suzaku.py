"""Suzaku archived-state ingestion for the Yamamoto validation case."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.time import Time

from darknessalp.yamamoto.schema import MissionState


def _mjdref(header) -> float:
    return float(header.get("MJDREFI", 0.0)) + float(header.get("MJDREFF", 0.0))


def mission_time(time_s: float, header) -> Time:
    """Convert Suzaku mission seconds to an Astropy epoch using FITS metadata."""

    scale = str(header.get("TIMESYS", "TT")).strip().lower()
    if scale not in {"tt", "utc", "tai"}:
        raise ValueError(f"unsupported Suzaku TIMESYS {scale!r}")
    return Time(_mjdref(header) + float(time_s) / 86400.0, format="mjd", scale=scale)


def _continuous_at(times, values, sample_times, *, angular=False):
    values = np.asarray(values, dtype=float)
    if angular:
        unwrapped = np.unwrap(np.deg2rad(values))
        return np.rad2deg(np.interp(sample_times, times, unwrapped)) % 360.0
    return np.interp(sample_times, times, values)


def _nearest_indices(times: np.ndarray, sample_times: np.ndarray) -> np.ndarray:
    right = np.searchsorted(times, sample_times, side="left")
    right = np.clip(right, 0, len(times) - 1)
    left = np.maximum(right - 1, 0)
    choose_left = np.abs(sample_times - times[left]) <= np.abs(times[right] - sample_times)
    return np.where(choose_left, left, right)


def gti_bin_centers(gti: np.ndarray, cadence_s: float = 60.0):
    """Return exposure-centered samples that exactly partition each cleaned GTI."""

    centers: list[float] = []
    exposures: list[float] = []
    indices: list[int] = []
    for gti_index, (start, stop) in enumerate(gti):
        edge = float(start)
        stop = float(stop)
        while edge < stop:
            duration = min(float(cadence_s), stop - edge)
            centers.append(edge + duration / 2.0)
            exposures.append(duration)
            indices.append(gti_index)
            edge += duration
    return (
        np.asarray(centers),
        np.asarray(exposures),
        np.asarray(indices, dtype=int),
    )


def merge_gti_intervals(*gti_arrays: np.ndarray) -> np.ndarray:
    """Return the sorted union of valid GTIs without double-counting overlap."""

    arrays = [np.asarray(gti, dtype=float).reshape(-1, 2) for gti in gti_arrays]
    if not arrays or not any(len(gti) for gti in arrays):
        return np.empty((0, 2), dtype=float)
    intervals = np.concatenate([gti for gti in arrays if len(gti)])
    if not np.all(np.isfinite(intervals)):
        raise ValueError("GTIs must contain finite START and STOP values")
    if np.any(intervals[:, 1] <= intervals[:, 0]):
        raise ValueError("every GTI must have STOP greater than START")
    intervals = intervals[np.argsort(intervals[:, 0], kind="stable")]
    merged = [intervals[0].tolist()]
    for start, stop in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], float(stop))
        else:
            merged.append([float(start), float(stop)])
    return np.asarray(merged, dtype=float)


def load_suzaku_states(
    obsid: str,
    *,
    data_root: str | Path = "data/suzaku",
    xis: int | None = 0,
    cadence_s: float = 60.0,
) -> tuple[list[MissionState], dict]:
    """Build 60-second mission states from a cleaned XIS GTI and EHK file."""

    try:
        import forms
    except ImportError as exc:
        raise RuntimeError(
            "FORMS is required; install the local SDK from ../../forms/python/sdk"
        ) from exc

    obsdir = Path(data_root) / obsid
    if xis is None:
        from darknessalp.yamamoto.archive import select_event_products

        selected = select_event_products(obsid, data_root)
        if selected is None:
            raise FileNotFoundError(f"no cleaned XIS event file under {obsdir}")
        xis = selected[0]
    ehk_path = obsdir / f"ae{obsid}.ehk"
    event_candidates = sorted(
        path
        for path in (obsdir / f"xis{xis}").glob(f"ae{obsid}xi{xis}*_cl.evt")
        if "_3x3" in path.name or "_5x5" in path.name
    )
    if not ehk_path.exists():
        raise FileNotFoundError(ehk_path)
    if not event_candidates:
        raise FileNotFoundError(f"no cleaned XIS{xis} event file under {obsdir}")

    with fits.open(ehk_path, memmap=True) as hdul:
        ehk = hdul[1].data
        ehk_header = hdul[1].header.copy()
        columns = {name: np.asarray(ehk[name]) for name in ehk.columns.names}
    raw_gtis = []
    event_headers = []
    for event_path in event_candidates:
        with fits.open(event_path, memmap=True) as hdul:
            raw_gtis.append(
                np.column_stack(
                    (hdul["GTI"].data["START"], hdul["GTI"].data["STOP"])
                )
            )
            event_headers.append(hdul["EVENTS"].header.copy())
    event_header = event_headers[0]
    for path, header in zip(event_candidates[1:], event_headers[1:]):
        if str(header.get("TIMESYS", "")).strip() != str(
            event_header.get("TIMESYS", "")
        ).strip() or not np.isclose(_mjdref(header), _mjdref(event_header), atol=0):
            raise ValueError(f"inconsistent time reference in {path}")
    gti = merge_gti_intervals(*raw_gtis)
    if not len(gti):
        raise ValueError(f"no valid GTIs across cleaned XIS{xis} products")

    centers, exposure, gti_indices = gti_bin_centers(gti, cadence_s)
    times = np.asarray(columns["TIME"], dtype=float)
    nearest = _nearest_indices(times, centers)

    continuous = {
        "latitude": _continuous_at(times, columns["SAT_LAT"], centers),
        "longitude": _continuous_at(
            times, columns["SAT_LON"], centers, angular=True
        ),
        "altitude": _continuous_at(times, columns["SAT_ALT"], centers),
        "ra": _continuous_at(times, columns["FOC_RA"], centers, angular=True),
        "dec": _continuous_at(times, columns["FOC_DEC"], centers),
        "roll": _continuous_at(times, columns["FOC_ROLL"], centers, angular=True),
        "elv": _continuous_at(times, columns["ELV"], centers),
        "dye_elv": _continuous_at(times, columns["DYE_ELV"], centers),
        "nte_elv": _continuous_at(times, columns["NTE_ELV"], centers),
        "cor2": _continuous_at(times, columns["COR2"], centers),
        "ang_dist": _continuous_at(times, columns["ANG_DIST"], centers),
    }

    states: list[MissionState] = []
    for index, center in enumerate(centers):
        epoch = mission_time(center, ehk_header)
        mjd_tt = float(epoch.tt.mjd)
        mjd2000_tt = float(epoch.tt.jd - 2451545.0)
        instant = forms.Instant.from_mjd2000(mjd2000_tt)

        lat = float(continuous["latitude"][index])
        lon = float(continuous["longitude"][index])
        if lon > 180.0:
            lon -= 360.0
        alt = float(continuous["altitude"][index])
        geo = forms.Geodetic(np.deg2rad(lat), np.deg2rad(lon), alt)
        r_itrf = geo.to_coord()
        r_gcrf = r_itrf.to(forms.Frame.GCRF, at=instant)

        ra = float(continuous["ra"][index])
        dec = float(continuous["dec"][index])
        boresight = forms.RaDec(np.deg2rad(ra), np.deg2rad(dec)).to_coord()
        boresight_values = np.asarray(boresight.to_list(), dtype=float)
        boresight_values /= np.linalg.norm(boresight_values)

        nearest_index = int(nearest[index])
        offset = abs(float(times[nearest_index] - center))
        saa = int(columns["SAA"][nearest_index])
        values = [
            lat,
            lon,
            alt,
            ra,
            dec,
            float(continuous["elv"][index]),
            float(continuous["cor2"][index]),
        ]
        flags: list[str] = []
        if not np.all(np.isfinite(values)):
            flags.append("nonfinite_input")
        if offset > 2.0:
            flags.append("ehk_time_gap")
        if saa != 0:
            flags.append("saa")
        if float(continuous["elv"][index]) <= 0.0:
            flags.append("earth_occulted_ehk")
        if float(continuous["cor2"][index]) < 8.0:
            flags.append("cor2_below_8_gv")

        states.append(
            MissionState(
                mission="Suzaku",
                obsid=obsid,
                sample_id=index,
                gti_index=int(gti_indices[index]),
                mission_time_tt_s=float(center),
                utc=epoch.utc.isot,
                mjd_tt=mjd_tt,
                mjd2000_tt=mjd2000_tt,
                exposure_s=float(exposure[index]),
                latitude_deg=lat,
                longitude_deg=lon,
                altitude_km=alt,
                r_itrf_x_km=float(r_itrf.x),
                r_itrf_y_km=float(r_itrf.y),
                r_itrf_z_km=float(r_itrf.z),
                r_gcrf_x_km=float(r_gcrf.x),
                r_gcrf_y_km=float(r_gcrf.y),
                r_gcrf_z_km=float(r_gcrf.z),
                boresight_gcrf_x=float(boresight_values[0]),
                boresight_gcrf_y=float(boresight_values[1]),
                boresight_gcrf_z=float(boresight_values[2]),
                foc_ra_deg=ra,
                foc_dec_deg=dec,
                foc_roll_deg=float(continuous["roll"][index]),
                earth_limb_elevation_deg=float(continuous["elv"][index]),
                day_earth_limb_elevation_deg=float(continuous["dye_elv"][index]),
                night_earth_limb_elevation_deg=float(continuous["nte_elv"][index]),
                cor2_gv=float(continuous["cor2"][index]),
                saa=saa,
                pointing_separation_deg=float(continuous["ang_dist"][index]),
                ehk_nearest_offset_s=offset,
                in_cleaned_gti=True,
                data_valid=not any(
                    flag in flags for flag in ("nonfinite_input", "ehk_time_gap")
                ),
                quality_flags="|".join(flags),
            )
        )

    metadata = {
        "obsid": obsid,
        "xis": xis,
        "cadence_s": cadence_s,
        "ehk_path": str(ehk_path.resolve()),
        "event_paths": [str(path.resolve()) for path in event_candidates],
        "ehk_timesys": str(ehk_header.get("TIMESYS", "")),
        "ehk_mjdref": _mjdref(ehk_header),
        "ehk_leapfile": str(ehk_header.get("LEAPFILE", "")),
        "event_timesys": str(event_header.get("TIMESYS", "")),
        "event_mjdref": _mjdref(event_header),
        "event_leapfile": str(event_header.get("LEAPFILE", "")),
        "event_file_count": len(event_candidates),
        "raw_gti_count": int(sum(len(raw) for raw in raw_gtis)),
        "gti_count": int(len(gti)),
        "gti_exposure_s": float(np.sum(gti[:, 1] - gti[:, 0])),
        "sample_exposure_s": float(np.sum(exposure)),
    }
    return states, metadata
