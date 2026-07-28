# Certified cross-family gate for the \(r=1\) profile

Date: 2026-07-28.

## The theorem certified here

Let \(V\) have thirteen vertices.  Suppose \(D\) is the edge-disjoint
union of six matchings, four with four edges and two with five edges, and
suppose
\[
1\le d_D(v)\le5\qquad(v\in V). \tag{1}
\]
For two ten-sets \(Y_0,Y_1\), put
\[
G_i=K_{Y_i}-D[Y_i]\qquad(i=0,1). \tag{2}
\]
If both \(G_0\) and \(G_1\) have perfect matchings, then one of the
following holds:

1. \(G_0,G_1\) have edge-disjoint perfect matchings; or
2. some edge belongs to every perfect matching of both graphs.

This is exactly the cross-family gate isolated in
`../coordinated_nine_r1_reduction/NOTE.md`.  The hypotheses are slightly
weaker than the full class-B row system: the CNFs use only the six-prefix
conditions (1), not the existence of the eleven remaining complement
columns.

The result is computer-assisted.  Six independently checked DRAT
certificates are included, so the claim does not rest on a solver status
line.

## Why six cases are exhaustive

Write \(T_i=V\setminus Y_i\) and
\[
k=|T_0\cap T_1|\in\{0,1,2,3\}.
\]
After relabelling, the pair of triples is fixed by \(k\).  Choose any
perfect matching \(P\) of \(G_0\).  The stabilizer of the two triples acts
as the full symmetric groups on
\[
A=Y_0\setminus Y_1,\qquad C=Y_0\cap Y_1,
\]
where \(|A|=3-k\).  The orbit of \(P\) is determined by
\[
x=|P\cap\tbinom A2|,\qquad
0\le x\le\left\lfloor\frac{3-k}{2}\right\rfloor. \tag{3}
\]
Indeed, after its \(x\) edges inside \(A\), the matching has exactly
\(3-k-2x\) \(A\)-to-\(C\) edges and all other edges lie inside \(C\);
arbitrary permutations inside \(A\) and \(C\) identify any two such
patterns.  Thus the exhaustive orbit list is
\[
(k,x)=(0,0),(0,1),(1,0),(1,1),(2,0),(3,0). \tag{4}
\]
The dependency-free auditor enumerates all 945 perfect matchings of
\(K_{10}\) and checks (3)--(4) directly.

## Exact negation encoded

For each case in (4), the CNF fixes a canonical \(P\) and asserts:

* six labelled matchings of sizes \(4,4,4,4,5,5\);
* no edge is reused by two labelled matchings;
* their union \(D\) has every degree between one and five;
* the fixed \(P\) survives in \(G_0\);
* at least one of all 945 perfect matchings survives in \(G_1\);
* for every edge-disjoint pair among the two 945-element families, at
  least one member does not survive;
* for every edge in the common support, at least one side has a surviving
  perfect matching avoiding that edge.

A variable records every prefix-colour edge, every edge of \(D\), and
the exact availability of each perfect matching.  Cardinalities use a
documented exact unary prefix counter.  Consequently, a satisfying
assignment would be precisely a counterexample to the theorem in the
fixed orbit, with no assumptions hidden in solver callbacks.

The six formulas have 8,257 variables.  Their clause and
edge-disjoint-pair counts are:

| case | clauses | disjoint pairs |
|---|---:|---:|
| \(k=0,x=0\) | 719,561 | 684,180 |
| \(k=0,x=1\) | 719,561 | 684,180 |
| \(k=1,x=0\) | 663,288 | 627,900 |
| \(k=1,x=1\) | 663,288 | 627,900 |
| \(k=2,x=0\) | 606,176 | 570,780 |
| \(k=3,x=0\) | 549,485 | 514,080 |

All six formulas are unsatisfiable.

## Certificate chain

`generate_certificates.py` is a dependency-free deterministic DIMACS
generator.  The compressed DIMACS formulas and binary DRAT proofs are in
`certificates/`; `certificates/manifest.json` records SHA-256 hashes of
the uncompressed files.

The proofs were emitted by CaDiCaL 3.0.1.  They were checked both by
CaDiCaL's internal proof checker and by the independent
[DRAT-trim checker](https://github.com/marijnheule/drat-trim).  DRAT-trim
reported `s VERIFIED` in all six cases.

`audit_certificates.py` does not import the generator or any third-party
Python package.  It independently:

1. enumerates the support matchings and checks orbit exhaustion;
2. reconstructs every semantic and unary-counter clause;
3. compares the parsed DIMACS clauses exactly;
4. checks both CNF and proof hashes; and
5. optionally decompresses and sends each proof to DRAT-trim.

Run the dependency-free audit:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/audit_certificates.py
```

With a compiled DRAT-trim binary:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/audit_certificates.py \
  --drat-trim /path/to/drat-trim
```

To regenerate a case before solving it:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/generate_certificates.py \
  --overlap 0 --aa-edges 0 --output o0_x0.cnf
cadical --unsat --checkproof=3 o0_x0.cnf o0_x0.drat
drat-trim o0_x0.cnf o0_x0.drat
```

## Consequence and remaining \(r=1\) frontier

After the support-preserving switch in the reduction note, every one of
the six remaining size-ten supports is individually matchable and \(D\)
has no \(K_6\).  The forced-edge analysis shows that at most five of
those supports can have a forced edge.  Choose one with no forced edge.
The theorem above says it has edge-disjoint perfect matchings with every
other support in at least one pairwise choice.  Hence two size-ten
matchings can be selected disjointly from each other and from the
six-prefix.

This closes the pair-selection gate, not the full coordinated-nine
theorem.  After the two size-ten matchings, the remaining size-twelve
support initially has the terminal Tutte list
\[
K_{5,7},\qquad K_{3,1,1,1,1,1},\qquad K_7.
\]
The exact row identity eliminates \(K_{5,7}\): the eight selected
matchings have 36 edges, the omitted vertex \(z\) has selected degree at
least three, and therefore their union has at most 33 edges inside the
size-twelve support, fewer than the 35 core edges.  Eliminating
\(K_{3,1,1,1,1,1}\) and \(K_7\), possibly by coordinated prefix/pair
switches, is the remaining \(r=1\) task.
