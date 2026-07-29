# Two exact no-go theorems for natural \(k=16\) constructions

This note concerns a hypothetical proper \(17\)-colouring of
\[
J(32,16).
\]
Equivalently, it concerns a partition of the \(16\)-subsets of a
32-point set into seventeen Steiner systems \(S(15,16,32)\).

The results below do **not** rule out an arbitrary, asymmetric colouring.
They rigorously rule out two especially natural ways in which the exceptional
identity \(32=2^5\) might have produced one:

1. a colouring equivariant under the full affine group
   \(\operatorname{AGL}(5,2)\), and
2. any fusion of the standard 32-colour XOR-syndrome colouring down to
   seventeen colours.

## 1. No \(\operatorname{AGL}(5,2)\)-equivariant colouring

Identify the 32 points with the additive group
\[
V=\mathbb F_2^5.
\]
Let
\[
G=\operatorname{AGL}(5,2)=V\rtimes \operatorname{GL}(5,2).
\]

By a \(G\)-equivariant 17-colouring we mean a proper colouring
\[
c:\binom V{16}\longrightarrow \Omega,\qquad |\Omega|=17,
\]
together with a homomorphism
\[
\varphi:G\longrightarrow \operatorname{Sym}(\Omega)
\]
such that
\[
c(gS)=\varphi(g)c(S)
\]
for every \(g\in G\) and every \(16\)-set \(S\).  Since every
\(15\)-star is a \(17\)-clique, a proper 17-colouring uses every colour.
Consequently the permutation \(\varphi(g)\), if equivariance is asserted, is
uniquely determined.

### Theorem 1

There is no \(\operatorname{AGL}(5,2)\)-equivariant proper 17-colouring of
\(J(32,16)\).

### Proof

We first show that the induced action of \(G\) on the seventeen colours must
be trivial.

All 31 nonzero translations are conjugate in \(G\), because
\(\operatorname{GL}(5,2)\) is transitive on \(V\setminus\{0\}\).  Their
images under \(\varphi\) therefore have a common number \(F\) of fixed
colours.  Burnside's lemma, applied to the action of the translation group
\(V\) on \(\Omega\), says that the number of colour-orbits is
\[
\frac{17+31F}{32}.
\]
This is an integer.  Reducing the numerator modulo 32 gives
\[
17-F\equiv0\pmod {32}.
\]
As \(0\le F\le17\), necessarily \(F=17\).  Thus every translation fixes
every colour, so \(V\le\ker\varphi\).

The colour action therefore factors through \(\operatorname{GL}(5,2)\).
We use two standard elementary facts about this group:

* \(\operatorname{GL}(5,2)=\operatorname{PSL}(5,2)\) is simple.  Indeed,
  over \(\mathbb F_2\) the determinant and scalar-centre quotients are
  trivial, and the usual simplicity theorem for
  \(\operatorname{PSL}(n,q)\) applies outside
  \((n,q)=(2,2),(2,3)\).
* \(\operatorname{GL}(5,2)\) contains an element of order 31.  Identify
  \(V\) with the additive group of \(\mathbb F_{32}\); multiplication by a
  primitive element of \(\mathbb F_{32}^{\times}\) is an
  \(\mathbb F_2\)-linear map of order 31.

If the resulting homomorphism
\(\operatorname{GL}(5,2)\to S_{17}\) were nontrivial, simplicity would make
it injective.  Its order-31 element would then map to an element of order
31 in \(S_{17}\), which is impossible: a permutation of prime order 31
requires a 31-cycle.  Hence \(G\) acts trivially on the colours.

It follows that every colour class \(\mathcal D\) is itself
\(G\)-invariant.  It is an \(S(15,16,32)\), and its number of blocks is
\[
b=\frac{\binom{32}{15}}{16}
 =\frac{\binom{32}{16}}{17}
 =35{,}357{,}670.
\]
Kummer's theorem shows that
\[
\nu_2\binom{32}{16}=1:
\]
adding \(16=10000_2\) to itself produces exactly one binary carry.
Division by the odd number 17 does not change the 2-adic valuation, so
\[
b\equiv2\pmod4.
\]

