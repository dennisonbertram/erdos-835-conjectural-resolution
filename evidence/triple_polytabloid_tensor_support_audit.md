# Support and parity of the triple-polytabloid tensor

This note makes the tensor in
`top_degree_cross_matching_cubic_audit.md` completely explicit.  The
result sharply reduces its support, but it does **not** produce a
contradiction for the first open parameter \(k=16,p=17\).

Let \(M,N,L\) be oriented perfect matchings of a \(2k\)-set.  Parallel
edges are retained, so their union is a three-edge-coloured cubic
multigraph \(G=M\cup N\cup L\).  As before,

\[
 e_M(S)=\prod_{(u,v)\in M}
 \bigl(\boldsymbol1_{u\in S}-\boldsymbol1_{v\in S}\bigr)
\]

and

\[
 T_{MNL}=\sum_{S\in\binom{[2k]}k}e_M(S)e_N(S)e_L(S).
\tag{1}
\]

## Exact support theorem

For a connected component \(C\) of \(G\), write
\(\lvert C\rvert=2m_C\).  If \(C\) is bipartite, choose either side
\(A_C\) of its bipartition and put

\[
 \sigma_C(A_C)=
 \prod_{\substack{(u,v)\in M\cup N\cup L\\u,v\in C}}
 \bigl(\boldsymbol1_{u\in A_C}-\boldsymbol1_{v\in A_C}\bigr).
\tag{2}
\]

Here the product retains the orientation and colour multiplicity of
every edge.

**Theorem.**  If some component of \(G\) is non-bipartite, or if some
\(m_C\) is odd, then

\[
 T_{MNL}=0.
\tag{3}
\]

Otherwise every component has order divisible by four and

\[
 \boxed{\displaystyle
 T_{MNL}=2^{c(G)}\prod_C\sigma_C(A_C),}
\tag{4}
\]

where \(c(G)\) is the number of connected components.  When \(m_C\) is
even, the sign in (2) is independent of which bipartition side was
chosen.

### Proof

A summand in (1) is nonzero exactly when \(S\) contains one endpoint of
every edge of all three matchings.  On a connected component, these
binary choices propagate along edges.  They are consistent exactly
when the component is bipartite, and then the only two choices are its
two bipartition sides.

Every one of the three perfect matchings restricts to \(m_C\) edges in
a component of order \(2m_C\).  Replacing one bipartition side by the
other reverses all \(3m_C\) oriented edge factors.  The two component
contributions therefore have ratio

\[
 (-1)^{3m_C}=(-1)^{m_C}.
\]

They cancel when \(m_C\) is odd and add to
\(2\sigma_C(A_C)\) when \(m_C\) is even.  Choices on distinct
components are independent, and every global choice has exactly
\(\sum_Cm_C=k\) points.  Multiplying the component sums proves
(3)--(4).  \(\square\)

Reversing one edge orientation in any one of \(M,N,L\) reverses both
sides of (4), as required.

## Consequences for the \(k=16\) cubic equations

Every nonzero tensor entry is even.  More precisely,

\[
 T_{MNL}\equiv
\begin{cases}
2\sigma\pmod4,&G\text{ is connected and satisfies the theorem},\\
0\pmod4,&G\text{ has at least two components or }T_{MNL}=0.
\end{cases}
\tag{5}
\]

There is no corresponding vanishing modulo \(17\): a nonzero entry is
a signed power of two.

These observations look tempting because, when \(k=16\), every signed
colour count

\[
 \Delta_M(a)=\langle \boldsymbol1_{C_a},e_M\rangle
\]

is even.  Thus each individual term
\(\Delta_N(a)\Delta_L(b)T_{MNL}\) is divisible by \(8\).
The full sum has much stronger divisibility, but that strength is an
automatic frame identity rather than an obstruction.

Let \(E\) be the matrix whose rows are the \(e_M\)'s.  The exact frame
identity gives

\[
 E^{\mathsf T}E=p!P_K=p\,k!P_K.
\tag{6}
\]

If \(f_a\) is the indicator of an
\(S(k-1,k,2k)\), then
\(P_Kf_a=f_a-p^{-1}\boldsymbol1\).  Therefore

\[
 E^{\mathsf T}E f_a=k!(pf_a-\boldsymbol1)=k!q_a.
\tag{7}
\]

Contracting the tensor directly now yields

\[
\boxed{\displaystyle
 \sum_{N,L}\Delta_N(a)\Delta_L(b)T_{MNL}
 =k!^2\langle e_M,q_aq_b\rangle.}
\tag{8}
\]

