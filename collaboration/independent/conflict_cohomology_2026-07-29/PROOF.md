# The exact \(\mathbf F_2\) cochain form of the last-two-system obstruction

Date: 2026-07-29.

## 1. Scope and verdict

This note proves an exact reformulation of the last-two-system
bipartiteness test.  It also identifies precisely what complement closure
does, and does not do, at the top rung.

The reformulation is an **equivalence**, not by itself a new obstruction.
At the top rung it says that an obstruction is exactly an odd binary Steiner
trade on the complemented deleted systems, or equivalently the failure of a
common odd-transversal problem.  Every single elementary cochain star has
two residual blocks, and complement closure makes the elementary global
parities consistent; neither fact decides whether a larger odd cocycle
exists.

Consequently this note does **not** solve Erdős--Rosenfeld Problem #835.

Throughout, \(X\) is an \(n\)-point set,

\[
 n=t+p,\qquad p\ \hbox{odd},
\]

and

\[
 {\cal D}_1,\ldots,{\cal D}_{p-2}
\]

are pairwise block-disjoint \(S(t,t+1,n)\)'s.  Put

\[
 {\cal D}:=\bigcup_{i=1}^{p-2}{\cal D}_i,\qquad
 {\cal E}:=\binom X{t+1}\setminus{\cal D}.
\]

Every \(t\)-set lies in exactly two blocks of \({\cal E}\).

All vector spaces and matrices below are over \(\mathbf F_2\).

## 2. The affine system and its dual

Let \(H_{\cal E}\) have rows indexed by \(\binom Xt\), columns indexed by
\({\cal E}\), and entries

\[
 H_{\cal E}(T,B)=1\quad\Longleftrightarrow\quad T\subset B.
\]

Every row has exactly two ones.  The two columns in that row are the
endpoints of the edge of the residual conflict graph indexed by \(T\).

### Theorem 2.1 (affine and dual forms)

The following are equivalent.

1. The residual conflict graph \(G_{\cal E}\) is bipartite.
2. The affine system
   \[
   H_{\cal E}x={\bf 1}
   \tag{2.1}
   \]
   is soluble.
3. Every \(z\in\ker H_{\cal E}^{\mathsf T}\) has even weight:
   \[
   \langle z,{\bf 1}\rangle=0.
   \tag{2.2}
   \]

#### Proof

A vector \(x\) assigns a bit to every residual block.  The row of (2.1)
indexed by \(T\) says that the two residual extensions of \(T\) receive
opposite bits.  Thus (2.1) is exactly a proper two-colouring of
\(G_{\cal E}\), proving \(1\Longleftrightarrow2\).

A linear system \(Hu=b\) over a field is soluble exactly when \(b\) is
orthogonal to the left kernel:

\[
 b\in\operatorname{col}H
 \quad\Longleftrightarrow\quad
 \langle z,b\rangle=0\quad
 \hbox{for every }z\in\ker H^{\mathsf T}.
\]

Apply this with \(b={\bf1}\).  This proves
\(2\Longleftrightarrow3\). \(\square\)

There is also a useful graph interpretation.  A vector \(z\) selects edges
of \(G_{\cal E}\).  The equation \(H_{\cal E}^{\mathsf T}z=0\) says that
every residual vertex has even selected degree.  Hence the left kernel is
the cycle space.  Such an Eulerian edge set has odd cardinality if and only
if its cycle decomposition contains an odd cycle.  Thus (2.2) is literally
the usual odd-cycle criterion, written linearly.

## 3. Simplex exactness

For \(0\le s<n\), let \(C_s\) be the space of functions on the \(s\)-subsets
of \(X\), and define

\[
 \delta_s:C_s\longrightarrow C_{s+1},\qquad
 (\delta_s f)(B):=
 \sum_{\substack{A\subset B\\|A|=s}}f(A).
\]

Over \(\mathbf F_2\),

\[
 \delta_{s+1}\delta_s=0,
\tag{3.1}
\]

because each \(s\)-set in an \((s+2)\)-set has exactly two intermediate
\((s+1)\)-sets.

### Lemma 3.1 (exactness of the full simplex)

For \(1\le s<n\),

\[
 \ker\delta_s=\operatorname{im}\delta_{s-1}.
\tag{3.2}
\]

#### Proof

