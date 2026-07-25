# Complete arguments (Opus 5 frontier session, 2026-07-25)

Everything in this file is proved here in full. Nothing in this file was
produced by running code; see `STATUS.md` for the execution constraint of
this session. Where a numerical value appears it is derived symbolically and
cross-checked by hand against a *genuine* small design (`k=2,4,6`).

Notation. `k` even, `p = k+1`, `V = [2k]`, `X = binom(V,k)`.
A **tight colouring** is a proper `p`-colouring of `J(2k,k)`; equivalently a
large set `LS(k-1,k,2k)`, i.e. a partition of `X` into `p` classes
`C_0,...,C_{p-1}`, each an `S(k-1,k,2k)`. Write `f_a = 1_{C_a}`.
For a single design write `B` for its block set and `f = 1_B`.

`A_u` = adjacency matrix of the Johnson relation `|S ∩ S'| = k-u` on `X`
(so `A_1` is the Johnson graph `J(2k,k)`), and
`R^{2k} = E_0 ⊥ E_1 ⊥ ... ⊥ E_k` the Johnson (harmonic) decomposition of
`R^X`, with `E_j` the irreducible carrying `S^{(2k-j,j)}`.
**Slice degree** of `φ: X → R` is the least degree of a multilinear
polynomial in the incidence variables `x_1,...,x_{2k}` restricting to `φ`.
We use the standard fact that for `d ≤ k` the functions of slice degree
`≤ d` are exactly `E_0 ⊕ ... ⊕ E_d`.

---

## 1. The exact-one lemma and self-duality of `S(k-1,k,2k)`

### Theorem 1

Let `B` be any `S(k-1,k,2k)` (no primality or parity assumed). Then every
`(k+1)`-subset `U ⊆ V` contains **exactly one** block.

### Proof

Fix `U`, `|U| = k+1`, and put `D = { y ∈ U : U \ {y} ∈ B }`, so the number
of blocks inside `U` is `|D|`.

*Upper bound.* If `y ≠ z` both lay in `D`, then the `(k-1)`-set
`T = U \ {y,z}` would be contained in the two distinct blocks `U \ {y}` and
`U \ {z}`, contradicting `λ = 1`. Hence `|D| ≤ 1`.

*Averaging.* Count incidences between `(k+1)`-sets and the blocks they
contain. Each block `B` lies in exactly `2k - k = k` of them, so the total
is `|B| · k`. The number of blocks of an `S(k-1,k,2k)` is
`|B| = binom(2k,k-1)/binom(k,k-1) = binom(2k,k-1)/k`, and
`binom(2k,k-1) = (k/(k+1)) binom(2k,k)`, hence

    |B| = binom(2k,k)/(k+1) = C_k    (the Catalan number).

The number of `(k+1)`-sets is `binom(2k,k+1) = binom(2k,k-1) = k·C_k`.
So the average of `|D|` over all `U` is `(C_k · k)/(k · C_k) = 1`.
An average of `1` with every value `≤ 1` forces every value `= 1`. □

### Corollary 1.1 (self-duality)

`B* := { V \ B : B ∈ B }` is again an `S(k-1,k,2k)`.

*Proof.* A `(k-1)`-set `T` lies in `V \ B` iff `B ⊆ V \ T`, and
`|V \ T| = k+1`; by Theorem 1 exactly one block lies inside `V \ T`. □

### Corollary 1.2 (the canonical crossing matching)

Let `S ∈ X \ B`. Then `S` has exactly `k` neighbours in `B` in `J(2k,k)`, and
they are given by a **bijection** `β_S : S → V \ S` via
`S \ {x} ∪ {β_S(x)} ∈ B`. Blocks are pairwise non-adjacent.

*Proof.* Two blocks at distance `1` would share a `(k-1)`-set, so `B` is
independent. For `S ∉ B` and `x ∈ S`: the `(k-1)`-set `S \ {x}` lies in a
unique block `S \ {x} ∪ {y}`, and `y ≠ x` because `S ∉ B`; this defines
`β_S(x)`, and distinct `x` give distinct neighbours because the deleted
point is recoverable from the neighbour. Dually, for `y ∉ S` the
`(k+1)`-set `S ∪ {y}` contains exactly one block (Theorem 1), which is not
`S`, hence is `S \ {x} ∪ {y}` for a unique `x`. So `β_S` is onto. □

