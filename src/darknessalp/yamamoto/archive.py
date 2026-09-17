"""Minimal Suzaku archive products for the Yamamoto geometry cohort."""

from __future__ import annotations

import gzip
import re
import shutil
from pathlib import Path
from urllib.request import urlopen, urlretrieve

import numpy as np
from astropy.io import fits

from darknessalp.yamamoto.schema import ProductStatus, SuzakuObservation

BASE_URL = "https://heasarc.gsfc.nasa.gov/FTP/suzaku/data/obs"
XIS_PRECEDENCE = (0, 1, 3)
TARGET_TOLERANCE_DEG = 1.0

THESIS_URL = (
    "https://www.isas.jaxa.jp/home/yamasaki/theses/"
    "Dthesis_2018_RYamamoto.pdf"
)
PAPER_URL = "https://arxiv.org/abs/1906.04429"


def _obs(obsid: str, field: str, ra: float, dec: float) -> SuzakuObservation:
    return SuzakuObservation(obsid, field, ra, dec)


PRIMARY_COHORT = (
    _obs("101002010", "Lockman Hole", 162.937, 57.256),
    _obs("102018010", "Lockman Hole", 162.926, 57.258),
    _obs("103009010", "Lockman Hole", 162.937, 57.255),
    _obs("104002010", "Lockman Hole", 162.938, 57.255),
    _obs("105003010", "Lockman Hole", 162.938, 57.251),
    _obs("106001010", "Lockman Hole", 162.927, 57.253),
    _obs("107001010", "Lockman Hole", 162.920, 57.255),
    _obs("108001010", "Lockman Hole", 162.944, 57.275),
    _obs("109014010", "Lockman Hole", 162.940, 57.278),
    _obs("507076010", "MBM16", 49.752, 11.602),
    _obs("507076020", "MBM16", 49.769, 11.580),
    _obs("508078010", "MBM16", 49.765, 11.582),
    _obs("508078020", "MBM16", 49.771, 11.580),
    _obs("509073010", "MBM16", 49.764, 11.584),
    _obs("509073020", "MBM16", 49.770, 11.580),
    _obs("504069010", "SEP", 89.966, -66.577),
    _obs("504071010", "SEP", 89.966, -66.571),
    _obs("504073010", "SEP", 89.958, -66.568),
    _obs("504075010", "SEP", 89.980, -66.568),
    _obs("504070010", "NEP", 270.049, 66.560),
    _obs("504072010", "NEP", 270.052, 66.566),
    _obs("504074010", "NEP", 270.048, 66.570),
    _obs("504076010", "NEP", 270.045, 66.579),
)

SUPPLEMENTAL_COHORT = (
    SuzakuObservation(
        "104002020",
        "Lockman Hole",
        162.94,
        57.26,
        primary=False,
        provenance="DARTS Suzaku public archive",
        inclusion_note=(
            "Supplemental diagnostic only. The paper reports 11 Lockman "
            "observations, but 11 unique primary IDs have not been identified."
        ),
    ),
)

DEFAULT_COHORT = PRIMARY_COHORT + SUPPLEMENTAL_COHORT

THESIS_EXPOSURE_KS = {
    "101002010": 80.4,
    "102018010": 96.1,
    "103009010": 83.4,
    "104002010": 92.8,
    "105003010": 78.0,
    "106001010": 42.3,
    "107001010": 35.9,
    "108001010": 38.8,
    "109014010": 37.1,
    "507076010": 24.9,
    "507076020": 81.0,
    "508078010": 82.3,
    "508078020": 87.9,
    "509073010": 78.8,
    "509073020": 92.0,
    "504069010": 51.9,
    "504071010": 58.0,
    "504073010": 44.4,
    "504075010": 50.0,
    "504070010": 56.3,
    "504072010": 48.7,
    "504074010": 50.2,
    "504076010": 49.8,
}

PUBLISHED_BINS = {
    "Lockman Hole": {
        "edges_tm": (100, 113, 127, 149, 184, 226, 314),
        "means_t2m2": (11470, 14256, 18879, 27423, 42230, 64060),
    },
    "MBM16": {
        "edges_tm": (60, 79, 92, 109, 137, 191, 300),
        "means_t2m2": (5128, 7309, 9934, 14884, 25985, 53639),
    },
    "SEP": {
        "edges_tm": (90, 116, 140, 165, 255),
        "means_t2m2": (10837, 16384, 23104, 37404),
    },
    "NEP": {
        "edges_tm": (120, 134, 161, 205, 286),
        "means_t2m2": (15977, 21550, 33379, 51393),
    },
}


