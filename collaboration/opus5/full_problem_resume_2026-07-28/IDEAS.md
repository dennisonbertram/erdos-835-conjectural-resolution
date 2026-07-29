# IDEAS — unproved ideas and dead ends, labelled honestly

Date: 2026-07-28.  Author: Claude Opus 5.

Everything here is **unproved**, **refuted**, or **blocked**, and is labelled
as such.  Proved material is in `PROOF.md`.  No script was run and no
literature search was performed this session (both were permission-gated), so
nothing below rests on either.

---

## A.  Routes I tried and closed, with the exact failure point

### A.1  Mod-\(p\) linear algebra on the colouring — **closed, gives one condition only**

*Status: proved, but non-obstructive.*

Identify the \(k+1=p\) colours with \(\mathbb F_p\).  Rainbowness of every
\((k+1)\)-set gives, for each \((k+1)\)-set \(S\) and each \(1\le j\le p-2\),
\(\sum_{s\in S}c(S\setminus s)^j=0\), and \(=-1\) at \(j=p-1\).  The \(j=1\)
condition says \(U_kc=0\) where \(U_k\) is the \(k\to k+1\) inclusion matrix.

By Wilson's theorem on \(p\)-ranks of inclusion matrices (applied after the
complementation identity \(\operatorname{rank}W_{k,k+1}(2k)
=\operatorname{rank}W_{k-1,k}(2k)\), since \(W_{k,k+1}\) itself violates the
hypothesis \(k\le v-t\)),
\(\operatorname{rank}_pW_{k,k+1}(2k)=\binom{2k}{k-1}\), so
\(\dim\ker_p U_k=\binom{2k}k-\binom{2k}{k-1}=C_k\), the Catalan number.  The
same count holds for the down map \(D_k\), and \(\ker_pU_k=\ker_pD_k\) because
both are the mod-\(p\) reduction of the same saturated integral lattice
\(\ker_{\mathbb Z}U_k=\ker_{\mathbb Z}D_k=V_k\cap\mathbb Z^\Omega\).

**Failure point.**  The condition is exactly "\(c\) lies in the top Specht
module \(S^{(k,k)}\) mod \(p\)" — one linear condition of corank
\(\binom{2k}{k-1}\), and the up- and down-versions coincide, so the top rung
gets no extra linear information from its self-complementarity.  Nothing
further was extracted.  This overlaps the kernel criterion already recorded at
`../../../erdos_835_conjectural_resolution.md:425-433`.

### A.2  Chevalley–Warning on the full polynomial system — **refuted, by a wide margin**

*Status: refuted.*

