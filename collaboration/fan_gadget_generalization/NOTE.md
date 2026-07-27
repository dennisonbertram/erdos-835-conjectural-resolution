# Why the \(k=6\) fan gadget does not directly lift to the cyclic \(k=16\) link

## Status

This is a rigorous delimiter, not a solution of Erdős--Rosenfeld Problem
#835.  The explicit \(18\)-cell/\(11\)-triangle obstructions at \(k=6\) do
not transfer by the three most immediate mechanisms:

1. a linear or modular incidence-count identity;
2. padding each triangle with ten private cells; or
3. a one-step palette/equality gadget anchored on one constraint
   \(K_{13}\).

The calculations below use the committed cyclic \(LS(2,3,19)\).  They do not
exclude a nonlinear multistep gadget, a different link, or a simultaneous
\(13\)-fan.

## 1. Incidence formulation

For a fixed link, let \({\cal E}\) be the constraint groups and \({\cal V}\)
the allowed cells.  Every group has size \(q\), where \(q=3\) at \(k=6\)
and \(q=13\) at \(k=16\).  Let
\[
 B\in\{0,1\}^{{\cal E}\times{\cal V}}
\]
be the group-versus-cell incidence matrix.

A fan colouring partitions the cells into \(q\) colour classes, and every
class meets every group exactly once.  Hence the indicator \(x\) of any
class satisfies
\[
 Bx={\bf1}. \tag{1}
\]
This remains a necessary condition over every field, especially over
\(\mathbb F_q\).

Consequently, a vector of group weights \(w\) with
\[
 B^\mathsf{T}w=0,\qquad w^\mathsf{T}{\bf1}\ne0 \tag{2}
\]
is an obstruction.  Regular-degree divisibility arguments, Fano-style
incidence counts, and their weighted variants are all special cases of
(2).

## 2. What happens at \(k=6\)

For each of the two point-isomorphism types of \(LS(2,3,9)\), the complete
\(630\)-group by \(378\)-cell system (1) is inconsistent over
\(\mathbb F_3\).  Deterministic elimination gives independently checked
certificates supported on \(92\) groups for type A and \(86\) groups for
type B.

This linear fact does **not** explain the much smaller published gadgets.
For each \(18\)-cell/\(11\)-triangle gadget, its own eleven equations
\[
 \sum_{v\in e}x_v=1\quad(e\text{ one of the eleven triangles})
\]
have rank eleven and are consistent over \(\mathbb F_3\).  The contradiction
uses the nonlinear requirement that each triangle contains all three
colours, not merely the first-moment equations.

Thus a faithful lift of the \(18\)-cell gadget must transfer nonlinear
palette propagation.

## 3. Exact characteristic-\(13\) test on the cyclic link

The cyclic link has a \(C_{17}\) action translating its seventeen finite
points and its seventeen link colours simultaneously.  It acts freely on
the cells and groups, reducing the full incidence system from
\[
 19,380\text{ equations in }50,388\text{ variables}
\]
to
\[
 1,140\text{ orbit equations in }2,964\text{ orbit variables}. \tag{3}
\]

This quotient loses no information about consistency over
\(\mathbb F_{13}\).  If the full system has a solution, average its
\(C_{17}\)-translates and divide by \(17\), which is invertible modulo
\(13\), to obtain an invariant solution.  Conversely, a quotient solution
expands to a full invariant solution.

Exact sparse elimination gives
\[
 \operatorname{rank}_{\mathbb F_{13}} B_{\rm orb}=1083
\]
and, crucially,
\[
 B_{\rm orb}x={\bf1}\quad\textbf{is consistent}. \tag{4}
\]
The verifier reconstructs one solution, expands it to all \(50,388\)
cells, and checks all \(19,380\) equations.  The orbit vector has SHA-256
digest
```
d68e33b42c10d4c745ae767bf26d929de17423ca0209fce5f31cf72f0a349928
```

