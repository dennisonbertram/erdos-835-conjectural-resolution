# Erdős–Rosenfeld Problem #835

A proof-oriented research record for Erdős–Rosenfeld Problem #835, with
rigorous reductions, exact structural theorems, and reproducible evidence.

## Status

The full problem remains open as of 28 July 2026. This repository does
**not** claim a complete proof. It advances and precisely formulates the
negative conjecture

\[
\chi(J(2k,k)) \geq k+2 \qquad (k>2),
\]

and proves several consequences and restricted obstructions. The first
unresolved case is \(k=16\).

New exact results in the note include:

- a solver-free \(r=0\) cut-feasible repair-selection theorem: after at
  most one support-preserving two-edge switch, some three of the seven
  remaining size-ten rows satisfy every internal-edge capacity cut.  A
  complete Tutte--Lovász audit now proves that those cuts and the full
  eleven-row ledger always supply the required simple \(b\)-factor.  The
  prescribed three-edge-colouring of that factor remains open in twelve
  of the sixteen selected-support Venn types, so this is not yet
  coordinated nine;
- a computer-assisted closure of the identical-support Venn type
  (orbit zero): after reducing a compatible pair to \(C_{10}\) or
  \(C_4\mathbin{\dot\cup}C_6\), both exact finite CNFs are UNSAT.  CaDiCaL
  generated the proof traces, its internal DRAT/LRAT checks passed, and an
  independent `drat-trim` replay also reports `VERIFIED`;
- a second computer-assisted closure for the common-nine-core Venn type
  (orbit one).  Every compatible pair has one of five exhaustive
  path-and-cycle types.  All five frozen CNFs are UNSAT, with CaDiCaL
  internal checking, independent Glucose 4 solves, and independent
  `drat-trim` verification of the committed proof traces;
- a certified closure of orbit two.  Its two identical supports reduce a
  compatible pair to three marked even-cycle types.  All three relaxed
  support-level formulas are UNSAT; the semantic verifier exhausts all
  514,080 compatible pairs and checks all 513,114 learned clauses, and
  every DRAT trace replays as `VERIFIED`;
- a certified closure of orbit three.  An explicit support-stabilizer
  catalogue reduces every compatible pair to sixteen marked
  path-and-cycle types.  All sixteen frozen formulas are UNSAT; an
  independent semantic verifier checks every one of the 2,352,609 learned
  clauses, and all sixteen DRAT traces replay as `VERIFIED`.  The other
  twelve Venn types remain open;
- an exact generic compatible-pair classifier for those twelve remaining
  Venn types.  A complete alternating path/cycle word invariant, checked
  independently against the full stabilizer action graph, reduces
  7,077,840 labelled matching pairs to 1,126 canonical cases.  This is a
  finite reduction, not yet cut sufficiency for those orbits;
- an exact boundary-flow formulation of the remaining colouring problem.
  For a fixed \(b\)-factor it is a nowhere-zero
  \(\mathbb F_2^2\) flow with prescribed boundary.  Explicit audited
  uncolourable \(b\)-factors exist in every Venn type, so a proof must
  choose a favourable factor using the ambient residual graph rather than
  claim that an arbitrary factor is colourable;
- coordinated-nine theorems for the class-B \(r=1,2\) profiles: in
  \(r=1\), a complement-cover prefix of type \(8^4\,10^2\) can be
  switched on the same supports and extended; in \(r=2\), every legal
  such prefix extends by three further support-respecting matchings.
  Together with the earlier \(r=3,4,5\) theorem, this leaves only the
  \(r=0\) coordinated-nine profile before the later first-lift and
  fan-realizability layers;
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
- exact exhaustive audits of two frozen higher-dimensional shortenings.
  The dimension-ten choice forces a projective doubly-even
  \([16\,359,20]\) image with \(1640\le d\le8024\), still \(303\) above
  its optimistic Griesmer boundary.  The dimension-twelve choice gives
  \([4291,18]\) with a joint Johnson-graph/Hoffman lower bound \(d\ge556\);
  an exact word of weight \(2188\) crosses Griesmer by \(96\), but it is an
  upper rather than lower bound.  These close two promising frozen
  subspaces without contradicting a hypothetical \(S(14,15,31)\);
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
  matrices remain open; and
- a uniform top-two-moment obstruction for every prime
  \(p\equiv7\pmod8\), \(p\ge23\), completing the earlier
  \(p\equiv1\pmod4\) and \(p\equiv3\pmod8\) arguments.  Consequently the
  single-maximal-minor colouring proposal is impossible for every
  \(k>2\).  This closes that one determinantal ansatz only; ratios or tuples
  of several Plücker coordinates and arbitrary colourings remain open; and
- a projective-geometric no-go theorem for the next genuinely
  two-coordinate family: for every odd prime \(p\ge5\), no arbitrary
  decoder of the ratio of two maximal-minor systems spanning a line inside
  the Grassmannian can colour \(J(2p-2,p-1)\).  In the \(p=17\) rank-two
  link, decoder rigidity would require sixteen internal points of a conic
  on one projective line, while the exact maximum is nine.  Two unrelated
  minors, affine pairs retaining scale, and three-or-more-coordinate tuples
  remain open;
- an exact delimiter for the unrelated two-minor frontier.  Two independent
  decomposable contracted forms either give the excluded rank-two
  Grassmann-line pencil or the canonical rank-four pencil
  \(e_1\wedge e_2,e_3\wedge e_4\).  An explicit \(p=17\) rank-four member has
  a perfect-matching zero graph, proving that the conic-parallelism argument
  cannot simply be extended.  The same exact control has only nine or ten
  raw labels per star and is not a decoder witness; and
- an unrestricted necessary theorem for every hypothetical \(k=16\) cover.
  Its triangle-monodromy Schreier graph is \(120\)-regular on
  \(17{,}678{,}835\) vertices and has the forced spectral decomposition
  \[
   \operatorname{Spec}(R)
   =\{120^1,(-97)^{30},77^{434}\}\mathbin{\uplus}\Lambda,
   \qquad \Lambda\subseteq[-83,82].
  \]
  The \(77\)-eigenvalue may occur again in \(\Lambda\), while \(-97\) has
  exactly multiplicity \(30\).  Exact two-step algebra gives
  \(R^2=120I+5A_{13}+Q\), with \(Q\) supported on intersection twelve,
  entries in \(\{0,1,2,3\}\), and row sum \(10080\).  Every mixed product
  of \(1,3,5,7,\) or \(9\) triangle monodromies is fixed-point-free, although
  the corresponding odd-girth-\(11\) condition is already automatic from
  the set-intersection geometry.  These are conditional constraints, not a
  contradiction; and
