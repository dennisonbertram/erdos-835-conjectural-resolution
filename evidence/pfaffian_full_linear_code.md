# Linear-code / determinant formulation

Let \(q\) be odd, \(k=q-1\), \(n=2k\), and let \(G\) be a full-rank
\(k\times n\) matrix over \(\mathbb F_q\). Define

\[
c(S)=\det G[S], \qquad |S|=k.
\]

For a \((k-1)\)-set \(T\), choose an ordering of \(T\) and set
\(\ell_T(x)=\det(G[T],x)\). The \(q=n-(k-1)\) desired star colours are
exactly

\[
\{\ell_T(g_u):u\notin T\}=\mathbb F_q. \tag{1}
\]

This is the full determinant-value requirement. In particular every
\((k-1)\)-subset is independent, and exactly one of its \(q\) extensions
has determinant zero. Consequently its zero extensions form an
\(S(k-1,k,2k)\), and \(G\) generates an NMDS \([2k,k,k]_q\) code: every
hyperplane contains at most \(k\) columns, while some contain exactly \(k\).

The converse is false in general: NMDS only controls the maximum
hyperplane intersection. It does not force every \((k-1)\)-set to acquire
exactly one zero extension, much less the all-field-value condition (1).

## Allowed transformations

For \(L\in GL_k(q)\), left multiplication sends all colours to
\(\det(L)c(S)\), which preserves (1). Column scalings
\(G\mapsto G\operatorname{diag}(s_1,\ldots,s_n)\) preserve the zero
support but change the star values by

\[
\det(G[T\cup\{u\}])\longmapsto
\Bigl(\prod_{t\in T}s_t\Bigr)s_u\det(G[T\cup\{u\}]).
\]

Thus the scaling problem is the simultaneous exact system
\[
\{s_u\det(G[T\cup\{u\}]):u\notin T\}=\mathbb F_q
\quad\text{for every }T, \tag{2}
\]
since the first factor is a star-wide nonzero scalar. A support design
alone cannot decide (2).

The companion script tests the full condition for named
\([I\mid A]\) Fourier and quadratic-residue candidates at \(q=5,7,11\),
and uses exact random counterstars at \(q=17,19\). At \(q=5 it also
exhausts all projective column scalings whenever the displayed unscaled
counterstar leaves scaling logically possible.

    python3 evidence/search_pfaffian_full_linear_code.py --large-trials 20

No candidate is reported as a witness unless all stars are checked.
