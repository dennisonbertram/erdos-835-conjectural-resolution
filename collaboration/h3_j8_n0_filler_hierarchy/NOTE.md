# The \(N=0\) outside-filler hierarchy for a \(j=8\) torsion cube

## Scope

This note derives exact identities inside the unresolved normalized
\(\Delta=60\) branch of the \(j=8\to9\) arithmetic lift.  Here \(N\) denotes
the total \(d\)-mass on the eight negative cube cells, and this note assumes
\(N=0\).  The identities do not prove that this branch is feasible or
infeasible, do not construct a tower or colouring, and do not solve
Erdős--Rosenfeld Problem #835.

## Setup

Let the eight cube vertices be four pairs and let \(X\) be the five points
outside the cube.  For a transversal cube cell \(Q\) and a filler
\(F\subseteq X\), put \(S=Q\cup F\) and \(s=|S|=4+|F|\).  Write
\[
D_S=\sum_{R\in\binom S4}d_R.
\]
The recurrence multiplicities through the last available filler level are
\[
\begin{array}{c|c}
s&N_s(S)\\ \hline
4&D_S\\
5&(13-D_S)/2\\
6&13+D_S/3\\
7&(195-D_S)/4\\
8&65+D_S/5\\
9&117-D_S/6.
\end{array}
\tag{1}
\]

For a function on the sixteen transversals, let \(\partial^4\) denote the
oriented four-cube alternating sum, with the same orientation as
\(\partial^4d=60\).

## Forced derivatives

### Proposition 1

For every filler \(F\subseteq X\) of the required size,
\[
\partial^4N_s=
60,-30,20,-15,12,-10
\qquad(s=4,5,6,7,8,9).
\tag{2}
\]

### Proof

In the alternating sum of \(D_{Q\cup F}\), a four-set involving a filler
point, or failing to select one point from every cube pair, depends on fewer
than four cube choices and cancels.  Only the sixteen transversal four-sets
survive.  Hence
\[
\partial^4D_{Q\cup F}=\partial^4d=60.
\]
Multiplying by the coefficient of \(D_S\) in each row of (1) gives (2).
\(\square\)

Equivalently, taking the four-cube derivative of the recurrence gives
\[
(s-3)\partial^4N_s
+\sum_{x\in F}\partial^4N_{s-1}(F\setminus\{x\})=0.
\]

## The first outside layer when \(N=0\)

Fix \(x\in X\).  Let \(A_x\) and \(B_x\) be the sums of \(N_5(Q\cup\{x\})\)
over the eight positive and eight negative cube cells.  Since every
five-set raw \(d\)-sum is odd and at most \(13\),
\[
0\le N_5\le6.
\]
Equation (2) gives
\[
A_x-B_x=-30,\qquad B_x=A_x+30,\qquad0\le A_x\le18.
\tag{3}
\]

Let \(Z_x\) be the total \(d\)-mass on the 32 blocks consisting of \(x\)
and a transversal triple from three distinct cube pairs.  Summing
\[
2N_5(Q\cup\{x\})+d_Q+
\sum_{v\in Q}d_{(Q\setminus\{v\})\cup\{x\}}=13
\]
over either cube half gives
\[
Z_x=44-2A_x=104-2B_x.
\tag{4}
\]

Let \(C\) be the total mass on the 48 internal cube four-sets with pair
occupancy \(2+1+1\).  Summing the 32 transversal edge-triple capacities
counts every positive cube cell four times, every \(2+1+1\) block twice,
and every first-layer outside block once.  Since the positive cube mass is
60,
\[
240+2C+\sum_{x\in X}Z_x\le416.
\]
Using (4),
\[
\boxed{\ \sum_{x\in X}A_x\ge22+C.\ }
\tag{5}
\]

## The second outside layer

