# Independent audit of the repaired full-row factor proof

Date: 2026-07-28.

## Verdict

The factor-existence proof in
[`2026-07-28_cut_sufficiency_agent_factor_gate.md`](2026-07-28_cut_sufficiency_agent_factor_gate.md)
and
[`2026-07-28_cut_sufficiency_agent_factor_complete.md`](2026-07-28_cut_sufficiency_agent_factor_complete.md)
is sound after the three omitted \(|A|=5\) cases were inserted.

Under the exact full-row hypotheses and all capacity cuts (C), every
Tutte--Lovász inequality holds.  Hence \(G\) has a simple \(b\)-factor
\[
d_H(v)=3-|\{i:v\in R_i\}|.
\]

This audit concerns factor existence only.  It does not audit or prove the
prescribed three-edge-colouring of the factor.

The proof uses the previously audited fact that (C) plus the full row
equations makes each selected size-ten support individually matchable.  That
fact is used only in the \(B=\varnothing,\ |A|=3,\ b(A)=0\) branch.

## 1. Criterion, normalization, and parity

For disjoint \(A,B\subseteq V\), put
\[
C=V\setminus(A\cup B)
\]
and let \(q(A,B)\) count those components \(K\) of \(G[C]\) for which
\[
b(K)+e_G(K,B)
\]
is odd.  The exact Tutte--Lovász criterion is
\[
\Delta(A,B)=
b(A)+\sum_{v\in B}d_{G-A}(v)-b(B)-q(A,B)\ge0. \tag{1}
\]
It applies with \(b(v)=0\) allowed; also \(b(v)\le3<d_G(v)\).

Let \(u(v)\) count incidence in the other eight remaining rows.  The full
column equation and the deleted-degree cap give
\[
\rho(v)=t(v)+u(v)=d_D(v)-1,\qquad 0\le u(v)\le4.
\]
Since \(d_G(v)=12-d_D(v)\),
\[
d_G(v)-b(v)
=12-(t(v)+u(v)+1)-(3-t(v))
=8-u(v).
\]
Therefore
\[
\Delta(A,B)
=b(A)+8|B|-u(B)-e_G(A,B)-q(A,B), \tag{2}
\]
and, by expanding the degree sum on \(B\),
\[
\Delta(A,B)
=b(A)-b(B)+2e(G[B])+e_G(B,C)-q(A,B). \tag{3}
\]

The parity assertion is exact.  Modulo two,
\[
q(A,B)\equiv b(C)+e_G(C,B),
\]
while
\[
\sum_{v\in B}d_{G-A}(v)
\equiv e_G(B,C).
\]
Thus
\[
\Delta(A,B)\equiv b(A)+b(B)+b(C)=b(V)=30\equiv0
\pmod2. \tag{4}
\]

Finally, \(\delta(G)\ge7\).  A component \(K\) of \(G[C]\) has no
\(G\)-edge to another component of \(G[C]\), so
\[
7\le d_G(v)\le |K|-1+|A|+|B|
\]
for \(v\in K\).  Hence
\[
|K|\ge8-|A|-|B|. \tag{5}
\]

No selected-row intersection assumption enters these identities.

## 2. Exhaustion of the separator sizes

Write
\[
a=|A|,\qquad k=|B|,\qquad c=13-a-k.
\]

The gate proves:

1. every \(k=0\) case, for all \(0\le a\le13\);
2. every \(k>0,\ a\le4\) case; and
3. the cases \(a=5,\ 1\le k\le4\).

For \(a=5\), the rigid continuation proves \(k=5\), and the repair proves
\(k=6,7,8\).  Thus every feasible \(a=5\) case is covered.

For \(a\ge6,\ k>0\), put
\[
p(v)=8-u(v)-e_G(v,A).
\]
The bounds
\[
p(v)\ge4-a,\qquad b(A)\ge3a-9,\qquad q\le c
\]
give
\[
\Delta(A,B)\ge4a-22+(5-a)k. \tag{6}
\]
If the right side is at least \(-1\), evenness (4) closes the case.  Exact
enumeration leaves only
\[
\begin{array}{c|c|c}
a&k&c\\ \hline
6&4,5,6,7&3,2,1,0\\
7&4,5,6&2,1,0\\
8&4,5&1,0\\
9&4&0.
\end{array} \tag{7}
\]
The continuation treats all ten triples in (7): four with \(c=0\) and six
with \(c>0\).  For \(a\ge10\), (6) leaves none.

This covers every feasible disjoint-set size.  In particular, the earlier
gap at
\[
(a,k,c)=(5,6,2),(5,7,1),(5,8,0)
\]
is no longer present.

## 3. Independent check of the repaired \(|A|=5\) cases

For \(a=5\), the crude bound is \(-2\).  A negative witness must attain
equality everywhere:
\[
\begin{gathered}
b(A)=6,\qquad p(v)=-1\ (v\in B),\qquad q=c,\\
G[C]\text{ edgeless with every vertex a counted singleton}.
\end{gathered} \tag{8}
\]

