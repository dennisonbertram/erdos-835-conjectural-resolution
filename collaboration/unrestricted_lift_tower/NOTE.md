# The unrestricted layer tower and the first \(K_{13}\)-hole lift

Date: 2026-07-27.

## Scope

This note concerns the first open case \(k=16\) of Erdős--Rosenfeld
Problem #835.  It makes **no cyclic or \(C_{17}\)-equivariance assumption**.

The results below are exact and reversible:

1. a full \(17\)-colouring of \(J(32,16)\) is rewritten as a compatible
   thirteen-level tower over a fixed split \(V=U\mathbin{\dot\cup}A\), with
   \((|U|,|A|)=(19,13)\);
2. the already-proved simultaneous \(13\)-fan is identified as precisely the
   top-proper truncation through level \(1\);
3. the first new compatibility layer, from level \(1\) to level \(2\), is
   reduced for each \(P\in\binom U5\) to completion of a prescribed partial
   one-factorization of \(K_{18}\), whose uncoloured hole is \(K_{13}\);
4. the elementary parity condition for that completion is proved to hold
   identically.

This does **not** construct the required fan, prove that every such partial
one-factorization completes, make the level-\(2\) maps proper across different
five-sets, or settle Problem #835.  The exact remaining gap is stated in
Section 5.

Throughout, \({\cal C}\) is a labelled set of \(17\) colours.

## 1. A reversible tower for the full Johnson colouring

Put \(V=U\mathbin{\dot\cup}A\), where \(|U|=19\) and \(|A|=13\).  Every
\(S\in\binom V{16}\) has a unique representation
\[
 S=(U\setminus Q)\cup B,\qquad
 B=S\cap A,\quad Q=U\setminus S,
\tag{1}
\]
where, on writing \(j=|B|\),
\[
 B\in\binom Aj,\qquad Q\in\binom U{j+3}.
\tag{2}
\]

For maps
\[
 G_B:\binom U{|B|+3}\longrightarrow{\cal C}
 \qquad(B\subseteq A),
\tag{3}
\]
consider the following tower law.  For \(B\in\binom Aj\) and
\(P\in\binom U{j+4}\), the following \(17\) indexed values are all distinct:
\[
 \bigl(G_B(P\setminus\{x\})\bigr)_{x\in P},
 \qquad
 \bigl(G_{B\cup\{a\}}(P)\bigr)_{a\in A\setminus B}.
\tag{4}
\]
There are \((j+4)+(13-j)=17\) of them.  At \(j=13\), the second list is
empty and \(|P|=17\).

> **Theorem 1 (full tower equivalence).**  Proper labelled
> \(17\)-colourings \(c\) of \(J(32,16)\) are in bijection with families
> \((G_B)_{B\subseteq A}\) satisfying (4).  The bijection is
> \[
> G_B(Q)=c((U\setminus Q)\cup B).
> \tag{5}
> \]

### Proof

Every \(15\)-set \(R\subset V\) is contained in exactly \(17\) members of
\(\binom V{16}\), and those extensions form a \(K_{17}\) in \(J(32,16)\).
Write \(B=R\cap A\), \(j=|B|\), and
\[
 P=U\setminus(R\cap U).
\]
Since \(|R\cap U|=15-j\), one has \(|P|=j+4\).  The \(17\) extensions of
\(R\) are exactly
\[
 (U\setminus(P\setminus\{x\}))\cup B
       \quad(x\in P),
\qquad
 (U\setminus P)\cup(B\cup\{a\})
       \quad(a\in A\setminus B).
\tag{6}
\]
Under (5), their colours are precisely the two lists in (4).  Thus a proper
colouring implies every tower law.

Conversely, two distinct \(16\)-sets are adjacent exactly when their
intersection is a \(15\)-set \(R\).  They are then two extensions in the
unique clique (6), and (4) separates their colours.  Formulae (1)--(2) show
that (5) assigns exactly one value to every vertex.  The constructions are
inverse. \(\square\)

## 2. The simultaneous fan is the exact level-\(1\) truncation

At level \(0\), write
\[
 L(T)=G_\varnothing(T)\qquad(T\in\binom U3),
\tag{7}
\]
and at level \(1\), write \(F_a(Q)=G_{\{a\}}(Q)\) for
\(Q\in\binom U4\).  The \(j=0\) instance of (4) is
\[
 \bigl\{L(P\setminus\{x\}):x\in P\bigr\}
 \mathbin{\dot\cup}
 \bigl\{F_a(P):a\in A\bigr\}
 ={\cal C}
 \qquad(P\in\binom U4).
\tag{8}
\]

In addition, for every \(a\in A\), the five values
\[
 F_a(P\setminus\{x\})\qquad(x\in P)
\tag{9}
\]
must be distinct for every \(P\in\binom U5\).  Call (9) **top
properness** at level \(1\).

