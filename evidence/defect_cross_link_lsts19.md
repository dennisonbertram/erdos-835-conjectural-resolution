# The defect-link tower and its exact \(LS(2,3,19)\) boundary

Status: **proved reduction and verified coherent local countermodel; not a
global colouring and not a solution of Problem #835.**

This note identifies the first genuine compatibility condition between
different defect links.  All defect links through one common
\((r-2)\)-set form a large set \(LS(2,3,r+4)\).  At the target \(r=15\)
this is an \(LS(2,3,19)\).  A completely checked example of that large set
still has zero and multiple finite rainbow-triangle counts.  Consequently
one whole codimension-three link is not enough to prove that the defect map
is bijective.

## 1. Extending the tight colouring

Let \(r\) be odd, let \(|X|=2r+1\), and let \({\cal C}\) be a set of
\(r+2\) colours.  A hypothetical large set
\[
 LS(r-1,r,2r+1)
\]
is equivalently a colouring
\[
 \chi:\binom Xr\longrightarrow{\cal C}                 \tag{1}
\]
such that for every \(F\in\binom X{r-1}\),
\[
 \{\chi(F+x):x\in X\setminus F\}={\cal C}.             \tag{2}
\]

Adjoin a point \(\infty\), put \(Y=X\sqcup\{\infty\}\), and define
\[
 \widehat\chi(K)=
 \begin{cases}
   \chi(K\setminus\{\infty\}),&\infty\in K,\\
   \chi(X\setminus K),&\infty\notin K
 \end{cases}
 \qquad\left(K\in\binom Y{r+1}\right).                 \tag{3}
\]

**Lemma 1.**  Every \(r\)-set of \(Y\) has one extension of every colour
under \(\widehat\chi\).  Thus (3) is a large set
\[
 LS(r,r+1,2r+2).                                      \tag{4}
\]

**Proof.**  If the \(r\)-set is \(F+\infty\), (2) gives the assertion
directly.  Let instead \(A\in\binom Xr\).  The extension \(A+\infty\)
has colour \(\chi(A)\).  For \(x\in X\setminus A\), the finite extension
\(A+x\) has the colour of
\[
 B_x=X\setminus(A+x).
\]
The \(r+1\) sets \(B_x\) are the \(r\)-subsets of \(X\setminus A\).
Any two share an \((r-1)\)-set and hence have different colours by (2).
None has colour \(\chi(A)\): two blocks of one
\(S(r-1,r,2r+1)\) cannot be disjoint (the standard internal intersection
number is \(n_0=0\)).  Therefore their colours are exactly
\({\cal C}\setminus\{\chi(A)\}\). \(\square\)

## 2. The complete link tower

The useful point is that every lower link of (3) is itself a large set.

**Theorem 2 (link tower).**  Fix \(1\leq s\leq r+1\) and
\[
 J\in\binom Y{r+1-s},\qquad P=Y\setminus J.
\]
Then \(|P|=r+1+s\), and
\[
 q_J(S)=\widehat\chi(J\cup S)
 \qquad\left(S\in\binom Ps\right)                      \tag{5}
\]
is a large set
\[
 LS(s-1,s,r+1+s)                                      \tag{6}
\]
with the same \(r+2\) colours.

**Proof.**  Fix \(E\in\binom P{s-1}\).  The sets
\[
 J\cup E\cup\{x\},\qquad x\in P\setminus E,
\]
are exactly the \(r+2\) extensions of the \(r\)-set \(J\cup E\) in
\(Y\).  Lemma 1 says that their colours are all of \({\cal C}\), once
each.  Hence each colour class in (5) is an
\(S(s-1,s,r+1+s)\), and the classes partition all \(s\)-sets. \(\square\)

At \(r=15\), the first three nontrivial layers are
\[
\begin{array}{c|c|c}
s&\text{residual object}&\text{meaning}\\ \hline
2&LS(1,2,18)&\text{a one-factorization of }K_{18},\\
3&LS(2,3,19)&\text{a coherent family of nineteen }K_{18}\text{ links},\\
4&LS(3,4,20)&\text{the next cross-link compatibility layer}.
\end{array}                                            \tag{7}
\]

## 3. Defect matchings are exactly the \(s=2\) links

Let \(R\in\binom X{r-1}\), put \(U=X\setminus R\), and set
\[
 P_R=Y\setminus R=U\sqcup\{\infty\}.
\]
The \(s=2\) link at \(R\) colours the edges of \(K_{r+3}\) by
\[
 f_R(\{x,y\})=\widehat\chi(R+x+y).                     \tag{8}
\]
At every vertex, the incident \(r+2\) edges have all colours, so (8) is
a one-factorization.

It is exactly the extended matching link used by the defect map:
\[
\begin{aligned}
 f_R(\{\infty,x\})&=\chi(R+x),\\
 f_R(\{x,y\})&=\chi(U\setminus\{x,y\})
 \qquad(x,y\in U).
\end{aligned}                                          \tag{9}
\]
The first line pairs \(\infty\) with the extension point of \(R\) in
each system.  The second line says that a finite edge is the complement
inside \(U\) of the corresponding contained block.

