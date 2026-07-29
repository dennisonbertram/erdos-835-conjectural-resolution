# Exact radius-4 reduction for \(O_{16}\)

Let \(A,B\) be disjoint sets with \(|A|=15\), \(|B|=16\), and take
\(A\) as the root of \(O_{16}=KG(31,15)\).  Write \(V\) for a
16-element set of finite colours and put
\[
\mathcal C=V\sqcup\{\infty\}.
\]
After relabelling colours, the root has colour \(\infty\) and its
neighbour \(B\setminus\{u\}\) has colour \(u\), for \(u\in V\).

The next three spheres have canonical coordinates:
\[
\begin{array}{ccl}
C_{u,i}&=&(A\setminus\{i\})\cup\{u\},\\
D_{i,\{u,v\}}&=&(B\setminus\{u,v\})\cup\{i\},\\
E_{\{i,j\},\{u,v\}}&=&
 (A\setminus\{i,j\})\cup\{u,v\}.
\end{array}
\]
Here \(i,j\in A\), \(u,v\in V\), and the displayed pairs are unordered.
Thus the sphere sizes through radius 4 are
\[
1,\quad16,\quad240,\quad1800,\quad12600.
\]

Define their colours by
\[
\operatorname{col}(C_{u,i})=L_i(u),\qquad
\operatorname{col}(D_{i,\{u,v\}})=M_i(uv),\qquad
\operatorname{col}(E_{\{i,j\},\{u,v\}})=N_{uv}(ij).
\]

## Proposition

A colouring of the radius-4 ball is locally bijective at every centre
through radius 3 if and only if \(L,M,N\) have the following properties.

1. For every \(u\in V\),
   \[
   \{L_i(u):i\in A\}=V\setminus\{u\}.
   \]
2. For every \(i\in A\), \(L_i\) is a derangement permutation of \(V\),
   and \(M_i\) is an edge-colouring of \(K_V\) such that the colours on
   the fifteen edges incident with \(u\) are
   \[
   \mathcal C\setminus\{u,L_i(u)\}.
   \]
3. For every edge \(uv\) of \(K_V\),
   \[
   \{M_i(uv):i\in A\}=\mathcal C\setminus\{u,v\}.
   \]
4. For every fixed \(uv\), \(N_{uv}\) is an edge-colouring of \(K_A\)
   such that the fourteen colours incident with \(i\) are
   \[
   \mathcal C\setminus
   \{M_i(uv),L_i(u),L_i(v)\}.
   \]

### Proof

The closed neighbourhood of \(B\setminus\{u\}\) consists of the root,
that vertex, and \(C_{u,i}\) over all \(i\).  Local bijectivity is
therefore exactly condition 1.

The closed neighbourhood of \(C_{u,i}\) consists of itself, its
distance-one parent, and \(D_{i,\{u,v\}}\) over the fifteen \(v\ne u\).
This gives the incidence-colour requirement in condition 2.

It also forces each \(L_i\) to be a permutation.  Fix \(i\) and a finite
colour \(x\), and let \(d_x=|\{u:L_i(u)=x\}|\).  In the matching formed
by the \(x\)-coloured edges of \(M_i\), precisely \(1+d_x\) vertices
miss colour \(x\): vertex \(x\), and the \(d_x\) preimages of \(x\).
This number must be even, so every \(d_x\) is odd.  Since
\(\sum_xd_x=16\), every \(d_x=1\).  Condition 1 already says
\(L_i(u)\ne u\).  The \(\infty\)-coloured edges of \(M_i\) form a
perfect matching.

The closed neighbourhood of \(D_{i,\{u,v\}}\) contains that vertex,
the two vertices \(C_{u,i},C_{v,i}\), and
\(E_{\{i,j\},\{u,v\}}\) over the fourteen \(j\ne i\).  This is exactly
condition 4.

It remains to derive condition 3, which is forced by parity.  Fix
\(uv\), and let
\[
m_x=|\{i:M_i(uv)=x\}|.
\]
For the \(x\)-coloured matching in \(N_{uv}\), the number of vertices
of \(K_A\) missing \(x\) must have the same parity as 15 and is
therefore odd.  Across \(i\), the values \(L_i(u)\) comprise
\(V\setminus\{u\}\), and the values \(L_i(v)\) comprise
\(V\setminus\{v\}\).  Also \(M_i(uv)\) is distinct from
\(u,v,L_i(u),L_i(v)\).  Hence the missing count is
\[
\begin{cases}
m_\infty,&x=\infty,\\
1,&x=u\text{ or }x=v,\\
2+m_x,&x\in V\setminus\{u,v\}.
\end{cases}
\]
Thus \(m_x\) is positive and odd for every
\(x\in\mathcal C\setminus\{u,v\}\).  Those fifteen multiplicities sum
to 15, so all of them equal one.  This proves condition 3.

Conversely, the four displayed colour-set conditions directly verify
the closed neighbourhoods in spheres 0 through 3. \(\square\)

## One-factorization interpretation

For each \(i\), conditions 1 and 2 extend canonically to a
one-factorization of \(K_{18}\).  Add vertices \(\alpha,\beta\) and
colour
\[
\alpha\beta\mapsto\infty,\qquad
\alpha u\mapsto u,\qquad
\beta u\mapsto L_i(u),\qquad
uv\mapsto M_i(uv).
\]
Every vertex sees every colour exactly once, so every colour class is
a one-factor.  Condition 3 is an additional transversal condition
across the fifteen normalized one-factorizations.  It should not be
replaced by the weaker assertion that a projective plane of order 16
exists.

Likewise, parity is only a necessary condition for each \(N_{uv}\).
The actual list edge-colouring in condition 4 must still be constructed
or proved impossible.
