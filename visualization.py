"""
Dieses Modul enthält alle grafischen Auswertungen
des CityBike-Projekts.

Alle Diagramme werden automatisch als PNG-Dateien
im output/figures-Verzeichnis gespeichert.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


FIGURES_DIR = Path(__file__).resolve().parent / "output" / "figures"


def _save_figure(fig: plt.Figure, filename: str) -> None:
    """
    Speichert eine Matplotlib-Figur im definierten Ausgabeordner.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")


# ---------------------------------------------------------------------------
# 1. Balkendiagramm — Trips pro Station
# ---------------------------------------------------------------------------

def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    """
    Erstellt ein horizontales Balkendiagramm
    der Top 10 Startstationen.
    """
    counts = (
        trips["start_station_id"]
        .value_counts()
        .head(10)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )

    merged = counts.merge(
        stations[["station_id", "station_name"]],
        on="station_id",
        how="left",
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(merged["station_name"], merged["trip_count"])

    ax.set_title("Top 10 Start Stations by Trip Count")
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")

    ax.invert_yaxis()
    _save_figure(fig, "trips_per_station.png")


# ---------------------------------------------------------------------------
# 2. Liniendiagramm — Monatlicher Trend
# ---------------------------------------------------------------------------

def plot_monthly_trend(trips: pd.DataFrame) -> None:
    """
    Visualisiert die monatliche Entwicklung
    der Fahrtenanzahl.
    """
    df = trips.copy()
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["year_month"] = df["start_time"].dt.to_period("M")

    monthly_counts = df.groupby("year_month").size()

    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_counts.plot(kind="line", marker="o", ax=ax)

    ax.set_title("Monthly Trip Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Trips")
    ax.legend(["Trips"])

    _save_figure(fig, "monthly_trend.png")


# ---------------------------------------------------------------------------
# 3. Histogramm — Dauerverteilung
# ---------------------------------------------------------------------------

def plot_duration_histogram(trips: pd.DataFrame) -> None:
    """
    Zeigt die Verteilung der Fahrtdauer
    als Histogramm.
    """
    durations = trips["duration_minutes"]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(durations, bins=30)

    ax.set_title("Trip Duration Distribution")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Frequency")

    _save_figure(fig, "duration_histogram.png")


# ---------------------------------------------------------------------------
# 4. Boxplot — Dauer nach Nutzertyp
# ---------------------------------------------------------------------------

def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    """
    Vergleicht die Fahrtdauer zwischen
    unterschiedlichen Nutzertypen.
    """
    grouped = trips.groupby("user_type")["duration_minutes"]

    data = [group for _, group in grouped]
    labels = [name for name, _ in grouped]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(data, labels=labels)

    ax.set_title("Trip Duration by User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Duration (minutes)")

    _save_figure(fig, "duration_by_user_type.png")
