# First-lift sufficiency: fractional criterion and Kempe audit

Date: 2026-07-27.

## Scope and outcome

This is a follow-up to `collaboration/first_lift_support_completion/`.
It concerns only the prescribed-support edge-colouring of \(K_{13}\) in
the first unrestricted lift.  It does **not** prove universal completion,
fan realizability, the compatibility between different five-sets, or
Erdős--Rosenfeld Problem #835.

The matching-deletion inequalities have not been proved sufficient for an
integer completion.  What can be proved exactly is:

1. their arbitrary nonnegative-weight extension is necessary and sufficient
   for a **fractional** packing of the prescribed perfect matchings;
2. the original inequalities are precisely the \(0/1\)-weight subfamily;
3. exhaustive order-five computation found no gap between the \(0/1\)
   inequalities and integer completion, but this does not settle order
   thirteen;
4. a naive proposed Kempe lemma is false: an abstract incidence \(2\)-switch
   need not be realizable by one alternating-chain swap, even in the standard
   round-robin completion.  A separate exhaustive \(K_5\) control nevertheless
   found the corresponding fixed-class-size colouring space connected.

## 1. Exact fractional criterion

Let \(E=E(K_{13})\).  For each colour \(c\), let \({\cal M}_c\) be the set
of perfect matchings of \(K[V_c]\), and let
\[
 P_c=\operatorname{conv}\{{\bf 1}_M:M\in{\cal M}_c\}\subseteq\mathbb R^E.
\]
A **fractional completion** is a choice \(x_c\in P_c\) such that
\[
 \sum_c x_c={\bf 1}_E.
\tag{1}
\]

> **Theorem 1 (weighted fractional criterion).**  A fractional completion
> exists if and only if, for every nonnegative edge-weight vector
> \(w\in\mathbb R_{\ge0}^E\),
> \[
>  \sum_c\min_{M\in{\cal M}_c}w(M)
>  \ \le\ \sum_{e\in E}w_e.
> \tag{2}
> \]

### Proof

Necessity follows at once from (1):
\[
 \sum_c\min_{M\in{\cal M}_c}w(M)
 \le \sum_c w\mathbin{\cdot}x_c
 =w\mathbin{\cdot}{\bf1}_E.
\]

For sufficiency, put \(Q=\sum_cP_c\), a compact convex set.  Every point
of \(Q\) has coordinate sum
\[
 \sum_c |V_c|/2=156/2=78=|E|.
\tag{3}
\]
If \({\bf1}_E\notin Q\), strict separation supplies a real vector \(w\)
such that
\[
 \min_{z\in Q}w\mathbin{\cdot}z
 >w\mathbin{\cdot}{\bf1}_E.
\tag{4}
\]
The left side of (4) is
\(\sum_c\min_{M\in{\cal M}_c}w(M)\).  Adding the same constant \(K\) to
every coordinate of \(w\) adds \(78K\) to both sides, by (3).  We may
therefore choose \(K\) so that \(w+K{\bf1}_E\ge0\), contradicting (2).
Thus \({\bf1}_E\in Q\), which is (1). \(\square\)

This theorem is only fractional.  It does not show that
\({\bf1}_E\in\sum_cP_c\) has a representation by vertices of all the
\(P_c\)'s, which is the required integer completion.

## 2. The deletion inequalities are the binary slice

For \(F\subseteq E\), take \(w={\bf1}_F\).  For one even support \(V\),
\[
 \min_{M\text{ perfect on }V}|M\cap F|
 =
 \frac{|V|}{2}-\nu(K[V]-F).
\tag{5}
\]
The lower bound is the matching-deletion argument already recorded.  For
the reverse inequality, take a maximum matching of \(K[V]-F\).  No edge
of \(K[V]-F\) joins two unmatched vertices, or the matching could be
augmented by that edge.  Pair the even number of unmatched vertices
arbitrarily; all those new edges lie in \(F\), and (5) follows.

Consequently the previous family
\[
 \sum_c\left(|V_c|/2-\nu(K[V_c]-F)\right)\le |F|
\tag{6}
\]
is exactly (2) restricted to \(0/1\) weights.  Sufficiency of (6) would
require an additional result: first that binary weights already imply all
weighted inequalities, and then that the resulting fractional packing is
integral.  Neither implication is proved for the target family.

## 3. Exact and bounded computations

### Exhaustive order-five analogue

