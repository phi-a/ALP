"""ConOps figures: the geometry and signal pictures behind the ALP objective.

Importable figure functions for jupyter/conops.ipynb and the deck; the
CLI renders the reference case (Galactic Centre, ISS-like, one day).
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LogNorm, TwoSlopeNorm

from darknessalp import (field, frames, geometry, kinematics, orbit,
                         pointing, sim, source)
from darknessalp.constants import R_EARTH_KM, R_EQUATOR_KM

SHADE = "#eeeae0"           # science window
UMBRA = "#3b3b6d"
SUNLIT = "0.6"
SCIENCE = "#e07b39"
SUN = "#f2b134"


def science_mask(table, mode_index=None):
    """Return the samples that count as exposure: umbra, sky in view."""
    sci = table["umbra"] & ~table["occulted"]
    return sci if mode_index is None else sci & (mode_index == 0)


def _shade(ax, hours, mask):
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    for start, stop in edges.reshape(-1, 2):
        ax.axvspan(hours[start], hours[stop - 1], color=SHADE, lw=0,
                   zorder=0)


def _ray_plane(r_eci, n_hat):
    """Return (up, side): the local vertical and the ray's in-plane axis."""
    r = np.asarray(r_eci, float)
    n = np.asarray(n_hat, float)
    up = r / np.linalg.norm(r)
    side = n - np.dot(n, up) * up
    if np.linalg.norm(side) < 1e-9:              # ray along the vertical
        side = np.cross(up, [0.0, 0.0, 1.0])
    return up, side / np.linalg.norm(side)


def _north_up(up, side):
    """Return (x, y, tilt): in-plane axes, y toward projected north."""
    normal = np.cross(up, side)
    y = np.array([0.0, 0.0, 1.0]) - normal[2] * normal   # spin axis ~ ECI z
    if np.linalg.norm(y) < 1e-6:                # plane is the equator
        y = up
    y = y / np.linalg.norm(y)
    x = np.cross(y, normal)
    if x @ up < 0:                              # spacecraft on the right
        x = -x
    return x, y, np.degrees(np.arcsin(abs(normal[2])))


def _field_lines(ax, x_hat, y_hat, time, coeffs, lmax, extent_re):
    """Draw the in-plane field, the Earth and the spin axis."""
    g = np.linspace(-extent_re, extent_re, 60) * R_EARTH_KM   # skips r = 0
    gx, gy = np.meshgrid(g, g)
    pts = gx[..., None] * x_hat + gy[..., None] * y_hat
    b = field.igrf_field_eci(pts.reshape(-1, 3), time, coeffs, lmax)
    b = b.reshape(pts.shape)
    ax.streamplot(g / R_EARTH_KM, g / R_EARTH_KM, b @ x_hat, b @ y_hat,
                  color="0.75", density=1.3, linewidth=0.8, arrowsize=0.8)
    ax.plot([0, 0], [-extent_re, extent_re], color="0.45", lw=0.8,
            ls="--", zorder=2)
    ax.text(0.06, 0.92 * extent_re, "N", color="0.35", fontsize=10)
    ax.add_patch(plt.Circle((0, 0), 1.0, color="steelblue", zorder=3))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            zorder=4)
    ax.set_aspect("equal")
    ax.set_xlim(-extent_re, extent_re)
    ax.set_ylim(-extent_re, extent_re)
    ax.set_xlabel("across the spin axis  [Earth radii]")
    ax.set_ylabel("toward north, spin axis projected  [Earth radii]")