Because
\[
b(A)=15-t(A)=6,
\]
all nine selected-row incidences lie in \(A\).  Therefore every selected
row is contained in \(A\), including when rows repeat.  For \(v\in B\),
\[
-1=p(v)=8-u(v)-e_G(v,A)
\]
and the separate bounds \(u(v)\le4,\ e_G(v,A)\le5\) force
\[
u(v)=4,\quad e_G(v,A)=5,\quad
d_D(v)=5,\quad e_D(v,A)=0. \tag{9}
\]

Every six-, seven-, or eight-set disjoint from the three selected rows
therefore obeys
\[
\begin{array}{c|c|c}
|X|&e(G[X])\text{ required by (C)}&e(D[X])\text{ allowed}\\ \hline
6&\ge3&\le12,\\
7&\ge6&\le15,\\
8&\ge9&\le19.
\end{array} \tag{10}
\]

### The \(5+8+0\) case

Every vertex of \(B\) has all five deleted neighbours in \(B\), so
\[
2e(D[B])=40,\qquad e(D[B])=20,
\]
contradicting the eight-set bound \(e(D[B])\le19\).

### The \(5+7+1\) case

Let \(C=\{c\}\) and \(m=e_D(c,B)\).  Summing deleted degrees on \(B\)
gives
\[
35=2e(D[B])+m.
\]
The seven-set bound on \(B\) gives \(e(D[B])\le15\), hence \(m\ge5\).
The eight-set bound on \(B\cup C\) gives
\[
e(D[B])+m=\frac{35+m}{2}\le19,
\]
hence \(m\le3\), a contradiction.

### The \(5+6+2\) case

Let \(C=\{c_1,c_2\}\) and
\[
m_j=e_D(c_j,B),\qquad m=m_1+m_2.
\]
Since \(G[C]\) is edgeless, \(c_1c_2\in D\).  Each \(c_j\) is counted,
and all selected rows avoid \(C\), so
\[
b(c_j)+e_G(c_j,B)=3+(6-m_j)
\]
is odd.  Thus \(m_j\) is even.  Its existing deleted neighbour in \(C\)
and \(d_D(c_j)\le5\) give \(m_j\le4\).

The degree sum on \(B\) is
\[
30=2e(D[B])+m.
\]
The six-set and eight-set bounds in (10) force respectively
\[
m\ge6,\qquad
e(D[B\cup C])=16+\frac m2\le19,
\]
so \(m=6\).  Hence
\[
\{m_1,m_2\}=\{2,4\}.
\]
For the vertex with \(m_j=4\), the seven-set \(B\cup\{c_j\}\) has
\[
e(D[B\cup\{c_j\}])=12+4=16,
\]
contradicting the seven-set bound in (10).

All three new derivations are valid.

## 4. Audit of the ten \(|A|\ge6\) eliminations

For the four \(C=\varnothing\) cases, (3) becomes
\[
\Delta=30-2b(B)+2e(G[B]).
\]
The \(k=4,5\) cases are immediate from \(b(B)\le3k\).  For
\((a,k)=(7,6),(6,7)\), the six- and seven-set cuts give respectively
\[
t(B)+e(G[B])\ge3,\qquad t(B)+e(G[B])\ge6,
\]
which are exactly the two remaining inequalities.

For \(C\ne\varnothing\), putting
\[
r_B=t(B),\quad r_C=t(C),\quad r_U=r_B+r_C,\quad U=B\cup C
\]
gives
\[
\Delta
=30-6k-3c+2r_B+r_C+2e(G[B])+e_G(B,C)-q. \tag{11}
\]
The cut on \(U\) gives
\[
r_U+e(G[U])\ge
\begin{cases}
6,&a=6,\ |U|=7,\\
3,&a=7,\ |U|=6.
\end{cases} \tag{12}
\]

Substitution in each of the six displayed cases is exact:

- \((6,4,3)\) uses \(e(G[C])+q\le4\);
- \((6,6,1)\) additionally uses the six-set bound
  \(r_B+e(G[B])\ge3\);
- \((6,5,2)\) is the only equality branch and is correctly reduced to
  the three possibilities
  \[
  (e(G[C]),n_1+n_2,m_1+m_2)
  =(1,0,5),(0,0,4),(0,1,5);
  \]
  the two six-set cuts and counted-singleton parity exclude all three;
- \((7,4,2)\) would force an all-avoiding independent six-set;
- \((7,5,1)\) is at least \(-1\);
- \((8,4,1)\) is at least \(2\).

All uses of \(e_D\) and \(e_G\) in these branches are complementary counts
inside the same vertex set.  No conversion drops a crossing-edge term.

## 5. Verification

Run:

```sh
python3 collaboration/opus5_r0_orbit_repair/verify_factor_size_exhaustion.py
python3 collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_independent_verify.py
ruff check collaboration/opus5_r0_orbit_repair/verify_factor_size_exhaustion.py \
  collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_independent_verify.py
```

The first verifier checks the exceptional-size list and the three repaired
\(a=5\) calculations.  The independent verifier reconstructs the complete
size partition, the small component-count bounds, every cut-demand
conversion used in the proof, and the finite equality branch for
\((6,5,2)\).

The remaining theorem gap is prescribed colouring, not factor existence.

