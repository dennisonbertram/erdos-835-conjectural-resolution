# Norton-compression audit

This note tests a tempting spectral attack on a hypothetical large set
\(LS(r-1,r,2r+1)\), especially the unresolved target
\[
 r=15,\qquad q=r+2=17.
\]
The attack begins with a striking exact pattern in the Fano and Witt
controls: a natural compression of the top Johnson projector has only the
three eigenvalues
\[
 0,\qquad \frac13,\qquad \frac{q-1}{q}.
\]
If that pattern persisted at \(q=17\), it would prove nonexistence
immediately.  It does **not** follow from the currently available universal
identities.  The first two moments already make the extrapolated spectrum
impossible, while the first new trace order, the cubic trace, depends on
genuine three-block data.

The final section gives a rank-correct abstract compression model satisfying
all axis, partition-of-unity, Naimark-rank, trace, and pair-moment constraints
at \(q=17\), but having eigenvalues \(1/6\) and \(1/9\).  Thus this route
needs a new theorem using the actual Johnson kernel or the full coloured
three-block tensor.  Low-order Norton/fusion-frame identities alone do not
settle Erdős problem 835.

## 1. Axes and compression operators

Put
\[
 X=\binom{[2r+1]}r,\qquad N=|X|,\qquad
 W=W_{r-1,r}(2r+1),
\]
and let \(P\) be the orthogonal projector onto
\[
 E=\ker W,\qquad \dim E=\frac{2N}{q}.
\]
If \(D_i\) is one constituent Steiner system, write \(f_i\) for its
indicator, \(F_i=\operatorname{diag}(f_i)\), and
\[
 n=|D_i|=\frac Nq,\qquad
 y_i=f_i-\frac1q\mathbf1.
\]
The Steiner equations say \(Wf_i=\mathbf1\) and
\(W\mathbf1=q\mathbf1\), hence \(y_i\in E\).  For a large set,
\[
 \sum_{i=0}^{q-1}y_i=0,\qquad
 \langle y_i,y_j\rangle
 =n\left(\delta_{ij}-\frac1q\right).
\]

The Norton product on \(E\) is
\[
 x*y=P(x\mathbin{\circ}y).
\]
The two-level coordinates of the \(y_i\) give, without any spectral
assumption,
\[
 y_i*y_i=\left(1-\frac2q\right)y_i,\qquad
 y_i*y_j=-\frac1q(y_i+y_j)\quad(i\ne j).
\]
Define the positive compression
\[
 T_i=P F_iP=M_{y_i}+\frac1qI_E.
\]
Then
\[
 0\preceq T_i\preceq I,\qquad
 \sum_iT_i=I,\qquad
 \operatorname{rank}T_i\le n.
\]

Let \(Y=\langle y_0,\ldots,y_{q-1}\rangle\), so \(\dim Y=q-1\).
This is a common invariant subspace, and
\[
 T_i|_Y=\frac1n\,y_i\otimes y_i.
\]
Consequently \(T_i|_Y\) has eigenvalue
\[
 h=\frac{q-1}{q}
\]
once and eigenvalue \(0\) with multiplicity \(q-2\).  On \(Y\),
\[
 \operatorname{tr}(T_iT_j)=\frac1{q^2}\quad(i\ne j).
\]
All of these statements are forced by the large-set equations.

## 2. The exact top-projector kernel

For \(A,B\in X\), the entry \(P_{A,B}\) depends only on
\(t=|A\cap B|\).  Write this value as \(p_t\).  Summing a projector column
over the \(r\)-sets containing a fixed \((r-1)\)-set gives the recurrence
\[
 (r-t)p_{t+1}+(t+2)p_t=0.
\]
Since the diagonal is
\[
 p_r=\frac{\dim E}{N}=\frac2q,
\]
the recurrence gives
\[
 \boxed{\displaystyle
 p_t=(-1)^{r-t}\frac{2}{q\binom{r+1}{t+1}}.}
\tag{2.1}
\]

Fix a block \(B\in D_i\).  Let \(a_t\) count the blocks
\(C\in D_i\) with \(|B\cap C|=t\).  If \(j\ne i\), let \(b_t\) count
the blocks \(C\in D_j\) with the same intersection size.  The Steiner
equations give the triangular systems
\[
 \sum_t\binom ts a_t
 =\binom rs\lambda_s,\qquad
 \sum_t\binom ts b_t
 =\binom rs\lambda_s
 \quad(0\le s<r),
\tag{2.2}
\]
where
\[
 \lambda_s=\frac{\binom{2r+1-s}{r-1-s}}{r-s},
\]
with boundary values \(a_r=1\) and \(b_r=0\).  Thus every one- and
two-constituent intersection distribution is forced.

