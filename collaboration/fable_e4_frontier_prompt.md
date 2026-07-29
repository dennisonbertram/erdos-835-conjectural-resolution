You are Claude Fable 5 at xhigh effort, collaborating on Erdős–Rosenfeld
Problem #835.  The problem remains open.  Work in
`/Users/dennison/Documents/Math Problem`.

Use the efficient-fable skill.  Do not restate old files wholesale.  Inspect
only the frontier artifacts needed:

- `evidence/f32_four_statistic_k32_obstruction.md`
- `evidence/f32_four_statistic_k32_verifier.py`
- `evidence/f32_prefix8_trace_hyperplanes.md`
- `evidence/f32_prefix8_trace_classification_verifier.py`
- `evidence/f32_two_statistic_k18_obstruction.md`
- your prior `collaboration/fable_frontier/PROOF.md`

Current exact result: the actual-edge quotient for

  sigma(S)=(e1,e2,e3,e8+e1^8)

contains a certified K32, on states

  (a,a^2,a^3,L(a)),  a in F32,

where L(a)=1 iff a=0 or Tr(a)=1.  An independent Python run has verified
all 496 actual Johnson edges.  This rules out only colour rules using those
four statistics.

The immediate boundary is e4.  For a 17-set R with deletion states indexed
by a,b, elementary-symmetric deletion identities imply that along an
edge joining first coordinates a,b, the transformed coordinate

  h(a) = e4(state_a) + a^4

is the common e4(R).  Thus any clique with one vertex over each a should
force a common value r for h(a).  Another agent is independently testing
the resulting finite graphs; do not modify its evidence files.

Your tasks:

1. Independently prove or correct the common-r implication, including all
   characteristic-two signs and exactly what hypotheses are needed.
2. Formulate the finite actual-edge graph for each r with vertices
   (a,lambda) representing
   (e1,e2,e3,e4,e8+e1^8) =
   (a,a^2,a^3,a^4+r,lambda).
3. Find an exact obstruction or construction:
   - If every r graph has clique number <18 or chromatic number >17, give a
     static certificate and independent checker.
   - If some graph has a 17-colouring that pulls back to a genuine statistic
     rule on all 16-sets, verify that complete rule; a partial sampled graph
     is not enough.
   - If neither is tractable, derive the sharpest exact structural reduction
     or counterexample to the proposed implication.
4. Separately identify whether the K32 admits any K18 surviving the e4
   refinement; a no-result search is not a theorem.

Write only into `collaboration/fable_e4/`.  Put a concise judgment in
`JUDGMENT.md`, any complete proof in `PROOF.md`, and independent executable
checkers beside them.  Label heuristic computations and unproved ideas
explicitly.  Do not claim #835 is solved unless you produce either a full
tight colouring/large set or a universal nonexistence theorem covering all
eligible k.
