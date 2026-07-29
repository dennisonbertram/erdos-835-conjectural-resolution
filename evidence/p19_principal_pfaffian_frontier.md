# The \(p=19\) principal-Pfaffian rank frontier

Consider the principal-Pfaffian colouring ansatz
\[
 c(S)=\operatorname{Pf}(M[S])\in\mathbb F_{19},
 \qquad M\in\operatorname{Alt}_{36}(\mathbb F_{19}),\quad |S|=18.
\tag{1}
\]
This note proves three exact obstructions:

1. a matrix satisfying the rainbow condition cannot have rank at most \(18\);
2. the first genuinely rank-four local link cannot have its twenty
   projective rows on a normal rational curve, even with arbitrary
   independent choices of vector lifts;
3. no independent diagonal rescaling of an alternating circulant
   rank-at-most-four link works.

The last two statements exhaust natural rank-four subfamilies, not arbitrary
rank-four links.  Consequently this note does **not** rule out all matrices
of rank at least \(20\), and does not solve Erdos--Rosenfeld Problem #835.

## 1. Rank at most \(18\) is impossible

Every 17-star in (1) has nineteen colours and must contain all of
\(\mathbb F_{19}\).  In particular, some 18-Pfaffian of \(M\) is nonzero,
so
\[
 \operatorname{rank}M\ge18.
\tag{2}
\]

Suppose equality holds.  Every alternating matrix of rank \(18\) factors as
\[
 M=UJU^T,
\tag{3}
\]
where \(U\) is \(36\)-by-\(18\) of full column rank and \(J\) is an
invertible alternating \(18\)-by-\(18\) matrix.  For every 18-set \(S\),
the Pfaffian congruence identity gives
\[
 \operatorname{Pf}(M[S])
 =\operatorname{Pf}(U_SJU_S^T)
 =\det(U_S)\operatorname{Pf}(J).
\tag{4}
\]
Since \(\operatorname{Pf}(J)\ne0\), multiplying by this common scalar does
not affect whether a star is rainbow.  Thus \(G=U^T\) would be an
\(18\)-by-\(36\) matrix whose ordered maximal minors are rainbow on every
17-star.

This contradicts the exact \(p=19\) determinant-link theorem in
[`determinant_link_p19.md`](determinant_link_p19.md).  Alternating ranks are
even, so every surviving matrix in (1) must satisfy
\[
 \boxed{\operatorname{rank}M\ge20.}
\tag{5}
\]

The dependency-free checker
[`p19_rank18_pfaffian_factor_verify.py`](p19_rank18_pfaffian_factor_verify.py)
independently checks (4), including singular minors, on every maximal
minor of deterministic \(r+2\)-row examples for
\((p,r)=(3,2),(7,6),(11,10),(19,18)\).  The proof is the standard identity
\(\operatorname{Pf}(PAP^T)=\det(P)\operatorname{Pf}(A)\); the finite check
is arithmetic evidence, not its proof.

## 2. Rank \(20\) descends to a rank-four ordered link

Now suppose \(\operatorname{rank}M=20\).  A nonzero 18-Pfaffian has, by
Pfaffian expansion, a nonzero principal 16-Pfaffian.  Choose its index set
\(Q\), put \(q=\operatorname{Pf}(M[Q])\ne0\), and let \(X=[36]\setminus Q\),
so \(|X|=20\).

Take the Pfaffian Schur complement of \(M[Q]\), with the diagonal sign
correction that restores the original point order.  This produces an
alternating matrix \(B\) on \(X\) such that
\[
 \operatorname{Pf}(M[Q\cup\{i,j\}])=qB_{ij}\qquad(i<j,\ i,j\in X).
\tag{6}
\]
The rank-additivity of a Schur complement gives
\[
 \operatorname{rank}B=\operatorname{rank}M-16=4.
\tag{7}
\]
For each fixed \(i\), the original star based at \(Q\cup\{i\}\) says that
the nineteen **ordered edge labels**
\[
 \{B_{ji}:j<i\}\ \cup\ \{B_{ij}:j>i\}
\tag{8}
\]
are exactly \(\mathbb F_{19}\).  Thus rank \(20\) is the first case not
subsumed by the determinant obstruction: it demands a rank-four
alternating ordered link on twenty vertices.

## 3. Exact no-go for every lifted twisted-cubic link

