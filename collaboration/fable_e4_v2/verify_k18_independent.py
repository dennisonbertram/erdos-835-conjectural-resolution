#!/usr/bin/env python3
"""Independent static verification of the claimed actual-edge K18 in the
five-statistic F_32 quotient (e1, e2, e3, e4, e8 + e1^8) of J(32,16).

This checker was written from scratch and shares no code with
evidence/f32_five_statistic_k18_verifier.py.  It contains only the claim
data: 18 (x, lambda) pairs and three 15-set masks.  Everything else is
recomputed from first principles:

  * GF(32) = F_2[a]/(a^5 + a^2 + 1), element z encoded as a 5-bit integer
    with bit i the coefficient of a^i; a 32-bit mask has bit z set iff the
    field element z belongs to the set.
  * Field multiplication is implemented twice (shift/reduce and log tables
    from the generator a) and the two are compared on all 1024 pairs.
  * Every elementary symmetric coefficient is recomputed from the roots of
    each actual 15-set and each exchanged 16-set.

Checks performed:
  1. field sanity: a has multiplicative order 31 (so the ring is a field);
  2. each mask encodes a 15-set;
  3. for each mask B and each claimed x outside B, the 16-set B + {x} has
     sigma = (1 + x, x, 0, 0, lambda_x) with lambda recomputed through e8;
  4. the three sets M_i = X ∩ B_i of claimed parameters NOT realized by
     mask B_i are pairwise disjoint, so no unordered pair of parameters
     can be missed by all three masks;
  5. explicitly, every one of the 153 unordered pairs is covered by a mask
     whose two completions intersect in exactly 15 points (an actual edge);
  6. the 18 states are pairwise distinct;
  7. structural cross-check: each mask has (e1,e2,e3,e4) = (1,0,0,0), all
     three share (e7, e8), and lambda(x) = (e8 + 1) + e7 * x + x^8 holds
     for all 18 claimed pairs.
"""

REDUCE = 0x25  # a^5 = a^2 + 1


def gmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x20:
            a ^= REDUCE
        b >>= 1
    return r


def build_tables():
    log = {}
    exp = []
    z = 1
    for i in range(31):
        exp.append(z)
        assert z not in log
        log[z] = i
        z = gmul(z, 2)
    assert z == 1, "generator a does not have order 31"
    return log, exp


LOG, EXP = build_tables()


def gmul_table(a, b):
    if a == 0 or b == 0:
        return 0
    return EXP[(LOG[a] + LOG[b]) % 31]


def pow8(a):
    for _ in range(3):
        a = gmul(a, a)
    return a


def epoly(mask, deg=8):
    """Coefficients e_0..e_deg of prod_{z in mask} (1 + z t) over GF(32)."""
    e = [0] * (deg + 1)
    e[0] = 1
    for z in range(32):
        if mask >> z & 1:
            for j in range(deg, 0, -1):
                e[j] ^= gmul(z, e[j - 1])
    return e


CLAIM = [(31, 31), (26, 28), (25, 4), (24, 9), (23, 14), (22, 3),
         (19, 0), (17, 21), (16, 24), (13, 22), (12, 27), (11, 13),
         (10, 0), (9, 24), (6, 31), (2, 17), (1, 9), (0, 4)]
MASKS = [0x7975CD00, 0x149693B9, 0xFA3041BA]


def main():
    # 1. field sanity + independent multiplication cross-check
    for a in range(32):
        for b in range(32):
            assert gmul(a, b) == gmul_table(a, b)
            assert gmul(a, b) == gmul(b, a)
    assert all(gmul(1, z) == z for z in range(32))

    xs = [x for x, _ in CLAIM]
    lam = dict(CLAIM)
    assert len(set(xs)) == 18

    # 6. distinct states: distinct x gives distinct e2 coordinate
    #    (and distinct e1 = 1 + x); nothing more is needed.

    realized = []
    for mi, B in enumerate(MASKS):
        assert bin(B).count("1") == 15, f"mask {mi} is not a 15-set"
        out = [x for x in xs if not (B >> x & 1)]
        for x in out:
            S = B | (1 << x)
            assert bin(S).count("1") == 16
            f = epoly(S)
            assert f[1] == 1 ^ x, (mi, x, "e1")
            assert f[2] == x, (mi, x, "e2")
            assert f[3] == 0, (mi, x, "e3")
            assert f[4] == 0, (mi, x, "e4")
            assert f[8] ^ pow8(f[1]) == lam[x], (mi, x, "lambda")
        realized.append(set(out))
        print(f"mask {mi}: 15-set, realizes {len(out)} claimed states, "
              f"missing x = {sorted(set(xs) - set(out))}")

    # 4. the three miss-sets M_i = X ∩ B_i are pairwise disjoint, so no
    #    2-element subset of X can meet all three (expected sizes 5, 6, 3)
    missing = [set(xs) - r for r in realized]
    assert sorted(len(m) for m in missing) == [3, 5, 6]
    for i in range(3):
        for j in range(i + 1, 3):
            assert not (missing[i] & missing[j])

    # 5. all 153 pairs covered by an actual edge
    edges = 0
    for i in range(18):
        for j in range(i + 1, 18):
            x, y = xs[i], xs[j]
            wit = [mi for mi in range(3)
                   if x in realized[mi] and y in realized[mi]]
            assert wit, f"pair ({x},{y}) uncovered"
            B = MASKS[wit[0]]
            Sx, Sy = B | (1 << x), B | (1 << y)
            assert Sx != Sy and bin(Sx & Sy).count("1") == 15
            edges += 1
    assert edges == 153

    # 7. structural cross-check on the masks themselves
    taus = [epoly(B) for B in MASKS]
    for t in taus:
        assert t[1] == 1 and t[2] == 0 and t[3] == 0 and t[4] == 0
    d = taus[0][7]
    c = taus[0][8] ^ 1
    assert all(t[7] == d and t[8] ^ 1 == c for t in taus)
    for x, l in CLAIM:
        assert l == c ^ gmul(d, x) ^ pow8(x)
    print(f"masks share (e1..e4) = (1,0,0,0), e7 = {d}, e8 = {c ^ 1}; "
          f"lambda(x) = {c} + {d}*x + x^8 matches all 18 pairs")

    print("PASS: all 153 pairs of the 18 five-statistic states are "
          "actual Johnson edges; the K18 is verified")


if __name__ == "__main__":
    main()