def validate_manifest(
    observations: tuple[SuzakuObservation, ...] = DEFAULT_COHORT,
) -> dict:
    """Validate identity, counts, coordinates, and primary membership."""

    obsids = [item.obsid for item in observations]
    if len(obsids) != len(set(obsids)):
        raise ValueError("Suzaku manifest contains duplicate ObsIDs")
    if any(not re.fullmatch(r"\d{9}", item.obsid) for item in observations):
        raise ValueError("every Suzaku ObsID must contain nine digits")
    if any(not (0 <= item.expected_ra_deg < 360) for item in observations):
        raise ValueError("manifest RA must be in [0, 360) degrees")
    if any(not (-90 <= item.expected_dec_deg <= 90) for item in observations):
        raise ValueError("manifest Dec must be in [-90, 90] degrees")

    counts = {
        field: sum(item.primary and item.field == field for item in observations)
        for field in PUBLISHED_BINS
    }
    expected = {"Lockman Hole": 9, "MBM16": 6, "SEP": 4, "NEP": 4}
    if counts != expected:
        raise ValueError(f"primary field counts {counts!r} do not match {expected!r}")
    primary_ids = {item.obsid for item in observations if item.primary}
    if primary_ids != set(THESIS_EXPOSURE_KS):
        raise ValueError("primary manifest does not match the thesis exposure table")
    return {
        "valid": True,
        "primary_count": sum(item.primary for item in observations),
        "supplemental_count": sum(not item.primary for item in observations),
        "field_counts": counts,
        "paper_lockman_count_note": (
            "Yamamoto et al. report 11 Lockman observations; this provenance-locked "
            "primary cohort contains the nine annual thesis observations. "
            "104002020 is supplemental, and no duplicated ID is used."
        ),
    }


def _event_candidates(obsdir: Path, obsid: str, xis: int) -> list[Path]:
    return sorted(
        path
        for path in (obsdir / f"xis{xis}").glob(f"ae{obsid}xi{xis}*_cl.evt")
        if path.is_file() and ("_3x3" in path.name or "_5x5" in path.name)
    )


def select_event_products(
    obsid: str,
    data_root: str | Path = "data/suzaku",
    precedence: tuple[int, ...] = XIS_PRECEDENCE,
) -> tuple[int, list[Path]] | None:
    """Select all standard cleaned products for one detector by precedence."""

    obsdir = Path(data_root) / obsid
    for xis in precedence:
        candidates = _event_candidates(obsdir, obsid, xis)
        if candidates:
            return xis, candidates
    return None


def select_event_product(
    obsid: str,
    data_root: str | Path = "data/suzaku",
    precedence: tuple[int, ...] = XIS_PRECEDENCE,
) -> tuple[int, Path] | None:
    """Compatibility wrapper returning the first selected standard product."""

    selected = select_event_products(obsid, data_root, precedence)
    return (selected[0], selected[1][0]) if selected else None


def _angular_separation_deg(ra1, dec1, ra2, dec2) -> float:
    ra1, dec1, ra2, dec2 = np.deg2rad([ra1, dec1, ra2, dec2])
    cosine = np.sin(dec1) * np.sin(dec2) + np.cos(dec1) * np.cos(dec2) * np.cos(
        ra1 - ra2
    )
    return float(np.rad2deg(np.arccos(np.clip(cosine, -1.0, 1.0))))


def inspect_products(
    observation: SuzakuObservation,
    *,
    data_root: str | Path = "data/suzaku",
    target_tolerance_deg: float = TARGET_TOLERANCE_DEG,
) -> ProductStatus:
    """Inspect the minimal local products and validate their FITS identity."""

    obsdir = Path(data_root) / observation.obsid
    ehk_path = obsdir / f"ae{observation.obsid}.ehk"
    selected = select_event_products(observation.obsid, data_root)
    missing = []
    if not ehk_path.is_file():
        missing.append("EHK")
    if selected is None:
        missing.append("cleaned XIS event/GTI")
    if missing:
        return ProductStatus(
            observation.obsid,
            observation.field,
            observation.primary,
            "missing",
            selected[0] if selected else None,
            str(ehk_path.resolve()) if ehk_path.is_file() else None,
            tuple(str(path.resolve()) for path in selected[1]) if selected else (),
            None,
            None,
            None,
            ", ".join(missing),
        )

    xis, event_paths = selected
    try:
        with fits.open(ehk_path, memmap=True) as hdul:
            header = hdul[1].header
            obsid = str(header.get("OBS_ID", "")).strip()
            ra = float(header.get("RA_NOM", header.get("RA_OBJ")))
            dec = float(header.get("DEC_NOM", header.get("DEC_OBJ")))
            required = {
                "TIME",
                "SAT_LAT",
                "SAT_LON",
                "SAT_ALT",
                "FOC_RA",
                "FOC_DEC",
            }
            missing_columns = required.difference(hdul[1].columns.names)
        for event_path in event_paths:
            with fits.open(event_path, memmap=True) as hdul:
                event_obsid = str(hdul["EVENTS"].header.get("OBS_ID", "")).strip()
                if event_obsid != observation.obsid:
                    raise ValueError(
                        f"FITS ObsID mismatch in {event_path.name}: {event_obsid!r}"
                    )
                if "GTI" not in hdul or not {"START", "STOP"}.issubset(
                    hdul["GTI"].columns.names
                ):
                    raise ValueError(
                        f"event product has no usable GTI extension: {event_path.name}"
                    )
        if missing_columns:
            raise ValueError(f"EHK missing columns: {sorted(missing_columns)}")
        if obsid != observation.obsid:
            raise ValueError(f"FITS ObsID mismatch in EHK: {obsid!r}")
    except Exception as exc:
        return ProductStatus(
            observation.obsid,
            observation.field,
            observation.primary,
            "invalid",
            xis,
            str(ehk_path.resolve()),
            tuple(str(path.resolve()) for path in event_paths),
            None,
            None,
            None,
            str(exc),
        )

    separation = _angular_separation_deg(
        observation.expected_ra_deg, observation.expected_dec_deg, ra, dec
    )
    status = "ready" if separation <= target_tolerance_deg else "mismatch"
    reason = (
        ""
        if status == "ready"
        else f"target separation {separation:.3f} deg exceeds {target_tolerance_deg:.3f} deg"
    )
    return ProductStatus(
        observation.obsid,
        observation.field,
        observation.primary,
        status,
        xis,
        str(ehk_path.resolve()),
        tuple(str(path.resolve()) for path in event_paths),
        ra,
        dec,
        separation,
        reason,
    )