def meridian_plane(r_eci, n_hat, time, coeffs, lmax=13, extent_re=2.6):
    """Return a figure: the field in the plane of the ray, and |A(s)|."""
    r = np.asarray(r_eci, float)
    n = np.asarray(n_hat, float)
    x_hat, y_hat, tilt = _north_up(*_ray_plane(r, n))

    res = geometry.los_field_integral(r, n, time, coeffs, lmax=lmax)
    s_km = res["s_km"][0]
    running = res["running_tm"][0]
    ray = r + s_km[:, None] * n
    x, y = ray @ x_hat / R_EARTH_KM, ray @ y_hat / R_EARTH_KM

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(12, 5.8), gridspec_kw={"width_ratios": [1.25, 1]})
    _field_lines(ax, x_hat, y_hat, time, coeffs, lmax, extent_re)
    sc = ax.scatter(x, y, c=running, cmap="viridis", s=14, zorder=5)
    ax.plot(x[0], y[0], "k^", ms=10, zorder=6, label="spacecraft")
    ax.annotate("boresight", (x[len(x) // 5], y[len(y) // 5]),
                xytext=(10, 10), textcoords="offset points")
    occulted = bool(res["occulted"][0])
    if occulted:
        ax.plot(x[-1], y[-1], "kx", ms=8, zorder=6, label="ray hits Earth")
    ax.set_title(f"Field in the plane of the ray, north up\n(plane "
                 f"{tilt:.0f}° from the spin axis)", fontsize=11)
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


def _sphere(ax, radius, color, alpha, axis=None, length=0.0):
    """Draw a sphere, or a cylinder of that radius along axis."""
    u = np.linspace(0, 2 * np.pi, 40)
    if axis is None:
        w = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(w))
        y = np.outer(np.sin(u), np.sin(w))
        z = np.outer(np.ones_like(u), np.cos(w))
        xyz = radius * np.stack([x, y, z], -1)
    else:
        a, b = geometry.fov_axes(axis)
        ring = radius * (np.cos(u)[:, None] * a + np.sin(u)[:, None] * b)
        ell = np.linspace(0, length, 2)
        xyz = ring[:, None, :] + ell[None, :, None] * axis
    ax.plot_surface(*np.moveaxis(xyz, -1, 0), color=color, alpha=alpha,
                    linewidth=0, shade=False)


def orbit_geometry(r_eci, n_hats, sun_hat, target, sci, umbra,
                   radiator=None, n_orbit=93, every=4, view=None):
    """Return a figure: one orbit in 3D, Sun, shadow, target, boresights."""
    w = slice(0, n_orbit)
    p = np.asarray(r_eci, float)[w] / R_EARTH_KM
    n = np.asarray(n_hats, float)[w]
    sci, umbra = np.asarray(sci)[w], np.asarray(umbra)[w]
    s = np.asarray(sun_hat, float)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d", computed_zorder=False)
    ax.set_position((0.0, 0.0, 1.0, 0.95))
    _sphere(ax, 1.0, "steelblue", 0.35)
    _sphere(ax, 1.0, "0.3", 0.12, axis=-s, length=2.4)
    ax.plot(*p.T, color="0.4", lw=0.8)

    cls = np.where(sci, 2, np.where(umbra, 1, 0))
    colors = [SUNLIT, UMBRA, SCIENCE]
    labels = ["sunlit: boresight anti-Sun",
              "umbra, target behind Earth: looking into it",
              "umbra, target in view: science"]
    pick = np.zeros(len(p), bool)
    pick[::every] = True
    for c, (col, lab) in enumerate(zip(colors, labels)):
        m = (cls == c) & pick
        ax.scatter(*p[cls == c].T, s=8, color=col, depthshade=False)
        ax.quiver(*p[m].T, *n[m].T, length=0.7, color=col,
                  arrow_length_ratio=0.25, lw=1.4, label=lab)
    if radiator is not None:
        q = np.asarray(radiator, float)[w]
        m = pick & (cls == 2)
        ax.quiver(*p[m].T, *q[m].T, length=0.35, color="crimson",
                  arrow_length_ratio=0.3, lw=1.0,
                  label="radiator normal (roll: away from Earth)")

    for vec, col, text in [(s, SUN, "to the Sun"),
                           (target, "k", "to the target (fixed on the sky)")]:
        ax.quiver(0, 0, 0, *vec, length=2.6, color=col,
                  arrow_length_ratio=0.08, lw=2)
        ax.text(*(2.75 * vec), text, color=col, fontsize=9)
    ax.text(*(-2.5 * s), "shadow", color="0.3", fontsize=9, ha="center")

    lim = 1.7
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    if view is None:                  # camera on the Sun x target normal
        h = np.cross(p[0], p[1])
        h /= np.linalg.norm(h)
        cam = np.cross(s, target)
        cam *= np.sign(cam @ h) / np.linalg.norm(cam)
        cam = cam + 0.6 * h
        view = (np.degrees(np.arcsin(cam[2] / np.linalg.norm(cam))),
                np.degrees(np.arctan2(cam[1], cam[0])))
    ax.view_init(elev=view[0], azim=view[1])
    ax.legend(loc="lower left", fontsize=9, frameon=False,
              bbox_to_anchor=(0.0, 0.0))
    ax.set_title("One orbit: what the schedule sees  [Earth radii, ECI]",
                 y=0.98)
    return fig


def field_geometry(coeffs, alt_km=420.0, inc_deg=51.6, lmax=13,
                   extent_re=3.0):
    """Return a figure: the field in the meridian plane of the dipole."""
    north = field.dipole_axis(coeffs)
    north = north * np.sign(north[2])           # northern end, ECEF
    z = np.array([0.0, 0.0, 1.0])
    x_hat = north - north[2] * z
    x_hat /= np.linalg.norm(x_hat)
    tilt = np.degrees(np.arccos(north[2]))
    lon = np.degrees(np.arctan2(x_hat[1], x_hat[0]))

    g = np.linspace(-extent_re, extent_re, 240)
    gx, gy = np.meshgrid(g, g)
    pts = (gx[..., None] * x_hat + gy[..., None] * z) * R_EARTH_KM
    b = field.igrf_field(pts.reshape(-1, 3), coeffs, lmax)
    b = b.reshape(pts.shape)
    inside = np.hypot(gx, gy) < 1.0
    bx = np.ma.masked_where(inside, b @ x_hat)
    by = np.ma.masked_where(inside, b @ z)
    b_ut = np.ma.masked_where(np.hypot(gx, gy) < 0.9,
                              np.linalg.norm(b, axis=-1) * 1e6)

    # footpoints at magnetic latitudes, both hemispheres, both sides
    axis = np.arctan2(north[2], north @ x_hat)
    lat = np.radians(np.arange(15, 76, 7.5))
    ang = np.concatenate([axis + s * (np.pi / 2 - lat)
                          for s in (-1, 1)])
    ang = np.concatenate([ang, ang + np.pi])
    starts = 1.02 * np.stack([np.cos(ang), np.sin(ang)], 1)

    fig, ax = plt.subplots(figsize=(8.5, 8))
    cs = ax.contourf(gx, gy, b_ut, levels=[0.5, 1, 2, 5, 10, 20, 50, 70],
                     norm=LogNorm(0.3, 100), cmap="Blues")
    ax.streamplot(g, g, bx, by, start_points=starts, color="0.25",
                  linewidth=0.8, arrowsize=0.8, broken_streamlines=False,
                  integration_direction="both")
    ax.add_patch(plt.Circle((0, 0), 1.0, color="steelblue", zorder=3))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            zorder=4)

    ax.plot([0, 0], [-extent_re, extent_re], color="k", lw=1, ls="--",
            zorder=5)
    ax.text(0.06, 0.93 * extent_re, "spin axis", fontsize=9, zorder=5)
    d = np.array([np.cos(axis), np.sin(axis)]) * extent_re
    ax.plot([-d[0], d[0]], [-d[1], d[1]], color="crimson", lw=1, ls="--",
            zorder=5)
    ax.text(*(0.8 * d + [0.08, 0]), f"dipole axis, {tilt:.1f}° off",
            color="crimson", fontsize=9, zorder=5)

    rad = (R_EQUATOR_KM + alt_km) / R_EARTH_KM
    arc = np.radians(np.linspace(-inc_deg, inc_deg, 60))
    for side in (1, -1):
        ax.plot(side * rad * np.cos(arc), rad * np.sin(arc), color=SCIENCE,
                lw=3, zorder=6, label=None if side < 0 else
                f"orbit: {alt_km:.0f} km, latitudes ±{inc_deg:.1f}°")

    ax.set_aspect("equal")
    ax.set_xlim(-extent_re, extent_re)
    ax.set_ylim(-extent_re, extent_re)
    ax.set_xlabel(f"toward longitude {lon:.0f}°  [Earth radii]")
    ax.set_ylabel("along the spin axis  [Earth radii]")
    ax.set_title("The geomagnetic field in the meridian plane of the dipole"
                 " (IGRF)", fontsize=11)
    ax.legend(loc="lower left", fontsize=9)
    fig.colorbar(cs, ax=ax, shrink=0.8, label="|B|  [µT]", format="%g",
                 ticks=[0.5, 1, 2, 5, 10, 20, 50])
    fig.tight_layout()
    return fig


