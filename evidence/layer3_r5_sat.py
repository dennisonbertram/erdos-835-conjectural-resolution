#!/usr/bin/env python3
"""Layer-3 discrimination at the r=5 scale (v=11, b=66, b/v=6).

SEARCH: a point-identified family of 66 distinct 5-blocks on [11] and
two tilings w, w' at ODD fibre-distance, subject only to constraints
PROVED necessary for real S(4,5,11) mate systems:

  (N1a) pairwise |B_i intersection B_j| in {1,2,3}
        [Steiner bound <= t-1 = 3;
        no-disjointness n_0 = 0 from the intra distribution (2.3)]
  (N1b) every point lies in exactly 30 blocks     [lambda_1 = 30]
  (N1c) every 7-set contains exactly 3 blocks     [(r+1)/2-law]
  (N3)  tiling: every 7-set contains exactly one H_i = B_i u {w(i)}
        [mate characterization]
  (N4)  w and w' are 6-uniform: each point chosen by exactly 6 fibres
        [uniformity theorem, b/v = 6]
  (T)   sum_i [w(i) != w'(i)] is odd              [the target]

Deliberately NOT encoded (would collapse the relaxation to Steinerness):
lambda_2 = 12, lambda_3 = 4 (with N1a, lambda_3 = 4 forces lambda_4 = 1).

Protocol: FEASIBLE -> materialize witness, verify with check_witness()
(pure python, no solver).  INFEASIBLE -> CP-SAT provides no portable
certificate, so the run is reported as UNKNOWN* (solver-claimed
infeasibility, uncertified).  Timeout -> UNKNOWN.
A small-case UNSAT, certified or not, must NOT be read as a proof of
r=15 parity.

Run: python3 layer3_r5_sat.py [--seconds S] [--workers 1]
"""
import argparse
from itertools import combinations

V, R, NB, REPL, UNIF = 11, 5, 66, 30, 6