For a colour triple \(S\in\binom{\cal C}3\), let \(d_R(S)\) be the
number of triangles in \(U=P_R\setminus\{\infty\}\) whose three edge
colours under (8) are \(S\).  The exact preimage theorem in
`defect_facet_map_audit.md` gives
\[
 d_R(S)=|T_S^{-1}(R)|.                                \tag{10}
\]

## 4. Exact adjacent-link transport

Fix \(H\in\binom X{r-2}\), put \(P=Y\setminus H\), and use the
\(s=3\) link
\[
 q_H(\{p,x,y\})=\widehat\chi(H+p+x+y).                 \tag{11}
\]
By Theorem 2, this is an \(LS(2,3,r+4)\).  For every finite
\(p\in P\setminus\{\infty\}\), the point link of \(q_H\) at \(p\) is
exactly the defect one-factorization \(f_{H+p}\).

Take distinct \(p,q\in P\) and identify the vertex \(q\) in the
\(p\)-link with the vertex \(p\) in the \(q\)-link; call the identified
vertex \(z\).  The two one-factorizations then obey:

1. they agree on the entire star at \(z\), because for \(x\notin\{p,q\}\)
   both colours are \(q_H(\{p,q,x\})\);
2. they disagree on every other common edge \(\{x,y\}\), because
   \(q_H(\{p,x,y\})\) and \(q_H(\{q,x,y\})\) are two different
   completions of the pair \(\{x,y\}\) in one Steiner large set.

This transport law is exact, not merely necessary.  Conversely, a family
of one-factorizations on the eighteen-point complements of the points of
a nineteen-set, with the common-star agreements above, defines
\(q(\{p,q,x\})\) unambiguously.  A row of any one factorization then shows
that the seventeen triples over every fixed pair have all seventeen
colours.  Thus the coherent family is precisely an \(LS(2,3,19)\).

## 5. A fully coherent countermodel to link-local bijectivity

The independent checker

```bash
/opt/homebrew/bin/python3 -B \
  evidence/verify_defect_cross_link_lsts19.py
```

reconstructs a cyclic \(LS(2,3,19)\) from two 17-entry Wallis starters
and forty phase values.  It checks directly:

* all \(969=\binom{19}3\) coloured triples;
* seventeen disjoint \(STS(19)\) classes of 57 blocks each;
* every pair exactly once in every colour;
* all nineteen point-link one-factorizations of \(K_{18}\); and
* all \(171=\binom{19}2\) adjacent-link transports from Section 4.

Designate point \(18\) as the global \(\infty\).  The other eighteen
centres model the eighteen finite facets \(H+p\).  Across all
\[
 18\binom{17}3=12\,240
\]
centre--colour-triple pairs, the exact finite rainbow multiplicity
distribution is
\[
\begin{array}{c|rrrrrrr}
d&0&1&2&3&4&5&6\\ \hline
\#&4760&4267&2176&697&204&102&34.
\end{array}                                            \tag{12}
\]
The frequencies sum to \(12\,240\), and their \(d\)-weighted sum is also
\(12\,240\), so the average remains one.

For example, centre \(0\) and colour triple \(\{0,1,7\}\) give
multiplicity zero.  Centre \(0\) and colour triple \(\{1,12,14\}\) give
the six triangles
\[
\begin{gathered}
 \{1,3,15\},\ \{2,5,14\},\ \{3,11,15\},\\
 \{6,12,13\},\ \{7,9,16\},\ \{8,12,13\}.
\end{gathered}                                         \tag{13}
\]
In particular, (13) also supplies a checked example in which same-colour
rainbow triangles share edges.  This is why the correct general local
bound is \(d_R(S)\leq r\), not the false vertex-disjoint bound.

There is a canonical scalar orientation test once \(\infty\) and the
colour labels are fixed.  The \(\infty\)-star in the link at a finite
centre identifies its other seventeen vertices with the colours.  This
normalizes the remaining factorization to a symmetric idempotent Latin
square \(L_p\) on \({\cal C}\).  Put
\[
 \sigma_p=\prod_{c\in{\cal C}}
   \operatorname{sign}\bigl(L_p(c,\mathord\cdot)\bigr). \tag{14}
\]
The checker finds seventeen centres with \(\sigma_p=-1\) and one with
\(\sigma_p=+1\).  Hence even this natural scalar link orientation is not
constant under a completely coherent \(LS(2,3,19)\) transport.

## 6. The scalar orientation boundary cancels exactly

The signs in (14) satisfy a clean identity, but it closes rather than
contradicts the next compatibility layer.

