from pathlib import Path
from darknessalp.bfield.IGRF13Cilm import cilm
from darknessalp.bfield.MakeMagGridPoint import MagFieldCalculator
def igrf13(year, lat, lon, alt_km, lmax=13):
    # data/bfield/IGRF13.dat at the repo root
    root = Path(__file__).resolve().parents[3]
    dat_path = root / "data" / "bfield" / "IGRF13.dat"

    c = cilm(dat_path, year)

    a = 6371e3
    r = a + alt_km * 1e3
    
    return MagFieldCalculator(c, a, r, lat, lon, lmax)

