"""
Dieses Modul enthält Hilfsfunktionen,
die im gesamten Projekt wiederverwendet werden.

Ziele:
- Zentrale Validierung von Eingabewerten
- Einheitliches Parsing von Datum/Zeit
- Formatierungsfunktionen
- Vermeidung von Code-Duplikation (DRY-Prinzip)
"""

import re
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Standardformate für Datum und Zeit
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Erlaubte Werte für verschiedene Kategorien
VALID_BIKE_TYPES = {"classic", "electric"}
VALID_USER_TYPES = {"casual", "member"}
VALID_TRIP_STATUSES = {"completed", "cancelled"}
VALID_MAINTENANCE_TYPES = {
    "tire_repair",
    "brake_adjustment",
    "battery_replacement",
    "chain_lubrication",
    "general_inspection",
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_positive(value: float, name: str = "value") -> float:
    """
    Stellt sicher, dass ein Wert strikt positiv ist (> 0).
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")

    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")

    return value


def validate_non_negative(value: float, name: str = "value") -> float:
    """
    Stellt sicher, dass ein Wert nicht negativ ist (>= 0).
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")

    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")

    return value


def validate_email(email: str) -> str:
    """
    Einfache Validierung einer E-Mail-Adresse
    mithilfe eines regulären Ausdrucks (Regex).
    """
    if not isinstance(email, str):
        raise TypeError("Email must be a string")

    # Einfaches Regex-Muster für E-Mail-Validierung
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        raise ValueError(f"Invalid email: {email!r}")

    return email


def validate_in(value: Any, allowed: set, name: str = "value") -> Any:
    """
    Prüft, ob ein Wert in einer erlaubten Menge enthalten ist.
    """
    if value not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")

    return value


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_datetime(text: str) -> datetime:
    """
    Konvertiert einen String im Format YYYY-MM-DD HH:MM:SS
    in ein datetime-Objekt.
    """
    if not isinstance(text, str):
        raise TypeError("Datetime input must be string")

    try:
        return datetime.strptime(text.strip(), DATETIME_FORMAT)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {text!r}") from e


def parse_date(text: str) -> datetime:
    """
    Konvertiert einen String im Format YYYY-MM-DD
    in ein datetime-Objekt.
    """
    if not isinstance(text, str):
        raise TypeError("Date input must be string")

    try:
        return datetime.strptime(text.strip(), DATE_FORMAT)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {text!r}") from e


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_duration(minutes: float) -> str:
    """
    Formatiert eine Dauer in Minuten als String im Format 'Xh Ym'.
    """
    validate_non_negative(minutes, "minutes")

    h = int(minutes // 60)
    m = int(minutes % 60)

    return f"{h}h {m}m"


def fmt_currency(amount: float) -> str:
    """
    Formatiert einen Geldbetrag mit zwei Nachkommastellen.
    """
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be numeric")

    return f"€{amount:.2f}"
