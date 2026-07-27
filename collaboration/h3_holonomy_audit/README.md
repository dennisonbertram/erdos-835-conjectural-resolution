# Independent holonomy audit

Date: 2026-07-27

Status: **rigorous necessary conditions and exact finite controls; no solution
of Erdős--Rosenfeld Problem #835.**

This directory is a self-contained audit of the holonomy arguments around a
putative \(LS(3,4,20)\).  It corrects the cycle-type universe from 231 to 55,
proves two additional cross-root laws, reproduces the cyclic
\(LS(2,3,19)\) controls, and independently audits
[`evidence/holonomy_group_algebra_tower.md`](../../evidence/holonomy_group_algebra_tower.md)
and its
[`verifier`](../../evidence/verify_holonomy_group_algebra_tower.py).

The only executable here uses the Python standard library and reconstructs
its cyclic large set from 74 small integers.  It imports nothing from the
rest of the repository.

## Reproduction

Fast default, including all structural checks, the pseudogluing, and a
deterministic 128-factorization affine smoke:

```text
python3 -B collaboration/h3_holonomy_audit/verify_holonomy_audit.py
```

Audited receipt:

```text
37/37 checks passed
seed=932741 samples=128 distinct=128 rank=51
```

Core only:

```text
python3 -B collaboration/h3_holonomy_audit/verify_holonomy_audit.py --core-only
```

Audited receipt:

```text
33/33 checks passed
```

Replay the reported 3,000-factorization experiment without repeating the
cyclic controls:

```text
python3 -B collaboration/h3_holonomy_audit/verify_holonomy_audit.py \
  --full --affine-only
```

Its deterministic result is:

```text
seed=932741 samples=3000 distinct=3000 rank=53
```

The full computation is optional because the default run is intended to
remain quick.  Arbitrary deterministic prefixes are available with
`--samples N`.

## Scope ledger

### Proved universally

The following statements hold for every large set with the indicated
parameters.  They do not depend on the cyclic example.

1. Every holonomy has exactly one fixed colour.  Consequently an
   \(S_{17}\) holonomy type is \((\lambda,1)\), where \(\lambda\) is a
   fixed-point-free partition of 16.  There are
   \[
   p(16)-p(15)=231-176=55
   \]
   such types, not 231.
2. The exact labelled group-algebra tower identity is
   \[
   \sum_{p\in X}H(c^p)=(t-1)H(c).
   \]
3. In an \(LS(2,3,19)\), the three holonomies attached to any point-triple
   obey an exact nonabelian cocycle:
   \[
   \sigma_k(i,j)\sigma_i(j,k)=\sigma_j(i,k).
   \]
   Hence each point-triple has zero or two odd holonomies.
4. The holonomy signs are encoded by a tournament on 19 points.  If \(d_i\)
   are its outdegrees and \(O\) is the total number of odd holonomies, then
   \[
   O=2\sum_i\binom{d_i}{2}
    =1368+\sum_i(d_i-9)^2,
   \qquad 1368\le O\le1938,\quad O\equiv0\pmod2.
   \]
5. If \(m_2(\kappa)\) is the number of 2-cycles in type \(\kappa\), then
   every one-factorization of \(K_{18}\), and therefore every
   \(LS(2,3,19)\), obeys
   \[
   \sum_\kappa m_2(\kappa)N_\kappa\equiv0\pmod2.
   \]
6. The augmented transitions are a pure-gauge cocycle and satisfy the exact
   autocorrelation identity described below.

### Exact finite computations

The verifier checks these statements for the repository's particular cyclic
\(LS(2,3,19)\):

| quantity | exact value |
|---|---:|
| unordered holonomies | \(19\binom{18}{2}=2907\) |
| nonzero cycle-type coordinates | 34 of 55 |
| cycle-type coordinates with odd count | 17 |
| odd holonomies \(O\) | 1530 |
| root odd-count multiset | \(73^{\times17},136,153\) |
| 2-cycle-weighted census | 1938 |
| point-triples with 0 / 2 odd holonomies | 204 / 765 |
| oriented exact-\(H\) summands | 5814 |
| distinct labelled permutations in exact \(H\) | 5814 |

The verifier also reconstructs twenty transported genuine links that pass
all 190 overlap-resolved exact-\(H\) fingerprint equalities but disagree in
27,478 of 29,070 pairwise overlap comparisons.

Finally, the deterministic 3,000-\(K_{18}\)-factorization computation has
3,000 distinct 55-bit parity vectors and affine rank 53.

### Still open

Nothing here proves that twenty \(LS(2,3,19)\) links can or cannot satisfy
their full cellwise compatibility.  In particular:

