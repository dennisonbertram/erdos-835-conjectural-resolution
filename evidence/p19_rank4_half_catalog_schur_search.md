# Exact Schur search for the \(p=19\) paired half-link

This is a construction/no-go search for one particular route to a
rank-at-most-four ordered link over \(\mathbb F_{19}\).  It does **not** by
itself solve Erdős--Rosenfeld Problem #835.

## Half-link and paired lift

For \(x\in\mathbb F_{19}^{\times}\), write
\[
 [x]=\{x,-x\}\in\{1,\ldots,9\}.
\]
A **half-link** is a \(10\times10\) alternating matrix \(A\) over
\(\mathbb F_{19}\) such that
\[
 \{[A_{ij}]:j\ne i\}=\{1,\ldots,9\}
 \quad\text{for every }i,
 \qquad \operatorname{rank}A\le4. \tag{1}
\]

Such a matrix gives a full twenty-vertex ordered link.  Put
\[
 J=\begin{pmatrix}1&-1\\-1&1\end{pmatrix},
 \qquad B=A\otimes J.
\]
Then \(\operatorname{rank}B=\operatorname{rank}A\), because
\(\operatorname{rank}J=1\).  Index the two copies of each vertex
lexicographically and label an unordered edge by the corresponding
upper-triangular entry of \(B\).  At either copy of vertex \(i\), the other
copy has label zero and the two copies of every \(j\ne i\) have labels
\(A_{ij}\) and \(-A_{ij}\), possibly exchanged by the common ordering sign.
Equation (1) therefore makes the nineteen incident labels exactly
\(\mathbb F_{19}\).

## Reduction to the 396 one-factorizations

In a half-link, the five edges of any fixed sign class form a perfect
matching: every vertex sees that class exactly once.  The nine classes
therefore form a one-factorization of \(K_{10}\).

Gelling classified 396 isomorphism classes.  The machine-readable catalogue
used here, its independent decoder, provenance, and hashes are documented in
[`k10_factorization_catalogue.md`](k10_factorization_catalogue.md).

For one fixed representative, assign the nine magnitudes \(1,\ldots,9\)
bijectively to its nine factors.  Multiplication of all entries by a nonzero
field element preserves rank and permutes the nine sign classes, so the
magnitude of the catalogue's first factor may be normalized to \(1\).
Exactly \(8!=40{,}320\) magnitude assignments remain.

This loses no labelled case.  Any half-link's nine matchings are carried by
a vertex permutation to one of the 396 representatives; the induced
permutation of the nine factors is absorbed by the magnitude assignment.
The image of any nonsingular principal four-set is then one of the 210
four-subsets enumerated below.

## Exact sign completion from a four-vertex anchor

Choose four vertices and write the alternating matrix in blocks
\[
 A=\begin{pmatrix}H&X\\-X^T&D\end{pmatrix},
 \qquad H\in\mathbb F_{19}^{4\times4}.
\]
If \(H\) is nonsingular and \(\operatorname{rank}A\le4\), the Schur
complement must vanish:
\[
 D=-X^T H^{-1}X. \tag{2}
\]
Conversely, (2) gives rank exactly four.

Every alternating matrix of rank four has a nonsingular principal
\(4\times4\) submatrix: if \(\omega\) is its associated two-form, then
\(\omega\wedge\omega\ne0\), and the coefficients of
\(\omega\wedge\omega\) are twice its principal four-Pfaffians.  A half-link
of rank at most two is already
impossible: its paired lift above would be a rank-at-most-two full ordered
link, contradicting the proved \(p=19\) determinant-link obstruction in
[`determinant_link_p19.md`](determinant_link_p19.md).  Explicitly, every
rank-two alternating matrix over a field of odd characteristic has a
factorization
\(B=U^T\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)U\);
the columns of \(U\) are the two-dimensional vectors in that link, and the
row condition makes every column nonzero.  Alternating rank is even, so
consequently the 210 four-vertex anchors exhaust every rank that can survive.

Vertex switching
\(A_{ij}\mapsto\epsilon_i\epsilon_jA_{ij}\),
\(\epsilon_i\in\{\pm1\}\), preserves all sign classes and rank.  It permits
the three entries from the first anchor vertex to the other anchor vertices
to be positive.  Thus \(H\) has only \(2^3=8\) sign patterns.  It also
permits the first coordinate of each of the six columns of \(X\) to be
positive, leaving exactly \(2^3=8\) states per column.

For every nonsingular \(H\), the verifier enumerates those states by an exact
depth-first search.  When a new outside state is chosen, it checks (2)
against every already chosen outside state and requires the predicted entry
to have the magnitude assigned to that edge's factor.  Hence a failed
anchor job exhausts every sign assignment consistent with that factorization
and magnitude bijection.

The implementation is
[`p19_unrestricted_rank4_half_catalog_search.cpp`](p19_unrestricted_rank4_half_catalog_search.cpp).
As a negative search can otherwise hide an accidental always-rejecting
implementation, the independent
[`verify_p19_half_schur_positive_control.py`](verify_p19_half_schur_positive_control.py)
plants a dense rank-four alternating matrix, erases all 45 edge signs, and
recovers a rank-four matrix by the same normalized \(8\)-state enumeration.
It reports:

