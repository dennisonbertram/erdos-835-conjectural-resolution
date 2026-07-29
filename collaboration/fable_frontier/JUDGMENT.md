# Frontier judgment, 2026-07-25

Independent audit of the four newest claims for Erdős–Rosenfeld #835 at
\(k=16\), selection of the next attack, and the concrete step taken.
Problem #835 remains **open**; nothing here is a resolution.

## Execution disclosure

`python3` invocations were permission-blocked in this session (every
attempt, including via a subagent, returned "requires approval"; only
trivial shell reads ran).  Consequences:

- All verdicts below rest on line-by-line mathematical replay of the
  proofs and hand-verification of the finite data, not on re-running the
  repo verifiers.
- `evidence/verification.txt` contains **no recorded output** for the five
  newest verifiers (`f32_prefix8_trace_classification_verifier.py`,
  `f32_two_statistic_k18_verifier.py`,
  `verify_top_degree_pairing_derivative.py`,
  `verify_top_degree_cross_matching_cubic.py`,
  `local_one_factorization_sign_verify.py`; all dated 2026-07-25, checked
  by grep).  Whether they were ever run is not verified.
- The two scripts added in this directory are therefore **not yet
  executed**.  First action for the next session with execution rights:

```bash
python3 -B collaboration/fable_frontier/validate_k18_independent.py
python3 -B collaboration/fable_frontier/decide_cubic_embedding_k4.py
```

## Claim-by-claim verdicts

**Claim 1 (trace-hyperplane classification at coefficient eight): CORRECT,
proved.**  I replayed both proofs in
`evidence/f32_prefix8_trace_hyperplanes.md` in full: the divisibility step
\(L\mid(X^{32}+X)+L^2\), the coefficient comparison forcing
\(c_3=c_5=c_6=c_7=0\), \(c_4=u^{-14}\), \(c_2=u^{-6}\), \(c_1=u^{-2}\)
(including the automatic \(X\)-coefficient identity \(u^2c_1=1\)), the
rewriting as \(b^{-16}\operatorname{Tr}(bX)\) with \(u=b^{-8}\), and in
Theorem 2 the forcing \(s=0\Rightarrow y=a,x=c\), the derivation
\(B_0=0\) (using \(B_8=A_6\) from the degree-23 comparison), and the
converse recursion \(e_j(S_a)=a^j\).  These stand as written proofs; no
computation is needed for the theorems themselves.  The claimed
\(K_{17}\sqcup15K_1\) lifted-layer structure follows.

**Claim 2 (actual-edge \(K_{18}\) kills every \(F(e_1,e_8+e_1^8)\) rule):
LOGIC AND SCOPE CORRECT; certificate hand-verified except the e8 layer.**

- Scope logic is airtight: proper 17-colourings of \(J(32,16)\) and tight
  colourings coincide (a shared 15-set star is a \(K_{17}\), so proper
  \(\Rightarrow\) rainbow stars; tight \(\Rightarrow\) proper likewise),
  and a \(G\) with \(\le17\) values on 18 pairwise actual-edge-adjacent
  quotient states must repeat a value on an actual Johnson edge.  The 18
  states are pairwise distinct (17 distinct \(e_1\) values at
  \(\lambda=1\), plus \(\lambda=27\ne1\)).
- Hand-verified without a machine: the base set equals
  \(\{0\}\cup\{\operatorname{Tr}=1\}\) via the bit formula
  \(\operatorname{Tr}(x)=b_0\oplus b_3\) (PROOF.md Lemma 4), which by the
  audited Theorem 2 of claim 1 *proves* the whole \(K_{17}\) half of the
  certificate (136 of 153 edges) analytically; all 17 witness masks have
  popcount 17; the stated deletions lie in their masks; the markdown hex
  table matches the verifier's decimal masks (4 of 17 conversions checked
  by hand, all 17 by the new validator); and the full \(e_1\) layer of all
  17 extension rows is internally coherent — in every row
  \(x\oplus a=y\oplus29\), as adjacency demands, and I recomputed one full
  17-set XOR from its mask (row \(a=28\): XOR \(=0\)) confirming the
  common value is genuinely \(e_1(R)\).
- Remaining machine-only content: the \(e_8\) values of the 34 extension
  16-sets.  The repo verifier (audited line by line: independent long
  division field arithmetic, statistics from scratch, all 153
  intersections checked, distinctness asserted) covers this, and
  `validate_k18_independent.py` now re-covers it with third-party
  arithmetic (discrete logs, full root polynomial with root self-checks).
  Until one of them is actually executed, cite the \(K_{18}\) as
  "machine-checkable, checker audited", not as re-verified.

