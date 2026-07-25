# Candidate problem: \(C(12,6,4)\)

This directory contains exact intermediate results for the open covering-design
case

\[
40\le C(12,6,4)\le 41.
\]

It does **not** yet claim a resolution.

## Local degree theorem

[`local_c1042_degree_proof.md`](local_c1042_degree_proof.md) proves

\[
C(10,4,2)=9
\]

and proves that every point in every nine-block \(C(10,4,2)\) has degree
\(3\) or \(4\).  The exclusions of eight blocks, degrees at least six, and
the final degree distribution are human proofs.  The remaining degree-five
case is a finite exhaustive check implemented in
[`check_c1042_degree5.cpp`](check_c1042_degree5.cpp); the note gives a
line-by-line completeness argument.  The captured compiler, source hash,
command, output, and timing are in
[`degree5_verification_output.txt`](degree5_verification_output.txt).

## Exact local excess theorem

Suppose a nine-block \(C(10,4,2)\) has six points of degree \(4\) and four
points of degree \(3\). For a pair \(i,j\) of degree-\(4\) points, put

\[
z_{ij}=\lambda_{ij}-1.
\]

Every pair touching a degree-\(3\) point has multiplicity exactly one, and the
weighted graph \(z\) on the six degree-\(4\) points is a loopless cubic
multigraph. There are nine such multigraphs up to \(S_6\). Exactly four are
realizable by nine distinct four-subsets.

Equivalently, a cubic excess multigraph is locally realizable precisely when

\[
\sum_{i<j}\binom{z_{ij}}2\ge 3.
\]

The realizable isomorphism types have concentration \(9,5,3,3\); the five
impossible types have concentration \(2,1,2,0,0\).

## Reproduce

Run:

```bash
python3 candidate_c12/classify_c1042_excess.py
```

The verifier is solver-free. It:

1. generates all 760 labeled loopless cubic multigraphs on six vertices;
2. obtains exactly nine canonical \(S_6\)-orbits;
3. enumerates all 280 possible partitions forced by one degree-\(3\) point;
4. performs complete exact backtracking for the remaining six blocks;
5. checks each positive witness directly.

Expected final line:

```text
realizable_types 0 1 2 4
```

The five exhaustive negative searches visit respectively
`575, 606, 477, 793, 696` memoized search states.

## Consequence for a hypothetical 40-cover

Normalize the six degree-\(10\) pairs as a perfect matching. For each unmatched
pair \(P\), the nine selected six-subsets containing \(P\), after deleting
\(P\), form a nine-block \(C(10,4,2)\). If

\[
z_Q=d_Q-1
\]

is the excess multiplicity of a four-subset, the local theorem gives the
necessary inequality

\[
\sum_{Q\supset P}\binom{z_Q}{2}\ge 3
\]

for every one of the 60 unmatched pairs \(P\).

This constraint has been added to the ongoing global search, but it has not
yet produced a complete construction or nonexistence proof.

## Fixed-support Farkas certificates

[`fixed_support_farkas.md`](fixed_support_farkas.md) gives exact rational
Farkas contradictions for two fixed \(A=45\), \(z_Q\in\{0,1,3\}\) support
representatives.  The solver-free verifier checks all \(924\) possible
six-subsets with exact arithmetic.  These are conditional fixed-support
exclusions, not a claim that the global problem is resolved.
