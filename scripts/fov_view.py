"""Draw what the boresight sees: Earth, Sun, Galaxy, sources, and K."""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from darknessalp import background, field, frames, geometry, orbit, pointing
from darknessalp.constants import R_EQUATOR_KM

HALF_ANGLE = 10.0


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", default="gc", help="gc, apex, or ra,dec")
    p.add_argument("--epoch", default="2027-01-01T00:00:00", help="UTC")
    p.add_argument("--t", type=float, default=0.0, help="s after epoch")
    p.add_argument("--alt", type=float, default=420.0, help="km")
    p.add_argument("--inc", type=float, default=51.6, help="deg")
    p.add_argument("--raan", type=float, default=0.0, help="deg")
    p.add_argument("--extent", type=float, default=40.0, help="deg")
    p.add_argument("--lmax", type=int, default=13, help="IGRF degree")
    p.add_argument("--out", default=None, help="png path; show if absent")
    return p.parse_args()


def fov_view(r_eci, time, n_hat, coeffs, extent=40.0, lmax=13, ax=None):
    """Draw the boresight view on ax; return ax."""
    ax = ax or plt.subplots(figsize=(7, 7))[1]
    x_hat, y_hat = geometry.fov_axes(n_hat)
    grid = np.linspace(-extent, extent, 61)
    gx, gy = np.meshgrid(grid, grid)
    dirs = geometry.offset_direction(gx, gy, n_hat, x_hat,
                                     y_hat).reshape(-1, 3)

    res = geometry.los_field_integral(r_eci, dirs, time, coeffs, lmax=lmax,
                                      n_steps=100)
    amp = np.where(res["occulted"], np.nan, res["amplitude_tm"])
    im = ax.pcolormesh(grid, grid, amp.reshape(gx.shape), cmap="viridis",
                       shading="nearest", alpha=0.85)
    plt.colorbar(im, ax=ax, shrink=0.8, label="|A| = B_perp L  [T m]")

    nadir = -r_eci / np.linalg.norm(r_eci)
    depth = np.degrees(np.arccos(np.clip(dirs @ nadir, -1, 1)))
    rho = geometry.earth_angular_radius_deg(r_eci)
    ax.contourf(grid, grid, depth.reshape(gx.shape), levels=[0, rho],
                colors="steelblue", alpha=0.5)
    ax.fill([], [], color="steelblue", alpha=0.5, label="Earth")

    plane = frames.galactic_vector(np.arange(0, 360, 2), np.zeros(180))
    px, py = geometry.project(plane, n_hat, x_hat, y_hat)
    ax.scatter(px, py, s=3, color="grey", label="Galactic plane")
    ax.plot(*geometry.project(frames.galactic_vector(0, 0), n_hat, x_hat,
                              y_hat), "k+", markersize=12, label="GC")

    sun = frames.sun_vector(time)[0]
    if np.dot(sun, n_hat) > 0:
        ax.plot(*geometry.project(sun, n_hat, x_hat, y_hat), "o",
                color="orange", markersize=12, label="Sun")

    names, vec, flux = background.source_vectors()
    sx, sy = geometry.project(vec, n_hat, x_hat, y_hat)
    for name, x, y, f in zip(names, sx, sy, flux):
        if np.hypot(x, y) < extent * 1.4:
            ax.plot(x, y, "r.", markersize=4 + 3 * np.log10(f))
            ax.annotate(name, (x, y), fontsize=7, xytext=(3, 3),
                        textcoords="offset points")

    ax.add_patch(plt.Circle((0, 0), HALF_ANGLE, fill=False, color="k",
                            linewidth=1.5, label="FOV 10 deg"))
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.set_xlabel("offset [deg]")
    ax.set_ylabel("offset [deg]  (up = celestial north)")
    ax.legend(loc="lower left", fontsize=8)
    return ax


def main():
    a = parse_args()
    time = frames.times(a.epoch, a.t)[0]
    coeffs = field.load_igrf(float(frames.decimal_year(time)))
    r0, v0 = orbit.elements_to_state(R_EQUATOR_KM + a.alt, 0.0, a.inc,
                                     a.raan, 0.0, 0.0)
    r, _ = orbit.propagate(r0, v0, a.t)
    n = pointing.sky_target(a.target)
    ax = fov_view(r[0], time, n, coeffs, a.extent, a.lmax)

    r_ecef = frames.eci_to_ecef(r, time)
    lat, lon, rad = frames.spherical(r_ecef)
    mlat = field.magnetic_latitude(r_ecef, coeffs)[0]
    sun = frames.sun_vector(time)
    ax.set_title(
        f"{a.target}  {a.epoch[:10]} +{a.t:.0f} s  lat {lat[0]:.0f} "
        f"lon {lon[0]:.0f}  maglat {mlat:.0f}  "
        f"Rc {field.cutoff_rigidity(mlat, rad[0]):.1f} GV  "
        f"limb {geometry.limb_angle(r[0], n)[0]:.0f} deg  "
        f"umbra {bool(geometry.in_umbra(r, sun)[0])}", fontsize=9)
    if a.out:
        ax.figure.savefig(a.out, dpi=130, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
