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
vectors would have to be unit-valued: every nonzero TC coefficient is
\(+1\) or \(-1\).

The all-unit stratum is also exactly excluded.  For a unit double vector
\(A\), unit single vector \(S\), and required unit double
\(B=-A-S\), let \(k=|\operatorname{supp}A|\), \(s=|\operatorname{supp}S|\),
and let \(c\) count opposite-sign overlaps of \(A,S\).  Same-sign overlap
would make a forbidden coefficient two, while
\[
|\operatorname{supp}B|=k+s-2c\le16.
\]
Thus \(c\ge\lceil(k+s-16)/2\rceil\).  Signed posting lists enumerate every
\(A\) meeting this necessary threshold; \(B\) is then an exact lookup.
The sole zero-threshold case \(k=10,s=6\) is enumerated separately.

Across all 35,568 single swaps, the verifier processes 2,328,439,580 signed
posting hits, tests 2,614,558 threshold candidates, and makes 2,329,004
exact residual lookups.  It finds none.  Therefore
\[
\boxed{\text{the support-ten partition }2+2+1\text{ is impossible}.}
\]
The only remaining support-ten partitions are \(2+1+1+1\) and \(1^5\).

## Exclusion of \(2+1+1+1\)

For each of the 978,120 double swaps, let \(t\) be its negative TC vector.
Three single swaps \(u,v,w\), in three mutually distinct Q-groups also
distinct from the double group, would have to satisfy \(u+v+w=t\).
At a nonzero coordinate of \(t\), at least one of the three moves has the
target sign.  The signed-row index enumerates it.  The residual is bounded
by two because only two unit moves remain.  A second signed-row forcing
then reduces the problem to one exact single-vector lookup.
If the first residual is zero, the double and first single already form a
smaller-support trade excluded by the preceding support audits; the driver
therefore omits that already-settled branch.

For speed, the final lookup first uses a deterministic additive 64-bit
fingerprint
\[
h(x)=\sum_r x_r\,w_r\pmod{2^{64}},
\]
where the committed source defines every \(w_r\) by a fixed integer mixing
function.  A 24-bit membership table rejects most candidates before the
full fingerprint lookup.  This filtering is exact: vector equality implies
fingerprint equality, and any full-fingerprint collision is checked by
exact sparse-vector equality.  It therefore has no probabilistic
soundness assumption.

The twelve fixed Q-ranges exhaust all 978,120 double configurations,
138,197,446 first forced moves, 18,498,153,804 fingerprint probes, and
39,181,742 low-table hits.  There are no full fingerprint hits and hence no
trade.  Therefore
\[
\boxed{\text{the support-ten partition }2+1+1+1\text{ is impossible}.}
\]
Only \(1+1+1+1+1\) remains at this stage.

## Exclusion of \(1+1+1+1+1\)

Represent a candidate as five oriented single swaps in five distinct
Q-groups.  Fix the least Q-group and its first move.  At a nonzero row of
the current partial sum, one remaining move must have the opposite sign.
Three successive signed-row forcing steps enumerate the second, third, and
fourth moves.  Coefficient bounds \(3,2,1\) discard only partial sums that
the remaining three, two, or one unit moves cannot cancel.  The fifth move
is uniquely determined and looked up by the same exact fingerprint filter
described above.  All later Q-groups are required to exceed the fixed
minimum and to be mutually distinct.
If the first two moves already cancel, they form a support-four trade
excluded earlier, so the corresponding zero partial sum is safely skipped.

The twelve fixed minimum-Q ranges process 2,150,540 second-move hits,
184,640,524 third-move hits, 17,360,802,928 final fingerprint probes, and
36,769,906 low-table hits.  There are no full fingerprint hits and no
trade.  Hence the \(1^5\) partition is impossible.

All seven partitions of five have now been excluded.  Together with the
support-two through support-eight audits, this proves
\[
\boxed{\text{every nonzero squarefree cyclic-quotient trade has support
at least }12.}
\]
This is a local rigidity theorem for the cyclic quotient.  It does not
exclude an exact cover or a fan and does not solve Erdős--Rosenfeld Problem
#835.
