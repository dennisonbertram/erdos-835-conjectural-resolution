# The oriented cross-Gram signature attack

Date: 2026-07-24.  Verifier:
`evidence/verify_cross_gram_signature.py`.

Labels used below:

- **Proved** means an argument is given here.
- **Verified** means a finite computation is reproduced by the verifier.
- **Refuted** means there is an exact counterexample.
- **Open** means that no proof is known.

## 1. Setting and the crossing form

Let \(r\) be odd, \(v=2r+1\), and let \(A,B,C\) be
\(S(r-1,r,v)\) systems with
\[
 A\cap B=A\cap C=\varnothing .
\]
Write
\[
 B_0=B\setminus C,\qquad C_0=C\setminus B,\qquad
 h=|B\cap C|,\qquad t=|B_0|=b-h .
\]

Fix the standard orientation of \(\mathbb R^v\).  On the increasing
\(r\)-subset basis of \(\bigwedge^r\mathbb R^v\), put
\[
 {\cal T}=\iota_{e_0+\cdots+e_{v-1}}* .
\]
Thus \({\cal T}_{S,R}=0\) unless \(S\cap R=\varnothing\); in the latter
case it is the sign of the concatenation
\((S,R,X\setminus(S\cup R))\).  Since \(r\) is odd,
\[
 {\cal T}^{\mathsf T}=-{\cal T}.                 \tag{1.1}
\]

For \(S=(s_0<\cdots<s_{r-1})\), let
\[
 d_S=\sum_{i=0}^{r-1}(-1)^i
 e_{S\setminus\{s_i\}}
\]
be its oriented facet boundary.  The simplex identity is
\[
 {\cal T}^2=\partial^{\mathsf T}\partial-vI.      \tag{1.2}
\]

Every \(S\in B_0\) has a unique disjoint block
\(\phi(S)\in C_0\).  Consequently
\[
 P={\cal T}[B_0,C_0]                              \tag{1.3}
\]
is a signed permutation matrix.  Define the signed facet cross-Gram
matrix
\[
 G=(\langle d_S,d_R\rangle)_{S\in B_0,R\in C_0}
   ={\cal T}^2[B_0,C_0],                          \tag{1.4}
\]
and then
\[
 U=GP^{\mathsf T},\qquad
 \boxed{H=U+U^{\mathsf T}}.                       \tag{1.5}
\]

If
\[
 Q_{S,T}=\mathbf 1\{|S\cap\phi(T)|=r-1\},
\]
then \(U\) has exactly the zero pattern of \(Q\), with the natural
orientation signs.  Direct enumeration finds that \(Q\) is never
symmetric in the canonical \(r=3\) or \(r=5\) families.  The useful
object is the symmetric signed form \(H\), not \(Q\) itself.

## 2. Exact operator identities

Let \(P_D\) denote coordinate projection onto the blocks of a system
\(D\), and set
\[
 L_D={\cal T}P_D{\cal T}.                         \tag{2.1}
\]

**Lemma 2.1 (Proved).**
\[
 L_D^2=-(r+1)L_D,\qquad
 J_D=I+\frac{2}{r+1}L_D
\]
is a symmetric orthogonal involution.

**Proof.**
Let \(E_D\) be the coordinate inclusion and \(V_D={\cal T}E_D\).
The columns of \(V_D\) are the signed disjoint-neighbour vectors of
the blocks of \(D\).  Each has \(r+1\) entries of magnitude one.
Two distinct columns have disjoint supports: an \(r\)-set disjoint
from two distinct \(D\)-blocks would force those blocks to share an
\((r-1)\)-set, contrary to the Steiner property.  Hence
\[
 V_D^{\mathsf T}V_D=(r+1)I.
\]
By (1.1), \(L_D=-V_DV_D^{\mathsf T}\), and the displayed identities
follow immediately. \(\square\)

**Lemma 2.2 (Proved).**  On \(\mathbb R^{B_0}\),
\[
 \boxed{
 H=P_{B_0}\bigl({\cal T}P_C{\cal T}^2
       -{\cal T}^2P_C{\cal T}\bigr)P_{B_0}
   =\frac{r+1}{2}P_{B_0}[J_C,{\cal T}]P_{B_0}.}   \tag{2.2}
\]
Moreover
\[
 P_{B_0}J_CP_{B_0}=\frac{r-1}{r+1}I.             \tag{2.3}
\]

