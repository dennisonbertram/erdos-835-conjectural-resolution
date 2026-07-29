# Unconditional results on the common odd-transversal bottleneck

Date: 2026-07-29.  Author run: Opus 5, max effort.

Everything in this file is proved.  Conjectures, rejected routes and the
remaining lemma are in `IDEAS.md`.  Statements that are *cited* rather than
reproved are marked **[cited]** and carry a source on the same line.

Nothing here resolves Erdős--Rosenfeld Problem #835.

---

## 0.  Notation

`X` is a set of `n` points.  Throughout

```
n = t + p,      p odd,      D_1, ..., D_r   pairwise block-disjoint S(t,t+1,n),
D = D_1 u ... u D_r,        E = C(X,t+1) \ D.
```

The *top rung* is `t = k-1`, `n = 2k`, `p = k+1`, so `k` is even and
`k+1` is odd.  `C_k = binom(2k,k)/(k+1)` is the Catalan number and the block
count of an `S(k-1,k,2k)`.

Here an even parameter `k` is called *divisibility-admissible* when all
standard derived numbers
`lambda_j = binom(2k-j,k-j)/(k+1)` are integers.  This is a numerical
condition only; it does not assert that an `S(k-1,k,2k)` exists.

When `r = p-2`, every `t`-set lies in exactly two blocks of `E`.  The
*residual conflict graph* `G` has vertex set `E`; for each `A` in `C(X,t)`
it has one edge joining the two blocks of `E` that contain `A`.  `G` is
`(t+1)`-regular with `2*lambda_0` vertices and `binom(n,t)` edges, where
`lambda_0 = |D_i|`.

All linear algebra is over **F**<sub>2</sub>.  `delta_s : C_s -> C_{s+1}` is the
simplicial coboundary `(delta_s f)(B) = sum over s-subsets A of B of f(A)`.

---

## 1.  Audit of the exact equivalence

**Claim audited.**  `collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md`,
Theorems 2.1, 4.1, 6.2 and display (8.1).

**Verdict: correct.**  No flaw found.  I re-derived the chain independently by
a different route; the two derivations agree.  The independent derivation is
recorded here because it is shorter and makes the top-rung statement
manifestly symmetric.

### Theorem 1.1 (general rung — the audited chain, verified)

Let `r = p-2`.  The following are equivalent.

1. `G` is bipartite, equivalently `D_1,...,D_{p-2}` extend to `p` pairwise
   disjoint `S(t,t+1,n)`'s.
2. Every `y` in `ker M_D` has even weight, where `M_D` is the
   `C(X,t+2)`-by-`D` containment matrix.
3. `1_D` lies in the row space of `M_D`.

This is Theorem 4.1 of the audited note.  I checked every step of its proof:
simplex exactness (its Lemma 3.1), surjectivity of `z |-> delta_t z` from
`ker H_E^T` onto `ker M_D`, the parity identity
`|delta_t z| = (n-t)|z| = p|z| = |z|` mod 2 (valid because `p` is odd), and
`row M_D = (ker M_D)^perp`.  All are correct as written.  Note that (3)
unwrapped says: there is `c` on `C(X,t+2)` with `sum_{F ⊇ B} c(F) = 1` for
every `B` in `D` — an **upper**-shadow condition on `(t+2)`-sets, not a
`delta_t` condition on `t`-sets.  The two coincide only after complementation
at the top rung.

### Theorem 1.2 (top rung — independent derivation of the transversal form)

Let `t = k-1`, `n = 2k`, `p = k+1`, `r = k-1`, `k` even.  Add to the list:

4. There is `a : C(X,k-1) -> F_2` with `sum_{A subset C, |A| = k-1} a(A) = 1`
   for every `C` in `D`  (a **common odd transversal** of the `k-1`
   partitions).
5. There is `y` in `ker delta_k` with `y(C) = 1` for every `C` in `D`.

