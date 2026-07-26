# Exact global flag Alon--Tarsi formula

Date: 2026-07-26.  This note audits the flag-square calculation in
`collaboration/flag_at_exact_formula_audit_prompt.md`.  All positions below
are zero-based.  The conclusion is a sign evaluation forced by a radius-5
structure; it is neither a construction nor a contradiction.

## Theorem

Let \(k\) be even and let \((L,M,N)\) satisfy the unrestricted radius-5
conditions.  Order \(A,V,\mathcal C=V\sqcup\{\infty\}\), and at a flag
\((i,u)\) use the induced orders
\[
 R_i=A\setminus\{i\},m,l,\qquad
 K_u=V\setminus\{u\},*,\qquad
 X_{i,u}=\mathcal C\setminus\{L_i(u)\}.
\]
Let \(Q^{i,u}\) be the flag Latin square from
`radius4_dual_trace_forced.md`.  Define
\[
 T(i,u)=L_i(u),\quad T(e,u)=u
\]
on rows \(A,e\), columns \(V\), symbols \(V\).  Define the symmetric
idempotent Latin square \(S_i\) on \(\mathcal C\) by
\[
 S_i(u,u)=u,\quad S_i(u,v)=M_i(uv),\quad
 S_i(u,\infty)=S_i(\infty,u)=L_i(u),\quad
 S_i(\infty,\infty)=\infty.
\]
If \(\delta(S_i)\) is the product of its row signs, then
\[
\boxed{\displaystyle
 \prod_{i\in A,u\in V}\operatorname{AT}(Q^{i,u})
 =(-1)^{k(k-1)/2}\operatorname{AT}(T)
   \prod_{i\in A}\delta(S_i).}
\tag{1}
\]

## Sign audit

We use two elementary facts.  Deleting domain position \(r\) and image
position \(s\) from a permutation multiplies its sign by
\((-1)^{r+s}\).  If a common bijection onto
\(\mathcal C\setminus\{a,b\}\) is completed once by a last entry of \(b\)
with target \(\mathcal C\setminus\{a\}\), and once by a last entry of
\(a\) with target \(\mathcal C\setminus\{b\}\), the product of the two
signs is
\[
 (-1)^{\operatorname{pos}(a)+\operatorname{pos}(b)+1}.
\tag{2}
\]

Pair all existing rows at fixed \(u\): row \(j\) at \((i,u)\) with row
\(i\) at \((j,u)\).  Formula (2) applies with
\(a=L_i(u),b=L_j(u)\).  Across all \(u\), each value-position term has
even multiplicity \(k-2\), and the constant term occurs
\(k\binom{k-1}{2}\) times.  The total factor is \(+1\).

Pair all existing columns at fixed \(i\): column \(v\) at \((i,u)\)
with column \(u\) at \((i,v)\).  Their common part consists of the
\(N\)-entries plus the \(m\)-entry \(M_i(uv)\); the \(l\)-entry
completes it by \(L_i(v)\) or \(L_i(u)\).  As \(L_i\) is a permutation,
the exponent is
\[
 (k-1)\sum_{x\in V}\operatorname{pos}(x)+\binom{k}{2}
 =k\binom{k}{2},
\]
so this factor is also \(+1\).

For a dummy \(l\)-row, extend \(L_i\) by
\(\infty\mapsto\infty\), then delete
\(u\mapsto L_i(u)\).  Its sign is
\[
 (-1)^{u+L_i(u)}\operatorname{sgn}(L_i).
\]
The product over \(u\) is \(+1\).

Let \(\pi_{i,u}\) be finite row \(u\) of \(S_i\), and put
\(a=L_i(u)\).  To obtain the dummy \(m\)-row, delete
\(\infty\mapsto a\), then move domain element \(u\) to the last
position representing \(*\).  Its exact sign is
\[
 (-1)^{k+a}(-1)^{k-1-u}\operatorname{sgn}(\pi_{i,u})
 =(-1)^{1+a+u}\operatorname{sgn}(\pi_{i,u}).
\tag{3}
\]
The correction factors in (3) multiply to \(+1\).  Since row
\(\infty\) of \(S_i\) has sign \(\operatorname{sgn}(L_i)\),
\[
 \prod_u\operatorname{sgn}(m\text{-row at }(i,u))
 =\delta(S_i)\operatorname{sgn}(L_i).
\tag{4}
\]

Finally extend each dummy \(*\)-column to
\[
 \Lambda_u:A,m,l\longrightarrow\mathcal C,\qquad
 i\mapsto L_i(u),\quad m\mapsto u,\quad l\mapsto\infty.
\]
Deleting \(i\mapsto L_i(u)\) gives its sign
\((-1)^{i+L_i(u)}\operatorname{sgn}(\Lambda_u)\).  Because \(k-1\)
is odd, multiplication over all flags gives
\[
 \prod_{i,u}\operatorname{sgn}(*\text{-column})
 =(-1)^{k(k-1)/2}\prod_u\operatorname{sgn}(\Lambda_u)
 =(-1)^{k(k-1)/2}C(T).
\tag{5}
\]
The row-sign product of \(T\) is
\(R(T)=\prod_i\operatorname{sgn}(L_i)\).  Multiplying the five audited
groups proves (1).

## What the universal symbol identity does, and does not, evaluate

Let \(\Sigma(Q)\) be the product of the symbol-permutation signs of a
Latin square \(Q\).  The universal Latin-square parity identity is
\[
 \operatorname{AT}(Q)\Sigma(Q)=(-1)^{k(k-1)/2}.
\tag{6}
\]
There are \(k(k-1)\) flags, an even number.  Consequently (6) gives
\[
 \prod_{i,u}\Sigma(Q^{i,u})
 =\prod_{i,u}\operatorname{AT}(Q^{i,u}),
\tag{7}
\]
so the product of the signs of the **completed** symbol permutations is
the same global scalar as (1).
At \(k=16\), the factor in (6) is already \(+1\) flag by flag.

