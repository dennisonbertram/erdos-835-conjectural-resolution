# The simultaneous \(13\)-fan shadow at \(k=16\)

## Scope

**Erdős–Rosenfeld Problem #835 remains open.** This note gives a stronger
unrestricted necessary condition for the first open parameter \(k=16\). It
does not construct or refute \(LS(3,4,20)\), does not decide the \(k=16\)
instance, and does not settle the existential problem.

The new point is simultaneous compatibility. A standalone restriction of a
hypothetical \(17\)-colouring gives one \(LS(3,4,20)\). Keeping all thirteen
overlapping restrictions with the same \(19\)-point core forces thirteen
labelled \(LS(3,4,20)\)'s with a common labelled point-link and \(3,876\)
additional all-different constraints. This is a strictly stronger constraint
system than one fixed-link completion, although strict separation at the
existential level is not known because existence of even one
\(LS(3,4,20)\) remains open.

The proof and implementation were independently audited. No
literature-priority claim is made.

## 1. The induced-shadow theorem

Let \(V=U\mathbin{\dot\cup}A\), where \(|U|=19\) and \(|A|=13\). Let
\[
 {\cal X}=
 \left\{S\in\binom V{16}: |S\cap U|\in\{15,16\}\right\}.
\]
Thus
\[
 |{\cal X}|=\binom{19}{16}+13\binom{19}{15}
 =969+13\cdot3,876=51,357.
\]
Write \({\cal C}\) for a labelled palette of seventeen colours.

> **Theorem 1 (simultaneous \(13\)-fan).** Proper labelled
> \(17\)-colourings of the subgraph of \(J(32,16)\) induced by \({\cal X}\)
> are in bijection with the following data:
>
> 1. a labelled \(LS(2,3,19)\) colouring
>    \(L:\binom U3\to{\cal C}\);
> 2. for every \(a\in A\), a labelled \(LS(3,4,20)\) colouring
>    \(F_a:\binom{U\cup\{a\}}4\to{\cal C}\);
> 3. the thirteen systems have the same point-link,
>    \[
>      F_a(\{a\}\cup T)=L(T)
>      \qquad(T\in\binom U3);
>    \]
> 4. for every \(Q\in\binom U4\), the thirteen values
>    \[
>      \{F_a(Q):a\in A\}
>    \]
>    are pairwise distinct.
>
> In fact the thirteen values in (4) are exactly
> \[
> {\cal C}\setminus
> \{L(Q\setminus\{x\}):x\in Q\}. \tag{1}
> \]

### Proof

Let \(c:{\cal X}\to{\cal C}\) be proper. For
\(T\in\binom U3\), \(a\in A\), and
\(Q\in\binom{U\cup\{a\}}4\), define
\[
 L(T)=c(U\setminus T),\qquad
 F_a(Q)=c((U\cup\{a\})\setminus Q). \tag{2}
\]
Complementation within \(U\), respectively within \(U\cup\{a\}\), turns
each relevant Johnson star into a clique of seventeen vertices in the
induced graph. Hence \(L\) is an \(LS(2,3,19)\), each \(F_a\) is an
\(LS(3,4,20)\), and
\[
 F_a(\{a\}\cup T)=c(U\setminus T)=L(T).
\]

Fix \(Q\in\binom U4\). The seventeen extensions of the \(15\)-set
\(U\setminus Q\) are
\[
 (U\setminus Q)\cup\{a\}\quad(a\in A),\qquad
 (U\setminus Q)\cup\{x\}\quad(x\in Q).
\]
They form a \(K_{17}\) in \(J(32,16)\), so their colours are all distinct.
By (2), their colours are respectively \(F_a(Q)\) and
\(L(Q\setminus\{x\})\). This proves (1), and in particular (4).

Conversely, use (2) as the definition of a colouring on \({\cal X}\).
There are exactly four adjacency cases.

