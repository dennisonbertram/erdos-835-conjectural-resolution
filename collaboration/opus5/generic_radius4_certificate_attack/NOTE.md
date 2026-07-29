# The generic one-point lift, and where the derivation tower actually breaks

## 0. Scope, stated first

**Erdős–Rosenfeld problem #835 remains OPEN.**  Nothing here settles a
previously open value of \(k\), constructs a new large set, or decides
\(LS(3,4,20)\), \(LS(4,5,21)\), or \(LS(14,15,31)\).  The \(C_{17}\)
fixed-link extension remains UNKNOWN and is untouched by this note.

Two additions are recorded here.

* **Theorem G1**, an unconditional equivalence uniform in every odd colour
  count \(m\) and every \(s\).  It strictly generalises the repository's
  "Odd-neighbour lift theorem"
  (`erdos_835_conjectural_resolution.md:174–181`), which is the diagonal case
  \(s=m-2\).  For each fixed root and retained set, it identifies the
  standalone restriction of the derived/link colouring with one rung of the
  derivation tower (Corollary G1.1).  It does **not** remove simultaneous
  compatibility constraints among several roots or overlapping restrictions.
  No literature-priority claim is made.
* A deterministic exact computation independently reproduces the classical
  Kramer–Mesner value **\(D(10)=5\)**, the maximum number of pairwise disjoint
  \(SQS(10)\).  Hence \(LS(3,4,10)\) does not exist, and tower monotonicity
  also excludes \(LS(4,5,11)\) and \(LS(5,6,12)\).  This is a reproducibility
  check and a lower-rung re-proof of the already known \(k=6\) exclusion, not
  a new mathematical result.

The consequence for the programme is a *targeting* observation, not an
obstruction: the two smallest admissible cases profiled here both fail at the
first rung not classically guaranteed, and for \(m=17\) that rung is exactly
\(LS(3,4,20)\).

Claims below are marked **proved** (mathematics, argued here), **certified
computational** (exhaustive finite enumeration by the committed verifiers), or
**UNKNOWN**.

## 1. Why this route, and not a generic radius-four certificate

The brief named a complete generic radius-four \(k=16\) obstruction.  Two facts
decided against spending the session there.

1. **The plain radius-four ball is satisfiable at \(k=16\).**  The repository
   already holds "an explicit cyclic-golf radius-four colouring … checked
   semantically on all \(14{,}657\) ball vertices and against every clause of an
   independently generated \(738{,}537\)-clause CNF"
   (`README.md`, `evidence/odd_graph_local_ball/`).  A satisfiable object
   carries no obstruction.  The only radius-four-flavoured instance that could
   is the radius-four-**plus-forced-trace** CNF (883,521 variables,
   1,909,497 clauses), which is a pure solver task, has no verdict after
   repeated attempts, and would attach no new mathematics.
2. **Even a complete radius-four obstruction excludes only \(k=16\).**
   Theorem G1 instead gives a uniform equivalence for every odd \(m\) and every
   \(s\), although it is a route delimiter rather than an obstruction.

## 2. Notation

Fix a colour count \(m\ge3\).  The **tower** is the family of large sets
\[
  LS(t,t+1,t+m),\qquad t\ge1 ,
\]
i.e. \(m\) pairwise disjoint Steiner systems \(S(t,t+1,t+m)\) partitioning all
\((t+1)\)-subsets of a \((t+m)\)-set; the member count \( (t+m)-t = m\) is
constant up the tower.  For \(m=k+1\) the #835 object at parameter \(k\) is the
rung \(t=k-1\), and rung \(t=k-2\) is its \(S(k-2,k-1,2k-1)\) form.  Derivation
(companion Theorem 9) gives rung \(t\Rightarrow\) rung \(t-1\), so **the tower
is decided by its first failing rung**.

