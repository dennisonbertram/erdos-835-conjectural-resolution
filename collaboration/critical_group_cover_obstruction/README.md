# Critical groups do not obstruct the prime cases

## Status and scope

Assume that a tight coloring gives an \(n\)-sheeted graph covering

\[
\pi:O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}.
\]

The composite-case obstruction already known for problem #835 leaves the
case

\[
k=p-1,\qquad p=k+1\ \text{an odd prime}.
\]

This note computes the strongest immediate critical-group consequences of
such a cover.  They all pass.  In fact, if

\[
N=\binom{2p-3}{p-2},\qquad n=N/p,
\]

then

\[
\boxed{\;
K(O_{p-1})_{(p)}
\cong(\mathbb Z/p\mathbb Z)^{\,2n-1}.
\;}
\tag{0.1}
\]

The target requires only

\[
K(K_p)\cong(\mathbb Z/p\mathbb Z)^{p-2}.
\tag{0.2}
\]

Since \(p\nmid n\), transfer would make (0.2) a direct summand of (0.1).
There is ample room: \(2n-1\ge p-2\).  The spanning-tree divisibility and
the Laplacian spectral inclusion also pass.

Thus this route supplies an exact no-go result **for the proposed
obstruction**, not for the graph cover.  It neither constructs nor excludes
a tight coloring, and it does **not** solve Erdős--Rosenfeld problem #835.

## 1. A self-contained transfer lemma

For a connected graph \(G\), write

\[
K(G)=\operatorname{Div}^0(G)/L_G\mathbb Z^{V(G)}
\]

for its critical group.  Here \(\operatorname{Div}^0(G)\) is the lattice of
integer vertex vectors with coordinate sum zero.

Let \(\pi:\widetilde G\to G\) be a connected \(n\)-sheeted graph cover.
Define

\[
(\pi_*x)(v)=\sum_{\widetilde v\in\pi^{-1}(v)}x(\widetilde v),
\qquad
(\pi^*y)(\widetilde v)=y(\pi(\widetilde v)).
\]

For each edge \(vw\) of \(G\), the edges above it give a perfect matching
between \(\pi^{-1}(v)\) and \(\pi^{-1}(w)\).  Summing the Laplacian over a
fibre therefore gives

\[
\pi_*L_{\widetilde G}=L_G\pi_*,
\qquad
L_{\widetilde G}\pi^*=\pi^*L_G,
\qquad
\pi_*\pi^*=nI.
\tag{1.1}
\]

The first two identities induce homomorphisms

\[
K(\widetilde G)
\mathop{\longrightarrow}^{\pi_*}K(G),
\qquad
K(G)\mathop{\longrightarrow}^{\pi^*}K(\widetilde G).
\tag{1.2}
\]

The first is surjective: any degree-zero divisor on \(G\) can be lifted by
placing each of its coefficients on one chosen vertex of the corresponding
fibre.  The last identity in (1.1) remains true on critical groups.
Consequently:

1. \(K(G)\) is a quotient of \(K(\widetilde G)\), so
   \(\tau(G)\mid\tau(\widetilde G)\).
2. On the \(q\)-primary parts, (1.2) splits whenever \(q\nmid n\).
   Indeed, if \(q^a\) kills \(K(G)_{(q)}\), choose \(c\) with
   \(cn\equiv1\pmod{q^a}\); then \(c\pi^*\) is a section of \(\pi_*\).

This proves the transfer statement used below rather than assuming it.

There is also a compatible statement for the monodromy pairing.  If
\(\langle\ ,\ \rangle_G\) denotes the usual perfect
\(\mathbb Q/\mathbb Z\)-valued pairing on \(K(G)\), then

\[
\langle\pi^*x,\pi^*y\rangle_{\widetilde G}
=n\langle x,y\rangle_G,
\qquad
\langle\pi^*x,z\rangle_{\widetilde G}
=\langle x,\pi_*z\rangle_G.
\tag{1.3}
\]

