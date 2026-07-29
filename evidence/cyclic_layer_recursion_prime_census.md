# The cyclic layer recursion across the prime cases

**Scope, stated first.** Nothing in this note solves, or claims to solve,
Erdős–Rosenfeld Problem #835, which remains **open**. Everything here is about
the *cyclic ansatz*: the hypothesis that a tight \((k+1)\)-colouring of
\(J(2k,k)\) exists which is equivariant for a colour-transitive \(\mathbb Z_p\)
translation action, \(p=k+1\) prime. A no-go for the cyclic ansatz at some \(k\)
is **not** a no-go for #835 at that \(k\); a witness for the cyclic ansatz at
\(k=16\) would be an intermediate object, not a solution.

Verifier: `evidence/verify_cyclic_layer_recursion_prime_census.py` (stdlib
only, no solver). Every existence claim below is a witness that the verifier
re-checks; every non-existence claim is an exhaustive search that terminates.

---

## 1. The general-\(p\) setting, and what layer 1 actually is

The reduction in `cyclic17_equivariant_reduction.md` is written at \(p=17\). It
generalises verbatim. Split the \(2k\) points as
\[
 A\sqcup F,\qquad A=\mathbb Z_p,\quad p=k+1,\quad |F|=k-1=p-2,
\]
with \(x\mapsto x+1\) on \(A\) fixing \(F\) and sending colour \(q\) to \(q+1\).
No \(k\)-subset is fixed by the translation (a fixed block would need
\(X\in\{\varnothing,\mathbb Z_p\}\), forcing \(|Y|=p-1>p-2\)), so every block
orbit has length \(p\) and the layer recursion of that note applies unchanged.

**Lemma 1 (layer 1).** *The \(|R|=1\) layer of the cyclic ansatz is precisely a
partition of the edge set of the complete graph on \(\mathbb Z_p\setminus\{0\}\)
into \(p-2\) starters.*

*Proof.* For \(R=\{i\}\) and \(|U|=1\), the rainbow condition reads
\(\{x\}\sqcup\{S_i(x,a):a\ne x\}=\mathbb Z_p\), i.e. \(S_i\) is a symmetric
idempotent Latin square, translation-equivariant by (4). Such a square is
determined by its colour-zero class \(M_i=S_i^{-1}(0)\), a perfect matching of
\(\mathbb Z_p\setminus\{0\}\); equivariance makes the colouring proper exactly
when \(M_i\) meets every difference class \(\{d,-d\}\) once, i.e. \(M_i\) is a
**starter** of \(\mathbb Z_p\). Cross-\(R\) compatibility at \(s=1\) says
\(S_i(x,y)\ne S_j(x,y)\) for all \(i\ne j\) and \(x\ne y\); since
\(S_i(x,y)=c\iff (x-c,y-c)\in M_i\), that is exactly \(M_i\cap M_j=\varnothing\).
Finally \((p-2)\cdot\frac{p-1}{2}=\binom{p-1}{2}\), so \(p-2\) pairwise disjoint
starters partition the edge set. \(\square\)

We call such a partition a **golf design of \(\mathbb Z_p\)**. The verifier
checks directly that the Wallis circulant used throughout this repository is
one, for \(p=17\).

---

## 2. Theorem A — multiplier rigidity at a Fermat prime

Write \(P=\{\{x,-x\}:x\ne0\}\), the *patterned starter*. For a golf design
\(D\) let \(H=\{m\in\mathbb Z_p^{*}: mD=D\}\) be its **multiplier group**.

> **Theorem A.** Let \(p\) be a Fermat prime, \(p-1=2^{n}\) with \(n\ge2\), and
> let \(D\) be a golf design of \(\mathbb Z_p\). Then either \(H=\{1\}\), or
> \(H=\{1,-1\}\) and \(P\in D\).

*Proof.*

1. For \(m\in\mathbb Z_p^{*}\), \(mM\) is a starter whenever \(M\) is: \(m\)
   permutes \(\mathbb Z_p\setminus\{0\}\) and multiplies the difference set by
   \(m\), which permutes the difference classes. So \(H\) is a group acting on
   the \(p-2\) members of \(D\).