`exhaust_n5_capacity.py` exhausts all unordered multisets of nonempty even
supports on five vertices for which every vertex belongs to four supports.
There are \(1,194\) such multisets.  Exactly \(272\) have an integer
completion and \(922\) do not.  Every one of the \(922\) incomplete
families violates (6) for at least one of the \(2^{10}\) edge sets \(F\).

Thus the binary inequalities characterize integer completion in this
small analogue.  This is exhaustive evidence, not an induction or a
theorem for \(K_{13}\).

### Weighted target search

For a fixed integer \(w\), `search_weighted_obstruction.py` computes every
minimum perfect-matching weight exactly, then uses CP-SAT to maximize the
left side of (2) over **all** support-admissible multisets in a specified
histogram.  The logged run covered all six histograms, the uniform vector,
six two-level cut vectors, and thirty independently seeded random integer
vectors per histogram.  All \(222\) outer maximizations were certified
optimal and none violated (2).

This finite search does not quantify over all weight vectors.  It proves
only the \(222\) stated optimum bounds.

## 4. Kempe-switch route: the direct lemma fails

For two colours \(c,d\), their two matchings form disjoint alternating
paths and cycles.  Swapping one component changes colour incidence only
at the endpoints of a path.  An abstract support-matrix \(2\)-switch uses
vertices
\[
 u\in V_c\setminus V_d,\qquad v\in V_d\setminus V_c
\]
and exchanges their memberships in \(V_c,V_d\), preserving all row and
column sums.  One alternating-chain swap realizes exactly this switch only
when \(u\) and \(v\) are endpoints of the same \(c/d\) component.

`audit_kempe_switch.py` checks the standard round-robin one-factorization
of \(K_{18}\), restricted to its \(K_{13}\) hole.  Among \(1,160\)
abstract size-preserving \(2\)-switches, only \(130\) have their two
vertices in the same bichromatic component; \(1,030\) do not.  The first
certificate uses colours \(0,3\), vertices \(5,13\), and distinct
component identifiers.

Therefore the statement “every incidence \(2\)-switch is one Kempe-chain
swap” is false even for a completable target instance.  This does not rule
out a longer sequence of swaps, possibly using buffer colours.  Such a
global connectivity theorem remains a possible route, but it requires a
substantially stronger invariant-reducing argument.

There is modest positive evidence for that stronger route.
`audit_kempe_n5_connectivity.py` exhausts all \(20,880\) labelled proper
edge-colourings of \(K_5\) with colour-class sizes
\[
 (2,2,2,1,1,1,1,0,0).
\]
It joins two states when one connected bichromatic component can be swapped
without changing either labelled class size.  The resulting reconfiguration
graph is connected and contains \(14,520\) distinct labelled support
signatures.  This is an exhaustive small control, not a connectivity theorem
for \(K_{13}\).

It is also important to distinguish the required statement from known
unrestricted Kempe equivalence.  Mohar's theorem says that all
\((\chi'(G)+2)\)-edge-colourings of a simple graph are Kempe-equivalent.
Since \(\chi'(K_{13})=13\), all proper \(17\)-edge-colourings of \(K_{13}\)
are therefore Kempe-equivalent when intermediate colour-class sizes and
supports may vary.  The theorem is summarized as Theorem 1.5 in
[Bonamy--Defrain--Klimošová--Lagoutte--Narboni](https://arxiv.org/abs/2107.07900).
This cannot prove that a colouring with a prescribed support matrix exists:
Kempe equivalence only connects two colourings already known to exist, and
its sequence need not preserve the target class sizes.  The missing lemma is
a constrained descent to the prescribed incidence matrix, not ordinary
Kempe connectivity.

## 5. Relevant scheduling literature

The first lift is a balanced round-robin scheduling problem with five
pre-announced absences per player: a colour is a round and \(a\notin V_c\)
means player \(a\) is absent.  Schauz defines exactly this avoiding
edge-colouring model and notes that the general complete-graph problem
with at least two absences was still open in that framework:
[The Tournament Scheduling Problem with Absences](https://arxiv.org/abs/1509.00488).
The present instance has the extra even-attendance restriction
\(|V_c|\in\{8,10,12\}\), so it is a special balanced subcase rather than a
resolution of that broader problem.

## Conclusion

No exact target support matrix violating a deletion or weighted fractional
inequality was found, and no target support matrix was proved
non-completable.  The rigorous advance is the exact separation between:

* binary deletion capacity;
* arbitrary-weight fractional feasibility; and
* the still-unproved integer completion.

The single-chain Kempe shortcut is eliminated.  The small analogue supports,
but does not prove, a multi-step connectivity route; such a proof or an exact
adversarial counterexample search remains necessary.