def build_and_solve(seconds, workers):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [[m.new_bool_var(f"x{i}_{p}") for p in range(V)]
         for i in range(NB)]
    for i in range(NB):
        m.add(sum(x[i]) == R)
    # symmetry: slot values strictly increasing; slot 0 = {0..4} (WLOG
    # by point relabelling of the lex-smallest block)
    vals = []
    for i in range(NB):
        vi = m.new_int_var(0, 2 ** V - 1, f"v{i}")
        m.add(vi == sum((1 << p) * x[i][p] for p in range(V)))
        vals.append(vi)
    for i in range(NB - 1):
        m.add(vals[i] < vals[i + 1])
    for p in range(V):
        m.add(x[0][p] == (1 if p < R else 0))
    # N1b replication
    for p in range(V):
        m.add(sum(x[i][p] for i in range(NB)) == REPL)
    # N1a pairwise intersections in {1,2,3}
    for i, j in combinations(range(NB), 2):
        ands = []
        for p in range(V):
            a = m.new_bool_var(f"a{i}_{j}_{p}")
            m.add_bool_or([x[i][p].Not(), x[j][p].Not(), a])
            m.add_implication(a, x[i][p])
            m.add_implication(a, x[j][p])
            ands.append(a)
        m.add(sum(ands) >= 1)
        m.add(sum(ands) <= 3)
    # subset indicators s[i][Z] and N1c
    sevens = list(combinations(range(V), 7))
    s = {}
    for zi, Z in enumerate(sevens):
        out = [p for p in range(V) if p not in Z]
        for i in range(NB):
            si = m.new_bool_var(f"s{i}_{zi}")
            m.add_bool_and([x[i][p].Not() for p in out]
                           ).only_enforce_if(si)
            m.add_bool_or([x[i][p] for p in out]
                          ).only_enforce_if(si.Not())
            s[(i, zi)] = si
        m.add(sum(s[(i, zi)] for i in range(NB)) == 3)
    # two tilings
    ys = []
    for tag in ("w", "w2"):
        y = [[m.new_bool_var(f"{tag}{i}_{p}") for p in range(V)]
             for i in range(NB)]
        for i in range(NB):
            m.add(sum(y[i]) == 1)
            for p in range(V):
                m.add_implication(y[i][p], x[i][p].Not())
        for p in range(V):  # N4
            m.add(sum(y[i][p] for i in range(NB)) == UNIF)
        for zi, Z in enumerate(sevens):  # N3
            cs = []
            for i in range(NB):
                g = m.new_bool_var(f"g{tag}{i}_{zi}")
                m.add(g == sum(y[i][p] for p in Z))
                c = m.new_bool_var(f"c{tag}{i}_{zi}")
                m.add(c <= s[(i, zi)])
                m.add(c <= g)
                m.add(c >= s[(i, zi)] + g - 1)
                cs.append(c)
            m.add(sum(cs) == 1)
        ys.append(y)
    # odd distance: d[i] <-> w_i != w'_i
    ds = [m.new_bool_var(f"d{i}") for i in range(NB)]
    for i in range(NB):
        same = m.new_bool_var(f"same{i}")
        for p in range(V):
            # same => y and y2 agree at p
            m.add(ys[0][i][p] == ys[1][i][p]).only_enforce_if(same)
        # not same => exists p with y=1, y2=0
        diff_lits = []
        for p in range(V):
            dl = m.new_bool_var(f"dl{i}_{p}")
            m.add_implication(dl, ys[0][i][p])
            m.add_implication(dl, ys[1][i][p].Not())
            diff_lits.append(dl)
        m.add_bool_or(diff_lits).only_enforce_if(same.Not())
        m.add(ds[i] == same.Not())
    tot = m.new_int_var(0, NB, "tot")
    m.add(tot == sum(ds))
    k = m.new_int_var(0, NB // 2, "k")
    m.add(tot == 2 * k + 1)

    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = seconds
    sol.parameters.num_search_workers = workers
    sol.parameters.random_seed = 1
    status = sol.solve(m)
    name = sol.status_name(status)
    print(f"status: {name}  wall: {sol.wall_time:.1f}s  "
          f"branches: {sol.num_branches}")
    if name in ("FEASIBLE", "OPTIMAL"):
        fam = [tuple(p for p in range(V) if sol.value(x[i][p]))
               for i in range(NB)]
        w1 = [next(p for p in range(V) if sol.value(ys[0][i][p]))
              for i in range(NB)]
        w2 = [next(p for p in range(V) if sol.value(ys[1][i][p]))
              for i in range(NB)]
        print("WITNESS FAMILY:", fam)
        print("W :", w1)
        print("W':", w2)
        ok = check_witness(fam, w1, w2)
        print(f"independent checker: {'PASS' if ok else 'FAIL'}")
        return name, (fam, w1, w2)
    if name == "INFEASIBLE":
        print("NOTE: CP-SAT emits no portable certificate; per protocol "
              "this run is recorded as UNKNOWN* (uncertified "
              "solver-claimed infeasibility).")
    return name, None


def check_witness(fam, w1, w2):
    """Pure-python direct verification of all encoded constraints."""
    from itertools import combinations as C
    assert len(fam) == NB and len(set(fam)) == NB
    for B in fam:
        assert len(B) == R and all(0 <= p < V for p in B)
    for i, j in C(range(NB), 2):
        inter = len(set(fam[i]) & set(fam[j]))
        assert 1 <= inter <= 3, (i, j, inter)
    for p in range(V):
        assert sum(1 for B in fam if p in B) == REPL
    sevens = list(C(range(V), 7))
    for Z in sevens:
        Zs = set(Z)
        assert sum(1 for B in fam if set(B) <= Zs) == 3
    for w in (w1, w2):
        for i, B in enumerate(fam):
            assert w[i] not in B
        for p in range(V):
            assert sum(1 for i in range(NB) if w[i] == p) == UNIF
        for Z in sevens:
            Zs = set(Z)
            cnt = sum(1 for i, B in enumerate(fam)
                      if set(B) <= Zs and w[i] in Zs)
            assert cnt == 1, (Z, cnt)
    d = sum(1 for i in range(NB) if w1[i] != w2[i])
    assert d % 2 == 1, d
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=1800.0)
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    build_and_solve(a.seconds, a.workers)
