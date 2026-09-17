import numpy as np

def cilm(filename, year):
    """
    Load IGRF13 spherical harmonic coefficients and return Schmidt-normalized cilm array at given year.

    Parameters:
        filename : str
            Path to IGRF13 .dat file.
        year : float
            Decimal year, e.g., 2020.0 or 2023.5

    Returns:
        cilm : np.ndarray of shape (2, lmax+1, lmax+1)
    """
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    header = lines[1].split()
    epochs = []
    raw_epochs = []
    for e in header[3:]:
        try:
            epochs.append(float(e))
            raw_epochs.append(e)
        except ValueError:
            raw_epochs.append(e)

    g_data = {}
    h_data = {}

    for line in lines[2:]:
        parts = line.split()
        typ, n, m = parts[0], int(parts[1]), int(parts[2])
        values = list(map(float, parts[3:]))
        key = (n, m)
        if typ == "g":
            g_data[key] = values
        elif typ == "h":
            h_data[key] = values

    if year < epochs[0] or year > 2025.0:
        raise ValueError(f"Year {year} out of range ({epochs[0]} to 2025.0)")

    if year > epochs[-1]:  # extrapolate using SV
        t0 = epochs[-1]
        f = year - t0
        use_sv = True
        i0 = len(epochs) - 1
    else:
        for i in range(len(epochs) - 1):
            if epochs[i] <= year <= epochs[i + 1]:
                t0, t1 = epochs[i], epochs[i + 1]
                f = (year - t0) / (t1 - t0)
                use_sv = False
                i0, i1 = i, i + 1
                break

    lmax = max(n for (n, _) in g_data.keys())
    cilm = np.zeros((2, lmax + 1, lmax + 1))

    for (n, m) in g_data:
        g0 = g_data[(n, m)][i0]
        h0 = h_data.get((n, m), [0.0] * len(raw_epochs))[i0]

        if use_sv:
            g_sv = g_data[(n, m)][i0 + 1]
            h_sv = h_data.get((n, m), [0.0] * len(raw_epochs))[i0 + 1]
            g = g0 + f * g_sv
            h = h0 + f * h_sv
        else:
            g1 = g_data[(n, m)][i1]
            h1 = h_data.get((n, m), [0.0] * len(raw_epochs))[i1]
            g = (1 - f) * g0 + f * g1
            h = (1 - f) * h0 + f * h1

        cilm[0, n, m] = g * 1e-9  # convert from nT to Tesla
        cilm[1, n, m] = h * 1e-9

    return cilm
