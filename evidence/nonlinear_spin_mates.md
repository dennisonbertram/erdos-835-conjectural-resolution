# The nonlinear spin-mate locus

Status: **exact finite theorem at \(r=3,5\); conjectural at \(r=15\)**.

This note tests a narrower replacement for the false claim that the whole
support trade lattice is 4-even.  It uses the nondegenerate basic-spin
quotient of the full stable trade code and asks whether **actual**
mate differences lie on the pure-spin cone.

The test is reproducible with

```bash
python3 evidence/verify_nonlinear_spin_mates.py
```

No floating-point arithmetic or probabilistic search is used.

## 1. Stable code and Clifford action

Put
\[
 L=\ker_{\mathbf Z}W_{r-1,r}(2r+1),\qquad
 C=L/2L\subseteq\mathbf F_2^{\binom{2r+1}r},
\]
let \(R=\operatorname{rad}C\) for the coordinate dot product, and put
\[
 S=C/R.
\]
The exact dimensions are
\[
\begin{array}{c|ccc}
r&\dim C&\dim R&\dim S\\ \hline
3&14&6&8\\
5&132&100&32.
\end{array}
\]
They agree with the characteristic-two basic-spin quotient
\(D^{(r+1,r)}\), of dimension \(2^r\).

There is a useful completely explicit Clifford test.  Let
\[
 V=\{x\in\mathbf F_2^{\,2r+1}:\sum x_i=0\},
 \qquad
 Q_V(x)=\frac{\operatorname{wt}(x)}2\pmod2.
\]
The adjacent roots
\(\alpha_i=e_i+e_{i+1}\), \(0\le i<2r\), form a basis of \(V\).
Let \(\gamma_i\) be the action on \(S\) of the adjacent point
transposition \((i,i+1)\).  Direct exact quotient computation gives
\[
\begin{aligned}
\gamma_i^2&=I,\\
\gamma_i\gamma_j+\gamma_j\gamma_i
&=\begin{cases}
 I,&|i-j|=1,\\
 0,&|i-j|>1.
\end{cases}
\end{aligned}
\tag{1}
\]
Consequently
\[
 c\!\left(\sum_i a_i\alpha_i\right)=\sum_i a_i\gamma_i
\tag{2}
\]
satisfies \(c(v)^2=Q_V(v)I\).  This is the Clifford/Fock realization of
the basic-spin module, obtained here without choosing an abstract
isomorphism.

For \(\psi\in S\), define
\[
\operatorname{Ann}(\psi)
=\{v\in V:c(v)\psi=0\}.
\tag{3}
\]
For the plus-type point spaces relevant to \(r=3,15\), a nonzero spinor
is pure when
\(\dim\operatorname{Ann}(\psi)=r\), the maximal possible value.  The
\(r=5\) point space is minus type (Witt index \(4\), not \(5\)); no
nonzero \(r=5\) purity claim is made below.
For every nonzero singular \(v\), the verifier checks that
\(\operatorname{im}c(v)\) is totally singular for
\[
q_S(\bar z)=\frac{z\cdot z}{2}\pmod2.
\tag{4}
\]
Since \(\ker c(v)=\operatorname{im}c(v)\), any nonzero spinor with a
nonzero Clifford annihilator has \(q_S=0\).  In particular,
\[
\boxed{\text{pure (or zero)}\quad\Longrightarrow\quad q_S=0.}
\tag{5}
\]

## 2. Exact \(r=3\) result

Fix a Fano plane \(A\).  It has eight disjoint mates.  For every unordered
mate pair \(B,C\), the class
\[
\psi_{B,C}=[x_B+x_C]\in S
\tag{6}
\]
is nonzero and pure:
\[
\dim\operatorname{Ann}(\psi_{B,C})=3,\qquad q_S(\psi_{B,C})=0.
\tag{7}
\]
The 28 pairs produce seven distinct pure classes, each four times.

This is not a relabeling of the desired quadratic conclusion.  Exhaustion
of all 255 nonzero vectors of the eight-dimensional spin module gives
\[
\begin{array}{c|c|c}
\dim\operatorname{Ann}(\psi)&q_S(\psi)&\#\psi\\ \hline
0&1&120\\
2&0&105\\
3&0&30.
\end{array}
\tag{8}
\]
Thus only 30 of the 135 nonzero singular vectors are pure.  Moreover, the
image of the whole support lattice is a four-dimensional totally singular
space.  Among its 15 nonzero vectors, eight are pure and seven are not.
Actual mate differences occupy seven of those eight pure points.

The affine classes \([x_A+x_B]\) tell a complementary story: all eight
are anisotropic, with \(q_S=1\) and zero Clifford annihilator.  It is the
**difference of two mates**, not the base-to-mate class, that is pure.

