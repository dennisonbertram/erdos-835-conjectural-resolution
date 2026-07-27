# A joint invariant of overlapping restrictions, and the exact reach of the sign layer

## 0. Scope, stated first

**Erdős–Rosenfeld problem #835 remains OPEN.**  Nothing here constructs a large
set, excludes \(k=16\), or decides \(LS(3,4,20)\), \(LS(4,5,21)\),
\(LS(14,15,31)\) or \(LS(15,16,32)\).

What is added:

* a **joint** invariant of the overlapping fixed-root restrictions of a large
  set — the exact structure the independent audit flagged as still open in
  Corollary G1.1 — together with an identity relating it up and down the
  derivation tower (Theorems 1–2);
* the resulting **necessary condition** on the \(190\) pair-links of any
  \(LS(3,4,20)\), and the \(347{,}373{,}600\) parity equations on
  fourteen-point link signs forced by any \(LS(15,16,32)\) (Theorem 4);
* a demonstration that this invariant is **not vacuous**: it excludes
  \(LS(2,3,7)\), the unique exception in the LSTS spectrum, by a two-line
  parity argument (Corollary 3);
* a **route delimiter**: the invariant, and provably every abelian-valued
  invariant of the same shape, **cannot decide \(LS(3,4,20)\)** (Theorems
  5–6).  Explicit witnesses inside a genuine repository object show why
  (§5).

Claims are marked **proved** (mathematics, argued here) or **certified
computational** (exhaustive finite enumeration by `verify_star_sign.py`,
44 checks).  Solver runs are reported in §7 and carry **no** mathematical
weight in either direction.

**No priority is claimed for the one-factorization sign.**  It is known: see
§6.

## 1. Notation

\(m\ge3\) is odd, \(v=t+m\), and \(X\) is an ordered \(v\)-set.  A large set
\(LS(t,t+1,v)\) is presented as a colouring
\[
  c:\tbinom X{t+1}\longrightarrow[m]
\]
whose colour classes are \(m\) pairwise disjoint \(S(t,t+1,v)\).  Equivalently
and more usefully here:

> **(L)** for every \(T\in\binom Xt\) the *star map*
> \(\chi_T:X\setminus T\to[m]\), \(\chi_T(x)=c(T\cup\{x\})\), is a
> **bijection**.

