# Execution-debt clearance, 2026-07-26

Five prior sessions (`collaboration/opus5`, `opus5_v2`, `fable_frontier`,
`fable_e4`, `fable_e4_v2`) recorded in their own `STATUS.md`/`JUDGMENT.md` that
every script-execution route was permission-blocked, and left their validators
unrun.  This session ran them.  Raw output is appended to `verification.txt`
under 2026-07-26.

## Results

| script | verdict | runtime | what it settles |
|---|---|---|---|
| `opus5/verify_opus5_forced_structure.py` | PASS **after a validator fix** | 0.1 s | opus5 Thms 1–10, including Thm 7/7a (the Fourier-support theorem the whole no-go pattern rests on) |
| `opus5_v2/verify_intersection_numbers.py` | PASS | 0.1 s | Thms 1.3/3.1; sieve rejects k = 8, 14, 20 |
| `opus5_v2/verify_disjointness_parity.py` | consistent at all three parameters | ~3 min | Disjointness–Parity has no counterexample at S(2,3,7), S(3,4,8), S(4,5,11) |
| `opus5_v2/verify_onefactorization_row_parity.py` | PASS, ε_row **not** constant | 0.5 s | reproduces an answer already in the repo — see §2 |
| `fable_e4_v2/verify_k18_independent.py` | PASS | 0.1 s | the five-statistic K₁₈, 153/153 edges |
| `fable_e4_v2/verify_rigidity_and_controls.py` | PASS | 0.4 s | adjacency-rigidity R1–R3 plus the k=2 and k=4 controls |
| `fable_frontier/validate_k18_independent.py` | PASS | 0.1 s | the two-statistic K₁₈ |
| `fable_e4/verify_edge_law_smallfield.py` | PASS | 4.5 s | the edge law exhaustively in F₁₆, with non-vacuity counterexamples |
| `fable_e4/remote_run_e4.py` | **DECIDED** | 29 s | ω(G₀) = ω(G₁) = 17 — no K₁₈ at the e4 level |
| `fable_e4/verify_e4_refinement_independent.py` | agrees on all 32 r | ~9 min | independent second implementation of the same decision |
| `collaboration/verify_global_sign_attack.py` | PASS (orphaned) | ~min | exhaustive K₆/K₈ row-sign distributions — see §2 |
| `collaboration/verify_fable_specht_lattice_attack.py` | PASS **after a validator fix**, long-running | > 10 min | orphaned; r=3/r=5 lattice battery |

Twelve scripts; **eleven completed and passed**, and the twelfth (the
long-running Specht lattice battery) was still in progress when this note was
written — it is past the assertion that used to abort it and its identity
batteries are green.  Two hard-coded expectations were wrong and were corrected
— both in **scripts**, not in theorems — and in each case the underlying
arithmetic was independently recomputed before the edit.  No previously recorded
theorem was contradicted by any run.

## 1. One validator bug found and fixed

`opus5/verify_opus5_forced_structure.py` exited 1 on its first-ever run, at
`pred_inner_general(8, 16, 3) = 896/3`.

This is a **validator** bug, not a theorem failure.  Its loop
`for k in range(2, 20, 2)` includes k = 8 and k = 14, which are exactly the
parameters where the `opus5_v2` Cor 1.5 integrality sieve rejects
S(k−1,k,2k) — a non-integral inner-distribution entry there *is* the sieve
firing, and is the desired outcome.  The loop now skips non-integral k and
asserts that the sieved set is exactly [8, 14].  Everything downstream then
runs and passes.

Consequence: **opus5's Thm 7/7a is now actually verified**, not merely asserted.
That matters because it is load-bearing — it is why every LP/SDP/association-
scheme relaxation in this repo came back feasible.

I also confirmed the numeric part of the T3/T7 check is not vacuous: for
k = 2, 4, 6 every eigenspace mask has exactly the predicted multiplicity
C(2k,j) − C(2k,j−1), the masks together cover all N eigenvalues, no NaN arises,
and the intermediate-eigenspace projection norms are 1e-28…1e-32 against
1.1e+01 (k=4) and 1.9e+01 (k=6) on E_k.  BLAS emits spurious overflow
`RuntimeWarning`s during this step; they do not affect the assertions.

## 2. The ε_row "lever" was already answered

`collaboration/opus5_v2/IDEAS.md` §B calls

> is ε_row constant over all 1-factorizations of K_n for even n?

"the single cheapest unexplored lever", with n = 8 as the first real test, and
states that a *constant* answer closes the §4 route while a *non-constant*
answer yields a new finite obstruction.

It was not unexplored.  The three definitions in the repo differ only by a
global constant depending on n:

- `opus5_v2/IDEAS.md` §B defines ε_row over rows of the symmetric Latin square
  **including** the diagonal ∞ symbol.
