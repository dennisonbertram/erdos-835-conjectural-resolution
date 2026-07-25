#!/usr/bin/env python3
"""Round 2: structure of the shaped-kernel relaxation (2026-07-24).

Shaped vectors (base A an S(r-1,r,2r+1)): z supported on non-A blocks,
viewed in sphere coordinates (P,p); in each sphere either z=0 or z has one
+1 and one -1.  These are exactly differences of two sphere-transversal
choice maps.  Steiner differences x_B - x_C (B,C disjoint from A) are the
shaped kernel vectors with both endpoints Steiner.

Questions:
  Q-Z   (integer): can a shaped z with Wz=0 (over Z) have an odd number of
        active spheres?
  Q-F2  (mod 2):  can a shaped u (one 2-subset or nothing per sphere) with
        Wu=0 over GF(2) have an odd number of active spheres?
  Q-lat: is the full integer lattice {z on non-A blocks: Wz=0, sphere sums
        zero} 4-even (all norms == 0 mod 4)?

r=3: exhaustive; r=5: CP-SAT feasibility (UNSAT = impossibility).
Also classifies the 112 nonzero shaped kernel vectors found at r=3.
"""

import sys
from collections import Counter
from itertools import combinations
from math import comb

sys.setrecursionlimit(100000)


# ---------------- shared small utilities ----------------

def build_fano():
    n, r = 7, 3
    blocks_list = [frozenset(c) for c in combinations(range(n), r)]
    facets = list(combinations(range(n), r - 1))
    cols = {f: set() for f in facets}
    rows = {}
    for i, K in enumerate(blocks_list):
        rows[i] = [f for f in facets if frozenset(f) <= K]
        for f in rows[i]:
            cols[f].add(i)

    solutions = []
    partial = []

    def select(rr):
        removed = []
        for j in rows[rr]:
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].remove(i)
            removed.append(cols.pop(j))
        return removed

    def deselect(rr, removed):
        for j in reversed(rows[rr]):
            cols[j] = removed.pop()
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].add(i)

    def solve():
        if not cols:
            solutions.append(list(partial))
            return
        c = min(cols, key=lambda k: len(cols[k]))
        for rr in sorted(cols[c]):
            partial.append(rr)
            rem = select(rr)
            solve()
            deselect(rr, rem)
            partial.pop()

    solve()
    systems = [frozenset(blocks_list[i] for i in s) for s in solutions]
    assert len(systems) == 30
    return blocks_list, systems


def steiner_mates(systems, A):
    return [S for S in systems if not (S & A)]


# ---------------- r=3 exhaustive analyses ----------------

