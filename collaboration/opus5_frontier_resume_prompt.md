# Claude Opus 5 frontier assignment: resolve Erdős–Rosenfeld #835

You are the principal mathematical investigator. Use Opus 5 at maximum
reasoning effort. Cost is not a stopping condition. Work on the full
Erdős–Rosenfeld Problem #835:

> Does any \(k>2\) admit a tight \((k+1)\)-colouring of \(J(2k,k)\)?

Equivalently, does any \(LS(k-1,k,2k)\) exist? A construction for one \(k\)
settles the existential problem positively. A negative resolution must cover
every \(k>2\), not merely \(k=16\).

Read `README.md` for scope and then personally audit the following newest
frontier files:

- `evidence/f32_prefix8_trace_hyperplanes.md`
- `evidence/f32_prefix8_trace_classification_verifier.py`
- `evidence/f32_two_statistic_k18_obstruction.md`
- `evidence/f32_two_statistic_k18_verifier.py`
- `evidence/top_degree_pairing_derivative_audit.md`
- `evidence/top_degree_cross_matching_cubic_audit.md`
- `evidence/verify_top_degree_cross_matching_cubic.py`
- `evidence/local_one_factorization_sign_audit.md`
- `evidence/local_one_factorization_sign_verify.py`
- `evidence/full_slice_degree_necessity.md`

Current exact frontier:

1. Divisibility leaves \(k=p-1\), \(p\) prime; known results exclude
   \(k\le14\); \(k=16\) is first open.
2. For \(k=16\), a tight colouring is \(LS(15,16,32)\), equivalently a
   covering \(O_{16}\to K_{17}\).
3. Every \(15\)-set \(U\subset\mathbb F_{32}^{\times}\) with
   \(e_1(U)=\cdots=e_7(U)=0\) is exactly a trace hyperplane
   \(\{x\ne0:\operatorname{Tr}(bx)=0\}\), with \(e_8(U)=b^{-8}\).
   Each nonzero coefficient-eight lifted layer is
   \(K_{17}\sqcup15K_1\).
4. The actual-edge quotient by
   \((e_1,e_8+e_1^8)\) contains an explicit verified \(K_{18}\).
   Therefore *every* 17-colour formula depending only on those two
   statistics is impossible. This is a no-go for that family, not for an
   arbitrary colouring.
5. Matching-cube top derivatives give an exact frame for the top Specht
   component. Projected pointwise idempotence yields the cross-matching
   cubic identity
   \[
   P_K(q_aq_b)=
   \begin{cases}
     (p-2)q_a,&a=b,\\
     -q_a-q_b,&a\ne b.
   \end{cases}
   \]
   The corresponding quadratic relaxation is feasible even in the false
   \(k=4\) control, so the cubic/global coupling is the live issue.
6. The natural scalar one-factorization sign descent recovers the
   \(p=5\) contradiction but closes consistently at \(p=17\); do not spend
   time repeating that scalar route.
7. Four exact searches are running, but solver silence or unchecked
   `INFEASIBLE` is not evidence.

Do the heavy lifting now. Pursue both:

- a richer explicit construction not killed by the two-statistic \(K_{18}\);
- a full contradiction from the cross-matching cubic or another genuinely
  global invariant.

Look especially for a representation-theoretic or sum-of-squares identity
that combines the cubic equations over all matchings and points, or a
finite-field statistic with enough information to define 17 colours while
remaining provably proper. Check all small false/true controls. Do not
return a literature summary or merely propose future work.

Write only new material under `collaboration/opus5/`:

- update `STATUS.md` with the strongest proved result and exact gap;
- put complete arguments only in `PROOF.md`;
- put unproved directions/failures in `IDEAS.md`;
- add independent validators for finite claims.

If you find a full solution, include a section `Why this proves the full
problem`. If not, give the strongest new unconditional theorem and continue
to a mathematically different attack rather than stopping at the first
failure.
