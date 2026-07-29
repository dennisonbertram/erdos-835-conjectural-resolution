# The second-moment parity identity at \(r=15\) is tautological

## Scope

This note audits the combined count \(E_3+X_3\) from the endpoint-parity
approach to Erdős--Rosenfeld Problem #835.  It proves that, for two genuine
mates \(B,C\) of a fixed \(S(r-1,r,2r+1)\), the second-moment calculation at
\(r=15\) gives
\[
E_3+X_3\equiv t\pmod 2,
\]
where \(t=\#\{P:w_B(P)\ne w_C(P)\}\).  Thus proving the combined count even
would still prove the desired endpoint parity, but the displayed
second-moment identity itself is only an equivalent restatement: it does not
force the parity.

This does not rule out a separate integral involution or another global
argument proving \(E_3+X_3\) even.

## Setup

Put \(v=2r+1\), and let \(\mathcal H=\binom{[v]}{r+1}\).  For a mate \(B\),
write
\[
H_B(P)=P\cup\{w_B(P)\}\in\mathcal H
\]
for every block \(P\) of the fixed \(S(r-1,r,v)\), and let
\(x_B\in\{0,1\}^{\mathcal H}\) be the incidence vector of these \(H\)-sets.
Every \((r+3)\)-set contains exactly
\[
\mu=\frac{r+3}{2}
\]
members of this tiling.

Let \(N\) be the inclusion matrix whose rows are the \((r+3)\)-sets and
whose columns are the \((r+1)\)-sets:
\[
N_{Y,H}=[H\subseteq Y].
\]
Let \(A_i\) be the relation matrix on \(\mathcal H\) defined by
\[
(A_i)_{H,K}=[\,|H\cap K|=r+1-i\,].
\]

## Incidence identity

For two \((r+1)\)-sets \(H,K\), the \((H,K)\)-entry of \(N^\mathsf TN\)
is the number of \((r+3)\)-sets containing \(H\cup K\).  There are only
three nonzero cases:

\[
N^\mathsf TN
=\binom r2 I+(r-1)A_1+A_2
\qquad\text{over the integers.}
\]

Indeed:

- if \(H=K\), choose the two new points in \(\binom r2\) ways;
- if \(|H\cap K|=r\), choose one new point in \(r-1\) ways;
- if \(|H\cap K|=r-1\), their union already has size \(r+3\), giving
  one choice;
- smaller intersections give a union larger than \(r+3\).

For odd \(r\), reduction modulo \(2\) therefore gives
\[
A_2=N^\mathsf TN+\binom r2 I. \tag{1}
\]

For genuine tilings \(x=x_B\), \(y=x_C\), the constant containment law
is
\[
Nx=Ny=\mu\mathbf1.
\]
Consequently (1) gives
\[
x^\mathsf TA_2y
\equiv
\mu^2\binom{2r+1}{r+3}
+\binom r2\,x^\mathsf Ty
\pmod2. \tag{2}
\]

The left side of (2) is the second-moment count \(M_2\).  Its exact
decomposition has only even nonexceptional terms, so
\[
M_2\equiv E_3+X_3\pmod2. \tag{3}
\]

Also \(x^\mathsf Ty=h\), the number of common \(H\)-sets.  Equality
\(H_B(P)=H_C(Q)\) forces \(P=Q\): two distinct blocks of an
\(S(r-1,r,v)\) cannot lie in one \((r+1)\)-set because they would meet
in \(r-1\) points.  Hence
\[
h=\#\{P:w_B(P)=w_C(P)\}=b-t, \qquad
b=\frac1r\binom{2r+1}{r-1}. \tag{4}
\]

Combining (2)--(4),
\[
E_3+X_3
\equiv
\mu^2\binom{2r+1}{r+3}
+\binom r2(b-t)
\pmod2. \tag{5}
\]

## Parameter consequences

If \(r\equiv1\pmod4\), both \(\mu=(r+3)/2\) and \(\binom r2\) are even.
Thus (5) forces \(E_3+X_3\) even for genuine tilings.  This explains
the observed \(r=5\) true-tiling census.  It is not, by itself, a proof
of the stronger cancellation on every point of the particular
\(\mathbb F_2\)-affine relaxation; that is separately verified by
`verify_linear_relaxation_nogo.py`.

At \(r=15\),
\[
\mu=9,\qquad \binom{15}{2}=105.
\]
Since \(31=2^5-1\), Lucas's theorem makes every \(\binom{31}{j}\) odd.
In particular,
\[
\binom{31}{18}\equiv1\pmod2,\qquad
b=\frac1{15}\binom{31}{14}\equiv1\pmod2.
\]
Equation (5) is therefore
\[
E_3+X_3\equiv1+(b-t)\equiv t\pmod2. \tag{6}
\]

The same tautology occurs at every Mersenne parameter
\(r=2^s-1\) with \(s\ge2\), not only at \(r=15\): the two binomial
coefficients and \(b\) are odd.

At the finite controls:

- \(r=3\): (6) again gives \(E_3+X_3\equiv t\);
- \(r=5\): both coefficients in (5) vanish, so
  \(E_3+X_3\equiv0\).

## Audited conclusion

The earlier phrasing that the second moment "reduces" endpoint parity to a
new combined parity law was logically true as an implication but
mathematically misleading.  At \(r=15\), the combined law is exactly the
original \(t\)-parity law modulo \(2\).  The \(r=5\) cancellation is a
coefficient phenomenon for \(r\equiv1\pmod4\) and supplies no lift to the
Mersenne \(r=15\) case.

Validator: `verify_M2_incidence_tautology.py`.
