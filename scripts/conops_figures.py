"""ConOps figures: the geometry and signal pictures behind the ALP objective.

Importable figure functions for jupyter/conops.ipynb and the deck; the
CLI renders the reference case (Galactic Centre, ISS-like, one day).
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm, TwoSlopeNorm

from darknessalp import field, frames, geometry, orbit, pointing, sim, source
from darknessalp.constants import R_EARTH_KM, R_EQUATOR_KM

SHADE = "#eeeae0"           # science window
UMBRA = "#3b3b6d"


def science_mask(table, mode_index=None):
    """Return the samples that count as exposure: umbra, sky in view."""
    sci = table["umbra"] & ~table["occulted"]
    return sci if mode_index is None else sci & (mode_index == 0)


def _shade(ax, hours, mask):
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    for start, stop in edges.reshape(-1, 2):
        ax.axvspan(hours[start], hours[stop - 1], color=SHADE, lw=0,
                   zorder=0)


def meridian_plane(r_eci, n_hat, time, coeffs, lmax=13, extent_re=2.6):
    """Return a figure: the field in the plane of the ray, and |A(s)|."""
    r = np.asarray(r_eci, float)
    n = np.asarray(n_hat, float)
    up = r / np.linalg.norm(r)
    side = n - np.dot(n, up) * up
    if np.linalg.norm(side) < 1e-9:              # ray along the vertical
        side = np.cross(up, [0.0, 0.0, 1.0])
    side /= np.linalg.norm(side)

    # field lines in the plane spanned by up and the ray
    g = np.linspace(-extent_re, extent_re, 60) * R_EARTH_KM   # skips r = 0
    gx, gy = np.meshgrid(g, g)
    pts = gx[..., None] * up + gy[..., None] * side
    b = field.igrf_field_eci(pts.reshape(-1, 3), time, coeffs, lmax)
    b = b.reshape(pts.shape)

    res = geometry.los_field_integral(r, n, time, coeffs, lmax=lmax)
    s_km = res["s_km"][0]
    running = res["running_tm"][0]
    ray = r + s_km[:, None] * n
    x, y = ray @ up / R_EARTH_KM, ray @ side / R_EARTH_KM

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})
    ax.streamplot(g / R_EARTH_KM, g / R_EARTH_KM, (b @ up).T,
                  (b @ side).T, color="0.75", density=1.3, linewidth=0.8,
                  arrowsize=0.8)
    ax.add_patch(plt.Circle((0, 0), 1.0, color="steelblue", zorder=3))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            zorder=4)
    sc = ax.scatter(x, y, c=running, cmap="viridis", s=14, zorder=5)
    ax.plot(x[0], y[0], "k^", ms=10, zorder=6, label="spacecraft")
    ax.annotate("boresight", (x[len(x) // 5], y[len(y) // 5]),
                xytext=(10, 10), textcoords="offset points")
    occulted = bool(res["occulted"][0])
    if occulted:
        ax.plot(x[-1], y[-1], "kx", ms=8, zorder=6, label="ray hits Earth")
    ax.set_aspect("equal")
    ax.set_xlim(-extent_re, extent_re)
    ax.set_ylim(-extent_re, extent_re)
    ax.set_xlabel("along local vertical  [Earth radii]")
    ax.set_ylabel("along the ray  [Earth radii]")
    ax.set_title("Field lines in the plane of the line of sight")
    ax.legend(loc="lower left", fontsize=9)
    fig.colorbar(sc, ax=ax, shrink=0.8, label="running |A|  [T m]")

    s_re = s_km / R_EARTH_KM
    ax2.plot(s_re, running, color="k")
    ax2.fill_between(s_re, 0, running, color="#cde2fb")
    ax2.set_xlabel("distance along the ray  [Earth radii]")
    ax2.set_ylabel("|A(s)| = |∫ B⊥ e^{iqs} ds|  [T m]")
    end = "the Earth surface" if occulted else "10 Earth radii"
    ax2.set_title(f"K = |A|² = {running[-1] ** 2:.0f} T² m² "
                  f"by {end}")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def orbit_strip(table, mode_index=None, hours=4.7):
    """Return a figure: K, cutoff rigidity, limb angle over a few orbits."""
    h = table["t_s"] / 3600
    w = h < hours
    sci = science_mask(table, mode_index)
    fig, ax = plt.subplots(3, 1, figsize=(10, 7.2), sharex=True)
    for a in ax:
        _shade(a, h[w], sci[w])
    ax[0].plot(h[w], table["k_fov_t2m2"][w] / 1e3, label="aperture average")
    ax[0].plot(h[w], table["k_t2m2"][w] / 1e3, lw=1.2, label="boresight only")
    ax[0].set_ylabel("K  [10³ T² m²]")
    ax[0].set_title("Conversion kernel")
    ax[0].legend(loc="upper right", ncols=2, frameon=False)
    ax[1].plot(h[w], table["cutoff_gv"][w])
    ax[1].set_ylabel("cutoff rigidity  [GV]")
    ax[1].set_title("Particle-background proxy (high = shielded)")
    ax[2].plot(h[w], table["limb_deg"][w])
    ax[2].axhline(0, color="0.7", lw=1)
    ax[2].set_ylabel("limb angle  [deg]")
    ax[2].set_title("Boresight above the limb (negative = at Earth)")
    ax[2].set_xlabel("hours after epoch")
    ax[0].text(0.01, 0.88, "shaded: science exposure", color="0.35",
               fontsize=9, transform=ax[0].transAxes)
    fig.tight_layout()
    return fig


def ground_track(table, coeffs, mode_index=None, alt_km=420.0):
    """Return a figure: the day's ground track coloured by K, with modes."""
    lat = np.linspace(-89, 89, 90)
    lon = np.linspace(-180, 180, 181)
    glon, glat = np.meshgrid(np.radians(lon), np.radians(lat))
    rad = R_EARTH_KM + alt_km
    pts = rad * np.stack([np.cos(glat) * np.cos(glon),
                          np.cos(glat) * np.sin(glon), np.sin(glat)], -1)
    b_ut = np.linalg.norm(field.igrf_field(pts.reshape(-1, 3), coeffs),
                          axis=1).reshape(glat.shape) * 1e6

    fig, ax = plt.subplots(figsize=(12, 5.6))
    cs = ax.contourf(lon, lat, b_ut, levels=[0, 21, 24], colors=["#f6d5c8",
                     "#fbebe4"], alpha=0.9)
    ax.contour(lon, lat, b_ut, levels=[21, 24], colors="#c8836a",
               linewidths=0.8)
    sci = science_mask(table, mode_index)
    sunlit = ~table["umbra"]
    ax.scatter(table["lon_deg"][sunlit], table["lat_deg"][sunlit], s=6,
               color="0.75", label="sunlit: anti-Sun pointing")
    dark = table["umbra"] & ~sci
    ax.scatter(table["lon_deg"][dark], table["lat_deg"][dark], s=10,
               color=UMBRA, label="umbra, target behind Earth")
    sc = ax.scatter(table["lon_deg"][sci], table["lat_deg"][sci], s=16,
                    c=table["k_fov_t2m2"][sci], cmap="viridis",
                    norm=LogNorm(vmin=1e2, vmax=1e5), label="science exposure")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-70, 70)
    ax.set_xlabel("longitude  [deg]")
    ax.set_ylabel("latitude  [deg]")
    ax.set_title("One day: where the science happens, and how strong K is")
    ax.text(-45, -40, "weak field\n|B| < 21 µT", color="#a0523a",
            fontsize=9, ha="center")
    ax.legend(loc="lower left", fontsize=9, markerscale=1.5)
    fig.colorbar(sc, ax=ax, shrink=0.85, label="aperture K  [T² m²]")
    fig.tight_layout()
    return fig


