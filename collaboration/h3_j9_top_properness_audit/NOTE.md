# Automatic \(j=9\to10\) top-properness

Date: 2026-07-27.

## Scope

This note proves the next high-lift implication in the unrestricted lift
tower.  It uses the notation
\[
 |U|=19,\qquad |A|=13,\qquad |{\cal C}|=17
\]
from `collaboration/unrestricted_lift_tower/NOTE.md`.

> **Theorem.**  Assume the tower laws for every \(B\subset A\) with
> \(3\leq |B|\leq9\).  Fix \(P\in\binom U{14}\).  Then, for every
> triple \(abc\in\binom A3\), the fourteen values
> \[
> G_{A\setminus\{a,b,c\}}(P\setminus\{x\}),\qquad x\in P,
> \tag{1}
> \]
> are pairwise distinct.

Thus, once the lower tower has been constructed through level \(9\), the
new maps indexed by the ten-subsets of \(A\) are automatically top-proper
at level \(10\).  This is a conditional high-lift theorem.  It neither
constructs the lower tower nor resolves Erdős--Rosenfeld Problem #835.

## 1. The fixed-colour recurrence

Fix a colour \(\gamma\).  For \(S\subseteq A\), \(s=|S|\geq3\), put
\[
 F_S(X)=G_{A\setminus S}(P\setminus X),
 \qquad X\in\binom P{s-2},
 \tag{2}
\]
and
\[
 N_S=\#\{X:F_S(X)=\gamma\}.
 \tag{3}
\]
For a triple \(abc\), write
\[
 d_{abc}=N_{\{a,b,c\}}.
 \tag{4}
\]
This is precisely the multiplicity of \(\gamma\) in the column (1), so
\[
 0\leq d_{abc}\leq14.
 \tag{5}
\]

Let \(4\leq s\leq10\), fix \(S\in\binom As\), and fix
\(Y\in\binom P{s-3}\).  Apply the tower law indexed by
\(B=A\setminus S\) to \(Q=P\setminus Y\).  Its seventeen entries are
\[
 \{F_S(Y\cup\{z\}):z\in P\setminus Y\}
 \mathbin{\dot\cup}
 \{F_{S\setminus\{a\}}(Y):a\in S\}.
 \tag{6}
\]
The colour \(\gamma\) occurs exactly once.  Sum over all \(Y\).  Each
\((s-2)\)-set counted by \(N_S\) has \(s-2\) faces of size \(s-3\), so
\[
 (s-2)N_S+\sum_{a\in S}N_{S\setminus\{a\}}
 =\binom{14}{s-3}.
 \tag{7}
\]