There are also \(57\) exact independent integral row relations.  For each
of the \(57\) translation orbits \({\cal R}\) of triples,
\[
 \sum_{\substack{(T,c)\\[T]={\cal R}}}B_{(T,c)}
 -
 \sum_Q m_{\cal R}(Q)B_Q=0, \tag{5}
\]
where \(m_{\cal R}(Q)\) counts the faces of \(Q\) in \({\cal R}\).  Each
relation has its own disjoint set of sixteen \(+1\) triple-colour rows, so
the relations are independent.  They give
\[
 \operatorname{rank}_{\mathbb Q}B_{\rm orb}\le1140-57=1083.
\]
Rank cannot increase after reduction modulo \(13\), so the mod-\(13\) rank
above proves the reverse inequality.  Hence
\[
 \operatorname{rank}_{\mathbb Q}B_{\rm orb}
 =\operatorname{rank}_{\mathbb F_{13}}B_{\rm orb}=1083. \tag{6}
\]

This implies a stronger integral statement.  Let
\(d_1,\ldots,d_{1083}\) be the nonzero Smith factors of \(B_{\rm orb}\).
Equality (6) says that none is divisible by \(13\).  On the other hand,
every row has sum thirteen, so
\[
 B_{\rm orb}{\bf1}=13{\bf1}. \tag{7}
\]
In the cokernel of \(B_{\rm orb}\), the class of the right-hand side
\([{\bf1}]\) is therefore killed by \(13\).  It lies in the torsion subgroup
(indeed (7) already puts \({\bf1}\) in the rational image), while the Smith
calculation says that this torsion subgroup has no \(13\)-torsion.  Thus
\([{\bf1}]=0\), proving
\[
\boxed{B_{\rm orb}x={\bf1}\text{ has a signed integral solution}.} \tag{8}
\]

This independently confirms that no characteristic-\(13\) certificate of
form (2), of any support, exists.  More strongly, reducing the signed
integral solution modulo any integer shows that **no integral or modular
linear weighted group-count identity can exclude a fan for this cyclic
link**.  Expanding the orbit coordinates gives the corresponding invariant
signed integral solution of the full \(19,380\)-row system; no division or
averaging is needed in that direction.  Over a field of characteristic
other than \(13\), the constant vector \(x_v=13^{-1}\) is the immediate
solution.

The signed solution in (8) need not have coordinates in \(\{0,1\}\).  It
does not produce an exact cover, much less a partition into thirteen exact
covers.  It only closes the linear route.

## 4. The first possible squarefree trade has support at least ten

A squarefree trade is a pair of disjoint cell sets \(P,N\) satisfying
\[
 B_{\rm orb}{\bf1}_P=B_{\rm orb}{\bf1}_N.
\]
Such trades are the natural local moves for changing a \(0/1\) exact cover
without changing any group count.

For the cyclic quotient there is no nonzero squarefree trade on two, four,
six, or eight cells.  The finite proof uses the \(228\) quadruple-group
rows.

- At support two, two cells would have identical incidence columns.
- At support four, quadruple-group balance leaves either \(2+2\) cells in
  one quadruple group or one positive/negative pair in each of two groups.
  Exact multiset comparison excludes both cases.
- At support six, quadruple-group balance allows the three positive cells
  to be paired with the three negative cells within their common
  quadruple groups.  Thus every candidate is a zero sum of three oriented
  within-group column differences.  The verifier enumerates all
  \(228\cdot13\cdot12=35,568\) such differences.  Their supports have the
  exact census
  \[
  34,910\text{ of size }8,\qquad658\text{ of size }6.
  \]
  Sparse meet-in-the-middle enumeration encounters \(391,248\) algebraic
  zero-sum pair-completion hits, but every completed triple cancels or
  repeats a cell; none has three distinct \(+1\) and three distinct
  \(-1\) coordinates.

Therefore
\[
\text{every nonzero squarefree quotient trade has support at least }8.
\]

At support eight there are four positive and four negative cells.  Balance
in every quadruple-group row forces the positive and negative multiplicity
of each \(Q\)-group to agree.  The distribution of the four positive cells
is therefore one of the five partitions
\[
4,\qquad3+1,\qquad2+2,\qquad2+1+1,\qquad1+1+1+1.
\]
All five cases are exhausted exactly.

- For \(4\), the verifier compares the TC-row multisets of all
  \(228\binom{13}{4}=163,020\) four-subsets within a \(Q\)-group.  There is
  no signature collision at all.
- For \(3+1\), it enumerates the
  \(228\binom{13}{3}\binom{10}{3}=7,824,960\) oriented disjoint
  triple-versus-triple differences and looks up the required opposite
  single swap in a different \(Q\)-group.  None exists.
