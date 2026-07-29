# Odd precursor: exact structural consequence and controls

This note records an attempt to rule out every tight
\(q=m+2\)-colouring of \(J(2m,m)\) for odd \(m>1\).  It does **not**
prove that universal assertion.  Its value is a precise characterization that
any such colouring must satisfy, together with independent small controls.

Let \(c:\binom X m\to[q]\) be a proper colouring, where \(|X|=2m\),
\(m\ge3\) is odd, and \(q=m+2\).  The odd-neighbour lift calculation gives
the missing-colour map

\[
d:\binom X{m-1}\to[q]
\]

and shows that it is rainbow over the \(q\) extensions of every
\((m-2)\)-set.  Hence its fibres are a large set

\[
 \{d^{-1}(a):a\in[q]\}=LS(m-2,m-1,2m). \tag{1}
\]

For a colour \(a\), put \(C_a=c^{-1}(a)\), and let
\(\overline C_a=\{S^c:S\in C_a\}\).  The same calculation establishes
\(c(S)\ne c(S^c)\), so the three sets

\[
C_a,\qquad \overline C_a,\qquad
D_a=\binom Xm\setminus(C_a\cup\overline C_a)
\]

are disjoint and cover the vertices of \(J(2m,m)\).

## Forced equitable partition

They form an equitable partition, with quotient matrix (in the displayed
order)

\[
 Q_m=
 \begin{pmatrix}
 0&m&m^2-m\\
 m&0&m^2-m\\
 m-1&m-1&m^2-2m+2
 \end{pmatrix}. \tag{2}
\]

Here is a short derivation.  Each fibre \(C_a\) is an
\((m-2)\)-design with

\[
 \lambda_i(C_a)=\frac{\binom{2m-i}{m-i}}q
 \quad(0\le i\le m-2). \tag{3}
\]

If \(S\) has colour \(b\ne a\), the local rainbow edge-colouring at the
\((m-2)\)-facets of \(S\) says that the number of its neighbours in
\(C_a\) is \(m\) when \(c(S^c)=a\), and \(m-1\) otherwise.  This gives
the last row of (2), and complementing gives the corresponding counts into
\(\overline C_a\).  Finally, if \(S\in C_a\), apply the preceding
neighbour count to \(S^c\): its complement has colour \(a\), so it has
exactly \(m\) neighbours in \(C_a\).  Complementing those neighbours gives
exactly \(m\) neighbours of \(S\) in \(\overline C_a\).  The rest of its
\(m^2\) neighbours lie in \(D_a\).

The eigenvalues of (2) are

\[
 m^2,\qquad -m,\qquad 2-m.
\]

They are respectively the Johnson-graph eigenvalues in eigenspaces
\(E_0,E_m,E_{m-1}\).  Thus this very rigid three-cell structure passes the
basic spectral/interlacing test; it cannot by itself prove nonexistence.
This also explains why the usual low-order association-scheme positivity
tests remain feasible for the prime candidates.

Equation (1) is already highly restrictive, but it is not an automatic
contradiction.  For the first open case of Problem #835, \(m=15\), it is
an \(LS(13,14,30)\), which derives to the still-unresolved
\(LS(4,5,21)\).  Consequently a universal argument must use compatibility
between different colour classes beyond (1)--(3), or an additional global
obstruction.

## Small controls

* \(m=1\) is degenerate: \(J(2,1)=K_2\) is 2-colourable, rather than
  tight 3-colourable.  The target after the two-point lift,
  \(J(4,2)\), does have chromatic number 3, so the stated odd-neighbour
  equivalence properly begins at \(m\ge3\).
* \(m=3\) has no tight 5-colouring.  The verifier
  [`verify_odd_precursor_m3.py`](verify_odd_precursor_m3.py) enumerates all
  six one-factorisations of \(K_6\) (modulo only the irrelevant colour-name
  permutation) and, for each, all \(2^{10}\) complementary-triple
  orientations.  None satisfies the rainbow condition at every edge.  This
  is an independent precursor-side check of the already-known \(k=4\)
  obstruction.
* \(m=5\) would lift to a tight 7-colouring of \(J(12,6)\), equivalently
  a partition into seven disjoint Witt systems \(S(5,6,12)\).  The known
  Kramer--Mesner result that at most two such labelled systems can be
  mutually block-disjoint rules this out.  This is a control, not a new
  proof of that classical result.

Running the finite check:

```sh
python3 -B evidence/verify_odd_precursor_m3.py
```
