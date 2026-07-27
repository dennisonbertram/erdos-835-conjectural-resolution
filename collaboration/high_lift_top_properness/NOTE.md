# High-lift top-properness

Date: 2026-07-27.

## Scope

This note studies whether the locally forced constructions at
\(j=10,11,12\) automatically satisfy top-properness at the next level.
The setting and notation are those of the unrestricted lift tower, with
\[
 |U|=19,\qquad |A|=13,\qquad |{\cal C}|=17.
\]

The results below prove the implications at \(j=12\), \(j=11\), and \(j=10\).
They are
conditional on the stated lower tower laws already holding.  They do not
construct those lower levels or solve Erdős--Rosenfeld Problem #835.

## 1. The final \(j=12\) implication is automatic

At level \(12\), fix \(R\in\binom U{16}\).  For
\(B\in\binom A{12}\), the tower law is
\[
 \{G_B(R\setminus\{x\}):x\in R\}
 \mathbin{\dot\cup}
 \{G_A(R)\}
 ={\cal C}.
\tag{1}
\]
Level-\(12\) top-properness says that the first sixteen values are
distinct.  Thus \(G_A(R)\) is their unique missing colour.  The
fixed-\(R\) complement theorem independently shows that the same missing
colour works for all thirteen choices of \(B\), but that fact is not needed
in the argument once the tower law (1) is assumed.

> **Theorem 1 (automatic final top-properness).**  Suppose the maps
> \(G_B:\binom U{15}\to{\cal C}\), \(B\in\binom A{12}\), are
> top-proper at level \(12\), and suppose values
> \(G_A(R)\), \(R\in\binom U{16}\), satisfy every level-\(12\) tower
> law (1).  Then \(G_A\) is automatically top-proper:
> \[
> \bigl(G_A(P\setminus\{x\})\bigr)_{x\in P}
> \text{ are pairwise distinct}
> \qquad(P\in\binom U{17}).
> \tag{2}
> \]

### Proof

Fix \(P\in\binom U{17}\) and any \(B\in\binom A{12}\).  Colour the edges
of a complete graph on vertex set \(P\) by
\[
 \phi(\{x,y\})=G_B(P\setminus\{x,y\}).
\tag{3}
\]
At vertex \(x\), these are the sixteen values
\[
 G_B((P\setminus\{x\})\setminus\{y\}),
 \qquad y\in P\setminus\{x\}.
\]
They are distinct by level-\(12\) top-properness on the sixteen-set
\(P\setminus\{x\}\).  Hence \(\phi\) is a proper \(17\)-edge-colouring
of \(K_{17}\).

The tower law (1) on \(R=P\setminus\{x\}\) says that
\[
 m(x):=G_A(P\setminus\{x\})
\tag{4}
\]
is the unique colour missing at vertex \(x\) in \(\phi\).

For a colour \(\gamma\), its edge class is a matching \(M_\gamma\).
Consequently the number of vertices missing \(\gamma\) is
\[
 17-2|M_\gamma|,
\tag{5}
\]
which is a positive odd integer.  On the other hand, every vertex misses
exactly one of the seventeen colours, so the total number of
vertex--missing-colour incidences is \(17\).  There are seventeen colours,
and each contributes at least one incidence by (5); therefore each
contributes exactly one.  The missing colours \(m(x)\), \(x\in P\), are
pairwise distinct, proving (2). \(\square\)

The parity of the odd complete graph is essential to this short proof.
It is stronger than simply observing that every \(G_A(R)\) is locally
forced: it couples the seventeen overlapping sixteen-sets inside \(P\).

## 2. The \(j=11\) implication is also automatic

Here the conclusion is top-properness of the maps indexed by the
twelve-subsets \(A\setminus\{a\}\).

> **Theorem 2 (automatic level-\(12\) top-properness).**  Assume all tower
> laws for \(B\subset A\) with \(1\leq |B|\leq11\).  Fix
> \(P\in\binom U{16}\).  Then, for every \(a\in A\), the sixteen values
> \[
>   G_{A\setminus\{a\}}(P\setminus\{x\}),\qquad x\in P,
> \tag{6}
> \]
> are pairwise distinct.  In fact the same one colour is absent from (6)
> for every \(a\).

