# Two-valued top-module projections for #835: complete arguments

Only fully proved statements appear in this file.  Conjectures, heuristics and
failed routes are in `IDEAS.md`.  Verdict and gap are in `STATUS.md`.

## 0. Setting and notation

Fix an even integer \(k>2\) and put

\[
 q=k+1,\qquad v=2k-1,\qquad r=k-1,\qquad
 X=\binom{[v]}{r},\qquad N=|X|=\binom{2k-1}{k-1}.
\]

Let \(O_k=KG(v,r)\) be the Odd graph: vertex set \(X\), with \(S\sim T\) iff
\(S\cap T=\varnothing\).  Its degree is \(\binom{v-r}{r}=\binom{k}{k-1}=k\).
Write \(A\) for its adjacency matrix, \(J\) for the all-ones \(N\times N\)
matrix, \(\mathbf 1\) for the all-ones vector, and \(\circ\) for the entrywise
(Schur) product.

Let \(J(v,r)\) be the Johnson scheme on \(X\), with relations \(A_0,\dots,A_r\)
(\(A_i\) = "\(|S\cap T|=r-i\)"), primitive idempotents \(E_0,\dots,E_r\),
eigenspaces \(V_i=\operatorname{col}E_i\), and multiplicities
\(m_i=\binom vi-\binom v{i-1}\).  Note \(A=A_r\).

For \(x,y,z\in\mathbb R^X\) write the triple product
\(\tau(x,y,z)=\sum_{p\in X}x_py_pz_p\).

**Lemma 0.**  \(A\) acts on \(V_i\) as \(\lambda_i=(-1)^i(k-i)\).  Since \(k\)
is even, \(\lambda_i=-1\) holds **only** for \(i=r=k-1\); that is, the
\((-1)\)-eigenspace of \(O_k\) is exactly the top Johnson module \(V_r\).

*Proof.*  The Kneser eigenvalue on \(V_i\) is
\((-1)^i\binom{v-r-i}{r-i}=(-1)^i\binom{k-i}{k-1-i}=(-1)^i(k-i)\).
Solving \((-1)^i(k-i)=-1\) with \(0\le i\le k-1\) forces \(k-i=1\) and \(i\)
odd, i.e. \(i=k-1\), which is odd because \(k\) is even.  \(\square\)

---

## 1. Theorem A (automaticity): the projection package is graph-free

**Theorem A.**  Let \(Y\) be *any* finite set with \(|Y|=N\), let \(q\mid N\),
put \(k=q-1\), and let \(\mathcal C=\{C_0,\dots,C_k\}\) be *any* partition of
\(Y\) into \(q\) classes of size \(N/q\).  Let \(R\) be its equivalence-relation
matrix, \(x_a=\mathbf 1_{C_a}\), \(y_a=x_a-q^{-1}\mathbf 1\), and

\[
 P:=\frac{qR-J}{N}.
\]

Then all of the following hold, with no reference to any graph, association
scheme, or field:

1. \(P^{\mathsf T}=P\) and every entry of \(P\) lies in \(\{k/N,\,-1/N\}\),
   with \(P_{uv}=k/N\) iff \(u,v\) share a class.
2. \(P\mathbf 1=0\).
3. \(P^2=P\); hence \(P\) is an orthogonal projector and is positive
   semidefinite.
4. \(\operatorname{tr}P=k\), so \(\operatorname{rank}P=k\).
5. \(P\) is the orthogonal projector onto \(W:=\operatorname{span}\{y_a\}\),
   and the Gram matrix of \((y_0,\dots,y_k)\) is
   \(\frac Nq\bigl(I_q-\frac1qJ_q\bigr)\) — a regular simplex.
6. \(P\circ P=\frac{k-1}{N}P+\frac{k}{N^2}J\).
7. For every integer \(m\ge1\), \(P^{\circ m}\in\operatorname{span}(P,J)\).
8. \((NP+J)/q=R\) is a \(0/1\) equivalence-relation matrix.

