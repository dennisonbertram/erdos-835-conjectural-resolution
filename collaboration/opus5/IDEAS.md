# Unproved directions and recorded failures — Opus 5, 2026-07-25

Nothing here is a theorem. Anything marked *hand-computed* was derived
symbolically by me with no code execution available (see `STATUS.md`) and
must be re-derived before use.

---

## A. Attacks that Theorem 7 now proves cannot work

`PROOF.md` Theorem 7 (`f_a - 1/p·1 ∈ E_k` exactly) closes, for every `k`, all
of the following. These should not be attempted again.

* Delsarte LP in `J(2k,k)` and every refinement of it that reads only the
  inner distribution and its MacWilliams transform.
* Any obstruction from block-intersection numbers of one system, or of two
  disjoint systems: both distributions are forced in closed form
  (Theorems 5, 6) and both are nonnegative integers whenever `p` is prime.
* Any obstruction from counts of blocks inside or above a fixed set: forced
  (Theorem 4), and the divisibility they demand is exactly primality of `p`
  (Theorem 2), so it is satisfied at every surviving parameter.
* Any obstruction from a linear functional of slice degree `≤ k-1`
  (Corollary 3.1). In particular no "power-sum"/moment obstruction below the
  top degree can survive.
* Positive-semidefiniteness of the Gram matrix of the class indicators: the
  large-set condition is exactly its equality case (Theorem 9), so PSD is
  slack everywhere else.

This also retro-explains, as a theorem rather than a coincidence, the
feasibility results in `evidence/four_point_terwilliger_exact_witness.md`,
`evidence/state_sdp_p17/`, `evidence/teichmuller_schur_no_go.md`, and the
`k=4` relaxation in `evidence/top_degree_cross_matching_cubic_audit.md`.

---

## B. Odd-graph cover trace identities (worked out, judged unpromising)

Formulation. A tight colouring at even `k` is a covering projection
`π : O_k → K_p` with fibre size `d = binom(2k-1,k-1)/p`. In block form the
adjacency matrix of `O_k` is `(P_{ij})` with `P_{ij}` a permutation matrix
for `i ≠ j`, `P_{ii} = 0`, `P_{ji} = P_{ij}^T`. Because `O_k` has girth 6 for
`k ≥ 4`, every triangle monodromy `σ_{ijl} = P_{li}P_{jl}P_{ij}`, every
4-walk monodromy and every 5-walk monodromy is a **derangement** of the
fibre.

What I checked by hand. Writing `W_m = tr(A^m) = Σ_i m_i θ_i^m` with
`θ_i = (-1)^i (k-i)`, `m_i = binom(2k-1,i) - binom(2k-1,i-1)`:

* Every closed walk of length `≤ 5` in `K_p` either reduces to the trivial
  walk (monodromy = identity, contributing `d` lifts) or reduces to a
  triangle/4-cycle/5-cycle (derangement, contributing `0`). This predicts
  `W_3 = W_5 = 0` and `W_4 = N·k(2k-1)`.
* *Hand-computed, `k = 4` (`O_4 = KG(7,3)`, `N = 35`):* `W_4 = 980` and
  `35 · c_4(4) = 35 · 28 = 980`, where `c_{2n}(k)` counts closed `2n`-walks
  at the root of the `k`-regular tree — an exact match, confirming the
  bookkeeping. Also `W_5 = 4^5 - 6·3^5 + 14·2^5 - 14 = 0`.
