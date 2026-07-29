# Audit of the Opus 5 remaining-orbit reduction

Date: 2026-07-28

## Verdict

Claude Opus 5 was asked at maximum effort to close the twelve remaining
Venn types of the prescribed-colour \(r=0\) gate.  No code ran in that
session and no UNSAT certificate was produced.  The response therefore did
not prove the local theorem.

Its main new structural proposal is nevertheless correct:

> **Single-matching reduction.**  Under the full campaign's selected
> pairwise-compatible triple, the twelve open Venn types reduce to exactly
> \(50\) finite formulas if one matching of a compatible support pair is
> canonicalized and its mate remains existential.

The reduction, its case count, its premise, and the downstream CNF encoding
have now been checked independently.  The \(50\) formulas themselves are
not all UNSAT yet, so this is a finite reduction rather than the missing
prescribed-colour theorem.

## The canonicalization theorem

Fix three omitted rows \(R_0,R_1,R_2\), their supports
\(S_i=V(K_{13})\setminus R_i\), and the selected maximum-intersection pair
\((S_0,S_1)\).  A vertex of \(S_0\) lies in one of the four Venn cells with
masks

\[
0,\quad 2,\quad 4,\quad 6.
\]

Write their multiplicities as

\[
\mathbf a=(a_0,a_2,a_4,a_6),\qquad \sum a_m=10.
\]

The subgroup fixing each of the three rows setwise contains, and on
\(S_0\) restricts to,

\[
\prod_{m\in\{0,2,4,6\}}\operatorname{Sym}(C_m).
\]

For a perfect matching \(M\) of \(S_0\), record the multiset of unordered
endpoint-cell pairs

\[
\mathcal I(M)=
\big\{\!\big\{\{\mu(x),\mu(y)\}:xy\in M\big\}\!\big\}.
\]

This is a complete orbit invariant.  Necessity is immediate.  Conversely,
if two matchings have the same multiset, match their edges type by type,
orient the endpoints inside each cell, and combine the resulting endpoint
bijections.  This gives an independent permutation in every \(C_m\) and
maps one matching to the other.

Equivalently, the orbits are the symmetric nonnegative integer matrices
\((q_{mn})_{m\le n}\) satisfying

\[
2q_{mm}+\sum_{n\ne m}q_{mn}=a_m,
\qquad
\sum_{m\le n}q_{mn}=5.
\]

Thus they are loop-multigraphs with five edges and prescribed degree vector
\(\mathbf a\).

## Exact counts

The independently verified vectors and counts are:

| orbit | \(\mathbf a\) on \(S_0\) | cases |
|---:|---|---:|
| 0 | \((10,0,0,0)\) | 1 |
| 1 | \((9,0,0,1)\) | 1 |
| 2 | \((9,0,1,0)\) | 1 |
| 3 | \((8,0,1,1)\) | 2 |
| 4 | \((8,0,2,0)\) | 2 |
| 5 | \((7,0,3,0)\) | 2 |
| 6 | \((8,1,1,0)\) | 2 |
| 7 | \((7,1,2,0)\) | 3 |
| 8 | \((8,1,1,0)\) | 2 |
| 9 | \((7,1,1,1)\) | 4 |
| 10 | \((7,1,2,0)\) | 3 |
| 11 | \((6,1,3,0)\) | 4 |
| 12 | \((6,2,2,0)\) | 6 |
| 13 | \((6,2,2,0)\) | 6 |
| 14 | \((5,2,3,0)\) | 7 |
| 15 | \((4,3,3,0)\) | 9 |

Hence the open types \(4,\ldots,15\) require

\[
2+2+2+3+2+4+3+4+6+6+7+9=50
\]

canonical first-matching cases.

The primary audit derives all sixteen Venn signatures and checks the counts
in three separate ways:

1. endpoint-cell invariant buckets over all \(945\) perfect matchings;
2. connected components of the explicit within-cell generator action; and
3. direct enumeration of the loop-multigraph incidence matrices.

An independent agent then enumerated all \(81{,}796\) anchored ordered row
pairs and reproduced the orbit counts by Burnside's lemma, rather than any
of those three methods.

Run:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/opus5_r0_orbit_repair/2026-07-28_single_matching_orbit_audit.py
```

The expected final lines are

```text
open_total=50
all_total=55
PASS
```

## Quantifier audit

The reduction must not fix an arbitrary matching.  Its valid quantifier
order is:

\[
\forall D\text{ in the searched counterexample class},\quad
\exists(P_0,P_1)\text{ compatible},\quad
\exists g\text{ preserving the rows}
\]

such that \(gP_0\) is canonical.  The same \(g\) transports \(D\) and the
still-existential mate \(P_1\).  Every constraint and the absence of a
simultaneous triple are invariant under this relabeling.

The compatible-pair premise is available in the intended full-row campaign.
The cut-selection theorem supplies an individually and pairwise compatible
triple satisfying every capacity cut after the permitted repair.  The
certified pair gate and incompatibility theorem give the same dependency
locally: the surviving \(K_6-e\) incompatibility core contradicts the
selected cut, while the \(K_{5,5}-e\) alternative is excluded by the full
row inventory.

## Downstream formula

For each canonical \(P_0\), the implemented formula keeps:

1. \(|D|=27\);
2. \(t(v)+1\le d_D(v)\le5\);
3. every nonautomatic capacity cut;
4. availability of \(P_0\);
5. edge variables forming an existential available perfect matching
   \(P_1\) on \(S_1\), disjoint from \(P_0\);
6. for every third matching \(N\) disjoint from \(P_0\), the sound clause
   saying \(N\) is deleted or meets \(P_1\); and
7. exact CEGIS clauses requiring \(D\) to hit every available
   prescribed-colour triple.

The independent audit checked the partner encoding, every static
third-extension clause, the semantic model verifier, and the CEGIS
exhaustion logic.  It also tested the identical-support and disjoint-row
extremes.

Generator:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/opus5_r0_orbit_repair/2026-07-28_single_matching_cegis.py \
  --orbit 5 --cases all
```

## Gap audit

The first missing statement is exactly:

> Every one of the \(50\) accumulated formulas for support orbits
> \(4,\ldots,15\) is UNSAT.

Orbit 4 is also being closed through its finer eleven-case compatible-pair
catalogue, which supplies an independent route.  Solver terminal output is
not promoted to a theorem until the frozen CNF is semantically reconstructed
and the external DRAT replay succeeds.

Even closure of all \(50\) cases proves only the local prescribed-colour
gate.  The later seventeen-matching first-lift completion and the
six-instance shared-colour/global coupling remain necessary before
Erdős--Rosenfeld Problem #835 is resolved.
