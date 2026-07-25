# Exact cyclic-17 reduction for the first open case

This note tests a genuine colour-transitive symmetry for
Erdős--Rosenfeld problem 835 at \(k=16\).  It does **not** assume that every
solution has this symmetry.

Let the 32 points be
\[
 A\sqcup F,\qquad A=\mathbb Z_{17},\quad |F|=15,
\]
and suppose translation \(x\mapsto x+1\) on \(A\), fixing \(F\), sends every
colour \(q\) to \(q+1\).  A tight colouring is the same as a large set
\(LS(15,16,32)\).

## 1. The exact starter formulation

Write \(D\) for colour zero.  No 16-subset is fixed by the translation, so
every block orbit has length 17.  Equivariance is therefore equivalent to:

1. \(D\) contains exactly one block from every translation orbit; and
2. \(D\) is an \(S(15,16,32)\).

Indeed, the seventeen translates of such a starter are disjoint, cover every
16-subset, and are all Steiner systems.

For a completely explicit zero-one formulation, write a block as
\((X,Y)\), where \(X\subseteq A\), \(Y\subseteq F\), and
\(|X|+|Y|=16\), and let \(d(X,Y)\) be its indicator in \(D\).  The two
conditions are
\[
 \sum_{t\in\mathbb Z_{17}}d(X+t,Y)=1                                      \tag{1}
\]
for every block orbit, and
\[
 \sum_{a\in A\setminus U}d(U\cup\{a\},V)
 +\sum_{f\in F\setminus V}d(U,V\cup\{f\})=1                              \tag{2}
\]
for every \(15\)-set \((U,V)\).  Equations (1)--(2) are an exact quotient,
not a relaxation.

## 2. Complement closure is forced

Complement closure is not an extra ansatz here.  The degree of
\(J(32,16)\) is \(256\), its least eigenvalue is \(-16\), and a
17-colouring attains the Hoffman bound.  Hence the centred indicator of
each colour class lies in the last Johnson eigenspace \(E_{16}\).  The
complement permutation acts on \(E_j\) as \((-1)^j\), so it acts as \(+1\)
on \(E_{16}\).  Consequently
\[
             c(B)=c(B^c)                                                  \tag{3}
\]
for every 16-set \(B\).

This pairs the two block layers described below.  It does not by itself
construct the middle layer or prove that the cyclic symmetry exists.

## 3. Layer recursion

It is more convenient to record the omitted fixed points.  For
\(R\subseteq F\), \(|R|=s\), and \(X\subseteq A\), \(|X|=s+1\), set
\[
 C_R(X)=c\bigl(X\cup(F\setminus R)\bigr).
\]
Equivariance says
\[
 C_R(X+t)=C_R(X)+t.                                                        \tag{4}
\]
After translating the origin, the first layer is
\(C_\varnothing(\{x\})=x\).

For \(|U|=|R|=s\), the rainbow condition on the corresponding 15-set is
exactly
\[
 \{C_{R\setminus\{f\}}(U):f\in R\}
 \mathbin{\dot\cup}
 \{C_R(U\cup\{a\}):a\in A\setminus U\}
 =\mathbb Z_{17}.                                                         \tag{5}
\]
Thus the construction proceeds one block layer at a time.

In colour-zero form, let
\[
 {\cal D}_R=\{X:C_R(X)=0\}.
\]
Equation (4) says that \({\cal D}_R\) chooses one translate from every
\((s+1)\)-subset orbit.  If the already constructed colours in the first
set of (5) are distinct, define their zero leave
\[
 L_R=\{U: C_{R\setminus\{f\}}(U)=0\text{ for some }f\in R\}.
\]
Then (5), for all colours, is equivalent to the finite exact cover
\[
 \#\{X\in{\cal D}_R:U\subset X\}=
 \begin{cases}
 0,&U\in L_R,\\
 1,&U\notin L_R.
 \end{cases}                                                              \tag{6}
\]
After all \(R\)'s of one size have been chosen, the colours supplied to the
next layer must also be pairwise distinct.  This cross-\(R\) compatibility
is essential; solving (6) independently for every \(R\) is not enough.

Complement closure becomes
\[
 C_R(X)=C_{F\setminus R}(A\setminus X).                                   \tag{7}
\]
One may therefore choose layers \(|R|\le 7\), reflect them by (7), and
then impose the remaining middle compatibility between the
\(|R|=7\) and \(|R|=8\) layers.  Equivalently, the colour-zero starter must
be an independent set in \(J(32,16)\); its forced size then makes it an
\(S(15,16,32)\).

