# Exact candidate formula: please audit or refute every sign

The absence of a nondegenerate radius-5 control does not prevent a symbolic
cofactor proof.  I derived the following exact formula.  Please attack it
line-by-line, run synthetic cofactor controls and the \(k=2\) genuine control,
and either certify it or identify the first wrong sign.

Fix zero-based orders on \(A,V\), order
\(\mathcal C=V,\infty\), and at flag \((i,u)\) order

- rows: \(A\setminus\{i\},m,l\);
- columns: \(V\setminus\{u\},*\);
- symbols: \(\mathcal C\setminus\{L_i(u)\}\),

all by induced order with dummy elements last.

Define the order-\(k\) Latin square \(T\) on rows \(A\cup\{e\}\),
columns \(V\), symbols \(V\) by
\[
 T(i,u)=L_i(u),\qquad T(e,u)=u.
\]
Define the symmetric idempotent Latin square \(S_i\) of order \(k+1\)
on \(\mathcal C\) by
\[
\begin{aligned}
S_i(u,u)&=u,&S_i(u,v)&=M_i(uv)\quad(u\ne v),\\
S_i(u,\infty)&=S_i(\infty,u)=L_i(u),&
S_i(\infty,\infty)&=\infty.
\end{aligned}
\]
Let \(\delta(S_i)\) be the product of all \(k+1\) row-permutation
signs and \(\operatorname{AT}(T)\) the row-sign product times
column-sign product.  Claim, for every even \(k\):
\[
\boxed{\displaystyle
 \prod_{i\in A,u\in V}\operatorname{AT}(Q^{i,u})
 =(-1)^{k(k-1)/2}\operatorname{AT}(T)
   \prod_{i\in A}\delta(S_i).}
\tag{F}
\]

Use the elementary completion/cofactor lemma:
if \(g:D\to\mathcal C\setminus\{a,b\}\), and \(f_a\) appends
\(*\mapsto b\) with target \(\mathcal C\setminus\{a\}\), while \(f_b\)
appends \(*\mapsto a\) with target \(\mathcal C\setminus\{b\}\), then
\[
 \operatorname{sgn}(f_a)\operatorname{sgn}(f_b)
 =(-1)^{\operatorname{pos}(a)+\operatorname{pos}(b)+1}.
\tag{C}
\]
The sign of a permutation restricted by deleting domain position \(r\)
and its image position \(s\) is
\((-1)^{r+s}\) times the full sign.

## Pairing calculation to check

1. Existing rows: pair row \(j\) of \(Q^{i,u}\) with row \(i\) of
   \(Q^{j,u}\).  Apply (C) with
   \(a=L_i(u),b=L_j(u)\).  For fixed \(u\), the \(a\)'s run over
   \(V\setminus\{u\}\), and each occurs in \(k-2\) pairs.  Over all
   \(k\) values of \(u\), the total factor is \(+1\).

2. Existing columns: pair column \(v\) of \(Q^{i,u}\) with column \(u\)
   of \(Q^{i,v}\).  Their common part includes the \(N\)-entries and
   the common \(m\)-entry \(M_i(uv)\); the last \(l\)-entry completes by
   \(L_i(v)\) versus \(L_i(u)\).  Apply (C).  For fixed \(i\),
   \(\{L_i(u),L_i(v)\}\) runs over every pair of \(V\); the product is
   \(+1\) for even \(k\).

3. Dummy \(l\)-rows: these are the row permutation
   \(v\mapsto L_i(v),\infty\mapsto\infty\), with domain \(u\) and image
   \(L_i(u)\) deleted.  For fixed \(i\), their product over \(u\) is
   \[
   \operatorname{sgn}(L_i)^k
   (-1)^{\sum_u\operatorname{pos}(u)+
          \sum_u\operatorname{pos}(L_i(u))}=1.
   \]

4. Dummy \(m\)-rows: let \(\pi_{i,u}\) be row \(u\) of \(S_i\).
   Delete domain \(\infty\) and image \(L_i(u)\); then move domain
   \(u\) to the last position to represent \(*\).  The signs from
   deletion/reordering multiply to \(+1\) over all \(u\).  Hence
   \[
   \prod_u\operatorname{sgn}(m\text{-row of }Q^{i,u})
   =\prod_{u\in V}\operatorname{sgn}(\pi_{i,u})
   =\delta(S_i)\operatorname{sgn}(L_i),
   \]
   since row \(\infty\) of \(S_i\) has sign \(\operatorname{sgn}(L_i)\).

5. Dummy \(*\)-columns: extend it before deletion to the permutation
   \(\Lambda_u:A\cup\{m,l\}\to\mathcal C\),
   \(i\mapsto L_i(u),m\mapsto u,l\mapsto\infty\).
   Deleting \(i\mapsto L_i(u)\) gives the \(*\)-column of \(Q^{i,u}\).
   Since \(k-1\) is odd, multiplication first over \(i\), then \(u\),
   gives
   \[
   \prod_{i,u}\operatorname{sgn}(*\text{-column})
   =(-1)^{k(k-1)/2}\,C(T),
   \]
   where \(C(T)\) is the column-sign product of \(T\).

The row-sign product of \(T\) is
\(R(T)=\prod_i\operatorname{sgn}(L_i)\).  Multiplying items 1--5
therefore yields (F).

At \(k=2\), the genuine structure has two order-2 flag squares,
\(\operatorname{AT}=+1\) each; \(T\) has \(\operatorname{AT}=+1\);
the order-3 symmetric idempotent \(S\) has \(\delta(S)=-1\); thus the
right side is \((-1)^1(+1)(-1)=+1\), a genuine control.

If (F) is correct, state its scope exactly: it evaluates the global
flag AT product entirely from radius-3 \(L,M\) data, but is not yet a
contradiction.  Then determine whether some second evaluation of the
same product from the forced symbol fibers yields a different sign at
\(k=16\), or prove that it reduces to the same identity.  Do not stop
merely because a nondegenerate radius-5 test instance is absent.