### Proof

Fix a colour \(\gamma\).  For every nonempty \(S\subseteq A\), put
\[
 F_S(X)=G_{A\setminus S}(P\setminus X)
 \quad\left(X\in\binom P{|S|}\right),\qquad
 N_S=\#\{X:F_S(X)=\gamma\}.
\tag{7}
\]
Write \(d_a=N_{\{a\}}\).  Thus \(d_a\) is the multiplicity of \(\gamma\)
in column \(a\) of (6).

Let \(2\leq s=|S|\leq12\), and fix
\(Y\in\binom P{s-1}\).  Apply the tower law for \(B=A\setminus S\) to
\(Q=P\setminus Y\).  Notice that
\[
 |Q|=17-s=|B|+4.
\]
Its seventeen pairwise distinct entries are exactly
\[
 \{F_S(Y\cup\{z\}):z\in P\setminus Y\}
 \mathbin{\dot\cup}
 \{F_{S\setminus\{a\}}(Y):a\in S\}.
\tag{8}
\]
Consequently \(\gamma\) occurs exactly once in (8).  Sum this assertion
over all \(Y\in\binom P{s-1}\).  A set counted by \(N_S\) has \(s\)
different \((s-1)\)-faces, while the second part of (8) contributes the
smaller \(N\)'s once each.  Hence
\[
 sN_S+\sum_{a\in S}N_{S\setminus\{a\}}
 =\binom{16}{s-1}.
\tag{9}
\]

Define \(\alpha_1=0\) and
\[
 \alpha_s=\frac1s\binom{16}{s-1}-\alpha_{s-1}.
\tag{10}
\]
Induction in (9) gives the exact formula
\[
 N_S=\alpha_s+\frac{(-1)^{s-1}}s\sum_{a\in S}d_a.
\tag{11}
\]
For the sizes needed here, the constants are
\[
\begin{array}{c|rrrrrrrrrrr}
s&2&3&4&5&6&7&8&9&10&11&12\\ \hline
\alpha_s&8&32&108&256&472&672&758&672&472&256&108 .
\end{array}
\tag{12}
\]
They are all integers.  Since \(N_S\) is an integer, (11) therefore says
\[
 \sum_{a\in S}d_a\equiv0\pmod s
 \qquad(2\leq |S|=s\leq12).
\tag{13}
\]

Take distinct \(a,b\in A\).  For each \(2\leq s\leq12\), choose an
\((s-1)\)-set \(T\subset A\setminus\{a,b\}\).  This is possible because
\(|A\setminus\{a,b\}|=11\).  Subtract (13) for
\(T\cup\{a\}\) and \(T\cup\{b\}\).  It follows that
\[
 d_a-d_b\equiv0\pmod s\qquad(2\leq s\leq12).
\]
Thus \(d_a-d_b\) is divisible by
\(\mathop{\rm lcm}(2,\ldots,12)=27720\).  But \(0\leq d_a,d_b\leq16\),
so all thirteen numbers \(d_a\) equal a common \(d\).

For each fixed \(x\in P\), the thirteen values
\[
 G_{A\setminus\{a\}}(P\setminus\{x\}),\qquad a\in A,
\tag{14}
\]
are pairwise distinct: the values for distinct \(a,b\) occur together in
the tower law for \(A\setminus\{a,b\}\).  Hence, for the fixed colour
\(\gamma\),
\[
 13d=\sum_{a\in A}d_a\leq16,
\]
so \(d\in\{0,1\}\).  There are \(16\cdot13\) entries in (14) as \(x,a\)
vary, and each colour with \(d=1\) contributes thirteen entries.
Therefore exactly sixteen colours have \(d=1\).  Each column in (6)
contains each of those sixteen colours once and omits the same remaining
colour.  This proves the theorem. \(\square\)

Only the tower laws with \(1\leq|B|\leq11\) entered the proof:
\(|B|=13-s\) in (8), for \(2\leq s\leq12\).  No level-\(0\) tower law
and no level-\(12\) top-properness assumption was used.

### A weakened boundary countermodel, and its exact delimiter

There is a small certificate with \(|A|=3\), \(|P|=6\), and seven colours
that satisfies the following *immediate fixed-\(P\) slice constraints*:

