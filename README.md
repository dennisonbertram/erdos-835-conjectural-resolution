# Erdős–Rosenfeld Problem #835

A proof-oriented research record for Erdős–Rosenfeld Problem #835, with
rigorous reductions, exact structural theorems, and reproducible evidence.

## Status

The full problem remains open as of 26 July 2026. This repository does
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
  \(\mathbb F_p\) whenever \(p\equiv1\pmod4\); and
- an exact integrability theorem showing that the full simultaneous
  transposition-flow system is equivalent to a single global colouring
  potential, so this formulation introduces no hidden weaker solutions;
- a precise audit of Teirlinck's ordered-design theorem: it gives a weighted
  support design at \(k=16\), but not the required orbit-closed large set;
- no-go theorems for every quadratic incidence-polynomial colouring, every
  additive binary syndrome decoded by an arbitrary \(4\)-spread (including
  Kerdock spreads), and the natural cyclic-\(17\) barycentre family; and
- a no-go theorem for the exact Hamming-weight coincidence
  \(A_{14}+A_{15}=17{,}678{,}835\): no choice of one-point extensions of
  the weight-\(14\) supports can coexist with all natural weight-\(15\)
  supports as an \(O_{16}\) perfect code;
- a general degree theorem: every nonconstant zero-sum statistic of a
  hypothetical tight prime colouring has maximum slice degree; and
- a \(32\)-clique certificate excluding every arbitrary postprocessing of
  the first seven \(\mathbb F_{32}\) half-set coefficients at \(k=16\);
  and
- an exact classification of the coefficient-eight boundary: every
  \(15\)-set with \(e_1=\cdots=e_7=0\) is a trace hyperplane, and its lifted
  coefficient-eight layer is \(K_{17}\sqcup15K_1\); and
- an explicit actual-edge \(K_{18}\) excluding every colouring based only
  on \((e_1,e_8+e_1^8)\), strengthened to an actual-edge \(K_{32}\) after
  retaining the larger tuple
  \((e_1,e_2,e_3,e_8+e_1^8)\), with completely arbitrary postprocessing;
  and
- an exhaustive coefficient-four boundary for that \(K_{32}\): every
  moment-curve edge has a common offset \(e_4+a^4\), and the two resulting
  finite graphs both have exact clique number \(17\), so this template
  cannot be lifted to a \(K_{18}\) after retaining \(e_4\); and
- an explicit actual-edge \(K_{18}\) in the full five-statistic quotient
  \((e_1,e_2,e_3,e_4,e_8+e_1^8)\), witnessed by three concrete
  \(15\)-sets and all \(153\) pairwise exchanges.  Thus the apparent
  moment-curve escape does not extend to the full quotient; and
- an exact matching-cube top-derivative frame and its projected
  zero-one cubic identity, including a complete support formula for its
  triple-polytabloid tensor and the first overlap-sensitive \(2\)-adic
  quotient, together with audited controls showing that the corresponding
  modular, quadratic, SOS, scalar-sign, and proposed Norton \(1/3\)-gap
  reductions do not finish the degree-\(16\) case;
- an exact defect-map reduction whose indegrees are rainbow-triangle
  counts, together with a coherent \(LS(2,3,19)\) certificate realizing
  every multiplicity from zero through six and an orientation-boundary
  identity.  This proves that the complete codimension-three link layer
  does not force bijectivity; the next genuine compatibility layer is
  \(LS(3,4,20)\);
- the complete forced binary weight enumerator of a hypothetical
  \(S(14,15,31)\) point-incidence code, plus a Fourier-averaging theorem
  proving that **no** common-zero shortening in any dimension can violate
  Griesmer when the unresolved middle layer is bounded only by independent
  endpoints.  This closes that coding route, not the design or the large
  set;
- a static rational facet-profile certificate proving that every
  intersection-six block pair in a hypothetical \(S(14,15,31)\) has at
  least \(666\) completing blocks of profile \((0,4,4,7)\).  Their
  complements force affine two-flats of weights
  \((14,16,16,16)\), so the numerically best dimension-two shortening
  has exact parameters
  \([4\,419\,003,28,2\,197\,848]\) and still misses Griesmer by
  \(23\,291\);
- an exhaustive perfect-information closure of **every**
  dimension-two common-zero shortening: even after allowing arbitrary
  joint resolution of all middle-layer indicators, each candidate
  satisfies Griesmer with at least \(14\,940\) slack.  Dimensions three
  and above remain open under such coupling;
- exact cyclic prescribed-link completions for all \(105\) radius-five
  slices, directly reconstructed as \(1{,}785\) Steiner triple systems;
  their shared-\(N\) compatibility still fails in the checked seeds, so
  they are not a radius-five witness; and