def r3_analysis():
    print("=" * 72)
    print("r=3 shaped-kernel structure (exhaustive)")
    n = 7
    X = frozenset(range(n))
    blocks_list, systems = build_fano()
    A = sorted(systems[0], key=sorted)
    Aset = frozenset(A)
    mates = steiner_mates(systems, Aset)
    spheres = [sorted(X - P) for P in A]

    pair_pos = {}
    for a in range(7):
        for b_ in range(a + 1, 7):
            Pa, Pb = A[a], A[b_]
            qa = [spheres[a].index(q) for q in sorted(Pb - Pa)]
            qb = [spheres[b_].index(q) for q in sorted(Pa - Pb)]
            pair_pos[(a, b_)] = (qa, qb)

    # ---- integer shaped enumeration, recording solutions ----
    opts = [None] + [(i, j) for i in range(4) for j in range(4) if i != j]

    def zsum(o, positions):
        if o is None:
            return 0
        t = 0
        for i in positions:
            if o[0] == i:
                t += 1
            if o[1] == i:
                t -= 1
        return t

    ca = {k: [zsum(o, v[0]) for o in opts] for k, v in pair_pos.items()}
    cb = {k: [zsum(o, v[1]) for o in opts] for k, v in pair_pos.items()}

    sols = []
    assignment = [0] * 7

    def dfs(s):
        if s == 7:
            sols.append(tuple(assignment))
            return
        for k in range(len(opts)):
            ok = True
            for t in range(s):
                key = (t, s)
                if ca[key][assignment[t]] + cb[key][k] != 0:
                    ok = False
                    break
            if ok:
                assignment[s] = k
                dfs(s + 1)
                assignment[s] = 0

    dfs(0)
    nonzero = [s for s in sols if any(k != 0 for k in s)]
    print("nonzero shaped integer kernel vectors:", len(nonzero))

    # classify: which are Steiner differences?
    def mate_vector(B):
        """sphere -> (pos_index, ) choice of B in each sphere."""
        out = []
        for idx, P in enumerate(A):
            K0 = next(K for K in B if not (K & P))
            p0 = next(iter(X - P - K0))
            out.append(spheres[idx].index(p0))
        return out

    mate_vecs = {B: mate_vector(B) for B in mates}
    steiner_diffs = set()
    for B in mates:
        for C in mates:
            if B is C:
                continue
            vb, vc = mate_vecs[B], mate_vecs[C]
            key = []
            for s in range(7):
                if vb[s] == vc[s]:
                    key.append(0)
                else:
                    key.append(opts.index((vb[s], vc[s])))
            steiner_diffs.add(tuple(key))
    print("distinct ordered Steiner differences:", len(steiner_diffs))
    inside = sum(1 for s in nonzero if tuple(s) in steiner_diffs)
    print("shaped kernel vectors that are Steiner differences:", inside,
          "; others:", len(nonzero) - inside)

    # structure of the non-Steiner ones: facet vector of the completion
    others = [s for s in nonzero if tuple(s) not in steiner_diffs]
    # active-sphere patterns
    def active_pattern(s):
        return tuple(i for i in range(7) if s[i] != 0)
    pat_steiner = Counter(active_pattern(s) for s in nonzero
                          if tuple(s) in steiner_diffs)
    pat_other = Counter(active_pattern(s) for s in others)
    print("distinct active-sphere 6-sets (Steiner):", len(pat_steiner),
          "(others):", len(pat_other))
    overlap = set(pat_steiner) & set(pat_other)
    print("patterns shared between the two classes:", len(overlap))

    # ---- GF(2)-shaped exhaustive ----
    opts2 = [None] + [frozenset(p) for p in combinations(range(4), 2)]

    def usum(o, positions):
        if o is None:
            return 0
        return sum(1 for i in positions if i in o) % 2

    ca2 = {k: [usum(o, v[0]) for o in opts2] for k, v in pair_pos.items()}
    cb2 = {k: [usum(o, v[1]) for o in opts2] for k, v in pair_pos.items()}

    counts2 = Counter()
    assignment2 = [0] * 7

    def dfs2(s):
        if s == 7:
            act = sum(1 for k in assignment2 if opts2[k] is not None)
            counts2[act] += 1
            return
        for k in range(len(opts2)):
            ok = True
            for t in range(s):
                key = (t, s)
                if (ca2[key][assignment2[t]] + cb2[key][k]) % 2 != 0:
                    ok = False
                    break
            if ok:
                assignment2[s] = k
                dfs2(s + 1)
                assignment2[s] = 0

    dfs2(0)
    print("GF(2)-shaped kernel vectors by #active spheres:",
          dict(sorted(counts2.items())))
    odd2 = {k: v for k, v in counts2.items() if k % 2 == 1}
    print("odd-active GF(2)-shaped:", odd2 if odd2 else "NONE")

    # ---- full binary code on non-A columns ----
    nonA = [K for K in blocks_list if K not in Aset]
    facets = list(combinations(range(n), 2))
    Wrows = []
    for f in facets:
        fs = frozenset(f)
        m = 0
        for i, K in enumerate(nonA):
            if fs <= K:
                m |= 1 << i
        Wrows.append(m)
    # rank
    piv = {}
    for row in Wrows:
        v = row
        while v:
            p = v.bit_length() - 1
            if p in piv:
                v ^= piv[p]
            else:
                piv[p] = v
                break
    rank = len(piv)
    dimk = len(nonA) - rank
    print("code ker_2(W restricted to 28 non-A blocks): rank =", rank,
          ", dim =", dimk)
    # weight distribution mod 4 by full enumeration if small
    if dimk <= 20:
        # nullspace basis
        work = list(Wrows)
        pivot_cols = []
        rk = 0
        for col in range(len(nonA)):
            pr = next((i for i in range(rk, len(work))
                       if (work[i] >> col) & 1), None)
            if pr is None:
                continue
            work[rk], work[pr] = work[pr], work[rk]
            for i in range(len(work)):
                if i != rk and ((work[i] >> col) & 1):
                    work[i] ^= work[rk]
            pivot_cols.append(col)
            rk += 1
        pcs = set(pivot_cols)
        basis = []
        for f in range(len(nonA)):
            if f in pcs:
                continue
            word = 1 << f
            for i, p in enumerate(pivot_cols):
                if (work[i] >> f) & 1:
                    word |= 1 << p
            basis.append(word)
        wmod4 = Counter()
        for mask in range(1 << len(basis)):
            w = 0
            mm = mask
            word = 0
            while mm:
                lb = mm & (-mm)
                word ^= basis[lb.bit_length() - 1]
                mm ^= lb
            wmod4[bin(word).count("1") % 4] += 1
        print("weights mod 4 over the whole code:", dict(sorted(wmod4.items())))

    # ---- integer lattice 4-evenness ----
    # M = facet rows + sphere rows over the 28 non-A columns
    sphere_rows = []
    for P in A:
        m = 0
        for i, K in enumerate(nonA):
            if not (K & P):
                m |= 1 << i
        sphere_rows.append(m)
    Mrows = []
    for m in Wrows + sphere_rows:
        Mrows.append([(m >> i) & 1 for i in range(len(nonA))])
    ncols = len(nonA)
    # unimodular column reduction: track U (28 x 28), columns of U are the
    # current column basis of Z^28
    U = [[1 if i == j else 0 for j in range(ncols)] for i in range(ncols)]
    Mt = [row[:] for row in Mrows]
    used = [False] * ncols

    def col_op_add(dst, src, mult):
        for row in Mt:
            row[dst] += mult * row[src]
        for row in U:
            row[dst] += mult * row[src]

    def col_swap(i, j):
        for row in Mt:
            row[i], row[j] = row[j], row[i]
        for row in U:
            row[i], row[j] = row[j], row[i]

    row_idx = 0
    for ri in range(len(Mt)):
        # eliminate row ri among unused columns
        free = [c for c in range(ncols) if not used[c]]
        # gcd elimination on entries of row ri over free columns
        while True:
            nzs = [c for c in free if Mt[ri][c] != 0]
            if len(nzs) <= 1:
                break
            nzs.sort(key=lambda c: abs(Mt[ri][c]))
            c0 = nzs[0]
            for c in nzs[1:]:
                qq = Mt[ri][c] // Mt[ri][c0]
                col_op_add(c, c0, -qq)
        nzs = [c for c in free if Mt[ri][c] != 0]
        if nzs:
            used[nzs[0]] = True
    kernel_basis = []
    for c in range(ncols):
        if not used[c]:
            vec = [U[i][c] for i in range(ncols)]
            # verify in kernel
            for row in Mrows:
                assert sum(row[i] * vec[i] for i in range(ncols)) == 0
            kernel_basis.append(vec)
    print("integer lattice Lambda: dim =", len(kernel_basis))
    norms = [sum(v * v for v in vec) % 4 for vec in kernel_basis]
    dots_even = all(
        sum(a * b for a, b in zip(u, v)) % 2 == 0
        for i, u in enumerate(kernel_basis)
        for v in kernel_basis[i + 1:]
    )
    print("basis norms mod 4:", Counter(norms),
          "; all pairwise dot products even:", dots_even)
    four_even = all(x == 0 for x in norms) and dots_even
    print("Lambda 4-even:", four_even)
    if not four_even:
        # find an explicit small-norm violator: single basis vector or sum
        viol = None
        for vec in kernel_basis:
            if sum(v * v for v in vec) % 4 != 0:
                viol = vec
                break
        if viol is None:
            for i, u in enumerate(kernel_basis):
                for v in kernel_basis[i + 1:]:
                    if sum(a * b for a, b in zip(u, v)) % 2 != 0:
                        viol = [a + b for a, b in zip(u, v)]
                        break
                if viol:
                    break
        print("example Lambda vector with norm mod 4 =",
              sum(v * v for v in viol) % 4, ":", viol)


