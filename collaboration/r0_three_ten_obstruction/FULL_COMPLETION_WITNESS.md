# Full completion of the dead-six-prefix support instance

Date: 2026-07-28.

The support instance in `DEAD_SIX_PREFIX.md` is **not** a counterexample
to coordinated nine or full completion.  Although its displayed
six-prefix has only two individually extendible remaining colours, the
same seventeen supports admit the following complete decomposition of
\(K_{13}\).

The colour order is the order of complements in that note: the six
selected complements (5)--(6), the four five-sets (7), the five triples
(8), and the two triples (9).

\[
\begin{array}{c|l}
0&c_0c_2,\ c_1c_5,\ c_3o_0,\ c_4o_3,\ o_1o_5\\
1&c_0c_4,\ c_1c_3,\ c_2o_6,\ c_5o_4,\ o_0o_2\\
2&c_0c_1,\ c_2c_3,\ c_4o_6,\ c_5o_0,\ o_3o_5\\
3&c_1o_6,\ c_3c_4,\ c_5o_5,\ o_0o_4\\
4&c_0c_5,\ c_1c_2,\ o_3o_4,\ o_5o_6\\
5&c_0c_3,\ c_2o_3,\ c_4o_5,\ o_4o_6\\
6&c_0o_5,\ o_0o_1,\ o_2o_4,\ o_3o_6\\
7&c_1o_4,\ o_0o_5,\ o_1o_3,\ o_2o_6\\
8&c_2o_4,\ o_0o_3,\ o_1o_6,\ o_2o_5\\
9&c_3o_5,\ o_0o_6,\ o_1o_4,\ o_2o_3\\
10&c_0o_4,\ c_1o_3,\ c_2c_4,\ c_3o_1,\ c_5o_2\\
11&c_0o_6,\ c_1c_4,\ c_2o_0,\ c_3o_2,\ c_5o_1\\
12&c_0o_2,\ c_1o_0,\ c_2o_5,\ c_3c_5,\ c_4o_1\\
13&c_0o_1,\ c_1o_2,\ c_2c_5,\ c_3o_4,\ c_4o_0\\
14&c_0o_0,\ c_1o_1,\ c_2o_2,\ c_3o_3,\ c_4c_5\\
15&c_2o_1,\ c_3o_6,\ c_4o_2,\ c_5o_3,\ o_4o_5\\
16&c_0o_3,\ c_1o_5,\ c_4o_4,\ c_5o_6,\ o_1o_2
\end{array} \tag{1}
\]

Each row is a perfect matching on its prescribed support.  The rows are
pairwise edge-disjoint and contain
\[
3\cdot5+3\cdot4+4\cdot4+7\cdot5=78
\]
edges, so they partition \(E(K_{13})\).

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_full_completion.py
```

The verifier reconstructs all supports from `DEAD_SIX_PREFIX.md`, checks
every matching endpoint set, and confirms that (1) uses every edge of
\(K_{13}\) exactly once.

This exact witness isolates the quantifier failure: the displayed
six-prefix is dead before nine, while a wholesale recolouring of the
same support instance reaches all seventeen colours.
