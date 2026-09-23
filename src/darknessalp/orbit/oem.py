"""CCSDS Orbit Ephemeris Message (OEM, CCSDS 502.0-B) in KVN text form."""
import numpy as np
from astropy.time import Time

from darknessalp.frames.eme2000 import eme2000_to_gcrf, gcrf_to_eme2000

TO_FRAME = {"GCRF": np.atleast_2d, "EME2000": gcrf_to_eme2000}
FROM_FRAME = {"GCRF": np.atleast_2d, "EME2000": eme2000_to_gcrf}


def write_oem(path, time, r, v, ref_frame="GCRF", object_name="DARKNESS"):
    """Write GCRF states (km, km/s) as a CCSDS OEM on ref_frame axes."""
    epochs = Time(time, precision=6).isot
    r, v = TO_FRAME[ref_frame](r), TO_FRAME[ref_frame](v)
    head = ["CCSDS_OEM_VERS = 2.0",
            f"CREATION_DATE = {Time.now().isot}",
            "ORIGINATOR = DARKNESSALP", "",
            "META_START",
            f"OBJECT_NAME = {object_name}",
            f"OBJECT_ID = {object_name}",
            "CENTER_NAME = EARTH",
            f"REF_FRAME = {ref_frame}",
            f"TIME_SYSTEM = {time.scale.upper()}",
            f"START_TIME = {epochs[0]}",
            f"STOP_TIME = {epochs[-1]}",
            "META_STOP", ""]
    rows = [f"{t} {x:.6f} {y:.6f} {z:.6f} {vx:.9f} {vy:.9f} {vz:.9f}"
            for t, (x, y, z), (vx, vy, vz) in zip(epochs, r, v)]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(head + rows) + "\n")


def read_oem(path):
    """Return (Time, r (N, 3) km, v (N, 3) km/s) on GCRF axes from an OEM."""
    meta, epochs, rows = {}, [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts or parts[0] == "COMMENT":
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                meta.setdefault(key.strip(), value.strip())
            elif len(parts) >= 7:
                epochs.append(parts[0])
                rows.append(parts[1:7])

    state = np.array(rows, float)
    back = FROM_FRAME[meta["REF_FRAME"]]
    time = Time(epochs, scale=meta["TIME_SYSTEM"].lower())
    return time, back(state[:, :3]), back(state[:, 3:])