(\(|X\setminus T|=v-t=m\); a class covers \(T\) exactly once iff its colour
occurs exactly once in the star.)  For \(p\in X\) the derived large set is
\(c^p(B)=c(B\cup\{p\})\) on \(X\setminus\{p\}\), an \(LS(t-1,t,v-1)\);
note
\[
  \chi^{\,p}_{T'}=\chi_{T'\cup\{p\}}\qquad\bigl(T'\in\tbinom{X\setminus\{p\}}{t-1}\bigr),
  \tag{1}
\]
as maps, with the same domain and the same induced order.

\(J(n,s)\) is the Johnson graph.  Theorem G1 of
`collaboration/opus5/generic_radius4_certificate_attack/NOTE.md` is used as
stated there: for \(m\) odd and \(n=m+s-2\),
\(\chi(J(n,s))\le m\iff LS(s-1,s,n+1)\).

For ordered finite sets \(A,B\) with \(|A|=|B|\) and a bijection \(f:A\to B\),
\(\operatorname{sgn}(f)\) is the sign of the induced permutation.

## 2. The star sign

> **Definition.**  \(\displaystyle E_t(c)=\prod_{T\in\binom Xt}\operatorname{sgn}(\chi_T)\in\{\pm1\}.\)

> **Theorem 1 (well-definedness and exact equivariance; *proved*).**
> Let \(\pi\) be a transposition of the colours and \(\tau\) a transposition of
> the points.  Then
> \[
>   E_t(\pi\!\cdot\!c)=(-1)^{\binom vt}E_t(c),\qquad
>   E_t(\tau\!\cdot\!c)=(-1)^{\binom vt+\binom{v-1}{t-1}+\binom{v-2}{t-1}}E_t(c).
> \]
> Hence \(E_t\) is an isomorphism invariant of the large set precisely when both
> exponents are even.

*Proof.*  A colour transposition replaces each \(\chi_T\) by \(\pi\chi_T\),
multiplying each factor by \(-1\); there are \(\binom vt\) factors.
For points, \(\chi'_{\tau T}=\chi_T\circ\tau^{-1}\), so
\(E_t(\tau\!\cdot\!c)=E_t(c)\prod_T\sigma(\tau,T)\) where \(\sigma(\tau,T)\) is
the sign of \(\tau:X\setminus T\to X\setminus\tau T\).  Splitting \(\tau\) into
its restrictions to \(T\) and to \(X\setminus T\) and shuffling both \(T\) and
\(\tau T\) to the front gives
\(\sigma(\tau,T)=\operatorname{sgn}(\tau)\,\alpha(T)\,\alpha(\tau T)\operatorname{sgn}(\tau|_T)\)
with \(\alpha\) the shuffle sign; since \(T\mapsto\tau T\) is a bijection of
\(\binom Xt\), the two \(\alpha\)-products cancel and
\[
  \prod_T\sigma(\tau,T)=\operatorname{sgn}(\tau)^{\binom vt}\prod_T\operatorname{sgn}(\tau|_T).
\]
The \(t\)-th compound matrix \(\Lambda^t(P_\tau)\) is the signed permutation
matrix with permutation \(T\mapsto\tau T\) and signs \(\operatorname{sgn}(\tau|_T)\), so
\(\det\Lambda^t(P_\tau)=\operatorname{sgn}(\tau^{(t)})\prod_T\operatorname{sgn}(\tau|_T)\); and
\(\det\Lambda^t(A)=\det(A)^{\binom{v-1}{t-1}}\).  Hence
\(\prod_T\operatorname{sgn}(\tau|_T)=\operatorname{sgn}(\tau)^{\binom{v-1}{t-1}}\operatorname{sgn}(\tau^{(t)})\).
Finally a transposition moves exactly the \(t\)-sets containing exactly one of
its two points, in \(\binom{v-2}{t-1}\) swapped pairs, so
\(\operatorname{sgn}(\tau^{(t)})=(-1)^{\binom{v-2}{t-1}}\). \(\square\)

*Certified computational.*  Both formulas are checked against brute force over
all \(5!\) colour and all \(6!\) point relabellings at \((v,t)=(6,1)\), and the
predicted **anti**-invariance is checked at \((v,t)=(9,2)\) on a genuine
\(LS(2,3,9)\).

On the \(m=17\) segment relevant to \(k=16\), namely \(1\le t\le15\), the
table is (*certified computational*): \(E_t\) is a genuine isomorphism
invariant exactly for odd \(t\).  This is not asserted for \(t>15\) (for
example \(E_{18}\) at \(v=35\) is also invariant).  In particular \(E_3\)
(the \(LS(3,4,20)\) rung) and \(E_{15}\) (the \(k=16\) target rung) are
invariants; \(E_2\) (the \(LS(2,3,19)\) rung) is **not** — an odd colour
relabelling flips it, because \(\binom{19}2=171\) is odd.  That last fact is
what closes this particular route; see §5.

## 3. The tower identity

> **Theorem 2 (*proved*).**  For every large set \(c\) of type
> \(LS(t,t+1,v)\), \(t\ge1\),
> \[
>   \boxed{\ \prod_{p\in X}E_{t-1}\bigl(c^{\,p}\bigr)\;=\;E_t(c)^{\,t}.\ }
> \]

*Proof.*  By (1), \(E_{t-1}(c^{\,p})=\prod_{T\ni p,\;|T|=t}\operatorname{sgn}(\chi_T)\).
Multiplying over \(p\in X\) counts each \(T\) once for each of its \(t\)
points. \(\square\)

Two regimes.  For **odd** \(t\) the identity *computes* \(E_t\) and constrains
nothing.  For **even** \(t\) the right-hand side is \(+1\) and the identity is a
genuine parity law:

> **Theorem 3 (rung-two parity law; *proved*).**  In every \(LS(2,3,v)\) the
> number of points \(p\) whose derived one-factorization of \(K_{v-1}\) has star
> sign \(-1\) is **even**.

> **Corollary 3.1 (*proved*, with a certified finite input).**
> \(LS(2,3,7)\) does not exist.
>
> *Proof.*  Every one-factorization of \(K_6\) has star sign \(-1\) (exhaustive
> enumeration of all six, and invariance under all \(6!\cdot5!\) relabellings).
> An \(LS(2,3,7)\) has seven points, so Theorem 3 would need \((-1)^7=+1\).
> \(\square\)

This is the unique exception in the LSTS spectrum.  The result is classical
(Cayley 1850); the argument above is offered only as evidence that the
invariant has teeth, and no priority is claimed (§6).

*Certified computational.*  Theorem 2 is replayed on an exhaustively
constructed \(LS(2,3,9)\) and on the repository's audited cyclic
\(LS(2,3,19)\); Corollary 3.1 is cross-checked against an independent
exhaustive search that finds no \(LS(2,3,7)\).

## 4. The joint constraint on overlapping restrictions

Corollary G1.1 classifies each **single** fixed-root/retained-set restriction.
The audit's open question was whether several such restrictions are jointly
stronger.  Theorem 2 gives an explicit instance of exactly that.

Fix an \(LS(3,4,20)\).  For each pair \(P=\{p,q\}\subseteq[20]\) the
**pair-link**
\[
  F_P(xy)=c(\{p,q,x,y\}),\qquad x,y\in[20]\setminus P,
\]
is a one-factorization of \(K_{18}\) with \(17\) colours (properness: two such
quadruples sharing a vertex share a triple).  Let
\(\varepsilon(P)=E_1(F_P)\in\{\pm1\}\); by Theorem 1 with \((v,t)=(18,1)\) this
is an isomorphism invariant of \(F_P\) alone.

More generally, for \(R\in\binom X{t-1}\), write
\[
  \varepsilon(R)=E_1(c^R),
\]
where \(c^R\) is the one-factorization obtained by deriving along all points
of \(R\).

> **Theorem 4 (*proved*).**  Let \(c\) be an \(LS(3,4,20)\).  Then for every
> \(p\in[20]\)
> \[
>   \prod_{q\ne p}\varepsilon(\{p,q\})=+1 ,
> \]
> i.e. the graph \(G_-=\{\,pq:\varepsilon(\{p,q\})=-1\,\}\) on \([20]\) has all
> degrees **even**.
>
> More generally, in any \(LS(t,t+1,t+17)\), for every
> \(W\in\binom X{t-2}\),
> \[
>   \boxed{\ \prod_{p\in X\setminus W}\varepsilon(W\cup\{p\})=+1.\ }
> \]
> Equivalently, when \(t\ge3\), for every \(Z\in\binom X{t-3}\), the graph
> on \(X\setminus Z\) with edge \(pq\) when
> \(\varepsilon(Z\cup\{p,q\})=-1\) has all degrees even.
>
> At the \(k=16\) rung \(t=15\), there are
> \(\binom{32}{13}=347{,}373{,}600\) nineteen-term equations on
> \(\binom{32}{14}=471{,}435{,}600\) fourteen-subset signs.  Their exact
> \(\mathbb F_2\)-rank is
> \(\binom{31}{13}=206{,}253{,}075\).  Equivalently there are
> \(\binom{32}{12}=225{,}792{,}840\) even graphs indexed by
> twelve-subsets.

*Proof.*  The displayed \(LS(3,4,20)\) result is Theorem 3 after deriving at
\(p\).  In general, derive along \(W\); by Theorem 9 of
`collaboration/opus5/derivation_tower_obstruction/NOTE.md` the result is an
\(LS(2,3,19)\), and its point-derived factorization at \(p\) is exactly
\(c^{W\cup\{p\}}\).  Apply Theorem 3.  The rank statement is the standard
rank \(\binom{n-1}{r}\) of the mod-two inclusion matrix from
\((r+1)\)-subsets to \(r\)-subsets (equivalently, exactness of the simplex
chain complex), here with \(n=32,r=13\). \(\square\)

**Why this is a joint condition and not a restatement of G1.1.**  Each single
pair-link is a standalone \(LS(1,2,18)\) restriction; by G1.1 its standalone
test is exactly "a one-factorization of \(K_{18}\) exists", which is
satisfiable, and \(\varepsilon\) takes **both** values on \(K_{18}\)
(§5), so no single restriction constrains \(\varepsilon\) at all.  Theorem 4
constrains the \(190\) of them **simultaneously**.  The sign patterns not
excluded by these equations form precisely the cycle space of \(K_{20}\), of
dimension \(190-19=171\); the twenty equations have
\(\mathbb F_2\)-rank \(19\), not \(20\), because they sum to zero.  This
linear-algebra statement does not assert that every cycle-space pattern is
realizable by a large set.  This is the first invariant in this programme
that lives on the overlap of several restrictions rather than on any one of
them.

*Certified computational.*  The \(19\)-point instance of Theorem 4 is verified
directly on the repository's cyclic \(LS(2,3,19)\): its nineteen point-links
have signs \(18\times(-1)\) and \(1\times(+1)\), an even number of \(-1\)s.

## 5. Route delimiter: the sign layer cannot decide \(LS(3,4,20)\)

The mechanism of Corollary 3.1 needs two ingredients at a rung with an odd
number of points: the predecessor rung must be **rigid** (its star sign
constant) and the constant must be \(-1\).  Neither survives in the \(m=17\)
tower.

> **Theorem 5 (*proved*; the negative input is certified computational).**
> The star-sign parity law cannot exclude any rung of the \(m=17\) tower at or
> below \(LS(3,4,20)\).  Specifically:
>
> **(a)** \(K_{18}\) is not rigid.  Both signs occur: among the nineteen
> point-links of the repository's audited cyclic \(LS(2,3,19)\), eighteen have
> star sign \(-1\) and one has \(+1\).  Hence Theorem 3 is satisfiable at
> \(v=19\), as it must be.
>
> **(b)** At the \(LS(3,4,20)\) rung the identity reads
> \(\prod_{p\in[20]}E_2(c^{\,p})=E_3(c)\).  This *defines* \(E_3\) and
> constrains nothing.  It cannot be turned into a parity law, because
> \(E_2\) is not an isomorphism invariant at \(v=19\)
> (\(\binom{19}2=171\) is odd, Theorem 1), so no rigidity is available to feed
> it.
>
> **(c)** The next even rung, \(t=4\), gives
> \(\prod_{p\in[21]}E_3(c^{\,p})=+1\).  The same rigidity argument used in
> Corollary 3.1 would fire if \(E_3\) were known to be constantly \(-1\) on
> all attainable \(LS(3,4,20)\).  No such rigidity is proved here; other
> information about attainable sign distributions or overlapping derived
> objects is not ruled out.

The delimiter is not confined to this one invariant.

> **Theorem 6 (the abelian layer is exactly the star sign; *proved*).**  Fix
> the order-preserving reference bijections \(\iota_T:X\setminus T\to[m]\) and
> read \(\chi_T\iota_T^{-1}\in S_m\).  Let \(A\) be any abelian group and
> \(\varphi:S_m\to A\) any homomorphism.  Then
> \[
>   I_\varphi(c)=\prod_{T\in\binom Xt}\varphi\bigl(\chi_T\iota_T^{-1}\bigr)
> \]
> is a function of \(E_t(c)\) alone.
>
> *Proof.*  \([S_m,S_m]=A_m\) for \(m\ge2\), so \(S_m^{\mathrm{ab}}\cong\mathbb
> Z/2\) and \(\varphi=\psi\circ\operatorname{sgn}\) for some
> \(\psi:\mathbb Z/2\to A\).  Hence \(I_\varphi(c)=\psi(E_t(c))\). \(\square\)

**Consequence, stated exactly.**  No product-over-stars invariant with values
in an abelian group is stronger than \(E_t\); by Theorem 5 that whole family is
blind to \(LS(3,4,20)\).  This is a delimiter for the *shape* of the invariant.
It does **not** close non-abelian holonomy invariants (the transition
permutations \(\chi_{R\cup b}\chi_{R\cup a}^{-1}\in S_m\) up to conjugacy),
counting invariants, or anything that is not a product over stars of a
homomorphic image.  It is also consistent with, and independently explains, the
repository's repeated finding that its Pfaffian/flag/layer sign computations
come out identically \(+1\).

## 5b. The successor layer: holonomy, and why the delimiter is not the end

Theorem 6 closes the abelian layer.  The obvious next layer is non-abelian, and
it exists, is computable, and satisfies its own tower identity.

For \(R\in\binom X{t-1}\) and \(a\ne b\) in \(X\setminus R\) put
\[
  \sigma_R(a,b)=\chi_{R\cup b}\circ\chi_{R\cup a}^{-1}.
\]
It is defined on \([m]\) minus the colour \(c(R\cup\{a,b\})\) and permutes that
set (because \(\chi_{R\cup b}(a)=c(R\cup\{a,b\})=\chi_{R\cup a}(b)\)); extended
by fixing that colour it lies in \(S_m\).  This is its **unique** fixed point:
another fixed colour would give two same-coloured edges incident with one
vertex in the induced one-factorization.  Its **cycle type** is a conjugation
invariant, strictly finer than its sign, which it determines via
\(\operatorname{sgn}=(-1)^{m-\#\text{cycles}}\).  Write
\(N_\kappa(c)\) for the number of pairs \((R,\{a,b\})\) whose holonomy has cycle
type \(\kappa\).

> **Theorem 7 (holonomy tower identity; *proved*).**  For every large set of
> type \(LS(t,t+1,v)\) with \(t\ge2\), and every cycle type \(\kappa\),
> \[
>   \sum_{p\in X}N_\kappa\bigl(c^{\,p}\bigr)=(t-1)\,N_\kappa(c).
> \]
>
> *Proof.*  By (1), the holonomy of \(c^{\,p}\) indexed by
> \((R',\{a,b\})\) with \(|R'|=t-2\) is
> \(\chi_{R'\cup\{p,b\}}\chi_{R'\cup\{p,a\}}^{-1}=\sigma_{R'\cup\{p\}}(a,b)\).
> Summing over \(p\) counts each \((R,\{a,b\})\) once for each of the \(|R|=t-1\)
> points of \(R\). \(\square\)

At the \(LS(3,4,20)\) rung this reads
\(\sum_{p\in[20]}N_\kappa(c^{\,p})\equiv0\pmod 2\) for **every** cycle type
\(\kappa\) — a joint condition on the twenty derived \(LS(2,3,19)\), one parity
per cycle type.  The relevant types have exactly one part \(1\): they are
\((\lambda,1)\), where \(\lambda\vdash16\) has no part \(1\).  There are
\(p(16)-p(15)=231-176=\mathbf{55}\), not 231.

*Certified computational.*  Theorem 7 is replayed on the exhaustively
constructed \(LS(2,3,9)\) (\(9\binom82=252\) holonomy pairs, \(4\) cycle types)
and on the repository's cyclic \(LS(2,3,19)\) (\(19\binom{18}2=2907\) pairs,
**\(34\)** distinct cycle types, every one with exactly one fixed point).
Thirty-four values where the sign layer has two is a direct measurement that
this layer is strictly finer.

**What is not claimed.**  Theorem 7 is an identity, so on any genuine object it
holds automatically; it is a necessary condition on *candidate* families of
derived large sets, not an obstruction.  Whether the holonomy census of an
\(LS(2,3,19)\) is constrained enough to make the parity conditions bite is
**open**, and is the concrete next question this note leaves behind.

## 6. Literature

**The one-factorization sign is known; no priority is claimed.**  For a
one-factorization \(F\) of \(K_n\), \(E_1(F)=\prod_y\operatorname{sgn}(\rho_y)\)
with \(\rho_y(z)=F(yz)\) is the sign used in the list-edge-colouring
literature: U. Schauz, *Orientations of 1-factorizations and the list chromatic
index of small graphs*, arXiv:1705.00484, defines it in this form and refers to
"the well-known connection between the sign of 1-factorizations and the List
Edge Coloring Conjecture", tracing to M. N. Ellingham and L. Goddyn, *List edge
colourings of some 1-factorable multigraphs*, Combinatorica **16** (1996)
343–352, which applies the method of N. Alon and M. Tarsi, *Colorings and
orientations of graphs*, Combinatorica **12** (1992) 125–134.

**Not found** by an independent primary-source search: the star sign \(E_t\) of
a large set for \(t\ge2\); the tower identity of Theorem 2; any sign or parity
invariant for large sets of designs or for partitions of the \(k\)-subsets of
an \(n\)-set into Steiner systems; any parity proof of the \(LS(2,3,7)\)
exception (the standard citation is A. Cayley, *On the triadic arrangements of
seven and fifteen things*, Phil. Mag. (3) **37** (1850) 50–53; textbook
treatment C. Colbourn and A. Rosa, *Triple Systems*, OUP 1999, ch. 16).  "Not
found" is not a priority claim.

**Two corrections to the repository's recorded literature status.**

1. `evidence/large_set_literature_2026-07-26.md` states that "Keevash's general
   theorem proves their existence nonconstructively for all sufficiently large
   admissible \(v\)" for \(LS(3,4,v)\).  The *assertion* is indeed in the
   literature — T. Etzion and J. Zhou, arXiv:1912.04489, write "it is known
   that they exist if \(n\equiv2\) or \(4\pmod6\) is large enough" — but the
   general theorem an independent search could locate is S. Lovett, S. Rao and
   A. Vardy, *Probabilistic existence of large sets of designs*, SODA 2018,
   arXiv:1704.07964, whose hypothesis is \(k>12t\).  For \(LS(t,t+1,\cdot)\)
   one has \(k=t+1\), so \(k>12t\) fails for **every** \(t\ge1\) and that
   theorem does not cover any rung of any tower here.  An independent search of
   Glock–Kühn–Lo–Osthus found no occurrence of "large set" at all.  The
   attribution therefore needs checking before it is relied on.  **Nothing in
   this note depends on it either way**; it is recorded because a route
   delimiter of the form "no fixed rung can obstruct all \(k\), because low
   rungs exist for large \(m\)" would depend on it, and that delimiter is
   therefore **not** established here.
2. Two facts worth having, both from A. E. Brouwer's maintained tables (citing
   Etzion–Bitan 1996 and Brouwer–Etzion 2011 for the first, Brouwer–Etzion 2011
   and Agrell–Vardy–Zeger 2000 for the second):
   \(\chi(J(15,4))\in\{13,14\}\) and \(\chi(J(16,4))\in\{13,14\}\) are **open**
   entries, and the packing numbers \(C(15,4,3)=105\), \(C(19,4,3)=228\) are
   **optimal**.  By Theorem G1, \(\chi(J(15,4))=13\iff LS(3,4,16)\); by the
   packing numbers, \(\chi(J(15,4))\ge13\) and \(\chi(J(19,4))\ge17\).

## 7. Operational record (no mathematical weight)

**Stochastic local search is the wrong tool, and the calibration says so.**
Two independent searches were written — a min-conflicts annealer on the large
set directly (`anneal_ls.c`) and TabuCol on the Theorem-G1 form
(`tabucol_johnson.c`) — and calibrated on **known-positive** instances.  Both
solve \(LS(2,3,9)\) in well under a second.  Both then fail on
\(LS(2,3,13)\), which **exists** (Lu–Teirlinck): the annealer finishes at
`best_cost=9` after \(1{,}610{,}612{,}736\) iterations in \(120.1\) s
(`runs/calib_anneal_ls2313.txt`), and TabuCol on the equivalent \(J(12,3)\)
instance with \(11\) colours plateaus in double figures of monochromatic edges
(`runs/calib_tabu_j12.txt`).  The reason is structural and worth recording: in
every one of these instances the colour classes must be *maximum* packings with
zero slack — \(\binom{19}4/17=228=C(19,4,3)\), \(\binom{15}4/13=105=C(15,4,3)\),
and at the calibration point \(\binom{12}3/11=20=C(12,3,2)\) — which is the
classical failure regime for local search.
Since the method cannot reach a large set that is known to exist at \(v=13\),
it carries no information at \(v=16\) or \(v=20\).  **This is an operational
observation about a method, not evidence about existence.**

**Exact solving.**  Instances in the Theorem-G1 form were generated by
`g1_cnf.py` with a root-star normalisation that is a genuine WLOG, and a
complete second-star symmetry break (`second_star_split.py`) whose orbit
classification is verified against brute force at small sizes:

| instance | meaning | vars | clauses | branches |
|---|---|---|---|---|
| \(J(15,4)\), \(m=13\) | \(LS(3,4,16)\); an open entry of Brouwer's table | 17,745 | 498,237 | 56 |
| \(J(19,4)\), \(m=17\) | \(LS(3,4,20)\); the first open rung at \(k=16\) | 65,892 | 2,507,788 | 176 |

The positive control is retained under `controls/`: CaDiCaL 3.0.1 constructs
a \(J(8,3)\) seven-colouring and `verify_solution.py` semantically verifies
its G1 lift as \(LS(2,3,9)\).  Separately, `verify_star_sign.py` performs an
exhaustive solver-free refutation of \(LS(2,3,7)\).  An attempted
\(LS(3,4,10)\) solver control did not finish and no claim is made from it.

**State of the sweep at the close of this session: complete but
inconclusive.**  The \(J(15,4)\) sweep used a \(900\)-second CaDiCaL limit per
branch, four at a time, on a machine already carrying the repository's own
long-running searches (load average above \(200\), so each solver initially
received roughly a third of a core).  All \(56\) branches returned
`UNKNOWN(exit 0)`.  The complete log and structured ledger are retained as
`runs/j15_branches.log` and `runs/j15_branches/verdicts.json`; temporary branch
CNFs were deleted by the runner.  The unbranched \(J(19,4)\) run likewise
retained only `c UNKNOWN` and produced no verdict.  See `runs/README.md` for
exact scope and hashes.

Per the standing discipline of this repository: an `UNKNOWN`, a timeout, or an
unfinished search is **not** mathematical evidence in either direction; a SAT
result counts only after `verify_solution.py` accepts it; an UNSAT result
counts only after an independent proof check.  Note also that even a decided
\(LS(3,4,16)\) says
nothing about \(k=16\): it is a rung of the \(m=13\) tower, and \(k=12\) is
already excluded at the rung above it by the nonexistence of \(S(4,5,17)\).

## 8. Inventory

**Proved here.**  Theorem 1 (exact equivariance of the star sign, with the
compound-matrix computation); Theorem 2 (the tower identity); Theorem 3 (the
rung-two parity law) and Corollary 3.1 (a parity exclusion of \(LS(2,3,7)\));
Theorem 4 (the joint even-degree condition on the \(LS(3,4,20)\) pair-links
and its correctly indexed general parity law, including
\(347{,}373{,}600\) equations of rank \(206{,}253{,}075\) at the \(k=16\)
rung); Theorem 5 (the limits of the displayed rigidity argument, with
explicit both-sign witnesses in \(K_{18}\)); Theorem 6 (every
abelian-valued product-over-stars invariant is a function of the star sign);
Theorem 7 (the holonomy tower identity, the non-abelian successor left open
by Theorem 6).

**Not claimed.**  Existence or nonexistence of \(LS(3,4,16)\), \(LS(3,4,20)\),
\(LS(4,5,21)\), \(LS(14,15,31)\) or \(LS(15,16,32)\); any exclusion of
\(k=16\); **and any progress on the existential quantifier in Erdős–Rosenfeld
#835, which remains open.**

## 9. Verification

```sh
cd collaboration/opus5/unrestricted_ls3420_attack_2
python3 -B verify_star_sign.py        # 44 checks, standard library only
python3 -B second_star_split.py       # brute-force completeness of the branch split
python3 -B verify_solution.py 8 3 7 controls/j8_3_m7.model
```

Standard library only, exact finite arithmetic, no solver, no randomness, no
network.  `verify_star_sign.py` checks the compound-matrix restriction identity of
Theorem 1 by brute force over **every** permutation of \([v]\) for
\(v\le7\) and every \(t\) (with no design theory involved), checks the
Theorem 6 group input \([S_m,S_m]=A_m\) for \(m=3,4,5\), re-derives the
equivariance exponents against brute force, enumerates every one-factorization of \(K_4\), \(K_6\) and
\(K_8\) (1, 6 and 6240 of them, signs \(\{+1\}\), \(\{-1\}\) and
\(5280\!:\!960\)), rebuilds an \(LS(2,3,9)\) exhaustively, imports and
re-validates the repository's cyclic \(LS(2,3,19)\), replays Theorem 2 on both,
runs an independent exhaustive refutation of \(LS(2,3,7)\) as a control, and
checks every arithmetic constant quoted above.  `AUDIT.md` records the
independent proof-and-code audit and the corrections incorporated here.