*Proof.*
(1) and (8) are immediate from the definition, since
\(N\cdot\frac kN+1=q\) and \(N\cdot\frac{-1}N+1=0\).

(2) Row \(u\) of \(P\) sums to \(\frac1N\bigl(q\cdot\frac Nq-N\bigr)=0\).

(3) \(R^2=\frac Nq R\), \(RJ=JR=\frac NqJ\), \(J^2=NJ\), hence
\[
 N^2P^2=q^2R^2-qRJ-qJR+J^2=qNR-2NJ+NJ=N(qR-J)=N^2P .
\]
A symmetric \(P\) with \(P^2=P\) satisfies \(x^{\mathsf T}Px=\|Px\|^2\ge0\).

(4) \(\operatorname{tr}P=N\cdot\frac kN=k\); an idempotent has rank equal to its
trace.

(5) \(Py_a=\frac1N(qRy_a-Jy_a)\).  Now \(Rx_a=\frac Nq x_a\), \(R\mathbf 1=\frac
Nq\mathbf 1\), so \(Ry_a=\frac Nq y_a\); and \(Jy_a=0\).  Hence \(Py_a=y_a\), so
\(W\subseteq\operatorname{col}P\).  Since \(\sum_ay_a=0\) and the \(y_a\) are
otherwise independent, \(\dim W=q-1=k=\operatorname{rank}P\), giving
\(W=\operatorname{col}P\).  The Gram entries are
\(\langle y_a,y_b\rangle=\delta_{ab}\frac Nq-\frac N{q^2}\).

(6)/(7) \(P\) takes exactly two values on a two-point set of values, and the
space of real functions on a two-element set is two-dimensional and spanned by
the two functions \(t\mapsto t\) and \(t\mapsto1\).  Hence every entrywise
function of \(P\) — in particular every Schur power — is of the form
\(\alpha P+\beta J\).  Solving the two linear equations for \(m=2\),
\[
 \alpha\tfrac kN+\beta=\tfrac{k^2}{N^2},\qquad
 -\tfrac\alpha N+\beta=\tfrac1{N^2},
\]
gives \(\alpha=\frac{k-1}N,\ \beta=\frac k{N^2}\).  \(\square\)

**Remark A'.**  Nothing in Theorem A uses \(q\) prime, \(k\) even, the Johnson
scheme, or the graph \(O_k\).  Items (1)–(8) are the entire list of structural
properties asserted for \(P_W\) in the attack statement, *except* for
\(AP=-P\) and \(P\in E_{r}\operatorname{Mat}E_{r}\).

---

## 2. Theorem B (converse): two-valued + idempotent forces the partition

The attack statement asks for a two-valued rank-\(k\) projection *and*
separately assumes that its \(k/N\) relation "has exactly \(q\) equivalence
classes".  That assumption is redundant.

**Theorem B.**  Let \(k\ge2\), \(q=k+1\), \(N\) a positive integer, and let
\(P\in\mathbb R^{N\times N}\) be symmetric with every entry in
\(\{k/N,-1/N\}\) and \(P^2=P\).  Define \(u\sim v\iff P_{uv}=k/N\).  Then
\(\sim\) is an equivalence relation, every class has size exactly \(N/q\)
(so \(q\mid N\) and there are exactly \(q\) classes), and \(P=(qR-J)/N\) for
the resulting equivalence matrix \(R\).  Consequently
\(\operatorname{rank}P=\operatorname{tr}P=k\) automatically.

*Proof.*
*Reflexivity.*  \(P=P^{\mathsf T}\) and \(P^2=P\) give \(P=P^{\mathsf T}P\),
so \(P_{uu}=\|Pe_u\|^2\ge0\).  As \(-1/N<0<k/N\), every diagonal entry is
\(k/N\); thus \(u\sim u\).  Symmetry is the symmetry of \(P\).