2. **If \(-M=M\) then \(M=P\).** For \(e=\{x,y\}\in M\) the edge \(-e\) also
   lies in \(M\) and has the *same* difference class as \(e\). A starter holds
   exactly one edge per class, so \(-e=e\), i.e. \(y=-x\). Every edge of \(M\)
   is therefore \(\{x,-x\}\), and \(M\) being a perfect matching of
   \(\mathbb Z_p\setminus\{0\}\) forces \(M=P\).
3. \(\mathbb Z_p^{*}\) is cyclic of order \(2^{n}\), so it has a **unique**
   involution, namely \(-1\), and every nontrivial subgroup contains it.
4. Let \(M\in D\) have nontrivial stabiliser \(H_M\le H\). By 3 applied to
   \(H_M\) we get \(-1\in H_M\), so \(-M=M\) and \(M=P\) by 2. Hence every
   member of \(D\) other than \(P\) has trivial stabiliser and lies in an
   \(H\)-orbit of full size \(|H|\).
5. Count members. If \(P\notin D\) then \(p-2=2^{n}-1=|H|\cdot t\); the left
   side is odd and \(|H|\) is a power of two, so \(|H|=1\). If \(P\in D\) then
   the other members number \(p-3=2^{n}-2=2(2^{n-1}-1)\) with \(2^{n-1}-1\)
   odd, so \(|H|\) divides \(2\). \(\square\)

**The bound is attained at \(p=17\).** This work exhibits a golf design of
\(\mathbb Z_{17}\) with \(H=\{1,16\}\); it is listed as `SYMMETRIC_GOLF_17` in
the verifier, has \(P\) as its starter 0, and its remaining fourteen starters
fall into seven negation-swapped pairs.

**The repository's Wallis design has \(H=\{1\}\)** (verified), and \(P\) is not
one of its starters — consistent with, and explained by, Theorem A.

**Why this is Fermat-specific.** The proof uses only that \(p-1\) is a power of
two. At \(p=13\) it fails, and genuinely so: the verifier finds that the golf
design of \(\mathbb Z_{13}\) has multiplier group \(\{1,3,9\}\), of order 3.

**Consequence for the \(k=16\) search.** Any symmetry of the joint radius-five
phase system that is induced by the ambient affine group of \(\mathbb Z_{17}\)
lies in \(H\), so it has order at most 2. (This does not exclude symmetries of
the constraint hypergraph that are not of ambient affine origin; none is
claimed.) In particular no Singer-, Paley- or \(\mathrm{GF}\)-style multiplier
group can act transitively, or even with large orbits, on the fifteen links.
That is a precise limit on the "field/character construction" route, and it
matches the independently recorded fact that the labelled Wallis quotient
instance has automorphism group of order one.

---

## 3. Theorem B — the layer-1 census

The verifier enumerates every starter of \(\mathbb Z_p\) by two independent
algorithms (recursion on the least unmatched point; and filtering all perfect
matchings) and computes the exact maximum pairwise-disjoint family by
branch and bound.

| \(k\) | \(p\) | starters of \(\mathbb Z_p\) | max pairwise disjoint | need \(p-2\) | golf design |
|---|---|---|---|---|---|
| 2 | 3 | 1 | 1 | 1 | **exists** |
| 4 | 5 | 1 | 1 | 3 | **impossible** |
| 6 | 7 | 3 | 3 | 5 | **impossible** |
| 10 | 11 | 25 | 7 | 9 | **impossible** |
| 12 | 13 | 133 | 11 | 11 | **exists** (exactly tight) |
| 16 | 17 | — (not enumerated) | \(\ge15\) | 15 | **exists** (Wallis; also a symmetric one) |

> **Theorem B.** There is no \(\mathbb Z_p\)-equivariant colour-transitive tight
> \((k+1)\)-colouring of \(J(2k,k)\) for \(k=4,6,10\): by Lemma 1 such a
> colouring requires a golf design of \(\mathbb Z_p\), and none exists.

