# Exact cyclic-17 reduction for the first open case

This note tests a genuine colour-transitive symmetry for
Erdős--Rosenfeld problem 835 at \(k=16\).  It does **not** assume that every
solution has this symmetry.

Let the 32 points be
\[
 A\sqcup F,\qquad A=\mathbb Z_{17},\quad |F|=15,
\]
and suppose translation \(x\mapsto x+1\) on \(A\), fixing \(F\), sends every
colour \(q\) to \(q+1\).  A tight colouring is the same as a large set
\(LS(15,16,32)\).

## 1. The exact starter formulation

Write \(D\) for colour zero.  No 16-subset is fixed by the translation, so
every block orbit has length 17.  Equivariance is therefore equivalent to:

1. \(D\) contains exactly one block from every translation orbit; and
2. \(D\) is an \(S(15,16,32)\).

Indeed, the seventeen translates of such a starter are disjoint, cover every
16-subset, and are all Steiner systems.

For a completely explicit zero-one formulation, write a block as
\((X,Y)\), where \(X\subseteq A\), \(Y\subseteq F\), and
\(|X|+|Y|=16\), and let \(d(X,Y)\) be its indicator in \(D\).  The two
conditions are
\[
 \sum_{t\in\mathbb Z_{17}}d(X+t,Y)=1                                      \tag{1}
\]
for every block orbit, and
\[
 \sum_{a\in A\setminus U}d(U\cup\{a\},V)
 +\sum_{f\in F\setminus V}d(U,V\cup\{f\})=1                              \tag{2}
\]
for every \(15\)-set \((U,V)\).  Equations (1)--(2) are an exact quotient,
not a relaxation.

## 2. Complement closure is forced

Complement closure is not an extra ansatz here.  The degree of
\(J(32,16)\) is \(256\), its least eigenvalue is \(-16\), and a
17-colouring attains the Hoffman bound.  Hence the centred indicator of
each colour class lies in the last Johnson eigenspace \(E_{16}\).  The
complement permutation acts on \(E_j\) as \((-1)^j\), so it acts as \(+1\)
on \(E_{16}\).  Consequently
\[
             c(B)=c(B^c)                                                  \tag{3}
\]
for every 16-set \(B\).

This pairs the two block layers described below.  It does not by itself
construct the middle layer or prove that the cyclic symmetry exists.

## 3. Layer recursion

It is more convenient to record the omitted fixed points.  For
\(R\subseteq F\), \(|R|=s\), and \(X\subseteq A\), \(|X|=s+1\), set
\[
 C_R(X)=c\bigl(X\cup(F\setminus R)\bigr).
\]
Equivariance says
\[
 C_R(X+t)=C_R(X)+t.                                                        \tag{4}
\]
After translating the origin, the first layer is
\(C_\varnothing(\{x\})=x\).

For \(|U|=|R|=s\), the rainbow condition on the corresponding 15-set is
exactly
\[
 \{C_{R\setminus\{f\}}(U):f\in R\}
 \mathbin{\dot\cup}
 \{C_R(U\cup\{a\}):a\in A\setminus U\}
 =\mathbb Z_{17}.                                                         \tag{5}
\]
Thus the construction proceeds one block layer at a time.

In colour-zero form, let
\[
 {\cal D}_R=\{X:C_R(X)=0\}.
\]
Equation (4) says that \({\cal D}_R\) chooses one translate from every
\((s+1)\)-subset orbit.  If the already constructed colours in the first
set of (5) are distinct, define their zero leave
\[
 L_R=\{U: C_{R\setminus\{f\}}(U)=0\text{ for some }f\in R\}.
\]
Then (5), for all colours, is equivalent to the finite exact cover
\[
 \#\{X\in{\cal D}_R:U\subset X\}=
 \begin{cases}
 0,&U\in L_R,\\
 1,&U\notin L_R.
 \end{cases}                                                              \tag{6}
\]
After all \(R\)'s of one size have been chosen, the colours supplied to the
next layer must also be pairwise distinct.  This cross-\(R\) compatibility
is essential; solving (6) independently for every \(R\) is not enough.

