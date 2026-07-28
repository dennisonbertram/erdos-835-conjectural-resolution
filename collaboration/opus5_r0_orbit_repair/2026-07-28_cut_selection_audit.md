# Audit of the Opus 5 cut-selection follow-up

Date: 2026-07-28.

## Verdict

The run proves one rigid branch of the cut-feasible repair-selection lemma.
It does not prove the full lemma.  Its claimed \(|A_U|=6\) branch contains
several compressed overlap inequalities without derivations and is not
promoted to a theorem here.

For a cut \(U\), write
\[
A_U=\{R:\ R\subseteq V\setminus U\}.
\]
The valid new result treats a six-set with \(e(G[U])=2\) and
\(|A_U|=7\): all seven remaining triple rows lie in the complementary
seven-set.

## Rigid all-seven-rows repair theorem

Let \(|U|=6\), \(W=V\setminus U\), \(e(D[U])=13\), and suppose all seven
remaining triple rows lie in \(W\).

The remaining-row incidence outside \(U\) is
\[
\sum_{w\in W}\rho(w)=41+6-2e(D[U])-e_D(U,W)=21-e_D(U,W).
\]
The seven triple rows already contribute 21, so
\[
e_D(U,W)=0.
\]
All four remaining five-set rows therefore lie in \(U\).  Since
\(|D|=27\),
\[
e(D[W])=14.
\]
Equivalently, before repair,
\[
e(G[U])=2,\qquad e(G[W])=7,
\]
and all 42 crossing edges belong to \(G\).

Every size-five prefix layer splits into internal matching edges on \(U\)
and on \(W\).  It has five edges in total, while a matching has at most three
edges on either side.  Hence it has at least two on each side.  Choose
\[
u_1u_2\in M[U],\qquad w_1w_2\in M[W]
\]
and replace them by
\[
u_1w_1,\qquad u_2w_2.
\]
The new edges were not in any prefix layer because \(D\) had no crossing
edge.  Thus this is a legal support-preserving repair.  It preserves every
vertex degree and every row, and changes the residual counts to
\[
e(G'[U])=3,\qquad e(G'[W])=8,
\]
with exactly two unavailable crossing edges.

For any \(X\subseteq V\), put
\[
p=|X\cap U|,\qquad q=|X\cap W|.
\]
The residual graph has at least
\[
\max(0,pq-2)+3\,\mathbf1_{p=6}+8\,\mathbf1_{q=7}
\]
edges inside \(X\).  Since every selected triple row is contained in \(W\),
its smallest possible intersection with a \(q\)-subset of \(W\) is
\(\max(0,q-4)\).  Therefore the demand of any three rows is at most
\[
3\max\{0,p+q-5-\max(0,q-4)\}.
\]
Direct arithmetic for all 20 possible \((p,q)\) types with
\(p+q\in\{6,7,8\}\) proves that the edge lower bound dominates the demand.
Other cut sizes are automatic.  The verifier
`verify_rigid_cut_repair_arithmetic.py` checks all 20 inequalities.

The response unnecessarily asserted that the two missing edges of \(D[U]\)
are disjoint.  The repair and the cut proof do not need that assertion, so it
is omitted.

## Useful single-cut classification

The small-cut reduction is correct.  Under individual and pairwise
compatibility, a six-set can create a genuinely three-way violation only
when \(e(G[U])=2\), in which case all three selected rows lie in \(A_U\).

For seven-sets:

- when \(e(G[U])=4\), violations have either three rows in \(A_U\), or two
  in \(A_U\) and a third meeting \(U\) once;
- when \(e(G[U])=5\), only three rows in \(A_U\) violate.

For eight-sets, only three rows contained in the complementary five-set
violate.  The class-B row budget gives respectively
\[
|A_U|\le4,\quad |A_U|\le5,\quad |A_U|\le3.
\]
There is at most one tight eight-set: two distinct saturated eight-sets
would put a degree-five vertex into a separated five-set, where its degree is
at most four.

These facts narrow the covering problem but do not solve simultaneous
avoidance of all cuts.

## Unaccepted \(|A_U|=6\) branch

The response states, without complete derivations, overlap bounds such as
\[
3|A_{U_1}\cap A_{U_2}|\le(|U_1\cap U_2|-1)^2,
\]
several uniqueness claims for dense six- and seven-set partners, and a final
covering reduction to unions of \(K_4\)'s and \(K_3\)'s.  Those statements
are exactly where the claimed no-repair theorem for \(|A_U|=6\) rests.
They require an independent proof or exhaustive certificate before use.

The honest residual obligation is therefore broader than the run states:
prove or refute the cut-feasible repair-selection lemma outside the rigid
\(|A_U|=7\) branch.  The semantic-witness CEGIS searches this full residual
space without assuming the unverified overlap catalogue.
