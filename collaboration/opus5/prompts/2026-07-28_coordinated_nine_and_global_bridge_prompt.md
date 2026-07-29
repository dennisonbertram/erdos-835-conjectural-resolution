# Erdős–Rosenfeld #835: coordinated-nine blockers and the global bridge

Date: 2026-07-28

You are Claude Opus 5 working at maximum reasoning effort. This is a novel
mathematics task, not a request for exposition. Work as a skeptical research
mathematician. A complete proof is preferred, but an exact counterexample to a
proposed lemma or a sharply reduced finite obstruction is also valuable.

## Non-negotiable scope

The actual target is Erdős–Rosenfeld Problem #835, equivalently the first open
case at `k=16` of the conjectural lower bound

    chi(J(2k,k)) >= k+2.

The current 13-vertex "class-B first lift" is only a local subproblem. Even a
proof of all six local profiles does not by itself solve #835. Never call the
problem solved unless you supply and audit the missing global implication.

Read these files first:

- `README.md`
- `collaboration/coordinated_nine_structural/NOTE.md`
- `collaboration/coordinated_nine_structural/verify_catalogue.py`
- `collaboration/r0_complement_cover_six/NOTE.md`
- `collaboration/r0_complement_cover_six/verify_arithmetic.py`
- `collaboration/coordinated_nine_r2_obstruction/NOTE.md`
- `collaboration/coordinated_nine_r2_obstruction/verify_obstruction.py`
- `collaboration/coordinated_eight_r1/NOTE.md`
- `collaboration/first_lift_global_theorem/NOTE.md`
- `collaboration/first_lift_global_theorem/TWELVE_SUPPORT_SWITCHING_NOTE.md`
- `collaboration/first_lift_global_theorem/verify_twelve_support_switching.py`
- `collaboration/opus5/first_lift_classB_attack/NOTE.md`
- `collaboration/opus5/first_lift_classB_attack/AUDIT.md`

Treat computation as evidence only. A universal claim requires a solver-free
proof unless a fully checkable certificate covers an explicitly finite and
proved-complete catalogue.

## Established local theorem

The repository now contains a solver-free proof that every graph on 13
vertices with minimum degree at least 7 contains three pairwise edge-disjoint
near-perfect matchings missing any three prescribed vertices, with repetitions
allowed. This proves coordinated nine for class-B profiles `r=3,4,5`.

The remaining profiles are `r=0,1,2`.

## Exact blocker A: r=0

There is a solver-free universal `3+3` complement-cover selection: among the
available size-five and size-three complements one can choose three of each
covering all 13 vertices. The probability bound by row multiplicity `a` is

    p(a) = C(7-a,3)/C(7,3) * C(5+a,3)/C(10,3)
         = (1/12, 2/21, 1/12, 4/75, 1/50, 0)

for `a=0,...,5`, and `p(a) <= (5-a)/36`; since `sum a=35`, expected uncovered
is at most `5/6 < 1`.

The three size-8 supports can be packed, and then the three selected size-10
supports can be packed using the ambient lemma:

    If H has 13 vertices and delta(H) >= 9, any three prescribed 10-subsets
    admit pairwise edge-disjoint perfect matchings.

This yields a six-prefix with complement cover and residual minimum degree at
least 7. The exact remaining task is to add three of the remaining size-10
supports. Prove a direct `3 x size8 + 6 x size10` theorem, or prove a switching
lemma that extends this six-prefix by three. If false, give an exact class-B
counterexample, not merely an arbitrary support system.

## Exact blocker B: r=1

For a complement-cover six-prefix `D` with `|E(D)|=26`, `Delta(D)<=5`, and
residual complement multiplicity `rho=d_D-1`, a remaining size-10 support is
blocked iff it contains a saturated `K6` of `D`.

The `K5+K5` Tutte obstruction is globally impossible by complement incidence:
its ten vertices would require `10*4=40` remaining-complement incidences while
all 11 remaining complements have total capacity 39. There is at most one
`K6`, and at most five of the six size-10 supports are blocked, so one
extendable size-10 matching exists.

After choosing such a matching `M`, the exact Tutte catalogue for a second
size-10 support in `(K13-D)-M` is:

    K5+K5, K_{3,1,1,1,1}, or K6.

`K333` is impossible because a 3-vertex component would have at most two
internal used edges plus one `M` edge, below the necessary used degree four.

The immediate blocker is the separator-3 `K_{3,1,1,1,1}` case. In a rigid
subcase, `M` has type `2(TT)+3(CA)` relative to the separator/component split,
and the selected/target omitted triples are `S/A`; the obvious two-edge switch
uses the only `C`-edge required by the target matching.

Find a support-preserving alternating switch, a short sequence changing the
choice of the first size-10 support, or a counting argument showing some
second support avoids this obstruction. State every adjacency forced by
`Delta(D)<=5` and by complement-incidence row sums. Do not silently assume an
edge is available.

## Exact blocker C: r=2

The repository gives an exact legitimate class-B instance where a natural
`8^4 10^2` complement-cover prefix blocks every remaining size-10 support.
That same fixed prefix nevertheless extends explicitly to nine with pattern
`8^5 10^2 12^2`. Therefore the "append one 10 plus both 12s" strategy is
false, but coordinated nine survives that instance.

Seek a universal reason that some remaining size-8 support plus both
size-12 supports can be packed after a suitable six-prefix, possibly after
switching at least two prefix layers. If the prefix itself must change,
formulate the weakest invariant on the chosen complement-cover six-prefix that
guarantees the extension, then prove that such a prefix can always be chosen.

## Global bridge

Independently inspect the exact first-lift reduction in the repository. Decide
what statement beyond class B would actually imply a 17-colouring or its
impossibility for `J(32,16)`. Produce one of:

1. a rigorous global theorem reducing #835 to finitely many local lift classes,
   together with a proof;
2. a precise counterexample showing that the current local-to-global
   propagation cannot work, plus the minimum additional compatibility
   invariant needed;
3. a new global invariant (parity, incidence, trade connectivity, or
   obstruction) with a fully proved implication strong enough to advance the
   original problem.

Review the existing global parity/frame/gluing attacks before reusing them;
several attractive invariants were already falsified.

## Deliverable

Write your result to:

`collaboration/opus5/coordinated_nine_and_global_bridge/NOTE.md`

The note must contain:

- exact theorem or counterexample statements;
- complete proof details or explicit certificates;
- a section named `Gap audit`;
- a section named `Scope relative to #835`;
- exact files/commands used for any computation;
- a short list of the next irreducible obligations if the full problem remains
  open.

Do not edit the existing proof notes. You may add verifier scripts only inside
`collaboration/opus5/coordinated_nine_and_global_bridge/`.
