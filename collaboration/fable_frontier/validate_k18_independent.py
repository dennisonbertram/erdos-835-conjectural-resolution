#!/usr/bin/env python3
"""Independent re-verification of the (e1, e8+e1^8) actual-edge K18.

Third implementation, deliberately different from
evidence/f32_two_statistic_k18_verifier.py:

  * field multiplication via discrete-log/antilog tables over the
    generator alpha (integer 2), not polynomial long division;
  * elementary symmetric coefficients read off a full degree-16 root
    polynomial, with an extra self-check that the polynomial vanishes at
    every element of the set;
  * certificate data re-entered from the HEX table in
    evidence/f32_two_statistic_k18_obstruction.md and cross-checked
    against the decimal masks embedded in the repo verifier;
  * the trace function is computed twice (definition vs the bit formula
    Tr(x) = b0 XOR b3 proved in PROOF.md Lemma 4) and compared.

Authored 2026-07-25 in a session where python execution was
permission-blocked, so this file has NOT been executed yet.  Run:

    python3 -B collaboration/fable_frontier/validate_k18_independent.py

Expected on success: several PASS lines ending in "ALL CHECKS PASS".
Any assertion failure means the K18 certificate (or this checker) is
wrong and must be investigated before the certificate is cited.
"""

from itertools import combinations

MOD = 0b100101  # alpha^5 + alpha^2 + 1


def build_tables():
    powers = []
    x = 1
    for _ in range(31):
        powers.append(x)
        x <<= 1
        if x & 32:
            x ^= MOD
    assert x == 1, "alpha^31 != 1: reduction rule broken"
    log = {}
    for i, v in enumerate(powers):
        assert 1 <= v < 32 and v not in log
        log[v] = i
    assert len(log) == 31
    return powers, log


POWERS, LOG = build_tables()


def mul(a, b):
    if a == 0 or b == 0:
        return 0
    return POWERS[(LOG[a] + LOG[b]) % 31]


def fpow(a, e):
    if a == 0:
        return 0 if e else 1
    return POWERS[(LOG[a] * e) % 31]


def trace_def(x):
    t, c = 0, x
    for _ in range(5):
        t ^= c
        c = mul(c, c)
    assert t in (0, 1)
    return t


def trace_bits(x):
    return (x ^ (x >> 3)) & 1


def root_poly(points):
    """Coefficients c[j] = e_j of prod_{s in points}(X + s), descending."""
    c = [1]
    for s in points:
        c = [1] + [c[j] ^ mul(s, c[j - 1]) for j in range(1, len(c))] \
            + [mul(s, c[-1])]
    return c


def poly_eval(c, x):
    val = 0
    for coeff in c:
        val = mul(val, x) ^ coeff
    return val


def statistic(points):
    """(e1, e8 + e1^8) of a 16-set, with a root self-check."""
    pts = sorted(points)
    assert len(pts) == 16
    c = root_poly(pts)
    assert len(c) == 17
    for s in pts:
        assert poly_eval(c, s) == 0, "root check failed"
    e1 = c[1]
    return (e1, c[8] ^ fpow(e1, 8))


BASE_ROOTS = (0, 1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30)
EXTERNAL_STATE = (29, 27)

# (a, hex mask, x, y) exactly as printed in the markdown certificate table.
MD_ROWS = (
    (0, "0x7913db25", 9, 20),
    (1, "0xa3b106bf", 1, 29),
    (3, "0xd197f846", 24, 6),
    (5, "0xa62abb4e", 17, 9),
    (7, "0x61769bb8", 4, 30),
    (8, "0xe6c12dbc", 5, 16),
    (10, "0xe74526da", 16, 7),
    (12, "0x2d8da91f", 11, 26),
    (14, "0x014bf9bd", 22, 5),
    (17, "0xd12fd05e", 14, 2),
    (19, "0x29baa4bb", 21, 27),
    (21, "0xec927533", 23, 31),
    (23, "0xcde2d662", 6, 12),
    (24, "0x6f032d5d", 29, 24),
    (26, "0x014bf9bd", 2, 5),
    (28, "0xf7513256", 28, 29),
    (30, "0x42e9c8f7", 7, 4),
)