In the low-layer coordinates this last condition is concrete.  Two selected
level-seven blocks \((R,X)\) and \((R',X')\), with
\(|R|=|R'|=7\) and \(|X|=|X'|=8\), may not satisfy
\[
                 R\cap R'=\varnothing,\qquad X\cap X'=\varnothing,         \tag{8}
\]
because the first block is adjacent to the complement of the second.
All other high-layer independence conditions are complements of conditions
already imposed in the low layers.

## 4. The first two nontrivial layers

For \(R=\{i\}\), equation (5) says that
\[
 S_i(x,x)=x,\qquad S_i(x,y)=C_{\{i\}}(\{x,y\})
\]
is a translation-equivariant symmetric idempotent Latin square on
\(\mathbb Z_{17}\).  Cross-\(R\) compatibility says that the fifteen
squares form a golf design \(G(17)\).  This conclusion is forced by the
17-cycle.

The current computation fixes the explicit Wallis circulant \(G(17)\)
already audited in `global_latin_audit.py`.  Choosing that particular golf
design is an ansatz, not a without-loss-of-generality step.

For \(R=\{i,j\}\), there are 40 translation orbits of moving triples.
Equation (6) asks for one translate from each orbit which decomposes
\(K_{17}\) minus the two colour-zero one-factors belonging to \(S_i,S_j\).
Adjoin two points \(i,j\).  The selected moving triples, the triples
\(\{i,x,y\}\) and \(\{j,x,y\}\) from those two one-factors, and
\(\{i,j,0\}\) form an \(STS(19)\).  Translating produces a cyclic
\(LS(2,3,19)\) with the two prescribed links.  This equivalence gives a
small, independently checkable 40-phase model for each fixed pair.

Single slices do not glue automatically.  For each moving-triple orbit,
the 40 phases on the 105 edges of \(K_{15}\) must, separately, be proper
edge-colourings: phases on two fixed-pair edges sharing a fixed point must
differ.  The `--joint` model imposes exactly this condition together with
all 105 slice exact covers.  It has 4,200 phase variables, represented by
71,400 primary one-hot variables in the direct Boolean encoding.

There is also a substantially smaller exact integer encoding.  The moving
edges split into eight translation orbits, indexed by their undirected
differences \(d=1,\ldots,8\).  Across the forty moving-triple orbits, one
representative contains exactly fifteen edge occurrences of each difference.
This count is independent of the selected translates.  One way to see it is
that each of the seventeen edges of difference \(d\) lies in fifteen moving
triples, giving \(17\cdot15\) incidences; dividing by the common
translation-orbit length \(17\) leaves fifteen.

For every golf square and difference \(d\), translation covariance gives
exactly one colour-zero edge position.  Thus a fixed pair of golf squares
forbids two positions and leaves fifteen.  After the phase domains exclude
those two forbidden positions, exact coverage in difference class \(d\) is
equivalent simply to requiring its fifteen selected edge positions to be
pairwise distinct.  Hence the whole joint layer has the equivalent compact
form
\[
 \begin{array}{rcl}
 4{,}200&&\text{phase integers},\\
 12{,}600&&\text{modular edge-position auxiliaries},\\
 105\cdot8=840&&\text{slice }{\rm AllDifferent}(15)\text{ constraints},\\
 15\cdot40=600&&\text{cross-slice }{\rm AllDifferent}(14)\text{ constraints}.
 \end{array}                                                             \tag{9}
\]
The compact model removes the one-hot variables without relaxing or
strengthening the fixed-Wallis, cyclic joint problem.

The cross constraints have an equivalent round-robin interpretation.  For a
triple orbit \(q\) and golf square \(i\), let \(F_i(q)\) be the three phases
at which the translated triple contains an edge of the colour-zero matching
of \(i\).  Then the phase domain on fixed edge \(ij\) is exactly
\[
       \mathbb Z_{17}\setminus(F_i(q)\cup F_j(q)).
\]
For a fixed phase \(c\), the \(c\)-labelled edges of \(K_{15}\) must form a
perfect matching on the fixed vertices \(i\) with \(c\notin F_i(q)\).
Fourteen phases have twelve such vertices and the three phases at which the
moving triple contains \(0\) have fourteen.  Thus every orbit decomposes
\(K_{15}\) into fourteen matchings of size six and three matchings of size
seven.  Across all forty orbits, the 120 singleton holes meet every fixed
vertex eight times.  The 560 three-vertex holes form a
\(2\text{-}(15,3,16)\) multidesign: every fixed vertex occurs 112 times and
every fixed pair 16 times.  (There are 336 distinct hole triples, with
multiplicities from one through five.)  Consequently every fixed pair has
exactly 456 allowed phases across its forty cells.