*Class size.*  Let \(d(u)=|\{x:u\sim x\}|\) (which counts \(x=u\)).  The
\((u,u)\) entry of \(P^2=P\) reads
\[
 d(u)\frac{k^2}{N^2}+\bigl(N-d(u)\bigr)\frac1{N^2}=\frac kN
 \;\Longrightarrow\;
 d(u)(k^2-1)=N(k-1)
 \;\Longrightarrow\;
 d(u)=\frac N{k+1}=\frac Nq,
\]
using \(k\ge2\), so \(k^2-1\ne0\) and \(k-1\ne 0\).

*Transitivity.*  Fix \(v\ne w\) and let
\(s=|\{x: v\sim x\text{ and }w\sim x\}|\).  Splitting the sum in the
\((v,w)\) entry of \(P^2=P\) by the four sign patterns and using
\(d(v)=d(w)=N/q\),
\[
 \sum_xP_{vx}P_{wx}
 =\frac1{N^2}\Bigl[sk^2-2k\bigl(\tfrac Nq-s\bigr)
   +\bigl(N-\tfrac{2N}q+s\bigr)\Bigr]
 =\frac{s(k+1)^2-2N\frac{k+1}{q}+N}{N^2}
 =\frac{sq^2-N}{N^2}.
\]
Setting this equal to \(P_{vw}\):

* if \(P_{vw}=k/N=(q-1)/N\) then \(sq^2=Nq\), i.e. \(s=N/q\);
* if \(P_{vw}=-1/N\) then \(sq^2=0\), i.e. \(s=0\).

Now suppose \(u\sim v\) and \(u\sim w\) with \(v\ne w\).  Then \(x=u\) witnesses
\(s\ge1\), so \(s\ne0\), so \(P_{vw}=k/N\), i.e. \(v\sim w\).

Hence \(\sim\) is an equivalence relation whose classes all have size \(N/q\);
there are therefore exactly \(q\) of them, and \(qR-J=NP\) by inspection of the
two possible entries.  \(\square\)

---

## 3. Theorem C: the exact content of the projection formulation

**Theorem C.**  Let \(k>2\) be even, \(q=k+1\), and let \(P\) be a symmetric
\(N\times N\) matrix with entries in \(\{k/N,-1/N\}\) and \(P^2=P\), where
\(N=\binom{2k-1}{k-1}\).  Then the following are equivalent:

1. \(AP=-P\);
2. \(\operatorname{col}P\subseteq V_r\) (i.e. \(P=E_rPE_r\));
3. \((A+I)R=J\), where \(R=(NP+J)/q\);
4. each class of \(R\) is a perfect \(1\)-code of \(O_k\), i.e. \(\mathcal C\)
   is a partition of \(O_k\) into \(q\) perfect codes;
5. the colouring \(u\mapsto\) class of \(u\) is a covering projection
   \(O_k\to K_q\).

*Proof.*  By Theorem B, \(P=(qR-J)/N\) for an equipartition into \(q\) classes.

\((1)\Leftrightarrow(2)\): \(\operatorname{col}P=W\) is \(A\)-invariant is not
assumed, but \(AP=-P\) says exactly that \(A\) acts as \(-1\) on
\(\operatorname{col}P\), and by Lemma 0 the \((-1)\)-eigenspace of \(A\) is
exactly \(V_r\).  Conversely if \(\operatorname{col}P\subseteq V_r\) then
\(AP=-P\).

\((1)\Leftrightarrow(3)\): \(N\,AP=qAR-kJ\) and \(-NP=-qR+J\), so \(AP=-P\) iff
\(q(AR+R)=(k+1)J=qJ\) iff \((A+I)R=J\).

\((3)\Leftrightarrow(4)\): the \((u,a)\) entry of \((A+I)R=J\) says
\(|N(u)\cap C_a|+[\,u\in C_a\,]=1\), which is precisely the statement that
every vertex has exactly one element of \(C_a\) in its closed neighbourhood.

\((4)\Leftrightarrow(5)\): \(O_k\) is \(k\)-regular and \(q=k+1\); "exactly one
element of each class in each closed ball" is the same as "the \(k\) neighbours
of \(u\) receive the \(k\) colours \(\ne c(u)\), bijectively".  \(\square\)