- a sharp continuation of that unrestricted theorem on the forced
  point- and pair-harmonic modules.  Every zero-extended pair-harmonic unit vector
  has exact global Odd spectral measure
  \[
    \frac1{17}\delta_{14}+\frac{29}{85}\delta_{-3}
    +\frac4{15}\delta_2+\frac13\delta_{-1},
  \]
  hence satisfies a quartic annihilator.  Every fibre relation preserves
  both modules and acts by an explicit integer scalar; on the pair module
  those scalars include \(449,1488,5148,3564\) for
  \(A_{13},A_2,A_{12},Q\), respectively.  The complete single-fibre
  Frobenius moment test still passes.  A new local double count identifies
  its first free statistic and sharpens
  \(10080n\leq\operatorname{tr}Q^2\leq13440n\), equivalently
  \(2100n\leq\#C_4(R)\leq2520n\).  The proof and its factor-of-two audit are
  checked against the actual \(k=6\) Witt fibre.  This is stronger necessary
  structure, not a contradiction; and
- a degree-three continuation of the same unrestricted theorem.  Design
  quadrature forces every zero-extended \(H_3\) vector onto exactly the five
  global eigenspaces \(E_3,E_{12},E_{13},E_{14},E_{15}\).  All endpoint
  freedom is one operator \(0\preceq Z\preceq3I/5\), and every fibre
  intersection relation has the full right action
  \(A_sP_3=(\alpha_sI+\beta_sR)P_3\).  Exact trace and leakage constraints give
  \[
    \frac{206336}{1125}\le\operatorname{tr}Z^2\le\frac{9548}{45},
    \qquad \operatorname{rank}Z\ge3484.
  \]
  A compatible integral compressed-\(R\) spectrum at the upper endpoint
  proves that support, rank, scalar moment, and elementary integrality tests
  still do not contradict a hypothetical cover.  Pointwise refinement
  identifies the two first leakages as the integer commutators
  \([R,P_3]=\Delta/305900\) and
  \([Q,P_3]=(R\Delta+\Delta R-5\Delta)/305900\); explicit integral moment
  witnesses realize every local \(Q\)-state.  The missing datum is therefore
  the two-root/global coupling of those one-factorization asymmetries; and
- a degree-four continuation.  Design quadrature confines \(H_4\) to six
  global eigenspaces and reduces every fibre relation to a right action in
  \(\operatorname{span}(I,R,A_{13})P_4\).  The exact two-operator endpoint
  cone, its first leakage inequality, all endpoint rank budgets, and the
  regular-simplex coupling of all seventeen fibres admit explicit finite
  operator witnesses.  These witnesses deliberately omit the fixed
  entrywise Johnson kernels and are not covers; they close this relaxation,
  not the problem; and
- all-parameter degree-one and degree-two rigidity theorems.  For every even
  \(k\) admitting a hypothetical cover, design cross-quadrature confines
  \(H_1\) to \(E_1,E_{k-2},E_{k-1}\) and \(H_2\) to
  \(E_2,E_{k-3},E_{k-2},E_{k-1}\), with explicit weights and full scalar
  actions for every fibre intersection relation.  The resulting divisibility
  conditions automatically pass whenever \(k+1\) is prime; the ordinary
  design indices separately recover the Ma--Tang exclusion of every composite
  \(k+1\).  Thus this uniform spectral route sharpens the necessary structure
  but gives no new obstruction at a surviving prime; and
- a corrected staircase theorem for \(k=16\).  Exact design quadrature
  confines \(H_a\) to
  \(E_a\oplus E_{15-a}\oplus\cdots\oplus E_{15}\) for every
  \(0\le a\le7\).  Together with \(N_aP_a=P_a/17\), this gives a certified
  relation family and the honest upper bound
  \(\dim{\cal J}P_a\le\max(1,a-1)\), not the false exact-rank claim in an
  initial draft.  Exact ranks are proved only for \(a\le3\); in particular
  \(A_{13}P_3=(R+372I)P_3\), so the previously proposed free level-three Gram
  entries are actually forced.  The corrected \(234\)-equation
  triple-profile system is rationally consistent, while its joint
  nonnegative-integral feasibility remains open; and
- an automatic-intersection theorem.  The full fixed-block moments of every
  \(S(k-2,k-1,2k-1)\) force
  \[
  n_s=\frac{\binom{k-1}{s}}{k+1}
  \left(\binom{k}{s+1}+(-1)^{k-1-s}k\right).
  \]
  Hence even \(k\) forces \(n_0=0\); specifically, every
  \(S(14,15,31)\) is already intersecting and has \(n_1=120\).
  Therefore the \(k=16\) problem is exactly the existence of
  \(LS(14,15,31)\), with no additional disjointness condition.  Cross-fibre
  disjointness gives the perfect matchings of the graph cover
  \(O_{16}\to K_{17}\), but their elementary parity and monodromy constraints
  remain consistent; and
- an exact audit of the next intersection/cover shortcut.  Hoffman equality
  makes every exact-intersection relation equitable, and the
  intersection-one endpoints in the Odd graph are exactly two-to-one images
  of ordered intermediate-colour pairs along length-three geodesics.  The
  two paths to an endpoint need not reverse their intermediate colours, so
  the proposed commutativity, matching-sign, and parity conclusions do not
  follow.  Fano and Witt controls show that one-class intersection data
  cannot supply the missing simultaneous cross-colour obstruction; and
- a second unrestricted necessary theorem obtained by deleting one colour
  class \(D\).  Any tight prime colouring forces a
  \((p-2)\)-dimensional subspace \(U\le\ker M_D\) on which every Hadamard
  product has constant star sums, with a nondegenerate scalar pairing.
  Complete finite-field enumeration passes the true \(k=2\) control and
  rejects the false \(k=4\) control already at degree two: its deleted
  \(56\times56\) kernel has only eight isotropic projective lines and no
  compatible pair, so its maximum capacity is \(1<3\).  The required
  capacity at \(k=16\) is \(15\); no uniform bound there is yet proved.
  Independent Opus 5 and Fable audits verify the frame reformulation and
  show that derivation preserves the full \(15\)-dimensional structure while
  linear inclusion-matrix rank gives no useful capacity bound.  An exact
  \(k=6\) computation gives deleted-kernel dimension \(77\), refuting the
  tempting \(|D|/2\) guess without closing the full quadratic cone.  A frozen
  \(5\!-\!(12,6,3)\) witness produces a non-mate isotropic \(k=6\) line,
  proving that the 144 Steiner-mate lines do not exhaust that cone.  Gluing
  the local simplexes forces a global equal-norm tight frame whose nonedge
  first and square moments are exact; these moments rule out constant
  nonedge squared inner products, but standard Schur-product, modular-rank,
  and finite-field Gerzon theorems do not yet bound the capacity.  Abstract
  linear-hypergraph countermodels realize all displayed moment-only
  identities in this attack at the target parameters, so any further
  obstruction must use additional structure such as the actual Johnson
  subset geometry.

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
- an unrestricted small-ball census at \(k=2,4,6\): \(k=2\) passes,
  \(k=4\) already fails at radius three, and all 1,680 labelled \(k=6\)
  radius-three families fail at radius four for every root-colour choice.
  All 45,360 infeasible \(k=6\) subproblems have the same forced-edge
  collision mechanism. The self-contained exhaustive verifier also proves
  why that mechanism does not transfer to \(k=16\). A separate portable
  certificate package independently checks DRAT exclusions for \(k=4\) at
  radii four and five and for \(k=6\) at radius five, together with a
  6,850,440-clause SAT/semantic positive control at \(k=16\); and
- a lossless radius-five trace theorem: in every unrestricted local
  \(O_k\to K_{k+1}\) extension for even \(k\), parity forces the
  \(N\)-traces to be perfect or near-perfect matchings. At \(k=16\), the
  lower bounds \(8+16\cdot7=120\) exhaust \(E(K_{16})\), so every one of the
  105 fixed-pair slices is necessarily a prescribed-link
  \(LS(2,3,19)\). This removes a previously stated “minimal-trace ansatz”
  without constructing the shared trace or solving #835; and
- the radius-four dual fibering theorem: for every fixed \(uv\), each
  colour class of \(N_{uv}\) is already forced to be a perfect matching on
  its allowed index set. At \(k=16\) the three special colours match 14
  indices and the other fourteen colours match 12 indices, giving
  \(3\cdot7+14\cdot6=105\). The three generic holes are always distinct,
  so the corresponding first-order parity test is automatically satisfied
  and supplies no \(k=16\) obstruction. At radius five, fixing a flag
  \((i,u)\) gives a third forced fibering: every colour class in the
  \((j,v)\) rectangle is a partial permutation with its omitted rows and
  columns prescribed exactly. Adding two canonical dummy rows and one dummy
  column completes every such flag to a Latin square \(Q^{i,u}\) of order
  \(k\). A cofactor calculation now evaluates its global Alon--Tarsi product
  exactly as
  \[
    \prod_{i,u}\operatorname{AT}(Q^{i,u})
    =(-1)^{k(k-1)/2}\operatorname{AT}(T)\prod_i\delta(S_i),
  \]
  entirely from the radius-three \(L,M\) data.  The residual generic
  hole-orientation product is in fact identically \(+1\) for every
  admissible even-\(k\) chart, so any genuine extension must have partial
  fiber-sign product equal to the displayed right-hand side.  Exact
  one-sided controls show that separate prescribed \(ij\)-trace slices do
  not determine the fiber signs.  A subsequent full two-sided calculation
  canonically augments each colour layer to a no-hole matching tensor and
  proves
  \[
    H_\infty=P(\Psi^\infty),\qquad
    H_x=(-1)^{x+1+(k-2)/2}\operatorname{sgn}(\lambda_x)P(\Psi^x).
  \]
  The infinity value genuinely depends on its one-factorization: exact
  \(k=16\) tensors realize both signs.  Nevertheless, the product of all
  \(k+1\) layer equations simplifies identically to the displayed
  radius-three flag formula for every admissible chart.  The seventeen
  individual equations have explicit quadratic XOR forms, but the existing
  exact-one and forced-trace constraints already imply every one of them.
  Across the \(k+1\) roots of one golf design,
  \(P(\Psi^{r,x})\) is root-independent and all scalar transitions form a
  coboundary, so every root-cycle product is \(+1\).  Thus the total,
  individual-XOR, and formal scalar cross-root sign routes are closed as new
  obstructions.  Finer relations from the overlap of actual cross-root
  \(N\)-tables remain open, and no \(k=16\) contradiction follows; and
- a certificate-ready CNF for the complete unrestricted radius-four ball plus
  all 1,680 forced traces: 883,521 variables and 1,909,497 clauses, with
  canonical SHA-256
  `2eb2e0efba279655021e4c709b03148e3cea73d98e32c745637864ba177327d4`.
  Its independent verifier reconstructs the entire parent and augmented byte
  streams, checks every semantic trace incidence, and exhaustively validates
  the Sinz projection on all \(2^{15}\) primary assignments.  A proof-logging
  run was stopped without a verdict for disk safety; a separate non-proof
  Kissat reconnaissance run is still live.  No SAT or UNSAT result is
  claimed; and
- a complete unrestricted CNF for the necessary shadow \(LS(3,4,20)\):
  159,885 variables and 251,957 clauses, independently reconstructed
  byte-for-byte with canonical SHA-256
  `f855ff1dcd09c420d8d086a9bd759c7906b7685b0e40eb0149eb42768424625f`.
  The root-star normalization gives a lossless 55-way second-star split,
  indexed by all fixed-point-free cycle types on 16 points. A subsequent
  four-bijection parity lemma proves that every model can be relabelled into
  exactly one of the 28 even-permutation types, so only those 28 branches are
  needed for an exhaustive sweep. Independent verifiers check both the full
  derangement census and the 55-to-28 reduction. SAT and proof-logging
  runs attempted so far have ended `UNKNOWN` or without a durable verdict;
  no SAT or UNSAT result is claimed. Checked UNSAT certificates for all 28
  even branches would exclude \(k=16\), while SAT would construct a derived
  large set but would not solve #835; and
- a parameter-free "one short of a large set" lemma: \(P-1\) pairwise disjoint
  \(S(k-1,k,v)\) force a \(P\)-th, so the maximum number of pairwise disjoint
  systems is never exactly \(P-1\).  In particular no search for \(16\)
  pairwise disjoint \(SQS(20)\), or for \(16\) pairwise disjoint
  \(S(15,16,32)\), can succeed; and
- three newly certified route delimiters.  The corrected \(234\)-equation
  degree-three profile system has exact nonnegative rational and integer
  witnesses for every intersection parameter, closing the local
  profile/Farkas route.  For every odd prime \(p\), the \(p\)-primary critical
  group of \(O_{p-1}\) is
  \((\mathbb Z/p)^{\,2\binom{2p-3}{p-2}/p-1}\), whose enormous \(p\)-rank
  supplies no cover obstruction.  Finally, the commutator asymmetry
  \(\Delta\) vanishes on fibre intersection layers \(12\) and \(13\), but
  its exact rank bound and compatible integral endpoint spectrum still give
  no \(k=16\) contradiction; and
- two exact construction-frontier results.  Any arbitrary decoder of the
  two-layer additive syndrome
  \(\sum_{z\in S}z\in\mathbb F_{17}^2\) on
  \(\mathbb F_{17}^{*}\times\{0,1\}\) needs at least \(34\) colours, witnessed
  by an explicit quotient \(K_{34}\).  In the authenticated
  Etzion--Hartman \(15\)-system \(SQS(20)\) core, the full point/system
  automorphism group is trivial.  A general leave-graph theorem proves that
  a partial large set completes exactly when its \(j\)-fold leave is
  \(j\)-colourable, and the four intrinsic \(K_5\)s show that any completion
  retaining this core must replace at least three systems.  An exhaustive
  ten-point colouring certificate excludes exactly the \(30\)
  same-five-pack retain-twelve repairs, while independently reconstructed and
  replayed point-link DRAT certificates exclude all other \(425\) cases.
  Therefore every \(LS(3,4,20)\), if one exists, shares at most eleven of
  these fifteen EH systems: the repair distance of this fixed core is at least
  four.  The \(425\) point-link-certified leaves have \(STS(19)\) packing
  number exactly three.  In contrast, an independent exact screen shows that all
  \(86{,}450\) pair-links of all \(455\) cases are \(1\)-factorizable,
  proving that point links are a strictly stronger local invariant here; and
- a fixed-link construction frontier for \(LS(3,4,20)\).  The unrestricted
  completion CNF for an independently reconstructed cyclic
  \(LS(2,3,19)\) point link has \(159{,}885\) variables and \(252{,}909\)
  clauses.  Its \(C_{17}\)-equivariant restriction has an independently
  reconstructed \(2{,}964\times1{,}140\) exact-cover formulation.  The
  type-(i) layer has exactly \(1{,}326\) feasible branches; a complete
  bounded sweep found no witness but timed out on every branch, so no
  SAT/UNSAT verdict is claimed; and
- an exact delimiter for the holonomy-census route.  The full
  \(\mathbb Z[S_m]\) tower identity, every representation projection, and
  its fixed-colour and orientation projections are proved to hold for
  arbitrary chart families, so they carry no design-existence information.
  At the genuinely design-dependent one-factorization layer,
  \[
    \sum_{\{a,b\}}m_2(\sigma_{ab})=2C_4(F),
  \]
  and exact finite spanning witnesses prove that, for \(K_{18}\), this parity
  law and the total count span every universal affine
  \(\mathbb F_2\) census equation.  An independent implementation reaches the
  maximal affine rank \(53\) on \(3{,}000\) verified \(K_{18}\)
  one-factorizations.  These results close this linear holonomy route only;
  they neither construct nor exclude \(LS(3,4,20)\); and
- a complete small-parameter theorem for the simultaneous-fan formulation.
  Exact enumeration gives all \(840\) labelled \(STS(9)\)'s and all
  \(15{,}360\) large sets on a fixed labelled nine-point set, exhausted by
  two point-isomorphism orbits of sizes \(8{,}640\) and \(6{,}720\).
  Each representative's fan conflict graph contains an explicit
  non-\(3\)-colourable subgraph on only eighteen cells and eleven constraint
  triangles, with a short human proof.  Hence no \(LS(2,3,9)\) admits a
  simultaneous \(3\)-fan and \(\chi(J(12,6))\ge8\).  This recovers a known
  small case by this local route; it does not extend to \(k=16\); and
- exact kernel and symmetry delimiters for the cyclic \(k=16\) fan graph.
  There is a universal \(969\)-dimensional row-dependency space.  For the
  committed cyclic link,
  \[
    \operatorname{rank}_{\mathbb F_2}B=15{,}963,\qquad
    \dim\ker_{\mathbb F_2}B=34{,}425,
  \]
  while \(Bx=\mathbf1\) is consistent over every prime field.  An exhaustive
  orbit search first proved \(\omega(H_L)=13\) for the cyclic link, and a
  subsequent local argument proves the same equality for every fixed link.
  The quotient equation moreover has a signed integral solution, which lifts
  to the full fixed-link incidence system, so no signed linear obstruction
  exists for this link.  The exact nonlinear target is the
  Schur-power condition
  \(f,\ldots,f^{11}\in\ker_{\mathbb F_{13}}B\),
  \(Bf^{12}=-\mathbf1\).  The \(C_{17}\)-invariant restriction has
  \(2{,}964\) cells and \(1{,}140\) rainbow groups. Three equivalent
  deterministic CNFs, including a 38,532-variable direct encoding, have
  independent byte-level audits. Their searches have not yet returned a
  model or certificate, so neither a fan nor an obstruction is claimed.

These are restricted-core, shadow, and ansatz results, not a construction or
proof of #835.

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
- [`evidence/s141531_high_dimension_boundaries.md`](evidence/s141531_high_dimension_boundaries.md):
  exhaustive common-zero shortening audits for fixed dimensions ten and
  twelve, including exact quotient enumerators, divisible-code structure,
  joint middle-layer occupancy bounds, and both Griesmer margins.  The
  companion stdlib verifier checks every coset and records a canonical
  digest.
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
- [`collaboration/opus5/radius5_followup/`](collaboration/opus5/radius5_followup/):
  Opus 5's self-contained unrestricted radius-three census, exhaustive
  \(k=6\) radius-four obstruction, and independent audit of the forced-trace
  theorem, with both quick and full finite verifiers. It also contains an
  independent structural audit of the \(LS(3,4,20)\) and \(S(4,5,21)\)
  shadows and an independent line-by-line audit of the global flag-sign
  formula.
- [`evidence/odd_graph_local_ball/radius4_dual_trace_forced.md`](evidence/odd_graph_local_ball/radius4_dual_trace_forced.md):
  the ansatz-free per-\(uv\) matching decomposition forced at radius four,
  the flag partial-permutation fibering and canonical order-\(k\) Latin-square
  augmentation at radius five, the exact global Alon--Tarsi product, plus the
  proof that the naive allowed-set parity is vacuous for every even \(k\).
- [`evidence/odd_graph_local_ball/flag_at_exact_formula.md`](evidence/odd_graph_local_ball/flag_at_exact_formula.md):
  a separate cofactor proof of the global flag-sign formula, the exact
  residual left by completing the partial symbol fibers, and a stdlib verifier
  covering 450,176 finite sign cases plus the genuine \(k=2\) control.
- [`evidence/odd_graph_local_ball/partial_fiber_sign_head.md`](evidence/odd_graph_local_ball/partial_fiber_sign_head.md):
  the proof that the residual orientation factor is universally \(+1\),
  the resulting exact required value of the full partial-fiber sign product,
  and finite one-sided controls proving that separate prescribed
  \(ij\)-trace slices cannot determine individual fiber signs.
- [`collaboration/global_h_parity/README.md`](collaboration/global_h_parity/README.md):
  the complete two-sided layer theorem, including the exact infinity and
  finite-colour formulas, the Pfaffian proof that their total is identically
  the previous flag formula, and exact \(k=6\) and \(k=16\) controls.
  [`collaboration/finite_total_identity/README.md`](collaboration/finite_total_identity/README.md)
  is an independent derivation and verifier; the supporting
  [`finite augmentation`](collaboration/full_layer_augmentation/README.md)
  and [`infinity-layer theorem`](collaboration/infinity_layer_theorem/README.md)
  retain the layer-by-layer constructions.
- [`collaboration/opus5/full_n_sign/`](collaboration/opus5/full_n_sign/)
  and [`collaboration/fable_sign_head/`](collaboration/fable_sign_head/):
  the requested external-model audit and falsification records, retained
  with explicit notices where the later two-sided theorem supersedes their
  interim open-status statements.
- [`evidence/odd_graph_local_ball/small_k_balls/`](evidence/odd_graph_local_ball/small_k_balls/):
  deterministic small-\(k\) CNFs, independently checked DRAT certificates,
  semantic witnesses, hashes, and the repaired \(k=16\) positive-control
  archive.
- [`evidence/odd_graph_local_ball/radius4_forced_trace_cnf.md`](evidence/odd_graph_local_ball/radius4_forced_trace_cnf.md):
  the deterministic materializer, pinned manifest, and independent verifier
  for the complete unrestricted radius-four-plus-forced-trace CNF. The
  exact authenticated 37 MB instance and trace map are checked into Git.
- [`evidence/odd_graph_local_ball/radius5_large_set_equivalence.md`](evidence/odd_graph_local_ball/radius5_large_set_equivalence.md):
  an exact equivalence between a radius-five slice and a prescribed-link
  \(LS(2,3,19)\), plus an eight-`AllDifferent` cyclic quotient.
  [`radius5_minimal_trace_forced.md`](evidence/odd_graph_local_ball/radius5_minimal_trace_forced.md)
  proves that the required trace matching is forced, not an ansatz. All
  \(105\) Wallis slices have independent exact cyclic completions, while
  their shared-\(N\) compatibility remains the decisive condition.
- [`evidence/ls_3_4_20_generic_cnf/`](evidence/ls_3_4_20_generic_cnf/):
  a deterministic complete CNF for the unrestricted \(LS(3,4,20)\)
  necessary shadow, together with a canonical variable map, manifest, and an
  independent stream verifier.
- [`evidence/ls_3_4_20_second_star_branching.md`](evidence/ls_3_4_20_second_star_branching.md)
  and [`evidence/ls_3_4_20_second_star_branches/`](evidence/ls_3_4_20_second_star_branches/):
  the proof, deterministic generator, compact cubes, manifests, materializer,
  and independent verifier for the lossless 55-way second-star
  decomposition. The later
  [`28-branch reduction`](collaboration/ls3420_structural_attack/LS3420_EVEN_FLAG_REDUCTION.md)
  and its independent verifier prove that only the 28 even cycle types need
  be searched; they also relabel the Etzion--Hartman partial exactly from
  branch 54 to branch 0. The
  [`branch-0 search handoff`](collaboration/ls3420_branch0_search/README.md)
  authenticates the resulting 4,773-assignment hint, its inverse relabelling,
  and the exact propagation-enhanced branch-0 CNF. No branch verdict is
  claimed.
- [`evidence/cyclic17_all_105_exact_slices_status.md`](evidence/cyclic17_all_105_exact_slices_status.md):
  the exact certificates, independent verifier, and carefully limited scope
  for those \(105\) separately feasible prescribed-link slices.
- [`evidence/cyclic17_equivariant_reduction.md`](evidence/cyclic17_equivariant_reduction.md):
  the exact layer recursion under a colour-transitive order-\(17\)
  symmetry, with a direct-verified 40-phase certificate for one
  prescribed-link \(LS(2,3,19)\) slice.  The joint layer, later layers,
  and asymmetric colourings remain open.
- [`evidence/cyclic17_star_centre0_infeasibility.md`](evidence/cyclic17_star_centre0_infeasibility.md)
  and [`evidence/cyclic17_star_centre0/`](evidence/cyclic17_star_centre0/):
  a fixed-Wallis centre-star obstruction whose minimal incompatible core has
  six rows. Three independently encoded UNSAT certificates replay with
  `drat-trim`; the stored slice-family completeness is independently
  reproduced by two exhaustive traversals. This excludes one cyclic chart
  only, not all cyclic charts and not #835.
- [`evidence/cyclic17_star_scope_rev2_and_pointwise_exhaustion.md`](evidence/cyclic17_star_scope_rev2_and_pointwise_exhaustion.md):
  the repaired theorem that every colour-transitive tight solution is
  cyclic-\(17\), a chart-independent proof that every individual star orbit
  satisfies Hall, and an unrestricted proof that the entire purely
  pointwise indicator algebra is parameter-forced. These identify the scope
  and close proof strategies; they do not decide existence.
- [`evidence/cyclic17_all_power_sums_audit.md`](evidence/cyclic17_all_power_sums_audit.md):
  the exact endpoint of the cyclic layer's finite-field linearized moment
  route.  All dependency-cancelled power sums through degree \(16\) are
  consistent (3,240 rows, rank 3,000), so the nonlinear phase constraints
  remain the genuine obstruction.
- [`evidence/cyclic_layer_recursion_prime_census.md`](evidence/cyclic_layer_recursion_prime_census.md):
  a solver-free census of the small prime cyclic layers, a new
  negation-symmetric \(G(17)\) certificate, and an exact
  \(\mathbb Z_2\)-equivariant reduction of its joint radius-five boundary.
  The reduced search is still `UNKNOWN`; these are cyclic-ansatz results,
  not a solution of Problem #835.
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
  a fresh, explicitly limited seven-day X claim search, including resolution
  of two third-party “erdős 835” links to a small-cases/primality-sieve note.
  It found no full-solution claim; this is not evidence of priority or absence.
- [`collaboration/recent_solution_check_2026-07-28.md`](collaboration/recent_solution_check_2026-07-28.md):
  the latest official-page, public-index, and seven-day X refresh.  No checked
  source claimed a full solution; the result cannot exclude unpublished or
  unindexed work.
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
- [`collaboration/global_construction_attack/maximal_minor_p7mod8_closure.md`](collaboration/global_construction_attack/maximal_minor_p7mod8_closure.md):
  the top-two-moment and quadratic-character proof for all primes
  \(p\equiv7\pmod8\), \(p\ge23\), completing the single-maximal-minor
  no-go across every possible prime parameter.
- [`collaboration/multi_plucker_construction/grassmann_line_ratio_no_go.md`](collaboration/multi_plucker_construction/grassmann_line_ratio_no_go.md):
  the oval-and-internal-point proof excluding every arbitrary projective
  decoder of two maximal-minor coordinates spanning a Grassmann line, with
  an exact \(p=3\) boundary control and a \(p=17\) census.
- [`collaboration/opus5/rank4_plucker_ratio/NOTE.md`](collaboration/opus5/rank4_plucker_ratio/NOTE.md):
  Claude Opus 5's exact classification of the next local rank-four pencil
  as one congruence orbit, its Segre-quadric formulation, and a checked
  \(p=3\) local positive link.  Seeded searches find no \(p=5,7,11\)
  link, but are explicitly non-exhaustive and prove nothing at \(p=17\).
- [`collaboration/rank4_plucker_ratio/rank4_plucker_ratio.md`](collaboration/rank4_plucker_ratio/rank4_plucker_ratio.md):
  an independent exact \(p=17\) rank-four control whose one pencil member
  has a perfect-matching zero graph, sharply disproving the naive extension
  of the rank-two oval argument while failing the full decoder condition.
- [`collaboration/layer_sign_xor_cuts/README.md`](collaboration/layer_sign_xor_cuts/README.md)
  and [`collaboration/cross_root_layer_sign/README.md`](collaboration/cross_root_layer_sign/README.md):
  exact proofs that the individual layer XOR equations are already entailed
  by the reduced \(N\)-constraints and that their formal root transitions
  have trivial scalar holonomy.  Neither result constructs a compatible
  \(N\)-table.
- [`collaboration/triangle_monodromy_spectrum/README.md`](collaboration/triangle_monodromy_spectrum/README.md):
  the mixed-word theorem and initial exact Schreier-spectrum interval for
  every hypothetical cover.
- [`collaboration/schreier_spectrum_obstruction/README.md`](collaboration/schreier_spectrum_obstruction/README.md):
  the strengthened point/pair harmonic decomposition, exact multiplicity of
  \(-97\), residual interval \([-83,82]\), two-step intersection algebra,
  and fourth-moment constraints, including a complete \(k=6\) Witt control.
- [`collaboration/schreier_krein_followup/README.md`](collaboration/schreier_krein_followup/README.md):
  the exact four-point global support theorem for the pair-harmonic module,
  its quartic annihilator and full fibre-relation invariance, and a complete
  audit of the still-feasible Schur/Krein and harmonic trace budgets.
- [`collaboration/schreier_h3_support/README.md`](collaboration/schreier_h3_support/README.md):
  the exact five-eigenspace support theorem on \(H_3\), the one-operator
  endpoint parametrisation, the affine right action of every fibre relation,
  sharp leakage/rank bounds, and an integral moment-level compatibility
  witness.
- [`collaboration/h3_state_refinement/README.md`](collaboration/h3_state_refinement/README.md):
  the pointwise \(H_3\) commutator formulas, the four masked \(Q\)-states,
  exact integral pair-moment witnesses, and the two-root finite frontier.
- [`collaboration/schreier_h3_triple_profiles/README.md`](collaboration/schreier_h3_triple_profiles/README.md):
  all exact block-through-triple profiles, their global double counts, a
  strictly positive rational witness for every known linear one-root margin,
  and reproducible but nondecisive cyclic zero-one probes.
- [`collaboration/corrected_triple_profile_lp/README.md`](collaboration/corrected_triple_profile_lp/README.md):
  the corrected exact-rank census and explicit nonnegative rational and
  integer witnesses for every intersection parameter in the local
  \(234\)-equation triple-profile system.
- [`collaboration/h3_delta_rank_attack/README.md`](collaboration/h3_delta_rank_attack/README.md):
  the vanishing of the degree-three commutator asymmetry on intersection
  layers \(12\) and \(13\), its exact even-rank ceiling, and a carefully
  scoped no-go for the generic skew-rank/Pfaffian route.
- [`collaboration/schreier_h4_support/README.md`](collaboration/schreier_h4_support/README.md):
  the six-eigenspace \(H_4\) support theorem, exact endpoint cone and
  three-map right module, together with explicit 17-colour operator
  relaxation witnesses.
- [`collaboration/opus5/joint_schreier_krein_attack/NOTE.md`](collaboration/opus5/joint_schreier_krein_attack/NOTE.md):
  Opus 5's independently audited point/pair rigidity proof, the precisely
  scoped single-fibre quadratic moment no-go result, and the corrected
  \(\varepsilon\) double count sharpening the fourth-moment interval.
- [`collaboration/general_h1_rigidity/README.md`](collaboration/general_h1_rigidity/README.md)
  and [`collaboration/general_h2_rigidity/README.md`](collaboration/general_h2_rigidity/README.md):
  the all-even-\(k\) point- and pair-harmonic support theorems, exact spectral
  weights, closed scalar actions for every fibre relation, and proofs that
  those scalar divisibilities add no obstruction when \(k+1\) is prime.
- [`collaboration/opus5/staircase_support_frontier/NOTE.md`](collaboration/opus5/staircase_support_frontier/NOTE.md):
  Opus 5's corrected \(H_0,\dots,H_7\) staircase-support computation, the
  certified compression-rank upper bounds, the forced level-three Gram
  entries, and the exactly scoped rational triple-profile audit.  The note
  explicitly retracts an initial false exact-rank claim.
- [`collaboration/steiner_disjoint_matching/README.md`](collaboration/steiner_disjoint_matching/README.md):
  the general fixed-block intersection formula proving automatic
  intersectingness, the exact equivalence of the \(k=16\) case with
  \(LS(14,15,31)\), and the still-consistent cross-fibre matching and
  monodromy counts.
- [`evidence/general_rigidity_staircase_audit_2026-07-26.md`](evidence/general_rigidity_staircase_audit_2026-07-26.md):
  the independent verification checkpoint and explicit record of the
  exact-rank, level-three Gram, disjointness, and triple-profile corrections
  made before this research batch was committed.
- [`collaboration/hadamard_kernel_attack/README.md`](collaboration/hadamard_kernel_attack/README.md):
  the deleted-colour Hadamard-kernel theorem, complete \(k=2,4\) quadratic
  controls, and the explicitly limited \(k=6\) design-valued sector audit.
- [`collaboration/opus5/hadamard_kernel_followup/NOTE.md`](collaboration/opus5/hadamard_kernel_followup/NOTE.md)
  and [`collaboration/fable_hadamard_kernel/2026-07-26_fable_note.md`](collaboration/fable_hadamard_kernel/2026-07-26_fable_note.md):
  independent audits of the kernel theorem, its finite-field frame
  reformulation, the exact \(k=6\) nullity \(77\), and the proof that
  derivation preserves the required dimension while linear rank alone
  supplies no capacity obstruction.
- [`collaboration/schur_product_literature/README.md`](collaboration/schur_product_literature/README.md):
  a primary-source hypothesis audit and the exact global tight-frame theorem,
  including forced nonedge moments and explicit two-star gluing controls.
- [`collaboration/opus5/post_spectrum_kernel_synthesis/NOTE.md`](collaboration/opus5/post_spectrum_kernel_synthesis/NOTE.md):
  an Opus 5 audit showing that several coarse residual spectral-moment bounds
  overlap, without claiming spectral consistency, plus an exact standalone
  \(LS(2,3,9)\) control for the derived degree-two capacity condition.
- [`collaboration/fable_hadamard_global_gluing/2026-07-26_fable_note.md`](collaboration/fable_hadamard_global_gluing/2026-07-26_fable_note.md):
  the finite orthogonal-group coset-CSP reformulation of global frame gluing.
  Its attempted \(k=6\) decision hit the connected Fable account's spend
  limit and produced no mathematical verdict.
- [`collaboration/global_frame_moment_attack/`](collaboration/global_frame_moment_attack/):
  abstract linear-hypergraph countermodels to every displayed moment-only
  frame obstruction in scope, and a frozen exact \(k=6\) non-mate
  isotropic-line witness with an independent standard-library verifier.
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
- [`collaboration/critical_group_cover_obstruction/README.md`](collaboration/critical_group_cover_obstruction/README.md):
  the exact \(p\)-primary critical group of \(O_{p-1}\), with an independent
  modular Smith-rank verifier and the explicit reason this invariant does
  not obstruct a locally bijective cover.
- [`collaboration/f17_additive_syndrome_k34/README.md`](collaboration/f17_additive_syndrome_k34/README.md):
  an explicit \(K_{34}\) in the exact quotient of the two-layer additive
  \(\mathbb F_{17}^2\) syndrome, excluding every arbitrary decoder of that
  statistic into seventeen colours.
- [`collaboration/eh_residual_odd_cycle/README.md`](collaboration/eh_residual_odd_cycle/README.md),
  [`collaboration/eh_core_symmetry_orbits/README.md`](collaboration/eh_core_symmetry_orbits/README.md),
  and [`collaboration/eh_j5_repair_search/README.md`](collaboration/eh_j5_repair_search/README.md):
  authenticated exact structure of the Etzion--Hartman \(15\)-core, its
  trivial automorphism group, the ten-point obstruction excluding \(30\) of
  \(455\) retain-twelve repairs, bounded CP-SAT reconnaissance, and two
  independent exact confirmations that every one of the \(86{,}450\)
  pair-links is \(1\)-factorizable.
- [`collaboration/opus5/large_set_completion_colouring/NOTE.md`](collaboration/opus5/large_set_completion_colouring/NOTE.md):
  the general leave-graph colouring equivalence, the corrected
  completability-only rainbow criterion, the Etzion--Hartman repair-distance
  theorem, and exhaustive negative screens of the local triple, pair-link,
  and labelled cross-pair conditions.
- [`collaboration/eh_point_link_screen/README.md`](collaboration/eh_point_link_screen/README.md):
  the aggregate theorem excluding all \(455\) retain-twelve subfamilies of the
  EH core, including deterministic semantic CNF reconstruction and
  independently replayed compressed DRAT proofs for \(425\) point links.
- [`collaboration/cyclic_lsts19_extension/README.md`](collaboration/cyclic_lsts19_extension/README.md):
  the fixed cyclic-point-link completion CNF, the \(C_{17}\)-equivariant
  exact-cover reduction, the exact \(1{,}326\)-branch census, and the
  scope-explicit bounded sweep.
- [`collaboration/opus5/cyclic_lsts19_extension_attack/NOTE.md`](collaboration/opus5/cyclic_lsts19_extension_attack/NOTE.md):
  Opus 5's independently executable algebraic audit of that construction
  frontier, including the orbit congruence, the full-rank first-moment system,
  the type-(i) domino reduction, and the exact-cover branch invariant.
- [`collaboration/opus5/derivation_tower_obstruction/NOTE.md`](collaboration/opus5/derivation_tower_obstruction/NOTE.md):
  the derivation homomorphism, packing dichotomy, and the exact implication
  from the \(455\)-case aggregate certificate to EH-core repair distance four.
- [`collaboration/opus5/generic_radius4_certificate_attack/NOTE.md`](collaboration/opus5/generic_radius4_certificate_attack/NOTE.md):
  the generic one-point lift theorem, including its \(s=1\) boundary, and the
  exact fixed-root restriction quantifiers.  Its exhaustive tower profiler
  independently reproduces the classical Kramer--Mesner value \(D(10)=5\);
  it does not decide \(LS(3,4,20)\) or #835.
- [`collaboration/h3_generic_one_point_audit/README.md`](collaboration/h3_generic_one_point_audit/README.md):
  an independent proof and implementation audit of the one-point theorem,
  labelled inverse, two-point counterexamples, restriction quantifiers, and
  the small packing maxima through \(S(4,5,11)\).
- [`collaboration/simultaneous_ls3420_fan/README.md`](collaboration/simultaneous_ls3420_fan/README.md):
  the unrestricted \(51{,}357\)-vertex shadow forced at \(k=16\), equivalently
  thirteen labelled \(LS(3,4,20)\) extensions sharing one
  \(LS(2,3,19)\) point-link with \(3{,}876\) cross-copy all-different
  constraints; its \(50{,}388\)-vertex fixed-link conflict graph and exact
  Hoffman-bound delimiter are independently audited and executable.
- [`collaboration/h3_simultaneous_fan_audit/README.md`](collaboration/h3_simultaneous_fan_audit/README.md):
  an independent derivation, edge census, Gram-identity check, and
  standard-library verifier for the simultaneous-fan theorem.
- [`collaboration/unrestricted_lift_tower/NOTE.md`](collaboration/unrestricted_lift_tower/NOTE.md):
  a reversible, symmetry-free thirteen-level tower for the full
  \(J(32,16)\) colouring.  It identifies the simultaneous \(13\)-fan as the
  exact truncation through level one and reduces the first lift to linked
  \(K_{13}\)-hole completions of partial one-factorizations of \(K_{18}\);
  the elementary parity condition for every hole is proved automatic.  More
  generally, each subsequent lift is exactly a joint
  \(K_{j+1}^{(j)}\)-decomposition problem, and every standard local
  divisibility condition for all twelve lifts is proved automatic.
- [`collaboration/high_lift_complement_decomposition/NOTE.md`](collaboration/high_lift_complement_decomposition/NOTE.md):
  a proof that at \(j=10,11,12\) those divisibility conditions are also
  sufficient for every fixed-\(R\) decomposition, with cross-colour block
  compatibility automatic.  The rank-three case reduces two-graphs to
  upper shadows of matchings.
- [`collaboration/high_lift_top_properness/NOTE.md`](collaboration/high_lift_top_properness/NOTE.md):
  proofs that cross-\(R\) top-properness is automatic at all three final
  lifts \(j=10,11,12\).  The last lift is the missing-colour map of a
  proper \(17\)-edge-colouring of \(K_{17}\); the two preceding lifts are
  forced by exact defect recurrences.  At \(j=10\), every colour's
  multiplicity graph is either all of \(K_{13}\) or \(K_{13}\) with one
  star deleted.  These theorems remain conditional on constructing the
  lower tower.
- [`collaboration/h3_j9_top_properness_audit/NOTE.md`](collaboration/h3_j9_top_properness_audit/NOTE.md):
  a solver-free extension of automatic top-properness to \(j=9\).  The
  fixed-colour recurrence forces an exact pair-additive multiplicity tensor
  with common fractional part \(1/3\); a short integer-weight argument then
  rules out every repeated colour in a fourteen-entry column.
- [`collaboration/j9_integer_weight_lemma/NOTE.md`](collaboration/j9_integer_weight_lemma/NOTE.md):
  an independent proof and standard-library arithmetic audit of the final
  \(K_{13}\) integer edge-weight lemma used in the \(j=9\) theorem.
- [`collaboration/h3_j8_exact_trade_elimination/NOTE.md`](collaboration/h3_j8_exact_trade_elimination/NOTE.md):
  a solver-free elimination of the exact triple-degree-zero branch at
  \(j=8\).  Complementary nine-set sums and the mod-\(6\) recurrence force
  every integral \(3\)-trade coefficient to vanish; the general
  triple-degree-at-most-three case remains open.
- [`collaboration/h3_j8_torsion_dichotomy/NOTE.md`](collaboration/h3_j8_torsion_dichotomy/NOTE.md):
  an exact reduction of every \(j=8\) four-cube coefficient to
  \(0,\pm60\), together with prime-field rank calculations proving that the
  nine-set mod-\(6\) rows add nothing beyond the five-set mod-\(2\) and
  six-set mod-\(3\) rows.  In the normalized \(\Delta=60\) branch, the
  negative-cell load is at most \(20\), the positive-cell load at most
  \(80\), and every triple load has one binary mod-\(7\) choice.  That
  branch remains open.
- [`collaboration/h3_j8_n0_outside_s5/NOTE.md`](collaboration/h3_j8_n0_outside_s5/NOTE.md):
  an independently replayed exact finite elimination of the \(N=0\)
  torsion subclass invariant under all permutations of the five vertices
  outside the cube.  A dependency-free audit checks the complete
  1,386-variable, 1,318-constraint orbit model.  The exterior symmetry is
  an extra ansatz, so the unrestricted \(N=0\) branch remains open.
- [`collaboration/h3_j8_n0_outside_s4_boundary/NOTE.md`](collaboration/h3_j8_n0_outside_s4_boundary/NOTE.md):
  a boundary attack fixing one exterior point and imposing \(S_4\) symmetry
  on the other four.  Independent full-equation CP-SAT and rank-reduced
  Gurobi searches exactly eliminate seven \((m,w)\) subcases, with a
  dependency-free audit of all orbit counts, row reductions, and cube
  symmetry breakers.  Twelve branches and the unrestricted \(N=0\)
  problem remain open.
- [`collaboration/first_lift_support_completion/NOTE.md`](collaboration/first_lift_support_completion/NOTE.md):
  the exact separation between support-admissible,
  partial-factorization-realizable, and fan-realizable first-lift
  instances; a matching-deletion capacity inequality for every edge set;
  and a proof that all ordinary cut instances are automatic.  The logged
  dense completion searches are positive evidence only, not a universal
  first-lift theorem.
- [`collaboration/first_lift_sufficiency_search/NOTE.md`](collaboration/first_lift_sufficiency_search/NOTE.md):
  a proof that the arbitrary nonnegative-weight matching inequalities
  characterize fractional first-lift completion, an exact identification
  of the deletion inequalities as their binary slice, exhaustive order-five
  controls, and a counterexample to the naive one-chain Kempe shortcut.
  Integer completion on thirteen vertices remains unproved.
- [`collaboration/opus5/first_lift_k13_hole/NOTE.md`](collaboration/opus5/first_lift_k13_hole/NOTE.md):
  Opus 5's independently replayed first-lift attack.  It proves two cut
  inequalities necessary for every prescribed \(K_{13}\)-hole completion
  and proves by exact dynamic programming that neither can fail at
  \(k=16\).  It also supplies smaller class-B′ counterexamples and a
  cut-clean non-completable instance, so the inequalities are not sufficient
  in general.  All \(42{,}300\) sampled \(k=16\) instances completed, but
  universal completion remains open.
- [`collaboration/opus5/first_lift_classB_attack/NOTE.md`](collaboration/opus5/first_lift_classB_attack/NOTE.md):
  Opus 5's stronger class-B follow-up.  It proves the two-sided bipartite
  capacity condition (BC), its parity refinement (BP), exact threshold
  theorems showing neither can obstruct the \(n=13,r=5\) target, and complete
  enumerations of three nearby parameter pairs.  It also gives explicit
  counterexamples proving that these conditions and the tested fractional
  relaxation are not sufficient in general.  The target class-B completion
  theorem, and hence the first lift, remain open.
- [`collaboration/first_lift_partial_factorization_audit/NOTE.md`](collaboration/first_lift_partial_factorization_audit/NOTE.md):
  an independent audit of the exact class-B′/partial-factorization
  equivalence and the nearby literature.  It gives a solver-free
  five-saturated-vertex counterexample at order \(12\), showing that no
  unrestricted five-row completion theorem is possible; the order-\(18\)
  target remains untouched because its supports are much denser.
- [`collaboration/first_lift_dense_support_prefix/NOTE.md`](collaboration/first_lift_dense_support_prefix/NOTE.md):
  a solver-free dense-support packing lemma.  It proves that every target
  first-lift palette has a simultaneously matchable five-colour prefix and
  that every profile containing a support-twelve colour has a six-colour
  prefix.  Global compatibility across all seventeen colours remains open.
- [`collaboration/first_lift_global_theorem/NOTE.md`](collaboration/first_lift_global_theorem/NOTE.md):
  an exact target-order class-B′ example showing that an arbitrary valid
  dense five-colour prefix need not extend even to the sixth colour.  The
  same instance has an explicit different full completion, so this rules
  out the greedy-prefix proof strategy rather than the first-lift theorem.
- [`collaboration/first_lift_global_theorem/SEARCH_README.md`](collaboration/first_lift_global_theorem/SEARCH_README.md):
  reproducible negative evidence from all \(1{,}344\) cases in a fixed
  finite three-cell weighted relaxation.  Its best obstruction margin is
  zero; this is a scoped search record, not a completion theorem.
- [`collaboration/first_lift_global_theorem/TWO_STAR_NOTE.md`](collaboration/first_lift_global_theorem/TWO_STAR_NOTE.md):
  a coordinated two-star theorem at the target order.  Two
  minimum-degree-six \(11\)-by-\(11\) incidence matchings can always be
  chosen without a common-label collision, so every class-B instance admits
  a proper support-respecting colouring of all \(23\) edges incident with
  any chosen pair of vertices.
- [`collaboration/first_lift_global_theorem/SIX_PACKING_NOTE.md`](collaboration/first_lift_global_theorem/SIX_PACKING_NOTE.md):
  a universal six-colour packing theorem for every target class-B support
  profile.  A Tutte-extremal switching argument handles the unique
  non-greedy profile, proving that some dense five-colour prefix always
  extends to a sixth matching; the remaining eleven colours are unresolved.
- [`collaboration/first_lift_global_theorem/SEVEN_PACKING_NONZERO_R_NOTE.md`](collaboration/first_lift_global_theorem/SEVEN_PACKING_NONZERO_R_NOTE.md):
  a seven-colour packing theorem for every target profile containing a
  size-twelve support.  A six-matching resilience lemma on twelve vertices
  proves the extension; the exceptional profile \((7,10,0)\) is reduced to
  two explicit residual equality barriers, \(K_7-E(K_3)\) and \(K_6\).
- [`collaboration/first_lift_global_theorem/SEVEN_PACKING_R0_NOTE.md`](collaboration/first_lift_global_theorem/SEVEN_PACKING_R0_NOTE.md):
  closes the exceptional \((7,10,0)\) profile by proving the two equality
  cores cannot coexist and using the class-B row sums to escape the unique
  surviving core.  Together the two notes give a universal seven-colour
  prefix; completion of the remaining ten colours is still open.
- [`collaboration/first_lift_global_theorem/PROPAGATION_COUNTEREXAMPLE.md`](collaboration/first_lift_global_theorem/PROPAGATION_COUNTEREXAMPLE.md):
  a minimal two-colour residual certificate showing that the exact
  residual-degree identity cannot propagate an arbitrary prefix.  An
  explicit locally maximal fifteen-matching prefix leaves
  \(C_3\mathbin{\dot\cup}C_5\) on two identical supports; this rules out
  the invariant-only induction, not a different global completion.
- [`collaboration/first_lift_global_theorem/EIGHTH_MATCHING_CORE_CATALOGUE.md`](collaboration/first_lift_global_theorem/EIGHTH_MATCHING_CORE_CATALOGUE.md):
  the exact large-support obstruction catalogue after seven matchings.
  A blocked size-ten support forces one of seven complete multipartite
  cores; a blocked size-twelve support forces \(K_7\) or
  \(K_8-E(K_3)\).  This is a historical intermediate reduction: its
  exceptional-\(r=0\) configurations are now closed by the theorem below,
  while coordinated packing, rather than arbitrary-prefix extension, is
  now the relevant nonzero-profile question.
- [`collaboration/first_lift_global_theorem/R0_EIGHTH_MATCHING_THEOREM.md`](collaboration/first_lift_global_theorem/R0_EIGHTH_MATCHING_THEOREM.md):
  the consolidated computer-assisted theorem that every exceptional
  \((7,10,0)\) seven-prefix of type \(8^4\,10^3\) extends to an eighth
  matching.  Its dependency ledger gives the exact commits and replay
  artifacts for all one-through-seven-core branches.  The theorem is
  strictly \(r=0\); the two coordinated theorems below handle every
  nonzero profile.  The final nine colours remain open.
- [`collaboration/coordinated_eight_r1/NOTE.md`](collaboration/coordinated_eight_r1/NOTE.md):
  a solver-free coordinated eight-packing theorem for the last outstanding
  profile \(r=1\).  An affine expectation bound selects a six-complement
  cover; saturated \(K_{5,5}\) and \(K_6\) obstruction cores then force a
  seventh matching, and a twelve-vertex Tutte lemma supplies the eighth.
- [`collaboration/coordinated_eight_r2_r5/NOTE.md`](collaboration/coordinated_eight_r2_r5/NOTE.md):
  a solver-free universal coordinated eight-packing theorem for every
  class-B profile with \(r=2,3,4,5\).  A probabilistic complement-cover
  lemma produces six matchings whose union has maximum degree at most five;
  Ore/Dirac Hamiltonicity then supplies two further size-twelve matchings.
  Together with the \(r=0\) and \(r=1\) theorems, this closes the coordinated
  eighth frontier for all six class-B profiles.
- [`collaboration/coordinated_nine_structural/NOTE.md`](collaboration/coordinated_nine_structural/NOTE.md):
  a solver-free prescribed three-near-factor theorem: every graph on
  thirteen vertices with minimum degree at least seven contains three
  pairwise edge-disjoint near-perfect matchings with arbitrary prescribed
  omissions, including repetitions.  Exact Tutte catalogues reduce the
  proof to three terminal cores, and explicit switches eliminate all three.
  Applied to the complement-cover six-prefix, this proves coordinated
  nine-packings directly for the class-B profiles \(r=3,4,5\); the
  \(r=1,2\) profiles are now closed by the mixed-support theorems below.
  Profile \(r=0\), colours ten through seventeen, the later
  fan-compatibility layers, and Problem #835 remain open.
- [`collaboration/r0_complement_cover_six/NOTE.md`](collaboration/r0_complement_cover_six/NOTE.md):
  a solver-free \(r=0\) complement-covering six-prefix theorem.  An exact
  expectation argument selects three size-eight and three size-ten supports,
  while a new dense-ambient lemma packs arbitrary three prescribed
  ten-supports in every thirteen-vertex graph of minimum degree at least nine.
  A distinct-triple example also refutes the tempting universal \(4+2\)
  complement cover.  Three further matchings in the residual
  minimum-degree-seven graph are still required for coordinated nine.
- [`collaboration/r0_three_ten_obstruction/NOTE.md`](collaboration/r0_three_ten_obstruction/NOTE.md):
  a sharp delimiter for extending that \(r=0\) prefix.  At least two of the
  seven remaining size-ten supports always extend individually, and an exact
  valid class-B instance has precisely two, so an arbitrary such prefix
  cannot reach nine by appending three size-ten colours.  The same instance
  refutes an ambient forced-edge strengthening of the three-near-factor
  theorem.  A successful proof must switch the prefix or use a remaining
  size-eight support.
- [`collaboration/r0_three_ten_obstruction/DEAD_SIX_PREFIX.md`](collaboration/r0_three_ten_obstruction/DEAD_SIX_PREFIX.md):
  a stronger exact dead-prefix certificate attaining the same lower bound
  while blocking all four remaining size-eight supports as well.  Precisely
  two of its eleven remaining colours are individually matchable, so no
  three-colour continuation of that six-prefix exists.  This forces an
  \(r=0\) coordinated-nine proof to backtrack or switch the six-prefix
  itself.  A separate exact witness fully decomposes the same support
  instance into all seventeen matchings, proving that the obstruction is
  purely prefix-dependent.
- [`collaboration/r0_three_ten_obstruction/K6_PREFIX_SWITCH.md`](collaboration/r0_three_ten_obstruction/K6_PREFIX_SWITCH.md):
  a solver-free support-preserving switch theorem for \(r=0,1,2\).
  After any complement-cover six-prefix, a blocked size-ten support can
  arise only from a unique saturated \(K_6\); one two-edge switch destroys
  that component without creating another.  Consequently every remaining
  size-ten support is individually matchable.  Simultaneous selection of
  three such matchings is still open.
- [`collaboration/r0_three_ten_obstruction/K6_FREE_THREE_TEN_OBSTRUCTION.md`](collaboration/r0_three_ten_obstruction/K6_FREE_THREE_TEN_OBSTRUCTION.md):
  a literal distinct-complement class-B \(r=0\) certificate showing that
  the \(K_6\)-free conclusion still does not coordinate three size-ten
  colours.  All seven supports are individually live, but six matching
  families force the same edge, so none of the \(35\) triples packs.  The
  same prefix has an explicit mixed \(10+10+8\) extension, so the
  \(r=0\) proof must use a size-eight colour, change more than two prefix
  edges, or choose a different complement-cover prefix.
- [`collaboration/r0_three_ten_obstruction/K6_FREE_MIXED_DEAD_PREFIX.md`](collaboration/r0_three_ten_obstruction/K6_FREE_MIXED_DEAD_PREFIX.md):
  a sharper equality certificate in which the prefix is \(K_6\)-free,
  all four remaining size-eight colours are blocked, all seven size-ten
  colours are live, and none of the \(165\) remaining-colour triples packs.
  One additional support-preserving two-edge trade explicitly repairs it.
  Exact row arithmetic reduces this six-fold forced-edge boundary to
  \((a,r)=(0,2),(0,3),(1,3)\), and a solver-free equality-core lemma proves
  that a core-breaking trade always exists.
- [`collaboration/coordinated_nine_r0_pair_gate_sat/NOTE.md`](collaboration/coordinated_nine_r0_pair_gate_sat/NOTE.md):
  six exact SAT/DRAT orbit certificates proving the \(r=0\) pair gate:
  two live size-ten families either admit edge-disjoint perfect matchings or
  share a common forced edge.  The semantic auditor reconstructs every CNF,
  checks its manifest and hash, and replays all six DRAT proofs.
- [`collaboration/r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md`](collaboration/r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md):
  a solver-free trade theorem coordinating any two of the six forced
  size-ten families with the seventh family throughout all three equality
  cases, including repeated complements.
- [`collaboration/r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md`](collaboration/r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md):
  an exact classification of the seven-family incompatibility graph as
  \(K_t\dot\cup(7-t)K_1\), \(t\le6\).  The no-independent-triple case is
  precisely the equality boundary already repaired above.  The remaining
  \(r=0\) gate must use the full complement-row inventory to coordinate an
  independent triple; pairwise compatibility alone is not sufficient.
- [`collaboration/r0_three_family_helly_gate/NOTE.md`](collaboration/r0_three_family_helly_gate/NOTE.md):
  an exact full-row counterexample to the tempting three-family Helly step.
  Three repeated live supports have 42 perfect matchings, every pair of
  colour occurrences coordinates, yet no three matchings are mutually
  edge-disjoint.  A compact 190-pair certificate proves the failure.
  Nevertheless 34 of the certificate's 35 seven-family colour triples do
  pack, isolating the correct remaining target as a global seven-family
  selection theorem.
- [`collaboration/r0_three_family_helly_gate/GLOBAL_ALL_35_OBSTRUCTION.md`](collaboration/r0_three_family_helly_gate/GLOBAL_ALL_35_OBSTRUCTION.md):
  a stronger full-row \(r=0\) prefix on which all 35 triples of remaining
  size-ten occurrences fail.  Every pair still coordinates, all 84
  \(10+10+8\) routes pack, and one support-preserving two-edge switch repairs
  all 35 size-ten routes.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_opus5_note.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_opus5_note.md):
  an independently audited cut invariant for simultaneous remaining
  matchings.  A complete \(2^{13}\)-cut check corrects the first orbit-4
  interpretation: every regenerated targeted bad-prefix orbit \(2,\ldots,10\)
  violates the simple internal-edge capacity inequality.  This is evidence
  for, not a proof of, cut sufficiency.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_audit.md):
  the independently corrected audit of a second Opus 5 attack.  It verifies
  an explicit weaker-ambient example in which all \(2^{13}\) capacity cuts
  pass although even one selected perfect matching is impossible, and proves
  that the full class-B row inventory excludes that example.  It retains the
  valid small-cut and single-row reductions while rejecting an erroneous
  directed-cut bound and an unproved edge-colouring jump.  Cut sufficiency
  under the full eleven-row equations was still open at that stage; the
  later factor theorem below closes the \(b\)-factor half only.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_factor_followup_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_factor_followup_audit.md):
  the corrected audit of the follow-up factor/colouring attack.  It identifies
  (C) with the elementary \(b\)-Hall slice when all three terms are positive,
  proves the component-parity and bridge-colour necessities, and independently
  verifies a full-row instance that fails exactly one six-set cut by one edge.
  It rejects the run's false independence-number lemma and does not promote
  the incomplete Tutte--Lovász case analysis to a theorem.  The repaired,
  exhaustive factor proof below supersedes that incomplete analysis.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_complete.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_complete.md):
  the complete Tutte--Lovász elimination.  The first draft omitted three
  \(|A|=5\) size triples; an independent audit found them, the proof now
  closes them by six-, seven-, and eight-set cuts, and two independent
  arithmetic verifiers partition all 105 feasible separator-size triples.
  Thus (C) plus the full row ledger always gives the exact simple
  \(b\)-factor.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_independent_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_independent_audit.md):
  a line-by-line independent audit of the repaired factor theorem,
  including the exact normalization, parity, component bounds, all
  equality branches, and the three repaired \(|A|=5\) cases.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_colour_factor_agent_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_colour_factor_agent_audit.md):
  the exact nowhere-zero \(\mathbb F_2^2\) boundary-flow formulation for
  prescribed colouring.  Its verifier supplies balanced,
  bridge-admissible but uncolourable exact-degree factors in every one of
  the sixteen Venn types, proving that ambient factor switching is
  essential.
