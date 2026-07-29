NOT SOLVED

# Status — common odd transversal at the top rung

Date: 2026-07-29.  Directory: `collaboration/opus5/common_odd_transversal_2026-07-29/`.

## Exact scope of what is and is not claimed

**Erdős--Rosenfeld Problem #835 is not resolved, in either direction, for any
admissible `k > 2`.**  No `LS(k-1,k,2k)` is constructed and no unrestricted
nonexistence theorem is proved.  The first unrestricted open case remains
`k = 16`, `p = 17`, unchanged.

The assignment's target theorem

> **(COT)** every `k-1` pairwise disjoint, complement-closed `S(k-1,k,2k)`'s
> possess a common odd transversal

is **neither proved nor refuted**.  What is settled is its *status*: it is
**vacuous on every admissible parameter that has been decided**, so it
currently admits no Steiner countermodel and no confirming Steiner instance.

## Results, by confidence

### Proved here, unconditionally (`PROOF.md`)

| # | Statement | Where |
|---|---|---|
| 1 | The audited exact equivalence is **correct**; no flaw. Re-derived independently at the top rung without forming `Q` or `M_D`. | Thm 1.1, 1.2 |
| 2 | An `S(k-1,k,2k)` has exactly **two** intersection characters: closed forms for `#{C : |B ∩ C| = i}` in both the `B in T` and `B not in T` cases. | Thm 2.1 |
| 3 | Complement closure (the audited Lemma 6.0) is the `i = 0` coefficient of #2; also `x_1 = x_{k-1} = 0` on blocks and `= k` off blocks. | Cor 2.2, 2.3 |
| 4 | Divisibility-admissible ⟺ `k+1` prime, both directions, from `lambda_j` integrality via Lucas. This does not assert design existence. | Cor 2.4 |
| 5 | **Link theorem**: at every rung, the links of `r` disjoint systems at any `s`-set are `r` disjoint systems one rung down. | Thm 3.1 |
| 6 | At `s = t-1` the links are `p-2` disjoint one-factors of `K_{p+1}` and the residual `R(A_0)` is a **2-factor**; its cycles embed in the conflict graph `G` with the **same length**. | Thm 3.2, 3.3 |
| 7 | **Local odd-cycle certificate**: an odd cycle in any `R(A_0)` proves non-extendability, in `O(p^2)` from the link one-factors alone. | Cor 3.4 |
| 8 | At `t = 1` the local condition is also **sufficient** — the base case of the open lemma. | Cor 3.5 |
| 9 | The repository's authenticated negative control (Etzion--Hartman, `(t,n,p) = (3,20,17)`, 15 systems) **is** an instance of #7: its three certificate labels all contain `{14,17}`, so it is the triangle `0-2-5` in `R({14,17})`. | Prop 3.6 |
| 10 | At the top rung, complementation is a **free** involution on vertices *and* edges of `G`, and `G` is bipartite ⟺ `G/iota` is bipartite. Every proper 2-colouring is `iota`-invariant. | Thm 4.1 |
| 11 | New certificate format: an **odd-length walk from a residual block to its complement** disproves extendability. | Cor 4.2 |
| 12 | **Vacuity**: for every admissible `k` with `2 < k < 16` there are fewer than `k-1` pairwise disjoint `S(k-1,k,2k)`'s, so (COT) has no instance. | Thm 5.1 |
| 13 | `LS(k-1,k,2k)` forces `LS(t,t+1,k+1+t)` for every `1 <= t <= k-1`; conditional on that top large set, the derived families attain the counting upper bound `k+1`. This reproduces the whole `k < 16` exclusion table from one lemma. | Thm 6.1, 6.2 |

Results 2, 3, 4, 5 and 13 overlap material already in the repository
(`verify_intersection_distribution.py`, `derivation_tower_obstruction/`,
`erdos_835_conjectural_resolution.md:78-87, 358-378`).  They are re-proved
here from scratch so the note is self-contained, and the derivations are
independent.

Novelty of 6, 7, 9, 10, 11, 12 is **not** asserted.  A targeted search
(`1-factor`, `one-factor`, `1-factorization` across `collaboration/`, plus a
directed read of the five frontier documents) did not surface them, but that
search returned ~30 files I did not read in full, so "new to this repository"
is unverified.  What is verified is that each is proved here from first
principles.

### Cited, not reproved

Cayley (max 2 disjoint Fano planes); Kramer--Mesner (max 2 disjoint
`S(5,6,12)`); Mendelsohn--Hung (no `S(4,5,15)`); Östergård--Pottonen (no
`S(4,5,17)`).  Each is used only inside Theorem 5.1 and each is sourced to a
line of `erdos_835_conjectural_resolution.md`.

### Open

(COT) itself; the converse of Corollary 3.4 (Lemma **LLS** in `IDEAS.md`);
everything at `k >= 16`.

## The one thing that changes what to do next

Theorem 5.1.  At the top rung the odd-transversal condition is **not** the
binding constraint on any decided parameter — the existence of `k-1` pairwise
disjoint systems is.  `k = 4` dies at 2 disjoint systems (need 3); `k = 6`
dies at 2 (need 5); `k = 10` and `k = 12` have no system at all.  So work
aimed at proving or refuting (COT) cannot be validated against any example,
and cannot on its own decide #835.  The productive direction is the local
lemma **LLS**, which is testable today on the two objects the repository
already owns.

## Independent verification status — read this

The Opus author could not execute `verify_common_odd_transversal.py`.
The later independent audit did execute it with Python 3.14. Its first run
found a parser defect in Part E: colour `0` alone was treated as residual,
although the authenticated partial has fifteen complete colour classes and
residual labels `-1`, `0`, and `13`. The parser now derives the complete
classes by their exact 285-block counts. After that correction, every asserted
finite check passed and Ruff reported no lint failures.

The run also settles the proposed stronger LLS-span experiment negatively:
on the `LS(2,3,9)` control,
`dim L = 11 < 13 = dim Z_1`; on the Etzion--Hartman partial,
`dim L = 467 < 587 = dim Z_1`. This does not refute the weaker Local Link
Sufficiency conjecture, but it rules out proving it merely by equality of
those two spaces on either control.

The Opus hand cross-checks recorded in `PROOF.md` remain useful: the
intersection formulas at `k = 2, 4, 6` (totals `2, 14, 132`, matching the
block counts of `S(1,2,4)`, `S(3,4,8)`, `S(5,6,12)`); the admissibility
criterion at `k = 8, 10, 12, 14, 24`; and Proposition 3.6, which is a direct
reading of two committed files.

## Deliverables

* `PROOF.md` — unconditional results only.
* `IDEAS.md` — rejected routes, why the abstract countermodels fail, and the
  single best remaining lemma.
* `verify_common_odd_transversal.py` — standard library only, independently
  executed after the documented Part E parser correction.
