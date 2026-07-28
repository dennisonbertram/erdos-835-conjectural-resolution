# An exact \(r=2\) obstruction to the size-eight terminal route

Date: 2026-07-28.

## Result and exact scope

There is a target class-B support instance of profile
\[
(n_8,n_{10},n_{12})=(9,6,2)
\]
with a legitimate complement-cover six-packing of types
\[
8^4\,10^2
\]
whose residual graph has no perfect matching on **any** of the five
remaining size-eight supports.

This refutes a universal proof route that takes an arbitrary such
six-prefix and always appends one remaining size-eight matching and the
two size-twelve matchings.  It does not refute coordinated nine: the same
displayed six-prefix extends to nine by appending one size-ten matching
and the two size-twelve matchings.

## The six-prefix

On vertex set \(\{0,\ldots,12\}\), take:
\[
\begin{array}{c|l|l}
&\text{matching}&\text{support complement}\\ \hline
M_0&0\,4,\ 1\,5,\ 2\,3,\ 8\,11&\{6,7,9,10,12\}\\
M_1&1\,6,\ 2\,9,\ 4\,8,\ 10\,11&\{0,3,5,7,12\}\\
M_2&0\,8,\ 2\,6,\ 3\,5,\ 9\,10&\{1,4,7,11,12\}\\
M_3&1\,9,\ 3\,6,\ 4\,10,\ 11\,12&\{0,2,5,7,8\}\\
M_4&0\,11,\ 1\,2,\ 3\,9,\ 5\,6,\ 8\,10&\{4,7,12\}\\
M_5&0\,10,\ 1\,3,\ 2\,5,\ 4\,11,\ 7\,12&\{6,8,9\}.
\end{array} \tag{1}
\]
The six complements cover every vertex.  The matchings are pairwise
edge-disjoint, and their union \(D\) has
\[
|E(D)|=26,\qquad
(d_D(v))_{v=0}^{12}=(4,5,5,5,4,4,4,1,4,4,5,5,2),
\qquad \Delta(D)=5. \tag{2}
\]

## Completing the class-B inventory

Use the five remaining size-five complements
\[
\begin{split}
A_0&=\{1,2,3,5,9\},&
A_1&=\{1,2,3,6,12\},\\
A_2&=\{0,4,9,10,11\},&
A_3&=\{0,4,8,10,11\},\\
A_4&=\{2,3,5,6,9\},
\end{split} \tag{3}
\]
the four remaining triples
\[
\{1,8,11\},\quad
\{3,6,10\},\quad
\{4,8,10\},\quad
\{1,2,11\}, \tag{4}
\]
and the singleton complements
\[
\{5\},\qquad\{0\}. \tag{5}
\]
Together with (1), these are nine five-sets, six triples, and two
singletons.  Every vertex occurs in exactly five complements.  Thus they
form an exact target class-B \(r=2\) support instance.

## Why all five size-eight supports are blocked

The graph \(D\) contains two disjoint cliques
\[
K=\{0,4,8,10,11\},\qquad
L=\{1,2,3,5,6\}. \tag{6}
\]
Put \(G=K_{13}-D\).  The supports complementary to
\(A_0,A_1,A_4\) all contain \(K\), while those complementary to
\(A_2,A_3\) contain \(L\).  Hence each of the five residual size-eight
graphs contains an independent five-set.

An eight-vertex graph with an independent five-set has no perfect
matching: all five independent vertices would have to be matched to the
other three vertices.  Therefore none of the five remaining size-eight
supports has a perfect matching in \(G\).

## An instance-specific size-ten repair

The obstruction is specific to the size-eight terminal choice.  For the
size-twelve supports missing \(5\) and \(0\), take
\[
\begin{split}
N_{12}^{(5)}
 &=\{0\,12,\ 1\,11,\ 2\,8,\ 3\,4,\ 6\,10,\ 7\,9\},\\
N_{12}^{(0)}
 &=\{1\,12,\ 2\,11,\ 3\,10,\ 4\,9,\ 5\,8,\ 6\,7\}.
\end{split} \tag{7}
\]
For the size-ten support with complement \(\{1,8,11\}\), take
\[
N_{10}=\{0\,9,\ 2\,10,\ 3\,12,\ 4\,6,\ 5\,7\}. \tag{8}
\]
These three matchings are pairwise edge-disjoint and avoid \(D\).
Appending them to (1) gives a literal nine-packing of pattern
\[
8^4\,10^3\,12^2. \tag{9}
\]
This repair is instance-specific, not a universal \(r=2\) theorem.

## Verification

Run:

```sh
python3 collaboration/r2_size8_gate_obstruction/verify_obstruction.py
```

The verifier uses only the Python standard library.  It reconstructs the
six-prefix, verifies the exact class-B row and column data, checks the two
clique obstructions and exhaustively confirms that all five size-eight
supports lack a perfect matching, then verifies every edge and support in
the explicit nine-packing (7)--(9).