Inclusion from right to left is (3.1).  Conversely, let
\(y\in C_s\) satisfy \(\delta_s y=0\), and fix \(a\in X\).  Define
\(z\in C_{s-1}\) by

\[
 z(A)=
 \begin{cases}
 y(A\cup\{a\}),&a\notin A,\\
 0,&a\in A.
 \end{cases}
\]

If \(a\in B\in\binom Xs\), only the facet \(B\setminus\{a\}\) contributes
to \((\delta z)(B)\), and the answer is \(y(B)\).  If \(a\notin B\), then

\[
 (\delta z)(B)
 =\sum_{b\in B}y((B\setminus\{b\})\cup\{a\})
 =y(B),
\]

where the last equality is \((\delta y)(B\cup\{a\})=0\).
Thus \(\delta z=y\). \(\square\)

## 4. The deleted-block incidence matrix

Let \(M_{\cal D}\) have rows indexed by \(\binom X{t+2}\), columns indexed by
\({\cal D}\), and entries

\[
 M_{\cal D}(F,B)=1\quad\Longleftrightarrow\quad B\subset F.
\tag{4.1}
\]

Equivalently, extend a vector \(y\in\mathbf F_2^{\cal D}\) by zero to all
\((t+1)\)-sets.  Then

\[
 M_{\cal D}y=0
\quad\Longleftrightarrow\quad
\delta_{t+1}y=0.
\tag{4.2}
\]

### Theorem 4.1 (exact cochain/row-space reformulation)

The map

\[
 z\longmapsto y:=\delta_tz
\tag{4.3}
\]

sends \(\ker H_{\cal E}^{\mathsf T}\) onto
\(\ker M_{\cal D}\), with \(y\) regarded as supported on \({\cal D}\).
Moreover

\[
 |y|\equiv |z|\pmod2.
\tag{4.4}
\]

Consequently the following are equivalent:

1. \(G_{\cal E}\) is bipartite;
2. every \(y\in\ker M_{\cal D}\) has even weight;
3. the all-one vector on the deleted blocks belongs to the row space:
   \[
   {\bf1}_{\cal D}\in\operatorname{row}M_{\cal D}.
   \tag{4.5}
   \]

#### Proof

For a \((t+1)\)-block \(B\),

\[
 (\delta_tz)(B)
 =\sum_{\substack{T\subset B\\|T|=t}}z(T)
 =(H_{\cal E}^{\mathsf T}z)(B)
\]

when \(B\in{\cal E}\).  Hence \(H_{\cal E}^{\mathsf T}z=0\) exactly says
that \(\delta z\) vanishes on \({\cal E}\), so \(y=\delta z\) is supported
on \({\cal D}\).  Equation (3.1) then gives \(M_{\cal D}y=0\).

Conversely, take \(y\in\ker M_{\cal D}\), extend it by zero on \({\cal E}\),
and use (4.2).  Lemma 3.1 supplies \(z\in C_t\) with \(\delta_tz=y\).
Since \(y\) vanishes on \({\cal E}\), this \(z\) lies in
\(\ker H_{\cal E}^{\mathsf T}\).  Thus (4.3) is onto.

For parity, sum \(\delta_tz\) over every \((t+1)\)-set.  Each \(t\)-set is
counted in exactly \(n-t=p\) extensions.  Therefore

\[
 \langle\delta_tz,{\bf1}\rangle
 =(n-t)\langle z,{\bf1}\rangle
 =p\langle z,{\bf1}\rangle
 =\langle z,{\bf1}\rangle
\]

in \(\mathbf F_2\), because \(p\) is odd.  This proves (4.4).

Theorem 2.1 and surjectivity with parity preservation prove the equivalence
of \(1\) and \(2\).  Finally,

\[
 \operatorname{row}M_{\cal D}
 =(\ker M_{\cal D})^\perp.
\]

Thus \({\bf1}_{\cal D}\) is in the row space exactly when it is orthogonal
to every kernel vector, which is exactly condition \(2\). \(\square\)

### Corollary 4.2 (odd cycles are odd deleted trades)

An obstruction is exactly an odd vector \(y\) supported on deleted blocks
such that every \((t+2)\)-set contains an even number of selected deleted
blocks.

