# Discovery search for the three-near-factor theorem

Date: 2026-07-28.

## Scope

`search_cegar.py` was a counterexample-guided discovery tool for the
following statement:

> Every graph on thirteen vertices with minimum degree at least seven
> contains three pairwise edge-disjoint near-perfect matchings with any
> three prescribed omitted vertices, with repetitions allowed.

The subsequent solver-free proof is in
`../coordinated_nine_structural/NOTE.md`, with an independent terminal
\(K_7\) proof in `../k7_terminal_switching/NOTE.md`.  Consequently this
search is retained only as a reproducible discovery record.  It is not
part of the proof.

## Model

For one of the three equality patterns

\[
(x,x,x),\qquad (x,x,y),\qquad (x,y,z),
\]

the master CP-SAT model chooses a graph \(H\) on thirteen vertices with
\(\delta(H)\ge7\) and minimizes its number of edges.  The subproblem seeks
the prescribed triple of edge-disjoint near-perfect matchings.  Whenever it
finds one, the master receives a no-good cut requiring at least one of those
eighteen edges to be absent.  Random relabellings fixing the prescribed
omissions add orbit-equivalent cuts.

An `INFEASIBLE` master result would still require an independently
checkable proof certificate before it could be cited as a theorem.
`COUNTEREXAMPLE` would mean that the fixed subproblem was proved
infeasible.  `UNKNOWN` and `TIME_LIMIT` are telemetry only.

## Discovery runs

The main symmetry-cut runs used:

```sh
python3 collaboration/three_near_factor_cegar/search_cegar.py \
  --pattern same --total-time 120 --orbit-cuts 8

python3 collaboration/three_near_factor_cegar/search_cegar.py \
  --pattern two --total-time 120 --orbit-cuts 8

python3 collaboration/three_near_factor_cegar/search_cegar.py \
  --pattern distinct --total-time 120 --orbit-cuts 8
```

They generated respectively \(8{,}496\), \(8{,}736\), and \(8{,}624\)
packing cuts without finding a counterexample.  Every master candidate was
one of the sparsest possible graphs, with \(46\) edges.  Earlier
non-symmetry runs generated roughly \(1{,}167\) cuts per pattern.  None of
these incomplete runs is a proof.

The structural lesson was more useful than the raw volume: exact Tutte
analysis after two matchings leaves only the separator-zero \(K_{5,7}\),
separator-four \(K_{3,1^5}\), and separator-five \(K_7\) cores.  The
committed proof eliminates those cores directly, so no longer depends on
CEGAR.

## Reproduction

The script requires OR-Tools.  A short smoke run is:

```sh
python3 collaboration/three_near_factor_cegar/search_cegar.py \
  --pattern distinct --total-time 10 --master-time 2 \
  --subproblem-time 2 --orbit-cuts 4
```

Any finite output other than a separately certified `MASTER_INFEASIBLE` or
an independently checked `COUNTEREXAMPLE` must be treated as discovery
telemetry.