**Proof.**  This proof does not pass through `M_D` and so is an independent
check on the audited Theorem 6.2.

*(4) <=> (5).*  `(delta_{k-1} a)(C) = sum_{A subset C} a(A)`, so (4) says
`y := delta_{k-1} a` restricts to `1` on `D`.  By exactness of the simplex,
`im delta_{k-1} = ker delta_k`, so the two statements have the same solution
sets.

*Two labellings of the edges of `G`.*  Let `{C_1,C_2}` be an edge of `G`,
i.e. two residual blocks with `|C_1 ∩ C_2| = k-1`.  Set
`A := C_1 ∩ C_2` (a `(k-1)`-set) and `F := C_1 u C_2` (a `(k+1)`-set).
Every `A` in `C(X,k-1)` labels exactly one edge, because `A` lies in `k+1`
`k`-sets and in exactly one block of each of the `k-1` systems, leaving
exactly two residual ones — this needs no complement structure.  So `|E(G)| = binom(2k,k-1)`.
The `F`-labelling is injective into `E(G)`: two distinct `k`-subsets of a
`(k+1)`-set meet in `k-1` points, so the two residual blocks inside `F` — there
are exactly two, by Lemma 6.1 of the audited note, which does use Corollary 2.2
below — form an edge, and `F = C_1 u C_2` is recovered from it.  Since
`binom(2k,k+1) = binom(2k,k-1) = |E(G)|`, that injection is a bijection.
**Hence the `A`-labelling and the `F`-labelling enumerate the same edge set,
each exactly once** (note `A = C_1 ∩ C_2` is a subset of `F = C_1 u C_2`; the
two labels of one edge are *not* complementary).

*(1) <=> (5).*  Write `y = 1 + w`, so `y` restricts to `1` on `D` exactly when
`w` is supported on `E`.  For `F` in `C(X,k+1)`,
`(delta_k 1)(F) = k+1 = 1` in `F_2` because `k` is even.  Hence
`delta_k y = 0` is the affine system

```
sum over the k-subsets C of F with C in E  of  w(C)  =  1     for all F.
```

By the previous paragraph each such `F` contributes exactly two terms, namely
the two endpoints of the edge labelled `F`.  So the system says precisely that
`w` gives opposite values to the two ends of every edge of `G`, i.e. `w` is a
proper 2-colouring.  Solvability is bipartiteness.  []

Theorem 1.2 reproduces the audited Theorem 6.2 by a route that never forms
`Q`, and it agrees with it.

**Three cautions that survive the audit.**

* Theorem 6.2 of the audited note writes the top-rung condition as
  `Q^T a = 1` where `Q` is the *point-versus-cell* matrix (rows `C(X,k-1)`,
  columns the blocks).  Row sums of `Q` are `k-1`, column sums are `k`.  The
  transpose placement is correct as written; reading `Q a = 1` instead is
  false (that system is solved by `a = 1` since `k-1` is odd).
* The whole chain is conditional on the `D_i` existing.  Section 5 below
  shows this is not a formality.
* `Corollary 4.2` calls the certificate an "upward-incidence" trade.  That is
  the right caveat: it is a cocycle for `delta`, not a Steiner trade in the
  usual downward sense, except after complementation at the top rung.

---

## 2.  The two intersection profiles of a top system

### Theorem 2.1 (forced intersection distribution)

Let `k` be even, `|X| = 2k`, and let `T` be any `S(k-1,k,2k)`.  Let `B` be any
`k`-subset of `X` and put `x_i = #{ C in T : |B ∩ C| = i }`.  Then

```
          1  [               k-i        ]
x_i  =  ----- [ binom(k,i)^2 + k(-1)   binom(k,i) ]      if B is in T,
        k+1  [                          ]

          1  [               k-i        ]
x_i  =  ----- [ binom(k,i)^2 -   (-1)   binom(k,i) ]      if B is not in T.
        k+1  [                          ]
```

