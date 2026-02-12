"""
Dieses Skript führt die vollständige Analyse-Pipeline aus:
    1. Laden der Daten
    2. Datenprüfung und -bereinigung
    3. Business-Analysen
    4. Numerische Berechnungen (NumPy)
    5. Visualisierungen
    6. Export eines Summary-Reports
"""

import numpy as np

from analyzer import BikeShareSystem
from visualization import (
    plot_trips_per_station,
    plot_monthly_trend,
    plot_duration_histogram,
    plot_duration_by_user_type,
)
from numerical import (
    station_distance_matrix,
    trip_duration_stats,
    detect_outliers_zscore,
)


def main() -> None:
    """Startet die komplette Analyse-Pipeline."""

    system = BikeShareSystem()

    # ------------------------------------------------------------
    # 1. Load raw data
    # ------------------------------------------------------------
    print("\n>>> Step 1 — Loading data")
    system.load_data()

    # ------------------------------------------------------------
    # 2. Inspect & clean data
    # ------------------------------------------------------------
    print("\n>>> Step 2 — Inspecting data")
    system.inspect_data()

    print("\n>>> Cleaning data")
    system.clean_data()

    # ------------------------------------------------------------
    # 3. Business Analytics
    # ------------------------------------------------------------
    print("\n>>> Step 3 — Running analytics")

    summary = system.total_trips_summary()
    print(f"Total trips      : {summary['total_trips']}")
    print(f"Total distance   : {summary['total_distance_km']} km")
    print(f"Average duration : {summary['avg_duration_min']} min")

    print("\nTop 5 Start Stations:")
    print(system.top_start_stations(5))

    print("\nPeak Usage Hours:")
    print(system.peak_usage_hours())

    print("\nAverage Distance by User Type:")
    print(system.avg_distance_by_user_type())

    print("\nTop 5 Routes:")
    print(system.top_routes(5))

    # ------------------------------------------------------------
    # 4. Numerical Computations (NumPy)
    # ------------------------------------------------------------
    print("\n>>> Step 4 — Running numerical computations")

    # ---- Statistik zu Fahrtdauern ----
    durations = system.trips["duration_minutes"].to_numpy()
    stats = trip_duration_stats(durations)

    print("\nTrip Duration Statistics:")
    for k, v in stats.items():
        print(f"{k}: {v:.2f}")

    # ---- Ausreißererkennung ----
    outliers = detect_outliers_zscore(durations)
    print(f"\nDetected {np.sum(outliers)} duration outliers")

    # ---- Distanzmatrix der Stationen ----
    latitudes = system.stations["latitude"].to_numpy()
    longitudes = system.stations["longitude"].to_numpy()

    distance_matrix = station_distance_matrix(latitudes, longitudes)
    print(f"\nDistance matrix shape: {distance_matrix.shape}")

    # ------------------------------------------------------------
    # 5. Visualizations
    # ------------------------------------------------------------
    print("\n>>> Step 5 — Generating visualizations")

    plot_trips_per_station(system.trips, system.stations)
    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # ------------------------------------------------------------
    # 6. Export summary report
    # ------------------------------------------------------------
    print("\n>>> Step 6 — Generating summary report")
    system.generate_summary_report()

    print("\n>>> Done! Check the output/ folder.")


if __name__ == "__main__":
    main()
