# The post-\(r=0\) global bridge: the exact six-instance coupling, and a snark obstruction to prefix extension

Date: 2026-07-28.  Author: Claude Opus 5.

## 0. What this note contains, and what it does not

Erdős–Rosenfeld Problem #835 is **open**.  Nothing below closes it, and
nothing below constructs a \(17\)-colouring of \(J(32,16)\) or refutes one.

Everything asserted as a theorem here is proved by hand.  **No script was
executed in this session** — interpreter execution was unavailable — so no
claim rests on a computation.  The three scripts in this directory are audit
surface for an independent checker, and are labelled *unrun* throughout.

New results:

1. **Theorem A (R-local Johnson reformulation).**  For a fixed
   \(R\in\binom U6\) the whole level-\(\le2\) tower datum is *exactly* a
   proper \(17\)-colouring of the Johnson graph \(J(19,3)\) on
   \(W=R\mathbin{\dot\cup}A\), restricted to the triples that meet \(R\).
   The general level-\(j\) statement replaces \(J(19,3)\) by
   \(J(j+17,\,j+1)\) on \(W=R\mathbin{\dot\cup}A\), \(R\in\binom U{j+4}\).

2. **Theorem B (the shared data, explicitly).**  The six class-B instances
   \(I(P_x)\), \(x\in R\), are determined by thirteen **proper
   \(17\)-edge-colourings \(e_a\) of \(K_6=K_R\)**, one per \(a\in A\),
   together with \(L|_{\binom R3}\); and
   \(S_a(P_x)\) is exactly *the set of colours appearing at the vertex
   \(x\) in \(e_a\)*, so
   \(V_\gamma(P_x)=\{a\in A:\gamma\hbox{ is missing at }x\hbox{ in }e_a\}\).
   This is the precise sense in which the six instances are not independent.

3. **Theorem C (the coupling, with all quantifiers).**  The reconstruction
   and proof of the "six simultaneous same-colour matchings" statement,
   together with its exact support and size ledger, and the corollary that
   the coupling at a *single* \(R\) is never obstructed in isolation
   (restrict any \(LS(2,3,19)\)); the content is consistency across
   different \(R\).