- at the next candidate prime \(p=19\), an exact obstruction to the
  maximal-minor construction and to every principal-Pfaffian construction
  of rank at most \(18\), together with exhaustive no-go results for the
  lifted normal-rational-curve and lifted circulant rank-four links, and a
  \(3{,}353{,}011{,}200\)-job exact exclusion of every rank-at-most-four
  paired half-link.  Arbitrary rank-four links and higher-rank Pfaffian
  matrices remain open.

- a reduction proving that the triangle-closure law for boundary Steiner
  systems is exactly a statement about the design derived at the pair
  intersection, an \(S(m,m+1,3m+3)\) with \(m=(r-1)/2\).  It follows whenever a
  block of that design is disjoint from exactly two others, which happens
  **only** at \(r=3,5\) (the count is \(22\) at \(r=9\) and \(758\) at
  \(r=15\)).  This proves the law at \(r=3,5\) and shows the exhaustive
  verifications there carry no weight at \(r=15\), where it becomes a
  resolvability statement about a hypothetical \(S(7,8,24)\).  That statement is
  then **refuted**: a triangle-closure triple is exactly a weight-3 word of the
  even-subcode dual, whose count is forced at \(927\,696\,866\,625\), so only
  \(10495/162591\approx6.45\%\) of critical pairs complete, against ratio
  exactly \(1\) at \(r=3,5\); and
- a closure of the third-moment shortening route for \(S(14,15,31)\): because a
  weight-3 dual word of the even subcode is exactly such a triple,
  \(\sum(n-2w)^3=|C|\cdot6A_3(Z_H)\ge0\), so a strictly negative third moment is
  what an existing design predicts rather than a contradiction.  Exact dual
  certificates give
  \(57\,485\,606\,222\le A_3(Z_H)\le60\,070\,286\,637\); and
- the exact autocorrelation law of every hypothetical \(S(14,15,31)\):
  the number of block pairs with symmetric difference \(D\) is uniform on every
  even weight layer, except for the forced \(157\,425/142\,590\) split at
  \(|D|=16\).  A direct inverse Fourier transform proves that this strong
  regularity is already equivalent to the forced weight enumerator, so it is a
  consistency theorem and candidate falsification test, not an obstruction; and
