# One-layer repair CEGIS for coordinated-nine at \(r=0\)

Date: 2026-07-28.

## Scope

This directory contains an exact finite search for the following bounded
statement.

> **C1 repair statement.**  From every packed complement-cover six-prefix of
> profile
> \[
> 8^3\,10^3
> \]
> in an \(r=0\) class-B instance, one selected prefix layer can be repacked on
> exactly the same support so that some three of the eleven remaining
> supports admit mutually edge-disjoint perfect matchings.

The three new colours may have any of the four possible type patterns:
\(10+10+10\), \(10+10+8\), \(10+8+8\), or \(8+8+8\).

This is a **search reduction**, not a theorem or proof certificate.  An
`unsat_uncertified` result means that the accumulated finite CNF was
unsatisfiable in the search solver.  It must still be frozen, regenerated
independently, proved by CaDiCaL, and replayed with DRAT-trim before the C1
repair statement may be cited as proved.

The companion `search_cut_feasible_repair.py` tests the narrower intermediate
claim needed by the current cut route:

> after repacking at most one prefix layer on the same support, some three of
> the seven remaining size-ten rows satisfy every internal-edge capacity cut.

For a decoded prefix it enumerates every legal replacement matching and all
\(\binom73\) selected row triples, checking only the provably relevant
six-, seven-, and eight-vertex cuts.  A semantic witness clause conditions on
the repaired layer's support, the exact union of the other five layers, and
the three selected row occurrences.  The exact other-layer union is necessary
because cut feasibility depends on all residual internal-edge counts.  A
second raw pass re-enumerates every repair and route before a counterexample
can be reported.  This script is likewise discovery evidence until an UNSAT
CNF and proof are independently frozen and replayed.

No \(K_6\), \(K_6-e\), \(K_6-2K_2\), forced-edge, or Tutte-core
classification is assumed.  In particular, the search does not rely on the
false claim that every obstruction has the \(K_6-2K_2\) form.

## Exact base CNF

Let \(V=\{0,\ldots,12\}\) and let \(E=\binom V2\).  The base variables are:

* \(x_{i,e}\), for the six selected prefix layers and all \(e\in E\);
* \(d_e\), for the union of the prefix layers;
* \(c_{i,v}\), saying that \(v\) belongs to the support of prefix layer \(i\);
* \(y_{r,v}\), for the eleven remaining complement rows; and
* \(o_{i,e}\), saying that some prefix layer other than \(i\) uses \(e\).

The prefix sizes are
\[
(4,4,4,5,5,5).
\]
Each layer is constrained to be a matching of its exact size, and different
layers are edge-disjoint.  The union variables are exact.  At every vertex,
\[
1\le d_D(v)\le5.
\]

Rows \(0,\ldots,6\) are the seven remaining triples and rows
\(7,\ldots,10\) are the four remaining five-sets.  The exact class-B column
equation is encoded as
\[
\sum_{e\ni v} d_e+\sum_{r=0}^{10}(1-y_{r,v})=12. \tag{1}
\]
If \(\rho(v)=\sum_r y_{r,v}\), equation (1) is precisely
\[
\rho(v)=d_D(v)-1.
\]
Together with the degree-five upper bound, these are the complete row
equations for a complement-cover prefix.

The only static symmetry reductions are:

1. one remaining triple is fixed to \(\{0,1,2\}\);
2. the other six triple rows are lexicographically ordered;
3. the four five-set rows are lexicographically ordered; and
4. the three size-four prefix layers and, separately, the three size-five
   prefix layers are lexicographically ordered.

Repeated remaining rows remain allowed.

## Why one repacked layer is a bounded local repair

Let \(M_i\) be one old prefix layer and let \(P\) be any perfect matching on
the same support which avoids the other five prefix layers.  The symmetric
difference \(M_i\mathbin{\triangle}P\) is a disjoint union of alternating
even cycles.  Flip each nontrivial cycle.

The only possible cycle lengths are \(4,6,8,10\).  Since
\(|M_i|\le5\), there are at most two nontrivial cycles.  Every intermediate
layer is a perfect matching on the original support, and every new edge
avoids the other five layers.  Thus the repacking is exactly realizable by
at most two support-preserving local alternating-cycle switches.

## Witness-negation cuts

A successful witness records:

* the repaired prefix layer \(i\);
* its replacement perfect matching \(P\);
* three distinct remaining row indices;
* their exact complement sets; and
* three pairwise edge-disjoint perfect matchings \(N_0,N_1,N_2\), also
  disjoint from \(P\).

Let \(S=V(P)\) and
\[
E^*=P\cup N_0\cup N_1\cup N_2.
\]
The witness works whenever:

1. \(c_{i,v}\) is the characteristic vector of \(S\);
2. \(o_{i,e}=0\) for every \(e\in E^*\); and
3. the three selected \(y\)-rows equal the recorded complements.

The search adds the single clause negating that conjunction.  Each cut is
therefore semantically reconstructible from its typed witness record.
Every genuine C1 counterexample satisfies every such clause.

The optional `--witness-log` output writes one canonical JSON record and the
SHA-256 hash of its reconstructed clause for every added cut.

## Encoding and quantifier audit

