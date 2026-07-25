# Ideas beyond the five-statistic kill (all unproved unless cited)

Status labels: **proved** = in `PROOF.md` with complete argument;
**heuristic** = counting estimate, no theorem; **open** = genuinely
unknown; **blocked** = needs execution, none was possible in the
authoring session.

## 1. The six-statistic frontier \((e_1,\dots,e_5,\;e_8+e_1^8)\)

The natural next family after the five-statistic \(K_{18}\).  Its status
is **open** in both directions.

What is proved (PROOF.md §6): for two states with distinct \(e_1\), any
witnessing \(17\)-set has its entire prefix \((\rho_1,\dots,\rho_5)\) and
both deletion points determined in closed form by the two states, and
three pair conditions \(C_3,C_4,C_5\) must hold.  Adjacency then reduces
to membership of \(\{u,v\}\) in an actual \(17\)-set with that determined
prefix and a two-equation linear tail condition on
\((\rho_6,\rho_7,\rho_8)\).

Heuristic sparsity: there are \(\binom{32}{17}\approx2^{29.07}\)
seventeen-sets and a determined class costs five prefix coordinates plus
two tail equations \(\approx2^{35}\); a typical pair's witness class is
empty, so the six-statistic quotient graph is far sparser than the
five-statistic one.  Two opposite conjectures are both live:

* (kill) a \(K_{18}\) still exists, found by a search over
  prefix-constrained fibres rather than stars — the five-statistic
  certificate's fibre \((1,1,0,0,0,\tau_7{=}12,\tau_8{=}5)\) shows fibres
  can be unexpectedly rich;
* (survive) the quotient graph has chromatic number \(\le17\), in which
  case ANY proper \(17\)-colouring of the quotient graph would pull back
  to a genuine tight \(17\)-colouring of \(J(32,16)\) and settle #835's
  \(k=16\) case **positively**.  Nothing known excludes this today; the
  repository's no-gos cover other families.

Search design (**blocked**, ready to implement): adapt
`evidence/f32_five_statistic_global_clique_search.cpp`.  Enumerate
half-set generating polynomials of both 16-halves through degree 8
(\(2^{16}\) each, as in the existing meet-in-the-middle notes); index
right halves by (size, first five coefficients); for a candidate state
pair, the determined \((\rho_1..\rho_5,u,v)\) prune immediately via
\(C_3\wedge C_4\wedge C_5\) before any set enumeration.  Because every
edge is triply constrained, build the edge list of the *realizable* state
graph first, then run the existing branch-and-bound clique code.  A
\(K_{18}\) here would kill every postprocessing of six statistics; an
exact bound \(\le17\) plus an explicit quotient colouring would solve the
problem — either outcome is decisive for the family.

## 2. Line-family structure inside the five-statistic quotient

**Proved** (R3): every edge between line states
\((1{+}x,x,0,0,\cdot)\) is witnessed in the fibration of
prefix-\((1,1,0,0,0)\) fifteen-sets over \((\tau_7,\tau_8)\), with
per-edge \(\lambda\)-compatibility
\(h(x)+h(y)=(x+y)\tau_7\), \(h(z):=\lambda(z)+1+z^8\).

**Open**: the maximum line-family clique.  Eighteen is realized.  A
\(K_{19}\) would need a \(\lambda\)-function on 19 parameters such that
every pair admits a fibre member omitting both parameters with the right
\((\tau_7,\tau_8)\).  If all edges use ONE fibre \((d,c{+}1)\) — as the
certificate does — then \(\lambda(x)=c+dx+x^8\) globally, and the
question becomes purely one about the hypergraph of miss-sets
\(\{X\cap T\}\) over the fibre: we need the miss-sets restricted to \(X\)
to have the property that no pair of parameters is hit by every member.
**Blocked**: enumerate the fibre \((1,1,0,0,0,\ast,\ast,12,5)\)
exhaustively (meet-in-the-middle, cheap) and compute the maximum
\(X\) for which the miss-set family covers all pairs; this would give the
exact line-family clique number and a cleaner canonical certificate.

## 3. Where a genuinely universal obstruction would have to live

Nothing in this session produced an obstruction valid for unrestricted
colourings, and the pattern of results argues against expecting one from
quotient cliques: a quotient \(K_{18}\) uses only that the colouring is
constant on \(\sigma\)-fibres, and every such argument dies the moment
the statistic is refined past injectivity.  The repository's sharpest
universal boundary remains the fourth-moment completion
(`evidence/unprojected_fourth_moment_completion.md`): the first
unprojected layer is *equivalent* to the colouring itself.  Any proposed
universal identity must therefore be tested immediately against the two
decided controls —

* \(k=2\): a tight \(3\)-colouring EXISTS; the identity must be
  satisfiable there (no false obstruction);
* \(k=4\): tight \(5\)-colourings do NOT exist (`verify_k4.py`,
  disjointness graph has clique number 2); an identity that "proves"
  nonexistence must actually distinguish these two cases by something
  other than parity of \(k\) or size bookkeeping.

The rigidity conditions \(C_3,\dots,C_m\) pass both controls (PROOF.md
§7) precisely because they are identities about witnesses, not
obstructions; they carry no nonexistence content by themselves.

## 4. Smaller concrete blocked tasks

* Run `verify_k18_independent.py` and `verify_rigidity_and_controls.py`
  (this directory) for machine confirmation of the hand proofs.
* Count the fibre \(|\{T:\;e(T)\equiv1+t\ (t^5),\ e_7(T)=12,\
  e_8(T)=5\}|\); the certificate needs only 3 members, and the heuristic
  expectation for a full \((\tau_1..\tau_4,\tau_7,\tau_8)\)-fibre is
  \(\binom{32}{15}/32^6\approx0.5\) — the actual fibre is at least
  \(3\), i.e. this fibre is at least \(6\times\) over-populated relative
  to the uniform heuristic.  Understanding why (the trace/subfield
  structure of \(\lambda(x)=4+12x+x^8\) suggests a hidden coset
  structure) may point to which richer statistics still admit large
  fibres — the engine behind every kill so far.
* \(k=4\) full-analogue decision: the two-statistic analogue
  \((e_1,e_2,e_4+e_1^4)\) over \(F_8\) is decidable by exhaustion
  (\(\binom{8}{4}=70\)); a clean statement there (family dead/alive at a
  decided \(k\)) is a useful control for the whole quotient-clique
  programme.  Note `collaboration/fable_frontier/` already contains a
  \(k=4\) decision script for the embedding reformulation; extend rather
  than duplicate.
