# Certified cross-family gate for the \(r=0\) profile

Date: 2026-07-28.

## The certified theorem

Let \(V\) have thirteen vertices.  Suppose \(D\) is the edge-disjoint
union of six matchings, three with four edges and three with five edges,
and suppose
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

This is the \(r=0\) analogue of the certified gate in
`../coordinated_nine_r1_gate_sat/NOTE.md`.  The assumptions are weaker
than the full class-B row system: the formulas use only the exact
six-prefix matching sizes and the degree interval (1).

The theorem is computer-assisted.  Six compressed CNFs and six DRAT
proofs are included.  An independent standard-library auditor
reconstructs every clause semantically, checks the support-pair orbit
exhaustion and recorded hashes, and can replay every proof with DRAT-trim.

## Why there are six cases

Put \(T_i=V\setminus Y_i\), and let \(k=|T_0\cap T_1|\).  After relabelling
the two triples, fix one perfect matching \(P\) of \(G_0\).  If
\[
A=Y_0\setminus Y_1,\qquad C=Y_0\cap Y_1,
\]
then the stabilizer acts as the full symmetric groups on \(A\) and \(C\).
The orbit of \(P\) is determined by the number \(x\) of its edges inside
\(A\).  This gives exactly
\[
(k,x)=(0,0),(0,1),(1,0),(1,1),(2,0),(3,0). \tag{3}
\]
The auditor independently enumerates all \(945\) perfect matchings of
\(K_{10}\) and verifies this orbit list.

## Exact negation encoded

For each orbit, the CNF fixes the canonical matching \(P\) and asserts:

- six labelled matchings of sizes \(4,4,4,5,5,5\);
- no edge reused by two prefix matchings;
- every vertex degree in their union lies between one and five;
- the fixed matching survives on \(Y_0\);
- at least one perfect matching survives on \(Y_1\);
- no surviving pair is edge-disjoint; and
- no common-support edge is forced in every surviving matching on both
  sides.

A satisfying assignment would therefore be exactly a counterexample to
the theorem in the fixed orbit.  All six formulas are unsatisfiable.
Their sizes are:

| case | variables | clauses | edge-disjoint pairs |
|---|---:|---:|---:|
| \(k=0,x=0\) | 8,330 | 719,853 | 684,180 |
| \(k=0,x=1\) | 8,330 | 719,853 | 684,180 |
| \(k=1,x=0\) | 8,330 | 663,580 | 627,900 |
| \(k=1,x=1\) | 8,330 | 663,580 | 627,900 |
| \(k=2,x=0\) | 8,330 | 606,468 | 570,780 |
| \(k=3,x=0\) | 8,330 | 549,777 | 514,080 |

CaDiCaL 3.0.1 generated the binary DRAT proofs and checked them
internally.  DRAT-trim independently reported `s VERIFIED` for all six.

## Reproduction

The shared generator and auditor default to the committed \(r=1\) shape.
Pass the \(r=0\) shape explicitly:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/audit_certificates.py \
  --certificate-dir collaboration/coordinated_nine_r0_pair_gate_sat/certificates \
  --prefix-sizes 4 4 4 5 5 5 \
  --label r=0
```

With DRAT-trim:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/audit_certificates.py \
  --certificate-dir collaboration/coordinated_nine_r0_pair_gate_sat/certificates \
  --prefix-sizes 4 4 4 5 5 5 \
  --label r=0 \
  --drat-trim /path/to/drat-trim
```

Regenerate one formula with:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/generate_certificates.py \
  --overlap 0 --aa-edges 0 \
  --prefix-sizes 4 4 4 5 5 5 \
  --output o0_x0.cnf
```

## Consequence and exact scope

After the support-preserving saturated-core switch, every remaining
size-ten support in the \(r=0\) profile is individually matchable.
The theorem now converts every incompatible support pair into a shared
forced-edge core.  The exact forced-edge catalogue consists of
\(K_6-e\) and the \(r=0\) equality possibility \(K_{5,5}-e\).

This is a structural bridge, not yet a coordinated-nine theorem.
The incompatibility-graph classification in
`../r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md` now proves that
the no-independent-triple case is exactly the six-fold \(K_6-e\) equality
boundary handled by
`../r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md`; it also
eliminates the \(K_{5,5}-e\) pair branch.  The remaining \(r=0\) gate is
three-way coordination for an independent triple, using the full
class-B complement-row inventory.  No full \(r=0\) theorem or solution of
Problem #835 is claimed here.
