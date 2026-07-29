#!/usr/bin/env python3
"""Synthetic-table generator for the sign-head programme (NOT the verifier).

May use OR-Tools CP-SAT.  All outputs are JSON files in this directory;
verify_sign_head.py (pure stdlib) re-checks every stored table independently.

Subcommands:
  k4check    per-ij slice structures at k = 4: forced/vacuous analysis
  k6perij    per-ij-only tables at k = 6 on a genuine radius-3 chart
  k8chart    CP-SAT search for k = 8 radius-3 charts (7 discordant SILS(9))
  k8joint    CP-SAT search for genuine two-sided N-tables at k = 8
             (full condition 4 + full forced trace), samples solutions
  k8peruv    per-uv-only tables at k = 8 (needs k8chart output)
  k16perij   per-ij-only tables at k = 16 Wallis
  k16peruv   per-uv-only tables at k = 16 Wallis
"""
import json
import random
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_sign_head as V  # noqa: E402


def enc_table(N):
    return {f"{u},{v}": {f"{i},{j}": x for (i, j), x in row.items()}
            for (u, v), row in N.items()}


# ------------------------------------------------------------ list colouring
def list_edge_colouring(nverts, allowed, rng, max_backtracks=200000):
    """Random proper edge colouring of K_nverts where edge e=(a,b) must take
    a colour in allowed[e] and colours are proper at vertices.  Returns dict
    e -> colour, or None on backtrack blowup."""
    edges = [(a, b) for a in range(nverts) for b in range(a + 1, nverts)]
    used = [set() for _ in range(nverts)]
    col = {}
    bt = [0]

    def choices(e):
        a, b = e
        return [c for c in allowed[e] if c not in used[a] and c not in used[b]]

    def rec(rem):
        if not rem:
            return True
        if bt[0] > max_backtracks:
            return False
        # most-constrained edge
        e = min(rem, key=lambda t: len(choices(t)))
        cs = choices(e)
        rng.shuffle(cs)
        for c in cs:
            a, b = e
            col[e] = c
            used[a].add(c)
            used[b].add(c)
            if rec([t for t in rem if t != e]):
                return True
            bt[0] += 1
            used[a].discard(c)
            used[b].discard(c)
            del col[e]
        return False

    return dict(col) if rec(edges) else None


def gen_slice(L, k, i, j, rng):
    """One per-ij slice: partition of E(K_V) into D_inf (PM of V) and D_x
    (PM of V\\{L_i^-1(x), L_j^-1(x)}).  Encoded as edge -> colour."""
    Li = [None] * (k + 1)
    Lj = [None] * (k + 1)
    for u in range(k):
        Li[L[i][u]] = u
        Lj[L[j][u]] = u
    allowed = {}
    for u in range(k):
        for v in range(u + 1, k):
            al = [k]
            for x in range(k):
                if Li[x] not in (u, v) and Lj[x] not in (u, v):
                    al.append(x)
            allowed[(u, v)] = al
    for attempt in range(50):
        col = list_edge_colouring(k, allowed, rng)
        if col is not None:
            return col
    raise RuntimeError(f"slice generation failed for pair ({i},{j})")


def gen_peruv_colouring(L, M, k, u, v, rng):
    """One condition-4 colouring N_uv of K_{k-1}."""
    nA = k - 1
    allowed = {}
    holes = [{M[i][u][v], L[i][u], L[i][v]} for i in range(nA)]
    for a in range(nA):
        for b in range(a + 1, nA):
            allowed[(a, b)] = [c for c in range(k + 1)
                              if c not in holes[a] and c not in holes[b]]
    for attempt in range(50):
        col = list_edge_colouring(nA, allowed, rng)
        if col is not None:
            return col
    return None


def perij_table_from_slices(slices, k):
    """slices: dict (i,j) -> {edge -> colour}.  Returns N table."""
    N = {}
    for u in range(k):
        for v in range(u + 1, k):
            N[(u, v)] = {}
            for (i, j), col in slices.items():
                N[(u, v)][(i, j)] = col[(u, v)]
    return N


def peruv_table_from_colourings(cols, k):
    N = {}
    for (u, v), col in cols.items():
        N[(u, v)] = {(i, j): col[(i, j)]
                     for i in range(k - 1) for j in range(i + 1, k - 1)}
    return N


