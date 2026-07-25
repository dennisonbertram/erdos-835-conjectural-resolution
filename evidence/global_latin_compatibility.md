# Global Latin compatibility and the golf-design boundary

This note isolates the exact Latin-square transition forced by a
\((k+1)\)-colouring
\[
 c:\binom{X}{k}\longrightarrow {\cal C},\qquad |X|=2k,\quad
 |{\cal C}|=k+1,
\]
which is rainbow on every lower \((k-1)\)-star and every upper
\((k+1)\)-clique.  It gives two definite conclusions.

1. The transition already rules out \(k=4\), locally.
2. At \(k=16\), not only the transition but the whole first global
   compatibility layer is feasible.  That layer is the classical
   golf design of order \(17\), and an explicit cyclic witness is
   verified below.  The witness can also be extended through the
   complete radius-four Odd-graph ball.

Thus a parity or topology argument which only sees one middle-layer
star, or only one adjacent pair of local Latin squares, cannot settle
the first open case.

## 1. The exact adjacent transition

For a \(k\)-set \(K\), put \(s=c(K)\) and define
\[
 L_K(x,y)=c(K-\{x\}+\{y\}),
 \qquad x\in K,\quad y\in X\setminus K.
 \tag{1}
\]
Every row is the lower star through \(K-\{x\}\), with the colour
\(s\) deleted.  Every column is the upper clique on \(K\cup\{y\}\),
again with \(s\) deleted.  Consequently \(L_K\) is a Latin square of
order \(k\), with symbol set \({\cal C}\setminus\{s\}\).

Let
\[
 K'=K-\{a\}+\{b\},\qquad d=c(K')=L_K(a,b).
