# Audit of Theorem 3 and the obstruction to a universal-moment bridge

## Verdict

The proof of Theorem 3 in `algebraic_construction_no_go.md` is sound.
In particular, the ordered-minor signs, the rank reduction to a
two-dimensional quotient, the eighth-power argument, and the
first-power recurrence are mutually consistent.

The same contradiction does **not** currently extend to an arbitrary
seventeen-colouring.  The precise missing ingredient is the
rank-two alternating (Pluecker) factorisation of the labels in every
14-column link.  The universal \(\mathbb F_{17}\) power identities say
only that such a link is a one-factorisation of \(K_{18}\); they neither
imply the Pluecker relations nor provide vertex vectors from which the
recurrence in Theorem 3 can be formed.

## 1. Line-by-line audit of the determinant link

Let \(R\) be fourteen columns of a hypothetical matrix \(G\).

1. **Rank of \(R\).** If \(\operatorname{rank}R\leq 13\), choose any
   column \(i\notin R\).  The 15-set \(R\cup\{i\}\) has rank at most
   fourteen, so adjoining any of its seventeen possible extensions
   produces a singular 16-set.  Its entire star would therefore have
   colour zero, contradicting rainbowness.  Thus
   \(\operatorname{rank}R=14\).

2. **Nonzero quotient vectors.** If the image of an outside column
   \(i\) in the quotient by \(\langle R\rangle\) were zero, the same
   argument applied to the 15-set \(R\cup\{i\}\) would make all its
   extensions singular.  Hence all eighteen quotient vectors are
   nonzero.

3. **The ordering sign.** Write \(R\) in increasing global order and
   take \(i<j\) outside \(R\).  Moving the appended columns \(i,j\)
   into their places among the columns of \(R\) makes
   \[
      \#\{r\in R:r>i\}+\#\{r\in R:r>j\}
   \]
   transpositions.  Therefore the sign is \(s_i s_j\), with
   \[
      s_i=(-1)^{|\{r\in R:r>i\}|}.
   \]
   Replacing the \(i\)-th quotient vector by \(s_i\) times that vector
   consequently gives one common nonzero scalar times
   \(\det(u_i,u_j)\) for every \(i<j\).  There is no unabsorbed
   pair-dependent sign.

4. **Symmetric edge labels.** In the star based at
   \(R\cup\{i\}\), the edge to \(j<i\) is labelled
   \(d_{ji}=\det(u_j,u_i)\), while the edge to \(j>i\) is labelled
   \(d_{ij}=\det(u_i,u_j)\).  This is exactly the displayed row in
   the theorem, and rainbowness makes its seventeen entries all of
   \(\mathbb F_{17}\).

5. **Parallel classes.** Every such row has exactly one zero.  Since
   determinant zero is projective parallelism, every quotient vector
   has exactly one parallel mate.  A projective parallel class cannot
   have size larger than two (each member would then have at least two
   zero neighbours), so the eighteen vectors occupy exactly nine
   directions, twice each.

6. **Finite slopes.** The projective line over \(\mathbb F_{17}\) has
   eighteen directions.  Nine are unused, so one unused direction can
   be moved to infinity.  Every used direction then has a finite,
   distinct slope \(t_e\), and its two vectors have the form
   \(a_e(1,t_e),b_e(1,t_e)\) with \(a_e,b_e\ne0\).

7. **Eighth moment.** For a row belonging to
   \(a_e(1,t_e)\), its eighth-power sum is
   \[
      a_e^8\sum_{f\ne e}
      (a_f^8+b_f^8)(t_f-t_e)^8.
   \]
   The analogous formula holds with \(b_e^8\) for the mate row.
   The leading scalar is nonzero and can be divided out.  Because
   eight is even, changing \(\det(u_i,u_j)\) to
   \(\det(u_j,u_i)\) contributes no sign.  Thus equation (13) is
   correct.

8. **Shifted-power independence.** The polynomial
   \[
      F(x)=\sum_f(a_f^8+b_f^8)(t_f-x)^8
   \]
   has degree at most eight and nine distinct roots.  Moreover the
   coefficient matrix of the nine shifted powers is a Vandermonde
   matrix times the nonzero diagonal entries
   \(\binom80,\ldots,\binom88\) in \(\mathbb F_{17}\).  Hence all
   \(a_f^8+b_f^8\) vanish, and every mate ratio \(r\) satisfies
   \(r^8=-1\).  In particular \(r\ne-1\).

9. **First moment and recurrence.** With
   \(P_i=\sum_{j<i}u_j\) and \(W=\sum_j u_j\), the symmetric ordered
   row sum is
   \[
   \begin{aligned}
      \sum_{j<i}\det(u_j,u_i)+\sum_{j>i}\det(u_i,u_j)
      &=\det(P_i,u_i)+\det(u_i,W-P_i-u_i)\\
      &=\det(u_i,W-2P_i).
   \end{aligned}
   \]
   Thus \(Q_i=W-2P_i\) and \(Q_{i+1}=Q_i-2u_i\) are correct.

