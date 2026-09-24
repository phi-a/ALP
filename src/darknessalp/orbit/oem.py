"""CCSDS Orbit Ephemeris Message (OEM, CCSDS 502.0-B) in KVN text form."""
import numpy as np
from astropy.time import Time

from darknessalp.frames.eme2000 import eme2000_to_gcrf, gcrf_to_eme2000

TO_FRAME = {"GCRF": np.atleast_2d, "EME2000": gcrf_to_eme2000}
FROM_FRAME = {"GCRF": np.atleast_2d, "ICRF": np.atleast_2d,
              "EME2000": eme2000_to_gcrf}  # ICRF about Earth = GCRF


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


def _epoch(text):
    """Return a CCSDS epoch in a form astropy reads."""
    day, _, clock = text.partition("T")
    if len(day) == 8:
        return day.replace("-", ":") + ":" + clock  # YYYY-DDD day of year
    return text


def _segments(path):
    """Return one dict per OEM segment: metadata, epochs, state rows."""
    segments, in_cov = [], False
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split() or ["COMMENT"]
            if parts[0] in ("COVARIANCE_START", "COVARIANCE_STOP"):
                in_cov = parts[0] == "COVARIANCE_START"
            if parts[0] == "META_START":
                segments.append({"epochs": [], "rows": []})
            if parts[0] == "COMMENT" or in_cov or not segments:
                continue

            seg = segments[-1]
            if "=" in line:
                key, _, value = line.partition("=")
                seg[key.strip()] = value.strip()
            elif len(parts) >= 7:
                seg["epochs"].append(_epoch(parts[0]))
                seg["rows"].append(parts[1:7])
    return segments


def read_oem(path):
    """Return (Time, r (N, 3) km, v (N, 3) km/s) on GCRF axes from an OEM."""
    times, r, v = [], [], []
    for seg in _segments(path):
        if seg["CENTER_NAME"] != "EARTH":
            raise ValueError(seg["CENTER_NAME"])
        state = np.array(seg["rows"], float)
        back = FROM_FRAME[seg["REF_FRAME"]]
        times.append(Time(seg["epochs"], scale=seg["TIME_SYSTEM"].lower()))
        r.append(back(state[:, :3]))
        v.append(back(state[:, 3:]))
    return np.concatenate(times), np.vstack(r), np.vstack(v)
