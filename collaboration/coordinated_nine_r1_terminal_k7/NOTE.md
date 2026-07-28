# A replacement-triple repair for the \(K_7\) terminal in profile \(r=1\)

Date: 2026-07-28.

## Result and scope

Continue with the notation of
`../coordinated_nine_r1_reduction/NOTE.md`.  Let \(D\) be the
complement-cover six-prefix, let \(M_0,M_1\) be edge-disjoint perfect
matchings on two size-ten supports, and let
\[
X=V\setminus\{z\}
\]
be the unique size-twelve support.  Suppose that
\[
R=K_X-(D\cup M_0\cup M_1)
\]
has the remaining \(K_7\) Tutte barrier.  Thus
\[
X=U\mathbin{\dot\cup}S,\qquad |U|=7,\quad |S|=5,
\]
and every edge of \(K_U\) belongs to
\[
F=D\cup M_0\cup M_1. \tag{1}
\]
Put \(W=S\cup\{z\}\), so \(|W|=6\).

This note proves:

> **Replacement-triple lemma.** If neither \(M_0\) nor \(M_1\) has an
> edge with both endpoints in \(W\), then one of the four unused triple
> complements can replace one of the two selected triples, and the two
> resulting size-ten supports and \(X\) have three mutually
> edge-disjoint perfect matchings in \(K_{13}-D\).

The last finite coordination in the proof is exhaustively checked by the
dependency-free verifier in this directory.  The lemma closes the
no-\(WW\) equality branch of the \(K_7\) terminal.  The certified
two-switch lemma in
`../coordinated_nine_r1_terminal_k7_ww_sat/NOTE.md`, together with the
all-bad construction below, closes the complementary branch in which an
old matching has a \(WW\)-edge.  Thus the three pieces close the full
\(K_7\) terminal.

## The no-\(WW\) equality structure

Let \(T_i\) be the selected triple complement whose size-ten support is
matched by \(M_i\), and put
\[
r_i=|T_i\cap U|.
\]
Write \(a_i,b_i\) for the numbers of \(UU\)- and \(UW\)-edges in
\(M_i\).  Since no \(M_i\) has a \(WW\)-edge, every supported vertex of
\(W\) is matched to \(U\).  Hence
\[
b_i=3+r_i,\qquad 2a_i+b_i=7-r_i,
\]
and therefore
\[
a_i=2-r_i,\qquad r_i\le2. \tag{2}
\]

Every \(u\in U\) is incident with all six other core edges in (1).
Because \(d_D(u)\le5\), at least one of those edges belongs to
\(M_0\cup M_1\).  Thus the graph
\[
L=(M_0\cup M_1)[U]
\]
has minimum degree at least one.  By (2),
\[
|E(L)|=4-(r_0+r_1).
\]
Consequently
\[
7\le\sum_{u\in U}d_L(u)=8-2(r_0+r_1),
\]
which forces
\[
r_0=r_1=0. \tag{3}
\]

Both selected triples therefore lie in \(W\).  The graph \(L\) has four
edges, covers all seven vertices, and is the union of two two-edge
matchings.  Its degree sequence is
\[
(2,1,1,1,1,1,1). \tag{4}
\]
Let \(h\) be its unique degree-two vertex.  Equation (1) now gives
\[
D[U]=K_U-L,\qquad |E(D[U])|=17. \tag{5}
\]
Every vertex of \(U-\{h\}\) already has \(D\)-degree five inside \(U\),
while \(h\) has core degree four.  It follows that
\[
E_D(U,W)\subseteq\{hw:w\in W\},\qquad |E_D(U,W)|\le1. \tag{6}
\]
If \(\varepsilon=|E_D(U,W)|\), then \(|E(D)|=26\) and (5) also give
\[
|E(D[W])|=9-\varepsilon,\qquad
|E((K_{13}-D)[W])|=6+\varepsilon. \tag{7}
\]

## An unused triple meets the core twice

For every vertex \(v\), the class-B row identity after the six-prefix is
\[
\rho(v)=d_D(v)-1,
\]
where \(\rho(v)\) counts its incidence in the eleven unused
complements.  Summing over \(U\) and using (5)--(6), the unused
complements have at least
\[
\sum_{u\in U}(d_D(u)-1)
=2|E(D[U])|+\varepsilon-7
=27+\varepsilon \tag{8}
\]
incidences on \(U\).