- [`collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_cut_sufficiency.md`](collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_cut_sufficiency.md):
  the computer-assisted closure of the identical-support orbit.  Two
  canonical compatible-pair types reduce to frozen UNSAT CNFs; their
  CaDiCaL traces pass both the generator's internal checks and a separate
  DRAT-trim replay.
- [`collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_cut_sufficiency.md`](collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_cut_sufficiency.md):
  the certified common-nine-core orbit theorem.  Its exhaustive
  path-and-cycle catalogue gives five canonical compatible-pair types.
  Every frozen CNF is UNSAT, independently solved with Glucose 4, and
  accompanied by a compressed DRAT trace that replays as `VERIFIED`.
- [`collaboration/r0_three_family_helly_gate/2026-07-28_orbit2_cut_sufficiency.md`](collaboration/r0_three_family_helly_gate/2026-07-28_orbit2_cut_sufficiency.md):
  the certified repeated-support orbit theorem.  Three marked alternating
  two-factor types reduce to independently audited UNSAT formulas, and
  their compressed DRAT traces all replay as `VERIFIED`.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_cut_sufficiency.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_cut_sufficiency.md):
  the certified orbit-three theorem.  Sixteen support-stabilizer pair
  types reduce to frozen UNSAT CNFs; a separate verifier reconstructs the
  static formulas and checks every learned prescribed-triple clause, and
  all sixteen compressed DRAT traces replay independently.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_remaining_pair_orbit_classifier.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_remaining_pair_orbit_classifier.md):
  the complete compatible-pair symmetry catalogue for support orbits
  four through fifteen.  Its component-word invariant and independent
  generator-action audit agree on all 7,077,840 labelled pairs, reducing
  them to exactly 1,126 canonical types.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md):
  a solver-free rigid-branch theorem from the concise Opus selection attack.
  When one dense six-set has all seven triple rows on its far side, one legal
  cross-switch makes every row triple pass every cut; all 20 binding
  \((p,q)\) types are independently checked.  The response's claimed next
  branch relied on overlap inequalities that were unproved in that response;
  the subsequent theorem below supplies the missing derivations.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_selection_theorem.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_selection_theorem.md):
  the complete solver-free cut-feasible repair-selection theorem.  A
  degree-cap ledger proves that dense six-cuts are disjoint, binding
  seven-cuts are unique, and a tight eight-cut is unique; the certified
  \(K_t\dot\cup(7-t)K_1\) incompatibility classification then guarantees a
  compatible triple outside every obstruction family.  The proof audits
  the one-switch budget in both the saturated-\(K_6\) preprocessing and
  six-fold equality branches.