- the complete higher block-XOR hierarchy of a hypothetical \(S(14,15,31)\).
  A \(j\)-subset of blocks is a dual word exactly when its XOR is \(0\) (\(j\)
  even) or all-ones (\(j\) odd), and the general law
  \(a_j(D)=g_j(|D|)+\Delta_jF(D)/2^{30}\) shows every \(j\)-fold XOR count is
  uniform on weight layers apart from one split — at \(|D|=15\) for odd \(j\),
  \(|D|=16\) for even \(j\).  This yields the forced values
  \(A_5=13\,402\,303\,385\,620\,814\,734\,177\,080\) and
  \(A_6=39\,490\,202\,682\,224\,904\,419\,269\,612\,470\,360\), the exact
  identities \(\sum_Dm_Dt_{\mathbf 1+D}=10A_5+3(b-3)A_3\) and
  \(\sum_Et_E^2=\binom b3+6(b-4)A_4+20A_6\), and the per-block identity
  \(4A_4/b=858\,252\,625\,232\); convexity is tight at \(j=4\) but has slack
  \(354\,375\,828\,032\,095\,615\,907\,520\) at \(j=6\).  Being an inverse
  transform of the forced enumerator does **not** make the hierarchy vacuous:
  non-negativity and exact integrality of \(a_j(D)\) are genuine
  MacWilliams/Delsarte-type necessary conditions.  The **positivity** half is
  a theorem for all \(j\): for nontrivial \(u\) one has
  \(|F(u)|\le b/31\), so a Cauchy estimate against the maximal binomial term
  gives \(|K_j(F)|/\binom bj\le(b+1)\rho^{\,b-f}\) with
  \(\rho^{\,b-f}\le\exp(-30j(b-j)/(31b))\); the two trivial characters
  contribute \(2\binom bj\) and dominate the other \(2^{31}-2\) for
  \(40\le j\le b-40\), which with the finite sweep gives \(a_j(D)\ge0\) for
  **every** \(j\).  The **integrality** half is now closed as well.  A
  Δ-divisibility lemma handles the two middle branches; factoring out
  \((1-z^2)^{8\,554\,275}\) reduces the nontrivial terms to nine
  degree-\(570\,285\) cofactors; and a tail theorem makes every condition with
  \(j\ge570\,315\) automatic modulo \(2^{31}\).  Independent Python and C++
  NTT/CRT computations certify the complete remaining window with zero
  violations (the C++ run checks \(9\,125\,520\) on-parity conditions).
  Finally, the formal identity
  \((1-z^2)A'(z)=b(C_B(z)-zA(z))\), proved from explicit binomial identities,
  shows that \(a_j(D)\)-integrality implies both \(A_j\)-integrality and
  \(b\mid jA_j\).  Thus the entire higher-XOR necessary-condition route is
  closed and yields no contradiction; it does not solve #835; and
- an exact elementary modular audit of the two necessary designs
  \(S(14,15,31)\) and \(S(7,8,24)\).  Forced incidence-Gram spectra,
  Wilson-rank upper bounds, determinant divisibility, chain squeezes, and
  honest mod-\(p\) ranks through inclusion level three all close consistently;
  several ranks saturate exactly.  A rectangular point-Gram factorization and
  an exhaustive check of the standard modular intersection-rank contradiction
  also give no obstruction.  These results close only the explicitly stated
  tests; higher-Gram lattice structure and \(0/1\) compatibility remain open;
  and
- a structural proof of the \(k=4\) case: the \(30\) systems \(S(3,4,8)\) are
  the \(30\) maximal totally singular subspaces of a hyperbolic \(O_6^+(2)\)
  form, block-disjointness forces opposite Klein families, and there are only
  two families — so at most two are pairwise disjoint.  This replaces the
  brute-force count with a mechanism and realizes the conjectured
  disjointness-parity sign at \(k=4\); and
- a parameter-free "one short of a large set" lemma: \(P-1\) pairwise disjoint
  \(S(k-1,k,v)\) force a \(P\)-th, so the maximum number of pairwise disjoint
  systems is never exactly \(P-1\).  In particular no search for \(16\)
  pairwise disjoint \(SQS(20)\), or for \(16\) pairwise disjoint
  \(S(15,16,32)\), can succeed.

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
- [`evidence/five_point_star_gluing_status.md`](evidence/five_point_star_gluing_status.md):
  an exact rational feasible certificate for the stronger free-\(F\),
  full-position-reorder, re-based five-point necessary relaxation.  The
  independent checker verifies \(441{,}905\) rational equalities and
  \(5{,}118{,}391\) nonzero coefficients; feasibility closes this LP route
  but is not a colouring.
- [`evidence/mersenne_spin_functional_audit.md`](evidence/mersenne_spin_functional_audit.md):
  an exact audit of the Mersenne spin-functional route.  It proves that any
  hypothetical \(S(14,15,31)\) has full binary point-incidence rank, derives
  the complete \(2\)-adic subset-star norm filtration, and isolates the
  unresolved saturation and half-spin steps; it is not a nonexistence proof.
- [`evidence/s141531_incidence_code_audit.md`](evidence/s141531_incidence_code_audit.md):
  the forced \([17\,678\,835,31]\) point-incidence weight enumerator,
  its \(30\)-dimensional even subcode, initial MacWilliams checks, and
  exact simplex-shortening parameters.
- [`evidence/s141531_griesmer_averaging_no_go.md`](evidence/s141531_griesmer_averaging_no_go.md):
  a global Fourier-averaging proof that independent size-\(16\) endpoint
  bounds plus common-zero shortening and Griesmer cannot contradict a
  hypothetical \(S(14,15,31)\), for any shortening subspace.
- [`evidence/s141531_dim2_subcode_audit.md`](evidence/s141531_dim2_subcode_audit.md):
  an exhaustive \(1{,}450\)-profile dimension-two shortening audit and
  two explicitly nonexhaustive dimension-three controls.
- [`evidence/s141531_affine_triple_forcing.md`](evidence/s141531_affine_triple_forcing.md):
  an exact nonlinear refinement of the dimension-two audit.  A static
  rational dual forces abundant three-block profiles and proves that all
  three uncertain size-\(16\) endpoints in the best affine coset occur
  simultaneously; this closes that candidate but is not a design or a
  nonexistence proof.
- [`evidence/s141531_m2_perfect_info_closure.md`](evidence/s141531_m2_perfect_info_closure.md):
  an exhaustive \(1{,}450\)-profile theorem closing the entire
  dimension-two common-zero/Griesmer route even with perfect joint
  knowledge of the middle layer.  The checked per-profile table is
  [`evidence/s141531_dim2_margins.csv`](evidence/s141531_dim2_margins.csv).
- [`evidence/boundary_triangle_closure.md`](evidence/boundary_triangle_closure.md):
  exact coset-cell calibration at the Fano and Witt boundary systems.
  It isolates a triangle-closure law verified at \(r=3,5\) but explicitly
  conjectural at \(r=15\).
- [`evidence/full_color_block_hodge_audit.md`](evidence/full_color_block_hodge_audit.md):
  an exact audit of the full \(17\times17\) signed colour-block operator.
  It proves the majority-block nullity bounds, identifies the canonical
  projections as a regular tight-fusion simplex, and gives an exact-size
  voltage countermodel showing why block sparsity and two-step support counts
  alone do not capture the global Hodge cubic.
- [`evidence/transposition_flow_cocycle.md`](evidence/transposition_flow_cocycle.md):
  a universal necessary condition for \(k=16\).  Every hypothetical colouring
  forces 496 compatible nowhere-zero \(\mathbb F_{17}\) top-Specht flows,
  with exact row-derangement, anti-complement, Frobenius, and triangle-cocycle
  identities.  The accompanying \(k=4\) control proves that one isolated flow
  is insufficient; simultaneous compatibility is the unresolved content.
- [`evidence/simultaneous_flow_integrability.md`](evidence/simultaneous_flow_integrability.md):
  a proof that reversal, same-star triangles, and all pair-kernel equations
  integrate the complete simultaneous family to a unique global potential.
  With full support at \(k=16\), this is exactly a tight \(17\)-colouring,
  not a relaxation or a solution.
- [`evidence/three_way_trade.md`](evidence/three_way_trade.md): the exact
  three-leg trade-flow criterion, with small-case stress tests and an
  explicit statement of the remaining gap.
- [`evidence/fable_trade_quadratic.md`](evidence/fable_trade_quadratic.md):
  a proved mod-4 reduction for pair-trade codes, followed by the exact
  dimension theorem showing that universal doubly-evenness cannot hold at
  \(k=16\); any surviving parity obstruction must use the nonlinear
  exact-degree slice.
- [`evidence/block_local_sign_rowspace_no_go.md`](evidence/block_local_sign_rowspace_no_go.md):
  an exact small-case audit showing that the most natural block-local sign
  has reference-order-dependent rowspace membership and that the exterior
  sign retains genuine quadratic crossing terms.  This closes that proposed
  linearization route, not the parity conjecture or Problem #835.
- [`evidence/defect_facet_map_audit.md`](evidence/defect_facet_map_audit.md):
  the exact defect-map/rainbow-triangle correspondence, its corrected
  universal indegree bound, and explicit local countermodels.
- [`evidence/defect_cross_link_lsts19.md`](evidence/defect_cross_link_lsts19.md):
  the full link-tower reduction, a verified coherent \(LS(2,3,19)\)
  countermodel to link-local bijectivity, and the scalar orientation
  boundary identity.  This is a no-go for one proof layer, not a colouring.
- [`evidence/modular_kernel/`](evidence/modular_kernel/): exact modular-kernel
  identities, a characteristic-17 module audit, and a tensor-ansatz
  obstruction.
- [`evidence/odd_graph_local_ball/`](evidence/odd_graph_local_ball/): an exact
  radius-three certificate, the full radius-four reduction, and an explicit
  cyclic-golf radius-four colouring.  The latter was checked semantically on
  all \(14{,}657\) ball vertices and against every clause of an independently
  generated \(738{,}537\)-clause CNF.  Radius five and global extension
  remain open, so this local feasibility is not a global colouring.
- [`evidence/odd_graph_local_ball/radius5_large_set_equivalence.md`](evidence/odd_graph_local_ball/radius5_large_set_equivalence.md):
  an exact equivalence between one minimal-trace radius-five slice and a
  prescribed-link \(LS(2,3,19)\), plus an eight-`AllDifferent` cyclic
  quotient.  All \(105\) slices now have independent exact completions,
  while their shared-\(N\) compatibility remains the decisive condition.
- [`evidence/cyclic17_all_105_exact_slices_status.md`](evidence/cyclic17_all_105_exact_slices_status.md):
  the exact certificates, independent verifier, and carefully limited scope
  for those \(105\) separately feasible prescribed-link slices.
- [`evidence/cyclic17_equivariant_reduction.md`](evidence/cyclic17_equivariant_reduction.md):
  the exact layer recursion under a colour-transitive order-\(17\)
  symmetry, with a direct-verified 40-phase certificate for one
  prescribed-link \(LS(2,3,19)\) slice.  The joint layer, later layers,
  and asymmetric colourings remain open.
- [`evidence/global_latin_compatibility.md`](evidence/global_latin_compatibility.md):
  the exact Latin-square transition, its golf-design form, a cyclic
  \(G(17)\), and the verified bridge through the complete radius-four ball.
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
- [`search_s_4_5_21_extension.py`](search_s_4_5_21_extension.py):
  an exact-cover search for the necessary \(S(4,5,21)\) extension.  Its
  unrestricted mode uses a lossless first-link normalization and splits a
  second link into seven exhaustive alternating-cycle types.  Restricted
  `INFEASIBLE` and bounded `UNKNOWN` results do not settle \(k=16\).
- [`evidence/s_4_5_21_cnf.py`](evidence/s_4_5_21_cnf.py) and
  [`evidence/audit_s_4_5_21_cnf.py`](evidence/audit_s_4_5_21_cnf.py):
  a direct DIMACS exact-cover encoding of the same seven unrestricted cases
  and an independent clause-by-clause comparison with the CP-SAT model.
  A decoded SAT witness would be checked as a complete \(S(4,5,21)\);
  an UNSAT claim still requires an independently checked proof certificate.
- [`evidence/literature_and_x_search_2026-07-24.md`](evidence/literature_and_x_search_2026-07-24.md):
  exact recent X queries, the one matching preliminary report, and the
  full-archive tier limitation.
- [`evidence/x_search_refresh_2026-07-26.md`](evidence/x_search_refresh_2026-07-26.md):
  a fresh, explicitly limited seven-day X claim search.  It found no post
  claiming a solution of #835; this is not evidence of priority or absence.
- [`evidence/large_set_literature_attack_2026-07-25.md`](evidence/large_set_literature_attack_2026-07-25.md):
  a primary-literature audit of the exact
  \(LS(15,16,32)\)/\(O_{16}\) frontier and the nearby theorems that do not
  settle it.
- [`evidence/ordered_design_symmetrization_audit.md`](evidence/ordered_design_symmetrization_audit.md):
  the exact weighted-support gap between Teirlinck's
  \(LOD(15,16,32)\) and the required large set.
- [`evidence/kerdock_spread_additive_syndrome_no_go.md`](evidence/kerdock_spread_additive_syndrome_no_go.md)
  and [`evidence/cyclic17_barycenter_kerdock_spread_no_go.md`](evidence/cyclic17_barycenter_kerdock_spread_no_go.md):
  exact exclusions of the additive spread/Kerdock decoder and cyclic
  barycentre construction families.
- [`evidence/hamming_weight_bridge_no_go.md`](evidence/hamming_weight_bridge_no_go.md):
  the exact obstruction to turning the binary Hamming weight-\(14\) and
  weight-\(15\) enumerator coincidence into an \(O_{16}\) perfect code.
- [`evidence/quadratic_coloring_ansatz_no_go.md`](evidence/quadratic_coloring_ansatz_no_go.md):
  a symbolic no-go theorem for all degree-at-most-two incidence-polynomial
  colourings over the candidate prime field.
- [`evidence/full_slice_degree_necessity.md`](evidence/full_slice_degree_necessity.md):
  the maximum-slice-degree necessity theorem for every surviving prime
  parameter.
- [`evidence/f32_halfset_prefix_no_go.md`](evidence/f32_halfset_prefix_no_go.md):
  an exact \(32\)-clique obstruction to all first-seven-coefficient
  half-set-polynomial colour rules.
- [`evidence/f32_prefix8_affine_boundary.md`](evidence/f32_prefix8_affine_boundary.md):
  the exact point where that affine clique template fails at coefficient
  eight; this is a boundary result, not a general eight-prefix no-go.
- [`evidence/f32_prefix8_trace_hyperplanes.md`](evidence/f32_prefix8_trace_hyperplanes.md):
  the exact trace-hyperplane classification at coefficient eight, including
  the induced \(K_{17}\sqcup15K_1\) lifted-layer graph.
- [`evidence/f32_two_statistic_k18_obstruction.md`](evidence/f32_two_statistic_k18_obstruction.md):
  an explicit actual-edge \(K_{18}\) ruling out every
  \(F(e_1,e_8+e_1^8)\) colour rule.  This excludes that full two-statistic
  family, not arbitrary tight colourings.
- [`evidence/f32_four_statistic_k32_obstruction.md`](evidence/f32_four_statistic_k32_obstruction.md):
  a stronger actual-edge \(K_{32}\) which survives after retaining \(e_2\)
  and \(e_3\) as well.  It proves that every colouring in this family needs
  all 32 colours, while still leaving later coefficients and arbitrary
  colourings open.
- [`evidence/f32_five_statistic_moment_curve_clique_bound.md`](evidence/f32_five_statistic_moment_curve_clique_bound.md):
  the exact \(e_4\) boundary of that moment-curve obstruction.  Every clique
  in the family lies in one of two offset graphs, and exhaustive
  meet-in-the-middle enumeration gives clique number \(17\) in both.
- [`evidence/f32_five_statistic_k18_obstruction.md`](evidence/f32_five_statistic_k18_obstruction.md):
  a three-mask static certificate for an actual-edge \(K_{18}\) in the
  complete five-statistic quotient.  It rules out every arbitrary
  postprocessing of those five statistics, not arbitrary colourings.
- [`evidence/mate_cross_gram_determinant_audit.md`](evidence/mate_cross_gram_determinant_audit.md):
  a narrowed audit of direct fixed determinant, invertibility, and
  first-cofactor tests for two mates.
- [`evidence/top_degree_pairing_derivative_audit.md`](evidence/top_degree_pairing_derivative_audit.md):
  the exact matching-cube derivative frame and the remaining
  cross-matching/zero-one compatibility gap.
- [`evidence/top_degree_cross_matching_cubic_audit.md`](evidence/top_degree_cross_matching_cubic_audit.md):
  the exact projected-idempotence cubic coupling different matchings, with
  true and false small-parameter controls.
- [`evidence/triple_polytabloid_tensor_support_audit.md`](evidence/triple_polytabloid_tensor_support_audit.md):
  a complete support-and-sign formula for the cubic tensor.  Its direct
  mod-\(2\), mod-\(4\), mod-\(17\), and first Hilbert--Schmidt SOS tests
  close consistently rather than contradicting the target.
- [`evidence/triple_tensor_2adic_threshold_audit.md`](evidence/triple_tensor_2adic_threshold_audit.md):
  the exact first overlap-sensitive \(2\)-adic lift.  At \(k=16\) the
  first 28 bits are forced identities; the normalized quotient detects
  overlap, but exact disjoint \(k=4\) controls realize both parities.
- [`evidence/unprojected_fourth_moment_completion.md`](evidence/unprojected_fourth_moment_completion.md):
  the sharp boundary beyond the projected cubic.  The missing fourth
  moments form a positive-semidefinite \(K^\perp\)-residual Gram matrix;
  attaining the model lower bound is exactly equivalent to recovering an
  actual tight colouring, rather than a cheaper obstruction.
- [`evidence/norton_one_third_gap_no_go.md`](evidence/norton_one_third_gap_no_go.md):
  an exact moment audit showing that the tempting Norton nonzero-spectrum
  gap at \(1/3\) would itself already be a nonexistence theorem.  Any
  hypothetical target constituent is instead forced to have at least
  \(12{,}723{,}868\) eigenvalues below \(1/3\).
- [`evidence/local_one_factorization_sign_audit.md`](evidence/local_one_factorization_sign_audit.md):
  an exact descent of the scalar one-factorization sign route.  It recovers
  the \(p=5\) contradiction but proves that the scalar signs close
  consistently at \(p=17\).
- [`evidence/determinant_link_p19.md`](evidence/determinant_link_p19.md):
  a proof that the ordered rank-two determinant link, and hence the
  maximal-minor colouring ansatz, is impossible over \(\mathbb F_{19}\).
- [`evidence/p19_rank4_half_catalog_schur_search.md`](evidence/p19_rank4_half_catalog_schur_search.md):
  the complete 210-anchor Schur-complement exhaustion excluding every
  rank-at-most-four paired half-link over \(\mathbb F_{19}\), with explicit
  scope boundary and independent controls.
- [`evidence/p19_principal_pfaffian_frontier.md`](evidence/p19_principal_pfaffian_frontier.md):
  the rank-\(18\) Pfaffian reduction to that determinant obstruction and
  exhaustive no-go theorems for two natural rank-four link families.
- [`evidence/triangle_monodromy_cycle_girth_audit.md`](evidence/triangle_monodromy_cycle_girth_audit.md)
  and [`evidence/monodromy_character_factorisation_audit.md`](evidence/monodromy_character_factorisation_audit.md):
  exact long-odd-cycle constraints and a countermodel showing why the
  current one-fibre character factorisation cannot contradict them.
- [`evidence/triangle_closure_derived_reduction.md`](evidence/triangle_closure_derived_reduction.md):
  the exact reduction of the triangle-closure law to the derived
  \(S(m,m+1,3m+3)\), a complete proof at \(r=3,5\) from the count
  \(N_0=2\), and the demonstration that this mechanism is absent at every
  larger admissible parameter.  The later exact census refutes the law at
  \(r=15\), while leaving existence of the design open.
- [`evidence/s141531_triangle_third_moment_audit.md`](evidence/s141531_triangle_third_moment_audit.md)
  and [`evidence/triangle_census_r15.md`](evidence/triangle_census_r15.md):
  independent exact derivations of the \(927\,696\,866\,625\) triangle triples,
  the \(6.45\%\) closure ratio, and the certified dimension-two shortening
  interval.
- [`evidence/s141531_autocorrelation_law.md`](evidence/s141531_autocorrelation_law.md)
  and [`evidence/s141531_pair_difference_regularity.md`](evidence/s141531_pair_difference_regularity.md):
  independent proofs of the complete block-pair difference table, including a
  direct inverse-transform proof showing why it supplies no new obstruction.
- [`evidence/s141531_higher_xor_hierarchy.md`](evidence/s141531_higher_xor_hierarchy.md):
  the all-level block-XOR transform and the all-\(j\) positivity theorem.
- [`evidence/s141531_higher_xor_2adic_closure.md`](evidence/s141531_higher_xor_2adic_closure.md)
  and [`evidence/s141531_xor_divisibility_reduction.md`](evidence/s141531_xor_divisibility_reduction.md):
  the Δ/tail/finite-window closure of \(2^{31}\)-divisibility, two independent
  certified window computations, and the noncircular formal reduction from
  that condition to \(A_j\)-integrality and \(b\mid jA_j\).  These close the
  higher-XOR route, not Problem #835.
- [`evidence/s141531_prank_snf_audit.md`](evidence/s141531_prank_snf_audit.md):
  the scoped elementary p-rank, determinant, chain, point-Gram, and standard
  modular-intersection audit for \(S(14,15,31)\) and \(S(7,8,24)\).
- [`evidence/s7824_nonexistence_audit.md`](evidence/s7824_nonexistence_audit.md)
  and [`evidence/s7824_tower_config_sweep.md`](evidence/s7824_tower_config_sweep.md):
  exact necessary-condition audits for the derived \(S(7,8,24)\) tower.  Every
  tested distribution and localized configuration LP is feasible.
- [`evidence/s7824_literature_survey.md`](evidence/s7824_literature_survey.md):
  a source-graded survey of the smallest open high-strength Steiner tower,
  published exclusion mechanisms, current symmetry-restricted computations,
  and comparatively unexplored \(p\)-rank/SNF directions.  It also records the
  independent 2026 Erdős-forum post of the same \(k=16\) tower refinement.
- [`evidence/sqs8_klein_family_parity.md`](evidence/sqs8_klein_family_parity.md):
  the \(O_6^+(2)\) Klein-family proof that at most two \(S(3,4,8)\) are
  pairwise disjoint, and the explicit disjointness-parity sign at \(k=4\).
  The mechanism is specific to length-eight binary codes and gives no
  information about \(k=16\).
- [`evidence/large_set_literature_2026-07-26.md`](evidence/large_set_literature_2026-07-26.md):
  the parameter-free "one short of a large set" lemma, cited status of every
  tower level, and the record that no nontrivial \(LS(3,4,v)\) has been
  constructed at any order.
- [`evidence/execution_debt_2026-07-26.md`](evidence/execution_debt_2026-07-26.md):
  first actual runs of eleven validators left unrun by earlier
  permission-blocked sessions, one validator bug found and fixed, the
  \(e_4\)-level decision \(\omega(G_0)=\omega(G_1)=17\), and the finding that
  the proposed \(\varepsilon_{\mathrm{row}}\) "open lever" was already
  answered elsewhere in this repository.
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
python3 -B evidence/verify_five_point_full_reorder_exact.py
python3 -B evidence/verify_mersenne_spin_functional_audit.py
python3 evidence/verify_full_color_block_hodge_audit.py
python3 -B evidence/verify_transposition_flow_cocycle.py
python3 -B evidence/verify_simultaneous_flow_integrability.py
python3 evidence/verify_three_way_trade.py
python3 -B evidence/verify_block_local_sign_rowspace_no_go.py
python3 evidence/modular_kernel/verify_modular_kernel.py
python3 evidence/odd_graph_local_ball/construct_radius3.py \
  --seconds-per-column 60 --workers 8
python3 -B evidence/global_latin_audit.py
python3 -B evidence/odd_graph_local_ball/verify_radius5_large_set_boundary.py
python3 -B \
  evidence/odd_graph_local_ball/verify_radius5_golf_cyclic_exact_slice_seed.py \
  evidence/cyclic17_all_105_exact_slices_certificate.json
python3 -B \
  evidence/odd_graph_local_ball/verify_radius5_golf_cyclic_exact_slice_seed.py \
  evidence/cyclic17_all_105_exact_slices_cross_seed.json
python3 -B evidence/search_cyclic17_r3_extension.py \
  --verify evidence/cyclic17_r3_pair_0_1_certificate.json \
  --only-fixed-pair 0,1
python3 -B evidence/verify_cyclic17_r3_pair.py \
  evidence/cyclic17_r3_pair_0_1_certificate.json --fixed-pair 0,1
python3 -B evidence/odd_graph_local_ball/generate_radius4_generic_sinz_cnf.py \
  --cnf /tmp/o16-r4-generic.cnf \
  --map /tmp/o16-r4-generic.map.json \
  --manifest /tmp/o16-r4-generic.manifest.json
python3 -B evidence/odd_graph_local_ball/emit_global_latin_radius4_generic_model.py \
  --model /tmp/o16-r4.model \
  --colouring /tmp/o16-r4.colouring.json \
  --manifest /tmp/o16-r4.model-manifest.json
python3 -B evidence/odd_graph_local_ball/verify_radius4_generic_sinz_assignment.py \
  --model /tmp/o16-r4.model \
  --cnf /tmp/o16-r4-generic.cnf
python3 evidence/state_sdp_p17/verify_state_sdp_p17.py
python3 search_cyclic_ls_4_5_21.py --reflection --seconds 30
python3 search_cyclic_ls_4_5_21.py --seconds 300
python3 -B search_s_4_5_21_extension.py \
  --second-link-cycles 8 --seconds 300
python3 -B evidence/audit_s_4_5_21_cnf.py
python3 -B evidence/verify_ordered_design_symmetrization.py
python3 -B evidence/verify_quadratic_coloring_ansatz_no_go.py
python3 -B evidence/verify_kerdock_spread_additive_syndrome_no_go.py
python3 -B evidence/verify_cyclic17_barycenter_kerdock_spread_no_go.py
python3 -B evidence/verify_hamming_weight_bridge_no_go.py
python3 -B evidence/verify_full_slice_degree_necessity.py
python3 -B evidence/verify_f32_halfset_prefix_no_go.py
python3 -B evidence/f32_prefix8_affine_boundary_verifier.py
python3 -B evidence/f32_prefix8_trace_classification_verifier.py
python3 -B evidence/f32_two_statistic_k18_verifier.py
python3 -B evidence/f32_four_statistic_k32_verifier.py
python3 -B evidence/f32_five_statistic_moment_curve_clique_bound.py
python3 -B evidence/f32_five_statistic_k18_verifier.py
python3 -B evidence/verify_mate_cross_gram_audit.py
python3 -B evidence/verify_top_degree_pairing_derivative.py
python3 -B evidence/verify_top_degree_cross_matching_cubic.py
python3 -B evidence/verify_triple_polytabloid_tensor_support.py
python3 -B evidence/verify_triple_tensor_2adic_threshold.py
python3 -B evidence/verify_unprojected_fourth_moment_completion.py
python3 -B evidence/verify_norton_one_third_gap_no_go.py
python3 -B evidence/local_one_factorization_sign_verify.py
python3 -B evidence/verify_triangle_monodromy_cycle_girth.py
python3 -B evidence/verify_monodromy_character_factorisation.py
python3 -B evidence/verify_determinant_link_p19.py
python3 -B evidence/verify_p19_half_catalog_all_anchors.py
python3 -B evidence/verify_p19_half_schur_positive_control.py
python3 -B evidence/verify_p19_half_catalog_compatibility_crosscheck.py
python3 -B evidence/p19_rank18_pfaffian_factor_verify.py
python3 -B evidence/p19_circulant_rank4_link_verify.py
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  evidence/p19_twisted_cubic_link_verify.cpp \
  -o /tmp/p19_twisted_cubic_link_verify
/tmp/p19_twisted_cubic_link_verify
python3 -B evidence/s_4_5_21_cnf.py \
  --cycles 8 \
  --cnf /tmp/s4521-cycle-8.cnf \
  --map /tmp/s4521-cycle-8.map.json
python3 -B evidence/verify_triangle_closure_reduction.py
python3 -B evidence/verify_s141531_triangle_third_moment.py
python3 -B evidence/verify_triangle_census.py
python3 -B evidence/verify_s141531_autocorrelation_law.py
python3 -B evidence/verify_pair_difference_regularity.py
python3 -B evidence/verify_s141531_higher_xor_hierarchy.py
python3 -B evidence/verify_s141531_prank_snf_audit.py --fast
python3 -B evidence/verify_s7824_conditions.py
python3 -B evidence/verify_derived_closure_lp.py
python3 -B evidence/verify_ambient_moment_lp.py
python3 -B evidence/verify_s7824_tower_config_sweep.py
python3 -B evidence/verify_sqs8_klein_family_parity.py
python3 -B collaboration/opus5/verify_opus5_forced_structure.py
python3 -B collaboration/opus5_v2/verify_intersection_numbers.py
python3 -B collaboration/opus5_v2/verify_disjointness_parity.py
python3 -B collaboration/fable_e4/remote_run_e4.py
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
- The unrestricted DIMACS audit reports
  `CNF/CP-SAT structural equivalence: PASS` for all seven lossless cases.
  The current solver search has not supplied a checked SAT or UNSAT result.

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