**Corollary C1 (route vacuity).**  The assignment
\(\mathcal C\mapsto P=(qR-J)/N\) is a bijection between

* partitions of \(X\) into \(q\) classes of size \(N/q\), and
* symmetric \(N\times N\) matrices with entries in \(\{k/N,-1/N\}\) satisfying
  \(P^2=P\),

under which "partition into \(q\) perfect codes" corresponds to \(AP=-P\).
Every other condition named in the projection formulation — rank \(k\), trace
\(k\), positive semidefiniteness, \(P\mathbf 1=0\), the two-valued Schur
identity \(P\circ P=\frac{k-1}NP+\frac k{N^2}J\), all higher Schur powers, and
the \(0/1\) equivalence-relation condition on \((NP+J)/q\) — holds identically
on both sides and therefore carries **no** information about \(O_k\).

*Proof.*  Theorem A gives one direction and Theorem B the other; the identity
statements are Theorem A(1)–(8).  \(\square\)

---

## 4. What a colour class is: perfect codes are Steiner systems

**Lemma D.**  For even \(k>2\) and \(C\subseteq X\), the following are
equivalent:

1. \(C\) is a perfect \(1\)-code of \(O_k\);
2. \(\mathbf 1_C-\frac1q\mathbf 1\in V_r\);
3. \(C\) is a Steiner system \(S(k-2,\,k-1,\,2k-1)\).

*Proof.*  Write \(\mathbf 1_C=\frac{|C|}N\mathbf 1+\sum_{i\ge1}z_i\) with
\(z_i\in V_i\).  Then
\((A+I)\mathbf 1_C=\frac{|C|(k+1)}N\mathbf 1+\sum_{i\ge1}(\lambda_i+1)z_i\).

\((1)\Leftrightarrow(2)\): \((A+I)\mathbf 1_C=\mathbf 1\) holds iff
\(|C|=N/q\) and \((\lambda_i+1)z_i=0\) for all \(i\ge1\).  By Lemma 0,
\(\lambda_i+1=0\) only at \(i=r\); hence the condition is \(z_i=0\) for
\(1\le i\le r-1\), i.e. \(\mathbf 1_C\in V_0\oplus V_r\), together with
\(|C|=N/q\).  The latter is implied by the former (take inner products with
\(\mathbf 1\): \(\langle(A+I)\mathbf 1_C,\mathbf 1\rangle=(k+1)|C|=N\)).

\((2)\Leftrightarrow(3)\): by Delsarte's characterisation, a subset of
\(\binom{[v]}{r}\) is a \(t\)-design iff its indicator has zero component in
\(V_1,\dots,V_t\).  So (2) says exactly that \(C\) is a \((k-2)\)-design with
\(|C|=N/q\).  Its index at \(t=k-2\) is
\[
 \lambda=\frac{|C|\binom{k-1}{k-2}}{\binom{2k-1}{k-2}}
 =\frac{N}{k+1}\cdot\frac{k-1}{\binom{2k-1}{k-1}\frac{k-1}{k+1}}=1,
\]
using \(\binom{2k-1}{k-2}=\binom{2k-1}{k-1}\frac{k-1}{k+1}\).  Conversely an
\(S(k-2,k-1,2k-1)\) is a \((k-2)\)-design with
\(|C|=\binom{2k-1}{k-2}/(k-1)=N/(k+1)\).  \(\square\)

**Corollary D1.**  A covering projection \(O_k\to K_{k+1}\) is exactly a large
set \(LS(k-2,k-1,2k-1)\).  In particular the projection formulation is the
perfect-code / large-set formulation already committed in
`erdos_835_conjectural_resolution.md` §4, not a new object.

---

## 5. A basic Schur–Krein support test, and why that test is blind

### 5.1 A vanishing criterion

