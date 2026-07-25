# Judgment: the e4 frontier (2026-07-25)

**Verdict.**  Tasks 1–2 are settled by proof.  Tasks 3–4 are reduced to a
finite decision that is fully scripted, double-implemented, and
cross-checked — but **not yet executed**: this session's permission
profile denied every script-execution route (local `python3`/`node`,
subagent shell, remote agent).  No computational number below the line is
claimed.  Erdős–Rosenfeld #835 is not resolved by anything here.

## Proved (PROOF.md, complete hand proofs)

1. **Edge law (Theorem A), strengthening the proposed implication.**  The
   common-\(r\) conclusion holds along **every single actual edge**
   between refined moment-curve states, not just on cliques with one
   vertex per \(a\):
   \(e_4(S)+a^4=e_4(S\cup T)=e_4(T)+b^4\).  Exact hypotheses: the two
   \(e_2=e_1^2\) conditions force the deleted points to be \(x=a,y=b\)
   (Lemma 1 gives the general deleted-point formula (L1.1)); the two
   \(e_3=e_1^3\) conditions then give \(e_{1,2,3}(S\cup T)=0\) and the
   common \(e_4\).  \(a\ne b\) is automatic (adjacent 16-sets never share
   \(e_1\)).  Dropping an \(e_3\) hypothesis breaks the law by the exact
   defect identity (A.1).  All char-2 steps written out.
2. **Exact formulation of the \(r\)-graphs (Theorem B).**
   \(G_r\) is precisely the union of labelled 17-cliques
   \(\{(a,\lambda_R(a)):a\in R\}\) over the family \(\mathcal R_r\) of
   17-sets with \(e_1=e_2=e_3=0\), \(e_4=r\), where
   \(\lambda_R(a)=ra^4+e_5a^3+e_6a^2+e_7a+e_8\).  A single \(r\) with
   \(\omega(G_r)\ge18\) or \(\chi(G_r)\ge18\) refutes every 17-colour
   rule in \((e_1,e_2,e_3,e_4,e_8+e_1^8)\) (Corollary B1).
3. **Reduction to two graphs (Theorem C).**  Scaling gives
   \(G_r\cong G_1\) for all \(r\ne0\); only \(G_0,G_1\) need deciding.
   The isomorphism does not respect the layer constraint, so task 4's
   \(H_r\) (at most 32 vertices each) must be checked for all 32 \(r\).
4. **Task 4 reduction.**  A \(K_{18}\) inside the \(K_{32}\) survives the
   e4 refinement iff \(\omega(H_r)\ge18\) for some \(r\), where
   \(H_r=G_r[\{(a,L(a))\}]\).

## Scripted, pending execution (no results claimed)

| Script | Role |
|---|---|
| `remote_run_e4.py` | Self-contained decision: MITM enumeration of every \(\mathcal R_r\); alternate-split identity check; from-scratch re-verification of each \(R\); all 496 \(K_{32}\) witness masks re-found with layer-consistent labels; exact \(\omega(G_0),\omega(G_1)\) (span-17 peeling + Tomita B&B) with printed pair-covering certificate if a \(K_{18}\) exists; \(\omega(H_r)\) for all 32 \(r\) with witness; DSATUR + 200 random greedy colour bounds, printing any \(\le17\)-colouring found. |
| `enumerate_e4_refinement.py` | Same logic, repo-local variant (reads the masks from the evidence verifier, dumps JSON for certificate extraction). |
| `verify_e4_refinement_independent.py` | Independent replay: suffix-DP DFS enumeration (no MITM), labels computed from the actual 16-sets (no quartic), fibre-based B&B (no Tomita), all 32 \(r\) decided without Theorem C.  Must agree with the above. |
| `verify_edge_law_smallfield.py` | Exhaustive \(\mathbb F_{16}\) validation of every identity used (all 11,440 nine-sets, all 411,840 adjacent pairs), including counterexample existence when hypotheses are dropped. |

Run order: `python3 collaboration/fable_e4/remote_run_e4.py` (est. 5–30
min), then the two verifiers.  Outcome tree:

- **"K18 FOUND" for \(G_0\) or \(G_1\)** → the five-statistic colour rule
  is refuted; the printed witness states and per-pair 17-set masks are a
  static certificate in the style of the \(K_{32}\) verifier.
- **\(\omega=17\) for both** → no clique obstruction at the e4 level;
  only \(\chi(G_0)\) or \(\chi(G_1)\ge18\) could still refute.  The
  colouring stages bound \(\chi\) from above; an exact \(\chi=17\)
  decision would need a SAT escalation (not yet written).  A printed
  17-colouring is a positive certificate for the moment-curve sector
  only — off-curve states remain open either way (Corollary B1 is
  one-directional).
- **Stage-6 output** answers task 4 exactly: \(\max_r\omega(H_r)\) with
  witness; \(\ge18\) means the \(K_{32}\) retains a surviving \(K_{18}\),
  anything smaller is a sharp nonexistence statement.

Labelled heuristic (not evidence): a uniform-random model of the pair
coverage suggests \(\omega(G_r)\) well below 18 and small
\(\omega(H_r)\); the graphs are algebraic, not random, so only the run
decides.

## Status

Blocked on one script run; every execution route in this session was
permission-denied.  All mathematics above stands independently.  Nothing
was written outside `collaboration/fable_e4/`.
