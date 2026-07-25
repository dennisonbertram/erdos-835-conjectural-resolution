#!/usr/bin/env python3
"""Decide feasibility of the projected-idempotence cubic system at k=4.

System C_p on J(2k,k), p = k+1 prime, d = C(2k,k)/p, K = ker W_{k-1,k}:

    q_a in K (a in F_p),  sum_a q_a = 0,
    Gram:   <q_a,q_b> = p*d*(p-1) if a=b else -p*d,
    cubic:  P_K(q_a q_b) = (p-2) q_a   if a=b,
                         = -q_a - q_b  if a != b.

PROOF.md (this directory) shows: (i) the cubic forces the Gram shape up to
one scalar; (ii) every polarization/contraction of C_p against the span of
the q_a is consistently realized by a weighted p-point model, so no such
argument can refute C_p at any prime; (iii) the entire residual content of
C_p is one decision problem — does (K, P_K∘mult) contain a beta-closed
reduced-p-point subalgebra at norm nu = p*d*(p-1)?

This script decides that numerically at the FALSE parameter k=4
(J(8,4), p=5: no tight 5-colouring exists, verify_k4.py), after validating
the machinery at the TRUE parameter k=2 (J(4,2), p=3), where the actual
tight colouring must give residual ~0.

Interpretation at k=4:
  * best residual ~ machine zero (relative < 1e-24) reproducibly:
    C_5 is numerically FEASIBLE although no colouring exists, so the cubic
    system alone cannot separate true from false parameters; the route is
    then closed pending an exact certificate (rational reconstruction or
    interval Newton around the found point).
  * best residual floor stays large (relative > 1e-10) over all restarts:
    strong evidence C_5 is INFEASIBLE; the cubic detects the k=4
    obstruction and becomes the leading candidate for a p-uniform
    nonexistence attack; the follow-up is an exact infeasibility proof via
    the S_8-equivariant decomposition of Sym^2(K) -> K.
Neither numerical outcome is a proof by itself; either is decisive for
attack selection.

Authored 2026-07-25 in a session where python execution was blocked, so
this file has NOT been executed yet.  Requires numpy; uses scipy if
available (falls back to random search + local descent otherwise).  Run:

    python3 -B collaboration/fable_frontier/decide_cubic_embedding_k4.py

Options: --restarts N (default 200), --seed S, --maxiter M.
"""

import argparse
import itertools
import math

import numpy as np

try:
    from scipy.optimize import minimize as _scipy_minimize
except Exception:  # pragma: no cover
    _scipy_minimize = None


def johnson_kernel(n, k):
    """Orthonormal basis (columns) of ker W_{k-1,k}(n)."""
    sets_k = list(itertools.combinations(range(n), k))
    sets_km1 = list(itertools.combinations(range(n), k - 1))
    W = np.zeros((len(sets_km1), len(sets_k)))
    for r, t in enumerate(sets_km1):
        ts = set(t)
        for c, s in enumerate(sets_k):
            if ts <= set(s):
                W[r, c] = 1.0
    dim = len(sets_k) - len(sets_km1)
    _, sv, vt = np.linalg.svd(W)
    rank = int(np.sum(sv > 1e-9))
    null = vt[rank:]
    assert null.shape[0] == dim, (null.shape, dim)
    return sets_k, W, null.T  # U: |X| x dim, orthonormal columns


def beta_tensor(U):
    """B[i, j, :] = U-coordinates of P_K(u_i * u_j)."""
    m = U.shape[1]
    B = np.zeros((m, m, m))
    for i in range(m):
        for j in range(i, m):
            coords = U.T @ (U[:, i] * U[:, j])
            B[i, j] = coords
            B[j, i] = coords
    return B


def helmert_rows(p):
    """p rows h_a in R^{p-1} with h_a . h_b = delta_ab - 1/p."""
    A = np.eye(p) - np.full((p, p), 1.0 / p)
    _, sv, vt = np.linalg.svd(A)
    V = vt[: p - 1]
    H = A @ V.T
    assert np.allclose(H @ H.T, A, atol=1e-12)
    return H


def cubic_residual(B, X, p):
    """Sum of squared cubic residuals; X columns are q_a in K-coords."""
    total = 0.0
    norm = 0.0
    for a in range(p):
        for b in range(a, p):
            v = np.einsum("ijl,i,j->l", B, X[:, a], X[:, b])
            rhs = (p - 2) * X[:, a] if a == b else -X[:, a] - X[:, b]
            total += float(np.sum((v - rhs) ** 2))
            norm += float(np.sum(rhs ** 2))
    return total, norm


def make_objective(B, H, s, p, m):
    def phi(flat):
        M = flat.reshape(m, p - 1)
        Q, _ = np.linalg.qr(M)
        X = s * (Q @ H.T)
        total, _ = cubic_residual(B, X, p)
        return total

    return phi


