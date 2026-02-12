"""
Ziel:
Objekte (Bike, User usw.) werden nicht direkt im restlichen Code erzeugt,
sondern über Factory-Funktionen.

Vorteile:
- Kapselung der Objekt-Erzeugung
- Zentrale Stelle für Logik zur Typ-Auswahl
- Bessere Erweiterbarkeit
- Reduzierte Abhängigkeiten vom konkreten Klassentyp
"""

from datetime import datetime
from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
)


# ---------------------------------------------------------------------------
# Bike Factory
# ---------------------------------------------------------------------------

def create_bike(data: dict) -> Bike:
    """
    Erstellt ein Bike-Objekt (ClassicBike oder ElectricBike)
    basierend auf einem Dictionary (z.B. aus einer CSV-Zeile).

    Parameter:
        data: Dictionary mit Bike-Informationen

    Rückgabe:
        Ein Objekt vom Typ Bike (konkret: ClassicBike oder ElectricBike)
    """

    # Fahrradtyp wird normalisiert (Leerzeichen entfernen + lowercase)
    bike_type = data.get("bike_type", "").strip().lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            # Falls kein Wert vorhanden ist, wird Standard 7 verwendet
            gear_count=int(data.get("gear_count", 7)),
        )

    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            # Standardwerte, falls keine Daten vorhanden sind
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )

    else:
        # Fehlerbehandlung bei unbekanntem Typ
        raise ValueError(f"Unknown bike_type: {bike_type!r}")


# ---------------------------------------------------------------------------
# User Factory
# ---------------------------------------------------------------------------

def create_user(data: dict) -> User:
    """
    Erstellt ein User-Objekt (CasualUser oder MemberUser)
    aus einem Dictionary.

    Parameter:
        data: Dictionary mit Benutzerinformationen

    Rückgabe:
        Ein Objekt vom Typ CasualUser oder MemberUser
    """

    # Benutzertyp normalisieren
    user_type = data.get("user_type", "").strip().lower()

    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            # Falls kein Name angegeben ist → Default-Wert
            name=data.get("name", "Unknown"),
            # Falls keine E-Mail vorhanden → Default
            email=data.get("email", "unknown@email.com"),
            day_pass_count=int(data.get("day_pass_count", 0)),
        )

    elif user_type == "member":

        # Mitgliedschaftsdaten sicher parsen
        start_str = data.get("membership_start")
        end_str = data.get("membership_end")

        # Falls Datum vorhanden → ISO-Format konvertieren
        # Falls nicht → aktuelles Datum verwenden
        membership_start = (
            datetime.fromisoformat(start_str)
            if start_str
            else datetime.now()
        )

        # Falls kein Enddatum vorhanden → +1 Jahr Laufzeit
        membership_end = (
            datetime.fromisoformat(end_str)
            if end_str
            else membership_start.replace(year=membership_start.year + 1)
        )

        return MemberUser(
            user_id=data["user_id"],
            name=data.get("name", "Unknown"),
            email=data.get("email", "unknown@email.com"),
            membership_start=membership_start,
            membership_end=membership_end,
            tier=data.get("tier", "basic").lower(),
        )

    else:
        # Fehler bei unbekanntem Benutzertyp
        raise ValueError(f"Unknown user_type: {user_type!r}")