Equivalently, it is an odd cochain cocycle supported on \({\cal D}\).
Under (4.3), odd residual cycles and odd deleted cocycles correspond
surjectively and with the same parity.  This upward-incidence condition is
not, in general, the usual downward-incidence definition of a Steiner
trade.  At the top rung, complementation converts it into exactly such a
binary trade; see Theorem 6.2.

This is a genuine certificate format, but not a parameter-only obstruction:
finding such a cocycle is equivalent to finding the odd residual cycle one
started with.

### Corollary 4.3 (exact rank formula)

There is a short exact sequence

\[
0\longrightarrow\ker\delta_t
\longrightarrow\ker H_{\cal E}^{\mathsf T}
\mathrel{\mathop{\longrightarrow}^{\delta_t}}
\ker M_{\cal D}\longrightarrow0.
\tag{4.6}
\]

If \(c(G_{\cal E})\) is the number of connected components of the residual
graph, then

\[
\boxed{\operatorname{rank}_{2}M_{\cal D}
=\binom{n-1}{t+1}-c(G_{\cal E}).}
\tag{4.7}
\]

#### Proof

Surjectivity in (4.6) is Theorem 4.1, and its kernel is exactly
\(\ker\delta_t\).

Exactness of the simplex and Pascal's identity give, inductively,

\[
\operatorname{rank}\delta_s=\binom{n-1}s,\qquad
\dim\ker\delta_t=\binom{n-1}{t-1}.
\]

Therefore

\[
\begin{aligned}
\dim\ker M_{\cal D}
&=\dim\ker H_{\cal E}^{\mathsf T}-\dim\ker\delta_t\\
&=\binom nt-\operatorname{rank}H_{\cal E}
  -\binom{n-1}{t-1}\\
&=\binom{n-1}t-\operatorname{rank}H_{\cal E}.
\end{aligned}
\]

Over \(\mathbf F_2\), an unoriented graph incidence matrix has rank equal to
its number of vertices minus its number of connected components.  Hence

\[
\operatorname{rank}H_{\cal E}=|{\cal E}|-c(G_{\cal E}).
\]

Using
\(|{\cal D}|+|{\cal E}|=\binom n{t+1}\), we obtain

\[
\begin{aligned}
\operatorname{rank}M_{\cal D}
&=|{\cal D}|-\dim\ker M_{\cal D}\\
&=\binom n{t+1}-\binom{n-1}t-c(G_{\cal E})\\
&=\binom{n-1}{t+1}-c(G_{\cal E}),
\end{aligned}
\]

as claimed. \(\square\)

Thus even the exact binary rank of \(M_{\cal D}\) records only the number of
residual connected components.  It cannot distinguish a connected
bipartite residual graph from a connected nonbipartite one; the affine
membership of \({\bf1}_{\cal D}\), not the rank alone, is essential.

## 5. The elementary cochain generators, and a necessary warning

The relevant elementary coboundary is not the downward boundary of a
\((t+2)\)-set.  It is the upward star of a \(t\)-set.  For
\(T\in\binom Xt\), put

\[
 s_T:=\delta_t{\bf1}_{\{T\}}
 ={\bf1}_{\{B\in\binom X{t+1}:T\subset B\}}.
\tag{5.1}
\]

It has \(n-t=p\) blocks, hence odd weight.  Every deleted system chooses
exactly one extension of \(T\), so \(s_T\) contains exactly \(p-2\) deleted
and two residual blocks.  Therefore no single elementary coboundary is
supported on \({\cal D}\).

Lemma 3.1 says that every cocycle on the \((t+1)\)-sets is a sum of these
stars:

\[
 y=\delta_tz=\sum_{T:z(T)=1}s_T.
\tag{5.2}
\]

It is supported on \({\cal D}\) precisely when all residual blocks cancel.
Those cancellation equations are \(H_{\cal E}^{\mathsf T}z=0\).
Thus an obstruction necessarily uses a nontrivial collection of elementary
stars whose two residual appearances cancel at every residual block.

This distinction prevents a tempting but incorrect argument.  The vector
of all \((t+1)\)-facets of one \((t+2)\)-set is a **chain boundary**, while
\(\delta\) here is the cochain coboundary.  Such a facet vector is generally
not in \(\ker\delta_{t+1}\): other \((t+2)\)-sets containing one of its
facets see it with odd multiplicity.  The \((t+2)\)-sets index the parity
checks (the rows of \(M_{\cal D}\)); their downward boundaries are not
automatic kernel witnesses.