# ---------------------------------------------------------------- k4check
def k4check():
    k = 4
    from itertools import permutations
    der = [p for p in permutations(range(4)) if all(p[u] != u
                                                    for u in range(4))]
    charts = []
    for rows in combinations(der, 3):
        ok = all(len({r[u] for r in rows}) == 3 for u in range(4))
        if ok:
            charts.append([list(r) for r in rows])
    feas = 0
    freedom = 0
    for L in charts:
        allok = True
        for i in range(3):
            for j in range(i + 1, 3):
                Li = [None] * 4
                Lj = [None] * 4
                for u in range(4):
                    Li[L[i][u]] = u
                    Lj[L[j][u]] = u
                forced = []
                bad = False
                for x in range(4):
                    supp = [w for w in range(4) if w not in (Li[x], Lj[x])]
                    if len(supp) != 2:
                        bad = True
                        break
                    forced.append(tuple(sorted(supp)))
                if bad or len(set(forced)) != 4:
                    allok = False
                    continue
                rest = [e for e in combinations(range(4), 2)
                        if e not in forced]
                if len(rest) != 2 or len({w for e in rest for w in e}) != 4:
                    allok = False
        if allok:
            feas += 1
    print(f"[k4check] condition-1 charts at k=4: {len(charts)}; charts whose "
          f"3 slices are all feasible: {feas}")
    print("[k4check] every finite class has a 2-vertex support, so every "
          "feasible slice is FORCED (zero freedom): per-ij tables at k=4 "
          "carry no variability -- vacuous for falsification")
    return charts, feas


# ---------------------------------------------------------------- k6perij
def k6perij(n_instances=300):
    sq = V.all_sils(7)
    fams = V.discordant_families(sq, 7, 5)
    F = [sq[t] for t in fams[0]]
    L, M = V.chart_from_sils(F, 7, 6)
    V.check_conditions_123(L, M, 6)
    rhs, _, _, _ = V.RHS_of_chart(L, M, 6)
    E, _, _ = V.E_of_chart(L, M, 6)
    hreq = E * rhs
    k = 6
    pairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    instances = []
    hvals = []
    for s in range(n_instances):
        rng = random.Random(10000 + s)
        slices = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
        N = perij_table_from_slices(slices, k)
        V.verify_perij_table(N, L, k)
        h, _ = V.hhat_of_table(N, k)
        hvals.append(h)
        if s < 40:                       # store a manageable subset
            instances.append({"tag": f"seed{10000 + s}", "seed": 10000 + s,
                              "N": enc_table(N), "Hhat": h})
    # minimal counterexample: resample ONE slice of instance seed10000
    rng = random.Random(10000)
    base_slices = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
    Nb = perij_table_from_slices(base_slices, k)
    hb, _ = V.hhat_of_table(Nb, k)
    cex = None
    for s in range(3000):
        rng2 = random.Random(500000 + s)
        sl2 = dict(base_slices)
        sl2[(0, 1)] = gen_slice(L, k, 0, 1, rng2)
        N2 = perij_table_from_slices(sl2, k)
        h2, _ = V.hhat_of_table(N2, k)
        if h2 != hb:
            instances.append({"tag": "cex_base", "seed": 10000,
                              "N": enc_table(Nb), "Hhat": hb})
            instances.append({"tag": "cex_flip", "seed": 500000 + s,
                              "N": enc_table(N2), "Hhat": h2})
            cex = ["cex_base", "cex_flip"]
            break
    out = {"kind": "perij", "k": 6, "family_index": 0, "root": 6,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": cex,
           "note": "tables satisfy ONLY the per-ij trace constraints; "
                   "the two cex instances differ only in the (0,1) slice"}
    (HERE / "falsify_k6_perij.json").write_text(json.dumps(out))
    print(f"[k6perij] chart family 0 root 6: E={E}, RHS(F)={rhs}, "
          f"H_required={hreq}")
    print(f"[k6perij] {n_instances} per-ij-only tables: Hhat "
          f"+1:{hvals.count(1)}  -1:{hvals.count(-1)}")
    print(f"[k6perij] one-slice-swap counterexample found: {cex is not None}")


# ---------------------------------------------------------------- k8chart
def sils_cyclic9():
    S = {}
    for u in range(9):
        for v in range(u + 1, 9):
            S[(u, v)] = (5 * (u + v)) % 9
    return S