# ---------------- r=5 CP-SAT feasibility ----------------

def r5_cpsat():
    print("=" * 72)
    print("r=5 shaped-kernel parity: CP-SAT feasibility")
    from ortools.sat.python import cp_model
    n, r = 11, 5
    X = frozenset(range(n))
    blocks_list = [frozenset(c) for c in combinations(range(n), r)]
    facets = list(combinations(range(n), r - 1))

    # base A by exact cover
    cols = {f: set() for f in facets}
    rows = {}
    for i, K in enumerate(blocks_list):
        rows[i] = [f for f in facets if frozenset(f) <= K]
        for f in rows[i]:
            cols[f].add(i)

    solution = []

    def select(rr):
        removed = []
        for j in rows[rr]:
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].remove(i)
            removed.append(cols.pop(j))
        return removed

    def deselect(rr, removed):
        for j in reversed(rows[rr]):
            cols[j] = removed.pop()
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].add(i)

    def solve_first():
        if not cols:
            return True
        c = min(cols, key=lambda k: len(cols[k]))
        for rr in sorted(cols[c]):
            solution.append(rr)
            rem = select(rr)
            if solve_first():
                return True
            deselect(rr, rem)
            solution.pop()
        return False

    assert solve_first()
    A = [blocks_list[i] for i in solution]
    A_sorted = sorted(A, key=sorted)
    spheres = [sorted(X - P) for P in A_sorted]

    # facet constraints in sphere coordinates:
    # facet F: over A-blocks P disjoint from F, coordinates (P, q) for
    # q in X - F - P.
    constraints = []
    for f in facets:
        fs = frozenset(f)
        terms = []
        for idx, P in enumerate(A_sorted):
            if P & fs:
                continue
            for q in X - fs - P:
                terms.append((idx, spheres[idx].index(q)))
        constraints.append(terms)
    m_per = Counter(len(t) // 2 for t in constraints)
    print("facet constraint sizes (#A-blocks in each 7-set):", dict(m_per))

    def build_and_solve(mode, parity, forced_total=None, time_limit=600):
        model = cp_model.CpModel()
        nsph = len(A_sorted)
        npts = r + 1
        active = [model.NewBoolVar(f"a{i}") for i in range(nsph)]
        if mode == "int":
            pos = [[model.NewBoolVar(f"p{i}_{j}") for j in range(npts)]
                   for i in range(nsph)]
            neg = [[model.NewBoolVar(f"m{i}_{j}") for j in range(npts)]
                   for i in range(nsph)]
            for i in range(nsph):
                model.Add(sum(pos[i]) == active[i])
                model.Add(sum(neg[i]) == active[i])
                for j in range(npts):
                    model.Add(pos[i][j] + neg[i][j] <= 1)
            for terms in constraints:
                model.Add(
                    sum(pos[i][j] for (i, j) in terms)
                    - sum(neg[i][j] for (i, j) in terms) == 0
                )
        else:  # GF(2)
            u = [[model.NewBoolVar(f"u{i}_{j}") for j in range(npts)]
                 for i in range(nsph)]
            for i in range(nsph):
                model.Add(sum(u[i]) == 2 * active[i])
            for k, terms in enumerate(constraints):
                aux = model.NewIntVar(0, len(terms), f"h{k}")
                model.Add(sum(u[i][j] for (i, j) in terms) == 2 * aux)
        if forced_total is not None:
            model.Add(sum(active) == forced_total)
        if parity == "odd":
            tot = model.NewIntVar(0, nsph, "tot")
            model.Add(tot == sum(active))
            half = model.NewIntVar(0, nsph // 2, "half")
            model.Add(tot == 2 * half + 1)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = 8
        status = solver.Solve(model)
        name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
                cp_model.INFEASIBLE: "UNSAT",
                cp_model.UNKNOWN: "UNKNOWN"}[status]
        witness = None
        if name == "SAT":
            witness = sum(solver.Value(a) for a in active)
        return name, witness, solver.WallTime()

    print("--- GF(2)-shaped, odd number of active spheres ---")
    res, wit, t = build_and_solve("gf2", "odd")
    print("result:", res, "active:", wit, "time: %.1fs" % t)
    gf2_res = res

    if gf2_res != "UNSAT":
        print("--- integer shaped, odd number of active spheres ---")
        res, wit, t = build_and_solve("int", "odd")
        print("result:", res, "active:", wit, "time: %.1fs" % t)
    else:
        print("integer shaped odd-active: UNSAT (implied by GF(2) UNSAT)")

    # smallest nonzero active counts (curiosity, small even values)
    for k in (2, 4, 6):
        res, wit, t = build_and_solve("int", None, forced_total=k,
                                      time_limit=120)
        print("integer shaped with exactly {} active spheres: {} "
              "({:.1f}s)".format(k, res, t))


def main():
    r3_analysis()
    r5_cpsat()
    print("=" * 72)
    print("DONE")


if __name__ == "__main__":
    main()
