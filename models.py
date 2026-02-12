"""
Enthaltene Konzepte:
- Abstrakte Basisklasse (Entity) mit dem abc-Modul
- Vererbung (Bike -> ClassicBike / ElectricBike)
- Vererbung (User -> CasualUser / MemberUser)
- Validierung im Konstruktor
- Properties für kontrollierten Zugriff
- __str__ für benutzerfreundliche Darstellung
- __repr__ für Debugging-Zwecke
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------------
# Abstract Base Class
# ---------------------------------------------------------------------------

class Entity(ABC):
    """
    Abstrakte Basisklasse für alle Domänenobjekte.

    Jede Entität besitzt:
    - eine eindeutige ID
    - ein Erstellungsdatum
    - abstrakte Methoden für __str__ und __repr__
    """

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        # Validierung der ID
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")

        self._id = id
        # Falls kein Datum übergeben wird, wird das aktuelle Datum gesetzt
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        """Gibt die ID der Entität zurück (nur lesbar)."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Gibt das Erstellungsdatum zurück."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Benutzerfreundliche Darstellung."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Technische Darstellung für Debugging."""
        ...


# ---------------------------------------------------------------------------
# Bike hierarchy
# ---------------------------------------------------------------------------

class Bike(Entity):
    """
    Basisklasse für alle Fahrradtypen.

    Attribute:
    - bike_type (classic oder electric)
    - status (available, in_use, maintenance)
    """

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(self, bike_id: str, bike_type: str, status: str = "available") -> None:
        super().__init__(id=bike_id)

        # Validierung des Fahrradtyps
        if bike_type not in ("classic", "electric"):
            raise ValueError("bike_type must be 'classic' or 'electric'")

        # Validierung des Status
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid bike status")

        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        """Gibt den Fahrradtyp zurück."""
        return self._bike_type

    @property
    def status(self) -> str:
        """Gibt den aktuellen Status zurück."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Erlaubt kontrollierte Änderung des Status."""
        if value not in self.VALID_STATUSES:
            raise ValueError("Invalid bike status")
        self._status = value

    def __str__(self) -> str:
        return f"Bike {self.id} ({self.bike_type}) - {self.status}"

    def __repr__(self) -> str:
        return f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, status={self.status!r})"


class ClassicBike(Bike):
    """
    Repräsentiert ein klassisches Fahrrad mit Gangschaltung.
    """

    def __init__(self, bike_id: str, gear_count: int = 7, status: str = "available") -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)

        # Validierung der Ganganzahl
        if gear_count <= 0:
            raise ValueError("gear_count must be positive")

        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        """Gibt die Anzahl der Gänge zurück."""
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike {self.id} - {self.gear_count} gears"

    def __repr__(self) -> str:
        return f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, status={self.status!r})"