def z9_starters():
    """All starters of Z_9: partitions of Z_9\\{0} into 4 pairs with
    pairwise distinct difference classes."""
    n = 9
    out = []

    def rec(rem, pairs, used):
        if not rem:
            out.append(frozenset(pairs))
            return
        x = rem[0]
        for y in rem[1:]:
            d = min((y - x) % n, (x - y) % n)
            if d in used:
                continue
            rec([z for z in rem if z not in (x, y)],
                pairs + [frozenset((x, y))], used | {d})

    rec(list(range(1, 9)), [], set())
    return out


def sils_from_starter(starter, n=9):
    """Develop a starter cyclically: S(u,v) = c iff {u-c, v-c} in starter."""
    S = {}
    for c in range(n):
        for e in starter:
            x, y = tuple(e)
            p, q = sorted(((x + c) % n, (y + c) % n))
            S[(p, q)] = c
    return S


def k8chart():
    """Enumerate all cyclic k=8 charts: 7-subsets of pairwise edge-disjoint
    Z_9 starters, developed into SILS(9)."""
    sts = z9_starters()
    print(f"[k8chart] starters of Z_9: {len(sts)}")
    cliques = []

    def expand(cur, cand):
        if len(cur) == 7:
            cliques.append(tuple(cur))
            return
        for t, s in enumerate(cand):
            expand(cur + [s], [z for z in cand[t + 1:] if not (z & s)])

    expand([], sts)
    print(f"[k8chart] pairwise-disjoint 7-subsets (cyclic charts): "
          f"{len(cliques)}")
    charts = []
    for cl in cliques:
        F = [sils_from_starter(st) for st in cl]
        sol = [{f"{u},{v}": S[(u, v)] for (u, v) in S} for S in F]
        # analyse per root
        roots = {}
        for infp in range(9):
            L, M = V.chart_from_sils(F, 9, infp)
            V.check_conditions_123(L, M, 8)
            E, neg, tot = V.E_of_chart(L, M, 8)
            rhs, _, _, _ = V.RHS_of_chart(L, M, 8)
            assert E == 1
            roots[infp] = {"E": E, "RHS_F": rhs, "H_required": E * rhs,
                           "neg_pairs": neg, "tot_pairs": tot}
        charts.append({"sils": sol, "roots": roots})
        print(f"[k8chart] chart {len(charts)-1}: RHS per root = "
              f"{{r: d['RHS_F'] for r, d in roots.items()}}"
              .replace("{r: d['RHS_F'] for r, d in roots.items()}",
                       str({r: d['RHS_F'] for r, d in roots.items()})))
    (HERE / "k8_charts.json").write_text(json.dumps(charts))
    print(f"[k8chart] saved {len(charts)} charts to k8_charts.json")
    return charts


# ---------------------------------------------------------------- k8joint
def load_k8_chart(idx):
    charts = json.loads((HERE / "k8_charts.json").read_text())
    sol = charts[idx]["sils"]
    F = [{(int(ek.split(",")[0]), int(ek.split(",")[1])): c
          for ek, c in sq.items()} for sq in sol]
    return F, charts[idx]["roots"]


