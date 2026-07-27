# The disjointness graph of an \(S(14,15,31)\) is empty

## Status and correction

This note is conditional on a Steiner system

\[
{\cal C}=S(14,15,31).
\]

It proves that **every such system is automatically intersecting**: no two
of its blocks are disjoint.  Thus the disjointness graph inside one fibre is
not merely a matching; it is the empty matching.

This corrects the proposed free statistic \(d(B)\) in the staircase-support
note.  The identity

\[
n_1(B)+15d(B)=120
\]

and the inequality \(d(B)\leq 1\) do not by themselves force an answer, but
the remaining Steiner design moments do:

\[
\boxed{d(B)=0,\qquad n_1(B)=120\quad\text{for every }B\in{\cal C}.}
\]

Consequently, in a partition of all \(15\)-subsets into seventeen
\(S(14,15,31)\) systems, the requirement that each fibre be intersecting is
not extra.  It follows already from the Steiner property.

This does **not** construct such a large set and does **not** prove that none
exists.  In particular, it does not solve Erdős--Rosenfeld problem #835.

## 1. What follows from the two elementary observations alone

Fix \(B\in{\cal C}\), let

\[
Y=[31]\setminus B,\qquad |Y|=16,
\]

and put

\[
n_s(B)=|\{C\in{\cal C}:|B\cap C|=s\}|,\qquad d(B)=n_0(B).
\]

Every block disjoint from \(B\) is one of the sixteen sets

\[
D_y=Y\setminus\{y\}\qquad(y\in Y).
\]

Two distinct candidates \(D_y,D_z\) intersect in the \(14\)-set
\(Y\setminus\{y,z\}\).  They therefore cannot both lie in an
\(S(14,15,31)\).  Hence

\[
d(B)\in\{0,1\}.
\tag{1}
\]

Now count the \(120=\binom{16}{14}\) fourteen-subsets of \(Y\).  A block
meeting \(B\) once accounts for one of them, while a block disjoint from
\(B\) accounts for \(\binom{15}{14}=15\).  The Steiner property assigns
each fourteen-subset to exactly one block, so

\[
\boxed{n_1(B)+15d(B)=120.}
\tag{2}
\]

At this truncated level, both local states are arithmetically possible:

\[
(d,n_1)=(0,120)\quad\text{or}\quad(1,105).
\tag{3}
\]

The graph on \({\cal C}\) joining point-disjoint blocks is therefore a
matching.  Write \(b=|{\cal C}|\) and let the matching have \(m\) edges.
Then

\[
b=\frac{\binom{31}{14}}{15}=17\,678\,835
\tag{4}
\]

is odd, and the elementary consequences are:

* \(0\le m\le (b-1)/2\);
* exactly \(2m\) blocks have \(d=1,n_1=105\);
* exactly \(b-2m\), an odd positive number, have \(d=0,n_1=120\);
* the number \(N_1\) of unordered block pairs meeting in one point is
  \[
  N_1=\frac12\sum_Bn_1(B)=60b-15m,
  \tag{5}
  \]
  so \(N_1\equiv m\pmod2\).

None of these truncated matching or handshake facts forces \(m>0\).
Indeed, \(m=0\) satisfies all of them.  The decisive information comes from
the other design moments.

## 2. The full Steiner moments force \(d=0\)

For \(0\le j\le14\), the number of blocks through a fixed \(j\)-set is

\[
\lambda_j
=\frac{\binom{31-j}{14-j}}{\binom{15-j}{14-j}}
=\frac{\binom{31-j}{14-j}}{15-j}.
\tag{6}
\]

Count pairs \((T,C)\) with \(T\subseteq B\cap C\), \(|T|=j\).  For every
fixed block \(B\),

\[
\sum_{s=j}^{15}\binom{s}{j}n_s(B)
=\binom{15}{j}\lambda_j
\qquad(0\le j\le14),
\tag{7}
\]

and \(n_{15}(B)=1\).  This is a triangular system, so it has a unique
solution.

> **Theorem 1 (complete fixed-block intersection distribution).**
> For every block \(B\) of every \(S(14,15,31)\),
> \[
> \boxed{
> n_s(B)=
> \frac{\binom{15}{s}
> \left(\binom{16}{s+1}+(-1)^{s+1}16\right)}{17}
> \quad(0\le s\le15).}
> \tag{8}
> \]

