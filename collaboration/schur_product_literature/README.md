# Schur-product and finite-frame literature audit

Date: 2026-07-26.

## Outcome

No theorem located in the primary literature gives a dimension cap below \(15\),
or otherwise contradicts the deleted-colour Hadamard-kernel condition, for
either a hypothetical \(LS(4,5,21)\) or \(LS(3,4,20)\).

The relevant results do give exact information, but their hypotheses stop
short of the needed conclusion:

* Schur-product bounds control \(\dim U^{\langle2\rangle}\) from below using
  global MDS, dual-distance, minimum-distance, or stabilizer hypotheses.  Those
  hypotheses are not supplied by the local simplex condition.  Even the
  conditional trivial-stabilizer bound is only
  \(\dim U^{\langle2\rangle}\geq29\).
* Wilson's modular rank theorem applies to the complete inclusion matrix, not
  to the matrix after the columns of an arbitrary Steiner system have been
  removed.
* The arbitrary-deletion theorem of Plaza--Xiang permits at most four deleted
  rows after transposition here, versus \(1197\) or \(285\).
* Finite-field Gerzon bounds require a globally equiangular system.  The
  deleted-colour theorem fixes inner products only for pairs of blocks in a
  common star.

There is, however, a new rigorous consequence of gluing all local simplexes:
the complete family of evaluation vectors is a global equal-norm tight frame.
Its first two nonedge moments can be computed exactly.  At every vector, the
squared inner products with the nonneighbors must take at least two distinct
values.  This is a genuine necessary condition, but not a capacity bound and
not a resolution of Erdős--Rosenfeld Problem #835.

The exact verifier is
`collaboration/schur_product_literature/verify_literature_hypotheses.py`.
It uses only the Python standard library and arithmetic in \(\mathbb F_{17}\).
It does not assume that either large set exists.

## 1. Setup and dimension pressure

Let \(t=4,v=21\) or \(t=3,v=20\), put \(k=t+1\), and fix one design
\(D\) in a hypothetical large set.  Let
\[
 M_D\in\mathbb F_{17}^{R\times N}
\]
be the inclusion matrix whose rows are the \(t\)-subsets and whose columns are
the \(k\)-subsets outside \(D\).  The deleted-colour theorem would supply
\[
 U\leq\ker M_D,\qquad \dim U=15,
\]
and a nondegenerate symmetric form \(b\) on \(U\), such that
\[
 U^{\langle2\rangle}
 :=\operatorname{span}\{x\circ y:x,y\in U\}
 \ \leq\
 Q_D:=\{z:M_Dz\in\langle\mathbf1\rangle\}.       \tag{1}
\]

The exact parameters are:

| layer | \(R\) | \(|D|\) | \(N\) | \(\dim Q_D\) lower bound |
|---|---:|---:|---:|---:|
| \(LS(4,5,21)\) | \(5985\) | \(1197\) | \(19152\) | \(13168\) |
| \(LS(3,4,20)\) | \(1140\) | \(285\) | \(4560\) | \(3421\) |

Indeed, every row of \(M_D\) has \(16=-1\pmod {17}\) entries, so
\(\langle\mathbf1\rangle\) lies in its image.  Hence
\[
 \dim Q_D=N-\operatorname{rank}M_D+1\geq N-R+1. \tag{2}
\]
On the other hand,
\[
 \dim U^{\langle2\rangle}\leq\dim\operatorname{Sym}^2(U)
 =\binom{16}{2}=120.                             \tag{3}
\]
Thus the ambient target in (1) has thousands of spare dimensions even if the
square map has maximum rank.

Every deleted star restricts \(U\) isomorphically to the
\([16,15]\) single-parity-check code
\[
 H_0=\{z\in\mathbb F_{17}^{16}:\textstyle\sum_i z_i=0\}.
\]
The Schur square of \(H_0\) is all of \(\mathbb F_{17}^{16}\), so puncturing
\(U^{\langle2\rangle}\) to any star is surjective and
\[
 16\leq\dim U^{\langle2\rangle}\leq120.          \tag{4}
\]
The lower endpoint is not an artificial weakness: if a tight colouring
existed, its canonical \(U\), spanned by the powers \(g,\ldots,g^{15}\), would
have square equal to the \(16\)-dimensional code of all functions of the
nonzero colour \(g\).  Consequently a universal square-dimension lower bound
strictly above \(16\) would already need to use geometry that excludes the
desired colouring itself.

## 2. A global tight-frame consequence

For every remaining \(k\)-block \(S\), let \(v_S\in U\) be its evaluation
vector:
\[
 b(v_S,x)=x(S)\qquad(x\in U).
\]
In each deleted star the \(16\) vectors have Gram matrix \(P=I+J\):
\[
 b(v_S,v_S)=2,\qquad b(v_S,v_T)=1
 \quad(S\ne T\text{ in the same star}),          \tag{5}
\]
and their sum is zero.  Since \(P^2=P\) and \(\operatorname{rank}P=15\), the
local frame operator is the identity on \(U\).