Thus every non-block `S` carries a canonical perfect matching
`M_S = { {x, β_S(x)} : x ∈ S }` of `V`, all of whose `k` edges cross the cut
`(S, V\S)`.

---

## 2. Divisibility: `S(k-1,k,2k)` forces `k+1` prime

### Theorem 2

For `0 ≤ s ≤ k-1` the higher indices of an `S(k-1,k,2k)` are

    λ_s = binom(2k-s, k-s)/(k+1) = binom(k+m, m)/(k+1),   m := k-s.   (2.1)

Consequently an `S(k-1,k,2k)` exists only if `(k+1) | binom(k+m,m)` for
every `1 ≤ m ≤ k`, and this holds for **all** such `m` if and only if
`k+1` is prime.

### Proof

*(2.1).* `λ_s = binom(2k-s, k-1-s)/binom(k-s, k-1-s) = binom(k+m,m-1)/m`,
and `binom(k+m,m-1)/m = (k+m)!/((m-1)!(k+1)! m) = (k+m)!/(m!(k+1)!)
= binom(k+m,m)/(k+1)`.

*Prime ⇒ divisibility.* Put `n = k+1 = p` prime and `1 ≤ m ≤ p-1`. Then

    binom(p-1+m, m) = [ p (p+1) ... (p+m-1) ] / m! ,

a product of `m` consecutive integers starting at `p`, divided by `m!`.
Since `m ≤ p-1`, exactly one factor of the numerator is divisible by `p`
(namely `p` itself, to the first power), and `p ∤ m!`. Hence
`v_p(binom(p-1+m,m)) = 1`, so `p | binom(p-1+m,m)`.

*Composite ⇒ failure.* Let `n = k+1` be composite with least prime factor
`q`, so `q ≤ n-1 = k` and `q | n`. Take `m = q`:

    binom(n+q-1, q) = [ n (n+1) ... (n+q-1) ] / q! .

For `1 ≤ i ≤ q-1` we have `n + i ≡ i ≢ 0 (mod q)`, so `q` divides none of
those `q-1` factors; and `v_q(q!) = 1`. Therefore

    v_q( binom(n+q-1,q) ) = v_q(n) - 1 < v_q(n),

so `n ∤ binom(n+q-1,q)`, i.e. `λ_{k-q}` is not an integer. □

Theorem 2 is the classical prime obstruction; the point of stating it in the
form (2.1) is that the *same* binomials reappear in Theorem 4 as the
**upper** indices, so the prime condition is exactly the self-dual
divisibility of the design.

---

## 3. Fourier support: `f` lives in `E_0 ⊕ E_k` only

### Theorem 3

Let `B` be an `S(k-1,k,2k)`, `f = 1_B`, `g = f - (1/p)·1`. Then

    A_1 f = k(1 - f),      i.e.   (A_1 + k I) f = k·1,      (3.1)
    g ∈ E_k    exactly (the eigenspace of A_1 for its least eigenvalue -k).

### Proof

(3.1) is Corollary 1.2. Since `A_1 · 1 = k^2 · 1`, applying `(A_1 + kI)` to
`(1/p)·1` gives `(k^2+k)/p · 1 = k·1`, so `(A_1 + kI)g = 0`. The eigenvalues
of `J(2k,k)` are `θ_j = (k-j)^2 - j`, and `θ_j = -k` forces `j = k`;
`E_k` is the corresponding eigenspace. □

`dim E_k = binom(2k,k) - binom(2k,k-1) = C_k`, and `E_k` carries the top
Specht module `S^{(k,k)}`; this is the space called `K` in
`evidence/top_degree_pairing_derivative_audit.md`.

### Corollary 3.1 (degree barrier)

For every `φ : X → R` of slice degree `≤ k-1`,

    ⟨f, φ⟩ = (1/p) ⟨1, φ⟩.                                   (3.2)

*Proof.* `φ ∈ E_0 ⊕ ... ⊕ E_{k-1}`, which is orthogonal to `g`. □

So **every** linear count of slice degree at most `k-1` is forced to its
average value, uniformly over all `S(k-1,k,2k)`. No such count can obstruct
existence. Sections 4–6 make this concrete.

---

## 4. All sub- and super-set counts are forced

### Theorem 4

Let `B` be an `S(k-1,k,2k)` and let `U ⊆ V` with `|U| = k + j`, `1 ≤ j ≤ k`.
Then

    #{ B ∈ B : B ⊆ U } = binom(k+j, j) / p ,                  (4.1)