\(J(n,s)\) is the Johnson graph: vertices the \(s\)-subsets of \([n]\), adjacent
when they meet in \(s-1\) points.  Two \(s\)-sets are adjacent exactly when
both lie in the **star** of their common \((s-1)\)-set, so a colouring of
\(\binom{[n]}s\) is proper on \(J(n,s)\) **iff every star is rainbow**.  A star
has \(n-s+1\) members.

## 3. Theorem G1 (the generic one-point lift)

> **Theorem G1** (*proved*).  Let \(m\ge3\) be **odd** and let \(s\ge1\).  Put
> \[
>   n=m+s-2,\qquad v=n+1=m+s-1 .
> \]
> Then
> \[
>  \boxed{\ \chi\bigl(J(n,s)\bigr)\le m
>   \iff LS(s-1,s,v)\ \text{exists}.\ }
> \]
> Moreover *delete a point* and *adjoin a point via the missing-colour map*
> are **mutually inverse bijections** between the proper \(m\)-colourings of
> \(J(n,s)\) and the large sets \(LS(s-1,s,v)\) with labelled classes.

For \(s\ge2\), the two hypotheses are exactly what make the proof work:
\(n=m+s-2\) makes a star of \(J(n,s)\) have \(n-s+1=m-1\) members — one short of
the colour count — and makes the complement of an \((s-2)\)-set have exactly
\(m\) points; \(m\) odd makes \(K_m\) class 2 in the sharp way used in Step 2.
The boundary case \(s=1\) is elementary and does not require oddness.

### Proof

**(\(\Leftarrow\))**  Let \(\{D_1,\dots,D_m\}\) be a large set \(LS(s-1,s,v)\)
on \([v]\) and fix \(p\in[v]\).  Put \(C_i=\{B\in D_i:p\notin B\}\).  The
\(C_i\) partition \(\binom{[v]\setminus\{p\}}s=\binom{[n]}s\), and each
\(C_i\subseteq D_i\) is a partial \(S(s-1,s,\cdot)\), so no two of its members
share \(s-1\) points: each \(C_i\) is independent in \(J(n,s)\).  Hence the
class map is a proper \(m\)-colouring.

**(\(\Rightarrow\))**  Let \(c\) be a proper \(m\)-colouring of \(J(n,s)\).

If \(s=1\), then \(J(m-1,1)=K_{m-1}\), so the \(m-1\) singleton vertices have
distinct colours and leave a unique colour unused.  Give the new singleton
\(\{\ast\}\) that missing colour.  The \(m\) labelled colour classes are then
the \(m\) singleton systems of \(LS(0,1,m)\), and deletion plainly reverses the
construction.  Hence assume \(s\ge2\).

*Step 1 (the missing-colour map).*  For \(S\in\binom{[n]}{s-1}\) the star
\(\{S\cup\{x\}:x\in[n]\setminus S\}\) is a clique with
\(n-s+1=m-1\) members, so its colours are \(m-1\) distinct values.  Let
\(\psi(S)\in[m]\) be the unique colour absent from it.

*Step 2 (key lemma).*  **For every \(R\in\binom{[n]}{s-2}\) the map
\(y\mapsto\psi(R\cup\{y\})\) is a bijection \([n]\setminus R\to[m]\).**

Put \(V=[n]\setminus R\), so \(|V|=n-(s-2)=m\).  For \(y\ne z\) in \(V\) the set
\(R\cup\{y,z\}\) is an \(s\)-set; colour the edge \(yz\) of \(K_V\) by
\(\gamma(yz)=c(R\cup\{y,z\})\).  Two edges sharing a vertex \(y\) give
\(s\)-sets sharing the \((s-1)\)-set \(R\cup\{y\}\), hence adjacent, hence
differently coloured: \(\gamma\) is a **proper edge colouring of \(K_m\)** with
colours from \([m]\).  Since \(m\) is odd, every colour class is a matching of
size at most \((m-1)/2\); as \(K_m\) has \(m(m-1)/2\) edges and there are only
\(m\) colours, **every** class is a maximum matching of size exactly
\((m-1)/2\), so each colour misses exactly one vertex, and all \(m\) colours
occur.  The \(m-1\) edges at a fixed \(y\) have distinct colours, so exactly one
colour is missing at \(y\).  Counting incidences, the deficiency map
\(\mathrm{def}:[m]\to V\) is a bijection.  Finally the star of \(R\cup\{y\}\)
is \(\{R\cup\{y,x\}:x\in V\setminus\{y\}\}\), whose colours are the
\(\gamma\)-colours of the edges at \(y\); so \(\psi(R\cup\{y\})\) is precisely
the colour missing at \(y\), i.e. \(\mathrm{def}^{-1}(y)\).  \(\square\)

