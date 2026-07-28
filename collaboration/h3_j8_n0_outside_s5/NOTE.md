# Exact elimination of the exterior-\(S_5\)-symmetric \(N=0\) subclass

## Result and strict scope

Normalize a \(\Delta=60\) four-cube on vertices \(0,\ldots,7\), and let the
five exterior vertices be \(8,\ldots,12\).  There is no nonnegative integer
array
\[
0\le d_Q\le13\qquad\left(Q\in\binom{[13]}4\right)
\]
that simultaneously:

1. is invariant under every permutation of the five exterior vertices;
2. has every triple load \(\sum_{Q\supset T}d_Q\le13\);
3. satisfies the exact recurrence-count equations at sizes \(5,\ldots,11\);
4. has negative cube mass \(N=0\) and positive cube mass \(P=60\).

This is an exact finite, computer-assisted elimination, independently replayed
with CP-SAT and Gurobi.  The exterior \(S_5\) symmetry is an additional ansatz,
not a without-loss-of-generality reduction.  Therefore this result does **not**
eliminate the general \(N=0\) branch, prove the \(j=8\to9\) lift, or solve
Erdős--Rosenfeld Problem #835.

## Finite model

For an exterior-symmetric four-set, retain its exact cube part and only the
number of exterior points.  This gives
\[
\sum_{k=0}^4\binom8{4-k}=163
\]
integer \(d\)-orbits.

There are 93 triple orbits.  For one representative \(T\) of each orbit, the
model expands all ten actual four-sets containing \(T\), with orbit
multiplicities retained, and imposes
\[
\sum_{Q\supset T}d_Q\le13.
\]

For every orbit representative \(S\) of sizes \(5,\ldots,11\), introduce a
nonnegative integer count \(N_S\), put
\(D_S=\sum_{Q\in\binom S4}d_Q\), and impose
\[
\begin{array}{c|c}
|S|&\text{exact equation}\\ \hline
5&2N_S+D_S=13\\
6&3N_S-D_S=39\\
7&4N_S+D_S=195\\
8&5N_S-D_S=325\\
9&6N_S+D_S=702\\
10&7N_S-D_S=546\\
11&8N_S+D_S=858.
\end{array}
\]
The numbers of recurrence orbits are respectively
\[
219,\ 246,\ 246,\ 219,\ 163,\ 93,\ 37,
\]
for a total of 1,223.  Finally, the eight negative cube cells sum to zero
and the eight positive cells sum to 60.  The resulting integer feasibility
model has 1,386 variables and 1,318 constraints.

## Reproduction and audit

Run the dependency-free semantic audit:

```text
python3 -B verify_model.py
```

It checks all 120 exterior permutations, every four-set orbit, every actual
triple and size-\(5,\ldots,11\) subset against its representative's
coefficient signature, the recurrence equations, the cube orientation, and
the reported model totals.  This verifies the mathematical translation, not
the infeasibility conclusion.

Run either exact integer solver:

```text
python3 -B search_cp_sat.py --seconds 120 --workers 16
python3 -B search_gurobi.py --seconds 600 --threads 16
```

Both returned `INFEASIBLE`; see
[`CP_SAT_RUN_LOG.txt`](CP_SAT_RUN_LOG.txt) and
[`GUROBI_RUN_LOG.txt`](GUROBI_RUN_LOG.txt).  CP-SAT and Gurobi are independent
solver implementations, but the repository does not yet contain a
proof-checker-consumable UNSAT certificate.  The defensible claim is therefore
an independently replayed exact finite elimination with a separately audited
model, not a stand-alone formal proof.
