# The exact partial-fiber sign head

Date: 2026-07-26.  This note corrects the status of the final sign factor in
`flag_at_exact_formula.md`.  The global partial-fiber product is algebraically
fixed on every hypothetical radius-5 extension.  What is missing is an
**independent** evaluation that could conflict with that fixed value.

Throughout, the row, column, and colour orders are the induced orders used in
`flag_at_exact_formula.md`.  This is a conditional structural calculation, not
a construction or an obstruction for Erdős--Rosenfeld Problem #835.

## 1. The exact identity

For a radius-5 structure define

\[
 H(N)=\prod_{i,u}\prod_{x\ne L_i(u)}
       \operatorname{sgn}\Phi_{i,u,x}.
\]

For a generic finite \(x\), let \(v_L=L_i^{-1}(x)\), and let \(v_M\)
be the mate of \(u\) in the \(x\)-class of \(M_i\).  Put

\[
 E(L,M)=\prod_{i,u}
 \prod_{\substack{x\in V\\x\ne u,L_i(u)}}
 \varepsilon_u(v_M,v_L),
\]

where \(\varepsilon_u(a,b)=+1\) when \(a\) precedes \(b\) in the
induced order on \(V\setminus\{u\}\), and \(-1\) otherwise.  Equation
(10) of `flag_at_exact_formula.md`, multiplied over all \(k(k-1)\)
flags, gives

\[
 \prod_{i,u}\Sigma(Q^{i,u})=E(L,M)H(N).                 \tag{1}
\]

The fixed sign in (10) disappears because the number of flags is even.
The universal Latin-square identity gives
\(\prod\Sigma(Q)=\prod\operatorname{AT}(Q)\), and formula (F) gives

\[
 F(L,M):=(-1)^{k(k-1)/2}\operatorname{AT}(T)
          \prod_i\delta(S_i)
       =\prod_{i,u}\operatorname{AT}(Q^{i,u}).           \tag{2}
\]

Therefore every radius-5 extension satisfies the already forced equation

\[
 \boxed{H(N)=F(L,M)/E(L,M).}                            \tag{3}
\]

Calling \(H\) “unevaluated” without this qualification is incorrect.  It is
not independently evaluated, but its required value is fixed by (3).

## 2. The orientation product is always \(+1\)

In fact the denominator in (3) is trivial.

**Theorem.**  For every even \(k\) chart satisfying conditions 1--2,

\[
 \boxed{E(L,M)=+1.}                                     \tag{4}
\]

**Proof.**  Relative order in \(V\setminus\{u\}\) is the same as relative
order in \(V\), so suppress the subscript on \(\varepsilon\).  Fix \(i,x\),
put \(v=L_i^{-1}(x)\), and let \(p_{i,x}\) be the mate involution of the
\(x\)-class of \(M_i\).  By condition 2, colour \(x\) is available exactly
at \(U=V\setminus\{x,v\}\) and occurs once at each vertex there, so its
class is a perfect matching on \(U\).  Its support is therefore
\(U=V\setminus\{x,v\}\).  Hence

\[
 \prod_{u\in U}\varepsilon(p_{i,x}(u),v)
 =\prod_{z\in U}\varepsilon(z,v),                       \tag{5}
\]

because \(p_{i,x}\) permutes \(U\).  Write
\(B_v=\prod_{z\ne v}\varepsilon(z,v)\).  Substituting
\(x=L_i(v)\), the contribution of \(i,v\) is
\(B_v/\varepsilon(L_i(v),v)\).  Condition 1 says that, for fixed \(v\),
the values \(L_i(v)\) run once through \(V\setminus\{v\}\).  Thus

\[
 \prod_i\frac{B_v}{\varepsilon(L_i(v),v)}
 =\frac{B_v^{\,k-1}}{B_v}=B_v^{\,k-2}=1,
\]

since \(k-2\) is even.  Multiplication over \(v\) proves (4). \(\square\)

Combining (3) and (4) gives the exact remaining condition

\[
 \boxed{H(N)=(-1)^{k(k-1)/2}\operatorname{AT}(T)
                  \prod_i\delta(S_i).}                  \tag{6}
\]

This is still the same completion/cofactor evaluation, not a second theorem
about \(N\).

## 3. Exact finite values