10. **Forced opposite mate.** If \(Q_0,Q_1,Q_2\) were all nonzero,
    the recurrence and \(\det(u_i,Q_i)=0\) would put
    \(u_0,u_1,u_2\) in the same projective direction, impossible.
    At the first \(i\le2\) with \(Q_i=0\), \(Q_{i+1}=-2u_i\), so
    \(u_{i+1}\) is the unique mate of \(u_i\).  If \(Q_{i+2}\ne0\),
    then \(u_{i+2}\) would be a third vector in that direction.
    Hence \(Q_{i+2}=0\), giving \(u_{i+1}=-u_i\), in contradiction
    with the eighth moment.

This also shows why the proof is genuinely order-sensitive in its first
moment but order-insensitive in its eighth moment: both uses of signs
have been accounted for explicitly.

## 2. What the universal power identities give

Now let
\[
   c:\binom{[32]}{16}\longrightarrow\mathbb F_{17}
\]
be an arbitrary hypothetical proper colouring, and again fix a
14-set \(R\).  Put \(V=[32]\setminus R\), so \(|V|=18\), and define
the symmetric edge label
\[
   \lambda_{ij}=c(R\cup\{i,j\})\qquad(i\ne j\in V).
\]

For each \(i\), the seventeen 16-sets containing the 15-set
\(R\cup\{i\}\) form a clique.  Consequently
\[
   \{\lambda_{ij}:j\ne i\}=\mathbb F_{17}.
   \tag{1}
\]
Equivalently, the edges of \(K_{18}\) have a proper 17-edge-colouring,
and every colour class is a perfect matching.

Taking powers in (1) gives all the universal scalar moment identities:
\[
 \sum_{j\ne i}\lambda_{ij}^m=
 \begin{cases}
 0,&1\le m\le15,\\
 -1,&m=16.
 \end{cases}
 \tag{2}
\]
Thus the power-vector formulation
\[
   \sum_{j\ne i}
   (\lambda_{ij},\lambda_{ij}^2,\ldots,\lambda_{ij}^{15})=0
   \tag{3}
\]
contains no more local information than the one-factorisation (1).

## 3. An exact local countermodel to a moment-only bridge

The identities (1)--(3) are consistent.  Take
\[
   V=\mathbb F_{17}\cup\{\infty\}
\]
and label the edges by
\[
   \lambda_{\infty,x}=x,\qquad
   \lambda_{x,y}=\frac{x+y}{2}\quad(x\ne y\in\mathbb F_{17}).
   \tag{4}
\]
At \(\infty\), the incident labels are visibly all of
\(\mathbb F_{17}\).  At a finite vertex \(x\), the edge to infinity
has label \(x\), while
\[
   y\longmapsto\frac{x+y}{2}
\]
maps \(\mathbb F_{17}\setminus\{x\}\) bijectively onto
\(\mathbb F_{17}\setminus\{x\}\).  Hence every row is rainbow and
all the power identities hold.

This local model is not a claim that the colouring extends to all
16-subsets.  Its role is sharper: it proves that no contradiction
using only one 14-link and the universal row power sums can work.

It also displays the missing Pluecker condition concretely.  Order the
four finite vertices \(0<1<2<3\), orient each label by that order, and
use \(2^{-1}=9\) in \(\mathbb F_{17}\).  Then
\[
\begin{array}{c|rrrrrr}
ij&01&02&03&12&13&23\\ \hline
\lambda_{ij}&9&1&10&10&2&11.
\end{array}
\]
The rank-two Pluecker expression is
\[
 \lambda_{01}\lambda_{23}
 -\lambda_{02}\lambda_{13}
 +\lambda_{03}\lambda_{12}
 =9\cdot11-1\cdot2+10\cdot10
 =10\ne0
 \quad\text{in }\mathbb F_{17}.
 \tag{5}
\]
Vertex sign gauges multiply all three terms in (5) by the same
nonzero factor, so they cannot repair this failure.

## 4. Exact obstruction to transferring Theorem 3

For a determinant link, the oriented labels
\[
   p_{ij}=\det(u_i,u_j)
\]
form a skew-symmetric matrix of rank at most two.  Equivalently, they
satisfy every four-index Pluecker relation
\[
   p_{ij}p_{k\ell}-p_{ik}p_{j\ell}
   +p_{i\ell}p_{jk}=0.
   \tag{6}
\]
This extra structure is used twice:

* it factorises the eighth powers into vertex scalars and shifted slope
  powers, producing the degree-eight polynomial in Theorem 3;
* its alternating bilinearity converts the ordered first row sum into
  \(\det(u_i,W-2P_i)\), producing the vector recurrence.

For an arbitrary colouring, (2) supplies scalar edge sums only.
Embedding a colour as its power vector does not attach a vector to each
vertex and does not imply (6).  The explicit one-factorisation (4)
satisfies every universal power identity while (5) violates the first
necessary rank-two relation.

Globally, if \(f(S)=c(S)\) and \(D\) is the down-incidence operator from
16-sets to 15-sets, the same facts can be written
\[
   D(f^m)=0\qquad(1\le m\le15).
   \tag{7}
\]
Those coordinatewise-power kernel equations are valid and potentially
useful, but they do not imply that a restriction of \(f\) to a
14-link is a decomposable alternating two-form.  Compatibility among
different 14-links is precisely the additional global large-set
structure that is absent from the local countermodel.

Therefore a genuine bridge from Theorem 3 to arbitrary colourings needs
a new cross-link theorem forcing either the Pluecker relations, a
rank-two substitute, or another vertex-attached recurrence.  The
universal \(\mathbb F_{17}\) power-vector identities alone cannot supply
that bridge.
