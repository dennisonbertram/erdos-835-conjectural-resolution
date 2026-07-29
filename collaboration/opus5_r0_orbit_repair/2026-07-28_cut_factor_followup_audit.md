# Audit of the Opus 5 factor and colouring follow-up

Date: 2026-07-28.

## Verdict

The follow-up does not prove factor existence, prescribed
three-edge-colourability, cut sufficiency, or coordinated nine at \(r=0\).
It contributes one valid reformulation, two valid necessary colouring laws,
and an independently verified tightness certificate.  A proposed
independence-number lemma is false, so none of the case eliminations that use
it are retained.

## The valid \(b\)-Hall slice

For the three selected triple rows put
\[
t(v)=\#\{i:v\in R_i\},\qquad b(v)=3-t(v).
\]
Then \(b(V)=30\), and for every \(X\subseteq V\)
\[
b(X)-b(V\setminus X)=6|X|-30-2\sum_i|R_i\cap X|.
\]
Consequently the elementary degree-capacity condition
\[
b(X)\le b(V\setminus X)+2e(G[X])
\]
is
\[
e(G[X])\ge
\sum_i\bigl(|X|-5-|R_i\cap X|\bigr).
\]
Whenever all three summands are positive, this is exactly the capacity cut
(C).  In general (C), which takes the positive part term by term, is at least
as strong as this elementary slice.

This does not prove a \(b\)-factor.  The full Tutte--Lovász criterion has
additional disjoint-set and odd-component terms, and the Opus run did not
eliminate them.

## Valid colouring obstructions

If a degree-constrained union \(H\) is the union of the three required
matchings, then every component \(C\) satisfies
\[
|C\cap S_i|\equiv0\pmod2
\quad(i=1,2,3).
\]
This is immediate because colour \(i\) is a matching covering exactly the
vertices of \(S_i\).

Equivalently encode the three edge colours as the nonzero elements of
\(\mathbb F_2^2\).  The prescribed missing colours determine a vertex sum
\(\sigma(v)\).  Summing within one side \(A\) of a bridge \(e\) gives
\[
\varphi(e)=\sum_{v\in A}\sigma(v),
\]
which must be nonzero.  These are necessary laws only; they do not show that
an admissible \(H\) exists or can be selected to satisfy them.

## Independently verified tightness certificate

The explicit six-prefix and eleven rows in
`verify_factor_tightness_certificate.py` satisfy every class-B equation.
For the three selected rows, exactly one of all \(2^{13}\) capacity cuts
fails:
\[
U=\{6,7,8,9,10,11\},\qquad
3>e(G[U])=2.
\]
The corresponding degree demand is
\[
b(U)=18>b(V\setminus U)+2e(G[U])=12+4,
\]
so even the underlying degree-constrained union is impossible.  The first
selected support nevertheless has an explicit individual perfect matching.

Thus the six-set cuts are genuinely load-bearing after the full row
inventory is imposed.  The example misses the target hypothesis by exactly
one residual edge and is not a counterexample to cut sufficiency.

## Rejected claims

The claimed theorem \(\alpha(G)\le5\) is false.  A \(K_6\) in \(D\) is
compatible with a valid six-prefix: the repository already contains audited
saturated-\(K_6\) prefix certificates and a support-preserving switch theorem
for them.  The response's assertion that a sixth prefix matching would have
to lie wholly on the other seven vertices does not follow; all six layers may
contribute edges inside the \(K_6\) while also matching vertices outside it.

Therefore the component bounds and the claimed unconditional
\(|S|\le3\) portion of the subsequent factor case analysis are not accepted
without a new proof independent of that false lemma.  The asserted
repeated-row density bound and 2-connectivity conclusion were also not
derived in the response and are not used.

The honest remaining factor gap is the full Tutte--Lovász condition beyond
the elementary \(b\)-Hall slice.  Even if that is closed, a separate
selection or switching argument is required to obtain a degree-constrained
union with the prescribed three-edge-colouring.
