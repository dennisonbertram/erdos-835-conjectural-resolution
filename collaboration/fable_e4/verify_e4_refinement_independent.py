#!/usr/bin/env python3
"""Independent replay of the e4-refinement decision (see PROOF.md).

Deliberately different from remote_run_e4.py / enumerate_e4_refinement.py:

  * R-family enumeration: depth-first search over the 32 field elements
    with exact suffix-reachability pruning (no meet-in-the-middle);
  * vertex labels: for each R and a in R the checker BUILDS the 16-set
    R \\ {a} and computes e1..e4 and e8+e1^8 from scratch from the
    definition (no lambda quartic, no deletion identities);
  * K18 decision: peeling by distinct-first-coordinate span, then a
    fibre-based branch and bound (no Tomita colouring bound);
  * every r in F_32 is decided directly (the scaling isomorphism of
    PROOF.md Theorem C is NOT assumed).

Agreement of this script's counts and verdicts with remote_run_e4.py is
the double-implementation guarantee behind the computational claims in
JUDGMENT.md.
"""

from itertools import combinations

MODULUS = 0b100101  # X^5 + X^2 + 1


def _mul(left: int, right: int) -> int:
    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    return raw


MUL = tuple(tuple(_mul(a, b) for b in range(32)) for a in range(32))


def fpow(a: int, e: int) -> int:
    r = 1
    while e:
        if e & 1:
            r = MUL[r][a]
        a = MUL[a][a]
        e >>= 1
    return r


def trace(a: int) -> int:
    t, c = 0, a
    for _ in range(5):
        t ^= c
        c = MUL[c][c]
    return t


def layer(a: int) -> int:
    return int(a == 0 or trace(a) == 1)


def stats8(points):
    """[e_0..e_8] of an iterable of field elements, from the definition."""
    e = [1] + [0] * 8
    for p in points:
        for d in range(8, 0, -1):
            e[d] ^= MUL[p][e[d - 1]]
    return e


def enumerate_family():
    """All 17-sets R with e1=e2=e3=0, by DFS with suffix reachability.

    SUF[i][k] = set of (e1,e2,e3) over all k-subsets of {i,...,31}.
    """
    SUF = [[set() for _ in range(18)] for _ in range(33)]
    SUF[32][0].add((0, 0, 0))
    for i in range(31, -1, -1):
        for k in range(0, 18):
            acc = set(SUF[i + 1][k])
            if k >= 1:
                for c1, c2, c3 in SUF[i + 1][k - 1]:
                    acc.add((c1 ^ i, c2 ^ MUL[i][c1], c3 ^ MUL[i][c2]))
            SUF[i][k] = acc

    family = []

    def dfs(i, size, p1, p2, p3, chosen_mask):
        if size == 17:
            if p1 == 0 and p2 == 0 and p3 == 0:
                family.append(chosen_mask)
            return
        if i == 32:
            return
        need = 17 - size
        # stats the suffix subset must contribute for e1=e2=e3(R)=0
        b1 = p1
        b2 = p2 ^ MUL[p1][p1]
        b3 = p3 ^ MUL[p2][b1] ^ MUL[p1][b2]
        if (b1, b2, b3) not in SUF[i][need]:
            return
        dfs(i + 1, size + 1,
            p1 ^ i, p2 ^ MUL[i][p1], p3 ^ MUL[i][p2],
            chosen_mask | (1 << i))
        dfs(i + 1, size, p1, p2, p3, chosen_mask)

    dfs(0, 0, 0, 0, 0, 0)
    return family