Fix distinct \(x,y\in X\), and define
\[
A'_{xy}=\sum_{Q\ {\rm positive}}(N_6(Q\cup\{x,y\})-13),
\quad
B'_{xy}=\sum_{Q\ {\rm negative}}(N_6(Q\cup\{x,y\})-13).
\]
Summing the six five-set bounds inside a six-set gives \(D_S\le39\), so
each summand lies in \([0,13]\).  Equation (2) gives
\[
A'_{xy}-B'_{xy}=20.
\tag{6}
\]

Let \(W_{xy}\) be the total mass on the 24 blocks made from \(x,y\) and two
cube vertices in distinct coordinate pairs.  Summing \(D_{Q\cup\{x,y\}}\)
over all sixteen transversals counts:

- the cube transversal mass once, for a total of \(60\);
- the \(x\)- and \(y\)-layer masses twice;
- every \(W_{xy}\) block four times.

Thus
\[
3(A'_{xy}+B'_{xy})
=60+2(Z_x+Z_y)+4W_{xy}.
\]
Combining this with (6) yields the exact identity
\[
\boxed{\ 3B'_{xy}=Z_x+Z_y+2W_{xy}.\ }
\tag{7}
\]

## Shifted identities through the remaining fillers

For an outside triple \(F=\{x,y,z\}\), let \(U_F\) be the total mass on
the eight blocks consisting of one cube vertex and \(F\).  For an outside
four-set \(H\), write \(V_H=d_H\).  The shifts
\[
M_7=48-N_7=(D_7-3)/4,\qquad
M_8=N_8-65=D_8/5,\qquad
M_9=117-N_9=D_9/6
\]
are nonnegative integers, with cube derivatives \(15,12,10\).

Let \(B_{3,F}\) be the sum of \(M_7(Q\cup F)\) over the eight negative cube
cells.  In the negative half, a first-layer block has one transversal
extension, a second-layer block has two, and a \(U_F\) block has four.
The cube-cell contribution is zero because \(N=0\).  Therefore
\[
\boxed{\ 4B_{3,xyz}+24
=Z_x+Z_y+Z_z+2(W_{xy}+W_{xz}+W_{yz})+4U_{xyz}.\ }
\tag{8}
\]
The \(24\) is the shift \(8\cdot3\).

For a four-set \(F\subset X\), let \(B_{4,F}\) be the negative-half sum of
\(M_8\).  A four-outside block \(V_F\) belongs to all eight negative
transversal extensions, giving
\[
\boxed{\ 5B_{4,F}
=\sum_{x\in F}Z_x
+2\sum_{\{x,y\}\in\binom F2}W_{xy}
+4\sum_{H\in\binom F3}U_H
+8V_F.\ }
\tag{9}
\]

Finally, for the unique five-point filler \(X\), let \(B_5\) be the
negative-half sum of \(M_9\).  Then
\[
\boxed{\ 6B_5
=\sum_{x\in X}Z_x
+2\sum_{\{x,y\}\in\binom X2}W_{xy}
+4\sum_{H\in\binom X3}U_H
+8\sum_{J\in\binom X4}V_J.\ }
\tag{10}
\]

The ten all-outside triple capacities give one further exact global bound:
each \(U_H\) occurs once, while every \(V_J\) contains four outside
triples.  Hence
\[
\boxed{\ \sum_{H\in\binom X3}U_H
+4\sum_{J\in\binom X4}V_J\le10\cdot13=130.\ }
\tag{11}
\]

Summing (8) over the ten outside triples and (9) over the five outside
four-sets gives the useful aggregate forms
\[
\begin{aligned}
4\sum B_{3,F}+240&=6Z+6W+4U,\\
5\sum B_{4,F}&=4Z+6W+8U+8V,\\
6B_5&=Z+2W+4U+8V,
\end{aligned}
\tag{12}
\]
where undecorated letters denote totals over their respective outside
subsets.

## Remaining gap

Equations (5), (7), and (8)--(12) give the full filler hierarchy between the
torsion cube and its five outside vertices.  A contradiction still requires
a sharp upper bound on the left of (5), or a lower bound on \(C\), obtained
by combining these identities with the \(q=7,8\) congruences.