Consider the translation-group orbits on the blocks of \(\mathcal D\).
Their sizes are powers of two.  An orbit cannot have size one, since the
only subsets of the transitive \(V\)-set \(V\) fixed by every translation
are \(\varnothing\) and \(V\), not a 16-set.  Since the sum of the orbit
sizes is \(2\bmod4\), \(\mathcal D\) contains an odd number, in particular
at least one, of translation-orbits of size two.

Let \(B\) lie in such an orbit.  Its translation stabilizer \(H\) has
order 16, so \(H\) is a four-dimensional subspace of \(V\).  As \(B\) is
\(H\)-invariant, it is a union of \(H\)-cosets.  There are exactly two such
cosets and \(|B|=16\), hence \(B\) is one coset of \(H\).  Its size-two
translation orbit is precisely the pair of affine hyperplanes parallel to
\(H\).

The group \(\operatorname{GL}(5,2)\) is transitive on the
four-dimensional subspaces of \(V\).  Since \(\mathcal D\) is
\(G\)-invariant and contains one parallel class of affine hyperplanes, it
must contain all 31 parallel classes, i.e. all 62 affine hyperplanes of
\(\mathbb F_2^5\).

The same argument applies to every colour class.  Thus all seventeen
classes would contain the same 62 blocks, contradicting the fact that
colour classes are disjoint.  This proves the theorem. \(\square\)

### Small-parameter check

The argument makes the expected distinction between \(k=2\), where the
clique bound is attained, and the first failed analogue \(k=4\).

* For \(k=4\), put the eight points on \(\mathbb F_2^3\).  Burnside gives
  trivial translation action on five colours.  The simple group
  \(\operatorname{GL}(3,2)\) contains an element of order seven, so it
  cannot act nontrivially on five colours.  The same orbit argument then
  forces every invariant colour class to contain all affine hyperplanes.
  Thus an \(\operatorname{AGL}(3,2)\)-equivariant five-colouring is
  impossible, consistently with the known global nonexistence.
* For \(k=2\), translations again fix the three colours, but
  \(\operatorname{GL}(2,2)\cong S_3\) does act on them.  The standard
  colouring
  \[
  c(\{x,y\})=x+y\in\mathbb F_2^2\setminus\{0\}
  \]
  is exactly affine-equivariant.  This is precisely the step at which the
  \(k=16\) proof no longer applies.

## 2. No fusion of the XOR-syndrome colouring

