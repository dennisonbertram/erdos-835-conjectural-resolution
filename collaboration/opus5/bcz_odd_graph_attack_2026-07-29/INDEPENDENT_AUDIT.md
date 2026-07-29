# Independent audit: Bailey--Cameron--Zhou Odd-graph attack

Date: 2026-07-29

## Verdict

The specialization in `PROOF.md` is mathematically valid, including the
uniform feasibility result in Theorem 11.4. It does **not** solve
Erdős--Rosenfeld Problem #835: it proves that the tested equitable-partition
projections, divisibility tests, and scalar two-colour transport inequality
cannot supply the required obstruction.

## Primary-source check

I retrieved Bailey, Cameron and Zhou,
[*Equitable partitions of regular graphs, and perfect sets in normal Cayley
graphs*](https://arxiv.org/html/2605.17376v1), arXiv:2605.17376v1
(17 May 2026), and checked Theorem 2.3, Corollary 2.4, and systems (6)--(8)
and (13) against the formulas used here.

There are two different parameters called \(k\). In the source theorem it is
the graph degree. In this repository \(O_k=KG(2k-1,k-1)\) has graph degree
\(k\), and a hypothetical large set partitions it into
\(q=k+1\) perfect codes. Its colour quotient is
\[
M_\tau=J_q-I_q.
\]
For distinct colours \(i,j\), the source notation therefore gives
\[
c_{ij}=1,\qquad c_{jj}=0,\qquad
r_{ij}=\frac1{k+1}=\frac1q.
\]
Consequently source system (6) is
\[
J_qd=0,
\]
so its full real solution set is \({\bf1}^{\mathsf T}d=0\).
Writing the intersection-density matrix as
\(T=q^{-1}J+Z\), source formula (7) becomes
\[
h=Z_{\cdot j}-Td,
\]
and source system (8) is
\[
(B_\pi+I)h=0.
\]
Both terms lie in that kernel because
\((B_\pi+I)T=J\), \(d\perp{\bf1}\), and
\((B_\pi+I)(q^{-1}{\bf1})={\bf1}\). This agrees exactly with the
specialization in Theorems 1--3 of `PROOF.md`.

Corollary 2.4(a), applied to one perfect code, is the corresponding single
column projection. The partition into singletons is itself equitable and
has quotient matrix \(A\); for that choice the projected equation is the
original perfect-code equation. Thus ranging over *all* auxiliary equitable
partitions is logically equivalent to the original design quadrature. A
proper auxiliary partition is only a projection and can be strictly weaker.

## Corrections and scope controls

The audited files now make the following distinctions explicitly.

1. Real-linear feasibility of a projected system does not prove feasibility
   in its integral or zero-one domain.
2. The equations decouple by colour, but the identity
   \(\sum_a{\bf1}_{C_a}={\bf1}\) is a genuine global disjointness condition.
   The package therefore does not say that one code and \(q\) disjoint codes
   are indistinguishable.
3. The \(k=4\) and \(k=6\) controls show only that the named proper
   projections remain feasible although the corresponding large sets do
   not exist. The singleton projection is the full infeasible problem.
4. The route-closure theorem covers the intersection-density,
   projection/intertwining, and derived Gram systems in this package. It
   does not exclude constraints using triple intersections, a non-equitable
   common refinement, a stronger transportation-polytope cut, or additional
   normal-Cayley character data.
5. The Kummer calculation in Theorem 7 uses
   \(n-s=k-m+j=q-1-(m-j)\). The earlier expression \(k-1-m+j\)
   would have been an off-by-one error; the proof and current prose use the
   corrected digit.

## Independent theorem checks

I checked the main algebra independently:

- \(B_\pi^{\mathsf T}S=SB_\tau\) follows by counting graph edges between
  cells of the two equitable partitions in either order.
- With \(M_\tau=J-I\), the density equation is
  \((B_\pi+I)T=J\), and its complete affine solution space is
  \(T=q^{-1}J+Z\), where every column of \(Z\) lies in
  \(\ker(B_\pi+I)\) and \(Z{\bf1}=0\).
- The singleton partition recovers
  \((A+I)X_\tau=J\), so the asserted sharpness of the projection statement
  is exact.
- Theorem 7's binomial divisibility has one base-\(q\) carry: both
  \(s=q-2-j\) and \(n-s=q-1-(m-j)\) lie in
  \(\{1,\ldots,q-1\}\), while their sum is at least \(q\).
- In Theorem 11.4, the difference of the proposed telescoping expression
  is exactly
  \[
  \binom{k-1}{i}
  \left[\binom{k}{i+1}-\binom{k}{i}\right].
  \]
  Substitution gives (11.5), and the three slack formulas (11.6) reduce the
  upper bounds to the elementary inequalities stated there. The boundary
  cases \(i=0,k-1\) are included.

## Executable audit

I ran:

```sh
python3 -B \
  collaboration/opus5/bcz_odd_graph_attack_2026-07-29/\
verify_bcz_odd_graph.py

ruff check \
  collaboration/opus5/bcz_odd_graph_attack_2026-07-29/\
verify_bcz_odd_graph.py
```

The exact verifier reported `RESULT: 0 failure(s)`. It enumerated all
equitable partitions and ordered pairs for \(K_3,C_6,Q_3\), the Petersen
graph, and \(O_4\); checked the \(k=2\) positive control; matched algebraic
and geometric eigenspace dimensions on all 64 equitable partitions of
\(O_4\); verified the Fano-plane control; checked Theorems 8.1 and 11.3 for
all 45 admissible \(k\le200\); and checked Theorem 7 for every admissible
\(k\le80\). Ruff passed after removal of one unused local variable.

## Exact remaining gap

The package supplies no contradiction and no construction. A continuation
of this route must use an integral or zero-one obstruction in a strategically
chosen projection, a genuinely stronger multi-colour transportation cut, or
higher-order coupling not implied by the single-colour design equations.
The unrestricted \(k=16\) case, and therefore Problem #835, remains open.