To verify (8), substitute it into the left side of (7), write
\(s=j+u\), and use

\[
\binom{s}{j}\binom{15}{s}
=\binom{15}{j}\binom{15-j}{u}.
\]

The alternating part vanishes because

\[
\sum_{u=0}^{15-j}(-1)^u\binom{15-j}{u}=0
\qquad(j\le14),
\]

while Vandermonde's identity gives

\[
\sum_{u=0}^{15-j}
\binom{15-j}{u}\binom{16}{j+u+1}
=\binom{31-j}{15-j}.
\]

Finally,

\[
\frac1{17}\binom{31-j}{15-j}
=\frac1{15-j}\binom{31-j}{14-j}
=\lambda_j.
\]

Thus (8) satisfies all the triangular equations and is their unique
solution.

At the two entries relevant to (2),

\[
n_0(B)=\frac{16-16}{17}=0,\qquad
n_1(B)=\frac{15(120+16)}{17}=120.
\tag{9}
\]

So \(d(B)=n_0(B)=0\) for every \(B\), and the disjointness matching has
exactly

\[
\boxed{m=0}
\tag{10}
\]

edges.  There is no Steiner-side route that can force a matching edge:
the full Steiner equations force the opposite conclusion.

## 3. Exact local and global intersection counts

The complete row is independent of \(B\):

| \(s\) | \(n_s\) |
|---:|---:|
| 0 | 0 |
| 1 | 120 |
| 2 | 3,360 |
| 3 | 49,140 |
| 4 | 349,440 |
| 5 | 1,417,416 |
| 6 | 3,363,360 |
| 7 | 4,877,730 |
| 8 | 4,324,320 |
| 9 | 2,362,360 |
| 10 | 768,768 |
| 11 | 147,420 |
| 12 | 14,560 |
| 13 | 840 |
| 14 | 0 |
| 15 | 1 |

For \(s<15\), the intersection-\(s\) graph is \(n_s\)-regular.  Since
\(b\) is odd, the handshake lemma forces every \(n_s\) with \(s<15\) to
be even, as the table confirms.

The number \(N_s\) of unordered pairs of distinct blocks meeting in \(s\)
points is \(bn_s/2\):

| \(s\) | \(N_s\) |
|---:|---:|
| 0 | 0 |
| 1 | 1,060,730,100 |
| 2 | 29,700,442,800 |
| 3 | 434,368,975,950 |
| 4 | 3,088,846,051,200 |
| 5 | 12,529,131,795,180 |
| 6 | 29,730,143,242,800 |
| 7 | 43,116,291,922,275 |
| 8 | 38,224,469,883,600 |
| 9 | 20,881,886,325,300 |
| 10 | 6,795,461,312,640 |
| 11 | 1,303,106,927,850 |
| 12 | 128,701,918,800 |
| 13 | 7,425,110,700 |
| 14 | 0 |

Their sum is

\[
\sum_{s=0}^{14}N_s=\binom b2=156\,270\,594\,639\,195.
\tag{11}
\]

Thus all pair counts and all parity constraints inside one fibre are
consistent; none supplies a contradiction.

## 4. The general automatic-intersection theorem

The same calculation has a useful parameter-free form.

> **Theorem 2.**  Suppose
> \[
> {\cal D}=S(k-2,k-1,2k-1)
> \]
> exists, and let \(n_s\) be the fixed-block intersection numbers.  Then
> \[
> \boxed{
> n_s=
> \frac{\binom{k-1}{s}
> \left(\binom{k}{s+1}+(-1)^{k-1-s}k\right)}
> {k+1}.}
> \tag{12}
> \]
> If \(k>1\), existence forces \(k\) even; for even \(k\), every such
> system is automatically intersecting.

The proof is the same triangular moment calculation.  At \(s=0\),

\[
n_0=\frac{k+(-1)^{k-1}k}{k+1}.
\tag{13}
\]

For even \(k\), this is zero.  For odd \(k>1\), it is \(2k/(k+1)\), which
is not an integer because \(\gcd(k,k+1)=1\) and \(k+1>2\).  This proves
both assertions.

