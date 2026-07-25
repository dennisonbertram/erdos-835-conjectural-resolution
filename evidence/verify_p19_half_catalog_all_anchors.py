#!/usr/bin/env python3
"""Verify completeness accounting for the 210-anchor Schur sweep."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "6eeab50ed32037e7f28646543343465d837d32e233b845c51f54c521c12e5e12"
)
EXPECTED_CATALOGUE_SHA256 = (
    "226c5addbf5915c7a68023302c2eefc80cbe7cf243441f2fea68b8f263f7bc46"
)
JOBS_PER_ANCHOR = 396 * 40320


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse_values(path: Path) -> tuple[dict[str, str], str]:
    values: dict[str, str] = {}
    lines = path.read_text().splitlines()
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
    source = base / "p19_unrestricted_rank4_half_catalog_search.cpp"
    catalogue = base / "k10_one_factorizations_396.txt"
    logs = base / "p19_half_catalog_anchor_logs"

    assert sha256(source) == EXPECTED_SOURCE_SHA256
    assert sha256(catalogue) == EXPECTED_CATALOGUE_SHA256

    expected_anchors = list(itertools.combinations(range(10), 4))
    missing: list[int] = []
    total_jobs = 0
    wall_seconds: list[float] = []
    log_manifest = hashlib.sha256()
    for anchor_index, vertices in enumerate(expected_anchors):
        path = logs / f"anchor-{anchor_index:03d}.txt"
        if not path.exists():
            missing.append(anchor_index)
            continue
        values, terminal = parse_values(path)
        if not terminal:
            missing.append(anchor_index)
            continue
        if terminal == "WITNESS":
            raise RuntimeError(f"witness present in {path}")
        assert values["catalogue_factorizations"] == "396"
        assert values["anchor_positions"] == "210"
        assert int(values["exact_anchor_index"]) == anchor_index
        parsed_vertices = tuple(
            int(value)
            for value in values["exact_anchor_vertices"].strip("[]").split(",")
        )
        assert parsed_vertices == vertices
        assert int(values["exact_jobs_total"]) == JOBS_PER_ANCHOR
        assert int(values["magnitude_assignments_sampled"]) == JOBS_PER_ANCHOR
        assert int(values["anchor_trials"]) == JOBS_PER_ANCHOR
        elapsed = float(values["wall_seconds"])
        assert elapsed > 0
        assert terminal == "NO WITNESS FOR THIS ANCHOR (complete)"
        total_jobs += JOBS_PER_ANCHOR
        wall_seconds.append(elapsed)
        log_manifest.update(path.name.encode())
        log_manifest.update(b"\0")
        log_manifest.update(path.read_bytes())

    if missing:
        print(f"completed_anchors={210 - len(missing)}")
        print(f"missing_anchor_count={len(missing)}")
        print(
            "missing_anchor_preview="
            + ",".join(map(str, missing[:12]))
        )
        raise SystemExit(1)

    assert total_jobs == 210 * 396 * 40320
    print("source_sha256=PASS")
    print("catalogue_sha256=PASS")
    print("completed_anchors=210")
    print(f"total_exact_jobs={total_jobs}")
    print(f"aggregate_anchor_wall_seconds={sum(wall_seconds):.6f}")
    print(f"minimum_anchor_wall_seconds={min(wall_seconds):.6f}")
    print(f"maximum_anchor_wall_seconds={max(wall_seconds):.6f}")
    print(f"ordered_log_manifest_sha256={log_manifest.hexdigest()}")
    print("all_anchor_completion_accounting=PASS")


if __name__ == "__main__":
    main()