```text
planted_seed=3
recovered_anchor_pattern=0
recovered_outside_states=0,6,3,5,3,5
recovered_rank=4
schur_sign_enumeration_positive_control=PASS
```

## Independent implementation and job-index checks

The negative result does not rely on one CSP branching routine.  The
independent source
[`p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp`](p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp)
uses lazy eight-bit compatibility masks, minimum-domain branching, and domain
propagation instead of the primary implementation's fixed-order direct
checks.  It exhaustively repeated four dispersed anchors
\(0,84,137,209\), for a total of
\[
 4\cdot396\cdot8!=63{,}866{,}880
\]
jobs, and agreed that every anchor has no witness.  The exact logs, source
hash, limitations, and verifier output are recorded in
[`p19_half_catalog_compatibility_crosscheck.md`](p19_half_catalog_compatibility_crosscheck.md).

The primary program maps job indices \(0,\ldots,8!-1\) to magnitude
assignments using a factoradic unranking function.  The C++ wrapper
[`verify_p19_half_catalog_unranking.cpp`](verify_p19_half_catalog_unranking.cpp)
includes the pinned production source and calls that exact function.  It
checks that all \(40{,}320\) outputs have normalized first magnitude \(1\),
are distinct, and exhaust all permutations of \(2,\ldots,9\):

```text
normalized_first_magnitude=PASS
distinct_tail_permutations=40320
factoradic_unranking=PASS
```

## Complete all-anchor result

The primary search completed every one of the
\(\binom{10}{4}=210\) possible principal anchors.  For each anchor it
exhausted
\[
396\cdot8!=15{,}966{,}720
\]
factorization/magnitude jobs, and every log ended with the exact terminal
marker

```text
NO WITNESS FOR THIS ANCHOR (complete)
```

Thus the total exact job count was
\[
210\cdot396\cdot8!=3{,}353{,}011{,}200.
\]

The source and catalogue remained pinned throughout:

```text
6eeab50ed32037e7f28646543343465d837d32e233b845c51f54c521c12e5e12  evidence/p19_unrestricted_rank4_half_catalog_search.cpp
226c5addbf5915c7a68023302c2eefc80cbe7cf243441f2fea68b8f263f7bc46  evidence/k10_one_factorizations_396.txt
```

The independent aggregate verifier checks those hashes; every anchor index
and four-set; all three per-anchor job counters; every terminal marker; and
an ordered hash of all 210 logs.  Its output was:

```text
source_sha256=PASS
catalogue_sha256=PASS
completed_anchors=210
total_exact_jobs=3353011200
aggregate_anchor_wall_seconds=17723.344000
minimum_anchor_wall_seconds=25.562600
maximum_anchor_wall_seconds=252.773000
ordered_log_manifest_sha256=4cdbab1c6ebcb48aa38f938045e4fe79e92890da9f1e192f7dc26eeb41f228da
all_anchor_completion_accounting=PASS
```

The exact output of this verifier and all three controls is frozen in
[`p19_rank4_half_catalog_verification.txt`](p19_rank4_half_catalog_verification.txt).
The individual logs are under
[`p19_half_catalog_anchor_logs`](p19_half_catalog_anchor_logs).

Reproduce the accounting with:

```bash
python3 -B evidence/verify_p19_half_catalog_all_anchors.py
python3 -B evidence/verify_p19_half_schur_positive_control.py
python3 -B evidence/verify_p19_half_catalog_compatibility_crosscheck.py
clang++ -std=c++20 -O2 -Wall -Wextra -pedantic -pthread \
  evidence/verify_p19_half_catalog_unranking.cpp \
  -o /tmp/verify_p19_half_catalog_unranking
/tmp/verify_p19_half_catalog_unranking
```

## Restricted theorem

> **Theorem.** There is no \(10\times10\) alternating matrix \(A\) over
> \(\mathbb F_{19}\), of rank at most four, for which every row sees each
> nonzero sign class \(\{x,-x\}\) exactly once.

Indeed, rank zero is incompatible with the row condition.  A rank-two
matrix would give, through the paired lift \(A\otimes J\), a rank-two full
ordered determinant link, excluded by
[`determinant_link_p19.md`](determinant_link_p19.md).  Alternating rank is
even, so only rank four remains.  Every rank-four alternating matrix has a
nonsingular principal four-set.  The one-factorization classification,
factor-label normalization, switching normalization, and Schur completion
above reduce every such matrix to exactly one of the jobs covered across the
210 anchors.  The verified exhaustion found none.

Consequently there is no rank-at-most-four full twenty-vertex ordered link
of the paired form
\[
A\otimes
\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

This is a complete theorem for the paired half-link route only.  It does
**not** exclude an arbitrary rank-four twenty-vertex ordered link, and it
does **not** solve Erdős--Rosenfeld Problem #835.