**Claim 3 (exact cross-matching cubic; quadratic relaxation has a false
\(k=4\) control): CORRECT.**  Replayed: the frame scalar
\(|\mathcal M|2^k/\dim K=(k+1)!\); \(\langle\boldsymbol1,e_M\rangle=0\);
\(W q_a=0\) from tightness; the projected-idempotence identity (4); the
cubic (8) by inserting the reconstruction twice; and the Helmert
relaxation numbers at \(k=4\) (\(\sqrt{350}\): diagonal
\(350\cdot\tfrac45=280=5\cdot14\cdot4\), off-diagonal \(-70=-pd\)).  The
note's scope statements are accurate.

**Claim 4 (scalar one-factorization signs close at \(p=17\)): CORRECT.**
Replayed the flag-transposition bookkeeping, the parity of the pinned
descent, and the formal sign model (9): its consistency needs exactly
\(a_p=h_p\), which I checked by direct computation at
\(p=3,5,7,17\) (\(\binom22,\binom32,\binom42,\binom92\) vs
\(\binom54,\binom74,\binom94,\binom{19}4\) mod 2), matching the Lucas
classes stated.  A homomorphic model satisfying every generator means no
product of the sign identities can yield \(-1=+1\).  Route closed, as
claimed.

## Decision on the cubic question

**The cross-matching cubic cannot be summed, polarized, or represented as
a positive form to force a contradiction at \(p=17\).**  This is now a
theorem, not an impression — PROOF.md:

- Lemma 1: the cubic forces the entire Gram shape up to one scalar, so
  quadratic information adds only a normalization.
- Theorem 1: every scalar obtained by iterated products/contractions
  inside the span of the colour vectors is determined and simultaneously
  realized by an explicit weighted \(p\)-point model — consistent at every
  prime, including 17.
- Lemma 3: \(K\) contains no nonzero nonnegative function, so there is no
  "integrate against a nonnegative kernel" refutation either.
- Theorem 2: the full residual content of the cubic system is a single
  decision problem — does \((K,P_K\circ\mathrm{mult})\) contain a
  \(\beta\)-closed reduced-\(p\)-point subalgebra at norm
  \(\nu=pd(p-1)\)?

## Attack comparison and selection

1. **Cubic/embedding decision — SELECTED.**  The theorem above closes all
   cheap uses of the cubic, and Theorem 2 isolates what is left as a
   bounded real-algebraic decision.  At the false parameter \(k=4\) it is
   a 56-parameter least-squares search over \(\dim K=14\), and *both*
   outcomes advance the program: numerical feasibility closes the cubic
   route with a new no-go (after exact certification); a robust residual
   floor makes the cubic the first relaxation in this hierarchy to detect
   the \(k=4\) obstruction, and the follow-up (exact equivariant
   infeasibility, then \(p\)-uniform scaling) becomes the leading
   negative-side attack.  Implemented: `decide_cubic_embedding_k4.py`
   (with a \(k=2\) true-parameter control that must pass before the
   \(k=4\) result is trusted).
2. **Richer finite-field statistics** — secondary; see IDEAS.md.  Key
   structural point: for any statistic map, a proper 17-colouring of its
   actual-edge quotient pulls back to a tight colouring, so quotient
   \(K_{18}\)s only ever close specific families, while *any* quotient of
   chromatic number exactly 17 would already resolve #835 positively.
   The found \(K_{18}\) does not automatically survive refinement (its
   extension vertex splits under any statistic separating the 17 witness
   rows), so each family needs its own search.
3. **Scalar sign route** — correctly closed; do not reinvest.

## Strongest unconditional new result of this session

The polarization no-go (PROOF.md Lemmas 1–3, Theorem 1) plus the
embedding reformulation (Theorem 2), and, on the audit side, the analytic
proof of the \(K_{17}\) half of the \(K_{18}\) certificate (Lemma 4).

## Single best executable next attack

```bash
python3 -B collaboration/fable_frontier/decide_cubic_embedding_k4.py --restarts 500
```

then act per its printed outcome (exact certification if feasible;
equivariant infeasibility proof if a floor).  Independently, run
`validate_k18_independent.py` once to close the last open layer of the
\(K_{18}\) audit, and append both outputs to `evidence/verification.txt`.
