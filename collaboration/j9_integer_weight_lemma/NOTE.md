# The integer edge-weight lemma at the ninth lift

## Statement

Let \(z_{ab}\in\mathbb Z\) be assigned to the \(78\) edges of \(K_{13}\), and
write

\[
Z_a=\sum_{b\ne a}z_{ab}.
\]

Assume

\[
z_{ab}+z_{ac}+z_{bc}\ge -1
\tag{T}
\]

for every triangle \(abc\), and

\[
9z_{ab}+Z_a+Z_b\le 3
\tag{P}
\]

for every edge \(ab\). Then every triangle has weight at most \(0\).

This note proves only this finite integer lemma. It does not by itself solve
Erdős--Rosenfeld problem #835.

## Proof

Put \(E=\sum_{a<b}z_{ab}\). Each edge belongs to \(11\) triangles, so summing
(T) over the \(\binom{13}{3}=286\) triangles gives

\[
11E\ge-286,\qquad E\ge-26.
\tag{1}
\]

In the sum of (P) over all \(78\) edges, the \(9z_{ab}\) terms contribute
\(9E\), while every \(Z_a\) occurs on the \(12\) edges incident with \(a\).
Because \(\sum_a Z_a=2E\), this gives

\[
33E\le234,\qquad E\le7.
\tag{2}
\]

Fix a vertex \(a\). Sum (T) over the \(66\) triangles containing \(a\).
An edge incident with \(a\) is counted \(11\) times and every other edge once,
so

\[
10Z_a+E\ge-66.
\tag{3}
\]

Sum (P) over the \(12\) edges incident with \(a\). The result is

\[
20Z_a+2E\le36,
\quad\text{or}\quad
10Z_a+E\le18.
\tag{4}
\]

Using (1)--(2) in (3)--(4), and using that \(Z_a\) is integral, yields

\[
-7\le Z_a\le4.
\tag{5}
\]

Now fix an edge \(ab\). Summing (T) over the \(11\) triangles containing that
edge gives

\[
9z_{ab}+Z_a+Z_b\ge-11.
\tag{6}
\]

Combining (5), (6), and (P) shows

\[
z_{ab}\in\{-2,-1,0,1\}.
\tag{7}
\]

In fact, the value \(-2\) is impossible. If \(z_{ab}=-2\), (6) gives
\(Z_a+Z_b\ge7\); by (5), both \(Z_a\) and \(Z_b\) are at least \(3\).
For every third vertex \(c\), (T) says

\[
z_{ac}+z_{bc}\ge1.
\]

By (7), at least one of these two edges has weight \(1\). If, for example,
\(z_{ac}=1\), then (P) gives

\[
Z_c\le-6-Z_a\le-9,
\]

contrary to (5). Hence

\[
z_{ab}\in\{-1,0,1\}\quad\text{for every edge }ab.
\tag{8}
\]

For a vertex \(v\), let

\[
N(v)=\{x:z_{vx}=-1\},\qquad n_v=|N(v)|,
\]

and let \(p_v\) be the number of weight-\(1\) edges incident with \(v\).
Then \(Z_v=p_v-n_v\).

The set \(N(v)\) is a positive clique: if \(x,y\in N(v)\), then (T) on
\(vxy\) gives

\[
-1-1+z_{xy}\ge-1,
\]

so (8) forces \(z_{xy}=1\).

Write \(k=n_v\). Each \(x\in N(v)\) has \(k-1\) positive edges inside
\(N(v)\), the negative edge \(xv\), and only \(12-k\) other edges, each of
weight at least \(-1\). Therefore

\[
Z_x\ge(k-1)-1-(12-k)=2k-14.
\tag{9}
\]

If \(k\ge2\), choose distinct \(x,y\in N(v)\). Their edge is positive, so (P)
gives \(Z_x+Z_y\le-6\). By (9),

\[
4k-28\le-6,
\]

which implies \(k\le5\). Thus \(n_v\le5\) for every vertex.

For any positive edge \(ab\), (P) and \(Z=p-n\) give

\[
p_a+p_b\le n_a+n_b-6\le4.
\tag{10}
\]

Apply this to an edge \(xy\) inside \(N(v)\). Both \(x\) and \(y\) have at
least \(k-1\) positive neighbors in that clique, so (10) gives

\[
2(k-1)\le4.
\]

Consequently \(n_v=k\le3\) for every vertex (the cases \(k<2\) are already
covered).

Finally, if a positive edge \(ab\) existed, then \(p_a,p_b\ge1\) and
\(n_a,n_b\le3\), hence

\[
Z_a+Z_b=(p_a-n_a)+(p_b-n_b)\ge-4.
\]

But (P) on the positive edge says \(Z_a+Z_b\le-6\), a contradiction. Thus no
edge has weight \(1\). By (8), all edge weights are \(-1\) or \(0\), and every
triangle has weight at most \(0\), as required. \(\square\)

## Machine-checkable arithmetic audit

`verify_arithmetic.py` uses only the Python standard library. It exhausts all
integer values in the bounded ranges appearing above and checks:

1. the global bounds force \(-7\le Z_a\le4\);
2. (P) and (6) force \(z_{ab}\in\{-2,-1,0,1\}\);
3. every numerical case required by a hypothetical \(-2\) edge contradicts
   the row bounds;
4. the positive-clique inequality forces negative degree first to at most
   \(5\), then to at most \(3\);
5. the remaining endpoint counts make a positive edge impossible.

Run:

```sh
python3 collaboration/j9_integer_weight_lemma/verify_arithmetic.py
```

Expected final line:

```text
PASS: all arithmetic implications in the human proof were exhausted
```