\]
The row set of \(L_{K'}\) is
\((K-\{a\})\cup\{b\}\), its column set is
\((X\setminus(K\cup\{b\}))\cup\{a\}\), and its symbols are
\({\cal C}\setminus\{d\}\).  Direct substitution in (1) gives
\[
\begin{aligned}
 L_{K'}(b,a)&=s,\\
 L_{K'}(b,y)&=L_K(a,y) &&(y\notin K,\ y\ne b),\\
 L_{K'}(x,a)&=L_K(x,b) &&(x\in K,\ x\ne a),\\
 L_{K'}(x,y)&\ne L_K(x,y)
   &&(x\ne a,\ y\ne b).
\end{aligned}
\tag{2}
\]
The last inequality holds because the two \(k\)-sets represented by
the two cells differ by the single exchange \(a\leftrightarrow b\).
Equation (2), rather than a scalar sign, is the full adjacent
transition law.

After permuting rows, columns, and the common symbols, a transition
pair can be normalized as follows.  The first square has symbols
\(\{1,\ldots,k\}\), the second has symbols
\(\{0,2,\ldots,k\}\), their upper and left borders agree except for
\(1\leftrightarrow0\) at the corner, and their
\((k-1)\)-by-\((k-1)\) interiors disagree cellwise.

For \(k=2\), the unique normalized pair is
\[
\begin{pmatrix}1&2\\2&1\end{pmatrix},
\qquad
\begin{pmatrix}0&2\\2&0\end{pmatrix}.
\tag{3}
\]
For \(k=4\), there is no normalized pair.  There are only four
reduced Latin squares on either symbol set.  Comparing the sixteen
pairs gives the following matrix of numbers of equal interior cells:
\[
\begin{pmatrix}
6&4&4&4\\
4&6&2&2\\
4&2&6&2\\
4&2&2&6
\end{pmatrix}.
\tag{4}
\]
Every entry is positive, contradicting the final line of (2).
`global_latin_audit.py` generates the reduced squares rather than
assuming their classification, and reproduces (3) and (4).

## 2. A whole star is exactly a golf design

Fix a \((k-1)\)-set \(T\), put \(Y=X\setminus T\), and use the
rainbow star to identify points of \(Y\) with colours:
\[
 \lambda_T(x)=c(T\cup\{x\}),\qquad \lambda_T:Y\longrightarrow{\cal C}.
\]
For every \(t\in T\), define a square on \(Y\) by
\[
\begin{aligned}
 S_t(x,x)&=x,\\
 S_t(x,y)&=\lambda_T^{-1}
 \bigl(c(T-\{t\}+\{x,y\})\bigr)\qquad(x\ne y).
\end{aligned}
\tag{5}
\]

**Star-to-golf theorem.**  The \(k-1\) squares
\((S_t)_{t\in T}\) are symmetric idempotent Latin squares of order
\(k+1\), and for all \(x\ne y\),
\[
 \{S_t(x,y):t\in T\}=Y\setminus\{x,y\}.
 \tag{6}
\]

**Proof.**  Symmetry and idempotence are immediate.  Fix \(t,x\).
As \(y\) runs over \(Y\setminus\{x\}\), the sets
\(T-\{t\}+\{x,y\}\) are the members other than \(T\cup\{x\}\) of
the lower star based at \(T-\{t\}+\{x\}\).  Their colours are exactly
the colours other than \(\lambda_T(x)\), so the \(x\)-row of \(S_t\)
is a permutation of \(Y\).  Finally, for fixed \(x,y\), changing
\(t\) gives \(k-1\) mutually adjacent \(k\)-sets.  Their colours
avoid the two colours of \(T\cup\{x\}\) and \(T\cup\{y\}\), and hence
are exactly the remaining \(k-1\) colours.  This is (6). \(\square\)

A family in (6) is called a **golf design** \(G(k+1)\), or a large
set of symmetric idempotent Latin squares.  Conversely, a golf
design reconstructs all the colours in (5), and therefore gives a
coherent family of all \(k+1\) local Latin squares \(L_{T\cup\{x\}}\)
around the star.  This converse also checks every adjacent transition
in (2), simultaneously.

The existence spectrum of golf designs is known:
\[
 \boxed{G(v)\text{ exists exactly when }v\ge3\text{ is odd and }v\ne5.}
\tag{7}
\]
This is recorded, with the original references, in Chang's spectrum
theorem and in the modern SAT literature on golf designs.  In
particular:

- \(G(3)\) gives the existing \(k=2\) colouring locally;
- the failure of \(G(5)\) gives the local \(k=4\) obstruction above;
- \(G(17)\) exists, so the entire one-star layer at \(k=16\) is
  feasible.

This identification also corrects a possible misreading of the
radius-four reduction: the fifteen symmetric idempotent Latin
squares themselves are not an open search problem at order \(17\).
The subsequent coupled \(N\)- and triangle-decomposition layers are
where new compatibility begins.

## 3. An explicit cyclic \(G(17)\)

Here is a compact exact witness.  Arithmetic is modulo \(17\).  The
columns below are indexed by the fifteen squares \(2,3,\ldots,16\);
the eight displayed rows give \(a_1,\ldots,a_8\).
\[
\begin{array}{c|rrrrrrrrrrrrrrr}
 &2&3&4&5&6&7&8&9&10&11&12&13&14&15&16\\ \hline
a_1&2&3&4&5&6&7&8&9&10&11&12&13&14&15&16\\
a_2&5&1&7&8&9&16&14&4&13&15&10&6&11&3&12\\
a_3&9&10&12&2&15&13&16&14&4&7&5&8&1&11&6\\
a_4&14&12&2&13&3&8&9&16&7&5&1&15&6&10&11\\
a_5&16&11&13&15&1&3&6&10&2&14&4&7&8&12&9\\
a_6&13&15&16&1&14&11&4&7&12&8&9&3&10&5&2\\
a_7&15&4&1&14&11&2&10&3&5&6&13&16&12&9&8\\
a_8&12&13&14&11&10&9&2&6&16&3&15&1&7&4&5
\end{array}
\tag{8}
\]
For each column, set \(a_0=0\) and extend by
\[
 a_{17-j}=a_j-j\pmod {17}\qquad(1\le j\le8).
\tag{9}
\]
The corresponding square is
\[
 S(x,y)=a_{x-y}+y\pmod {17}.
\tag{10}
\]
The verifier checks directly that:

1. every row \(a_0,\ldots,a_{16}\) is a permutation;
2. all fifteen \(S\)'s are symmetric, idempotent, and Latin;
3. every off-diagonal cell contains exactly
   \(\mathbb Z_{17}\setminus\{x,y\}\) across the fifteen squares;
4. the seventeen induced order-\(16\) local squares are Latin and
   satisfy every transition in (2).

The construction is the circulant golf array displayed by Wallis;
the verifier makes the witness independent of typography or OCR.

## 4. The next layer is still feasible: an exact radius-four ball

Take \(\infty=16\), \(V=\{0,\ldots,15\}\), and index the fifteen
squares in (8) by \(i\).  Put
\[
 L_i(u)=S_i(u,\infty),\qquad M_i(uv)=S_i(u,v).
\tag{11}
\]
The golf identities give conditions 1--3 of
`odd_graph_local_ball/radius4_reduction.md` exactly.

For each of the \(120\) edges \(uv\) of \(K_{16}\), the remaining
condition asks for an edge-colouring \(N_{uv}\) of \(K_{15}\) such
that the colours incident with \(i\) are
\[
 {\cal C}\setminus
 \{M_i(uv),L_i(u),L_i(v)\}.
\tag{12}
\]
The 120 problems are independent.  The script
`global_latin_radius4_certificate.py` solves each exact finite model
and then checks (11)--(12) without trusting the solver constraints.
With OR-Tools 9.15.6755 and one deterministic worker, all 120
instances return `OPTIMAL` in about 22 seconds and the concatenated
12,600 colour values have SHA-256
```
f03067f8614037a067820970da11ca73cba16e6a62cab334c11a70a44e399cba
```

Therefore the actual \(14{,}657\)-vertex radius-four ball in
\(O_{16}\) has a colouring locally bijective at every centre through
radius three.  This is a genuine positive certificate, not a
relaxation.  It does not assert an extension through radius five.
A bounded joint search imposing the known mod-two and mod-three
radius-five conditions remained `UNKNOWN`, which is not evidence
either for or against radius-five feasibility.

## 5. Parity and topology: the precise boundary

When \(k\) is even, complement closure gives
\[
 L_{K^c}=L_K^{\mathsf T}.
\tag{13}
\]
For the usual Latin sign
\(\epsilon(L)=\prod\operatorname{sgn}(\text{rows})
\prod\operatorname{sgn}(\text{columns})\), equation (13) implies
\[
 \prod_{K\in\binom Xk}\epsilon(L_K)=1.
\tag{14}
\]
This is a tautological square over complementary pairs, not an
obstruction.  The explicit \(G(17)\) has
\(\epsilon(L_{T\cup\{x\}})=+1\) for all seventeen \(x\), so it also
passes the strongest scalar test on one complete star.

Topologically, a colouring of the Odd graph is a graph covering
\(O_{16}\to K_{17}\).  Ordinary obstruction theory for maps of graphs
has no two-dimensional obstruction class: graphs are one-dimensional
and their fundamental groups are free.  This does **not** say that the
fixed graph \(O_{16}\) automatically covers \(K_{17}\); its spectrum,
girth, and labelled closed walks remain genuine restrictions.  It says
that a proposed higher cohomological obstruction must use those
specific global walks or the subset geometry, rather than only the
abstract local covering chart.  The extra subset labels create the golf
and \(N\) compatibility above, but both survive through radius four.  A
successful global argument must therefore use at least the radius-five
coupled triangle decompositions, or a genuinely global relation not
determined by a single star, an adjacent transition, or scalar
orientation signs.

## References

- Y. Chang, *The existence spectrum of golf designs*, Journal of
  Combinatorial Designs **15** (2007), 84--89.
- P. Huang, F. Ma, C. Ge, J. Zhang, and H. Zhang,
  [*Investigating the Existence of Orthogonal Golf Designs via
  Satisfiability Testing*](https://fmv.jku.at/papers/HuangLGMZ_ISSAC19.pdf),
  ISSAC 2019, 203--210.
- X. Li, Y. Chang, and J. Zhou,
  [*The existence of r-golf designs*](https://doi.org/10.1002/jcd.21766),
  Journal of Combinatorial Designs **29** (2021), 243--266.
- W. D. Wallis, *Introduction to Combinatorial Designs*, 2nd ed.,
  Chapman & Hall/CRC, 2007, Section 16.3.
