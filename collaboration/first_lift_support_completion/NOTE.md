# The first unrestricted lift: support, partial, and fan tiers

Date: 2026-07-27.

## Scope

This note concerns only the first local lift in the \(k=16\) case of
Erdős--Rosenfeld Problem #835.  It does **not** construct a simultaneous
\(13\)-fan, prove that every first-lift instance completes, impose the
six-set compatibility between different five-sets, or solve #835.

Fix one five-set \(P\subset U\).  The established tower reduction asks for
a proper edge-colouring of \(K_A\cong K_{13}\) with colour palette
\({\cal C}\), \(|{\cal C}|=17\), such that colour \(c\) is a perfect matching
on its prescribed support
\[
 V_c=\{a\in A:c\notin S_a(P)\}.
\tag{1}
\]
Every vertex belongs to twelve supports, and every support has size
\(8,10\), or \(12\).

## 1. Three distinct instance classes

It is important not to identify the following nested classes.

1. A **support-admissible** instance is a family
   \((V_c:c\in{\cal C})\) with
   \[
   |V_c|\in\{8,10,12\},\qquad
   \#\{c:a\in V_c\}=12\quad(a\in A).
   \tag{2}
   \]
2. A **partial-factorization-realizable** instance is the support family
   left on \(A\) by some proper \(17\)-edge-colouring of
   \(K_{18}-K_{13}\), with all five vertices outside \(A\) saturated.
3. A **fan-realizable** instance is produced at \(P\) by an actual
   simultaneous \(13\)-fan through the formula (1).

Thus
\[
 \{\hbox{fan-realizable}\}
 \subseteq
 \{\hbox{partial-factorization-realizable}\}
 \subseteq
 \{\hbox{support-admissible}\}.
\tag{3}
\]
No converse in (3) is proved here.