For example, choose a rational vector \(f\) with \(L_Gf=x\).  Then
\(L_{\widetilde G}\pi^*f=\pi^*x\), and taking dot products proves both
identities.

## 2. Odd-graph Laplacian arithmetic at \(p=k+1\)

Put

\[
k=p-1,\qquad r=p-2,\qquad v=2p-3,\qquad
N=\binom vr,\qquad n=N/p.
\tag{2.1}
\]

The Odd graph has adjacency eigenvalues and multiplicities

\[
\theta_i=(-1)^i(k-i),\qquad
\mu_i=\binom vi-\binom v{i-1}
\quad(0\le i\le r).
\tag{2.2}
\]

Thus its Laplacian eigenvalues are

\[
\lambda_i=k-\theta_i=
\begin{cases}
i,&i\ \text{even},\\
2p-2-i,&i\ \text{odd}.
\end{cases}
\tag{2.3}
\]

Because \(r=p-2\) is odd,

\[
\lambda_r=p,\qquad
\mu_r
=\binom{2p-3}{p-2}-\binom{2p-3}{p-3}
=\frac{2N}{p}=2n.
\tag{2.4}
\]

No other nonzero \(\lambda_i\) is divisible by \(p\).  Also

\[
v_p(N)=1,
\tag{2.5}
\]

since \((2p-3)!\) contains exactly one factor \(p\), while
\((p-2)!\) and \((p-1)!\) contain none.  In particular \(n\) is an
integer and \(p\nmid n\).  Reducing the same factorial quotient after
removing its unique factor \(p\) gives the slightly sharper identity

\[
n\equiv\frac{(p-1)!(p-3)!}{(p-2)!(p-1)!}
\equiv-\frac12\pmod p.
\tag{2.6}
\]

Kirchhoff's eigenvalue formula now gives

\[
\tau(O_{p-1})
=\frac1N\prod_{i=1}^{p-2}\lambda_i^{\mu_i},
\qquad
v_p\!\left(\tau(O_{p-1})\right)=2n-1.
\tag{2.7}
\]

Since \(\tau(K_p)=p^{p-2}\),

\[
v_p\!\left(\frac{\tau(O_{p-1})}{\tau(K_p)}\right)
=2n-p+1\ge0.
\tag{2.8}
\]

The tree-number divisibility forced by Section 1 therefore passes for
every surviving prime parameter.

The ordinary spectral condition passes as well.  The nonzero Laplacian
eigenvalue of \(K_p\) is \(p\), with multiplicity \(p-1\), while
\(O_{p-1}\) has eigenvalue \(p\) with multiplicity \(2n\).  A cover would
use only \(p-1\) dimensions of this much larger eigenspace.

## 3. Exact \(p\)-primary Smith group

It remains possible in principle that the valuation in (2.6) is
concentrated in large powers of \(p\), leaving too few direct
\(\mathbb Z/p\)-summands.  It is not.

Let \(W\) be the inclusion matrix from functions on \(r\)-subsets to
functions on \((r-1)\)-subsets:

\[
(Wf)(U)=\sum_{\substack{S\supset U\\|S|=r}}f(S).
\tag{3.1}
\]

The matrix \(W\) has full row rank over \(\mathbb Q\).  One quick check is
that

\[
WW^{\mathsf T}=(r+2)I+A_{J(2r+1,r-1)}.
\]

The Johnson eigenvalue indexed by \(0\le j\le r-1\) is

\[
(r-1-j)(r+2-j)-j.
\]

After adding \(r+2\), this becomes

\[
(r-j)(r-j+2)>0,
\tag{3.2}
\]

so \(WW^{\mathsf T}\) is nonsingular.  Hence the integral lattice

\[
\Lambda=\ker\!\left(W:\mathbb Z^N\to
\mathbb Z^{\binom v{r-1}}\right)
\]

has rank

\[
\operatorname{rank}\Lambda
=N-\binom v{r-1}
=2n.
\tag{3.3}
\]

It is primitive: \(\mathbb Z^N/\Lambda\cong\operatorname{im}W\) is a
subgroup of a free abelian group and is therefore torsion-free.

