# Judgment: the claimed five-statistic \(K_{18}\) is CORRECT

Date: 2026-07-25.  Auditor: Claude Fable 5 (independent second audit,
no code shared with the discovering agent).

## Verdict

**Confirmed.**  The eighteen states \((1{+}x,\,x,\,0,\,0,\,\lambda)\) for
the claimed \((x,\lambda)\) pairs form an actual-edge \(K_{18}\) in the
quotient of \(J(32,16)\) by
\((e_1,e_2,e_3,e_4,\,e_8+e_1^8)\) over
\(F=\mathbb F_2[\alpha]/(\alpha^5{+}\alpha^2{+}1)\), witnessed entirely by
the three claimed \(15\)-set masks.  Consequently **no proper colouring
of \(J(32,16)\) that factors through these five statistics uses fewer
than 18 colours**, for completely arbitrary postprocessing.  The
five-statistic construction family is dead.

## What was checked, and how

Execution constraint: every code path (python, node, codex, remote
agents, web evaluators) was permission-denied in this session, so the
audit was done by **exact hand computation in \(\mathbb F_{32}\)**, fully
displayed in `PROOF.md` for line-by-line audit, with redundant
cross-checks; the from-scratch machine checkers are provided and should
be run at first opportunity:

```bash
python3 -B collaboration/fable_e4_v2/verify_k18_independent.py
python3 -B collaboration/fable_e4_v2/verify_rigidity_and_controls.py
```

Checked items (all pass):

1. The three masks decode to \(15\)-sets (popcounts 15).
2. Each satisfies \(\prod_{b\in B_i}(1+bt)\equiv1+t\pmod{t^5}\), computed
   twice per mask via untruncated half-products (each half verified by an
   independent evaluation identity at \(t=1\), and at \(t=2\) for
   \(B_2\)), then convolved term-by-term; \(\tau_1=1\) additionally
   confirmed by direct XOR of the fifteen elements of each mask.
3. All three masks share \(e_7=12\), \(e_8=5\) — three disjoint
   computations giving the same pair.
4. Hence every completion \(B_i\cup\{p\}\) has
   \(\sigma=(1{+}p,p,0,0,\;4\oplus12p\oplus p^8)\), and the closed form
   \(4\oplus12x\oplus x^8\) reproduces all 18 claimed \(\lambda\)'s
   (18/18 rows displayed).
5. Coverage: the miss-sets \(X\cap B_i\) have sizes 5, 6, 3 and are
   pairwise disjoint, so every one of the 153 pairs avoids some mask
   entirely and is realized as an actual star edge (intersection exactly
   15).  Note the masks realize 13, 12, 15 of the 18 states
   respectively — coverage comes from disjointness of the miss-sets, not
   from near-complete stars.
6. The 18 states are pairwise distinct (distinct \(e_2=x\)).

Residual risk: hand arithmetic.  Mitigations: self-checking discrete-log
table (order-31 cycle), two-route computation of every half-product
evaluation, three-way agreement of \((\tau_7,\tau_8)\), 18 independent
\(\lambda\)-matches, and two end-to-end direct-XOR spot checks of
\(e_1\) on actual \(16\)-sets.  A conspiracy of errors surviving all of
that is implausible, but the scripts should still be run.

## Why this kills the family but not #835

The argument uses only that the colouring is constant on
\(\sigma\)-fibres: 18 fibres pairwise joined by actual Johnson edges need
18 colours.  It makes no claim about colourings that separate points
within a fibre — i.e. almost all colourings.  The 51 concrete \(16\)-sets
involved lie in three stars, and a star is merely rainbow under any
proper 17-colouring: no contradiction survives unquotiented.  It is
\(k=16\)-specific.  #835 remains open in both directions.

## Position in the programme

* Supersedes the four-statistic \(K_{32}\)
  (`evidence/f32_four_statistic_k32_obstruction.md`) in the
  \(e_4\)-retaining direction.
* Complements, and does not contradict, the moment-curve bound
  (`evidence/f32_five_statistic_moment_curve_clique_bound.md`): that note
  proved clique number 17 for cliques with \((e_1,e_2,e_3)=(a,a^2,a^3)\);
  the new clique lives on the disjoint line \((e_1,e_2)=(1{+}x,x)\)
  (disjoint because \(e_1^2{+}e_1{+}1=0\) has no root in
  \(\mathbb F_{32}\)).  The moment-curve family was the wrong place to
  look for the \(K_{18}\); the full quotient does contain one.
* The README's five-statistic frontier entry should, on merge, be updated
  to record the full-quotient \(K_{18}\) (not edited here; this audit
  writes only under `collaboration/fable_e4_v2/`).

## New proved material beyond the audit

`PROOF.md` §6 adds exact adjacency-rigidity theorems for every prefix
quotient (deletion-determined witnesses, pair conditions
\(C_3,\dots,C_m\), star form R3), with \(k=2\) and \(k=4\) controls
(§7): the machinery reconstructs every actual edge at both decided
parameters, imposes nothing at \(k=2\) (where the tight colouring
exists), and is non-vacuous at \(k=4\).  These structure the
six-statistic search (`IDEAS.md` §1), which is the next decisive target:
a \(K_{18}\) there kills six statistics; a proper 17-colouring of that
quotient graph would settle \(k=16\) positively.

## Honest gaps

* No universal (unrestricted-colouring) obstruction was found; none is
  claimed.
* No richer statistic yielding a genuine 17-colouring was found; none is
  claimed.
* The two companion scripts are unexecuted as of this writing (execution
  denied in session); the hand proof in `PROOF.md` is the verification of
  record until they are run.
* The full problem is **not** solved, and nothing here should be cited as
  progress on existence for any \(k>2\) beyond the death of this
  construction family.