For two disjoint constituents this is exactly

\[
 p\,k!^2
\begin{cases}
(p-2)\Delta_M(a),&a=b,\\
-\Delta_M(a)-\Delta_M(b),&a\ne b.
\end{cases}
\tag{9}
\]

At \(k=16,p=17\), \(v_2(16!)=15\).  Equations (8)--(9), together
with the evenness of every \(\Delta\), force divisibility by
\(2^{31}\).  The theorem supplies only the termwise factor \(2^3\);
the remaining cancellation is already enforced by (6)--(7).
Consequently reduction modulo \(2\) or \(4\) cannot contradict (9).

Modulo \(17\), Wilson's theorem gives \(16!\equiv-1\).  Equation (7)
also gives

\[
 E^{\mathsf T}E f_a\equiv\boldsymbol1\pmod {17}.
\]

Hence the left side of (8) is congruent to
\(\langle e_M,\boldsymbol1\rangle=0\pmod {17}\), exactly as required
by the factor \(p\) on the right of (9).  This congruence is automatic
even before using disjointness.

Thus the obvious reductions modulo \(2,4,\) and \(17\) all close
without residue.  Any contradiction from the tensor support must use
finer simultaneous information about which bipartite
four-divisible union graphs carry the nonzero derivatives, not merely
the value set \(0,\pm2^c\).

### The first support-sensitive parity relation

Dividing (8) by \(8\) and reducing modulo two exposes more than the
aggregate divisibility statement.  Put

\[
 \delta_M(a)=\frac{\Delta_M(a)}2\pmod2.
\]

For each fixed \(M\), define a symmetric binary matrix

\[
 (K_M)_{N,L}=1
 \quad\Longleftrightarrow\quad
 M\cup N\cup L\text{ is connected and bipartite}.
\tag{10}
\]

At \(k=16\), connectedness makes the unique component have order
\(32\), so the divisibility-by-four condition in the support theorem
is automatic.  The reduced cubic equation is

\[
\boxed{\displaystyle
 \delta(a)^{\mathsf T}K_M\delta(b)=0
 \quad\text{over }\mathbb F_2}
\tag{11}
\]

for every \(M\) and every pair of colours.

In the self-colour case \(a=b\), the off-diagonal terms cancel in
symmetric pairs.  The diagonal entry \((K_M)_{N,N}\) is one exactly
when \(M\cup N\) is one alternating Hamilton cycle.  If \(H\) is the
binary adjacency matrix on perfect matchings defined by

\[
 H_{MN}=1
 \quad\Longleftrightarrow\quad
 M\cup N\text{ is a single }2k\text{-cycle},
\tag{12}
\]

then the self-colour part of (11) is

\[
\boxed{\displaystyle
 H\delta(a)=0.}
\tag{13}
\]

Equation (13) is automatic for a much more elementary reason.  Let
\(\overline X\) be the set of complementary pairs of \(k\)-subsets,
and let \(A\) be the binary matrix

\[
 A_{M,\{S,S^c\}}=1
 \quad\Longleftrightarrow\quad
 S\text{ is a transversal of }M.
\tag{14}
\]

For every complement-invariant indicator \(f_a\),

\[
 \delta(a)=A\overline f_a.
\tag{15}
\]

Two matchings whose union has \(c\) alternating components have
\(2^{c-1}\) common transversal pairs.  Therefore

\[
 AA^{\mathsf T}=H\pmod2.
\tag{16}
\]

For two half-sets with intersection size \(j\), the number of
matchings transverse to both is

\[
 j!(k-j)!.
\tag{17}
\]

When \(k\ge3\), this is always even, so

\[
 A^{\mathsf T}A=0,\qquad HA=A(A^{\mathsf T}A)=0.
\tag{18}
\]

Equations (15) and (18) prove (13) without using proper cube
colouring at all.

The mixed bilinear relation (11) is the first parity condition not
erased by the elementary factorisation (16)--(18).  It is nevertheless
automatic for any pair of exact-design indicators: equation (8)
already contributes the factor \(k!^2\), independently of whether the
two designs are disjoint.  The complete \(k=4\) false control makes
this limitation concrete.  All thirty labelled \(S(3,4,8)\)'s give
derivative parity vectors in \(\operatorname{im}H\), and all
\(105\cdot30^2=94\,500\) equations

\[
 \delta(a)^{\mathsf T}K_M\delta(b)=0
\tag{19}
\]

