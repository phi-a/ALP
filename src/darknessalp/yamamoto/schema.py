"""Typed records for archived and simulated mission states."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MissionState:
    """One time-centered spacecraft observation sample.

    Cartesian positions are in km. The boresight is a unit vector in GCRF.
    """

    mission: str
    obsid: str
    sample_id: int
    gti_index: int
    mission_time_tt_s: float
    utc: str
    mjd_tt: float
    mjd2000_tt: float
    exposure_s: float
    latitude_deg: float
    longitude_deg: float
    altitude_km: float
    r_itrf_x_km: float
    r_itrf_y_km: float
    r_itrf_z_km: float
    r_gcrf_x_km: float
    r_gcrf_y_km: float
    r_gcrf_z_km: float
    boresight_gcrf_x: float
    boresight_gcrf_y: float
    boresight_gcrf_z: float
    foc_ra_deg: float
    foc_dec_deg: float
    foc_roll_deg: float
    earth_limb_elevation_deg: float
    day_earth_limb_elevation_deg: float
    night_earth_limb_elevation_deg: float
    cor2_gv: float
    saa: int
    pointing_separation_deg: float
    ehk_nearest_offset_s: float
    in_cleaned_gti: bool
    data_valid: bool
    quality_flags: str

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def position_gcrf_km(self) -> tuple[float, float, float]:
        return (self.r_gcrf_x_km, self.r_gcrf_y_km, self.r_gcrf_z_km)

    @property
    def boresight_gcrf(self) -> tuple[float, float, float]:
        return (
            self.boresight_gcrf_x,
            self.boresight_gcrf_y,
            self.boresight_gcrf_z,
        )


@dataclass(frozen=True)
class SuzakuObservation:
    """One provenance-locked member of the Yamamoto geometry cohort."""

    obsid: str
    field: str
    expected_ra_deg: float
    expected_dec_deg: float
    primary: bool = True
    provenance: str = "Yamamoto 2018 thesis, Appendix A, Table A.1"
    inclusion_note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ProductStatus:
    """Readiness of EHK plus the standard cleaned-GTI product set."""

    obsid: str
    field: str
    primary: bool
    status: str
    xis: int | None
    ehk_path: str | None
    event_paths: tuple[str, ...]
    observed_ra_deg: float | None
    observed_dec_deg: float | None
    target_separation_deg: float | None
    rejection_reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


STATE_UNITS = {
    "mission_time_tt_s": "s since Suzaku MJDREF",
    "mjd_tt": "day",
    "mjd2000_tt": "day since J2000 TT",
    "exposure_s": "s",
    "latitude_deg": "deg geodetic",
    "longitude_deg": "deg east geodetic",
    "altitude_km": "km above WGS84 ellipsoid",
    "r_itrf_x_km": "km",
    "r_itrf_y_km": "km",
    "r_itrf_z_km": "km",
    "r_gcrf_x_km": "km",
    "r_gcrf_y_km": "km",
    "r_gcrf_z_km": "km",
    "boresight_gcrf_x": "dimensionless",
    "boresight_gcrf_y": "dimensionless",
    "boresight_gcrf_z": "dimensionless",
    "foc_ra_deg": "deg ICRS/GCRF",
    "foc_dec_deg": "deg ICRS/GCRF",
    "foc_roll_deg": "deg",
    "earth_limb_elevation_deg": "deg",
    "day_earth_limb_elevation_deg": "deg",
    "night_earth_limb_elevation_deg": "deg",
    "cor2_gv": "GV",
    "pointing_separation_deg": "deg",
    "ehk_nearest_offset_s": "s",
}