def ray_fan(r_eci, n_hat, time, coeffs, lmax=13, step_deg=3.0,
            extent_re=2.6, half_angle_deg=10.0):
    """Return a figure: rays from one spot coloured by K, and |A| by angle."""
    r = np.asarray(r_eci, float)
    n = np.asarray(n_hat, float)
    up, side = _ray_plane(r, n)
    x_hat, y_hat, tilt = _north_up(up, side)
    axes = np.stack([x_hat, y_hat], 1)          # (3, 2) onto the page
    theta = np.radians(np.arange(-180, 180, step_deg))
    dirs = np.cos(theta)[:, None] * up + np.sin(theta)[:, None] * side
    res = geometry.los_field_integral(r, dirs, time, coeffs, lmax=lmax)
    amp = res["amplitude_tm"]
    k = amp**2
    rho = geometry.earth_angular_radius_deg(r)
    n_theta = np.degrees(np.arctan2(n @ side, n @ up))
    norm = LogNorm(vmin=max(k.min(), 1.0), vmax=k.max())

    fig = plt.figure(figsize=(13, 6))
    ax = fig.add_subplot(1, 2, 1)
    _field_lines(ax, x_hat, y_hat, time, coeffs, lmax, extent_re)
    start = r @ axes / R_EARTH_KM
    s_end = np.minimum(res["s_km"][:, -1], 4 * extent_re * R_EARTH_KM)
    end = start + s_end[:, None] / R_EARTH_KM * (dirs @ axes)
    lines = LineCollection(np.stack([np.tile(start, (len(k), 1)), end], 1),
                           cmap="viridis", norm=norm, lw=1.6, zorder=5)
    lines.set_array(k)
    ax.add_collection(lines)
    for off in (-half_angle_deg, 0.0, half_angle_deg):
        a = np.radians(n_theta + off)
        d = (np.cos(a) * up + np.sin(a) * side) @ axes
        ax.plot(*np.stack([start, start + 1.6 * d]).T, color="k",
                lw=2.2 if off == 0 else 0.8, zorder=6)
    ax.plot(*start, "k^", ms=10, zorder=7)
    ax.set_title(f"Rays from the spacecraft coloured by K, north up\n"
                 f"(plane {tilt:.0f}° from the spin axis)", fontsize=11)
    fig.colorbar(lines, ax=ax, shrink=0.8, label="K = |A|²  [T² m²]")

    ax2 = fig.add_subplot(1, 2, 2, projection="polar")
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    edge = np.radians(np.linspace(180 - rho, 180 + rho, 50))
    ax2.fill_between(edge, 0, amp.max() * 1.1, color="steelblue",
                     alpha=0.35, lw=0, label="Earth disk")
    loop = np.r_[theta, theta[0]]
    ax2.plot(loop, np.r_[amp, amp[0]], color="k", lw=1.2)
    ax2.scatter(theta, amp, c=k, cmap="viridis", norm=norm, s=18, zorder=5)
    amp_n = np.interp(n_theta, np.degrees(theta), amp)
    ax2.plot(np.radians(n_theta), amp_n, "o", ms=11, mfc="none", mec="k",
             mew=1.8, label="boresight")
    ax2.set_rmax(amp.max() * 1.1)
    ax2.set_xticks(np.radians([0, 90, 180, 270]))
    ax2.set_xticklabels(["zenith", "", "nadir", ""], fontsize=9)
    ax2.tick_params(labelsize=8)
    ax2.set_title("|A|  [T m] against the angle from the zenith", pad=15)
    ax2.legend(loc="lower right", fontsize=9, bbox_to_anchor=(1.15, -0.05))
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
    sci = science_mask(table)
    k = int(np.flatnonzero(sci)[0])
    sun = frames.sun_vector(time[:1])[0]
    per_orbit = int(orbit.period_s(R_EQUATOR_KM + a.alt) / a.cadence)

    orbit_geometry(r, n, sun, n[0], sci, table["umbra"], n_orbit=per_orbit,
                   every=max(1, per_orbit // 24)).savefig(
        out / "orbit_geometry.png", dpi=150)
    field_geometry(coeffs, a.alt, a.inc, a.lmax).savefig(
        out / "field_geometry.png", dpi=150)
    ray_fan(r[k], n[k], time[k], coeffs, a.lmax).savefig(
        out / "ray_fan.png", dpi=150)
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