# Decimal masks and deletions embedded in the repo verifier, for
# cross-checking that the two documents describe one certificate.
REPO_MASKS = (
    2031344421, 2746287807, 3516397638, 2787818318, 1635163064,
    3871419836, 3880068826, 764258591, 21756349, 3509571678,
    700097723, 3969021235, 3454195298, 1862479197, 21756349,
    4149293654, 1122617591,
)
REPO_DELETIONS = (
    (9, 20), (1, 29), (24, 6), (17, 9), (4, 30), (5, 16), (16, 7),
    (11, 26), (22, 5), (14, 2), (21, 27), (23, 31), (6, 12), (29, 24),
    (2, 5), (28, 29), (7, 4),
)


def mask_points(mask):
    pts = frozenset(j for j in range(32) if mask >> j & 1)
    assert len(pts) == 17
    return pts


def main():
    # 1. Field and trace cross-checks.
    for x in range(32):
        assert trace_def(x) == trace_bits(x), x
    print("PASS field tables and trace bit formula (32/32 elements)")

    # 2. Base set is {0} plus the trace-one coset.
    base = frozenset(BASE_ROOTS)
    assert len(base) == 17
    assert base == {0} | {x for x in range(1, 32) if trace_def(x) == 1}
    print("PASS base 17-set equals {0} union {Tr=1}")

    # 3. The K17: deletion statistics and pairwise adjacency.
    edges = set()
    base_states = []
    for a in BASE_ROOTS:
        st = statistic(base - {a})
        assert st == (a, 1), (a, st)
        base_states.append(st)
    for u, v in combinations(BASE_ROOTS, 2):
        assert len((base - {u}) & (base - {v})) == 15
        edges.add(frozenset(((u, 1), (v, 1))))
    print("PASS K17: 17 deletion states (a,1), 136 actual edges")

    # 4. Markdown table vs repo verifier data.
    assert len(MD_ROWS) == 17
    for i, (a, hexmask, x, y) in enumerate(MD_ROWS):
        assert int(hexmask, 16) == REPO_MASKS[i], (i, hexmask)
        assert (x, y) == REPO_DELETIONS[i], (i, x, y)
        assert a == BASE_ROOTS[i]
    print("PASS markdown hex table matches repo verifier masks (17/17)")

    # 5. The 17 extension edges to EXTERNAL_STATE.
    for a, hexmask, x, y in MD_ROWS:
        pts = mask_points(int(hexmask, 16))
        assert x in pts and y in pts and x != y
        s_base = pts - {x}
        s_ext = pts - {y}
        assert statistic(s_base) == (a, 1), (a, hexmask)
        assert statistic(s_ext) == EXTERNAL_STATE, (a, hexmask)
        assert len(s_base & s_ext) == 15
        # all 17 deletion states of this 17-set must be distinct, so the
        # two statistics above really come from two different 16-sets
        states = {statistic(pts - {z}) for z in pts}
        assert len(states) == 17
        edges.add(frozenset(((a, 1), EXTERNAL_STATE)))
    print("PASS 17 extension edges to state (29, 27)")

    # 6. Assemble the K18.
    vertices = set(base_states) | {EXTERNAL_STATE}
    assert len(vertices) == 18
    assert len(edges) == 153
    for u, v in combinations(sorted(vertices), 2):
        assert frozenset((u, v)) in edges
    print("PASS K18 assembled: 18 distinct quotient states, 153/153 edges")

    print("ALL CHECKS PASS")
    print("consequence: no proper 17-colouring of J(32,16) has the form")
    print("  c(S) = G(e1(S), e8(S) + e1(S)^8)  for any G with <= 17 values")


if __name__ == "__main__":
    main()
