"""Body attitude from a boresight and roll, via scipy Rotation."""
import numpy as np
from scipy.spatial.transform import Rotation

BORESIGHT_BODY = np.array([0.0, 0.0, 1.0])  # ASSUME: aperture along +Z
RADIATOR_BODY = np.array([1.0, 0.0, 0.0])  # ASSUME: radiator normal +X


def look_at(boresight_eci, up_hint=(0.0, 0.0, 1.0), roll_deg=0.0):
    """Return a body->ECI Rotation pointing +Z at boresight, +Y near up."""
    z = np.asarray(boresight_eci, float)
    z = z / np.linalg.norm(z)
    y = np.asarray(up_hint, float) - np.dot(up_hint, z) * z
    y = y / np.linalg.norm(y)
    x = np.cross(y, z)
    body_to_eci = Rotation.from_matrix(np.stack([x, y, z], axis=1))
    return body_to_eci * Rotation.from_euler("z", roll_deg, degrees=True)


def boresight(rotation):
    """Return the ECI boresight of a body->ECI Rotation."""
    return rotation.apply(BORESIGHT_BODY)


def radiator_normal(rotation):
    """Return the ECI radiator normal of a body->ECI Rotation."""
    return rotation.apply(RADIATOR_BODY)