## 6. The top rung and complement closure

Put

\[
 k=p-1,\qquad t=k-1,\qquad n=2k,\qquad r=p-2=k-1.
\]

Here \(k\) is even.  We use the already-proved top-rung fact that every
\(S(k-1,k,2k)\) is closed under complementation.  For completeness, the
needed special case is re-proved next.

### Lemma 6.0 (top systems are complement-closed)

If \(k\) is even and \({\cal S}\) is an \(S(k-1,k,2k)\), then

\[
B\in{\cal S}\quad\Longrightarrow\quad X\setminus B\in{\cal S}.
\]

#### Proof

Fix \(B\in{\cal S}\), and let \(N_i\) be the number of blocks
\(C\in{\cal S}\) with \(|B\cap C|=i\).  A fixed \(j\)-set lies in

\[
\lambda_j
=\frac{\binom{2k-j}{k-j}}{k+1}
\tag{6.0}
\]

blocks.  Counting pairs \((J,C)\) with
\(J\in\binom Bj\) and \(J\subset C\) gives

\[
\sum_{i=j}^k\binom ijN_i=\binom kj\lambda_j
\qquad(0\le j\le k-1).
\tag{6.01}
\]

For \(j=k\), the same left side is \(N_k=1\).  Binomial inversion at zero
therefore gives

\[
\begin{aligned}
N_0
&=\sum_{j=0}^{k-1}(-1)^j\binom kj\lambda_j+(-1)^k\\
&=\frac{S-(-1)^k}{k+1}+(-1)^k,
\end{aligned}
\tag{6.02}
\]

where

\[
S:=\sum_{j=0}^k(-1)^j
\binom kj\binom{2k-j}{k-j}.
\]

The last sum is one, since

\[
\begin{aligned}
S
&=[x^k]\sum_{j=0}^k(-1)^j
  \binom kj(1+x)^{2k-j}\\
&=[x^k](1+x)^{2k}
  \left(1-\frac1{1+x}\right)^k\\
&=[x^k]x^k(1+x)^k=1.
\end{aligned}
\]

As \(k\) is even, (6.02) yields \(N_0=1\).  The only \(k\)-subset disjoint
from \(B\) is \(X\setminus B\), so that complement is a block of
\({\cal S}\). \(\square\)

### Lemma 6.1 (each top face has exactly two residual facets)

Every \(F\in\binom X{k+1}\) contains exactly one block from each
\({\cal D}_i\), hence exactly \(k-1\) deleted and two residual \(k\)-sets.

#### Proof

Put \(A=X\setminus F\), so \(|A|=k-1\).  In \({\cal D}_i\), there is a
unique block \(C_i(A)\) containing \(A\).  Complement closure puts

\[
 B_i(A):=X\setminus C_i(A)
\]

in the same system, and \(B_i(A)\subset F\).  Conversely, the complement of
any block of \({\cal D}_i\) contained in \(F\) is a block containing \(A\),
so uniqueness gives exactly one.  The systems are block-disjoint, so these
\(k-1\) blocks are distinct.  There are \(k+1\) facets in total, leaving
two. \(\square\)

This is the face-side counterpart of Section 5: at the top rung every row of
the deleted-block parity-check matrix has exactly \(k-1\) deleted entries and
the two omitted facets are residual.  The row is a check, not a cocycle.

### Theorem 6.2 (common odd-transversal form)

For each \(i\), the family

\[
 {\cal P}_i:=
 \left\{
 \binom C{k-1}: C\in{\cal D}_i
 \right\}
\tag{6.1}
\]

is a partition of the universe \(V=\binom X{k-1}\) into

\[
 N=C_k=\frac1{k+1}\binom{2k}k
\tag{6.2}
\]

cells of size \(k\).  Cells from distinct partitions meet in at most one
point.

The top residual graph is bipartite if and only if there is a function

\[
 a:V\longrightarrow\mathbf F_2
\tag{6.3}
\]

which has odd sum on every cell of all \(k-1\) partitions:

\[
 \sum_{A\in\binom C{k-1}}a(A)=1
\qquad
(C\in{\cal D}_i,\ 1\le i\le k-1).
\tag{6.4}
\]

#### Proof