For an odd prime \(p\), use the \(p+1\) standard lifts of the normal
rational curve
\[
 v_t=(1,t,t^2,t^3)\quad(t\in\mathbb F_p),\qquad
 v_\infty=(0,0,0,1).
\tag{9}
\]
Let \(J\) range over all nonzero alternating \(4\)-by-\(4\) forms, choose
arbitrary scalars \(\lambda_t\in\mathbb F_p^\times\), and put
\[
 B_{st}=(\lambda_sv_s)^T J(\lambda_tv_t).
\tag{10}
\]
This includes forms of rank four, so it is genuinely broader than the
rank-two determinant link.  Ranging over \(J\) absorbs every common
projective coordinate change, while the \(\lambda_t\) allow every choice of
nonzero lift for each of the \(p+1\) projective points.

There is an order-independent necessary test for any total ordering to
make (10) rainbow.  At every vertex the \(p\) incident labels would be
exactly \(\mathbb F_p\).  After forgetting signs, their multiplicities
must therefore be
\[
 \#0=1,\qquad \#\{\pm a\}=2
 \quad\text{for every }a\in\mathbb F_p^\times/\{\pm1\}.
\tag{11}
\]

The alternating-form space has dimension six.  Common nonzero scaling of
\(J\) preserves the rainbow property, so it is enough to normalize the
first nonzero coefficient to \(1\).  The exact number of projective forms
checked is
\[
 1+p+p^2+p^3+p^4+p^5=\frac{p^6-1}{p-1}.
\tag{12}
\]

The zero pattern in (11) is independent of the nonzero lift scalars.  For a
form with exactly one zero in every row, write the sign class of
\(\lambda_t\) as \(x_t\in\mathbb Z/((p-1)/2)\), and similarly write the
class of \(v_s^TJv_t\) as \(d_{st}\).  At vertex \(s\), the common summand
\(x_s\) only permutes all sign classes.  Thus arbitrary lift scalings can
work only if the following one-hot system has a solution:
\[
\begin{aligned}
 &z_{t,a}\in\{0,1\},\qquad \sum_a z_{t,a}=1,\\
 &\sum_{\substack{t\ne s\\v_s^TJv_t\ne0}}
     z_{t,r-d_{st}}=2
 \quad\text{for every vertex }s\text{ and class }r.
\end{aligned}
\tag{13}
\]
Adding one constant to every \(x_t\) preserves (13), so \(x_0=0\) may be
fixed.

[`p19_twisted_cubic_link_verify.cpp`](p19_twisted_cubic_link_verify.cpp)
exhausts the projective forms, builds (13) for every form with the required
zero pattern, and performs exact Gaussian elimination on its linear
relaxation.  It obtains:

| field | projective forms | one-zero forms | survive (13) mod \(3\) | unscaled pass (11) | unscaled ordered |
|---:|---:|---:|---:|---:|---:|
| \(\mathbb F_3\) | \(364\) | \(24\) | \(24\) | \(24\) | \(21\) |
| \(\mathbb F_7\) | \(19{,}608\) | \(49\) | \(49\) | \(49\) | \(0\) |
| \(\mathbb F_{11}\) | \(177{,}156\) | \(55\) | \(0\) | \(0\) | \(0\) |
| \(\mathbb F_{19}\) | \(2{,}613{,}660\) | \(171\) | \(0\) | \(0\) | \(0\) |

Every integral one-hot solution of (13) would remain a solution after
reduction modulo \(3\).  At \(p=19\), however, all 171 possible zero-pattern
forms have inconsistent linear systems over \(\mathbb F_3\), even after
discarding the one-hot integrality restriction.  Gaussian elimination over
\(\mathbb F_5\) independently eliminates the same 171 forms.  Therefore no
choices of the twenty nonzero lift scalars can work.  In particular:
\[
 \boxed{\text{No lifted normal-rational-curve rank-four link works at }p=19.}
\tag{14}
\]
For \(p=3,7\), every total order of every **unscaled** survivor of (11) is
also checked.  The \(p=3\) positive controls show that the program does not
merely reject the whole family by construction.

The normal-rational-curve qualifier in (14) is essential.  Independent
rescalings and every common projective coordinate change are covered, but
an arbitrary rank-four matrix need not have its twenty projective row
points on such a curve.

## 4. Exact no-go for every lifted circulant rank-four link

