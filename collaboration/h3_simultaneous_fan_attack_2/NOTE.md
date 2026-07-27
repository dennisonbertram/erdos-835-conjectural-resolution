# Kernel, modular, clique, and symmetry audit of the cyclic simultaneous fan

Date: 2026-07-27

Status: **new exact reductions and delimiters; no fan construction and no
nonexistence proof.  Erdős--Rosenfeld Problem #835 remains open.**

This note attacks the exact conflict graph associated with the committed
cyclic \(LS(2,3,19)\).  It does not repeat the fan-colouring equivalence.
The new results are:

1. a universal \(969\)-dimensional row-dependency space omitted by the first
   Hoffman count;
2. the exact cyclic rank over \(\mathbb F_2\), sharpening
   \(\dim\ker B\) from \(31\,008\) to \(34\,425\);
3. an exact characteristic-\(13\) computation showing that the exact-cover
   equations \(Bx=\mathbf1\) are consistent over every prime field;
4. an exhaustive proof that the cyclic conflict graph has clique number
   exactly \(13\), so no hidden \(K_{14}\) can obstruct this link;
5. a Schur-power characterization of a fan inside the
   \(\mathbb F_{13}\) code \(\ker B\);
6. a \(C_{17}\)-invariant finite target with 2,964 variables and 1,140
   rainbow groups, together with a certificate checker.

All computations proving claims in this note are reproduced by:

```text
python3 -B \
  collaboration/h3_simultaneous_fan_attack_2/verify_fan_kernel_reduction.py
```

The verifier is standard-library-only and reconstructs the cyclic large set
from its two starters and forty phases.  It imports no repository code.

## 1. Hoffman equality is the exact-cover equation

Let \(B\) be the \(19\,380\times50\,388\) group-versus-cell incidence matrix:
there are 3,876 quadruple rows, 15,504 triple-colour rows, and every cell
belongs to five rows.  Every row contains thirteen cells.

If \(x\) is the indicator of an independent set of size 3,876, then every
quadruple group contains at most one selected cell.  Since there are exactly
3,876 such groups, every quadruple row contains exactly one.  The selected
cells have \(4\cdot3\,876=15\,504\) triple-colour incidences; independence
and the fact that there are 15,504 triple-colour rows then force exactly one
in every such row.  Therefore
\[
\boxed{Bx=\mathbf1.} \tag{1}
\]
Conversely, a zero-one solution of (1) is a maximum independent transversal.

