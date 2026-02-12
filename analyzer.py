"""
Verantwortlichkeiten:
- Laden der Rohdaten
- Dateninspektion und -bereinigung
- Berechnung von Business-Kennzahlen
- Erstellung eines textbasierten Reports

Die Klasse kapselt die gesamte Analyse-Logik
und bildet damit das Kernstück des Projekts.
"""

import pandas as pd
from pathlib import Path


# Verzeichnisse relativ zur Projektstruktur
DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Lädt alle CSV-Dateien in Pandas DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print("Data loaded successfully.")

    # ------------------------------------------------------------------
    # Data inspection
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """
        Gibt grundlegende Informationen zu den Datensätzen aus:
        - Struktur (df.info)
        - Fehlende Werte
        - Erste Zeilen
        """
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            if df is None:
                print(f"{name} not loaded.")
                continue

            print(f"\n{'='*40}")
            print(f"{name}")
            print(f"{'='*40}")
            print(df.info())
            print("\nMissing values:")
            print(df.isnull().sum())
            print("\nFirst 3 rows:")
            print(df.head(3))

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """
        Führt Datenbereinigung durch:

        - Entfernt Duplikate
        - Konvertiert Datums- und Zahlenformate
        - Behandelt fehlende Werte
        - Entfernt inkonsistente Einträge
        - Standardisiert kategoriale Variablen
        - Exportiert bereinigte Datensätze
        """

        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # Duplikate entfernen
        self.trips.drop_duplicates(subset=["trip_id"], inplace=True)
        self.maintenance.drop_duplicates(subset=["record_id"], inplace=True)

        # Datumsfelder parsen
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"], errors="coerce")
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"], errors="coerce")
        self.maintenance["date"] = pd.to_datetime(self.maintenance["date"], errors="coerce")

        # Numerische Felder konvertieren
        self.trips["duration_minutes"] = pd.to_numeric(
            self.trips["duration_minutes"], errors="coerce"
        )
        self.trips["distance_km"] = pd.to_numeric(
            self.trips["distance_km"], errors="coerce"
        )
        self.maintenance["cost"] = pd.to_numeric(
            self.maintenance["cost"], errors="coerce"
        )

        # Fehlende Werte behandeln
        # Strategie:
        # - Kritische Trip-Daten werden entfernt
        # - Fehlende Wartungskosten werden mit 0 ersetzt
        self.trips.dropna(
            subset=["start_time", "end_time", "duration_minutes", "distance_km"],
            inplace=True,
        )

        self.maintenance["cost"] = self.maintenance["cost"].fillna(0)

        # Logische Konsistenz prüfen
        self.trips = self.trips[
            self.trips["end_time"] >= self.trips["start_time"]
        ]

        # Kategoriale Werte vereinheitlichen
        self.trips["status"] = (
            self.trips["status"].astype(str).str.strip().str.lower()
        )
        self.trips["user_type"] = (
            self.trips["user_type"].astype(str).str.strip().str.lower()
        )
        self.trips["bike_type"] = (
            self.trips["bike_type"].astype(str).str.strip().str.lower()
        )

        # Bereinigte Daten exportieren
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        """Berechnet zentrale Gesamtkennzahlen."""
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Ermittelt die n häufigsten Startstationen."""
        counts = (
            self.trips["start_station_id"]
            .value_counts()
            .head(n)
            .reset_index()
        )
        counts.columns = ["station_id", "trip_count"]

        return counts.merge(
            self.stations[["station_id", "station_name"]],
            on="station_id",
            how="left"
        )[["station_id", "station_name", "trip_count"]]

    def peak_usage_hours(self) -> pd.Series:
        """Ermittelt die Auslastung nach Stunden."""
        return (
            self.trips["start_time"]
            .dt.hour
            .value_counts()
            .sort_index()
        )

    def avg_distance_by_user_type(self) -> pd.Series:
        """Durchschnittliche Distanz pro Nutzertyp."""
        return (
            self.trips.groupby("user_type")["distance_km"]
            .mean()
            .round(2)
        )

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Gesamte Wartungskosten nach Fahrradtyp."""
        return (
            self.maintenance.groupby("bike_type")["cost"]
            .sum()
            .round(2)
        )

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Häufigste Routen (Start- und Zielstation)."""
        return (
            self.trips.groupby(
                ["start_station_id", "end_station_id"]
            )
            .size()
            .sort_values(ascending=False)
            .head(n)
            .reset_index(name="trip_count")
        )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """
        Erstellt einen strukturierten Textbericht
        mit zentralen Analyseergebnissen.
        """

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines = []
        lines.append("=" * 60)
        lines.append("CityBike — Summary Report")
        lines.append("=" * 60)

        summary = self.total_trips_summary()

        lines.append("\n--- Overall Summary ---")
        lines.append(f"Total trips: {summary['total_trips']}")
        lines.append(f"Total distance: {summary['total_distance_km']} km")
        lines.append(f"Average duration: {summary['avg_duration_min']} min")

        report_text = "\n".join(lines)
        report_path.write_text(report_text)

        print(f"Report saved to {report_path}")