4. **Theorem D (snark obstruction; the item-2 counterexample).**  An
   explicit target-order **class-B\('\)** instance of profile \(r=3\) —
   a profile for which coordinated nine *is* already proved in this
   repository — together with an explicit legitimate **fourteen**-matching
   prefix whose residual graph is exactly the **Petersen graph**.  The
   prefix extends to exactly fifteen and never to sixteen.  The obstruction
   is \(3\)-edge-colourability: it is invisible to the fractional
   relaxation (the uniform point \(x\equiv\frac13\) is feasible, by
   Edmonds' perfect-matching polytope theorem) and to the whole
   matching-deletion capacity family, which by the new **Lemma D4** is
   satisfied with slack by every \(3\)-edge-connected cubic residual.

5. **Theorem E (tail dichotomy).**  In every class-B instance the last
   matching is automatic; the last two are obstructed only by conditions
   that are odd-cut visible; and the last three already contain
   \(3\)-edge-colourability of cubic graphs.  So \(k=3\) is exactly where
   counting invariants stop working.

6. **Corollary F (dichotomy).**  Either the certificate instance of
   Theorem D completes — and then "every coordinated prefix extends" is
   false at depth fourteen inside class B\('\), with an obstruction that
   neither the matching-deletion capacity family (which contains both cut
   inequalities and vertex Hall) nor the fractional relaxation can see — or
   it does not complete, and
   then the class-B\('\) completion Question at \(n=13\) is refuted.  Which
   of the two holds is a finite exact computation, isolated in
   `decide_certificate_completion.py`.

Not proved: assignment item 1 (coordinated nine \(\Rightarrow\) seventeen)
— Theorem D shows the *arbitrary-prefix* form of it is false at depth
fourteen and that no capacity- or LP-type invariant can repair it; and assignment
item 4 (that the global coupling always completes, or a no-go) — Theorem C
reduces it to an exact partial-\(LS(2,3,19)\) completion problem but does
not settle it.

---

## 1. Objects, fixed once

Throughout \({\cal C}\) is a labelled \(17\)-set of colours.

### 1.1 Global object

\(V\) is a \(32\)-set and \(c:\binom V{16}\to{\cal C}\) a proper colouring
of \(J(32,16)\) (two \(16\)-sets adjacent iff they meet in \(15\) points).
Fix a split
\[
 V=U\mathbin{\dot\cup}A,\qquad |U|=19,\quad |A|=13 ,
\]
and put, for \(B\subseteq A\) and \(Q\in\binom U{|B|+3}\),
\[
 G_B(Q)=c\bigl((U\setminus Q)\cup B\bigr).
\tag{1.1}
\]
This is the tower of `../../unrestricted_lift_tower/NOTE.md`, whose
Theorem 1 says that proper \(17\)-colourings of \(J(32,16)\) correspond
bijectively to families \((G_B)_{B\subseteq A}\) obeying, for every
\(B\in\binom Aj\) and every \(P\in\binom U{j+4}\), the **tower law**: the
\(17\) values
\[
 \bigl(G_B(P\setminus\{u\})\bigr)_{u\in P}
 \ \sqcup\
 \bigl(G_{B\cup\{a\}}(P)\bigr)_{a\in A\setminus B}
\tag{1.2}
\]
are pairwise distinct.  Write \(L=G_\varnothing\) on \(\binom U3\) and
\(F_a=G_{\{a\}}\) on \(\binom U4\).

### 1.2 Local objects

For \(P\in\binom U5\) and \(a\in A\) put
\[
 S_a(P)=\bigl\{F_a(P\setminus\{u\}):u\in P\bigr\},
 \qquad
 V_\gamma(P)=\{a\in A:\gamma\notin S_a(P)\}.
\tag{1.3}
\]
Level-\(1\) top-properness (the \(j=1\) case of (1.2) at \(B=\{a\}\)) gives
\(|S_a(P)|=5\).

* The **first-lift instance at \(P\)** is
  \(I(P)=\bigl(A,{\cal C},(S_a(P))_{a\in A}\bigr)\).
* A **solution of \(I(P)\)** is a map \(h_P:E(K_A)\to{\cal C}\) that is a
  proper edge-colouring of \(K_A\) in which the colours missing at \(a\)
  are exactly \(S_a(P)\).  Equivalently (Theorem 3 of the tower note) it is
  a family of perfect matchings \(M_\gamma(P)\subseteq K_A[V_\gamma(P)]\),
  \(\gamma\in{\cal C}\), partitioning \(E(K_A)\).  We identify
  \(h_P(ab)=G_{\{a,b\}}(P)\).
* \(I(P)\) is **class B** when every \(|S_a(P)|=5\) and every colour lies
  in an odd number \(m_\gamma\le5\) of the \(S_a(P)\); equivalently every
  \(|V_\gamma(P)|\in\{8,10,12\}\).  It is **class B\('\)** when in addition
  the support family is the one left on \(A\) by some proper
  \(17\)-edge-colouring of \(K_{18}-E(K_{13})\) saturating the five
  vertices outside \(A\).  It is **class C** (fan-realisable) when it
  actually arises from a simultaneous \(13\)-fan by (1.3).
  \(C\subseteq B'\subsetneq B\).
* The **profile index** is \(r(P)=\#\{\gamma:|V_\gamma(P)|=12\}\), and
  \((n_8,n_{10},n_{12})=(7+r,\,10-2r,\,r)\).
* **Coordinated nine** at \(P\) is the assertion that nine pairwise
  edge-disjoint support-perfect matchings exist.

### 1.3 The coupling

For \(R\in\binom U6\) and \(x\in R\) write \(P_x=R\setminus\{x\}\).
**Level-\(2\) top-properness at \(R\)** is the \(j=2\) instance of the
distinctness requirement in (1.2) restricted to the six triples meeting
\(R\):
\[
 \forall\{a,b\}\in\tbinom A2:\quad
 \bigl|\{\,h_{P_x}(ab):x\in R\,\}\bigr|=6 .
\tag{1.4}
\]

---

## 2. Theorem A: the R-local Johnson reformulation

Fix \(R\in\binom U6\) and put
\[
 W=R\mathbin{\dot\cup}A,\qquad |W|=6+13=19 .
\]
Let
\[
 {\cal T}=\Bigl\{Z\in\tbinom W3:Z\cap R\neq\varnothing\Bigr\},
 \qquad
 |{\cal T}|=\tbinom{19}3-\tbinom{13}3=969-286=683 .
\]

> **Definition (the local coordinate map).**  For \(Z\in{\cal T}\) put
> \[
>  B(Z)=Z\cap A,\qquad Q(Z)=R\setminus(Z\cap R) .
> \]
> Then \(|Q(Z)|=6-(3-|B(Z)|)=|B(Z)|+3\), so \(G_{B(Z)}(Q(Z))\) is defined
> whenever \(|B(Z)|\le2\), which holds for every \(Z\in{\cal T}\).  Set
> \[
>  c^{*}(Z)=G_{B(Z)}\bigl(Q(Z)\bigr).
> \tag{2.1}
> \]

Concretely:
\[
 c^{*}(T)=L(R\setminus T)\ \ (T\subseteq R),\qquad
 c^{*}(\{u,v,a\})=F_a\bigl(R\setminus\{u,v\}\bigr),\qquad
 c^{*}(\{u,a,b\})=G_{\{a,b\}}\bigl(R\setminus\{u\}\bigr),
\tag{2.2}
\]
for \(u,v\in R\) and \(a,b\in A\).

> **Theorem A.**  Let \(J(19,3)\) be the Johnson graph on \(\binom W3\)
> (two triples adjacent iff they meet in two points).  Then the family
> \[
>  \Bigl(L|_{\binom R3},\ \ (F_a|_{\binom R4})_{a\in A},\ \
>   \bigl(G_{\{a,b\}}(R\setminus\{x\})\bigr)_{\{a,b\}\in\binom A2,\;x\in R}\Bigr)
> \]
> satisfies **all** tower laws (1.2) with \(j\in\{0,1\}\) whose five-set or
> four-set argument lies inside \(R\), and level-\(2\) top-properness (1.4)
> at \(R\), **if and only if** \(c^{*}\) is a proper \(17\)-colouring of the
> subgraph of \(J(19,3)\) induced on \({\cal T}\).
>
> More generally, for \(j\ge0\) and \(R\in\binom U{j+4}\), with
> \(W=R\mathbin{\dot\cup}A\), \(|W|=j+17\), the same coordinate map
> \(D\mapsto\bigl(D\cap A,\ R\setminus(D\cap R)\bigr)\) on the
> \((j+1)\)-subsets of \(W\) meeting \(R\) turns the level-\(\le j+1\) tower
> datum at \(R\) into a proper \(17\)-colouring of \(J(j+17,\,j+1)\)
> restricted to those \((j+1)\)-sets.

### Proof

The map \(Z\mapsto(B(Z),Q(Z))\) is a bijection from
\(\{Z\in\binom W3:Z\cap R\ne\varnothing\}\) onto the pairs \((B,Q)\) with
\(B\subseteq A\), \(|B|\le2\), \(Q\subseteq R\), \(|Q|=|B|+3\): the inverse
is \((B,Q)\mapsto B\cup(R\setminus Q)\), and \(|B\cup(R\setminus Q)|=
|B|+6-(|B|+3)=3\).  So \(c^{*}\) is well defined on \({\cal T}\) and records
exactly the displayed datum.

Two triples \(Z\ne Z'\) of \(\binom W3\) are adjacent in \(J(19,3)\) iff
\(Y=Z\cap Z'\) has two points.  Fix such a \(Y\) and let
\(j=|Y\cap A|\in\{0,1,2\}\).  The triples through \(Y\) are \(Y\cup\{w\}\),
\(w\in W\setminus Y\), and there are \(19-2=17\) of them.  Split
\(w\in R\setminus Y\) (there are \(6-|Y\cap R|\) such) and \(w\in A\setminus Y\)
(there are \(13-j\)); the two counts sum to \(17\).

*Case \(j\le1\).*  Put \(B=Y\cap A\) and \(P=R\setminus(Y\cap R)\), so
\(|P|=6-(2-j)=j+4\).  For \(w=u\in P\) one has
\(B(Y\cup\{u\})=B\) and \(Q(Y\cup\{u\})=R\setminus\bigl((Y\cap R)\cup\{u\}\bigr)
=P\setminus\{u\}\); for \(w=a\in A\setminus B\) one has
\(B(Y\cup\{a\})=B\cup\{a\}\) and \(Q(Y\cup\{a\})=R\setminus(Y\cap R)=P\).
Hence the multiset of \(c^{*}\)-values on the star of \(Y\) is precisely the
list (1.2) at \((B,P)\).  Since \(|Y\cap R|=2-j\ge1\), *every* triple in
that star lies in \({\cal T}\).  So "the star of \(Y\) is rainbow'' is
literally the tower law at \((B,P)\), and conversely.  Ranging over all
\(Y\) with \(j\le1\) ranges over all \((B,P)\) with \(|B|\le1\) and
\(P\subseteq R\).

*Case \(j=2\).*  Then \(Y=\{a,b\}\subseteq A\) and the triples
\(Y\cup\{w\}\) lying in \({\cal T}\) are exactly those with \(w\in R\), six
of them, with
\(c^{*}(\{a,b,x\})=G_{\{a,b\}}(R\setminus\{x\})=h_{P_x}(ab)\).  So "the six
\({\cal T}\)-triples through \(Y\) are rainbow'' is literally (1.4).

Properness of \(c^{*}\) on \({\cal T}\) is the conjunction of the two cases,
which proves the equivalence.

For general \(j\), replace \(3\) by \(j+1\) and \(6\) by \(j+4\)
throughout: \(D\mapsto(D\cap A,\,R\setminus(D\cap R))\) is a bijection from
the \((j+1)\)-subsets of \(W\) meeting \(R\) onto the pairs \((B,Q)\) with
\(B\subseteq A\), \(|B|\le j\), \(Q\subseteq R\), \(|Q|=|B|+3\); the star of
a \(j\)-set \(Y\subseteq W\) has \(|W|-j=17\) members; and the same two-case
argument identifies the star conditions with the tower laws and with
top-properness.  (The device \(W=R\mathbin{\dot\cup}A\), \(|W|=j+17\), is the
one used in the proof of Theorem 5 of `../../unrestricted_lift_tower/NOTE.md`;
what is new here is the identification of the *whole* system of tower laws
and top-properness conditions with Johnson-graph properness.)  \(\square\)

> **Corollary A1.**  A proper \(17\)-colouring of the *whole* of
> \(J(j+17,j+1)\) is exactly an \(LS(j,j+1,j+17)\).  Hence the level-\(\le
> j+1\) datum at any \(R\in\binom U{j+4}\) is a **partial**
> \(LS(j,j+1,j+17)\) on \(W=R\mathbin{\dot\cup}A\): the part supported on the
> \((j+1)\)-sets meeting \(R\).  For \(j=2\) the ambient object is
> \(LS(2,3,19)\), which exists; for \(j=3\) it is \(LS(3,4,20)\), which is
> open.

*Proof.*  Independent sets of \(J(n,s)\) are partial \(S(s-1,s,n)\)'s, of
size at most \(\binom n{s-1}/s\); with \(n=j+17\), \(s=j+1\) the identity
\(\binom{j+17}{j+1}(j+1)=17\binom{j+17}{j}\) forces every class of a proper
\(17\)-colouring to attain the bound, i.e. to be a Steiner system, and
conversely.  This is Theorem 6 of
`../coordinated_nine_and_global_bridge/NOTE.md`; Corollary A1 only adds
that the \(R\)-local object is the *restriction* of such a colouring to a
prescribed sub-family of blocks.  \(\square\)

> **Corollary A2 (the level-\(2\) coupling is never obstructed in
> isolation).**  For every \(R\) there exist level-\(\le2\) data at \(R\)
> satisfying every condition of Theorem A: take any \(LS(2,3,19)\) on a
> \(19\)-set \(W\), split \(W=R\mathbin{\dot\cup}A\) arbitrarily, and
> restrict its colouring to \({\cal T}\).  Consequently no counting or
> existence obstruction lives at a single \(R\); the entire content of the
> coupling is whether the level-\(\le1\) datum *actually produced by a
> simultaneous \(13\)-fan* extends, and whether the extensions at different
> \(R\) agree.  \(\square\)

---

## 3. Theorem B: the shared data of the six instances

Fix \(R\in\binom U6\).  Identify \(\binom R4\) with \(E(K_R)\) by
complementation, \(Q\leftrightarrow R\setminus Q\), and define for
\(a\in A\)
\[
 e_a:E(K_R)\longrightarrow{\cal C},
 \qquad
 e_a(uv)=F_a\bigl(R\setminus\{u,v\}\bigr).
\tag{3.1}
\]
For \(u\in R\) let
\[
 {\rm app}_a(u)=\{e_a(uv):v\in R\setminus\{u\}\},
 \qquad
 \mu_a(u)={\cal C}\setminus{\rm app}_a(u).
\tag{3.2}
\]

> **Theorem B.**  Assume the tower laws (1.2) for \(j\in\{0,1\}\) at all
> arguments inside \(R\).  Then:
>
> 1. every \(e_a\) is a **proper edge-colouring of \(K_R\cong K_6\) with the
>    \(17\) colours \({\cal C}\)**; in particular \(|{\rm app}_a(u)|=5\) and
>    \(|\mu_a(u)|=12\);
> 2. \(S_a(P_x)={\rm app}_a(x)\) and hence
>    \(\;V_\gamma(P_x)=\{a\in A:\gamma\in\mu_a(x)\}\);
> 3. writing \(\Lambda(Y)=\{L(R\setminus Z):Y\subseteq Z\subseteq R,\ |Z|=3\}\)
>    for \(Y\in E(K_R)\), one has \(|\Lambda(Y)|=4\) and
>    \(a\mapsto e_a(Y)\) is a **bijection** \(A\to{\cal C}\setminus\Lambda(Y)\);
> 4. conversely, any \(L|_{\binom R3}\) and any thirteen proper
>    \(17\)-edge-colourings \(e_a\) of \(K_R\) satisfying 3 arise this way.
>
> Consequently the six first-lift instances \(I(P_x)\), \(x\in R\), are
> **completely determined** by the single object
> \(\bigl(L|_{\binom R3},(e_a)_{a\in A}\bigr)\): a link colouring of the
> \(20\) triples of \(R\) and thirteen proper \(17\)-edge-colourings of
> \(K_6\).

### Proof

By (2.2), \(e_a(uv)=c^{*}(\{u,v,a\})\), and \(\Lambda(uv)\) is the set of
\(c^{*}\)-values on the four triples \(Z\subseteq R\) containing \(\{u,v\}\).
Statement 3 is the star condition of Theorem A at \(Y=\{u,v\}\subseteq R\)
(the case \(j=0\) there, i.e. the fan law); its \(4+13=17\) values are
distinct, and the four link values are distinct among themselves, whence
\(|\Lambda(Y)|=4\).

Statement 1: two edges \(uv,uv'\) of \(K_R\) sharing the vertex \(u\)
correspond to \(Q=R\setminus\{u,v\}\) and \(Q'=R\setminus\{u,v'\}\) with
\(|Q\cap Q'|=3\), so \(Q\cup Q'=P\) is a five-subset of \(R\) with
\(Q=P\setminus\{v'\}\), \(Q'=P\setminus\{v\}\).  Level-\(1\)
top-properness at \((a,P)\) — which is part of the star condition at
\(Y=\{a\}\cup(R\setminus P)\), a pair with \(|Y\cap A|=1\) — gives
\(F_a(Q)\ne F_a(Q')\), i.e. \(e_a(uv)\ne e_a(uv')\).  So \(e_a\) is proper;
a vertex of \(K_6\) has five incident edges, so \(|{\rm app}_a(u)|=5\).

Statement 2: \(P_x=R\setminus\{x\}\), so
\[
 S_a(P_x)=\{F_a(P_x\setminus\{v\}):v\in P_x\}
 =\{F_a(R\setminus\{x,v\}):v\in R\setminus\{x\}\}
 ={\rm app}_a(x),
\]
and (1.3) gives \(V_\gamma(P_x)=\{a:\gamma\notin{\rm app}_a(x)\}\).

Statement 4 is Theorem A read backwards: conditions 1 and 3 are exactly the
star conditions at pairs \(Y\) with \(|Y\cap A|\le1\), which by Theorem A
are exactly the tower laws for \(j\in\{0,1\}\) with arguments inside \(R\).
\(\square\)

> **Corollary B1 (support ledger).**  For \(\gamma\in{\cal C}\) let
> \(m_{a,\gamma}=e_a^{-1}(\gamma)\subseteq E(K_R)\) — a matching of \(K_6\),
> of size \(u_{a,\gamma}\in\{0,1,2,3\}\) — and let \(X_{a,\gamma}\subseteq R\)
> be the set of vertices it covers, \(|X_{a,\gamma}|=2u_{a,\gamma}\).  Then
> \[
>  a\in V_\gamma(P_x)\iff x\notin X_{a,\gamma},
>  \qquad
>  |V_\gamma(P_x)|=13-\#\{a:x\in X_{a,\gamma}\} .
> \tag{3.3}
> \]
> Let \(t_\gamma(R)=\#\{Z\subseteq R:|Z|=3,\ c^{*}(Z)=\gamma\}\) and
> \(\tau_\gamma(x)=\#\{Z\ni x:|Z|=3,\ Z\subseteq R,\ c^{*}(Z)=\gamma\}\).
> Then
> \[
>  \sum_{a\in A}u_{a,\gamma}=15-3t_\gamma(R),
>  \qquad
>  |V_\gamma(P_x)|=8+2\tau_\gamma(x),
>  \qquad
>  \sum_{x\in R}\tau_\gamma(x)=3t_\gamma(R),
> \tag{3.4}
> \]
> with \(t_\gamma(R)\le4\), \(\tau_\gamma(x)\le2\) and
> \(|V_\gamma(P_x)|\in\{8,10,12\}\).

*Proof.*  (3.3) is Theorem B.2 with (3.2): \(\gamma\in{\rm app}_a(x)\) iff
some edge at \(x\) has \(e_a\)-colour \(\gamma\) iff \(x\in X_{a,\gamma}\).

By Theorem A the \(\gamma\)-class of \(c^{*}\) covers every pair of \(W\)
meeting \(R\) at most once, and every pair \(Y\subseteq R\) exactly once
(the star at \(Y\) is rainbow with all \(17\) colours present, because it
has exactly \(17\) members).  A pair \(Y\subseteq R\) is covered either by a
\(\gamma\)-triple inside \(R\) or by a unique triple \(Y\cup\{a\}\), i.e. by
a unique \(a\) with \(e_a(Y)=\gamma\).  Counting the \(15\) pairs of \(R\):
the \(t_\gamma(R)\) internal \(\gamma\)-triples cover \(3t_\gamma(R)\) of
them (they meet pairwise in at most one point, since two triples sharing a
pair are \(J\)-adjacent and \(c^{*}\) is proper), and the rest are covered
once each by the \(m_{a,\gamma}\).  This is the first identity of (3.4), and
it also shows \(t_\gamma(R)\le\lfloor 15/3\rfloor\) refined by the packing
bound on six points, \(t_\gamma(R)\le4\).

Finally \(x\in X_{a,\gamma}\) iff \(\gamma\in{\rm app}_a(x)\), and summing
the star condition at the five pairs \(Y\ni x\) inside \(R\) gives
\(\#\{a:x\in X_{a,\gamma}\}=5-2\tau_\gamma(x)\): each pair \(Y\ni x\) is
covered by an \(a\) unless it lies in an internal \(\gamma\)-triple, and each
internal \(\gamma\)-triple through \(x\) absorbs exactly two such pairs, no
two of them sharing a pair.  Hence \(|V_\gamma(P_x)|=8+2\tau_\gamma(x)\);
\(\tau_\gamma(x)\le2\) because three internal \(\gamma\)-triples through
\(x\) would need \(1+3\cdot2=7>6\) points.  Summing over \(x\) gives
\(3t_\gamma(R)\).  \(\square\)

These identities agree with Theorem 4 of `../../unrestricted_lift_tower/NOTE.md`
and with equation (28) there; the new content is that all of them are
statements about the thirteen \(K_6\)-colourings \(e_a\).

---

## 4. Theorem C: the six simultaneous same-colour matchings

> **Theorem C.**  Fix \(R\in\binom U6\) and suppose the tower laws for
> \(j\in\{0,1\}\) hold at all arguments inside \(R\), and that for each
> \(x\in R\) a solution \(h_{P_x}\) of \(I(P_x)\) has been chosen, with
> colour classes \(M_\gamma(P_x)\).  Then level-\(2\) top-properness (1.4)
> at \(R\) holds **iff**
> \[
>  \forall\gamma\in{\cal C}\ \ \forall x\ne x'\in R:\qquad
>  M_\gamma(P_x)\cap M_\gamma(P_{x'})=\varnothing .
> \tag{4.1}
> \]
> The supports are given by (3.3), and
> \[
>  \sum_{x\in R}\bigl|M_\gamma(P_x)\bigr|
>   =24+3\,t_\gamma(R)\ \le\ 36,
>  \qquad
>  \sum_{\gamma\in{\cal C}}\sum_{x\in R}\bigl|M_\gamma(P_x)\bigr|
>   =6\cdot78=468 .
> \tag{4.2}
> \]

### Proof

For an edge \(ab\in E(K_A)\) and \(x\in R\) we have \(h_{P_x}(ab)=\gamma\)
iff \(ab\in M_\gamma(P_x)\).  So the six values \(h_{P_x}(ab)\), \(x\in R\),
are pairwise distinct iff no colour class is used twice at \(ab\), i.e. iff
no two of the six matchings \(M_\gamma(P_x)\) share the edge \(ab\).
Quantifying over \(ab\) and \(\gamma\) gives (1.4) \(\Leftrightarrow\) (4.1).

By Corollary B1, \(|M_\gamma(P_x)|=\tfrac12|V_\gamma(P_x)|=4+\tau_\gamma(x)\),
and \(\sum_x\tau_\gamma(x)=3t_\gamma(R)\le12\), giving the first identity in
(4.2).  Summing over \(\gamma\) and using
\(\sum_\gamma t_\gamma(R)=\binom63=20\) gives
\(17\cdot24+3\cdot20=408+60=468\), which also equals \(6\cdot78\) because
for each fixed \(x\) the seventeen matchings partition the \(78\) edges of
\(K_A\).  \(\square\)

Theorem C is the precise reconstruction of the statement identified in
`../coordinated_nine_and_global_bridge/NOTE.md`, Theorem 8, together with
its shared data.  Three consequences are worth recording explicitly.

> **Corollary C1 (no counting obstruction).**  The six matchings of a fixed
> colour occupy at most \(36\) of the \(78\) edges of \(K_A\), so (4.1) can
> never fail for a global edge-count reason.  For a fixed vertex \(a\in A\)
> the six matchings use at most \(6\) of the \(12\) edges at \(a\), so no
> vertex-degree count obstructs either.  \(\square\)

> **Corollary C2 (the coupling is a list problem at each edge).**  For a
> fixed edge \(ab\), condition (1.4) asks for six distinct colours
> \(\gamma_x\in\mu_a(x)\cap\mu_b(x)\), and
> \(|\mu_a(x)\cap\mu_b(x)|=7+|S_a(P_x)\cap S_b(P_x)|\ge7>6\).  So the
> single-edge relaxation of the coupling is always satisfiable, by Hall.
> \(\square\)

> **Corollary C3 (the six instances are rigidly linked).**  By Theorem B the
> six instances \(I(P_x)\) share the thirteen colourings \(e_a\).  In
> particular, for every \(a\in A\),
> \(\sum_{x\in R}|S_a(P_x)|=30\) and each colour \(\gamma\) lies in
> \(S_a(P_x)\) for exactly \(2u_{a,\gamma}\) of the six \(x\); and for every
> \(\gamma\), \(\sum_{x\in R}|V_\gamma(P_x)|=48+6t_\gamma(R)\).  Hence a
> proof of (4.1) may use the whole \(K_6\)-colouring structure and is not
> forced to treat the six instances as independent class-B instances.
> \(\square\)

### The earliest missing implication, with full quantifiers

Let \({\frak F}\) be a **simultaneous \(13\)-fan**: a labelled
\(LS(2,3,19)\) \(L\) on \(U\) together with maps \(F_a:\binom U4\to{\cal C}\)
(\(a\in A\)) satisfying the \(j=0\) tower law and level-\(1\)
top-properness, equivalently (Proposition 2 of the tower note) thirteen
labelled \(LS(3,4,20)\)'s \(\widehat F_a\) with common link \(L\) whose
thirteen values on every \(Q\in\binom U4\) are pairwise distinct.

> **(EMI).**  For every simultaneous \(13\)-fan \({\frak F}\):
> \[
> \Bigl[\forall P\in\tbinom U5\ \exists h_P\ \hbox{solution of }I(P)\Bigr]
> \ \Longrightarrow\
> \Bigl[\exists (h_P)_{P\in\binom U5},\ \hbox{each a solution of }I(P),\
> \forall R\in\tbinom U6\ \forall\{a,b\}\in\tbinom A2:\
> \bigl|\{h_{R\setminus\{x\}}(ab)\}_{x\in R}\bigr|=6\Bigr].
> \]

The hypothesis is a conjunction of \(\binom{19}5=11\,628\) **independent**
existence statements.  The conclusion is a single simultaneous choice
subject to \(\binom{13}2\binom{19}6=78\cdot27\,132=2\,116\,296\) constraints,
each of which couples six of the \(11\,628\) choices.  **(EMI) is not proved
here and is not a formal consequence of its hypothesis.**  What Theorem C
adds is that the coupling is not a conjunction of unrelated demands either:
by Theorem B every constraint set is generated by thirteen proper
\(17\)-edge-colourings of \(K_6\), and by Corollary A2 each individual
\(R\)-constraint is satisfiable in isolation.

Two further implications sit *before* (EMI) and are also unproved:

* **(EMI-0a)** the \(r=0\) prescribed-colour gate — assumed as a
  **hypothesis** throughout this note, per the assignment; the certified
  campaign has closed orbits \(0\)–\(4\), orbit \(5\) is solver-terminal and
  under DRAT certification, and eleven Venn types have only an audited
  finite reduction (`../../opus5_r0_orbit_repair/2026-07-28_prescribed_colour_remaining_audit.md`);
* **(EMI-0b)** coordinated nine at \(P\) \(\Rightarrow\) a full solution of
  \(I(P)\).  Section 5 shows the arbitrary-prefix form of (EMI-0b) is false
  at depth fourteen, and that no counting invariant can repair it.

---

## 5. Theorem D: an exact class-B\('\) prefix whose obstruction is a snark

### 5.1 The certificate

Let \(\mathbb Z_5=\{0,1,2,3,4\}\), all indices mod \(5\).  Put
\[
 A=\{x,y,z\}\ \dot\cup\ V,
 \qquad
 V=\{e_0,\dots,e_4\}\ \dot\cup\ \{f_0,\dots,f_4\},
 \qquad |A|=13 .
\]
Define the **Petersen graph** \(\Pi\) on \(V\) by
\[
 E(\Pi)=\{e_ie_{i+2}\}\cup\{f_if_{i+1}\}\cup\{e_if_{i+2}\}
 \qquad(i\in\mathbb Z_5),
\tag{5.1}
\]
an inner pentagram on the \(e\)'s, an outer pentagon on the \(f\)'s and five
spokes; \(|E(\Pi)|=15\) and \(\Pi\) is \(3\)-regular.

Define four perfect matchings of \(V\) and one \(2\)-factor:
\[
 Q_1=\{e_if_i\},\quad
 Q_2=\{e_if_{i+4}\},\quad
 Q_3=\{e_if_{i+3}\},\quad
 Q_4=\{e_if_{i+1}\},\quad
 \Psi=\{e_ie_{i+1}\}\cup\{f_if_{i+2}\}
\tag{5.2}
\]
(\(i\) ranging over \(\mathbb Z_5\) in each).  Write \(E_i=e_ie_{i+1}\) and
\(F_i=f_if_{i+2}\) for the ten edges of \(\Psi\).

The **fourteen prefix matchings** are
\[
\begin{aligned}
 M_A&=\{yz\}\cup Q_1, &
 M_B&=\{xz\}\cup Q_2, &
 M_C&=\{xy\}\cup Q_3, &
 M_D&=Q_4,\\[2pt]
 N_i&=\{xf_i,\ yf_{i+1},\ zf_{i+2}\}\cup\{E_i\}, &
 N'_i&=\{xe_i,\ ye_{i+1},\ ze_{i+2}\}\cup\{F_i\}
 &&(i\in\mathbb Z_5).
\end{aligned}
\tag{5.3}
\]
The **seventeen colour rows** are their supports together with three
further colours \(\gamma_1,\gamma_2,\gamma_3\) whose support is \(V\).
Writing \(B_c=A\setminus V_c\):
\[
\begin{array}{ll}
 B(M_A)=\{x\},\quad B(M_B)=\{y\},\quad B(M_C)=\{z\}
   &\hbox{(three rows, }|V_c|=12),\\[2pt]
 B(M_D)=B(\gamma_1)=B(\gamma_2)=B(\gamma_3)=\{x,y,z\}
   &\hbox{(four rows, }|V_c|=10),\\[2pt]
 B(N_i)=\{f_{i+3},f_{i+4},e_{i+2},e_{i+3},e_{i+4}\},\quad
 B(N'_i)=\{e_{i+3},e_{i+4},f_{i+1},f_{i+3},f_{i+4}\}
   &\hbox{(ten rows, }|V_c|=8).
\end{array}
\tag{5.4}
\]

> **Theorem D.**  The seventeen rows (5.4) are a target-order **class-B\('\)**
> instance of profile \(r=3\), i.e.
> \((n_8,n_{10},n_{12})=(10,4,3)\).  The fourteen matchings (5.3) are
> pairwise edge-disjoint and each is a perfect matching on its prescribed
> support, so they are a legitimate coordinated-fourteen prefix.  Their
> union is \(K_{13}-\Pi\); the residual graph is exactly the Petersen graph
> \(\Pi\), and the three unused colours all have support \(V\).
> Consequently the prefix extends by exactly one further matching — to
> **fifteen** — and never to sixteen or seventeen.

### 5.2 Proof that the certificate is a class-B instance of profile \(r=3\)

*The \(25\) \(e\)–\(f\) edges of \(K_V\) split by offset into five perfect
matchings \(\{e_if_{i+k}\}\), \(k\in\mathbb Z_5\).*  By (5.1)–(5.2),
\(\Pi\) takes \(k=2\) and \(Q_1,Q_4,Q_3,Q_2\) take \(k=0,1,3,4\).  The ten
\(e\)–\(e\) edges split by offset into \(\{e_ie_{i+2}\}\subseteq\Pi\) and
\(\{e_ie_{i+1}\}\subseteq\Psi\); the ten \(f\)–\(f\) edges into
\(\{f_if_{i+1}\}\subseteq\Pi\) and \(\{f_if_{i+2}\}\subseteq\Psi\).
Therefore
\[
 K_V=\Pi\ \dot\cup\ Q_1\ \dot\cup\ Q_2\ \dot\cup\ Q_3\ \dot\cup\ Q_4\ \dot\cup\ \Psi,
 \qquad 45=15+4\cdot5+10 ,
\tag{5.5}
\]
each \(Q_j\) is a perfect matching of \(V\) (it is a bijection
\(e_i\mapsto f_{i+k}\)), and \(\Psi\) is a \(2\)-factor consisting of the
two \(5\)-cycles \(e_0e_1e_2e_3e_4\) and \(f_0f_2f_4f_1f_3\).

*Edge-disjointness and supports of (5.3).*  \(M_A,M_B,M_C\) use the three
distinct edges \(yz,xz,xy\) inside \(\{x,y,z\}\) and the pairwise disjoint
matchings \(Q_1,Q_2,Q_3\); \(M_D=Q_4\).  So these four are pairwise
edge-disjoint, and \(M_A\) covers \(\{y,z\}\cup V\) (\(12\) vertices,
\(6\) edges), similarly \(M_B,M_C\), while \(M_D\) covers \(V\)
(\(10\) vertices, \(5\) edges).  The ten matchings \(N_i,N'_i\) use only
\(\{x,y,z\}\)–\(V\) edges and \(\Psi\)-edges, hence are disjoint from the
first four.  Among themselves: the \(x\)-partners are \(f_0,\dots,f_4\)
(from the \(N_i\)) and \(e_0,\dots,e_4\) (from the \(N'_i\)), each exactly
once, and likewise for \(y\) (partners \(f_{i+1}\), \(e_{i+1}\)) and \(z\)
(partners \(f_{i+2}\), \(e_{i+2}\)); so the thirty \(\{x,y,z\}\)–\(V\) edges
are used exactly once each.  The \(\Psi\)-edges \(E_i,F_i\) are used exactly
once each.  Inside \(N_i\), the edge \(E_i=e_ie_{i+1}\) is disjoint from
\(\{f_i,f_{i+1},f_{i+2}\}\); inside \(N'_i\), \(F_i=f_if_{i+2}\) is disjoint
from \(\{e_i,e_{i+1},e_{i+2}\}\).  So each \(N_i,N'_i\) is a matching of
four edges covering eight vertices, giving the supports and complements in
(5.4).

*Total.*  The prefix uses \(3+30+20+10=63\) edges, and
\(78-63=15=|E(\Pi)|\); by (5.5) the unused edges are exactly \(E(\Pi)\).

*Class-B row condition.*  Each vertex must lie in exactly five complements.
\(x\) lies in \(B(M_A)\) and in the four rows with \(B=\{x,y,z\}\): five.
Same for \(y\) (via \(B(M_B)\)) and \(z\) (via \(B(M_C)\)).  For \(e_j\):
\(e_j\in B(N_i)\iff j\in\{i+2,i+3,i+4\}\), three values of \(i\); and
\(e_j\in B(N'_i)\iff j\in\{i+3,i+4\}\), two values: five.  For \(f_j\):
\(f_j\in B(N_i)\iff j\in\{i+3,i+4\}\), two; and
\(f_j\in B(N'_i)\iff j\in\{i+1,i+3,i+4\}\), three: five.  Every
\(|B_c|\in\{1,3,5\}\) is odd and at most \(5\), so the instance is class B,
with \((n_8,n_{10},n_{12})=(10,4,3)\) and
\(\sum_c|V_c|=10\cdot8+4\cdot10+3\cdot12=156=13\cdot12\).  This is the
profile \(r=3\).

### 5.3 Proof that the certificate is class B\('\)

By §1 of `../../first_lift_support_completion/NOTE.md`, the instance is
partial-factorization-realizable iff the missing-incidence bipartite graph
\({\cal B}=\{(a,c):a\in B_c\}\) admits a proper edge-colouring by the five
points \(P=\{p_1,\dots,p_5\}\) using every point once at every \(a\), such
that the points unused at each colour \(c\) pair into a matching \(N_c\)
with the seventeen \(N_c\) partitioning \(E(K_P)\cong K_5\).

Take
\[
\begin{array}{l|ccccc}
 &M_A\ \hbox{or}\ M_B\ \hbox{or}\ M_C&M_D&\gamma_1&\gamma_2&\gamma_3\\\hline
 x&p_1&p_2&p_3&p_4&p_5\\
 y&p_2&p_1&p_4&p_5&p_3\\
 z&p_3&p_5&p_1&p_2&p_4
\end{array}
\]
(the first column meaning \(\lambda(x,M_A)=p_1\), \(\lambda(y,M_B)=p_2\),
\(\lambda(z,M_C)=p_3\); those are the only incidences of \(M_A,M_B,M_C\)).
Each row of the table is a permutation of \(P\), so every point is used once
at each of \(x,y,z\).  At each colour the entries are distinct:
\(M_D\!:\{p_2,p_1,p_5\}\), \(\gamma_1\!:\{p_3,p_4,p_1\}\),
\(\gamma_2\!:\{p_4,p_5,p_2\}\), \(\gamma_3\!:\{p_5,p_3,p_4\}\).  Unused
points and their pairings:
\[
 N_{M_D}=\{p_3p_4\},\ N_{\gamma_1}=\{p_2p_5\},\ N_{\gamma_2}=\{p_1p_3\},\
 N_{\gamma_3}=\{p_1p_2\},
\]
\[
 N_{M_A}=\{p_2p_3,\,p_4p_5\},\quad
 N_{M_B}=\{p_1p_4,\,p_3p_5\},\quad
 N_{M_C}=\{p_1p_5,\,p_2p_4\} .
\]
These ten pairs are precisely the ten edges of \(K_P\), each once.

The remaining incidences are those with \(a\in V\), and every such \(a\) has
all five of its complements among the ten size-five rows (each \(a\in V\)
lies in the supports of \(M_A,M_B,M_C,M_D,\gamma_1,\gamma_2,\gamma_3\)).
The bipartite graph between \(V\) and the ten size-five rows is therefore
\(5\)-regular on both sides, so by König's edge-colouring theorem it has a
proper \(5\)-edge-colouring; since every degree equals \(5\), every vertex
of \(V\) uses all five points once, and every size-five row receives five
distinct points, leaving no unused point and \(N_c=\varnothing\).  All
conditions hold, so the instance is class B\('\).  \(\square\)

### 5.4 Proof that the prefix dies at fifteen

> **Lemma D1.**  The Petersen graph has no two edge-disjoint perfect
> matchings, and hence is not \(3\)-edge-colourable.

*Proof.*  If \(M\ne M'\) were edge-disjoint perfect matchings, \(M\cup M'\)
would be a spanning \(2\)-regular subgraph all of whose cycles alternate
between \(M\) and \(M'\), hence are even.  A partition of the ten vertices
into even cycles of length \(\ge4\) is \(10\), \(6+4\) or \(4+4+\dots\).
The Petersen graph has girth \(5\), so it has no \(4\)-cycle; and it is not
Hamiltonian, so it has no \(10\)-cycle.  Contradiction.  A proper
\(3\)-edge-colouring of a cubic graph is a partition into three pairwise
disjoint perfect matchings, so \(\Pi\) is class \(2\).  \(\square\)

The three unused colours \(\gamma_1,\gamma_2,\gamma_3\) all have support
\(V\), so each of their matchings must be a perfect matching of \(V\)
contained in the residual graph \(\Pi\), and the three must be pairwise
edge-disjoint.  By Lemma D1 at most one such matching can be chosen; and
\(\Pi\) does have perfect matchings, so exactly one can.  Hence the prefix
extends to exactly fifteen matchings and to no more.  This proves
Theorem D. \(\square\)

### 5.5 The obstruction is invisible to the capacity family and to the LP

> **Lemma D4 (capacity slack of a \(3\)-edge-connected cubic graph).**  Let
> \(H\) be a \(3\)-edge-connected cubic graph on \(2n\) vertices and let
> \(F\subseteq E(H)\).  Then
> \[
>  n-\nu(H-F)\ \le\ \tfrac13|F| .
> \]

*Proof.*  Put \(G=H-F\) and \({\rm def}=n-\nu(G)\); the number of vertices
left unmatched by a maximum matching of \(G\) is \(2\,{\rm def}\).  If
\({\rm def}=0\) there is nothing to prove, so assume \({\rm def}\ge1\).  By
the Berge–Tutte formula choose \(S\subseteq V(H)\), \(s=|S|\), with
\(o(G-S)-s=2\,{\rm def}\).  Let \(C_1,\dots,C_p\) be the components of
\(G-S\), so \(p\ge o(G-S)=s+2\,{\rm def}\ge 2\); in particular no \(C_i\)
is all of \(V(H)\).

Since \(H\) is \(3\)-edge-connected, \(|\delta_H(C_i)|\ge3\) for every
\(i\).  Every \(H\)-edge joining two distinct components is absent from
\(G\), hence lies in \(F\); write \(I\) for the number of such edges and
\(T\) for the number of \(H\)-edges between \(\bigcup_iC_i\) and \(S\).
Counting boundary incidences,
\[
 2I+T=\sum_{i=1}^p|\delta_H(C_i)|\ \ge\ 3p\ \ge\ 3s+6\,{\rm def},
\]
while \(T\le 3s\) because every vertex of \(S\) has degree \(3\).  Hence
\(2I\ge6\,{\rm def}\), i.e. \(|F|\ge I\ge3\,{\rm def}\). \(\square\)

> **Theorem D2.**  Let \({\cal R}\) be the residual instance of Theorem D:
> three colours, common support \(V\), available graph \(\Pi\).  Then
>
> 1. every colour individually has a perfect matching in \(\Pi\), so no
>    Tutte/odd-set condition fires per colour, and the ordinary cut test is
>    satisfied;
> 2. the matching-deletion capacity inequality of Theorem 1 of
>    `../../first_lift_support_completion/NOTE.md`,
>    \(\sum_{c}\bigl(\tfrac12|V_c|-\nu(\Pi-F)\bigr)\le|F|\), holds for
>    **every** \(F\subseteq E(\Pi)\);
> 3. the fractional relaxation
>    \(\{x_{e,c}\ge0,\ \sum_cx_{e,c}=1\ (e\in E(\Pi)),\
>    \sum_{e\ni a}x_{e,c}=1\ (a\in V,\ c)\}\)
>    is feasible, with the **uniform** point \(x_{e,c}=\tfrac13\) for all
>    \(e,c\);
> 4. nevertheless \({\cal R}\) has no integral solution.

*Proof.*  1 is classical (Petersen's theorem: every bridgeless cubic graph
has a perfect matching; \(\Pi\) is \(3\)-edge-connected).  The ordinary cut
test is the special case \(F=\delta(X)\) of 2.

2: the three colours all have \(\tfrac12|V_c|=5=n\), so the left side is
\(3\bigl(n-\nu(\Pi-F)\bigr)\), and Lemma D4 bounds it by \(|F|\).

3: by Edmonds' perfect-matching polytope theorem, \(x\ge0\) lies in the
perfect-matching polytope of a graph \(H\) iff \(x(\delta(v))=1\) for every
vertex and \(x(\delta(S))\ge1\) for every odd \(S\subseteq V(H)\).  For
\(x\equiv\frac13\) on the cubic graph \(\Pi\):
\(x(\delta(v))=3\cdot\frac13=1\); and \(x(\delta(S))=|\delta(S)|/3\ge1\)
because \(\Pi\) is \(3\)-edge-connected, so \(|\delta(S)|\ge3\) for every
odd \(S\) with \(1\le|S|\le9\).  Hence \(x\equiv\frac13\) is a convex
combination of perfect matchings of \(\Pi\) for each colour, and
\(\sum_{c}x_{e,c}=3\cdot\frac13=1\) for every edge.

4 is Lemma D1.  \(\square\)

So the deadness of the prefix is not detectable by any member of the
capacity family — which by Proposition BC1 of
`../first_lift_classB_attack/NOTE.md` contains both cut inequalities of
`../first_lift_k13_hole/NOTE.md` and vertex Hall — nor by the fractional
relaxation.  I do **not** claim that literally every conceivable counting
condition is checked: (BC), (BP) and (PART) are stated for class-B
instances inside \(K_A\), not for a residual subgraph, and I have verified
only their natural analogues listed in Theorem D2.  What is proved is that
the separating certificate is \(3\)-edge-colourability, and that the whole
capacity/LP layer is blind to it.

> **Corollary D3 (what the "minimal additional invariant'' cannot be).**
> No invariant of a prefix that depends only on the residual graph's degree
> sequence, its odd-cut system, its matching numbers \(\nu(\Pi-F)\) after
> edge deletions, or any linear function on the fractional matching
> polytope can characterise extendability of a class-B\('\) prefix at the
> target order: by Theorem D2 every one of them is *satisfied* on the
> Petersen residual, exactly as it is on any \(3\)-edge-connected cubic
> residual of class \(1\), where extension does succeed; so none of them
> separates the two.  An invariant sufficient for a prefix-extension
> theorem must, at minimum, decide \(3\)-edge-colourability of the residual
> cubic core.  \(\square\)

### 5.6 The dichotomy

> **Corollary F.**  Exactly one of the following holds for the instance of
> Theorem D.
>
> (a) The instance has a full \(17\)-matching completion.  Then there is a
> class-B\('\) instance at the target order, of a profile for which
> coordinated nine is already a theorem in this repository (\(r=3\)),
> possessing a legitimate coordinated-fourteen prefix that does not extend,
> whose obstruction is invisible to every counting certificate listed in
> §5.5.  In particular **no theorem of the form "every coordinated
> \(k\)-prefix extends'' can hold for \(k\ge14\)**, and the completion
> theorem must be existential in the prefix and must control the residual up
> to edge-colourability.
>
> (b) The instance has no completion.  Then the class-B\('\) completion
> Question at \(n=13,q=17\) is **refuted**, and with it the first-lift
> completion route to a simultaneous \(13\)-fan.

*Proof.*  The two alternatives are exhaustive and exclusive; the content of
(a) is Theorem D plus §5.5, and the content of (b) is the definition of the
Question in §11 of `../first_lift_classB_attack/NOTE.md` together with §5.3
(the instance is class B\('\)).  \(\square\)

Deciding (a) versus (b) is a finite exact computation over the seventeen
prescribed supports of (5.4); `decide_certificate_completion.py` performs
it by complete depth-first search.  **It was not run in this session.**
I expect (a), because every sampled class-B and class-B\('\) instance in this
repository has completed; but that is an expectation, not a result, and
nothing above depends on it.

---

## 6. Theorem E: the tail dichotomy, and where counting stops working

Let \(I\) be any class-B instance at \(n=13\) and let \(k\) colours remain
unused after a legitimate \((17-k)\)-prefix with union \(D\), residual
\(H=K_{13}-D\).

> **Theorem E.**  For every vertex \(v\),
> \(d_H(v)=\#\{\hbox{remaining colours }c:v\in V_c\}\), so
> \(\Delta(H)\le k\), and the remaining problem is exactly: properly
> \(k\)-edge-colour \(H\) so that the class of \(c\) is a perfect matching
> on \(V_c\).  Moreover
>
> 1. \(k=1\): the residual **is** the required perfect matching; the last
>    colour is automatic.
> 2. \(k=2\): \(H\) has maximum degree \(\le2\), so its components are paths
>    and cycles; a solution exists iff every cycle component is even and
>    every path component has the parity forced by the colours of its two
>    end-edges.  Every failure is witnessed by an odd-cut violation on the
>    component's vertex set, hence is visible to the cut conditions.
> 3. \(k=3\): the problem already contains, as a special case, proper
>    \(3\)-edge-colourability of an arbitrary cubic residual on the vertices
>    lying in all three remaining supports.  By Theorem D2 that is visible
>    neither to the matching-deletion capacity family nor to the fractional
>    relaxation.

### Proof

The degree identity: \(v\) lies in exactly \(12\) of the \(17\) supports and
is saturated by exactly those chosen matchings whose support contains it,
so \(d_H(v)=12-\#\{\hbox{chosen }c:v\in V_c\}
=\#\{\hbox{remaining }c:v\in V_c\}\).  The remaining matchings must be
edge-disjoint, cover their supports, and exhaust \(H\) (because
\(\sum_c|V_c|/2=78\)); that is exactly a proper \(k\)-edge-colouring of
\(H\) with the prescribed classes.

1.  \(d_H(v)=[v\in V_{c}]\) for the single remaining colour \(c\), so \(H\)
is a graph of maximum degree \(1\) covering exactly \(V_c\): a perfect
matching on \(V_c\).

2.  Components of \(H\) are paths and cycles.  A vertex of degree \(2\) lies
in both remaining supports, so it must receive one edge of each colour: the
colours alternate.  A vertex of degree \(1\) lies in exactly one remaining
support, which forces the colour of its edge.  Hence on a cycle the
alternation closes iff the cycle is even, and on a path the two forced end
colours must be compatible with the alternation, a parity condition on the
path's length.  If a cycle \(C\) is odd, take \(X=V(C)\): both remaining
colours have \(|V_c\cap X|=|C|\) odd, so each needs an odd number — in
particular at least one — of residual edges leaving \(X\); but \(C\) is a
component of \(H\), so no residual edge leaves \(X\).  This is a violation
of the ordinary odd-cut inequality.  The path case is the same count with
\(X\) the path's vertex set.

3.  Take three remaining colours with a common support \(V\) (a twin class
of size three; the certificate of §5 realises one of size four).  Then
\(d_H(v)=3\) for \(v\in V\) and \(0\) otherwise, so \(H\) is a cubic graph
on \(V\), and the remaining problem is precisely a proper
\(3\)-edge-colouring of \(H\).  Theorem D exhibits \(H=\Pi\).  \(\square\)

So the exact frontier of counting methods in the first lift is between
\(k=2\) and \(k=3\): **the last two colours are governed by cuts, the last
three are not.**

---

## 7. Independent audit surface

Everything in §§2–4 and §§5.2–5.4, 5.5, 6 is proved by hand above and can
be re-derived with pencil and paper.  The finite data an auditor should
re-check directly are:

* **(A1)** the coordinate bijection \(Z\mapsto(Z\cap A,\ R\setminus(Z\cap R))\)
  of §2 and the star count \(|W|-2=17\);
* **(B1)** Theorem B.1–B.3 on any explicit \(LS(2,3,19)\): pick a
  \(19\)-set \(W\), a \(6\)-subset \(R\), and check that the induced
  \(e_a\) are proper \(17\)-edge-colourings of \(K_6\) and that
  \(a\mapsto e_a(uv)\) is a bijection onto the complement of the four link
  colours;
* **(C1)** identities (4.2) on the same control;
* **(D1)** the certificate of §5.1: fourteen matchings, \(63\) edges, all
  distinct, supports as in (5.4), residual \(=\Pi\), class-B row counts all
  equal to five, and the class-B\('\) point-labelling of §5.3;
* **(D2)** Lemma D1 by direct enumeration of the perfect matchings of the
  Petersen graph (there are six, and any two share exactly one edge);
* **(D4)** Lemma D4 on \(\Pi\) by exhausting all \(2^{15}=32\,768\) subsets
  \(F\subseteq E(\Pi)\) and comparing \(3\bigl(5-\nu(\Pi-F)\bigr)\) with
  \(|F|\).  (The lemma is proved above for every \(3\)-edge-connected cubic
  graph; this is only a control on the proof.)

Three scripts are provided for this, all standard-library only and
deterministic.  **None of them was executed in this session**, because no
interpreter was available; their output is therefore *not* evidence for any
claim above, and every claim above is proved without them.

```sh
cd "<repo root>"
python3 -B collaboration/opus5/post_r0_global_bridge/verify_petersen_dead_prefix.py
python3 -B collaboration/opus5/post_r0_global_bridge/verify_coupling_reformulation.py
python3 -B collaboration/opus5/post_r0_global_bridge/decide_certificate_completion.py
```

The first re-checks (D1) and (D2) from the definitions and prints
`ALL CHECKS PASS`.  The second re-checks (A1), (B1) and (C1) against the
repository's committed cyclic \(LS(2,3,19)\)
(`collaboration/cyclic_lsts19_extension`), printing `SKIP` for the empirical
part if that import fails.  The third decides Corollary F by complete
depth-first search and prints `COMPLETES` or `NO COMPLETION`.

---

## 8. Gap audit

**Proved here, unconditionally and solver-free:**

* Theorem A and Corollaries A1, A2 (the \(R\)-local Johnson reformulation at
  every level).
* Theorem B and Corollary B1 (the shared data; the support ledger).
* Theorem C and Corollaries C1–C3 (the six simultaneous same-colour
  matchings, with all quantifiers).
* Theorem D, Lemma D1, Lemma D4, Theorem D2, Corollary D3 (the class-B\('\)
  fourteen-prefix with Petersen residual, and its invisibility to the
  capacity family and to the LP).
* Theorem E (the tail dichotomy).
* Corollary F as a dichotomy — **not** as a determination of which branch
  holds.

**Not proved here:**

* **(EMI)** — the implication from per-\(P\) completability to a coordinated
  choice across all \(P\).  This remains the earliest gap after the local
  campaign, and §4 states it with full quantifiers.
* Assignment item 1.  No theorem upgrading coordinated nine to a full
  seventeen-matching completion is proved.  Theorem D refutes the
  *arbitrary-prefix* form at depth fourteen and Corollary D3 rules out an
  entire class of candidate invariants, but the existential form —
  "some coordinated nine, after coordinated switches, extends" — is
  untouched.
* Assignment item 4.  Neither a proof that the six-instance coupling always
  completes nor a no-go is obtained.  Corollary A2 shows a single \(R\) is
  never obstructed in isolation, which is a *negative* result about where an
  obstruction can live, not a positive one.
* Which branch of Corollary F holds.  I did **not** decide whether the
  §5 instance completes.  If it does not, the class-B\('\) Question is
  refuted; I make no claim either way.
* Whether the six matchings \(M_\gamma(P_x)\), \(x\in R\), can always be
  chosen pairwise edge-disjoint *for a single colour in isolation*.  I
  proved the counting is never binding (Corollary C1) and that the
  single-edge relaxation always succeeds (Corollary C2); the full
  single-colour packing statement is left open.  The greedy/dense rule does
  not prove it: with six supports of size eight, the fifth and sixth steps
  fall below the \(s\ge2i\) threshold.
* The \(r=0\) prescribed-colour gate is used only as a **hypothesis**, per
  the assignment.  It is not proved here and its own campaign is
  incomplete (orbit \(5\) under certification; eleven Venn types reduced but
  open).

**Provenance of every number used above.**  \(683=969-286\),
\(468=6\cdot78=17\cdot24+3\cdot20\), \(63=78-15\),
\(156=10\cdot8+4\cdot10+3\cdot12\), \(45=15+20+10\),
\(2\,116\,296=78\cdot27\,132\) and \(11\,628=\binom{19}5\) are all
arithmetic performed and displayed in the text.  \(11\,628\) and the
profile identities are also recorded in
`../coordinated_nine_and_global_bridge/NOTE.md`.  No number in this note
was taken from a program run.

---

## 9. Scope relative to #835

Erdős–Rosenfeld Problem #835 is **open** and \(k=16\) is **not** settled
here.  Precisely:

* Theorem D is a statement about *one local instance and one prefix*.  It is
  not a colouring and not an obstruction to a colouring.  Even branch (b) of
  Corollary F would only close the first-lift route through class B\('\); a
  \(17\)-colouring of \(J(32,16)\) requires the fan-realisable class C,
  which is smaller and is not known to be non-empty.
* Theorem C makes the six-instance coupling exact, but by Corollary A2 the
  coupling at any single \(R\) is satisfiable; and by Corollary A1 the whole
  \(R\)-local layer at level \(j\) is a *partial* \(LS(j,j+1,j+17)\), so it
  can be no stronger than the derivation tower already recorded as
  Theorem 6 of `../coordinated_nine_and_global_bridge/NOTE.md`.  The route
  delimiter established there is confirmed, not weakened: **do not expect a
  levelwise Johnson-colouring condition to obstruct \#835.**
* The local campaign that this note sits on top of — coordinated nine for
  \(r=1,\dots,5\), the \(r=0\) cut-selection theorem, and the
  prescribed-colour orbit closures — covers, for the repository's committed
  cyclic link, a distribution of first-lift profiles
  \((3519,5151,2397,561,0,0)\) over \(r=0,\dots,5\) as recorded in
  `../coordinated_nine_and_global_bridge/NOTE.md`.  Even a complete local
  theorem for all \(11\,628\) instances would leave (EMI) and every higher
  lift untouched.

---

## 10. Verdict

**Reduced, with one exact counterexample and one dichotomy.**

* Assignment item 3 is **proved**: Theorems A, B, C give the six-instance
  same-colour coupling with all quantifiers and with its shared data made
  completely explicit (thirteen proper \(17\)-edge-colourings of \(K_6\)).
* Assignment item 1 is **refuted in its arbitrary-prefix form** and
  otherwise **open**: Theorem D gives an exact legitimate class-B\('\)
  fourteen-prefix at profile \(r=3\) that dies at fifteen.
* Assignment item 2's "minimal additional invariant'' is **delimited from
  below**: by Corollary D3 no cut, parity, partition or linear-programming
  invariant can suffice; the invariant must decide edge-colourability of the
  residual cubic core.
* Assignment item 4 is **open**.  Corollary A2 localises where an
  obstruction cannot be (a single \(R\)), and Corollary A1 identifies the
  \(R\)-local object at level \(j\) as a partial \(LS(j,j+1,j+17)\).
* Erdős–Rosenfeld Problem #835 remains **open**.