`verify_partial_fiber_sign_head.py` computes the terms, reusing the committed
complete radius-3 census generator.

* At \(k=6\), all 1,680 labelled radius-3 families and all seven choices of
  distinguished colour give 11,760 cases.  In every case \(E=+1\).
  The conditional target is \(H_{\rm required}=-1\) in 6,720 cases and
  \(+1\) in 5,040 cases.  Each family has four negative and three positive
  distinguished-colour choices; all 35 such four-subsets occur, each for
  48 families.
* For the Wallis \(k=16\) family, all 17 choices of distinguished colour give
  \((E,F,H_{\rm required})=(+1,+1,+1)\).

No actual \(H\) is observed in either computation: no \(k=6\) radius-5
extension exists, and no Wallis \(k=16\) radius-5 extension is known.
Consequently the mixed \(k=6\) targets do **not** refute a constant-sign
theorem for genuine radius-5 structures.  Such a theorem would instead
exclude precisely the radius-3 charts whose required value disagreed with
it.

## 4. What one-sided trace data cannot prove

There is an exact local no-go for the simplest proposed route.  Take the
cyclic order-6 Latin chart

\[
 L_i(u)=u+i+1\pmod 6.
\]

For every \(ij\), enumerate all complete edge-colourings of \(K_6\) having
the forced radius-5 trace: one perfect \(\infty\)-class and six
near-perfect finite classes with the prescribed two missing vertices.
Depending on \(ij\), there are 12, 20, or 56 such complete slices (four,
four, and two pairs \(ij\), respectively).

At the single flag \((i,u)=(0,0)\), independent choices of those exact
\(ij\)-slices give:

* for \(x=\infty\), five possible four-column image sets, and **both**
  partial-permutation signs occur for every image set;
* for the generic colour \(x=2\), four possible three-column image sets, and
  **both** signs occur for three of them.

Thus even after the image set is fixed, the exact per-\(ij\) trace conditions
do not determine the sign of one fiber.  This is a genuine collection of
complete one-sided slices, not merely a list of abstract permutations:
the verifier constructs every slice from its prescribed perfect and
near-perfect colour classes.

The conclusion is narrow.  It rules out a proof that assigns the fiber signs
from each \(ij\)-trace separately.  It does not rule out a global parity
theorem using compatibility among all \(ij\)-slices, the dual \(uv\)-matching
conditions, or the full \(N\)-table.  Indeed, the same verifier finds that
this cyclic synthetic chart has no globally proper assembly even after all
\(M\)-palette conditions are omitted.

## 5. The complete no-hole analogue

As a control, let both sides be \(K_n\), with no holes: every \(ij\) chooses a
perfect matching on the second \(K_n\), and for every \(uv\) the selected
\(ij\)'s also form a perfect matching.  The verifier exhausts:

* all six \(K_4\times K_4\) tensors;
* all 336 \(K_6\times K_6\) tensors after fixing the matching at one edge.

The normalization at \(n=6\) is without loss.  A relabelling of the second
vertex set sends any perfect matching to the fixed canonical matching.  If
\(\rho\) is such a relabelling, the local link sign at \((i,u)\) changes by
the cofactor sign

\[
 (-1)^{\operatorname{pos}(u)+\operatorname{pos}(\rho(u))}
 \operatorname{sgn}(\rho).
\]

This factor is repeated for all \(n\) choices of \(i\), so its global product
is \(+1\) when \(n\) is even.  Hence the global sign is preserved.

Every enumerated no-hole tensor has global link-sign product \(+1\).  This is
only a finite positive control, not a theorem for every even \(n\).  More
importantly, it does not transfer to (6): the actual fibers have
colour-dependent deleted rows and columns, and their cofactor orientations
are exactly the terms audited in Sections 1--2.  No independent general
\(H=+1\) theorem is proved here.

## Reproduction and status

Run:

```bash
python3 -B evidence/odd_graph_local_ball/verify_partial_fiber_sign_head.py
```

The remaining decisive task is an independent parity theorem for the full
compatible \(N\)-layer.  To exclude \(k=16\), it must disagree with (6) for
every admissible \(k=16\) radius-3 chart; disagreement only on Wallis excludes
only Wallis.  No such theorem is presently known, and Problem #835 remains
open.
