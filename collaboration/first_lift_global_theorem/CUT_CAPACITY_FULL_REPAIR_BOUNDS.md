# Cut-capacity lower bounds for full prefix repair

Date: 2026-07-28.

## General theorem

Let \(S_1,\ldots,S_q\) be even supports in \(V(K_n)\), and suppose a full
completion would partition \(E(K_n)\) into perfect matchings on those
supports.  Let \(P\subseteq\{1,\ldots,q\}\) be a selected prefix with
prescribed matchings \(M_i\) on \(S_i\), \(i\in P\).  A selected layer is
**retained** if the completion uses exactly \(M_i\), and **changed**
otherwise.

Fix a nontrivial cut \(\delta(X)\).  Write
\[
 d_X=|X|(n-|X|),\qquad
 u_i(X)=\min\bigl(|S_i\cap X|,\ |S_i\setminus X|\bigr),
\]
and, for \(i\in P\),
\[
 a_i(X)=|M_i\cap\delta(X)|,\qquad
 g_i(X)=u_i(X)-a_i(X).
\]
Let \(R=\{1,\ldots,q\}\setminus P\), and define the cut deficit with the
entire prefix retained by
\[
 D_X=d_X-\sum_{j\in R}u_j(X)-\sum_{i\in P}a_i(X). \tag{1}
\]
Order the selected gains as
\[
 g_{(1)}(X)\ge\cdots\ge g_{(|P|)}(X).
\]
Then every full completion changes at least
\[
 k_X=\min\left\{
   k:\sum_{\ell=1}^{k}g_{(\ell)}(X)\ge\max(D_X,0)
 \right\} \tag{2}
\]
selected layers.  Equivalently, at most \(|P|-k_X\) selected layers can
remain fixed.  If the set in (2) is empty, the support system itself has
no full completion.

### Proof

A perfect matching on \(S_i\) uses at most \(u_i(X)\) cut edges: every
crossing edge consumes one vertex on each side of the cut.  A retained
selected layer contributes exactly \(a_i(X)\).  Therefore, if
\(T\subseteq P\) is the set of changed layers, a necessary condition for
covering all \(d_X\) edges of \(\delta(X)\) is
\[
 \sum_{i\in P}a_i(X)
 +\sum_{i\in T}g_i(X)
 +\sum_{j\in R}u_j(X)
 \ge d_X. \tag{3}
\]
Thus the gains of the changed layers must sum to at least \(D_X\).  Among
all sets of \(k\) changed layers, the largest possible gain is the sum of
the \(k\) largest \(g_i(X)\).  Formula (2) follows.  This also proves that
\(k_X\) is the exact lower bound obtainable from this single cut and
these per-layer capacities.  \(\square\)

Taking \(\max_X k_X\) gives the strongest one-cut capacity lower bound.
This is a necessary condition, not in general a sufficient condition for
a repair.

## The \(r=1\) dead prefix

For the certificate in `R1_DEAD_SEVEN_PREFIX.md`, take
\[
 X=C=\{0,\ldots,5\}.
\]
The cut has demand \(6\cdot7=42\).  The seven selected matchings use no
cut edge.  The ten remaining supports have total capacity
\[
 6\cdot4+1+1+2+2=30.
\]
The selected-layer gains, in decreasing order, are
\[
 6,4,4,4,4,4,4.
\]
Hence \(D_X=12\), while the two largest gains sum to \(10\) and the three
largest sum to \(14\).  At least three selected layers must change.

Exhaustion of all \(2^{12}-1=4095\) unordered nontrivial cuts shows that
\[
 \max_X k_X=3.
\]
The canonical maximizing sides are \(\{0,\ldots,5\}\) and
\(\{0,\ldots,6\}\).  Thus three is the exact strongest one-cut lower
bound.  The separate explicit three-layer completion in
`R1_MINIMUM_FULL_REPAIR.md` makes the actual repair distance three as
well.

## The \(r=3\), \(C\subset G\), dead prefix

For the `C_in_G` certificate in `R3_DEAD_SEVEN_PREFIXES.md`, take
\[
 X=U=\{0,\ldots,6\}.
\]
Again \(d_X=42\).  The selected cut counts and capacities are
\[
 (a_i)=(0,0,0,0,0,1,1),\qquad
 (u_i)=(2,2,2,2,4,5,5).
\]
The ten remaining capacities are
\[
 (2,2,2,2,2,2,3,3,3,5),
\]
with sum \(26\).  Therefore \(D_X=42-26-2=14\), and the decreasing gains
are
\[
 4,4,4,2,2,2,2.
\]
Three changes recover at most \(12\), whereas four recover \(14\).
Consequently every full repair changes at least four selected layers.

The same 4095-cut exhaustion gives
\[
 \max_X k_X=4,
\]
with \(U\) the unique canonical maximizing side.  Four is therefore the
exact strongest one-cut lower bound for this certificate.

## The \(r=3\), \(D\subset G\), dead prefix

For the `D_in_G` certificate, use the same \(X=U\).  All seven selected
matchings have zero crossing count.  Their decreasing capacities, hence
gains, are
\[
 6,6,4,2,2,2,2.
\]
The remaining capacities are
\[
 (2,2,2,2,2,3,4,3,3,5),
\]
with sum \(28\).  Thus \(D_X=42-28=14\).  Two changes recover at most
\(12\), while three recover \(16\), so at least three selected layers
must change.

Exhausting all cuts gives
\[
 \max_X k_X=3.
\]
The canonical maximizing sides are \(U\) and \(U\cup\{10\}\).  Three is
the exact strongest one-cut lower bound for this certificate.

## Verification and scope

`verify_cut_capacity_full_repair_bounds.py` reconstructs all three
committed prefix certificates, verifies the displayed cut data, and
enumerates every unordered nontrivial cut without an optimizer.  It
checks both the maxima and all maximizing cut sides.

The theorem applies to any proposed support-perfect-matching
decomposition of a complete graph.  Its three numerical applications
are certificate-specific repair lower bounds.  They do not prove a
universal switching theorem or resolve Erdős--Rosenfeld Problem #835.
