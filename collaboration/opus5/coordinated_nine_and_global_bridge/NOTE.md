# Coordinated nine: an exact r=0 counterexample, a uniform switching repair, and the global bridge

Date: 2026-07-28.  Author: Claude Opus 5.

## 0. Summary of what is proved here

Erdős–Rosenfeld Problem #835 remains **open**, and nothing below closes it.
The results are:

1. **Blocker A is false as posed.**  There is an exact class-B target
   instance of profile \(r=0\) together with a legitimate complement-cover
   six-prefix of pattern \(8^3\,10^3\) that extends to **exactly eight** and
   never to nine — not by three size-ten supports, and not by any three of
   the eleven remaining supports.  (Theorem 1.)

2. **A uniform repair.**  Every complement-cover six-prefix whose union
   \(D\) blocks any size-ten support does so through a unique *saturated
   core*, a \(K_6\) or a \(K_{5,5}\); a single support-preserving,
   degree-preserving two-edge switch destroys it and creates no other.
   After the switch **every** ten-subset of the thirteen vertices spans a
   perfect matching of \(K_{13}-D\).  (Theorem 2 and Lemma 3.)
   This simultaneously repairs the repository's \(r=2\) obstruction
   (blocker C: the switched prefix reaches nine with pattern
   \(8^4\,10^3\,12^2\)) and upgrades the \(r=1\) step-one statement of
   `../../coordinated_eight_r1/NOTE.md` from "at least one remaining
   size-ten support extends" to "all of them do" (blocker B, step one).

3. **Blocker B's residual catalogue is sharpened** and \(K_{3,3,3}\) is
   eliminated by a one-line covering argument.  The second and third steps
   are **not** proved.  The run proposed Statement (T3) after 27,000
   supporting tests; a post-run independent audit then produced an exact
   class-B counterexample to T3.  The corrected frontier is recorded below.

4. **Global bridge.**  Every level of the lift tower is a proper
   \(17\)-colouring of a Johnson graph, and the whole family of those
   conditions collapses **exactly** onto the derivation tower
   \(LS(t-1,t,16+t)\), \(1\le t\le16\) — whose top member *is* the problem.
   So the levelwise layer carries no information beyond the known shadow
   chain (Theorems 5 and 6: a route delimiter).  The genuine residual
   content is identified exactly: it is a **per-colour simultaneous
   six-packing across the star of a six-set** (Theorem 8), a coupling that
   the class-B question — a conjunction of independent per-\(P\) statements —
   cannot see.

5. **A scope theorem for the whole coordinated-nine programme.**  The
   average first-lift profile index is exactly \(1\):
   \(\sum_{P\in\binom U5}r(P)=\binom{19}5=11628\) for every
   \(LS(2,3,19)\) link.  Hence at least two thirds of the 11,628 first-lift
   instances have \(r\le2\) and at least one half have \(r\le1\) — the two
   profiles that are **not** proved.  For the repository's committed cyclic
   link the exact distribution is \((3519,5151,2397,561,0,0)\) for
   \(r=0,\dots,5\): the proved profiles \(r=3,4,5\) account for
   \(561/11628=4.8\%\) of the instances.  (Theorem 7.)

### Post-run independent audit

The Opus run finished before the parallel \(r=0\) audit.  That audit found
that Statement (T3) in Section 4 is false even under the full
complement-cover and class-B hypotheses.  The exact certificate is
[`../../r0_three_ten_obstruction/K6_FREE_THREE_TEN_OBSTRUCTION.md`](../../r0_three_ten_obstruction/K6_FREE_THREE_TEN_OBSTRUCTION.md):
the union \(D\) is \(K_6\)-free and \(K_{5,5}\)-free, all seven relevant
ten-supports are individually matchable, but six families force one common
edge, so no three of them pack.  A sharper mixed dead-prefix certificate and
a universal equality-core trade are in
[`../../r0_three_ten_obstruction/K6_FREE_MIXED_DEAD_PREFIX.md`](../../r0_three_ten_obstruction/K6_FREE_MIXED_DEAD_PREFIX.md).

Accordingly, the deterministic random sweep below is retained only as an
audit of the search that was actually run; its conjectural inference is
withdrawn.  Theorem 1, Lemmas 3–4, Theorem 2, Corollary A, and Theorems 5–9
are unaffected.

---

## 1. Setting and notation