This observation does **not** independently evaluate the signs of the
forced partial fibers \(\Phi_{i,u,x}\).  It says only that after the
prescribed dummy completions, the ordinary symbol-sign product is the same
invariant already evaluated by (1).  A separate theorem constraining the
partial-fiber signs through their per-\(ij\) or per-\(uv\) matchings could
still force a value and could therefore yield a contradiction.  No such
second evaluation is proved here.  The present bare completion/cofactor
calculation merely reproduces (1); the stronger partial-fiber route remains
open.

The exact residual can be displayed.  Let \(p_u(v)\) be the position of
\(v\) in \(V\setminus\{u\}\), and \(r_i(j)\) the position of \(j\) in
\(A\setminus\{i\}\).  Give each partial fiber its induced domain and
codomain orders and write its sign as \(\operatorname{sgn}\Phi_x\).
Let \(w_\infty\) be the \(M_i\)-\(\infty\) partner of \(u\), and put
\(v_0=L_i^{-1}(u)\).  Direct cofactor expansion of the dummy completion
gives
\[
\begin{aligned}
 \operatorname{sgn}(\text{completed }\Phi_\infty)
 &=(-1)^{k-2-p_u(w_\infty)}\operatorname{sgn}\Phi_\infty,\\
 \operatorname{sgn}(\text{completed }\Phi_u)
 &=(-1)^{k-1-p_u(v_0)}\operatorname{sgn}\Phi_u.
\end{aligned}
\tag{8}
\]
For generic \(x\), let \(j_x\) be the omitted row,
\(v_M(x)\) its \(M_i\)-hole, and \(v_L(x)=L_i^{-1}(x)\) its
\(L_i\)-hole.  Then
\[
 \operatorname{sgn}(\text{completed }\Phi_x)
 =(-1)^{r_i(j_x)+p_u(v_M)+p_u(v_L)}
   \varepsilon(v_M,v_L)\operatorname{sgn}\Phi_x,
\tag{9}
\]
where \(\varepsilon(v_M,v_L)=+1\) if \(v_M\) precedes \(v_L\) and
\(-1\) otherwise.  Indeed, on the three deleted rows the completion is
\(j_x\mapsto *,m\mapsto v_M,l\mapsto v_L\); its sign is precisely
\(\varepsilon(v_M,v_L)\).

Across the colors at one flag, the ordinary position exponents in
(8)--(9) reduce to
\[
 \binom{k-2}{2}+1 \pmod 2.
\]
The reason is that the generic omitted rows run once over
\(A\setminus\{i\}\), the \(M\)-holes run over all finite columns except
\(w_\infty\), and the \(L\)-holes run over all finite columns except
\(v_0\).  Therefore
\[
 \Sigma(Q^{i,u})
 =(-1)^{\binom{k-2}{2}+1}
   \left(\prod_{x\ {\rm generic}}\varepsilon(v_M(x),v_L(x))\right)
   \left(\prod_x\operatorname{sgn}\Phi_{i,u,x}\right).
\tag{10}
\]
The fixed factor in (10) cancels over the even number \(k(k-1)\) of
flags.  What remains is an orientation product computable from \(L,M\)
times a partial-fiber sign product depending on \(N\).  Consequently,
with the induced orders fixed, (1), (7), and (10) give the exact
necessary identity
\[
 \boxed{\displaystyle
 \prod_{i,u}\prod_{x\in\mathcal C\setminus\{L_i(u)\}}
   \operatorname{sgn}\Phi_{i,u,x}
 =E(L,M)(-1)^{k(k-1)/2}\operatorname{AT}(T)
   \prod_i\delta(S_i), }\tag{11}
\]
where
\[
 E(L,M)=\prod_{i,u}\prod_{x\ {\rm generic}}
 \varepsilon(v_M(i,u,x),v_L(i,u,x)).
\]
Thus (11) does determine the required global partial-fiber sign from
\(L,M\); it is not, however, an independent evaluation.  A contradiction
would require a second per-\(ij\), per-\(uv\), or joint compatibility
theorem forcing a different value.  No such theorem is proved here.

The companion note `partial_fiber_sign_head.md` proves the further
unrestricted simplification \(E(L,M)=+1\) for every even-\(k\) chart
satisfying conditions 1--2.  Hence every genuine radius-5 extension must
satisfy
\[
 \prod_{i,u}\prod_{x\in\mathcal C\setminus\{L_i(u)\}}
   \operatorname{sgn}\Phi_{i,u,x}
 =(-1)^{k(k-1)/2}\operatorname{AT}(T)\prod_i\delta(S_i).
\]
This remains the same completion/cofactor evaluation, not an independent
constraint on the shared \(N\)-table.

## Reproducible audit

Run:

```bash
python3 -B evidence/odd_graph_local_ball/verify_flag_at_exact_formula.py
```

The stdlib verifier exhausts both elementary sign identities through order
8, checks every dummy-line transformation and the exact symbol-fiber
completion factors on synthetic even orders \(2,4,6,8\), and checks the
genuine \(k=2\) structure:
both flag squares have Alon--Tarsi sign \(+1\),
\(\operatorname{AT}(T)=+1\), \(\delta(S)=-1\), and both sides of (1)
equal \(+1\).

**Scope.**  Formula (1) is conditional on an unrestricted radius-5
structure.  No such structure at \(k=16\) has been constructed or excluded,
so its left side is not presently realized there; only its radius-3
right-hand side can be evaluated on a radius-4 chart.  Erdős--Rosenfeld
Problem #835 remains open.
