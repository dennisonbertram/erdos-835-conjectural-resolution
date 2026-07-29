#!/usr/bin/env python3
"""Check the two exhaustive slice traversals against the canonical store."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL = ROOT / "families"
ALTERNATE = ROOT / "families_alt"
RESULTS = ROOT / "enumeration_results"
ORBITS = 40


def rows(path):
    raw = path.read_bytes()
    assert raw and len(raw) % ORBITS == 0
    result = [
        raw[offset : offset + ORBITS]
        for offset in range(0, len(raw), ORBITS)
    ]
    assert len(set(result)) == len(result)
    return sorted(result)


def load_result(prefix, outer):
    stem = f"{prefix}_result" if prefix else "result"
    path = RESULTS / f"{stem}_0_{outer}.json"
    result = json.loads(path.read_text(encoding="ascii"))
    assert result["pair"] == [0, outer]
    assert result["rows"] == 456
    assert result["capped"] is False
    assert result["stored"] == result["count"]
    assert result["store_complete"] is True
    return result


def main():
    report = {}
    for outer in range(1, 15):
        canonical = rows(CANONICAL / f"sols_0_{outer}.bin")
        alternate = rows(ALTERNATE / f"alt_sols_0_{outer}.bin")
        assert canonical == alternate

        alternate_result = load_result("alt", outer)
        assert alternate_result["count"] == len(canonical)
        if outer >= 2:
            primary_result = load_result("", outer)
            assert primary_result["count"] == len(canonical)
            assert primary_result["nodes"] == alternate_result["nodes"]

        report[str(outer)] = {
            "count": len(canonical),
            "equal_row_sets": True,
            "sorted_sha256": hashlib.sha256(
                b"".join(canonical)
            ).hexdigest(),
        }

    print(json.dumps({"status": "PASS", "families": report}, sort_keys=True))


if __name__ == "__main__":
    main()