Put
\[
 D(S)=\sum_{T\in\binom S3}d_T.
 \tag{8}
\]
Induction in (7), starting with \(N_T=d_T\) at \(s=3\), gives
\[
 N_S=\alpha_s+
 \frac{(-1)^{s-3}}{s-2}D(S),
 \tag{9}
\]
where \(\alpha_s\) depends only on \(s\).  In particular, for two
\(s\)-sets \(S,S'\),
\[
 D(S)-D(S')\equiv0\pmod{s-2}.
 \tag{10}
\]
The first three instances are
\[
 N_S=
 \begin{cases}
 7-\frac12D(S),&s=4,\\[2mm]
 \frac{56+D(S)}3,&s=5,\\[2mm]
 63-\frac14D(S),&s=6.
 \end{cases}
 \tag{11}
\]
Consequently
\[
 \begin{array}{c|ccc}
 |S|&4&5&6\\ \hline
 D(S)&0\pmod2&1\pmod3&0\pmod4.
 \end{array}
 \tag{12}
\]

## 2. The multiplicity tensor is pair-additive

We first extract exact, not merely modular, octahedral relations.
Fix six distinct vertices \(a,b,t,u,v,w\in A\), and put
\[
 \delta_{rs}=d_{ars}-d_{brs}.
 \tag{13}
\]
For each \(q=2,\ldots,8\), use (10) at size \(s=q+2\).  Comparing
\(T\cup\{a\}\) with \(T\cup\{b\}\), where \(|T|=q+1\), gives
\[
 \sum_{\{r,s\}\in\binom T2}\delta_{rs}\equiv0\pmod q.
 \tag{14}
\]
Compare two choices of \(T\) that exchange \(t\) and \(u\), and then
compare their common \(q\)-sets by exchanging \(v\) and \(w\).  The
required common \((q-1)\)-set exists because the other seven vertices of
\(A\) are available.  The result is
\[
 \delta_{tv}-\delta_{uv}-\delta_{tw}+\delta_{uw}
 \equiv0\pmod q.
 \tag{15}
\]
Thus the left side is divisible by
\[
 \mathop{\rm lcm}(2,\ldots,8)=840.
 \]
After expansion it is a signed sum of eight numbers in \([0,14]\), four
with each sign, so its absolute value is at most \(56\).  It must vanish.
Therefore all octahedral relations hold exactly.

The standard inclusion-matrix lemma now applies:

> **Pair-additivity lemma.**  A rational function \(d\) on the triples of
> a thirteen-set satisfies every octahedral relation if and only if there
> are unique rational numbers \(x_{ab}=x_{ba}\) on its pairs such that
> \[
> d_{abc}=x_{ab}+x_{ac}+x_{bc}.
> \tag{16}
> \]

For completeness, `verify_j9_top_properness.py` proves the lemma at the
exact parameters without importing it.  Let \(W\) be the
\(\binom{13}3\times\binom{13}2\) triple--pair inclusion matrix, and let
\(O\) have the octahedral relations as rows.  The verifier checks
\[
 OW=0,\qquad \operatorname{rank}W=78,\qquad
 \operatorname{rank}O=208=286-78
\tag{17}
\]
over a prime field.  The modular lower bounds are rational lower bounds,
while \(OW=0\) supplies the matching rational upper bounds.  Hence
\(\ker_{\mathbb Q}O=\operatorname{im}_{\mathbb Q}W\), proving existence
and uniqueness in (16).

## 3. The fractional parts are forced

For \(S\subseteq A\), let
\[
 X(S)=\sum_{\{a,b\}\in\binom S2}x_{ab}.
\]
Every pair of an \(s\)-set lies in exactly \(s-2\) of its triples, so
\[
 D(S)=(s-2)X(S).
\tag{18}
\]
Equations (12) and (18) say:

* \(X(S)\) is integral for every four-set;
* \(X(S)\equiv1/3\pmod1\) for every five-set;
* \(X(S)\) is integral for every six-set.

Fix \(a\in A\).  Subtract the four-set assertion on \(T\) from the
five-set assertion on \(T\cup\{a\}\).  For every four-set
\(T\subset A\setminus\{a\}\),
\[
 \sum_{t\in T}x_{at}\equiv\frac13\pmod1.
\tag{19}
\]
Comparing two such four-sets that exchange \(b\) and \(c\) shows
\[
 x_{ab}\equiv x_{ac}\pmod1.
\]
Thus all edges incident with \(a\) have one fractional part.  Symmetry of
\(x_{ab}\) makes this fractional part common to every pair; call it
\(\theta\).

A four-set has six pairs and a six-set has fifteen, so
\[
 6\theta=0,\qquad15\theta=0\qquad\text{in }\mathbb R/\mathbb Z.
\]
Hence \(3\theta=0\).  Equation (19) gives \(4\theta=1/3\), and therefore
\(\theta=1/3\).  We may write
\[
 x_{ab}=z_{ab}+\frac13,\qquad z_{ab}\in\mathbb Z,
\tag{20}
\]
and (16) becomes
\[
 d_{abc}=1+z_{ab}+z_{ac}+z_{bc}.
\tag{21}
\]

## 4. The local pair capacity

Fix a pair \(ab\).  For each fixed \(x\in P\), at most one triple
\(abc\) can have
\[
 G_{A\setminus\{a,b,c\}}(P\setminus\{x\})=\gamma.
\tag{22}
\]
Indeed, the two values for distinct \(c,d\) occur together in the tower
law indexed by the complementary nine-set
\(A\setminus\{a,b,c,d\}\), so they are distinct.

Summing over the fourteen choices of \(x\) yields
\[
 0\leq\sum_{c\notin\{a,b\}}d_{abc}\leq14.
\tag{23}
\]
Put
\[
 Z_a=\sum_{b\ne a}z_{ab}.
\tag{24}
\]
Using (21), the upper bound in (23) is exactly
\[
 9z_{ab}+Z_a+Z_b\leq3.
\tag{25}
\]
Nonnegativity of \(d\) also gives
\[
 z_{ab}+z_{ac}+z_{bc}\geq-1
\qquad(abc\in\binom A3).
\tag{26}
\]

The proof now reduces to the following elementary integer lemma.

## 5. Integer-weight lemma

> **Lemma.**  Let integers \(z_{ab}\) weight the edges of \(K_{13}\), and
> put \(Z_a=\sum_{b\ne a}z_{ab}\).  If (25) and (26) hold, then no edge
> has positive weight.  In particular every triangle has weight at most
> zero.

### Proof

Let
\[
 E=\sum_{\{a,b\}}z_{ab}.
\]
Sum (26) over all \(286\) triples.  Every edge occurs eleven times, so
\[
 E\geq-26.
\tag{27}
\]
Sum (25) over all \(78\) pairs.  Since
\(\sum_aZ_a=2E\), this gives
\[
 33E\leq234,
\qquad\text{hence}\qquad E\leq7.
\tag{28}
\]

For a fixed vertex \(a\), sum (26) over the \(66\) triples containing
\(a\):
\[
 E+10Z_a\geq-66.
\tag{29}
\]
Sum (25) over the twelve pairs containing \(a\):
\[
 20Z_a+2E\leq36.
\tag{30}
\]
Together with (27)--(28), these inequalities imply
\[
 -7\leq Z_a\leq4.
\tag{31}
\]

For a fixed edge \(ab\), sum (26) over the eleven triples containing it:
\[
 9z_{ab}+Z_a+Z_b\geq-11.
\tag{32}
\]
Combine (25), (31), and (32).  Since \(z_{ab}\) is integral,
\[
 z_{ab}\in\{-2,-1,0,1\}.
\tag{33}
\]

There is no edge \(ab\) of weight \(-2\).  If there were, (26) would say
\[
 z_{ac}+z_{bc}\geq1
\qquad(c\notin\{a,b\}).
\]
Consequently
\[
 Z_a+Z_b\geq-4+11=7.
\]
By (31), both \(Z_a\) and \(Z_b\) are at least \(3\).  For each \(c\),
at least one of \(ac,bc\) has weight \(1\).  If, say, \(z_{ac}=1\),
then (25) gives
\[
 Z_c\leq-6-Z_a\leq-9,
\]
contradicting (31).

We now have only the weights \(-1,0,1\).  Let \(p_v\) and \(n_v\) be the
numbers of positive and negative edges incident with \(v\).  Then
\[
 Z_v=p_v-n_v.
\tag{34}
\]
If \(a,b\) are two negative neighbours of \(v\), (26) forces
\(z_{ab}=1\).  Thus the negative neighbourhood of every vertex induces
a positive clique.

Write \(k=n_v\).  Every vertex of that positive clique has positive
degree at least \(k-1\), and therefore, using at most twelve incident
edges,
\[
 Z_a=p_a-n_a\geq2p_a-12\geq2k-14.
\tag{35}
\]
For an edge of the clique, (25) says \(Z_a+Z_b\leq-6\).  Equations
(35) therefore give
\[
 4k-28\leq-6,
\]
so \(n_v\leq5\) for every vertex \(v\).

Now take any positive edge \(ab\).  From \(n_a,n_b\leq5\), (34), and
\(Z_a+Z_b\leq-6\), we obtain
\[
 p_a+p_b\leq4.
\tag{36}
\]
Apply this once more inside the positive clique induced by the negative
neighbourhood of \(v\).  Its vertices have positive degree at least
\(k-1\), so (36) gives \(2(k-1)\leq4\), and hence
\[
 n_v\leq3
\qquad(v\in A).
\tag{37}
\]
Finally, an endpoint of a positive edge has \(p_v\geq1\), so
\[
 Z_v=p_v-n_v\geq-2.
\]
The two endpoints then have sum at least \(-4\), contradicting the
positive-edge consequence \(Z_a+Z_b\leq-6\) of (25).  No positive edge
exists. \(\square\)

## 6. Conclusion

By the lemma, every triangle has
\[
 z_{ab}+z_{ac}+z_{bc}\leq0.
\]
Equation (21) and the original nonnegativity (5) imply
\[
 d_{abc}\in\{0,1\}.
\]
This holds for every colour \(\gamma\).  Thus no colour repeats among the
fourteen values in any column (1), proving the theorem.

The argument is solver-free.  The verifier uses only exact integer and
finite-field arithmetic and audits the one finite-dimensional linear
algebra lemma in (17).

## Verification

Run:

```sh
python3 -B \
  collaboration/h3_j9_top_properness_audit/verify_j9_top_properness.py
```

Expected final line:

```text
PASS: automatic j=9 -> j=10 top-properness arithmetic and rank audit
```

This verification concerns only the conditional high-lift implication
proved here.  It is not a construction of the missing lower tower and is
not a proof of Problem #835.
