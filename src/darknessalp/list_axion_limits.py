import json
from urllib.request import urlopen


AXION_LIMITS_TREE = (
    "https://api.github.com/repos/cajohare/AxionLimits/"
    "git/trees/master?recursive=1"
)


def list_axion_limits(coupling="AxionPhoton"):
    """Return file names available under limit_data/<coupling>/."""
    with urlopen(AXION_LIMITS_TREE, timeout=60) as response:
        tree = json.load(response)["tree"]

    prefix = f"limit_data/{coupling}/"
    return sorted(
        item["path"][len(prefix):]
        for item in tree
        if item["path"].startswith(prefix) and item["path"].endswith(".txt")
    )