The two implications needed for every auxiliary
\(o_{i,e}\) are both present:

\[
x_{k,e}\Longrightarrow o_{i,e}\quad(k\ne i),\qquad
o_{i,e}\Longrightarrow\bigvee_{k\ne i}x_{k,e}.
\]

In particular, a learned witness can never claim that an edge is free while
another prefix layer uses it.

The symmetry reductions do not discard an isomorphism class.  Given any
valid labelled input, choose one of its seven triple occurrences and relabel
its vertices to \(0,1,2\).  Permute the other six triple occurrences into
lexicographic order, do the same for the four five-set occurrences, and
permute the three size-four and three size-five prefix layers within their
equal-size groups.  These operations preserve repairability and produce a
base-CNF representative.  Repeated rows cause no problem because occurrences,
not distinct sets, are permuted.

The witness generator is exhaustive for each decoded model: it enumerates all
six repaired layers, every perfect matching on the unchanged support avoiding
the other five layers, all \(165\) triples of remaining occurrences, and all
perfect matchings on their exact supports.  If its first pass finds no
witness, `independent_has_witness` repeats the raw search without using SAT
variables before a counterexample can be reported.

Consequently, a certified UNSAT result would have the correct quantifier
order.  Each learned clause removes only assignments for which its recorded
repair works; if no assignment survives, every valid input is covered by at
least one concrete repair witness.

## Canonical replay

`--replay-witness-log PATH` streams a prior canonical JSONL log before
solving.  It rejects duplicate JSON keys, malformed types, noncanonical
matchings or complements, invalid edge-disjointness, noncanonical byte
serialization, and a mismatch between the recorded and reconstructed clause
hash.  The replay input cannot also be the output path.

A deterministic audit generated four cuts, replayed all four, and added four
new cuts.  The replay hash was

```text
6c557eb980a7d919dec07671db2f44f2ca64442c17c4a6c0de46c903d609e401
```

## Bounded campaign results

These are discovery runs, not proof certificates:

| campaign | replayed | new cuts | total cuts | result |
|---|---:|---:|---:|---|
| dense, 60 s, 256 cuts/model | 0 | 710,912 | 710,912 | time limit |
| dense, 120 s, 1,024 cuts/model | 0 | 1,752,064 | 1,752,064 | time limit |
| diverse, 120 s, 990 cuts/model | 0 | 460,350 | 460,350 | time limit |
| replay wave 1 + diverse, 600 s | 710,912 | 1,480,050 | 2,190,962 | time limit |

The last campaign reached 2,235,439 clauses after replay and learning.  Its
replay SHA-256 was

```text
0e27abcbe19eab1f7970b15141015029dba122d176718149ed2d8010bd6d2873
```

and its combined witness-stream SHA-256 was

```text
8041bd8da8402b52b557e184cb745d49b20cd653eefec84f0de725654e85367a
```

The standalone second-wave JSONL hash was

```text
317d845dc152737e0d33b2607936fe40be9f405f12baf422ee64202199b5969b
```

Both logs are published as compressed assets in the public
[`r0-cegis-evidence-2026-07-28`](https://github.com/dennisonbertram/erdos-835-conjectural-resolution/releases/tag/r0-cegis-evidence-2026-07-28)
release.  Their gzip SHA-256 values are

```text
wave 1: 1ea8c0e40842e2570f9ae0fc539f7884d9d0650256007cec9fb04e28d3165a95
wave 2: e96f82ea68bfe81beabb4bbe08ec5966b28f96ec4d3a899f9f6c802c1a65e82f
```

It exercised all \(990=6\binom{11}{3}\) repair-layer/route signatures and
found neither a validated counterexample nor UNSAT.  This is positive
coverage evidence only.

## Search and independent counterexample replay

For a SAT model, the program enumerates:

1. each of the six possible repaired layers;
2. every replacement perfect matching on that layer's fixed support which
   avoids the other five layers;
3. all \(\binom{11}{3}=165\) triples of remaining colour occurrences; and
4. exact perfect matchings on their supports.

If it finds witnesses, it adds up to `--cuts-per-model` cuts and resumes the
solver.  If it finds none, the raw prefix and row data are checked again
without SAT variables.  This replay verifies the matching sizes,
edge-disjointness, complement cover, all class-B row equations, and performs
a second exhaustive one-layer-repair/three-colour search before the JSON is
reported as a `counterexample`.

## Running

A short bounded search:

```sh
python3 collaboration/coordinated_nine_r0_repair_cegis/search_one_layer_repair.py \
  --max-rounds 2 \
  --cuts-per-model 2
```

An unbounded-round campaign still has a hard ten-minute wall-clock guard:

```sh
python3 collaboration/coordinated_nine_r0_repair_cegis/search_one_layer_repair.py \
  --max-rounds 0 \
  --cuts-per-model 32 \
  --witness-log /tmp/r0-c1-witnesses.jsonl
```

The program prints one JSON result.  Status values are:

* `round_limit`;
* `time_limit`;
* `counterexample`, always with `counterexample_validated: true`; or
* `unsat_uncertified`.

Only a separately regenerated and independently replayed DRAT certificate
could upgrade the last status into a theorem.
