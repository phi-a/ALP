"""A mode is a primary target for the boresight and a roll rule."""
import numpy as np

from darknessalp.kinematics.attitude import look_at
from darknessalp.pointing.targets import target_direction


def mode(primary, roll="anti_earth"):
    """Return a mode dict; roll: anti_earth, anti_sun, or a target spec."""
    return {"primary": primary, "roll": roll}


def desired_attitude(m, time, r_eci, v_eci, b_eci=None):
    """Return body->ECI Rotation(s) realising a mode at each sample."""
    z = target_direction(m["primary"], time, r_eci, v_eci, b_eci)
    spec = {"anti_earth": "zenith", "anti_sun": "anti_sun"}.get(
        m["roll"], m["roll"])
    hint = target_direction(spec, time, r_eci, v_eci, b_eci)
    return look_at(z, hint)


def attitudes(modes, mode_index, time, r_eci, v_eci, b_eci=None):
    """Return Rotation(s) following mode_index (N,) into a list of modes."""
    quats = np.empty((len(mode_index), 4))
    for i, m in enumerate(modes):
        pick = mode_index == i
        if pick.any():
            rot = desired_attitude(m, time[pick], r_eci[pick], v_eci[pick],
                                   None if b_eci is None else b_eci[pick])
            quats[pick] = rot.as_quat()
    from scipy.spatial.transform import Rotation
    return Rotation.from_quat(quats)
