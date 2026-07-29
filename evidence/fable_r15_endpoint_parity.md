# Endpoint parity at r=15: status, reductions, and the exact gap

Question (Conjecture E at \(r=15\)): for two mates \(B,C\) of a fixed
\(S(14,15,31)\) leg \(A\), is
\(t=|\Delta|=\#\{P\in A: w_B(P)\ne w_C(P)\}\) always even?
Since \(b=17\,678\,835\) is odd, this is equivalent to
\(|B\cap C|\equiv b\pmod2\), and it implies that no two mates are
disjoint, hence no \(LS(14,15,31)\) and \(\chi(J(32,16))\ge18\).

Labels: **PROVED** (complete proof), **FINITE-VERIFIED** (exhaustive
finite computation, validator recorded), **CONJECTURAL** / **GAP**.

## 1. PROVED reductions

**1.1 Tiling characterization of mates.**  Mates \(B\) of \(A\)
correspond exactly to maps \(w:A\to[2r+1]\), \(w(P)\notin P\), whose
16-sets \(H_w(P)=P\cup\{w(P)\}\) contain-exactly-one in every
\((r+2)\)-set: \(B\) Steiner \(\iff\) each facet \(f\) has one
\(B\)-block through it \(\iff\) each \(Z=f^c\) contains exactly one
\(H\).  Explicitly, the \(B\)-block associated to \(H\) is
\([2r+1]\setminus H\), and
\([2r+1]\setminus H\supseteq f\iff H\subseteq[2r+1]\setminus f\).

**1.2 The \((r{+}1)/2\)-law.**  Every \((r+2)\)-set contains exactly
\((r+1)/2\) blocks of \(A\) (8 at \(r=15\)).  Proof: the number of
blocks avoiding a facet is an alternating sum of the design numbers
\(\lambda_i\), hence constant; the average
\(b\binom{r+1}2/(rb)=(r+1)/2\) fixes it.
FINITE-VERIFIED: \(\{2{:}21\}\) at \(r=3\), \(\{3{:}330\}\) at
\(r=5\).

**1.3 Fibre-transversal normal form.**  By 1.1–1.2, mates of \(A\) are
exactly the transversals (one extension \(H\)-column from each
\(A\)-block's fibre of \(v-r\) extensions) covering each of the \(rb\)
\((r+2)\)-set rows exactly once, where each row meets \((r+1)/2\)
fibres in 2 columns each and each column lies in \(r\) rows.  At
\(r=3\) the row–fibre incidence is \(K_7\) and the constraint per edge
\(\{i,j\}\) is \([w_i\in A_{ij}]+[w_j\in A_{ji}]=1\) with
\(|A_{ij}|=2\).

**1.4 Difference vectors and mod 4.**  For two mates,
\(u=\sum_{P\in\Delta}(e_{H_B(P)}+e_{H_C(P)})\) lies in
\(\ker_2\) of the \((r+2)\)-by-\((r+1)\)-set incidence, has weight
\(2t\), and weight \(0\) or \(2\) on each fibre; \(t\) even
\(\iff\operatorname{wt}(u)\equiv0\pmod4\).

**1.5 Doubly-even routes fail.**  The full kernel at level
\((16,17)\) has dimension \(155\,117\,520>145\,422\,675=\)rank, so it
is not self-orthogonal.  The restricted code \(K_A\) (columns with an
\(A\)-block) is an even code but NOT self-orthogonal already at
\(r=3\) (dim 13) and \(r=5\) (dim 186) — FINITE-VERIFIED — although
every actual tiling difference has \(\operatorname{wt}\equiv0\pmod4\)
(28/28 and 10\,296/10\,296).  Hence no ambient-code 4-divisibility
argument can prove E; the tiling subclass is strictly special.

## 2. PROVED gap: shape axioms do not imply parity

**Layer 1.**  There exists an explicit abstract system with the full
\(r=3\) shape — \(K_7\) row–fibre incidence, \(|A_{ij}|=2\), every
fibre element of column weight \(r=3\) — admitting two transversal
solutions at fibre-distance **1** (odd).  (Witness hardcoded and
re-verified directly in `verify_endpoint_parity_gap.py`.)  Hence
\{shape axioms\}
\(\not\vdash\) parity.  The witness has two fibre elements with
identical membership patterns, which the real system forbids (at
\(r=3\) an extension point's pattern is its line pencil; pencils
separate points), and distance 1 also violates the real
configuration-graph simplicity bound \(t\ge r-1=2\)
(\(t\ge14\) at \(r=15\)).

**Layer 2.**  Adding element-distinguishability (all four patterns in
each fibre distinct) still admits odd distances.  An explicit witness
(hardcoded and verified directly in the validator — no randomized
replay): a distinguishable system with exactly two transversal covers,
at fibre-distance **7** \(=b\) (odd).  Hence
\{shape + distinguishability\} \(\not\vdash\) parity.

**Exact gap statement (PROVED by the above).**  Any proof of E must
use constraints beyond the local fibre/row shape and element
distinguishability.  Necessary constraints absent from those abstract
models include the point-identification facts: fibre elements are points of
\([2r+1]\) shared across fibres, with (i) \(w\)-uniformity (each point
is chosen by exactly \(b/v\) fibres in any single tiling — a global
coherence the abstract models violate), (ii) coherent \(A_{ij}\)
geometry (\(A_{ij}=Z\setminus P_i\) with \(Z=P_i\cup P_j\)), and
(iii) configuration-graph simplicity (\(t=0\) or \(t\ge r-1\)).

## 2.5 Layer 3: point identification is categorical at the r=3 scale

Encoded constraints, each PROVED to be a necessary consequence of a
real Steiner mate system:
(N1) the fibre index family is the block set of \(A\); two fibres
co-occur in an \((r+2)\)-row exactly when their blocks intersect in
\(r-2\) points.  At \(r=3\), the boundary no-disjointness law and the
Steiner intersection bound force every pair of distinct blocks to meet
in exactly one point;
(N2) fibre elements are the points of \([2r+1]\setminus B_i\) and
\(A_{ij}=B_j\setminus B_i\) (definitional);
(N3) solutions are \(H\)-tilings: every \((r+2)\)-set contains exactly
one \(B_i\cup\{w(i)\}\) (the mate characterization, §1.1);
(N4) solutions are bijections onto points at \(r=3\) (uniformity
theorem, \(b/v=1\)).

**Categorical theorem (FINITE-VERIFIED, exhaustive).**  Every family
of 7 distinct triples on \([7]\) pairwise intersecting in exactly one
point is a Fano plane (all 30 such families are Steiner, replication-3,
2-law); each admits exactly 8 tiling solutions (the mates), and no two
solutions are at odd fibre-distance (all distances are 6).  Validator:
`layer3_categorical()`.

**Interpretation (exact scope).**  At the \(r=3\) scale, Layer-3
point identification admits NO abstract instances beyond real Steiner
systems, so it cannot discriminate whether the point-identification
constraints *prove* parity or merely inherit it from Fano rigidity.
The discriminating experiment lives at the \(r=5\) scale: a
point-identified family of 66 five-blocks on \([11]\) satisfying
(N1)–(N4)-analogues without being an \(S(4,5,11)\), admitting two
tilings at odd distance — existence open, search expensive
(CONJECTURAL territory; formulated here precisely for the next
session).

## 2.6 The r=5 discrimination SAT (formulation and necessity proofs)

Model: `layer3_r5_sat.py`.  Search for 66 distinct 5-blocks on
\([11]\) and two tilings at odd fibre-distance, under exactly these
constraints, each PROVED necessary for a real \(S(4,5,11)\) mate
system:

- **(N1a)** pairwise \(|B_i\cap B_j|\in\{1,2,3\}\).  *Necessity:*
  distinct blocks of a Steiner system with \(t=4\) share at most
  \(t-1=3\) points; the intra-distribution (2.3) of the boundary
  family gives \(n_0=0\), excluding intersection 0.
- **(N1b)** every point in exactly 30 blocks.  *Necessity:*
  \(\lambda_1=\binom{10}{3}/\binom43=30\) for \(S(4,5,11)\).
- **(N1c)** every 7-set contains exactly 3 blocks.  *Necessity:* the
  \((r{+}1)/2\)-law (§1.2).
- **(N3)** every 7-set contains exactly one \(H_i=B_i\cup\{w(i)\}\).
  *Necessity:* the tiling characterization (§1.1).
- **(N4)** each tiling is 6-uniform (each point chosen by exactly
  \(b/v=6\) fibres).  *Necessity:* the uniformity theorem.

Deliberately NOT encoded: \(\lambda_2=12\) and \(\lambda_3=4\),
because with (N1a), \(\lambda_3=4\) already forces \(\lambda_4=1\)
(each 3-set has 8 extensions to 4-sets, its 4 blocks cover 2 each,
pairwise-\(\le3\) makes the coverage disjoint), i.e. full
Steinerness — the relaxation would collapse and the experiment would
be vacuous.  Whether \{N1a, N1b, N1c\} alone force Steinerness at
\(r=5\) is OPEN (the analogous set at \(r=3\) is categorical); the
counting system relating \(n_2(T),n_3(T)\) to \(\lambda_4(T)\) via
\(105-15\lambda_4(T)=5n_3(T)+n_2(T)\) is underdetermined without
\(\lambda_3\), so no collapse proof is available — and no
countermodel either.

Protocol: FEASIBLE \(\Rightarrow\) witness materialized and verified
by the pure-python `check_witness` (no solver dependence).
INFEASIBLE \(\Rightarrow\) CP-SAT emits no portable certificate, so
the outcome is recorded as UNKNOWN\(^*\) (uncertified claim) unless a
certifying pipeline is added.  Timeout \(\Rightarrow\) UNKNOWN.  In no
case does a small-scale UNSAT license the \(r=15\) parity theorem.

**Run log.**  2026-07-25, single worker (per the concurrent
210-anchor certificate's CPU reservation): 20 s smoke UNKNOWN
(presolve); 1800.3 s probe UNKNOWN after 1,894,897 branches.  This is
a timeout, not an infeasibility result or a certificate.

**Symbolic lift prospects (CONJECTURAL).**  All five necessity proofs
are general-\(r\); so if the discrimination at \(r=5\) finds no
countermodel and a symbolic argument shows \{N-constraints\}
\(\Rightarrow\) parity for all boundary parameters, it lifts to
\(r=15\) verbatim.  The current obstacle is that the only proof
mechanisms known to force parity (the \(D_6\)-torsor) are
\(r=3\)-specific, and the only mechanisms known to fail (ambient
4-divisibility, Klein actions, local signs) are proved dead.  The
live symbolic candidates are: a free 4-divisible group action on
configurations built from (N3)–(N4), or a mod-4 invariant of the
fibration graph using (N1c).

## 2.7 Full fibration census, spectator structure, and the screen

**Generic screen (PROVED).**  Connectivity cannot be the mechanism:
for any \(d=r-1\) and any \(t>d\), the circulant bipartite graph
joining \(x_L\) to \((x+s)_R\), \(s=0,\dots,d-1\), on two copies of
\(\mathbb Z/t\mathbb Z\) is simple, \(d\)-regular and connected, with
\(t\) odd allowed.  So \{connected + \((r-1)\)-regular bipartite\}
\(\not\vdash\) parity; a symbolic invariant must use N1c/N3/N4.

**Spectator lemma (PROVED).**  For \(r\ge5\), every split
\((r+2)\)-set \(Z\) contains, besides its two bases, exactly
\((r+1)/2-2\) further \(A\)-blocks (one at \(r=5\), six at
\(r=15\)), and each such spectator \(S\) has both \(w_B(S)\) and
\(w_C(S)\) outside \(Z\) — otherwise \(Z\) would contain a second
\(H_B\) or \(H_C\), violating the tiling.  This structure vanishes at
\(r=3\) (no spectators), so it is invisible to all \(r=3\)
mechanisms.

**Full census (FINITE-VERIFIED, all 10\,296 unordered \(r=5\) mate
pairs; validator `verify_fibration_connectivity.py`).**  Every
fibration graph is simple, 4-regular, bipartite and CONNECTED.  The
pair \((t,\#\{\text{edges with spectator}\in\Delta\})\) takes exactly
four values, constant on each of the four mate-pair species and with
the same multiplicities as the \(\sigma\)-cycle-type classes:
\((48,106)\times3960\), \((60,180)\times792\),
\((60,200)\times1584\), \((60,210)\times3960\).  In particular the
spectator-in-\(\Delta\) edge count is EVEN in every instance — the
sharpest currently known invariant candidate derived from N1c.

**Exact status of the strengthened route.**  Connectivity alone:
insufficient (proved above).  Spectator evenness: FINITE-VERIFIED
only; no symbolic proof yet, and no derivation of "\(t\) even" from it
is known — the missing link would be an identity tying
\(\#\{\text{spec}\in\Delta\}\bmod2\) to \(t\bmod2\).  No countermodel
occurs among the real \(r=5\) mate pairs; whether one exists in the
strictly weaker N-axiom relaxation is the pending SAT question of
§2.6.  The route is OPEN, not closed.

## 2.8 The spectator double count: proved identities and t-blindness

Notation: \(m=(r+1)/2\); ordered pairs \((P,S)\) of distinct
\(A\)-blocks with \(|P\cap S|=r-2\); \(U_B=\#[w_B(P)\in S]\), with
superscripts \(\Delta\) restricting membership;
\(\Sigma_\gamma\) = Δ-content of crossed sets;
\(\Sigma_{\rm spec}\) = (split set, Δ-spectator) incidences.

**PROVED (validator `verify_spectator_congruence.py`, all 28 + 10\,296
pairs):**
- **I1** \(U_B=U_C=rb(m-1)\): group by \(Y=P\cup S\); each \(Y\) has
  exactly one \(B\)-base, and every other block of \(Y\) meets it in
  exactly \(r-2\) points.
- **I2** \([w_B(P)\in S\wedge w_B(S)\in P]\) never occurs (two
  \(H_B\)'s in one \((r+2)\)-set).
- **I3** \(U_B^\Delta=rt(m-1)\).
- **I4** \(U^{\Delta\Delta}=\Sigma_\gamma+(r-1)t+\Sigma_{\rm spec}\),
  and the same value results for \(B\) and \(C\)
  (\(U_B^{\Delta\Delta}=U_C^{\Delta\Delta}\), a nontrivial symmetry).

**t-blindness theorem (PROVED).**  Modulo 2 the identity I4 reads
\(\Sigma_{\rm spec}\equiv U^{\Delta\Delta}+\Sigma_\gamma\): the
\(t\)-term has even coefficient \(r-1\) for every odd \(r\), and the
only \(t\)-carrying first-moment identity (I3) is exact, hence mod-2
tautological.  Therefore **no first-moment spectator double count
yields a congruence with \(t\)**; the observed evenness of
\(\Sigma_{\rm spec}\) is equivalent to
\(U^{\Delta\Delta}\equiv\Sigma_\gamma\pmod2\), whose common parity is
\(r\)-dependent (both odd at \(r=3\): \(15,3\); both even in all four
\(r=5\) species: \(U^{\Delta\Delta}\in\{358,546,550,540\}\),
\(\Sigma_\gamma\in\{60,96,110,120\}\)) and is NOT determined by the
intersection numbers, tiling laws, uniformity, or the \(m\)-law.

**Exact residual gap.**  Any parity proof must produce a quantity in
which \(t\) appears with an ODD coefficient; in the entire first-moment
calculus above every \(t\)-coefficient is even.  The residual
undetermined datum is the parity pair
\((\Sigma_\gamma,U^{\Delta\Delta})\bmod2\) — only the sum is
constrained.  Species table (FINITE-VERIFIED, full data):
\((t,\Sigma_\gamma,U^{\Delta\Delta},\Sigma_{\rm spec})\) =
\((6,3,15,0)\) at \(r=3\); \((48,60,358,106)\times3960\),
\((60,96,546,210)\times3960\), \((60,110,550,200)\times1584\),
\((60,120,540,180)\times792\) at \(r=5\) — \(\Sigma_\gamma\) alone
separates all species.  Scope note: the Layer-1/2 abstract
countermodels do not define \((r+2)\)-sets, so I1–I4 are inapplicable
there (they require N1c + N3).

## 2.9 The second-moment identities and their parity tautology

Validator: `verify_M2_reduction.py` (all identities checked on every
mate pair at \(r=3,5\)).

**H-level law (PROVED).**  Every \((r+1+k)\)-set contains exactly
\(\binom{r+1+k}{r+2}/k\) H-sets of a tiling (group the exactly-one law
over its \((r+2)\)-subsets); in particular every \((r+3)\)-set contains
\(\mu=(r+3)/2\) of each tiling.

**Second-moment identity (PROVED).**  Expanding
\(\sum_Y(\#H_B\subseteq Y)(\#H_C\subseteq Y)=\mu^2\binom{2r+1}{r+3}\)
over ordered pairs and classifying by \(|H_B(P)\cup H_C(Q)|\):
\[
 M_2=\mu^2\tbinom{2r+1}{r+3}-b\tbinom r2-t\tbinom r2 ,
\]
where \(M_2=\#\{(P,Q):P\ne Q,\ |H_B(P)\cap H_C(Q)|=r-1\}\), and the
coefficient \(\binom r2\) of \(t\) is ODD iff \(r\equiv3\pmod4\) — the
odd-\(t\)-coefficient identity that the first-moment calculus provably
lacks.  Here is the complete multiplicity accounting.  Put \(h=b-t\).
The \(h\) diagonal pairs with \(H_B(P)=H_C(P)\) have union size
\(r+1\) and occur in \(\binom r2\) choices of \(Y\).  The \(t\)
remaining diagonal pairs have union size \(r+2\), as do the
\(X=(r-1)t\) off-diagonal crossed configurations from the fibre
lemma; each occurs in \(r-1\) choices of \(Y\).  Every pair counted by
\(M_2\) has union size \(r+3\) and occurs once.  Thus
\[
 \mu^2\binom{2r+1}{r+3}
 =h\binom r2+(t+X)(r-1)+M_2
 =b\binom r2+t\binom r2+M_2,
\]
which is the displayed identity.

To decompose \(M_2\), first take \(|P\cap Q|=r-2\).  The two crossed
events \(w_B(P)\in Q\) and \(w_C(Q)\in P\) occur
\(rb(m-1)\) times each by I1; their intersection consists of the
\(X=(r-1)t\) crossed configurations, which have
\(|H_B(P)\cap H_C(Q)|=r\) and must be removed twice.  Equality
\(w_B(P)=w_C(Q)\) is a third, disjoint way to raise the intersection
from \(r-2\) to \(r-1\), and contributes \(E_3\).  For
\(|P\cap Q|=r-3\), both crossed events are necessary and sufficient,
contributing \(X_3\).  Smaller base intersections cannot contribute.
Therefore
\[
 M_2=2rb(m-1)-2(r-1)t+E_3+X_3 ,
\]
with \(E_3=\#\{(P,Q):|P\cap Q|=r-2,\ w_B(P)=w_C(Q)\}\) and
\(X_3=\#\{(P,Q):|P\cap Q|=r-3,\ w_B(P)\in Q,\ w_C(Q)\in P\}\).
Hence at \(r\equiv3\pmod4\):
\[
 t\equiv E_3+X_3+\mu^2\tbinom{2r+1}{r+3}+b\tbinom r2\pmod2 .
\]

**Non-reductive implication (PROVED).**  At \(r=15\), the displayed
congruence formally gives
\[
 E_3\ \text{even and}\ X_3\ \text{even}\ \Longrightarrow\ t\ \text{even}
 \ \Longrightarrow\ \text{Conjecture E}\ \Longrightarrow\
 \chi(J(32,16))\ge18 .
\]
The tautology audit below shows why this implication is not a
reduction: at \(r=15\), \(E_3+X_3\equiv t\), so its hypothesis already
contains the desired parity.

**FINITE-VERIFIED.**  \(E_3\) and \(X_3\) are even in every existing
instance: \((t,E_3,X_3)=(6,6,0)\) at \(r=3\) (note \(X_3\) vanishes
there: no block pairs at distance \(r-3=0\)); at \(r=5\):
\((48,212,352)\times3960\), \((60,220,320)\times4752\),
\((60,240,300)\times1584\) — \(E_3+X_3\) is the \(t\)-determined
constant (564, 540) forced by the identity, and \((E_3,X_3)\) is a
coarser invariant than \(\Sigma_\gamma\) (it merges two
\(\sigma\)-species).

**Localization REFUTED (FINITE-VERIFIED).**  Per-point counts
\(K_z\) (with \(E_3=\sum_zK_z\) over the uniformity fibres
\(F_z\times G_z\), \(|F_z|=|G_z|=b/v\)) take odd values freely (at
\(r=3\): exactly six loci with \(K_z=1\); at \(r=5\): odd values
17, 19, 21, 25 occur), and per-\((r+3)\)-set \(X_3\)-counts of 1 and 3
abound.  Both evenness laws are irreducibly global.

**TAUTOLOGY CORRECTION (audited 2026-07-25; supersedes the earlier
"reduction" wording).**  Writing \(N\) for the
\((r+3)\)-by-\((r+1)\)-set incidence
and \(A_2\) for the \(|H\cap K|=r-1\) relation, one has over \(\mathbb Z\)
\(N^{\mathsf T}N=\binom r2I+(r-1)A_1+A_2\), so for odd \(r\),
\(A_2\equiv N^{\mathsf T}N+\binom r2 I\pmod2\).  With
\(Nx=Ny=\mu\mathbf 1\) and \(x\cdot y=h=b-t\) for true mates, this gives
\[
 E_3+X_3\equiv M_2=x^{\mathsf T}A_2y
 \equiv\mu^2\tbinom{2r+1}{r+3}+\tbinom r2(b-t)\pmod2 .
\]
At \(r\equiv1\pmod4\) both coefficients are even (\(\mu\) even,
\(\binom r2\) even): \(E_3+X_3\equiv0\) is forced — explaining the
audited fact that the 1583 \(T_E\)- and \(T_X\)-kernel-pair violations
at \(r=5\) coincide exactly and \(T_E+T_X\) is constant on the affine
hull (0/8778).  The earlier claim that "the affine route is dead" is
RETRACTED for the combined form at \(r\equiv1\pmod4\) — but the
resulting statement is \(t\)-blind there.  At
\(r\equiv3\pmod4\), only \(\mu\) and \(\binom r2\) are automatically
odd, giving
\[
 E_3+X_3\equiv\binom{2r+1}{r+3}+b-t\pmod2.
\]
Specifically at \(r=15\), Lucas's theorem makes
\(\binom{31}{18}\) odd, and
\(b=\binom{31}{14}/15\) is odd, hence
\(E_3+X_3\equiv t\pmod2\) IDENTICALLY.  Therefore the combined parity
target is a TAUTOLOGY at \(r=15\): it
is Conjecture E verbatim, not a reduction of it, and the
\(M_2\)-reduction below carries no independent leverage — given the
identity, \(\{E_3\text{ even}\wedge X_3\text{ even}\}\iff
\{E_3\text{ even}\wedge t\text{ even}\}\): the hypothesis contains
the conclusion.  (Form-level caveat: on arbitrary affine points
\(x^{\mathsf T}A_2y=T_E+T_X+T_{\text{one-sided}}\); the displayed
identity for \(T_E+T_X\) alone is proved for true mates, and the
\(r=5\) hull-constancy is the audited finding, independently
re-verified in the validator.)

**Status after the correction.**  The only remaining target is
Conjecture E itself — an integral pairing or counting proof of
\(t\) even — with \(E_3\)-evenness surviving as a separate,
independent conjecture that alone does NOT yield E.  Scope: finite
\(r=5\) is not \(r=15\); the layer-3 SAT probe returned UNKNOWN at
1800 s (1\,894\,897 branches, single worker) and licenses nothing.

## 2.12 The combined configuration set and its localization

**Unified characterization (PROVED).**  \(E_3\sqcup X_3\) is exactly
the set of *mutual* \(M_2\)-configurations:
\[
 \mathcal C=\{(P,Q):P\ne Q,\ w_B(P)\in H_C(Q),\ w_C(Q)\in H_B(P),\
 |H_B(P)\cup H_C(Q)|=r+3\},
\]
with the shared-\(w\) pairs at \(|P\cap Q|=r-2\) forming the
\(E_3\)-type and the crossed pairs at \(|P\cap Q|=r-3\) the
\(X_3\)-type; one-sided coincidences are excluded by mutuality.  Each
configuration canonically determines the \((r+3)\)-set
\(Y'=H_B(P)\cup H_C(Q)\).  The combined parity target is
\(|\mathcal C|\equiv0\pmod2\).

**Combined localization REFUTED (FINITE-VERIFIED).**  The per-\(Y'\)
count of \(\mathcal C\)-configurations is NOT always even: at \(r=3\)
every occupied \(Y'\) is odd (values 1 and 3); at \(r=5\) odd loci
abound (14\,880 of 48\,588 occupied loci over 300 pairs) and all four
per-\(Y'\) parity mixes \((E_3\bmod2,X_3\bmod2)\) occur.

**Superseded as a target (see the tautology correction in §2.9).**
By the \(N^{\mathsf T}N\)-identity, at \(r=15\) one has
\(|\mathcal C|=E_3+X_3\equiv t\): the combined parity statement IS
Conjecture E at this parameter, so no pairing on \(\mathcal C\) —
local or trans-local —
can be a reduction; a fixed-point-free involution on \(\mathcal C\)
would directly prove E, but constructing one is exactly as hard as
proving \(t\) even, and the localization data above shows it cannot be
built \(Y'\)-locally.  The unified mutuality characterization of
\(\mathcal C\) remains PROVED and may still be useful bookkeeping for
a direct integral attack on \(t\).

## 3. Status ledger

## 2.10 Rigorous no-go: the F2-linear relaxation cannot prove
E3/X3 evenness

Validator: `verify_linear_relaxation_nogo.py` (deterministic, green).

Encode a tiling as \(x[z][P]=[w(P)=z]\), and retain only these
\(\mathbb F_2\)-affine consequences of the exact constraints:
per-block parity, per-\((r+2)\)-set tiling parity, and per-point
uniformity parity.  The exact-one cardinality conditions themselves
are deliberately absent.  \(E_3\) and \(X_3\) become bilinear forms
\(T_E,T_X\) in the two encodings.  At the two accessible scales these
forms are not constant on the corresponding affine spaces:

- \(r=3\): 5 of the 7 kernel generators \(k\) have \(T_E(k,g_0)=1\)
  (\(T_X\) is vacuous there).  Enumerating all 128 affine solutions:
  exactly 8 are 0/1-fibre-legal, these are EXACTLY the 8 true
  tilings (zero "pseudo-tilings"), all with \(T_E=0\); among the 120
  illegal solutions, 64 have \(T_E=1\).
- \(r=5\): linear terms are clean for both forms, but the full
  kernel-pair check violates in 1583 of 8778 pairs for \(T_E\) and
  likewise for \(T_X\); in the deterministic reduced-echelon basis,
  pair \((10,61)\) is the first witness for each.  (An earlier
  40-generator sample happened to
  be violation-free; the interim "linear proof at r=5" claim made from
  it is RETRACTED — the full check refutes it.)

**Conclusions (PROVED by explicit witnesses).**  \(T_E\) is not
constant on the \(r=3\) affine hull, and neither \(T_E\) nor \(T_X\)
is constant on the \(r=5\) hull.  This refutes any
parameter-uniform proof which merely asserts that the displayed
affine constraints force the two forms to vanish.  At \(r=3\),
per-fibre exactly-one removes every countermodel and leaves precisely
the true mates.  At \(r=5\), however, this computation does not
isolate which omitted exact-cardinality condition is decisive.

The scope boundary is essential: the validator does not construct or
analyze the enormous \(r=15\) affine hull.  A parameter-specific
\(v=31\) module identity could still exist, and the true integral
tilings could satisfy a pairing invisible to every relaxation tested
here.  Thus this is a finite no-go for a general proof mechanism, not
a proof or disproof of the \(r=15\) evenness conjectures.

## 2.11 Integral pairing search: canonical candidates falsified

Validator: `verify_integral_pairing_failures.py` (r=3 exact; r=5
recounts under `--full`).

A-priori constraint (PROVED, from the localization refutations): per-z
\(E_3\)-counts and per-union \(X_3\)-counts are frequently odd, so any
parity-proving involution or free action must move configurations
across loci.

Candidates tested on true mates and falsified:
- **m1, reversal on \(E_3\)** \((P,Q,z)\mapsto(Q,P)\): holds in 0/336
  configs at \(r=3\) — an exact anti-reversal law there — but in
  3434/44\,028 (7.8%) at \(r=5\): neither absent nor universal, so
  neither the map nor the anti-law generalizes.
- **m6, complement-of-\(H\)**: PROVED impossible a priori:
  \([v]\setminus H_B(P)\) is an \(r\)-set disjoint from \(P\), and a
  block there would contradict intra-\(n_0=0\).  (0/44\,364 observed,
  as forced.)
- **m4, bases of \(Y=P\cup Q\)**: the image pair \((\beta,\gamma)\) is
  NEVER an \(E_3\)- or \(X_3\)-configuration (0 at both scales;
  \(\beta=\gamma\) in 24.5% of \(r=5\) configs).
- **c2, the \(Y^*\)-successor** via the canonical mate-blocks
  \(T_P=P^c\setminus\{z\}\in B\), \(U_Q=Q^c\setminus\{z\}\in C\) (with
  \(|T_P\cap U_Q|=r-2\) forced): the image bases land in \(E_3\) in
  0/336 (r=3) and 0/26\,384 (r=5, 120 pairs) — total failure despite
  being the most structured candidate.
- **m2/m3, \(w\)-successors** \(z\mapsto w_B(Q)\) etc.: not functions
  — per-locus counts vary (0..25 at \(r=5\)), images empty or
  multivalued.  Falsified structurally.
- **Reversal on \(X_3\)**: 29\,002/65\,868 (44.0%): not universal.

**Narrow failure statement.**  These falsifications eliminate the five
canonical constructions above (and their compositions built from the
same primitives, where the first step already fails).  They do NOT
show that no integral pairing exists; the evenness of \(E_3\) and
\(X_3\) remains FINITE-VERIFIED at \(r=3,5\) and CONJECTURAL at
\(r=15\).  What any surviving construction must satisfy: trans-local,
uses integral exactly-one structure (not its parity shadow, §2.10),
and is canonical for every \(S(14,15,31)\) — coordinate-free (the
\(v=2^5-1\) coincidence may only be used through parameter-uniform
statements such as the parity of \(\binom{31}k\)).

## 3. Status ledger

- PROVED: 1.1–1.5, Layer-1/Layer-2 countermodels (existence by
  explicit witness), the equivalences \(t\) even \(\iff\)
  \(\operatorname{wt}(u)\equiv0\ (4)\) \(\iff\) \(h\equiv b\ (2)\),
  the spectator identities and first-moment t-blindness, the
  second-moment identities, and the tautological equivalence
  \(E_3+X_3\equiv t\pmod2\) at \(r=15\).
- FINITE-VERIFIED: E itself at \(r=3\) (all 28 pairs) and \(r=5\)
  (all 10\,296 pairs); the \(D_6\)-torsor mechanism at \(r=3\)
  (56/56) — which does not extend as-is (fibres have \(r-1=14\)
  elements at \(r=15\), and the Klein commuting mechanism is refuted
  0/56); all spectator and second-moment censuses at \(r=3,5\).
- CONJECTURAL: Conjecture E itself at \(r=15\).  Separate evenness of
  \(E_3\) and \(X_3\) is a strictly stronger optional conjecture; its
  conjunction implies E only because it includes the equivalent
  combined parity.  No proof and no countermodel within the true
  Steiner axioms; the countermodels above bound what a proof must use,
  they do not refute E.

## 4. Validators

- `verify_H_identity.py` — tiling identity, fibre lemma
  \(X=(r-1)(b-h)\), Klein test.
- `verify_endpoint_parity_gap.py` — the \((r{+}1)/2\)-law census, the
  \(K_A\) computations of 1.5, the explicit Layer-1/Layer-2
  countermodels, and the exhaustive Layer-3 \(r=3\) check.
- `layer3_r5_sat.py` — the weaker \(r=5\) point-identified relaxation;
  its recorded 1800.3 s result is only UNKNOWN.
- `verify_fibration_connectivity.py` — the full \(r=5\) fibration and
  spectator census.
- `verify_spectator_congruence.py` — I1–I4, including direct
  enumeration of every spectator incidence.
- `verify_M2_reduction.py` — the second-moment identities, complete
  \(r=3,5\) species census, and explicit localization counterchecks.
- `verify_linear_relaxation_nogo.py` — explicit failures of the
  proposed affine-bilinear mechanism at \(r=3,5\), with no \(r=15\)
  inference.

All computations 2026-07-25, exact integer arithmetic.