def k8joint(chart_idx=0, root=8, n_solutions=20, time_cap=300.0,
            outname=None):
    from ortools.sat.python import cp_model
    F, roots = load_k8_chart(chart_idx)
    k = 8
    L, M = V.chart_from_sils(F, 9, root)
    V.check_conditions_123(L, M, k)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    hreq = E * rhs
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    idxpairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    Linv = []
    for i in range(k - 1):
        inv = [None] * (k + 1)
        for u in range(k):
            inv[L[i][u]] = u
        Linv.append(inv)

    model = cp_model.CpModel()
    nv = {}
    for (u, v) in edges:
        for (i, j) in idxpairs:
            excl = {M[i][u][v], L[i][u], L[i][v],
                    M[j][u][v], L[j][u], L[j][v]}
            dom = [c for c in range(k + 1) if c not in excl]
            nv[(u, v, i, j)] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(dom), f"n{u}{v}{i}{j}")
    # condition 4 (per-uv): at each edge uv and index i, the 6 values over j
    # are AllDifferent (domains already inside the 6-element allowed set)
    for (u, v) in edges:
        for i in range(k - 1):
            model.AddAllDifferent(
                [nv[(u, v, min(i, j), max(i, j))]
                 for j in range(k - 1) if j != i])
    # forced trace (per-ij): for each pair and vertex w, the 7 edge values
    # at w are AllDifferent (each in its 7-element allowed set)
    for (i, j) in idxpairs:
        for w in range(k):
            model.AddAllDifferent(
                [nv[(min(w, v), max(w, v), i, j)]
                 for v in range(k) if v != w])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_cap
    solver.parameters.num_search_workers = 8
    sols = []
    while len(sols) < n_solutions:
        solver.parameters.random_seed = 4000 + len(sols)
        solver.parameters.randomize_search = True
        st = solver.Solve(model)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"[k8joint] chart {chart_idx} root {root}: solver status "
                  f"{solver.StatusName(st)} after {len(sols)} solutions")
            if not sols:
                out = {"kind": "joint", "k": k, "chart_index": chart_idx,
                       "root": root, "L": L, "M": M, "E": E, "RHS_F": rhs,
                       "H_required": hreq, "instances": [],
                       "status": solver.StatusName(st)}
                name = outname or "joint_k8_trace_cond4.json"
                (HERE / name).write_text(json.dumps(out))
            break
        N = {}
        for (u, v) in edges:
            N[(u, v)] = {(i, j): solver.Value(nv[(u, v, i, j)])
                         for (i, j) in idxpairs}
        V.verify_peruv_table(N, L, M, k)
        V.verify_perij_table(N, L, k)
        h, _ = V.hhat_of_table(N, k)
        hd = V.h_direct_of_table(N, k, L)
        assert h == hd, "Hhat != H_direct on a two-sided table"
        sols.append({"tag": f"sol{len(sols)}", "N": enc_table(N),
                     "Hhat": h, "H_direct": hd})
        print(f"[k8joint] chart {chart_idx} root {root} sol {len(sols)-1}: "
              f"H = {hd} (H_required = {hreq})  "
              f"{'OK' if hd == hreq else '*** MISMATCH ***'}")
        lits = []
        for key, var in nv.items():
            b = model.NewBoolVar("")
            model.Add(var != solver.Value(var)).OnlyEnforceIf(b)
            model.Add(var == solver.Value(var)).OnlyEnforceIf(b.Not())
            lits.append(b)
        model.AddBoolOr(lits)
    if sols:
        out = {"kind": "joint", "k": k, "chart_index": chart_idx,
               "root": root, "L": L, "M": M, "E": E, "RHS_F": rhs,
               "H_required": hreq, "pairs": None, "instances": sols,
               "status": "FEASIBLE"}
        name = outname or "joint_k8_trace_cond4.json"
        (HERE / name).write_text(json.dumps(out))
        hs = [s["H_direct"] for s in sols]
        print(f"[k8joint] {len(sols)} genuine two-sided tables saved; "
              f"H values {set(hs)}; H_required = {hreq}")
    return sols


# ---------------------------------------------------------------- k8peruv
def k8peruv(chart_idx=0, root=8, n_instances=200):
    F, roots = load_k8_chart(chart_idx)
    k = 8
    L, M = V.chart_from_sils(F, 9, root)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    hreq = E * rhs
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    # feasibility of every edge problem
    rng = random.Random(1)
    for (u, v) in edges:
        if gen_peruv_colouring(L, M, k, u, v, rng) is None:
            print(f"[k8peruv] edge ({u},{v}) has NO condition-4 colouring "
                  f"-- per-uv layer infeasible for this chart/root")
            return None
    instances = []
    hvals = []
    for s in range(n_instances):
        rng = random.Random(30000 + s)
        cols = {e: gen_peruv_colouring(L, M, k, e[0], e[1], rng)
                for e in edges}
        N = peruv_table_from_colourings(cols, k)
        V.verify_peruv_table(N, L, M, k)
        h, _ = V.hhat_of_table(N, k)
        hvals.append(h)
        if s < 40:
            instances.append({"tag": f"seed{30000 + s}", "seed": 30000 + s,
                              "N": enc_table(N), "Hhat": h})
    # one-edge-recolour counterexample
    rng = random.Random(30000)
    base = {e: gen_peruv_colouring(L, M, k, e[0], e[1], rng) for e in edges}
    Nb = peruv_table_from_colourings(base, k)
    hb, _ = V.hhat_of_table(Nb, k)
    cex = None
    for s in range(3000):
        rng2 = random.Random(600000 + s)
        cols2 = dict(base)
        cols2[(0, 1)] = gen_peruv_colouring(L, M, k, 0, 1, rng2)
        N2 = peruv_table_from_colourings(cols2, k)
        h2, _ = V.hhat_of_table(N2, k)
        if h2 != hb:
            instances.append({"tag": "cex_base", "seed": 30000,
                              "N": enc_table(Nb), "Hhat": hb})
            instances.append({"tag": "cex_flip", "seed": 600000 + s,
                              "N": enc_table(N2), "Hhat": h2})
            cex = ["cex_base", "cex_flip"]
            break
    out = {"kind": "peruv", "k": k, "chart_index": chart_idx, "root": root,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": cex,
           "note": "tables satisfy ONLY condition 4 (per-uv); the two cex "
                   "instances differ only in the N_{01} colouring"}
    (HERE / "falsify_k8_peruv.json").write_text(json.dumps(out))
    print(f"[k8peruv] chart {chart_idx} root {root}: E={E}, RHS(F)={rhs}, "
          f"H_required={hreq}")
    print(f"[k8peruv] {n_instances} per-uv-only tables: Hhat "
          f"+1:{hvals.count(1)}  -1:{hvals.count(-1)}; cex={cex is not None}")


