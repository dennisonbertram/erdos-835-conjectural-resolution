# Orbit-2 cubic/switch exploration: status and supersession

Date: 2026-07-28

These files are retained as exploratory evidence:

- `2026-07-28_orbit2_switch_cegis.py`
- `2026-07-28_orbit2_obstruction_census.py`
- `2026-07-28_orbit2_exception_cegis.py`
- `orbit2_2026-07-28_pair_switch_results.jsonl`
- `orbit2_2026-07-28_outer_results.jsonl`

They are **not** the final proof of orbit 2.  The much smaller
repeated-support compatible-pair reduction in
`../r0_three_family_helly_gate/2026-07-28_orbit2_cut_sufficiency.md`
supersedes this route.

## What the exploration established

For selected omitted rows \(012,012,123\), a prescribed factor \(H\) has
degrees

\[
d_H(0)=1,\qquad d_H(3)=2,\qquad d_H(v)=3\quad(4\le v\le12).
\]

If \(03\notin H\), write \(x\) for the neighbour of \(0\).  Deleting \(0x\)
and adding \(3x\) converts \(H\) to a cubic ten-vertex graph, with a doubled
root edge exactly when \(3x\in H\).  In the simple case, prescribed
colourability of \(H\) is equivalent to ordinary three-edge-colourability of
the cubic completion.

The nauty 2.8.9 census has 19 connected simple cubic graphs on ten vertices.
Only the Petersen graph and one bridged type fail three-edge-colourability.
Directed-root automorphism reduction leaves one Petersen case and six
bridged cases.  A disconnected simple cubic graph on ten vertices has
component orders \(4+6\); the components are \(K_4\) and either \(K_{3,3}\)
or the triangular prism, hence are three-edge-colourable.

For the nonsimple branches, the retained exact graph6 census gives:

- 19 unlabeled cores of degree sequence \((1,3^9)\), corresponding to
  \(03\in H\);
- 23 unlabeled cores of degree sequence \((2,2,3^8)\) whose degree-two
  vertices are adjacent;
- 28 directed-root types in the latter class, only five of whose associated
  factors are not prescribed-colourable.

Thus the exceptional fixed-factor catalogue consists of 31 directed types:
seven simple-cubic types, nineteen \(03\)-edge types, and five uncolourable
doubled-root types.

## What the switch search did not prove

The switch program fixes one labelled bad factor and searches its
degree-preserving two-edge-switch component.  It deliberately omits vertex
symmetry breaking, because deleted-graph canonicalization is not sound after
a labelled factor has been fixed.  Its optional pair mode includes explicit
matching witnesses for pair compatibility.

The pair-compatible run reached a closed two-switch component for each of
the six bridged rooted types before it was stopped:

| case | rounds |
|---|---:|
| `bridge_0_4` | 93 |
| `bridge_0_6` | 66 |
| `bridge_1_5` | 89 |
| `bridge_1_8` | 128 |
| `bridge_3_6` | 93 |
| `bridge_3_8` | 85 |

This means only that no prescribed-colourable factor lies in that particular
two-switch component for the displayed deletion model.  It is not a
counterexample to the target theorem.  For example, the first displayed
model has an independently found simultaneous triple outside the fixed
component.  The Petersen case was still in its UNSAT solve when this route
was stopped.

`orbit2_2026-07-28_outer_results.jsonl` is empty because the global relaxed
outer run was interrupted before producing a terminal result.  The exception
CEGIS generator was completed but not run after the sharper reduction was
found.

## Final status

No theorem claim relies on these exploratory searches.  Orbit 2 is closed by
fixing a compatible pair on the two identical supports, reducing its union
to three marked even-cycle types, and globally excluding every simultaneous
triple for each type.  That proof changes the chosen duplicate-support pair
when necessary and therefore avoids the obstruction that defeats a purely
local fixed-factor switch argument.