In particular the profile does not depend on `B`, on `T`, or on any further
data: an `S(k-1,k,2k)` has exactly two intersection characters.

**Proof.**  For `0 <= j <= k-1` count pairs `(J,C)` with `J` a `j`-subset of
`B`, `C` in `T`, `J` contained in `C`.  Grouping by `J` gives
`binom(k,j) lambda_j` with

```
lambda_j = binom(2k-j, k-j) / (k+1)                                    (2.1)
```

the number of blocks on a fixed `j`-set (valid for `j <= k-1`).  Grouping by
`C` gives `sum_i binom(i,j) x_i`.  Hence

```
sum_i binom(i,j) x_i = binom(k,j) lambda_j        (0 <= j <= k-1),
sum_i binom(i,k) x_i = x_k = [B in T].                                 (2.2)
```

Multiply the `j`-th equation by `y^j` and sum over `0 <= j <= k`.  The left
side is `sum_i x_i (1+y)^i`.  Writing `eps = [B in T]` and adding and
subtracting the `j = k` term of the closed formula (2.1), the right side is

```
   1                                             (       1  )
 ----- sum_{j=0}^{k} binom(k,j) binom(2k-j,k-j) y^j + ( eps - --- ) y^k .
  k+1                                            (      k+1 )
```

Put `x = 1+y`.  For the first sum use
`binom(2k-j,k-j) = [z^k] z^j (1+z)^{2k-j}`:

```
sum_j binom(k,j) y^j z^j (1+z)^{2k-j}
   = (1+z)^{2k} ( 1 + y z/(1+z) )^k
   = (1+z)^k (1 + (1+y) z)^k ,
```

so the sum equals `[z^k] (1+z)^k (1+xz)^k = sum_i binom(k,i)^2 x^i`.
Therefore

```
                    1                            (       1  )
sum_i x_i x^i  =  ----- sum_i binom(k,i)^2 x^i + ( eps - --- ) (x-1)^k .   (2.3)
                   k+1                           (      k+1 )
```

Reading off the coefficient of `x^i` and using `(x-1)^k = sum_i (-1)^{k-i} binom(k,i) x^i`
gives the two displayed formulas, with `eps = 1` and `eps = 0`.  []

### Corollary 2.2 (complement closure; = Lemma 6.0 of the audited note)

`x_0 = 1` when `B` is in `T`, and `x_0 = 0` when `B` is not in `T`.  The only
`k`-set disjoint from `B` is `X \ B`.  Hence **`B` in `T` implies `X \ B` in
`T`**, and no block of `T` is disjoint from a non-block.

**Proof.**  `binom(k,0) = 1`, so `x_0 = (1 + k(-1)^k)/(k+1) = 1` for `k` even
when `B` is in `T`, and `x_0 = (1 - 1)/(k+1) = 0` otherwise.  []

### Corollary 2.3

`x_1 = x_{k-1} = 0` for `B` in `T`, and `x_1 = x_{k-1} = k` for `B` not in `T`.
Summing (2.3) at `x = 1` gives `sum_i x_i = binom(2k,k)/(k+1) = C_k` in both
cases, as it must.

### Corollary 2.4 (divisibility-admissible iff `k+1` is prime) **— criterion also at
`erdos_835_conjectural_resolution.md:78-87`, attributed there to Ma--Tang**

The standard derived numbers are all integral if and only if `k+1` is
prime.  In particular, an `S(k-1,k,2k)` exists only if `k+1` is prime.

**Proof.**  Existence forces every `lambda_j` in (2.1) to be an integer.  With
`m = k-j` this is `(k+1) | binom(k+m, m)` for `1 <= m <= k`.

*Sufficiency for divisibility-admissibility* (not for design existence): if
`k+1 = q` is prime and `1 <= m <= q-1`,
then `q-1+m = q + (m-1)` has base-`q` digits `(1, m-1)` while `m` has digits
`(0, m)`; Lucas gives `binom(q-1+m, m) = binom(1,0) binom(m-1,m) = 0` mod `q`.

