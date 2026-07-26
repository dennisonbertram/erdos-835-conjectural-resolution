# LS(3,4,20): an exact 28-branch reduction

## Scope

This note concerns only the necessary \(k=16\) shadow
\(LS(3,4,20)\).  It does not establish existence or nonexistence.
Nonexistence would exclude \(k=16\) only; existence would be only a
necessary shadow and would not solve Erdős--Rosenfeld Problem #835.

The canonical CNF and its 55 second-star branches were independently
rechecked before deriving the reduction below.  Their encodings are sound.
The new result is that the unused point symmetry cuts the exhaustive sweep
from 55 branches to 28.  In particular, branch 54 is not needed.

Verifier:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/ls3420_structural_attack/verify_ls3420_even_flag_reduction.py
```

The verifier is standard-library only, launches no solver, writes no files,
and reads the existing branch manifest and Etzion--Hartman partial read-only.

## The four-bijection lemma

Let
\[
 c:\binom{V}{4}\longrightarrow {\cal C},\qquad |V|=20,\quad |{\cal C}|=17,
\]
be an \(LS(3,4,20)\) colouring: the seventeen extensions of every triple
have all seventeen colours.

Fix a four-set \(B\subset V\), put \(\alpha=c(B)\), and let
\(Y=V\setminus B\), so \(|Y|=16\).  For every \(i\in B\), define
\[
 \mu_i:Y\longrightarrow {\cal C}\setminus\{\alpha\},\qquad
 \mu_i(y)=c\bigl((B\setminus\{i\})\cup\{y\}\bigr).
 \tag{1}
\]
Each \(\mu_i\) is a bijection.  Its values avoid \(\alpha\), since the
corresponding block and \(B\) share the triple \(B\setminus\{i\}\).
Two different inputs give different values because their blocks share that
same triple.  The domain and codomain both have size sixteen.

For distinct \(r,q\in B\), put
\[
 \pi_{r,q}=\mu_q^{-1}\mu_r\in\operatorname{Sym}(Y).
 \tag{2}
\]
This is a derangement: for every \(y\in Y\), the blocks
\((B\setminus\{r\})\cup\{y\}\) and
\((B\setminus\{q\})\cup\{y\}\) share the triple
\((B\setminus\{r,q\})\cup\{y\}\), so their colours differ.

It is exactly a row permutation of the existing second-star construction.
Take
\[
 T=B\setminus\{q\},\qquad e=B\setminus\{r,q\}.
\]
Normalize colours by the extension star of \(T\), choose \(e\) as the
second-star pair, and choose \(q\) as the row point.  On \(Y\), that row is
\(\pi_{r,q}\).  Exchanging \(r\) and \(q\) replaces the row by its inverse.

## Parity obstruction and the 28 branches

Give \(Y\) and \({\cal C}\setminus\{\alpha\}\) arbitrary fixed orders.  The
four bijections \(\mu_i\) have four signs in \(\{+1,-1\}\).  Two have the
same sign, say \(\mu_r,\mu_q\).  Consequently
\[
 \operatorname{sgn}(\pi_{r,q})
 =\operatorname{sgn}(\mu_q)^{-1}\operatorname{sgn}(\mu_r)
 =+1.
 \tag{3}
\]
Thus every hypothetical \(LS(3,4,20)\), around every chosen four-set, has
an **even** second-star flag.

The point group \(\operatorname{Sym}(20)\), unused by the canonical CNF's
colour normalization, maps the chosen data
\[
 (e,r,q,Y)\longmapsto(\{0,1\},2,3,\{4,\ldots,19\}).
 \]
The colour group then normalizes the root star, and the remaining
\(\operatorname{Sym}(16)\) conjugates \(\pi_{r,q}\) to the canonical
representative of its cycle type.  This is exactly the normalization used
by the existing branch CNFs.

A derangement of sixteen points with \(s\) cycles has sign
\[
 (-1)^{16-s}=(-1)^s.
 \]
Hence an even row has an even number of cycles.  Of the 55 partitions of
16 with all parts at least two, exactly 28 have an even number of parts.
Therefore the following existing branch IDs are already an exhaustive
LS(3,4,20) sweep:

```text
0, 3, 4, 5, 7, 11, 12, 15, 17, 18, 19, 23, 24, 25,
27, 28, 33, 35, 36, 37, 39, 43, 44, 48, 50, 51, 52, 53
```

No new CNF is required.  The other 27 current branches are
symmetry-redundant.  In particular, branch 54 has cycle type \((16)\), an
odd permutation, and can be dropped from an exhaustive sweep.

Equivalently, branch 54 cannot be the globally selected even flag.  This is
not an UNSAT proof for the current labelled branch-54 CNF: a model of that
CNF would necessarily contain another flag of even type and could be
relabelled into one of the 28 branches above.

There is also a concrete branch-54 local invariant.  For its canonical data,
take \(B=\{0,1,2,3\}\).  The fixed row is
\(\pi_{2,3}=\mu_3^{-1}\mu_2\), which is odd, so \(\mu_2\) and \(\mu_3\)
have opposite parity.  Among the other five unordered pairs in this same
four-set, exactly two or three have even relative permutation.  Thus every
model of the labelled branch-54 CNF exposes at least two even flags already
around \(0123\); no global scan is needed to find a relabelling into the
28-branch sweep.

## The Etzion--Hartman partial moves from branch 54 to branch 0

The checked 4,773-block Etzion--Hartman partial is in branch 54 for the
previous fixed choice
\[
 (T,e,q)=(012,01,3).
 \]
That is a statement about its current labels, not its point-symmetry orbit.

The same partial has the fully assigned flag
\[
 B=\{0,4,5,9\},\qquad
 T=\{0,4,5\},\qquad e=\{0,5\},\qquad r=4,\qquad q=9,
\]
for which \(\pi_{r,q}\) has cycle type
\[
 (2,2,2,2,2,2,2,2),
\]
the canonical branch 0 type.  The verifier constructs a deterministic
point map sending this flag to \((012,01,3)\), constructs the forced colour
map from the new root star, transforms all 4,845 entries in memory, and
checks:

* 4,773 assigned blocks and 72 holes are preserved;
* every partially assigned triple star remains conflict-free;
* the transformed root star has the canonical colour order;
* all sixteen transformed second-star units equal the existing branch-0
  representative.

Therefore a completion search targeted at this near-solution can use an
isomorphic branch-0 hint.  The old branch-54 targeting is valid in its fixed
labels, but it is not the strongest symmetry reduction.

## What this proves

It proves a lossless reduction from 55 to 28 existing CNF branches and gives
an exact branch-0 relabelling of the Etzion--Hartman near-completion.  It
does not prove any branch SAT or UNSAT, does not construct
\(LS(3,4,20)\), and does not establish its nonexistence.
