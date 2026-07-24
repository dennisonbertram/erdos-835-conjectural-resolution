# State-refined association certificate for \(p=17\)

This directory records an exact rational feasible point for the
colour-state association-scheme relaxation described by the ordered cells
\[
P_{ab}=\{S:c(S)=a,\ c(S^c)=b\},\qquad a\ne b.
\]

It is a certificate for a necessary relaxation, not a colouring and not an
existence proof.  Its purpose is negative: the averaged state-refined
Delsarte/PSD conditions, including the aggregate parity and integrality
conditions visible after colour symmetrisation, do not yield a
contradiction at \(q=17,m=15\).

Run:

```bash
python3 evidence/state_sdp_p17/verify_state_sdp_p17.py
```

The verifier uses only the Python standard library and exact
`fractions.Fraction` arithmetic.  It checks:

- positivity and normalisation of the high-isotypic spectral weights;
- nonnegativity of all five ordered-state orbit entries at every Johnson
  distance \(0,\ldots,15\);
- the own-colour, complement-colour, and other-colour marginal formulas;
- divisibility by four of the aggregate same-state traces;
- integrality and evenness of every aggregate orbit total; and
- the expected total number of ordered pairs at each distance.