def sky_scan(time, r, coeffs, lmax=13, n_dir=192, half_angle_deg=10.0):
    """Return a dict of per-direction K (T, N), occultation, D and (l, b)."""
    i = np.arange(n_dir) + 0.5
    b = np.degrees(np.arcsin(1 - 2 * i / n_dir))
    l = np.degrees(np.pi * (1 + 5 ** 0.5) * i) % 360
    dirs = frames.galactic_vector(l, b)

    k = np.empty((len(r), n_dir))
    occ = np.empty((len(r), n_dir), bool)
    for j in range(len(r)):
        res = geometry.los_field_integral(r[j], dirs, time[j], coeffs,
                                          lmax=lmax)
        k[j], occ[j] = res["amplitude_tm"] ** 2, res["occulted"]

    d_fov = np.empty(n_dir)
    for m in range(n_dir):
        cone, w = geometry.cone_directions(dirs[m], half_angle_deg)
        d_fov[m] = np.sum(w * source.column_density(*frames.to_galactic(cone)))
    return {"l": l, "b": b, "dirs": dirs, "k": k, "occulted": occ,
            "d_fov": d_fov}


def sky_maps(scan, umbra, cutoff_gv, dt_s):
    """Return a figure: continuum and line signal per day, and the confound."""
    use = umbra[:, None] & ~scan["occulted"]
    fom_c = np.sum(np.where(use, scan["k"], 0.0), axis=0) * dt_s
    fom_l = fom_c * scan["d_fov"]
    corr = np.full(len(scan["l"]), np.nan)
    for m in range(len(corr)):
        u = use[:, m]
        if u.sum() > 10:
            corr[m] = np.corrcoef(scan["k"][u, m], cutoff_gv[u])[0, 1]
    from_gc = np.degrees(np.arccos(np.cos(np.radians(scan["b"]))
                                   * np.cos(np.radians(scan["l"]))))
    gc = int(np.argmin(from_gc))

    x = -np.radians(((scan["l"] + 180) % 360) - 180)
    y = np.radians(scan["b"])
    panels = [(fom_c / fom_c[gc], "Blues", None,
               "Continuum signal per day  [× GC pointing]"),
              (fom_l / fom_l[gc], "Oranges", None,
               "Milky Way line signal per day  [× GC pointing]"),
              (corr, "RdBu_r", TwoSlopeNorm(0, -1, 1),
               "Confound: corr(K, cutoff rigidity)")]
    fig = plt.figure(figsize=(15, 4.8))
    for i, (v, cmap, norm, title) in enumerate(panels):
        ax = fig.add_subplot(1, 3, i + 1, projection="mollweide")
        sc = ax.scatter(x, y, c=v, cmap=cmap, norm=norm, s=40, lw=0)
        ax.plot(x[gc], y[gc], "o", ms=11, mfc="none", mec="k", mew=1.6)
        ax.annotate("GC", (x[gc], y[gc]), xytext=(8, 8),
                    textcoords="offset points", fontweight="bold")
        ax.set_title(title, fontsize=10, pad=12)
        ax.set_xticklabels([])
        ax.tick_params(labelsize=8)
        ax.grid(alpha=0.3)
        fig.colorbar(sc, ax=ax, orientation="horizontal", pad=0.05,
                     fraction=0.05)
    fig.text(0.01, 0.02, "Galactic coordinates, l = 0 at centre. Each dot: "
             "one fixed inertial pointing held for the day.", fontsize=9,
             color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return fig, {"rel_continuum": fom_c / fom_c[gc],
                 "rel_line": fom_l / fom_l[gc], "corr": corr, "gc": gc}


def coherence_scan(r, n, time, coeffs, samples, q_grid, lmax=13):
    """Return sum K(q) / sum K(0) over the chosen samples, boresight rays."""
    def total(q):
        return sum(geometry.los_field_integral(
            r[k], n[k], time[k], coeffs, lmax=lmax,
            q_per_m=q)["amplitude_tm"][0] ** 2 for k in samples)
    return np.array([total(q) for q in q_grid]) / total(0.0)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("out", help="directory for the PNGs")
    p.add_argument("--epoch", default="2027-05-01T00:00:00", help="UTC")
    p.add_argument("--alt", type=float, default=420.0, help="km")
    p.add_argument("--inc", type=float, default=51.6, help="deg")
    p.add_argument("--cadence", type=float, default=600.0, help="s")
    p.add_argument("--lmax", type=int, default=13, help="IGRF degree")
    p.add_argument("--sky", action="store_true", help="also the sky maps")
    return p.parse_args()


def main():
    a = parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t = np.arange(0.0, 86400.0, a.cadence)
    time = frames.times(a.epoch, t)
    r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + a.alt, 0.0, a.inc,
                                     0.0, 0.0, 0.0)
    r, _ = orbit.propagate(r0, v0, t)
    n = np.tile(pointing.sky_target("gc"), (len(t), 1))
    coeffs = field.load_igrf(float(np.mean(frames.decimal_year(time))))
    table = sim.state_table(a.epoch, t, r, n, lmax=a.lmax)
    k = int(np.flatnonzero(science_mask(table))[0])

    meridian_plane(r[k], n[k], time[k], coeffs, a.lmax).savefig(
        out / "conversion_path.png", dpi=150)
    orbit_strip(table).savefig(out / "orbit_strip.png", dpi=150)
    ground_track(table, coeffs, alt_km=a.alt).savefig(
        out / "ground_track.png", dpi=150)
    if a.sky:
        scan = sky_scan(time, r, coeffs, a.lmax)
        fig, _ = sky_maps(scan, table["umbra"], table["cutoff_gv"], a.cadence)
        fig.savefig(out / "sky_maps.png", dpi=150)


if __name__ == "__main__":
    main()
