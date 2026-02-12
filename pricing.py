"""
Dieses Modul implementiert das Strategy Pattern zur Berechnung von Fahrpreisen.

Statt feste Preislogik im Trip oder User zu implementieren,
werden unterschiedliche Preisstrategien als austauschbare Klassen definiert.

Vorteile:
- Erweiterbarkeit (Open/Closed Principle)
- Klare Trennung von Geschäftslogik
- Flexible Preisgestaltung je nach Nutzertyp oder Situation
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class PricingStrategy(ABC):
    """
    Abstrakte Strategieklasse zur Preisberechnung.

    Jede konkrete Preisstrategie muss die Methode
    calculate_cost() implementieren.
    """

    @abstractmethod
    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """
        Berechnet die Kosten einer Fahrt in Euro.

        Parameter:
        - duration_minutes: Dauer der Fahrt in Minuten
        - distance_km: Zurückgelegte Strecke in Kilometern
        """
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class CasualPricing(PricingStrategy):
    """
    Preisstrategie für Gelegenheitsnutzer (Casual User).

    Tarif:
        - 1,00 € Startgebühr (Unlock Fee)
        - 0,15 € pro Minute
        - 0,10 € pro Kilometer
    """

    UNLOCK_FEE = 1.00
    PER_MINUTE = 0.15
    PER_KM = 0.10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:

        # Eingabevalidierung
        if duration_minutes < 0 or distance_km < 0:
            raise ValueError("Duration and distance must be non-negative")

        # Berechnung der Gesamtkosten
        cost = (
            self.UNLOCK_FEE
            + self.PER_MINUTE * duration_minutes
            + self.PER_KM * distance_km
        )

        # Rundung auf zwei Nachkommastellen
        return round(cost, 2)


class MemberPricing(PricingStrategy):
    """
    Preisstrategie für Mitglieder (Member User).

    Vorteile für Mitglieder:
        - Keine Startgebühr
        - 0,08 € pro Minute
        - 0,05 € pro Kilometer
    """

    PER_MINUTE = 0.08
    PER_KM = 0.05

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:

        # Eingabevalidierung
        if duration_minutes < 0 or distance_km < 0:
            raise ValueError("Duration and distance must be non-negative")

        # Berechnung der Kosten mit reduziertem Tarif
        cost = (
            self.PER_MINUTE * duration_minutes
            + self.PER_KM * distance_km
        )

        return round(cost, 2)


class PeakHourPricing(PricingStrategy):
    """
    Preisstrategie für Stoßzeiten (Peak Hours).

    Diese Strategie basiert auf CasualPricing,
    wendet jedoch einen Multiplikator von 1.5 an.
    """

    MULTIPLIER = 1.5

    def __init__(self) -> None:
        # Komposition: Wiederverwendung der CasualPricing-Strategie
        self._base_strategy = CasualPricing()

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:

        # Berechnung des Basispreises
        base_cost = self._base_strategy.calculate_cost(
            duration_minutes,
            distance_km,
        )

        # Anwendung des Peak-Multiplikators
        peak_cost = base_cost * self.MULTIPLIER

        return round(peak_cost, 2)