**Proof.**
Because \(P^{\mathsf T}=-P_C{\cal T}P_{B_0}\),
\[
 U=-P_{B_0}{\cal T}^2P_C{\cal T}P_{B_0};
\]
transposing gives the first formula in (2.2), and Lemma 2.1 gives the
second.  For (2.3), the \((S,T)\)-entry of
\({\cal T}P_C{\cal T}\), for \(S,T\in B_0\), is \(-1\) if \(S=T\)
and zero otherwise.  Indeed the unique \(C\)-block disjoint from
\(S\) cannot also be disjoint from a distinct \(B\)-block \(T\).
\(\square\)

The global commutator in (2.2) does have paired spectrum:
\[
 J_C[J_C,{\cal T}]+[J_C,{\cal T}]J_C=0.          \tag{2.4}
\]
The unresolved point is that compression to
\(\mathbb R^{B_0}\) need not preserve this anti-commutation.  Equation
(2.3) says only that the *diagonal compression* of \(J_C\) is scalar;
it does not make \(\mathbb R^{B_0}\) invariant under \(J_C\).

**Lemma 2.3 (Proved; swap identity).**  If the form for the reversed
ordered pair \((C,B)\) is transported back to \(B_0\) using \(P\), then
\[
 \boxed{P\,H(C,B)\,P^{\mathsf T}=-H(B,C).}        \tag{2.5}
\]

**Proof.**
\(G(C,B)=G^{\mathsf T}\) and
\({\cal T}[C_0,B_0]=-P^{\mathsf T}\).  Substitute these two identities
in (1.5), and use \(PP^{\mathsf T}=I\). \(\square\)

Thus the signature is an antisymmetric pair invariant.  Equation (2.5)
does not by itself identify a pair with its reversal.

## 3. The theorem that would prove the parity conjecture

The exact surviving target is:

> **Crossing-form conjecture (Open, \(r\ge3\)).**  If \(B\) and \(C\)
> have a common block-disjoint Steiner mate \(A\), then \(H(B,C)\) is
> nonsingular and has zero signature.  A stronger possible form says
> that its characteristic polynomial is even.

If this conjecture holds, then
\[
 t=\dim H=2\,n_+(H)
\]
is even.  Hence
\[
 |B\cap C|=b-t\equiv b\pmod2,                    \tag{3.1}
\]
which is exactly the fixed-base parity conjecture.  At \(r=15\), (3.1)
would rule out three pairwise block-disjoint \(S(14,15,31)\) systems and
settle the first open case of Erdős problem 835 negatively.

This is a sufficient structural theorem, not a proof.  Its two clauses
must both be supplied independently of the desired parity.

## 4. Exact and exhaustive small-case evidence

**Verified, \(r=3\).**  Fix a Fano plane \(A\).  It has eight disjoint
mates.  On all \(\binom82=28\) mate pairs,
\[
 t=6,\qquad H^2=8I,\qquad
 \chi_H(x)=(x^2-8)^3,\qquad
 \det H=-512,\qquad \operatorname{inertia}(H)=(3,3,0).
\]

The common base is essential.  Over all 435 unordered pairs of the 30
labelled Fano planes, the signature imbalance
\(|n_+(H)-n_-(H)|\) is:
\[
\begin{array}{c|ccc}
 |B\cap C|&0&1&3\\ \hline
 \text{imbalance}&5&0&2\\
 \text{number of pairs}&120&210&105 .
\end{array}
\]
Thus the crossing form is not balanced for arbitrary pairs of Steiner
systems.

**Verified, \(r=5\).**  For a deterministic \(S(4,5,11)\) base \(A\),
exact cover gives all 144 disjoint mates and all 10,296 unordered mate
pairs.  The verifier obtains:
\[
\begin{array}{c|c|c|c}
h&t&\text{number of pairs}&\text{inertia}\\ \hline
6&60&6336&(30,30,0)\\
18&48&3960&(24,24,0).
\end{array}
\]

The nonsingularity assertion in this table is exact: every matrix has
full rank over \(\mathbb F_{101}\), hence over \(\mathbb Q\).  The inertia
census uses a symmetric eigensolver; the smallest absolute eigenvalue in
the full census is greater than \(0.517\).  It is therefore strong
finite evidence, but it is labelled numerical rather than a general
proof.  Independently, the exact integer identities
\[
 \operatorname{tr}H=\operatorname{tr}H^3
 =\operatorname{tr}H^5=0
\]
hold on all 10,296 matrices.

