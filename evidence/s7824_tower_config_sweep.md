# S(7,8,24) tower: pair-configuration sweep, forced constants, no contradiction

Date: 2026-07-26.  Validator: `verify_s7824_tower_config_sweep.py`
(exact rationals throughout; 16 s).  Status: **exact necessary-condition
audit of the derived tower; every test passes, so no nonexistence
result — the value is the forced structure and the certified
conditioning targets.**

Tower: D1 = S(7,8,24) (7-fold derived from S(14,15,31)), D2 = S(6,7,23),
D3 = S(5,6,22), D4 = S(4,5,21).  Any infeasibility below would have
refuted S(14,15,31); none occurred.

## 1. Forced pair distributions (all positive ⟹ every configuration exists)

n_j = blocks meeting a fixed block in j points:

- D1 (j=0..6): 758, 5376, 13216, 14336, 7560, 1792, 224
- D2 (j=0..5): 672, 3304, 5376, 3780, 1120, 168
- D3 (j=0..4): 472, 1536, 1620, 640, 120
- D4 (j=0..3): 256, 540, 320, 80

## 2. Delsarte is saturated tower-wide

\(\binom{v}{k}=17b\) in all four cases, and the dual (Q-) distribution
of the forced inner distribution is exactly \((1,0,\dots,0,16)\) for
every design (duality \(PQ=\binom vk I\) verified exactly before use).
Strength-t zeros plus the sum rule pin the tail at 16: **no
Delsarte-level obstruction exists anywhere in the tower.**

## 3. Configuration LPs: all feasible; forced cells certified

For each design and each intersection size j, the complete 4-cell
moment system (cells \(I,S_1,S_2,W\); all identities of total degree
≤ t; forced values from t-subset uniqueness) is FEASIBLE with an
exactly verified witness.  Certified cell bounds (LP min/max, each
endpoint verified by an achieving point plus dual multipliers lifted to
original-equation multipliers):

- The "closing" cell \(M(j,0,0,k{-}j)\) has range **identical down the
  tower at matching co-intersection**: \([20/3, 40]\), \([27,39]\),
  \([16,16]\), \([7,7]\) — the last two PINNED: every block pair of
  D1 meeting in 5 points has exactly **16** blocks on the complement
  core, and every pair meeting in 6 points exactly **7**; the same
  constants recur in D2, D3, D4 at shifted j.
- Forced-existence cells (LP min > 0) certified for conditioning:
  e.g. D1 j=4: closing cell ≥ 27 and W-block cell ≥ 2; D1 j=6:
  W-block cell ∈ [176,181].  Full table in the validator output.
- Bonus: the derived-level k=8 CASE Z1 (left unresolved in
  `verify_derived_closure_lp.py`'s original run) is FEASIBLE — max of
  the complement cell over the (D1, j=0) system is exactly 1, with the
  witness aggregated and re-verified against the k=8 Z1 system.

## 4. Reading

The first-order localized theory of the tower is completely
non-obstructive: pair distributions positive, Delsarte saturated,
every pair-configuration system feasible.  A direct S(7,8,24)
exclusion must therefore use deeper coupling: level-2 conditioning on
the certified forced cells (5-cell systems around a pair plus a forced
third block), the quintic/sextic dual-weight identities coupling
difference distributions (see `s141531_pair_difference_regularity.md`),
or global enumerative structure — not per-configuration counting.