- [`collaboration/opus5_r0_orbit_repair/2026-07-28_cut_cover_followup_audit.md`](collaboration/opus5_r0_orbit_repair/2026-07-28_cut_cover_followup_audit.md):
  the independent audit of the final Opus 5 obstruction-covering run.  It
  reconstructs the edge and degree ledgers, verifies the complete
  coexistence table and the sharp residual cover bound of eleven, and
  supplies the certified pair-compatibility dependency that the raw
  tool-free response correctly left conditional.
- [`collaboration/r0_three_family_helly_gate/2026-07-28_cut_cover_independent_theorem.md`](collaboration/r0_three_family_helly_gate/2026-07-28_cut_cover_independent_theorem.md):
  a second, independent proof of the same cut-selection result that does
  not use individual matchability, the pair gate, or the incompatibility
  graph.  It classifies all capacity failures directly, proves that a
  non-all-cover family of critical cuts misses at least one of the 35 row
  triples, and removes the three all-cover cases with the audited
  \(K_6\), \(K_6-e\), and rigid \(K_6-2K_2\) switches.
- [`collaboration/coordinated_nine_r0_repair_cegis/NOTE.md`](collaboration/coordinated_nine_r0_repair_cegis/NOTE.md):
  an exact semantic-witness CEGIS for one-layer support-preserving repair and
  a three-colour continuation.  Strict canonical replay has been audited; a
  replayed ten-minute campaign accumulated 2,190,962 valid repair cuts
  without finding either a counterexample or UNSAT.  The bounded run is
  coverage evidence, not a theorem; the two compressed witness logs are
  published in the
  [`r0-cegis-evidence-2026-07-28`](https://github.com/dennisonbertram/erdos-835-conjectural-resolution/releases/tag/r0-cegis-evidence-2026-07-28)
  release.  Its companion `search_cut_feasible_repair.py` isolates the
  narrower cut-selection lemma, with independent raw counterexample replay,
  strict semantic-witness logging, canonical replay, and automatic final-CNF
  export if the accumulated model reaches UNSAT.
- [`collaboration/r0_three_family_helly_gate/freeze_full_row_cut_sufficiency.py`](collaboration/r0_three_family_helly_gate/freeze_full_row_cut_sufficiency.py):
  the certificate-oriented decision driver for the remaining local theorem.
  It reconstructs the exact 16 three-row Venn orbits by integer-cell
  enumeration, installs every binding cut statically, and freezes the final
  DIMACS formula and hash on incremental UNSAT.  The fast orbit enumerator
  reproduces the original orbit list while reducing its discovery time from
  about 40.3 seconds to 0.04 seconds.  Any UNSAT output still requires
  independent CNF reconstruction and CaDiCaL/DRAT-trim replay.
- [`collaboration/coordinated_nine_r1_reduction/NOTE.md`](collaboration/coordinated_nine_r1_reduction/NOTE.md):
  the exact \(r=1\) one- and two-step Tutte catalogues, core-reuse ceilings,
  and three literal class-B pair obstructions with triple intersections
  zero, one, and two.  These prove that even individually matchable
  size-ten supports need not admit arbitrary disjoint choices.  The
  companion pair gate uses all six triples simultaneously, and the
  terminal notes coordinate the size-twelve layer.
- [`collaboration/coordinated_nine_r1_gate_sat/NOTE.md`](collaboration/coordinated_nine_r1_gate_sat/NOTE.md):
  a certificate-complete proof of the \(r=1\) cross-family gate.  Six
  symmetry-orbit CNFs prove that two individually matchable size-ten
  supports either admit disjoint perfect matchings or share a common forced
  edge.  The included compressed CNFs and DRAT proofs are hash-checked,
  semantically reconstructed by an independent standard-library auditor,
  and all six replay with DRAT-trim.  This closes pair selection.  Exact
  class-B bookkeeping also eliminates the \(K_{5,7}\) size-twelve
  terminal.
- [`collaboration/coordinated_nine_r1_terminal_k311111/NOTE.md`](collaboration/coordinated_nine_r1_terminal_k311111/NOTE.md):
  a solver-free re-selection theorem for the separator-four
  \(K_{3,1^5}\) terminal, including the unique no-outside-edge pattern and
  its length-five augmenting repair.
- [`collaboration/coordinated_nine_r1_terminal_k7/NOTE.md`](collaboration/coordinated_nine_r1_terminal_k7/NOTE.md):
  the exact equality reduction and replacement-support theorem for the
  \(K_7\) terminal when neither selected size-ten matching has an edge
  wholly outside the seven-core.  Class-B incidence forces an unused triple
  to meet the core at least twice; \(91{,}140\) exhaustive cross-matching
  checks coordinate that replacement with the retained ten-support and the
  size-twelve support.  Its all-bad \(K_8\) construction also closes the
  equality case for an old outside-outside edge.
- [`collaboration/coordinated_nine_r1_terminal_k7_ww_sat/NOTE.md`](collaboration/coordinated_nine_r1_terminal_k7_ww_sat/NOTE.md):
  a certificate-complete proof of the remaining \(K_7\) two-switch gate.
  A stronger local CNF uses only the prefix degree bound, two five-edge
  matchings, core saturation, and the proper Hall-star condition.  CaDiCaL
  proves it unsatisfiable, and the committed DRAT proof independently
  replays with DRAT-trim.  Together with the two terminal notes and the
  pair gate, this proves the coordinated ninth extension for \(r=1\).
- [`collaboration/coordinated_nine_r2_obstruction/NOTE.md`](collaboration/coordinated_nine_r2_obstruction/NOTE.md):
  an exact \(r=2\) delimiter.  A legitimate \(8^4\,10^2\)
  complement-cover prefix can block every remaining size-ten support, so the
  fixed “append one ten and both twelves” route is false.  The same prefix has
  an explicit verified \(8+12+12\) extension to nine, showing that the
  obstruction is to that route rather than to coordinated nine.  The mixed
  theorem below now closes the universal \(r=2\) choice.
- [`collaboration/r2_terminal_flexibility/NOTE.md`](collaboration/r2_terminal_flexibility/NOTE.md):
  the complete terminal theorem for the \(r=2\) switching frontier.  After a
  size-eight or size-ten candidate, the first prescribed near-factor always
  exists.  The \(K_{5,7}\) and coarsened \(K_{3,1^5}\) terminals have explicit
  local switches; the ordinary, \(P_4\), and all-bad \(K_7\) rows switch as
  well.  The only rigid residue is a seventeen-edge \(K_7\) core, eliminated
  globally by the companion cross-route gate.
- [`collaboration/r2_size8_gate_obstruction/NOTE.md`](collaboration/r2_size8_gate_obstruction/NOTE.md):
  a literal class-B \(r=2\) six-prefix for which all five remaining
  size-eight supports are blocked by two disjoint \(K_5\) cores.  This
  refutes the universal \(8+12+12\) terminal route.  The same prefix has an
  explicit \(10+12+12\) extension to nine, isolating a size-eight/size-ten
  switching dichotomy rather than an obstruction to coordinated nine.
- [`collaboration/r2_initial_support_dichotomy/NOTE.md`](collaboration/r2_initial_support_dichotomy/NOTE.md):
  a solver-free theorem that after every \(r=2\) complement-cover
  six-prefix, at least one of the five remaining size-eight supports or four
  remaining size-ten supports has a residual perfect matching.  Common
  saturated \(K_6\) and \(K_5\) obstruction cores would require respectively
  \(22>21\) and \(15>14\) row incidences.  This is the initial-choice input to
  the completed terminal and cross-route theorem.
- [`collaboration/r2_size10_terminal_obstruction/NOTE.md`](collaboration/r2_size10_terminal_obstruction/NOTE.md):
  a literal class-B certificate showing that an arbitrary perfect matching
  on a live size-ten support need not extend with the two prescribed
  size-twelve near-factors.  Both near-factor families are nonempty but all
  \(120^2\) cross-pairs share one forced edge.  Together with the size-eight
  delimiter, this proves that the initial-support dichotomy must be
  strengthened to a globally coordinated choice.
- [`collaboration/r2_cross_route_reduction/NOTE.md`](collaboration/r2_cross_route_reduction/NOTE.md):
  the solver-free global bridge completing coordinated nine for \(r=2\).
  A seventeen-edge terminal core excludes every initially blocked size-eight
  or size-ten support and forces an alternative route; a saturated \(K_6\)
  supplies a direct complete-cut construction.  Combined with the exhaustive
  terminal switches and initial-support dichotomy, every legal
  \(8^4\,10^2\) six-prefix extends to nine.  The final eight colours and the
  later fan-realizability layers remain open.
- [`collaboration/opus5/coordinated_nine_and_global_bridge/NOTE.md`](collaboration/opus5/coordinated_nine_and_global_bridge/NOTE.md):
  Opus 5's max-effort audit.  It supplies an independent exact \(r=0\)
  dead-prefix certificate, a solver-free saturated-core switch covering
  both \(K_6\) and \(K_{5,5}\), and a global theorem identifying the next
  tower coupling as six simultaneous same-colour matchings across six
  class-B instances.  Its proposed three-size-ten conjecture was refuted by
  the parallel \(K_6-e\) equality certificate; a post-run audit in the note
  records that correction explicitly.
- [`collaboration/k7_terminal_switching/NOTE.md`](collaboration/k7_terminal_switching/NOTE.md):
  a self-contained independent proof and \(6^7\)-case arithmetic audit of
  the last separator-five \(K_7\) switch.  It tracks the exact Hall
  missing-label mutation that invalidates a naive three-edge switch and
  supplies the corrected size-six and exceptional-type repairs.
- [`collaboration/coordinated_nine_search/NOTE.md`](collaboration/coordinated_nine_search/NOTE.md):
  exact optimization evidence on \(3{,}726\) fixed class-B instances.
  Every tested instance had packing number seventeen, including
  switch-walk, duplicate-heavy, and dead-prefix cases.  This motivates the
  full class-B completion conjecture but is not an exhaustive theorem.
- [`collaboration/first_lift_global_theorem/R1_DEAD_SEVEN_PREFIX.md`](collaboration/first_lift_global_theorem/R1_DEAD_SEVEN_PREFIX.md):
  an exact \(r=1\) class-B seven-prefix that blocks all ten remaining
  supports even though the same support matrix has a separate full
  seventeen-matching completion.  Thus arbitrary-prefix extension is
  false and coordinated switching is genuinely necessary.
- [`collaboration/first_lift_global_theorem/R1_MINIMUM_LAYER_REPAIR.md`](collaboration/first_lift_global_theorem/R1_MINIMUM_LAYER_REPAIR.md)
  and [`R1_MINIMUM_FULL_REPAIR.md`](collaboration/first_lift_global_theorem/R1_MINIMUM_FULL_REPAIR.md):
  exact repair distances for that \(r=1\) certificate.  One changed layer
  admits an eighth matching, while a full completion needs exactly three;
  the latter lower bound is a solver-free \(6:7\) crossing-cut argument.
- [`collaboration/first_lift_global_theorem/R3_DEAD_SEVEN_PREFIXES.md`](collaboration/first_lift_global_theorem/R3_DEAD_SEVEN_PREFIXES.md):
  two exact \(r=3\) dead seven-prefixes, with nested \(C\subset G\) and
  \(D\subset G\) obstruction cores.  Both block all ten remaining supports
  but their support matrices have explicit full completions.
- [`collaboration/first_lift_global_theorem/R3_MINIMUM_LAYER_REPAIR.md`](collaboration/first_lift_global_theorem/R3_MINIMUM_LAYER_REPAIR.md):
  exact repair distances for the two \(r=3\) certificates: one changed
  layer admits an eighth matching, while full completion requires four
  changes in the \(C\subset G\) case and three in the \(D\subset G\) case.
- [`collaboration/first_lift_global_theorem/R2_DEAD_SEVEN_PREFIX.md`](collaboration/first_lift_global_theorem/R2_DEAD_SEVEN_PREFIX.md)
  and [`R4_DEAD_SEVEN_PREFIX.md`](collaboration/first_lift_global_theorem/R4_DEAD_SEVEN_PREFIX.md):
  fully completable dead arbitrary prefixes closing the analogous boundary
  for \(r=2\) and \(r=4\).
- [`collaboration/first_lift_global_theorem/R2_R4_STRUCTURAL_REPAIR.md`](collaboration/first_lift_global_theorem/R2_R4_STRUCTURAL_REPAIR.md):
  exact one-layer and full-completion repair distances for those two
  certificates, a cut-bound transport lemma across the \(r=1\to2\) and
  \(r=3\to4\) lifts, and literal class-B-prime realizations.
- [`collaboration/first_lift_global_theorem/CLASS_B_PRIME_DEAD_PREFIX_REALIZATIONS.md`](collaboration/first_lift_global_theorem/CLASS_B_PRIME_DEAD_PREFIX_REALIZATIONS.md):
  proper saturated partial \(K_{18}\) factorizations inducing the \(r=1\)
  and both \(r=3\) dead-prefix support matrices.  These examples are
  class-B-prime but are not asserted fan-realizable.
- [`collaboration/first_lift_global_theorem/CUT_CAPACITY_FULL_REPAIR_BOUNDS.md`](collaboration/first_lift_global_theorem/CUT_CAPACITY_FULL_REPAIR_BOUNDS.md):
  a general crossing-cut lower bound for the number of prefix layers any
  full repair must change, with exhaustive all-cut audits recovering the
  exact \(r=1\) and both \(r=3\) distances above.
- [`collaboration/first_lift_global_theorem/R5_LARGE_SUPPORT_PAIR_COUNTEREXAMPLE.md`](collaboration/first_lift_global_theorem/R5_LARGE_SUPPORT_PAIR_COUNTEREXAMPLE.md):
  an \(r=5\) certificate blocking both remaining size-twelve supports while
  every remaining size-eight support still extends.  It refutes only the
  large-support-first route; the stronger certificate below subsequently
  closed arbitrary-prefix extension itself.
- [`collaboration/first_lift_global_theorem/R5_DEAD_SEVEN_PREFIX.md`](collaboration/first_lift_global_theorem/R5_DEAD_SEVEN_PREFIX.md):
  a fully completable class-B-prime \(r=5\) instance with a seven-prefix
  blocking all ten remaining supports.  Together with the \(r=1,2,3,4\)
  certificates, blind arbitrary-prefix induction is now refuted for every
  nonzero profile.
- [`collaboration/first_lift_global_theorem/TWELVE_SUPPORT_SWITCHING_NOTE.md`](collaboration/first_lift_global_theorem/TWELVE_SUPPORT_SWITCHING_NOTE.md):
  a two-edge switching-resilience theorem on twelve vertices.  After any
  six matching layers, a residual perfect matching can avoid any prescribed
  one or two disjoint available edges; every seventh-layer obstruction must
  contribute a critical matching pattern of size at least three.
- [`collaboration/first_lift_global_theorem/R0_CORE_PAIR_CATALOGUE.md`](collaboration/first_lift_global_theorem/R0_CORE_PAIR_CATALOGUE.md):
  an exact \(S_{13}\)-reduced enumeration of all \(764{,}764\) labelled
  size-ten obstruction cores in the exceptional profile.  The pair table
  rules out every coexistence involving \(K_{3,3,3}\), restricts
  \(K_{5,5}\) to one partner type, and leaves a finite sparse-core overlap
  frontier for the eighth matching.
- [`collaboration/first_lift_global_theorem/R0_ROW_SUM_CORE_ELIMINATION.md`](collaboration/first_lift_global_theorem/R0_ROW_SUM_CORE_ELIMINATION.md):
  combines the pair catalogue with exact complement row sums to eliminate
  \(K_{3,3,3}\), \(K_{5,5}\), and \(K_{3,7}\) from any obstruction of all
  seven remaining size-ten supports.  The exhaustive \(K_{3,7}\) branch
  checks 147 degree-valid prefix graphs and 588 reuse cases.  Its statement
  that four sparse types remained unresolved records that intermediate
  stage; those \(r=0\) types are now exhausted in the consolidated theorem.
- [`collaboration/first_lift_global_theorem/r0_two_core_refutations/README.md`](collaboration/first_lift_global_theorem/r0_two_core_refutations/README.md):
  independently replayed DRAT certificates for all twenty-two two-core
  branches that have enough reuse capacity to block all seven remaining
  size-ten supports.  Together with the analytic disjoint-\(K_6\) case,
  this proves that any total obstruction must use at least three distinct
  surviving cores.  Its three-or-more-core frontier is historical: the
  later three-through-seven-core layers close it for \(r=0\).
- [`collaboration/first_lift_global_theorem/R0_FIVE_CORE_ZERO_B.md`](collaboration/first_lift_global_theorem/R0_FIVE_CORE_ZERO_B.md)
  and [`R0_FIVE_CORE_ZERO_B_UNION.md`](collaboration/first_lift_global_theorem/R0_FIVE_CORE_ZERO_B_UNION.md):
  two independent exact exclusions of all 21 five-core type multisets over
  \(K_{5,1,1,1},K_{3,1,1,1,1},K_6\): a full labelled-family census with
  vertex-set row cuts, and a compact support-union optimization.  Together
  with the \(K_{3,3,1,1}\)-containing screen, they close every exactly-five-
  core \(r=0\) obstruction.
- [`collaboration/first_lift_global_theorem/R0_SIX_SEVEN_SIX_SEVEN_EXCEPTIONAL.md`](collaboration/first_lift_global_theorem/R0_SIX_SEVEN_SIX_SEVEN_EXCEPTIONAL.md):
  the terminal six/seven-core layer.  With the companion zero-through-five
  non-\(K_6\) classifications, it exhausts every exactly-six- or
  exactly-seven-core \(r=0\) cover by exact union minima and complement
  row-rank inequalities.
- [`collaboration/first_lift_global_theorem/write_r0_full_blocking_cnf.py`](collaboration/first_lift_global_theorem/write_r0_full_blocking_cnf.py):
  a core-independent exact CNF for the complete exceptional-profile
  eighth-matching obstruction, including all perfect matchings of every
  chosen ten-support.  It is reproducible search tooling, not a terminal
  SAT or UNSAT result.
- [`collaboration/first_lift_aggregate_graphicity/NOTE.md`](collaboration/first_lift_aggregate_graphicity/NOTE.md):
  an exhaustive relaxation theorem proving that the aggregate degree
  sequence of every colour subfamily is graphic.  All \(18{,}032\) relaxed
  sequences pass both Erdős--Gallai and Havel--Hakimi, so any obstruction
  must use colour-by-colour compatibility rather than aggregate degrees.
- [`collaboration/fan_small_controls/ALL_K6_THEOREM.md`](collaboration/fan_small_controls/ALL_K6_THEOREM.md):
  the complete universal \(k=6\) fan obstruction, including the exhaustive
  two-type \(LS(2,3,9)\) classification and two explicit 18-cell human
  proofs.
- [`collaboration/h3_simultaneous_fan_attack_2/NOTE.md`](collaboration/h3_simultaneous_fan_attack_2/NOTE.md):
  exact cyclic-link kernel ranks, the prime-field consistency delimiter, the
  full clique-number-\(13\) proof, the Schur-power characterization, and the
  \(C_{17}\)-invariant certificate target.
- [`collaboration/fan_13adic_screen/NOTE.md`](collaboration/fan_13adic_screen/NOTE.md):
  the exact Smith/cokernel screen proving that the cyclic quotient's signed
  matching equation is solvable over \(\mathbb Z\).
- [`collaboration/fan_13adic_screen/branch0_prefix1_refutation/README.md`](collaboration/fan_13adic_screen/branch0_prefix1_refutation/README.md):
  one byte-reconstructible \(88\)-row prefix-local refutation in the fixed
  cyclic-link quotient, with its exact CNF and independently replayable
  compressed DRAT proof.  This excludes only that explicit prefix.
- [`collaboration/fan_13adic_screen/c17_layer_scan_1326/README.md`](collaboration/fan_13adic_screen/c17_layer_scan_1326/README.md):
  scope-explicit bounded telemetry for both fixed-point layers of all
  \(1{,}326\) mixed branches.  It records 19 compatible prefix-local
  failures and 2,485 `UNKNOWN` layer outcomes; it is not a global
  unsatisfiability result.
- [`collaboration/fan_13adic_screen/finite_first_packing_132/README.md`](collaboration/fan_13adic_screen/finite_first_packing_132/README.md):
  an exact collision-free packing of 132 of the 140 finite quadruple
  orbits in the fixed cyclic-link quotient, with a semantic witness checker
  and byte-reconstructed telemetry for 140 size-139 searches.  This proves
  only the lower bound \(\alpha_{\rm finite}\ge132\); every size-139 run
  remained `UNKNOWN`, so the upper bound is still the trivial 140.  A
  separate exact search excludes 302,743 explicitly defined neighborhoods
  around one score-ten near-assignment, without implying a global upper
  bound.
- [`collaboration/fan_gadget_generalization/NOTE.md`](collaboration/fan_gadget_generalization/NOTE.md):
  the nonlinear \(k=6\) delimiter, sharp palette-anchor bounds, and the
  universal theorem \(\omega(H_L)=13\), together with the exhaustive cyclic
  quotient theorem that every nonzero squarefree trade has support at least
  twelve.  All seven possible support-ten Q-group partitions are excluded
  exactly; this remains a local rigidity result, not a fan obstruction.
- [`collaboration/fan_gadget_generalization/support12_attack/NOTE.md`](collaboration/fan_gadget_generalization/support12_attack/NOTE.md):
  exact exclusions for all eleven multiplicity partitions of a
  support-twelve cyclic quotient trade.  Therefore every nonzero squarefree
  trade in this quotient has support at least fourteen.  This remains a
  local quotient obstruction, not a resolution of the simultaneous fan.
- [`collaboration/h3_k6_fan_theorem_audit/README.md`](collaboration/h3_k6_fan_theorem_audit/README.md):
  an independent reconstruction of the universal \(k=6\) theorem and
  byte-level audits of all three cyclic invariant-fan CNFs, plus the
  independently reconstructed \(C_{17}\)-invariant matching matrix and both
  exact matching CNFs.
- [`collaboration/opus5/unrestricted_ls3420_attack_2/NOTE.md`](collaboration/opus5/unrestricted_ls3420_attack_2/NOTE.md):
  Opus 5's unrestricted star-sign and holonomy attack, including the
  correctly indexed joint parity law, its exact top-rung rank, a
  non-abelian tower identity, reproducible CNFs, retained positive control,
  and an independent audit. These are necessary identities and route
  delimiters; they do not decide \(LS(3,4,20)\), \(k=16\), or #835.
- [`evidence/holonomy_group_algebra_tower.md`](evidence/holonomy_group_algebra_tower.md):
  the exact noncommutative tower identity, augmented cocycle, natural-module
  flatness theorem, and a twenty-link pseudogluing control that passes all
  aggregate fingerprints while failing \(27{,}478\) actual overlap
  comparisons.
- [`collaboration/opus5/holonomy_followup/NOTE.md`](collaboration/opus5/holonomy_followup/NOTE.md):
  Opus 5's proof that the tower identity is gauge-vacuous, the exact
  one-factorization intercalate congruence, and the certified
  two-dimensional universal \(\mathbb F_2\) census space at \(K_{18}\).
- [`collaboration/h3_holonomy_audit/README.md`](collaboration/h3_holonomy_audit/README.md):
  an independent proof and implementation audit, including a separate
  deterministic \(3{,}000\)-factorization computation attaining the maximal
  affine rank \(53\).
- [`evidence/solver_reconnaissance_2026-07-27.md`](evidence/solver_reconnaissance_2026-07-27.md):
  the completed one-hour unrestricted forced-trace CP-SAT `UNKNOWN` result and
  scope-explicit snapshots of the remaining live searches and the two
  proof-writing runs stopped without verdict for disk safety.
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
python3 -B collaboration/global_construction_attack/verify_maximal_minor_p7mod8_closure.py
python3 -B collaboration/infinity_layer_theorem/verify_infinity_layer_theorem.py
python3 -B collaboration/full_layer_augmentation/verify_full_layer_augmentation.py
python3 -B collaboration/global_h_parity/verify_global_h_parity.py
/opt/homebrew/bin/python3 -B \
  collaboration/finite_total_identity/verify_finite_total_identity.py
python3 -B collaboration/layer_sign_xor_cuts/verify_layer_sign_xor_cuts.py
python3 -B collaboration/cross_root_layer_sign/verify_cross_root_layer_sign.py
python3 -B \
  collaboration/multi_plucker_construction/verify_grassmann_line_ratio_no_go.py
python3 -B collaboration/opus5/rank4_plucker_ratio/verify_rank4_ratio.py
python3 -B collaboration/rank4_plucker_ratio/verify_rank4_plucker_ratio.py
python3 -B \
  collaboration/triangle_monodromy_spectrum/verify_triangle_monodromy_spectrum.py
python3 -B \
  collaboration/schreier_spectrum_obstruction/verify_schreier_spectrum_obstruction.py
python3 -B \
  collaboration/schreier_krein_followup/verify_schreier_krein_followup.py
python3 -B \
  collaboration/schreier_h3_support/verify_schreier_h3_support.py
python3 -B \
  collaboration/h3_state_refinement/verify_h3_state_refinement.py
python3 -B \
  collaboration/schreier_h3_triple_profiles/verify_schreier_h3_triple_profiles.py
python3 -B \
  collaboration/corrected_triple_profile_lp/verify_corrected_triple_profile_lp.py
python3 -B \
  collaboration/h3_delta_rank_attack/verify_h3_delta_rank_attack.py
python3 -B \
  collaboration/schreier_h4_support/verify_schreier_h4_support.py
python3 -B \
  collaboration/opus5/joint_schreier_krein_attack/verify_joint_schreier_krein_attack.py
python3 -B \
  collaboration/general_h1_rigidity/verify_general_h1_rigidity.py
python3 -B \
  collaboration/general_h2_rigidity/verify_general_h2_rigidity.py
python3 -B \
  collaboration/opus5/staircase_support_frontier/verify_staircase_support_frontier.py
python3 -B \
  collaboration/steiner_disjoint_matching/verify_steiner_disjoint_matching.py
python3 -B \
  collaboration/h3_intersection_cover_audit/verify_intersection_cover_audit.py
python3 -B collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py
python3 -B \
  collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py --k6
python3 -B \
  collaboration/fable_hadamard_kernel/verify_layer_capacity_facts.py
python3 -B \
  collaboration/opus5/hadamard_kernel_followup/verify_frame_and_clique.py
python3 -B \
  collaboration/opus5/hadamard_kernel_followup/verify_k6_kernel.py
python3 -B \
  collaboration/schur_product_literature/verify_literature_hypotheses.py
python3 -B \
  collaboration/opus5/post_spectrum_kernel_synthesis/verify_spectrum_moments.py
python3 -B \
  collaboration/opus5/post_spectrum_kernel_synthesis/verify_derived_capacity_control.py
python3 -B \
  collaboration/global_frame_moment_attack/verify_global_frame_moment_no_go.py
python3 -B \
  collaboration/global_frame_moment_attack/verify_k6_lambda3_witness.py
python3 -B collaboration/opus5/full_n_sign/verify_full_n_sign.py
python3 -B collaboration/fable_sign_head/verify_sign_head.py
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
python3 -B \
  collaboration/critical_group_cover_obstruction/verify_critical_group_cover_obstruction.py
python3 -B \
  collaboration/f17_additive_syndrome_k34/verify_f17_additive_syndrome_k34.py
python3 -B \
  collaboration/eh_residual_odd_cycle/verify_eh_residual_odd_cycle.py
python3 -B \
  collaboration/eh_core_symmetry_orbits/verify_eh_core_symmetry_orbits.py
python3 -B \
  collaboration/eh_j5_repair_search/screen_pair_links.py
python3 -B \
  collaboration/eh_j5_repair_search/verify_pair_links_direct.py
python3 -B \
  collaboration/opus5/large_set_completion_colouring/verify_large_set_completion_colouring.py
python3 -B \
  collaboration/eh_point_link_screen/verify_point_link_certificate.py \
  --drat-trim /path/to/drat-trim
python3 -B \
  collaboration/eh_point_link_screen/verify_all_455_coverage.py \
  --batch-recon collaboration/eh_point_link_screen/remaining_423_point0_recon.jsonl \
  --batch-manifest collaboration/eh_point_link_screen/remaining_423_point0_certificate_manifest.jsonl \
  --batch-base-dir collaboration/eh_point_link_screen \
  --drat-trim /path/to/drat-trim \
  --receipt collaboration/eh_point_link_screen/all_455_point0_theorem_receipt.json
python3 -B \
  collaboration/eh_point_link_screen/verify_drop_four_sample.py \
  --results collaboration/eh_point_link_screen/drop_four_point0_sample_recon.jsonl \
  --receipt collaboration/eh_point_link_screen/drop_four_point0_sample_receipt.json
python3 -B \
  collaboration/opus5/derivation_tower_obstruction/verify_derivation_tower_obstruction.py
python3 -B \
  collaboration/opus5/cyclic_lsts19_extension_attack/verify_cyclic_lsts19_extension_attack.py
python3 -B collaboration/opus5/unrestricted_ls3420_attack_2/verify_star_sign.py
python3 -B evidence/verify_holonomy_group_algebra_tower.py
python3 -B collaboration/opus5/holonomy_followup/verify_holonomy_followup.py
python3 -B collaboration/h3_holonomy_audit/verify_holonomy_audit.py \
  --full --affine-only
python3 -B collaboration/fan_small_controls/verify_all_k6_links.py
python3 -B collaboration/fan_small_controls/verify_k6_fan_certificate.py
python3 -B \
  collaboration/h3_simultaneous_fan_attack_2/verify_fan_kernel_reduction.py
python3 -B \
  collaboration/unrestricted_lift_tower/verify_unrestricted_lift_tower.py
python3 -B \
  collaboration/high_lift_complement_decomposition/verify_high_lift_complements.py
python3 -B \
  collaboration/high_lift_complement_decomposition/enumerate_r3_small.py \
  --max-n 7
python3 -B \
  collaboration/high_lift_top_properness/verify_j12_top_properness.py
python3 -B \
  collaboration/high_lift_top_properness/verify_j11_top_properness.py
python3 -B \
  collaboration/high_lift_top_properness/verify_j10_top_properness.py
python3 -B \
  collaboration/h3_j9_top_properness_audit/verify_j9_top_properness.py
python3 -B \
  collaboration/j9_integer_weight_lemma/verify_arithmetic.py
python3 -B \
  collaboration/h3_j8_exact_trade_elimination/verify_j8_exact_trade_elimination.py
python3 -B \
  collaboration/h3_j8_n0_outside_s5/verify_model.py
python3 -B \
  collaboration/h3_j8_n0_outside_s4_boundary/verify_model.py
python3 -B \
  collaboration/h3_j8_n0_outside_s4_boundary/search_cp_sat_reduced.py \
  --seconds 60 --workers 1 --reference-positive 13 \
  --reference-weight-two 10
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support8.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_compact.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_remaining.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_remaining_221_coeff2.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_remaining_221_unit.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_remaining_2111.py
python3 -B \
  collaboration/fan_gadget_generalization/verify_cyclic_support10_remaining_11111.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_partial.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case222.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case3111.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case321.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case2211.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case21111.py
python3 -B \
  collaboration/fan_gadget_generalization/support12_attack/verify_case111111.py
python3 -B \
  collaboration/fan_13adic_screen/branch0_prefix1_refutation/verify_prefix_refutation.py
python3 -B \
  collaboration/fan_13adic_screen/c17_layer_scan_1326/verify_scan_telemetry.py
python3 -B \
  collaboration/fan_13adic_screen/finite_first_packing_132/verify_finite_packing_132.py
python3 -B \
  collaboration/first_lift_support_completion/verify_capacity_lemma.py
python3 -B \
  collaboration/first_lift_sufficiency_search/exhaust_n5_capacity.py
python3 -B \
  collaboration/first_lift_sufficiency_search/audit_kempe_switch.py
python3 -B \
  collaboration/first_lift_sufficiency_search/audit_kempe_n5_connectivity.py
python3 -B \
  collaboration/first_lift_sufficiency_search/search_weighted_obstruction.py \
  --random 30 --seed 130835 --max-weight 100 --seconds 10 --q 0
python3 -B \
  collaboration/opus5/first_lift_k13_hole/verify_first_lift_obstruction.py
python3 -B \
  collaboration/opus5/first_lift_classB_attack/verify_classB.py
python3 -B \
  collaboration/first_lift_partial_factorization_audit/verify_boundary.py
python3 -B \
  collaboration/first_lift_dense_support_prefix/verify_prefix_criteria.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_dead_prefix.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_propagation_counterexample.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_eighth_matching_core_catalogue.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_twelve_support_switching.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_r0_core_pairs.py
python3 -B \
  collaboration/first_lift_global_theorem/verify_r0_row_sum_core_elimination.py
python3 -B \
  collaboration/r0_three_family_helly_gate/verify_global_counterexample.py
python3 -B \
  collaboration/opus5_r0_orbit_repair/check_crossing_hall.py
python3 -B \
  collaboration/coordinated_nine_r0_repair_cegis/search_one_layer_repair.py \
  --max-rounds 2 --cuts-per-model 2
python3 -B \
  collaboration/first_lift_aggregate_graphicity/verify_aggregate_graphicity.py
python3 -B collaboration/opus5/unrestricted_ls3420_attack_2/second_star_split.py
python3 -B \
  collaboration/opus5/unrestricted_ls3420_attack_2/verify_solution.py \
  8 3 7 collaboration/opus5/unrestricted_ls3420_attack_2/controls/j8_3_m7.model
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
- [Latest official/X status audit, 28 July 2026](collaboration/recent_solution_check_2026-07-28.md)
- [Recent official/X status audit, 27 July 2026](evidence/recent_status_audit_2026-07-27.md)
- J. Ma and Q. Tang,
  [A Note on Erdős Problem #835](https://github.com/QuanyuTang/erdos-problem-835/blob/main/On_Problem_835.pdf)
- P. Hammond and D. H. Smith,
  [Perfect codes in the graphs \(O_k\)](https://doi.org/10.1016/0095-8956(75)90087-8)
- E. Kolotoğlu and S. S. Magliveras,
  [On the possible automorphism groups of a Steiner quintuple system of
  order 21](https://doi.org/10.1002/jcd.21370)

Additional references are listed in the main note.
