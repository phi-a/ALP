"""Body attitude from a boresight and a roll hint, via scipy Rotation."""
import numpy as np
from scipy.spatial.transform import Rotation

BORESIGHT_BODY = np.array([0.0, 0.0, 1.0])  # ASSUME: aperture along +Z
RADIATOR_BODY = np.array([0.0, 1.0, 0.0])   # ASSUME: radiator normal +Y


def _unit(v):
    v = np.atleast_2d(np.asarray(v, float))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def look_at(boresight_eci, hint=(0.0, 0.0, 1.0)):
    """Return body->ECI Rotation(s): +Z on the boresight, +Y toward hint."""
    z = _unit(boresight_eci)
    hint = np.broadcast_to(np.asarray(hint, float), z.shape)
    y = hint - np.sum(hint * z, axis=1, keepdims=True) * z
    bad = np.linalg.norm(y, axis=1) < 1e-9        # hint along boresight
    y[bad] = np.cross(z[bad], [1.0, 0.0, 0.0])
    y = _unit(y)
    x = np.cross(y, z)
    return Rotation.from_matrix(np.stack([x, y, z], axis=2))


def boresight(rotation):
    """Return (N, 3) ECI boresight(s) of body->ECI Rotation(s)."""
    return np.atleast_2d(rotation.apply(BORESIGHT_BODY))


def radiator_normal(rotation):
    """Return (N, 3) ECI radiator normal(s) of body->ECI Rotation(s)."""
    return np.atleast_2d(rotation.apply(RADIATOR_BODY))
