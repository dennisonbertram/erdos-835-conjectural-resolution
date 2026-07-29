# Independent audit: common odd transversals and local links

Date: 2026-07-29

## Verdict

The corrected unconditional theorems in `PROOF.md` are valid. They do not
resolve Erdős--Rosenfeld #835 or the common odd-transversal conjecture.

The audit found and corrected three scope or implementation defects:

1. primality of \(k+1\) is equivalent to the standard divisibility
   conditions, not to existence of the Steiner system;
2. Theorem 6.1 proves a counting upper bound of \(k+1\), not unconditional
   attainment of that bound;
3. the original Part E verifier parser treated colour \(0\) alone as
   residual, whereas the authenticated partial has fifteen complete
   285-block colours and residual labels \(-1,0,13\).

After those corrections, all asserted executable checks pass. The run also
shows that the proposed stronger LLS-span statement fails on both available
controls; the weaker Local Link Sufficiency conjecture remains open.

## Independent proof checks

I checked the following steps.

1. At the top rung, \(\delta_{k-1}a\) restricts to one on the deleted
   systems exactly when \(a\) is a common odd transversal. Simplex exactness
   converts this to the stated cocycle condition.
2. Every \((k+1)\)-set contains exactly two residual \(k\)-sets. Reindexing
   it by their intersection and union gives the same residual edge once in
   each direction, so the affine cocycle equations are exactly the proper
   two-colouring equations.
3. The intersection generating function in Theorem 2.1 follows from
   \[
   [z^k](1+z)^k(1+xz)^k
   =\sum_i\binom ki^2x^i.
   \]
   Its \(i=0\) coefficient gives complement closure, and the \(i=1,k-1\)
   coefficients give the stated zero-or-\(k\) values.
4. The Lucas/Kummer calculation proves that all derived
   \(\lambda_j\)'s are integral exactly when \(k+1\) is prime. It supplies
   no design-existence implication, now stated explicitly.
5. Linking \(r\) disjoint \(S(t,t+1,n)\)'s at an \(s\)-set gives \(r\)
   block-disjoint \(S(t-s,t+1-s,n-s)\)'s. At \(s=t-1\), deleting the
   \(p-2\) one-factors from \(K_{p+1}\) leaves a 2-factor.
6. The line graph of each link 2-factor embeds in the residual conflict
   graph with cycle lengths preserved. Hence any odd link cycle is a valid
   local non-extension certificate.
7. The authenticated Etzion--Hartman labels
   \(\{0,14,17\},\{2,14,17\},\{5,14,17\}\) become the triangle
   \(0,2,5\) in the link at \(\{14,17\}\); the corrected verifier confirms
   this directly from all 4,845 block rows.
8. At the top rung, complementation preserves residual vertices and edges
   and acts freely. If the residual graph is bipartite, each colour class is
   itself an \(S(k-1,k,2k)\), hence is complement-closed. Therefore every
   proper colouring descends to the quotient. This special argument avoids
   the false general claim that bipartiteness always descends through a
   free double cover.
9. An odd walk from a residual block to its complement contradicts that
   invariant proper colouring, so Corollary 4.2 is sound.
10. The small-parameter vacuity theorem correctly uses the link operation
    and the cited packing/nonexistence results for \(k=4,6,10,12\). Its
    conclusion is only that the common-transversal premise has no known
    nontrivial decided instance.
11. The corrected Theorem 6.1 is only the block-count upper bound. Under a
    hypothetical top large set, Theorem 3.1 produces \(k+1\) derived
    systems, which meet that bound and therefore form the lower-rung large
    set. The conditional propagation theorem remains valid.

## Executable audit

I ran:

```sh
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  collaboration/opus5/common_odd_transversal_2026-07-29/\
verify_common_odd_transversal.py

ruff check \
  collaboration/opus5/common_odd_transversal_2026-07-29/\
verify_common_odd_transversal.py
```

The verifier reported `ALL CHECKS PASS`, including:

- divisibility-admissibility for every even \(k\le80\);
- both intersection profiles on \(S(3,4,8)\) and \(S(5,6,12)\);
- exhaustive disjointness maxima for the 30 labelled Fano planes and 30
  labelled \(S(3,4,8)\)'s;
- a constructed \(LS(2,3,9)\) positive control;
- the complete Etzion--Hartman residual census and link triangle.

The measured cycle-space data are:

| control | \(\dim L\) | \(\dim Z_1(G)\) | result |
|---|---:|---:|---|
| \(LS(2,3,9)\), five systems | 11 | 13 | \(L\ne Z_1\), \(G\) bipartite |
| Etzion--Hartman, fifteen systems | 467 | 587 | \(L\ne Z_1\), \(G\) non-bipartite |

Thus link cycles do not span the full cycle space on either control. The
weaker implication “all link cycles even \(\Rightarrow G\) bipartite” is
consistent with both examples but remains unproved.

## Exact remaining gap

No top-rung partial with \(k-1\) systems is known for any unresolved
parameter, and no theorem rules out such partials uniformly. A decisive
result still requires an unrestricted construction or a universal
nonexistence mechanism. The common odd-transversal conjecture and Local Link
Sufficiency are research directions, not completed steps.