# ---------------------------------------------------------------- k8perij
def k8perij(chart_idx=0, root=8, n_instances=200):
    F, roots = load_k8_chart(chart_idx)
    k = 8
    L, M = V.chart_from_sils(F, 9, root)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    hreq = E * rhs
    pairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    instances = []
    hvals = []
    for s in range(n_instances):
        rng = random.Random(20000 + s)
        slices = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
        N = perij_table_from_slices(slices, k)
        V.verify_perij_table(N, L, k)
        h, _ = V.hhat_of_table(N, k)
        hvals.append(h)
        if s < 20:
            instances.append({"tag": f"seed{20000 + s}", "seed": 20000 + s,
                              "N": enc_table(N), "Hhat": h})
    rng = random.Random(20000)
    base = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
    Nb = perij_table_from_slices(base, k)
    hb, _ = V.hhat_of_table(Nb, k)
    cex = None
    for s in range(3000):
        rng2 = random.Random(550000 + s)
        sl2 = dict(base)
        sl2[(0, 1)] = gen_slice(L, k, 0, 1, rng2)
        N2 = perij_table_from_slices(sl2, k)
        h2, _ = V.hhat_of_table(N2, k)
        if h2 != hb:
            instances.append({"tag": "cex_base", "seed": 20000,
                              "N": enc_table(Nb), "Hhat": hb})
            instances.append({"tag": "cex_flip", "seed": 550000 + s,
                              "N": enc_table(N2), "Hhat": h2})
            cex = ["cex_base", "cex_flip"]
            break
    out = {"kind": "perij", "k": k, "chart_index": chart_idx, "root": root,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": cex,
           "note": "cyclic k=8 chart; tables satisfy ONLY the per-ij trace; "
                   "cex instances differ only in the (0,1) slice"}
    (HERE / "falsify_k8_perij.json").write_text(json.dumps(out))
    print(f"[k8perij] {n_instances} per-ij-only tables: Hhat "
          f"+1:{hvals.count(1)}  -1:{hvals.count(-1)}; H_required={hreq}; "
          f"cex={cex is not None}")