Throughout \(V\) is a \(13\)-set, \(K_{13}\) the complete graph on it.  A
*class-B target instance* is a family of seventeen complements
\(B_1,\dots,B_{17}\subseteq V\) with every \(|B_c|\in\{1,3,5\}\) and every
vertex in exactly five of them; the supports are \(V_c=V\setminus B_c\) with
\(|V_c|\in\{8,10,12\}\), and the profile index is \(r=n_{12}\), so
\[
 (n_8,n_{10},n_{12})=(7+r,\;10-2r,\;r),\qquad 0\le r\le5 .
\tag{1}
\]
A *packing* is a family of pairwise edge-disjoint perfect matchings
\(M_c\subseteq K_{13}[V_c]\).  *Coordinated nine* is the assertion that nine
such matchings always exist.

A *complement-cover six-prefix* is a choice of six of the seventeen
complements whose union is all of \(V\), together with an edge-disjoint
packing of the six corresponding supports; \(D\) denotes the union of the six
matchings and \(H=K_{13}-D\).  Writing \(\sigma(v)\) for the number of
selected complements containing \(v\) and \(\rho(v)\) for the number of
remaining ones,
\[
 d_D(v)=6-\sigma(v),\qquad \rho(v)=5-\sigma(v)=d_D(v)-1,
\tag{2}
\]
so the cover gives \(\Delta(D)\le5\) and \(\delta(H)\ge7\), and
\(1\le d_D(v)\le5\) for every \(v\).  With \(s=\sum_i|B_{c_i}|\) over the six
selected complements,
\[
 \sum_{v}d_D(v)=78-s,\qquad |E(D)|=\tfrac{78-s}2 .
\tag{3}
\]
The repository's covers are \(3+3\) at \(r=0\) (\(s=24\), \(|E(D)|=27\)) and
\(4+2\) at \(r\ge1\) (\(s=26\), \(|E(D)|=26\)).

---

## 2. Blocker A: the six-prefix route at \(r=0\) is false

> **Theorem 1.**  There is a class-B target instance of profile
> \((n_8,n_{10},n_{12})=(7,10,0)\) and a complement-cover six-prefix of
> support pattern \(8^3\,10^3\) whose residual graph \(H=K_{13}-D\)
> satisfies \(\delta(H)\ge7\) and for which **exactly two** of the eleven
> remaining supports carry a perfect matching of \(H\).  Consequently the
> prefix extends to eight and to no more.  The instance itself is not a
> counterexample to coordinated nine: a different packing of the *same* six
> selected supports extends to nine.

### The certificate

Vertices \(0,\dots,12\).  Put \(C=\{0,1,2,3,4,5\}\), \(O=\{6,\dots,12\}\).

Selected complements (three five-sets, three triples), covering \(V\):
\[
\begin{array}{ll}
G_1=\{0,1,6,10,11\}, & T_1=\{6,7,8\},\\
G_2=\{2,4,7,11,12\}, & T_2=\{6,7,9\},\\
G_3=\{3,5,6,7,12\}, & T_3=\{6,7,10\}.
\end{array}
\tag{4}
\]
Remaining complements: the four five-sets \(C\setminus\{c\}\) for
\(c=0,1,2,3\); the five triples
\(\{8,9,10\},\{8,9,11\},\{8,10,12\},\{9,11,12\},\{10,11,12\}\); and the two
triples \(\{0,1,8\}\), \(\{2,3,9\}\).  Every vertex lies in exactly five of
the seventeen complements, and the profile is \(7\times5\text{-set}+
10\times3\text{-set}\), i.e. \(r=0\).

The six prescribed matchings:
\[
\begin{array}{ll}
M_{G_1}=\{34,\,25,\,79,\,8\,12\}, & M_{T_1}=\{01,\,23,\,45,\,9\,11,\,10\,12\},\\
M_{G_2}=\{13,\,05,\,68,\,9\,10\}, & M_{T_2}=\{02,\,14,\,35,\,8\,10,\,11\,12\},\\
M_{G_3}=\{04,\,12,\,89,\,10\,11\}, & M_{T_3}=\{03,\,15,\,24,\,8\,11,\,9\,12\}.
\end{array}
\tag{5}
\]
They are pairwise edge-disjoint, each saturates its support, and
\[
 D=K_6[C]\ \dot\cup\ D'',\qquad |E(D)|=15+12=27,\qquad \Delta(D)=5 .
\tag{6}
\]
Here \(D''=K_5[\{8,\dots,12\}]+\{68\}+\{79\}\) on \(O\).

### Why nothing extends

\(C\) is independent in \(H\) and \(H\) contains every \(C\)–\(O\) edge.
Hence any support \(S\) with \(|S\cap C|>|S\setminus C|\) is dead.

* the five remaining triples inside \(\{8,\dots,12\}\) give supports with
  \(|S\cap C|=6>4\): **dead**;