Sum the \(R=\binom vt\) local frame operators.  Every remaining block occurs
in exactly \(k\) stars, so
\[
 \sum_{S\notin D} v_Sv_S^*
   =\frac{R}{k}I,                                \tag{6}
\]
where \(v_Sv_S^*\) denotes \(x\mapsto b(v_S,x)v_S\).  Similarly, summing the
local zero-centroid identities gives
\[
 \sum_{S\notin D}v_S=0.                          \tag{7}
\]
Thus the global vectors form a finite-field equal-norm tight frame of norm
\(2\), with the following parameters in \(\mathbb F_{17}\):

| layer | number of vectors | dimension | frame constant \(c=R/k\) |
|---|---:|---:|---:|
| \(LS(4,5,21)\) | \(19152\) | \(15\) | \(7\) |
| \(LS(3,4,20)\) | \(4560\) | \(15\) | \(13\) |

The trace identity \(2N=15c\) holds in both cases.

### Exact nonedge moments

Join two remaining blocks when they share a \(t\)-subset.  This residual
Johnson graph is regular of degree \(15k\): at each of the \(k\) facets of a
remaining block, one of the other \(16\) extensions is the deleted block and
the other \(15\) remain.  Therefore its degrees are \(75\) and \(60\).

Fix \(S\).  Equations (5)--(7) give
\[
 \sum_{\substack{T\ne S\\T\not\sim S}}b(v_S,v_T)
   =-(2+15k),                                    \tag{8}
\]
and
\[
 \sum_{\substack{T\ne S\\T\not\sim S}}b(v_S,v_T)^2
   =2c-4-15k.                                    \tag{9}
\]
The numerical values are:

| layer | number of nonneighbors mod \(17\) | sum in (8) | sum in (9) |
|---|---:|---:|---:|
| \(LS(4,5,21)\) | \(2\) | \(8\) | \(3\) |
| \(LS(3,4,20)\) | \(11\) | \(6\) | \(13\) |

If all nonedge squared inner products at this fixed \(S\) were equal, their
common value would have to be
\[
 3/2=10\quad\text{or}\quad13/11=12
 \qquad\text{in }\mathbb F_{17}.                 \tag{10}
\]
Both \(10\) and \(12\) are quadratic nonresidues modulo \(17\), whereas every
quantity \(b(v_S,v_T)^2\) is a square.  Therefore, for every \(S\), the
nonedge squared inner products are nonconstant.

This also explains the precise reach of the finite-field Gerzon bound.
Greaves--Iverson--Jasper--Mixon, Proposition 2.9, bounds an
\((a,b)\)-equiangular system with \(a^2\ne b\) by
\(\binom{d+1}{2}\).  If all off-diagonal squares here were \(1\), the
parameters would be \(a=2,b=1,d=15\), forcing \(N\leq120\), contrary to both
tables.  But the theorem does not apply to the actual data because nonedge
inner products are unspecified; (10) proves they cannot even all have one
other squared value.

## 3. Audit of componentwise-product code theorems

### Product Singleton bound

Mirandola--Zémor, Theorem 1.1, and Randriambololona's product-code treatment
give
\[
 d_{\min}(CD)\leq
 \max\{1,n-\dim C-\dim D+2\}.                    \tag{11}
\]
For \(C=D=U\), this says only
\[
 d_{\min}(U^{\langle2\rangle})\leq N-28,
\]
namely \(19124\) or \(4532\).  A large upper bound on minimum distance gives
no contradiction with (1).

The classifications of Product-MDS pairs in Mirandola--Zémor require equality
in (11) and \(d_{\min}(CD)\geq2\).  Neither condition follows from the
deleted-colour theorem, so the Reed--Solomon/direct-sum conclusions cannot be
invoked.

### MDS product lower bound

Mirandola--Zémor, Theorem 2.5, states for full-support codes, with at least one
factor globally MDS,
\[
 \dim(CD)\geq\min\{n,\dim C+\dim D-1\}.           \tag{12}
\]
The local restriction \(U|_{\text{star}}=H_0\) is MDS, but this is not the
global MDS hypothesis on the length-\(N\) code \(U\).  Therefore (12) does not
apply.  Even granting its conclusion conditionally would yield only
\(\dim U^{\langle2\rangle}\geq29\), still far below (2).

### Coding-theoretic Kneser theorem