For deterministic representatives of the two intersection types, exact
characteristic-polynomial factorization gives
\[
\begin{aligned}
h=6:\quad
(x^2-20)&(x^{10}-36x^8+418x^6-2028x^4+4049x^2-2756)\\
&\cdot(x^{24}-152x^{22}+9577x^{20}-328977x^{18}
+6845163x^{16}-90629163x^{14}\\
&\qquad+778660745x^{12}-4330680850x^{10}
+15191067377x^8-31618730813x^6\\
&\qquad+34331963136x^4-14575936720x^2
+2030508145)^2 ,
\end{aligned}                                                     \tag{4.1}
\]
and
\[
\begin{aligned}
h=18:\quad
&(x-2)(x+2)(x^2-20)
(x^3-8x-4)^2(x^3-8x+4)^2\\
&\qquad\cdot(x^4-52x^2+400)(x^4-20x^2+16)
(x^6-48x^4+416x^2-828)^4 .
\end{aligned}                                                     \tag{4.2}
\]
Both are even polynomials and have nonzero constant term.

There is also a compact exact certificate for each representative.
The verifier records a signed permutation matrix \(R\) satisfying
\[
 R^2=-I,\qquad R^{\mathsf T}HR=-H,
 \quad\text{equivalently}\quad RH=-HR.             \tag{4.3}
\]
This proves spectral pairing for those two matrices without numerical
diagonalization.  What is not known is how to construct \(R\) from the
Steiner axioms for an arbitrary triple.  Indeed, the underlying
permutation in each recorded \(R\) is already fixed-point-free, so merely
postulating such an \(R\) would assume that \(t\) is even.

The certificates are not disguised half-turns of the already observed
even monodromy cycles.  For the \(h=6\) representative, the canonical
triangle permutation has cycle lengths
\[
 2,2,2,4,6,44,
\]
but the underlying involution of \(R\) preserves no one of those cycles
setwise and sends only \(34\) of the \(60\) coordinates back into their
original cycle.  For the \(h=18\) representative the lengths are
\[
 2,2,2,2,18,22;
\]
again no cycle is preserved setwise, and only \(12\) of \(48\)
coordinates stay in their original cycle.  In neither case does the
involution conjugate the monodromy to its inverse.  Thus the finite
certificate genuinely mixes monodromy cycles, although a general
construction of it remains open.

## 5. Exact boundary cases and failed shortcuts

**Refuted at \(r=1\).**  The crossing-form conjecture is false if stated
for every odd \(r\).  Take
\[
 A=\{\{0\}\},\qquad B=\{\{1\}\},\qquad C=\{\{2\}\}
\]
as \(S(0,1,3)\) systems.  Then \(t=1\), \(G=(1)\), \(P=(1)\), and
\[
 H=(2),
\]
which is nonsingular and unbalanced.  Any valid theorem must assume
\(r\ge3\) and use more than the abstract perfect-code or reflection
identities of Section 2.

The following nearby ideas also fail on exact \(r=5\) representatives:

- \(U\) need not be nonsingular (rank \(59\) when \(h=6,t=60\));
- \(U-U^{\mathsf T}\) need not be nonsingular (rank \(46\) when
  \(h=18,t=48\));
- the unsigned \(Q\), \(Q+Q^{\mathsf T}\), and \(Q-Q^{\mathsf T}\)
  do not have a uniform determinant property;
- the support graph of \(H\) need not be bipartite.

Consequently ordinary determinant, Pfaffian, or support-bipartition
arguments do not yet prove (3.1).

## 6. Verdict

The cross-Gram construction is a genuine new reduction:

1. it is derived canonically from oriented disjointness and facet
   incidence;
2. nonsingularity is exactly verified on every accessible canonical
   \(r=3,5\) instance;
3. balanced signature is exhaustive in those instances and has exact
   anti-isometry certificates on the two deterministic \(r=5\)
   representatives.

But the required general theorem is **open**.  The global reflection
anti-commutation (2.4) does not automatically survive compression, and
the \(r=1\) example proves that the displayed operator identities alone
cannot force it.  A complete proof still needs a new Steiner-specific
construction of a nondegenerate balanced crossing form, or an
independent anti-isometry that does not presuppose \(t\) even.