# ------------------------------------------------------------------ k8cnf
def k8cnf(chart_idx=0, root=8):
    """Independent CNF encoding of the k=8 joint (condition 4 + trace)
    problem for cadical, with DRAT proof output."""
    F, roots = load_k8_chart(chart_idx)
    k = 8
    L, M = V.chart_from_sils(F, 9, root)
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    idxpairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    var = {}

    def vid(u, v, i, j, x):
        key = (u, v, i, j, x)
        if key not in var:
            var[key] = len(var) + 1
        return var[key]

    allowed = {}
    for (u, v) in edges:
        for (i, j) in idxpairs:
            excl = {M[i][u][v], L[i][u], L[i][v],
                    M[j][u][v], L[j][u], L[j][v]}
            allowed[(u, v, i, j)] = [c for c in range(k + 1)
                                     if c not in excl]
    cls = []
    # exactly-one colour per (edge, pair)
    for (u, v) in edges:
        for (i, j) in idxpairs:
            al = allowed[(u, v, i, j)]
            cls.append([vid(u, v, i, j, x) for x in al])
            for a in range(len(al)):
                for b in range(a + 1, len(al)):
                    cls.append([-vid(u, v, i, j, al[a]),
                                -vid(u, v, i, j, al[b])])
    # condition 4: at (uv, i), each allowed colour at most once over j
    for (u, v) in edges:
        for i in range(k - 1):
            ps = [(min(i, j), max(i, j)) for j in range(k - 1) if j != i]
            for x in range(k + 1):
                lits = [vid(u, v, p[0], p[1], x) for p in ps
                        if x in allowed[(u, v, p[0], p[1])]]
                for a in range(len(lits)):
                    for b in range(a + 1, len(lits)):
                        cls.append([-lits[a], -lits[b]])
    # trace: at (pair, vertex w), each allowed colour at most once over v
    # (counts are tight, so at-most-one everywhere == exactly-one)
    for (i, j) in idxpairs:
        for w in range(k):
            es = [(min(w, v), max(w, v)) for v in range(k) if v != w]
            for x in range(k + 1):
                lits = [vid(e[0], e[1], i, j, x) for e in es
                        if x in allowed[(e[0], e[1], i, j)]]
                for a in range(len(lits)):
                    for b in range(a + 1, len(lits)):
                        cls.append([-lits[a], -lits[b]])
    path = HERE / f"k8_joint_c{chart_idx}_r{root}.cnf"
    with open(path, "w") as f:
        f.write(f"p cnf {len(var)} {len(cls)}\n")
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(f"[k8cnf] wrote {path.name}: {len(var)} vars, {len(cls)} clauses")
    print(f"[k8cnf] run: /opt/homebrew/bin/cadical {path.name} "
          f"{path.stem}.drat")


# ------------------------------------------------------------- k16 one-sided
def k16perij(n_instances=30):
    k = 16
    F = V.wallis_sils()
    L, M = V.chart_from_sils(F, 17, 16)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    hreq = E * rhs
    pairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    instances = []
    hvals = []
    for s in range(n_instances):
        rng = random.Random(40000 + s)
        slices = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
        N = perij_table_from_slices(slices, k)
        V.verify_perij_table(N, L, k)
        h, _ = V.hhat_of_table(N, k)
        hvals.append(h)
        if s < 6:
            instances.append({"tag": f"seed{40000 + s}", "seed": 40000 + s,
                              "N": enc_table(N), "Hhat": h})
        print(f"[k16perij] instance {s}: Hhat = {h}", flush=True)
    out = {"kind": "perij", "k": k, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": None,
           "note": "Wallis chart; tables satisfy ONLY the per-ij trace"}
    (HERE / "falsify_k16_perij.json").write_text(json.dumps(out))
    print(f"[k16perij] sampling done: +1:{hvals.count(1)} "
          f"-1:{hvals.count(-1)}; JSON written; hunting cex", flush=True)
    rng = random.Random(40000)
    base = {p: gen_slice(L, k, p[0], p[1], rng) for p in pairs}
    Nb = perij_table_from_slices(base, k)
    hb, _ = V.hhat_of_table(Nb, k)
    cex = None
    for s in range(500):
        rng2 = random.Random(700000 + s)
        sl2 = dict(base)
        sl2[(0, 1)] = gen_slice(L, k, 0, 1, rng2)
        N2 = perij_table_from_slices(sl2, k)
        h2, _ = V.hhat_of_table(N2, k)
        if h2 != hb:
            instances.append({"tag": "cex_base", "seed": 40000,
                              "N": enc_table(Nb), "Hhat": hb})
            instances.append({"tag": "cex_flip", "seed": 700000 + s,
                              "N": enc_table(N2), "Hhat": h2})
            cex = ["cex_base", "cex_flip"]
            break
    out = {"kind": "perij", "k": k, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": cex,
           "note": "Wallis chart; tables satisfy ONLY the per-ij trace; cex "
                   "instances differ only in the (0,1) slice"}
    (HERE / "falsify_k16_perij.json").write_text(json.dumps(out))
    print(f"[k16perij] {n_instances} tables: Hhat +1:{hvals.count(1)} "
          f"-1:{hvals.count(-1)}; H_required={hreq}; cex={cex is not None}")


