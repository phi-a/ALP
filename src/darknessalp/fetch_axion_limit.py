from pathlib import Path
from urllib.request import urlopen


AXION_LIMITS_RAW = (
    "https://raw.githubusercontent.com/cajohare/AxionLimits/master/"
    "limit_data/"
)
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "axionlimits"


def fetch_axion_limit(name, coupling="AxionPhoton", cache_dir=DATA_DIR):
    """Return (mass, coupling) columns from one AxionLimits file, cached."""
    cache = Path(cache_dir) / coupling / name
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(AXION_LIMITS_RAW + f"{coupling}/{name}", timeout=60) as r:
            cache.write_bytes(r.read())

    masses, couplings = [], []
    for line in cache.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue

        x, y = line.split()[:2]
        masses.append(float(x))
        couplings.append(float(y))

    return masses, couplings