1. each row \(a\mapsto\lambda_x(a)\) is injective;
2. for each pair \(ab\), \(\phi_{ab}\) is a proper seven-edge-colouring
   of \(K_6\), and the two colours missing at vertex \(x\) are
   \(\lambda_x(a),\lambda_x(b)\);
3. on each edge \(xy\), the three values \(\phi_{ab}(xy)\) properly
   edge-colour \(K_3\).

Nevertheless one column of \(\lambda\) has a repeated value.  The complete
certificate is embedded in `verify_j11_top_properness.py`.

**Delimiter.**  This is not a counterexample to Theorem 2 and does not
refute automaticity under the full tower hypotheses.  It specifies only
one fixed \(P\)-slice, omits the maps on the other lower-tower faces, and
does not obey the cross-face recurrence (9).  Its sole purpose is to show
that the three immediate slice constraints above are insufficient without
the rest of the lower tower.

## 3. The \(j=10\) implication is automatic

The last case is a weighted-edge defect problem rather than the
one-dimensional defect problem in Theorem 2.

> **Theorem 3 (automatic level-\(11\) top-properness).**  Assume all tower
> laws for \(B\subset A\) with \(2\leq |B|\leq10\).  Fix
> \(P\in\binom U{15}\).  Then, for every pair \(a,b\in A\), the fifteen
> values
> \[
>   G_{A\setminus\{a,b\}}(P\setminus\{x\}),\qquad x\in P,
> \tag{15}
> \]
> are pairwise distinct.

### Proof

Fix a colour \(\gamma\).  For \(S\subseteq A\), \(|S|=s\geq2\), put
\[
 F_S(X)=G_{A\setminus S}(P\setminus X)
 \quad\left(X\in\binom P{s-1}\right),\qquad
 N_S=\#\{X:F_S(X)=\gamma\}.
\tag{16}
\]
Write \(d_{ab}=N_{\{a,b\}}\).  Thus \(d_{ab}\) is the multiplicity of
\(\gamma\) in the column (15) indexed by \(ab\).

Let \(3\leq s=|S|\leq11\), and fix
\(Y\in\binom P{s-2}\).  The tower law for \(B=A\setminus S\), applied to
\(Q=P\setminus Y\), says that \(\gamma\) occurs once among
\[
 \{F_S(Y\cup\{z\}):z\in P\setminus Y\}
 \mathbin{\dot\cup}
 \{F_{S\setminus\{a\}}(Y):a\in S\}.
\tag{17}
\]
Summing over \(Y\) gives
\[
 (s-1)N_S+\sum_{a\in S}N_{S\setminus\{a\}}
 =\binom{15}{s-2}.
\tag{18}
\]
Starting with \(N_{\{a,b\}}=d_{ab}\), induction in (18) has the form
\[
 N_S=\alpha_s+
 \frac{(-1)^{s-2}}{s-1}
 \sum_{\{a,b\}\in\binom S2}d_{ab},
\tag{19}
\]
where \(\alpha_s\) depends only on \(s\).  Its precise value will not be
needed.  Since \(N_S\) is an integer, the edge sum in (19) has a residue
modulo \(s-1\) depending only on \(s\).

Fix distinct \(a,b,t,u\in A\).  For every \(q=2,\ldots,10\), compare
(19) on \(T\cup\{a\}\) and \(T\cup\{b\}\), where
\(T\in\binom{A\setminus\{a,b\}}q\).  Their difference shows
\[
 \sum_{v\in T}(d_{av}-d_{bv})\equiv0\pmod q.
\tag{20}
\]
Choose two such sets that differ only by exchanging \(t\) and \(u\).
This is possible for every \(q\leq10\), because the other nine vertices
provide the common \(q-1\) elements.  Hence
\[
 (d_{at}-d_{bt})-(d_{au}-d_{bu})\equiv0\pmod q
 \quad(q=2,\ldots,10).
\tag{21}
\]
The left side lies between \(-30\) and \(30\), whereas
\(\mathop{\rm lcm}(2,\ldots,10)=2520\).  It must therefore vanish.

