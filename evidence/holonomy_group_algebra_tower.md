# The exact holonomy tower and its augmented cocycle

Date: 2026-07-27

Status: **proved necessary identities; not a resolution of Problem #835.**

Verifier:

```text
python3 -B evidence/verify_holonomy_group_algebra_tower.py
```

This note strengthens the cycle-type holonomy identity in
`collaboration/opus5/unrestricted_ls3420_attack_2/NOTE.md`, Theorem 7.  The
strengthening is exact and solver-free.  The subsequent independent analysis
in `collaboration/opus5/holonomy_followup/NOTE.md` proves that the tower
identity itself holds for arbitrary chart families and is therefore pure
gauge; it also determines the complete universal affine mod-\(2\) census
arithmetic at \(K_{18}\).  The labelled cocycle and pseudogluing controls below
remain useful route delimiters, but no contradiction is presently known.

## 1. Setup

Let \(c:\binom X{t+1}\to[m]\) be an \(LS(t,t+1,v)\) colouring.  For each
\(t\)-set \(T\), write

\[
 \chi_T:X\setminus T\longrightarrow[m],\qquad
 \chi_T(x)=c(T\cup\{x\}).
\]

Every \(\chi_T\) is a bijection.  For \(R\in\binom X{t-1}\) and distinct
\(a,b\in X\setminus R\), put

\[
 \sigma_R(a,b)=\chi_{R\cup\{b\}}\chi_{R\cup\{a\}}^{-1}\in S_m.
\]

As usual, the common colour \(d=c(R\cup\{a,b\})\) is fixed when the partial
composition is extended to all of \([m]\).  We retain the orientation:
\(\sigma_R(b,a)=\sigma_R(a,b)^{-1}\).

The fixed colour is unique.  If \(e\ne d\), put
\(x=\chi_{R\cup\{a\}}^{-1}(e)\).  Then \(x\ne b\).  If
\(\sigma_R(a,b)(e)=e\), the two blocks \(R\cup\{a,x\}\) and
\(R\cup\{b,x\}\) would have the same colour while sharing the \(t\)-set
\(R\cup\{x\}\), contradicting the rainbow-star property.

Define the exact holonomy sum

\[
 H(c)=\sum_{\substack{R\in\binom X{t-1}\\
                       a,b\in X\setminus R,\ a\ne b}}
       [\sigma_R(a,b)]\ \in\mathbb Z[S_m],
 \tag{1}
\]

where \([g]\) is the basis element indexed by the *labelled* permutation
\(g\).  Thus (1) remembers which colour is sent to which colour.  Passing to
conjugacy classes recovers twice the unordered cycle-type census.

## 2. Exact group-algebra tower identity

> **Theorem 1.**  If \(t\ge2\), then
> \[
>   \sum_{p\in X} H(c^{\,p})=(t-1)H(c)
>   \qquad\text{in }\mathbb Z[S_m].
>   \tag{2}
> \]

