# Perfect-information closure of the dim-2 shortening route

Date: 2026-07-25.  Status: **proved route closure; not a nonexistence
proof for \(S(14,15,31)\) and not a solution of Problem 835.**
Validator: `verify_s141531_dim2_perfect_info_closure.py`
(single-threaded; per-tuple table `s141531_dim2_margins.csv`, SHA-256
`0982008c066a55a0fb436b75710b9997696a6bfe1c4a41ad840894f69bf1b578`).
Supersedes, for \(m=2\), the independent-endpoint no-go of
`s141531_griesmer_averaging_no_go.md`.

## Theorem (m=2 closure under arbitrary coupling)

For every dimension-2 subspace \(H\) of the even point-incidence code
of a hypothetical \(S(14,15,31)\) and **every joint resolution of all
size-16 Fourier uncertainties** (that is, any consistent assignment of
which complementary 15-sets are blocks), the common-zero shortening
satisfies the Griesmer bound with slack at least
\[
 L-G(d,28)\ \ge\ 14\,940 .
\]
Hence no dimension-2 common-zero shortening can yield a Griesmer
contradiction, even with perfect coupled information.

## Proof organization

All 1,450 labelled column tuples; kernel dimension is exactly 2 for
every tuple (Griesmer on removed positions), so the image dimension is
exactly \(k=28\) everywhere.

1. 1,092 tuples with no weight-16 words in \(H\): length \(L\) exact,
   and an explicitly realized coset weight \(D_{\rm up}\) (from a
   size-16-free coset) upper-bounds the shortened distance for every
   resolution.  Direct check: \(G(D_{\rm up},28)-L\le-14\,940\).
2. 358 tuples with weight-16 words in \(H\): with
   \(B=\sum_{h\in H}F(h)=B_{\rm lo}+2^{15}a\), \(0\le a\le A\)
   (\(A\) = number of weight-16 words of \(H\)), the length is
   \(L=B/4\) and each coset weight is \((B-S_p)/8\), sharing the same
   \(B\).  For every resolution the margin obeys
   \[
    G(d,28)-L\ \le\
    \min_p\max_{0\le a\le A}
    \Big[G\big(\lfloor\tfrac{B_{\rm lo}+2^{15}a-S_{p,\rm lo}}8\rfloor,28\big)
      -\lfloor\tfrac{B_{\rm lo}+2^{15}a}4\rfloor\Big],
   \]
   valid because coset-word uncertainties are disjoint from \(H\)'s
   (endpoints conservative) and every coset word restricts nonzero to
   \(Z_H\) (global \(d_{\rm lower}=1\,975\,240>0\)).  Max over the 358
   tuples: \(-14\,940\).
   (Caution recorded: naively decoupling \(B\) between length and
   coset weight would reach \(+9\,372\) at tuple \((7,8,8,8)\) — an
   artifact of pairing inconsistent resolutions; the shared-\(B\)
   coupling is what closes it.)

Fourteen tuples tie at the extremal margin \(-14\,940\), e.g.
\((4,9,9,9)\): \(L=4\,419\,387\) exact, realized \(D_{\rm up} =
2\,202\,216\), \(G=4\,404\,447\).

## Scope

Route closure only.  Unaffected: dimensions \(m\ge3\) under coupling
(only two sampled dim-3 profiles exist, margins \(-26\,669\) and
\(-23\,291\), not exhaustive); bounds stronger than Griesmer (any
successful one must beat it by at least \(14\,940\) at \(m=2\));
non-common-zero shortenings; and the design's existence.  The number
\(14\,940\) is the exact quantitative target any stronger
coding-theoretic bound must clear at \(m=2\).
