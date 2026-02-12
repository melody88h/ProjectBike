"""
Dieses Modul enthält eigene Implementierungen von
Sortier- und Suchalgorithmen sowie Performance-Vergleiche.

Ziel:
- Verständnis von Algorithmus-Komplexität (Big-O)
- Vergleich eigener Implementierungen mit Python Built-ins
- Analyse der Laufzeit mit dem Modul timeit
"""

import timeit
from collections.abc import Callable
from typing import Any


# ---------------------------------------------------------------------------
# Sorting — Merge Sort
# ---------------------------------------------------------------------------

def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """
    Implementierung von Merge Sort (Divide-and-Conquer).

    Time  — O(n log n)
    Space — O(n)

    Parameter:
        data: Liste beliebiger Elemente
        key: optionale Schlüssel-Funktion (wie bei sorted())

    Rückgabe:
        Neue sortierte Liste
    """
    if len(data) <= 1:
        return list(data)

    # Liste halbieren
    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)

    return _merge(left, right, key)


def _merge(left: list[Any], right: list[Any], key: Callable) -> list[Any]:
    """
    Hilfsfunktion für Merge Sort:
    Führt zwei sortierte Listen zusammen.
    """
    result = []
    i = j = 0

    # Vergleiche Elemente beider Listen
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Restliche Elemente anhängen
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Sorting — Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """
    Implementierung von Insertion Sort.

    Time  — O(n²) im Worst- und Average-Case
            O(n) im Best-Case (fast sortierte Liste)
    Space — O(n)

    Besonders geeignet für kleine oder fast sortierte Datenmengen.
    """
    arr = list(data)  # Kopie der Eingabeliste erstellen

    for i in range(1, len(arr)):
        current = arr[i]
        current_key = key(current)
        j = i - 1

        # Größere Elemente nach rechts verschieben
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = current

    return arr


# ---------------------------------------------------------------------------
# Searching — Binary Search
# ---------------------------------------------------------------------------

def binary_search(
    sorted_data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    """
    Implementierung der binären Suche.

    Voraussetzung:
        Die Liste muss bereits sortiert sein.

    Time  — O(log n)
    Space — O(1)

    Rückgabe:
        Index des gefundenen Elements oder None
    """
    low, high = 0, len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


# ---------------------------------------------------------------------------
# Searching — Linear Search
# ---------------------------------------------------------------------------

def linear_search(
    data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    """
    Lineare Suche.

    Time  — O(n)
    Space — O(1)

    Durchläuft die Liste sequenziell.
    """
    for i, item in enumerate(data):
        if key(item) == target:
            return i

    return None


# ---------------------------------------------------------------------------
# Benchmarking — Sorting
# ---------------------------------------------------------------------------

def benchmark_sort(
    data: list,
    key: Callable = lambda x: x,
    repeats: int = 5,
) -> dict:
    """
    Vergleicht die Laufzeit von:
        - merge_sort
        - built-in sorted()

    Rückgabe:
        Dictionary mit durchschnittlicher Laufzeit in Millisekunden
    """

    merge_time = timeit.timeit(
        lambda: merge_sort(data, key=key),
        number=repeats,
    )

    builtin_time = timeit.timeit(
        lambda: sorted(data, key=key),
        number=repeats,
    )

    return {
        "merge_sort_ms": round(merge_time / repeats * 1000, 2),
        "builtin_sorted_ms": round(builtin_time / repeats * 1000, 2),
    }


# ---------------------------------------------------------------------------
# Benchmarking — Searching
# ---------------------------------------------------------------------------

def benchmark_search(
    data: list,
    target: Any,
    key: Callable = lambda x: x,
    repeats: int = 5,
) -> dict:
    """
    Vergleicht die Laufzeit von:
        - binary_search
        - linear_search
        - Python built-in 'in' Operator

    Hinweis:
        Für binary_search muss die Liste sortiert sein.
    """

    binary_time = timeit.timeit(
        lambda: binary_search(data, target, key=key),
        number=repeats,
    )

    linear_time = timeit.timeit(
        lambda: linear_search(data, target, key=key),
        number=repeats,
    )

    builtin_time = timeit.timeit(
        lambda: target in [key(x) for x in data],
        number=repeats,
    )

    return {
        "binary_search_ms": round(binary_time / repeats * 1000, 2),
        "linear_search_ms": round(linear_time / repeats * 1000, 2),
        "builtin_in_ms": round(builtin_time / repeats * 1000, 2),
    }
