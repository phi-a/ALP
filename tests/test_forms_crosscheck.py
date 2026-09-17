import numpy as np

import forms
from forms.bricks.mag import geomagnetic_field, load_igrf_model

from darknessalp.yamamoto.suzaku import load_suzaku_states


def test_direct_geomagnetic_field_matches_handle_bgcrs():
    state = load_suzaku_states("101002010")[0][0]
    handle = forms.FORMS()
    handle.time.sync(state.mjd2000_tt)
    handle.satellite.set_state([*state.position_gcrf_km, 0.0, 0.0, 0.0])
    handle.derive.advance()
    handle.derive.ensure("magnetic_field")
    bgcrs = handle.get_variable("BGCRS")
    via_handle = np.asarray([bgcrs.x, bgcrs.y, bgcrs.z])

    direct = geomagnetic_field(
        state.position_gcrf_km,
        state.mjd2000_tt,
        loaded_model=load_igrf_model(),
        return_cartesian="gcrs",
    )
    assert np.array_equal(via_handle, direct)