The Steiner property says that every \(A\in V\) belongs to exactly one
block \(C\in{\cal D}_i\), proving that (6.1) is a partition.  Each cell has
the \(k\) facets of its block.  If cells belonging to two distinct systems
shared two \((k-1)\)-sets, their two \(k\)-blocks would be equal; disjointness
excludes this.  Formula (6.2) is

\[
 |{\cal D}_i|
 =\frac1k\binom{2k}{k-1}
 =\frac1{k+1}\binom{2k}k.
\]

Now reindex the rows of \(M_{\cal D}\) by
\(A=X\setminus F\in\binom X{k-1}\), and reindex every column
\(B\in{\cal D}_i\) by its complement \(C=X\setminus B\in{\cal D}_i\).
Then

\[
 B\subset F\quad\Longleftrightarrow\quad A\subset C.
\]

Thus the reindexed matrix \(Q\) is the point-versus-cell incidence matrix
of the partitions (6.1).  The row-space condition
\({\bf1}\in\operatorname{row}Q\) says exactly that some row coefficient
vector \(a\) satisfies \(Q^{\mathsf T}a={\bf1}\), which is (6.4).
Apply Theorem 4.1. \(\square\)

Theorem 6.2 is an exact halving/complement-fold formulation, but it does not
make existence automatic: a common odd transversal for several partitions
is a substantive linear condition.

## 7. Why the immediate top-rung parities do not obstruct

Let \(Q\) be the matrix in the proof of Theorem 6.2.

* Every row has \(r=k-1\) ones, which is odd:
  \[
  Q{\bf1}={\bf1}.
  \tag{7.1}
  \]
* Every column has \(k\) ones, which is even:
  \[
  Q^{\mathsf T}{\bf1}=0.
  \tag{7.2}
  \]
* If \(e_i\) is the indicator of the columns from \({\cal D}_i\), then
  \(Qe_i={\bf1}\), so
  \[
  e_i+e_j\in\ker Q.
  \tag{7.3}
  \]

The forced kernel vectors in (7.3) have weight \(2C_k\), hence even.

Also \(C_k\) is even because \(k\) is positive and even.  Indeed

\[
 C_k=\frac{2}{k+1}\binom{2k-1}{k-1},
\]

and the odd number \(k+1\) divides the numerator; being coprime to \(2\), it
already divides the binomial coefficient.  Therefore \(C_k\) is twice an
integer.

If a common odd transversal \(a\) exists, summing (6.4) over every cell of
one partition gives

\[
 \sum_{A\in V}a(A)=|{\cal D}_i|=C_k=0.
\tag{7.4}
\]

The same equation results from every \(i\).  Thus all partition totals agree,
but they agree at zero.  There is no contradiction.

Equations (7.1)--(7.4) show that the immediate row-sum, column-sum, Catalan,
and design-difference tests do not obstruct.  An obstruction not already
visible in those identities must prove that \(\ker Q\) contains some
**additional odd-weight** vector.  Equivalently, it must produce a global
odd trade not generated by the evident even differences \(e_i+e_j\).

### Theorem 7.1 (unitrade gap inside the top partial)

Let \({\cal U}\) be a nonempty family of \(k\)-subsets of a set such that
every \((k-1)\)-set is contained in an even number of members of
\({\cal U}\).  Then

\[
 |{\cal U}|=k+1
 \quad\hbox{or}\quad
 |{\cal U}|\geq2k.
\tag{7.5}
\]

In the first case, \({\cal U}\) consists of all \(k\)-facets of one
\((k+1)\)-set.

Consequently, if \({\cal U}\) is supported on the union of the \(k-1\)
top-rung deleted systems, then the first case is impossible.  Every nonzero
vector in \(\ker Q\) therefore has weight at least \(2k\), and every
odd-weight vector in \(\ker Q\) has weight at least

\[
 2k+1.
\tag{7.6}
\]

#### Proof

Fix \(B\in{\cal U}\).  Each of the \(k\) facets of \(B\) must occur in at
least one further block.  A block other than \(B\) contains at most one
facet of \(B\), so these are \(k\) distinct blocks.  Hence
\(|{\cal U}|\geq k+1\).

Suppose first that every two blocks of \({\cal U}\) meet in \(k-1\) points.
Fix

\[
 B=I\cup\{b\},\qquad C=I\cup\{c\},
\qquad |I|=k-1.
\]

