"""One row per time sample: where, which way, what field, what flags."""
import numpy as np

from darknessalp.field.igrf import load_igrf
from darknessalp.field.magnetic_coords import (
    cutoff_rigidity, magnetic_latitude)
from darknessalp.frames.eci_ecef import eci_to_ecef, spherical
from darknessalp.frames.sky import to_galactic
from darknessalp.frames.sun import sun_position
from darknessalp.frames.time import decimal_year, times
from darknessalp.geometry.limb import limb_angle
from darknessalp.geometry.los_integral import fov_field_integral
from darknessalp.geometry.shadow import shadow
from darknessalp.kinematics.slew import angle_between
from darknessalp.source.halo import column_density


def state_table(epoch, t_s, r_eci, boresights, lmax=13, q_per_m=0.0,
                half_angle_deg=10.0):
    """Return a dict of arrays, one entry per sample, for a pointing law."""
    t = np.atleast_1d(t_s).astype(float)
    time = times(epoch, t)
    coeffs = load_igrf(float(np.mean(decimal_year(time))))
    r_ecef = eci_to_ecef(r_eci, time)
    lat, lon, rad = spherical(r_ecef)
    mlat = magnetic_latitude(r_ecef, coeffs)
    sun_km = sun_position(time)
    sun = sun_km / np.linalg.norm(sun_km, axis=1, keepdims=True)
    lit = shadow(r_eci, sun_km)
    l_gal, b_gal = to_galactic(boresights)

    amp, k_fov, occ_frac, d_bore, d_fov, dk_fov = (
        np.empty(len(t)) for _ in range(6))
    occ = np.empty(len(t), bool)
    for k in range(len(t)):
        res = fov_field_integral(r_eci[k], boresights[k], time[k], coeffs,
                                 lmax=lmax, q_per_m=q_per_m,
                                 half_angle_deg=half_angle_deg)
        amp[k], occ[k] = res["amplitude_tm"][0], res["occulted"][0]
        k_fov[k] = res["k_t2m2"]
        occ_frac[k] = np.sum(res["weights"] * res["occulted"])
        d = column_density(*to_galactic(res["dirs"]))
        d_bore[k], d_fov[k] = d[0], np.sum(res["weights"] * d)
        dk_fov[k] = np.sum(res["weights"] * d * res["amplitude_tm"] ** 2)

    return {
        "t_s": t, "x_km": r_eci[:, 0], "y_km": r_eci[:, 1],
        "z_km": r_eci[:, 2], "lat_deg": lat, "lon_deg": lon,
        "alt_km": rad - 6371.2, "maglat_deg": mlat,
        "cutoff_gv": cutoff_rigidity(mlat, rad),
        "limb_deg": np.array([limb_angle(r_eci[k], boresights[k])[0]
                              for k in range(len(t))]),
        "sun_deg": angle_between(boresights, sun),
        "umbra": lit["umbra"], "penumbra": lit["penumbra"],
        "lit_fraction": lit["lit_fraction"], "occulted": occ,
        "l_deg": l_gal, "b_deg": b_gal,
        "amp_tm": amp, "k_t2m2": amp**2,
        "k_fov_t2m2": k_fov, "fov_occ_frac": occ_frac,
        "d_gevcm2": d_bore, "d_fov_gevcm2": d_fov,
        "dk_fov_gevcm2_t2m2": dk_fov,
    }


def to_csv(table, path):
    """Write a state table to CSV with a header row."""
    names = list(table)
    data = np.column_stack([np.asarray(table[n], float) for n in names])
    np.savetxt(path, data, delimiter=",", header=",".join(names),
               comments="", fmt="%.6g")