For \(f\in\Lambda\), all lower containment sums vanish as well.  Indeed,
if \(|X|=j<r\), summing (3.1) over the \((r-1)\)-sets \(U\) containing
\(X\) gives

\[
(r-j)\sum_{S\supset X}f(S)=0.
\tag{3.4}
\]

For an \(r\)-set \(B\), inclusion-exclusion now yields

\[
\begin{aligned}
(Af)(B)
&=\sum_{S:S\cap B=\varnothing}f(S)\\
&=\sum_{X\subseteq B}(-1)^{|X|}
  \sum_{S\supseteq X}f(S)
=(-1)^rf(B)=-f(B).
\end{aligned}
\tag{3.5}
\]

Therefore \(L f=pf\) on \(\Lambda\).  Reducing modulo \(p\), primitivity
of \(\Lambda\) supplies a \(2n\)-dimensional subspace of
\(\ker(L\bmod p)\).

Write the Smith form of \(L\) as

\[
\operatorname{diag}(d_1,\ldots,d_{N-1},0).
\]

If \(t\) of the nonzero \(d_i\) are divisible by \(p\), then
\[
\dim_{\mathbb F_p}\ker(L\bmod p)=t+1.
\]
The preceding paragraph gives \(t\ge2n-1\), while (2.6) gives
\[
\sum_i v_p(d_i)=2n-1.
\]
It follows that exactly \(2n-1\) Smith entries are divisible by \(p\),
and every one has valuation exactly one.  This proves (0.1).

## 4. The first open parameter \(k=16\)

For \(p=17\),

\[
N=\binom{31}{15}=300\,540\,195,
\qquad
n=17\,678\,835.
\]

The exact source and target groups at \(17\) are therefore

\[
\boxed{
K(O_{16})_{(17)}
\cong(\mathbb Z/17)^{35\,357\,669},
\qquad
K(K_{17})\cong(\mathbb Z/17)^{15}.}
\tag{4.1}
\]

The forced direct summand occupies only fifteen of the
\(35\,357\,669\) available dimensions.  The spanning-tree quotient has

\[
v_{17}\!\left(\frac{\tau(O_{16})}{\tau(K_{17})}\right)
=35\,357\,654.
\tag{4.2}
\]

For reference, its complete prime factorization is

\[
\frac{\tau(O_{16})}{\tau(K_{17})}
=2^{212416154}3^{97750066}5^{27978677}7^{99249600}
17^{35357654}19^{65132549}23^{12271349}29^{4029}31^{29}.
\tag{4.3}
\]

Thus neither tree divisibility nor the Smith normal form contradicts the
hypothetical \(O_{16}\to K_{17}\) cover.

## 5. Even the abstract pairing condition has room

By (1.3), the hypothetical split copy of \(K(K_p)\) would carry its
monodromy pairing multiplied by the unit \(n\bmod p\).  Both sides of
(0.1)--(0.2) are elementary \(p\)-groups, so their pairings are
nondegenerate symmetric bilinear forms over \(\mathbb F_p\).

This adds no abstract obstruction.  Over a finite field of odd
characteristic, nondegenerate symmetric forms are classified by their
dimension and determinant square class.  Given the source form and the
scaled target form, choose a nondegenerate complement of dimension

\[
(2n-1)-(p-2)=2n-p+1>0
\]

with the required determinant square class.  A diagonal matrix realizes
either square class.  The target plus this complement is therefore
isometric to the source form.

This statement concerns only the abstract paired critical group.  A real
cover must realize the summand by the particular fibre-sum and pullback
maps, as well as satisfy all local matching constraints.  Nothing here
shows that such geometric maps exist.

## 6. Reproduction

The standard-library verifier checks the exact spectrum, valuations,
source and target ranks for every odd prime through a chosen bound, and
the complete factorization (4.3):

```bash
python3 collaboration/critical_group_cover_obstruction/verify_critical_group_cover_obstruction.py
python3 collaboration/critical_group_cover_obstruction/verify_critical_group_cover_obstruction.py --max-prime 199
```