**Lemma E (standard; proof included).**  In a symmetric commutative
association scheme on \(X\) with primitive idempotents \(E_i\), multiplicities
\(m_i\) and Krein parameters defined by
\(E_i\circ E_j=\frac1{|X|}\sum_l q^l_{ij}E_l\), fix orthonormal bases
\(\{w^i_a\}\) of \(V_i\).  Then

\[
 \frac{m_l}{|X|}\,q^l_{ij}
 =\sum_{a,b,c}\tau\bigl(w^i_a,w^j_b,w^l_c\bigr)^2 .
\]

In particular \(q^l_{ij}\ge0\), and \(q^l_{ij}=0\) iff \(\tau\) vanishes
identically on \(V_i\times V_j\times V_l\).

*Proof.*  Using \((E_i)_{uv}=\sum_a(w^i_a)_u(w^i_a)_v\),
\[
 \operatorname{tr}\bigl((E_i\circ E_j)E_l\bigr)
 =\sum_{u,v}(E_i)_{uv}(E_j)_{uv}(E_l)_{uv}
 =\sum_{a,b,c}\Bigl(\sum_u (w^i_a)_u(w^j_b)_u(w^l_c)_u\Bigr)^{2},
\]
while the defining relation gives
\(\operatorname{tr}((E_i\circ E_j)E_l)=\frac{q^l_{ij}}{|X|}\operatorname{tr}E_l
=\frac{q^l_{ij}m_l}{|X|}\).  \(\square\)

### 5.2 A necessary condition derived from the two-valued Schur identity

**Proposition F.**  If a partition of \(O_k\) into \(q\) perfect codes exists,
then the Johnson scheme \(J(2k-1,k-1)\) satisfies \(q^{\,r}_{rr}\ne0\)
(\(r=k-1\)).

*Proof.*  Let \(P\) be the associated projector, \(W=\operatorname{col}P\subseteq
V_r\) (Theorem C), \(\dim W=k\ge1\), and let \(w_1,\dots,w_k\) be an
orthonormal basis of \(W\).  Then \(P=\sum_iw_iw_i^{\mathsf T}\) and
\[
 P\circ P=\sum_{i,j}(w_iw_i^{\mathsf T})\circ(w_jw_j^{\mathsf T})
 =\sum_{i,j}(w_i\circ w_j)(w_i\circ w_j)^{\mathsf T},
\]
so \(\operatorname{col}(P\circ P)\subseteq\operatorname{span}\{w_i\circ w_j\}\).
By Theorem A(6), \(P\circ P=\frac{k-1}NP+\frac k{N^2}J\), whose column space is
\(W\oplus\langle\mathbf 1\rangle\) because \(k-1\ne0\), \(k\ne 0\) and
\(W\perp\mathbf 1\).  Pick \(0\ne z\in W\); writing
\(z=\sum_{i,j}c_{ij}(w_i\circ w_j)\) and pairing with \(z\) gives
\(\sum_{i,j}c_{ij}\tau(w_i,w_j,z)=\|z\|^2\ne0\), so some
\(\tau(w_i,w_j,z)\ne0\) with all three arguments in \(V_r\).  By Lemma E,
\(q^r_{rr}\ne0\).  \(\square\)

### 5.3 Theorem G: the basic Krein support test cannot decide a case

**Theorem G.**  For every even \(k>2\), the necessary condition of
Proposition F is satisfied whenever it is not vacuous.  Precisely:

* if no \(S(k-2,k-1,2k-1)\) exists, then no partition of \(O_k\) into perfect
  codes exists for the trivial reason that no single perfect code exists
  (Lemma D), so Proposition F is not needed;
* if an \(S(k-2,k-1,2k-1)\) exists, then \(q^r_{rr}>0\).

Hence Proposition F never rules out a value of \(k\) that the existence of a
single constituent Steiner system leaves open.

