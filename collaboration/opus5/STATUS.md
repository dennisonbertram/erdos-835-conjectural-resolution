# Status — Opus 5 frontier session, 2026-07-25

## Session constraint (read first)

**No code was executed in this session.** Python invocation was
permission-blocked for the main agent and for a delegated subagent
(`python3 -c "print(6*7)"` → `This command requires approval`; the session is
non-interactive so approval could not be granted). Consequences:

* I did **not** re-run any of the ten frontier files I was asked to audit.
  My audit of them is a proof-reading audit only: I read the arguments and
  checked their mathematics by hand. I did not confirm that their verifiers
  still pass.
* Every numeric value in `PROOF.md` is derived symbolically and hand-checked
  against `k = 2, 4, 6`. Nothing is quoted from a program run.
* `verify_opus5_forced_structure.py` is an **unrun** validator. It must be
  run before `PROOF.md` is relied on.

## Verdict on the problem

Erdős–Rosenfeld #835 remains open. This session did not resolve it and did
not construct a tight colouring. It produced new unconditional structure
theorems, one new negative result about whole classes of proof methods, and
a sharpening of the reduction that changes where effort should go.

## Priority — what is genuinely new here, and what is not

Not new. That the block-intersection numbers are parameter-determined and
that the Delsarte/Johnson-positivity layer is exactly saturated was already
recorded in this project: `erdos_835_conjectural_resolution.md` lines 352–354
assert it in one sentence ("this regularity is a genuine theorem, not yet a
contradiction"), and a prior session verified it numerically at the target
parameters. Complement-closure of colour classes is also already in the note
(§4, via `ker M` and polytabloids).

New here. The closed-form formulas with proofs (Theorems 5, 5a, 6); the
general-`v` version that needs only `t = k-1` (Theorem 7a) and its two
corollaries — the tower-wide LP no-go (7.1) and the `v = 2k-1` nonexistence
(7.2); the upgrade from "verified at the target parameters" to "proved for
every `k` and every `v`, hence no method in this family can ever work"
(Theorem 7); the exact-one lemma and the crossing-matching bijection
(Theorem 1, Corollaries 1.1–1.2); the forced sub/superset counts and the
pointwise form of the tower (Theorem 4, Corollaries 4.1–4.3); the
Latin-square rigidity (Theorem 8); the local reformulation (Theorem 10);
and the two elementary corollaries 6.1 (odd `k` excluded by nonnegativity
alone) and 6.2 (complement-closure of a *single* system, no Specht module
needed).

## Strongest new proved results

All in `PROOF.md`, all self-contained.

1. **Theorem 7 / 7a (method no-go).** For **any** `S(k-1,k,v)` with
   `v ≥ 2k-1` — not just `v = 2k` — the indicator satisfies `Π_j f = 0` for
   `1 ≤ j ≤ k-1`, so its Fourier support in `J(v,k)` is contained in
   `{E_0, E_k}`. Hence the Delsarte LP is feasible at the exact design size,
   and **every** necessary condition that is a function of the inner
   distribution, the dual distribution, or any linear functional of slice
   degree `≤ k-1` is automatically satisfied. This is a proof, not a
   heuristic, that no LP/association-scheme/two-point method can ever refute
   existence — at `k = 16` *or at any level of the derived tower*, including
   `S(4,5,21)` and `S(3,4,20)` (Corollary 7.1). It retroactively predicts
   every "relaxation remains feasible" result already recorded in this
   repository.

2. **Theorems 5 and 6 (both two-point distributions in closed form).** For a
   block `B` of an `S(k-1,k,2k)` and `0 ≤ u ≤ k`:

       #{B' in same system : |B ∩ B'| = k-u} = C(k,u)[C(k,u) + (-1)^u k]/p
       #{B' in a disjoint system : |B ∩ B'| = k-u} = C(k,u)[C(k,u) - (-1)^u]/p

   Both are forced, uniformly. Cross-check at `k = 6`: `(1,0,45,40,45,0,1)`,
   which is the classical hexad intersection distribution of the Witt system
   `S(5,6,12)`. Theorem 5a extends the first formula to all `v`: with
   `P = v-k+1`,

       #{B' : |B ∩ B'| = k-u} = C(k,u)[ C(v-k,u) + (-1)^u (P-1) ]/P,

   which forces the block-intersection distribution of a hypothetical
   `S(4,5,21)` to be `(1, 0, 80, 320, 540, 256)` for
   `|B ∩ B'| = 5,4,3,2,1,0`, total `1197`. All nonnegative integers, so this
   too yields no obstruction — but it is a concrete, checkable new fact about
   an object nobody has constructed.

3. **Corollary 6.1 / 6.2 / 7.2.** Nonnegativity of the `u = k` term alone
   excludes every odd `k > 1`. For even `k`, `n_0 = 1` gives
   complement-closure of a *single* `S(k-1,k,2k)` with no Specht-module
   argument and no large set. And at the boundary `v = 2k-1` there is no
   `E_k` at all, so Theorem 7a forces `f` constant: **no `S(k-1,k,2k-1)`
   exists for any `k ≥ 2`.**

4. **Theorem 1 (exact-one lemma).** Every `(k+1)`-set contains exactly one
   block. Proof: two blocks in one `(k+1)`-set force a repeated
   `(k-1)`-set, so the count is `≤ 1`; the average is exactly `1`.

5. **Theorem 4 and Corollary 4.1 (the tower, sharp form).** For every
   `1 ≤ j ≤ k` and every `(k+j)`-set `U`, the number of blocks inside `U` is
   exactly `binom(k+j,j)/p`, and `{U \ B : B ⊆ U}` is an `S(j-1,j,k+j)` on
   `U`. So the derived tower is a *pointwise* statement about every `U`, not
   just one derivation.

6. **Theorem 8 (Latin-square rigidity).** In any tight colouring, for every
   `k`-set `S` the array `L_S(x,y) = c(S \ {x} ∪ {y})` on `S × (V\S)` is a
   Latin square of order `k` on the `k` colours other than `c(S)`.

7. **Theorem 9.** At most `p` pairwise disjoint `S(k-1,k,2k)` exist, with
   equality iff they form the large set — the large-set condition is the
   equality case of an otherwise slack PSD constraint.

8. **Theorem 2.** `λ_s = binom(k+m,m)/(k+1)`, `m = k-s`; integrality for all
   `s` holds iff `k+1` is prime, with a complete proof of the composite
   direction via `v_q(binom(n+q-1,q)) = v_q(n) - 1`.

## The exact gap

A nonexistence proof must use, simultaneously:

* a functional of **full slice degree `k`** (a nonzero pairing against
  `E_k` — everything of lower degree is forced, Theorem 7); **and**
* pointwise idempotence `f_a f_b = δ_{ab} f_a` at **third order or higher**
  (all second-order consequences are forced, Theorems 5–6, 9).

That is exactly the position of the cross-matching cubic (8) in
`evidence/top_degree_cross_matching_cubic_audit.md`. Theorem 7 upgrades that
file's observation "the quadratic relaxation is feasible at the false `k=4`"
from an experimental finding to a theorem valid for every `k`: the quadratic
level *cannot* fail, ever.

## Audit of the ten frontier files I was asked to check

Proof-reading only; no verifier was re-run (see session constraint).

* `f32_prefix8_trace_hyperplanes.md` — Theorems 1 and 2 read as correct.
  The step I checked hardest is (5): `L | (X^32 + X) + L^2` forces
  `L = X^16 + uX^8 + u^{-14}X^4 + u^{-6}X^2 + u^{-2}X = b^{-16}Tr(bX)`. The
  degree/leading-coefficient argument excluding `u = 0` is sound. The
  `B_0 = 0` computation identifying which factor contains zero is the
  delicate part and is correctly done.
* `f32_two_statistic_k18_obstruction.md` — the logic (a `K_18` in the
  statistic quotient plus pigeonhole) is valid; the 17 masks are a finite
  certificate I could not recompute without execution. **Unverified here.**
* `top_degree_pairing_derivative_audit.md` — the frame identity (7) is
  correct: `A = Σ_M e_M e_M^T` is `S_{2k}`-equivariant on the irreducible
  `K_Q`, hence scalar, and trace gives `|M|2^k / dim K_Q = (k+1)!`. Consistent
  with my Theorem 3 (`K_Q = E_k`, `dim = C_k`).
* `top_degree_cross_matching_cubic_audit.md` — (4), (5), (7), (8) are
  correct. Its `k=4` feasible relaxation is now explained by my Theorem 7.
* `local_one_factorization_sign_audit.md` — the scalar no-go is correctly
  argued; the model (9) does satisfy both generator families, so the
  conclusion "no derivation of `-1 = +1` in that sign algebra" stands.
* `full_slice_degree_necessity.md` — correct, and it is the exact dual of my
  Corollary 3.1: it says the *colouring* has full degree, mine says every
  *count* of degree `< k` is forced. Both follow from `f_a - 1/p ∈ E_k`.
* The three `.py` verifiers and `f32_two_statistic_k18_search.py` were read
  for intent, not executed.

## What this changes about the construction side

Corollary 4.3: a tight `17`-colouring at `k = 16` implies an `LS(4,5,21)` —
seventeen pairwise disjoint `S(4,5,21)` systems — and in particular that a
single `S(4,5,21)` exists. This repository's own literature section records
`S(4,5,15)` and `S(4,5,17)` as *proved nonexistent* (Mendelsohn–Hung;
Östergård–Pottonen) and `S(4,5,21)` as the first unsettled order, citing
Kolotoğlu–Magliveras on its possible automorphism groups.

So searching for "a richer explicit construction not killed by the
two-statistic `K_18`" at `k = 16` is searching for something that would
settle a separate long-standing open existence problem as a by-product.
That is the correct place to record effort, not a reason to stop, but it
means finite-field colour formulas over `F_32` are the wrong instrument: any
such formula would have to produce 17 disjoint `S(4,5,21)`s inside every
`21`-subset of `[32]` simultaneously.

The redirection I recommend is to attack `LS(4,5,21)` directly: its
nonexistence kills `k = 16` by Corollary 4.2, and it is a `21`-point,
`20349`-cell, `17`-class exact-cover instance rather than a `32`-point one.
Note this is *not* algebraically softer — Corollary 7.1 and Theorem 5a show
its LP is equally feasible and its intersection distribution equally forced —
the gain is purely that the search space is four orders of magnitude smaller,
so the SAT/CP-SAT machinery already in this repository can address it.

*Literature-dependent claim, not verified in this session:* the same tower at
`j = 7` requires an `S(6,7,23)`, and I believe no nontrivial Steiner system
with `t ≥ 6` has ever been constructed. If that is right, every open case
`k ≥ 16` requires a first-of-its-kind object. I did not check this claim
against sources here and it should be confirmed before being used.

## Files added

* `PROOF.md` — Theorems 1–9 with complete proofs.
* `IDEAS.md` — attacks attempted and not completed, with honest assessments.
* `verify_opus5_forced_structure.py` — unrun independent validator for every
  finite claim in `PROOF.md`.