There is a stronger intrinsic check over all 435 unordered pairs of the
30 labelled Fano planes:
\[
\begin{array}{c|c|c|c|c}
|B\cap C|&q_S&\dim\operatorname{Ann}&
\#\{A:A\cap B=A\cap C=\varnothing\}&\#\{B,C\}\\ \hline
0&1&0&0&120\\
1&0&3&4&210\\
3&0&2&0&105.
\end{array}
\tag{9}
\]
Thus, at \(r=3\), a pair has a common disjoint base **if and only if** its
difference is a nonzero pure spinor.  Purity distinguishes the
common-base triples from both the disjoint pairs and the highly
intersecting singular-but-nonpure pairs.  This is substantially more
specific than checking \(q_S=0\).

There is nevertheless a serious extrapolation warning.  At \(r=3\) the
eight-dimensional full spin module is the exceptional \(D_4\) case: its
two half-spin spaces each have dimension four, every nonzero half-spinor
is automatically pure, and triality is available.  Thus the \(r=3\)
calculation tests essentially a chirality constraint, not the
nontrivial high-rank Cartan/Wick quadrics that appear at \(r=15\).

## 3. Exact \(r=5\) audit and adversarial control

The \(r=5\) result is much more degenerate.  Generate the full orbit of the
Witt \(S(4,5,11)\) under adjacent point transpositions.  It consists of
all 5,040 labelled systems.  Every one has the same class modulo \(R\):
\[
[x_D+x_A]=0\in S
\qquad\text{for all 5,040 systems }D.
\tag{10}
\]
Equivalently, every difference of two Witt systems is full-radical.
Their intersection distribution with a fixed \(A\) is
\[
\begin{array}{c|rrrrrr}
|A\cap D|&0&6&12&18&30&66\\ \hline
\#D&144&2574&1760&495&66&1.
\end{array}
\tag{11}
\]
All intersection sizes are even.  In particular, genuine mate
differences satisfy the homogeneous pure-spin equations only at the cone
vertex \(0\); there is no nonzero \(r=5\) purity evidence.

The ambient relaxation is sharply different.  The support lattice maps
onto all 32 dimensions of \(S\).  The recorded shaped-kernel witness with
49 active spheres maps to a nonzero spinor with
\[
q_S=1,\qquad \dim\operatorname{Ann}=0.
\tag{12}
\]
So a “zero or pure” endpoint theorem would exclude a known false positive
that passes every linear support equation.  It is genuinely nonlinear.

## 4. The exact surviving conjecture

The computational pattern suggests the following deliberately narrow
statement.

> **Pure-mate conjecture.**  Let \(r=2^m-1\) with \(m\ge2\).  If
> \(A,B,C\) are \(S(r-1,r,2r+1)\) systems with
> \(A\cap B=A\cap C=\varnothing\), then
> \([x_B+x_C]\in S\) is zero or a pure spinor.

The exclusion \(m=1\) is necessary: for \(r=1\), the three singleton
systems give a pair difference of \(q_S=1\).

At \(r=15\),
\[
q_S([x_B+x_C])
=\frac{\operatorname{wt}(x_B+x_C)}2
=b-|B\cap C|\pmod2,
\tag{13}
\]
and \(b=17\,678\,835\) is odd.  Equations (5) and (12) show that the
pure-mate conjecture would force \(|B\cap C|\) odd, ruling out a third
system disjoint from \(A\), and hence ruling out the required large set.

In the concrete Clifford model, the missing theorem is exactly:
\[
\dim\left\{
(a_0,\ldots,a_{2r-1})\in\mathbf F_2^{2r}:
\sum_{i=0}^{2r-1}a_i\,
[(i,i+1)(x_B+x_C)]=0\text{ in }S
\right\}=r,
\tag{14}
\]
unless \([x_B+x_C]=0\).  The brackets mean reduction modulo the full
stable radical \(R\).

The all-odd/Mersenne parameter lemma supplies a plausible discriminator:
every derived \(\lambda_i\) is odd and every off-diagonal internal
intersection valency is even at \(r=3,15\), unlike \(r=5\).  What is **not**
yet proved is that these scalar moment parities imply the Cartan
annihilator equations (14).  Association-scheme moments alone leave
\(|B\cap C|\) as their one free parameter, so treating (14) as a formal
consequence of those moments would be circular.

## 5. Cartan quadrics pulled back to block variables

Choose a polarization \(V=E\oplus F\) of the plus-type point space at
\(r=15\).  The Fock model identifies the full spin module with
\(\bigwedge E\), with coordinates \(p_I\) indexed by all
\(I\subseteq[15]\); the two half-spin spaces use the even and odd
subsets separately.  For a stable block word \(u\), every Fock coordinate
is a fixed linear functional
\[
p_I(u)=\ell_I(u)
=\sum_{K\in\binom Xr}a_{I,K}u_K
\qquad(a_{I,K}\in\mathbf F_2).
\tag{W1}
\]
The coefficients are obtained exactly by choosing a vacuum in the common
kernel of \(c(E)\) and applying the dual Clifford generators.  Thus (W1)
is an explicit, finite change of coordinates on \(C/R\), although it is
global rather than facet-local.