The executable audit also records the exact phase-domain distribution
\[
  2{,}658\text{ domains of size }11,\quad
  1{,}407\text{ of size }12,\quad
  132\text{ of size }13,\quad
  3\text{ of size }14,
\]
totalling \(47{,}880\) allowed phase values.  This is a reformulation of the
600 cross `AllDifferent` constraints, not an additional assumption.

There is a useful exact intermediate problem between one row and the whole
joint layer.  Fix one Wallis square \(i\).  Its fourteen incident pair rows
\(\{i,j\}\) must be exact simultaneously, and their phases must be distinct
in each of the forty triple orbits.  Equivalently, those fourteen rows
partition the 560 moving triples whose three edges avoid the zero one-factor
of \(i\).  The compact **star model** has 560 phase integers, 1,680 modular
edge-position auxiliaries, 112 row `AllDifferent(15)` constraints, and 40
cross `AllDifferent(14)` constraints.  Its independent direct SAT encoding
has 6,384 primary variables, 35,504 variables in all, and 87,360 clauses.
Every joint layer restricts to a solution of all fifteen stars.  Thus a
portable infeasibility proof for one star would exclude this fixed-Wallis
cyclic ansatz, while a star witness remains only a necessary local piece.

Taking the sum of each forced permutation gives a useful exact linear
shadow over \(\mathbb F_{17}\): 840 slice equations and 600 cross-slice
equations in the 4,200 phases.  The stdlib-only audit finds rank 1,320 and
nullity 2,880, and the augmented system is consistent.  Thus these
first-moment equations do not obstruct the joint layer.

There are exactly 120 dependencies among those 1,440 rows.  Applying every
dependency to the corresponding squared permutation identities cancels all
quadratic phase terms and produces 120 further linear equations.  The exact
audit finds that all 120 are consistent and add no rank beyond 1,320.
Consequently even every linear consequence obtainable by this
second-moment cancellation supplies no obstruction.

Another strict necessary relaxation keeps the phase lists and cross-slice
permutations but replaces each full residual-edge decomposition by its vertex
degrees.  The two zero one-factors avoid moving point \(0\), so their
complement has degree \(16\) at \(0\) and degree \(14\) at every other moving
point.  A triangle decomposition must therefore select triples containing
\(0\) eight times and every other point seven times, for each of the 105
fixed pairs.  The deterministic compact CNF for this relaxation has
47,880 primary variables, 2,033,640 total variables, and 4,094,160 clauses.
It deliberately omits all 12,600 edge-position collision constraints.
SAT would provide a degree-correct search seed; independently proof-checked
UNSAT would exclude the fixed-Wallis cyclic ansatz, not problem 835.

The cross permutations make 345 of those 1,785 degree equations redundant.
For each golf square \(i\), their aggregate forces the sum of the fourteen
incident fixed-pair degree vectors to be \(112\) at moving point \(0\) and
\(98\) elsewhere.  It is therefore enough to impose the first sixteen moving
points on ninety fixed-pair edges.  Omit
\[
 \{01,12,02\}\cup\{0k:3\le k\le14\}.
\]
The twelve leaves first recover the twelve omitted star-edge deviations; the
remaining odd triangle then forces its three deviations to zero.  A reduced
proof-capable CNF uses 47,880 primary variables, 656,559 variables in all,
and 1,739,128 clauses.  Its deterministic DIMACS SHA-256 is
`244df53753926be6e2bc64cdb5d25b7a6838276f86c967ae24d03f3b2c476543`.
This remains exactly the vertex-degree relaxation: it contains no
edge-position collision constraints.

