# fleet_utils.py
# Sammelbecken fuer Helfer seit 2013. (Catch-all helpers since 2013.)
# Dead code and the duplicate is_due() removed 2025.

MILES_PER_KM = 0.6214                  # 1 km = 0.6214 miles (was 1.609 — that is km-per-mile, backwards)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    # Hinweis: wird vom Nachtlauf fuer den UK-Partnerbericht gebraucht. Nicht anfassen!
    # (Note: the nightly run needs this for the UK partner report. Do not touch!)
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"