* \(H[O]\) has exactly nine edges, all incident with \(6\) or \(7\), so its
  matching number is \(2\).  A remaining size-eight support
  \(\{c\}\cup O\) needs three disjoint \(H[O]\)-edges: **dead** (all four);
* the two mixed triples \(\{0,1,8\}\), \(\{2,3,9\}\) do extend.

So the prefix extends by at most two.  Both extensions are compatible, so it
extends to exactly eight.  A separate depth-first search finds a nine-packing
of the same instance using \(G_1,G_2,G_3\), three of the remaining five-sets,
and \(T_1,T_2,T_3\) — a different packing of the same six selected supports.

This is the exact class-B counterexample blocker A asked for.  It is strictly
stronger than the repository's \(r=2\) obstruction
(`../../coordinated_nine_r2_obstruction/NOTE.md`), which kills only the
size-ten supports and still reaches nine through a size-eight support.

---

## 3. The saturated-core switching theorem

Call a subgraph of \(D\) a **saturated core** if it is a \(K_6\) or a
\(K_{5,5}\).  Under \(\Delta(D)\le5\) each of its vertices has *all* its
\(D\)-edges inside the core, and the core's neighbourhood structure is
completely rigid.

> **Lemma 3 (universal ten-set matchability).**  Let \(H\) be a graph on a
> \(13\)-set with \(\delta(H)\ge7\), and suppose \(D=K_{13}-H\) contains no
> \(K_6\) and no \(K_{5,5}\).  Then \(H[S]\) has a perfect matching for
> **every** \(S\in\binom V{10}\).

*Proof.*  \(\delta(H[S])\ge7-3=4\).  Suppose \(H[S]\) has no perfect
matching and let \(Q\), \(|Q|=q\), be a Tutte set, so \(H[S]-Q\) has
\(m\ge q+2\) odd components, of orders \(a_1\le\dots\le a_m\) summing to at
most \(10-q\).  A vertex of an odd component of order \(a\) has
\(4\le a-1+q\), so \(a\ge5-q\).

*\(q=0\):* \(a_i\ge5\) and odd, \(m\ge2\), \(\sum a_i\le10\); hence \(m=2\),
\(a_1=a_2=5\) and there is no even component.  So \(S\) splits into two
\(5\)-sets with no \(H\)-edge between them, i.e. \(D\supseteq K_{5,5}\).
*\(q=1\):* \(a_i\ge5\), \(m\ge3\), \(\sum\ge15>9\).
*\(q=2\):* \(a_i\ge3\), \(m\ge4\), \(\sum\ge12>8\).
*\(q=3\):* \(a_i\ge3\), \(m\ge5\), \(\sum\ge15>7\).
*\(q=4\):* \(\sum a_i\le6\) and \(m\ge6\), so there are exactly six singleton
odd components and no even component; those six vertices are pairwise
non-adjacent in \(H\), i.e. \(D\supseteq K_6\).
*\(q\ge5\):* \(q+2\le m\le\sum a_i=10-q\) forces \(q\le4\).
Both surviving cases are excluded by hypothesis. \(\square\)

The converse is immediate: a \(K_6\) on \(C\) blocks every ten-set
containing \(C\), and a \(K_{5,5}\) blocks its own ten-set.  So for a
complement-cover six-prefix, **a size-ten support is blocked if and only if
\(D\) has a saturated core inside it**.

> **Lemma 4 (uniqueness, and \(r\ge1\) kills \(K_{5,5}\)).**  Let
> \(\Delta(D)\le5\).
> (a) \(D\) contains at most one \(K_6\), at most one \(K_{5,5}\), and never
> both.
> (b) If the six selected complements have total size \(s\ge26\) — in
> particular for every \(4+2\) cover, i.e. every profile \(r\ge1\) treated in
> the repository — then \(D\) contains no \(K_{5,5}\).