Mirandola--Zémor, Theorem 3.3, is unconditional:
\[
 \dim(ST)\geq
 \dim S+\dim T-\dim\operatorname{St}(ST),         \tag{13}
\]
where
\(\operatorname{St}(C)=\{z:z\circ C\subseteq C\}\).
It gives
\[
 \dim U^{\langle2\rangle}\geq
 30-\dim\operatorname{St}(U^{\langle2\rangle}).  \tag{14}
\]
There is no theorem in the deleted-colour hypotheses that makes this
stabilizer trivial.  In fact, for the canonical space of a genuine colouring,
\(U^{\langle2\rangle}\) consists of all functions of the \(16\) nonzero
colours and has a \(16\)-dimensional stabilizer spanned by the colour-class
indicators.  Thus (13) is structurally compatible with the target rather than
an obstruction to it.

The dual-distance refinements in the same paper also do not trigger:
the local simplex guarantees only that no evaluation column is zero.
Nonadjacent evaluation vectors may be proportional, so a global lower bound
\(d_{\min}(U^\perp)\geq3\) is unavailable.  Likewise no lower bound
\(d_{\min}(U^{\langle2\rangle})\geq2\) has been established.

### Quadratic hull

Randriambololona identifies
\[
 I_2(U)=\ker\bigl(\operatorname{Sym}^2U
       \longrightarrow U^{\langle2\rangle}\bigr),\qquad
 \dim U^{\langle2\rangle}=120-\dim I_2(U).        \tag{15}
\]
This is the natural projective-geometric language for the rank of the square
map.  The paper explicitly notes that a general code's quadratic hull has no
a priori uniform control.  The special reconstruction results concern AG or
otherwise structured codes; no such realization of \(U\) is present here.
Thus (15) reformulates the missing bound but does not supply it.

## 4. Audit of modular inclusion-matrix results

Wilson's diagonal form for the complete inclusion matrix \(W_{t,k}(v)\) has
diagonal factors
\[
 \binom{k-i}{t-i}
 \quad\text{with multiplicity}\quad
 \binom vi-\binom v{i-1}
 \qquad(0\leq i\leq t).                          \tag{16}
\]
For \(W_{4,5}(21)\) the factors are
\((5,4,3,2,1)\); for \(W_{3,4}(20)\) they are
\((4,3,2,1)\).  None vanishes modulo \(17\), so the complete matrices have
full row ranks \(5985\) and \(1140\).

This does not determine \(\operatorname{rank}M_D\).  Removing the columns in
an arbitrary design \(D\) destroys the complete Boolean-lattice
\(S_v\)-module map to which Wilson's diagonalization applies.

Plaza--Xiang, Theorem 4, is the directly relevant arbitrary-deletion result.
For \(0\leq s<r\leq n/2\), the transpose inclusion matrix retains its complete
rank over any field when the number of deleted \(r\)-set rows is at most
\((n-1)/r\).  Applied to \(M_D^\mathsf T\), its hypotheses would permit:

| layer | \((n-1)/r\) | actual deleted rows |
|---|---:|---:|
| \(LS(4,5,21)\) | \(4\) | \(1197\) |
| \(LS(3,4,20)\) | \(19/4\), hence at most \(4\) rows | \(285\) |

The deletion hypothesis fails by orders of magnitude.  Moreover, even a
separate proof that \(M_D\) had full row rank would merely turn (2) into
equality; the resulting spaces would still have dimensions \(13168\) and
\(3421\), much larger than \(120\).

## 5. Local frame gluing is pairwise feasible

The frame literature gives Gram and equiangular bounds but no theorem for this
partially prescribed, highly overlapping family of simplexes.  It is
important that even the two-star compatibility problem has exact solutions.

Let two adjacent \(t\)-stars have cross-Gram matrix \(C\).  Since each local
Gram matrix is \(P=I+J\) and each local frame operator is \(I\), necessarily
\[
 CC^\mathsf T=C^\mathsf TC=P,
 \qquad C\mathbf1=C^\mathsf T\mathbf1=0.          \tag{17}
\]
Permutation gluings \(C=P\Pi\) satisfy (17):

* if the union block is deleted, a \(16\)-cycle gives inner product \(1\) on
  all \(16\) corresponding outside-point pairs;
* if the union block remains, fix the shared coordinate and use a \(15\)-cycle
  on the others.  The shared vector has inner product \(2\) with itself and
  \(1\) with every other local vector, while all required corresponding pairs
  also have inner product \(1\).

Thus no obstruction occurs at the level of a single adjacent pair of stars.
The unresolved issue is global synchronization around the many overlap
cycles.

The closest primary paper found on finite-field simplex gluing is
Cheek--Cooper--Gilman--Iosevich--Jaber--Palsson--Sharan--Shuffelton--Tomé.
It counts congruence classes of simplex trees embedded in large subsets of
\(\mathbb F_q^d\), and describes cycles or gluings along edges/faces as only
partial extensions of that program.  Its hypotheses are asymptotic
large-subset assumptions and its objects are distance embeddings, not a
low-rank Gram completion with shared labelled vectors.  It therefore gives no
capacity theorem here.