Equations (2.1)--(2.2) imply
\[
 \operatorname{tr}T_i=\frac{2n}{q},
\tag{2.3}
\]
\[
 \boxed{\displaystyle
 \operatorname{tr}T_i^2
 =n\sum_ta_tp_t^2
 =\frac{2n(3q-1)}{q^2(q+1)},}
\tag{2.4}
\]
and, for \(i\ne j\),
\[
 \operatorname{tr}(T_iT_j)
 =n\sum_tb_tp_t^2
 =\frac{\operatorname{tr}T_i-\operatorname{tr}T_i^2}{q-1}.
\tag{2.5}
\]
The closed form in (2.4) follows by binomial inversion in (2.2);
the unsimplified finite sum is also an exact proof and is reproduced by the
verifier.

At the three parameters of interest these moments are
\[
\begin{array}{c|c|c|c}
r&q&\operatorname{tr}T_i^2&
  \operatorname{tr}(T_iT_j),\ i\ne j\\ \hline
3&5&98/75&28/75\\
5&7&330/49&99/49\\
15&17&98\,215\,750/289&31\,429\,040/289.
\end{array}
\]

## 3. The exact small-case cubic

Let \(K_i=F_iPF_i\) restricted to the \(n\) coordinates of \(D_i\).
The nonzero eigenvalues of \(K_i\) and \(T_i\) coincide.  For the
canonical Fano plane at \(r=3\), exact integer matrix multiplication gives
\[
 K_i\left(K_i-\frac13I\right)
 \left(K_i-\frac45I\right)=0
\]
and
\[
 \operatorname{Spec}(T_i)
 =\{0^7,(1/3)^6,(4/5)^1\}.
\]
For the canonical Witt \(S(4,5,11)\) at \(r=5\), it gives
\[
 K_i\left(K_i-\frac13I\right)
 \left(K_i-\frac67I\right)=0
\]
and
\[
 \operatorname{Spec}(T_i)
 =\{0^{77},(1/3)^{54},(6/7)^1\}.
\]
These are exact polynomial identities, not numerical eigensolver output.

Now suppose, only as an extrapolation, that the roots at general \(q\)
were \(0,1/3,h\).  Let \(a\) and \(b\) be the multiplicities of \(1/3\)
and \(h\).  The universal first two moments force
\[
 \frac a3+bh=\operatorname{tr}T_i,\qquad
 \frac a9+bh^2=\operatorname{tr}T_i^2.
\]
In particular,
\[
 \boxed{\displaystyle
 b=\frac{2n(-q^2+8q-3)}
 {(q+1)(q-1)(2q-3)}.}
\tag{3.1}
\]
This is \(1\) at \(q=5,7\), but it is negative for every \(q\ge9\).
At the target,
\[
 b=-\frac{2\,471\,235}{4},\qquad
 a=7\,983\,990.
\]
Therefore:

> **Exact conditional obstruction.**  No \(S(14,15,31)\) constituent can
> have a top-projector compression satisfying
> \[
> T_i(T_i-\tfrac13I)(T_i-\tfrac{16}{17}I)=0.
> \]

What is missing is a proof of that polynomial from the Steiner or large-set
axioms.  The two small controls do not supply one.

## 4. The first genuinely new trace order

The first two traces are one- and two-block sums.  The next trace is
\[
 \operatorname{tr}T_i^3
 =\sum_{A,B,C\in D_i}
 p_{|A\cap B|}p_{|B\cap C|}p_{|C\cap A|}.
\tag{4.1}
\]
Thus order three introduces the tensor
\[
 N_{abc}^{\,ijk}
 =\#\{(A,B,C)\in D_i\times D_j\times D_k:
 |A\cap B|=a,\ |B\cap C|=b,\ |C\cap A|=c\}.
\]
Equations (2.2) determine its two-dimensional marginals, not its full
three-block correlations.  Large-set orthogonality gives the aggregate
relations
\[
 \sum_k\operatorname{tr}(T_iT_jT_k)
 =\operatorname{tr}(T_iT_j)
\]
and
\[
 \operatorname{tr}T_i^3+
 \sum_{j\ne i}\operatorname{tr}(T_i^2T_j)
 =\operatorname{tr}T_i^2,
\]
but these do not determine the individual cubic terms.

This is the precise breakpoint:

* orders one and two are universal consequences of the fixed-block
  Steiner equations;
* the small-case degree-three matrix identity is stronger than those
  moments;
* at order three, the direct trace expansion first asks for information
  about triples of blocks.

This does not prove that no deeper Steiner theorem can control (4.1).
It identifies exactly what such a theorem would have to add.

## 5. A rank-correct abstract compression model at \(q=17\)

A useful no-go audit must retain the genuine bound
\(\operatorname{rank}T_i\le n\).  The following exact model does.

