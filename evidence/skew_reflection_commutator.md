# The skew reflection-commutator attack

Date: 2026-07-24.  Verifier:
`evidence/verify_skew_reflection_commutator.py`.

This note sharpens the oriented cross-Gram route in
`cross_gram_signature_attack.md`.  It replaces the conjectural balanced
signature of a symmetric matrix by the conjectural nonsingularity of a
canonical skew matrix.

## 1. Construction

Let \(r\) be odd, \(v=2r+1\), and let \(A,B,C\) be
\(S(r-1,r,v)\) systems with
\[
 A\cap B=A\cap C=\varnothing .
\]
Put
\[
 B_0=B\setminus C,\qquad C_0=C\setminus B,\qquad
 t=|B_0|=b-|B\cap C|.
\]

Use the skew oriented disjointness operator
\({\cal T}=\iota_u*\), and for a system \(D\) put
\[
 L_D={\cal T}P_D{\cal T},\qquad
 J_D=I+\frac{2}{r+1}L_D .
\]
As proved in `cross_gram_signature_attack.md`, \(J_D\) is a symmetric
orthogonal involution.

The new matrix is the compression
\[
 {\cal K}=P_{B_0}[J_A,J_C]P_{B_0}
 =\frac{4}{(r+1)^2}K_0,                          \tag{1.1}
\]
where
\[
 K_0=P_{B_0}[L_A,L_C]P_{B_0}.                   \tag{1.2}
\]
Both \({\cal K}\) and the integral matrix \(K_0\) are skew-symmetric.
They have the same rank and kernel.

## 2. Exact small-matrix formula

Let \(A_0\) be the \(t\) blocks of \(A\) disjoint from the blocks of
\(B_0\).  Equivalently, relative to the fixed-base sphere encoding,
\(A_0\) is the set of spheres on which \(B\) and \(C\) choose different
blocks.  Define
\[
 X={\cal T}[B_0,A_0],\qquad
 P={\cal T}[B_0,C_0],\qquad
 G={\cal T}^2[A_0,C_0]
   =(\langle d_a,d_c\rangle)_{a\in A_0,c\in C_0}. \tag{2.1}
\]
The matrices \(X\) and \(P\) are signed permutation matrices.

**Lemma 2.1 (Proved).**
\[
 \boxed{K_0=-XGP^{\mathsf T}+PG^{\mathsf T}X^{\mathsf T}
       =Z^{\mathsf T}-Z,\qquad Z=XGP^{\mathsf T}.} \tag{2.2}
\]

**Proof.**
Let \(V_D={\cal T}E_D\), so \(L_D=-V_DV_D^{\mathsf T}\).  On the
selected coordinates,
\[
 P_{B_0}V_A=X,\qquad P_{B_0}V_C=P,
\]
while
\[
 V_A^{\mathsf T}V_C
 =E_A^{\mathsf T}{\cal T}^{\mathsf T}{\cal T}E_C
 =-{\cal T}^2[A,C].
\]
Only the \(A_0,C_0\) columns survive the two outside restrictions.
It follows that
\[
 P_{B_0}L_AL_CP_{B_0}=-XGP^{\mathsf T},
\qquad
 P_{B_0}L_CL_AP_{B_0}=-PG^{\mathsf T}X^{\mathsf T}.
\]
Subtracting proves (2.2). \(\square\)

After the signed change of basis \(X\), (2.2) can also be written
\[
 X^{\mathsf T}K_0X=W G^{\mathsf T}-GW^{\mathsf T},
\qquad W=X^{\mathsf T}P,                         \tag{2.3}
\]
so the matrix is the skew part of the oriented facet cross-Gram after
identifying \(A_0\) and \(C_0\) along the path through \(B_0\).

### 2.1 Exact support and boundary factorization

