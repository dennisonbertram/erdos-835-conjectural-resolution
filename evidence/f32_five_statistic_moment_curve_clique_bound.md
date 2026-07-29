# The coefficient-four boundary of the \(F_{32}\) moment-curve clique

The four-statistic quotient
\[
 (e_1,e_2,e_3,e_8+e_1^8)
\]
contains the explicit \(K_{32}\) recorded in
[`f32_four_statistic_k32_obstruction.md`](f32_four_statistic_k32_obstruction.md).
This note gives the exact boundary after retaining \(e_4\).  It is a
finite-exhaustion theorem about the moment-curve family, not a
nonexistence proof for the full Johnson colouring.

Let
\[
 F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1),
 \qquad
 \lambda(S)=e_8(S)+e_1(S)^8.
\]

## 1. Every edge forces a common fourth-coordinate offset

Consider quotient states whose first three coordinates lie on the moment
curve:
\[
 (a,a^2,a^3,e_4,\lambda).
\]
Suppose states with distinct parameters \(a,b\) are joined by an actual
edge.  Let the adjacent half-sets be the deletions of \(x,y\) from their
common \(17\)-set \(R\), and write \(\rho_j=e_j(R)\).

For the deletion indexed by \(x\), coefficient multiplication gives
\[
 \rho_j=e_j(S_x)+x e_{j-1}(S_x). \tag{1}
\]
At \(j=1\), this says \(x=a+\rho_1\), and similarly
\(y=b+\rho_1\).  At \(j=2\),
\[
 \rho_2=a^2+(a+\rho_1)a=a\rho_1
       =b\rho_1. \tag{2}
\]
Since \(a\ne b\), equation (2) forces \(\rho_1=0\).  Hence
\[
 x=a,\qquad y=b,\qquad \rho_2=\rho_3=0. \tag{3}
\]
Finally,
\[
 \rho_4=e_4(S_a)+a\,e_3(S_a)=e_4(S_a)+a^4, \tag{4}
\]
and the same expression with \(b\) has the identical value \(\rho_4\).

Consequently every clique in this family has a constant
\[
 r=e_4+a^4. \tag{5}
\]
It is therefore enough to study, for fixed \(r\), the actual-edge graph
\[
 \Gamma_r
 \quad\text{on}\quad
 (a,\lambda)\longleftrightarrow
 (a,a^2,a^3,a^4+r,\lambda),
 \qquad a,\lambda\in F. \tag{6}
\]

## 2. Only two exact graphs are needed

Scaling every ground point by \(d\in F^\times\) sends
\[
 (a,\lambda,r)\longmapsto(da,d^8\lambda,d^4r). \tag{7}
\]
Because the fourth-power map permutes \(F^\times\), all nonzero offsets
are isomorphic.  Thus \(\Gamma_0\) and \(\Gamma_1\) exhaust (6) up to
isomorphism.

Exact enumeration gives:

| offset | realizable vertices | actual quotient edges | maximum clique |
|---:|---:|---:|---:|
| \(r=0\) | 1023 | 45,291 | 17 |
| \(r=1\) | 1024 | 71,648 | 17 |

For \(r=0\), the familiar trace-layer states
\[
 \{(a,1):a=0\text{ or }\operatorname {Tr}(a)=1\}
\]
give a clique of size \(17\).  The verifier also records an explicit
size-\(17\) witness for \(r=1\).  Deterministic branch and bound proves
that neither graph has a larger clique.

## 3. Exact finite method

The checker splits the 32 field elements into two sets of 16 and enumerates
all \(2^{16}\) subset generating polynomials in each half through degree
eight.  Right halves are indexed by subset size and their first four
coefficients.  For each \((a,r)\), truncated series division uniquely
determines the required right prefix from a left prefix.  The combined
eighth coefficient determines \(\lambda\).

This enumerates every \(16\)-set realizing a vertex of \(\Gamma_r\).
The checker then tests all \(16\cdot16=256\) one-point exchanges from every
realization, so every actual quotient edge is included.  Finally it runs
an exact maximum-clique search using greedy-colouring upper bounds.  The
clique routine is independently compared with brute force on every graph
of order five before it is used on the two quotient graphs.

Run:

```bash
python3 -B evidence/f32_five_statistic_moment_curve_clique_bound.py
```

## 4. Scope

The result proves that the \(K_{32}\) from the four-statistic quotient
cannot be lifted even to a \(K_{18}\) after an \(e_4\) value is assigned
to each moment-curve state.  More generally, every clique whose first
three coordinates are \((a,a^2,a^3)\) has size at most \(17\) in the
five-statistic quotient
\[
 (e_1,e_2,e_3,e_4,e_8+e_1^8).
\]

It does **not** prove that the full five-statistic quotient has no
\(K_{18}\): a different clique need not have its first three coordinates
on this moment curve.  It also does not construct a colouring or prove
that a tight \(17\)-colouring of \(J(32,16)\) is impossible.  Hence it
does not resolve Erdős--Rosenfeld Problem #835.
