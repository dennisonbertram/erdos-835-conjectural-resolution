#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GLOBAL = HERE.parent
sys.path.insert(0, str(GLOBAL))
import verify_r0_core_pairs as core

CADICAL = "/opt/homebrew/bin/cadical"
TMP = Path("/private/tmp")


class CNF:
    def __init__(self):
        self.variables = 0
        self.clauses = []

    def new(self):
        self.variables += 1
        return self.variables

    def add(self, *lits):
        self.clauses.append(tuple(lits))

    def exactly(self, lits, count, guard=None):
        lits = tuple(lits)
        prefix = () if guard is None else (-guard,)
        for choice in itertools.combinations(lits, count + 1):
            self.add(*prefix, *(-lit for lit in choice))
        for choice in itertools.combinations(lits, len(lits) - count + 1):
            self.add(*prefix, *choice)

    def write(self, path):
        lines = [f"p cnf {self.variables} {len(self.clauses)}"]
        lines += [" ".join(map(str, clause)) + " 0" for clause in self.clauses]
        path.write_text("\n".join(lines) + "\n")


def clique(values):
    mask = 0
    for edge in itertools.combinations(sorted(values), 2):
        mask |= 1 << core.EDGE_ID[edge]
    return mask


def pair_orbits(kind):
    if kind == "5111":
        groups = (tuple(range(5)), tuple(range(5, 8)), tuple(range(8, 13)))
    elif kind == "31111":
        groups = (tuple(range(3)), tuple(range(3, 7)), tuple(range(7, 13)))
    elif kind == "6":
        groups = (tuple(range(6)), (), tuple(range(6, 13)))
    else:
        raise ValueError(kind)
    first = core.embeddings(kind)[0]
    out = []
    for counts in itertools.product(*(range(len(group) + 1) for group in groups)):
        if sum(counts) != 6:
            continue
        vertices = tuple(
            vertex
            for group, count in zip(groups, counts)
            for vertex in group[:count]
        )
        second = clique(vertices)
        if kind == "6" and second == first:
            continue
        union = first | second
        degrees = [(union & core.INCIDENT[v]).bit_count() for v in core.VERTICES]
        if union.bit_count() > 31 or max(degrees) > 7:
            continue
        deficit = sum(max(0, 2 - value) for value in degrees)
        if union.bit_count() + (deficit + 1) // 2 > 31:
            continue
        out.append((counts, first, second))
    return out


def build(kind, counts, first, second, reuse_first):
    cnf = CNF()
    edge_list = tuple(core.EDGE_ID)
    x = {
        (color, edge): cnf.new()
        for color in range(7)
        for edge in edge_list
    }
    u = {(vertex, color): cnf.new() for vertex in range(13) for color in range(7)}
    z = {(row, vertex): cnf.new() for row in range(10) for vertex in range(13)}
    degree_choice = {
        (vertex, degree): cnf.new()
        for vertex in range(13)
        for degree in range(2, 8)
    }

    capacities = (5, 5, 5, 4, 4, 4, 4)
    for color, edges in enumerate(capacities):
        cnf.exactly([u[vertex, color] for vertex in range(13)], 2 * edges)
        for vertex in range(13):
            incident = [x[color, edge] for edge in edge_list if vertex in edge]
            cnf.add(-u[vertex, color], *incident)
            for value in incident:
                cnf.add(-value, u[vertex, color])
            for left, right in itertools.combinations(incident, 2):
                cnf.add(-left, -right)

    for edge in edge_list:
        for left, right in itertools.combinations(
            [x[color, edge] for color in range(7)], 2
        ):
            cnf.add(-left, -right)
    required = first | second
    for edge, index in core.EDGE_ID.items():
        if required >> index & 1:
            cnf.add(*(x[color, edge] for color in range(7)))

    all_vertices = (1 << 13) - 1
    outside_first = all_vertices ^ sum(
        1 << v for v in range(13) if first & core.INCIDENT[v]
    )
    outside_second = all_vertices ^ sum(
        1 << v for v in range(13) if second & core.INCIDENT[v]
    )
    for row in range(7):
        outside = outside_first if row < reuse_first else outside_second
        allowed = [v for v in range(13) if outside >> v & 1]
        cnf.exactly([z[row, v] for v in allowed], 3)
        for v in range(13):
            if v not in allowed:
                cnf.add(-z[row, v])
    for row in range(7, 10):
        cnf.exactly([z[row, v] for v in range(13)], 5)

    for vertex in range(13):
        choices = [degree_choice[vertex, degree] for degree in range(2, 8)]
        cnf.exactly(choices, 1)
        support = [u[vertex, color] for color in range(7)]
        complements = [z[row, vertex] for row in range(10)]
        for degree in range(2, 8):
            guard = degree_choice[vertex, degree]
            cnf.exactly(support, degree, guard)
            cnf.exactly(complements, degree - 2, guard)

    return cnf, x, z


