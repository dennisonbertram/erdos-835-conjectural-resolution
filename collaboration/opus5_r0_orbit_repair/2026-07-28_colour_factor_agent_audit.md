# Prescribed-colour \(b\)-factors: exact boundary-flow reduction and the first obstruction

Date: 2026-07-28.

## Verdict

Fix three selected triple rows \(R_1,R_2,R_3\), put
\[
S_i=V\setminus R_i,\qquad
t(v)=|\{i:v\in R_i\}|,\qquad b(v)=3-t(v),
\]
and suppose that a simple \(b\)-factor \(H\subseteq G\) has already been
found.

The prescribed-colouring half is **not automatic**, for any of the sixteen
Venn types.  Component parity and the usual nonzero bridge boundary are not
sufficient either.  The exact fixed-\(H\) problem is a nowhere-zero
\(\mathbb F_2^2\) boundary-flow problem.  Trees and unicyclic components
have complete elementary classifications, but components with at least two
independent cycles have a genuine affine cycle-space obstruction.  Cubic
snarks are its zero-boundary special case.

The accompanying verifier contains, for each of the sixteen Venn types, a
simple fifteen-edge graph \(H\) with the exact degree sequence \(b\) such
that:

1. every component has balanced boundary;
2. every bridge has nonzero forced colour; but
3. \(H\) has no prescribed colouring.

These graphs are not counterexamples to full-row cut sufficiency: the target
allows choosing a different \(b\)-factor in the dense ambient graph \(G\).
They prove that the missing argument must use that ambient choice or a
degree-preserving switch.  No Venn type makes an arbitrary \(b\)-factor
colourable.

## 1. Exact boundary-flow equivalence

Write the three nonzero elements of
\(\Gamma=\mathbb F_2^2\) as
\[
\gamma_1=a,\qquad \gamma_2=b,\qquad \gamma_3=a+b.
\]
Define the prescribed boundary
\[
\sigma(v)=\sum_{i:v\in S_i}\gamma_i
          =\sum_{i:v\in R_i}\gamma_i. \tag{1}
\]
The equality holds because
\(\gamma_1+\gamma_2+\gamma_3=0\).

> **Boundary-flow lemma.**  A simple graph \(H\) with
> \(d_H(v)=b(v)\) has the required proper edge-colouring if and only if
> there is a map
> \[
> \phi:E(H)\longrightarrow\Gamma\setminus\{0\}
> \]
> satisfying
> \[
> \sum_{e\ni v}\phi(e)=\sigma(v)\qquad(v\in V). \tag{2}
> \]

To prove the forward implication, label a colour-\(i\) edge by
\(\gamma_i\).  At \(v\), the incident colours are exactly those for
which \(v\in S_i\), so (2) follows.

Conversely, (2) and nonzeroness force exactly the prescribed local colour
set:

- at degree three, \(\sigma(v)=0\); three nonzero elements summing to zero
  must be the three distinct elements of \(\Gamma\setminus\{0\}\);
- at degree two, \(\sigma(v)=\gamma_i\), where \(i\) is the missing
  colour; the two nonzero summands must be the other two colours;
- at degree one, \(\sigma(v)\) is the unique required colour;
- at degree zero, both sides are zero.

Thus (2) proves the prescribed missing-colour condition, not merely
ordinary 3-edge-colourability.

## 2. The exact affine obstruction for a fixed graph

For a component \(C\), summing (2) gives the necessary balance law
\[
\sum_{v\in C}\sigma(v)=0. \tag{3}
\]
Assume (3), choose a spanning tree \(T\), and give arbitrary values in
\(\Gamma\) to the \(\mu=|E(C)|-|V(C)|+1\) cotree edges.  The tree-edge
values are then unique.  More explicitly, for a tree edge \(e\), let
\(A_e\) be the side below \(e\).  Summing (2) over \(A_e\) gives
\[
\phi(e)=
\sum_{v\in A_e}\sigma(v)
+\sum_{f\in\delta(A_e)\setminus\{e\}}\phi(f). \tag{4}
\]

Consequently:

> **Affine cycle-space criterion.**  A balanced component has a
> prescribed colouring if and only if one of its \(4^\mu\) boundary
> flows given by (4) is nonzero on every edge.

Equivalently, the affine \(\Gamma\)-cycle space is not covered by the
coordinate-zero sets
\[
\{\phi:\phi(e)=0\},\qquad e\in E(C). \tag{5}
\]
For the thirteen-vertex \(b\)-factors here, this is a small exact finite
test.  It is not, however, a cut criterion.

### Bridges

If \(e\) is a bridge and \(A\) is one side of it, (4) reduces to
\[
\phi(e)=\sum_{v\in A}\sigma(v). \tag{6}
\]
Hence a zero-boundary side is an immediate obstruction.  For a tree
component, (3) and the nonzeroness of (6) for every edge are also
sufficient, because every edge value is forced.

### Unicyclic components

For a connected unicyclic component, first assign every branch edge using
(6).  If one is zero, colouring is impossible.  At a cycle vertex \(v_j\),
move the assigned branch value, if present, to the right side of (2), and
call the resulting nonzero value \(\tau_j\).  If the cycle edges in cyclic
order are \(x_0,\ldots,x_{m-1}\), their equations are
\[
x_{j-1}+x_j=\tau_j. \tag{7}
\]
Balance gives \(\sum_j\tau_j=0\).  Put
\[
p_0=0,\qquad p_j=\tau_1+\cdots+\tau_j
\quad(1\le j<m).
\]
All solutions have the form \(x_j=x_0+p_j\).  Therefore:

