# Radius five forces the minimal trace

This note corrects the scope of
`radius5_large_set_equivalence.md`. The matching condition called the
“minimal-trace ansatz” there is not an extra assumption: every genuine
radius-five extension forces it.

This is a theorem about the complete, unrestricted local ball. It assumes no
cyclic action, golf chart, or finite-field construction. It does not construct
a radius-five ball, still less a global colouring, and it does not solve
Erdős–Rosenfeld Problem #835.

## Theorem

Use the notation of `radius4_reduction.md` and `radius5_reduction.md`, first
at general even \(k\). Thus \(|V|=k\), the colour set is
\(\mathcal C=V\sqcup\{\infty\}\), and \(i\ne j\) are two of the \(k-1\)
fixed-point indices. For a fixed pair \(ij\), put

\[
 D_x=\{uv\in\tbinom V2:N_{uv}(ij)=x\}\qquad(x\in\mathcal C).
\]

If the radius-four colouring extends through radius five, then

\[
\begin{aligned}
D_\infty&\text{ is a perfect matching of }V,\\
D_x&\text{ is a perfect matching of }
V\setminus\{L_i^{-1}(x),L_j^{-1}(x)\}
&& (x\in V).
\end{aligned}
\tag{1}
\]

Consequently, after adjoining the two link points corresponding to \(i,j\),
every fixed-\(ij\) radius-five slice is a prescribed-link
\(LS(2,3,k+3)\). At \(k=16\), every one of the 105 slices is therefore a
prescribed-link \(LS(2,3,19)\). This conclusion is lossless.

## Proof

For a colour \(x\), let \(a_{r,x}(u)\) be \(1\) when the
\(x\)-coloured matching of \(M_r\) covers \(u\), and \(0\) otherwise.
For fixed \(ij,x\), the \(x\)-coloured radius-five triples decompose

\[
G_{ij,x}=K_V-
\bigl(M_i^{-1}(x)\mathbin{\dot\cup}M_j^{-1}(x)
\mathbin{\dot\cup}D_x\bigr)
\]

into triangles. The union is edge-disjoint: the transversal condition makes
\(M_i(uv)\ne M_j(uv)\), and the allowed-colour condition for \(N_{uv}(ij)\)
excludes both values.

Every degree in a triangle-decomposable graph is even. Since \(k\) is even,
\(\deg_{K_V}(u)=k-1\) is odd, and hence

\[
\deg_{D_x}(u)\equiv
1+a_{i,x}(u)+a_{j,x}(u)\pmod2.
\tag{2}
\]

For \(x=\infty\), both \(M_i^{-1}(\infty)\) and
\(M_j^{-1}(\infty)\) are perfect matchings. Thus the right side of (2) is
odd at every one of the \(k\) vertices, so

\[
|D_\infty|\ge k/2.
\tag{3}
\]

For finite \(x\), the \(x\)-matching of \(M_r\) misses exactly
\(\{x,L_r^{-1}(x)\}\). The two preimages
\(L_i^{-1}(x)\) and \(L_j^{-1}(x)\) are distinct: otherwise the values
\(L_i(u)\) and \(L_j(u)\) would repeat in the rainbow column at that \(u\).
Equation (2) is therefore odd at \(x\) and at the \(k-3\) vertices outside
these three exceptional vertices, and even at the two preimages. It is odd
at exactly \(k-2\) vertices, giving

\[
|D_x|\ge (k-2)/2\qquad(x\in V).
\tag{4}
\]

The sets \(D_x\) partition \(E(K_V)\), because \(N_{uv}(ij)\) assigns one
colour to every edge \(uv\). But the lower bounds already sum to the entire
edge set:

\[
\frac{k}{2}
+k\frac{k-2}{2}
=\frac{k(k-1)}2
=|E(K_V)|.
\tag{5}
\]

Equality must therefore hold in every bound. Equality in the handshake
lower bound means that every vertex required odd by (2) has \(D_x\)-degree
exactly \(1\), while every vertex required even has degree \(0\). This is
exactly (1).

The prescribed-link equivalence in
`radius5_large_set_equivalence.md` now applies without an ansatz: (1) supplies
all pair equations involving either link point, while the genuine
radius-five equations supply all moving-pair equations. Each colour class is
an \(STS(k+3)\), and the \(k+1\) classes partition all triples. \(\square\)

## Target counts at \(k=16\)

\[
|D_\infty|=8,\qquad |D_x|=7\ (x\in V),\qquad
8+16\cdot7=120.
\]

Thus the complete radius-five search can be reformulated without loss as a
joint search for 105 prescribed-link \(LS(2,3,19)\) completions with their
shared \(N\)-table compatibility. The existing 105 cyclic slice certificates
show that the slices can be completed separately for the Wallis chart; their
shared trace remains unresolved.

## Lossless necessary-condition searches

The theorem permits two searches that omit the \(58{,}800\) sphere-five
\(P\)-variables while retaining a necessary consequence of every genuine
radius-five extension.

The first is completely unrestricted:

```sh
python3 -B evidence/odd_graph_local_ball/search_local_cover.py \
  --radius 4 --radius5-trace-only \
  --encoding integer --seconds 21600 --workers 8
```

It builds the full generic radius-four ball and adds the 1,680 forced
`AllDifferent(15)` trace stars. A satisfying assignment is only a
radius-four-plus-trace witness; infeasibility would exclude a radius-five
extension and hence exclude \(k=16\).

The second fixes the verified Wallis \(L/M\) chart and searches only its
12,600 shared \(N\)-values:

```sh
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_n_congruence.py \
  --seconds 21600 --workers 8 --seed 835
```

Its lean default uses the original 1,800 radius-four
`AllDifferent(14)` stars and the 1,680 forced trace stars. The older parity
and mod-three reifications are redundant once (1) is imposed and are
available only through `--redundant-congruences`. Infeasibility here would
exclude this one \(L/M\) chart, not arbitrary radius-five balls.

## Reproduce the finite audit

```sh
python3 -B evidence/odd_graph_local_ball/verify_radius5_minimal_trace_forced.py
```

The verifier checks the symbolic edge-count identity for even \(k\), then
instantiates all 105 pairs and all 17 colours in the verified Wallis
\(G(17)\), including the missing-vertex and parity sets. The proof above,
not that one chart, establishes the unrestricted theorem.
