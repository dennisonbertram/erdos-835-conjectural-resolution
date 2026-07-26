# Opus 5 xhigh follow-up: complete the joint note, then attack the live frontier

You are continuing the exact same Erdős–Rosenfeld #835 research task in the
same repository.

Your first response artifact is incomplete:
`collaboration/opus5/joint_schreier_krein_attack/NOTE.md` currently ends at
line 340, immediately after Corollary B1, even though its introduction and
verifier claim later Sections 5--8 (quadratic exhaustion, the epsilon
identity, the first unforced statistic, and the Witt control).

## Required first task: repair and finish the note

Append all missing sections to `NOTE.md`.  Do not merely summarize the
verifier.  Give complete human-checkable proofs.  In particular:

1. State and prove the exact quadratic-leakage no-go theorem, including the
   13-by-13 Gram matrix, its corank-two kernel, the one free moment, the exact
   PSD lower bound, why it is weaker than the entrywise bound, and the
   exhaustive 8191 Perron-subset check (clearly distinguishing a finite
   computation from a conceptual proof).
2. Give a fully explicit set-theoretic proof of the local epsilon identity.
   For a fibre pair B,C with |B cap C|=13, classify all five common
   R-neighbours, name the two 2-element difference sets, calculate the
   intersections of every kind of pair among those five blocks, prove exactly
   eight of the ten pairs have intersection 13, and prove each of the two
   remaining pairs has intersection 12 or 13.  Then derive, without a hidden
   double-counting assumption,
       sum_D Q_BD^2 = 10080 + 4 sum_{C:|B cap C|=13} epsilon_BC
   or the correct identity if this displayed form is not exact, followed by
   the trace(Q^2), trace(R^4), and 4-cycle bounds.  Audit every factor of two.
3. Define the first genuinely unforced mixed statistic precisely and explain
   why all lower-order quadratic attacks cannot determine it.
4. Include the k=6 Witt-system control and explain exactly what it validates
   and what it does not.
5. Make scope unmistakable: #835 remains open unless you actually derive a
   contradiction or construction.

Run the exact verifier and Ruff after editing.  If the verifier's epsilon
calculation is even slightly too schematic or wrong, repair both the proof
and checker rather than defending it.

## Required second task: resume the heavy mathematical attack

After the note is complete, use the new H1/H2 rigidity together with the live
H3/H4 frontier:

- H3 is supported on E3+E12+E13+E14+E15, all fibre relations act in
  span(I,R), and the first leakage is L=(I-P3)RP3.
- H4 is supported on E4+E11+...+E15, all fibre relations act in
  span(I,R,A13); the known operator polytope is feasible.

Search for the first cross-module or cross-fibre identity not already
collapsed by the scalar H1/H2 theory.  Prioritize an exact contradiction or
an explicit construction.  Promising targets include:

- mixed products whose trace has both a Johnson-spectral evaluation and a
  local matching/triple-profile evaluation;
- Krein/Schur positivity coupling P1,P2,P3,P4 rather than treating modules
  separately;
- the unforced epsilon statistic coupled to H3 or H4;
- triple-incidence profiles and integrality/congruence constraints;
- all 17 fibres simultaneously, not a single-fibre relaxation.

Do not report a numerical solver timeout as mathematical evidence.  Record
every theorem, failed route, exact checker, and next forced statistic in a new
or extended artifact under `collaboration/opus5/`.  Continue autonomously.
