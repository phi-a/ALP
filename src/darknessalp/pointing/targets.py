"""Named sky targets as ECI unit vectors."""
from darknessalp.frames.sky import galactic_vector, radec_vector

GALACTIC = {"gc": (0.0, 0.0), "apex": (57.0, 22.0)}  # apex: ASSUME


def target(name):
    """Return the unit vector of a named target or an 'ra,dec' string."""
    if name in GALACTIC:
        return galactic_vector(*GALACTIC[name])[0]
    ra, dec = (float(v) for v in name.split(","))
    return radec_vector(ra, dec)[0]
