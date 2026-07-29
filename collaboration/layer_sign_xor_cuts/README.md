# Individual layer signs as explicit XOR constraints

## Result

For the reduced radius-five shared-\(N\) model, every individual layer-sign
equation has an explicit quadratic XOR form.  For the fixed Wallis \(k=16\)
chart, however, **all seventeen equations are already logical consequences
of the existing domain and exact-one/`AllDifferent` constraints**.  Their
incremental rank is therefore zero.  Adding them to a live solver cannot
remove a feasible reduced-\(N\) assignment and cannot strengthen the model
logically.

This is a redundancy theorem, not a solver observation.  No `UNKNOWN` result
is used.  It neither constructs nor excludes a shared \(N\)-table, and it
does not resolve Erdős--Rosenfeld problem 835.

The accompanying checker leaves every live solver untouched.  If a Wallis
\(N\)-certificate is eventually produced, it can independently verify all
seventeen equations.

## 1. The explicit quadratic XOR

Use the orders

\[
 V=\{0,\ldots ,k-1\},\qquad A=\{0,\ldots ,k-2\},\qquad
 C=V\cup\{\infty\}.
\]

For \(uv\in\binom V2\), \(ij\in\binom A2\), and \(x\in C\), introduce the
one-hot indicator

\[
 b^x_{uv,ij}=[N_{uv}(ij)=x]\in\{0,1\}.
\tag{1}
\]

Write \(b^x_{u v,i j}\) with both unordered pairs silently sorted.  At the
flag \((i,u)\), the \(x\)-fibre is the partial permutation

\[
 \Phi_{i,u,x}:j\longmapsto v
 \quad\Longleftrightarrow\quad b^x_{uv,ij}=1.
\tag{2}
\]

The forced-trace stars make (2) injective in \(v\), and the condition-4 stars
make it injective in \(j\).  Both its source and target carry their induced
orders.  Hence its sign is \((-1)\) to the number of inversions.  If
\(\tau_x\in\mathbf F_2\) is zero for a target sign \(+1\) and one for a
target sign \(-1\), the complete \(x\)-layer equation is exactly

\[
\boxed{
 \bigoplus_{\substack{i\in A,\ u\in V\\
                       j<j',\ j,j'\ne i\\
                       v>v',\ v,v'\ne u}}
 \left(b^x_{uv,ij}\wedge b^x_{uv',ij'}\right)
 =\tau_x.}
\tag{3}
\]

Impossible literals can simply be deleted using the fixed \(L/M\) domains.
The common endpoints \(i,u\) are uniquely recoverable from the two variables
in a monomial, so (3) contains no accidental duplicate monomials.

Equation (3) is a quadratic algebraic-normal-form XOR, not a linear XOR of
the original integer variables.  A SAT/CP-SAT encoding would require an
auxiliary Boolean for every displayed conjunction (or a parity circuit with
equivalent definitions).  The verifier reports the exact raw term counts
for Wallis: the 143,640 allowed colour indicators generate 18,489,826
nonzero inversion conjunctions before exploiting the constraints which make
the equations redundant.

### Optional \(P\)-only form

In a complete radius-five model put

\[
 p^x_{ij,uvw}=[P_{ij}(uvw)=x].
\]

Whenever \(x\) is in the domain of \(N_{uv}(ij)\), condition 1 for the
\(P\)-star says exactly one of the omitted \(N\)-value and the fourteen
\(P\)-values has colour \(x\).  Therefore

\[
 b^x_{uv,ij}
 =1\oplus\bigoplus_{w\notin\{u,v\}}p^x_{ij,uvw}.
\tag{4}
\]

Substitution of (4) into every factor of (3) is the explicit \(P\)-only
quadratic XOR.  This substitution does not alter the redundancy result
below.

## 2. Exact Wallis targets

Let

\[
 a_i(x)=L_i^{-1}(x),\qquad
 \Psi_i^x=M_i^{-1}(x)\cup\{\{x,a_i(x)\}\}
\]

for finite \(x\), and let
\(\Psi_i^\infty=M_i^{-1}(\infty)\).  Put

\[
 \lambda_x(i)=a_i(x),\qquad\lambda_x(*)=x.
\]

The proved layer formulas in
[`../global_h_parity/README.md`](../global_h_parity/README.md) give

\[
 H_x=(-1)^{x+1+(k-2)/2}
      \operatorname{sgn}(\lambda_x)P(\Psi^x)
 \quad(x\in V),
\tag{5}
\]