**Proof.**  A summand of \(H(c^{\,p})\) is indexed by
\((R',a,b)\), where \(|R'|=t-2\) and \(p,a,b\) are outside \(R'\).  From the
definition of the derived colouring,

\[
 \sigma^{\,c^p}_{R'}(a,b)
 =\chi^c_{R'\cup\{p,b\}}
  \bigl(\chi^c_{R'\cup\{p,a\}}\bigr)^{-1}
 =\sigma^c_{R'\cup\{p\}}(a,b).
\]

Conversely, a fixed top summand \((R,a,b)\) occurs once for every \(p\in R\),
and \(|R|=t-1\).  This is an equality of the exact labelled permutations, not
only of their conjugacy classes.  Summing gives (2). \(\square\)

The proof is purely an indexing double count once the star charts and their
transition permutations are defined; it uses no additional compatibility
between different \(R\)'s.  Thus (2) is a bookkeeping law, not a standalone
obstruction.  Its only possible force is as a compatibility test on
independently proposed derived links.

For a putative \(LS(3,4,20)\), (2) says

\[
 \sum_{p\in X} H(c^{\,p})=2H(c).
 \tag{3}
\]

Consequently, after the twenty \(LS(2,3,19)\) links have been aligned in the
single inherited set of seventeen colour labels, the total coefficient of
**every** \(g\in S_{17}\) is even.  The cycle-type projection has **55**
coordinates: every holonomy has exactly one fixed colour, so its remaining
cycle lengths form a fixed-point-free partition of 16.  These 55 parity
conditions are the central projection of the coefficientwise conditions.

The common colour alignment is essential.  An isolated derived large set may
have its colours relabelled, conjugating every coefficient of \(H\).  Twenty
abstract \(LS(2,3,19)\) objects can be tested against (3) only after choosing
the conjugations that identify all of their colour sets with the one top-level
colour set.

Any integral linear representation or permutation module of \(S_m\) gives a
smaller necessary matrix identity by applying it to (2).  Unlike a character,
a matrix representation need not discard the global colour alignment.

The natural \(m\)-point permutation representation, however, is universally
flat and therefore gives no information.  For a fixed \(R\) and colours
\(\alpha,\beta\), fix \(a\) and let
\(x=\chi_{R\cup\{a\}}^{-1}(\alpha)\).  As \(b\) ranges over
\(Y\setminus\{a\}\), the values \(\sigma_R(a,b)(\alpha)\) run through every
colour exactly once: \(b=x\) gives \(\alpha\), while the other \(b\)'s see all
other colours on the edges incident with \(x\).  Hence

\[
 \rho_{\rm nat}(H_R)=(m+1)J_m
 \tag{4}
\]

for every local one-factorization, where \(J_m\) is the all-one matrix.
Noncentral projections must start above the natural module to add information.

There is a more informative, overlap-resolved form.  Let \(H_R(c)\) denote the
part of (1) with its first index fixed to \(R\).  At the
\(LS(3,4,20)\) rung, for every pair of distinct points \(p,q\),

\[
 H_{\{q\}}(c^{\,p})=H_{\{p\}}(c^{\,q})
                  =H_{\{p,q\}}(c).
 \tag{5}
\]

Indeed, all three expressions are computed from the same labelled
one-factorization

\[
 \{a,b\}\longmapsto c(\{p,q,a,b\})
\]

of \(K_{18}\) on \(X\setminus\{p,q\}\).  Summing (5) over the 190 pairs gives
(3), but (5) retains which two links must agree.  It supplies a finite
fingerprint screen for trying to glue twenty \(LS(2,3,19)\) links.

Even all 190 equalities (5) are insufficient.  Let \(L\) be any fixed
\(LS(2,3,19)\) on a 19-point set \(P\), and let
\(\ell:\binom{[20]}2\to P\) be a one-factorization of \(K_{20}\).  At each
point \(p\), the map

\[
 f_p(q)=\ell(\{p,q\})
\]

is a bijection from \([20]\setminus\{p\}\) to \(P\).  Transport \(L\) through
\(f_p\) to obtain a genuine \(LS(2,3,19)\), denoted \(L_p\).  For an edge
\(\{p,q\}\) labelled \(r\), the \(q\)-root fingerprint in \(L_p\) and the
\(p\)-root fingerprint in \(L_q\) are both the same point-relabel-invariant
quantity \(H_r(L)\).  Thus the twenty genuine links pass all 190 exact local
fingerprint equalities.

For the repository's cyclic \(L\) and the deterministic round-robin
factorization of \(K_{20}\), these links nevertheless disagree on 27,478 of
the 29,070 pairwise overlap comparisons (and agree on only 1,592).  Therefore
local \(H_R\) forgets decisive information: it sums over which base pair
produced each permutation.  A successful obstruction must retain that
point-labelled correspondence or an equally strong substitute.

At the opposite extreme, retaining every indexed
\(\sigma_R(a,b)\) is lossless but tautological.  Its unique fixed colour is
exactly \(c(R\cup\{a,b\})\), so the indexed holonomy array directly recovers
the entire one-factorization.  For two derived links, equality of their
indexed arrays is therefore equivalent to the original cellwise overlap
condition.  The unresolved target is a genuine intermediate compression:
stronger than the aggregate \(H_R\), but not merely a renaming of all original
colours.

As a finite control, the cyclic \(LS(2,3,19)\) used in the repository has
5,814 oriented holonomy summands and 5,814 distinct exact permutations: every
coefficient of its \(H\) is one.  Its central projection has only 34 nonzero
cycle types.  Thus the exact lift is dramatically finer on this example, even
though the explicit pseudogluing proves that even its overlap-resolved local
fingerprints are insufficient.

## 3. The augmented transition cocycle

For a fixed \(R\), let \(Y=X\setminus R\), so \(|Y|=m+1\).  The colours
\(c(R\cup\{a,b\})\) form a one-factorization of the complete graph on \(Y\).
Adjoin a symbol \(\infty\) and extend each star chart to a bijection

\[
 \widehat\chi_a:Y\longrightarrow[m]\cup\{\infty\},\qquad
 \widehat\chi_a(a)=\infty,\quad
 \widehat\chi_a(x)=c(R\cup\{a,x\})\ (x\ne a).
\]

Put

\[
 \tau_R(a,b)=\widehat\chi_b\widehat\chi_a^{-1}\in S_{m+1}.
\]

> **Theorem 2.**  For distinct \(a,b,c\in Y\),
> \[
>  \tau_R(b,c)\tau_R(a,b)=\tau_R(a,c).
>  \tag{6}
> \]
> If \(d=c(R\cup\{a,b\})\), and \(\sigma_R(a,b)\) is extended to fix
> \(\infty\), then
> \[
>  \tau_R(a,b)=(\infty\ d)\sigma_R(a,b).
>  \tag{7}
> \]

**Proof.**  Equation (6) follows by cancelling
\(\widehat\chi_b^{-1}\widehat\chi_b\).  For (7), both sides agree with
\(\sigma_R(a,b)\) away from \(d,\infty\); the left side sends
\(d\mapsto\infty\) and \(\infty\mapsto d\).  The permutation
\(\sigma_R(a,b)\) fixes both \(d\) and \(\infty\), so the displayed factors
commute. \(\square\)

Replacing the distinguished fixed point \(d\) of \(\sigma\) by the 2-cycle
\((\infty\,d)\) gives the cycle type of \(\tau\).  Therefore the *unpointed*
cycle type of \(\tau\) is in bijection with the cycle type of \(\sigma\): it
does not strengthen the 55 central conditions.  The useful information, if
any, must retain the labelled transition, its distinguished common colour, or
the simultaneous cocycle relations.

The augmented transitions also satisfy a positive-semidefinite
group-algebra law.  Choose \(a_0\in Y\), let
\(g_a=\widehat\chi_a\widehat\chi_{a_0}^{-1}\), and put
\(G_R=\sum_a[g_a]\).  With \(^{*}\) denoting inversion,

\[
 \sum_{a\ne b}[\tau_R(a,b)]+(m+1)[e]=G_RG_R^{*}.
 \tag{8}
\]

Thus every unitary representation sends the left side of (8) to a positive
semidefinite matrix.  This is a law for the augmented \(\tau\)-sum, not
directly for \(H_R\): the transposition \((\infty\,d)\) in (7) varies with the
edge.  At the central character level, one may transfer the inequality by
replacing the unique 1-cycle of \(\sigma\) with a 2-cycle.

## 4. What is and is not proved

Proved:

1. the exact coefficientwise tower identity (2);
2. its coefficient-parity consequence (3) for any \(LS(3,4,20)\);
3. the universal flatness (4) of the natural representation;
4. the overlap-resolved equality (5) and an explicit twenty-link
   pseudogluing proving that even local exact-\(H\) fingerprints are too weak;
5. the augmented pure-gauge cocycle (6), its exact relation (7) to the
   earlier holonomy;
6. the positive-semidefinite autocorrelation identity (8);
7. finite replay of these identities on genuine \(LS(2,3,9)\) and the
   repository's cyclic \(LS(2,3,19)\).

Not proved:

1. that the twenty required \(LS(2,3,19)\) links exist simultaneously;
2. any obstruction from nonlinear, integral, positivity, or jointly attainable
   holonomy data beyond (3); the follow-up note proves that projections of
   (3) itself cannot be inconsistent;
3. existence or nonexistence of \(LS(3,4,20)\);
4. existence or nonexistence of \(LS(15,16,32)\), and therefore Problem #835.
