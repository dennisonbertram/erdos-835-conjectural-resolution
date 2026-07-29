#!/usr/bin/env python3
"""Settles the one open lever in IDEAS.md section B.

NOT RUN when written (code execution was unavailable in that session).

For every 1-factorization of K_n (n = 4, 6, 8) build the symmetric Latin
square L (off-diagonal entry = colour of the edge, diagonal = the extra symbol
n-1) and compute the row parity

    eps_row = prod_x sgn(row x as a bijection [n] -> symbols).

QUESTION: is eps_row constant over all 1-factorizations of K_n?

  constant     -> IDEAS.md section B route is fully closed.
  not constant -> eps_row is a nontrivial invariant attached to every
                  (k-2)-set of a hypothetical tight colouring, and its
                  consistency across overlapping (k-2)-sets is a new finite
                  obstruction to attack.

Also prints the number of 1-factorizations found, which is a self-check
against the known values 1, 6, 6240 for n = 4, 6, 8.

Stdlib only.
"""

KNOWN_COUNTS = {4: 1, 6: 6, 8: 6240}


def perm_sign(seq):
    """Sign of seq viewed as a permutation of range(len(seq))."""
    n = len(seq)
    seen = [False] * n
    sign = 1
    for i in range(n):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = seq[j]
            length += 1
        if length % 2 == 0:
            sign = -sign
    return sign


def _complete(verts, used, acc, out):
    """All perfect matchings of `verts` avoiding edges in `used`."""
    if not verts:
        out.append(tuple(acc))
        return
    v = verts[0]
    for i in range(1, len(verts)):
        w = verts[i]
        if (v, w) in used:
            continue
        acc.append((v, w))
        _complete(verts[1:i] + verts[i + 1:], used, acc, out)
        acc.pop()


def one_factorizations(n):
    """Each unordered 1-factorization of K_n exactly once.

    Canonical factor order: factor c matches vertex 0 to the smallest partner
    still available, so the partners of vertex 0 increase with c.
    """
    used, factors, result = set(), [], []

    def rec(c):
        if c == n - 1:
            result.append([tuple(f) for f in factors])
            return
        w = min(x for x in range(1, n) if (0, x) not in used)
        rest = [x for x in range(1, n) if x != w]
        cand = []
        _complete(rest, used, [], cand)
        for m in cand:
            full = ((0, w),) + m
            used.update(full)
            factors.append(full)
            rec(c + 1)
            factors.pop()
            used.difference_update(full)

    rec(0)
    return result


def row_parity(n, factors):
    L = [[n - 1] * n for _ in range(n)]
    for c, f in enumerate(factors):
        for a, b in f:
            L[a][b] = c
            L[b][a] = c
    total = 1
    for x in range(n):
        total *= perm_sign(L[x])
    return total


def symbol_parity(n, factors):
    """Independent check of the closed form proved in IDEAS.md section B:
    eps_symbol = (-1)**((p+1)/2) with p+1 = n, i.e. (-1)**(n//2)."""
    total = 1
    for f in factors:
        pos = list(range(n))
        for a, b in f:
            pos[a], pos[b] = b, a
        total *= perm_sign(pos)
    return total  # identity symbol contributes +1


def main():
    ok = True
    for n in (4, 6, 8):
        fs = one_factorizations(n)
        cnt = len(fs)
        exp = KNOWN_COUNTS[n]
        print(f"\n=== K_{n} ===")
        print(f"  1-factorizations found: {cnt} (known {exp}) -> "
              f"{'PASS' if cnt == exp else 'FAIL'}")
        ok &= cnt == exp

        rows = {}
        syms = set()
        for f in fs:
            r = row_parity(n, f)
            rows[r] = rows.get(r, 0) + 1
            syms.add(symbol_parity(n, f))
        print(f"  eps_row value -> count: {rows}")
        print(f"  eps_row CONSTANT: {'YES' if len(rows) == 1 else 'NO'}")
        pred = (-1) ** (n // 2)
        print(f"  eps_symbol values: {syms}; predicted {pred} -> "
              f"{'PASS' if syms == {pred} else 'FAIL'}")
        ok &= syms == {pred}

    print("\nOVERALL:", "PASS" if ok else "FAIL")
    print("Interpretation: see IDEAS.md section B.")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