Complement closure becomes
\[
 C_R(X)=C_{F\setminus R}(A\setminus X).                                   \tag{7}
\]
One may therefore choose layers \(|R|\le 7\), reflect them by (7), and
then impose the remaining middle compatibility between the
\(|R|=7\) and \(|R|=8\) layers.  Equivalently, the colour-zero starter must
be an independent set in \(J(32,16)\); its forced size then makes it an
\(S(15,16,32)\).

## 4. The first two nontrivial layers

For \(R=\{i\}\), equation (5) says that
\[
 S_i(x,x)=x,\qquad S_i(x,y)=C_{\{i\}}(\{x,y\})
\]
is a translation-equivariant symmetric idempotent Latin square on
\(\mathbb Z_{17}\).  Cross-\(R\) compatibility says that the fifteen
squares form a golf design \(G(17)\).  This conclusion is forced by the
17-cycle.

The current computation fixes the explicit Wallis circulant \(G(17)\)
already audited in `global_latin_audit.py`.  Choosing that particular golf
design is an ansatz, not a without-loss-of-generality step.

For \(R=\{i,j\}\), there are 40 translation orbits of moving triples.
Equation (6) asks for one translate from each orbit which decomposes
\(K_{17}\) minus the two colour-zero one-factors belonging to \(S_i,S_j\).
Adjoin two points \(i,j\).  The selected moving triples, the triples
\(\{i,x,y\}\) and \(\{j,x,y\}\) from those two one-factors, and
\(\{i,j,0\}\) form an \(STS(19)\).  Translating produces a cyclic
\(LS(2,3,19)\) with the two prescribed links.  This equivalence gives a
small, independently checkable 40-phase model for each fixed pair.

Single slices do not glue automatically.  For each moving-triple orbit,
the 40 phases on the 105 edges of \(K_{15}\) must, separately, be proper
edge-colourings: phases on two fixed-pair edges sharing a fixed point must
differ.  The `--joint` model imposes exactly this condition together with
all 105 slice exact covers.  It has 4,200 phase variables, represented by
71,400 primary one-hot variables.

## 5. Four scopes that must not be conflated

1. **One fixed-pair slice.**  This is one prescribed-link cyclic
   \(LS(2,3,19)\).  It proves only that one \(R=\{i,j\}\) slice is feasible.
2. **The joint moving-triple layer.**  All 105 slices plus the shared
   phase constraints are exactly the translation-equivariant,
   fixed-Wallis-golf radius-five boundary.  Even a certificate here reaches
   only \(|R|=2\).
3. **A cyclic \(LS(4,5,21)\).**  Fixing eleven of the fifteen fixed points
   in a hypothetical full large set gives this necessary derived design.
   It is a different finite shadow; finding it would not supply the joint
   layer above or a full \(LS(15,16,32)\).
4. **Erdős--Rosenfeld 835.**  A positive solution requires all layers
   through \(|R|=7\), their complements, and the middle compatibility.
   A no-go for the Wallis golf starter, or even for every cyclic-17
   starter, would not rule out a nonsymmetric tight colouring.

## 6. Reproducible commands

The search and semantic checks are in
`evidence/search_cyclic17_r3_extension.py`.

```sh
# A diagnostic single slice.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --only-fixed-pair 0,1 --sat-solver maplechrono \
  --output /tmp/cyclic17-r3-01.json

# Recheck a partial certificate without asserting that all 105 exist.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --verify evidence/cyclic17_r3_pair_0_1_certificate.json \
  --only-fixed-pair 0,1

# Solver-independent reconstruction and incidence audit of its LS(2,3,19).
python3 -B evidence/verify_cyclic17_r3_pair.py \
  evidence/cyclic17_r3_pair_0_1_certificate.json --fixed-pair 0,1

# The genuinely coupled layer.
python3 -B evidence/search_cyclic17_r3_extension.py \
  --joint --sat-solver maplechrono \
  --output /tmp/cyclic17-r3-joint.json
```

As of this note, the slices \((0,1)\) and \((0,2)\) have direct-verified
phase witnesses.  The coupled search is still running.  Neither fact
settles problem 835.
