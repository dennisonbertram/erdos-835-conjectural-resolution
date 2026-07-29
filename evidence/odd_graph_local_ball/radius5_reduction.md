# Exact radius-5 extension and triangle-decomposition shadow

Use the notation \(L_i(u),M_i(uv),N_{uv}(ij)\) from
`radius4_reduction.md`.  A sphere-5 vertex has the form
\[
F_{\{i,j\},\{u,v,w\}}
  =(B\setminus\{u,v,w\})\cup\{i,j\},
\]
where \(\{i,j\}\in\binom A2\) and
\(\{u,v,w\}\in\binom V3\).  There are
\[
\binom{15}{2}\binom{16}{3}=58\,800
\]
such vertices.  Write their prospective colours as
\[
P_{ij}(uvw)\in\mathcal C.
\]

## Exact extension condition

Fix \(ij\in\binom A2\) and \(uv\in\binom V2\).  The sphere-4 vertex
\(E_{\{i,j\},\{u,v\}}\) has two sphere-3 neighbours, of colours
\(M_i(uv)\) and \(M_j(uv)\), and fourteen sphere-5 neighbours
\(F_{\{i,j\},\{u,v,w\}}\), one for each \(w\notin\{u,v\}\).
Consequently the radius-4 colouring extends through radius 5 if and
only if, for every \(ij,uv\),
\[
\{P_{ij}(uvw):w\notin\{u,v\}\}
=\mathcal C\setminus
\{N_{uv}(ij),M_i(uv),M_j(uv)\}.
\tag{1}
\]
The three excluded colours are distinct by the radius-4 conditions.

## Triangle-decomposition formulation

Fix \(ij\) and a colour \(x\).  Define a graph \(H_{ij,x}\) on \(V\)
by declaring \(uv\) to be an edge when
\[
x\in\{N_{uv}(ij),M_i(uv),M_j(uv)\},
\]
and put \(G_{ij,x}=K_V-H_{ij,x}\).  Under (1), the triples coloured
\(x\) form a triangle decomposition of \(G_{ij,x}\): a pair \(uv\)
lies in exactly one such triple precisely when \(x\) is allowed at
\(uv\).

Conversely, a family of triangle decompositions of all the
\(G_{ij,x}\) gives \(P_{ij}\) exactly when their selected triangles
are pairwise disjoint across \(x\).  Their total number is automatically
\(\binom{16}{3}=560\), so disjointness also makes them exhaustive.
Thus radius 5 is a coupled exact triangle-decomposition problem, not
merely a collection of divisibility tests.

## Immediate necessary congruences

For fixed \(ij\), let
\[
t_x=|\{uv:N_{uv}(ij)=x\}|.
\]
The \(x\)-coloured edges of \(M_i\) and \(M_j\) are disjoint, and they
are also disjoint from the \(x\)-coloured edges selected by \(N(ij)\).
For \(x=\infty\), each \(M\)-class is a perfect matching of size 8.
For finite \(x\), each has size 7.  Since a triangle-decomposable graph
has edge count divisible by three,
\[
\boxed{\quad
t_\infty\equiv2\pmod3,\qquad
t_x\equiv1\pmod3\quad(x\in V).
\quad}
\tag{2}
\]

There is also a vertex-parity condition.  Let \(a_{i,x}(u)\) be one
when \(u\) is covered by the \(x\)-matching of \(M_i\), and zero
otherwise.  Then every degree in \(G_{ij,x}\) must be even, equivalently
\[
\deg_{N(ij)=x}(u)
\equiv1+a_{i,x}(u)+a_{j,x}(u)\pmod2.
\tag{3}
\]
Here \(a_{i,\infty}(u)=1\) for every \(u\), while for finite \(x\) it
vanishes exactly at \(u=x\) and \(u=L_i^{-1}(x)\).

Conditions (2) and (3) are exact necessary filters for a radius-5
search.  They are not sufficient: the triangle decompositions and
their cross-colour disjointness must still be exhibited.

