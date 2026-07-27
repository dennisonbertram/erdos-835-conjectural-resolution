# The holonomy tower identity is pure gauge, and its universal affine mod-2 arithmetic is two functionals wide

## 0. Scope, stated first

**Erdős–Rosenfeld problem #835 remains OPEN.**  Nothing here constructs a large
set, excludes \(k=16\), or decides \(LS(3,4,20)\), \(LS(4,5,21)\),
\(LS(14,15,31)\) or \(LS(15,16,32)\).  No solver was run.

The concrete successor question left behind by the holonomy work — *can
universal affine mod-\(2\) congruences, linear-representation projections,
orientation refinements, or aggregate overlap compatibility of attainable
\(LS(2,3,19)\) holonomy censuses make the tower's componentwise-even identity
contradictory?* — is answered here **negatively and unconditionally**:

* **Theorem A (gauge vacuity, \(t\ge2\)).**  The holonomy tower identity, its exact
  \(\mathbb Z[S_m]\) lift, the image of that lift under **every** linear
  representation or permutation module of \(S_m\), the refinement by the fixed
  colour, and the orientation symmetry all hold for the holonomy of an
  **arbitrary family of bijections indexed by \(t\)-sets** — no design property
  of any kind is used.  Hence none of them can ever be contradictory, and none
  of them carries information about existence.  This closes the door that the
  group-algebra note left explicitly open ("any integral linear representation
  or permutation module of \(S_m\) gives a smaller necessary matrix identity").
* **Theorem B (the overlap system is the problem).**  Twenty \(LS(2,3,19)\)
  with pairwise matching pair-links are *exactly* an \(LS(3,4,20)\).  The
  overlap route is therefore lossless and yields **no reduction**.

What is added on the positive side:

* **Theorem C.**  A triangle law makes the holonomy sign graph balanced for
  every chart family.  When \(m\) is odd, as in the \(m=17\) application, the
  product of holonomy signs over the pairs of one link is exactly
  \(\varepsilon(R)\), and over the whole object is \(E_t(c)^t\).  So in the
  present odd-\(m\) setting the sign layer of the census *is* the already-known
  \(\varepsilon\) layer, and the census determines \(\varepsilon\) by an
  explicit \(\mathbb F_2\) functional.  Theorem C is also gauge-vacuous.
* **Theorem D (the one design-dependent congruence).**  For every
  one-factorization \(F\) of \(K_n\) (\(n\) even),
  \(\sum_{\{a,b\}}m_2(\sigma_{ab})=2\,C_4(F)\), where \(m_2\) counts the
  \(2\)-cycles of the holonomy and \(C_4\) counts alternating \(4\)-cycles.
  Hence \(\sum_{\kappa}N_\kappa\,m_2(\kappa)\equiv0\pmod 2\).  This is **not** a
  consequence of Theorem A: it holds at \(t=1\), where the tower identity does
  not exist.
* **Theorem E (exact arithmetic strength).**  The space of universal
  \(\mathbb F_2\) congruences on the census is **exactly two-dimensional** —
  spanned by the total count and Theorem D — at \(n=10\) (exhaustive over all
  \(396\) isomorphism classes), at \(n=12\), and at \(n=18\), the size that
  governs \(LS(3,4,20)\).  At \(n=8\) there is one extra congruence, and it is
  an accident that does not generalise.  At \(n=10\) there is, over
  \(\mathbb Q\), no linear constraint beyond the total count.

Consequence, stated exactly: the tower identity and all of its linear
projections are gauge-vacuous, while the universal affine mod-\(2\) arithmetic
of a standalone \(K_{18}\) link consists of two identities.  **No obstruction
can be obtained merely by projecting or orientation-refining the tower
identity, imposing universal affine mod-\(2\) equations on each link, or
replacing exact overlap by equality of aggregate holonomy sums.**  This does
not exclude other representation-theoretic restrictions on *attainable*
holonomy sums, or nonlinear, integral, positivity, and joint-feasibility uses
of the \(190\) link censuses.  §8 says where the live content sits instead.

Claims are marked **proved** or **certified computational** (exact finite
computation by `verify_holonomy_followup.py`, 94 checks, no solver, no
network).  Priority is claimed for nothing; §9 records what the primary
literature already contains, including the parts that could not be confirmed.

**Concurrency caveat.**  While this note was being written
(file modification times 02:45 and 02:55 EDT, 27 July 2026) another process was
modifying
`collaboration/opus5/unrestricted_ls3420_attack_2/{NOTE.md,holonomy.py,verify_star_sign.py}`
and `evidence/holonomy_group_algebra_tower.md`.  Citations to those files are
as read in that window.  This note and its verifier are self-contained: the
only repository input they consume is the committed cyclic \(LS(2,3,19)\)
certificate and the committed catalogue of the \(396\) one-factorizations of
\(K_{10}\).

## 1. Chart families

Let \(X\) be an ordered \(v\)-set, \(t\ge1\), \(m=v-t\).

> **Definition.**  A **chart family** of type \((v,t,m)\) is a family of
> bijections \(g_T:X\setminus T\to[m]\), one for each \(T\in\binom Xt\).
> It satisfies the **design condition** if
> \[
>   g_T(s)=g_{(T\setminus\{r\})\cup\{s\}}(r)\qquad(r\in T,\ s\notin T).
> \]

Design-condition chart families are exactly the \(LS(t,t+1,v)\) colourings:
put \(c(T\cup\{s\})=g_T(s)\), and \(g_T=\chi_T\).  At \(t=1\) they are exactly
the one-factorizations of \(K_v\).

> **Definition (holonomy, defined for every chart family).**  For
> \(R\in\binom X{t-1}\) and \(a\ne b\) in \(X\setminus R\), let
> \(\sigma_R(a,b)\in\operatorname{Sym}([m])\) be the permutation that agrees
> with \(g_{R\cup b}\,g_{R\cup a}^{-1}\) wherever the latter is defined and
> sends \(g_{R\cup a}(b)\mapsto g_{R\cup b}(a)\).

This is well defined: \(g_{R\cup b}g_{R\cup a}^{-1}\) is a bijection
\([m]\setminus\{g_{R\cup a}(b)\}\to[m]\setminus\{g_{R\cup b}(a)\}\), so exactly
one input and one output are missing.  Under the design condition the two
missing colours coincide, both equal to \(d=c(R\cup\{a,b\})\), and the
completion *fixes* \(d\); that \(d\) is then the **unique** fixed point is
recorded and machine-checked in `unrestricted_ls3420_attack_2` (§5b of its
`NOTE.md`, and the check `every holonomy permutation fixes exactly one colour`
in its verifier), and the resulting support of \(55\) cycle types
(fixed-point-free partitions of \(16\), \(p(16)-p(15)=231-176\)) is likewise
already committed there.  Neither is claimed here; both are used.

\(H(g)=\sum_{R}\sum_{(a,b)\text{ ordered}}[\sigma_R(a,b)]\in\mathbb Z[S_m]\) is
the exact holonomy sum, and \(N_\kappa\) the unordered-pair cycle-type census.
**Throughout, a census index \(\kappa\) is written as the fixed-point-free part
of the cycle type**, so \(\kappa\) is a partition of \(m-1\) into parts
\(\ge2\) and the suppressed part \(1\) is the fixed colour; at \(m=17\) there
are \(55\) such \(\kappa\).
For \(p\in X\) the **derived** chart family is
\(g^p=(g_{T'\cup\{p\}})_{T'\in\binom{X\setminus\{p\}}{t-1}}\), of type
\((v-1,t-1,m)\) — the same \(m\).

## 2. Theorem A: the tower identity is gauge-vacuous

> **Theorem A (*proved*).**  Let \(g\) be **any** chart family of type
> \((v,t,m)\) with \(t\ge2\).  Then, in \(\mathbb Z[S_m]\),
> \[
>   \boxed{\ \sum_{p\in X}H(g^{\,p})=(t-1)\,H(g).\ }
> \]
> No design condition, no large set, and no design-theoretic hypothesis of any
> kind is used.

*Proof.*  Fix \(p\).  A summand of \(H(g^p)\) is indexed by \((R',a,b)\) with
\(|R'|=t-2\) and \(p,a,b\notin R'\), and by definition of \(g^p\) its two
charts are \(g_{R'\cup\{p,b\}}\) and \(g_{R'\cup\{p,a\}}\) — the same two
charts that define \(\sigma_{R'\cup\{p\}}(a,b)\) for \(g\).  The completion
rule is the same function of those two charts in both cases, so the two
permutations are *equal*, not merely conjugate.  Hence
\(\sigma^{g^p}_{R'}(a,b)=\sigma^{g}_{R'\cup\{p\}}(a,b)\).  A top index
\((R,a,b)\) with \(|R|=t-1\) arises this way once for each \(p\in R\), and
\(|R|=t-1\). \(\square\)

> **Corollary A.1 (*proved*).**  Every consequence of the displayed identity is
> vacuous as an obstruction.  In particular:
>
> **(a)** the cycle-type identity \(\sum_pN_\kappa(g^p)=(t-1)N_\kappa(g)\);
> **(b)** the image of the identity under any linear representation or
> permutation module \(\rho\) of \(S_m\), since \(\rho\) is applied to both
> sides of an identity that already holds in \(\mathbb Z[S_m]\);
> **(c)** the refinement by the fixed colour.  Under the design condition each
> holonomy has exactly one fixed point, so the map
> \([\sigma]\mapsto(\text{cycle type},\text{fixed colour})\) is a function of
> \(\sigma\) alone; the refined census \(N_{\kappa,d}\) is therefore determined
> by \(H\) by a fixed linear rule (an ordered pair and its inverse share both
> the cycle type and the fixed colour, so the ordered refined count is twice
> the unordered one), and the refined identity is that rule applied to (A);
> **(d)** the orientation layer, because \(\sigma_R(b,a)=\sigma_R(a,b)^{-1}\)
> makes \(H\) invariant under the antipode \(g\mapsto g^{-1}\) for every chart
> family, so no orientation-sensitive functional exists to begin with.
>
> Consequently the componentwise-even condition on the twenty derived
> \(LS(2,3,19)\) of a putative \(LS(3,4,20)\) — in the cycle-type form, the
> exact \(\mathbb Z[S_{17}]\) form, the \((\kappa,d)\)-refined form
> (\(55\cdot17=935\) coordinates), and under every representation — **cannot be
> contradictory**.

*Certified computational.*  Random chart families that **violate** the design
condition (respectively \(201,\,326,\,1086,\,3926\) asymmetric holonomies) at
\((v,t)=(9,2),(8,3),(10,3),(11,4)\) satisfy the identity coefficientwise in
\(\mathbb Z[S_m]\); it also holds, as it must, on the exhaustively built
\(LS(2,3,9)\) and the committed cyclic \(LS(2,3,19)\).

**Relation to `evidence/holonomy_group_algebra_tower.md`** (that file was still
being edited; the content described here is its state at modification time
02:54:42 EDT, 27 July 2026).  It contains two delimiters of its own that
Theorem A neither duplicates nor contradicts:

* its \(\rho_{\rm nat}(H_R)=(m+1)J_m\) — the natural \(m\)-point permutation
  module is *flat*, taking the same value on every one-factorization, so it
  cannot distinguish objects.  That is a statement about one representation
  applied to one link's holonomy sum;
* its pseudogluing construction — transporting one fixed \(LS(2,3,19)\) through
  a one-factorization of \(K_{20}\) produces twenty genuine links that satisfy
  **all \(190\)** overlap-resolved fingerprint equalities, so those equalities
  are insufficient.

Theorem A is a different and, for the identity itself, stronger statement: the
identity holds with **no design hypothesis at all**, so *every* projection of
it — the natural module, any other representation, central or noncentral — is
empty as an obstruction, without needing a separate flatness computation for
each.  It also explains why the file's invitation to look above the natural
module ("Any integral linear representation or permutation module of \(S_m\)
gives a smaller necessary matrix identity by applying it to (2)") cannot
succeed: the object being projected carries no design information to begin
with.

## 3. Theorem B: the overlap system is exactly the problem

> **Theorem B (*proved*).**  Let \(t\ge2\), \(|X|=v\).  Giving, for every
> \(p\in X\), an \(LS(t-1,t,v-1)\) colouring \(L^p\) on \(X\setminus\{p\}\)
> such that
> \[
>   L^p\bigl(\{q\}\cup S\bigr)=L^q\bigl(\{p\}\cup S\bigr)
>   \qquad\bigl(p\ne q,\ S\in\tbinom{X\setminus\{p,q\}}{t-1}\bigr)
> \]
> is **equivalent** to giving an \(LS(t,t+1,v)\) on \(X\), by
> \(c(\{p\}\cup B)=L^p(B)\) and \(L^p=c^p\).

*Proof.*  Each \(L^p\) is symmetric in the \(t\) points of its block, and the
displayed condition adds the transposition exchanging \(p\) with one of them.
The symmetric group of a \(t\)-set together with one such cross transposition
generates the symmetric group of the \((t+1)\)-set, so
\(c(\{p\}\cup B):=L^p(B)\) is a well-defined function on \(\binom X{t+1}\).
For \(T\in\binom Xt\) pick \(p\in T\); then \(s\mapsto c(T\cup\{s\})\) is
\(s\mapsto L^p((T\setminus\{p\})\cup\{s\})\), a bijection because \(L^p\) is a
large set.  So \(c\) is an \(LS(t,t+1,v)\), and \(c^p=L^p\) by construction.
The converse is immediate. \(\square\)

> **Corollary B.1.**  The "simultaneous twenty-link" system at
> \(LS(3,4,20)\) is not a relaxation: satisfying it is exactly as hard as
> \(LS(3,4,20)\).  The overlap-resolved holonomy equalities
> \(H_{\{q\}}(c^p)=H_{\{p\}}(c^q)=H_{\{p,q\}}(c)\) are a *weakening* of the
> matching condition (they compare holonomy sums, not the pair-links
> themselves), and by Theorem A they are automatic re-indexings on any chart
> family.  So they screen nothing that is presented as a genuine object.

**Relation to prior work.**  `evidence/holonomy_group_algebra_tower.md` (state
of 02:54:42 EDT, 27 July 2026) already observes that the *fully indexed*
holonomy array of one link recovers that link's one-factorization, because the
unique fixed colour of \(\sigma_R(a,b)\) is \(c(R\cup\{a,b\})\), and concludes
that equality of indexed arrays for two derived links is equivalent to the
cellwise overlap condition.  Theorem B is the corresponding statement one level
up and in the other direction: it identifies the *whole twenty-link matching
system* with \(LS(3,4,20)\) itself, so the target that note poses — "a genuine
intermediate compression, stronger than the aggregate \(H_R\) but not merely a
renaming of all original colours" — is a search for something strictly between
two things that are now both pinned down: the aggregate end is vacuous
(Theorem A) and the indexed end is the problem (Theorem B).

*Certified computational.*  Replayed on the exhaustively built
\(LS(2,3,9)\): the nine point-links satisfy the matching condition,
reconstruction returns the same object, perturbing one link breaks the
matching, and the group-generation step is checked directly (\(|S_4|=24\)).

## 4. Theorem C: the sign layer of the census is the \(\varepsilon\) layer

For \(a\in X\setminus R\) extend \(g_{R\cup a}\) to
\(\widehat g_a:X\setminus R\to[m]\cup\{\infty\}\) by \(\widehat g_a(a)=\infty\)
(with \(\infty\) last), and put \(\eta_R(a)=\operatorname{sgn}(\widehat g_a)\)
relative to the fixed orders.  Recall
\(\varepsilon(R)=E_1(g^R)=\prod_{a}\operatorname{sgn}(g_{R\cup a})\) and
\(E_t(g)=\prod_{T}\operatorname{sgn}(g_T)\).

> **Theorem C (*proved*).**  For every chart family, write
> \(\tau_R(a,b)=\widehat g_b\widehat g_a^{-1}\).  Then
> **(a)** \(\tau_R(b,e)\tau_R(a,b)=\tau_R(a,e)\) and
> \(\tau_R(a,b)=(\infty\ g_{R\cup b}(a))\,\sigma_R(a,b)\);
> **(b)** \(\operatorname{sgn}\sigma_R(a,b)=-\eta_R(a)\eta_R(b)\), hence the
> triangle law
> \[
>   \operatorname{sgn}\sigma_R(a,b)\cdot\operatorname{sgn}\sigma_R(b,e)
>   \cdot\operatorname{sgn}\sigma_R(a,e)=-1 ,
> \]
> so the signed complete graph on \(X\setminus R\) with edge signs
> \(-\operatorname{sgn}\sigma_R(a,b)\) is **balanced**, i.e. a coboundary.
> If \(m\) is odd (equivalently \(n=m+1=|X\setminus R|\) is even), then also
> **(c)** \(\displaystyle\prod_{\{a,b\}}\operatorname{sgn}\sigma_R(a,b)=\varepsilon(R)\);
> **(d)** \(\displaystyle\prod_{R\in\binom X{t-1}}\prod_{\{a,b\}}\operatorname{sgn}\sigma_R(a,b)=E_t(g)^{\,t}\).

*Proof.*  (a) Cancel \(\widehat g_b^{-1}\widehat g_b\).  For the second part,
both sides agree off \(\{g_{R\cup a}(b),g_{R\cup b}(a),\infty\}\); the left side
sends \(\infty\mapsto g_{R\cup b}(a)\) and \(g_{R\cup a}(b)\mapsto\infty\),
and \(\sigma\) fixes \(\infty\) and sends
\(g_{R\cup a}(b)\mapsto g_{R\cup b}(a)\).
(b) Signs of bijections between ordered sets compose, so
\(\operatorname{sgn}\tau_R(a,b)=\eta_R(a)\eta_R(b)\); by (a),
\(\operatorname{sgn}\tau=-\operatorname{sgn}\sigma\).  Balance of a signed
complete graph is equivalent to all triangles positive, and here every triangle
of \(-\operatorname{sgn}\sigma\) is \(+1\).
(c) With \(n=m+1=|X\setminus R|\) even,
\(\prod_{\{a,b\}}(-\eta_R(a)\eta_R(b))
=(-1)^{\binom n2}\prod_a\eta_R(a)^{\,n-1}
=(-1)^{\binom n2}\prod_a\eta_R(a)\).
Moving \(a\) to the last position and \(\infty\) to the last position costs
\((-1)^{\,n-\mathrm{pos}(a)}\), so
\(\prod_a\eta_R(a)=\varepsilon(R)\,(-1)^{\,n^2-\binom{n+1}2}
=\varepsilon(R)(-1)^{\binom n2}\); the two signs cancel.
(d) \(\varepsilon(R)=\prod_{T\supseteq R,|T|=t}\operatorname{sgn}(g_T)\), and each
\(t\)-set contains \(\binom t{t-1}=t\) sets \(R\), so
\(\prod_R\varepsilon(R)=E_t(g)^t\); combine with (c). \(\square\)

> **Corollary C.1 (*proved*, for odd \(m\)).**  Since \(m\) is odd,
> \(\operatorname{sgn}\sigma=(-1)^{\ell}\) where \(\ell\) is the number of
> nontrivial cycles.  So the cycle-type census of a link **determines**
> \(\varepsilon(R)\):
> \(\varepsilon(R)=(-1)^{\sum_\kappa \ell(\kappa)N_\kappa(g^R)}\).
> The pair-sign parity law on the \(190\) links of an \(LS(3,4,20)\) is
> therefore a consequence of the censuses — the census layer contains the
> abelian layer exactly, and contributes nothing further in signs.  At \(t=3\)
> the total product is \(E_3(c)\), so \(E_3(c)=(-1)^{|E(G_-)|}\) for the
> even-degree graph \(G_-\) of the pair-sign law.

**Attribution of (a).**  For design families this is Theorem 2 (equations (5)
and (6)) of `evidence/holonomy_group_algebra_tower.md`; it is restated here
because parts (b)–(d) use it, and because the form above holds for **every**
chart family, where the two missing colours differ.  No priority is claimed for
(a).

*Certified computational.*  (b), (c), (d) verified on the exhaustive
\(LS(2,3,9)\), the committed cyclic \(LS(2,3,19)\), and random non-design chart
families at \((v,t)=(10,3)\) and \((11,4)\) — the last two showing that
Theorem C, too, is gauge-vacuous.

## 5. Theorem D: the intercalate congruence, the one design-dependent law

For a one-factorization \(F\) of \(K_n\) (\(n\) even, colours \([n-1]\)) let
\(m_2(\sigma)\) be the number of \(2\)-cycles of a holonomy and
\(C_4(F)=\sum_{e<f}\#\{4\text{-cycles of }F_e\cup F_f\}\).

> **Theorem D (*proved*).**
> \[
>   \boxed{\ \sum_{\{a,b\}\subseteq V}m_2(\sigma_{ab})=2\,C_4(F).\ }
> \]

*Proof.*  \(\sigma_{ab}\) has the \(2\)-cycle \(\{e,f\}\) iff there are
\(z,w\notin\{a,b\}\) with \(F(az)=F(bw)=e\) and \(F(aw)=F(bz)=f\); necessarily
\(z\ne w\), and this says exactly that \(a\,z\,b\,w\) is an alternating
\(4\)-cycle of \(F_e\cup F_f\).  Conversely such a \(4\)-cycle has two
diagonals, \(\{a,b\}\) and \(\{z,w\}\), and the computation above run at
\(\{z,w\}\) produces the same \(2\)-cycle \(\{e,f\}\) there.  So swapping the
two diagonals is a fixed-point-free involution on the set of
(vertex pair, \(2\)-cycle) incidences whose orbits are exactly the alternating
\(4\)-cycles. \(\square\)

> **Corollary D.1 (*proved*).**  For every one-factorization,
> \(\sum_\kappa N_\kappa\,m_2(\kappa)\equiv0\pmod2\), i.e.
> \(\sum_{\kappa:\,m_2(\kappa)\text{ odd}}N_\kappa\equiv0\pmod2\).  For every
> \(LS(t,t+1,v)\) and every \(R\in\binom X{t-1}\) the census of \(c^R\)
> satisfies it: \(190\) congruences at \(LS(3,4,20)\), one per pair-link.

> **Independence from Theorem A (*proved*).**  Corollary D.1 is a statement
> about a single one-factorization, i.e. the case \(t=1\), where the tower
> identity of Theorem A is empty (\(t-1=0\)) and relates nothing.  It is a
> constraint on one census vector, which no projection of an identity between
> levels can be.

In symmetric-Latin-square language: \(2\)-cycles of row quotients are
intercalates, the symmetric square of a one-factorization has
\(\binom n2\) intercalates lying on the diagonal (rows \(\{a,b\}\), columns
\(\{a,b\}\)), and Theorem D says the off-diagonal ones are permuted freely by
transposition, hence even in number.

*Certified computational.*  The identity and the congruence hold on: all
\(1\), \(6\) and \(6240\) one-factorizations of \(K_4,K_6,K_8\) (exhaustive);
all \(396\) isomorphism classes of \(K_{10}\) (exhaustive, committed
catalogue); \(150\) one-factorizations of \(K_{12}\) and \(150\) of
\(K_{18}\) (randomised-backtracking samples); and the \(19\) point-links of the
committed cyclic \(LS(2,3,19)\) (exhaustive for that object).

## 6. Theorem E: the exact mod-2 strength of the census

Call \(a\in\mathbb F_2^{T(n)}\) a **universal congruence** if \(a\cdot N\) is
the same element of \(\mathbb F_2\) for every one-factorization of \(K_n\).
Two are known: the total count \(\sum_\kappa N_\kappa=\binom n2\), and
Theorem D.

> **Theorem E (*certified computational*).**
>
> | \(n\) | types | object set | \(\dim\) of the congruence space | conclusion |
> |---|---|---|---|---|
> | \(8\) | \(4\) | all \(6240\) (exhaustive) | \(3\) | one **extra** congruence |
> | \(10\) | \(7\) | all \(396\) classes (exhaustive) | \(2\) | exactly \(\mathrm{span}\{\text{total},D\}\) |
> | \(12\) | \(12\) | \(150\) sampled | \(2\) | exactly \(\mathrm{span}\{\text{total},D\}\) |
> | \(18\) | \(55\) | \(150\) sampled \(+\) \(3\) committed witnesses | \(2\) | exactly \(\mathrm{span}\{\text{total},D\}\) |
>
> A larger object set can only *shrink* the observed space, and both listed
> functionals are proved universal, so a computed dimension of \(2\) pins the
> true value at \(2\).  Hence at \(n=18\) — the size of every pair-link of an
> \(LS(3,4,20)\) — **the entire universal mod-2 arithmetic of the holonomy
> census is the total count together with Theorem D.**

The \(n=8\) extra congruence is \(N_{(4,2)}\equiv0\), equivalently
\(N_{(2,2,2)}\equiv0\) (the two differ by Theorem D).  It is an accident: the
space is already exactly two-dimensional at \(n=10\).

The \(n=18\) row needs the three witnesses because a sample of \(150\) misses
three rare cycle types — \((4,2^6)\), \((3,3,2^5)\) and \((2^8)\) — and a type
that never occurs contributes a spurious congruence \(N_\kappa\equiv0\).  The
verifier commits one one-factorization of \(K_{18}\) for each, each realising
its type with multiplicity exactly \(1\), which is odd and therefore refutes
the spurious functional.  The \((2^8)\) witness was built by prescribing eight
alternating \(4\)-cycles through a single vertex pair and completing; the other
two were found by search.

> **Refutation E.1 (*certified computational*).**  Theorem D admits **no**
> per-type refinement: the diagonal-swap involution of its proof does not
> preserve the whole cycle type of the holonomy (counterexample found among the
> \(396\) classes of \(K_{10}\)).  So "\(N_\kappa\) even for each \(\kappa\)
> with \(m_2(\kappa)\) odd" is false in general, and the \(n=8\) coincidence
> must not be generalised.

> **Refutation E.2 (*certified computational*).**  Over \(\mathbb Q\) there is
> nothing at all beyond the total count: the \(396\) censuses at \(n=10\)
> affinely span the whole hyperplane \(\sum_\kappa N_\kappa=45\) (rank \(6\) of
> \(6\)).  Theorem D is a purely mod-2 phenomenon.

> **Measurement E.3 (*certified computational*).**  The census separates all
> \(6\) isomorphism classes of one-factorizations of \(K_8\), and \(374\) of the
> \(396\) classes of \(K_{10}\).  It is strictly finer than the sign, and not
> complete.  On the committed cyclic \(LS(2,3,19)\) it realises \(34\) of the
> \(55\) possible types, its \(5814\) oriented exact holonomies are pairwise
> distinct, and its refined \((\kappa,d)\) row sums are \(171\) for each of the
> \(17\) colours.

> **Methodological refutation E.4 (*certified computational*).**  A cycle-switch
> random walk seeded at the round-robin one-factorization is **inert** at
> \(n=12\) and \(n=18\), because those round-robin factorizations are perfect
> (every union of two factors is a single Hamiltonian cycle), so no switch is
> ever available.  It silently returned a constant "sample".  Recorded because
> the failure is invisible in the output; the samples above use randomised
> backtracking instead, and every sampled object is re-verified to be a
> one-factorization.

## 7. What the four candidate mechanisms turn out to be

The question asked about four mechanisms.  Each is now settled:

| mechanism | status |
|---|---|
| universal congruences | exactly two exist at \(n=18\): the total count and Theorem D (Theorem E). Both are identities on genuine objects, so neither can be violated. |
| representation-theoretic identities | every representation projection of the tower identity is vacuous (Corollary A.1(b)); no design hypothesis enters. |
| orientation constraints | \(H\) is antipode-invariant for every chart family, so there is no orientation functional (Corollary A.1(d)). |
| overlap compatibility | the strongest form is *equivalent* to \(LS(3,4,20)\) (Theorem B); the holonomy-sum form is a strict weakening and is an automatic re-indexing. |

## 8. Where the live content is instead, and the fan

Theorem B says the twenty-link overlap system is the problem, so it is not a
target.  The simultaneous \(13\)-fan shadow is different in kind: its binding
constraints are the \(3{,}876\) cross-copy **all-different** conditions, which
are not relations among chart quotients and are therefore untouched by Theorem
A.  Its exact finite target — find a labelled \(LS(2,3,19)\) whose
\(50{,}388\)-vertex conflict graph \(H_L\) is \(13\)-colourable, or prove none
is — is unaffected by anything in this note, and remains the honest live
target on that side.  Nothing here bears on it either way.

## 9. Literature

An independent primary-source search was run.  Findings, with their confidence
stated:

* The cycle structure of a row quotient of a Latin square is standard and is
  called the **row cycle**; that it is fixed-point-free is explicit in
  J. Allsop and I. M. Wanless, *Cycles of quadratic Latin squares and
  anti-perfect 1-factorisations*, arXiv:2302.12942, and in the same authors'
  *Row-Hamiltonian Latin squares and Falconer varieties*, arXiv:2211.13826.
  Those papers work with bipartite \(K_{n,n}\); the single fixed point in our
  setting is the constant-diagonal bookkeeping.  **Confirmed textually.**
* The identification "\(2\)-cycle of a row quotient = intercalate = \(2\times2\)
  Latin subrectangle" is explicit in arXiv:2302.12942.  **Confirmed
  textually.**  The summed identity of Theorem D was **not located** in any
  source searched.
* A cycle-type census of row quotients is a **named published invariant** of
  one-factorizations: "row-cycles" appears in the survey S. Matos, R. Melo,
  T. Januario, S. Urrutia and D. de Werra, *On invariants for 1-factorizations
  of \(K_{2n}\): Description and computation*, Communications in Combinatorics
  and Optimization (2025), alongside cycle profiles, tricolor vectors,
  divisions, trains and trains-path.  The text could **not** be extracted, so
  the identification with \(N_\kappa\) is **inferred, not verified**.  On the
  assumption that it is the same object, no priority is claimed for the census.
  Earlier named invariants: J. H. Dinitz and W. D. Wallis, *Trains: an
  invariant for one-factorizations*, Ars Combin. **32** (1991) 161–180;
  T. S. Griggs and A. Rosa, *An invariant for one-factorizations of the
  complete graph*, Ars Combin. **42** (1996) 77–88.  Neither text could be
  extracted.
* The sign of a one-factorization is known: U. Schauz, arXiv:1705.00484
  (confirmed textually; it contains no triangle/balance/coboundary
  construction), after M. N. Ellingham and L. Goddyn, Combinatorica **16**
  (1996) 343–352 and N. Alon and M. Tarsi, Combinatorica **12** (1992) 125–134
  (texts not extracted).  The triangle law and vertex balance of Theorem C
  were **not located**; the algebra is short once the definitions are in place,
  so folklore status is plausible and no priority is claimed.  The repository
  already records the coboundary phenomenon in other coordinates
  (`collaboration/cross_root_layer_sign/`), and already records that the
  per-vertex star-sign field yields no affine-linear obstruction
  (`evidence/star_sign_gluing_audit.md`).
* No published work on holonomy, transition permutations, or gauge invariants
  for **large sets** \(LS(t,t+1,v)\) with \(t\ge2\) was found.
* "Not located" is not a priority claim.  Several decisive sources are
  paywalled and resisted text extraction; this is a screen, not a
  MathSciNet-grade search.

## 10. Inventory

**Proved here.**  Theorem A and Corollary A.1 (for \(t\ge2\), the tower identity, its exact
group-algebra lift, every representation projection, the fixed-colour
refinement and the orientation symmetry hold for arbitrary chart families,
hence cannot obstruct); Theorem B and Corollary B.1 (the twenty-link overlap
system is equivalent to \(LS(3,4,20)\); the holonomy-sum overlap equalities are
automatic); Theorem C and Corollary C.1 (the augmented cocycle, the triangle
sign law and balance for every chart family, and for odd \(m\),
\(\prod\operatorname{sgn}\sigma=\varepsilon(R)\),
\(\prod\prod\operatorname{sgn}\sigma=E_t^t\), and the census functional that
recovers \(\varepsilon\)); Theorem D and Corollary D.1 (the intercalate
identity and its mod-2 congruence, with its independence from Theorem A).

**Certified computational.**  Theorem E (the congruence space is exactly
two-dimensional at \(n=10,12,18\), three-dimensional at \(n=8\)), Refutations
E.1, E.2, E.4, Measurement E.3, and every replay listed above.

**Not claimed.**  Existence or nonexistence of \(LS(3,4,16)\),
\(LS(3,4,20)\), \(LS(4,5,21)\), \(LS(14,15,31)\) or \(LS(15,16,32)\); any
exclusion of \(k=16\); any progress on the existential quantifier in
Erdős–Rosenfeld #835, **which remains open**.  What is claimed is that one
named route is now closed, with a proof of why.

## 11. Verification

```sh
python3 -B collaboration/opus5/holonomy_followup/verify_holonomy_followup.py
```

Standard library only, exact finite arithmetic, no solver, no network, refuses
`python -O`.  Randomness is used only to build controls (non-design chart
families, sampled one-factorizations); every object it samples is re-verified,
and every theorem is additionally checked on exhaustively enumerated or
committed objects.  External inputs: the committed cyclic \(LS(2,3,19)\)
(`evidence/verify_defect_cross_link_lsts19.py`) and the committed catalogue of
the \(396\) one-factorizations of \(K_{10}\)
(`evidence/k10_one_factorizations_396.txt`).

Current status: **94 checks, all passing**; `ruff check` and
`ruff format --check` clean; runtime about four seconds.
