# (name, ra_deg, dec_deg, mCrab 2-10 keV) -- ASSUME: typical, replace
# with MAXI/GSC catalogue values before quoting a contamination number
SOURCES = [
    ("Sco X-1", 244.979, -15.640, 14000),
    ("Crab", 83.633, 22.014, 1000),
    ("GX 5-1", 270.284, -25.079, 800),
    ("GX 17+2", 274.006, -14.036, 600),
    ("Cyg X-1", 299.590, 35.202, 500),
    ("GX 349+2", 256.435, -36.423, 500),
    ("GRS 1915+105", 288.798, 10.946, 500),
    ("Cyg X-2", 326.172, 38.322, 400),
    ("GX 9+1", 270.385, -20.529, 400),
    ("GX 3+1", 266.983, -26.564, 300),
    ("4U 1820-30", 275.919, -30.361, 300),
    ("Vela X-1", 135.529, -40.555, 300),
    ("Cyg X-3", 308.107, 40.958, 200),
    ("GX 13+1", 273.631, -17.157, 200),
    ("Ser X-1", 279.990, 5.036, 200),
    ("Cen X-3", 170.313, -60.623, 200),
    ("4U 1700-37", 255.987, -37.844, 200),
    ("Her X-1", 254.458, 35.342, 100),
]


def bright_sources(min_mcrab=0):
    """Return (name, ra, dec, mCrab) rows at or above min_mcrab."""
    return [s for s in SOURCES if s[3] >= min_mcrab]
