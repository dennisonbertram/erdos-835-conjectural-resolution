#!/usr/bin/env python3
"""Search the necessary 18-vector F_17^2 link for determinant colorings.

After fixing one projected vector A=(1,0), the determinant values against A
label the other nonparallel vectors by their second coordinate.  Thus every
candidate is equivalent to

    A=(1,0), B=(a,0), V_y=(x_y,y),  y in F_17^*.

For every vector, its determinants against the other 17 vectors must be all
of F_17.  This CP-SAT model decides that exact local condition.  It is only a
necessary condition for a global Grassmannian construction.
"""

import argparse
from ortools.sat.python import cp_model


P = 17


def solve_for_a(a, seconds, workers):
    model = cp_model.CpModel()
    xs = {
        y: model.new_int_var(0, P - 1, f"x_{y}")
        for y in range(1, P)
    }
    # The shear (x,y) -> (x-by,y) preserves every determinant, so normalize.
    model.add(xs[1] == 0)

    determinants = {}
    for y in range(1, P):
        row = [(-y) % P, (-a * y) % P]
        for z in range(1, P):
            if z == y:
                continue
            raw = model.new_int_var(
                -(P - 1) ** 2,
                (P - 1) ** 2,
                f"raw_{y}_{z}",
            )
            value = model.new_int_var(0, P - 1, f"d_{y}_{z}")
            model.add(raw == z * xs[y] - y * xs[z])
            model.add_modulo_equality(value, raw, P)
            determinants[y, z] = value
            row.append(value)
        assert len(row) == P
        model.add_all_different(row)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 20260724 + a
    status = solver.solve(model)
    name = solver.status_name(status)
    print(
        f"a={a} status={name} wall={solver.wall_time:.3f} "
        f"branches={solver.num_branches} conflicts={solver.num_conflicts}"
    )
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {y: solver.value(xs[y]) for y in range(1, P)}
        print("x=" + " ".join(f"{y}:{values[y]}" for y in range(1, P)))
        # Independent direct verification.
        vectors = [(1, 0), (a, 0)] + [
            (values[y], y) for y in range(1, P)
        ]
        for i, (x_i, y_i) in enumerate(vectors):
            row = [
                (x_i * y_j - y_i * x_j) % P
                for j, (x_j, y_j) in enumerate(vectors)
                if i != j
            ]
            assert sorted(row) == list(range(P)), (i, row)
        print("verified_local_link=True")
        return values
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--a", type=int)
    args = parser.parse_args()
    values = [args.a] if args.a else list(range(1, P))
    for a in values:
        result = solve_for_a(a, args.seconds, args.workers)
        if result is not None:
            break


if __name__ == "__main__":
    main()