- For \(2+2\), it enumerates the
  \(228\binom{13}{2}\binom{11}{2}=978,120\) oriented disjoint
  pair-versus-pair differences and looks for its opposite in a different
  \(Q\)-group.  None exists.
- For \(2+1+1\), it enumerates the same \(978,120\) double swaps.  Choose
  any nonzero coordinate of the required residual, preferring magnitude
  two.  At least one of the two remaining single swaps must have the
  required sign there, so a signed-row index enumerates it; the other move
  is then an exact dictionary lookup.  The exhaustive run makes
  \(118,592,198\) residual lookups and finds none.
- For \(1+1+1+1\), fix the least of the four distinct \(Q\)-groups and one
  of its oriented swaps.  At the first nonzero coordinate, one of the
  other three swaps must have the opposite sign, so all possibilities for
  the second swap are enumerated.  At a nonzero coordinate of their
  partial sum, one of the last two swaps must again have the opposite
  sign; enumerate the third and look up the uniquely determined fourth.
  Coefficient bounds discard only partial sums that one or two remaining
  \(\{-1,0,1\}\)-valued swaps cannot cancel.  The run checks
  \(1,204,296\) second-move hits, \(101,780,540\) third-move hits, and
  \(92,958,652\) exact final lookups, with no trade.

These five cases exhaust support eight, and every squarefree trade has even
support.
Consequently
\[
\boxed{\text{every nonzero squarefree quotient trade has support at least }10.}
\]
In particular, the difference of two distinct binary solutions of
\(B_0x=\mathbf1\) is such a trade, so any two invariant exact covers are
separated by Hamming distance at least ten.

The driver `verify_cyclic_support8.py` independently reconstructs the
quotient columns and checks their SHA-256 digest before compiling and
running the three C++17 exhaustive searches.  The search sources use only
the C++ standard library.

This remains a local-rigidity delimiter.  It does not exclude
nonsquarefree integer kernel vectors, trades of support ten or more, an
exact cover, or a fan.

### The support-ten search is reduced to four partitions

At support ten, Q-balance gives the seven partitions of five
\[
5,\quad4+1,\quad3+2,\quad3+1+1,\quad2+2+1,\quad
2+1+1+1,\quad1+1+1+1+1.
\]
The compact support-ten verifier exactly excludes the first three.

- Case \(5\) compares all \(228\binom{13}{5}=293,436\) five-subsets
  within their Q-groups and finds no TC-signature collision.
- Case \(4+1\) checks all
  \(228\binom{13}{4}\binom{9}{4}=20,540,520\) oriented disjoint
  four-versus-four differences against the required single swap in
  another Q-group.  Of these, \(18,091,188\) survive the necessary
  coefficient bound, and none completes.
- Case \(3+2\) checks all \(7,824,960\) oriented disjoint
  triple-versus-triple differences against the dictionary of \(978,120\)
  double-swap configurations in another Q-group.  None completes.

Thus a support-ten trade, if one exists, spans at least three Q-groups and
has one of
\[
\boxed{3+1+1,\quad2+2+1,\quad2+1+1+1,\quad1+1+1+1+1.}
\]
This is not a full exclusion of support ten.

## 5. Why padding the eleven triangles fails

At \(q=3\), a constraint triangle uses the whole palette.  Knowing two
colours determines the third, which powers every deduction in the
\(18\)-cell proof.

At \(q=13\), three mutually adjacent cells merely receive three distinct
colours.  If one pads every old triangle with ten private cells to make a
\(K_{13}\), those private cells can independently receive the ten unused
colours.  The old core then only needs an ordinary proper \(13\)-colouring,
so the contradiction disappears.

The fillers must therefore have their palettes aligned across different
constraint groups.  That requires an equality or permutation-propagation
gadget.

## 6. A sharp one-step palette barrier in \(H_L\)

For the fixed-link fan hypergraph, there are two kinds of constraint
\(K_{13}\)'s:

- \(Q\)-groups, containing all thirteen allowed colours at one quadruple;
- \((T,c)\)-groups, containing the thirteen allowed extensions of one
  triple-colour demand.

An outside cell has at most
\[
 \boxed{1}\quad\text{neighbour in a fixed \(Q\)-group}
\]
and at most
\[
\boxed{2}\quad\text{neighbours in a fixed \((T,c)\)-group}. \tag{9}
\]

