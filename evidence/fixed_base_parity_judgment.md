# The fixed-base parity conjecture: exact status (2026-07-24)

Labels: **Proved** (complete proof here or cited), **Verified** (finite exact
computation, script named), **Refuted** (explicit certificate), **Tautology**
(restatement with zero leverage), **Conjectural** (open).

Setting: \(r\) odd, \(v=2r+1\), \(A\) an \(S(r-1,r,v)\),
\(b=\binom vr/(r+2)\), \(W=W_{r-1,r}(v)\) the facet–block inclusion matrix,
\(\mathcal D(A)\) the set of \(S(r-1,r,v)\) block-disjoint from \(A\).

> **Conjecture P.** For all \(B,C\in\mathcal D(A)\):
> \(|B\cap C|\equiv b \pmod 2\).

Force: \(b\) is odd exactly at \(r\in\{3,15\}\) in the accessible family, so
P at \(r=15\) would give \(B\cap C\neq\emptyset\), i.e. no three pairwise
disjoint \(S(14,15,31)\): the first open case of Erdős 835 resolved
negatively (and \(\chi(J(32,16))\ge18\)).

Scripts: `verify_fixed_base_parity.py`, `verify_shaped_kernel_parity.py`,
`verify_r5_odd_witness.py` (this directory; stdlib except one optional
CP-SAT search; all recorded results re-verified in exact arithmetic).

## 1. Sphere encoding (Proved)

From \(n_0=1-[K\in\mathcal D]\) (three_way_trade.md (2.2)/(2.3)):

* (a) Every \(r\)-set \(K\notin A\) is uniquely \(K=X\setminus(P\cup\{p\})\),
  \(P\in A\), \(p\notin P\).  Write \(K=K(P,p)\); the **sphere** \(S_P\) is
  \(\{K(P,p):p\notin P\}\), of size \(r+1\).
* (b) Every \(B\in\mathcal D(A)\) meets every sphere exactly once (apply
  \(n_0=1\) to the system \(B\) and the \(r\)-set \(P\notin B\)).  So \(B\)
  is exactly a **mate map** \(\varphi_B:A\to X\), \(\varphi_B(P)\notin P\),
  which is additionally Steiner.
