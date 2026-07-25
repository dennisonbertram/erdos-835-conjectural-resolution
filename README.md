# Erdős–Rosenfeld Problem #835

A proof-oriented research record for Erdős–Rosenfeld Problem #835, with
rigorous reductions, exact structural theorems, and reproducible evidence.

## Status

The full problem remains open as of 24 July 2026. This repository does
**not** claim a complete proof. It advances and precisely formulates the
negative conjecture

\[
\chi(J(2k,k)) \geq k+2 \qquad (k>2),
\]

and proves several consequences and restricted obstructions. The first
unresolved case is \(k=16\).

New exact results in the note include:

- the Odd-graph covering equivalence and a reversible one- and two-point
  lift between the three neighboring Johnson graphs;
- uniformity of every ordered complementary colour-pair cell;
- an exact nonlinear finite-field kernel formulation, including a proof
  that a monochromatic local star forces the function to be constant;
- a large-set involution theorem: every nonidentity involution of a
  hypothetical \(LS(4,5,21)\) fixes exactly one point;
- nonexistence of an \(\operatorname{AGL}(5,2)\)-equivariant
  \(17\)-colouring; and
- nonexistence of every fusion of the natural 32-colour XOR-syndrome
  colouring down to seventeen colours; and
- a local power-sum obstruction excluding every single-maximal-minor
  construction over \(\mathbb F_{17}\), more generally over
  \(\mathbb F_p\) whenever \(p\equiv1\pmod4\).

These results close several natural algebraic and symmetric construction
routes, but not the asymmetric case.

## Contents

- [`erdos_835_conjectural_resolution.md`](erdos_835_conjectural_resolution.md):
  the complete mathematical note, literature review, proofs, conjecture, and
  explicit limitations.
- [`verify_k4.py`](verify_k4.py): exhaustively generates the 30 labelled
  \(S(3,4,8)\) systems and verifies that at most two are pairwise disjoint.
- [`search_cyclic_ls_4_5_21.py`](search_cyclic_ls_4_5_21.py): a CP-SAT exact
  cover model for a cyclic \(LS(4,5,21)\), including the reflection-restricted
  case.
- [`evidence/constructive_no_go.md`](evidence/constructive_no_go.md): full
  proofs excluding the affine-equivariant and XOR-fusion constructions.
- [`evidence/constructive_candidate_tests.md`](evidence/constructive_candidate_tests.md):
  exact tests and proofs excluding further algebraic candidates, including
  pair-local additive rules, hyperoctahedral symmetry, and several
  projective-line formulas.
- [`evidence/algebraic_construction_no_go.md`](evidence/algebraic_construction_no_go.md):
  three exact ansatz exclusions, including the maximal-minor obstruction;
  the accompanying verifier is
  [`evidence/verify_algebraic_construction_no_go.py`](evidence/verify_algebraic_construction_no_go.py).
- [`evidence/determinant_bridge_audit.md`](evidence/determinant_bridge_audit.md):
  an independent line-by-line audit of the maximal-minor proof and an
  explicit affine local countermodel showing why its power identities alone
  cannot be transferred to an arbitrary colouring.
- [`evidence/teichmuller_schur_no_go.md`](evidence/teichmuller_schur_no_go.md):
  the exact Fourier/Teichmüller colour algebra together with a coherent
  17-point Bose--Mesner quotient model; its verifier shows that this
  quotient-level Schur closure is compatible and therefore cannot by itself
  settle the problem.
- [`evidence/four_point_terwilliger_exact_witness.md`](evidence/four_point_terwilliger_exact_witness.md):
  an exact rational feasible witness for all colour-symmetrised triple-orbit
  equations, all colour-reduced Terwilliger PSD blocks, and the complete
  one-edge four-point extension.  This rules out that relaxation as a route
  to contradiction; it is not a colouring.
- [`evidence/mersenne_spin_functional_audit.md`](evidence/mersenne_spin_functional_audit.md):
  an exact audit of the Mersenne spin-functional route.  It proves that any
  hypothetical \(S(14,15,31)\) has full binary point-incidence rank, derives
  the complete \(2\)-adic subset-star norm filtration, and isolates the
  unresolved saturation and half-spin steps; it is not a nonexistence proof.
- [`evidence/full_color_block_hodge_audit.md`](evidence/full_color_block_hodge_audit.md):
  an exact audit of the full \(17\times17\) signed colour-block operator.
  It proves the majority-block nullity bounds, identifies the canonical
  projections as a regular tight-fusion simplex, and gives an exact-size
  voltage countermodel showing why block sparsity and two-step support counts
  alone do not capture the global Hodge cubic.
