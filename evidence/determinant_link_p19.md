# The rank-two determinant link is impossible at \(p=19\)

This note closes the local two-dimensional link left open by the
\(p\equiv1\pmod4\) maximal-minor argument, at the candidate prime
\(p=19\).  The implication proved here is exactly
\[
 \text{determinant-rainbow maximal-minor rule over }\mathbb F_{19}
 \ \Longrightarrow\ \text{the ordered 20-vector link below}
 \ \Longrightarrow\ \bot.
\]
It is an **ansatz obstruction only**: it rules out a single maximal-minor
colouring of \(J(36,18)\) over \(\mathbb F_{19}\).  It does not rule out a
general \(19\)-colouring of \(J(36,18)\), and therefore does not solve
Erdos--Rosenfeld Problem #835.

## Link hypothesis

Suppose that twenty ordered nonzero vectors
\(u_0,\ldots,u_{19}\in\mathbb F_{19}^2\) have the property that, at every
vertex \(i\), the nineteen symmetric labels
\[
 \{\det(u_j,u_i):j<i\}\ \cup\ \{\det(u_i,u_j):j>i\}
\tag{1}
\]
are exactly \(\mathbb F_{19}\).  This is the necessary 16-column link for
a maximal-minor colouring, as follows.  If an \(18\times36\) matrix \(G\)
had rainbow ordered maximal minors on every 17-star, fix any sixteen
columns \(R\).  The same star argument makes \(R\) independent and all
twenty remaining quotient columns nonzero in
\(\mathbb F_{19}^{18}/\langle R\rangle\cong\mathbb F_{19}^2\).  After
absorbing the induced ordering sign into each quotient vector, the minor on
\(R\cup\{i,j\}\) is one common nonzero scalar times
\(\det(u_i,u_j)\) for \(i<j\).  Each 17-star is rainbow, which is precisely
(1).  Thus failure of this link excludes the determinant-rainbow rule.

Every vector has exactly one parallel mate: zero occurs once in (1).
Thus the vectors occupy ten projective directions, twice each.

## The first moment makes every mate exact up to sign

The sum of the labels in (1) is zero.  Set
\[
 W=\sum_{j=0}^{19}u_j,\qquad P_i=\sum_{j<i}u_j,\qquad Q_i=W-2P_i.
\]
Exactly as in the \(p=17\) link calculation,
\[
 \det(u_i,Q_i)=0,\qquad Q_{i+1}=Q_i-2u_i. \tag{2}
\]
At least one of \(Q_0,Q_1,Q_2\) is zero: otherwise (2) successively puts
\(u_0,u_1,u_2\) in one projective direction, impossible because every
direction has only two representatives.

If \(Q_r=0\) and \(r+2<20\), then \(Q_{r+1}=-2u_r\), so (2) makes
\(u_{r+1}\) the mate of \(u_r\).  If \(Q_{r+2}\ne0\), (2) would make
\(u_{r+2}\) a third vector in that direction.  Hence
\[
 Q_{r+2}=0,\qquad u_{r+1}=-u_r. \tag{3}
\]
Iterating (3) from the first zero gives the following complete boundary
check:

* if the first zero is \(Q_0\), all consecutive pairs are opposite;
* if it is \(Q_2\), the pairs \((2,3),\ldots,(18,19)\) are opposite;
  their cancellation gives \(W=u_0+u_1\), while \(Q_2=0\) gives
  \(W=2(u_0+u_1)\), hence \(u_1=-u_0\);
* if it is \(Q_1\), the pairs \((1,2),\ldots,(17,18)\) are opposite.
  Their cancellation gives \(W=u_0+u_{19}\), while \(Q_1=0\) gives
  \(W=2u_0\), hence \(u_{19}=u_0\).

In every case, each projective pair has the form \(a v,-a v\) or
\(a v,a v\).  This stronger consequence of the ordered first moment is
what handles the signs when \((p-1)/2\) is odd.

## The eighth moment reduces the link to ten slopes

There are ten unused projective directions, so an invertible linear change
of coordinates can move an unused direction to infinity.  It multiplies
every determinant by one common nonzero scalar and preserves the exact
\(\pm\)-pair property, hence preserves the link hypothesis.  Write the used
directions as distinct finite slopes \(t_e\), with their pair represented
by
\[
 a_e(1,t_e),\quad \pm a_e(1,t_e),\qquad a_e\ne0,
 \quad e=1,\ldots,10.
\tag{4}
\]
Since the eighth powers of \(\mathbb F_{19}\) sum to zero, and eight is
even, the eighth-power sum in either row from direction \(e\) is
\[
 a_e^8\sum_{f\ne e} 2a_f^8(t_f-t_e)^8=0. \tag{5}
\]
Put
\[
 F(x)=\sum_{f=1}^{10}2a_f^8(t_f-x)^8.
\]
Equation (5) gives ten distinct roots of a polynomial of degree at most
eight, so \(F=0\).  Let
\(P(X)=\prod_f(X-t_f)\).  Comparing coefficients, or using the standard
barycentric identity, now gives
\[
 2a_e^8=\frac C{P'(t_e)}\qquad(e=1,\ldots,10) \tag{6}
\]
for one nonzero \(C\).  Indeed, the nullspace of the \(9\times10\)
Vandermonde matrix \((t_e^j)_{0\le j\le8}\) is spanned by
\((1/P'(t_e))_e\).

The image of \(x\mapsto x^8\) in \(\mathbb F_{19}^\times\) is exactly the
quadratic residues, because \(\gcd(8,18)=2\).  Thus (6) requires the ten
values \(P'(t_e)\) to have one common quadratic character.  This is already
impossible without a search: writing \(T=\{t_1,\ldots,t_{10}\}\),
\[
 \prod_{e=1}^{10}P'(t_e)
 =(-1)^{\binom{10}{2}}
   \prod_{1\le e<f\le10}(t_e-t_f)^2. \tag{7}
\]
The right side is minus a nonzero square in \(\mathbb F_{19}\), so its
quadratic character is \(-1\).  But ten equal characters have product
\(+1\), a contradiction.  Therefore (6) is impossible, and so is the
original ordered determinant link.

The same proof works for every prime \(p>3\) with \(p\equiv3\pmod8\): use
the even exponent \((p-3)/2\), and note that
\(\binom{(p+1)/2}{2}\) is odd.  The already established argument covers
\(p\equiv1\pmod4\).  This leaves the \(p\equiv7\pmod8\) determinant-link
case open; no claim about it is made here.

## Independent exact check

The dependency-free verifier
[`verify_determinant_link_p19.py`](verify_determinant_link_p19.py) exhausts
the \(\binom{19}{10}=92{,}378\) slope sets as an independent check of (7),
and also confirms that none has constant derivative character.  The proof
above does not rely on that enumeration.

Run:

```bash
python3 -B evidence/verify_determinant_link_p19.py
```

The verifier also checks a genuine \(p=3\) link.  Accordingly, this is not
a claim that rank-two determinant links fail for every prime; it is a
rigorous \(p=19\) obstruction with its scope stated above.
