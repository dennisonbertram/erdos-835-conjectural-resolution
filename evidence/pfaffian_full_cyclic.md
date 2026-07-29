# Exact cyclic screen for the full four-Pfaffian condition

For the descended \(p=17\) problem, a putative alternating \(20\times20\)
matrix must have zero row sums.  This note examines the translation-invariant
subfamily on \(\mathbb Z/(p+3)\):

\[
A_{ij}=f(j-i),\qquad f(-d)=-f(d),\qquad f((p+3)/2)=0.
\]

It automatically satisfies \(A\mathbf1=0\).  It has
\((p+1)/2-1\) parameters: 3, 4, 6, and 9 at \(p=5,7,11,17\), respectively.
Because a global nonzero scalar multiplies every principal 4-Pfaffian by a
square, the exact predicate is projective in the coefficient vector.

`search_pfaffian_full_cyclic.py --controls` enumerates every nonzero
projective coefficient vector at the \(p=5,7,11\) controls.  It does not use
moments: on every translation orbit of 3-stars it directly checks that the
\(p\) outside 4-Pfaffians are pairwise distinct.  Translation invariance
makes those orbit representatives equivalent to all stars.

```bash
python3 evidence/search_pfaffian_full_cyclic.py --controls
python3 evidence/search_pfaffian_full_cyclic.py --sample-17 1000000 --seed 835
```

The \(p=17\) projective cyclic space has
\((17^9-1)/16=7{,}411{,}742{,}281\) points, far too large for the included
unaccelerated exhaustive pass.  Its sample mode is
deterministic and reports the best prefix of the exact orbit-star test, but
is evidence only.

## Scope

An exhaustive rejection in this note rules out only skew-circulant descended
matrices.  It neither rules out an arbitrary \(20\times20\) alternating
matrix nor lifts a descended candidate to a \(32\times32\) principal-
Pfaffian colouring.  A descended candidate is necessary for the original
ansatz, but still has to satisfy the remaining 15-subset stars of a lift.