*Proof.*  Suppose \(C\) is an \(S(k-2,k-1,2k-1)\).  By Lemma D,
\(y:=\mathbf 1_C-\frac1q\mathbf 1\in V_r\), and \(|C|=N/q\).  Then
\[
 \tau(y,y,y)=\frac Nq\Bigl(1-\frac1q\Bigr)^{3}
 +\Bigl(N-\frac Nq\Bigr)\Bigl(-\frac1q\Bigr)^{3}
 =\frac{N(q-1)}{q^{4}}\bigl[(q-1)^{2}-1\bigr]
 =\frac{N(q-1)(q-2)}{q^{3}} .
\]
For \(k>2\) we have \(q=k+1\ge5\), so \(\tau(y,y,y)>0\); thus \(\tau\) does not
vanish identically on \(V_r\times V_r\times V_r\), and Lemma E gives
\(q^r_{rr}>0\).  \(\square\)

**Remark G'.**  Theorem G is the precise sense in which this **single scalar
Krein-support test** is blind to the distinction between one perfect code and
a partition into \(q\) perfect codes: a single constituent already supplies
the nonzero triple product needed to show \(q^r_{rr}>0\).  It does not show
that all Schur, Terwilliger, or semidefinite constraints on a \(k\)-dimensional
simplex subspace are blind.  The \(k=6\) control is exact for this scalar test:
\(S(4,5,11)\) exists, so \(q^{5}_{55}>0\) for \(J(11,5)\), while no
\(LS(4,5,11)\) exists.  The same holds at \(k=4\) with the Fano plane
\(S(2,3,7)\) and \(J(7,3)\).

### 5.4 The cubic normal form on \(W\)

**Proposition H.**  With \(y_a\) as in Theorem A, let \(y=\sum_at_ay_a\) with
\(\sum_at_a=0\).  Then

\[
 \|y\|^2=\frac Nq\sum_at_a^2,
 \qquad
 \tau(y,y,y)=\frac Nq\sum_at_a^3 .
\]

That is, the ambient invariant quadratic and cubic forms restrict to \(W\) as
\(\frac Nq\) times the standard \(A_{q-1}\) forms on \(\{t:\sum t_a=0\}\).

*Proof.*  The quadratic statement is Theorem A(5).  For the cubic, direct
evaluation of \(\tau(y_a,y_b,y_c)\) by cases (using that the \(C_a\) are
disjoint and of size \(N/q\)) gives
\(\tau(y_a,y_b,y_c)=\frac N{q^3}g_{abc}\) with
\[
 g_{abc}=q^2\delta_{abc}-q(\delta_{ab}+\delta_{bc}+\delta_{ca})+2 ,
\]
i.e. \((q-1)(q-2)\) if \(a=b=c\), \(2-q\) if exactly two indices agree, and
\(2\) otherwise.  Substituting and using \(\sum_at_a=0\) kills the last two
groups of terms and leaves \(\frac N{q^3}\cdot q^2\sum_at_a^3\).  \(\square\)

**Remark H'.**  Proposition H is graph-free once an equipartition is given,
but embedding such a \(k\)-dimensional simplex subspace **inside \(V_r\)** is
not graph-free.  Theorem B says that a two-valued idempotent already comes from
an equipartition; it does not rule out an obstruction obtained from the
orientation of that subspace inside \(V_r\), nor from stronger Schur,
Terwilliger, or semidefinite constraints.  Thus the displayed cubic normal
form is a necessary condition whose further strength is unresolved here.

---

## 6. Comparison with the two-equitable-partition lemma

**Lemma I.**  Let \(\Gamma\) be a regular graph on \(n\) vertices with adjacency
matrix \(A\) and spectral projectors \(\{\pi_\theta\}\).  For a partition
\(\Pi\) put \(U_\Pi=\operatorname{span}\{\mathbf 1_Q:Q\in\Pi\}\); if \(\Pi\) is
equitable then \(U_\Pi\) is \(A\)-invariant and its eigenvalue support
\(\operatorname{supp}\Pi\) equals the spectrum of the quotient matrix of
\(\Pi\).  For equitable partitions \(\Pi_1,\Pi_2\) and cells \(P\in\Pi_1\),
\(Q\in\Pi_2\),

