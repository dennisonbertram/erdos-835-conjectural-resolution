# Support-ten remaining cases

## Verified result

For the cyclic \(C_{17}\) quotient, no squarefree trade of support ten has
Q-group multiplicity partition \(3+1+1\).

Together with the separately verified compact audit, a support-ten trade,
if one exists, must now have one of
\[
2+2+1,\qquad 2+1+1+1,\qquad 1+1+1+1+1.
\]
This does not exclude support ten completely and does not solve
Erdős--Rosenfeld Problem #835.

## Exhaustive argument

Q-balance pairs the three positive and three negative cells in the
three-cell Q-group, producing a signed triple-swap vector \(t\).  The two
one-cell Q-groups produce oriented single-swap vectors \(u,v\), in distinct
Q-groups from each other and from the triple group.  A candidate is exactly
\[
t+u+v=0.
\]

The verifier enumerates every oriented disjoint triple-versus-triple
choice.  There are
\[
228\binom{13}{3}\binom{10}{3}=7,824,960.
\]
For the target \(-t\), choose a nonzero coordinate, preferring maximum
absolute coefficient and then the shortest signed-row index.  Since
\(u+v=-t\), at least one of \(u,v\) has the target sign at this coordinate.
The signed-row index therefore enumerates one of the two moves without
loss.  After subtracting it, coefficients outside \(\{-1,0,1\}\) cannot be
the remaining single swap and are safely rejected.  The final move is an
exact dictionary lookup.  The dictionary independently asserts that all
35,568 oriented single-swap vectors are distinct, and the final test
enforces three distinct Q-groups.

The canonical driver splits the 228 triple Q-groups into four fixed ranges.
It checks 1,956,240 configurations in each range and reproduces these exact
residual-lookup counts:

| Q range | lookups |
|---|---:|
| 0:57 | 220,203,366 |
| 57:114 | 213,540,502 |
| 114:171 | 214,422,052 |
| 171:228 | 182,612,718 |
| **Total** | **830,778,638** |

No range contains a completion.

## Partial closure of \(2+2+1\)

Exactly \(33,642\) of the \(978,120\) oriented double-swap vectors contain
a coefficient \(+2\) or \(-2\).  At such a row, if the target coefficient
is \(2\), the other double-swap and single-swap coefficients can only be
\((2,0)\) or \((1,1)\); the negative case is symmetric.  Signed coefficient
indices therefore enumerate the other double swap without loss, after
which the required single swap is an exact dictionary lookup.

The verifier exhausts all 33,642 coefficient-two double swaps, performs
234,386,020 indexed double checks and 104,226,058 exact single lookups, and
finds no completion.  Consequently, in any \(2+2+1\) trade both double-swap
vectors must be unit-valued: every nonzero TC coefficient is \(+1\) or
\(-1\).  The all-unit stratum remains open.