def inspect_cohort(
    observations: tuple[SuzakuObservation, ...] = DEFAULT_COHORT,
    *,
    data_root: str | Path = "data/suzaku",
) -> list[ProductStatus]:
    validate_manifest(observations)
    return [inspect_products(item, data_root=data_root) for item in observations]


def _uncompress(source: Path, target: Path) -> Path:
    if not target.exists():
        with gzip.open(source, "rb") as in_stream, target.open("wb") as out_stream:
            shutil.copyfileobj(in_stream, out_stream)
    return target


def _download_ehk(obsid: str, data_root: Path) -> Path:
    obsdir = data_root / obsid
    obsdir.mkdir(parents=True, exist_ok=True)
    target = obsdir / f"ae{obsid}.ehk"
    if target.exists():
        return target
    compressed = target.with_suffix(".ehk.gz")
    url = f"{BASE_URL}/{obsid[0]}/{obsid}/auxil/{compressed.name}"
    if not compressed.exists():
        urlretrieve(url, compressed)
    return _uncompress(compressed, target)


def _remote_event_names(obsid: str, xis: int) -> list[str]:
    url = f"{BASE_URL}/{obsid[0]}/{obsid}/xis/event_cl/"
    with urlopen(url) as response:
        html = response.read().decode("utf-8", errors="ignore")
    pattern = re.compile(rf'ae{obsid}xi{xis}[^"\'\s]*?_cl\.evt(?:\.gz)?')
    return sorted(set(pattern.findall(html)))


def _standard_event_names(names: list[str]) -> list[str]:
    """Return one remote name for each standard 3x3/5x5 cleaned product."""

    standard = [name for name in names if "_3x3" in name or "_5x5" in name]
    by_target: dict[str, str] = {}
    for name in standard:
        target = name[:-3] if name.endswith(".gz") else name
        current = by_target.get(target)
        if current is None or (current.endswith(".gz") and not name.endswith(".gz")):
            by_target[target] = name
    return [by_target[target] for target in sorted(by_target)]


def _download_events(obsid: str, xis: int, data_root: Path) -> list[Path]:
    names = _standard_event_names(_remote_event_names(obsid, xis))
    if not names:
        raise FileNotFoundError(f"no cleaned XIS{xis} event product for {obsid}")
    outdir = data_root / obsid / f"xis{xis}"
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in names:
        remote = f"{BASE_URL}/{obsid[0]}/{obsid}/xis/event_cl/{name}"
        local = outdir / name
        if not local.exists():
            urlretrieve(remote, local)
        path = _uncompress(local, outdir / local.stem) if local.suffix == ".gz" else local
        paths.append(path)
    return paths


def prepare_observation(
    observation: SuzakuObservation,
    *,
    data_root: str | Path = "data/suzaku",
) -> ProductStatus:
    """Acquire EHK plus all standard cleaned GTI products for one detector."""

    root = Path(data_root)
    try:
        _download_ehk(observation.obsid, root)
        for xis in XIS_PRECEDENCE:
            try:
                _download_events(observation.obsid, xis, root)
                break
            except FileNotFoundError:
                continue
    except Exception as exc:
        return ProductStatus(
            observation.obsid,
            observation.field,
            observation.primary,
            "invalid",
            None,
            None,
            (),
            None,
            None,
            None,
            f"acquisition failed: {exc}",
        )
    return inspect_products(observation, data_root=root)


def prepare_cohort(
    observations: tuple[SuzakuObservation, ...] = DEFAULT_COHORT,
    *,
    data_root: str | Path = "data/suzaku",
) -> list[ProductStatus]:
    """Acquire and inspect a cohort without orbit, attitude, or spectral products."""

    validate_manifest(observations)
    return [prepare_observation(item, data_root=data_root) for item in observations]
