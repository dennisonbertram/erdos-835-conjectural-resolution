You are Claude Fable 5 at xhigh effort, collaborating on the still-open
Erdős–Rosenfeld Problem #835. Use the efficient-fable skill. Work in
`/Users/dennison/Documents/Math Problem`.

The earlier API call was interrupted by an internet outage. Start from the
current repository truth, not from an assumed answer. Read `README.md` and
the following exact frontier files:

- `evidence/f32_four_statistic_k32_obstruction.md`
- `evidence/f32_five_statistic_moment_curve_clique_bound.md`
- `evidence/unprojected_fourth_moment_completion.md`
- `evidence/odd_graph_local_ball/radius5_reduction.md`

Important correction: the moment-curve \(e_4\) refinement has clique number
17 only inside that subfamily. A separate star-family search has now found
an explicit actual-edge \(K_{18}\) in the full quotient

\[
(e_1,e_2,e_3,e_4,e_8+e_1^8).
\]

The claimed states are

```
(1+x, x, 0, 0, lambda)
```

for these 18 `(x,lambda)` pairs:

```
(31,31),(26,28),(25,4),(24,9),(23,14),(22,3),
(19,0),(17,21),(16,24),(13,22),(12,27),(11,13),
(10,0),(9,24),(6,31),(2,17),(1,9),(0,4)
```

and all 153 edges are reportedly witnessed by only these three 15-set masks:

```
0x7975CD00
0x149693B9
0xFA3041BA
```

Your tasks:

1. Independently check or refute this static \(K_{18}\), recomputing every
   elementary-symmetric statistic from each actual 15-set and both exchanged
   16-sets. Do not rely on the other agent's program.
2. If it is correct, give the shortest exact proof and explain precisely why
   it rules out every arbitrary postprocessing of these five statistics but
   does not solve #835.
3. Then move beyond this failed family. Find either a richer explicit
   statistic giving a genuine 17-colouring on every 16-set, or an
   obstruction that applies to unrestricted colourings. A sampled or
   restricted graph is not enough.
4. Check \(k=2\) and \(k=4\) controls for every proposed universal identity.

Write only under `collaboration/fable_e4_v2/`: `JUDGMENT.md`, complete
arguments in `PROOF.md`, unproved ideas in `IDEAS.md`, and independent
executable checkers. Never claim the full problem is solved without either a
complete tight colouring/large set for some \(k>2\) or a universal
nonexistence theorem for all eligible \(k\).