Index the coordinates by active \(A\)-blocks \(Q\).  Let \(S_Q\in B_0\)
be disjoint from \(Q\), and let \(T_Q\in C_0\) be the block disjoint
from \(S_Q\).  Both \(Q\) and \(T_Q\) are \(r\)-subsets of the
\((r+1)\)-set \(X\setminus S_Q\), and \(A\cap C=\varnothing\), so there
are unique labels
\[
 t_Q\in Q,\qquad b_Q\notin Q,\qquad
 T_Q=Q\setminus\{t_Q\}\cup\{b_Q\}.               \tag{2.4}
\]
After multiplying individual boundary rows by the matching signs, write
\(D_A=(d_Q)\) and \(D_T=(d_{T_Q})\).  Then
\[
 Z=D_AD_T^{\mathsf T},\qquad
 \boxed{K_0=(D_T-D_A)(D_T+D_A)^{\mathsf T}.}     \tag{2.5}
\]
Indeed \(D_AD_A^{\mathsf T}=D_TD_T^{\mathsf T}=rI\), so the two
self-Gram terms in the product cancel and leave
\(D_TD_A^{\mathsf T}-D_AD_T^{\mathsf T}=Z^{\mathsf T}-Z\).

For distinct active \(Q,Q'\), the exact zero pattern is
\[
 Z_{Q,Q'}\ne0
 \quad\Longleftrightarrow\quad
 \begin{cases}
 |Q\cap Q'|=r-2,\\
 t_{Q'}\notin Q,\\
 b_{Q'}\in Q .
 \end{cases}                                     \tag{2.6}
\]
To prove this, use
\[
 |Q\cap T_{Q'}|
 =|Q\cap Q'|-\mathbf1_{t_{Q'}\in Q}
             +\mathbf1_{b_{Q'}\in Q}.
\]
Distinct blocks of \(A\) meet in at most \(r-2\) points, so this
quantity is \(r-1\) exactly under the three conditions in (2.6).
The support of \(K_0\) is the exclusive-or of (2.6) and the same
condition with \(Q,Q'\) reversed.

In characteristic two, (2.5) becomes the incidence-Gram identity
\[
 \boxed{\overline K_0=EE^{\mathsf T},\qquad
 E=D_T+D_A.}                                     \tag{2.7}
\]
The row indexed by \(Q\) is the symmetric difference of the facets of
\(Q\) and \(Q-t_Q+b_Q\), and has weight \(2(r-1)\).  Thus
\(\overline K_0\) is alternating, as it must be.

The row-sum parity is not fixed.  If \(I=A\setminus A_0\) is the set of
inactive spheres and \(D=B\cap C\), then
\[
 (\overline K_0\mathbf1)_Q
 =
 |\{d\in D:|Q\cap d|=r-1\}|
 +|\{a\in I:|a\cap T_Q|=r-1\}|
 \pmod2.                                         \tag{2.8}
\]
The all-odd/Mersenne intersection moments determine the *total*
intersection valencies, but do not determine either selected-subset
count in (2.8).  Also, (2.6) shows that \(K_0\) uses only the internal
\((r-2)\)-intersection graph of \(A\).  Its valency is \(6,30,840\)
at \(r=3,5,15\), respectively, so it is even in both the Mersenne and
non-Mersenne small cases.

## 3. Parity implication and the honest target

Every real skew-symmetric matrix has even rank.  Therefore
\[
 t\equiv\dim\ker K_0\pmod2.                      \tag{3.1}
\]
Consequently, an independently proved even-dimensional kernel would
give
\[
 |B\cap C|=b-t\equiv b\pmod2.                   \tag{3.2}
\]

There is an important tautology warning: by (3.1), merely conjecturing
that \(\dim\ker K_0\) is even is equivalent to conjecturing that \(t\)
is even.  It supplies no leverage by itself.  The clean stronger target
suggested by the finite data is:

> **Skew-commutator conjecture (Open).**  For odd \(r\ge5\), \(K_0\)
> is nonsingular for every canonical triple \(A,B,C\).

This is stronger than the required parity and is not a formal
restatement of it.  A proof at \(r=15\) would settle the first open case
of Erdős problem 835 negatively.

## 4. Exhaustive finite results

**Verified, \(r=1\).**  For the three singleton systems on three
points, \(t=1\) and \(K_0=(0)\).  Thus the claim cannot include \(r=1\).

**Verified, \(r=3\).**  Fix a Fano base \(A\).  On all 28 unordered
pairs of its eight disjoint mates,
\[
 t=6,\qquad \operatorname{rank}K_0=4,\qquad
 \dim\ker K_0=2.                                 \tag{4.1}
\]

The kernel has a uniform geometric support description.  Let
\[
 S_0\in B\cap C,\qquad
 a_0\in A\ \text{be disjoint from }S_0,\qquad
 \{x\}=X\setminus(S_0\cup a_0).
\]
The six coordinates split into
\[
 I_x=\{S\in B_0:x\in S\},\qquad
 I_{\bar x}=\{S\in B_0:x\notin S\},
\]
each of size three.  For every one of the 28 pairs,
\[
 \ker K_0=L_x\oplus L_{\bar x},                  \tag{4.2}
\]
where \(L_x\) is a one-dimensional line supported exactly on \(I_x\)
and \(L_{\bar x}\) is a one-dimensional line supported exactly on
\(I_{\bar x}\).  The nonzero entries are orientation signs that vary
with the pair; there is no uniform all-ones gauge in the fixed global
orientation.  Formula (4.2) is an exhaustive exact Fano statement, not
yet an \(r\)-general kernel theorem.

**Verified, \(r=5\).**  For the deterministic \(S(4,5,11)\) base, all
144 mates and all 10,296 unordered pairs give
\[
\begin{array}{c|c|c|c|c}
|B\cap C|&t&\text{pairs}&\operatorname{rank}K_0&
\dim\ker K_0\\ \hline
6&60&6336&60&0\\
18&48&3960&48&0.
\end{array}                                      \tag{4.3}
\]
Every rank in (4.3) is certified already over the parameter field
\(\mathbb F_{r+2}=\mathbb F_7\), hence is exact over \(\mathbb Q\).
This suggests the sharper possible target of proving nonsingularity over
\(\mathbb F_{17}\) at \(r=15\).  It is a direction, not yet a theorem.

Characteristic two does not give a uniform determinant even at \(r=5\):
\[
\begin{array}{c|c|c}
|B\cap C|&\dim\ker(\overline K_0)&\text{pairs}\\ \hline
18&2&3960\\
6&0&4750\\
6&2&792\\
6&4&794 .
\end{array}                                      \tag{4.4}
\]

For the deterministic representatives used elsewhere in the evidence,
\[
\begin{array}{c|c|c}
|B\cap C|&|\det K_0|&|\operatorname{Pf}K_0|\\ \hline
6&(3\cdot27883)^2&3\cdot27883\\
18&(2\cdot3\cdot5\cdot31)^2&2\cdot3\cdot5\cdot31 .
\end{array}                                      \tag{4.5}
\]
The \(h=6\) determinant is not constant over all pairs, so (4.5) is
representative data rather than a universal determinant formula.

At the parameter prime \(p=r+2\), Lemma 2.1 of the cross-Gram note gives
\[
 L_D^2=-(r+1)L_D=L_D\pmod p.                     \tag{4.6}
\]
Thus the proposed mod-\(17\) matrix is a compression of the commutator
of two symmetric idempotents.  This polynomial identity does not force
nondegeneracy.  There is a particularly small exact countermodel over
\(\mathbb F_{17}\).  On \(U\oplus U\), put
\[
 L=\begin{pmatrix}-I&7I\\7I&2I\end{pmatrix}.     \tag{4.7}
\]
Because \(7^2=-2\pmod {17}\), direct multiplication gives \(L^2=L\),
and the compression to the first copy of \(U\) is exactly \(-I\), as
for both \(L_A,L_C\) on active \(B\)-coordinates.  Taking
\(L_A=L_C=L\) makes the compressed commutator zero.  This is not a
Steiner counterexample; it proves that idempotence, symmetry, rank, and
the known diagonal compression alone cannot force the determinant.

The large mod-\(17\) Odd-graph Jordan and critical-group spaces likewise
control individual invariant subspaces, not their relative position,
and impose no lower bound on this compressed commutator.  A mod-\(17\)
proof must therefore use the coordinatewise Steiner relative-position
constraints encoded by (2.4)--(2.6).

## 5. Verdict

The reflection commutator is the cleanest parity matrix currently
available:

- skew-symmetry is proved structurally;
- its small \(t\times t\) formula (2.2) uses only signed matchings and
  oriented facet incidence;
- it is nonsingular on every one of the 10,296 canonical \(r=5\)
  instances, by exact modular certificates;
- the exceptional Fano kernel has a precise two-line incidence support.

The missing theorem is still substantial.  Nonsingularity of a
skew \(t\times t\) matrix already forces \(t\) even, so it cannot be
deduced from skew-symmetry or a formal Pfaffian-square identity alone.
A successful proof must show that the Pfaffian does not cancel, or
construct a nondegenerate pairing from the Steiner axioms without first
assuming the desired parity.