There is no additional safe relabelling symmetry to break after fixing the
Wallis starter.  An exact audit of its fifteen zero one-factors first uses
pairwise union-cycle-profile multisets to distinguish thirteen factor labels.
Labels 2 and 11 have the sole duplicate signature, but their different pair
profiles with the already distinguished label 1 forbid swapping them.  The
image of one moving point then determines a candidate point permutation;
checking all sixteen candidates leaves only the identity.  Thus the
automorphism group of this labelled quotient instance has order one.

## 5. Four scopes that must not be conflated

1. **One fixed-pair slice.**  This is one prescribed-link cyclic
   \(LS(2,3,19)\).  It proves only that one \(R=\{i,j\}\) slice is feasible.
2. **The joint moving-triple layer.**  All 105 slices plus the shared
   phase constraints are exactly the translation-equivariant,
   fixed-Wallis-golf radius-five boundary.  Even a certificate here reaches
   only \(|R|=2\).
3. **A cyclic \(LS(4,5,21)\).**  Fixing eleven of the fifteen fixed points
   in a hypothetical full large set gives this necessary derived design.
   It is a different finite shadow; finding it would not supply the joint
   layer above or a full \(LS(15,16,32)\).
4. **Erdős--Rosenfeld 835.**  A positive solution requires all layers
   through \(|R|=7\), their complements, and the middle compatibility.
   A no-go for the Wallis golf starter, or even for every cyclic-17
   starter, would not rule out a nonsymmetric tight colouring.

## 6. Reproducible commands

The search and semantic checks are in
`evidence/search_cyclic17_r3_extension.py`.

```sh
# A diagnostic single slice.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --only-fixed-pair 0,1 --sat-solver maplechrono \
  --output /tmp/cyclic17-r3-01.json

# Recheck a partial certificate without asserting that all 105 exist.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --verify evidence/cyclic17_r3_pair_0_1_certificate.json \
  --only-fixed-pair 0,1

# Solver-independent reconstruction and incidence audit of its LS(2,3,19).
python3 -B evidence/verify_cyclic17_r3_pair.py \
  evidence/cyclic17_r3_pair_0_1_certificate.json --fixed-pair 0,1

# The genuinely coupled layer.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --joint --sat-solver maplechrono \
  --output /tmp/cyclic17-r3-joint.json

# Preserve all 105 exact slices while optimizing their cross compatibility.
python3 -B evidence/improve_cyclic17_exact_slices_cross_lns.py \
  /tmp/cyclic17-row-exact-seed.json \
  /tmp/cyclic17-exact-slice-cross-lns.json \
  --sweeps 5 --seconds-per-pair 2 --accept-equal

# Equivalent compact 4,200-phase integer model.
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_cyclic_compact.py \
  --seconds 1200 --workers 8 \
  --phase-output /tmp/cyclic17-compact-phases.json \
  --certificate /tmp/cyclic17-compact-radius5.json

# Independent compact CNF of the same quotient.
python3 -B \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_compact_sat.py \
  --solver maplechrono \
  --phase-output /tmp/cyclic17-compact-sat-phases.json \
  --certificate /tmp/cyclic17-compact-sat-radius5.json

# Exact parity shadow of that joint model.
python3 -B evidence/audit_cyclic17_r3_mod2.py

# Exact first-moment shadow over F_17.
python3 -B evidence/audit_cyclic17_phase_sums_mod17.py

# Necessary vertex-degree SAT relaxation.
python3 -B \
  evidence/odd_graph_local_ball/search_cyclic17_vertex_degree_sat.py \
  --solver kissat404 --output /tmp/cyclic17-vertex-degree.json

# Equivalent smaller degree relaxation, with deterministic DIMACS support.
python3 -B \
  evidence/odd_graph_local_ball/search_cyclic17_vertex_degree_reduced_sat.py \
  --dimacs /tmp/cyclic17-vertex-degree-reduced.cnf --audit-only

# Alternate projections onto the 105 exact rows and 40 exact columns.
python3 -B \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_alternating_projection.py \
  /tmp/cyclic17-row-projector /tmp/cyclic17-cross-seed.json \
  --row-fallback evidence/cyclic17_all_105_exact_slices_cross_seed.json \
  --iterations 5

# Lagrangian row/column decomposition.  Its dual value is rigorous only
# when every one of the 105+40 weighted subproblems reports OPTIMAL.
python3 -B \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_lagrangian.py \
  /tmp/cyclic17-row-projector \
  evidence/cyclic17_all_105_exact_slices_cross_seed.json \
  /tmp/cyclic17-cross-seed.json --iterations 5

# Exact audit of the second-moment identity suggested by Opus 5.
python3 -B evidence/audit_cyclic17_opus_second_moment.py

# One exact 14-row star, in compact CP-SAT and independent direct SAT forms.
python3 -B \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_star.py \
  --centre 0 \
  --source evidence/cyclic17_all_105_exact_slices_cross_seed.json
python3 -B \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_star_sat.py \
  --centre 0 \
  --source evidence/cyclic17_all_105_exact_slices_cross_seed.json \
  --solver maplechrono
clang++ -O3 -std=c++17 \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_star_exact_cover.cpp \
  -o /tmp/cyclic17-star-dlx
/tmp/cyclic17-star-dlx --centre 0 --seconds 600 --seed 835

# If the joint search succeeds, convert and run the independent semantic
# radius-five ball verifier.
python3 -B evidence/convert_cyclic17_r3_to_radius5.py \
  /tmp/cyclic17-r3-joint.json /tmp/o16-r5-cyclic17.json
```

