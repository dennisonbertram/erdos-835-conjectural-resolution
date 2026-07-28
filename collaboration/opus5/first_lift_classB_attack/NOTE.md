# The class-B first lift at \(k=16\): two new obstructions, their exact vanishing, and the precise frontier

Date: 2026-07-27.

## 0. The question, and what is and is not settled here

> **Question (class B).**  Let \(A\) be a \(13\)-set and \({\cal C}\) a
> \(17\)-set.  For each \(a\in A\) let \(S_a\in\binom{\cal C}5\), and suppose
> every colour \(c\) lies in an **odd** number \(m_c\le5\) of the sets \(S_a\).
> Must \(E(K_A)\) partition into perfect matchings \(M_c\) on
> \(V_c=\{a\in A:c\notin S_a\}\)?

**The Question is not settled here and remains open.**  What is proved:

1. a new necessary condition **(BC)**, a two-sided bipartite capacity
   inequality for every pair of disjoint vertex sets, which *contains* both
   cut inequalities of `../first_lift_k13_hole/NOTE.md` and Hall's
   condition at a vertex as special cases (Section 3);
2. **(BC) can be violated exactly for \(n\in\{5,7,9,11\}\)** (\(k\in\{8,10,12,14\}\))
   and **for no \(n\in\{3,13,15,17\}\)**, by an exact dynamic program over a
   stated relaxation (Theorem BC2).  All four counterexamples stored in
   `../first_lift_k13_hole/certificates/` violate (BC), so (BC) accounts
   for every obstruction previously known here;
3. a second, independent necessary condition **(BP)**, a *parity* refinement
   of (BC), and a proof that **(BP) can never fire when \(n\ge 2r+2\)**, in
   particular never at \((n,r)=(13,5)\) (Lemma BP, Theorem BP2);
4. a clean threshold for vertex Hall: with \(|S_a|=r\) and \(m_c\le r\), no
   vertex-Hall violation is possible once \(n\ge2r+1\) (Lemma H);
5. **(BC) is not sufficient**, and neither is the natural fractional
   relaxation (LP) below.  Explicit
   certificates: a \((9,4)\) instance that violates (BP) in a regime where (BC)
   provably cannot fire and whose fractional relaxation has a *strict interior
   point*; and \(n=7,9\) instances at \(r=5\) that are (BC)-clean and have no
   completion (Sections 5, 6);
6. an **infinite family** \(\Pi(3s,\tfrac{3s-1}2)\), \(s\equiv3\pmod 4\), of
   instances with no completion whose minimum support \(n-r=\frac{3s+1}2\) is
   unbounded.  So *the minimum support size does not govern the phenomenon*;
   what governs the parity obstruction is \(q\le 3r\), i.e. \(n\le 2r+1\)
   (Section 6);
7. several **exhaustive** results, each a complete enumeration up to
   relabelling of an entire parameter pair (Section 7): every instance of
   \(\Pi(9,3)\) (103 830 representatives) and of \(\Pi(11,3)\)
   (10 212 660 representatives) completes, while \(\Pi(9,4)\)
   (2 448 157 representatives) has exactly one non-completable instance up to
   relabelling.  A further enumeration of the size-five twin family at
   \(n=13\) had decided \(\ge45\,000\,000\) representatives without finding a
   failure, but **had not terminated**;
8. the exact position of the Question in the literature: it is the
   \(r\times n\) symmetric-Latin-square completion problem with \(r=5\), open
   for every \(r\ge3\) (Section 9).

It does **not** construct a simultaneous \(13\)-fan, an \(LS(3,4,20)\) or a
colouring of \(J(32,16)\), and it does not settle Erdős–Rosenfeld Problem
\#835.

### The classes, kept strictly apart

* **class A**: \(|S_a|=5\) for all \(a\) and every \(|V_c|\) even
  (equivalently every \(m_c\) odd, since \(n=13\) is odd).
* **class B**: class A **and** \(m_c\le5\) for every colour; equivalently
  class A with every support \(|V_c|\in\{8,10,12\}\).