independently of `U`. Dually, for `|U| = k - j` with `1 ≤ j ≤ k`,
`#{B ∈ B : B ⊇ U} = λ_{k-j} = binom(k+j, j)/p`.

### Proof

`χ_U(S) := 1_{S ⊆ U} = 1_{S ∩ (V\U) = ∅} = Π_{z ∈ V\U} (1 - x_z)`, a
multilinear polynomial of degree `|V \ U| = k - j ≤ k-1`. By Corollary 3.1,

    #{B ⊆ U} = ⟨f, χ_U⟩ = (1/p)⟨1, χ_U⟩ = binom(k+j,k)/p = binom(k+j,j)/p.

The dual statement is (2.1); note the two right-hand sides coincide. □

### Corollary 4.1 (the exact derived/residual tower)

For `1 ≤ j ≤ k` and every `(k+j)`-set `U`, the family

    B|^U := { U \ B : B ∈ B, B ⊆ U }

is an `S(j-1, j, k+j)` on the point set `U`.

*Proof.* `|U \ B| = j`. A `(j-1)`-subset `T ⊂ U` satisfies `T = U \ B` for
some block `B ⊆ U` iff `B ⊆ U` and `B ⊇ U \ T` with `|U\T| = k+1`, i.e. iff
`B` is a block inside the `(k+1)`-set `U \ T` — and by Theorem 1 there is
exactly one such block. Counting: (4.1) gives `binom(k+j,j)/p` blocks,
which is the block count of an `S(j-1,j,k+j)` by (2.1) read at parameter
`k' = j`. □

`j = k` recovers Corollary 1.1. `j = 1` is the trivial design.

### Corollary 4.2 (tower for the large set)

If `LS(k-1,k,2k)` exists then for every `1 ≤ j ≤ k` and every `(k+j)`-set
`U`, the `p` families `C_a|^U` form an `LS(j-1, j, k+j)`.

*Proof.* Each is an `S(j-1,j,k+j)` by 4.1, they are pairwise disjoint
(distinct blocks of `X` give distinct complements inside `U`), and their
total block count is `p · binom(k+j,j)/p = binom(k+j,j)` = the number of
`j`-subsets of `U`. □

### Corollary 4.3 (hardness at `k = 16`)

A tight `17`-colouring of `J(32,16)` implies, for `j = 5`, an
`LS(4,5,21)`: seventeen pairwise disjoint `S(4,5,21)` systems partitioning
all `20349` five-subsets of a `21`-set. In particular it implies that an
`S(4,5,21)` exists. Likewise `j = 6` implies an `S(5,6,22)` and `j = 7` an
`S(6,7,23)`.

This is the sharp form of the derivation used in the main note. It is what
makes the *construction* side at `k = 16` at least as hard as an
outstanding open problem of design theory (see `STATUS.md`).

---

## 5. Both two-point distributions are forced, in closed form

*Priority.* That these numbers are parameter-determined, nonnegative and
integral is already asserted in `erdos_835_conjectural_resolution.md`
(lines 352–354) and was checked numerically at the target parameters in an
earlier session of this project. What follows is the closed form, its proof,
and its extension to all `v`; the *phenomenon* is not claimed as new.

The eigenvalue of `A_u` on `E_j` is the Eberlein polynomial
`E_u(j) = Σ_h (-1)^h binom(j,h) binom(k-j, u-h) binom(2k-k-j, u-h)`.
For `j = k` and `n = 2k` both trailing binomials are `binom(0, u-h)`, so
only `h = u` survives:

    A_u acts on E_k as the scalar   (-1)^u binom(k,u).          (5.1)

Two independent checks of (5.1): `u = 1` gives `-k = θ_k` ✓; `u = k` gives
`(-1)^k = +1` for `k` even, and `A_k` is the permutation matrix of
`S ↦ V\S`, which indeed acts as `+1` on `E_k` when `k` is even — the
complement-closure fact of the main note. ✓

### Theorem 5 (inner distribution)

Let `B` be an `S(k-1,k,2k)` and `B ∈ B`. Then for every `0 ≤ u ≤ k`,

    n_{k-u} := #{ B' ∈ B : |B ∩ B'| = k-u }
             = binom(k,u) [ binom(k,u) + (-1)^u k ] / p .        (5.2)

