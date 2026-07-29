VERDICT: NOT SOLVED — Erdős--Rosenfeld Problem #835 remains open.

# Status: conflict-cohomology attack

Date: 2026-07-29.

## Exact result

The residual bipartiteness question has been converted, with proofs in
`PROOF.md`, into three exactly equivalent forms:

\[
G_{\cal E}\text{ bipartite}
\iff
H_{\cal E}x={\bf1}\text{ soluble}
\iff
{\bf1}_{\cal D}\in\operatorname{row}M_{\cal D}.
\]

Here \(M_{\cal D}\) is the \((t+2)\)-set-versus-deleted-\((t+1)\)-block
incidence matrix.  The dual obstruction is an odd vector

\[
y\in\ker M_{\cal D},
\]

equivalently an odd binary Steiner trade supported on the \(p-2\) deleted
systems after complementation at the top rung.  At a general rung it is an
upward-incidence cochain cocycle, not the usual downward-incidence trade.
Full-simplex exactness proves that every such \(y\) is
\(y=\delta z\) for a residual cycle vector \(z\), and

\[
|y|\equiv|z|\pmod2
\]

because \(n-t=p\) is odd.

This is an exact certificate translation.  It is not a new uniform
obstruction: odd deleted cocycles (top-rung trades after complementation)
and odd residual cycles contain precisely the same unresolved information.

The exact rank formula is

\[
\operatorname{rank}_2 M_{\cal D}
=\binom{n-1}{t+1}-c(G_{\cal E}).
\]

Thus rank records only the number of residual components and cannot detect
bipartiteness; the affine row-space membership is the essential condition.

## Top rung

At \(t=p-2\), write \(k=p-1\).  Complement closure transforms the row-space
condition into the following exact problem.

Each of the \(k-1\) deleted \(S(k-1,k,2k)\)'s partitions
\(\binom X{k-1}\) into \(C_k\) cells of size \(k\).  The residual graph is
bipartite exactly when there is a binary point set meeting every cell of
every partition oddly.

The immediate top-rung tests are vacuous:

* every \((k+1)\)-set contains exactly one block from each deleted system,
  hence \(k-1\) deleted and two residual facets;
* every matrix row has odd weight \(k-1\), every column has even weight \(k\);
* \(C_k\) is even for even \(k\);
* the forced kernel vectors obtained by adding two complete design
  indicators have even weight.

Therefore any genuine negative proof must find an additional odd trade
forced by the full mutual geometry of the deleted systems.  No such uniform
trade was proved here.  Conversely, proving a common odd transversal always
exists would only show that \(k-1\) disjoint systems extend; it would not
construct those systems.

There is one nontrivial support restriction.  A self-contained unitrade-gap
argument proves that any nonzero binary \((k-1)\)-trade has either \(k+1\)
blocks, namely all facets of one \((k+1)\)-set, or at least \(2k\) blocks.
Each top face contains only \(k-1\) deleted blocks, so the first possibility
cannot be supported on the deleted systems.  Potapov's equality
classification says that every weight-\(2k\) unitrade is the symmetric
difference of two complete facet families; it contains \(k\) facets of one
top face and is therefore excluded by the same \(k-1\)-facet count.  Thus
every nonzero deleted-support kernel vector, and in particular every odd
obstruction, has at least \(2k+1\) blocks—at least \(33\) in the first open
case \(k=16\).  This does not prove that an obstruction exists.

## Controls

`verify_cochain_controls.py` passed all exact checks.

Positive control:

* constructs \(LS(2,3,9)\) from the \(840\) labelled \(STS(9)\)'s;
* deletes five classes;
* obtains a \(126\times60\) matrix of rank \(55\);
* explicitly expresses the deleted all-one vector as the sum of \(48\)
  matrix rows.

Negative fixed-partial control:

* authenticates the Etzion--Hartman 15-system partial at
  \((t,v,p)=(3,20,17)\);
* starts with its explicit three-edge residual triangle;
* computes \(y=\delta z\), an odd \(45\)-block vector supported on the
  \(4\,275\) deleted blocks;
* checks \(\delta y=0\) on all \(\binom{20}{5}=15\,504\) five-sets.

The negative control applies only to that fixed partial and does not rule
out \(LS(3,4,20)\).

## Scope relative to #835

No unrestricted value of \(k\) is resolved.  The first open case remains
\(k=16\), equivalently \(p=17\) and \(LS(15,16,32)\).

The precise remaining top-rung question is:

> Must every family of \(k-1\) pairwise disjoint,
> complement-closed \(S(k-1,k,2k)\)'s support an odd binary trade, or can such
> a family admit a common odd transversal?

This question is equivalent to the residual conflict obstruction once the
partial family is given.  It is still open.

No existing repository file was edited, and no commit was made.