The \(k=2\) row is the mandated control: a tight colouring *does* exist there,
and the layer-1 test correctly does not fire.

---

## 4. Theorem C — \(k=12\) is completely resolved, at layer 2

\(\mathbb Z_{13}\) has **exactly 4** golf designs (exhaustive clique
enumeration over the 133 starters). All four lie in a single orbit under
multiplication by \(\mathbb Z_{13}^{*}\).

For each of the four, the verifier runs an exhaustive bitmask exact-cover
search over all 55 fixed pairs, asking for one translate of each of the 22
triple orbits decomposing \(K_{13}-M_i-M_j\):

| design | slices feasible (witness verified) | slices proved infeasible |
|---|---|---|
| 0 | 24 | 31 |
| 1 | 24 | 31 |
| 2 | 24 | 31 |
| 3 | 24 | 31 |

> **Theorem C.** There is no \(\mathbb Z_{13}\)-equivariant colour-transitive
> tight 13-colouring of \(J(24,12)\). Layer 1 exists, but for every golf design
> 31 of the 55 prescribed-link cyclic slices do not exist.

The mechanism matters: at \(k=12\) the failure is at a **single slice**, not in
the coupling between slices. This is a strictly weaker kind of failure than the
one the \(k=16\) search is up against, where all 105 slices do exist.

**Refuted hypothesis.** It is natural to guess that slice feasibility is decided
by the cycle type of the 2-regular graph \(M_i\cup M_j\) (the invariant already
used in this repo to fingerprint Wallis factors). It is not. Over the
\(4\times55=220\) pairs:

| cycle type of \(M_i\cup M_j\) | infeasible | feasible |
|---|---|---|
| \((4,4,4)\) | 4 | 4 |
| \((4,8)\) | 12 | 36 |
| \((6,6)\) | 4 | 4 |
| \((12)\) | 104 | 52 |

Every type yields both outcomes, so no function of the cycle type can decide
slice feasibility. Recorded so the hypothesis is not re-tried.

---

## 5. Where \(k=16\) sits

Combining Theorem B, Theorem C and the repository's existing certificates:

| \(k\) | layer 1 (golf design) | single slices | joint layer 2 |
|---|---|---|---|
| 2 | exists | — (no free layer) | — |
| 4, 6, 10 | **impossible** | — | — |
| 12 | exists (4 of them) | **31 of 55 fail** | dead |
| 16 | exists (Wallis, and a symmetric one) | **all 105 exist** | open |

\(k=16\) is the **first prime case in which the cyclic route survives layer 1
and every single slice**, and therefore the first in which the genuinely coupled
boundary is reached at all. That reframes the current 4,200-phase search: it is
not grinding on a problem that smaller cases suggest is routine — it is at the
first point where the question is even posed.

Two further facts about \(p=17\), both confirmed here:

* Each of the 40 triple-orbit **columns** is individually feasible — the 105
  phases of one orbit satisfying only the 15 cross `AllDifferent(14)`
  constraints. Together with the 105 individually feasible rows, this locates
  any obstruction squarely in the coupling. *This is not new*: the existing
  `search_radius5_golf_cyclic_alternating_projection.py` and
  `search_cyclic17_vertex_degree_alternating_projection.py` already solve each
  column separately in `project_one_column`. It is recorded here only because
  the row side is documented and the column side was not.
* For the \((-1)\)-symmetric golf design, the induced permutation \(\sigma\) of
  the fifteen starters fixes exactly one (namely \(P\)) and swaps seven pairs;
  the induced permutation \(\tau\) of the forty triple orbits fixes exactly 8.

### 5.1 Cross-validation of the general-\(p\) machinery