independently of `B`.

### Proof

By Theorem 3 and (5.1), `A_u f = (binom(k,u)^2/p)·1 + (-1)^u binom(k,u)·g`.
On `B` we have `g = 1 - 1/p = k/p`, a constant, so `A_u f` is constant on
`B` with value `(binom(k,u)^2 + (-1)^u k binom(k,u))/p`, which is exactly
`n_{k-u}`. □

### Theorem 5a (general `v`)

The same argument runs for any `S(k-1,k,v)` with `v ≥ 2k` (so that `E_k`
exists in `J(v,k)`). Put `P = v-k+1`; then
`|B| = binom(v,k-1)/k = binom(v,k)/P`. The Eberlein eigenvalue of
`A_u` on `E_k` in `J(v,k)` is again `(-1)^u binom(k,u)` (with `j = k` the
factor `binom(k-j, u-h)` forces `h = u`), and `g = (P-1)/P` on `B`. Hence for
`B ∈ B` and `0 ≤ u ≤ k`,

    #{B' ∈ B : |B ∩ B'| = k-u} = binom(k,u)[ binom(v-k,u) + (-1)^u (P-1) ]/P.

`v = 2k` gives `P = p` and recovers (5.2).

**Worked instance, `S(4,5,21)` (`k=5`, `v=21`, `P=17`).** The distribution is

    |B ∩ B'| :   5    4    3    2    1    0
    count    :   1    0   80  320  540  256      (total 1197 = |B|)

so it is forced there as well, and it is a nonnegative integer vector. Two
blocks of an `S(4,5,21)` therefore *never* meet in exactly `4` points (which
is just `λ = 1`), and the remaining counts carry no slack. Integrality here
needs `P | binom(k,u)[binom(P-1,u) - (-1)^u]`, which holds because
`binom(P-1,u) ≡ (-1)^u (mod P)` whenever `gcd(u!, P) = 1`; at `P = 17` prime
this is automatic.

### Theorem 6 (cross distribution)

Let `B_a, B_b` be **disjoint** `S(k-1,k,2k)` systems (no large set needed)
and `B ∈ B_a`. Then

    m_u := #{ B' ∈ B_b : |B ∩ B'| = k-u }
         = binom(k,u) [ binom(k,u) - (-1)^u ] / p .              (5.3)

### Proof

As above with `g_b = f_b - (1/p)1`, which equals the constant `-1/p` on
`B_a` because `B_a ∩ B_b = ∅`. □

### Checks and immediate consequences

* Integrality. `p = k+1` prime gives `binom(k,u) = binom(p-1,u) ≡ (-1)^u
  (mod p)`, so both brackets in (5.2), (5.3) vanish mod `p`. Both formulas
  are automatically nonnegative integers. No new divisibility obstruction.
* Sums. `Σ_u n_{k-u} = [binom(2k,k) + k·Σ_u(-1)^u binom(k,u)]/p = C_k` ✓ and
  `Σ_u m_u = binom(2k,k)/p = C_k` ✓.
* `u = 1`: `n_{k-1} = k(k - k)/p = 0` (blocks pairwise non-adjacent ✓) and
  `m_1 = k(k+1)/p = k` (Corollary 1.2 ✓).
* `u = k`: `n_0 = 1` (the complement of a block is a block of the *same*
  system) and `m_k = 0` ✓ — consistent with complement-closure of classes.
* Symmetry `n_i = n_{k-i}`, `m_i = m_{k-i}` for `k` even.

### Corollary 6.1 (`k` must be even, by nonnegativity alone)

Read (5.2) at `u = k`: `n_0 = (1 + (-1)^k k)/p`. If `k` is odd and `k > 1`
this equals `(1-k)/(k+1) < 0`, which is impossible for a cardinality.
Hence **no `S(k-1,k,2k)` exists for odd `k > 1`.**

This is independent of Theorem 2 (for odd `k`, `p = k+1` is even, so
Theorem 2 also excludes it, but via a different mechanism). Sanity check:
`k = 3` would be an `S(2,3,6)`, and `6 ≢ 1,3 (mod 6)` ✓.

### Corollary 6.2 (complement-closure of a *single* system)

If `k` is even, then every `S(k-1,k,2k)` satisfies `V \ B ∈ B` for every
block `B`.

