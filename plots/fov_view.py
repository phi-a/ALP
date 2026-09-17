"""Draw what the boresight sees: Earth, Sun, Galaxy, sources, and K."""
import argparse
from datetime import datetime
from math import log10

import matplotlib.pyplot as plt

import darknessalp as d

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
    p.add_argument("--out", default=None, help="png path; show if absent")
    return p.parse_args()


def target_vector(name):
    if name == "gc":
        return d.radec_to_eci(*d.galactic_to_radec(0.0, 0.0))
    if name == "apex":
        return d.radec_to_eci(*d.galactic_to_radec(57.0, 22.0))
    ra, dec = (float(v) for v in name.split(","))
    return d.radec_to_eci(ra, dec)


def main():
    args = parse_args()
    epoch = datetime.fromisoformat(args.epoch)
    jd = d.julian_date(epoch) + args.t / 86400.0
    theta = d.gmst(jd)
    coeffs = d.load_igrf(epoch.year + epoch.timetuple().tm_yday / 365.25)
    r, _ = d.circular_orbit(args.t, args.alt, args.inc, args.raan)
    rad = sum(v * v for v in r) ** 0.5
    n = target_vector(args.target)
    x_hat, y_hat = d.fov_axes(n)

    def offset(v):
        return d.project_to_fov(v, n, x_hat, y_hat)

    fig, ax = plt.subplots(figsize=(7, 7))
    lim = args.extent
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")

    # K map over the extent, dipole field, coarse and fast
    step = lim / 12
    grid = [(-lim + step * i, -lim + step * j)
            for i in range(25) for j in range(25)]
    xs, ys, ks = [], [], []
    for gx, gy in grid:
        v = _direction(gx, gy, n, x_hat, y_hat)
        res = d.los_field_integral(r, v, theta, coeffs, lmax=1,
                                   n_steps=60)
        if not res["occulted"]:
            xs.append(gx)
            ys.append(gy)
            ks.append(res["amplitude_tm"])
    sc = ax.scatter(xs, ys, c=ks, s=90, marker="s", cmap="viridis",
                    alpha=0.6, linewidths=0)
    fig.colorbar(sc, ax=ax, shrink=0.8, label="|A| = B_perp L  [T m]")

    # Earth disk: grid cells whose direction lies within the disk
    from math import asin, degrees
    nadir = tuple(-v / rad for v in r)
    rho = degrees(asin(d.R_EARTH_KM / rad))
    fine = [-lim + 2 * lim * i / 60 for i in range(61)]
    depth = [[d.angular_separation(_direction(gx, gy, n, x_hat, y_hat),
                                   nadir) for gx in fine] for gy in fine]
    ax.contourf(fine, fine, depth, levels=[0.0, rho], colors="steelblue",
                alpha=0.35)
    ax.contour(fine, fine, depth, levels=[rho], colors="steelblue")
    ax.fill([], [], color="steelblue", alpha=0.35, label="Earth")

    # Galactic plane and centre
    plane = [offset(d.radec_to_eci(*d.galactic_to_radec(l, 0.0)))
             for l in range(0, 360, 2)]
    ax.scatter([p[0] for p in plane], [p[1] for p in plane], s=3,
               color="grey", label="Galactic plane")
    gc = offset(d.radec_to_eci(*d.galactic_to_radec(0.0, 0.0)))
    ax.plot(*gc, "k+", markersize=12, label="GC")

    # Sun
    sun = d.sun_direction(jd)
    if d.angular_separation(sun, n) < 90.0:
        ax.plot(*offset(sun), "o", color="orange", markersize=12,
                label="Sun")

    # bright sources
    for name, ra, dec, mcrab in d.bright_sources():
        v = d.radec_to_eci(ra, dec)
        if d.angular_separation(v, n) < lim * 1.4:
            px, py = offset(v)
            ax.plot(px, py, "r.", markersize=4 + 3 * log10(mcrab))
            ax.annotate(name, (px, py), fontsize=7, xytext=(3, 3),
                        textcoords="offset points")

    # field of view
    ax.add_patch(plt.Circle((0, 0), HALF_ANGLE, fill=False, color="k",
                            linewidth=1.5, label="FOV 10 deg"))

    r_ecef = d.eci_to_ecef(r, theta)
    lat, lon, _ = d.ecef_to_spherical(r_ecef)
    mlat = d.magnetic_latitude(r_ecef, coeffs)
    ax.set_title(
        f"{args.target}  {epoch.date()} +{args.t:.0f} s  "
        f"lat {lat:.0f} lon {lon:.0f}  maglat {mlat:.0f}  "
        f"Rc {d.cutoff_rigidity(mlat, rad):.1f} GV  "
        f"limb {d.earth_limb_angle(r, n):.0f} deg  "
        f"umbra {d.in_umbra(r, sun)}", fontsize=9)
    ax.set_xlabel("offset [deg]")
    ax.set_ylabel("offset [deg]  (up = celestial north)")
    ax.legend(loc="lower left", fontsize=8)
    if args.out:
        fig.savefig(args.out, dpi=130, bbox_inches="tight")
    else:
        plt.show()


def _direction(x_deg, y_deg, n, x_hat, y_hat):
    """Unit vector at angular offsets (x, y) from the boresight."""
    from math import cos, hypot, radians, sin
    theta = radians(hypot(x_deg, y_deg))
    if theta == 0.0:
        return n
    cx, cy = x_deg / hypot(x_deg, y_deg), y_deg / hypot(x_deg, y_deg)
    return tuple(cos(theta) * n[i] + sin(theta) * (cx * x_hat[i]
                                                   + cy * y_hat[i])
                 for i in range(3))


if __name__ == "__main__":
    main()
