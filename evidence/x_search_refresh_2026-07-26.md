# X claim-search refresh, 2026-07-26

This is a narrow public-claim check, not mathematical evidence and not proof
of priority or absence.  The X API recent-search endpoint covers only the
rolling seven-day window and can miss deleted, private, unindexed, differently
worded, or off-platform work.

The following four read-only queries were run on 2026-07-26, with retweets
excluded and up to 100 results requested per query:

1. `"Erdos problem 835" OR "Erdős problem 835" OR "Erdos-Rosenfeld"`
2. `"J(2k,k)" (solve OR solved OR proof OR coloring OR colouring OR chromatic)`
3. `"S(14,15,31)" OR "S(15,16,32)" OR "S(4,5,21)"`
4. `"erdosproblems.com/835" OR "#835" ("Johnson graph" OR Rosenfeld OR Steiner)`

Queries 2 and 3 returned no posts.  Queries 1 and 4 each returned the same
single post, [status 2080780379410342374](https://x.com/i/web/status/2080780379410342374),
created 2026-07-24 22:21:16 UTC.  Its text explicitly says that work beginning
from #835 led to a **distinct covering problem**; it does not claim a solution
of #835 itself.

Accordingly, this refresh found no X post in the recent-search window claiming
a proof or construction for Erdős–Rosenfeld #835 under the problem number,
Johnson-graph formulation, or the three first-open design formulations above.
The live problem page also still labels
[Problem #835](https://www.erdosproblems.com/835) **Open**.  Neither observation
can establish that no private or unpublished solution exists.

## Later same-day link-resolution pass

A second pass queried the exact name, exact first-open parameters, and
Johnson-graph/problem-number combinations. Besides the project's own post and
retweet, it found two posts by
[@NathanWilbanks_](https://x.com/NathanWilbanks_) that list “erdős 835”:

- [status 2080454669420175497](https://x.com/NathanWilbanks_/status/2080454669420175497),
  created 2026-07-24 00:47:00 UTC;
- [status 2081113474050977824](https://x.com/NathanWilbanks_/status/2081113474050977824),
  created 2026-07-25 20:24:52 UTC.

The API’s expanded-link metadata resolves both entries to the same AGNT report,
*Erdős 835: A Primality Sieve and Machine-Checked Small Cases*. Its own
description claims a reduction, a primality sieve, and machine-checked cases
\(k=2,3,4,5\); it does **not** claim a construction or impossibility theorem
settling the existential question. Thus these hits do not change the status
assessment.

An independent web search on 2026-07-26 again returned the Erdős Problems page
as **Open** and found no exact-parameter \(J(32,16)\) solution claim. This is
still only a bounded public-search audit, not a priority theorem.