Equivalently, regard the \(19\,380\) constraint groups as vertices and each
cell as the five-element hyperedge consisting of its five incident groups.
This gives a \(5\)-uniform, \(13\)-regular linear hypergraph
\(\mathcal G_L\), and \(H_L\) is its line graph. A binary solution of (1) is
a perfect matching of \(\mathcal G_L\), while a fan is a decomposition into
thirteen perfect matchings. Thus the exact question is whether this special
hypergraph is class one:
\[
\boxed{\chi'(\mathcal G_L)=\Delta(\mathcal G_L)=13.}
\]
The universal \(k=6\) control in `collaboration/fan_small_controls/` proves
that the analogous \(5\)-uniform, \(3\)-regular hypergraph is class two for
both possible link isomorphism types. Hence regularity and linearity alone
do not imply resolvability.

One classical sufficient condition also fails immediately.  A balanced
hypergraph has chromatic index equal to its maximum degree, but
\(\mathcal G_L\) is not balanced.  In the cyclic link, the three cells
\[
 (0123,0),\qquad(0126,0),\qquad(0136,0)
\]
and the three triple-colour groups
\[
 (012,0),\qquad(013,0),\qquad(016,0)
\]
have incidence submatrix
\[
\begin{pmatrix}
1&1&0\\
1&0&1\\
0&1&1
\end{pmatrix},
\]
a strong odd cycle of length three.  All cells are allowed and all three
groups are genuine; `verify_hypergraph_coloring_delimiters.py` checks the
witness.  Thus the balanced-matrix/perfect-line-graph shortcut cannot prove a
fan for this link.

Nor is the conflict graph perfect.  The five allowed cells
\[
(0123,0),(0124,0),(0146,0),(0168,0),(0138,0)
\]
induce a \(C_5\): consecutive quadruples share, respectively, the triples
\(012,014,016,018,013\), while each nonconsecutive pair shares only the pair
\(01\).  Thus the perfect-graph shortcut
\(\chi(H_L)=\omega(H_L)=13\) is also unavailable.  The same verifier checks
all five allowed-cell conditions and all ten induced adjacencies/nonedges.

Over \(\mathbb R\), put
\[
y=x-\frac1{13}\mathbf1.
\]
Because every row of \(B\) has sum 13, (1) is exactly \(By=0\).  Thus the
Hoffman equality vector is not merely in the least eigenspace abstractly: its
integral shape is
\[
13y\in\{-1,12\}^{50\,388},\qquad B(13y)=0. \tag{2}
\]
A fan is a resolution into thirteen such binary solutions
\[
x_0+\cdots+x_{12}=\mathbf1.
\]
The linear kernel is large; the difficulty is the simultaneous
\(\{-1,12\}\) integrality and disjointness in (2).

## 2. A universal 969-dimensional row kernel

For each triple \(T\), define a vector on the rows of \(B\) by
\[
r_T
=
\sum_{c\ne L(T)}e_{(T,c)}
-
\sum_{Q\supset T}e_Q. \tag{3}
\]
For a cell \((Q,c)\), the coefficient of that column in \(B^{\mathsf T}r_T\)
is zero unless \(T\subset Q\).  If \(T\subset Q\), the allowed-cell
condition gives \(c\ne L(T)\), and the \(+1\) from row \((T,c)\) cancels the
\(-1\) from row \(Q\).  Hence
\[
\boxed{B^{\mathsf T}r_T=0.} \tag{4}
\]

The 969 vectors are independent over every field: the triple-colour rows
appearing in \(r_T\) do not appear in \(r_{T'}\) for \(T'\ne T\).  Therefore
\[
\operatorname{rank}B\le19\,380-969=18\,411
\]
and
\[
\boxed{\dim\ker B\ge50\,388-18\,411=31\,977.} \tag{5}
\]
This improves the parameter-only lower bound \(31\,008\).  It still does not
approach a construction.

### Exact cyclic rank in characteristic two

Write a general row dependency as coefficients \(\lambda_Q\) on quadruple
rows and \(\mu_{T,c}\) on triple-colour rows.  The column equation is
\[
\lambda_Q+\sum_{T\in\binom Q3}\mu_{T,c}=0
\quad
(c\text{ allowed at }Q). \tag{6}
\]
For a fixed \(Q\), subtract one allowed-colour equation from the other
twelve.  This eliminates \(\lambda_Q\) and gives 46,512 equations in the
15,504 variables \(\mu_{T,c}\).  Conversely, every solution of those
difference equations determines each \(\lambda_Q\) uniquely, so their
nullity is exactly \(\dim\ker B^{\mathsf T}\).

For the committed cyclic link the verifier performs exact bitset Gaussian
elimination and obtains
\[
\operatorname{rank}_{\mathbb F_2}D=12\,087,
\qquad
\dim\ker_{\mathbb F_2}B^{\mathsf T}
=15\,504-12\,087
=3\,417.
\]
Consequently
\[
\boxed{
\operatorname{rank}_{\mathbb F_2}B=15\,963,\qquad
\dim\ker_{\mathbb F_2}B=34\,425.
} \tag{7}
\]
There are 2,448 characteristic-two dependencies beyond the universal 969.
They do not obstruct (1): modulo two, the all-one cell vector itself satisfies
\(B\mathbf1=\mathbf1\), because every row has odd size 13.

## 3. The prime-field modular screen is completely consistent

For any prime \(p\ne13\), the constant vector
\[
x=13^{-1}\mathbf1
\]
solves \(Bx=\mathbf1\) over \(\mathbb F_p\).  Characteristic 13 is the only
prime-field case that could carry a first-order incidence obstruction.

The cyclic link has an order-17 covariance: translate its seventeen finite
points and all colours simultaneously, fixing the other two points.  This
acts freely on the cells and rows.  Since \(17\ne0\) in \(\mathbb F_{13}\),
any row dependency \(w\) with nonzero coefficient sum could be averaged over
the group to give an invariant dependency with coefficient sum
\[
17\sum_iw_i=4\sum_iw_i\ne0. \tag{8}
\]
It is therefore enough to test invariant dependencies.

After eliminating the quadruple coefficients as in (6), the invariant system
has:

- 912 triple-colour variable orbits;
- 2,736 difference equations;
- rank 855 over \(\mathbb F_{13}\).

Let \(s\) be the linear functional that sums all row coefficients, after the
quadruple coefficients have been substituted from (6).  Appending \(s\) as
one more row leaves the rank equal to 855.  Thus \(s\) lies in the row span
and vanishes on every invariant dependency.  By (8), it vanishes on every
dependency.  The finite-field alternative then gives
\[
\boxed{Bx=\mathbf1\text{ is consistent over }\mathbb F_{13}.} \tag{9}
\]
Together with the constant solutions for \(p\ne13\), (1) is consistent over
every prime field.

The companion exact screen in `../fan_13adic_screen/` now closes the hidden
\(13^2\)-torsion possibility for this quotient.  It constructs 57 independent
integral left-row dependencies, all annihilating \(\mathbf1\), and proves
\[
\operatorname{rank}_{\mathbb Q}B_0
=\operatorname{rank}_{\mathbb F_{13}}B_0
=1083.
\]
Thus every nonzero Smith factor of \(B_0\) is a unit in
\(\mathbb Z_{13}\).  Moreover \(B_0\mathbf1=13\mathbf1\), so the cokernel
class of the right-hand side is killed by 13.  It is torsion because the 57
left dependencies annihilate it, but the Smith calculation shows that the
torsion cokernel has no 13-torsion.  The class is therefore zero:
\[
\boxed{B_0x=\mathbf1\text{ has a signed integral solution over }\mathbb Z.}
\]
The quotient solution lifts constant-on-orbits to a signed integral solution
of the full fixed-link incidence system.  Explicit compatible reductions
through \(13^6\) are also checked.  This is still only a signed linear
solution: it is neither a zero-one exact cover nor a simultaneous fan.

## 4. No clique obstruction for any fixed link

The same order-17 action has 2,964 cell orbits and 1,140 group orbits:
\[
2\,964=50\,388/17,\qquad
1\,140=19\,380/17=228+912.
\]
Every quotient group contains thirteen distinct cell orbits.  In particular,
no two adjacent full cells lie in the same cell orbit.

Project a clique in the full cyclic conflict graph to cell orbits.  The
projection is injective by the preceding observation, and adjacency projects
to adjacency in the quotient conflict graph.  Thus the full clique number is
at most the quotient clique number.

The verifier constructs the complete quotient adjacency graph and performs an
exact bitset search for a clique of size 14.  None exists.  Since every
constraint group is already a clique of size 13,
\[
\boxed{\omega(H_L)=13} \tag{10}
\]
for the committed cyclic link.  The quotient graph is not regular because
different full neighbour orbits can coalesce; its exact degree census is
\[
58^{\times257},\qquad59^{\times144},\qquad60^{\times2563}.
\]

The companion gadget audit in `../fan_gadget_generalization/` proves (10)
without cyclicity.  An outside cell has at most one neighbour in a fixed
\(Q\)-group and at most two in a fixed \((T,c)\)-group.  In a hypothetical
14-clique, choose a cell \(v\).  Among the other thirteen cells, three share
one of the five constraint groups through \(v\).  Any remaining clique cell
outside that group would have three neighbours inside it, contradicting the
preceding sharp bound.  Hence every clique has size at most thirteen, while
every constraint group attains thirteen.

Equation (10) therefore closes the larger-clique route for every fixed link.
It says nothing about chromatic number 13 versus greater than 13 through
non-clique mechanisms.

## 5. A Schur-power formulation in characteristic 13

Let
\[
\mathcal C=\ker_{\mathbb F_{13}}B
\subseteq\mathbb F_{13}^{50\,388}
\]
and write powers coordinatewise.  A fan labelling
\(f:\mathcal V_L\to\mathbb F_{13}\) makes each group contain every field
element once.  Therefore
\[
Bf^k=0\quad(1\le k\le11),
\qquad
Bf^{12}=-\mathbf1. \tag{11}
\]

These equations are also sufficient.  For one row, let its thirteen entries
be \(a_1,\ldots,a_{13}\), with power sums \(p_k\).  Equations (11) say
\[
p_1=\cdots=p_{11}=0,\qquad p_{12}=-1.
\]
Newton's identities are valid for \(1,\ldots,12\) in
\(\mathbb F_{13}\) and give
\[
e_1=\cdots=e_{11}=0,\qquad e_{12}=-1.
\]
Hence
\[
\prod_i(z-a_i)=z^{13}-z-e_{13}.
\]
Every \(a_i\in\mathbb F_{13}\) satisfies \(a_i^{13}-a_i=0\), so substituting
any one of the thirteen entries forces \(e_{13}=0\).  The polynomial is
\(z^{13}-z\), whose roots are the thirteen distinct field elements.  Thus
the row is rainbow.

We obtain the exact nonlinear code target
\[
\boxed{
\text{fan}
\iff
\exists f:
f,f^2,\ldots,f^{11}\in\mathcal C,\quad
Bf^{12}=-\mathbf1.
} \tag{12}
\]
For each \(a\in\mathbb F_{13}\), the corresponding exact-cover indicator is
\[
x_a=1-(f-a)^{12}.
\]

This separates the live obstruction from the large linear kernel: one needs
a vector whose first eleven Schur powers remain in the code and whose
twelfth power lands in a specified affine coset.  Ordinary rank, Hoffman
equality, and first-order parity do not test this.

## 6. The exact \(C_{17}\)-invariant fan target

Requiring the fan labels to be constant on the 2,964 cell orbits is a
restricted ansatz, not a without-loss reduction.  In that ansatz a fan is
exactly a labelling of the 2,964 quotient cells by \(0,\ldots,12\) such that
each of the 1,140 quotient groups is rainbow.

The quotient incidence matrix \(B_0\) has rank
\[
\operatorname{rank}_{\mathbb F_{13}}B_0
=228+855
=1\,083,
\]
so its power code has dimension
\[
\boxed{\dim\ker_{\mathbb F_{13}}B_0=2\,964-1\,083=1\,881.} \tag{13}
\]

A certificate is simply 2,964 integers, in the canonical orbit order emitted
by the verifier.  If
`cyclic_invariant_fan.txt` is present, the standard-library verifier checks
all 1,140 rainbow groups and thereby checks the lifted full 13-fan
semantically.

The smallest direct certificate-producing SAT target has:

- \(2\,964\cdot13=38\,532\) primary label variables;
- \(2\,964\cdot12=35\,568\) Sinz auxiliaries;
- 74,100 variables total;
- 2,964 cell at-least-one clauses;
- \(2\,964(3\cdot13-4)=103\,740\) cell at-most-one clauses;
- \(1\,140\cdot13=14\,820\) group-label coverage clauses;
- 13 lossless global label-symmetry units;
- \(\boxed{121\,537}\) clauses total.

Coverage is sufficient: a group has thirteen cells, every cell has exactly
one label, and all thirteen labels occur, so each occurs exactly once.  A SAT
model gives a portable 2,964-line semantic certificate.  A proof-checked UNSAT
result excludes only \(C_{17}\)-invariant fans over this fixed cyclic link.

`write_cyclic_invariant_fan_cnf.py` emits three equivalent deterministic
encodings, all independently reconstructed byte-for-byte by
`../h3_k6_fan_theorem_audit/verify_cyclic_cnf_audit.py`:

| encoding | variables | clauses | SHA-256 |
|---|---:|---:|---|
| sequential cell AMO | 74,100 | 121,537 | `b247b458dfeb3daff7c37046bd2def635601e26737761f5450541722dccb85a5` |
| plus conflict-edge AMO | 74,100 | 1,273,220 | `896d975b3246202daa0b1d6fd101e60d3f53814dc4f50ea1ada859f5715d2591` |
| direct cell AMO plus conflict-edge AMO | 38,532 | 1,400,672 | `74ac2417ffdc1410075faabb5d2292969f2247566583980ed46f777f98bc9249` |

The hardened decoder accepts only an exact `s SATISFIABLE` status and then
checks the combinatorial certificate directly: one label per orbit cell and
all 1,140 groups rainbow.

## 7. Search result and next exact target

The optional OR-Tools helper
`search_cyclic_invariant_fan.py` was run for 60 seconds with eight workers
after fixing one quotient group to the thirteen labels.  It returned
`UNKNOWN`, with no candidate.  This has no negative mathematical status.
No `cyclic_invariant_fan.txt` is claimed.

A second finite screen tested 272 translation-invariant rank formulae.  For
each quadruple it cyclically orders the thirteen allowed colours around an
anchor blending the finite-point barycentre and the face-colour barycentre;
the rank is automatically rainbow on every \(Q\)-group.  None was rainbow on
all \((T,c)\)-groups.  The best collision score was 4,098.  This excludes only
that explicit formula family and is not evidence of global infeasibility.

The exact next targets, in order, are:

1. seek either a semantically checked 2,964-line model or a proof-checked
   UNSAT certificate for the independently audited CNFs above;
2. attack the nonlinear Schur-power intersection (12), rather than another
   ordinary rank or Hoffman calculation;
3. if the invariant ansatz fails, return to the unrestricted 50,388-cell
   resolution problem.  Invariant UNSAT would not exclude nonsymmetric fans,
   other links, \(LS(3,4,20)\), \(k=16\), or Problem #835.

No construction or nonexistence theorem is asserted.

## 8. Necessary first step: one invariant matching

Before resolving all thirteen colour classes simultaneously, one can ask for
one binary solution of
\[
B_0x=\mathbf1,\qquad x\in\{0,1\}^{2964}. \tag{14}
\]
The first 228 quotient groups partition the cells, so (14) chooses exactly
one cell above every quadruple orbit.  The remaining 912 equations require
these choices to hit every triple-colour orbit exactly once.  A solution is
one \(C_{17}\)-equivariant \(LS(3,4,20)\) extending the fixed cyclic link;
equivalently, it is one perfect matching of the quotient hypergraph.  It is
necessary for an invariant fan but is neither a fan nor a solution of
Problem #835.

The deterministic exact-cover CNF for (14) has 3,876 phase variables:
2,964 allowed phases and 912 forbidden phases forced false.  It uses no
auxiliary variables and has 33,060 clauses.  Its independently audited digests
are:

```text
CNF  860aba8e26b2ec8c0fdbe268e5a19cac63647ef3593b123d7a12c5dec63eccf2
map  2908c7b90fc14a5229600b359fddf7e874f8665418b7e85ed94215143abab358
```

Four 600-second local-search runs did not find a matching; their best
collision scores were 51, 53, 51, and 54.  The extended 272-formula screen
tested all thirteen rank classes and attained 237.  The Boolean fan CP-SAT
model also returned only `UNKNOWN` after 964 seconds.  These are search
statistics, not negative mathematical evidence.

The exact single-matching CP-SAT model subsequently ran for one hour and
returned `UNKNOWN` after 22,236,271 conflicts and 42,619,484 branches.  Two
independently audited MIP variants give complementary reconnaissance: the
exact variant has 2,964 binary variables and all 1,140 equalities, while the
soft variant keeps the 228 Q equations hard and minimizes the exact integer
L1 defect of the remaining 912 equations.  A SCIP smoke reproduced the
score-54 hint at semantic L1 defect 108.  Only a semantically verified
zero-defect incumbent can write a certificate; backend-local `INFEASIBLE`,
timeouts, positive defects, and unknown status codes are explicitly
inconclusive.

The C++ witness hunter `search_c17_matching_two_opt.cpp` supplements the
exact solvers.  It searches Q-transversals under the collision objective and
exhausts improving changes of one, two, or three Q variables.  Because
\(\binom n2\) is quadratic, a combined delta is the sum of the individual
deltas and all pairwise coordinate interactions.  Opposite-sign incidence
indices make the two-change screen exhaustive.  After singles and pairs fail,
each interaction is at least \(-8\), so any improving triple has a constituent
negative-interaction pair of combined delta at most 15; the third move must
also share an opposite-sign affected group.  These facts make the sparse
three-change enumeration exhaustive.

The implementation passed 12,500 randomized one/pair delta checks and an
independent sparse-versus-brute comparison on 1,976,000 sampled triples.  A
positive control found the same unique improving triple of delta \(-1\) by
both methods.  The score-54 hint has no improving one-, two-, or three-Q
change.  This is only a local-optimality certificate for one best effort,
not a global lower bound; the timed witness search wrote no model.

Long CaDiCaL and Kissat searches on both exact-cover encodings, and a
diversified fan search, remain the current computational frontier.  None has
yet produced a model or a proof.
