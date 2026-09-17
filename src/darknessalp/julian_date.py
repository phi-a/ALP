def julian_date(t):
    """Return the Julian date of a naive UTC datetime."""
    year, month = t.year, t.month
    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + a // 4
    day = t.day + (t.hour + (t.minute + t.second / 60) / 60) / 24
    return (int(365.25 * (year + 4716)) + int(30.6001 * (month + 1))
            + day + b - 1524.5)