- [`evidence/three_way_trade.md`](evidence/three_way_trade.md): the exact
  three-leg trade-flow criterion, with small-case stress tests and an
  explicit statement of the remaining gap.
- [`evidence/fable_trade_quadratic.md`](evidence/fable_trade_quadratic.md):
  a proved mod-4 reduction for pair-trade codes, followed by the exact
  dimension theorem showing that universal doubly-evenness cannot hold at
  \(k=16\); any surviving parity obstruction must use the nonlinear
  exact-degree slice.
- [`evidence/modular_kernel/`](evidence/modular_kernel/): exact modular-kernel
  identities, a characteristic-17 module audit, and a tensor-ansatz
  obstruction.
- [`evidence/odd_graph_local_ball/`](evidence/odd_graph_local_ball/): an exact
  radius-three local-cover certificate and the derived radius-four
  one-factorization constraints. Local feasibility is not a global
  colouring.
- [`evidence/odd_matching_cells.md`](evidence/odd_matching_cells.md): exact
  odd cell counts, triangle-monodromy parity, and a cofactor-orientation
  identity for a hypothetical \(O_{16}\to K_{17}\) cover.
- [`evidence/state_sdp_p17/`](evidence/state_sdp_p17/): an exact rational
  certificate showing that the state-refined association-scheme relaxation
  remains feasible at \(p=17\); this is not a colouring.
- [`search_ls_3_4_20.py`](search_ls_3_4_20.py) and
  [`search_ls_3_4_20_exact_cover.py`](search_ls_3_4_20_exact_cover.py):
  independent CP-SAT formulations of the derived \(LS(3,4,20)\) condition.
  Bounded `UNKNOWN` results are exploratory evidence only.
- [`evidence/literature_and_x_search_2026-07-24.md`](evidence/literature_and_x_search_2026-07-24.md):
  exact recent X queries, the one matching preliminary report, and the
  full-archive tier limitation.
- [`evidence/verification.txt`](evidence/verification.txt): recorded output
  from the reproducibility checks.

## Reproduce the checks

Python 3.11 or newer is recommended.

```bash
python3 -m pip install -r requirements.txt
python3 verify_k4.py
python3 evidence/verify_constructive_no_go.py
python3 evidence/verify_constructive_candidates.py
python3 evidence/verify_algebraic_construction_no_go.py
python3 evidence/verify_teichmuller_schur_no_go.py
python3 evidence/verify_four_point_terwilliger_exact_witness.py
python3 -B evidence/verify_mersenne_spin_functional_audit.py
python3 evidence/verify_full_color_block_hodge_audit.py
python3 evidence/verify_three_way_trade.py
python3 evidence/modular_kernel/verify_modular_kernel.py
python3 evidence/odd_graph_local_ball/construct_radius3.py \
  --seconds-per-column 60 --workers 8
python3 evidence/state_sdp_p17/verify_state_sdp_p17.py
python3 search_cyclic_ls_4_5_21.py --reflection --seconds 30
python3 search_cyclic_ls_4_5_21.py --seconds 300
```

Expected decisive outputs:

- `verify_k4.py`: maximum pairwise disjoint systems = `2`, so no required
  five-colouring exists for \(k=4\).
- All exact evidence verifiers report that their stated checks pass.
- The radius-three constructor reproduces and verifies its local certificate;
  this deliberately makes no claim about a full Odd-graph cover.
- Reflection-restricted \(k=16\) model: `INFEASIBLE`.
- Unrestricted cyclic \(k=16\) model: currently `UNKNOWN` after the bounded
  five-minute search. This is neither an existence nor a nonexistence result.

## Primary references

- [Erdős Problem #835](https://www.erdosproblems.com/835)
- J. Ma and Q. Tang,
  [A Note on Erdős Problem #835](https://github.com/QuanyuTang/erdos-problem-835/blob/main/On_Problem_835.pdf)
- P. Hammond and D. H. Smith,
  [Perfect codes in the graphs \(O_k\)](https://doi.org/10.1016/0095-8956(75)90087-8)
- E. Kolotoğlu and S. S. Magliveras,
  [On the possible automorphism groups of a Steiner quintuple system of
  order 21](https://doi.org/10.1002/jcd.21370)

Additional references are listed in the main note.