The two selected triples contribute zero by (3).  The four unused
five-sets contribute at most twenty, and the singleton is \(\{z\}\).
The four remaining triples therefore contribute at least
\[
7+\varepsilon
\]
incidences on \(U\).  Some remaining triple \(T'\) satisfies
\[
r'=|T'\cap U|\ge2. \tag{9}
\]

## Canonical construction

The coloured graph in (4) has only one isomorphism type.  Relabel \(U\)
as \(0,\ldots,6\), and if necessary interchange the two old colours, so
that
\[
M_0[U]=\{01,23\},\qquad
M_1[U]=\{04,56\},\qquad h=0. \tag{10}
\]
Let \(T_0\subset W\) be the triple complement belonging to \(M_0\), and
put \(B_0=W-T_0\).

We reselect the retained matching as
\[
\widehat M_0=\{01,23\}\cup Q_0,
\]
where \(Q_0\) is a bijective matching from
\[
\{4,5,6\}\quad\text{to}\quad B_0. \tag{11}
\]
For the size-twelve support, use
\[
N=\{04\}\cup Q_N,
\]
where \(Q_N\) bijectively matches
\[
\{1,2,3,5,6\}\quad\text{to}\quad S. \tag{12}
\]
All cross edges in (11)--(12) avoid \(h\), so (6) says that they belong
to \(K_{13}-D\).

There are two cases for the replacement support \(V-T'\).

* If \(r'=2\), its two sides
  \[
  A'=U-T',\qquad B'=W-T'
  \]
  both have order five.  Take its matching \(M'=Q'\) entirely across
  \(A',B'\).
* If \(r'=3\), then \(|A'|=4\) and the support contains all six vertices
  of \(W\).  Choose an edge \(q\in (K_{13}-D)[W]\), whose existence
  follows from (7), and put
  \[
  M'=\{q\}\cup Q',
  \]
  where \(Q'\) bijectively matches \(A'\) to \(W-V(q)\).

It remains only to coordinate the three cross matchings
\(Q_0,Q_N,Q'\).  The following exact finite statement is the
coordination used here:

> For every \(T_0\in\binom W3\), every choice of no forbidden cross edge
> or one forbidden edge \(0w\), and every \(T'\) satisfying (9), the
> matchings in (11)--(12) and the applicable replacement matching above
> can be chosen pairwise edge-disjoint.  In the \(r'=3\) case this holds
> for every one of the fifteen possible choices of \(q\in\binom W2\).

The verifier enumerates exactly
\[
\binom63\cdot7\cdot\binom72\cdot6=17\,640
\]
configurations with \(r'=2\).  For \(r'=3\), it checks all
\[
\binom63\cdot7\cdot\binom73=4\,900
\]
base configurations and all fifteen possible \(W\)-edges in each, for
\(73\,500\) edge-specific checks.  Within a configuration it enumerates
all bijective matchings in (11), (12), and the applicable definition of
\(Q'\).  Thus it assumes no unproved greedy choice.

The two core edges used by \(\widehat M_0\) differ from the core edge
used by \(N\); the replacement matching uses only cross edges, or one
\(W\)-edge and cross edges.  The finite coordination therefore makes
\[
\widehat M_0,\quad M',\quad N
\]
mutually edge-disjoint perfect matchings on the required supports.  This
proves the lemma.

## Verification

Run:

```sh
python3 collaboration/coordinated_nine_r1_terminal_k7/verify_replacement.py
```

The verifier uses only Python's standard library.  Besides the finite
coordination, it audits the equality arithmetic, the unique coloured
core orbit, the incidence lower bound which produces \(T'\), and every
ordered pair of edge-disjoint one-factors used by the all-bad
\(K_8\) construction.

## Completing the \(K_7\) terminal

It remains to record how the replacement lemma fits with the
\(WW\)-switch certificate, including the equality excluded from that
certificate.

For \(s\in S\), define
\[
A_s=\{u\in U:us\in D\cup M_0\cup M_1\}. \tag{13}
\]
Every \(u\in U\) already has six selected core edges.  Since
\(d_D(u)\le5\) and each old matching contributes at most one edge at
\(u\), it has at most one selected neighbour in \(W\).  Hence the five
sets in (13) are pairwise disjoint.

If \(|A_s|\le6\) for every \(s\), the certified local lemma in
`../coordinated_nine_r1_terminal_k7_ww_sat/NOTE.md` applies whenever an
old matching has a \(WW\)-edge.  It finds a core edge \(e\) which is
simultaneously Hall-good for the size-twelve matching and admits a
two-switch against a \(WW\)-edge of its owner.  This gives the required
three-match extension.

Suppose finally that
\[
A_s=U \tag{14}
\]
for some \(s\in S\).  Put \(A=U\cup\{s\}\) and
\(B=V-A=W-\{s\}\).  All 28 edges of \(K_A\) belong to
\(F=D\cup M_0\cup M_1\).  At each vertex of \(A\), the degree bound on
\(D\) and the matching bounds force equality:
\[
d_D(a)=5,\qquad d_{M_0}(a)=d_{M_1}(a)=1. \tag{15}
\]
Thus
\[
P_i=M_i[A]
\]
is a perfect matching of \(K_A\), the two \(P_i\) are edge-disjoint, and
\[
D[A]=K_A-(P_0\cup P_1). \tag{16}
\]
Each \(M_i\) has one further edge \(q_i\) entirely in \(B\).  Equation
(15) also shows that no edge from \(A\) to \(B\) belongs to \(D\).

Choose vertex-disjoint edges
\[
e_0\in P_0,\qquad e_1\in P_1. \tag{17}
\]
Such a choice always exists: after choosing \(e_0\), at most two edges
of the perfect matching \(P_1\) meet its endpoints, leaving two choices.
For each \(i\), replace
\[
e_i,\ q_i
\]
in \(M_i\) by the two cross edges which match the endpoints of \(e_i\)
to the endpoints of \(q_i\).  All four new edges avoid \(D\), and the
two repaired colours are edge-disjoint because the \(A\)-endpoints in
(17) are disjoint.

Now take
\[
N=\{e_0,e_1\}\cup Q, \tag{18}
\]
where \(Q\) is any perfect matching from the four vertices of
\(A-V(e_0)-V(e_1)\) to \(S-\{s\}\).  All these cross edges avoid \(D\).
They also avoid the two repaired colours: their \(A\)-endpoints are
disjoint from the endpoints used in the two switches.  Hence (18) and
the two repaired size-ten matchings are mutually edge-disjoint.

The alternatives are now exhaustive:

* if neither old matching has a \(WW\)-edge, use the replacement-triple
  lemma proved above;
* if an old matching has a \(WW\)-edge and every \(|A_s|\le6\), use the
  certified two-switch lemma; and
* if some \(|A_s|=7\), use (14)--(18).

Therefore the \(K_7\) terminal is eliminated.
