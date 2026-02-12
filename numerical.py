import numpy as np

# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def station_distance_matrix(
    latitudes: np.ndarray, longitudes: np.ndarray
) -> np.ndarray:
    """
    Berechnet eine paarweise Distanzmatrix zwischen Stationen.

    Parameter:
    latitudes  Array mit Breitengraden
    longitudes  Array mit Längengraden

    Rückgabe:
        n x n Distanzmatrix (euklidische Distanz)
    """

    # Paarweise Differenzen der Breitengrade
    lat_diff = latitudes[:, np.newaxis] - latitudes[np.newaxis, :]

    # Paarweise Differenzen der Längengrade
    lon_diff = longitudes[:, np.newaxis] - longitudes[np.newaxis, :]

    # Euklidische Distanz
    distance_matrix = np.sqrt(lat_diff**2 + lon_diff**2)

    return distance_matrix


# ---------------------------------------------------------------------------
# Trip statistics
# ---------------------------------------------------------------------------

def trip_duration_stats(durations: np.ndarray) -> dict[str, float]:
    """
    Berechnet statistische Kennzahlen für Fahrtdauern.

    Rückgabe:
        Dictionary mit:
            - Mittelwert
            - Median
            - Standardabweichung
            - 25. Perzentil
            - 75. Perzentil
            - 90. Perzentil
    """

    return {
        "mean": float(np.mean(durations)),
        "median": float(np.median(durations)),
        "std": float(np.std(durations)),
        "p25": float(np.percentile(durations, 25)),
        "p75": float(np.percentile(durations, 75)),
        "p90": float(np.percentile(durations, 90)),
    }


# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    """
    Erkennt Ausreißer mithilfe der Z-Score-Methode.

    Ein Wert gilt als Ausreißer, wenn:
        |z| > threshold

    Standardmäßig: threshold = 3.0
    """

    mean = np.mean(values)
    std = np.std(values)

    # Falls keine Varianz vorhanden ist
    if std == 0:
        return np.zeros_like(values, dtype=bool)

    z_scores = (values - mean) / std

    return np.abs(z_scores) > threshold


# ---------------------------------------------------------------------------
# Vectorized fare calculation
# ---------------------------------------------------------------------------

def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    """
    Vollständig vektorisierte Preisberechnung.

    Formel:
        Preis = Grundgebühr + (Preis/Minute * Dauer)
                + (Preis/km * Distanz)
    """

    fares = unlock_fee + per_minute * durations + per_km * distances
    return fares
