"""
suzaku_archive.py
-----------------
Helper functions to fetch Suzaku orbit and attitude files
from the HEASARC public archive.

Based on Yamamoto et al. (2020), we focus on the four "deep fields":
- Lockman Hole
- MBM16
- North Ecliptic Pole (NEP)
- South Ecliptic Pole (SEP)

Files are cached under data/suzaku/<ObsID>/

Author: Phoenix Alpine (2025)
"""

import gzip
import shutil
import numpy as np
import urllib.request
from pathlib import Path
from astropy.io import fits

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------

HERE = Path(__file__).parent.resolve()     # points to .../data
CACHE_DIR = HERE.parents[2] / "data" / "suzaku"

BASE_URL = "https://heasarc.gsfc.nasa.gov/FTP/suzaku/data/obs"

# ----------------------------------------------------------------------
# ObsID lists (Yamamoto 2018 thesis, Appendix A, Table A.1)
# ----------------------------------------------------------------------

OBSIDS = {
    "LockmanHole": [
        "101002010", "102018010", "103009010", "104002010",
        "105003010", "106001010", "107001010", "108001010",
        "109014010",
    ],
    "MBM16": [
        "507076010", "507076020", "508078010",
        "508078020", "509073010", "509073020",
    ],
    "NEP": [
        "504070010", "504072010", "504074010", "504076010",
    ],
    "SEP": [
        "504069010", "504071010", "504073010", "504075010",
    ],
}

# Archive-visible additional Lockman pointing. It is deliberately excluded
# from OBSIDS until the paper's stated count is reconciled to unique products.
SUPPLEMENTAL_OBSIDS = {"LockmanHole": ["104002020"]}

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def obs_folder(obsid: str) -> str:
    """
    Suzaku archive directory is given by the leading digit of ObsID.
    Example:
      101002010 -> '1'
      706031010 -> '7'
      509073020 -> '5'
    """
    return obsid[0]


# ----------------------------------------------------------------------
# Generic downloader for auxiliary files (ORB, ATT, EHK, etc.)
# ----------------------------------------------------------------------

