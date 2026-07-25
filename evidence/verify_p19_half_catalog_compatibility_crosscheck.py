#!/usr/bin/env python3
"""Verify exact sample logs from the independent mask/MRV Schur solver."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "0cd7a6bf5fda3fb202810a3384ddd31c80709d798e1cf9f4403961bba777ec8a"
)
EXPECTED_CATALOGUE_SHA256 = (
    "226c5addbf5915c7a68023302c2eefc80cbe7cf243441f2fea68b8f263f7bc46"
)
SAMPLE_ANCHORS = (0, 84, 137, 209)
JOBS_PER_ANCHOR = 396 * 40320
TERMINAL = "NO WITNESS FOR THIS ANCHOR (complete)"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse_log(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text().splitlines()
    values = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    terminal = next(
        (
            line
            for line in reversed(lines)
            if line.startswith("WITNESS")
            or line.startswith("NO WITNESS")
        ),
        "",
    )
    return values, terminal


def main() -> None:
    base = Path(__file__).resolve().parent
    source = (
        base
        / "p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp"
    )
    catalogue = base / "k10_one_factorizations_396.txt"
    logs = base / "p19_half_catalog_anchor_logs"
    anchors = list(itertools.combinations(range(10), 4))

    assert sha256(source) == EXPECTED_SOURCE_SHA256
    assert sha256(catalogue) == EXPECTED_CATALOGUE_SHA256

    checked_jobs = 0
    for anchor_index in SAMPLE_ANCHORS:
        path = logs / f"compat-lazy-anchor-{anchor_index:03d}.txt"
        values, terminal = parse_log(path)
        assert terminal == TERMINAL
        assert values["catalogue_factorizations"] == "396"
        assert values["anchor_positions"] == "210"
        assert int(values["exact_anchor_index"]) == anchor_index
        parsed_vertices = tuple(
            int(value)
            for value in values["exact_anchor_vertices"].strip("[]").split(",")
        )
        assert parsed_vertices == anchors[anchor_index]
        assert int(values["exact_jobs_total"]) == JOBS_PER_ANCHOR
        assert int(values["magnitude_assignments_sampled"]) == JOBS_PER_ANCHOR
        assert int(values["anchor_trials"]) == JOBS_PER_ANCHOR
        checked_jobs += JOBS_PER_ANCHOR

    print("crosscheck_source_sha256=PASS")
    print("catalogue_sha256=PASS")
    print(f"completed_sample_anchors={len(SAMPLE_ANCHORS)}")
    print(f"total_crosscheck_jobs={checked_jobs}")
    print("compatibility_mask_crosscheck=PASS")


if __name__ == "__main__":
    main()