For even \(k\), the generalized form of (2) is

\[
n_1+(k-1)d=\binom{k}{2}.
\tag{14}
\]

Formula (12) gives \(d=n_0=0\) and
\(n_1=\binom{k}{2}\), exactly saturating (14).

## 5. Consequences for a hypothetical large set

Now assume, in addition, that all \(15\)-subsets of \([31]\) are partitioned
into seventeen systems

\[
{\cal C}_0,\ldots,{\cal C}_{16},
\qquad {\cal C}_a=S(14,15,31).
\]

Theorem 1 says that every \({\cal C}_a\) is already an independent set in
the Odd graph

\[
O_{16}=KG(31,15).
\]

Therefore such a large set is itself the required **locally bijective**
proper \(17\)-colouring, equivalently the graph cover
\(O_{16}\to K_{17}\); there is no additional within-fibre intersection
condition.

Fix \(B\in{\cal C}_a\).  Its sixteen Odd-graph neighbours are

\[
Y\setminus\{y\}\qquad(y\in Y=[31]\setminus B).
\]

None belongs to \({\cal C}_a\).  No two can belong to the same other fibre,
because they intersect in fourteen points.  Hence:

> **Corollary 3 (cross-fibre perfect matchings).**  For every \(a\ne b\),
> each block of \({\cal C}_a\) has exactly one point-disjoint mate in
> \({\cal C}_b\).  The disjointness edges between
> \({\cal C}_a\) and \({\cal C}_b\) form a perfect matching
> \[
> \nu_{ab}:{\cal C}_a\longrightarrow{\cal C}_b,
> \qquad \nu_{ba}=\nu_{ab}^{-1}.
> \tag{15}
> \]

Equivalently, for each \(B\in{\cal C}_a\), the sixteen other fibre labels
are in bijection with the sixteen omitted points \(y\in Y\).  A hypothetical
tight colouring is therefore a degree-\(b\) graph covering

\[
O_{16}\longrightarrow K_{17}.
\]

There are \(b\) edges above each of the \(\binom{17}{2}=136\) base edges,
and

\[
|V(O_{16})|=17b=300\,540\,195,\qquad
|E(O_{16})|=136b=2\,404\,321\,560.
\tag{16}
\]

Because \(b\) is odd, every cross-fibre perfect matching has odd size.
This is compatible with all global degree and edge counts.

There is also a modest monodromy consequence.  For three distinct fibres,
form

\[
\pi_{abc}=\nu_{ca}\nu_{bc}\nu_{ab}
\quad\text{on }{\cal C}_a.
\tag{17}
\]

A cycle of length \(\ell\) in \(\pi_{abc}\) lifts to a cycle of length
\(3\ell\) in \(O_{16}\).  Since \(b\) is odd, \(\pi_{abc}\) has an odd
number of odd cycles.  The Odd graph has no odd cycle shorter than \(31\):
along every two steps in \(KG(31,15)\), a \(15\)-set changes by at most one
element, so an odd cycle of length \(2q+1\) requires \(q\ge15\).
Consequently every odd cycle of \(\pi_{abc}\) has

\[
3\ell\ge31,\qquad\text{hence}\qquad \ell\ge11.
\tag{18}
\]

This still gives no contradiction.  A permutation of the odd number \(b\)
of sheets can, arithmetically, have one odd cycle of length \(b\).  Any
further obstruction must couple the matchings around many base cycles, not
just use their individual sizes or elementary parity.

## 6. Verification

Run:

```sh
python3 -B \
  collaboration/steiner_disjoint_matching/verify_steiner_disjoint_matching.py
```

The verifier uses only standard-library exact integer arithmetic.  It checks
all design indices, the triangular moment equations, the closed formula and
the full intersection table, the local matching arithmetic, every global
pair count, the general formula on a range of parameters, and the
large-set edge and monodromy arithmetic.

**Scope:** this closes the proposed \(d(B)\) freedom by proving
\(d(B)\equiv0\).  It neither constructs nor excludes
\(LS(14,15,31)\).  Erdős--Rosenfeld problem #835 remains open.
