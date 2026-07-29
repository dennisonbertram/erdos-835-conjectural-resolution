# A dead but fully completable seven-prefix for \(r=4\)

Date: 2026-07-28.

## Result and scope

There is an exact \(n=13,q=17\) class-B support instance with profile
\[
(n_8,n_{10},n_{12})=(11,2,4)
\]
and a seven-prefix of type \(8^4\,10\,12^2\) for which all ten remaining
supports are blocked. The same support matrix has a different literal
17-matching decomposition of \(K_{13}\).

Thus blind arbitrary-prefix induction also fails for \(r=4\). This is not a
noncompletable instance, a universal switching theorem, a class-B-prime or fan
realization, or a resolution of Problem #835.

## Complement-transfer construction

Start with the \(C\subset G\) prefix in `R3_DEAD_SEVEN_PREFIXES.md`; its prefix
union and selected supports are unchanged. Among its three remaining
size-ten complement triples, replace
\[
\{7,8,9\},\qquad\{7,10,12\}
\]
by
\[
\{7,8,9,10,12\},\qquad\{7\}.
\]
The first operation changes a remaining size-ten support to size eight; the
second changes another to size twelve. The pair \(\{10,12\}\) is added once
and removed once, so every complement-row sum is preserved.

The complete list of ten remaining complements is
\[
\begin{gathered}
01235,\ 12345,\ 01246,\ 02346,\ 12356,\ 03456,\\
789\,10\,12,\quad 89\,10,\quad\{7\},\quad\{12\}.
\end{gathered}
\]
Their sizes are \(5^7,3,1^2\), giving seven remaining size-eight supports,
one size-ten support, and two size-twelve supports.

The unchanged prefix consists of the following matchings:
\[
\begin{array}{c|l}
0&05,\ 26,\ 34,\ 7\,10\\
1&04,\ 13,\ 25,\ 79\\
2&12,\ 35,\ 46,\ 10\,12\\
3&02,\ 14,\ 36,\ 8\,12\\
4&06,\ 15,\ 23,\ 7\,12,\ 89\\
5&01,\ 24,\ 3\,11,\ 56,\ 78,\ 9\,10\\
6&03,\ 16,\ 2\,11,\ 45,\ 8\,10,\ 9\,12.
\end{array}
\]

## Verification

`verify_r4_dead_seven_prefix.py` is dependency-free. It checks all matching
and support endpoints, the profile and thirteen row sums, and every perfect
matching of all ten remaining supports. It also checks a literal
17-matching completion whose 78 distinct edges equal \(E(K_{13})\).

`search_r4_dead_seven_prefix.py` reuses the exact CP-SAT/CEGAR master from
the \(r=2\) search with complement inventory \(5^7,3,1^2\). The explicit
certificate is a zero-distance hint; the standard-library semantic replay
is the durable proof.

This settles the arbitrary-prefix boundary only. Whether every \(r=4\)
support instance has some coordinated eight-matching prefix remains open.