For a subset \(S\subseteq V=\mathbb F_2^5\), define its XOR syndrome
\[
\sigma(S)=\sum_{x\in S}x\in V.
\]
If \(S=T\cup\{x\}\) and \(S'=T\cup\{y\}\) are adjacent 16-sets, then
\[
\sigma(S)+\sigma(S')=x+y\ne0.
\]
Thus \(\sigma\) is a proper 32-colouring of \(J(32,16)\).

A tempting binary-code construction would fuse its 32 syndrome values into
seventeen colours.  The next theorem rules out every such fusion, with no
linearity assumption on the fusion map.

### Theorem 2

For every map \(h:\mathbb F_2^5\to\Omega\) with \(|\Omega|=17\), the
colouring
\[
c(S)=h(\sigma(S))
\]
is not proper on \(J(32,16)\).

### Exact subset-XOR count

Fix distinct \(x,y\in V\), put \(d=x+y\), and let
\[
R=V\setminus\{x,y\}.
\]
For \(w\in V\), let
\[
N_w=\#\left\{T\in\binom R{15}:\sum_{t\in T}t=w\right\}.
\]
Then
\[
N_w=
\begin{cases}
4{,}850{,}640,&w\in\{x,y\},\\
4{,}847{,}208,&w\notin\{x,y\}.
\end{cases}
\tag{1}
\]
In particular, every \(w\in V\) occurs.

Here is a character derivation of (1).  Write the 32 additive characters
of \(V\) as
\[
\chi_a(z)=(-1)^{a\cdot z},\qquad a\in V.
\]
Character orthogonality gives
\[
N_w=\frac1{32}\sum_{a\in V}\chi_a(w)\,
[z^{15}]\prod_{r\in R}(1+\chi_a(r)z).
\tag{2}
\]
For the trivial character, the coefficient is
\[
\binom{30}{15}=155{,}117{,}520.
\]

Now let \(a\ne0\).  On all of \(V\), the character \(\chi_a\) takes each of
the values \(+1,-1\) sixteen times.

* If \(\chi_a(d)=-1\), then \(\chi_a(x)\) and \(\chi_a(y)\) have opposite
  signs.  On \(R\) there are fifteen plus signs and fifteen minus signs,
  so the relevant product is
  \[
  (1+z)^{15}(1-z)^{15}=(1-z^2)^{15}.
  \]
  Its \(z^{15}\)-coefficient is zero.
* If \(\chi_a(d)=1\), then
  \(\chi_a(x)=\chi_a(y)=s\in\{+1,-1\}\).  For \(s=+1\), the coefficient is
  \[
  [z^{15}](1+z)^{14}(1-z)^{16}
  =[z^{15}](1-z^2)^{14}(1-z)^2
  =2\binom{14}{7}=6864.
  \]
  For \(s=-1\), interchanging the plus and minus exponents changes the
  odd-degree coefficient's sign.  Thus in both cases the coefficient is
  \[
  6864\,\chi_a(x).
  \]

The characters satisfying \(\chi_a(d)=1\) form the 16-element annihilator
of the one-dimensional subspace \(\langle d\rangle\).  Therefore
\[
\sum_{\substack{a\ne0\\\chi_a(d)=1}}
\chi_a(w)\chi_a(x)
=
\begin{cases}
15,&w+x\in\langle d\rangle,\\
-1,&w+x\notin\langle d\rangle.
\end{cases}
\]
The first condition is exactly \(w\in\{x,y\}\).  Substitution into (2)
gives
\[
\frac{155{,}117{,}520+15\cdot6864}{32}
=4{,}850{,}640
\]
in the first case and
\[
\frac{155{,}117{,}520-6864}{32}
=4{,}847{,}208
\]
in the second, proving (1).

### Proof of Theorem 2

By the pigeonhole principle, there are distinct \(u,v\in V\) with
\[
h(u)=h(v).
\]
Put \(d=u+v\ne0\), and choose any \(x\in V\); set \(y=x+d\).  By (1), there
is a 15-set
\[
T\subseteq V\setminus\{x,y\}
\]
with
\[
\sigma(T)=u+x.
\]
The two 16-sets \(T\cup\{x\}\) and \(T\cup\{y\}\) are adjacent, while
\[
\sigma(T\cup\{x\})=u
\]
and
\[
\sigma(T\cup\{y\})=u+x+y=u+d=v.
\]
They receive the same fused colour, so the fusion is not proper.
\(\square\)

### Small-parameter check

For \(V=\mathbb F_2^3\), the analogous calculation after deleting
\(\{x,y\}\) counts 3-subsets of the remaining six points.  Each target XOR
occurs: the count is four for \(w\in\{x,y\}\) and two otherwise.
Consequently no map from the eight XOR syndromes to five colours can colour
\(J(8,4)\).

For \(V=\mathbb F_2^2\) and 2-subsets, by contrast, the XOR of two distinct
points is always one of the three nonzero vectors.  Keeping those three
values distinct gives the standard optimal colouring of \(J(4,2)\).

## 3. No additive pair-local construction

Another natural use of
\[
32=2(17-1)
\]
is to partition the ground set into sixteen labelled pairs and let the colour
be a sum of contributions from the local occupancy states of the pairs.  The
following short argument rules out this whole ansatz.

For \(1\le i\le16\), let \(P_i=\{i_0,i_1\}\), and suppose there are arbitrary
functions
\[
f_i:\{\varnothing,\{i_0\},\{i_1\},P_i\}\longrightarrow\mathbb F_{17}
\]
such that
\[
c(S)=\sum_{i=1}^{16} f_i(S\cap P_i)
\tag{3}
\]
is proposed as a colour for every 16-set \(S\).

### Theorem 3

No function of the form (3) is a proper 17-colouring of \(J(32,16)\).

### Proof

For each pair define the increments
\[
\begin{aligned}
u_i^\epsilon&=f_i(\{i_\epsilon\})-f_i(\varnothing),\\
v_i^\epsilon&=f_i(P_i)-f_i(\{i_\epsilon\}),
\qquad \epsilon\in\{0,1\}.
\end{aligned}
\]

Take a 15-set \(T\) which leaves one pair \(P_a\) empty and selects one
point from each of the other fifteen pairs.  Relative to the common value
\(\sum_i f_i(T\cap P_i)\), the seventeen colours obtained by extending
\(T\) are
\[
\{u_a^0,u_a^1\}\ \cup\
\{v_b^{\epsilon_b}:b\ne a\},
\tag{4}
\]
where \(i_{\epsilon_i}\) is the selected point of the singleton pair
\(P_i\).  The star is rainbow exactly when (4) is the whole field
\(\mathbb F_{17}\), with no repetition.

Fix \(a\) and \(b\ne a\), and reverse the selected point in \(P_b\), leaving
all other choices unchanged.  The two multisets (4) are both
\(\mathbb F_{17}\) and differ in only one entry.  Hence
\[
v_b^0=v_b^1=:v_b.
\tag{5}
\]
As the empty pair \(a\) can be chosen independently of \(b\), (5) holds for
every \(b\).

For a fixed \(a\), (4) now says
\[
\{u_a^0,u_a^1\}\ \cup\ \{v_b:b\ne a\}=\mathbb F_{17}
\tag{6}
\]
without repetitions.  Given distinct \(b,c\), choose
\(a\notin\{b,c\}\) in (6); this shows \(v_b\ne v_c\).  Thus the sixteen
values \(v_1,\ldots,v_{16}\) are distinct.  Let \(r\) be the unique element
of \(\mathbb F_{17}\) outside their set.  Equation (6) forces
\[
\{u_a^0,u_a^1\}=\{r,v_a\}
\tag{7}
\]
for every \(a\).

Finally take a 15-set with one full pair \(P_d\), two empty pairs
\(P_a,P_c\), and one selected point in each of the remaining thirteen
pairs.  Its seventeen extension increments are
\[
\{u_a^0,u_a^1,u_c^0,u_c^1\}
\ \cup\ \{v_b:b\notin\{a,c,d\}\}.
\]
By (7), the value \(r\) occurs once among the two \(P_a\)-increments and
once among the two \(P_c\)-increments.  This star has a repeated colour,
the required contradiction. \(\square\)

This includes arbitrary signed-sum and occupancy-correction formulas over
\(\mathbb F_{17}\).  It also rules out multiplicative pair-local formulas
whenever a discrete logarithm converts all of their local factors into
additive contributions.  It does not cover formulas with genuine
interactions between different pairs.

## 4. No hyperoctahedrally equivariant construction

The pair-local theorem assumed an additive formula.  If one instead demands
the full natural symmetry of sixteen unordered pairs, no formula assumption
is needed.

Let
\[
W=C_2^{16}\rtimes S_{16}
\]
act on the 32 points: the base group independently swaps the two points in
each pair, and \(S_{16}\) permutes the pairs.

### Theorem 4

There is no \(W\)-equivariant proper 17-colouring of \(J(32,16)\), even when
\(W\) is allowed to permute the seventeen colours.

### Proof

Suppose such a colouring exists, with colour action
\[
\varphi:W\longrightarrow S_{17}.
\]
Write the base group additively as \(E_0=\mathbb F_2^{16}\), with standard
basis vector \(e_i\) representing the swap in pair \(i\), and let
\[
K=\ker(\varphi|_{E_0}).
\]
The subgroup \(K\) is invariant under the coordinate-permuting action of
\(S_{16}\).

An elementary abelian 2-subgroup of \(S_{17}\) has rank at most eight.  One
quick proof is to decompose its permutation action into orbits.  An orbit
of size \(2^r\) contributes at most \(r\) to a faithful quotient, and
\(r\le2^{r-1}\); summing over the nonsingleton orbits gives at most
\(\lfloor17/2\rfloor=8\).  Consequently
\[
\dim K\ge16-8=8.
\]

The only \(S_{16}\)-invariant subspaces of \(\mathbb F_2^{16}\) with
dimension at least eight are
\[
E=\left\{z:\sum_i z_i=0\right\}
\quad\text{and}\quad
\mathbb F_2^{16}.
\tag{8}
\]
For completeness, if an invariant subspace contains a vector other than
\(0\) or the all-ones vector, a transposition exchanging one coordinate in
its support with one outside its support shows that it contains some
\(e_i+e_j\).  Coordinate permutations then give every \(e_i+e_j\), whose
span is \(E\).  An additional odd-weight vector expands \(E\) to the whole
space.  This proves (8).

If \(K=\mathbb F_2^{16}\), every swap \(e_i\) fixes every colour.  Choose a
16-set containing exactly one point of pair \(i\).  Swapping that pair
produces an adjacent 16-set of the same colour, a contradiction.

It remains that \(K=E\).  Then all sixteen coordinate swaps have the same
nontrivial image
\[
\tau=\varphi(e_1)=\cdots=\varphi(e_{16}),
\]
an involution of the seventeen colours.  Every involution on an odd set
has a fixed colour; call one such colour \(a\).

The colour-\(a\) class has
\[
\frac{\binom{32}{16}}{17}=35{,}357{,}670
\]
vertices.  Only
\[
\binom{16}{8}=12{,}870
\]
16-sets have no singleton pair: such a set must take both points from eight
pairs and neither point from the other eight.  Hence some colour-\(a\)
vertex \(S\) has a singleton pair \(i\).  The set \(e_iS\) is adjacent to
\(S\), while equivariance gives
\[
c(e_iS)=\tau(c(S))=\tau(a)=a,
\]
again a contradiction. \(\square\)

At \(k=2\), the corresponding fixed colour class has exactly enough room
to consist of the two no-singleton edges, and the usual three-colouring is
indeed equivariant.  At \(k=16\), Theorem 4 rules out arbitrary nonlinear
constructions retaining the full signed-pair symmetry; a successful
pair-based construction must break that symmetry substantially.

## 5. No equivariance under a 31-cycle

The affine theorem used the full group \(\operatorname{AGL}(5,2)\).  A
different one-line obstruction rules out a much smaller cyclic symmetry
which occurs naturally when the 31 nonzero field elements are labelled
cyclically.

**Theorem 5.**  Let \(g\) be a permutation of the 32 points with cycle type
\(31\,1\).  There is no proper 17-colouring of \(J(32,16)\) equivariant
under \(\langle g\rangle\), even if \(\langle g\rangle\) is allowed to
permute the colours.

**Proof.**  Equivariance supplies a homomorphism
\[
 \varphi:\langle g\rangle\longrightarrow S_{17}.
\]
The image of \(g\) has order dividing the prime 31.  Since a permutation of
17 objects cannot have order 31, \(\varphi(g)=1\): \(g\) fixes every colour.

Write the long cycle as
\[
 (z_0\,z_1\,\ldots\,z_{30}).
\]
The two 16-sets
\[
 B=\{z_0,z_1,\ldots,z_{15}\},
 \qquad
 gB=\{z_1,z_2,\ldots,z_{16}\}
\]
differ by one exchange and hence are adjacent in \(J(32,16)\).  But
equivariance and the trivial colour action give
\[
 c(gB)=\varphi(g)c(B)=c(B),
\]
a contradiction. \(\square\)

The same argument applies to the forced \(LS(3,4,20)\) shadow.  If an
order-19 permutation acts as a 19-cycle and one fixed point, its action on
17 colours is trivial.  The consecutive quadruples
\(\{z_0,z_1,z_2,z_3\}\) and \(\{z_1,z_2,z_3,z_4\}\) would then be adjacent
and have the same colour.  Thus neither the original large set nor this
derived shadow can retain the most obvious prime-cycle symmetry.

## 6. No projectivized sum of two affine \(\mathbb F_{16}\)-lines

Another natural use of \(32=2\cdot16\) labels the points by
\(\mathbb F_{16}\times\{0,1\}\), embeds the two layers as affine lines in
\(\mathbb F_{16}^2\), sums the sixteen selected vectors, and takes its
projective class in
\(\mathbb P^1(\mathbb F_{16})\), which has seventeen points.  The following
argument rules out the entire affine-line family, including global
\(\operatorname{GL}_2(\mathbb F_{16})\) changes of coordinates and
independent nonzero rescalings of the layers.

**Theorem 6.**  Choose arbitrary vectors
\[
 u_0,u_1,w_0,w_1\in\mathbb F_{16}^2,
 \qquad u_0,u_1\ne0,
\]
and label point \((x,e)\) by
\[
 v(x,e)=x u_e+w_e.
\]
The rule
\[
 c(S)=\left[\sum_{(x,e)\in S}v(x,e)\right]
 \in\mathbb P^1(\mathbb F_{16})
 \tag{9}
\]
wherever the sum is nonzero is not a proper colouring of
\(J(32,16)\).

**Proof.**  Let \(H\) be any three-dimensional \(\mathbb F_2\)-subspace of
\(\mathbb F_{16}\).  It has eight elements and
\[
 \sum_{h\in H}h=0.
\]
Choose \(r\notin H\), a nonzero \(h\in H\), and
\[
 q\notin H,\qquad q\notin\{r,r+h\}.
\]
Such a \(q\) exists because the complement of \(H\) has eight elements.
Put
\[
 A=(H\setminus\{0\})\cup\{r\},\qquad B=H,
\]
and form the 16-set
\[
 S=(A\times\{0\})\cup(B\times\{1\}).
\]
Replace \((h,0)\) by \((q,0)\) to obtain the adjacent 16-set \(S'\).

Both layers of \(S\) and \(S'\) have size eight, so their affine offset
terms vanish in characteristic two.  Moreover
\[
 \sum_{a\in A}a=r,\qquad
 \sum_{b\in B}b=0,\qquad
 \sum_{a\in A\setminus\{h\}\cup\{q\}}a=r+h+q.
\]
The choices ensure that \(r\) and \(r+h+q\) are nonzero.  Therefore the two
vector sums in (9) are the nonzero vectors
\[
 r u_0,\qquad (r+h+q)u_0.
\]
They are distinct scalar multiples of the same vector and hence determine
the same point of \(\mathbb P^1(\mathbb F_{16})\).  Thus \(S\) and \(S'\)
are adjacent and have the same colour. \(\square\)

The special proposal \(v(x,e)=(x,a_e)\) is included by taking
\(u_0=u_1=(1,0)\) and \(w_e=(0,a_e)\).  Notice that the proof never uses
the relation between the two lines: even skew or coincident affine lines,
layer rescalings, and a common projective coordinate change all fail.

## 7. No construction from the quotient or difference alone

The exact odd-neighbour lift replaces the original problem by a
17-colouring of \(J(30,15)\).  Label its points by
\(\mathbb F_{16}^{\!*}\times\{0,1\}\).  A vertex is encoded by
\[
 A=\{x:(x,0)\in S\},\qquad
 C=\{x:(x,1)\notin S\}.
\]
The equality \(|S|=15\) is precisely \(|A|=|C|\).  Put
\[
 P_A(X)=\prod_{a\in A}(X-a),\qquad
 P_C(X)=\prod_{c\in C}(X-c).
\]

**Theorem 7.**  No rule depending only on either the rational function
\[
 R_S(X)=\frac{P_A(X)}{P_C(X)}
 \in\mathbb F_{16}(X)
 \tag{10}
\]
or the polynomial difference
\[
 D_S(X)=P_A(X)-P_C(X)
\]
is a proper colouring of \(J(30,15)\), regardless of how the rational
function or polynomial is postprocessed.

**Proof.**  Choose \(a\in\mathbb F_{16}^{\!*}\).  Let \(S\) contain the
first-layer point \((a,0)\) and every second-layer point except \((a,1)\).
Then \(S\) has fifteen points and its pair is
\[
 A=C=\{a\}.
\]
Replace \((a,0)\) by \((a,1)\), obtaining the adjacent vertex \(S'\).  Its
pair is \(A'=C'=\varnothing\).  Consequently
\[
 R_S(X)=\frac{X-a}{X-a}=1
 =\frac{1}{1}=R_{S'}(X).
\]
At the same time,
\[
 D_S(X)=(X-a)-(X-a)=0=1-1=D_{S'}(X).
\]
Every postprocessing of either statistic gives \(S\) and \(S'\) the same
colour. \(\square\)

More generally, any vertical exchange at a label in \(A\cap C\) removes
the same factor from numerator and denominator.  The theorem therefore
rules out all evaluations, zero/pole data, divisors, continued-fraction
data, and normalized coefficient formulas which see only the reduced
quotient.  It does not cover genuinely two-polynomial rules which retain
the ordered pair \((P_A,P_C)\).  In particular, the theorem now subsumes
every coefficient, degree, root, or evaluation rule applied only to
\(P_A-P_C\), including the leading-coefficient proposal tested separately.

## 8. Product ratio plus common-factor parity still needs 28 colours

The quotient obstruction suggests repairing vertical edges by remembering
the parity of the cancelled common factors.  Even arbitrary postprocessing
of those two statistics cannot use only seventeen colours.

For an equal-size pair \((A,C)\), put
\[
 \rho(A,C)=\frac{\prod_{a\in A}a}{\prod_{c\in C}c}
 \in\mathbb F_{16}^{\!*},
 \qquad
 \epsilon(A,C)=|A\cap C|\pmod2.
\]

**Theorem 8.**  Let \(\Omega\) be a colour set.  If
\[
 c(A,C)=f_{\epsilon(A,C)}(\rho(A,C))
 \tag{11}
\]
properly colours \(J(30,15)\), then \(|\Omega|\ge28\).  In particular,
no 17-colour rule of this form exists.

**Proof.**  Write \(G=\mathbb F_{16}^{\!*}\setminus\{1\}\), so
\(|G|=14\).  We prove that \(f_0(G)\) and \(f_1(G)\) are disjoint sets of
fourteen colours.

First take distinct \(a,b\in G\).  For any \(w\ne0\), the pairs
\[
 (\{aw\},\{w\}),\qquad(\{bw\},\{w\})
\]
encode adjacent vertices: in the first layer, replace \(aw\) by \(bw\).
Both intersections are empty and their product ratios are \(a,b\).
Therefore \(f_0(a)\ne f_0(b)\), so \(f_0\) is injective on \(G\).

For odd parity, choose
\[
 t\notin\{1,a,b\}.
\]
The adjacent pairs
\[
 (\{t,a\},\{t,1\}),\qquad
 (\{t,b\},\{t,1\})
\]
both have intersection exactly \(\{t\}\) and ratios \(a,b\).  Hence
\(f_1\) is injective on \(G\).

It remains to show the two images are disjoint.  Fix \(a,b\in G\).  If
\(a\ne b\), put \(d=b/a\ne1\).  Choose
\[
 w\notin\{1,d,a^{-1},a^{-1}d\};
\]
there is ample room in the 15-element multiplicative group.  The pair
\[
 A=\{1,aw\},\qquad C=\{1,w\}
\]
has intersection \(\{1\}\) and ratio \(a\).  Replacing the first-layer
label \(1\) by \(d\) gives
\[
 A'=\{d,aw\},\qquad C'=\{1,w\}.
\]
The choice of \(w\) makes \(A'\cap C'=\varnothing\), and
\[
 \rho(A',C')=\frac{daw}{w}=b.
\]
Thus properness gives \(f_1(a)\ne f_0(b)\).

If \(a=b\), use the same \(A,C\) with
\(w\notin\{1,a^{-1}\}\), and make the vertical exchange at label \(1\).
It removes \(1\) from both sets, leaving
\[
 A'=\{aw\},\qquad C'=\{w\}.
\]
The parity changes from one to zero while the ratio remains \(a\), so
again \(f_1(a)\ne f_0(a)\).

We have proved
\[
 |f_0(G)\cup f_1(G)|=14+14=28,
\]
which proves the theorem. \(\square\)

This includes every attempted repair
\(\rho\mapsto\tau^{\epsilon}(\rho)\), even when \(\tau\) is an arbitrary
permutation of the projective line rather than a Möbius transformation.

## Scope

Theorem 1 says that a successful binary, Reed--Muller, Kerdock, bent-function,
or affine-geometric construction cannot retain the full
\(\operatorname{AGL}(5,2)\) symmetry, even if that symmetry is allowed to
permute the colours.  Theorem 2 is stronger for constructions that depend
only on the ordinary binary syndrome: breaking affine symmetry in the
postprocessing map does not help.  Theorem 3 separately eliminates all
additive pair-local constructions, while Theorem 4 eliminates arbitrary
nonlinear constructions with the full signed-pair symmetry.  Theorem 5
additionally eliminates every construction equivariant under a single
31-cycle on the nonfixed points; its derived analogue eliminates
19-cycle-equivariant \(LS(3,4,20)\) constructions.  Theorem 6 eliminates
all constructions obtained by projectivizing the vector sum of two affine
\(\mathbb F_{16}\)-line embeddings.  Theorem 7 eliminates arbitrary
postprocessing of either the reduced quotient or the difference of the two
subset polynomials in the 30-point lift.  Theorem 8 shows that augmenting
the product quotient by common-factor parity still requires at least
28 colours.

These theorems do not exclude a construction using a smaller symmetry group
and genuinely higher-order interactions between points or pairs.  In
particular, nonlinear \(P^1(\mathbb F_{16})\), Paley, Pfaffian, and
difference-family ansätze remain outside their combined formal scope.
