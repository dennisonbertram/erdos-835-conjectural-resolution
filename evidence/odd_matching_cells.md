# Odd matching cells and triangle monodromy in \(O_{16}\)

This note records a parity consequence of a hypothetical locally bijective
colouring
\[
 c:O_{16}\longrightarrow K_{17}.
\]
The fibre size is
\[
 n=17\,678\,835=31\mu,\qquad \mu=570\,285.
\]
For two colours \(a\ne b\), their fibres are joined by a perfect matching.
An edge \(\{A,B\}\), where \(A,B\) are disjoint 15-subsets of a 31-set
\(X\), has the unique label
\[
 \ell(A,B)=X\setminus(A\cup B).
\]

The complementary-pair uniformity in the lower \(J(30,15)\) layer says
that, for every \(x\in X\) and every unordered colour pair \(\{a,b\}\),
exactly
\[
 \mu=\frac{\binom{30}{15}}{17\cdot16}=570\,285
\]
matching edges between the two fibres have label \(x\).  In particular,
every matching cell has odd size.

## 1. The mod-two label invariant

For each colour pair \(\{a,b\}\), xor the singleton labels over its matching.
Every point occurs \(\mu\) times and \(\mu\) is odd, so
\[
 \bigoplus_{e\in M_{ab}}e=X. \tag{1}
\]

Fix three colours \(a,b,c\), and compose their matchings around the triangle:
\[
 \tau_{abc}=M_{ca}M_{bc}M_{ab}.
\]
If a three-edge segment starting at \(A\) has labels \(x,y,z\), then, in
the binary vector space on \(X\),
\[
 \tau_{abc}(A)=A+X+\{x,y,z\}. \tag{2}
\]
The local bijection property forces
\[
 x\notin A,\qquad y\in A,\qquad
 z\notin A,\quad z\ne x,
\]
and hence
\[
 A\cap\tau_{abc}(A)=\{y\},\qquad
 X\setminus(A\cup\tau_{abc}(A))=\{x,z\}. \tag{3}
\]
Thus triangle monodromy is a fixed-point-free permutation of one fibre,
supported on the intersection-one relation.

Xoring (2) over a complete orbit of length \(s\) gives \(0\) when \(s\) is
even and \(X\) when \(s\) is odd.  On the other hand, xoring the labels over
all three matching sides and using (1) gives \(X+X+X=X\).  Therefore
\[
 \#\{\text{odd cycles of }\tau_{abc}\}\equiv1\pmod2. \tag{4}
\]
Because the fibre size \(n\) is odd, (4) is exactly the universal fact that
a permutation of an odd set has an odd number of odd cycles.  Hence the
first-order xor consequence of the odd cells is a tautology, not a new
obstruction.

The odd-girth condition remains nontrivial: an odd orbit of length \(s\)
lifts to an odd closed walk of length \(3s\) in \(O_{16}\), so
\(s\ge11\).  The cell parity alone does not force a shorter orbit.

## 2. A cofactor-orientation identity

At a vertex \(A\) in colour \(a\), local bijectivity gives a bijection
\[
 \phi_A:\{0,\ldots,16\}\setminus\{a\}\longrightarrow X\setminus A
\]
which sends a colour \(b\) to the label of the \(a\)-\(b\) matching edge
at \(A\).  Give colours and points their increasing orders and put
\[
 S_a=\prod_{A\in c^{-1}(a)}\operatorname{sgn}(\phi_A).
\]

For an \(a\)-\(b\) edge \(A B\) with label \(x\), delete \(b\mapsto x\)
from \(\phi_A\), and delete \(a\mapsto x\) from \(\phi_B\).  The two
resulting bijections have common domain
\(\{0,\ldots,16\}\setminus\{a,b\}\) and codomains \(B\) and \(A\),
respectively.  Call them \(\psi_{A,b}\) and \(\psi_{B,a}\).
The cofactor sign formula, multiplied over the whole matching, gives
\[
 \prod_{AB\in M_{ab}}
   \operatorname{sgn}(\psi_{A,b})
   \operatorname{sgn}(\psi_{B,a})
 =(-1)^{a+b}S_aS_b. \tag{5}
\]

Indeed, the deleted colour positions sum to \(a+b-1\) on every edge.
The two deleted point positions sum to \(x\), because \(A\) and \(B\)
partition \(X\setminus\{x\}\).  There are \(n\) edges, \(n\) is odd, and
each \(x=0,\ldots,30\) occurs \(\mu\) odd times; hence the total cofactor
exponent is
\[
 (a+b-1)n+\mu\sum_{x=0}^{30}x
 \equiv a+b\pmod2.
\]

Equation (5) is a genuine orientation identity exposed by the odd matching
cells.  By itself it does not yet constrain the triangle permutation
\(\tau_{abc}\): the block-orientation products on its left depend on the
chosen large set.  Any successful sign obstruction must add a compatibility
relation among these cofactor products for different colour pairs.

## 3. The compatibility relation closes, but is identically even

There is a canonical rank-15 connection along every matching edge.  If
\(A\) has colour \(a\), \(B\) has colour \(b\), and \(A B\) is their
matching edge, define
\[
 g_{AB}:A\longrightarrow B,\qquad
 g_{AB}\bigl(\phi_B(d)\bigr)=\phi_A(d)
 \quad(d\notin\{a,b\}). \tag{6}
\]
Both displayed lists contain 15 distinct points, so this is a bijection,
and \(g_{BA}=g_{AB}^{-1}\).

Let the sign of each \(\phi_A\) use the increasing orders fixed above.  If
the label of \(AB\) is \(x\), the same two-cofactor calculation as in
(5), now on one edge, gives
\[
 \operatorname{sgn}(g_{AB})
 =
 \operatorname{sgn}(\phi_A)\operatorname{sgn}(\phi_B)
 (-1)^{a+b-1+x}. \tag{7}
\]
Here \(a+b-1\) is the sum of the positions of \(b\) and \(a\) in the two
ordered 16-element colour sets.  The two positions of \(x\) in
\(X\setminus A\) and \(X\setminus B\) sum to \(x\), because \(A,B\)
partition \(X\setminus\{x\}\).

Now take any closed walk
\[
 A_0A_1\cdots A_L=A_0
\]
in \(O_{16}\), with vertex colours \(a_i\) and edge labels \(x_i\).
Multiplying (7) around the walk cancels all vertex-orientation signs and
all colour terms in pairs.  The determinant of its connection holonomy is
\[
 \operatorname{sgn}
 (g_{A_{L-1}A_L}\cdots g_{A_0A_1})
 =(-1)^{L+\sum_i x_i}. \tag{8}
\]
The edge recurrence in binary point-vectors is
\[
 A_{i+1}=A_i+X+\{x_i\}.
\]
Closure therefore says that every point-label occurs an even number of
times when \(L\) is even, and an odd number of times when \(L\) is odd.
If \(L\) is even, both terms in the exponent of (8) are even.  If \(L\)
is odd, then
\[
 \sum_i x_i\equiv\sum_{x=0}^{30}x=465\equiv1\pmod2,
\]
which again cancels \(L\).  Hence
\[
 \boxed{\text{the connection holonomy around every closed walk is even.}}
 \tag{9}
\]

For a triangle monodromy orbit, (9) is exactly the missing compatibility
relation obtained by multiplying (5) around the three colour pairs.  It
holds separately on every orbit, not just after multiplying all sheets.
Thus the determinant/sign refinement closes consistently and gives no
contradiction: the holonomy group merely lands in \(A_{15}\).  Any further
orientation attack must use more than the determinant, for example a
genuine restriction on the full \(A_{15}\)-valued holonomy.