*Proof.* `n_0 = (1+k)/p = 1`, so exactly one block is disjoint from `B`.
The only `k`-subset of `V` disjoint from `B` is `V \ B`. □

This is more elementary than, and strictly implies, the statement in the
main note that colour classes of a large set are complement-closed: no
Specht-module argument and no large set are needed.
* `k = 2`, `p = 3`: `(n_2,n_1,n_0) = (1,0,1)` — the perfect matchings of
  `K_4` ✓.
* `k = 4`, `p = 5`: `(n_4,...,n_0) = (1,0,12,0,1)` — SQS(8) = the 14 planes
  of `AG(3,2)`; two distinct planes meet in `0` or `2` points ✓.
* `k = 6`, `p = 7`: `(n_6,...,n_0) = (1, 0, 45, 40, 45, 0, 1)`. This is
  exactly the classical hexad intersection distribution of the Witt system
  `S(5,6,12)`: a hexad, its complement, `45 + 45` hexads meeting it in `2`
  or `4` points, and `40` meeting it in `3`. ✓ This is an independent
  confirmation of (5.2) against a real, nontrivial design.

---

## 6. Meta-theorem: no two-point or LP method can ever work

### Theorem 7a (general form: any `v`)

Let `v ≥ 2k-1` and let `B` be **any** `S(k-1,k,v)`, `f = 1_B`. Then

    Π_j f = 0    for every 1 ≤ j ≤ k-1,

so the Fourier support of `f` in `J(v,k)` is contained in `{E_0, E_k}` and
the dual distribution of `B` is supported on `{0,k}`. Hence the Delsarte LP
for `J(v,k)` is feasible at the exact size `|B| = binom(v,k-1)/k`, and no LP
bound can refute existence of an `S(k-1,k,v)`.

### Proof

For `J ⊆ [v]` with `j := |J| ≤ k-1`, put `m_J(S) = 1_{J ⊆ S}`. These span the
functions of slice degree `≤ k-1`, which is `E_0 ⊕ ... ⊕ E_{k-1}` (using
`k-1 ≤ min(k, v-k)`). The design gives `⟨f, m_J⟩ = λ_j`, where

    λ_j = binom(v-j, k-1-j)/(k-j).

The average value of the same functional is

    (|B|/binom(v,k)) ⟨1, m_J⟩ = (|B|/binom(v,k)) binom(v-j, k-j)
                              = binom(v-j, k-j)/(v-k+1),

using `|B| = binom(v,k-1)/k` and `binom(v,k-1)/binom(v,k) = k/(v-k+1)`.
These agree, because `binom(v-j,k-j) = binom(v-j,k-1-j)·(v-k+1)/(k-j)`.
So `⟨f - (|B|/binom(v,k))·1, m_J⟩ = 0` for every `J` with `|J| ≤ k-1`, i.e.
`Π_j f = 0` for `1 ≤ j ≤ k-1`. The dual distribution at index `j` is a
positive multiple of `‖Π_j f‖²`, and the LP constraints are satisfied by the
actual distribution of `B`. □

### Theorem 7 (sharp form at `v = 2k`)

Let `B` be an `S(k-1,k,2k)`, `f = 1_B`, and let `B_u = n_{k-u}` be its inner
distribution (5.2). Then the dual (MacWilliams) distribution of `B` in the
Johnson scheme `J(2k,k)` is supported on `{0, k}`:

    Σ_u B_u Q_j(u) = 0    for every 1 ≤ j ≤ k-1,

and is strictly positive at `j = 0` and `j = k`. Consequently:

1. the Delsarte linear program for `J(2k,k)` is **feasible** at the exact
   size `|B| = C_k`, so no LP bound — and no strengthening of it that uses
   only the inner distribution and its dual — can refute existence of an
   `S(k-1,k,2k)`, for any `k`;
2. more generally, by Corollary 3.1, every necessary condition expressible
   as a linear functional of slice degree `≤ k-1` applied to `f_a`, or as a
   function of the pairwise inner products `⟨f_a, A_u f_b⟩`, is
   automatically satisfied.

### Proof