* Length 6 is the first informative length. Reduced closed 6-walks in `K_p`
  are: 6-cycles, doubled triangles `(i,j,l,i,j,l)`, and two triangles
  sharing a vertex. So

      W_6 = d · N · c_6(k) + Σ_{6-cycles} fix + Σ_{doubled} fix(σ²)
                                            + Σ_{two-triangle} fix(σσ'),

  with `c_6(k) = 2k(k-1)² + 2k²(k-1) + k³`, and the left side is
  `12 ·` (number of hexagons of `O_k`) above the tree term.
* *Hand-computed, `k = 4`:* `W_6 = 4^6 + 6·3^6 + 14·2^6 + 14 = 9380`,
  `c_6(4) = 232`, tree term `35·232 = 8120`, so `O_4` has
  `(9380 - 8120)/12 = 105` hexagons. `K_5` has no 6-cycle, so at `p = 5` the
  identity reads `1260 = Σ_{doubled} 2·c_2(σ) + Σ_{two-triangle} fix(σσ')`.

**Assessment: unpromising.** The identity is one linear equation per walk
length in a large number of independent nonnegative unknowns
(`c_2(σ_{ijl})` and the fixed-point counts of products of two triangle
monodromies). Nothing forces it to be infeasible, and I did not find any
second relation pinning those unknowns. Any invariant depending only on the
girth, the spectrum, and the combinatorics of covers of `K_p` will be
satisfiable, because those data are the same at `k = 4` (where the answer is
NO) as at `k = 16`. To be worth resuming, this needs a genuinely
`O_k`-specific constraint on triangle monodromies — for instance a
description of `σ_{ijl}`'s cycle type forced by the odd-graph structure.

---

## C. Latin-square signs and Alon–Tarsi (untried, structurally interesting)

`PROOF.md` Theorem 8 gives, for every `k`-set `S`, a Latin square `L_S` of
order `k` on the colours other than `c(S)`. Two facts make this worth a
serious look:

1. The order is `k = p-1`, which is exactly one of the two families for which
   the Alon–Tarsi conjecture is a **theorem** (Glynn for `p-1`, Drisko for
   `p+1`). So the even/odd Latin-square count of the relevant order is
   provably unbalanced — an asymmetry available at every surviving parameter
   and at no other.
2. Adjacent squares overlap in exactly one row and one column
   (Theorem 8, third remark), so the row/column sign of `L_S` is not free:
   `ε_r(L_{S'})` and `ε_r(L_S)` differ by a controlled amount when
   `S' = S - x_0 + y_0`.

What I did not do: turn (1)+(2) into a global identity. The obvious first
step is to compute `ε_r(L_S) ε_c(L_S)` as a function on `X` and ask whether
it has slice degree `≤ k-1`; if so, Corollary 3.1 forces its average, giving
a genuine parity equation. **Warning:** the scalar-sign no-go in
`evidence/local_one_factorization_sign_audit.md` shows that a single `±1`
invariant built from local factorizations closes consistently at `p = 17`. A
Latin-square sign may well be in the same commutative sign algebra. Check
that first, cheaply, at `p = 5` (false) and `p = 17`, before investing.

---

## D. Why the construction search at `k = 16` is aimed wrong

Corollary 4.3 is sharp: a tight `17`-colouring forces, for **every**
`21`-subset `U ⊂ [32]` simultaneously, a large set of seventeen pairwise
disjoint `S(4,5,21)` systems on `U`. There are `binom(32,21) = 129 024 480`
such `U`. Any `F_32` colour formula `c(S) = F(statistics of S)` must produce
all of them at once.

So the instruction to look for "a richer explicit construction not killed by
the two-statistic `K_18`" should be read as: any such formula would settle
the existence of `S(4,5,21)` as a corollary. Per this repository's own
literature section, `S(4,5,15)` and `S(4,5,17)` are proved nonexistent and
`S(4,5,21)` is the first unsettled order. That is where the difficulty
actually is, and no amount of extra coefficient information in `F_32`
addresses it.

The productive inversion: **attack `LS(4,5,21)` directly.** It is a far
smaller object than `LS(15,16,32)` — `21` points, `20349` five-sets, `17`
classes of `1197` blocks — and by Corollary 4.2 its nonexistence kills
`k = 16` outright.

Caveat I worked out, and it kills the algebraic half of this redirection:
**the LP is dead there too, and so is the intersection distribution.**
Theorem 7a needs only `t = k-1`, not `v = 2k`, so an `S(4,5,21)` also has
Fourier support `{E_0, E_5}` in `J(21,5)`; and Theorem 5a then forces its
block-intersection distribution to be

    |B ∩ B'| :  5   4    3    2    1    0
    count    :  1   0   80  320  540  256      (total 1197)

with no slack. So `LS(4,5,21)` is *not* algebraically softer than
`LS(15,16,32)`; the reason to prefer it is purely size. It is a `21`-point,
`20349`-cell, `17`-class exact-cover instance — within reach of the SAT and
CP-SAT machinery already in this repository, unlike the `32`-point problem.
That is the redirection: same difficulty class, four orders of magnitude
smaller search space.

---

## E. Dead ends I confirmed by hand

* **Catalan/ballot construction.** `|C_a| = C_k` invites the guess that the
  Dyck-path `k`-sets form an `S(k-1,k,2k)`. False at `k = 2`: the `(k-1)`-set
  `{1}` lies in both ballot sets `{1,2}` and `{1,3}`.
* **Nonnegativity/integrality of the forced distributions.** Checked
  symbolically: `binom(k,u) ≡ (-1)^u (mod p)` makes every numerator in
  Theorems 5 and 6 vanish mod `p`, and both brackets are nonnegative. No
  obstruction, at any `k`.
* **Same-fibre distance 2.** In a cover of `K_p` no two vertices of one fibre
  are at distance 2 (their common neighbour would have two neighbours in that
  fibre), and the distance-2 vertices of `v ∈ C_i` split as exactly `k-1` in
  each other class. Fully consistent; no counting slack.
* **Mod-4 refinement of the matching derivatives `Δ_M(a)`.** Antipodal
  pairing on the matching cube makes `|C_a ∩ Even|` and `|C_a ∩ Odd|`
  separately even, so `Δ_M(a) ≡ 0 (mod 2)` and nothing further. No mod-4
  information is available from complement-invariance alone.
* **Bounding the number of pairwise disjoint systems below `p`.** Theorem 9
  gives `≤ p` from PSD and nothing better; the Gram matrix is exactly the
  scaled simplex, so no slack remains at `r < p`.

---

## F. Where I would go next, in order

1. `LS(4,5,21)` nonexistence (section D). Smallest object whose death
   settles `k = 16`, and outside the reach of my own Theorem 7.
2. The cubic system (8) of
   `evidence/top_degree_cross_matching_cubic_audit.md`, now known to be the
   *first* level that can possibly fail (Theorem 7). Specifically: look for a
   sum-of-squares certificate for the system
   `P_K(q_a q_b) = (p-2)q_a` / `-q_a - q_b` restricted to the span of a
   *small* explicit set of matchings, and test it at `p = 5` first — the
   control must fail there, otherwise the certificate proves nothing.
3. Latin-square signs (section C), but only after the cheap `p = 5` / `p = 17`
   sanity test against the existing scalar-sign no-go.