def k16peruv(n_instances=30):
    k = 16
    F = V.wallis_sils()
    L, M = V.chart_from_sils(F, 17, 16)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    hreq = E * rhs
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    instances = []
    hvals = []
    for s in range(n_instances):
        rng = random.Random(50000 + s)
        cols = {}
        for e in edges:
            c = gen_peruv_colouring(L, M, k, e[0], e[1], rng)
            assert c is not None, ("k16 per-uv edge infeasible?!", e)
            cols[e] = c
        N = peruv_table_from_colourings(cols, k)
        V.verify_peruv_table(N, L, M, k)
        h, _ = V.hhat_of_table(N, k)
        hvals.append(h)
        if s < 6:
            instances.append({"tag": f"seed{50000 + s}", "seed": 50000 + s,
                              "N": enc_table(N), "Hhat": h})
        print(f"[k16peruv] instance {s}: Hhat = {h}", flush=True)
    out = {"kind": "peruv", "k": k, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": None,
           "note": "Wallis chart; tables satisfy ONLY condition 4"}
    (HERE / "falsify_k16_peruv.json").write_text(json.dumps(out))
    print(f"[k16peruv] sampling done: +1:{hvals.count(1)} "
          f"-1:{hvals.count(-1)}; JSON written; hunting cex", flush=True)
    rng = random.Random(50000)
    base = {}
    for e in edges:
        base[e] = gen_peruv_colouring(L, M, k, e[0], e[1], rng)
    Nb = peruv_table_from_colourings(base, k)
    hb, _ = V.hhat_of_table(Nb, k)
    cex = None
    for s in range(500):
        rng2 = random.Random(800000 + s)
        cols2 = dict(base)
        cols2[(0, 1)] = gen_peruv_colouring(L, M, k, 0, 1, rng2)
        N2 = peruv_table_from_colourings(cols2, k)
        h2, _ = V.hhat_of_table(N2, k)
        if h2 != hb:
            instances.append({"tag": "cex_base", "seed": 50000,
                              "N": enc_table(Nb), "Hhat": hb})
            instances.append({"tag": "cex_flip", "seed": 800000 + s,
                              "N": enc_table(N2), "Hhat": h2})
            cex = ["cex_base", "cex_flip"]
            break
    out = {"kind": "peruv", "k": k, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": hreq,
           "n_sampled": n_instances,
           "Hhat_counts": {"+1": hvals.count(1), "-1": hvals.count(-1)},
           "instances": instances, "counterexample": cex,
           "note": "Wallis chart; tables satisfy ONLY condition 4; cex "
                   "instances differ only in the N_{01} colouring"}
    (HERE / "falsify_k16_peruv.json").write_text(json.dumps(out))
    print(f"[k16peruv] {n_instances} tables: Hhat +1:{hvals.count(1)} "
          f"-1:{hvals.count(-1)}; H_required={hreq}; cex={cex is not None}")


# ----------------------------------------------------------------- k8scan
def k8scan(chart_idx=0, root=8, time_cap=60.0):
    """Condition 4 on all edges + trace on the first n index pairs, for
    growing n: locate where joint infeasibility begins."""
    from ortools.sat.python import cp_model
    F, roots = load_k8_chart(chart_idx)
    k = 8
    L, M = V.chart_from_sils(F, 9, root)
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    idxpairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    results = {}
    for n in range(len(idxpairs) + 1):
        model = cp_model.CpModel()
        nv = {}
        for (u, v) in edges:
            for (i, j) in idxpairs:
                excl = {M[i][u][v], L[i][u], L[i][v],
                        M[j][u][v], L[j][u], L[j][v]}
                dom = [c for c in range(k + 1) if c not in excl]
                nv[(u, v, i, j)] = model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(dom), "")
        for (u, v) in edges:
            for i in range(k - 1):
                model.AddAllDifferent(
                    [nv[(u, v, min(i, j), max(i, j))]
                     for j in range(k - 1) if j != i])
        for (i, j) in idxpairs[:n]:
            for w in range(k):
                model.AddAllDifferent(
                    [nv[(min(w, v), max(w, v), i, j)]
                     for v in range(k) if v != w])
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_cap
        solver.parameters.num_search_workers = 8
        st = solver.Solve(model)
        results[n] = solver.StatusName(st)
        print(f"[k8scan] trace on first {n:2d} pairs: {results[n]}",
              flush=True)
        if results[n] == "INFEASIBLE":
            break
    (HERE / "k8_scan.json").write_text(json.dumps(
        {"chart_index": chart_idx, "root": root, "results": results}))
    return results


