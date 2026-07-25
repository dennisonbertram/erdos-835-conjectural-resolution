# Attack 2: perfect-code holonomy, determinant factorization, and the parity split

Date 2026-07-24.  Verifier: `collaboration/verify_fable_parity_attack_2.py`
(stdlib only, deterministic seed 20260724, full battery ~14 s; it loads the
Algorithm-X routines from `evidence/disjoint_mates.py`).  Labels: **Proved**
(complete proof below), **Verified** (finite exact computation, exhaustive
unless marked sampled), **Refuted** (explicit certificate), **Open**.

Setting as in `evidence/fable_trade_quadratic.md` and
`evidence/fixed_base_parity_judgment.md`: \(r\) odd, \(v=2r+1\),
systems are \(S(r-1,r,v)\), \(b=\binom vr/(r+2)\), \(K\) is the disjointness
(Kneser/odd-graph \(O_{r+1}\)) adjacency matrix on all \(r\)-sets,
\(F_{XY}:X\to Y\) fixes shared blocks and otherwise sends a block to its
unique disjoint \(Y\)-block, and for \(A\) block-disjoint from \(B,C\) the
triangle permutation is \(\sigma=F_{CB}F_{AC}F_{BA}\) on \(B\).  Target:
Conjecture P (\(|B\cap C|\equiv b\pmod 2\) for \(B,C\in\mathcal D(A)\)),
decisive at \(r=15\).

## 0. Verdict

**Conjecture P remains OPEN.**  The task's specific hope "prove
\(\operatorname{sgn}(\sigma)=+1\)" is **false as stated and, by itself,
insufficient for P**: \(\operatorname{sgn}(\sigma)=-1\) on all 28 canonical
\(r=3\) triangles and \(+1\) on all 10 296 canonical \(r=5\) triangles,
while P holds in both families; and Theorem 4.1 below proves the sign sees
only the number of *even* \(\sigma\)-cycles, whereas P is the parity of the
number of *odd* cycles.  What this note contributes:

| # | Result | Status |
|---|--------|--------|
| 2.1 | \(F_{XY}\) is a bijection for **arbitrary** pairs of systems (perfect-code groupoid, valid in any graph); \(F_{YX}=F_{XY}^{-1}\); matrix = \([X,Y]\)-submatrix of \(K+I\) | Proved |
| 3.1 | \(\operatorname{sgn}(\sigma_B)=f(A,B)f(A,C)f(B,C)\) with \(f(Y,Z)=\det(K+I)[Y,Z]\): determinant signs factor into pair terms | Proved |
| 3.2 | Cycle type of the triangle holonomy is an invariant of the unordered triple \(\{A,B,C\}\) | Proved |
| 4.1 | Parity split: \(\operatorname{sgn}(\sigma)=(-1)^{e}\) (\(e\) = # even cycles); P \(\iff o\equiv0\) (\(o\) = # odd cycles); sign alone does not determine P | Proved (no-go for sign alone) |
| 4.2 | Any label-product sign formula collapses to cycle-length parities (position identity) | Proved (no-go) |
| 5 | \(r=3\): \(\operatorname{sgn}(\sigma_B)=(-1)^{|A\cap B|+|A\cap C|+|B\cap C|}\) on all 4060 triples; **fails at \(r=5\)** (sign not a function of intersection type) | Verified / Refuted |
| 6.R | Even-cycle law for **general** triples is false: \(r=3\) type \((0,1,3)\) gives an odd 3-cycle (1680 instances) | Refuted |
| 6.1–6.3 | New chain laws: \(T_i\cap T_{i+1}=\{\alpha_{i+1}\}\), \(\alpha_{i+1}\in T_i\); each \(\sigma\)-cycle is an **induced** \(3\ell\)-cycle of \(O_{r+1}\); integer position identity \(2s_p=\ell-a_p-d_p+c_p\) | Proved |
| 6.R2 | Five corner-bit local invariants fail at \(r=5\); individual cycles are **never** trades at \(r=5\) (0/1828) | Refuted |
| 7.1 | P \(\iff\) the elementary divisor 2 of \(N=(KP_AK+K)[B\setminus C,\,C\setminus B]\) has even multiplicity (exact SNF \(\mathrm{diag}(1^{t-c},2^{o},0^{e})\)) | Proved reformulation; Open evaluation |
| 8.1 | Intersection distribution \(n_j(B,C)\) is affine in \(|B\cap C|\); Bose–Mesner moment identities alone merely repackage the free intersection parameter | Proved (no-go for moment-only routes) |
| 9 | Pair-parity phenomenon: at \(r=3,5\) every non-disjoint pair of systems has \(|Y\cap Z|\equiv b\pmod2\) | Verified; Open |

## 1. Notation

Blocks are \(r\)-subsets of \(X\), \(|X|=v=2r+1\).  For a system \(D\) and
an \(r\)-set \(k\), \(n_0(k)=1-[k\in D]\) counts disjoint \(D\)-blocks
(`three_way_trade.md` (2.2)/(2.3)).  Equivalently, in the odd graph
\(O_{r+1}\) (vertices all \(r\)-sets, adjacency = disjointness) every vertex
has exactly one closed-neighbour in \(D\):

\[(K+I)\,x_D=\mathbf 1\quad\text{over }\mathbb Z. \tag{1.1}\]

That is, every \(S(r-1,r,2r+1)\) is a **perfect 1-code** of \(O_{r+1}\)
(the classical Biggs correspondence; only the direction "Steiner
\(\Rightarrow\) perfect code" is used, and it is exactly \(n_0=1-[k\in D]\)).

## 2. The perfect-code groupoid

**Lemma 2.1 (Proved).**  Let \(G\) be any finite simple graph and let
\(Y,Z\) be perfect 1-codes of \(G\) (every vertex has exactly one closed
neighbour in the code).  Define \(F_{YZ}:Y\to Z\) by \(F_{YZ}(y)=\) the
unique element of \(N[y]\cap Z\).  Then:

1. \(F_{YZ}\) is a bijection (in particular all perfect codes of \(G\) are
   equinumerous);
2. \(F_{ZY}=F_{YZ}^{-1}\), and \(F_{YY}=\mathrm{id}\);
3. the \([Y,Z]\)-submatrix of \(A_G+I\) (rows \(Y\), columns \(Z\)) is the
   permutation matrix of \(F_{YZ}\).

*Proof.*  Well-definedness is the perfect-code property of \(Z\) at the
vertex \(y\).  Injectivity: if \(F_{YZ}(y)=F_{YZ}(y')=z\) then
\(y,y'\in N[z]\cap Y\), which is a single element by the perfect-code
property of \(Y\) at \(z\); so \(y=y'\).  An injection each way gives
\(|Y|=|Z|\) and bijectivity.  (2): \(z\in N[y]\iff y\in N[z]\), so
\(z=F_{YZ}(y)\iff y=F_{ZY}(z)\).  (3): row \(y\) restricted to \(Z\) has
support \(N[y]\cap Z=\{F_{YZ}(y)\}\). \(\square\)

Specialized to \(G=O_{r+1}\) via (1.1), \(F_{YZ}\) is exactly the task's
map (fix shared blocks, else unique disjoint \(Z\)-block), **now defined
and bijective for every pair of systems**, with no disjointness hypothesis.
Machine check: all \(30\times30\) ordered Fano pairs and 300 random ordered
\(r=5\) pairs (bijection + inverse property).

**Audit remark (scope).**  Lemma 2.1 holds for perfect codes in an
arbitrary graph.  Consequently *no* consequence of the groupoid structure
alone can encode the Steiner-specific parity P; whatever proves P must use
more than (1.1).  This is borne out by §6.R below: the even-cycle
phenomenon does not survive on general triples, where the groupoid exists
just as well.

## 3. Sign factorization and conjugacy

Fix once and for all a linear order on all \(r\)-sets.  For a bijection
\(h:P\to Q\) between equinumerous sets of blocks let
\(\operatorname{sgn}(h)\) be the sign of its permutation matrix with rows
and columns sorted by that order; then
\(\operatorname{sgn}(g\circ h)=\operatorname{sgn}(g)\operatorname{sgn}(h)\)
and \(\operatorname{sgn}(h^{-1})=\operatorname{sgn}(h)\) (transpose).
Define

\[f(Y,Z):=\operatorname{sgn}(F_{YZ})=\det\bigl[(K+I)[Y,Z]\bigr]\in\{\pm1\},\]

the determinant taken with sorted row/column order.  By Lemma 2.1,
\(f\) is defined for **all** pairs, symmetric, with \(f(Y,Y)=+1\).

**Lemma 3.1 (Proved).**  For any three systems, the base-\(B\) triangle
holonomy \(\sigma_B=F_{CB}F_{AC}F_{BA}\in\operatorname{Sym}(B)\) satisfies

\[\operatorname{sgn}(\sigma_B)=f(A,B)\,f(A,C)\,f(B,C). \tag{3.1}\]

Changing the global block order multiplies \(f(Y,Z)\) by
\(\varepsilon(Y)\varepsilon(Z)\) (reordering signs), so each factor is
gauge-dependent but every closed product such as (3.1) is canonical.

*Proof.*  Multiplicativity of \(\operatorname{sgn}\) plus symmetry of
\(f\).  Gauge: reordering \(Y\) composes the sorted permutation matrix with
a fixed reindexing on the \(Y\)-side wherever \(Y\) appears; in a closed
product each system appears once as domain and once as codomain, so the
reindexing signs cancel. \(\square\)

**Lemma 3.2 (Proved).**  \(F_{BA}\sigma_BF_{AB}=F_{BA}F_{CB}F_{AC}\), the
same-orientation holonomy based at \(A\); reversing orientation gives
\(\sigma_B^{-1}\).  Hence the multiset of cycle lengths of the triangle
holonomy is an invariant of the unordered triple \(\{A,B,C\}\).
(Machine check: 60 random \(r=3\) triples, 15 random \(r=5\) triples.)

**Lemma 3.3 (Proved).**  If \(A\cap B=A\cap C=\emptyset\), then
\(\sigma_B\) fixes \(B\cap C\) pointwise and on \(B\setminus C\) coincides
with the canonical \(\sigma=\varphi_2^{-1}\varphi_1\) of
`fable_trade_quadratic.md` Lemma 6; its fixed points are exactly
\(B\cap C\) (fixed-point-freeness on \(B\setminus C\) is Lemma 6.4 there).

*Proof.*  For \(S\in B\cap C\): \(S\notin A\), so \(F_{BA}(S)=\nu(S)=:D\);
\(D\notin C\), and \(S\in C\) is disjoint from \(D\), so \(F_{AC}(D)=S\);
\(S\in C\cap B\), so \(F_{CB}(S)=S\).  For \(S\in B\setminus C\):
\(F_{AC}(\nu(S))=\mu_{AC}(\nu(S))=\varphi_1(S)\), which lies in
\(C\setminus B\) (otherwise \(\varphi_1(S)\) and \(S\) are distinct
\(B\)-blocks on the facet \(S\setminus\{\beta\}\)); and for
\(T\in C\setminus B\), \(F_{CB}(T)\) is the unique \(B\)-block disjoint
from \(T\), which is precisely \(\varphi_2^{-1}(T)\). \(\square\)

Machine check: identity of \(\sigma_B\) with the Lemma-6 construction and
of its fixed-point set with \(B\cap C\) on all 28 canonical \(r=3\) pairs
and 30 canonical \(r=5\) pairs; identity (3.1) on **all 4060** \(r=3\)
triples and 400 random \(r=5\) triples.

## 4. The parity split: what sign can and cannot see

Work in the canonical case; \(t=b-|B\cap C|\), and let \(o,e,c=o+e\) be the
numbers of odd, even, and all cycles of \(\sigma\) on \(B\setminus C\).

**Theorem 4.1 (Proved; decisive no-go for sign alone).**

1. \(t\equiv o\pmod 2\); hence **P \(\iff o\equiv0\pmod2\)**.
2. \(\operatorname{sgn}(\sigma)=(-1)^{e}\).
3. Therefore the determinant-sign theory of §3 — and any identity
   involving only \(\operatorname{sgn}(\sigma)\) or products of the
   pair-invariant \(f\) — determines only \(e\bmod2\), not the
   \(o\bmod2\) required by P.  It could contribute only if supplemented by
   an independent geometric relation coupling \(e\) and \(o\).
4. Instances: at \(r=3\), \(\operatorname{sgn}(\sigma)=-1\) (cycle type
   \((6)\), all 28 canonical pairs); at \(r=5\),
   \(\operatorname{sgn}(\sigma)=+1\) (all 10 296 canonical pairs).  P holds
   in both families.  So no fixed sign value can signal P, and the task's
   proposal "prove \(\operatorname{sgn}(\sigma)=+1\)" is refuted at
   \(r=3\) and, even where true, toothless.

*Proof.*  (1) \(t=\sum_j\ell_j\equiv\#\{j:\ell_j\text{ odd}\}\).
(2) \(\operatorname{sgn}=\prod_j(-1)^{\ell_j-1}\); odd cycles contribute
\(+1\), even cycles \(-1\).  Thus sign alone supplies \(e\bmod2\), while
P asks for \(o\bmod2\).  The examples in (4) also show that P can hold
with either sign. \(\square\)

**Theorem 4.2 (Proved; edge-label formulas collapse).**  The \(3\ell\)
step labels \(\alpha_i,\beta_i,\delta_i\) are exactly the missing-point
labels of the \(3\ell\) edges of the lifted walk in \(O_{r+1}\), and by
the position identity (`fable_trade_quadratic.md` tautology screen) their
combined multiset equals \(\ell\cdot X\) modulo 2.  Hence for any fixed
point-sign function \(s:X\to\{\pm1\}\) applied uniformly to the walk
edges — the form every connection/holonomy determinant takes, cf.
`odd_matching_cells.md` (7)–(8) — the per-cycle product is
\(\prod_{\text{edges}}s(x_{\text{edge}})=\bigl(\prod_{p}s(p)\bigr)^{\ell}\),
a function of \(\ell\bmod2\) alone; postulating its value is *equivalent*
to postulating cycle-length parities.  The signed/oriented
(wedge-decorated) refinements of \(f\) therefore add nothing: this
re-derives, inside the three-system setting, the emptiness of the
determinant-holonomy route proved for the full colouring in
`odd_matching_cells.md` §3 (eq. (9)).  (Scope: formulas applying
*different* sign functions to the \(\alpha\)-, \(\beta\)-, \(\delta\)-
tracks are not covered by this collapse; none is currently proposed.)
\(\square\)

**The surviving sign statement (Verified, Open).**  Define the **SignLaw**
(SL): for canonical triangles,
\[f(A,B)f(A,C)f(B,C)=(-1)^{b}\qquad\bigl(\iff e\equiv b\pmod 2\bigr).\]
SL holds in all \(28+10\,296\) canonical instances
(\(-1=(-1)^7\) at \(r=3\); \(+1=(-1)^{66}\) at \(r=5\)).  Two caveats,
audited: (i) on P-conforming data SL is indistinguishable from the variant
\(\operatorname{sgn}(\sigma)=(-1)^{|B\cap C|}\) (same trap as Q1/Q2 in
`fixed_base_parity_judgment.md` §7 — the discriminating instances are
exactly the P-violating ones); (ii) by Theorem 4.1, SL even if proved does
not touch P.  SL's interest is that it is determinant-representable and
orthogonal to P: together with the even-cycle identity it would pin
\((o,e)\bmod 2=(0,b)\).  The relation of SL to the \(E\)-constancy
observable of `fixed_base_parity_judgment.md` §7 (a per-sphere slot theory,
also a "sign layer" statement) is not established here.

## 5. Global structure of f: an exact r=3 law that dies at r=5

**Verified (exhaustive), \(r=3\).**  Over all 4060 triples of distinct
Fanos, \(\operatorname{sgn}(\sigma_B)\) is a function of the intersection
type, and the exact law

\[\operatorname{sgn}(\sigma_B)=(-1)^{\,|A\cap B|+|A\cap C|+|B\cap C|}\]

holds in all 4060 cases (sign by sorted type: \((0,0,1)\mapsto-1\),
\((0,1,3)\mapsto+1\), \((1,1,1)\mapsto-1\), \((1,3,3)\mapsto-1\)).
Equivalently \(f=\varepsilon\otimes\varepsilon\cdot g(|Y\cap Z|)\) with
\(g(j)=(-1)^j\).  (The finite solve also admits the second branch
\((g(0),g(1),g(3))=(-1,-1,1)\); the ambiguity exists because every realized
\(r=3\) type contains an even number of sides with \(|{\cdot}\cap{\cdot}|\in\{0,3\}\).)

**Refuted at \(r=5\).**  On a 250-system sample (the base, its 144 mates,
and random systems from the full labelled family of 5040), the triangle
sign is **not a function of the intersection type**: types
\((0,6,12),(6,6,12),(6,12,12),(6,12,18),(6,12,30)\) each realize both
signs; types \((0,12,12),(12,12,12),(12,12,30),(12,18,18),(12,30,30)\)
realized only \(-1\); the canonical types \((0,0,6),(0,0,18)\) only \(+1\).
In particular \(f\) is not a coboundary at \(r=5\) and no universal
intersection-size sign law exists.  The elegant \(r=3\) law is a
small-parameter coincidence — a caution for every other \(r\equiv3\pmod4\)
dichotomy resting on \(r=3\) alone (cf. the same warning for Conjecture E
in `fixed_base_parity_judgment.md` §5).

## 6. General triples, chain-law completion, and the local no-gos

**6.R (Refuted): the even-cycle law does not extend beyond the canonical
case.**  \(r=3\), exhaustive census of holonomy cycle types over all 4060
triples (sorted intersection type: nontrivial cycle type × count):

| type | cycle type | count |
|------|-----------|-------|
| (0,0,1) | (6) | 840 |
| (0,1,3) | **(3)** | 1680 |
| (1,1,1) | (2,2,2) | 70 |
| (1,1,1) | (4) | 840 |
| (1,3,3) | (2) | 630 |

Every triple with type \((0,1,3)\) has an **odd** 3-cycle.  At \(r=5\)
(400 random sample triples), odd nontrivial cycles occur in most
non-canonical types, e.g. 6 of 8 triples of type \((0,6,6)\), 22 of 62 of
type \((6,6,6)\), 55 of 82 of type \((6,6,18)\); the canonical family
(all 10 296 pairs, exhaustive) has none.  Consequences: (i) **both**
disjointness hypotheses are essential to the even-cycle identity; (ii) any
proof strategy that deforms \((A,B,C)\) through non-disjoint triples while
tracking a cycle-parity invariant is impossible; (iii) the census also
shows the cycle type is not determined by intersection numbers
(type \((1,1,1)\) realizes both \((2,2,2)\) and \((4)\)).

For the remainder of §6 fix a canonical triangle and a \(\sigma\)-cycle
\(S_0\to S_1\to\cdots\) with step data as in `fable_trade_quadratic.md`
Lemma 7: \(D_i=\nu(S_i)=S_i^c\setminus\{\alpha_i\}\),
\(T_i=\varphi_1(S_i)=(S_i\setminus\{\beta_i\})\cup\{\alpha_i\}\),
\(S_{i+1}=(D_i\setminus\{\delta_i\})\cup\{\beta_i\}\).

**Lemma 6.1 (Proved; completes the chain laws).**
\(\alpha_{i+1}\in T_i\), and \(T_i\cap T_{i+1}=\{\alpha_{i+1}\}\) exactly.
Together with \(S_i\cap S_{i+1}=\{\beta_i\}\) (Lemma 7 loc. cit.) and
\(D_i\cap D_{i+1}=\{\delta_i\}\) (Lemma 8 loc. cit.), all three system
tracks are closed 1-intersection chains, with the shared point of each
consecutive \(T\)-pair being the **next** \(\alpha\).

*Proof.*  \(\alpha_{i+1}\in S_{i+1}^c=(S_i\setminus\{\beta_i\})
\cup\{\alpha_i,\delta_i\}\), and \(\alpha_{i+1}\ne\delta_i\) (Lemma 8
loc. cit.), so \(\alpha_{i+1}\in(S_i\setminus\{\beta_i\})\cup\{\alpha_i\}
=T_i\).  Next, \(T_i\) is disjoint from \(S_{i+1}\) (it is the
\(\varphi_2\)-partner of \(S_{i+1}\)), and
\(T_{i+1}=(S_{i+1}\setminus\{\beta_{i+1}\})\cup\{\alpha_{i+1}\}\); hence
\(T_i\cap T_{i+1}=T_i\cap\{\alpha_{i+1}\}=\{\alpha_{i+1}\}\). \(\square\)

**Lemma 6.2 (Proved; induced-cycle law).**  The closed walk
\(S_0\,D_0\,T_0\,S_1\,D_1\,T_1\cdots\) of length \(3\ell\) (Lemma 7
loc. cit.) is an **induced** cycle of \(O_{r+1}\): its \(3\ell\) vertices
are pairwise distinct and the only disjoint pairs among them are the
walk-consecutive ones.

*Proof.*  Distinctness: the \(S_i\) are distinct (\(\sigma\)-orbit), the
\(T_i=\varphi_1(S_i)\) and \(D_i=\nu(S_i)\) are images of injections, and
cross-type coincidences are impossible (\(A,B,C\) memberships:
\(S_i\in B\setminus C\), \(T_i\in C\setminus B\), \(D_i\in A\) with
\(A\cap B=A\cap C=\emptyset\)).  Non-adjacency: two blocks of one system
are never disjoint (\(n_0=0\) on blocks); across systems, uniqueness of
disjoint partners gives: \(S_i\perp D_j\iff D_j=\nu(S_i)=D_i\);
\(T_i\perp D_j\iff D_j=\nu(T_i)=D_i\); \(S_i\perp T_j\iff
T_j=\varphi_2(S_i)=T_{i-1}\).  Exactly the walk edges. \(\square\)

**Lemma 6.3 (Proved; integer position identity).**  Over \(\mathbb Z^X\),
\(x_{S_{i+1}}=\mathbf 1-x_{S_i}-e_{\alpha_i}-e_{\delta_i}+e_{\beta_i}\).
Telescoping around the cycle: for every point \(p\),

\[2\,s_p=\ell-a_p-d_p+c_p,\qquad t_p=\ell-s_p-d_p, \tag{6.1}\]

where \(s_p,t_p\) count the \(S_i\)- resp. \(T_i\)-blocks containing \(p\)
and \(a_p,c_p,d_p\) count occurrences of \(p\) as \(\alpha,\beta,\delta\)
label.  Modulo 2 this recovers the known \(\mathbb F_2\) position identity;
over \(\mathbb Z\) it adds the box constraints \(0\le s_p,t_p\le\ell\),
i.e. \(|a_p+d_p-c_p|\le\ell\) and \(s_p+d_p\le\ell\), for every point
simultaneously.

*Proof.*  \(X=S_i\sqcup D_i\sqcup\{\alpha_i\}\) gives
\(x_{D_i}=\mathbf 1-x_{S_i}-e_{\alpha_i}\), and
\(S_{i+1}=(D_i\setminus\{\delta_i\})\cup\{\beta_i\}\) with
\(\delta_i\in D_i\), \(\beta_i\notin D_i\).  Summing over a closed cycle
kills the \(x_S\)-telescope; the \(T\)-identity follows from
\(x_{T_i}=x_{S_i}-e_{\beta_i}+e_{\alpha_i}\). \(\square\)

Machine checks for 6.1–6.3: all 28 \(r=3\) cycles and 1222 \(r=5\) cycles
(200 random mate pairs), including the full pairwise non-adjacency scan of
Lemma 6.2 on every cycle.

**6.R2 (Refuted): radius-1 local invariants and cycle-trades.**

* Corner bits.  For the five natural step-comparison bits
  \([\beta_{i+1}{=}\beta_i]\), \([\alpha_{i+1}{=}\alpha_i]\),
  \([\delta_{i+1}{=}\delta_i]\), \([\delta_{i+1}{=}\alpha_i]\),
  \([\delta_{i+1}{\in}S_i]\), the cycle-sums have non-constant parity at
  \(r=5\): among 1222 cycles the counts of odd cycle-sums are 444, 426,
  445, 89, 356 respectively (at \(r=3\): 0, 0, 28, 28, 0 of 28 — a
  small-case artifact).  None extends the tautology screen to a usable
  invariant; no radius-1 corner statistic computes cycle-length parity.
* Cycle-trades.  A single \(\sigma\)-cycle is a trade iff its \(S\)-side
  and \(T\)-side cover the same facets.  At \(r=5\) this fails for **every
  one** of the 1828 cycles arising from 300 mate pairs (all lengths
  2–44); at \(r=3\) the unique cycle per pair is the entire trade
  \(B\triangle C\), so the question is vacuous there.  Hence the naive
  version of task direction (3) — "an odd cycle would itself be a
  forbidden trade" — is closed: an odd-cycle contradiction must couple the
  cycle to the rest of \(B,C\) (or to \(A\)), not stand alone.

What survives of direction (3): an odd \(\sigma\)-cycle of length \(\ell\)
is now known to be an induced \(3\ell\)-cycle of \(O_{r+1}\), 3-periodically
coloured \((B,A,C)\), whose three tracks are 1-intersection chains
decorated by (6.1).  The only length constraint currently provable from
this local package is the odd-girth bound \(3\ell\ge2r+1\) (\(\ell\ge11\)
at \(r=15\)).  The falsifiable next step is a radius-2 UNSAT computation
(in the style of `evidence/odd_graph_local_ball/`) for \(\ell=11,13\) at
\(r=15\) against the full §6 constraint system.

## 7. The honest determinant target: Smith form of the matching sum

Let \(\Phi_1,\Phi_2\) be the 0-1 matrices (rows \(B\setminus C\), columns
\(C\setminus B\)) of the matchings \(\varphi_1,\varphi_2\), and
\(N=\Phi_1+\Phi_2\).

**Theorem 7.1 (Proved).**

1. **Global formula.**  \(N=(K\,P_A\,K+K)[B\setminus C,\;C\setminus B]\),
   where \(P_A\) is the coordinate projector onto the \(A\)-blocks: for
   \(S\in B\setminus C\), \(T\in C\setminus B\),
   \(\sum_{D\in A}[S\perp D][D\perp T]=[T=\varphi_1(S)]\) (the inner sum
   collapses to \(D=\nu(S)\) by \(n_0=1\)) and \([S\perp T]=[T=\varphi_2(S)]\).
2. **Smith normal form.**  \(\operatorname{SNF}(N)=
   \operatorname{diag}(1^{\,t-c},\,2^{\,o},\,0^{\,e})\).
3. **Consequently P \(\iff\) the multiplicity \(o\) of the elementary
   divisor 2 is even \(\iff\)
   \(\operatorname{rank}_{\mathbb Q}N\equiv\operatorname{rank}_{\mathbb F_2}N\pmod2\).**
4. **Tautology audit.**  The unrestricted \([B,C]\)-version
   \((KP_AK+K+I)[B,C]\) has diagonal entries 2 on \(B\cap C\); its
   2-multiplicity is \(|B\cap C|+o\equiv b\pmod 2\) *universally* (any
   permutation of a \(b\)-set has \(\#\text{odd cycles}\equiv b\)).  All
   content of P sits on the trade restriction, where fixed-point-freeness
   holds (Lemma 3.3).

*Proof of (2).*  \(N\Phi_2^{\mathsf T}=\Phi_1\Phi_2^{\mathsf T}+I=P_\sigma+I\)
with \(P_\sigma\) the permutation matrix of \(\sigma\); permutation
matrices are unimodular, so
\(\operatorname{SNF}(N)=\operatorname{SNF}(P_\sigma+I)\), and after a
permutation conjugation \(P_\sigma+I\cong\bigoplus_j(C_{k_j}+I)\) over the
cycles.  For a \(k\)-cycle, \(\det(C_k+I)=\prod_{\zeta^k=1}(1+\zeta)
=1-(-1)^k\) is \(2\) for \(k\) odd and \(0\) for \(k\) even, while deleting
the last row and first column leaves a triangular matrix with unit diagonal,
so the gcd of \((k-1)\)-minors is 1.  Hence
\(\operatorname{SNF}(C_k+I)=(1^{k-1},2)\) for odd \(k\) and
\((1^{k-1},0)\) for even \(k\). \(\square\)

Machine checks: formula (1) entrywise and the rank consequences
\(\operatorname{rank}_{\mathbb Q}N=t-e\),
\(\operatorname{rank}_{\mathbb F_2}N=t-c\) on 2 \(r=3\) pairs
(\(t{=}6,c{=}e{=}1\), both ranks 5) and 3 \(r=5\) pairs
(\(t{=}48\) or 60, \(c{=}e{=}6\), ranks 42/54/54).

**Status.**  This is the exact, non-tautological content of task direction
(2) ("mod-4 determinant identities"): P is precisely a 2-adic elementary
divisor statement about a canonical restriction of the Johnson-scheme
matrix \(K(P_AK+I)\).  Open: any structural handle on
\(v_2\bigl(\prod\text{nonzero divisors}\bigr)\bmod 2\) for such
restrictions.  Note the audit in (4): every approach must break the
\(B\cap C\)-diagonal off first, exactly as the fixed-point-freeness lemma
does.

## 8. The Bose–Mesner moment-only no-go

For systems \(B,C\) let \(n_j(B,C)=\#\{(S,T)\in B\times C:|S\cap T|=j\}\).

**Theorem 8.1 (Proved).**  For all \(B,C\) and all \(0\le s\le r-1\),

\[\sum_{j=0}^{r}\binom js\,n_j(B,C)=b\binom rs\lambda_s,\qquad
\lambda_s=\frac{\binom{v-s}{r-1-s}}{r-s}. \tag{8.1}\]

The truncated Pascal system (8.1) has rank \(r\) with kernel spanned by
\(\bigl((-1)^j\binom rj\bigr)_j\); therefore

\[n_j(B,C)=u_j+(-1)^{r-j}\binom rj\,|B\cap C| \tag{8.2}\]

with constants \(u_j\) depending only on \((r,v)\).  Consequently, for
**every** matrix \(M=\sum_j m_jA_j\) in the Bose–Mesner algebra of the
Johnson scheme (\(m_j\in\mathbb Z\)),
\(x_B^{\mathsf T}Mx_C=\alpha_M+\beta_M|B\cap C|\) with universal integers
\(\alpha_M,\beta_M\).  Hence the design moment equations alone give no
parameter-only congruence for \(|B\cap C|\): every Bose–Mesner bilinear
quantity merely repackages that same free parameter.  An invariant
bilinear proof of P would therefore need an additional, genuinely
nonlinear reason why one such quantity has a fixed residue; the
Bose–Mesner identities themselves do not supply it.

*Proof.*  (8.1): \(\sum_{T\in C}\binom{|S\cap T|}s
=\sum_{\sigma\subseteq S,|\sigma|=s}\lambda_s=\binom rs\lambda_s\) for each
\(S\), since an \(S(r-1,r,v)\) is an \(s\)-design for \(s\le r-1\); sum
over \(S\in B\).  Kernel: \(\sum_j(-1)^j\binom rj\binom js
=\binom rs(-1)^s\sum_i(-1)^i\binom{r-s}i=0\) for \(s<r\); the system's
\(s,j\le r-1\) block is unitriangular, so the kernel is 1-dimensional.
Pinning the free parameter by \(n_r=|B\cap C|\) gives (8.2) with slope
\((-1)^j\binom rj/(-1)^r=(-1)^{r-j}\binom rj\). \(\square\)

Machine check: (8.1) and (8.2) on all 435 Fano pairs and 400 random
\(r=5\) pairs (slopes \((-1)^{r-j}\binom rj\) exact).

**Consequences.**  (8.2) subsumes at one stroke: \(n_0=b-|B\cap C|\)
(equivalently \(x_B^{\mathsf T}Kx_C=b-|B\cap C|\), the disagreement count
\(\delta\)); \(n_{r-1}=r\delta\) (tautology T3 of
`fixed_base_parity_judgment.md`); and tautology T2.  For task direction
(4): the quadratic intersection form on the exact-cover variety, paired
through **any** invariant bilinear form, reduces exactly to \(|B\cap C|\) —
the nonlinear content of P is not visible to the Bose–Mesner algebra and
lives (at present) precisely in the rank/SNF statement of §7 and in
non-invariant objects like \(f\).

## 9. Pair-parity phenomenon (context; not a route substitute)

**Verified.**  \(r=3\), all 435 Fano pairs: \(|Y\cap Z|\in\{0,1,3\}\)
(classical), and every **non-disjoint** pair has \(|Y\cap Z|\) odd
\(\equiv b=7\).  \(r=5\), all 31 125 pairs within the 250-system sample:
\(|Y\cap Z|\in\{0,6,12,18,30\}\) with multiplicities
\(702,\,16831,\,7251,\,6065,\,276\) — all even \(\equiv b=66\), disjoint
pairs included.  So at both testable parameters:

> every non-disjoint pair of systems satisfies
> \(|Y\cap Z|\equiv b\pmod2\), and disjoint pairs are the forced exception
> exactly when \(b\) is odd.

This suggests the parity in Conjecture P is a **pair** phenomenon — the
common base \(A\) may be irrelevant to the congruence itself and needed
only to exclude the disjoint escape.  Audit: this observation does *not*
imply P (it says nothing about whether two mates of a common base can be
disjoint, which at \(r=15\) is the whole question); it locates the
mechanism.  Status: Open in general; the \(r=5\) all-pairs spectrum here is
sample-complete for these 250 systems, and its literature status was not
checked in this session.

## 10. Answers to the four assigned directions, and next steps

1. **Oriented/signed boundary-Hodge representation; do determinant signs
   factor?**  Yes: Lemma 2.1 + Lemma 3.1 give a complete factorization of
   \(\operatorname{sgn}(\sigma)\) into pair determinants
   \(f(Y,Z)=\det(K+I)[Y,Z]\), gauge-canonical on closed products.  But
   Theorem 4.1 proves this entire layer measures \(e\bmod2\), which is
   disjoint from P; and Theorem 4.2 kills all signed-label refinements.
   Sign alone is now **closed as a vehicle for P**, with the SignLaw
   (§4) left as the residual, P-independent conjecture.  A combined
   argument would still be possible if it independently coupled odd and
   even cycle counts.
2. **Mod-4 determinant identities from inclusion/association matrices.**
   Split verdict.  Association/bilinear: the moment identities alone are
   **exhausted** (Theorem 8.1, all moduli); an additional nonlinear
   evaluation would be needed.  Determinant/elementary-divisor: the exact
   surviving target is
   Theorem 7.1 — P \(\iff\) even 2-multiplicity in
   \(\operatorname{SNF}\bigl((KP_AK+K)[B\setminus C,C\setminus B]\bigr)\).
   Open.
3. **Odd \(\sigma\)-cycle + Steiner uniqueness \(\Rightarrow\) forbidden
   trade?**  The naive version is **refuted** (cycles are never
   facet-closed at \(r=5\): 0/1828).  The rigorous residue is the complete
   radius-1 local model of an odd cycle (Lemmas 6.1–6.3: induced
   \(3\ell\)-cycle, three 1-intersection chains, integer position
   identity), with the odd-girth bound \(\ell\ge11\) at \(r=15\) still the
   only length obstruction.  Next falsifiable step: radius-2 UNSAT for
   \(\ell\in\{11,13\}\).
4. **Exact algebraic reduction of the quadratic intersection form.**
   Achieved in the negative-and-positive form: all invariant bilinear
   pairings reduce affinely to \(|B\cap C|\) (Theorem 8.1), and the
   genuinely quadratic-spectral content of P is isolated as the rank
   defect \(\operatorname{rank}_{\mathbb Q}-\operatorname{rank}_{\mathbb F_2}\)
   of the canonical matrix \(N\) (Theorem 7.1).

**Ranked next steps.**  (a) 2-adic analysis of
\(N=(KP_AK+K)[B\setminus C,C\setminus B]\) — e.g. relate its
\(\mathbb F_2\)-kernel to the pair-trade code \(C(D_1,D_2)\) machinery,
where dimension formulas are already exact (Theorem D loc. cit.).
(b) A structural (\(M_{11}\)-equivariant) proof of P at \(r=5\) remains the
single most informative feasible computation, now with the sharper goal of
explaining §9's all-pairs parity rather than the co-mate case only.
(c) Radius-2 UNSAT for short odd cycles at \(r=15\) against the full §6
constraint system.  (d) SL (§4) as an independent determinant-representable
target — valuable structurally, provably not sufficient for P.

## Provenance

All computations 2026-07-24 by
`collaboration/verify_fable_parity_attack_2.py` (single run, ~14 s, Python
stdlib, exact integer arithmetic, seed 20260724): \(r=3\) exhaustive over
all 30 systems / 435 pairs / 4060 triples; \(r=5\) over the full labelled
family of 5040 systems with sampled pair/triple checks as itemized above
and the canonical family (base + 144 mates, all 10 296 pairs) exhaustive
for cycle types and signs.  The cycle-trade census (0/1828 facet-closed at
\(r=5\); 300 pairs from 25 mates) was run as a separate inline computation
recorded in the session transcript.  The canonical \(r=5\) cycle-type
census reproduces `sigma_battery.py` exactly
(\((2,2,2,2,18,22)\times3960\), \((2,2,2,4,6,44)\times3960\),
\((4,4,4,4,4,40)\times1584\), \((2,2,2,2,2,10,20,20)\times792\)).
One stale item noticed in passing: the docstring of
`evidence/disjoint_mates.py` describes the Fano disjointness graph as a
perfect matching; the actual degree is 8 for every Fano (its own runtime
check would print "NOT a matching"), consistent with
\(|\mathcal D(A)|=8\) in the notes.