class ElectricBike(Bike):
    """
    Repräsentiert ein elektrisches Fahrrad mit Batterie.
    """

    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:

        super().__init__(bike_id=bike_id, bike_type="electric", status=status)

        # Batterielevel muss zwischen 0 und 100 liegen
        if not (0 <= battery_level <= 100):
            raise ValueError("battery_level must be between 0 and 100")

        # Reichweite muss positiv sein
        if max_range_km <= 0:
            raise ValueError("max_range_km must be positive")

        self._battery_level = battery_level
        self._max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        """Gibt den aktuellen Batteriestand zurück."""
        return self._battery_level

    @property
    def max_range_km(self) -> float:
        """Gibt die maximale Reichweite zurück."""
        return self._max_range_km

    def __str__(self) -> str:
        return f"ElectricBike {self.id} - Battery {self.battery_level}%"

    def __repr__(self) -> str:
        return (
            f"ElectricBike(bike_id={self.id!r}, "
            f"battery_level={self.battery_level}, "
            f"max_range_km={self.max_range_km}, "
            f"status={self.status!r})"
        )


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class Station(Entity):
    """
    Repräsentiert eine Fahrradstation mit Standort und Kapazität.
    """

    def __init__(
        self,
        station_id: str,
        name: str,
        capacity: int,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(id=station_id)

        # Validierung der Kapazität
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        # Validierung der Koordinaten
        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")

        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")

        self._name = name
        self._capacity = capacity
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def __str__(self) -> str:
        return f"Station {self.id} - {self.name}"

    def __repr__(self) -> str:
        return (
            f"Station(station_id={self.id!r}, name={self.name!r}, "
            f"capacity={self.capacity}, latitude={self.latitude}, "
            f"longitude={self.longitude})"
        )


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User(Entity):
    """
    Basisklasse für alle Benutzertypen.
    """

    def __init__(self, user_id: str, name: str, email: str, user_type: str) -> None:
        super().__init__(id=user_id)

        # Einfache Validierung der E-Mail
        if "@" not in email:
            raise ValueError("Invalid email format")

        if user_type not in ("casual", "member"):
            raise ValueError("user_type must be 'casual' or 'member'")

        self._name = name
        self._email = email
        self._user_type = user_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_type(self) -> str:
        return self._user_type

    def __str__(self) -> str:
        return f"User {self.id} ({self.user_type})"

    def __repr__(self) -> str:
        return f"User(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, user_type={self.user_type!r})"


class CasualUser(User):
    """
    Repräsentiert einen Gelegenheitsnutzer mit Tagespässen.
    """

    def __init__(self, user_id: str, name: str, email: str, day_pass_count: int = 0) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="casual")

        if day_pass_count < 0:
            raise ValueError("day_pass_count cannot be negative")

        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        return self._day_pass_count

    def __str__(self) -> str:
        return f"CasualUser {self.id} - Passes: {self.day_pass_count}"

    def __repr__(self) -> str:
        return f"CasualUser(user_id={self.id!r}, day_pass_count={self.day_pass_count})"


class MemberUser(User):
    """
    Repräsentiert einen registrierten Nutzer mit Mitgliedschaft.
    """

    VALID_TIERS = {"basic", "premium"}

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime,
        membership_end: datetime,
        tier: str = "basic",
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="member")

        if membership_end <= membership_start:
            raise ValueError("membership_end must be after membership_start")

        if tier not in self.VALID_TIERS:
            raise ValueError("tier must be 'basic' or 'premium'")

        self._membership_start = membership_start
        self._membership_end = membership_end
        self._tier = tier

    @property
    def tier(self) -> str:
        return self._tier

    def __str__(self) -> str:
        return f"MemberUser {self.id} - Tier: {self.tier}"

    def __repr__(self) -> str:
        return f"MemberUser(user_id={self.id!r}, tier={self.tier!r})"


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class Trip:
    """
    Repräsentiert eine einzelne Fahrt im System.
    """

    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:

        if distance_km < 0:
            raise ValueError("distance_km cannot be negative")

        if end_time < start_time:
            raise ValueError("end_time cannot be before start_time")

        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def duration_minutes(self) -> float:
        """Berechnet die Dauer der Fahrt in Minuten."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60

    def __str__(self) -> str:
        return f"Trip {self.trip_id} - {self.distance_km} km"

    def __repr__(self) -> str:
        return f"Trip(trip_id={self.trip_id!r}, distance_km={self.distance_km})"


# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class MaintenanceRecord:
    """
    Repräsentiert einen Wartungseintrag für ein Fahrrad.
    """

    VALID_TYPES = {
        "tire_repair",
        "brake_adjustment",
        "battery_replacement",
        "chain_lubrication",
        "general_inspection",
    }

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:

        if cost < 0:
            raise ValueError("cost cannot be negative")

        if maintenance_type not in self.VALID_TYPES:
            raise ValueError("Invalid maintenance type")

        self.record_id = record_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    def __str__(self) -> str:
        return f"MaintenanceRecord {self.record_id} - {self.maintenance_type}"

    def __repr__(self) -> str:
        return f"MaintenanceRecord(record_id={self.record_id!r}, cost={self.cost})"