*Necessity*: let `N = k+1` be composite with smallest prime factor `q`, so
`q <= N-1 = k`.  Take `m = q`.  Since `q | N`,

```
binom(N+q-1, q) = (N/q) * binom(N+q-1, q-1).
```

Write `N = q N_1`.  Then `N+q-1 = q(N_1+1) - 1` has base-`q` digits equal to
those of `N_1` followed by the digit `q-1`, while `q-1` has the single digit
`q-1`.  Lucas gives `binom(N+q-1, q-1) = 1` mod `q`, so `q` does not divide
it, so `N` does not divide `binom(N+q-1, q)`.  Hence `lambda_{k-q}` is not an
integer.  []

Consequently the admissible `k` in `(2, 40)` are exactly

```
k = 4, 6, 10, 12, 16, 18, 22, 28, 30, 36            (k+1 prime, k even).
```

---

## 3.  The link theorem

This holds at **every** rung and uses no complement structure.

### Theorem 3.1 (links are disjoint designs)

Let `D_1,...,D_r` be pairwise block-disjoint `S(t,t+1,n)`'s on `X`, let
`0 <= s <= t-1`, let `A_0` be an `s`-subset of `X` and `Y = X \ A_0`.  Put

```
D_i | A_0  :=  { B \ A_0 : B in D_i , A_0 subset of B } .
```

Then `D_1|A_0, ..., D_r|A_0` are **pairwise block-disjoint**
`S(t-s, t+1-s, n-s)`'s on `Y`.

**Proof.**  Let `A` be a `(t-s)`-subset of `Y`.  Then `A_0 u A` is a `t`-set,
so it lies in exactly one block `B` of `D_i`, and `B \ A_0` is the unique
member of `D_i|A_0` containing `A`.  So `D_i|A_0` is an `S(t-s,t+1-s,n-s)`.
If `B \ A_0 = B' \ A_0` with `B` in `D_i`, `B'` in `D_j`, then `B = B'`
(both equal `A_0 u (B \ A_0)`), so `i = j` by disjointness.  []

### Theorem 3.2 (the `(t-1)`-link is a one-factorisation deficiency)

Take `s = t-1` and `r = p-2`.  Then `|Y| = n-t+1 = p+1` is **even**, the links

```
M_i(A_0) := D_i | A_0
```

are `p-2` pairwise disjoint one-factors of the complete graph `K_Y`, and

```
R(A_0) := K_Y  \  ( M_1(A_0) u ... u M_{p-2}(A_0) )
```

is a **2-regular** graph on `p+1` vertices, i.e. a disjoint union of cycles.
Its edges are exactly the pairs `{y,y'}` with `A_0 u {y,y'}` in `E`.

**Proof.**  `S(1,2,p+1)` is a perfect matching, so each `M_i(A_0)` is a
one-factor; Theorem 3.1 gives disjointness.  `K_Y` is `p`-regular, and
removing `p-2` one-factors leaves a `2`-regular graph.  []

### Theorem 3.3 (link cycles are cycles of `G`)

Fix `A_0` in `C(X,t-1)`.  The map

```
  vertex  { y, y' } of the line graph  L(R(A_0))   |-->  block  A_0 u {y,y'} of E
  edge    y        of the line graph                |-->  edge   A_0 u {y}    of G
```

is an isomorphism of `L(R(A_0))` onto a subgraph of `G`.  Since `R(A_0)` is
2-regular, `L(R(A_0))` is isomorphic to `R(A_0)` itself.  Hence **every cycle
of `R(A_0)` of length `l` yields a cycle of `G` of length `l`.**