# ---------------------------------------------------------------- k16joint
def k16joint(n_pairs=1, n_solutions=3, time_cap=300.0):
    """Strongest jointly-feasible relaxation at k=16 Wallis we can reach:
    full condition 4 on all 120 edges + the forced trace on the first
    n_pairs index pairs.  Samples solutions and their Hhat."""
    from ortools.sat.python import cp_model
    k = 16
    F = V.wallis_sils()
    L, M = V.chart_from_sils(F, 17, 16)
    E, _, _ = V.E_of_chart(L, M, k)
    rhs, _, _, _ = V.RHS_of_chart(L, M, k)
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    idxpairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    tracepairs = idxpairs[:n_pairs]
    model = cp_model.CpModel()
    nv = {}
    for (u, v) in edges:
        for (i, j) in idxpairs:
            excl = {M[i][u][v], L[i][u], L[i][v],
                    M[j][u][v], L[j][u], L[j][v]}
            dom = [c for c in range(k + 1) if c not in excl]
            nv[(u, v, i, j)] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(dom), f"n{u}_{v}_{i}_{j}")
    for (u, v) in edges:
        for i in range(k - 1):
            model.AddAllDifferent(
                [nv[(u, v, min(i, j), max(i, j))]
                 for j in range(k - 1) if j != i])
    for (i, j) in tracepairs:
        for w in range(k):
            model.AddAllDifferent(
                [nv[(min(w, v), max(w, v), i, j)]
                 for v in range(k) if v != w])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_cap
    solver.parameters.num_search_workers = 8
    sols = []
    status = None
    while len(sols) < n_solutions:
        solver.parameters.random_seed = 9000 + len(sols)
        st = solver.Solve(model)
        status = solver.StatusName(st)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"[k16joint] n_pairs={n_pairs}: status {status} after "
                  f"{len(sols)} solutions")
            break
        N = {}
        for (u, v) in edges:
            N[(u, v)] = {(i, j): solver.Value(nv[(u, v, i, j)])
                         for (i, j) in idxpairs}
        V.verify_peruv_table(N, L, M, k)
        V.verify_perij_partial(N, L, k, tracepairs)
        h, t = V.hhat_of_table(N, k)
        sols.append({"tag": f"sol{len(sols)}", "N": enc_table(N), "Hhat": h})
        print(f"[k16joint] n_pairs={n_pairs} sol {len(sols)-1}: Hhat = {h}",
              flush=True)
        lits = []
        for key, var in nv.items():
            b = model.NewBoolVar("")
            model.Add(var != solver.Value(var)).OnlyEnforceIf(b)
            model.Add(var == solver.Value(var)).OnlyEnforceIf(b.Not())
            lits.append(b)
        model.AddBoolOr(lits)
    out = {"kind": "joint", "k": k, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": E * rhs,
           "pairs": [list(p) for p in tracepairs], "instances": sols,
           "status": status,
           "note": f"full condition 4 + trace on {n_pairs} pairs"}
    (HERE / "joint_k16_partial.json").write_text(json.dumps(out))
    hs = [s["Hhat"] for s in sols]
    print(f"[k16joint] saved {len(sols)} instances; Hhat values {set(hs)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    args = sys.argv[2:]
    if cmd == "k4check":
        k4check()
    elif cmd == "k6perij":
        k6perij()
    elif cmd == "k8chart":
        k8chart()
    elif cmd == "k8joint":
        kw = dict(a.split("=") for a in args)
        k8joint(chart_idx=int(kw.get("chart", 0)), root=int(kw.get("root", 8)),
                n_solutions=int(kw.get("n", 20)),
                time_cap=float(kw.get("cap", 300)),
                outname=kw.get("out"))
    elif cmd == "k8peruv":
        kw = dict(a.split("=") for a in args)
        k8peruv(chart_idx=int(kw.get("chart", 0)), root=int(kw.get("root", 8)))
    elif cmd == "k8perij":
        kw = dict(a.split("=") for a in args)
        k8perij(chart_idx=int(kw.get("chart", 0)), root=int(kw.get("root", 8)))
    elif cmd == "k8cnf":
        kw = dict(a.split("=") for a in args)
        k8cnf(chart_idx=int(kw.get("chart", 0)), root=int(kw.get("root", 8)))
    elif cmd == "k8scan":
        k8scan()
    elif cmd == "k16perij":
        k16perij()
    elif cmd == "k16peruv":
        k16peruv()
    elif cmd == "k16joint":
        kw = dict(a.split("=") for a in args)
        k16joint(n_pairs=int(kw.get("pairs", 1)),
                 n_solutions=int(kw.get("n", 3)),
                 time_cap=float(kw.get("cap", 300)))
    else:
        print(__doc__)
        sys.exit(2)