def local_descent(phi, x0, maxiter, rng):
    """Crude finite-difference descent fallback when scipy is absent."""
    x = x0.copy()
    fx = phi(x)
    step = 1e-2
    h = 1e-6
    for _ in range(maxiter):
        g = np.zeros_like(x)
        for i in range(x.size):
            e = np.zeros_like(x)
            e[i] = h
            g[i] = (phi(x + e) - fx) / h
        gn = np.linalg.norm(g)
        if gn < 1e-14:
            break
        improved = False
        for _ in range(30):
            cand = x - step * g / gn
            fc = phi(cand)
            if fc < fx:
                x, fx = cand, fc
                step *= 1.3
                improved = True
                break
            step *= 0.5
        if not improved:
            break
    return x, fx


def sanity_check_k2(verbose=True):
    """The true tight 3-colouring of J(4,2) must satisfy C_3 exactly."""
    p, k = 3, 2
    sets_k, W, U = johnson_kernel(2 * k, k)
    d = math.comb(2 * k, k) // p
    B = beta_tensor(U)
    classes = [
        {(0, 1), (2, 3)},
        {(0, 2), (1, 3)},
        {(0, 3), (1, 2)},
    ]
    X = np.zeros((U.shape[1], p))
    for a, cls in enumerate(classes):
        q = np.array([p * (s in cls) - 1.0 for s in sets_k])
        assert np.allclose(W @ q, 0.0, atol=1e-9), "q_a not in kernel"
        y = U.T @ q
        assert np.allclose(U @ y, q, atol=1e-9), "reconstruction failed"
        X[:, a] = y
    gram = X.T @ X
    nu = p * d * (p - 1)
    target = np.full((p, p), -p * d, dtype=float)
    np.fill_diagonal(target, nu)
    assert np.allclose(gram, target, atol=1e-8), gram
    total, norm = cubic_residual(B, X, p)
    assert total / norm < 1e-20, (total, norm)
    if verbose:
        print("PASS k=2 machinery check: true colouring satisfies C_3")
        print("     relative cubic residual = %.3e" % (total / norm))
    return True


def search(p, k, restarts, maxiter, seed, label):
    sets_k, _, U = johnson_kernel(2 * k, k)
    m = U.shape[1]
    d = math.comb(2 * k, k) // p
    s = math.sqrt(p * p * d)  # ||q_a||^2 = s^2 (1 - 1/p) = p d (p-1)
    B = beta_tensor(U)
    H = helmert_rows(p)
    phi = make_objective(B, H, s, p, m)
    rng = np.random.default_rng(seed)
    results = []
    best = (np.inf, None)
    for r in range(restarts):
        x0 = rng.standard_normal(m * (p - 1))
        if _scipy_minimize is not None:
            res = _scipy_minimize(
                phi, x0, method="L-BFGS-B",
                options={"maxiter": maxiter, "ftol": 1e-18, "gtol": 1e-14},
            )
            xr, fr = res.x, float(res.fun)
        else:
            xr, fr = local_descent(phi, x0, maxiter, rng)
        results.append(fr)
        if fr < best[0]:
            best = (fr, xr)
    results.sort()
    # scale for a relative view
    M = best[1].reshape(m, p - 1)
    Q, _ = np.linalg.qr(M)
    X = s * (Q @ H.T)
    total, norm = cubic_residual(B, X, p)
    print("== %s: p=%d on J(%d,%d), dim K = %d ==" % (label, p, 2 * k, k, m))
    print("restarts: %d   best 5 residuals: %s"
          % (restarts, ["%.3e" % v for v in results[:5]]))
    print("best absolute residual: %.6e   relative: %.6e"
          % (total, total / norm))
    return total / norm, X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--restarts", type=int, default=200)
    ap.add_argument("--maxiter", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260725)
    args = ap.parse_args()

    sanity_check_k2()
    # The k=2 run calibrates what "the optimizer found a solution" looks
    # like numerically: a solution certainly exists there.
    rel2, _ = search(3, 2, max(20, args.restarts // 10), args.maxiter,
                     args.seed, "control (true parameter)")
    if rel2 > 1e-6:
        print("WARNING: optimizer failed to approach the known k=2")
        print("         solution; the k=4 outcome below is untrustworthy.")

    rel4, X4 = search(5, 4, args.restarts, args.maxiter, args.seed + 1,
                      "decision (false parameter)")
    out = "collaboration/fable_frontier/cubic_k4_best.npz"
    try:
        np.savez(out, X=X4)
        print("best k=4 configuration saved to %s" % out)
    except OSError:
        print("could not save %s (run from repo root to save)" % out)

    print()
    feasible_bar = max(1e-18, 10 * rel2)
    floor_bar = max(1e-8, 1e6 * rel2)
    if rel4 <= feasible_bar:
        print("OUTCOME: C_5 numerically FEASIBLE at the false parameter")
        print("(k=4 residual within 10x of the known-feasible k=2 level).")
        print("The cubic system alone cannot separate true from false")
        print("parameters; certify exactly, then close the route.")
    elif rel4 >= floor_bar:
        print("OUTCOME: persistent residual floor far above the k=2")
        print("calibration. Evidence that C_5 is INFEASIBLE: the cubic")
        print("detects k=4. Next: exact equivariant infeasibility proof,")
        print("then scale the mechanism toward p=17.")
    else:
        print("OUTCOME: inconclusive floor; rerun with more restarts and")
        print("higher maxiter before drawing either conclusion.")


if __name__ == "__main__":
    main()