**Proof.**  Blocks `A_0 u {y,y'}` with `{y,y'}` in `R(A_0)` are residual by
Theorem 3.2, so they are vertices of `G`.  Let `y` be in `Y`.  The `t`-set
`A := A_0 u {y}` has residual extensions `A u {y'} = A_0 u {y,y'}` exactly for
`{y,y'}` in `R(A_0)`; there are exactly two, because `R(A_0)` is 2-regular.
So the `G`-edge `A` joins the two `R(A_0)`-edges at `y`, which is the defining
adjacency of the line graph.  A 2-regular graph is a disjoint union of cycles
and the line graph of a cycle of length `l` is a cycle of length `l`.  []

### Corollary 3.4 (local odd-cycle obstruction — an exact certificate)

If for some `A_0` in `C(X,t-1)` the 2-factor `R(A_0)` has a cycle of odd
length, then `G` is not bipartite; equivalently `1_D` is not in
`row M_D`, and `D_1,...,D_{p-2}` do **not** extend to a large set.

Such a certificate has size `l <= p+1` and is checkable in time
`O(p^2)` from the `p-2` link one-factors alone.

### Corollary 3.5 (`t = 1` is entirely local)

At `t = 1`, `C(X,t-1) = { empty set }`, `R(empty) = R`, and `G = L(R)`
exactly.  So at `t = 1` Corollary 3.4 is not merely necessary but also
sufficient: `G` is bipartite iff `R` is a union of even cycles.

### Proposition 3.6 (the authenticated negative control is a link triangle)

The Etzion--Hartman fixed partial at `(t,n,p) = (3,20,17)` with `r = 15`
systems carries the residual odd cycle recorded at
`collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md:676-680`
and hard-coded at
`collaboration/independent/conflict_cohomology_2026-07-29/verify_cochain_controls.py:29-33`
as the three `t`-sets

```
{0,14,17},  {5,14,17},  {2,14,17}.
```

All three contain `A_0 = {14,17}`, which has size `t-1 = 2`.  Therefore the
certificate is exactly the 3-cycle `0 - 2 - 5 - 0` of the link 2-factor
`R({14,17})` on the 18-point set `Y = X \ {14,17}` (`|Y| = p+1 = 18`), in the
sense of Theorem 3.3.

**Proof.**  Immediate from Theorem 3.3 and inspection of the three labels.
The three `G`-edges `A_0 u {0}`, `A_0 u {2}`, `A_0 u {5}` are precisely the
line-graph edges of the triangle on `{0,2,5}` in `R(A_0)`.  []

This is a check on Theorem 3.3, not a new fact about the EH partial: the only
authenticated top-of-repo negative certificate is an instance of the local
obstruction.

---

## 4.  The complement quotient at the top rung

Here `t = k-1`, `n = 2k`, `p = k+1`, `r = k-1`, `k` even.  Write
`iota(C) = X \ C`.

### Theorem 4.1 (`G` is a free `Z/2` double cover, and bipartiteness descends)

1. `E` is `iota`-invariant and `iota` acts **freely** on the vertices and on
   the edges of `G`.
2. No edge of `G` joins `C` to `iota(C)`.
3. Let `Gbar := G / iota`, a `k`-regular graph on `C_k` vertices with
   `k C_k / 2` edges.  Then

```
        G  is bipartite   <=>   Gbar  is bipartite.
```

4. If `G` is bipartite then **every** proper 2-colouring of `G` is
   `iota`-invariant.

**Proof.**
(1)  `C(X,k)` is `iota`-invariant and each `D_i` is `iota`-invariant by
Corollary 2.2, hence so is `E`.  `iota` has no fixed vertex because a `k`-set
never equals its complement in a `2k`-set.  An edge of `G` is an unordered
pair `{C_1,C_2}` of residual blocks with `|C_1 ∩ C_2| = k-1`, and the edge is
labelled by `A = C_1 ∩ C_2`.  Then `iota{C_1,C_2}` is labelled by
`X \ (C_1 u C_2)`, a `(k-1)`-set **disjoint** from `A`.  As `k >= 2` gives
`A` non-empty, the labels differ, so `iota` is free on edges.