Up to the usual positive normalisation, `Σ_u B_u Q_j(u)` equals
`(|X|/|B|) · ‖Π_j f‖²`, where `Π_j` is the orthogonal projection onto `E_j`.
By Theorem 3, `Π_j f = 0` for `1 ≤ j ≤ k-1`, `Π_0 f = (1/p)1 ≠ 0`, and
`Π_k f = g ≠ 0` (else `f` would be constant). Feasibility of the LP at the
exact size follows because the actual distribution (5.2) satisfies every LP
constraint. Item 2 is Corollary 3.1 together with Theorems 5 and 6, which
show that all the numbers `⟨f_a, A_u f_b⟩` are determined by the design
parameters alone. □

### Corollary 7.1 (the LP is dead at every level of the tower)

By Theorem 7a, for every `1 ≤ j ≤ k` the Delsarte LP in `J(k+j, j)` is
feasible at the exact size of an `S(j-1,j,k+j)`. So no LP argument can refute
any level of the derived tower of Corollary 4.1 — in particular none can
refute `S(4,5,21)` or `S(3,4,20)`. Note `S(4,5,21)` is a `4`-design with
block size `5`, i.e. `t = k'-1` with `k' = 5`, so Theorem 7a applies with
`v = 21 ≠ 2k'`; the *closed forms* (5.2)–(5.3) do **not** apply there, since
they use `v = 2k`.

`B` is thus a *tight* `T`-design in Delsarte's sense with
`T = {1, 2, ..., k-1}`, the largest possible index set. This is a structural
explanation, not a heuristic, for the pattern already recorded in this
repository: the Terwilliger four-point relaxation
(`evidence/four_point_terwilliger_exact_witness.md`), the state-refined
association-scheme SDP (`evidence/state_sdp_p17/`), the Bose–Mesner
quotient (`evidence/teichmuller_schur_no_go.md`) and the cross-matching
quadratic relaxation (`evidence/top_degree_cross_matching_cubic_audit.md`)
were all found feasible. Theorem 7 says that had to happen for every
relaxation whose only zero-one input is second order.

**Corollary (where an obstruction must live).** Any proof of nonexistence
must use a functional of full slice degree `k` (equivalently a nonzero
pairing against `E_k`) *together with* at least a third-order use of
pointwise idempotence `f_a f_b = δ_{ab} f_a`. This is exactly the position
of the cross-matching cubic (8) of
`evidence/top_degree_cross_matching_cubic_audit.md`.

### Corollary 7.2 (the degenerate boundary `v = 2k-1`)

For `v = 2k-1` the Johnson scheme `J(2k-1,k)` has eigenspaces
`E_0,...,E_{k-1}` only — there is no `E_k`. Theorem 7a then forces
`Π_j f = 0` for all `j ≥ 1`, i.e. `f` constant, i.e. `B = ∅` or `B` = all
`k`-sets. Hence

    no S(k-1, k, 2k-1) exists for any k ≥ 2.

Checks: `k = 2` asks for a perfect matching on `3` points; `k = 3` for an
`STS(5)`; `k = 4` gives `λ_0 = binom(7,3)/4 = 35/4 ∉ Z`. ✓

---

## 7. Local Latin-square rigidity of a tight colouring

### Theorem 8

Let `c` be a tight `p`-colouring of `J(2k,k)`. For `S ∈ X` define the
`k × k` array

    L_S(x, y) = c( (S \ {x}) ∪ {y} ),    x ∈ S,  y ∈ V \ S.

Then `L_S` is a **Latin square** of order `k` on the symbol set
`F_p \ {c(S)}`.

### Proof

*Rows.* Fix `x ∈ S` and put `T = S \ {x}`, `|T| = k-1`. The `p` sets
`T ∪ {z}`, `z ∈ V \ T`, are pairwise adjacent, hence receive all `p`
colours exactly once. Removing `z = x` (which gives `S`) leaves the `k`
values `L_S(x,y)`, `y ∈ V\S`, all distinct and all `≠ c(S)`.

*Columns.* Fix `y ∈ V \ S` and put `U = S ∪ {y}`, `|U| = k+1`. The `k+1`
`k`-subsets of `U` are pairwise adjacent, hence rainbow. They are `S`
together with the `k` sets `(S\{x}) ∪ {y}`, `x ∈ S`. So the `k` values
`L_S(x,y)`, `x ∈ S`, are distinct and `≠ c(S)`. □

### Remarks

* Complement compatibility: since `k` is even every class is
  complement-closed, and `L_{V\S} = L_S^T` under `x ↔ y`.