- no \(LS(3,4,20)\) is constructed or excluded;
- no \(LS(15,16,32)\), equivalent \(k=16\) tight colouring, or its
  one-point normalization is constructed or excluded;
- the existential quantifier over all \(k>2\) in Erdős--Rosenfeld #835 is
  untouched.

The 3,000-factorization rank result rules out an additional affine
\(\mathbb F_2\) equation only at the **standalone one-factorization level**.
It says nothing by itself about compatibility among different point links,
and it is not evidence that #835 has been decided.

## 1. Definitions

Let
\[
c:\binom X{t+1}\longrightarrow[m]
\]
be an \(LS(t,t+1,v)\) colouring.  For each \(t\)-set \(T\), its rainbow star
is the bijection
\[
\chi_T:X\setminus T\longrightarrow[m],
\qquad \chi_T(x)=c(T\cup\{x\}).
\]
For \(R\in\binom X{t-1}\) and distinct \(a,b\notin R\), define
\[
\sigma_R(a,b)=\chi_{R\cup\{b\}}\chi_{R\cup\{a\}}^{-1},
\]
extended at the common colour
\[
d=c(R\cup\{a,b\})
\]
by fixing \(d\).  The orientation used throughout is
\[
\sigma_R(b,a)=\sigma_R(a,b)^{-1}.
\]

For an \(LS(2,3,19)\), write \(\sigma_i(j,k)\) when \(R=\{i\}\).
The unordered central census is
\[
N_\kappa
=\#\{(i,\{j,k\}):\operatorname{type}\sigma_i(j,k)=\kappa\}.
\]

## 2. Unique fixed colour and the 55-type correction

The common colour \(d=c(Rab)\) is fixed by construction.  Suppose another
colour \(e\ne d\) were fixed.  Put
\[
x=\chi_{R\cup\{a\}}^{-1}(e).
\]
Since \(e\ne d\), \(x\ne b\).  The equation \(\sigma_R(a,b)(e)=e\) would then
give
\[
c(Rax)=c(Rbx)=e.
\]
Those two blocks both contain the \(t\)-set \(R\cup\{x\}\), contradicting
the rainbow-star property at that \(t\)-set.  Thus \(d\) is the unique fixed
colour.

For \(m=17\), deleting that unique 1-cycle leaves a partition of 16 with no
part 1.  The number of such partitions is
\[
p(16)-p(15)=55.
\]
The subtraction is the bijection that removes one 1 from a partition of 16
having a 1.  Counting all partitions of 17 that have at least one 1 would
give \(p(16)=231\), but that permits extra fixed colours and is therefore too
weak.  All central parity vectors in this audit use exactly 55 coordinates.

## 3. Exact group-algebra tower

Define
\[
H(c)=
\sum_{\substack{R\in\binom X{t-1}\\a,b\notin R,\ a\ne b}}
[\sigma_R(a,b)]\in\mathbb Z[S_m].
\]
This is a sum of labelled permutations, not merely conjugacy classes.