The rainbow conditions are equivalent to the power-sum system
\(p_1=\dots=p_{p-2}=0,\ p_{p-1}=-1\) over every \((k+1)\)-set (and this really
is equivalent: in characteristic \(p\), Newton's identities are invertible for
\(m\le p-1\), and \(p_1..p_{p-1}\) matching those of \(T^p-T\) forces
\(\prod(T-c_i)=T^p-T-e_p\), which has no \(\mathbb F_p\)-roots unless
\(e_p=0\)).  Chevalley–Warning needs \(\sum\deg<\#\text{variables}\); here the
degree sum is \(\binom{2k}{k-1}\cdot\frac{p(p-1)}2\) against
\(\binom{2k}{k}\) variables.  Off by a factor of order \(p^2\).  Dead.

### A.3  Sign / parity of the star bijections — **blocked, not refuted**

*Status: unproved and unverifiable this session.*

Each up-star \(\alpha_A\) (\(A\) a \((k-1)\)-set) and each down-star
\(\beta_P\) (\(P\) a \((k+1)\)-set) is a bijection onto \(\mathbb F_p\), so has
a sign against fixed reference orders.  Taking the product of the Vandermonde
identity \(\prod_{\{s,s'\}}(c(S\setminus s)-c(S\setminus s'))=\varepsilon\cdot V\)
over all \((k+1)\)-sets and separately over all \((k-1)\)-sets gives the *same*
product over all Johnson edges, hence
\(\prod_S\varepsilon(\beta_S)=\pm\prod_A\varepsilon(\alpha_A)\) with an
explicit constant.

**Failure point.**  Both sides are unknown; the relation is one equation in two
unknowns.  Pushing it further needs the row-sign invariant \(\mathrm{rsgn}\) of
a symmetric Latin square of even order with constant diagonal (equivalently of
a \(1\)-factorization of \(K_{2n}\)) to be a **constant** depending only on
\(n\).  I verified \(\mathrm{rsgn}\) is a genuine isomorphism invariant for
even order (relabelling factors or vertices multiplies it by
\(\mathrm{sgn}(\cdot)^{2n}=+1\)), and computed it to be \(+1\) for \(K_4\) by
hand, but **I could not test \(K_8\)** (6 isomorphism classes) without an
interpreter, and I do not reliably know the relevant Latin-square parity
theorem.  Not pursued further.  Note the repository already reports a star-sign
layer and a proof that it cannot decide the problem
(`../../opus5_v2/PROOF.md` §4), and separately a star-sign proof of
\(LS(2,3,7)\) nonexistence
(`../unrestricted_ls3420_attack_2/NOTE.md:136-146`), so this ground is partly
covered.

### A.4  Catalan parity via regular bipartite graphs — **refuted (the test is vacuous)**

*Status: refuted; recorded as Corollary 5.3 of `PROOF.md`.*

A \(d\)-regular bipartite graph has parts of equal size, hence even order.
Theorem 5 part 2 turns "the last two classes" into bipartiteness of a
\((t+1)\)-regular graph on \(2N\) vertices — even, so no obstruction.  Folding
by complementation at the top rung gives a \(k\)-regular graph on \(C_k\)
vertices (the \(|A\cap A'|=1\) neighbours are the complements of the
\(|A\cap A'|=k-1\) neighbours, so they collapse onto the same quotient
vertices — I first wrote \(2k\)-regular here and corrected it in `PROOF.md`
Corollary 5.3).  \(C_k\) is odd iff \(k=2^m-1\); since \(k=p-1\) is even for
every odd prime \(p\), \(C_k\) is always even.  **The parity test never
fires.**

### A.5  Erdős–Ko–Rado at rung \(p-3\) — **refuted (slack too large)**

*Status: refuted.*

`PROOF.md` Corollary 4 proves every class at rung \(p-3\) is an intersecting
family of \((p-2)\)-sets in a \((2p-3)\)-set, and \(n=2m+1\) there, so EKR
applies with bound \(\binom{2p-4}{p-3}\).  But
\(|\mathcal D|=\binom{2p-4}{p-3}\cdot\frac{2p-3}{p(p-2)}\), and
\(\frac{2p-3}{p(p-2)}<1\) for all \(p\ge5\).  The design is far below the EKR
bound; no contradiction.

### A.6  Additive / low-degree constructions — **refuted (short proof, recorded for completeness)**

*Status: refuted; this reproduces a route the repository already closed.*

Any colouring of the form \(c(B)=\phi(\text{symmetric function of }(w_x)_{x\in B})\)
fails: for a \((k+1)\)-set \(S\), the \(k+1\) colours are determined by the
multiset \(\{w_s\}\), so two points with equal weight in a common
\((k+1)\)-set collide.  With \(|X|=2k>k+1\) weights in \(\mathbb F_p\), such a
pair always exists.  The same argument kills \(c(B)=\phi(\sum_{x\in B}x)\) with
\(X\subseteq\mathbb F_{2^m}\): the condition becomes "\(\phi\) is a bijection on
every zero-sum \(p\)-subset", and any \(\phi:\mathbb F_{32}\to\mathbb Z_{17}\)
has a repeated value.

---

## B.  Unproved ideas that survived the session

### B.1  Odd-cycle invariant for the leftover conflict graph — **live only at a growing rung**

*Status: unproved; this is the concrete next attack.*

`PROOF.md` Theorem 5 gives an exact equivalence: \(LS(t,t+1,v)\) exists iff
some family of \(q-2\) pairwise disjoint systems has **bipartite** leftover
conflict graph \(G_{\mathcal E}\).  \(G_{\mathcal E}\) is \((t+1)\)-regular with
\(\binom vt\) edges, and at the top rung it is triangle-free (each
\((t+2)\)-set contributes exactly one edge).

The question is whether the cycle space of \(G_{\mathcal E}\) carries an
\(\mathbb F_2\)-invariant forced by the parameters.  Corollary 5.3 kills the
order-parity version.  A later literature correction (`FIXED_RUNG_EXISTENCE.md`)
also kills any proposed uniform obstruction at a **fixed** rung: for every
fixed \(t\), Keevash's large-set theorem gives \(LS(t,t+1,t+p)\) for every
sufficiently large prime \(p\).  Thus a finer invariant can resolve #835
negatively only if it applies at a rung \(t=t(p)\to\infty\), or directly at
the top rung.  Whether such a growing-rung cohomology or forced odd walk
exists remains unknown.

### B.2  The half-size folded reformulation — **proved but of unclear value**

*Status: the statement is proved (it follows from `PROOF.md` Corollary 4); its
usefulness is unproved.*

Because every class is complement-closed at the top rung, \(c\) descends to
complementary pairs.  Coordinatising by deleting one point \(a\) and setting
\(Y=X\setminus\{a\}\), \(|Y|=2k-1\), each complementary pair has exactly one
member avoiding \(a\), so \(\binom Yk\) is a transversal of the pairs and
\(\bigl|\binom Yk\bigr|=\tfrac12\binom{2k}k\).  One gets:

> \(\chi(J(2k,k))=k+1\) **iff** there is \(r:\binom Yk\to\mathbb F_{k+1}\) such
> that for every \((k-1)\)-set \(A\subseteq Y\),
> \(\{r(A\cup y):y\in Y\setminus A\}=\mathbb F_{k+1}\setminus\{r(Y\setminus A)\}\).

Equivalently: in any proper \((k+1)\)-colouring of \(J(2k-1,k)\), the colour
missing at a \((k-1)\)-set \(A\) is forced to be the colour of the
complementary \(k\)-set \(Y\setminus A\).  This is an exact halving of the
variable count and it composes with Theorem G1 of
`../generic_radius4_certificate_attack/`, which already gives
\(\chi(J(2k-1,k))\le k+1\iff LS(k-1,k,2k)\).  **What is added** is the explicit
missing-colour rule; **what is not shown** is that it helps any search or
proof.  Not pursued.

### B.3  \(\tau(p)\) as the right invariant — **absolute-bound conjecture refuted**

Define \(\tau(p)=\max\{t:LS(t,t+1,t+p)\ \text{exists}\}\).  Then #835 asks
whether \(\tau(p)=p-2\) ever.  The small-prime values and bounds in `STATUS.md`
remain correct.  However, the proposed absolute upper bound is false:
`FIXED_RUNG_EXISTENCE.md` proves from Keevash's Theorem 1.2 that, for every
fixed \(T\), \(\tau(p)\ge T\) for all sufficiently large primes.  Hence
\(\tau(p)\to\infty\).  The meaningful asymptotic question is how fast it can
grow relative to \(p\), not whether it is bounded.

### B.4  Group-invariant search targets — **not attempted (no interpreter)**

For \(k=16\) the natural invariant ansätze are \(\mathbb Z_{31}\) acting on the
folded formulation of B.2 (\(\binom{31}{16}=300{,}540{,}195=31\cdot9{,}694{,}845\)
orbits, all free since \(31\) is prime, and \(9{,}694{,}845=17\cdot570{,}285\),
so a \(\mathbb Z_{31}\)-invariant colouring would assign \(570{,}285\) orbits to
each colour), and \(\mathbb Z_{19}\cup\{\infty\}\) at rung \(3\)
(\(\binom{20}4=4845=19\cdot255\) orbits, \(255=17\cdot15\)).  Both arithmetics
are consistent, i.e. neither ansatz is excluded by a counting argument.  The
repository already has search scripts for the rung-3 version
(`search_ls_3_4_20*.py`, `search_cyclic_ls_4_5_21.py`).  **Not attempted here:
no interpreter.**

---

## C.  Things I checked and found already in the repository

Recorded so that a later session does not re-derive them a third time.

* The forced intersection distribution of \(S(k-1,k,2k)\) —
  `../../opus5_v2/PROOF.md:98-140` (Theorem 1.3).  I re-derived it
  independently via the Johnson scheme before finding it; that second proof is
  kept in `PROOF.md` §2.3 as cross-validation.
* Complement-closure of every \(S(k-1,k,2k)\) — `ibid.:196-213` (Theorem 2.1).
  I re-derived it as the \(i=K\) case of the distribution; same conclusion.
* The cross-class distribution and "first-order counting cannot beat the clique
  bound" — `ibid.:271-315` (Theorems 3.1, 3.2), top rung only.
* The star-bijection reformulation of a large set —
  `../unrestricted_ls3420_attack_2/NOTE.md:36-50`.
* The derivation tower and the class count \(v-t\) —
  `../../../erdos_835_conjectural_resolution.md:96-101`,
  `../../tower_automorphism_lemmas.md:9-13`.
* Divisibility \(\Rightarrow k+1\) prime, with the smallest-prime-factor
  argument — `../../../erdos_835_conjectural_resolution.md:56-89`.
* The gap lemma \(D\ne q-1\) —
  `../../../evidence/large_set_literature_2026-07-26.md:8-19`.

A note on one thing I derived and then found to be a repository result stated
differently: \(LS(3,4,8)\) fails because it derives to \(LS(2,3,7)\).  The
repository proves \(LS(3,4,8)\) nonexistence directly by exhausting the \(30\)
labelled \(S(3,4,8)\) (`verify_k4.py`, cited at
`../../../evidence/sqs8_klein_family_parity.md:8-10`); the derivation argument
is a one-line alternative and is not new.
