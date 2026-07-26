# Infinity-layer sign theorem

This note concerns only the two-sided infinity layer.  It is conditional on
the following finite combinatorial data:

* \(k\) is even, \(V\) has \(k\) elements, and \(A\) has \(k-1\) elements;
* \(\Psi:E(K_V)\to A\) is a one-factorization;
* for every \(ij\in E(K_A)\), \(D^{ij}\) is a perfect matching of \(V\);
* for every \(uv\in E(K_V)\), the set
  \({ij:uv\in D^{ij}\}) is a perfect matching of
  \(A\setminus\{\Psi(uv)\}\).

It neither constructs a radius-five ball nor proves an obstruction for
Erdős--Rosenfeld Problem #835.

The independent no-hole/Pfaffian proof in
[`../global_h_parity/README.md`](../global_h_parity/README.md) also identifies
the invariant below as the one-factorization row-sign product
\(\rho(\Psi)=P(\Psi)\).

## The invariant determined by the one-factorization

For \(i\in A\), let \(p_i\) be the mate involution of the matching
\(\Psi^{-1}(i)\).  Give all finite sets their fixed reference orders and
form the two ordered sets

\[
\begin{aligned}
 X_i&=\bigl((u,v):u\in V,\ v\notin\{u,p_i(u)\}\bigr),
       &&\text{ordered vertex-major in }(u,v),\\
 Y_i&=\bigl((f,u):f\in A\setminus\{i\},\ u\in V\bigr),
       &&\text{ordered factor-major in }(f,u).
\end{aligned}
\]

Both have \(k(k-2)\) elements.  The map

\[
 r_i:X_i\longrightarrow Y_i,
 \qquad r_i(u,v)=(\Psi(uv),u)
\tag{1}
\]

is a bijection.  Define

\[
 \rho(\Psi)=\prod_{i\in A}\operatorname{sgn}(r_i).
\tag{2}
\]

This is reference-order independent: changing an order of \(V\) or \(A\)
changes each relevant cofactor an even number of times in the product.

## Theorem

For the partial permutations

\[
 \Phi_{i,u,\infty}:A\setminus\{i\}
 \longrightarrow V\setminus\{u,p_i(u)\},
 \qquad
 \Phi_{i,u,\infty}(j)=D^{ij}(u),
\tag{3}
\]

one has

\[
 \boxed{
 H_\infty:=\prod_{i\in A,\ u\in V}
       \operatorname{sgn}\Phi_{i,u,\infty}=\rho(\Psi).}
\tag{4}
\]

Consequently the sign is independent of the choice of compatible
two-sided matchings \(D^{ij}\), but it can depend on the one-factorization
\(\Psi\).  It is therefore not a function of \(k\) alone.

### Corner-cell proof

Use the oriented cells

\[
 (i,j;u,v)\quad(i\ne j,\ \{u,v\}\in D^{ij}),
\tag{5}
\]

where both orientations \(u\to v\) and \(v\to u\) are retained.  Order
the cells first by the corner \((i,u)\), then by \(j\); changing to the
\((i,u)\), then \(v\), order has sign exactly the left side of (4).

Now rotate the cell description through its opposite corner.  The two
interior changes of order are:

1. on every \(ij\)-face, \(u\mapsto v\) is the involution of the
   matching \(D^{ij}\);
2. on every \(uv\)-face, \(i\mapsto j\) is the involution of the
   matching on \(A\setminus\{\Psi(uv)\}\).

Each face occurs in both orientations.  Thus its permutation sign occurs
twice, hence contributes \(+1\).  The coordinate swaps also occur in
opposite pairs; their inversion count is
\(k(k-1)(k-2)\), which is even.  After those cancellations, the only
unpaired boundary reordering at the \(i\)-faces is

\[
 (u,v)\longmapsto(\Psi(uv),u),
 \qquad v\ne u,p_i(u),
\]

which is precisely \(r_i\).  Multiplying the remaining \(i\)-face signs
proves (4).

This is a sign calculation on the fully specified cell incidence set; it
uses no other colour layer.  In particular, a proof that the sign were
always \(+1\), or depended only on \(k\), would be false.

## Two \(k=16\) witnesses

The verifier constructs two complete two-sided infinity-layer tensors.

1. **Binary model:** \(V=\mathbb F_2^4\), \(A=V\setminus\{0\}\),
   \(\Psi(uv)=u+v\), and
   \(D^{ij}=\{\{u,u+i+j\}:u\in V\}\).  It has \(H_\infty=+1\).
2. **Round-robin model:** use the standard cyclic one-factorization of
   \(K_{16}\), and let a Bose \(STS(15)\) choose a colour \(f(i,j)\) for
   each \(ij\); put \(D^{ij}=\Psi^{-1}(f(i,j))\).  It has
   \(H_\infty=-1\).

Both meet every condition above.  Thus (4) gives a genuine finite
counterexample to a \(k\)-only formula at the same parameter \(k=16\).

The standard round-robin factorization has

\[
 \rho(\Psi)=(-1)^{\binom{k/2-1}{2}}
\]

for the tested values \(4\le k\le30\); this is a property of that
specific one-factorization, not a universal law.

Run the independent finite checks:

```bash
python3 -B collaboration/infinity_layer_theorem/verify_infinity_layer_theorem.py
```