The pure-spinor ideal is generated by the quadratic Wick relations among
these coordinates.  In characteristic two, the shortest relations are
\[
\begin{aligned}
0={}&p_{S\cup\{a,b,c,d\}}p_S
 +p_{S\cup\{a,b\}}p_{S\cup\{c,d\}}\\
&+p_{S\cup\{a,c\}}p_{S\cup\{b,d\}}
+p_{S\cup\{a,d\}}p_{S\cup\{b,c\}},
\end{aligned}
\tag{W2}
\]
and the odd-coordinate analogue, for every \(S\) and four distinct
\(a,b,c,d\notin S\).  The full finite family consists of the general
quadratic Wick relations.  This is the standard Pfaffian description of
the spinor variety; see Felipe Rincón,
[Isotropical Linear Spaces and Valuated Delta-Matroids](https://arxiv.org/abs/1004.4950).

For endpoints \(B,C\), substitute \(u=x_B+x_C\) into (W1)--(W2).  Every
Cartan equation then becomes a completely explicit quadratic polynomial
in the Boolean block variables of \(B\) and \(C\).  The endpoint
constraints are
\[
x_B,x_C\in\{0,1\}^{\binom Xr},\quad
Wx_B=Wx_C=\mathbf1,\quad
(x_B)_K=(x_C)_K=0\ (K\in A).
\tag{W3}
\]
Proving that (W3) implies all pulled-back Wick quadrics would prove the
pure-mate conjecture.  No such ideal-membership derivation is presently
known.

The linear moment equations emphatically do not suffice, even in the
all-odd \(r=3\) case.  For the standard Fano base
\[
A=\{012,034,056,135,146,236,245\},
\]
take one inactive sphere \(012\), and on the other spheres put the
following plus/minus missing points:
\[
\begin{array}{c|rrrrrr}
P&034&056&135&146&236&245\\ \hline
p_+&1&2&6&5&4&3\\
p_-&2&1&4&3&5&6.
\end{array}
\tag{W4}
\]
The resulting integral vector has one \(+1\) and one \(-1\) in six
spheres and satisfies
\[
W_{i,3}z=0\qquad(i=0,1,2)
\tag{W5}
\]
exactly.  Its spin class has \(q_S=0\) but annihilator dimension \(2\),
so it is not pure.  Hence all scalar moment identities, the full facet
trade equations, sphere shape, and all-odd parameters still do not imply
the Cartan quadrics.  Filling the inactive sphere identically on both
sides never gives even the correct point degrees, so (W4) does **not**
refute the genuinely nonlinear Boolean endpoint implication (W3).

The failed pure-spin equation can be displayed explicitly.  In
simple-root coordinates, take the hyperbolic polarization
\[
\begin{aligned}
E&=(0123,\ 0145,\ 1256),\\
F&=(1234,\ 0245,\ 0346)
\end{aligned}
\tag{W6}
\]
of the six-dimensional point quadratic space.  Choose the unique vacuum
annihilated by \(c(E)\), and index the resulting Fock basis by subsets of
\(\{1,2,3\}\).  Exact basis conversion sends (W4) to
\[
\psi_{\rm shaped}=p_{\{1\}}+p_{\{1,2\}}.
\tag{W7}
\]
A pure full spinor belongs entirely to one of
\(\bigwedge^{\rm even}E\) and \(\bigwedge^{\rm odd}E\), so in particular it
satisfies every mixed-chirality quadratic
\(p_Ip_J=0\) for \(|I|\not\equiv|J|\pmod2\).  The witness instead has
\[
p_{\{1\}}p_{\{1,2\}}=1.
\tag{W8}
\]
Thus (W4) violates a concrete quadratic equation.  In the same
polarization, all 28 genuine fixed-base mate differences lie wholly in
the even half-spin summand.

An exhaustive audit gives 112 nonzero shaped \(r=3\) trades: 70 have pure
class and 42 have nonpure class.  Across the four possible fillings of
their inactive sphere, the only 56 pairs with the correct point degrees
are precisely genuine Steiner endpoint pairs, all pure.  This isolates
the remaining issue sharply: the endpoint exact-degree constraints, not
the design moments, would have to generate the Wick equations.

## 6. Verdict

The pure-spin formulation passes the strongest available exact tests and
excludes the known nonlinear-relaxation false positive.  It is also
strictly stronger than \(q=0\).  But its only nonzero positive instance is
\(r=3\), where \(D_4\) triality is exceptional; the \(r=5\) family
collapses to zero in the spin quotient.
Therefore it is a precise new conjectural route, not a completed proof of
the \(r=15\) case.
