# Recent-status audit for Erdős Problem #835

Audit time: 26 July 2026, approximately 19:03 EDT.

This is a read-only novelty/status check, not mathematical evidence for or
against the conjecture.

## Official problem record

The current indexed copy of
[Erdős Problem #835](https://www.erdosproblems.com/835) labels the problem
**Open** and states the same existential Johnson-graph question studied in
this repository.  The indexed page says it was last edited on 22 January
2026.  It also records the Ma--Tang prime sieve and says the listed chromatic
numbers exclude \(3\leq k\leq8\).

The current
[problem discussion](https://www.erdosproblems.com/forum/thread/835?order=oldest)
explicitly says that no partial or complete solution is claimed in its
comments.  Its latest visible comment is dated 30 May 2026.  The discussion
contains useful partial structure, including complement closure in the
remaining prime cases and the derived \(S(4,5,21)\) boundary at \(k=16\),
but no resolution.

The site itself returned HTTP 403 to a direct automated fetch, so this audit
used the search engine's current indexed copy.  That limitation matters:
the check confirms the indexed public status, not an unpublished result.

## X/Twitter recent search

The connected X API recent-search endpoint was queried over its seven-day
window with six independent query families:

1. `"Erdos Problem 835" OR "Erdős Problem 835"`
2. `"Erdos-Rosenfeld" OR "Erdős–Rosenfeld" OR "Erdős Rosenfeld"`
3. `"J(2k,k)" OR "Johnson graph J(2k,k)"`
4. `"χ(J(2k,k))" OR "chi(J(2k,k))"`
5. `(Johnson graph chromatic) (k+1 OR coloring OR colouring)`
6. `(Erdos 835 OR Erdős 835) (proof OR solved OR solution)`

Queries 1, 3, 4, and 5 returned zero posts.  Queries 2 and 6 returned only
two records: Dennison Bertram's 24 July 2026 post
([post 2080780379410342374](https://x.com/i/web/status/2080780379410342374))
about the distinct covering problem reached while working on #835, and one
retweet of that post.  Neither record claims a solution of #835 itself.

## Conclusion

No recent X post in the API's seven-day window claimed a proof or
construction for #835, and the official indexed record still labels it
open.  This is the strongest honest conclusion available from these
searches.  Absence from a recent social-media search cannot prove global
priority or rule out private, unindexed, or differently worded work.
