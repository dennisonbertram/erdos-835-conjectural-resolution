# Distance-regular and triangle-monodromy audit

This note isolates one exact consequence of a hypothetical cover

\[
 \pi:O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}\qquad(k\text{ even}),
\]

and records why the standard classification literature on *antipodal*
distance-regular covers does not apply.  The calculation is checked by
`python3 evidence/verify_distance_regular_cover_audit.py`.

It is a constraint, not an obstruction: it does not resolve
Erdos--Rosenfeld Problem #835.

## 1. Exact triangle factorisation

Let \(C_a=\pi^{-1}(a)\).  For distinct colours \(a,b\), let
\(m_{ab}:C_a\to C_b\) be the matching induced by the cover.  For ordered
pairwise distinct \(a,b,c\), set

\[
 \tau_{abc}=m_{ca}m_{bc}m_{ab}:C_a\longrightarrow C_a.
\]

For a fibre \(C_a\), let \(R_1^a\) be the zero-one matrix indexed by
\(C_a\), with an entry \((A,D)\) precisely when \(|A\cap D|=1\).  (For
\(k>2\), this is the distance-three relation of the Odd graph.)  Then

\[
 \boxed{\quad
 \sum_{\substack{b,c\ne a\\b\ne c}}P_{\tau_{abc}}=2R_1^a.\quad} \tag{1}
\]

Here \(P_\sigma\) is the permutation matrix of \(\sigma\).

**Proof.**  Write \(X\) for the \((2k-1)\)-set.  A three-edge lift from
\(A\in C_a\) through colours \(b,c,a\) has the form

\[
 A\xrightarrow{x}\overline A\setminus\{x\}
 \xrightarrow{y}(A\setminus\{y\})\cup\{x\}
 \xrightarrow{z}(\overline A\setminus\{x,z\})\cup\{y\},
\]

where bars are complements in \(X\).  Local bijectivity forces
\(y\in A\), \(x,z\notin A\), and \(x\ne z\): otherwise the second or
third vertex would repeat the colour of the preceding endpoint.  Thus the
endpoint has intersection exactly \(\{y\}\) with \(A\).

Conversely, if \(D\in C_a\) and \(|A\cap D|=1\), then
\(X\setminus(A\cup D)=\{x,z\}\).  Choosing which of these two points is
the first missing label gives exactly two three-edge paths from \(A\) to
\(D\).  Along either path the two intermediate colours are distinct and
different from \(a\), by local bijectivity.  They determine one summand of
the left side of (1); conversely a summand determines its unique lift.
This gives coefficient two at every such \((A,D)\), and zero elsewhere.
\(\square\)

Taking row sums in (1) gives the forced internal valency

\[
 |\{D\in C_a:|A\cap D|=1\}|=\frac{k(k-1)}2. \tag{2}
\]

The same number follows from the Bose--Mesner calculation.  The relation
\(|A\cap D|=i\) has valency

\[
 v_i={k-1\choose i}{k\choose i+1}
\]

and eigenvalue \(\eta_i=(-1)^{i+1}{k-1\choose i}\) on the \(-1\)
eigenspace.  Since a colour indicator has only its constant component and
that eigenspace, its same-colour relation-\(i\) count is

\[
 a_i=\frac{v_i+k\eta_i}{k+1}.
\]

At \(i=1\), this is (2).  Thus (1) adds a labelled factorisation of a
pairwise count, but no new scalar count.

## 2. Controls

The verifier checks all displayed arithmetic for \(k=2,4,6,16\).

* At \(k=2\), \(O_2=K_3\) and the identity is an actual cover.  The two
  oriented base triangles both have identity monodromy on a singleton fibre,
  so (1) is exactly \(2I=2I\).
* At \(k=4\), the seven Fano lines are a 1-perfect code in \(O_4\).  Its
  intersection-one graph is \(K_7\), of degree \(6=k(k-1)/2\).
* At \(k=6\), the 66 hexads through a fixed point of the exact
  Carmichael/PSL(2,11) model of \(W_{12}=S(5,6,12)\), with that point
  deleted, form a 1-perfect code in \(O_6\).  Its intersection-one degree
  is \(15=k(k-1)/2\).

The last two are **single perfect-code controls**, not covers of \(K_5\)
or \(K_7\); indeed the known small cases have no required full partition.
They show that neither the internal relation degree nor its local
distance-regular interpretation is the missing obstruction.

## 3. Why distance-regular-cover classifications do not decide this

The term “distance-regular cover of a complete graph” is often used in the
more restrictive DRACKN sense: an **antipodal** distance-regular graph whose
antipodal quotient is complete.  The classification results for that class
therefore assume antipodal fibres (and frequently further arc-transitivity or
abelian hypotheses).  A cover map from a distance-regular graph need not
have that property.  The cycle \(C_9\), with colours repeated \(0,1,2\),
is a locally bijective cover \(C_9\to K_3\) and is distance-regular, but
its three colour fibres are not antipodal classes.

Consequently no theorem about antipodal covers can be applied to a proposed
\(O_k\to K_{k+1}\) without first proving that its colour fibres are
antipodal.  In fact, for \(k\ge6\), (2) puts pairs at distance three in
one fibre while \(\operatorname{diam}(O_k)=k-1>3\).  At the exceptional
parameter \(k=4\), the full distance-three sphere has valency
\(v_1=18\), whereas (2) gives only six same-fibre vertices; it is not the
antipodal relation either.  Thus the colour fibres are specified by the
cover, not by a maximum-distance equivalence.

The unrestricted triple and colour-reduced Terwilliger feasibility witness
at \(k=16\), recorded separately in
`evidence/four_point_terwilliger_exact_witness.md`, also means that the
ordinary association-scheme and colour-symmetrised triple constraints cannot
be promoted to a nonexistence proof.  A useful continuation would have to
use the simultaneous, labelled factorisation in (1), or higher joint
monodromy/Hodge constraints; the scalar distance-regular data close exactly.