Every further block adjacent to both \(B\) and \(C\) either contains \(I\),
or is contained in \(I\cup\{b,c\}\).  A block of the first kind outside the
second family and a block of the second kind outside the first meet in only
\(k-2\) points.  Thus a pairwise adjacent family is wholly a star through
\(I\), or wholly a top inside \(I\cup\{b,c\}\).

A nonempty star cannot satisfy the even-facet condition: a facet obtained
by deleting one point of \(I\) from one of its blocks occurs only once.
In a top, the even-facet condition forces every one of the \(k+1\) facets
of the \((k+1)\)-set to occur.  This gives the first case of (7.5).

Otherwise choose \(B,C\in{\cal U}\) with
\[
 r:=|B\cap C|\leq k-2.
\]
As above, the \(k\) facets of each block require distinct further blocks.
If \(r\leq k-3\), no \(k\)-set can contain both a facet of \(B\) and a
facet of \(C\), since that would require
\[
 k\geq2(k-1)-r>k.
\]
The two sets of covering blocks are disjoint, and
\(|{\cal U}|\geq2+2k>2k\).

It remains that \(r=k-2\).  Write
\[
 B=I\cup\{b_1,b_2\},\qquad
 C=I\cup\{c_1,c_2\}.
\]
The only blocks that can simultaneously contain a facet of \(B\) and a
facet of \(C\) are
\[
 I\cup\{b_i,c_j\}\qquad(1\leq i,j\leq2).
\]
They can cover only the two facets of \(B\) containing \(I\), and the two
such facets of \(C\).  Let \(x_{ij}\) indicate which of these four common
covering blocks are selected, and put \(s=\sum x_{ij}\).  A special facet
of \(B\) needs an additional \(B\)-only covering block precisely when the
corresponding row sum of \(x\) is even; let \(b\) be the number of even row
sums.  Define \(c\) similarly from the columns and the special facets of
\(C\).  Directly for a \(2\)-by-\(2\) binary matrix,
\[
 s+b+c\geq2:
\]
for \(s=0,1\) the respective lower bounds are \(4,3\), and for \(s\geq2\)
the claim is immediate.

Each of the remaining \(k-2\) facets of \(B\) and \(k-2\) facets of \(C\)
needs its own further block, and none of these blocks can serve both sides.
Therefore
\[
 |{\cal U}|\geq
 2+s+b+c+(k-2)+(k-2)\geq2k.
\]
This proves (7.5).

For a top-rung deleted union, Lemma 6.1 says that every \((k+1)\)-set
contains only \(k-1\), rather than all \(k+1\), deleted blocks.  Hence the
minimum case cannot be supported on the deleted union.  Since \(k\) is
even, an odd kernel vector of weight at least \(2k\) has weight at least
\(2k+1\). \(\square\)