def _download_aux_file(obsid: str, kind: str, redownload: bool = False, basedir: Path = CACHE_DIR) -> Path:
    """
    Download and cache a Suzaku auxiliary file from /auxil/.

    Parameters
    ----------
    obsid : str
        Observation ID (e.g., "101002010")
    kind : str
        File type (e.g., "orb", "att", "ehk", "hk", etc.)
    redownload : bool, optional
        Force re-download if True.
    basedir : Path
        Cache base directory (default: CACHE_DIR)

    Returns
    -------
    Path
        Path to the uncompressed FITS file.
    """
    folder = obs_folder(obsid)
    subdir = Path(basedir) / obsid
    subdir.mkdir(parents=True, exist_ok=True)

    gz_name = f"ae{obsid}.{kind}.gz"
    fits_name = gz_name[:-3]
    local_gz = subdir / gz_name
    local_fits = subdir / fits_name
    url = f"{BASE_URL}/{folder}/{obsid}/auxil/{gz_name}"

    # Download if not cached or forced
    if redownload or not local_fits.exists():
        print(f"[Suzaku] Downloading {kind.upper()} for ObsID {obsid} ...")
        urllib.request.urlretrieve(url, local_gz)
        with gzip.open(local_gz, "rb") as f_in, open(local_fits, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    return local_fits


def _load_aux_data(path: Path) -> dict:
    """Load a FITS binary table into a dict of numpy arrays."""
    with fits.open(path) as hdul:
        data = hdul[1].data
        return {name: data[name] for name in data.columns.names}


# --- replace existing download_event with this version ---
import re
from urllib.request import urlopen, urlretrieve

def download_event(obsid: str, xis: int = 0, basedir: Path = CACHE_DIR) -> Path:
    """
    Download a Suzaku cleaned XIS event file from xis/event_cl/.
    Prefers 3x3 mode if available, falls back to 5x5.

    Returns path to the uncompressed .evt file.
    """
    import re
    from urllib.request import urlopen, urlretrieve

    folder = obs_folder(obsid)
    index_url = f"{BASE_URL}/{folder}/{obsid}/xis/event_cl/"
    outdir = Path(basedir) / obsid / f"xis{xis}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Grab directory listing
    with urlopen(index_url) as r:
        html = r.read().decode("utf-8", errors="ignore")

    # Match files for this obsid and XIS
    pat = re.compile(rf'ae{obsid}xi{xis}[^"\'\s]*?_cl\.evt(?:\.gz)?')
    files = sorted(set(pat.findall(html)))
    if not files:
        raise FileNotFoundError(f"No event files found in {index_url} for XIS={xis}")

    # Prioritize 3x3 > 5x5, then prefer uncompressed over .gz
    def score(name: str):
        mode_rank = 0 if "3x3" in name else 1
        gz_rank = 1 if name.endswith(".gz") else 0
        return (mode_rank, gz_rank, name)

    best = sorted(files, key=score)[0]
    remote = index_url + best
    local = outdir / best

    if not local.exists():
        print(f"Downloading {remote}")
        urlretrieve(remote, local)

    # If gzipped, unzip
    if local.suffix == ".gz":
        target = outdir / local.stem
        if not target.exists():
            with gzip.open(local, "rb") as f_in, open(target, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return target
    else:
        return local

# ----------------------------------------------------------------------
# Orbit / Attitude / EHK loaders
# ----------------------------------------------------------------------

def load_orbit(obsid: str, redownload: bool = False):
    return _load_aux_data(_download_aux_file(obsid, "orb", redownload))

def load_attitude(obsid: str, redownload: bool = False):
    return _load_aux_data(_download_aux_file(obsid, "att", redownload))

def load_ehk(obsid: str, redownload: bool = False):
    return _load_aux_data(_download_aux_file(obsid, "ehk", redownload))

# ----------------------------------------------------------------------
# CALMASK loader (manual local file)
# ----------------------------------------------------------------------

def load_calmask(xis: int = 0, basedir: Path = CACHE_DIR) -> np.ndarray:
    """
    Load the Suzaku XIS calibration mask (CALMASK) FITS file.

    Notes
    -----
    This file must be manually downloaded and placed under:
        <basedir>/ae_xi{xis}_calmask_20060731.fits

    Parameters
    ----------
    xis : int, optional
        XIS detector number (0–3). Default is 0.
    basedir : Path, optional
        Directory containing the CALMASK file. Default = CACHE_DIR.

    Returns
    -------
    np.ndarray
        2D CALMASK array (float), where:
            0 = excluded pixel
            1 = good pixel (science region)
    """
    fname = f"ae_xi{xis}_calmask_20060731.fits"
    path = Path(basedir) / fname

    if not path.exists():
        raise FileNotFoundError(
            f"CALMASK file not found: {path}\n"
            "Please download it manually from the Suzaku CALDB and place it in this directory."
        )

    with fits.open(path) as hdul:
        mask = hdul[0].data.astype(float)

    return mask

# ----------------------------------------------------------------------
# Event loader
# ----------------------------------------------------------------------

def load_event(obsid: str, xis: int = 0, redownload: bool = False):
    """
    Download (if needed) and load Suzaku cleaned event file for the given XIS.

    Parameters
    ----------
    obsid : str
        Observation ID (e.g., "101002010")
    xis : int, optional
        XIS detector number (0–3). Default is 0.
    redownload : bool, optional
        Force re-download if True.

    Returns
    -------
    tuple
        (data, hdul)
        data : dict
            Dictionary of event table columns (TIME, X, Y, PI, DETX, DETY, etc.)
        hdul : fits.HDUList
            Full FITS object, including headers and metadata.
    """
    evt_path = download_event(obsid, xis=xis, basedir=CACHE_DIR)
    if redownload and evt_path.exists():
        evt_path.unlink(missing_ok=True)
        evt_path = download_event(obsid, xis=xis, basedir=CACHE_DIR)

    hdul = fits.open(evt_path)
    data = hdul[1].data
    return {name: data[name] for name in data.columns.names}, hdul