*Step 3 (adjoin a point).*  Let \(\ast\) be a new point, \([v]=[n]\cup\{\ast\}\),
and set
\[
  D_i=\{B: c(B)=i\}\ \cup\ \bigl\{S\cup\{\ast\}: \psi(S)=i\bigr\}.
\]
These partition \(\binom{[v]}s\) by construction.  Each \(D_i\) is an
\(S(s-1,s,v)\):

* for \(S\in\binom{[n]}{s-1}\): the star of \(S\) contains exactly one block of
  colour \(i\) when \(i\ne\psi(S)\) and none when \(i=\psi(S)\), while
  \(S\cup\{\ast\}\in D_i\) exactly in the second case — one cover either way;
* for \(\{\ast\}\cup R\) with \(R\in\binom{[n]}{s-2}\): its covers in \(D_i\) are
  the \(S\cup\{\ast\}\) with \(R\subset S\) and \(\psi(S)=i\), i.e. the
  \(y\in[n]\setminus R\) with \(\psi(R\cup\{y\})=i\) — exactly one, by Step 2.

Since \(v-(s-1)=m\), the \(m\) systems \(D_i\) are a large set \(LS(s-1,s,v)\).

*Mutual inverses.*  Deleting \(\ast\) from the constructed large set returns
\(c\).  Conversely, starting from a large set and deleting \(p\), the
reconstructed \(\psi(S)\) is the colour \(i\) whose unique \(D_i\)-block on
\(S\) contains \(p\), i.e. the colour of \(S\cup\{p\}\); re-adjoining therefore
restores every \(D_i\) exactly.  \(\blacksquare\)

### Sharpness, on both sides (*certified computational*)