For a \(Q\)-group, an outside cell can meet it only at the unique cell with
the same link colour and a quadruple sharing a triple.  For a
\((T,c)\)-group, a cell of another colour can meet it through at most its
own quadruple.  A cell of colour \(c\) but outside the group has a quadruple
meeting \(T\) in at most two points; when it meets \(T\) in two points,
exactly the two remaining points of that quadruple give the only possible
members \(T\cup\{x\}\) sharing a triple.  This proves (9).  The verifier
also exhausts the cyclic graph and confirms that both maxima are attained.
The same exact maxima \(1,2\) are attained in both \(k=6\) links.  There,
however, the two visible neighbours are the entirety of a triangle after
one vertex is removed; at \(q=13\) they are only two of twelve.  This is the
precise local reason the triangle-complement deductions stop scaling.

Several standard palette gadgets are therefore impossible in one step:

- Joining a core cell to ten anchor vertices of one \(K_{13}\) would be
  needed to restrict it to the other three colours, but (9) permits at most
  two anchors.
- A \(K_{14}\) minus one edge equality gadget would require an outside
  endpoint adjacent to twelve members of a constraint \(K_{13}\).
- Aligning two \(K_{13}\) palettes by the usual
  \(K_{12,12}\)-minus-matching construction requires cross-degree eleven.

This is stronger than the generic linear-hypergraph bound of five and rules
out the most literal inflation of the \(k=6\) proof.

There is also a general class-two construction which shows exactly why a
host-embedding condition matters.  Start with a \(K_{q+1}\) on core
vertices.  For every core edge, add \(q-2\) private vertices and declare the
resulting \(q\)-set a rainbow group.  The groups form a linear
\(q\)-uniform hypergraph, and a rainbow \(q\)-colouring would properly
\(q\)-colour its \(K_{q+1}\) core, which is impossible.

For \(q=13\), this gadget cannot embed in \(H_L\), because in fact
\[
\boxed{\omega(H_L)=13}. \tag{10}
\]
The lower bound is any constraint group.  For the upper bound, choose a cell
\(v\) in a hypothetical clique of size fourteen.  Each of the other
thirteen cells shares exactly one of the five groups through \(v\), so three
of them share one group \(E\) through \(v\).  Any further clique vertex
outside \(E\) would have to be adjacent to those three members of \(E\),
contradicting (9).  Hence the whole clique lies in \(E\), which has only
thirteen cells.

The usual Mycielski lift of a \(K_{13}\) is blocked even more directly: each
duplicate vertex would need twelve neighbours in the original
\(K_{13}\), while (9) allows at most two.

It does not rule out a multistage sparse equality gadget.

## 7. The remaining nonlinear target

Label the thirteen fan colours by \(\mathbb F_{13}\), and let \(t_v\) be
the label on cell \(v\).  A constraint group is rainbow exactly when its
multiset of labels is the whole field.  In particular it obeys the
power-sum identities
\[
 B(t^{\circ m})=0\quad(1\le m\le11),\qquad
 B(t^{\circ12})=-{\bf1},\qquad t^{\circ13}=t. \tag{11}
\]

The first-moment relaxation is consistent by (4).  Any successful
generalization now has to exploit the coordinatewise coupling among the
thirteen powers in (11), or build a sparse multistage palette gadget despite
(9).  The useful exact search target is therefore:

> Find a small set of cyclic-link groups for which the equations (11) are
> inconsistent, and minimize it to a human-checkable Schur-power or
> palette-propagation certificate.

A failure to find such a set is only a delimiter.  It is not evidence that
a fan exists.

## 8. Verification

Run:

```sh
python3 -B \
  collaboration/fan_gadget_generalization/verify_k6_linear_obstruction.py

python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_linear_delimiter.py

python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_small_trades.py
```

The first script reconstructs both \(k=6\) links, both complete fan
hypergraphs, both small gadgets, and both characteristic-\(3\)
certificates.  The second reconstructs the committed cyclic link, every
cell and group, the \(C_{17}\) quotient, exact rank and solution over
\(\mathbb F_{13}\), the expanded full-system check, and the palette-anchor
maxima.  The third exhausts every squarefree trade of support at most six.