hold, including for overlapping pairs of systems.  Thus (11) does not
detect disjointness at \(k=4\), and at \(k=16\) it is a sharply reduced
identity for individual exact designs rather than a large-set
obstruction.  A continuation would need information beyond this first
binary support layer--for example a higher \(2\)-adic lift that
interacts with disjointness rather than only with the exact-design
frame.

## The first Hilbert--Schmidt SOS test is also compatible

There is a natural quadratic positivity test on the multiplication
operators.  On \(K\), write

\[
 L_x=P_K\operatorname{diag}(x)P_K\bigm|_K.
\]

The top Johnson projector has entries

\[
 (P_K)_{S,T}
 =\frac{(-1)^{k-\lvert S\cap T\rvert}}
 {p\binom{k}{\lvert S\cap T\rvert}}.
\tag{20}
\]

For even \(k\), Schur invariance and a calculation on one matching
polytabloid give

\[
\boxed{\displaystyle
 \operatorname{tr}(L_xL_y)
 =\frac{2}{p(p+1)}\langle x,y\rangle
 \qquad(x,y\in K).}
 \tag{21}
\]

Indeed, \(P_K\circ P_K\) is scalar on the irreducible top constituent.
On a matching transversal, grouping the other transversals by the
number \(r\) of flipped pairs gives the scalar

\[
 \frac1{p^2}\sum_{r=0}^k\frac{(-1)^r}{\binom kr}
 =\frac2{p(p+1)}.
\]

The last equality follows, for example, by integrating the finite
geometric sum after writing
\(\binom kr^{-1}=(k+1)\int_0^1t^r(1-t)^{k-r}\,dt\).

Let \(U=\langle q_0,\ldots,q_{p-1}\rangle\).  The cubic
projected-idempotence equations make \(U\) invariant under every
\(L_{q_a}\).  The Frobenius identity

\[
 \langle L_xy,z\rangle=\sum_Sx(S)y(S)z(S)
\]

then makes \(U^\perp\) invariant as well.  On \(U\),
\(L_{q_a}\) has eigenvalue \(p-2\) on \(q_a\) and eigenvalue \(-1\)
with multiplicity \(p-2\).  Consequently

\[
 \operatorname{tr}_U(L_{q_a}^2)=(p-1)(p-2),
\qquad
 \operatorname{tr}_U(L_{q_a}L_{q_b})=-(p-2)
\quad(a\ne b).
\tag{22}
\]

Put \(B_a=L_{q_a}|_{U^\perp}\).  Since
\(\langle q_a,q_a\rangle=N(p-1)\) and
\(\langle q_a,q_b\rangle=-N\), equations (21)--(22) force the
Hilbert--Schmidt Gram matrix

\[
 \operatorname{tr}(B_aB_b)=
\begin{cases}
R,&a=b,\\
-R/(p-1),&a\ne b,
\end{cases}
\quad
R=(p-1)\left(\frac{2N}{p(p+1)}-(p-2)\right).
\tag{23}
\]

This is a regular-simplex Gram matrix whenever \(R\ge0\).  At the true
\(k=2\) control, \(R=0\).  At the false \(k=4\) control,
\(R=20/3>0\).  At the target,

\[
 N=\binom{32}{16}=601\,080\,390,
\qquad R=62\,857\,840>0.
\tag{24}
\]

Thus the most immediate sum-of-squares test--subtract the forced
simplex action from the total Hilbert--Schmidt norm--is strictly
compatible at \(p=17\).  This does not construct the unknown
multiplication operators; it rules out only a negative-residual-norm
contradiction.

## Verification

Run

```bash
python3 -B evidence/verify_triple_polytabloid_tensor_support.py
```

The verifier:

* exhausts every ordered triple of perfect matchings for
  \(k=1,2,3,4\);
* computes (1) independently with signed-support bitsets and compares
  it with (3)--(4);
* checks orientation reversal;
* enumerates all thirty labelled \(S(3,4,8)\)'s, selects a disjoint
  pair, and verifies every contraction in (8)--(9);
* verifies \(AA^{\mathsf T}=H\), \(A^{\mathsf T}A=0\), and all
  \(94\,500\) mixed relations (19) in the complete \(k=4\) control;
* checks the target \(2\)-adic and \(17\)-adic arithmetic and the exact
  Hilbert--Schmidt residual (23)--(24).

This is a structural lemma for the cubic system, not a solution of
Erdős--Rosenfeld Problem #835.
