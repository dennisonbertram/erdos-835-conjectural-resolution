# Fixed-Wallis \(C_{17}\) vertex-degree structure

This note concerns only the necessary vertex-degree relaxation of the
fixed-Wallis, \(C_{17}\)-equivariant \(r=3\) layer.  It is not the complete
radius-five quotient and is not a solution or refutation of
Erdős--Rosenfeld problem 835.

## 1. Cross phases are prescribed-hole one-factorizations

Fix one of the forty translation orbits of moving triples, represented by
\(T\subset\mathbb Z_{17}\), and one Wallis golf square \(i\).  The square's
colour-zero edges are a matching \(M_i\) of the sixteen nonzero moving
points.  Exactly three shifts \(s\) make \(T+s\) contain an edge of \(M_i\);
write this three-set as \(F_i(T)\).

For this orbit, the phase on a fixed-pair edge \(ij\) avoids
\(F_i(T)\cup F_j(T)\).  At fixed vertex \(i\), its fourteen incident edges
have distinct phases, all in the fourteen-set
\(\mathbb Z_{17}\setminus F_i(T)\).  They therefore use every allowed phase
exactly once.

Equivalently, for each phase \(s\), let
\[
 B_s(T)=\{i:s\in F_i(T)\}.
\]
The pair-edges of phase \(s\) form a perfect matching on
\(\{0,\ldots,14\}\setminus B_s(T)\).  If \(0\in T+s\), then
\(|B_s(T)|=1\); otherwise \(|B_s(T)|=3\).  Thus every orbit is a
decomposition of \(K_{15}\) into three matchings of size seven and fourteen
matchings of size six, with the holes prescribed by the golf design:
\[
              3\cdot7+14\cdot6=105.
\]

This justifies replacing the old cross-phase `AtMostOne` groups by 8,400
direct `ExactlyOne` groups.  The replacement is equivalent, not a
strengthening.

Across all forty orbits, the 120 singleton holes hit each golf square eight
times.  The 560 three-point holes form a \(2\)-\((15,3,16)\) multidesign:
each golf square occurs 112 times and each pair of golf squares occurs
sixteen times.  For the pair count, the union of two distinct zero matchings
is a disjoint union of even cycles; each of its sixteen vertices is the
unique centre of a length-two path whose two edge colours are the given
squares.  It follows that every fixed pair has \(456\) allowed
triple-translates across all forty orbits, and hence that the exact total
number of primary phase literals is \(105\cdot456=47,880\).

## 2. Forced aggregate degree identity

Let \(d_{ij}(x)\) be the number of the forty selected translated triples in
fixed-pair slice \(ij\) which contain moving point \(x\).  Because the
fourteen phases incident with \(i\) exhaust the allowed shifts, their
aggregate over all forty triple orbits is fixed.

All \(40\cdot17=680\) translated representatives are precisely all triples
of \(\mathbb Z_{17}\).  The excluded triples are precisely those containing
one of the eight edges of \(M_i\).  A triple cannot contain two matching
edges, so there are \(8\cdot15=120\) such triples.

Every moving point occurs in \(\binom{16}{2}=120\) triples.  Point \(0\)
occurs in eight excluded triples, one for each edge of \(M_i\).  A nonzero
point occurs in fifteen excluded triples through its own matching edge and
in seven more as the third point on another matching edge.  Consequently
\[
 \sum_{j\ne i}d_{ij}(x)=
 \begin{cases}
 120-8=112=14\cdot8,&x=0,\\
 120-22=98=14\cdot7,&x\ne0.
 \end{cases}                                                   \tag{1}
\]

This identity is forced by the cross-phase constraints before any individual
slice degree equations are imposed.

## 3. An exact 1,440-equation basis

