#!/usr/bin/env python3
"""Convert a HiGHS v2 basis-status file to standard MPS BAS format.

HiGHS status 1 is basic and status 0 is at the lower bound in this LP.
For a valid basis, the number of basic structural columns equals the number
of nonbasic row slacks.  MPS BAS encodes each such exchange as

    XL <basic-column> <nonbasic-row>
"""

from __future__ import annotations

import argparse


def load_statuses(path):
    columns = []
    rows = []
    target = None
    valid = False
    with open(path, encoding="ascii") as stream:
        for raw_line in stream:
            line = raw_line.strip()
            if line == "Valid":
                valid = True
            elif line.startswith("# Columns "):
                target = columns
            elif line.startswith("# Rows "):
                target = rows
            elif target is not None and line and not line.startswith("#"):
                name, status = line.split()
                target.append((name, int(status)))
    assert valid
    assert columns and rows
    return columns, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()

    columns, rows = load_statuses(args.source)
    basic_columns = [name for name, status in columns if status == 1]
    nonbasic_rows = [name for name, status in rows if status != 1]
    assert len(basic_columns) == len(nonbasic_rows)

    with open(args.target, "w", encoding="ascii") as stream:
        stream.write("NAME  highs-crossover.bas\n")
        for column, row in zip(basic_columns, nonbasic_rows):
            stream.write(f" XL {column:<14} {row}\n")
        stream.write("ENDATA\n")

    print(
        {
            "columns": len(columns),
            "rows": len(rows),
            "basic_columns": len(basic_columns),
            "nonbasic_rows": len(nonbasic_rows),
            "status": "PASS",
        }
    )


if __name__ == "__main__":
    main()