def parse(path):
    return {
        int(token)
        for token in path.read_text().split()
        if token.lstrip("-").isdigit() and int(token) > 0
    }


def run_case(kind, orbit_index, counts, first, second, reuse_first, seconds):
    cnf, x, z = build(kind, counts, first, second, reuse_first)
    stem = f"r0_{kind}_6_o{orbit_index}_t{reuse_first}"
    cnf_path = TMP / f"{stem}.cnf"
    witness_path = TMP / f"{stem}.witness"
    cnf.write(cnf_path)
    result = subprocess.run(
        [
            CADICAL, "-q", "--sat", "--shuffle=true",
            f"--seed={51001 + orbit_index * 10 + reuse_first}",
            "-t", str(seconds), "-w", str(witness_path), str(cnf_path),
        ],
        check=False,
    )
    status = {10: "SAT", 20: "UNSAT"}.get(result.returncode, "UNKNOWN")
    print(kind, orbit_index, counts, reuse_first, status, cnf.variables, len(cnf.clauses), flush=True)
    if status != "SAT":
        return False
    positive = parse(witness_path)
    matchings = []
    used_edges = set()
    for color in range(7):
        matching = [edge for edge in core.EDGE_ID if x[color, edge] in positive]
        assert len(matching) == (5 if color < 3 else 4)
        assert len({v for edge in matching for v in edge}) == 2 * len(matching)
        assert used_edges.isdisjoint(matching)
        used_edges.update(matching)
        matchings.append(matching)
    required_edges = {edge for edge, i in core.EDGE_ID.items() if (first | second) >> i & 1}
    assert required_edges <= used_edges
    complements = [
        [v for v in range(13) if z[row, v] in positive] for row in range(10)
    ]
    assert [len(values) for values in complements] == [3] * 7 + [5] * 3
    degrees = [sum(v in edge for edge in used_edges) for v in range(13)]
    assert all(sum(v in values for values in complements) == degrees[v] - 2 for v in range(13))
    outside_first = set(range(13)) - {v for edge in required_edges if edge in {e for e,i in core.EDGE_ID.items() if first>>i&1} for v in edge}
    # Direct core containment checks are simpler and independent of Tutte:
    first_vertices = {v for edge,i in core.EDGE_ID.items() if first>>i&1 for v in edge}
    second_vertices = {v for edge,i in core.EDGE_ID.items() if second>>i&1 for v in edge}
    for row, missing in enumerate(complements[:7]):
        support = set(range(13)) - set(missing)
        assert (first_vertices if row < reuse_first else second_vertices) <= support
    output = TMP / "r0_two_core_sat.json"
    output.write_text(json.dumps({
        "kind_pair": [kind, "6"],
        "orbit_counts": counts,
        "reuse_counts": [reuse_first, 7 - reuse_first],
        "selected_matchings": [[list(edge) for edge in matching] for matching in matchings],
        "remaining_complements": complements,
    }, indent=2, sort_keys=True) + "\n")
    print("FOUND", output, flush=True)
    return True


def main():
    seconds = int(sys.argv[1])
    for kind in ("5111", "31111", "6"):
        orbits = pair_orbits(kind)
        print("ORBITS", kind, len(orbits), [item[0] for item in orbits], flush=True)
        reuse_values = (2, 3) if kind != "6" else (2, 3, 4, 5)
        for orbit_index, (counts, first, second) in enumerate(orbits):
            for reuse_first in reuse_values:
                if run_case(kind, orbit_index, counts, first, second, reuse_first, seconds):
                    return


if __name__ == "__main__":
    main()