* (c) \(|B\cap C|=\#\{P:\varphi_B(P)=\varphi_C(P)\}\); write
  \(\delta=b-|B\cap C|\) for the number of disagreeing spheres.
* (d) **Every \((r+2)\)-set contains exactly \((r+1)/2\) blocks of \(A\).**
  Proof: the number of blocks avoiding an \((r-1)\)-set is
  \(\sum_{j\le r-1}(-1)^j\binom{r-1}j\lambda_j\), a constant; double count
  \((P,Y)\), \(P\subseteq Y\), \(|Y|=r+2\):
  \(m=b\binom{r+1}2/\binom v{r-1}=(r+1)/2\).
  (Verified: 2 per 5-set at \(r=3\), 3 per 7-set at \(r=5\), all sets.)
  Consequently each facet \(F\) couples the \((r+1)/2\) spheres
  \(P\subseteq Y=X\setminus F\) through two coordinates each:
  \(\sum_{P\subseteq Y}\big(z_{(P,q_1)}+z_{(P,q_2)}\big)=0\),
  \(\{q_1,q_2\}=Y\setminus P\).

## 2. Tautology audit (Tautology, all three)

* **T1.** For \(B,C\in\mathcal D(A)\),
  \(\operatorname{wt}(x_B-x_C)=2\delta\).  So "mate-differences have weight
  divisible by 4" \(\iff\delta\) even \(\iff\) Conjecture P — at **every**
  odd \(r\).  The clause "for \(r\equiv3\pmod4\)" is irrelevant to this
  equivalence; \(r\bmod4\) only decides whether \(b\) is odd (whether the
  parity has killing power).  As posed, the weight question is P restated.
* **T2.** \(\langle x_B-x_A,\,x_C-x_A\rangle=|B\cap C|+b\) identically;
  asking for its evenness is again P.
* **T3.** For \(u=x_B+x_C\) (mod 2), the facet-sharing-pair count of
  fable_trade_quadratic Lemma 4 collapses exactly:
  \(I_{r-1}(B\setminus C,\,C\setminus B)=r\delta\) (each block of
  \(B\setminus C\) has \(r\) facets; the \(C\)-block at such a facet differs
  and meets it in exactly that facet; the correspondence facet
  \(\leftrightarrow\) pair is bijective).  The \(N_2\)-parity identity
  returns \(\delta\equiv\delta\): no leverage for P from that route.

## 3. Complete verification of P at r=3 and r=5 (Verified)

* \(r=3\) (`verify_fixed_base_parity.py`): all 30 Fano planes; fixed \(A\);
  \(|\mathcal D(A)|=8\); all 28 pairs have \(|B\cap C|=1\equiv b=7\).
  Complete (previously known; three_way_trade.md §5).
* \(r=5\): \(|\mathcal D(A)|=144\) (all mates enumerated by exhaustive exact
  cover); all \(\binom{144}2=10296\) pairs:
  \(|B\cap C|\in\{6\ (6336\ \text{pairs}),\ 18\ (3960\ \text{pairs})\}\) —
  all even \(=b=66\pmod2\).  Repeated for a second base (a mate of \(A\));
  identical distribution.  Complete for **every** base by uniqueness of
  \(S(4,5,11)\) up to relabelling (Witt; literature dependency) since P is
  label-invariant.  The sampled values 6/18 are in fact the whole spectrum.

So P has no counterexample at any testable parameter.  \(r=7,11,13\) are
parameter-empty; \(r=9\) needs an \(S(8,9,19)\) (existence open);
\(r=15\) needs a first \(S(14,15,31)\).

> **Correction, 2026-07-26.**  The \(r=9\) entry is settled negatively, so
> "existence open" is wrong.  Deriving \(S(8,9,19)\) at a \(4\)-set gives
> \(S(4,5,15)\), which does not exist (Mendelsohn–Hung, 1972).  Hence no
> \(S(8,9,19)\) exists and \(r=9\) is parameter-empty too.  The accessible
> list is therefore \(r\in\{3,5\}\) testable, \(r=15\) open — \(r=15\)
> surviving because the same derivation lands on \(S(4,5,21)\), the smallest
> \(S(4,5,v)\) of unknown existence.  See
> `triangle_closure_derived_reduction.md` §3b.

## 4. A lattice proof of P at r=3 (Proved, new)

Let \(\Lambda(A)=\{z\in\mathbb Z^{\text{non-}A\text{ blocks}}:\ Wz=0,\ \text{all
sphere sums }0\}\).  At \(r=3\) (any Fano \(A\); they are all equivalent):
\(\dim\Lambda=7\), and an explicit basis (computed by unimodular column
reduction, hence exactly saturating the kernel; basis re-verified in the
script) has **all norms \(\equiv0\bmod4\) and all pairwise inner products
even**.  Hence \(z\cdot z\equiv0\pmod 4\) for every \(z\in\Lambda\): the
lattice is 4-even.  Any difference \(z=x_B-x_C\), \(B,C\in\mathcal D(A)\),
lies in \(\Lambda\) with \(z\cdot z=2\delta\); so \(\delta\) is even and
\(|B\cap C|\) is odd.  This proves P at \(r=3\) from a 7-vector certificate,
independent of enumerating \(\mathcal D(A)\).

Exhaustive structure at \(r=3\): the shaped vectors of \(\Lambda\) (one
\(+1\), one \(-1\) per active sphere) number 112 nonzero; exactly 56 are
ordered Steiner differences and 56 are not; every one is active on exactly
the six spheres avoiding a single block.  The GF(2)-shaped class also has
active count 6 only (448 nonzero words).

## 5. The relaxation is FALSE at r=5 (Refuted)

`verify_r5_odd_witness.py` records a shaped vector \(z\) for the
deterministic base \(S(4,5,11)\): one \(+1\) and one \(-1\) in each of
**49** spheres, \(Wz=0\) verified over \(\mathbb Z\) on all 330 facets,
norm \(98\equiv2\pmod4\).  A GF(2)-shaped word with 47 active spheres also
exists (CP-SAT).  Consequences:

* \(\Lambda(A)\) is **not** 4-even at \(r=5\); no linear or lattice argument
  on \(\{Wz=0+\text{sphere shape}\}\) can prove P at \(r=5\).
* Since P nevertheless **holds** at \(r=5\) (complete check, §3), its truth
  there lives strictly on the nonlinear Steiner slice (both endpoints with
  every facet-degree exactly one) — the same phenomenon as the failure of
  pair-code self-orthogonality at \(r=5\) (fable_trade_quadratic, Data).
* CP-SAT side results (solver-certified only): no shaped kernel vector with
  exactly 2, 4, or 6 active spheres at \(r=5\).

**Conjecture E (Conjectural; the exact linear statement left open).**  For
\(r\equiv3\pmod4\) and every \(S(r-1,r,2r+1)\) base \(A\), the lattice
\(\Lambda(A)\) is 4-even.  E implies P at \(r\in\{3,15\}\), hence the
negative resolution of the first open Erdős 835 case.  Evidence: true at
\(r=3\); false at \(r=5\equiv1\); untestable at \(r=15\) without a first
\(S(14,15,31)\).  Epistemically parallel to Conjecture D
(fable_trade_quadratic): an \(r\bmod4\) dichotomy resting on the single
data point \(r=3\).

## 6. Dead end: rowspace membership (Refuted)

Sufficient condition considered: \(x_A+x_B\in\operatorname{rowspace}_2 W\)
for a disjoint pair \((A,B)\) — this would give
\(\langle x_A+x_B,\,x_A+x_C\rangle=0=b+|B\cap C|\) for **all**
\(C\in\mathcal D(A)\) at once, since \(x_A+x_C\in\ker_2W\).  Refuted:

* \(r=3\): \(\operatorname{rank}_2W=15\), \(\dim\ker_2W=20\),
  \(\dim(\text{rowspace}\cap\ker)=0\) — membership is structurally
  impossible for any nonzero kernel vector; all 8 disjoint pairs fail.
* \(r=5\): \(\operatorname{rank}_2W=210\); all 144 mate pairs fail, both
  bases; 300 permuted non-disjoint controls fail at every intersection size.

So the pairwise orthogonality \(\langle x_A+x_B,x_A+x_C\rangle=0\) that P
asserts is **not** explained by orthogonality to the whole kernel; the
vectors \(\{x_A+x_B\}\) form a self-orthogonal set inside \(\ker_2W\)
without lying in \((\ker_2W)^\perp\).

## 7. The sign route: exact content and caveat

Fix \(B\in\mathcal D(A)\), \(P\in A\).

**Lemma 3 (Proved).**  The map \(\pi_P^B:P\cup\{*\}\to X\setminus P\) with
\(\pi_P^B(x)=y\) where \((P\setminus\{x\})\cup\{y\}\in B\), and
\(\pi_P^B(*)=\varphi_B(P)\), is a well-defined bijection.  (Uniqueness and
\(y\notin P\) from Steinerness of \(B\) and \(A\cap B=\emptyset\); injectivity
among facet slots since two hits would force two \(B\)-blocks sharing an
\((r-1)\)-set; \(*\) separated since a hit would force two disjoint
\(B\)-blocks, impossible as \(n_0=0\) inside a system.)

**Lemma 4 (Proved; the tautological part of the route).**  With any fixed
reference orderings, \(\sigma_P(B,C):=\operatorname{sign}\big((\pi_P^C)^{-1}
\pi_P^B\big)\) factors as \(\varepsilon_P(B)\varepsilon_P(C)\); hence
\(\prod_P\sigma_P(B,C)=E(B)E(C)\) with
\(E(B):=\prod_P\operatorname{sign}(\pi_P^B)\).  "The product is \(+1\) on
all pairs" is **equivalent** to "\(E\) is constant on \(\mathcal D(A)\)";
the product form itself carries no content.

**Lemma 5 (Proved).**  Let \(\tau=\bigoplus_P(\pi_P^C)^{-1}\pi_P^B\).  Then
\(\tau\) has exactly \((r+1)|B\cap C|\) fixed points (slot agreements are
precisely shared-block incidences), and, \(r+1\) being even,
\(\operatorname{sign}(\tau)=(-1)^{\Gamma'}\) where \(\Gamma'\) is the number
of nontrivial local alternating cycles.  Hence the proposed identity
\(\prod_P\sigma_P=(-1)^{\,b-|B\cap C|}\) is equivalent to
\(\Gamma'\equiv\delta\pmod2\) (call it Q1), and \(E\)-constancy to
"\(\Gamma'\) always even" (Q2).  Q1 \(\wedge\) Q2 \(\Rightarrow\) P.

**Verified.**  \(r=3\): all 28 pairs; \(r=5\): all \(2\times10296\) pairs:
\(E\) is constant on \(\mathcal D(A)\) (values \(-1\) at \(r=3\), \(+1\) at
\(r=5\) under one fixed convention — only constancy is invariant),
\(\operatorname{sign}(\tau)=+1\) always, and the fixed-point and cycle
identities of Lemma 5 hold on every pair tested.

**Caveat (decisive).**  On every accessible instance P holds, so
\((-1)^{b-|B\cap C|}=+1\) and both Q1 and Q2 reduce to the same observable
"\(\Gamma'\) even".  The computations above **cannot** distinguish the
identity Q1 from its trivial truth on parity-conforming pairs; a genuine
test of Q1 needs a pair with \(\delta\) odd, which P says does not exist.
The observed "+1 products" are exactly the observed conjecture — zero
independent evidence for Q1 as an identity.  Both Q1 and Q2 are open;
their conjunction implies P, and P implies they are equivalent.

**Lemma 6 (Proved; the invariant content of \(E\)).**  For a non-\(A\)
block \(\kappa\): each facet \(\kappa\setminus\{w\}\) extends to a unique
\(A\)-block \(g_\kappa(w)=(\kappa\setminus\{w\})\cup\{x_\kappa(w)\}\) with
\(x_\kappa(w)\notin\kappa\); together with the mate sphere
(\(w=p_\kappa\), slot \(*\)) this gives \(r+1\) incidences with distinct
spheres, all determined by \((A,\kappa)\) alone.  Set, in the exterior
algebra on \(\mathbb R^{V}\oplus\mathbb R^{\Omega}\) (sphere-content
coordinates \(V\), slot coordinates \(\Omega\)),
\[u_\kappa=\Big(\textstyle\bigwedge_w e_{(g_\kappa(w),\,w)}\Big)\wedge
\Big(\textstyle\bigwedge_w f_{(g_\kappa(w),\,x_\kappa(w))}\Big),\]
a monomial of even degree \(2(r+1)\); all \(u_\kappa\) commute.  For every
\(B\in\mathcal D(A)\) the content labels sweep \(V\) once and the slot
labels sweep \(\Omega\) once (Lemma 3), and
\[\prod_{\kappa\in B}u_\kappa\;=\;E(B)\cdot\Omega_V\wedge\Omega_\Omega.\]
So \(E\)-constancy says: the (unordered, block-local) Grassmann product of
\(u_\kappa\) over a Steiner selection does not depend on the selection.
This is the cleanest formulation available for attacking Q2.

## 8. Verdict

* Conjecture P: **open**; completely verified at \(r=3\) and \(r=5\)
  (the only testable parameters); proved at \(r=3\) by the 4-even lattice
  certificate (§4).
* The mod-4 weight question as posed: a tautological restatement of P
  (T1).  Its honest non-tautological sharpening is Conjecture E (§5),
  which is refuted at \(r=5\) and therefore can only survive as an
  \(r\equiv3\pmod4\) dichotomy claim with \(r=3\) as sole support.
* The sign identity: automatic in its product form (Lemma 4); as an
  identity it is exactly \(\Gamma'\equiv\delta\pmod2\), unproved, and
  untestable beyond parity-conforming pairs; \(E\)-constancy is unproved
  and is the actual content of the observed "+1".
* Any proof of P valid at \(r=5\) must use the Steiner property of both
  \(B\) and \(C\) (all linear/lattice/GF(2) relaxations fail there by
  explicit certificate).  The most informative feasible next step is a
  structural (non-enumerative) proof of P at \(r=5\), e.g. through the
  \(M_{11}\) action, to expose a mechanism that survives the loss of
  linearity.