As of this note, all 105 slices have independently verified exact-cover phase
witnesses.  The combined row-exact seed has SHA-256
`7ddb20ec2ab02cd2dd029276c6df75dd425d5c1588c7b58c659299311dc8cdc5`;
every slice selects 40 triples, covers its 120 residual edges exactly, and has
moving-vertex degree vector \((8,7,\ldots,7)\).  A weighted, row-preserving
Algorithm-X search improves the shared-phase score to 5,928 of 8,400, with
2,935 collision pairs and SHA-256
`640ad301772b3224b7466e43bec5c659455b08af58d3178260efbff7b1bbcabb`.
The independent verifier still finds no conflict-free one of the 600 cross
groups, so this is not a joint witness.
The checked-in \((0,1)\) certificate has SHA-256
`64d910594b1307ac5a5f58d2dfe5aec468080a90bcd65be5bbd5c012da33529a`.
The joint GF(2) linearization is consistent: its 28,680 equations have rank
23,352 on 71,400 variables.  Thus parity supplies no obstruction at this
layer.  A cross-compatible orbit-LNS/Kempe seed covers 9,975 of the 12,600
required residual edges; the gap of 2,625 means it is not a joint witness,
and none of its 105 slices is exact.  Its SHA-256 is
`6c86fcdc5fdd0c6a74b45992a4a23c03859c86fd7a56cac450a27ebbf660b520`.
The first compact CP-SAT run returned `UNKNOWN` after 1,207 seconds,
6,460,436 branches, and 1,041,651 conflicts.  That is search status only.
Two further 1,805-second compact hinted runs also returned `UNKNOWN`, after
about 9.5 million branches each.  Alternating exact-family projection found
no witness; its best row/column Hamming gap was 2,184 of the 4,200 phase
cells.  Fixing the 1,982 cells on which its last two family states agreed
made that conditioned subproblem infeasible in presolve, but this is only a
seed-core rejection and has no consequence for the unconditioned ansatz.

The Opus-proposed forbidden-phase second-moment identity has also been settled
exactly.  With zero-sum triple representatives,
\(\Phi_i^{(2)}=0\) for every Wallis square, while the natural zero-factor
first moment is \(s_i=-1\) for every square.  Its proposed equation is
therefore the tautology \(0=0\) and supplies no new rank or obstruction; the
independent audit is in `evidence/cyclic17_opus_second_moment_audit.md`.
The tightened compact integer and independent compact SAT searches continue.
None of these facts settles problem 835.

## 7. Related primary literature

- K. T. Phelps, [*Cyclic large sets of Steiner triple systems of order
  15*](https://electronicsandbooks.com/edt/manual/Magazine/M/Mathematics%20of%20Computation/1960-2002/pdf/1990_v055_n192/2008449.pdf),
  *Mathematics of Computation* **55** (1990), 821--824.  This is the direct smaller-order
  analogue of the prescribed-link cyclic starter formulation used for one
  fixed-pair slice.
- G. Erskine and T. S. Griggs, [*Cycle switching in Steiner triple systems of
  order 19*](https://arxiv.org/abs/2405.07750) (2024).  Its cycle trades
  motivate the orbit-respecting exact-cover trade search, but its connectivity
  theorem does not preserve our two prescribed links or the cyclic-orbit
  starter condition.