* Two vertices \(U\setminus T\) and \(U\setminus T'\) are adjacent exactly
  when \(|T\cap T'|=2\), handled by \(L\).
* Two vertices represented inside the same \(U\cup\{a\}\) are handled by
  \(F_a\).
* A vertex \(U\setminus T\) and a vertex
  \((U\setminus Q)\cup\{a\}\) are adjacent exactly when \(T\subset Q\).
  Their colours differ because they are the colours of the adjacent
  quadruples \(\{a\}\cup T\) and \(Q\) in \(F_a\).
* For \(a\ne b\), the vertices
  \((U\setminus Q)\cup\{a\}\) and
  \((U\setminus R)\cup\{b\}\) are adjacent exactly when \(Q=R\), handled
  by (4).

This list is exhaustive, so the reconstructed colouring is proper. The two
constructions are visibly inverse. \(\square\)

The \(51,357\)-vertex shadow is only about \(0.0085\%\) of the
\(\binom{32}{16}=601,080,390\) vertices of the full graph. It is a stronger
local target, not a replacement for the unrestricted problem.

## 2. The smallest fixed-link formulation

Fix a labelled \(LS(2,3,19)\) colouring \(L\). Define a graph \(H_L\) whose
vertices are the allowed cells
\[
 (Q,c),\qquad Q\in\binom U4,\quad
 c\notin\{L(T):T\in\binom Q3\}. \tag{3}
\]
Join distinct cells when either

* they have the same quadruple \(Q\); or
* they have the same colour \(c\), and their quadruples share a triple.

> **Theorem 2 (fan-colouring equivalence).** The \(13\)-fans of Theorem 1
> having fixed common link \(L\) are in labelled bijection with the proper
> \(13\)-colourings of \(H_L\). The graph colour is the extension label
> \(a\in A\).

### Proof

The four faces of a quadruple have distinct \(L\)-colours, so every
\(Q\)-group in (3) has thirteen cells. Given a fan, colour \((Q,c)\) by the
unique \(a\) for which \(F_a(Q)=c\). The \(Q\)-groups are rainbow by
Theorem 1(4). If \(Q,Q'\) share a triple \(T\), a single \(F_a\) cannot give
both quadruples the same colour, because they lie in the same triple-star.
Thus this is a proper \(13\)-colouring of \(H_L\).

Conversely, a proper \(13\)-colouring uses all thirteen labels on every
\(Q\)-group, defining one value \(F_a(Q)\) for every \(a,Q\). Fix
\(T\in\binom U3\) and \(c\ne L(T)\). Of the sixteen quadruples
\(T\cup\{x\}\), exactly three are forbidden for colour \(c\): one for each
pair of \(T\), by the Steiner property of the colour-\(c\) triple system.
Those three points \(x\) are distinct, since otherwise two colour-\(c\)
faces would share a pair. Hence the thirteen allowed \((T,c)\)-cells form
a \(K_{13}\), so they also use every extension label. For each \(a\), the
sixteen old members of the \(T\)-star therefore use every colour except
\(L(T)\), while \(\{a\}\cup T\) receives \(L(T)\). Stars whose base contains
\(a\) are rainbow because \(L\) is a large set. Thus every \(F_a\) is an
\(LS(3,4,20)\) with link \(L\), and the \(Q\)-groups give the fan condition.
\(\square\)

This is also the conflict graph of the unrestricted fixed-link exact-cover
matrix: a vertex is an allowed row, and adjacency means that two rows claim
the same demand.

## 3. Exact size and the Hoffman delimiter

The graph \(H_L\) has
\[
 3,876\cdot13=\boxed{50,388}
\]
vertices. Its edges are partitioned into the following \(K_{13}\)'s:

* \(3,876\) quadruple groups;
* \(969\cdot16=15,504\) triple-colour demand groups.

There are \(19,380\) groups in total. Every cell belongs to its quadruple
group and its four face-demand groups. These five groups meet pairwise only
in that cell, so
\[
 H_L\text{ is }5(13-1)=\boxed{60}\text{-regular}. \tag{4}
\]

Let \(B\) be the \(19,380\times50,388\) group-versus-cell incidence matrix.
Two distinct cells share one group exactly when they are adjacent, while
every column has squared norm five. Therefore
\[
 A(H_L)=B^\top B-5I. \tag{5}
\]
It follows that the least adjacency eigenvalue is at least \(-5\). Since
\[
 \dim\ker B\ge50,388-19,380=31,008,
\]
\(-5\) is an eigenvalue, so the least eigenvalue is exactly \(-5\), with
multiplicity at least \(31,008\). The Hoffman ratio bound is consequently
\[
 \chi(H_L)\ge 1-\frac{60}{-5}=\boxed{13}. \tag{6}
\]
This is only the already-forced clique lower bound. Thus the ordinary
least-eigenvalue Hoffman bound can never prove \(\chi(H_L)>13\), for any
choice of \(L\).

The conclusion must not be broadened: the full spectrum or its eigenspaces
could still yield a stronger obstruction, \(H_L\) could contain other
cliques, and (5) does not construct a \(13\)-colouring. If a fan exists, its
thirteen classes are Hoffman-tight independent sets of size
\(50,388/13=3,876\), with their centred indicators in \(\ker B\).

## 4. What remains

The new exact finite target is:

> Find a labelled \(LS(2,3,19)\) whose \(50,388\)-vertex graph \(H_L\) is
> \(13\)-colourable, or prove that \(H_L\) is not \(13\)-colourable for every
> labelled \(LS(2,3,19)\).

A positive answer constructs thirteen simultaneously compatible
\(LS(3,4,20)\)'s sharing a point-link, but still only colours the induced
shadow \({\cal X}\). A negative answer for every possible \(L\) would rule
out \(k=16\); a negative answer for one fixed cyclic \(L\) would exclude only
that link.

The basic Hoffman route is now closed. The next honest targets are the
equality structure inside \(\ker B\), exact \(13\)-colouring for strategically
chosen links, and compatibility after enlarging \({\cal X}\) to the next
intersection layer.

## 5. Verification

Run:

```sh
python3 -B \
  collaboration/simultaneous_ls3420_fan/verify_simultaneous_ls3420_fan.py
```

The verifier uses the committed cyclic \(LS(2,3,19)\) only as an executable
control for the parameter-independent counts. It checks all \(50,388\) cells,
all \(19,380\) groups, every group size, every five-group membership, the
degree calculation, the matrix-overlap identity, the induced-shadow edge
census, and the exact Hoffman arithmetic. It does not search for a fan.