*Proof.* (a) If \(v\) lies in a \(K_6\) on \(C\) then
\(N_D(v)=C\setminus\{v\}\) exactly.  For two \(K_6\)'s on \(C,C'\) meeting in
\(t\) vertices, a common vertex has at least \(11-t\) \(D\)-neighbours, so
\(t\ge6\) and \(C=C'\).  For a \(K_{5,5}\) with parts \(X,Y\), a vertex of
\(X\) has \(N_D=Y\) exactly.  Two such cores meet in at least
\(10+10-13=7\) vertices; a common vertex forces one part of the first core to
equal a part of the second, and then the other parts agree as well.  Finally
a \(K_6\) on \(C\) and a \(K_{5,5}\) on \(X\dot\cup Y\) meet in at least
\(6+10-13=3\) vertices; a common vertex \(v\in C\cap X\) forces
\(Y=N_D(v)=C\setminus\{v\}\), and then any \(y\in Y\) forces
\(X=N_D(y)=C\setminus\{y\}\), contradicting \(X\cap Y=\varnothing\).

(b) By (2)–(3), \(\sum_vd_D(v)=78-s\) and \(d_D(v)\ge1\) for every \(v\).
A \(K_{5,5}\) pins ten vertices at \(d_D=5\), so
\(78-s\ge50+3=53\), i.e. \(s\le25\). \(\square\)

> **Theorem 2 (saturated-core switch).**  Let \(D\) be the union of a
> complement-cover six-prefix, so \(\Delta(D)\le5\) and \(|E(D)|\le27\).  If
> \(D\) contains a saturated core, then a single two-edge switch inside one
> of the six matchings — preserving every prescribed support, every vertex
> degree, and every complement — produces a packing of the same six supports
> whose union contains **no** saturated core.

*Proof.*
**Case \(K_6\) on \(C\).**  Every \(v\in C\) has \(N_D(v)=C\setminus\{v\}\),
so no \(D\)-edge leaves \(C\); consequently every prefix matching \(M_i\)
pairs \(C\setminus B_i\) inside \(C\) and \((V\setminus C)\setminus B_i\)
inside \(V\setminus C\).  In particular \(|B_i\cap C|\) is even, hence
\(\le4\), so \(|C\setminus B_i|\ge2\) and \(M_i\) has an edge \(e=cc'\)
inside \(C\); and \(|B_i\setminus C|\le5\), so
\(|(V\setminus C)\setminus B_i|\ge2\) and \(M_i\) has an edge \(f=uv\)
outside \(C\).  Replace \(e,f\) by \(cu,\,c'v\).  Both new edges join \(C\) to
its complement, so they lie in no \(M_j\) and in no part of \(D\); the
modified \(M_i\) is still a perfect matching on the same support and no
degree changes.  Write \(D'\) for the new union.

\(D'\) has no \(K_6\): for \(w\in C\setminus\{c,c'\}\),
\(N_{D'}(w)=C\setminus\{w\}\), so the only candidate through \(w\) is \(C\),
which lost the edge \(cc'\); for \(c\), \(N_{D'}(c)=(C\setminus\{c,c'\})
\cup\{u\}\), so the only candidate is \((C\setminus\{c'\})\cup\{u\}\), but
\(u\notin N_{D'}(w)\) for \(w\in C\setminus\{c,c'\}\); symmetrically for
\(c'\); and a \(K_6\) missing \(C\) would need fifteen edges inside
\(D'[V\setminus C]\), which has \(|E(D)|-16\le11\) of them.

\(D'\) has no \(K_{5,5}\): for \(w\in C\setminus\{c,c'\}\) its opposite part
would be \(C\setminus\{w\}\); picking \(y\in C\setminus\{w,c,c'\}\) in that
part gives \(N_{D'}(y)=C\setminus\{y\}\supseteq w\)'s part, and disjointness
forces \(w\)'s part \(\subseteq\{w\}\).  For \(c\), the opposite part is
\((C\setminus\{c,c'\})\cup\{u\}\) and the same step forces \(c\)'s part
\(\subseteq\{c,c'\}\); symmetrically for \(c'\).  A core missing \(C\) needs
ten vertices among the seven outside \(C\).

**Case \(K_{5,5}\) with parts \(X,Y\).**  Every core vertex has \(N_D=\)
opposite part, so \(X\) and \(Y\) are independent in \(D\) and no \(D\)-edge
joins \(X\cup Y\) to the remaining three vertices \(Z\).  Every prefix
matching meets \(X\cup Y\) only in \(X\)–\(Y\) edges, and those twenty-five
edges are distributed over six matchings, so some \(M_i\) contains at least
five of them, in particular two, say \(a_1b_1,a_2b_2\) with \(a_j\in X\),
\(b_j\in Y\).  Replace them by \(a_1a_2,\,b_1b_2\), which are non-edges of
\(D\); supports and degrees are unchanged.  The same neighbourhood argument
as above shows the new union has neither a \(K_{5,5}\) nor a \(K_6\), the
outside case being impossible because \(D[Z]\) has at most two edges and
\(|Z|=3\). \(\square\)

> **Corollary A (uniform first extension).**  For every class-B target
> profile, every complement-cover six-prefix can be replaced — with the same
> six complements and the same degree sequence — by one for which **every**
> ten-subset of \(V\), hence every remaining size-ten support, carries a
> perfect matching of \(H\).

This is exactly what the three blockers needed at their first step, and it is
sharp: the size-eight catalogue under \(\Delta(D)\le5\) is
\(\{K_{3,5},\,K_{3,1,1,1},\,K_5\}\), and a \(K_5\) is compatible with
\(\alpha(H)\le5\), so size-eight supports can still be blocked after the
switch — as they all are in the certificate of Theorem 1.

### Blocker C (\(r=2\)) is closed by the same switch

Applying Theorem 2 to the repository's \(r=2\) certificate
(`../../coordinated_nine_r2_obstruction/NOTE.md`, whose \(D\) is
\(K_6[\{7..12\}]\dot\cup K_5[\{2..6\}]\dot\cup K_2[\{0,1\}]\)): switch
\(7\,11\) and \(2\,6\) inside \(M_0\) to \(2\,7\) and \(6\,11\).  The union
keeps all six supports and all degrees, contains no saturated core, and every
ten-subset becomes matchable.  The switched prefix then extends to **nine**
with pattern \(8^4\,10^3\,12^2\) — one remaining size-ten support plus both
size-twelve supports, exactly the strategy the repository's note had declared
false for the unswitched prefix.  Verified.

---

## 4. Blocker B: what is settled and what is not

After Corollary A the first extra size-ten matching \(M\) exists for **all**
remaining size-ten supports (strengthening
`../../coordinated_eight_r1/NOTE.md`, which proved only that one exists, and
replacing its \(K_{5,5}\)/\(K_6\) incidence argument by Lemma 4).

For a second size-ten support inside \((K_{13}-D)-M\) the exact coarsened
Tutte catalogue at \(\Delta(D\cup M)\le6\) is
\[
 K_{5,5},\qquad K_{3,3,3},\qquad K_{3,1,1,1,1},\qquad K_6 ,
\tag{7}
\]
and \(K_{3,3,3}\) is impossible: all nine of its vertices have core degree
\(6>5=\Delta(D)\), so each must meet an edge of the single matching \(M\)
inside the core, but a matching covers at most \(2\lfloor9/2\rfloor=8\) of
nine vertices.  The catalogue for a third support is
\(\{K_{3,7},K_{5,5},K_{3,3,3},K_{5,1,1,1},K_{3,3,1,1},K_{3,1,1,1,1},K_6\}\).

Structure forced in the \(K_{3,1,1,1,1}\) case (the case blocker B singles
out): the four singleton blocks have \(D\cup M\)-degree exactly \(6\), hence
\(d_D=5\), \(\sigma=1\), \(\rho=4\), no \(D\cup M\)-edge outside the seven
core vertices, and each is covered by an \(M\)-edge inside the core.  Since
the three-block has only three vertices, at least one \(M\)-edge joins two
singleton blocks; the only two possibilities are that \(M\) pairs the four
singletons \(2+2\), or pairs two of them and sends the other two into the
three-block.

**Post-run audit: the following proposed obligation is refuted.**

> **Statement (T3).**  Let \(D\) be the union of six matchings on thirteen
> vertices with \(\Delta(D)\le5\), \(|E(D)|\le27\), containing no \(K_6\) and
> no \(K_{5,5}\), and put \(H=K_{13}-D\).  Then for any three ten-subsets
> \(S_1,S_2,S_3\) there are pairwise edge-disjoint perfect matchings
> \(M_i\subseteq H[S_i]\).

(T3) plus Theorem 2 would have given coordinated nine for \(r=0\) outright,
and would have supplied blocker B's steps two and three.  A deterministic
pseudo-random sweep generated **900** core-free complement-cover six-prefixes
(shapes \(3+3\) and \(4+2\)) and tested **27,000** ordered triples of
ten-sets; every one packed.  This is search evidence, not a proof, and (T3)
is false: the structured \(K_6-e\) equality certificate linked in the
post-run audit satisfies every hypothesis and leaves six ten-support
families forcing the same edge.  The sweep simply did not sample that thin
structured family.  The corresponding *hypothesis-free* statement —
\(\delta(H)\ge7\) alone — is also false, already by Theorem 1.

---

## 5. Global bridge

Let \(V\) be a \(32\)-set, \({\cal C}\) a \(17\)-set of colours, and let
\(c:\binom V{16}\to{\cal C}\) be a proper colouring of \(J(32,16)\).  Fix a
split \(V=U\dot\cup A\), \(u=|U|\ge16\), and for \(B\subseteq A\) put
\[
 G_B(Q)=c\bigl((U\setminus Q)\cup B\bigr),\qquad
 Q\in\binom U{\,u-16+|B|\,}.
\tag{8}
\]
This is the tower of `../../unrestricted_lift_tower/NOTE.md` (there \(u=19\)).

> **Theorem 5 (levelwise Johnson colourings).**  For every split and every
> \(B\subseteq A\), the map \(Q\mapsto(U\setminus Q)\cup B\) is an
> adjacency-preserving injection \(J(u,s)\hookrightarrow J(32,16)\), where
> \(s=u-16+|B|\).  Hence \(G_B\) is a proper \(17\)-colouring of
> \(J(u,s)\).

*Proof.*  \(|(U\setminus Q)\cup B|=u-s+|B|=16\).  If \(|Q\cap Q'|=s-1\) then
the images meet in \(u-s-1+|B|=15\) points, so they are adjacent in
\(J(32,16)\) and get different colours. \(\square\)

Thus a \(17\)-colouring of \(J(32,16)\) forces \(\chi(J(u,s))\le17\) for
every pair with \(u\le s+16\) (the pairs realised by some split and level).
The natural hope is that one of these is provably impossible.  It is not:

> **Theorem 6 (collapse to the derivation tower).**  For every \(t\ge1\),
> \[
>  \chi\bigl(J(16+t,\;t)\bigr)\le17
>  \iff
>  LS(t-1,t,16+t)\ \text{exists},
> \]
> and for \(u\le s+16\) the condition \(\chi(J(u,s))\le17\) follows from
> \(LS(s-1,s,16+s)\) by restriction to a \(u\)-subset.  The conditions form a
> descending chain, whose top member \(t=16\) is \(\chi(J(32,16))\le17\)
> itself.  Consequently the entire levelwise layer of the tower is **exactly**
> the derivation tower and yields no information beyond it.

*Proof.*  An independent set of \(J(n,t)\) is a family of \(t\)-sets no two
sharing \(t-1\) points, i.e. a partial \(S(t-1,t,n)\), of size at most
\(\binom n{t-1}/t\).  With \(n=16+t\) the exact identity
\(\binom{16+t}{t}\,t=17\binom{16+t}{t-1}\) (checked for \(t=1..16\)) says the
seventeen classes of any proper \(17\)-colouring must all attain that bound,
i.e. be perfect Steiner systems; conversely a large set is such a colouring.
Restriction of a large set to a \(u\)-subset preserves both the partial
Steiner property and the partition property.  Derivation at a point sends
\(LS(t,t+1,17+t)\) to \(LS(t-1,t,16+t)\), which gives the chain. \(\square\)

At \(t=3\) this is \(LS(2,3,19)\) (exists); at \(t=4\) it is \(LS(3,4,20)\)
(open, the repository's shadow); at \(t=15\) it is \(LS(14,15,31)\), which the
repository already records as equivalent to \(k=16\).  **So the answer to
"what beyond class B would imply a 17-colouring" is not to be found in this
layer.**

### Where the content actually is

At the split \(u=19\), level \(1\) is the simultaneous \(13\)-fan and level
\(2\) is the family \(G_{\{a,b\}}:\binom U5\to{\cal C}\).  The tower law at
level \(1\) says that for each \(P\) the map \(b\mapsto G_{\{a,b\}}(P)\) is a
**bijection** onto \({\cal C}\setminus S_a(P)\); that is exactly the class-B
completion problem at \(P\), one independent problem per \(P\).  The genuine
coupling is level-\(2\) top-properness, and it has an exact packing form.

> **Theorem 8 (the coupling is a per-colour six-packing).**  Fix
> \(R\in\binom U6\) and write \(P_x=R\setminus\{x\}\).  Level-\(2\)
> top-properness at \(R\) holds if and only if, for every colour \(\gamma\),
> the six perfect matchings \(M_\gamma(P_x)\subseteq K_A\), \(x\in R\), are
> **pairwise edge-disjoint**.  Their sizes satisfy
> \[
>   \sum_{x\in R}\bigl|M_\gamma(P_x)\bigr| = 24+3\,t_\gamma(R),
>   \qquad t_\gamma(R)=\#\{T\in\tbinom R3:L(T)=\gamma\}\le4 .
> \]

*Proof.*  \(h_{P_x}(ab)=\gamma\) exactly when \(ab\in M_\gamma(P_x)\), so the
six values at an edge are distinct precisely when no edge is used twice.  By
Theorem 4 of the tower note \(|M_\gamma(P)|=4+t_\gamma(P)\); each
\(\gamma\)-triple of \(R\) lies in three of the six five-subsets, and a
\(6\)-set carries at most four pairwise-\(1\)-intersecting triples. \(\square\)

So the residual global condition is a *coordinated six-packing across six
different class-B instances*, whereas all the repository's coordinated-\(n\)
theorems are packings *inside one* instance.  That is the precise sense in
which class B — even answered affirmatively — cannot bridge to \#835: class B
is a conjunction of \(\binom{19}5=11628\) independent existence statements,
while Theorem 8 is a simultaneous-choice statement over the
\(\binom{13}2\binom{19}6=78\cdot27132=2{,}116{,}296\) star constraints, and
no per-\(P\) strengthening can imply it.

### Forced global data (necessary conditions, all satisfied)

> **Theorem 9.**  Assume a simultaneous \(13\)-fan.  For every \(a\in A\) and
> \(\gamma\in{\cal C}\):
> \(\#\{Q\in\binom U4:F_a(Q)=\gamma\}=228\);
> \(\#\{P\in\binom U5:\gamma\in S_a(P)\}=3420\);
> \(\#\{P:\gamma\notin S_a(P)\}=8208\); and therefore
> \(\sum_{b\ne a}\#\{P:G_{\{a,b\}}(P)=\gamma\}=8208=12\cdot684\).

*Proof.*  \(\widehat F_a\) is an \(LS(3,4,20)\); each class has
\(\binom{20}3/\binom43=285\) blocks and \(\binom{19}2/\binom32=57\) of them
contain \(a\), leaving \(228\), and \(17\cdot228=\binom{19}4\).  Two
\(\gamma\)-quadruples cannot lie in one five-set (they would meet in three
points), so each contributes \(15\) five-sets, giving \(3420\); the bijection
of the level-\(1\) tower law distributes the remaining \(8208\) over the
twelve partners \(b\).  The number \(684\) is also
\(1197-285-285+57\), the number of blocks of an \(S(4,5,21)\) avoiding two
prescribed points, and \(17\cdot684=\binom{19}5\). \(\square\)

### Scope: which profiles actually occur

> **Theorem 7 (profile average, and the scope of coordinated nine).**  Let
> \(L\) be any \(LS(2,3,19)\) and \(r(P)=n_{12}(P)\) the first-lift profile
> index at \(P\in\binom U5\).  Then
> \[
>  \sum_{P\in\binom U5}r(P)=17\cdot19\cdot\binom92=11628=\binom{19}5 ,
> \]
> so the average profile index is exactly \(1\).  Consequently
> \(\#\{P:r(P)\le2\}\ge\tfrac23\cdot11628=7752\) and
> \(\#\{P:r(P)\le1\}\ge\tfrac12\cdot11628=5814\).

*Proof.*  \(t_\gamma(P)=2\) means \(P\) is the union of two \(\gamma\)-triples
meeting in one point, and such a pair is determined by \(P\); each point of
\(U\) lies in \((19-1)/2=9\) triples of a fixed \(STS(19)\), giving
\(19\binom92=684\) such pairs per colour and \(17\cdot684=11628\) in total.
The two bounds are Markov's inequality on a non-negative integer statistic
with mean \(1\). \(\square\)

For the repository's committed cyclic link the exact distribution over the
\(11{,}628\) first-lift instances is
\[
 (r=0,1,2,3,4,5)\ \longmapsto\ (3519,\;5151,\;2397,\;561,\;0,\;0).
\tag{9}
\]
The profiles for which coordinated nine **is** proved (\(r=3,4,5\)) therefore
cover \(561\) instances, \(4.8\%\) of the total; the unresolved profiles
\(r=0,1\) cover \(8670\), i.e. \(74.6\%\).  This is a statement about the
coverage of the current theorems, not about their correctness.

---

## Gap audit

What is **proved** here, unconditionally:

* Theorem 1 (the \(r=0\) counterexample) — an explicit finite certificate,
  every step exhaustively verified.
* Lemma 3, Lemma 4, Theorem 2, Corollary A — solver-free proofs; the finite
  Tutte catalogues they rest on are additionally re-enumerated by machine.
* The \(K_{3,3,3}\) elimination of Section 4.
* The \(r=2\) repair (blocker C): explicit switch plus an explicit
  nine-packing.
* Theorems 5–9 of Section 5.

What is **not** proved:

* Statement (T3) is **false**, by the post-run \(K_6-e\) equality
  certificate linked above.  Steps two and three of blockers A and B remain
  **open**, but T3 is no longer a viable route.  In particular
  **coordinated nine is not proved for \(r=0,1,2\)**, and the headline claim
  of this note is a repaired first step plus a counterexample, not a theorem
  for those profiles.
* The \(K_{3,1,1,1,1}\) case of blocker B: only its forced local structure is
  derived; no switch is exhibited.
* Nothing here bears on whether every class-B instance completes to all
  seventeen matchings.
* Theorem 7's distribution (9) is computed for the repository's committed
  cyclic link; only the sum rule and the two Markov bounds are
  link-independent.  In particular I do **not** claim \(r\le3\) always.
* Theorem 9 assumes a simultaneous \(13\)-fan exists; it is forced structure
  inside a hypothetical solution, not an obstruction.  Every identity it
  produces is satisfied, so it excludes nothing.
* Theorem 8's "no per-\(P\) strengthening can imply it" is an observation
  about the logical form of the two statements (a conjunction of independent
  existence claims versus a simultaneous choice), not a formal independence
  proof.  I did not construct two individually-completable instances with no
  compatible pair of completions.

Numbers used above and where each comes from: \(|E(D)|=27\) and
\(\Delta(D)=5\) for the \(r=0\) certificate, matching number \(2\) of
\(H[O]\), and "exactly two of eleven remaining supports extendable" are all
outputs of `verify_r0_prefix_obstruction.py`.  The catalogues, the switch,
and the \(r=2\) repair are outputs of `verify_saturated_core_switch.py`.
\(900\) prefixes / \(27{,}000\) triples / \(0\) counterexamples is the output
of `search_three_ten_sets.py 900`.  The distribution (9), the sum rule, the
ratio identities and Theorem 9's counts are outputs of
`verify_global_bridge.py`.

## Scope relative to #835

Erdős–Rosenfeld Problem #835 is **open**, and \(k=16\) is **not** settled
here.  Concretely:

* Coordinated nine is a fragment of the first lift, which is a fragment of
  level \(2\) of a thirteen-level tower.  Even a full proof of coordinated
  nine for all six profiles, and even a full proof that every class-B
  instance completes, would not give a \(17\)-colouring of \(J(32,16)\):
  Theorem 8 shows the missing content is a simultaneous choice across
  five-sets, and Theorem 6 shows the whole levelwise layer of the tower is
  already equivalent to the derivation tower \(LS(t-1,t,16+t)\) whose top
  member is the problem itself.
* Theorem 7 quantifies how much of the first lift the existing
  coordinated-nine theorems reach: for the committed link, \(4.8\%\) of the
  \(11{,}628\) instances.
* Theorem 1 removes one specific proof strategy; Theorem 2 restores it at
  its first step for all six profiles.  Neither is a colouring and neither is
  an obstruction.

## Files and commands

All files are new and live in this directory; no existing note was edited.

```sh
cd "<repo root>"
python3 -B collaboration/opus5/coordinated_nine_and_global_bridge/verify_r0_prefix_obstruction.py
python3 -B collaboration/opus5/coordinated_nine_and_global_bridge/verify_saturated_core_switch.py
python3 -B collaboration/opus5/coordinated_nine_and_global_bridge/verify_global_bridge.py
python3 -B collaboration/opus5/coordinated_nine_and_global_bridge/search_three_ten_sets.py 900
```

The first three are deterministic, standard-library only, and use no
optimizer or SAT solver; each prints a `PASS`/`FAIL` line per claim and ends
with `ALL CHECKS PASS`.  The fourth is a fixed-seed search driver: its output
is evidence, not a proof, and no claim above rests on it alone.
`verify_global_bridge.py` imports the repository's committed cyclic
\(LS(2,3,19)\) from `collaboration/cyclic_lsts19_extension`; if that import
fails it prints `SKIP` for the empirical part and still checks every
arithmetic identity.

## Next irreducible obligations

1. **Finish the \(r=0\) equality-core trade.**  T3 is refuted.  The exact
   remaining boundary has a \(K_6-e\) core, six triple complements avoiding
   it, and one of \((a,r)=(0,2),(0,3),(1,3)\).  A universal
   support-preserving trade gives two alternative internal core edges to all
   six families; what remains is to coordinate two of those families with
   the seventh support.
2. **Settle the \(K_{3,1,1,1,1}\) case** with the forced structure of
   Section 4 (four singleton blocks at \(d_D=5\), \(\rho=4\), matched by
   \(M\) inside the core in one of exactly two patterns).
3. **Decide whether a core-free prefix always exists that also survives two
   further matchings**, i.e. whether the invariant "no saturated core" is the
   *weakest* one that works, or must be strengthened to a condition on
   \(D\cup M_1\).
4. **On the global side:** the only statement that would advance \#835
   through this route is a handle on Theorem 8's simultaneous six-packing —
   for instance an obstruction to choosing, for one colour \(\gamma\) and one
   \(R\in\binom U6\), six pairwise edge-disjoint prescribed matchings whose
   supports are the six \(V_\gamma(P_x)\).  Their total size is
   \(24+3t_\gamma(R)\le36\) inside \(78\) edges, so no counting obstruction
   exists; any obstruction must use the prescribed supports.
5. **Do not** invest further in levelwise Johnson-colouring conditions: by
   Theorem 6 they are exactly the derivation tower.