(2)  If `C_1` and `C_2 = iota(C_1)` were adjacent they would share
`A = C_1 ∩ C_2 = empty`, contradicting `|A| = k-1 >= 1`.

(3)  (<=)  Pull back a proper 2-colouring of `Gbar`.  It is proper on `G`
because by (2) every `G`-edge projects to a genuine `Gbar`-edge.

(=>)  Let `E = P_1 u P_2` be a proper 2-colouring.  For every `A` in
`C(X,k-1)` the two residual extensions of `A` receive different colours, so
each `P_j` contains exactly one extension of every `(k-1)`-set: `P_1` and
`P_2` are `S(k-1,k,2k)`'s.  By Corollary 2.2 (which applies to *any*
`S(k-1,k,2k)` with `k` even) each `P_j` is closed under `iota`.  Hence the
colouring is `iota`-invariant, descends to `Gbar`, and is proper there.

(4)  Is exactly the argument just given.  []

### Corollary 4.2 (odd complement-walk certificate)

If for some residual block `C` there is a **walk of odd length** in `G` from
`C` to `X \ C`, then `G` is not bipartite and the family does not extend.

**Proof.**  By Theorem 4.1(4) a proper 2-colouring gives `C` and `X \ C` the
same colour, so every walk between them has even length.  []

This certificate format is genuinely different from an odd cycle: it is an
*open* walk, and it is available at every residual block.  It is a strict
consequence of Corollary 2.2 and has no analogue below the top rung, where
`E` need not be complement-closed.

---

## 5.  The hypothesis of the target theorem is empty on every decided
parameter

The theorem the assignment asks to decide is

> **(COT)**  Every `k-1` pairwise disjoint, complement-closed `S(k-1,k,2k)`'s
> possess a common odd transversal.

### Theorem 5.1 (vacuity)

For every admissible `k` with `2 < k < 16` there do **not** exist `k-1`
pairwise block-disjoint `S(k-1,k,2k)`'s.  Hence (COT) is vacuously true at
every such `k`, and has no instance there — neither a confirming one nor a
refuting one.

**Proof.**  By Corollary 2.4 the admissible `k` in that range are `4, 6, 10, 12`.
Let `M(k)` denote the maximum number of pairwise block-disjoint
`S(k-1,k,2k)`'s.

*`k = 4`, `k-1 = 3`.*  I give a self-contained derivation.  Apply
Theorem 3.1 with `s = 1`: the link of an `S(3,4,8)` at a point is an
`S(2,3,7)`, i.e. a Fano plane on the remaining 7 points, and the links of
pairwise disjoint systems are pairwise disjoint.  At most two Fano planes on
7 points are pairwise block-disjoint **[cited: Cayley 1850; also
`erdos_835_conjectural_resolution.md:361-362`]**.  Hence `M(4) <= 2 < 3`.
(The repository reaches `M(4) = 2` independently by enumerating all 30
labelled `S(3,4,8)` — `erdos_835_conjectural_resolution.md:363-364`.)

*`k = 6`, `k-1 = 5`.*  `M(6) = 2` **[cited: Kramer--Mesner, via
`erdos_835_conjectural_resolution.md:365-367`]**, so `M(6) = 2 < 5`.
(Theorem 3.1 with `s = 2` gives the weaker independent bound
`M(6) <= D(3,4,10) = 5` from the maximum number of pairwise disjoint
`SQS(10)` recorded at
`collaboration/opus5/full_problem_resume_2026-07-28/STATUS.md:95`; that alone
is exactly `k-1` and does **not** suffice, which is why the cited
Kramer--Mesner bound is needed.)

*`k = 10`.*  No `S(9,10,20)` exists at all, since ten-fold derivation
(Theorem 3.1) would produce an `S(4,5,15)`, proved nonexistent
**[cited: Mendelsohn--Hung, via `erdos_835_conjectural_resolution.md:368-369`]**.
So `M(10) = 0`.

