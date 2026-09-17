"""One row per time sample: where, which way, what field, what flags."""
import numpy as np

from darknessalp.field.igrf import load_igrf
from darknessalp.field.magnetic_coords import (
    cutoff_rigidity, magnetic_latitude)
from darknessalp.frames.eci_ecef import eci_to_ecef, spherical
from darknessalp.frames.sky import to_galactic
from darknessalp.frames.sun import sun_vector
from darknessalp.frames.time import decimal_year, times
from darknessalp.geometry.limb import limb_angle
from darknessalp.geometry.los_integral import los_field_integral
from darknessalp.geometry.umbra import in_umbra
from darknessalp.kinematics.slew import angle_between


def state_table(epoch, t_s, r_eci, boresights, lmax=13, q_per_m=0.0):
    """Return a dict of arrays, one entry per sample, for a pointing law."""
    t = np.atleast_1d(t_s).astype(float)
    time = times(epoch, t)
    coeffs = load_igrf(float(np.mean(decimal_year(time))))
    r_ecef = eci_to_ecef(r_eci, time)
    lat, lon, rad = spherical(r_ecef)
    mlat = magnetic_latitude(r_ecef, coeffs)
    sun = sun_vector(time)
    l_gal, b_gal = to_galactic(boresights)

    amp = np.empty(len(t))
    occ = np.empty(len(t), bool)
    for k in range(len(t)):
        res = los_field_integral(r_eci[k], boresights[k], time[k], coeffs,
                                 lmax=lmax, q_per_m=q_per_m)
        amp[k], occ[k] = res["amplitude_tm"][0], res["occulted"][0]

    return {
        "t_s": t, "x_km": r_eci[:, 0], "y_km": r_eci[:, 1],
        "z_km": r_eci[:, 2], "lat_deg": lat, "lon_deg": lon,
        "alt_km": rad - 6371.2, "maglat_deg": mlat,
        "cutoff_gv": cutoff_rigidity(mlat, rad),
        "limb_deg": np.array([limb_angle(r_eci[k], boresights[k])[0]
                              for k in range(len(t))]),
        "sun_deg": angle_between(boresights, sun),
        "umbra": in_umbra(r_eci, sun), "occulted": occ,
        "l_deg": l_gal, "b_deg": b_gal,
        "amp_tm": amp, "k_t2m2": amp**2,
    }


def to_csv(table, path):
    """Write a state table to CSV with a header row."""
    names = list(table)
    data = np.column_stack([np.asarray(table[n], float) for n in names])
    np.savetxt(path, data, delimiter=",", header=",".join(names),
               comments="", fmt="%.6g")
