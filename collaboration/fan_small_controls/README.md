# A certified small simultaneous-fan obstruction

## Result and scope

This directory contains a portable proof of the following finite theorem.

> No labelled \(LS(2,3,9)\) admits a simultaneous \(3\)-fan of
> \(LS(3,4,10)\)'s. Equivalently, every associated \(378\)-cell conflict
> graph is not \(3\)-colourable. Consequently
> \(\chi(J(12,6))\ge8\).

The complete proof is in `ALL_K6_THEOREM.md`. An exhaustive standard-library
classification verifies that there are two isomorphism types of
\(LS(2,3,9)\), and each representative contains an explicit
non-\(3\)-colourable subgraph with only 18 vertices and eleven constraint
triangles.

This remains a deliberately small control for the simultaneous-fan
reduction. It does **not** decide whether the \(50,388\)-cell graph attached
to an \(LS(2,3,19)\) has a simultaneous \(13\)-fan, and it does not solve
Erdős--Rosenfeld Problem #835.

## The finite object

The \(k=6\) analogue uses a common labelled
\[
L:\binom{[9]}3\longrightarrow[7]
\]
whose seven colour classes are Steiner triple systems. A cell is an allowed
pair
\[
(Q,c),\qquad Q\in\binom{[9]}4,\quad
c\notin\{L(T):T\in\binom Q3\}.
\]
Every quadruple forbids four colours and allows three, giving
\[
\binom94\cdot3=378
\]
cells.

There are two kinds of three-cell constraint group:

- one group for each of the \(\binom94=126\) quadruples \(Q\);
- one group for every triple \(T\) and colour \(c\ne L(T)\), giving
  \(\binom93\cdot6=504\) groups.

Thus there are \(630\) groups in all. A simultaneous \(3\)-fan is exactly an
assignment of labels \(0,1,2\) to the cells such that every constraint group
is rainbow.

## Universal verification

Run:

```sh
python3 -B collaboration/fan_small_controls/verify_all_k6_links.py
```

The standard-library verifier exhaustively enumerates the \(840\) labelled
\(STS(9)\)'s and all \(15,360\) large sets on the fixed labelled point set.
It proves that the two representative point-orbits exhaust that census, then
checks the 18-cell obstruction in each representative.

## Independent exact SAT certificate

For one deterministic representative, the encoding has one Boolean variable
\(x_{v,a}\) for each cell \(v\) and label \(a\):

- one at-least-one and three pairwise at-most-one clauses for every cell;
- one at-least-one clause for every pair `(group, label)`;
- three unit clauses fixing the labels on the first group, without loss of
  generality under global label permutation.

This produces exactly \(1,134\) variables and \(3,405\) clauses. The exact
DIMACS serialization reconstructed by the checker has SHA-256

```text
693e66c10202be59ab8eba2af350b6d9d2ca0d8a438a4c98c5929804e4112a6b
```

The committed 141-line ASCII DRAT proof has SHA-256

```text
45c46fa6da412ff716bf8825e5e2daa125c9dfbf927affd377157d3b4807ffb9
```

It has 131 additions, ten deletions, and ends by deriving the empty clause.
Every addition is RUP; no RAT-only lemma is used.

## Portable certificate verification

Run:

```sh
python3 -B collaboration/fan_small_controls/verify_k6_fan_certificate.py
```

The verifier uses only the Python standard library. It:

1. reconstructs the deterministic large set and all \(378\) cells;
2. reconstructs all \(630\) semantic constraint groups;
3. reconstructs the exact \(3,405\)-clause DIMACS instance;
4. checks both committed digests;
5. checks every proof addition by reverse unit propagation; and
6. requires a final empty-clause derivation.

As a tool-independent cross-check, the same proof was also accepted by the
official `drat-trim` checker, converted to LRAT, and the LRAT was accepted by
the official `lrat-check` checker. The exact receipts are in `RUN_LOG.txt`.
The LRAT is reproducible from the smaller committed DRAT proof and is
therefore not duplicated in the repository.

## Interpretation

The universal small theorem rules out the hope that the simultaneous-fan
condition is automatically satisfied once a common point link exists. Any
proof at \(k=16\) must address a genuinely global resolvability constraint.

It does not determine which side wins at \(k=16\). The small obstruction may
depend on arithmetic special to three labels. The next useful question is to
identify which feature of the two 18-cell obstructions can survive at
thirteen labels.