There is a second, differently structured rank-four family that can be
exhausted spectrally.  Put \(n=p+1\), index the vertices by
\(\mathbb Z/n\), and start with
\[
 C_{ij}=f(j-i),\qquad f(-d)=-f(d).
\tag{15}
\]
Thus \(C\) is alternating and circulant.  As in the curve family, allow
arbitrary independent nonzero vector lifts:
\[
 B=DCD,\qquad D=\operatorname{diag}(\lambda_0,\ldots,\lambda_p),
 \quad\lambda_i\ne0.
\tag{16}
\]

Let \(\zeta\in\mathbb F_{p^2}\) have order \(n\).  Since
\(p\equiv-1\pmod n\), Frobenius sends \(\zeta\) to \(\zeta^{-1}\).  The
Fourier eigenvalues of (15) consequently occur in pairs
\(\{a,-a\}\): alternation gives
\(\widehat f_{-a}=-\widehat f_a\), while base-field entries give
\(\widehat f_{-a}=\widehat f_a^p\).  Each nonzero pair contributes two to
the rank.  The frequencies \(0,n/2\) vanish, so a rank-at-most-four matrix
has at most two nonzero pairs among
\[
 a=1,\ldots,(p-1)/2.
\tag{17}
\]
For each pair, \(\widehat f_a^p=-\widehat f_a\), a one-dimensional
\(\mathbb F_p\)-space.  Up to common nonzero scaling, all rank-at-most-four
possibilities therefore number
\[
 h+\binom h2(p-1),\qquad h=(p-1)/2.
\tag{18}
\]

Diagonal rescaling cannot change the zero pattern.  Thus \(f(n/2)=0\) must
be the only off-diagonal zero, equivalently \(f(d)\ne0\) for
\(1\le d\le h\).  For the unscaled matrix, the differences \(d\) and
\(-d\) give the same sign class, so (11) would simply say that
\[
 [f(1)],\ldots,[f(h)]
 \quad\text{are all }h\text{ nonzero classes modulo }\{\pm1\}.
\tag{19}
\]
For arbitrary \(D\), the lift classes instead obey exactly the one-hot
system (13), now with \(d_{st}\) determined by \(f(t-s)\).

The dependency-free spectral checker
[`p19_circulant_rank4_link_verify.py`](p19_circulant_rank4_link_verify.py)
enumerates (18), directly recomputes the matrix ranks, and applies exact
bit-parallel Gaussian elimination over \(\mathbb F_3\) to the lift system:

| field | projective rank-\(\le4\) bases | one-zero bases | scaled systems surviving mod \(3\) | unscaled pass (19) | unscaled ordered |
|---:|---:|---:|---:|---:|---:|
| \(\mathbb F_3\) | \(1\) | \(1\) | \(1\) | \(1\) | \(1\) |
| \(\mathbb F_5\) | \(6\) | \(4\) | \(4\) | \(2\) | \(0\) |
| \(\mathbb F_7\) | \(21\) | \(14\) | \(0\) | \(0\) | \(0\) |
| \(\mathbb F_{11}\) | \(105\) | \(66\) | \(42\) | \(0\) | \(0\) |
| \(\mathbb F_{19}\) | \(657\) | \(380\) | \(0\) | \(0\) | \(0\) |

At \(p=19\), all 380 bases with the necessary zero pattern have
inconsistent lift systems already over \(\mathbb F_3\), without imposing
the one-hot \(0/1\) restriction.  Hence no diagonal rescaling in (16), and
therefore no total ordering, can work.  Orders are exhausted for the
unscaled small-field survivors.  The \(p=3\) ordered example is again a
genuine positive control.  The checker also compares its ternary bit-plane
elimination with brute force on 200 deterministic small linear systems.

## Reproduction

```bash
python3 -B evidence/verify_determinant_link_p19.py
python3 -B evidence/p19_rank18_pfaffian_factor_verify.py
python3 -B evidence/p19_circulant_rank4_link_verify.py
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  evidence/p19_twisted_cubic_link_verify.cpp \
  -o /tmp/p19_twisted_cubic_link_verify
/tmp/p19_twisted_cubic_link_verify
```

## Exact remaining frontier

The maximal-minor construction at \(p=19\) is fully excluded, as is every
principal-Pfaffian construction of rank at most \(18\).  At rank \(20\),
the problem becomes the unrestricted rank-four ordered-link condition
(8).  The twisted-cubic computation excludes every lift and every
alternating form on a natural projective point configuration, while the
spectral computation excludes every independently lifted circulant link of
rank at most four.
Arbitrary noncirculant projective row configurations and
principal-Pfaffian matrices of rank \(20\) or larger remain open.