*`k = 12`.*  No `S(11,12,24)` exists, since derivation would produce an
`S(4,5,17)`, proved nonexistent **[cited: Östergård--Pottonen, via
`erdos_835_conjectural_resolution.md:370-372`]**.  So `M(12) = 0`.

In every case `M(k) < k-1`.  []

### Corollary 5.2 (the only known instance of (COT) is `k = 2`)

At `k = 2` the hypothesis asks for `k-1 = 1` system, `S(1,2,4)`, which exists;
and `LS(1,2,4)` exists, so (COT) holds there.  `k = 2` is excluded from #835,
which asks for `k > 2`.  For every admissible `k > 2` that has been decided,
the hypothesis is unsatisfiable; for `k >= 16` nothing is known, including
whether a single `S(15,16,32)` exists.

### Corollary 5.3 (consequence for the attack)

(COT) cannot currently be refuted by any Steiner countermodel, because no
admissible Steiner instance of its hypothesis is known to exist.  Any
countermodel must be constructed at `k >= 16`, where the construction would
have to begin by exhibiting `k-1 >= 15` pairwise disjoint `S(k-1,k,2k)`'s —
which already implies the existence of a single `S(15,16,32)`, itself open.

Symmetrically, a proof of (COT) would reduce #835 to the existence of `k-1`
pairwise disjoint top systems and would not by itself decide #835.  This
matches the boundary already stated at
`collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md:636-642`;
Theorem 5.1 sharpens it from "the existence question remains" to "the
existence question is the *only* live question below `k = 16`, and it is
already decided negatively at every decided admissible `k`."

---

## 6.  The link tower for large sets

### Theorem 6.1 (the counting upper bound)

For `1 <= t <= k-1` set `v = k+1+t`.  The maximum possible number of pairwise
disjoint `S(t,t+1,v)`'s is at most `v - t = k+1`.

**Proof.**  A system has `lambda_0 = binom(v,t)/(t+1)` blocks, and pairwise
disjoint systems fit inside `binom(v,t+1)` blocks, so their number is at most

```
binom(v,t+1) (t+1) / binom(v,t)  =  (t+1) (v-t)/(t+1)  =  v - t = k+1 .    []
```

The bound need not be attained for an arbitrary parameter. The next theorem
shows that it is attained at every derived rung *conditional on* the assumed
top large set.

### Theorem 6.2 (large sets propagate down the tower)

If `LS(k-1,k,2k)` exists then `LS(t,t+1,k+1+t)` exists for every
`1 <= t <= k-1`.

**Proof.**  Take the `k+1` systems of the large set and apply Theorem 3.1 with
`s = k-1-t` at any `s`-subset `A_0`.  The result is `k+1` pairwise disjoint
`S(t,t+1,k+1+t)`'s on `X \ A_0`.  Their total block count meets the counting
upper bound in Theorem 6.1, so they exhaust `binom(k+1+t, t+1)` blocks and
form a large set.  []

At `t = 2` this says `LS(2,3,k+3)` must exist, which fails exactly for
`k = 4` (`LS(2,3,7)` does not exist), recovering the `k = 4` exclusion;
at `t = 3` it says `LS(3,4,k+4)` must exist, which fails for `k = 6`.
This reproduces the repository's exclusion table at
`collaboration/opus5/full_problem_resume_2026-07-28/STATUS.md:92-101`
from a single lemma.

---

## 7.  What is not proved here

* (COT) itself, in either direction, for any `k >= 16`.
* Whether `Gbar` (Theorem 4.1) admits an invariant unavailable to `G`.
* The converse of Corollary 3.4 — see `IDEAS.md`, Lemma LLS.
* Any existence statement for `S(15,16,32)` or for `k-1` disjoint copies.

No case of unrestricted #835 is resolved by this note.