## 6. Primary sources

1. Diego Mirandola and Gilles Zémor,
   [*Critical pairs for the Product Singleton Bound*](https://arxiv.org/abs/1501.06419),
   IEEE Transactions on Information Theory **61** (2015), 4928--4937,
   [doi:10.1109/TIT.2015.2450207](https://doi.org/10.1109/TIT.2015.2450207).
   The results used above are Theorems 1.1, 2.5, and 3.3; the
   Product-MDS classification explains its additional hypotheses.

2. Hugues Randriambololona,
   [*On products and powers of linear codes under componentwise multiplication*](https://arxiv.org/abs/1312.0022),
   Contemporary Mathematics **637** (2015), 3--78,
   [doi:10.1090/conm/637/12749](https://doi.org/10.1090/conm/637/12749).
   This supplies the general code-product formalism and Product Singleton
   treatment.

3. Hugues Randriambololona,
   [*The quadratic hull of a code and the geometric view on multiplication algorithms*](https://arxiv.org/abs/1912.06627)
   (arXiv:1912.06627v3, 2020).  The definition
   \(I_2(C)=\ker(\operatorname{Sym}^2C\to C^{\langle2\rangle})\) is the
   relevant reformulation.

4. Richard M. Wilson,
   [*A diagonal form for the incidence matrices of \(t\)-subsets vs. \(k\)-subsets*](https://doi.org/10.1016/S0195-6698(13)80046-7),
   European Journal of Combinatorics **11** (1990), 609--615.

5. Rafael Plaza and Qing Xiang,
   [*Resilience of ranks of higher inclusion matrices*](https://arxiv.org/abs/1612.08124),
   Journal of Algebraic Combinatorics **48** (2018), 31--50,
   [doi:10.1007/s10801-017-0791-1](https://doi.org/10.1007/s10801-017-0791-1).
   The arbitrary-field result audited above is Theorem 4.

6. Gary R. W. Greaves, Joseph W. Iverson, John Jasper, and Dustin G. Mixon,
   [*Frames over finite fields: Equiangular lines in orthogonal geometry*](https://arxiv.org/abs/2012.13642),
   Linear Algebra and its Applications **639** (2022), 50--80,
   [doi:10.1016/j.laa.2021.11.024](https://doi.org/10.1016/j.laa.2021.11.024).
   Definitions 2.3 and 2.8 and Propositions 2.7, 2.9, and 2.10 cover tight
   Gram matrices, equiangularity, Gerzon's bound, and ETF parameters.

7. Gary R. W. Greaves, Joseph W. Iverson, John Jasper, and Dustin G. Mixon,
   [*Frames over finite fields: Basic theory and equiangular lines in unitary geometry*](https://arxiv.org/abs/2012.12977),
   Finite Fields and Their Applications **77** (2022), 101954,
   [doi:10.1016/j.ffa.2021.101954](https://doi.org/10.1016/j.ffa.2021.101954).

8. Timothy Cheek et al.,
   [*Congruence Classes of Simplex Structures in Finite Field Vector Spaces*](https://arxiv.org/abs/2408.07912)
   (arXiv:2408.07912).  This is the closest simplex-tree/gluing result located,
   but its problem and hypotheses differ as explained above.

## 7. Verification

Run:

```bash
python3 -B collaboration/schur_product_literature/verify_literature_hypotheses.py
```

The verifier checks:

* the rank and frame identities for the local \(I+J\) simplex;
* that \(H_0^{\langle2\rangle}=\mathbb F_{17}^{16}\);
* the two exact adjacent-star permutation gluings;
* all layer counts, Wilson factors, and Plaza--Xiang hypothesis failures;
* the lower bounds for \(\dim Q_D\) and the \(120\)-dimensional symmetric-square
  ceiling;
* the global tight-frame constants and trace identities;
* the residual degrees and both nonedge moment calculations; and
* the quadratic-nonresidue and conditional Gerzon conclusions.

Its final line is:

```text
ALL LITERATURE-HYPOTHESIS AND FRAME-CONSEQUENCE CHECKS PASSED
```

## 8. Boundary of the result

This audit proves neither nonexistence nor existence of either large set.  It
does not prove that \(M_D\) has complete rank after a design is deleted, bound
the stabilizer of \(U^{\langle2\rangle}\), or solve the global Gram-completion
problem.  Its positive contribution is the exact global tight-frame and
nonedge-moment condition; its negative contribution is a hypothesis-level
explanation of why the standard product-code, modular-incidence, Gerzon, and
simplex-tree results do not currently cap the required dimension \(15\).