Put
\[
 \delta_{ij}(x)=d_{ij}(x)-(8\text{ if }x=0\text{ else }7).
\]
Equation (1) gives
\[
                  \sum_{j\ne i}\delta_{ij}(x)=0                \tag{2}
\]
for every fixed point \(i\) and moving point \(x\).  Also,
\(\sum_x\delta_{ij}(x)=0\), because each slice selects forty triples and
therefore has total incidence \(120\).

Omit the following fifteen fixed-pair edges:
\[
 H=\{01,12,02\}\cup\{0k:3\le k\le14\}.
\]
Enforce \(\delta_{ij}(x)=0\) only for the other ninety pair-edges and only
for \(x=0,\ldots,15\).  For each such \(x\), equation (2) at vertices
\(3,\ldots,14\) first forces the twelve star-edge deviations in \(H\) to
zero.  The equations at \(0,1,2\) then force the three triangle deviations
to zero.  Finally the total-incidence identity forces the omitted
\(x=16\) equation on every pair-edge.

Hence the original \(105\cdot17=1,785\) degree equalities are exactly
equivalent, in the presence of the phase and cross constraints, to
\[
                       90\cdot16=1,440                         \tag{3}
\]
equalities.  This is the full rank predicted by the two universal
identities: \((105-15)(17-1)=1,440\).

## 4. Audited reduced models

The compact CP-SAT model is
`odd_graph_local_ball/search_cyclic17_vertex_degree_reduced.py`.  Its audit
reports:

```text
47,880 primary Booleans
4,200 phase ExactlyOne constraints
8,400 cross ExactlyOne constraints
1,440 vertex-degree equalities
116,010 degree literal memberships
```

The proof-capable Boolean model is
`odd_graph_local_ball/search_cyclic17_vertex_degree_reduced_sat.py`.  It
introduces one membership variable for “the selected translate in this
orbit contains this point”, reducing every degree cardinality to at most
forty inputs.  Its audited counts are:

```text
47,880 primary phase variables
56,453 nonconstant membership variables
656,559 total variables
1,739,128 clauses
```

The earlier direct cardinality formula has 2,033,640 variables and
4,094,160 clauses.  Thus the new formula uses about 32% as many variables
and 42% as many clauses, with no change in solution set.

Reproduce the audits with:

```sh
python3 -B evidence/audit_cyclic17_vertex_degree_structure.py

python3 -B \
  evidence/odd_graph_local_ball/search_cyclic17_vertex_degree_reduced.py \
  --audit-only

python3 -B \
  evidence/odd_graph_local_ball/search_cyclic17_vertex_degree_reduced_sat.py \
  --audit-only --dimacs /tmp/cyclic17-vertex-degree-reduced.cnf
```

The deterministic DIMACS generated in the recorded run has SHA-256

```text
244df53753926be6e2bc64cdb5d25b7a6838276f86c967ae24d03f3b2c476543
```

and size 36 MiB.  A 182-second CP-SAT run on the reduced model returned
`UNKNOWN`; this has no mathematical meaning.  Exact SAT searches are still
required to produce either a semantically verified degree-correct phase
seed or a portable checked UNSAT proof.

## 5. No residual zero-factorization relabelling symmetry

The stdlib audit also checks the full automorphism group of the fifteen
Wallis colour-zero matchings on the sixteen nonzero moving points.  For two
matching factors, use the cycle-length multiset of their union as an
edge-colour on the fifteen zero-based factor labels.  The incident
edge-colour multisets distinguish thirteen factors immediately; only
factors 2 and 11 share a fingerprint.  Factor 1 is already distinguished,
and its union profiles with factors 2 and 11 differ, so those two cannot be
exchanged.
Thus every matching factor is fixed.

After the factors are fixed, a point automorphism is determined by the image
of point 1, because the fifteen matching mates of point 1 are all the other
points.  Checking the sixteen possible images leaves only the identity.
Therefore the zero-factorization automorphism group has order one.  In
particular, there is no nontrivial point/fixed-square relabelling symmetry
left to break in this fixed-Wallis degree model.
