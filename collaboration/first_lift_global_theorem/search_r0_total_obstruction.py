"""Search for an r=0 seven-prefix blocking all seven remaining 10-supports.

This is an exact counterexample search.  The CP-SAT master contains the
seven edge-disjoint selected matchings, the seven remaining complement
triples, the three remaining complement five-sets, and the exact
complement-degree identity.  Whenever a candidate residual support has a
perfect matching, a lazy linear cut forbids that matching for that precise
complement triple.  SAT therefore gives a checkable counterexample; UNSAT
after finitely many cuts proves that no such prefix exists.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

from ortools.sat.python import cp_model


N = 13
VERTICES = range(N)
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
INCIDENT = tuple(
    tuple(index for index, edge in enumerate(EDGES) if vertex in edge)
    for vertex in VERTICES
)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge = EDGE_INDEX[tuple(sorted((first, second)))]
        for tail in perfect_matchings(rest):
            result.append((edge, *tail))
    return tuple(result)


def find_residual_matching(
    support: tuple[int, ...],
    selected_edges: set[int],
) -> tuple[int, ...] | None:
    for matching in perfect_matchings(support):
        if selected_edges.isdisjoint(matching):
            return matching
    return None


def main() -> None:
    model = cp_model.CpModel()
    x = {
        (colour, edge): model.new_bool_var(f"x_{colour}_{edge}")
        for colour in range(7)
        for edge in range(len(EDGES))
    }
    f = [model.new_bool_var(f"f_{edge}") for edge in range(len(EDGES))]

    for colour in range(7):
        model.add(
            sum(x[colour, edge] for edge in range(len(EDGES)))
            == (4 if colour < 4 else 5)
        )
        for vertex in VERTICES:
            model.add(sum(x[colour, edge] for edge in INCIDENT[vertex]) <= 1)
    for edge in range(len(EDGES)):
        model.add(sum(x[colour, edge] for colour in range(7)) == f[edge])

    # Relabel vertices so that the first size-eight matching is canonical.
    canonical = {
        EDGE_INDEX[(0, 1)],
        EDGE_INDEX[(2, 3)],
        EDGE_INDEX[(4, 5)],
        EDGE_INDEX[(6, 7)],
    }
    for edge in range(len(EDGES)):
        model.add(x[0, edge] == int(edge in canonical))

    triples = {
        (index, vertex): model.new_bool_var(f"t_{index}_{vertex}")
        for index in range(7)
        for vertex in VERTICES
    }
    fives = {
        (index, vertex): model.new_bool_var(f"q_{index}_{vertex}")
        for index in range(3)
        for vertex in VERTICES
    }
    for index in range(7):
        model.add(sum(triples[index, vertex] for vertex in VERTICES) == 3)
    for index in range(3):
        model.add(sum(fives[index, vertex] for vertex in VERTICES) == 5)

    for vertex in VERTICES:
        degree = sum(f[edge] for edge in INCIDENT[vertex])
        omissions = sum(triples[index, vertex] for index in range(7))
        omissions += sum(fives[index, vertex] for index in range(3))
        model.add(omissions == degree - 2)

    # The seven triples are exchangeable.  Numeric binary encodings impose a
    # canonical nondecreasing order without changing the feasible set.
    weights = [1 << vertex for vertex in VERTICES]
    for index in range(6):
        model.add(
            sum(weights[v] * triples[index, v] for v in VERTICES)
            <= sum(weights[v] * triples[index + 1, v] for v in VERTICES)
        )
    for index in range(2):
        model.add(
            sum(weights[v] * fives[index, v] for v in VERTICES)
            <= sum(weights[v] * fives[index + 1, v] for v in VERTICES)
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60
    solver.parameters.num_search_workers = 8
    solver.parameters.log_search_progress = False

    cuts = 0
    rounds = 0
    while True:
        rounds += 1
        status = solver.solve(model)
        if status == cp_model.INFEASIBLE:
            print(f"MASTER_UNSAT rounds={rounds} cuts={cuts}")
            return
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"MASTER_UNKNOWN rounds={rounds} cuts={cuts}")
            return

        selected = {edge for edge in range(len(EDGES)) if solver.value(f[edge])}
        violations = []
        for index in range(7):
            omitted = tuple(
                vertex
                for vertex in VERTICES
                if solver.value(triples[index, vertex])
            )
            support = tuple(vertex for vertex in VERTICES if vertex not in omitted)
            matching = find_residual_matching(support, selected)
            if matching is not None:
                violations.append((index, omitted, matching))

        if not violations:
            print(f"COUNTEREXAMPLE rounds={rounds} cuts={cuts}")
            print("selected", [EDGES[edge] for edge in sorted(selected)])
            for index in range(7):
                print(
                    "triple",
                    index,
                    tuple(
                        vertex
                        for vertex in VERTICES
                        if solver.value(triples[index, vertex])
                    ),
                )
            for index in range(3):
                print(
                    "five",
                    index,
                    tuple(
                        vertex
                        for vertex in VERTICES
                        if solver.value(fives[index, vertex])
                    ),
                )
            return

        for index, omitted, matching in violations:
            # If this precise triple recurs, at least one edge of the exposed
            # perfect matching must belong to F.
            mismatch = 3 - sum(triples[index, vertex] for vertex in omitted)
            model.add(sum(f[edge] for edge in matching) + mismatch >= 1)
            cuts += 1
        if rounds % 100 == 0:
            print(f"PROGRESS rounds={rounds} cuts={cuts}")


if __name__ == "__main__":
    main()