The general gap in (7.5) is also known in the unitrade/code literature; see
[Potapov's Proposition 14](https://old.math.nsc.ru/~potapov/DPsplitting.pdf)
and the summary in Marin--Mogilnykh,
[*Binary codes from subset inclusion matrices*](https://arxiv.org/abs/2408.12154).
The proof above is included to keep the strengthened top-rung consequence
self-contained.

### Corollary 7.2 (the pre-minimum word is also excluded)

Every nonzero vector in \(\ker Q\) supported on the top-rung deleted union
has weight at least
\[
 2k+1.
\tag{7.7}
\]

#### Proof

The equality classification in Potapov's Proposition 14 says that every
\(k\)-unitrade of weight \(2k\) is the symmetric difference
\[
 W_k(F)\mathbin\triangle W_k(G)
\]
of the two complete facet families of \((k+1)\)-sets \(F,G\).  Since each
family has \(k+1\) blocks, weight \(2k\) means that the two families share
exactly one block.  In particular, the symmetric difference contains
exactly \(k\) of the \(k+1\) facets of \(F\).

Lemma 6.1 says that the deleted union contains exactly \(k-1\) facets of
every \((k+1)\)-set.  It therefore cannot contain those \(k\) facets of
\(F\).  The weight-\(2k\) equality case is impossible, and Theorem 7.1
gives (7.7). \(\square\)

Corollary 7.2 strengthens the minimum distance of the deleted-support
kernel, but does not improve the numerical lower bound for the odd
certificate needed in (8.1): that bound was already \(2k+1\).

## 8. Exact failure boundary of the cohomological route

By Lemma 3.1, every deleted cocycle is a sum of elementary \(t\)-set stars
\(s_T\).  Each star has exactly two residual blocks.  Hence an odd deleted
cocycle exists exactly when one can choose an odd number (modulo
cancellations among repeated stars) of these star generators whose residual
blocks all cancel in pairs.

But the residual cancellation equations are precisely

\[
 H_{\cal E}^{\mathsf T}z=0,
\]

the residual cycle-space equations.  Thus simplex exactness supplies a
canonical translation and certificate, but no relaxation:

\[
\boxed{
\begin{array}{c}
\text{odd residual cycle}\\
\Updownarrow\\
\text{odd deleted cochain cocycle}\\
\Updownarrow\\
{\bf1}_{\cal D}\notin\operatorname{row}M_{\cal D}.
\end{array}}
\tag{8.1}
\]

At the top rung, complement closure adds the equivalent fourth line

\[
\text{no common odd transversal for the partitions }{\cal P}_i.
\]

There the complemented odd cocycle is also an odd binary
\((k-1)\)-trade supported on the complemented deleted systems.

A genuinely new uniform negative theorem would therefore have to show that
**every** admissible top-rung family of \(k-1\) disjoint,
complement-closed Steiner systems supports an odd trade.  Nothing in
simplex exactness, face parity, complement closure, row/column parity, or the
forced design-difference kernel vectors proves that assertion.  Theorem 7.1
does prove that any such odd trade has at least \(2k+1\) blocks, but does not
force one to exist.

Conversely, a proof that every such family has a common odd transversal
would show that any \(k-1\) disjoint top systems automatically extend to a
large set, but would still leave the separate existence of those \(k-1\)
systems to be proved.

This is the exact logical boundary, not a solution in either direction.

## 9. Exact finite controls

The standard-library verifier
`verify_cochain_controls.py` checks both possible outcomes.

### 9.1 Positive control: \(LS(2,3,9)\)

The verifier enumerates all \(840\) labelled \(STS(9)\)'s, constructs seven
pairwise disjoint systems partitioning all \(84\) triples, and deletes five.
For the resulting matrix \(M_{\cal D}\):

\[
 \#\text{rows}=\binom94=126,\qquad
 \#\text{columns}=5\cdot12=60,
\]

and exact binary elimination gives

\[
 \operatorname{rank}M_{\cal D}=55,\qquad
 {\bf1}_{\cal D}\in\operatorname{row}M_{\cal D}.
\]

The deterministic witness uses \(48\) rows.  The two remaining systems give
the corresponding residual bipartition.

### 9.2 Negative fixed-partial control: the EH residual triangle

For the authenticated fifteen-system Etzion--Hartman partial at
\((t,n,p)=(3,20,17)\), take

\[
 z=
 {\bf1}_{\{0,14,17\}}+
 {\bf1}_{\{5,14,17\}}+
 {\bf1}_{\{2,14,17\}}.
\]

These are the three edge labels of the explicit residual triangle.  Hence
\(H_{\cal E}^{\mathsf T}z=0\) and \(|z|=3\).  Its coboundary

\[
 y=\delta_3z
\]

has \(45\) blocks.  To see the count directly, each selected triple has
\(17\) extensions.  Each pair of the three triples has one common extension,
namely one vertex of the residual triangle; there is no extension containing
all three.  The symmetric difference therefore has size

\[
 3\cdot17-2\cdot3=45.
\]

It is supported on the \(4\,275\) blocks of the fifteen deleted systems,
and \(\delta_4y=0\).  Thus it is an explicit odd vector in
\(\ker M_{\cal D}\), proving

\[
 {\bf1}_{\cal D}\notin\operatorname{row}M_{\cal D}
\]

for this fixed partial.

This negative control says nothing about another fifteen-system partial and
does not prove \(LS(3,4,20)\) impossible.

## 10. Conclusion for #835

The cochain and row-space formulations are now exact, including at the top
rung.  They provide short independently checkable certificates on either
side.  What remains open is the substantive statement that would be needed
for #835: whether the highly structured top-rung partition family in
Theorem 6.2 must fail, or can satisfy, the common odd-transversal condition
uniformly for the admissible \(k\).

The first unrestricted open case remains \(k=16\), \(p=17\).  No case of
unrestricted #835 is resolved here.
