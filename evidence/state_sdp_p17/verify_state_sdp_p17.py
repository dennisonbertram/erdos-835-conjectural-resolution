#!/usr/bin/env python3
"""Verify the exact p=17 colour-state association certificate."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"
ORBIT_NAMES = ("same", "reverse", "shared_end", "directed_path", "disjoint")


def johnson_eigenvalue(m: int, distance: int, eigenspace: int) -> int:
    """Eigenvalue of A_distance on E_eigenspace in J(2m,m)."""
    return sum(
        (-1) ** (distance - t)
        * comb(m - t, distance - t)
        * comb(m - eigenspace, t)
        * comb(m + t - eigenspace, t)
        for t in range(distance + 1)
        if t <= m - eigenspace
    )


def parse_weight_map(raw: dict[str, str]) -> dict[int, Fraction]:
    return {int(index): Fraction(value) for index, value in raw.items()}


def main() -> None:
    data = json.loads(CERTIFICATE.read_text())
    q = int(data["q"])
    m = int(data["m"])
    n = int(data["cell_size_n"])
    vertex_count = int(data["vertex_count_N"])
    state_count = int(data["ordered_state_count"])
    even_weights = parse_weight_map(data["even_high_weights"])
    odd_weights = parse_weight_map(data["odd_high_weights"])
    trace_quarters = [int(value) for value in data["same_state_trace_quarters_by_distance"]]

    assert q == m + 2 == 17
    assert state_count == q * (q - 1)
    assert vertex_count == comb(2 * m, m) == q * (q - 1) * n
    assert sorted(even_weights) == list(range(2, m, 2))
    assert sorted(odd_weights) == list(range(1, m + 1, 2))
    assert len(trace_quarters) == m + 1
    assert all(weight > 0 for weight in (*even_weights.values(), *odd_weights.values()))
    assert sum(even_weights.values()) == 1
    assert sum(odd_weights.values()) == 1

    serialization = "\n".join(
        f"{index}:{weight}"
        for index, weight in [*even_weights.items(), *odd_weights.items()]
    )
    digest = hashlib.sha256(serialization.encode()).hexdigest()
    assert digest == data["weight_serialization_sha256"]

    # Orthogonal-projector entries on the five S_q-orbits of pairs of
    # directed, non-loop colour states.
    trivial = (Fraction(1, 272),) * 5
    standard_plus = (
        Fraction(1, 17),
        Fraction(1, 17),
        Fraction(13, 510),
        Fraction(13, 510),
        Fraction(-2, 255),
    )
    standard_minus = (
        Fraction(1, 17),
        Fraction(-1, 17),
        Fraction(1, 34),
        Fraction(-1, 34),
        Fraction(0),
    )
    high_plus = (
        Fraction(7, 16),
        Fraction(7, 16),
        Fraction(-7, 240),
        Fraction(-7, 240),
        Fraction(1, 240),
    )
    high_minus = (
        Fraction(15, 34),
        Fraction(-15, 34),
        Fraction(-1, 34),
        Fraction(1, 34),
        Fraction(0),
    )

    orbit_sizes = (
        state_count,
        state_count,
        state_count * 2 * (q - 2),
        state_count * 2 * (q - 2),
        state_count * (q - 2) * (q - 3),
    )

    rows: list[tuple[Fraction, ...]] = []
    for distance in range(m + 1):
        valency = comb(m, distance) ** 2
        high_plus_eigenvalue = sum(
            weight * johnson_eigenvalue(m, distance, index)
            for index, weight in even_weights.items()
        )
        high_minus_eigenvalue = sum(
            weight * johnson_eigenvalue(m, distance, index)
            for index, weight in odd_weights.items()
        )
        row = tuple(
            valency * trivial[orbit]
            + johnson_eigenvalue(m, distance, m - 1) * standard_plus[orbit]
            + johnson_eigenvalue(m, distance, m) * standard_minus[orbit]
            + high_plus_eigenvalue * high_plus[orbit]
            + high_minus_eigenvalue * high_minus[orbit]
            for orbit in range(5)
        )
        rows.append(row)
        assert all(value >= 0 for value in row)

        same, reverse, shared_end, directed_path, disjoint = row
        binomial = comb(m, distance)
        own_profile = Fraction(
            binomial**2 + (-1) ** distance * (m - distance + 1) * binomial,
            q,
        )
        complement_profile = Fraction(
            binomial**2 - (-1) ** distance * (distance + 1) * binomial,
            q,
        )
        other_profile = Fraction(
            m * binomial**2 + (-1) ** distance * (2 * distance - m) * binomial,
            m * q,
        )
        assert same + (q - 2) * shared_end == own_profile
        assert reverse + (q - 2) * directed_path == complement_profile
        assert shared_end + directed_path + (q - 3) * disjoint == other_profile

        same_state_trace = state_count * n * same
        assert same_state_trace == 4 * trace_quarters[distance]

        orbit_totals = tuple(
            orbit_sizes[orbit] * n * row[orbit] for orbit in range(5)
        )
        assert all(total.denominator == 1 for total in orbit_totals)
        assert all(total.numerator % 2 == 0 for total in orbit_totals)
        assert sum(orbit_totals) == vertex_count * valency

    assert rows[0] == (1, 0, 0, 0, 0)
    assert rows[m] == (0, 1, 0, 0, 0)
    assert rows[1][0] == rows[1][2] == 0
    assert rows[m - 1][1] == rows[m - 1][3] == 0

    print("state-SDP certificate: VERIFIED")
    print(f"q={q}, m={m}, N={vertex_count}, n={n}")
    print(f"weight SHA-256: {digest}")
    print("all 16 distances and all 5 state-pair orbits are nonnegative")
    print("all aggregate orbit totals are even integers")


if __name__ == "__main__":
    main()