Decompose an abstract Euclidean space as
\[
 E_{\rm abs}=Y\mathbin{\perp}Z,\qquad
 \dim Y=16,\qquad \dim Z=35\,357\,654.
\]
On \(Y\), use the forced regular-simplex operators
\[
 T_i^Y=\frac1n y_i\otimes y_i.
\]
On \(Z\), use a diagonal construction indexed by a multiset of subsets of
the seventeen colours:

* \(x=33\,277\,568\) coordinates are supported on a \(6\)-subset, with
  value \(1/6\) on each supported colour;
* \(y=2\,080\,086\) coordinates are supported on a \(9\)-subset, with
  value \(1/9\) on each supported colour.

The supporting subsets can be chosen as explicit 2-design multisets.
Identify the colours with \(\mathbb F_{17}\).

* The \(\operatorname{AGL}(1,17)\)-orbit of
  \(\{0,1,2,3,4,6\}\) has 272 blocks and parameters
  \(2\text{-}(17,6,30)\).  Repeat it \(122\,344\) times.
* If \(Q\) is the set of nonzero quadratic residues, the affine orbit of
  \(\{0\}\cup Q\) has 34 blocks and parameters
  \(2\text{-}(17,9,9)\).  Repeat it \(61\,179\) times.

For a coordinate supported on \(B\), define
\[
 T_i^Ze_B=
 \begin{cases}
 |B|^{-1}e_B,&i\in B,\\
 0,&i\notin B.
 \end{cases}
\]
Every coordinate sums to one, so \(\sum_iT_i^Z=I_Z\).  The exact
per-colour multiplicities are
\[
 m_{1/6}=11\,745\,024,\qquad
 m_{1/9}=1\,101\,222.
\]
The pair replication numbers are
\[
 \lambda_6=3\,670\,320,\qquad
 \lambda_9=550\,611.
\]
Consequently the \(Z\)-part has
\[
\operatorname{tr}T_i^Z=2\,079\,862,\qquad
\operatorname{tr}(T_i^Z)^2=339\,846,\qquad
\operatorname{tr}(T_i^ZT_j^Z)=108\,751.
\]
Adding the forced \(Y\)-part reproduces (2.3)--(2.5) exactly.

Each full operator has spectrum
\[
\boxed{\displaystyle
\{0^{22\,511\,423},
(1/9)^{1\,101\,222},
(1/6)^{11\,745\,024},
(16/17)^1\}.}
\tag{5.1}
\]
In particular,
\[
\operatorname{rank}T_i=12\,846\,247
<17\,678\,835=n.
\]
Thus the model respects the compression rank bound and deliberately fails
the small-case cubic.

It also has a genuine Naimark realization.  Since the \(T_i\) are positive,
sum to \(I\), and each has rank at most \(n\), choose
\[
 U_i:E_{\rm abs}\longrightarrow\mathbb R^n,\qquad
 U_i^*U_i=T_i,
\]
and stack the \(U_i\) to an isometry \(U\).  The rank-one \(Y\)-part may be
placed in the constant line of each \(\mathbb R^n\), and the \(Z\)-part in
its orthogonal complement.  Then, with \(P_{\rm abs}=UU^*\) and \(F_i\)
the \(i\)-th block-coordinate projection,
\[
 U^*F_iU=T_i.
\]
Moreover the block indicator \(f_i\) satisfies
\[
 P_{\rm abs}f_i=f_i-\frac1{17}\mathbf1=Uy_i.
\]
So the model obeys the same indicator-axis relations and every general
identity coming from a partition into coordinate fibres.  What it does
not reproduce is the special Johnson entry kernel (2.1).

Finally, its cubic data visibly contains new information.  In the two
affine orbits above, the triples
\[
 \{0,1,2\},\quad\{0,1,3\},\quad\{0,1,4\}
\]
occur respectively
\[
 (12,5),\quad(8,4),\quad(6,4)
\]
times in the \(6\)- and \(9\)-block base orbits.  Hence the corresponding
mixed cubic traces are three distinct rational numbers despite identical
one- and two-colour data.

## 6. Verdict

The Norton calculation produces a clean conditional route:

> prove the Fano/Witt cubic fusion law for every constituent of a large
> set, and the target is impossible by the negative multiplicity (3.1).

At present that fusion law is an empirical low-parameter phenomenon, not
a theorem.  The exact model in Section 5 shows that axis multiplication,
positivity, the partition of unity, the true rank bound, and every universal
pair moment still leave enough room at \(q=17\).  A successful continuation
must use the actual Johnson kernel at cubic order or stronger coloured
Steiner correlations.

Reproduce every numerical statement with:

```bash
python3 evidence/verify_norton_algebra.py
```
