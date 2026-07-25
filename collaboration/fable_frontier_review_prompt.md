# Claude Fable xhigh: independent frontier judgment for Erdős–Rosenfeld #835

Use `/efficient-fable` first. Act as the senior mathematical orchestrator and
skeptical final judge. Delegate bounded algebra checks, exhaustive small-case
tests, and literature scans to cheaper subagents; reserve your own effort for
choosing and integrating the attack most likely to resolve the full problem.

The full objective is Erdős–Rosenfeld Problem #835: decide whether any \(k>2\)
has a tight \((k+1)\)-colouring of \(J(2k,k)\), equivalently whether any
\(LS(k-1,k,2k)\) exists. A negative proof must cover all surviving prime
parameters, while a construction at one parameter suffices positively.

Read `README.md`, then audit these newest files:

- `evidence/f32_prefix8_trace_hyperplanes.md`
- `evidence/f32_prefix8_trace_classification_verifier.py`
- `evidence/f32_two_statistic_k18_obstruction.md`
- `evidence/f32_two_statistic_k18_verifier.py`
- `evidence/top_degree_pairing_derivative_audit.md`
- `evidence/top_degree_cross_matching_cubic_audit.md`
- `evidence/verify_top_degree_cross_matching_cubic.py`
- `evidence/local_one_factorization_sign_audit.md`

Current exact claims, none yet a full solution:

1. At \(k=16\), the seven-zero-prefix \(15\)-sets in \(\mathbb F_{32}\)
   are exactly trace hyperplanes. Their nonzero coefficient-eight lifted
   layers are \(K_{17}\sqcup15K_1\).
2. The actual-edge quotient on
   \((e_1,e_8+e_1^8)\) contains an explicit \(K_{18}\), excluding every
   17-colour rule based only on those two statistics.
3. Top matching-cube derivatives yield an exact cross-matching cubic
   projected-idempotence identity. Quadratic data alone admits a false
   \(k=4\) control, so a real obstruction must use the cubic/global coupling.
4. The scalar one-factorization-sign route is consistent at \(p=17\), so it
   is a closed route rather than a contradiction.

Your assignment:

- independently decide whether the \(K_{18}\) certificate and its logical
  scope are correct;
- decide whether the cross-matching cubic can be summed, polarized, or
  represented as a positive form to force a contradiction at \(p=17\);
- seek a richer finite-field construction that evades the two-statistic
  obstruction;
- compare those paths and do one concrete, technically serious next step,
  not merely a list of ideas.

Put new work only under `collaboration/fable_frontier/`, with:

- `JUDGMENT.md` for audited conclusions and attack selection;
- `PROOF.md` for complete new lemmas only;
- `IDEAS.md` for unproved directions and explicit failure points;
- exact validators for any finite claims.

Do not call #835 solved without a complete proof or construction. If no full
solution is reached, return the strongest unconditional new theorem and the
single best executable next attack.