> **Unicyclic criterion.**  After all bridge values are checked, the
> component is colourable if and only if
> \[
> \{p_0,\ldots,p_{m-1}\}\ne\Gamma. \tag{8}
> \]

The smallest parity-balanced obstruction not detected by bridges is a
four-cycle of degree-two vertices with missing colours
\[
\gamma_1,\gamma_2,\gamma_1,\gamma_2. \tag{9}
\]
Its partial sums are \(0,\gamma_1,\gamma_1+\gamma_2,\gamma_2\), all four
elements of \(\Gamma\).  Thus it is uncolourable despite having no bridge
and despite meeting every component parity law.

### Cubic components

On a cubic component, \(\sigma=0\), so (2) is exactly an ordinary
nowhere-zero \(\mathbb F_2^2\)-flow, equivalently a proper
three-edge-colouring.  A bridge has forced value zero.  A bridgeless
class-two cubic graph is a snark-type obstruction; the Petersen graph is
the smallest example.

In the present Venn inventory, a cubic component can use only vertices
outside \(R_1\cup R_2\cup R_3\).  The table below shows that only orbit
zero has ten such vertices.  Its displayed certificate is exactly a
Petersen component plus the three degree-zero common-row vertices.  The
other fifteen certificates are prescribed-boundary obstructions, not
Petersen components.

## 3. The sixteen exact boundary inventories

The Venn signature lists the seven nonempty cells in mask order
\[
1,2,3,4,5,6,7.
\]
For each orbit, the table gives
\[
\bigl(
n_3;\
n_2(\gamma_1,\gamma_2,\gamma_3);\
n_1(\gamma_1,\gamma_2,\gamma_3);\
n_0
\bigr),
\]
where \(n_d\) counts degree-\(d\) vertices and the triples refine degrees
one and two by their nonzero boundary value.

\[
\begin{array}{c|c|c}
\text{orbit}&\text{Venn signature}&
(n_3;n_2;n_1;n_0)\\ \hline
0&(0,0,0,0,0,0,3)&(10;(0,0,0);(0,0,0);3)\\
1&(0,0,1,0,1,1,1)&(9;(0,0,0);(1,1,1);1)\\
2&(0,0,1,1,0,0,2)&(9;(0,0,1);(0,0,1);2)\\
3&(0,0,2,1,1,1,0)&(8;(0,0,1);(1,1,2);0)\\
4&(0,0,2,2,0,0,1)&(8;(0,0,2);(0,0,2);1)\\
5&(0,0,3,3,0,0,0)&(7;(0,0,3);(0,0,3);0)\\
6&(0,1,1,1,1,0,1)&(8;(0,1,1);(0,1,1);1)\\
7&(0,1,2,2,1,0,0)&(7;(0,1,2);(0,1,2);0)\\
8&(1,1,0,1,0,0,2)&(8;(1,1,1);(0,0,0);2)\\
9&(1,1,1,1,1,1,0)&(7;(1,1,1);(1,1,1);0)\\
10&(1,1,1,2,0,0,1)&(7;(1,1,2);(0,0,1);1)\\
11&(1,1,2,3,0,0,0)&(6;(1,1,3);(0,0,2);0)\\
12&(1,2,1,2,1,0,0)&(6;(1,2,2);(0,1,1);0)\\
13&(2,2,0,2,0,0,1)&(6;(2,2,2);(0,0,0);1)\\
14&(2,2,1,3,0,0,0)&(5;(2,2,3);(0,0,1);0)\\
15&(3,3,0,3,0,0,0)&(4;(3,3,3);(0,0,0);0).
\end{array} \tag{10}
\]

The degree sum is thirty in every row of the table.  The verifier derives
the sixteen signatures rather than assuming their completeness.

## 4. What the finite certificates prove

Run:

```sh
python3 collaboration/opus5_r0_orbit_repair/2026-07-28_colour_factor_agent_verify.py
```

For each orbit, the verifier checks the displayed representative rows and
an explicit graph stored in the script.  It verifies simplicity, all
thirteen prescribed degrees, fifteen edges, component balance, and every
bridge boundary.  It then independently obtains zero solutions both by:

1. prescribed-colour backtracking; and
2. the affine spanning-forest boundary-flow enumeration (4).

Orbit zero is additionally checked by the cubic ten-vertex Moore
characterization of the Petersen graph.

This proves a useful negative finite lemma:

> For every Venn type of three triples on thirteen vertices, there is a
> simple \(b\)-factor for which all component and bridge boundary tests
> pass but prescribed colouring fails.

It does **not** prove that such a graph is the only \(b\)-factor available
inside a valid residual graph \(G\), and the certificates are not claimed
to be graph-minor-minimal.

## 5. Earliest remaining gap

After factor existence, the precise unresolved statement is:

> Among the simple \(b\)-factors \(H\subseteq G\), prove that at least one
> has an affine boundary-flow solution avoiding all coordinate-zero sets
> (5), or construct a full-row residual graph in which every \(b\)-factor
> is covered by those sets.

The sixteen Venn inventories, component parity, bridge law, and exclusion
of a Petersen component do not prove this.  A valid next argument must use
alternating \(b\)-factor switches in the ambient \(G\) and show that they
strictly reduce an exact obstruction measure, or perform a certified finite
enumeration of every \(b\)-factor in every full-row residual instance.