* **class B\('\)**: class B and, in addition, the instance is the local data a
  simultaneous fan induces at one five-set.  Concretely, a class-B\('\) witness
  is a proper \(17\)-edge-colouring of \(K_{18}-E(K_{13})\) in which the five
  vertices outside the hole are saturated and the colours missing at \(a\in A\)
  are exactly \(S_a\).
* **class C**: fan-realisable; \(C\subseteq B'\subsetneq B\); not sampled here
  and not known to be non-empty.

**Only class B\('\)** is equivalent to the partial-edge-colouring extension
question.  Class B is a strictly stronger demand and class C a strictly weaker
one; they are never identified below.

### The two-parameter family

Everything below is stated for
\[
 \Pi(n,r):\quad |A|=n,\ \ q=n+r-1\ \hbox{colours},\ \ |S_a|=r,\ \
 m_c\le r,\ \ |V_c|=n-m_c\ \hbox{even}.
\]
The Question is \(\Pi(13,5)\).  Write \(\mu=n-r\), the minimum possible
support size.

## 1. Setting, and the problem as a list edge colouring

At \(\Pi(13,5)\): \(\sum_c m_c=65\), \(m_c\in\{1,3,5\}\), so exactly six
profiles \((n_5,n_3,n_1)\) with \(n_3=24-2n_5\), \(n_1=n_5-7\),
\(7\le n_5\le12\); and \(\sum_c|V_c|=156\), \(\sum_c|V_c|/2=78=\binom{13}2\).

> **Proposition L.**  Let \(|A|=n\), \(|{\cal C}|=q\), \(|S_a|=q-n+1\) for all
> \(a\).  A family of perfect matchings \(M_c\) on the \(V_c\) partitioning
> \(E(K_A)\) exists **iff** there is a proper edge colouring
> \(h:E(K_A)\to{\cal C}\) with \(h(ab)\notin S_a\cup S_b\) for every edge.

*Proof.*  One direction is clear.  Conversely, the \(n-1\) edges at \(a\) get
distinct colours, all inside \({\cal C}\setminus S_a\), a set of size
\(q-(q-n+1)=n-1\); so every colour of \({\cal C}\setminus S_a\) occurs exactly
once at \(a\), and \(h^{-1}(c)\) is a matching covering exactly \(V_c\).
\(\square\)

So the Question is a list edge colouring of \(K_{13}\) with lists
\({\cal C}\setminus(S_a\cup S_b)\) of size \(7+|S_a\cap S_b|\).  Since
\(\chi'(K_{13})=13\), no general list-colouring bound applies: all the content
is in the special shape of the lists.

## 2. What the earlier note left

`../first_lift_k13_hole/NOTE.md` proves two "cut" inequalities (its
Lemma 1), shows by an exact dynamic program that neither fires at \(n=13\)
(its Theorem B), and exhibits class-B\('\) counterexamples at \(n=5,7,9,11\).
It also stores one \(n=7\) instance violating neither cut and having no
completion.

Two facts about that instance are established here and were not there: it
**does** violate the stronger condition (BC) below — indeed it violates Hall's
condition at a single vertex — and its fractional relaxation is infeasible,
with an exact rational Farkas certificate.  So it is not an example of the
insufficiency of (BC).  Sections 5 and 6 supply instances that are.

## 3. (BC): a two-sided bipartite capacity condition

Fix disjoint \(X,W\subseteq A\).  For a colour \(c\) put
\(s^X_c=|V_c\cap X|\), \(s^W_c=|V_c\cap W|\), \(z_c=|V_c|-s^X_c-s^W_c\), and
\[
 \rho^{\max}_c=
 \begin{cases}
   \min(s^X_c,s^W_c), & z_c\ge1,\\
   \hbox{largest }\rho\le\min(s^X_c,s^W_c)\hbox{ with }\rho\equiv s^X_c\ (2),
     & z_c=0,
 \end{cases}
 \qquad
 \rho^{\min}_c=
 \begin{cases}1,& z_c=0,\ s^X_c\hbox{ odd},\\ 0,&\hbox{else.}\end{cases}
\]

> **Lemma BC.**  If \(E(K_A)\) partitions into perfect matchings \(M_c\) on the
> \(V_c\) then for every pair of disjoint \(X,W\subseteq A\)
> \[
>  \sum_{c}\rho^{\min}_c\;\le\;|X|\,|W|\;\le\;\sum_{c}\rho^{\max}_c .
> \]

*Proof.*  Let \(\rho_c\) be the number of edges of \(M_c\) with one end in
\(X\) and one in \(W\); since the \(M_c\) partition \(E(K_A)\),
\(\sum_c\rho_c=|X||W|\).  Trivially \(\rho_c\le\min(s^X_c,s^W_c)\).  If
\(z_c=0\) then \(V_c\subseteq X\cup W\), so the \(s^X_c-\rho_c\) vertices of
\(V_c\cap X\) unmatched into \(W\) are matched inside \(X\); hence
\(s^X_c-\rho_c\) is even, giving both the parity restriction in
\(\rho^{\max}_c\) and \(\rho_c\ge\rho^{\min}_c\). \(\square\)

Conversely every \(\rho_c\) in \([\rho^{\min}_c,\rho^{\max}_c]\) is attainable
by *some* perfect matching on \(V_c\), in steps of \(1\) if \(z_c\ge1\) and in
steps of \(2\) if \(z_c=0\) (the leftovers can always be paired inside
\(K_{V_c}\)).

> **Proposition BC1 (what (BC) contains).**  With \(W=A\setminus X\) every
> \(z_c=0\) and \(s^X_c\equiv s^W_c\pmod 2\), so
> \(\rho^{\max}_c=\min(s^X_c,s^W_c)\); the upper bound is then **exactly** the
> forced-inside cut \(\sum_c\max(0,s^X_c-\tfrac{|V_c|}2)\le\binom{|X|}2\) and
> the lower bound **exactly** the capacity cut
> \(\sum_c\lfloor s^X_c/2\rfloor\ge\binom{|X|}2\).  With \(X=\{a\}\) the upper
> bound is **exactly** Hall's condition, for the partner set \(W\), in the
> bipartite graph \(H_a\) joining each \(c\notin S_a\) to \(V_c\setminus\{a\}\).

*Proof.*  For \(W=A\setminus X\), \(\rho_c=s^X_c-2e_c\) with \(e_c\) the number
of \(M_c\)-edges inside \(X\); \(\sum_c s^X_c=(n-1)|X|\), so
\(\sum_c\rho_c=(n-1)|X|-2\binom{|X|}2=|X|(n-|X|)\).  Now
\(\rho_c\le\min(s^X_c,s^W_c)\) rearranges to \(e_c\ge s^X_c-|V_c|/2\), and
\(\rho_c\ge s^X_c\bmod2\) to \(e_c\le\lfloor s^X_c/2\rfloor\).  For
\(X=\{a\}\), \(\rho^{\max}_c=\min(1,s^W_c)\), so the upper bound reads
\(|W|\le\#\{c\notin S_a:V_c\cap W\ne\emptyset\}=|N_{H_a}(W)|\). \(\square\)

(The verifier re-checks Proposition BC1 on \(28\,800\) random triples.)

> **Theorem BC2 (exact vanishing at \(k=16\)).**  Neither inequality of
> Lemma BC can be violated by any class-B instance with \(n=13\).  The same
> exact computation for \(n=3,5,\dots,17\) shows a violation is possible
> exactly for \(n\in\{5,7,9,11\}\), i.e. \(k\in\{8,10,12,14\}\).

*Proof.*  Put \(d^X_c=\#\{a\in X:c\in S_a\}\), \(d^W_c=\#\{a\in W:c\in S_a\}\),
so \(s^X_c=|X|-d^X_c\), \(s^W_c=|W|-d^W_c\).  Every class-B instance and every
disjoint pair satisfies \(\sum_c d^X_c=5|X|\), \(\sum_c d^W_c=5|W|\),
\(d^X_c+d^W_c\le m_c\), \(\max(0,m_c-(n-|X|))\le d^X_c\le\min(m_c,|X|)\) (same
for \(W\)), \(m_c-d^X_c-d^W_c\le n-|X|-|W|\), and \((m_c)_c\) is one of the six
profiles.  Both sides are separable over colours once \((m_c,d^X_c,d^W_c)\) is
fixed, and the only coupling is two linear budgets, so the exact extremum over
the **relaxed** set of integer profiles is a two-dimensional knapsack dynamic
program per \((|X|,|W|,\hbox{profile})\).  It is a relaxation, so a
non-positive margin proves the condition for every class-B instance.  Result
(`conditions.bc_margin`):

| \(n\) | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 |
|---|---|---|---|---|---|---|---|---|
| \(k=n+3\) | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
| worst (BC) margin | \(+0\) | \(+4\) | \(+6\) | \(+8\) | \(+4\) | \(+0\) | \(+0\) | \(+0\) |
| attained at \((|X|,|W|)\) | (1,1) | (2,3) | (2,5) | (4,5) | (5,6) | (1,12) | (1,14) | (1,16) |

Margin \(+0\) means the extremum *equals* \(|X||W|\) — equality, not a
violation; at \(n=13\) it occurs at \(|X|=1\), where both sides are \(12\)
identically. \(\square\)

At the target order the lower inequality also has a short solver-free
check.  If \(Z=A\setminus(X\cup W)\) is nonempty, every colour counted by
\(\rho_c^{\min}\) is forbidden at every vertex of \(Z\), so there are at
most five such colours.  Its support has size at least eight and lies in
\(X\cup W\), hence \(|X|+|W|\ge8\) and \(|X||W|\ge7>5\).  If \(Z\) is empty
and \(\min(|X|,|W|)=1\), exactly the twelve colours available at the
singleton can contribute, giving equality; if both parts have size at least
two, then \(|X||W|\ge22>17\), the total number of colours.  Thus
\(\sum_c\rho_c^{\min}\le|X||W|\) for every target instance independently of
the dynamic program.

> **Corollary BC3.**  Each of the four stored counterexamples violates (BC):
>
> | certificate | violated at | value |
> |---|---|---|
> | `counterexample_n05` | \(X=\{1\},W=\{3\}\) | \(0<1\) |
> | `counterexample_n07` | \(X=\{0\},W=\{2,3,4,5,6\}\) | \(4<5\) |
> | `counterexample_n09` | \(X=\{0\},W=\{4,5,6,7,8\}\) | \(3<5\) |
> | `counterexample_n11` | \(X=\{0..5\},W=\{6..10\}\) | \(26<30\) |

The general \((n,r)\) margins are in `general.py`; the (BC) obstruction
switches off at \(n\ge9\) for \(r=3\) and \(r=4\), at \(n\ge12\) for \(r=5\),
at \(n\ge15\) for \(r=6\), and is still live at \((15,7)\).

## 4. The vertex-Hall threshold

> **Lemma H.**  In \(\Pi(n,r)\) with \(n\ge 2r+1\), for every \(a\in A\) the
> bipartite graph \(H_a\) between \({\cal C}\setminus S_a\) and
> \(A\setminus\{a\}\) (join \(c\) to \(b\) iff \(b\in V_c\)) has a perfect
> matching: the colours at \(a\) can always be matched to distinct partners.

*Proof.*  Both sides have \(n-1\) vertices, so Hall's condition on the colour
side suffices.  Suppose \(D\subseteq{\cal C}\setminus S_a\) has
\(|N(D)|=w<|D|=d\), \(N(D)=\bigcup_{c\in D}(V_c\setminus\{a\})\).  Every
\(c\in D\) has \(a\in V_c\subseteq\{a\}\cup N(D)\), so \(n-r\le|V_c|\le w+1\),
giving \(w\ge n-r-1\) and \(d\ge w+1\ge n-r\).  Also \(d\le n-1\), so
\(w\le n-2\) and \(Y:=A\setminus(\{a\}\cup N(D))\ne\emptyset\).  Every
\(c\in D\) has \(V_c\cap Y=\emptyset\), i.e. every vertex of \(Y\) forbids
every colour of \(D\); counting slots inside \(Y\) gives \(d|Y|\le r|Y|\), so
\(d\le r\), whence \(n-r\le r\). \(\square\)

For \(r=5\) this gives \(n\ge11\), so the \(n=11\) counterexample must use — and
does use — a genuinely bipartite (BC) violation with \(|X|=6\).

## 5. (BP): the parity refinement, and why it dies at \(n\ge2r+2\)

By the converse remark after Lemma BC, colour \(c\) contributes to
\(\sum_c\rho_c=|X||W|\) an arbitrary integer of
\([\rho^{\min}_c,\rho^{\max}_c]\) when \(z_c\ge1\), but only values congruent
to \(s^X_c\pmod2\) when \(z_c=0\).  Call \(c\) *parity-pinned* (for the pair
\(X,W\)) if \(z_c=0\) or \(\min(s^X_c,s^W_c)=0\).

> **Lemma BP.**  If every colour is parity-pinned then
> \[
>  |X|\,|W|\;\equiv\;\sum_{c:\,z_c=0}s^X_c \pmod 2 .
> \]

*Proof.*  A colour with \(\min(s^X_c,s^W_c)=0\) has \(\rho_c=0\); a colour with
\(z_c=0\) has \(\rho_c\equiv s^X_c\).  Sum. \(\square\)

Lemma BP is **not** implied by Lemma BC: it constrains a residue, not a range.
Section 6 exhibits instances that satisfy every (BC) inequality (indeed for
which (BC) provably cannot fire at all) and violate (BP).

> **Theorem BP2.**  In \(\Pi(n,r)\) with \(n\ge2r+2\), Lemma BP never yields a
> contradiction.  In particular it never fires at \((n,r)=(13,5)\).

*Proof.*  Let \(Z=A\setminus(X\cup W)\).
*Case \(Z=\emptyset\).*  Every \(z_c=0\), so the hypothesis of Lemma BP holds,
and \(\sum_c s^X_c=(n-1)|X|\) while \(|X||W|=|X|(n-|X|)\); their difference is
\(|X|(|X|-1)\), always even.  No contradiction.
*Case \(Z\ne\emptyset\).*  Partition the parity-pinned colours as
\({\cal A}=\{c:V_c\cap Z=\emptyset\}\), \({\cal B}=\{c:V_c\cap X=\emptyset\}\),
\({\cal C}_0=\{c:V_c\cap W=\emptyset\}\).  A colour in \({\cal A}\) is
forbidden by *every* vertex of \(Z\); fixing one \(a\in Z\), all such colours
lie in \(S_a\), so \(|{\cal A}|\le r\).  Likewise \(|{\cal B}|\le r\) (using a
vertex of \(X\)) and \(|{\cal C}_0|\le r\).  Hence at most \(3r\) colours are
parity-pinned.  There are \(q=n+r-1\) colours, and \(n\ge2r+2\) gives
\(q\ge3r+1>3r\), so some colour is not parity-pinned: it has \(z_c\ge1\) and
\(\min(s^X_c,s^W_c)\ge1\), hence \(\rho^{\max}_c\ge1>0=\rho^{\min}_c\) and it
contributes a full interval of integers.  The achievable set of
\(\sum_c\rho_c\) is then an interval, and Lemma BP imposes nothing beyond
Lemma BC. \(\square\)

Note \(q\le3r\iff n\le2r+1\); this is exactly the range in which the parity
obstruction can exist, and it is sharp — Section 6 realises it at \(n=2r+1\).

## 6. (BC) is not sufficient; nor is the natural fractional relaxation

### 6.1 The \(\Pi(9,4)\) parity counterexample

Take \(A=X_1\dot\cup X_2\dot\cup X_3\) with \(|X_i|=3\), and \(12\) colours in
three blocks \(\Gamma_{12},\Gamma_{13},\Gamma_{23}\) of four, with
\(V_c=X_i\cup X_j\) for \(c\in\Gamma_{ij}\).  Then \(|S_a|=4=r\), \(m_c=3\le r\),
\(|V_c|=6\) even, \(q=12=n+r-1\): a legitimate \(\Pi(9,4)\) instance, stored as
`certificates/n09r04_parity.json` with `forb = [15,15,15,240,240,240,3840,3840,3840]`.

Apply Lemma BP with \(X=X_1\), \(W=X_2\).  Colours of \(\Gamma_{12}\) have
\(z_c=0\) and \(s^X_c=3\); colours of \(\Gamma_{13}\) have \(s^W_c=0\) and those
of \(\Gamma_{23}\) have \(s^X_c=0\).  Every colour is parity-pinned and
\(\sum_{z_c=0}s^X_c=4\cdot3=12\) is even, while \(|X||W|=9\) is odd.  **No
completion exists.**

Two things make this instance sharp.

* At \((n,r)=(9,4)\) the exact dynamic program of Theorem BC2 gives worst (BC)
  margins \(+0\) and \(+0\): **(BC) provably cannot fire at \(\Pi(9,4)\)**.  So
  (BC) is not sufficient, in a regime where (BC) is vacuous.
* Its fractional relaxation is feasible with a **strict interior point**:
  \(\varphi^*=1/8>0\) (definition in Section 6.3), and an exact rational
  feasible point is stored and re-checked.  So the obstruction is purely
  integral and **invisible to the fractional relaxation (LP)**.  This does
  not rule out stronger linear formulations or an exact integer-hull
  description.

An exhaustive enumeration of \(\Pi(9,4)\) (Section 7) shows this is the
**only** non-completable instance of \(\Pi(9,4)\) up to relabelling.

### 6.2 An infinite family, and what does *not* govern the phenomenon

Generalise: let \(s\) be odd, \(|X_i|=s\) for \(i=1,2,3\), \(n=3s\), and let
each of the three colour blocks have \(r\) colours with \(V_c=X_i\cup X_j\).
Then \(|S_a|=r\), \(m_c=s\le r\), \(|V_c|=2s\), and \(q=3r=n+r-1\) forces
\(r=\frac{3s-1}2\).  Lemma BP with \(X=X_1,W=X_2\) gives
\(s^2\equiv rs\pmod 2\), violated exactly when \(r\) is even, i.e. when
\(s\equiv3\pmod4\).

> **Proposition F.**  For every \(s\equiv3\pmod4\) the instance above is a
> \(\Pi\bigl(3s,\tfrac{3s-1}2\bigr)\) instance with no completion.  Its minimum
> support is \(\mu=n-r=\frac{3s+1}2\), which is unbounded.

\(s=3\) is the \(\Pi(9,4)\) instance; \(s=7\) gives \(\Pi(21,10)\) with
\(\mu=11\); \(s=11\) gives \(\Pi(33,16)\) with \(\mu=17\).  (The verifier
re-derives all three from the definitions and re-checks the parity violation;
the parity argument is a proof, so no solver is needed.)

**Consequence.**  The intuition that a large minimum support \(\mu=n-r\)
should force completability is **false**.  What kills the parity obstruction is
\(q>3r\), i.e. \(n\ge2r+2\); at \(\Pi(13,5)\) we have \(q=17>15=3r\), with slack
\(2\).

### 6.3 The fractional relaxation, and its insufficiency at \(r=5\) too

\[
 x_{e,c}\ge0\ (e\subseteq V_c),\quad
 \sum_c x_{e,c}=1\ (e\in E(K_A)),\quad
 \sum_b x_{ab,c}=1\ (c\in{\cal C},a\in V_c).
\tag{LP}
\]
Every completion is a \(0/1\) feasible point, so infeasibility of (LP) is a
rigorous proof of non-completability, certified by a Farkas vector.  Define
\(\varphi^*=\max\{\rho: Ax=b,\ x_j\ge\rho\ \forall j\}\) (a single LP after the
substitution \(x=z+\rho\mathbf 1\)); \(\varphi^*<0\) certifies infeasibility.

Certificates stored in `certificates/` and re-checked from the definitions:

| certificate | \((n,r)\) | (BC) | (BP) | (LP) | completion |
|---|---|---|---|---|---|
| `n09r04_parity.json` | (9,4) | cannot fire (Thm BC2) | **violated** | feasible, \(\varphi^*=1/8\) | none |
| `n07_BCclean_LPinfeasible.json` | (7,5) | clean | clean | infeasible (exact Farkas) | none |
| `n07_BCclean_LPfeasible.json` | (7,5) | clean | clean | feasible, \(\varphi^*=0\) | none |
| `n09_BCclean.json` | (9,5) | clean | clean | infeasible (exact Farkas) | none |

Measured \(\varphi^*\): \(-1\) for `counterexample_n07` and
`counterexample_n09`; \(-1/15\) for `counterexample_n11`; \(-1/4\) for the
earlier note's `cut_insufficient_n07`; and \(0.0909\ldots0.1000\) for \(40\)
random class-B instances at \(n=13\).

## 7. Exhaustive enumerations

An instance of \(\Pi(n,r)\) *is* its \(n\times q\) incidence matrix (row sums
\(r\), column sums in \(\{r,r-2,\dots\}\)), so enumerating the matrices up to
\(S_n\times S_q\) enumerates the whole class.  We generate the columns
\(v_1,\dots,v_q\) (each read top to bottom as a binary number, row \(0\) the
most significant bit) subject to

* **(C)** \(v_1\ge v_2\ge\cdots\ge v_q\);
* **(R)** inside every maximal block of rows agreeing on columns \(1..j-1\),
  the rows with a \(1\) in column \(j\) precede those with a \(0\).

> **Lemma G (completeness).**  Every \(0/1\) matrix is
> \(S_n\times S_q\)-equivalent to one satisfying (C) and (R).

*Proof.*  In the orbit take the matrix whose column-by-column reading (a binary
string) is lexicographically maximal.  If \(v_j<v_{j+1}\), swapping columns
\(j,j+1\) increases the string, so (C) holds.  If rows \(i<i'\) agree on
columns \(1..j-1\) but \(M_{ij}=0\), \(M_{i'j}=1\), transposing them leaves
columns \(1..j-1\) unchanged and raises position \((i,j)\), increasing the
string; so (R) holds. \(\square\)

The scheme may output several representatives per orbit; only completeness
matters.  The implementation is unit-tested in the verifier against brute
force on two small analogues (\(4\times6\), row sums 3, column sizes
\(\{1,3\}\): \(5120\) labelled matrices, \(3\) orbits, all generated;
\(5\times5\), row sums 3, column size \(3\): \(2040\) labelled matrices,
\(2\) orbits, all generated).

Results (`exh.c`; every representative decided by the complete depth-first
search):

| \(\Pi(n,r)\) | \(\mu\) | (BC) can fire? | representatives | no completion |
|---|---|---|---|---|
| \((5,5)\) | 0 | yes | 248 | 185 |
| \((7,3)\) | 4 | yes | 1 535 | 2 |
| \((7,5)\) | 2 | yes | 2 531 207 | 454 148 |
| \((9,3)\) | 6 | **no** | 103 830 | **0** |
| \((9,4)\) | 5 | **no** | 2 448 157 | **1** |
| \((11,3)\) | 8 | **no** | 10 212 660 | **0** |
| \((13,3)\) | 10 | **no** | \(\ge\)42 000 000 (run not finished) | **0** so far |

So \(\Pi(9,3)\) is a parameter pair where (BC) provably cannot fire and every
instance completes; \(\Pi(9,4)\) is one where (BC) provably cannot fire and
exactly one instance (up to relabelling) fails, by parity.

### The size-five twin family at \(n=13\)

Call \(a,b\) *twins* if \(S_a=S_b\).  A class-B instance at \(n=13\) has a twin
class of size five **iff** five colours share one support of size eight: if
\(Y=\{a_1..a_5\}\) all have \(S_{a_i}=R\), every \(c\in R\) has \(m_c\ge5\),
hence \(m_c=5\) and \(V_c=X:=A\setminus Y\) with \(|X|=8\); conversely five
colours with a common \(8\)-support are forbidden by all five vertices outside
it, which have five slots each.  This is exactly the shape of the \(k=12\)
counterexample and of the \(X/Y\) split of the \(k=14\) family.  Such an
instance is determined by the \(8\times12\) incidence matrix of the remaining
twelve colours against \(X\) (row sums \(5\), column sums in \(\{1,3,5\}\)),
and the same scheme enumerates those.

> **Theorem T (partial).**  At least \(45\,000\,000\) representatives of the
> size-five twin family at \(n=13\) have been enumerated and decided, and every
> one of them has a completion.  **The enumeration had not terminated when this
> note was written**, so this is not yet a theorem about the whole family; the
> exact running totals are in `RUN_LOG.txt`.

The intended statement is that the whole family completes; what is *proved* at
the time of writing is only the partial count above.  Nothing elsewhere in this
note depends on Theorem T.

## 8. (PART): the amalgamation condition

Both (BC) and (BP) are the two-part case of a single condition.  Given a
partition \({\cal P}=\{P_1,\dots,P_k\}\) of \(A\), amalgamate each part to one
vertex.  If the \(M_c\) exist then for each colour there are integers
\(\rho_{ij}(c)\ge0\) (the number of \(M_c\)-edges between \(P_i\) and \(P_j\))
with \(\sum_{j\ne i}\rho_{ij}(c)\le v_i:=|V_c\cap P_i|\) and
\(v_i-\sum_j\rho_{ij}(c)\) even, such that
\(\sum_c\rho_{ij}(c)=|P_i||P_j|\) for all \(i<j\).  (The edge counts inside the
parts then come out as \(\binom{|P_i|}2\) automatically.)  Call this **(PART)**.

* \(k=2\) with \(P_2=A\setminus X\) is Lemma BC together with Lemma BP.
* (PART) with the three groups already refutes the \(\Pi(9,4)\) instance
  (verified).
* (PART) is **not** sufficient either.  An exhaustive check over *all* set
  partitions into \(k=2,3,4\) parts shows that the certificate
  `n07_BCclean_LPfeasible.json` satisfies every one of them, while having no
  completion.  (The same check finds that `n07_BCclean_LPinfeasible.json`
  *does* violate (PART) at \(k=3\), e.g. for
  \(\{\{0,2\},\{1,4\},\{3,5,6\}\}\), and at \(k=4\); and that
  `n09_BCclean.json` satisfies (PART) for \(k=2,3\).)  So (PART) strictly
  refines (BC)+(BP) but still does not capture everything.
* At \(n=13\): a randomised sweep over (instance, 3-partition) pairs found no
  violation; totals in `RUN_LOG.txt`.  This is evidence, not a theorem — no
  dynamic-programming bound for the *ranges* at \(k\ge3\) is proved here.

The **parity layer** of (PART) at \(k=3\), however, does vanish provably.

> **Theorem BP3.**  Let \({\cal P}=\{P_1,P_2,P_3\}\) be a partition of \(A\)
> in \(\Pi(n,r)\) with \(n\) odd and \(n\ge2r+2\).  Then the congruence
> conditions implied by (PART) modulo \(2\) are always satisfiable; in
> particular they never fire at \((13,5)\).

*Proof.*  Write \(v_i=|V_c\cap P_i|\).  Over \(\mathbb F_2\) the conditions
\(\rho_{12}+\rho_{13}=v_1\), \(\rho_{12}+\rho_{23}=v_2\),
\(\rho_{13}+\rho_{23}=v_3\) are consistent (\(v_1+v_2+v_3=|V_c|\) is even) and
their solution set is \(\{(t,v_1+t,v_2+t):t\in\mathbb F_2\}\).  Hence
\(\sum_c\rho_{12}\equiv T:=\sum_ct_c\),
\(\sum_c\rho_{13}\equiv\sum_cv_1^{(c)}+T\) and
\(\sum_c\rho_{23}\equiv\sum_cv_2^{(c)}+T\), while
\(\sum_cv_i^{(c)}=(n-1)|P_i|\) is even.  So (PART) mod \(2\) says exactly
\[|P_1||P_2|\equiv|P_1||P_3|\equiv|P_2||P_3|\equiv T \pmod 2 .\]
The three left-hand sides always agree: \(|P_1|+|P_2|+|P_3|=n\) is odd, so
either all three parts are odd (all products odd) or exactly one is odd (all
products even).  It remains to see that \(T\) can take either value.  Both
values of \(t_c\) are available for a colour unless some \(v_i=0\), i.e.
unless every vertex of \(P_i\) forbids \(c\); fixing one vertex of \(P_i\)
shows at most \(r\) colours are pinned by each \(i\), so at most \(3r\)
colours in all.  Since \(q=n+r-1\ge3r+1\), some colour is free, and flipping
its \(t_c\) changes \(T\). \(\square\)

## 9. Where the Question sits in the literature

The class-B\('\) form of the Question is: *given five complete rows of a
would-be unipotent symmetric Latin square of order \(18\), must it complete?*
(A unipotent symmetric Latin square of order \(2m\) is a one-factorization of
\(K_{2m}\).)  The following were obtained and read directly from A. Bahmanian
and A. J. W. Hilton, *Ryser's Theorem for Symmetric \(\rho\)-latin Squares*,
arXiv:2209.06401v2 (14 Sep 2025; accepted by *Combinatorial Theory*, July
2025), and are quoted as printed there.

* **Question 1.1** of that paper is the general problem: *"Let
  \(n>\min\{r,s\}\).  Find necessary and sufficient conditions that ensure that
  a symmetric \(r\times s\) \(\rho\)-latin rectangle \(L\) can be extended to a
  symmetric \(n\times n\) \(\rho\)-latin square \(L'\)."*  The paper states that
  *"even the case \(\rho=(n,\dots,n)\) … is far from being settled."*
* **Theorem 1.2 [Cruse 1974]**: *an \(r\times r\) symmetric latin rectangle
  \(L\) on \([n]\) can be extended to an \(n\times n\) symmetric latin square
  if and only if (i) \(e_\ell\ge2r-n\) for \(\ell\in[n]\); (ii)
  \(|\{\ell\in[n]\mid e_\ell\equiv n\ (\mathrm{mod}\ 2)\}|\ge r\).*
* **Theorem 1.3 [Andersen 1982; Hoffman 1983]**: the same with a prescribed
  diagonal tail.
* **Theorem 1.4** (that paper's main result): the \(r\times r\) symmetric
  \(\rho\)-latin case with a prescribed diagonal tail.
* The paper records that *"Bryant and Rodger [BR04] solved the case
  \(r\in\{1,2\},\ s=n,\ \rho=(n,\dots,n)\)"* of Question 1.1.

Two consequences, used only as stated.

1. **The case needed here — \(r=5\), \(s=n=18\), unipotent — is open.**  All
   the theorems above assume the *known* part is the principal \(r\times r\)
   block; here the known part is five full rows and the *unknown* part is the
   principal \(13\times13\) block.  Bryant–Rodger cover the \(r\times n\) shape
   only for \(r\in\{1,2\}\).  (The Bryant–Rodger paper itself was not obtained;
   the description of what it proves is the one printed in Bahmanian–Hilton and
   in the journal abstract, and nothing beyond that is used.)
2. **Why amalgamation/detachment does not transfer.**  The proofs of
   Theorems 1.2–1.4 amalgamate the \(n-r\) unknown rows into a single vertex
   and detach it; that is legitimate because the coloured part lies wholly
   inside the \(r\) known rows.  Here the coloured part consists of the edges
   *between* the five known vertices and the hole, so amalgamating the hole
   forgets which vertex of \(A\) each coloured edge attaches to — exactly the
   data the Question prescribes.  Amalgamating the five known vertices instead
   is legitimate but vacuous.  This is a statement about the method, not a
   proof that no detachment argument can work.

Independently of Problem \#835: the four stored counterexamples are five-row
instances of orders \(10,12,14,16\) satisfying every Cruse/Andersen–Hoffman
type condition and failing to complete, so for \(r=5\), \(s=n\) those
conditions are not sufficient.  Proposition F gives further such instances at
arbitrarily large order.

## 10. Search evidence and its calibration

All searches are drivers.  Every reported non-completion was re-decided by two
independent complete solvers (a C depth-first search and, in Python, a second
depth-first search and/or a CDCL SAT solver); node budgets steer the search and
are never used as evidence.  Exact totals are in `RUN_LOG.txt`.

**Calibration.**  Simulated annealing on the greedy-failure objective finds
counterexamples in bulk at \((9,5)\) and \((11,7)\) and none at \((11,5)\),
where they provably exist; annealing on the (LP) margin \(\varphi^*\) finds
(LP)-infeasible instances at \((9,5)\) **and at \((11,5)\)**.  So the (LP)
objective is calibrated at \(n=11\) and the greedy objective is not.

At \((13,5)\) neither objective produced a counterexample, and the (LP)
annealer drove \(\varphi^*\) only from \(\approx0.09\) (random) down to
\(\approx0.072\), never below \(0\).  **This is evidence, not a theorem.**  The
only unconditional statements about \((13,5)\) here are Theorems BC2, BP2,
BP3 and Lemma H.

## 11. The exact remaining question

> **Open.**  Does every class-B instance at \(n=13\), \(q=17\) complete?  And,
> separately and weakly, does every class-B\('\) instance complete — i.e. does
> every proper \(17\)-edge-colouring of \(K_{18}-E(K_{13})\) saturating the
> five vertices outside the hole extend to a one-factorization of \(K_{18}\)?

Removed at \(n=13\): every counting obstruction of type (BC), including both
cut inequalities and vertex Hall (Theorem BC2, Lemma H); the parity
obstruction (BP), both in its two-part form (Theorem BP2) and in the mod-2
layer of the three-part form (Theorem BP3).

Still live at smaller parameters, and therefore what a proof at \((13,5)\)
must handle:

* instances that are (BC)-clean and (BP)-clean and fail for a reason visible
  only to the fractional relaxation — these exist at \((7,5)\) and \((9,5)\);
* instances that fail with a *strictly feasible* fractional relaxation —
  these exist at \((7,5)\), where the failure survives every partition
  condition (PART) with \(k\le4\) as well, and, in the cleanest possible
  form, at \((9,4)\), where the failure is pure parity.

In other words no single one of {cuts, (BC), (BP), (PART), (LP)} is
sufficient, and the last of the five is not even implied by the other four.

Concrete next steps, in order of expected payoff:

1. Prove or refute a dynamic-programming bound for the *range* layer of (PART)
   with \(k=3,4\) at \((13,5)\), in the style of Theorem BC2 (the mod-2 layer
   is already settled by Theorem BP3).  A single violation at \((13,5)\) would
   refute the Question with an exactly checkable certificate.  Note (PART) is
   necessary but not sufficient — `n07_BCclean_LPfeasible.json` satisfies every
   partition condition for \(k\le4\) and still fails — so a proof that (PART)
   never fires at \((13,5)\) would not close the Question.
2. Decide whether (LP) is always feasible in class B at \(n=13\).  A proof
   would strengthen Theorem BC2; a single (LP)-infeasible instance would refute
   the Question.  Measured \(\varphi^*\) sits in a narrow band around \(1/11\).
3. Push the exhaustive method of Section 7 to \(\Pi(11,4)\), \(\Pi(12,5)\) (the
   one-vertex peel of \(\Pi(13,5)\), where (BC) also provably cannot fire), or
   to the twin-class-four family at \(n=13\).

For reference, peeling one vertex is exact:

> **Proposition P.**  Fix \(a_0\in A\) and an SDR
> \(\sigma:{\cal C}\setminus S_{a_0}\to A\setminus\{a_0\}\) with
> \(\sigma(c)\in V_c\) (one exists by Lemma H when \(n\ge2r+1\)).  With
> \(A'=A\setminus\{a_0\}\) and \(S'_b=S_b\cup\{\sigma^{-1}(b)\}\),
> \((A',{\cal C},S')\) is an instance of \(\Pi(n-1,r+1)\) whose completions are
> exactly the completions of the original in which the \(c\)-edge at \(a_0\) is
> \(a_0\sigma(c)\).

*Proof.*  \(|S'_b|=r+1\) since each \(b\) is \(\sigma(c)\) for exactly one
\(c\); the colour count is \(q=n+r-1=(n-1)+(r+1)-1\); for \(c\notin S_{a_0}\),
\(m'_c=m_c+1\le r+1\) and \(|V'_c|=n-2-m_c\) is even, and for \(c\in S_{a_0}\),
\(m'_c=m_c-1\) and \(|V'_c|=n-m_c\) is even. \(\square\)

So \(\Pi(13,5)\to\Pi(12,6)\to\Pi(11,7)\to\cdots\): peeling keeps \(q\) fixed
and lowers \(\mu\) by \(2\).  Note \(\Pi(11,7)\) *does* have counterexamples
(found by search), so a bad choice of \(\sigma\) can be fatal; the peel is not
by itself a proof strategy.

## 12. Verification

```sh
cd collaboration/opus5/first_lift_classB_attack && python3 -B verify_classB.py
```

Deterministic.  All exact-arithmetic checks use only the standard library
(`fractions.Fraction`); `scipy` and `python-sat`, when present, are used only
for additional independent cross-checks and never carry a claim alone.  In
order it

1. re-derives the class-B arithmetic at \(n=13\) and for general \(n\);
2. re-checks Proposition BC1 on \(28\,800\) random triples;
3. checks on \(1200\) instances at \(n=5,7,9\) that no completable instance
   violates (BC), and that the (UNSAT, (BC)-clean) cells are non-empty;
4. recomputes every (BC) margin of Theorem BC2 for \(n=3,\dots,17\), asserts the
   fire-set is exactly \(\{5,7,9,11\}\), and checks on \(480\) actual
   (instance, \(X\), \(W\)) triples at \(n=13\) that the dynamic-programming
   optimum really is a lower bound for \(\sum_c\rho^{\max}_c\) (a soundness
   control on the relaxation used in the proof);
5. re-runs the relaxation behind Lemma H and controls it on \(600\) random
   instances at \(n=11,13\);
6. re-verifies the four stored counterexamples: class-B arithmetic, the
   class-B\('\) witness rebuilt as an explicit proper colouring of
   \(K_{n+5}-E(K_n)\) saturating the five outside vertices, exhaustive UNSAT by
   two independent complete solvers, and an explicit (BC) certificate;
7. re-checks the new certificates, including exact rational Farkas vectors and
   exact rational (LP) points;
8. cross-validates the solvers on \(500\) instances at \(n=7\) against an
   independent fixed-order brute force;
9. unit-tests the completeness of the Section-7 generation scheme against brute
   force on two small analogues, and re-runs an independent python
   implementation of it on the complete pairs \(\Pi(5,5)\) and \(\Pi(7,3)\),
   reproducing `exh.c`'s counts (\(248\)/\(185\) and \(1535\)/\(2\)) exactly;
10. re-decides in Python a stored slice of the Section-7 exhaustive run at
    \(n=13\) and re-checks every completion from the definition;
11. re-checks Lemma BP and Theorem BP2 (including an exhaustive check, over all
    \(9\,418\,500\) pairs \((X,W)\) with non-empty rest on six random \(n=13\)
    instances, that some colour always has unconstrained parity), the
    \(\Pi(9,4)\) certificate, and the family of Proposition F for
    \(s=3,7,11\);
12. re-checks (PART) on the \(\Pi(9,4)\) instance, on completable \(n=13\)
    instances, the mod-2 layer of Theorem BP3 on \(157\) 3-partitions at
    \(n=13\), and the insufficiency of (PART) by scanning all \(714\) partitions
    into \(2,3,4\) parts of the purely-integral \(n=7\) certificate.
