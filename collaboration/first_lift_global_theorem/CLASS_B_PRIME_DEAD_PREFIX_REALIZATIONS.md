# Class-B-prime realizations of the three dead-prefix supports

Date: 2026-07-28.

## Result

Each of the three fully completable support matrices in
`R1_DEAD_SEVEN_PREFIX.md` and `R3_DEAD_SEVEN_PREFIXES.md` is induced by a
proper \(17\)-edge-colouring of
\[
 H=K_{18}-E(K_{13}). \tag{1}
\]
In every colouring, the five vertices outside the \(K_{13}\) hole are
saturated: each is incident with every colour exactly once.  Consequently
all three support matrices are **class-B-prime**, equivalently
partial-factorization-realizable.

Thus the dead-seven-prefix phenomenon is not an artifact of allowing an
arbitrary class-B incidence matrix.  It occurs for:

* the \(r=1\) profile \((n_8,n_{10},n_{12})=(8,8,1)\);
* the \(r=3\), \(C\subset G\), profile \((10,4,3)\);
* the \(r=3\), \(D\subset G\), profile \((10,4,3)\).

This strengthens the scope of those three examples.  It does not change
their positive completion status: each support matrix still has the
explicit full \(17\)-matching decomposition of \(K_{13}\) already checked
by its original verifier.

## Why the literal colourings prove class B-prime

Write
\[
 A=\{0,\ldots,12\},\qquad P=\{13,\ldots,17\}.
\]
The graph in (1) has the \(65\) edges between \(A\) and \(P\), together
with the \(10\) edges of \(K_P\), for a total of \(75\) edges.

For a colour \(c\), let \(S_c\subseteq A\) be the vertices not incident
with a colour-\(c\) edge in (1).  Properness makes the colour-\(c\) edges a
matching.  Saturation of every vertex in \(P\) means the matching covers
all five outside vertices.  Its unmatched vertices in \(A\) are therefore
exactly \(S_c\).  A perfect matching on \(S_c\) would extend this partial
colour class to a one-factor of \(K_{18}\).

The literal certificates in
`verify_dead_prefix_partial_factorizations.py` check that these induced
sets \(S_c\), in colour order, equal the supports reconstructed from the
three committed dead-prefix instances.  Hence the previously displayed
seven matchings on the \(S_c\)'s can be placed inside the same
\(K_{13}\) hole and give the same dead prefixes at the class-B-prime tier.

## Verification

Run:

```sh
python3 \
  collaboration/first_lift_global_theorem/verify_dead_prefix_partial_factorizations.py
```

The verifier uses only the Python standard library and committed local
certificate modules.  For each of the three cases it checks:

1. every one of the \(75\) edges of \(K_{18}-E(K_{13})\) occurs exactly
   once in the literal colouring;
2. incident edge colours are distinct at every vertex;
3. each of the five outside vertices sees all seventeen colours;
4. every colour class is a matching saturating the five outside vertices;
5. its unmatched vertices in the hole are exactly the prescribed support.

`search_dead_prefix_partial_factorizations.py` records the deterministic
CP-SAT discovery model and prints the certificate literals.  It is not
needed for the proof.

## Scope boundary

Partial-factorization-realizable, or class-B-prime, support data are still
more general than supports arising from the simultaneous fan construction
relevant to the final Erdős--Rosenfeld reduction.  No fan witness is
constructed here, and none of the three examples is proved
fan-realizable.  Therefore this result does not settle the fan-realizable
case or Erdős--Rosenfeld Problem #835.