* Adjacent overlap: if `S' = (S\{x_0\}) ∪ {y_0}`, then row `y_0` of `L_{S'}`
  agrees with row `x_0` of `L_S` off the entry at `(x_0,y_0)`, and column
  `x_0` of `L_{S'}` agrees with column `y_0` of `L_S` off that entry; the
  two exceptional entries are `c(S')` and `c(S)` respectively.
* Order `k = p-1` is exactly one of the two families for which the
  Alon–Tarsi conjecture is a theorem (Glynn for `p-1`, Drisko for `p+1`).
  We do **not** use this; see `IDEAS.md`.

---

## 8. At most `p` pairwise disjoint systems, with equality iff a large set

### Theorem 9

Let `B_1, ..., B_r` be pairwise disjoint `S(k-1,k,2k)` systems on `V`. Then
`r ≤ p = k+1`, and `r = p` if and only if they form an `LS(k-1,k,2k)`.

### Proof

Put `g_i = f_i - (1/p)1 ∈ E_k` (Theorem 3). Pairwise disjointness gives
`⟨f_i,f_j⟩ = C_k δ_{ij}`, hence

    ⟨g_i, g_j⟩ = C_k δ_{ij} - |X|/p² = (|X|/p²)( p δ_{ij} - 1 ).

The Gram matrix `(|X|/p²)(p I_r - J_r)` has eigenvalues `(|X|/p²)·p` with
multiplicity `r-1` and `(|X|/p²)(p-r)` once. Positive semidefiniteness
forces `r ≤ p`. If `r = p` then the Gram matrix is singular with kernel
spanned by the all-one vector, so `Σ_i g_i = 0`, i.e. `Σ_i f_i = 1`: the
systems partition `X`. Conversely a large set has `r = p`. □

Theorem 9 shows the large-set condition is exactly the extremal case of a
positive-semidefiniteness constraint that is otherwise slack — one more
instance of Theorem 7.

---

## 9. A purely local reformulation of the whole problem

### Theorem 10

A tight `p`-colouring of `J(2k,k)` exists if and only if there is a family of
bijections

    π_T : F_p → V \ T,     one for each (k-1)-set T ⊆ V,

such that for every `(k-2)`-set `A ⊆ V`, every colour `a ∈ F_p` and all
`u, v ∈ V \ A`,

    π_{A ∪ {u}}(a) = v   ⟺   π_{A ∪ {v}}(a) = u.                (9.1)

### Proof

*(⇒)* Given `c`, define `π_T(a)` to be the unique `y ∈ V \ T` with
`c(T ∪ {y}) = a`; this is a bijection by the rainbow-star property (the `p`
sets `T ∪ {y}` are pairwise adjacent). For (9.1), both sides say
`c(A ∪ {u,v}) = a`.

*(⇐)* Given the family, define `c(S)` for `S ∈ X` by picking any `u ∈ S` and
setting `c(S) = π_{S \ {u}}^{-1}(u)`. This is well defined: for `u ≠ u'` in
`S` put `A = S \ {u,u'}` and `a = π_{S\{u\}}^{-1}(u)`. Then
`π_{A ∪ {u'}}(a) = u`, so by (9.1) `π_{A ∪ {u}}(a) = u'`, i.e.
`π_{S \ {u'}}^{-1}(u') = a`. Independence of the choice of `u` follows by
chaining, since any two elements of `S` are compared directly.
The colouring is tight: for a `(k-1)`-set `T`, the `p` extensions
`T ∪ {y}` receive the colours `π_T^{-1}(y)`, all distinct. Two adjacent
`k`-sets share a `(k-1)`-set, so they get different colours. □

Note that (9.1) is a constraint only between `(k-1)`-sets at Hamming
distance one, so #835 is a constraint-satisfaction problem all of whose
constraints are local; all the difficulty is global consistency. Equivalently
(9.1) says that for each `A` and `a` the relation `u ↦ π_{A∪{u}}(a)` is a
fixed-point-free involution of the `(k+2)`-set `V \ A`, i.e. a perfect
matching — the local one-factorization of
`evidence/local_one_factorization_sign_audit.md`, here derived as an exact
equivalence rather than a consequence.

## 10. What is *not* proved here

Nothing in this file decides Erdős–Rosenfeld #835, for `k = 16` or for any
`k > 6`. Theorems 1–9 are necessary conditions and structure theorems, plus
one negative result (Theorem 7) about entire families of proof methods.
The exact remaining gap is stated in `STATUS.md`.