Let \(q:\binom V3\to{\cal C}\) be any \(LS(2,3,19)\), with fixed
orderings of its points and colours.  For \(a\in V\), define the raw sign
of its point-link one-factorization by
\[
 \epsilon_a=
 \prod_{p\in V\setminus\{a\}}
 \operatorname{sign}
 \left(x\longmapsto q(\{a,p,x\})\right),               \tag{15}
\]
where the displayed bijection has ordered domain
\(V\setminus\{a,p\}\) and codomain \({\cal C}\).

**Lemma 3.**
\[
 \prod_{a\in V}\epsilon_a=1.                           \tag{16}
\]

**Proof.**  The factor in (15) indexed by the ordered pair \((a,p)\)
is exactly the factor indexed by \((p,a)\): it is the same map on the same
ordered domain \(V\setminus\{a,p\}\).  Every factor therefore occurs
twice in the product, proving (16). \(\square\)

Now distinguish \(\infty\in V\), put \(P=V\setminus\{\infty\}\), and
define the normalized signs \(\sigma_p\) of (14) for all \(p\in P\).

**Lemma 4 (orientation boundary identity).**
\[
 \prod_{p\in P}\sigma_p=\epsilon_\infty.               \tag{17}
\]

**Proof.**  Put
\[
 \alpha_p(x)=q(\{p,\infty,x\}),
 \qquad x\in P\setminus\{p\},
\]
and let \(A_p=\operatorname{sign}(\alpha_p)\).  For
\(x\in P\setminus\{p\}\), define
\(\beta_{p,x}:P\setminus\{p\}\to{\cal C}\) by
\[
 \beta_{p,x}(y)=
 \begin{cases}
 q(\{p,x,\infty\}),&y=x,\\
 q(\{p,x,y\}),&y\ne x.
 \end{cases}
\]
The row of the normalized Latin square \(L_p\) indexed by
\(\alpha_p(x)\) is
\(\beta_{p,x}\alpha_p^{-1}\).  Since there are seventeen rows,
\[
 \sigma_p=A_p\prod_{x\ne p}\operatorname{sign}(\beta_{p,x}). \tag{18}
\]
Also \(\prod_p A_p=\epsilon_\infty\).

Pair the remaining factors in (18) for \((p,x)\) and \((x,p)\).
Their product is the sign of the order map
\[
 P\setminus\{p\}\longrightarrow P\setminus\{x\},
 \qquad x\mapsto p,\quad y\mapsto y\ (y\ne x).
\]
If \(p,x\) occupy positions \(i<j\) in the fixed order on the
eighteen-set \(P\), this sign is \((-1)^{i+j+1}\).  The product over all
pairs is therefore
\[
 (-1)^{\sum_{i<j}(i+j+1)}
 =(-1)^{18\cdot153}=1.                                \tag{19}
\]
Multiplying (18) proves (17). \(\square\)

This also explains the checked sign distribution in Section 5.  In that
certificate,
\[
 \prod_{p\ne\infty}\sigma_p
 =\epsilon_\infty=-1,
\qquad
 \prod_{a\in V}\epsilon_a=1.                           \tag{20}
\]

Finally suppose, only conditionally, that the next tower layer
\(LS(3,4,20)\) existed, and distinguish one of its points as
\(\infty\).  For distinct finite points \(a,p\), let
\(\sigma_{a,p}=\sigma_{p,a}\) be the normalized sign of their common
\(K_{18}\) link.  Apply (17) to the \(LS(2,3,19)\) point link at \(a\):
\[
 \prod_{p\ne a,\infty}\sigma_{a,p}=\epsilon_{a,\infty}, \tag{21}
\]
where the right side is the raw sign of the link at the pair
\(\{a,\infty\}\).  Multiplying (21) over all nineteen finite \(a\)'s,
every \(\sigma_{a,p}\) occurs twice, so the left side is \(1\).  The right
side is also \(1\) by (16), applied to the \(LS(2,3,19)\) point link at
\(\infty\):
\[
 \prod_a\epsilon_{a,\infty}=1.                         \tag{22}
\]

Thus the first scalar orientation product has zero global defect.  The
boundary of each nineteen-point link in (17) becomes the paired boundary
of the twenty-point layer in (22).  Any successful orientation argument
must retain data finer than the single signs \(\sigma_{a,p}\).

## 7. Exact boundary of the result

The certificate is not a triple of \(S(14,15,31)\) systems and not a
global defect map.  It proves the following precise no-go:

> The one-factorization axiom for every defect link, all common-star and
> cellwise-disjoint transports between the links through one fixed
> \(13\)-set, and every incidence consequence internal to that
> nineteen-point \(LS(2,3,19)\) do **not** force
> \(d_R(S)=1\), nor do they force constancy of the scalar orientation
> (14).

Therefore a successful global obstruction must couple the
\(LS(2,3,19)\) structures belonging to different \((r-2)\)-sets.
The first complete local object that performs this coupling is the next
line of (7), an \(LS(3,4,20)\).  This note neither constructs nor excludes
that object.  Still higher compatibility is required before any statement
can be called a solution of Erdős--Rosenfeld Problem #835.