\[
 H_\infty=P(\Psi^\infty).
\tag{6}
\]

For the Wallis chart rooted at \(16\), every \(P(\Psi^x)\) is \(+1\).  In
the order \(x=0,\ldots ,15,\infty\), the exact target signs are

\[
\boxed{
(+,-,-,-,-,-,+,+,-,-,-,+,+,+,+,+,+).}
\tag{7}
\]

Thus the corresponding right-side bits in (3) are

\[
\boxed{
(0,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0).}
\tag{8}
\]

The verifier derives (7) independently from the stored Wallis squares and
checks the chart SHA-256; it does not merely hard-code the profile.

## 3. Why every equation is redundant

Call the reduced constraints:

* **(D)** the fixed domains and the 1,800 condition-4
  `AllDifferent(14)` stars, one at every \((uv,i)\);
* **(T)** the 1,680 forced-trace `AllDifferent(15)` stars, one at every
  \((ij,u)\).

Fix \(ij,x\).  Constraint (T) says that

\[
 D_x^{ij}=\{uv:N_{uv}(ij)=x\}
\]

is a matching.  Its allowed support is \(V\) for \(x=\infty\), and

\[
 V\setminus\{a_i(x),a_j(x)\}
\]

for finite \(x\).  Hence its capacity is \(k/2\) or \((k-2)/2\),
respectively.  The capacities for the \(k+1\) colours sum to

\[
 \frac{k}{2}+k\frac{k-2}{2}=\binom{k}{2}.
\tag{9}
\]

The colour classes partition all \(\binom{k}{2}\) edges, so every capacity
is attained.  Thus (T) forces exactly the two families of matchings required
by the finite- and infinity-layer augmentations.

Constraint (D) gives the dual family.  For a fixed \(uv,x\), its holes among
the indices are:

* \(\{i_M\}\) when \(x=\infty\);
* \(\{i_v\}\) when \(x=u\), and \(\{i_u\}\) when \(x=v\);
* \(\{i_u,i_v,i_M\}\) when \(x\notin\{u,v,\infty\}\),

where \(L_{i_u}(u)=x\), \(L_{i_v}(v)=x\), and \(M_{i_M}(uv)=x\).
The canonical dummy completion adds

\[
\{i_M,*\},\qquad \{i_v,*\},\qquad \{i_u,*\},
\]

in the first three cases, and

\[
\{i_u,i_v\},\ \{i_M,*\}
\]

in the generic case.  It therefore produces a no-hole matching tensor on
two ordered \(k\)-sets for every colour.

The no-hole sign theorem says that the product of all \(k^2\) augmented link
signs is \(+1\).  Deleting the known dummy cofactors gives precisely
(5)--(6), so (D)+(T) entail each equation (3) separately.  Notice that
the \(P\)-variables and triangle decompositions are not needed for this
implication.

This proves logical redundancy for arbitrary reduced-\(N\) solutions, whether
or not a solver has found one.

## 4. Rank audit

There are two different ranks worth keeping separate.

| System | Rank of the 17 layer rows |
|---|---:|
| Raw ANF, treating each inversion conjunction as a defined XOR input | 17 |
| Quotient by the reduced constraints (D)+(T) | **0 incremental** |

The raw rank is 17 because every row is nonempty and different colours have
disjoint monomial supports.  The incremental rank is zero because every row
minus its target belongs to the consequence ideal of (D)+(T), by the
preceding theorem.  The all-colour product is the XOR-sum of these seventeen
rows and is likewise redundant.

Accordingly, adding millions of conjunction auxiliaries and seventeen parity
rows would provide no new feasible-set cut.  This package deliberately does
not modify the active search scripts.

## 5. Reproduction and certificate check

The audit is standard-library only:

```sh
python3 -B collaboration/layer_sign_xor_cuts/verify_layer_sign_xor_cuts.py
```

It checks the Wallis target signs, raw ANF sizes, all 1,785 trace support
capacities, all 105 capacity sums, and all 2,040 dual dummy completions.

If the reduced Wallis search later emits an \(N\)-only v2 certificate (or the
joint search emits a full v1 certificate), check its domains, all existing
exact-one constraints, and every explicit layer XOR with:

```sh
python3 -B collaboration/layer_sign_xor_cuts/verify_layer_sign_xor_cuts.py \
  --certificate /path/to/certificate.json
```

The checker authenticates the certificate self-hash and chart hash before
evaluating (3).