The general-\(p\) code path was written independently of the existing \(p=17\)
scripts. Run at \(p=17\) on the Wallis design it reproduces the recorded numbers
exactly: \(|B_c(q)|\) histogram \(\{1:120,\ 3:560\}\); the
\(2\)-\((15,3,16)\) multidesign with each golf square in 112 triple holes and
each pair of squares in 16; 456 allowed triple-translates per fixed pair;
47,880 primary phase literals; and the phase-domain distribution
\[
 2{,}658\text{ of size }11,\quad 1{,}407\text{ of }12,\quad
 132\text{ of }13,\quad 3\text{ of }14 .
\]
That is the distribution recorded in `cyclic17_equivariant_reduction.md`,
obtained here from a separate implementation.

The same run on the \((-1)\)-symmetric design gives identical **aggregate**
invariants — 47,880, 456, 112, 16 — which confirms that these are forced by the
golf-design axioms and are design-independent. Its **fine** distribution
differs, and is slightly tighter:
\(2{,}662\) of size 11, \(1{,}396\) of 12, \(142\) of 13, none of 14. So the
symmetric design buys a factor-2 symmetry at the cost of marginally smaller
phase domains. Which effect dominates for search is not established here.

---

## 6. The \(\mathbb Z_2\)-equivariant reduction (new, and available only now)

Because \(-1\) is a multiplier of `SYMMETRIC_GOLF_17`, the joint layer-2 system
for that design carries an involution. With \(-T_q=T_{\tau(q)}+a_q\),

\[
 \Phi\ \longmapsto\ \Phi',\qquad
 \Phi'(\sigma i,\sigma j,\tau(q))=a_q-\Phi(i,j,q)
\]

maps solutions to solutions: the selected triple \(T_q+\Phi\) negates to
\(T_{\tau(q)}+(a_q-\Phi)\), the residual graph \(K_{17}-M_i-M_j\) maps to
\(K_{17}-M_{\sigma i}-M_{\sigma j}\), and the cross constraints transport. It is
an involution exactly because \(a_{\tau(q)}=a_q\), which follows from negating
twice.