\[
 |P\cap Q|=\frac{|P||Q|}{n}
 +\sum_{\theta\in(\operatorname{supp}\Pi_1\cap\operatorname{supp}\Pi_2)
      \setminus\{\theta_0\}}
   \bigl\langle \pi_\theta\mathbf 1_P,\ \pi_\theta\mathbf 1_Q\bigr\rangle,
\]

where \(\theta_0\) is the degree.  In particular, if
\(\operatorname{supp}\Pi_1\cap\operatorname{supp}\Pi_2=\{\theta_0\}\) then
\(|P\cap Q|=|P||Q|/n\) exactly.

*Proof.*  \(|P\cap Q|=\langle\mathbf 1_P,\mathbf 1_Q\rangle
=\sum_\theta\langle\pi_\theta\mathbf 1_P,\pi_\theta\mathbf 1_Q\rangle\); the
\(\theta_0\) term is \(|P||Q|/n\); and \(\pi_\theta\mathbf 1_P=0\) for
\(\theta\notin\operatorname{supp}\Pi_1\), likewise for \(\Pi_2\).  \(\square\)

**Corollary I1.**  Let \(\Pi_1\) be a partition of \(O_k\) into \(q\) perfect
codes.  Its quotient matrix is \(J_q-I_q\), so
\(\operatorname{supp}\Pi_1=\{k,-1\}\) and, by Lemma 0, its non-trivial
eigenspace is exactly \(V_r\).  Hence for any equitable partition \(\Pi_2\) of
\(O_k\) with \(-1\notin\operatorname{supp}\Pi_2\) and any cell \(Q\in\Pi_2\),
\(|C_a\cap Q|=|Q|/q\) for every colour \(a\).

**Corollary I2 (the comparison is not stronger than design quadrature).**  The
committed design-quadrature condition is: \(\mathbf 1_{C_a}\in V_0\oplus V_r\)
(Lemma D), hence
\(\langle\mathbf 1_{C_a},z\rangle=\frac1q\langle\mathbf 1,z\rangle\) for
**every** \(z\in\mathbb R^X\) with \(\pi_{V_r}z=0\).  Corollary I1 is the
special case \(z=\mathbf 1_Q\) for \(Q\) a cell of an equitable partition whose
support misses \(-1\).  The set of such \(z\) is a subset of
\(\{z:\pi_{V_r}z=0\}\), so the two-equitable-partition comparison yields a
subset of the linear conditions already implied by design quadrature, never a
strictly stronger one.

**Provenance note.**  I was unable to retrieve arXiv:2605.17376
(Bailey–Cameron–Zhou) in this session: network access was not available.
Lemma I and Corollaries I1/I2 are proved here from scratch and are the standard
spectral comparison of two equitable partitions.  A later independent audit
retrieved the paper.  Its Corollary 2.4(a), specialised to a perfect code,
contains the same quotient-eigenspace condition as Corollary I1.  Its full
Theorem 2.3 and Corollary 2.4(b), however, are stated through the more general
systems (6)--(8).  Therefore I2 closes only the cell-indicator spectral
specialisation proved here; it does **not** by itself close every condition in
Theorem 2.3/Corollary 2.4.  See `INDEPENDENT_AUDIT.md`.

---

## 7. Statements that are *not* proved here

Listed so nothing above is over-read:

* No nonexistence result for any \(k\) is proved here.  Theorems A–C and G are
  statements about the *method*, not about \(O_k\).
* Proposition F is a genuine necessary condition, but Theorem G proves it is
  never decisive; no value of \(k\) is eliminated by it.
* The nonexistence of \(LS(2,3,7)\) and \(LS(4,5,11)\) is used only as a
  control and is quoted as classical, not proved here.
* The verifier `verify_projection_rigidity.py` was **not executed by Opus** in
  this session (Python execution was not permitted).  It was subsequently run
  by the independent audit with zero failures.  Nothing in §§1–6 depends on
  it; see `INDEPENDENT_AUDIT.md` for the exact result and scope.
