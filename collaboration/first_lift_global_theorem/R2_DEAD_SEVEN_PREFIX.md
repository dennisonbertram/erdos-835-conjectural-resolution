# A dead but fully completable seven-prefix for \(r=2\)

Date: 2026-07-28.

## Result and scope

There is an exact \(n=13,q=17\) class-B support instance with profile
\[
(n_8,n_{10},n_{12})=(9,6,2)
\]
and seven pairwise edge-disjoint support matchings of type
\[
8^4\,10\,12^2
\]
such that none of the ten remaining supports has a perfect matching avoiding
the prefix.

The same support matrix nevertheless has a separate literal decomposition of
all 78 edges of \(K_{13}\) into its seventeen prescribed matchings. This is a
dead arbitrary prefix, not a noncompletable class-B instance. It rules out
blind arbitrary-prefix induction for \(r=2\), while leaving coordinated
choice and switching open. No class-B-prime or fan realization is asserted.

## Explicit certificate

On vertices \(0,\ldots,12\), take the seven prefix matchings
\[
\begin{array}{c|l}
0&25,\ 34,\ 9\,12,\ 10\,11\\
1&02,\ 45,\ 79,\ 11\,12\\
2&15,\ 24,\ 8\,12,\ 9\,11\\
3&01,\ 35,\ 78,\ 10\,12\\
4&03,\ 12,\ 6\,11,\ 7\,10,\ 89\\
5&05,\ 14,\ 23,\ 7\,12,\ 8\,11,\ 9\,10\\
6&04,\ 13,\ 29,\ 6\,12,\ 7\,11,\ 8\,10.
\end{array}
\]
They have sizes \(4,4,4,4,5,6,6\) and 33 distinct edges.

The complements of the ten unselected supports are
\[
\begin{gathered}
02345,\ 12345,\ 0145\,11,\ 279\,10\,11,\ 0123\,12,\\
789,\ 9\,10\,11,\ 78\,12,\ 8\,10\,12,\ 9\,11\,12.
\end{gathered}
\]
The first five have size five and the last five have size three. Together
with the selected supports, they give profile \((9,6,2)\), and every vertex
belongs to exactly twelve supports.

This certificate can also be viewed as a one-edge lift of the \(r=1\) dead
prefix: add edge \(29\) to a selected size-ten layer and add its endpoints
to the corresponding remaining triple complement \(7\,10\,11\). Both
operations change the appropriate colour size by two and preserve the exact
remaining-complement identity
\[
\#\{\text{remaining complements containing }v\}=d_F(v)-2.
\]

## Verification and full completion

`verify_r2_dead_seven_prefix.py` uses only the Python standard library. It
reconstructs the two round-robin colourings, the seven prefix layers, and all
seventeen supports. It then:

- checks the support profile and all thirteen row sums;
- enumerates every perfect matching of each remaining support and confirms
  that all ten are blocked;
- checks a separate literal family of seventeen support-perfect matchings;
  and
- verifies that their 78 distinct edges are exactly \(E(K_{13})\).

`search_r2_dead_seven_prefix.py` is the exact CP-SAT/CEGAR discovery replay.
Its master models the seven disjoint matching layers, ten complement rows,
and the exact complement-degree identity. Whenever a candidate remaining
support has a residual perfect matching, the search adds a conditional
matching cut for that exact complement. The packaged witness is supplied as
a zero-distance hint, so the reproducible SAT run terminates in one round;
the standard-library verifier, not the CP-SAT status, is the durable proof.

This result settles only the arbitrary-prefix boundary. It does not prove or
disprove that every \(r=2\) support instance admits some coordinated
eight-matching prefix.