def fibre_max_clique(vertices, adj, pool, initial_best=0):
    """Exact max clique on `pool` via branch and bound over e1-fibres.

    Bound: |chosen| + number of later fibres still holding a vertex
    compatible with everything chosen."""
    classes = {}
    for v in pool:
        classes.setdefault(vertices[v][0], []).append(v)
    order = sorted(classes, key=lambda a: len(classes[a]))
    best = [initial_best, ()]

    def bb(idx, chosen):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = tuple(chosen)
        compatible = 0
        live = []
        for k in range(idx, len(order)):
            cands = [v for v in classes[order[k]]
                     if all(v in adj[u] for u in chosen)]
            if cands:
                compatible += 1
            live.append(cands)
        if len(chosen) + compatible <= best[0]:
            return
        if idx == len(order):
            return
        for v in live[0]:
            chosen.append(v)
            bb(idx + 1, chosen)
            chosen.pop()
        bb(idx + 1, chosen)

    bb(0, [])
    return best[0], [vertices[v] for v in best[1]]


def peel_span(vertices, adj, need):
    """Remove vertices whose surviving neighbours span < `need` distinct
    first coordinates; survivors contain every clique on `need`+1 fibres."""
    alive = set(range(len(vertices)))
    changed = True
    while changed:
        changed = False
        for v in list(alive):
            span = {vertices[u][0] for u in adj[v] & alive}
            if len(span) < need:
                alive.discard(v)
                changed = True
    return alive


def main() -> None:
    family = enumerate_family()
    per_r = {r: [] for r in range(32)}
    for mask in family:
        points = [p for p in range(32) if mask >> p & 1]
        assert len(points) == 17
        e = stats8(points)
        assert e[1] == e[2] == e[3] == 0
        per_r[e[4]].append(points)
    counts = [len(per_r[r]) for r in range(32)]
    print("independent R-family counts per r:", counts,
          "total:", sum(counts), flush=True)

    omegas = []
    h_omegas = []
    for r in range(32):
        vid, vertices = {}, []
        member_lists = []
        for points in per_r[r]:
            members = []
            for a in points:
                # label from the actual deletion 16-set, from scratch
                S = [p for p in points if p != a]
                eS = stats8(S)
                assert eS[1] == a
                assert eS[2] == fpow(a, 2)
                assert eS[3] == fpow(a, 3)
                assert eS[4] == fpow(a, 4) ^ r
                key = (a, eS[8] ^ fpow(a, 8))
                if key not in vid:
                    vid[key] = len(vertices)
                    vertices.append(key)
                members.append(vid[key])
            member_lists.append(members)
        adj = [set() for _ in range(len(vertices))]
        n_edges = 0
        for members in member_lists:
            for i, j in combinations(members, 2):
                if j not in adj[i]:
                    n_edges += 1
                adj[i].add(j)
                adj[j].add(i)

        # K18 decision: peel to the 17-span core first
        core = peel_span(vertices, adj, 17)
        if not core:
            # no clique on >= 18 fibres exists; any R gives a K17
            omega = 17 if per_r[r] else 0
            note = " (K18-peel empty)"
        else:
            om, wit = fibre_max_clique(vertices, adj, core, initial_best=17)
            if om > 17:
                omega, note = om, " K18-OR-LARGER FOUND"
                print("   witness:", sorted(wit), flush=True)
            else:
                omega, note = 17, " (core searched, no K18)"
        omegas.append(omega)
        print(f"r={r:2d}: |R_r|={len(per_r[r]):4d} "
              f"verts={len(vertices):4d} edges={n_edges:6d} "
              f"omega={omega}{note}", flush=True)

        # task 4: layer-pattern subgraph H_r (at most 32 vertices)
        keep = {vid[(a, layer(a))] for a in range(32) if (a, layer(a)) in vid}
        hom, hwit = fibre_max_clique(vertices, adj, keep)
        h_omegas.append(hom)

    print("omega(G_r) for r=0..31:", omegas, flush=True)
    print("omega(H_r) for r=0..31:", h_omegas, flush=True)
    print("max omega(G_r):", max(omegas),
          " max omega(H_r):", max(h_omegas), flush=True)
    print("INDEPENDENT-REPLAY-COMPLETE", flush=True)


if __name__ == "__main__":
    main()
