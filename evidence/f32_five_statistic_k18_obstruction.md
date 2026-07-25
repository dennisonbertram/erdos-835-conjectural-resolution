# An actual-edge \(K_{18}\) in the five-statistic \(F_{32}\) quotient

Let
\[
 F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1)
\]
and, for a \(16\)-set \(S\subset F\), put
\[
 \sigma(S)=
 \bigl(e_1(S),e_2(S),e_3(S),e_4(S),
             e_8(S)+e_1(S)^8\bigr). \tag{1}
\]
Join two values of (1) when they are realized by adjacent \(16\)-sets.

## Theorem

The actual-edge quotient graph of (1) contains a \(K_{18}\).
Consequently every proper colouring of the form
\[
 c(S)=G\bigl(e_1(S),e_2(S),e_3(S),e_4(S),
                  e_8(S)+e_1(S)^8\bigr) \tag{2}
\]
uses at least \(18\) colours.

## The eighteen states

For each pair \((x,\lambda)\) in the following list, take the state
\[
 v_{x,\lambda}=(1+x,x,0,0,\lambda).
\]

```text
(31,31) (26,28) (25,4)  (24,9)  (23,14) (22,3)
(19,0)  (17,21) (16,24) (13,22) (12,27) (11,13)
(10,0)  (9,24)  (6,31)  (2,17)  (1,9)   (0,4)
```

Their first coordinates are distinct, so these are eighteen distinct
quotient vertices.

## A three-mask certificate for all 153 edges

The following hexadecimal masks encode three \(15\)-sets, with bit \(z\)
indicating the field element \(z\):

```text
0x7975CD00
0x149693B9
0xFA3041BA
```

Explicitly, they are
\[
\begin{aligned}
B_0={}&\{8,10,11,14,15,16,18,20,21,22,24,27,28,29,30\},\\
B_1={}&\{0,3,4,5,7,8,9,12,15,17,18,20,23,26,28\},\\
B_2={}&\{1,3,4,5,7,8,14,20,21,25,27,28,29,30,31\}.
\end{aligned}
\]
Direct expansion gives
\[
 \prod_{b\in B_i}(1+bt)=1+t+O(t^5)
 \qquad(i=0,1,2). \tag{3}
\]
Thus, whenever \(x\notin B_i\), the first four coordinates of
\(\sigma(B_i\cup\{x\})\) are
\[
 (1+x,x,0,0). \tag{4}
\]
The fifth coordinate, recomputed through degree eight, is exactly the
listed \(\lambda\) for every applicable base.

For every two parameters \(x,y\) in the eighteen-element list, at least
one of \(B_0,B_1,B_2\) excludes both.  For such a base,
\[
 S_x=B_i\cup\{x\},\qquad S_y=B_i\cup\{y\}
\]
are \(16\)-sets satisfying
\[
 |S_x\cap S_y|=15,\qquad
 \sigma(S_x)=v_{x,\lambda_x},\qquad
 \sigma(S_y)=v_{y,\lambda_y}. \tag{5}
\]
Hence every one of the \(\binom{18}{2}=153\) pairs is an actual Johnson
edge.  The eighteen states therefore form a \(K_{18}\), proving the
theorem.

## Independent verification

Run

```bash
python3 -B evidence/f32_five_statistic_k18_verifier.py
```

The checker contains only the eighteen pairs and three static masks.  It
implements field multiplication by polynomial long division, recomputes
all elementary symmetric coefficients from the roots, checks every
applicable realization, and checks all 153 pairwise edges.  The search
that found the certificate is not part of the proof.

For provenance, the certificate was found by
[`f32_five_statistic_global_clique_search.cpp`](f32_five_statistic_global_clique_search.cpp).
Its low-coordinate reduction and semilinear orbit count are independently
audited by
[`verify_f32_five_statistic_global_reduction.py`](verify_f32_five_statistic_global_reduction.py).

## Scope

This is a rigorous obstruction to the entire five-statistic construction
(2), strictly beyond the four-statistic \(K_{32}\).  It does **not** show
that \(J(32,16)\) has no tight \(17\)-colouring: an arbitrary colouring
need not factor through (1).  It therefore does not resolve
Erdős--Rosenfeld Problem #835.