Imposing \(\Phi'=\Phi\) halves the free phases. On cells fixed by the symmetry
(\(\{\sigma i,\sigma j\}=\{i,j\}\) and \(\tau(q)=q\)) the phase is *forced* to
\(a_q/2 \bmod 17\). For the design tabulated above as `SYMMETRIC_GOLF_17`,
every such forced value was checked to lie inside its own domain (zero
conflicts), so equivariant solutions are not excluded on those grounds. The
same check has not been run on the other two symmetric designs found.

### 6.1 Executable checks on the reduction

`evidence/verify_cyclic17_z2_equivariant_reduction.py` (stdlib only, no solver)
verifies every structural claim above against the certificate
`evidence/cyclic17_symmetric_golf_design.json`
(SHA-256 `573e381dde4562b4076c76f687d33367db6a555b2ac43a04880d6de0be5bb593`):

| check | result |
|---|---|
| certificate is a golf design of \(\mathbb Z_{17}\), multiplier group \(\{1,16\}\), member 0 is \(P\) | ok |
| \(\sigma^2=\mathrm{id}\) on the 15 starters | ok |
| \(\tau^2=\mathrm{id}\) on the 40 triple orbits | ok |
| \(a_{\tau(q)}=a_q\) for all 40 orbits (this is what makes \(\Phi\mapsto\Phi'\) an involution rather than a 4-cycle) | ok |
| \(\sigma\) cycle type: 1 fixed starter (\(P\)) + 7 transpositions \(=1+2\cdot7=15\) | ok |
| \(\tau\) cycle type: 8 fixed orbits + 16 transpositions \(=8+2\cdot16=40\) | ok |
| \(s\in F_i(q)\iff a_q-s\in F_{\sigma i}(\tau q)\), all \(15\cdot40=600\) pairs | ok |
| domain transport: each of the **4,200** cell domains maps *onto* its image's domain | ok |
| \(\sigma\)-fixed pairs are exactly the 7 transpositions, so forced cells \(=7\times8=\mathbf{56}\) | ok |
| all 56 forced values \(a_q/2 \bmod 17\) lie inside their own domains (0 violations) | ok |
| orbit count: 4,200 cells \(\to\) 2,128 orbits \(=56\) singletons \(+\,2{,}072\) pairs | ok |

So the reduced model has **2,072 free phases instead of 4,200** (49.3%), with 56
phases forced to constants.

### 6.2 Verdict on the reduced model, with exact scope

`evidence/search_cyclic17_z2_equivariant_radius5.py` builds the model on
involution orbits (a genuine reduction, not added equality constraints) and
reports the free/forced split as 2,072 / 56 / 4,200, matching §6.1.

A 420-second single-worker run returned

```text
status UNKNOWN after 420.0s, 4126421 branches, 360839 conflicts
```

**`UNKNOWN` is a resource result and is not evidence of anything.** For
reference the recorded unreduced compact CP-SAT run returned `UNKNOWN` after
1,207 s, 6,460,436 branches and 1,041,651 conflicts; the two runs were made on
different machine loads, so the branch rates are not a controlled comparison
and no speed claim is made.

Scope, precisely:

* A **witness** would be an equivariant radius-five boundary for one
  non-Wallis golf design. That is an intermediate layer-2 object — not an
  \(LS(15,16,32)\), and not a resolution of #835.
* **`INFEASIBLE`** would exclude only the \(\mathbb Z_2\)-*equivariant*
  solutions for *this* golf design. It would say nothing about non-equivariant
  solutions for the same design, nothing about the Wallis design, and nothing
  about #835.
* Neither has been obtained. **Whether an equivariant witness exists is not
  settled.**

This is the first non-Wallis starting point used here for the radius-five
search.  Theorem A says that negation is the only possible nontrivial
multiplier symmetry type at \(p=17\); it does not single out this design
among the three negation-symmetric designs found.

---

## 7. What is not claimed

* No statement about #835 itself. It remains open.
* Theorems B and C are about the cyclic ansatz only. \(k=4,6,10,12\) are
  already known to admit no tight colouring at all; these give an independent
  and much shorter proof *for the equivariant case*, nothing more.
* Nothing here shows the \(k=16\) joint layer 2 is feasible or infeasible.
* The number of starters of \(\mathbb Z_{17}\), and the number of golf designs
  of \(\mathbb Z_{17}\), were not computed.
* The \(k=16\) analogue of Theorem C — whether some *other* golf design of
  \(\mathbb Z_{17}\) has infeasible slices — was not settled. A CP-SAT survey
  of all 105 slices for the symmetric designs was started and did not finish;
  no result is claimed.
* The \(\mathbb Z_2\)-equivariant radius-five model returned `UNKNOWN`; neither
  a witness nor an infeasibility proof was obtained.
* Nothing here is an all-layer construction or an unrestricted theorem, so
  **no claim is made that #835 is solved.**

---

## 8. Artifacts and reproduce

| file | what |
|---|---|
| `cyclic_layer_recursion_prime_census.md` | this note |
| `verify_cyclic_layer_recursion_prime_census.py` | Theorems A/B/C + cross-check; stdlib, no solver |
| `cyclic17_symmetric_golf_design.json` | the \((-1)\)-symmetric golf design of \(\mathbb Z_{17}\) |
| `verify_cyclic17_z2_equivariant_reduction.py` | §6.1 structural checks; stdlib, no solver |
| `search_cyclic17_z2_equivariant_radius5.py` | §6.2 orbit-variable search (CP-SAT) |

```sh
# full census, including the exhaustive p=13 slice proof (slow part, ~6 min)
python3 -B evidence/verify_cyclic_layer_recursion_prime_census.py

# everything except the p=13 exhaustive slice census
python3 -B evidence/verify_cyclic_layer_recursion_prime_census.py --quick

# the Z_2 reduction is well defined, and its exact size
python3 -B evidence/verify_cyclic17_z2_equivariant_reduction.py

# search the reduced model (UNKNOWN so far; UNKNOWN is never evidence)
python3 -B evidence/search_cyclic17_z2_equivariant_radius5.py \
    --seconds 600 --workers 1
```
