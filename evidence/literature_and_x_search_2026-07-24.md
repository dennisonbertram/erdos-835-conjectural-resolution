# Literature and X/Twitter status check — 2026-07-24

This is a reproducible record of the status check used by the accompanying
note.  It is evidence about public claims, not a mathematical proof that no
unindexed or private solution exists.

## Erdős Problems database

The live page
[Erdős Problem #835](https://www.erdosproblems.com/835) was opened on
2026-07-24.  It still labels the problem `Open`, identifies the equivalent
Johnson-graph formulation, and records the Ma--Tang prime obstruction.  The
page says it was last edited on 2026-01-22.  Its visible discussion contains
no accepted complete solution.

## Exact recent X searches

The connected X API's `GET /2/tweets/search/recent` endpoint was queried on
2026-07-24.  That endpoint covers only the preceding seven days.  Retweets
were excluded.  Each query requested up to 100 posts:

```text
"Erdos Problem #835" OR "Erdős Problem #835" -is:retweet
"Erdos 835" OR "Erdős 835" -is:retweet
"J(2k,k)" -is:retweet
"LS(k-1,k,2k)" OR "LS(15,16,32)" -is:retweet
(Erdos OR Erdős) "#835" -is:retweet
"S(15,16,32)" OR "S(14,15,31)" -is:retweet
"Johnson graph" "17" (color OR colour OR chromatic) -is:retweet
"Steiner" "Problem 835" -is:retweet
```

Seven of the eight queries returned zero posts.  The two broad Erdős-835
queries found the same single post, X post
[`2080454669420175497`](https://x.com/i/status/2080454669420175497), created
2026-07-24 at 00:47 UTC.  It links to
[Erdős 835: A Primality Sieve and Machine-Checked Small
Cases](https://agnt.gg/whitepapers/erdos-835-a-primality-sieve-and-machine-checked-small-cases.html).
The linked report's own title and description claim the prime sieve and
small-case checks, not a resolution of the remaining prime cases.

No recent post returned by these searches claimed a proof or construction
for the open cases.

## Archive limitation

A full-archive query for the combined Erdős-835 spellings was attempted.
The API returned HTTP 403 with:

```text
Full-archive search requires Pro or Enterprise on this access tier.
```

Accordingly, this evidence supports only the precise statement that no claim
was found in the available recent window under the listed formulations.  It
must not be paraphrased as a guarantee that nobody has posted a solution at
any earlier time.