For a derived colouring \(c^p\), a summand indexed by
\((R',a,b)\) is exactly
\[
\sigma_{R'}^{c^p}(a,b)
=\sigma_{R'\cup\{p\}}^c(a,b).
\]
A fixed top summand indexed by \((R,a,b)\) occurs for each \(p\in R\), hence
exactly \(t-1\) times.  Coefficientwise,
\[
\boxed{\sum_{p\in X}H(c^p)=(t-1)H(c).}
\]

At the \(LS(3,4,20)\) rung this becomes
\[
\sum_{p\in X}H(c^p)=2H(c).
\]
After all twenty link colour sets have been aligned with the one inherited
17-colour set, every labelled permutation has even total coefficient across
the links.  Projecting to conjugacy classes yields 55 central parity
conditions.  Colour alignment is essential: independently relabelling an
abstract link conjugates its exact \(H\).

## 4. Cross-root nonabelian cocycle

Fix distinct \(i,j,k\), let \(e=c(ijk)\), and put
\[
Y=X\setminus\{i,j,k\}.
\]
Restrict the three pair-star maps to bijections from \(Y\) to the same set
\([17]\setminus\{e\}\):
\[
A=\chi_{ij}|_Y,\qquad B=\chi_{ik}|_Y,\qquad C=\chi_{jk}|_Y.
\]
On the 16 noncommon colours,
\[
\sigma_i(j,k)=BA^{-1},\qquad
\sigma_k(i,j)=CB^{-1},\qquad
\sigma_j(i,k)=CA^{-1}.
\]
All three fix \(e\), so the equality extends to all 17 colours:
\[
\boxed{\sigma_k(i,j)\sigma_i(j,k)=\sigma_j(i,k).}
\]

Taking signs shows that a point-triple has zero or two odd holonomies.  More
finely, after deleting the common fixed colour, the three conjugacy classes
in \(S_{16}\) must have a positive connection coefficient.  Thus any
cycle-census feasibility model may be strengthened by class-product support
and marginal constraints.  This is a necessary condition; no contradiction
from it is presently known.

## 5. Tournament formula

Order \(X=\{0,\ldots,18\}\).  Let \(e_{ij}\) be the sign of the pair-star
bijection \(\chi_{ij}\), using the increasing order on
\(X\setminus\{i,j\}\) and the natural colour order.  Define
\[
t_{ij}=(-1)^{i+j+\mathbf1_{i>j}}e_{ij}.
\]
Because \(e_{ij}=e_{ji}\), exactly one of the two indicator exponents changes,
and
\[
t_{ji}=-t_{ij}.
\]
The \(t_{ij}\) therefore orient \(K_{19}\).

A direct deletion-order sign calculation gives
\[
\boxed{\operatorname{sgn}\sigma_i(j,k)=-t_{ij}t_{ik}.}
\]
At root \(i\), the holonomy is odd exactly when \(j\) and \(k\) are both
out-neighbours or both in-neighbours.  If \(d_i\) is the outdegree, the
number of odd holonomies at that root is
\[
\binom{d_i}{2}+\binom{18-d_i}{2}
=72+(d_i-9)^2.
\]

Every transitive tournament triangle contributes one out-neighbour pair at
its source and one in-neighbour pair at its sink; a cyclic triangle
contributes neither.  Therefore
\[
O
=2\,\#\{\text{transitive triangles}\}
=2\sum_i\binom{d_i}{2}
=1368+\sum_i(d_i-9)^2.
\]
The lower bound follows from the square sum.  There are at most
\(\binom{19}{3}=969\) transitive triangles, giving the upper bound:
\[
1368\le O\le1938.
\]

For the cyclic large set, the verifier obtains \(O=1530\), exactly 765
transitive and 204 cyclic point-triples.

## 6. The universal 2-cycle parity

Consider one labelled one-factorization \(F\) of \(K_{18}\), with perfect
matching \(M_c\) for colour \(c\).  A 2-cycle \(c\leftrightarrow d\) in
\(\sigma(a,b)\) is equivalent to distinct \(x,y\notin\{a,b\}\) satisfying
\[
F(ax)=c,\quad F(bx)=d,\quad
F(ay)=d,\quad F(by)=c.
\]
Equivalently, \(a-x-b-y-a\) is a 4-cycle component of \(M_c\cup M_d\).
Every such alternating 4-cycle produces the same 2-cycle for its two
opposite base pairs.  Hence
\[
\sum_{\{a,b\}}\#\{\text{2-cycles of }\sigma(a,b)\}
=2\sum_{\{c,d\}}\#\{\text{4-cycle components of }M_c\cup M_d\}.
\]
The left side is even.  Summing over roots proves
\[
\sum_\kappa m_2(\kappa)N_\kappa\equiv0\pmod2.
\]
The cyclic value is 1938, so divisibility by four is false in general.

Together with the total and tournament-sign laws, any
\(LS(2,3,19)\) central parity vector obeys at least
\[
\sum_\kappa N_\kappa=1,\qquad
\sum_{\kappa\text{ odd}}N_\kappa=0,\qquad
\sum_\kappa m_2(\kappa)N_\kappa=0
\pmod2.
\]
The middle equation uses cross-root compatibility; the first and third
already hold for a standalone \(K_{18}\) one-factorization.

## 7. Augmented transitions

For a fixed root, let \(Y\) be the 18 vertices of its one-factorization.
Adjoin a colour \(\infty\) and define charts
\[
\widehat\chi_a(a)=\infty,\qquad
\widehat\chi_a(x)=F(ax)\quad(x\ne a).
\]
Put
\[
\tau(a,b)=\widehat\chi_b\widehat\chi_a^{-1}\in S_{18}.
\]
Then cancellation gives the exact cocycle
\[
\tau(b,c)\tau(a,b)=\tau(a,c).
\]
If \(d=F(ab)\), then
\[
\tau(a,b)=(\infty\,d)\sigma(a,b),
\]
where \(\sigma\) is extended to fix \(\infty\).  Since \(d\) is the unique
fixed colour of \(\sigma\), every \(\tau(a,b)\) is a derangement.

Choose a reference \(a_0\), set
\[
g_a=\widehat\chi_a\widehat\chi_{a_0}^{-1},
\qquad G=\sum_a[g_a],
\]
and let \(^{*}\) denote inversion.  Exact multiplication in the group
algebra gives
\[
\boxed{
\sum_{a\ne b}[\tau(a,b)]+18[e]=GG^{*}.
}
\]
Every unitary representation therefore yields a positive-semidefinite
matrix.  This is an autocorrelation law for the augmented \(\tau\), not
directly for the original \(\sigma\)-sum: the transposition
\((\infty\,d)\) varies with the edge.

## 8. Exact audit of `holonomy_group_algebra_tower.*`

The current note and verifier were inspected formula by formula and replayed.
The source verifier reports:

```text
19/19 checks passed
```

The following parts are correct:

1. the orientation and coefficientwise indexing proof of the exact
   group-algebra tower;
2. the proof that the common colour is the unique fixed point;
3. the current corrected count of 55 possible \(S_{17}\) types;
4. central projection as twice the unordered census;
5. flatness of the natural permutation representation;
6. the pairwise overlap equality
   \[
   H_{\{q\}}(c^p)=H_{\{p\}}(c^q);
   \]
7. the augmented cocycle, its relation to \(\sigma\), and the distinction
   between \(\tau\)-autocorrelation positivity and the original \(H\);
8. the cyclic exact-\(H\) support count and pseudogluing receipts.

One coverage distinction is worth recording: the source verifier directly
tests the tower, central projection, unique fixed point, natural flatness,
the augmented cocycle and \(\tau/\sigma\) conversion, and the pseudogluing.
Its note proves the augmented autocorrelation identity algebraically, but
the source verifier does not separately name that identity as a check.  The
independent verifier in this directory checks the exact autocorrelation
Counter identity at all 19 cyclic roots.

### What the 1,592 / 27,478 receipt means

Let \(L\) be the cyclic \(LS(2,3,19)\) on a point set \(P\).  Label the edges
of \(K_{20}\) by the 19 factors of a round-robin one-factorization.  At every
vertex \(p\), incident edge labels give a bijection
\[
f_p:[20]\setminus\{p\}\longrightarrow P.
\]
Transport \(L\) through \(f_p\) to obtain a genuine link \(L_p\).

For an edge \(pq\) labelled \(r\), the \(q\)-root local exact-\(H\) fingerprint
in \(L_p\) and the \(p\)-root fingerprint in \(L_q\) are both transported
copies of \(H_r(L)\).  All 190 fingerprint equalities therefore hold.

Actual cellwise overlap is much stricter.  For each root pair \(p,q\) and
each pair \(a,b\) outside it, compare
\[
L_p(qab)\quad\text{with}\quad L_q(pab).
\]
There are
\[
\binom{20}{2}\binom{18}{2}
=190\cdot153
=29\,070
=6\binom{20}{4}
\]
such **pairwise comparisons**.  They are not 29,070 distinct cells: each of
the 4,845 quadruples is seen in four links and contributes six pairwise
comparisons.  The exact census is
\[
1\,592\text{ agreements},\qquad27\,478\text{ disagreements}.
\]

Thus even all overlap-resolved local exact-\(H\) fingerprints are
insufficient for gluing.  The fingerprint sums over which base pair produced
each permutation and loses decisive point-labelled correspondence.

## 9. The deterministic affine-rank experiment

Index the 55 possible types and associate to a standalone labelled
one-factorization \(F\) of \(K_{18}\) the parity vector
\[
v(F)_\kappa=N_\kappa(F)\pmod2\in\mathbb F_2^{55}.
\]
Every such vector obeys two independent affine equations:
\[
\mathbf1\cdot v(F)=153=1\pmod2,
\qquad
(m_2\bmod2)\cdot v(F)=0.
\]
Hence their affine hull has dimension at most \(55-2=53\).

The full verifier uses `random.Random(932741)`.  For each sample it starts
with all 153 edges, recursively chooses a perfect matching in the remaining
graph for each of 17 colours, and restarts if completion fails.  It then
independently checks that:

- all 153 edges occur exactly once;
- every factor has degree one at every vertex;
- all 153 holonomies have one of the 55 permitted types;
- both affine equations hold.

For the first 3,000 generated factorizations, all 3,000 parity vectors are
distinct and
\[
\operatorname{rank}_{\mathbb F_2}
\{v_i+v_0:1\le i<3000\}=53.
\]
Because this reaches the maximum, the annihilator has dimension two and is
exactly the span of the total and 2-cycle masks.  Therefore there is no third
affine \(\mathbb F_2\) equation that holds for **all standalone
one-factorizations of \(K_{18}\)**.

This conclusion is a finite spanning-witness result, not a probabilistic
inference.  Its scope is nonetheless narrow: an \(LS(2,3,19)\) couples 19
one-factorizations, and a putative \(LS(3,4,20)\) couples twenty entire links.
Cross-root identities can impose equations absent from isolated factors--the
tournament sign equation is an explicit example.  The rank experiment
neither models those couplings nor resolves #835.