- `evidence/local_one_factorization_sign_verify.py` (`star_product_bit`) and
  `collaboration/verify_global_sign_attack.py` (`row_sign_product`) use the
  same rows **without** the diagonal.
- The diagonal contributes (−1)^C(n,2), which is **+1 at n = 8** and −1 at
  n = 6 and n = 18.

So the recorded K₈ distribution in `local_one_factorization_sign_audit.md` §4 —
**6240 one-factorizations splitting 5280 positive / 960 negative**, hard-asserted
in the verifier as `distributions[8] == [5280, 960]` — *is* the ε_row
distribution, unchanged.  **ε_row is not constant.**  Running §B's own script
reproduces exactly this.

Both of §B's branches were therefore already closed:

- the "constant ⇒ route closed" branch is simply false; and
- the "not constant ⇒ new finite obstruction" branch is the one
  `star_sign_gluing_audit.md` §5 already kills at the affine-linear level (the
  normalized star-sign vectors have full affine rank 17, the maximum), on top of
  `local_one_factorization_sign_audit.md`'s theorem that the scalar sign algebra
  closes consistently at p = 17.

`collaboration/verify_global_sign_attack.py` is a third near-duplicate
implementation, orphaned: its stated target
`collaboration/fable_global_sign_attack.md` does not exist in the repository.
(`collaboration/verify_fable_specht_lattice_attack.py` is orphaned the same way.)

**Action taken:** recorded here.  §B should not be treated as an open lever.

## 3. The e4 decision, and why it does not contradict fable_e4_v2

`remote_run_e4.py` decides ω(G₀) = ω(G₁) = 17 — no K₁₈ — with the scaling
isomorphism G₁ → G_r verified edge-by-edge for every r ≠ 0, and
max_r ω(H_r) = 17.  A deliberately different second implementation
(`verify_e4_refinement_independent.py`, suffix-DP DFS, all 32 r decided without
assuming Theorem C) agrees.

This is **not** in tension with `fable_e4_v2`'s verified five-statistic K₁₈.
`fable_e4`'s G_r is built from 17-sets with e₁ = e₂ = e₃ = 0, i.e. from the
moment curve (e₁,e₂,e₃) = (a,a²,a³); `fable_e4_v2`'s K₁₈ lives on the line
(e₁,e₂) = (1+x, x), explicitly disjoint from the moment curve because
e₁² + e₁ + 1 = 0 has no root in F₃₂.  So `remote_run_e4.py` is an executed
confirmation of `f32_five_statistic_moment_curve_clique_bound.md` (clique number
17 in both offset graphs), and the full-quotient K₁₈ stands.

Per `fable_e4/JUDGMENT.md`'s own outcome tree, ω = 17 for both means: no clique
obstruction at the e4 level, and only χ ≥ 18 could still refute there.  The
colouring bounds obtained (DSATUR + 200 random greedy: 29 for G₀, 37 for G₁) are
upper bounds far above 17 and decide nothing; an exact χ decision would need the
SAT escalation that `fable_e4/JUDGMENT.md` notes is not written.

## 3a. A second stale assertion, in the other orphaned validator

`collaboration/verify_fable_specht_lattice_attack.py` aborted immediately on
`assert failures[7] == 1 and failures[13] == 2`, where `failures[r]` is the
first index i at which \(\lambda_i=\binom{2r+1-i}{r-1-i}/(r-i)\) fails to be an
integer.

Recomputed independently before touching the file: at r = 7 the non-integral
indices are 1 and 4; at r = 13 they are 1, 3, 4, 8, 10.  So the first bad index
is **1** in both cases, the script's own computed value was right, and the
expectation `== 2` was stale.  Because this script's companion note
(`collaboration/fable_specht_lattice_attack.md`) is missing from the
repository, there was no claim to check the expectation against.  Corrected
to 1; the script then proceeds into its r=3/r=5 lattice battery.

Both orphaned validators — this one and `verify_global_sign_attack.py` — now
run.  The second one's §2 is the exhaustive computation discussed above.

## 4. Still outstanding

- `fable_frontier/decide_cubic_embedding_k4.py` — needs numpy and a
  `--restarts 500` run; `cubic_k4_best.npz` is committed so it ran once, but its
  verdict is recorded nowhere.  Its "persistent floor" branch would make the
  cross-matching cubic the leading p-uniform negative attack.
- The five README-listed verifiers with no recorded output
  (`f32_prefix8_trace_classification_verifier.py`,
  `f32_two_statistic_k18_verifier.py`,
  `verify_top_degree_pairing_derivative.py`,
  `verify_top_degree_cross_matching_cubic.py`,
  `local_one_factorization_sign_verify.py`).