For fan-realizable instances, write
\[
 t_c=\#\{T\in\binom P3:L(T)=c\}.
\]
Then \(|V_c|=8+2t_c\), \(t_c\in\{0,1,2\}\), and
\(\sum_c t_c=10\).  If \(q=\#\{c:t_c=2\}\), the complete support-size
histogram is therefore
\[
 (n_8,n_{10},n_{12})=(7+q,\ 10-2q,\ q),
 \qquad 0\le q\le5.
\tag{4}
\]
Every support-admissible instance has one of the same six histograms, since
summing (2) gives \(\sum_c|V_c|=13\cdot12=156\).

Partial-factorization realizability has an exact support-only formulation.
Let
\[
 {\cal B}=\{(a,c):a\notin V_c\}
\tag{5}
\]
be the missing-incidence bipartite graph between \(A\) and \({\cal C}\).
Every \(a\) has degree five, while a colour has degree \(5,3\), or \(1\).
The instance is partial-factorization-realizable if and only if:

* the edges of \({\cal B}\) can be properly coloured by the five points of
  \(P\), using every point once at every \(a\); and
* for each \(c\), the points of \(P\) not used at \(c\) can be paired into
  a matching \(N_c\), with the seventeen \(N_c\)'s partitioning
  \(E(K_P)\).

Indeed, the first item colours the \(P\)-to-\(A\) edges, and the second
colours the internal \(K_P\) edges.  At every pair \((p,c)\), exactly one
of these two items is incident, so each \(p\) is saturated in all seventeen
colours.  The construction is plainly reversible.

The first item by itself is automatic: \({\cal B}\) is bipartite with
maximum degree five, so Kőnig's line-colouring theorem gives a proper
five-edge-colouring, and degree five at every \(a\) forces all five labels
there.  This isolates the only support-to-partial compatibility issue.
For any such line-colouring, every label \(p\in P\) is used on thirteen
edges and hence is unused at four colour vertices.  Pairing the unused
labels at every \(c\) therefore produces a \(4\)-regular multigraph with
ten edges on \(P\).  Partial-factorization realizability asks whether the
line-colouring and pairings can be chosen so that this multigraph is simple,
in which case it is exactly \(K_5\).

## 2. A matching-capacity obstruction

Parity of every \(|V_c|\) is necessary but is not the whole matching-packing
problem.  The following family of inequalities is valid for every edge set,
not merely a vertex cut.

> **Theorem 1 (matching-deletion capacity).**  If perfect matchings
> \(M_c\) on the supports \(V_c\) partition \(E(K_A)\), then for every
> \(F\subseteq E(K_A)\),
> \[
> \sum_{c\in{\cal C}}
> \left(
>   \frac{|V_c|}{2}
>   -\nu\bigl(K_A[V_c]-F\bigr)
> \right)
> \le |F|,
> \tag{6}
> \]
> where \(\nu(G)\) denotes the maximum matching size of \(G\).

### Proof

The edges of \(M_c\) outside \(F\) form a matching in
\(K_A[V_c]-F\).  Hence
\[
 |M_c\cap F|
 =\frac{|V_c|}{2}-|M_c\setminus F|
 \ge
 \frac{|V_c|}{2}-\nu(K_A[V_c]-F).
\]
The matchings \(M_c\) are edge-disjoint, so their intersections with \(F\)
are edge-disjoint subsets of \(F\).  Summing proves (6).
\(\square\)

The theorem is a necessary condition, not a claimed characterization.  It
is also not proved here that (2), partial-factorization realizability, or
fan realizability makes every inequality (6) automatic.

### The ordinary cut test is automatically passed

Take \(F=\delta(X)\), the cut of \(X\subseteq A\).  If
\(r_c=|V_c\cap X|\), then
\[
 \frac{|V_c|}{2}-\nu(K_A[V_c]-\delta(X))
 =
 \begin{cases}
 1,&r_c\text{ odd},\\
 0,&r_c\text{ even}.
 \end{cases}
\]
Thus (6) becomes
\[
 o(X):=\#\{c:r_c\text{ is odd}\}\le |X|(13-|X|).
\tag{7}
\]
For every support-admissible target instance, (7) is automatic.  If
\(2\le|X|\le11\), its right side is at least \(22>17\).  For
\(|X|=1\), exactly twelve supports contain the point, so both sides are
\(12\).  For \(|X|=12\), even support sizes imply that \(r_c\) is odd
exactly when the omitted point belongs to \(V_c\), again giving \(12\).
The cases \(|X|=0,13\) are zero.

Consequently a successful obstruction from Theorem 1 must use more structure
than one ordinary cut.

### Parity is genuinely insufficient in the general degree-matrix problem

The failure does occur outside the target support range.  On five vertices,
take nine colour supports
\[
\begin{array}{c|c}
0,1&\{0,1\}\\
2&\{0,2,3,4\}\\
3&\{1,2,3,4\}\\
4&\{0,2\}\\
5&\{1,3\}\\
6&\{2,4\}\\
7&\{3,4\}\\
8&\varnothing.
\end{array}
\tag{8}
\]
Every support is even and every vertex belongs to four supports, exactly
the degree of \(K_5\).  Nevertheless colours \(0\) and \(1\) both force
the single edge \(01\).  Equivalently, (6) with \(F=\{01\}\) has left side
at least \(2>|F|=1\).  This is a solver-free certificate that parity,
correct row totals, and individual graphicality do not characterize
coloured degree-matrix realizability in general.  It is **not** a
\(K_{13}\) or fan-realizable counterexample.

## 3. Exact computations and their limits

The accompanying CP-SAT searches deliberately sample two different
overapproximations.

* `search_support_instances.py` generates arbitrary support-admissible
  matrices across all six histograms (4), then independently solves both
  the \(K_{13}\) completion and, optionally, the five-saturated-vertex
  partial realization.
* `search_partial_factorizations.py` first constructs a proper colouring of
  \(K_{18}-K_{13}\) without taking it from a known full one-factorization,
  then independently solves its \(K_{13}\) hole.
* `search_capacity_obstruction.py` fixes \(F\), computes the exact matching
  deficiencies in (6), and optimizes their sum over all
  support-admissible matrices of a selected histogram.

The logged deterministic runs found:

* \(2,978\) completed arbitrary support-admissible samples; another \(22\)
  support-generation optimizations timed out and were not tested;
* \(300/300\) arbitrary samples that both completed and were
  partial-factorization-realizable;
* \(1,000/1,000\) independently generated proper
  \(K_{18}-K_{13}\) partial colourings whose \(K_{13}\) holes completed;
* no violation of (6) in \(24/24\) solver-certified optimal cases covering
  four structured edge sets and all six histograms; a further \(72\)
  bounded clique cases found none, and the one-vertex cut was tight.

These are reproducible finite experiments, not exhaustive searches.  A SAT
sample proves only that one sampled instance completes.  Failure to find an
UNSAT sample proves neither universal completion nor anything about
fan-realizable supports.

## 4. Literature delimiter

The completion is naturally a coloured-degree-matrix or symmetric-Latin
completion problem, but the nearby exact theorems located in the literature
do not have the required prescribed-cross-edge hypotheses.

* The general edge-disjoint degree-sequence realization problem is known to
  be NP-complete even with three colour rows whose vertex degrees sum to
  \(n-1\).  That result does not decide this special dense \(0/1\) family:
  [Bérczi--Király--Liu--Miklós (2019)](https://doi.org/10.31449/inf.v43i1.2675).
* Bryant and Rodger characterize completion when colours incident with
  **two** vertices are prescribed, not five:
  [J. Aust. Math. Soc. 76 (2004)](https://doi.org/10.1017/S1446788700008739).
* Henderson and Hilton characterize a precoloured \(K_r\) together with
  independent precoloured edges, not the complete \(K_{5,13}\) cross part:
  [J. London Math. Soc. 70 (2004)](https://doi.org/10.1112/S0024610704005526).
* The Andersen--Hoffman equitable-rectangle theorem prescribes a top-left
  symmetric subarray; it does not prescribe five complete rows of cross
  entries:
  [Bahmanian--Johnsen-Yu (2026)](https://arxiv.org/abs/2606.28634).

Therefore none of these results currently closes the first lift.  The
rigorous new frontier is:

1. prove (6), or a stronger exact-cover condition, automatically from the
   partial-factorization/fan tier; or
2. find a support-admissible violation and then test the two stronger
   realizability tiers; or
3. prove universal completion directly for all five-saturated partial
   colourings.

## 5. Verification

Run:

```sh
python3 -B \
  collaboration/first_lift_support_completion/verify_capacity_lemma.py
```

The verifier is deterministic and standard-library-only.  It checks the six
histograms (4), the exact small counterexample (8), all ordinary cuts for a
target round-robin control, and the matching-capacity inequality on a
deterministic family of non-cut edge sets for that completed control.
