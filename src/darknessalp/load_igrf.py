from pathlib import Path


IGRF_PATH = (Path(__file__).resolve().parents[2] / "data" / "bfield"
             / "igrf14coeffs.txt")


def load_igrf(year, path=IGRF_PATH):
    """Return {(n, m): (g, h)} in nT at a decimal year."""
    rows = [line.split() for line in Path(path).read_text().splitlines()
            if line and not line.startswith("#")]
    epochs = [float(e) for e in rows[1][3:-1]]
    if not epochs[0] <= year <= epochs[-1] + 5:
        raise ValueError("year outside the model range")

    # last column is secular variation for the five years past the end
    k = max(i for i, e in enumerate(epochs) if e <= year)
    last = k == len(epochs) - 1
    f = year - epochs[k] if last else (
        (year - epochs[k]) / (epochs[k + 1] - epochs[k]))

    coeffs = {}
    for row in rows[2:]:
        kind, n, m = row[0], int(row[1]), int(row[2])
        values = [float(v) for v in row[3:]]
        value = values[k] + f * (
            values[-1] if last else values[k + 1] - values[k])
        g, h = coeffs.get((n, m), (0.0, 0.0))
        coeffs[(n, m)] = (value, h) if kind == "g" else (g, value)
    return coeffs