* **\(m\) odd is necessary.**  For even \(m\) and \(s=2\): \(J(m,2)=L(K_m)\) is
  \(m\)-colourable (indeed \(\chi'(K_m)=m-1\)), yet \(LS(1,2,m+1)\) is a
  one-factorisation of \(K_{m+1}\) with \(m+1\) odd, which does not exist.
  Checked at \(m=4,6,8\).
* **A second deletion can be lossy.**  The following two examples show that a
  two-point analogue fails in general: \(J(5,3)\cong L(K_5)\) is
  \(5\)-colourable while \(J(6,3)\) is not, and \(LS(2,3,7)\) does not exist;
  likewise \(J(6,4)\cong L(K_6)\) is \(5\)-colourable while \(J(7,4)\) is not,
  and \(LS(3,4,8)\) does not exist.  They do not assert that every two-point
  restriction at every parameter is noninjective.

### Attribution

The local \(K_q\) edge-colouring device is the repository's own, from the proof
of the Odd-neighbour lift theorem (`erdos_835_conjectural_resolution.md:195–205`),
where it is used only at \(s=m-2\).  The instances \(s=2\) and \(s=3\) of G1 are
classical: \(\theta(n,3)=n-2\) for \(n\equiv1,3\pmod 6\), \(n>7\), and
\(\theta(n,3)=n-1\) for \(n\equiv0,2\pmod 6\), \(n>7\), with \(\theta(6,3)=6\)
(Lu 1983–84; Teirlinck, *JCTA* **57** (1991) 302–305; compiled in T. Etzion and
S. Bitan, *On the chromatic number, colorings, and codes of the Johnson graph*,
Discrete Appl. Math. **70** (1996) 163–175).  Our exhaustive computation
reproduces \(\theta(6,3)=6\) exactly.  A repository-wide search and a targeted
literature search found **no** statement of the general-\(s\) equivalence;
Etzion–Bitan move to recursive and computer-search constructions for
\(w\ge4\).  **This is not asserted as a priority claim** — only as "not found".

## 4. Corollaries

> **Corollary G1.1 (one-root restriction classification; *proved*, exact
> quantifiers).**  Let \(m=k+1\) be odd and suppose
> \(c:\binom Vk\to[m]\) is a proper colouring of \(J(2k,k)\).  Fix a root
> \(\infty\in V\) and form its derived/link colouring
> \[
>   \phi(A)=c(A\cup\{\infty\}),\qquad
>   A\in\binom{V\setminus\{\infty\}}{k-1}.
> \]
> For a fixed \(Y\subseteq V\setminus\{\infty\}\) of size
> \(k+1\le n\le2k-1\), restrict \(\phi\) to \(\binom Y{k-1}\), then complement
> inside \(Y\).  This is a proper \(m\)-colouring of \(J(n,s)\), where
> \(s=n-k+1\), and Theorem G1 identifies its standalone existence exactly with
> \[
>   LS(s-1,s,n+1)=LS(n-k,n-k+1,n+1),
> \]
> the derivation-tower rung \(t=n-k\).

Indeed, complementation is a Johnson-graph isomorphism and
\(n=(k+1)+(n-k+1)-2=m+s-2\), exactly the hypothesis of G1.  At \(n=2k-1\)
this returns the top rung; at \(n=2k-2\) it returns the first derived rung; and
smaller retained sets return successively lower rungs.

The quantifiers matter.  For each **fixed** root and retained set, the
standalone restriction test is equivalent to one rung.  This does not say
that an arbitrary colouring of that rung extends to the top, does not remove
simultaneous compatibility among several roots or overlapping retained sets,
and does not classify arbitrary sequences of derivations and restrictions.
Joint sub-configuration tests can therefore still be stronger.

> **Corollary G1.2 (\(k\) must be even; *proved*).**  If \(LS(k-1,k,2k)\) exists
> then \(k\) is even.
>
> *Proof.*  Restrict the induced colouring to any \(G\subseteq[2k]\) with
> \(|G|=k+2\) (possible for \(k\ge2\)).  Labelling each \(k\)-subset of \(G\) by
> the pair it omits, adjacency becomes "the omitted pairs meet", so we get a
> proper edge colouring of \(K_{k+2}\) with at most \(k+1\) colours, i.e.
> \(\chi'(K_{k+2})\le k+1\).  But \(\chi'(K_j)=j\) for odd \(j\); if \(k\) were
> odd then \(j=k+2\) is odd and \(\chi'(K_{k+2})=k+2>k+1\).  \(\square\)

This recovers a known fact (it also follows from \(n_0=0\) and from the design
indices) by a one-line argument that uses no design theory.

> **Corollary G1.3 (rung-by-rung reformulation; *proved*).**
> For every \(t\ge1\) and odd \(m\),
> \[
>   LS(t,t+1,t+m)\ \text{exists}\iff \chi\bigl(J(t+m-1,\,t+1)\bigr)\le m .
> \]
> At \(m=17\) the vertex set shrinks strictly at every rung, by exactly \(50\%\)
> at the top:

| rung \(t\) | \(LS(t,t{+}1,t{+}17)\) vertices | equivalent \(J(t{+}16,t{+}1)\) vertices | fewer |
|---|---|---|---|
| 1 | 153 | 136 | 11.1% |
| 2 | 969 | 816 | 15.8% |
| 3 | 4,845 | **3,876** | 20.0% |
| 4 | 20,349 | 15,504 | 23.8% |
| 5 | 74,613 | 54,264 | 27.3% |
| 10 | 13,037,895 | 7,726,160 | 40.7% |
| 14 | 300,540,195 | 155,117,520 | 48.4% |
| 15 | 601,080,390 | 300,540,195 | 50.0% |

**This is not a cheaper instance, and it should not be sold as one.**  Under the
natural exactly-one encoding the two formulations have *identical variable
sets*: the missing-colour map \(\psi\) is literally the colouring of the blocks
through the deleted point, so \(\psi(T)=i\) is the variable \(x_{T\cup\{p\},i}\).
What G1 removes is exactly the star constraints based at \(t\)-sets **through**
the deleted point, and what it proves is that those are **logically implied by
the rest**.  Counted exactly (*certified computational*):

| rung \(t\) | shared variables | star groups in \(LS\) | star groups in \(J(n,s)+\psi\) | proved implied |
|---|---|---|---|---|
| 2 | 16,473 | 2,907 | 2,601 | 306 |
| 3 | **82,365** | **19,380** | **16,473** | **2,907** |
| 4 | 345,933 | 101,745 | 82,365 | 19,380 |
| 15 | 10,218,366,630 | 9,617,286,240 | 5,109,183,315 | 4,508,102,925 |

So at the \(LS(3,4,20)\) rung, Theorem G1 says precisely that
\(2{,}907\) of the \(19{,}380\) star constraints — \(15.0\%\) of them, one point's
worth, and by symmetry any point's worth — are redundant.  Deleting redundant
constraints normally *hurts* a refutation search, so the practical value to the
solver track is at best neutral.  The value of the corollary is the theorem
(Corollary G1.1), not a smaller CNF, and no new CNF is shipped here.

> **Corollary G1.4 (what the colour classes are; *proved*).**  In any proper
> \(m\)-colouring of \(J(t+m-1,t+1)\) every class has exactly
> \(\binom{t+m-1}{t+1}/m\) blocks and is a **maximum packing**, and the \(m\)
> leaves \(\{\psi^{-1}(i)\}\) form the next rung down,
> \(LS(t-1,t,t+m-1)\).

Verified on genuine objects: the repository's cyclic \(LS(2,3,19)\) restricts to
seventeen maximum packings of 48 triples on 18 points whose leaves are exactly a
one-factorisation of \(K_{18}\); each of the fifteen Etzion–Hartman \(SQS(20)\)
restricts to a maximum packing of 228 quadruples on 19 points whose leave is the
derived \(STS(19)\), and adjoining the point rebuilds each system exactly.

## 5. Where the tower actually breaks (*certified computational*)

Rung \(t\Rightarrow\) rung \(t-1\), so only the **first failing rung** matters.
The two smallest admissible #835 candidates were profiled here by exhaustive
enumeration, independently reproducing their known statuses:

| \(m\) | \(k\) | rung 1 | rung 2 | rung 3 | first failure |
|---|---|---|---|---|---|
| 5 | 4 | \(LS(1,2,6)\) **exists** | \(LS(2,3,7)\) **fails** (maximum packing 2 of 5) | — (implied) | \(t=2\), the STS rung |
| 7 | 6 | \(LS(1,2,8)\) **exists** | \(LS(2,3,9)\) **exists** | \(LS(3,4,10)\) **fails** (\(D(10)=5\) of 7) | \(t=3\), the SQS rung |
| 17 | 16 | \(LS(1,2,18)\) exists | \(LS(2,3,19)\) exists | \(LS(3,4,20)\) **UNKNOWN** | UNKNOWN |

The computation independently reproduces **\(D(10)=5\)**: over all \(2{,}520\)
labelled \(SQS(10)\), the maximum number of pairwise disjoint ones is five, by
complete maximum-clique branch and bound with no time limit and no heuristic.
A five-member witness is emitted and independently re-checked from scratch,
and the value was obtained by two differently-pruned exhaustive searches.
Every labelled-system count cross-checks against its known value
\((15,30,105,840,2520)\).

This value is classical, not new.  Kramer and Mesner proved that the maximum
numbers of mutually disjoint \(S(3,4,10)\), \(S(4,5,11)\), and \(S(5,6,12)\)
are respectively \(5,2,2\): E. S. Kramer and D. M. Mesner, *Intersections
among Steiner systems*, J. Combin. Theory Ser. A **16** (1974), 273–285,
[doi:10.1016/0097-3165(74)90054-5](https://doi.org/10.1016/0097-3165(74)90054-5).
Etzion–Hartman also explicitly quote \(D(10)=5\).

Three consequences, none of them touching \(k=16\):

1. \(LS(3,4,10)\) does not exist, so by tower monotonicity **neither does
   \(LS(4,5,11)\) nor \(LS(5,6,12)\)**, and \(k=6\) is excluded from rung 3.
   The code supplies an independent reproducibility check of this classical
   lower-rung exclusion.
2. Both profiled towers fail at **the first rung not classically
   guaranteed**: for \(m=5\) the STS rung fails because \(7\) is Cayley's
   exception; for \(m=7\) the STS rung succeeds and the SQS rung fails.
3. For \(m=17\) the STS rung succeeds (\(LS(2,3,19)\) exists, by
   Lu–Teirlinck).  The SQS rung \(LS(3,4,20)\) is therefore the exact analogue
   of the rung that killed \(m=7\).

This is **evidence about where to look, not an obstruction**.  Two data points
are two data points; \(m=17\) differs from \(m=7\) in the one way that matters
here, namely that Etzion–Hartman reach \(15\) of the \(17\) required systems at
\(v=20\), whereas \(D(10)=5\) of \(7\) is far from the bound.  The honest
reading is only that the programme's concentration on \(LS(3,4,20)\) is aimed
at the right rung.

Wider context from the literature check: no **explicit construction** of a
nontrivial large set of Steiner quadruple systems \(LS(3,4,v)\) is known, while
Keevash's general theorem proves their existence nonconstructively for all
sufficiently large admissible \(v\).  See
`evidence/large_set_literature_2026-07-26.md` for the primary-source audit.
Also, \(S(4,5,21)\) is the smallest Steiner system \(S(4,5,v)\) of unknown
existence.

## 6. What this does **not** do

* It does not decide \(LS(3,4,20)\), \(LS(4,5,21)\), \(LS(14,15,31)\) or
  \(LS(15,16,32)\).
* It does not exclude \(k=16\) or any \(k>6\), and gives no radius-four verdict.
* It says nothing about the \(C_{17}\) fixed-link extension, which remains
  UNKNOWN.
* Corollary G1.1 classifies each standalone fixed-root restriction.  It does
  not dispose of joint compatibility conditions across several restrictions.
* The \(m=5,7\) tower profiles are two data points about small parameters.  They
  are not an argument that \(LS(3,4,20)\) fails.

## 7. Verification

```sh
python3 -B collaboration/opus5/generic_radius4_certificate_attack/\
verify_generic_one_point_lift.py     # Theorem G1: 51 checks

python3 -B collaboration/opus5/generic_radius4_certificate_attack/\
tower_profile.py                     # exhaustive m=5 and m=7 tower profiles
```

Standard library only, exact finite arithmetic, no solver, no randomness, no
network.  The first script checks the labelled \(s=1\) boundary at \(m=3,5\),
exhaustively round-trips every proper colouring at
\((m,s)=(3,2),(5,2),(7,2)\) up to colour permutation, confirms the two negative
predictions at \((5,3)\) and \((5,4)\), verifies both sharpness separations, and
runs the \(m=17\) instances on the repository's audited cyclic \(LS(2,3,19)\)
and on the fifteen genuine Etzion–Hartman \(SQS(20)\) (export digest asserted).
The second profiles the first failing rungs for \(m=5\) and \(m=7\) by complete
enumeration and writes `tower_profile.json` with a re-checked witness for each
maximum family.