Thus all off-diagonal four-point differences vanish.  Equivalently, there
are integers \(c,u_a\) such that
\[
 d_{ab}=c+u_a+u_b\qquad(a\ne b).
\tag{22}
\]
For completeness, choose a reference vertex \(r\).  The equality just
proved makes \(u_a=d_{at}-d_{rt}\), for
\(t\notin\{a,r\}\), independent of \(t\); the same equality then shows
that \(d_{ra}-u_a\) is independent of \(a\), giving (22).  This also
shows that the parameters may be chosen integral.

For each fixed \(x\in P\), the edges \(ab\) for which
\[
 G_{A\setminus\{a,b\}}(P\setminus\{x\})=\gamma
\tag{23}
\]
form a matching in \(K_{13}\).  Indeed, the three values on the edges of
any triangle occur together in the tower law indexed by the complementary
ten-set and are distinct.  Consequently the weighted degree
\[
 r_a:=\sum_{b\ne a}d_{ab}
\tag{24}
\]
satisfies \(0\leq r_a\leq15\).  Formula (22) gives
\[
 r_a-r_b=11(u_a-u_b).
\tag{25}
\]
After translating all \(u_a\) by a common integer, either they are all
zero or they take the two values \(0,1\).

If all \(u_a=0\), every edge has one common weight \(k=c\).  The
\(s=3\) instance of (18) says
\[
 2N_{\{a,b,c\}}+d_{ab}+d_{ac}+d_{bc}=15.
\tag{26}
\]
Thus \(3k\) is odd, while (24) gives \(12k\leq15\).  Hence \(k=1\).

Suppose both potential levels occur.  Let \(h\) vertices have potential
one.  The low--low, mixed, and high--high edge weights are respectively
\[
 k,\quad k+1,\quad k+2.
\tag{27}
\]
If there are at least two low vertices, nonnegativity gives \(k\geq0\),
and the degree of a high vertex gives
\[
 12k+h+11\leq15.
\tag{28}
\]
Therefore \(k=0\) and \(h\leq4\).  There are then at least nine low
vertices, but a low triangle has even edge sum zero, contradicting (26).
If there is exactly one low vertex, then \(h=12\); nonnegativity and the
two degree bounds force \(k=-1\).  The weights are zero on the star
centred at the low vertex and one on every other edge.

We have proved that, for each colour \(\gamma\), its multiplicity graph
\((d_{ab})\) is one of exactly two types:

1. every edge of \(K_{13}\) has weight one; or
2. every edge has weight one except the twelve edges of one star, which
   have weight zero.

Let \(h_a\) count the colours of the second type whose deleted star is
centred at \(a\).  There are seventeen colours in all.  Since each column
(15) has fifteen entries,
\[
 15=\sum_\gamma d_{ab}=17-h_a-h_b
 \qquad(a\ne b).
\tag{29}
\]
Thus \(h_a+h_b=2\) for every pair, so \(h_a=1\) for every \(a\).
In particular each \(d_{ab}\) is zero or one, and exactly fifteen colours
have \(d_{ab}=1\).  The fifteen values in every column (15) are therefore
pairwise distinct, as required. \(\square\)

Only the tower laws with \(2\leq|B|\leq10\) entered this proof.  The
theorem does not supply those laws; it shows that once they have been
constructed, top-properness at level \(11\) is no additional constraint.

## Verification

Run:

```sh
python3 -B \
  collaboration/high_lift_top_properness/verify_j12_top_properness.py
```

The standard-library checker constructs the cyclic proper
\(17\)-edge-colouring of \(K_{17}\), identifies its unique missing colour
at each vertex, and checks the matching-incidence count used in the proof.
It is a sanity control, not the basis of Theorem 1.

Run:

```sh
python3 -B \
  collaboration/high_lift_top_properness/verify_j11_top_properness.py
```

This checks the exact recurrence constants and numerical bounds in
Theorem 2.  It also validates the weakened boundary certificate and prints
the delimiter stating that the certificate is not a full-tower
counterexample.

Run:

```sh
python3 -B \
  collaboration/high_lift_top_properness/verify_j10_top_properness.py
```

This checks the recurrence coefficients, the \(2520\) divisibility
bound, and exhaustively enumerates the potential-level cases used in
Theorem 3.  It is an arithmetic audit of the proof, not a construction of
the lower tower.