> **Proposition 2.**  Equations (8)--(9), together with \(L\) being a
> labelled \(LS(2,3,19)\), are equivalent to the simultaneous \(13\)-fan
> data: the maps on \(\binom{U\cup\{a\}}4\) defined by
> \[
> \widehat F_a(Q)=F_a(Q)\quad(Q\in\binom U4),\qquad
> \widehat F_a(\{a\}\cup T)=L(T)
> \tag{10}
> \]
> are labelled \(LS(3,4,20)\)'s with common link \(L\), and their thirteen
> values on every \(Q\in\binom U4\) are pairwise distinct.

### Proof

Equation (8) is exactly the cross-\(a\) all-different condition and says
that every \(F_a(Q)\) avoids all four link-face colours of \(Q\).  If two
quadruples \(Q,Q'\subset U\) share a triple, then \(Q\cup Q'\) is a
five-set, so (9) separates \(F_a(Q)\) and \(F_a(Q')\).  Hence the sixteen
quadruples in \(U\) through a triple \(T\) have distinct \(F_a\)-colours;
by (8), all avoid \(L(T)\).  Together with \(\{a\}\cup T\), they give the
seventeen colours.  A triple containing \(a\) gives a rainbow star directly
from the \(LS(2,3,19)\) property of \(L\).  Thus (10) is an
\(LS(3,4,20)\).  The converse is immediate from its triple-star
all-different property and the simultaneous-fan law. \(\square\)

Thus the fan colours the levels \(|B|=0,1\) and already supplies the
top-properness needed before attempting level \(2\).

## 3. First lift: a prescribed-leave edge-colouring of \(K_{13}\)

Assume a simultaneous fan, and fix \(P\in\binom U5\).  For \(a\in A\), put
\[
 S_a(P)=\{F_a(P\setminus\{x\}):x\in P\}.
\tag{11}
\]
Top properness gives \(|S_a(P)|=5\).

The \(j=1\) tower law asks for values
\[
 G_{\{a,b\}}(P)\qquad(\{a,b\}\in\binom A2)
\tag{12}
\]
such that, at every \(a\),
\[
 S_a(P)\mathbin{\dot\cup}
 \{G_{\{a,b\}}(P):b\in A\setminus\{a\}\}
 ={\cal C}.
\tag{13}
\]

> **Theorem 3 (the \(K_{13}\)-hole equivalence).**  For a fixed five-set
> \(P\), choices (12) satisfying all equations (13) are equivalent to each
> of the following.
>
> 1. A proper edge-colouring \(h_P:E(K_A)\to{\cal C}\) in which the colours
>    missing at vertex \(a\) are exactly \(S_a(P)\), via
>    \(h_P(ab)=G_{\{a,b\}}(P)\).
> 2. For every \(c\in{\cal C}\), a perfect matching \(M_c(P)\) on
>    \[
>    V_c(P)=\{a\in A:c\notin S_a(P)\},
>    \tag{14}
>    \]
>    such that the seventeen matchings partition \(E(K_A)\).
> 3. A completion to a one-factorization of \(K_{P\mathbin{\dot\cup}A}
>    \cong K_{18}\) of the partial edge-colouring \(\phi_P\) defined on
>    every edge outside the hole \(K_A\) by
>    \[
>    \phi_P(xa)=F_a(P\setminus\{x\})
>       \quad(x\in P,\ a\in A),
>    \tag{15}
>    \]
>    \[
>    \phi_P(xy)=L(P\setminus\{x,y\})
>       \quad(\{x,y\}\in\binom P2).
>    \tag{16}
>    \]

### Proof

Equations (13) say exactly that the twelve edges incident with \(a\) receive
the twelve colours in \({\cal C}\setminus S_a(P)\), once each.  This proves
the equivalence with (1).  In a proper edge-colouring, the \(c\)-class is a
matching and covers exactly the vertices at which \(c\) is not missing.
This proves (1) \(\Leftrightarrow\) (2); the edge count then makes
"partition" equivalent to using each edge once.

It remains to check that (15)--(16) are a proper partial edge-colouring.
At \(a\), the five colours in (15) are distinct by (9).  Fix \(x\in P\)
and put \(Q=P\setminus\{x\}\).  By (8), the thirteen cross-edges \(xa\)
use exactly the complement of the four colours
\[
 \{L(Q\setminus\{y\}):y\in Q\}.
\]
Those four colours are exactly the colours of the internal edges \(xy\)
from (16), and they are distinct because \(L\) is proper.  Thus every
vertex \(x\in P\) is already incident with every colour exactly once.

The only uncoloured edges are those of \(K_A\).  Adding a colouring from
(1) makes every vertex \(a\) incident with all seventeen colours, while
vertices in \(P\) were already saturated.  Consequently every colour class
is a perfect matching of the eighteen vertices, and the result is a
one-factorization.  Restricting any such completion back to \(K_A\) reverses
the construction. \(\square\)

The problems for different \(P\)'s are independent at the level of equations
(13).  They cease to be independent when top properness at level \(2\) is
imposed: for every \(\{a,b\}\in\binom A2\) and
\(R\in\binom U6\), the six values
\[
 G_{\{a,b\}}(R\setminus\{x\})\qquad(x\in R)
\tag{17}
\]
must be pairwise distinct.

## 4. The first parity obstruction vanishes identically

For \(c\in{\cal C}\), define
\[
 t_c(P)=
 \#\{T\in\binom P3:L(T)=c\},
\qquad
 m_c(P)=\#\{a\in A:c\in S_a(P)\}.
\tag{18}
\]

> **Theorem 4 (automatic parity and exact support sizes).**
> For every \(P\in\binom U5\) and \(c\in{\cal C}\),
> \[
> m_c(P)=5-2t_c(P),\qquad
> |V_c(P)|=8+2t_c(P)\in\{8,10,12\}.
> \tag{19}
> \]
> In particular every support \(V_c(P)\) has even size, so the elementary
> parity condition for the perfect matching \(M_c(P)\) is automatic and
> cannot obstruct the first lift.

### Proof

For a four-set \(Q\subset P\), equation (8) says that the colour \(c\)
occurs exactly once among \(\{F_a(Q):a\in A\}\) if no triple face of \(Q\)
has \(L\)-colour \(c\), and zero times otherwise.  Summing this statement
over the five four-subsets \(Q\) of \(P\) gives \(m_c(P)\), because the five
entries in each column \(a\) are distinct.

Each \(c\)-coloured triple \(T\subset P\) lies in exactly two four-subsets
of \(P\).  No four-set contains two \(c\)-coloured triples, since two of its
triple faces share a pair and \(L\) separates triples sharing a pair.
Therefore exactly \(2t_c(P)\) of the five four-sets have a \(c\)-coloured
face.  This proves \(m_c(P)=5-2t_c(P)\), and (14) gives
\[
 |V_c(P)|=13-m_c(P)=8+2t_c(P).
\]

Finally, \(c\)-coloured triples form a pair-packing.  Three triples inside a
five-set would meet pairwise in exactly one point; inclusion--exclusion would
give their union size at least \(9-3=6\), impossible.  Hence
\(t_c(P)\le2\), proving the displayed range. \(\square\)

There is also a direct one-factorization interpretation.  In \(\phi_P\),
colour \(c\) appears on the \(t_c(P)\) internal edges complementary in \(P\)
to the \(c\)-coloured triples, and on the \(m_c(P)\) cross-edges.  These
form a matching with
\[
 t_c(P)+m_c(P)=5-t_c(P)
\]
edges, leaving precisely \(8+2t_c(P)\) unmatched vertices, all in \(A\).

## 5. Exact remaining compatibility problem

A simultaneous \(13\)-fan lifts to a proper colouring of all vertices with
\(|S\cap A|\le2\) if and only if there are choices \(G_{\{a,b\}}(P)\) such
that:

1. for every \(P\in\binom U5\), the partial one-factorization
   \(\phi_P\) of Theorem 3 completes across its \(K_{13}\) hole; and
2. the completions can be chosen jointly so that (17) holds for every
   \(\{a,b\}\) and every six-set \(R\).

Condition 1 is a finite prescribed-leave matching decomposition.  Theorem 4
proves that its most immediate parity test is always passed.  Condition 2 is
the first coupling across different five-sets.  Repeating the same mechanism
at higher \(j\) gives Theorem 1's full tower, terminating at \(j=13\).

Thus a positive fan is not yet a colouring of \(J(32,16)\), but the missing
bridge is now explicit: first complete \(\binom{19}{5}=11,628\) linked
\(K_{13}\)-hole one-factorization problems, then satisfy their
\(\binom{13}{2}\binom{19}{6}\) top-properness constraints.

## 6. Verification

Run:

```sh
python3 -B \
  collaboration/unrestricted_lift_tower/verify_unrestricted_lift_tower.py
```

The verifier is deterministic and standard-library-only.  It:

* checks the tower indexing and the unique \(17\)-star representation of
  every adjacency in a complete \(k=6\) control;
* reconstructs the committed cyclic \(LS(2,3,19)\) solely as an executable
  control and checks (19) for all \(11,628\cdot17\) pairs \((P,c)\);
* builds the round-robin one-factorization of \(K_{18}\), restricts it to the
  exact \(K_{13}\)-hole shape, and verifies both directions of Theorem 3 and
  the support-count identity.

The cyclic link and the round-robin factorization are controls for
parameter-independent proofs.  They are not a simultaneous fan and are not
evidence that the unrestricted completion always exists.
