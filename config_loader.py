# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Read settings.cfg and return a dict of recognised key/value pairs."""
    if path is None:
        path = SETTINGS_FILE
    settings = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)   # limit to 1 split so values may contain "="
            key = key.strip()
            value = value.strip()
            # Unbekannte Schluessel werden stillschweigend ignoriert. Ein Tippfehler im cfg
            # faellt also NIE auf. (Unknown keys are silently dropped, so a typo never surfaces.)
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return the integer value for key, or fallback if missing or non-numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return the string value for key, or fallback if missing.

    (A convenience wrapper around dict.get — kept for backward compatibility.)
    """
    return settings.get(key, fallback)
