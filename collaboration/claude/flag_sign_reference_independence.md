# Reference independence of the global flag symbol-sign product

Date: 2026-07-26.  Labels used exactly: **PROVED / COMPUTATION /
CONJECTURE / OPEN**.  Companion verifier:
`flag_sign_reference_independence.py` (passes; 200 random
relabellings, per-\(i\) and global identities, on the Wallis chart's
condition-1/2 data — which is all the lemma uses).  Everything is
about the **unrestricted** structure; the Wallis chart appears only as
COMPUTATION-level test data.

## Lemma (PROVED): global cancellation of the pair-orientation residual

Let \((L,M,N)\) satisfy radius-4 conditions 1–2 (only these are used).
For a permutation \(\tau\) of \(V\) let
\(\varepsilon_\tau(\{a,b\})=-1\) iff \(\tau\) reverses the relative
order of \(a,b\), and at a flag \((i,u)\) set

\[
 R_\tau(i,u)=\prod_{\substack{x\in V\\ x\ne u,\ x\ne L_i(u)}}
 \varepsilon_\tau\bigl(\{L_i^{-1}(x),\,p_{i,x}(u)\}\bigr),
\]

\(p_{i,x}(u)\) the mate of \(u\) in the \(x\)-class of \(M_i\).  Then

\[
 \prod_{u\in V}R_\tau(i,u)=\prod_{v\in V}
 \varepsilon_\tau(\{v,L_i(v)\})
 \qquad\text{and}\qquad
 \prod_{i\in A}\prod_{u\in V}R_\tau(i,u)=1 .
\]

*Proof.*  Fix \(i\) and a finite \(x\).  The colour \(x\) is generic at
\((i,u)\) iff \(u\notin\{x,L_i^{-1}(x)\}\) — precisely the support of
the \(x\)-class matching of \(M_i\) (condition 2).  As \(u\) runs over
that support, so does \(p_{i,x}(u)\), each vertex exactly once (the
mate map is an involution of the support).  Hence

\[
 \prod_u\varepsilon_\tau(\{L_i^{-1}(x),p_{i,x}(u)\})
 =\prod_{z\ne x,\,L_i^{-1}(x)}\varepsilon_\tau(\{L_i^{-1}(x),z\}).
\]

Substituting \(v=L_i^{-1}(x)\) (bijective in \(x\)) and multiplying
over \(x\) gives
\(\prod_uR_\tau(i,u)=\prod_v\prod_{z\notin\{v,L_i(v)\}}
\varepsilon_\tau(\{v,z\})\).  The full ordered product
\(\prod_v\prod_{z\ne v}\varepsilon_\tau(\{v,z\})\) counts every
unordered pair twice, hence equals \(1\); removing the factors
\(z=L_i(v)\) therefore leaves \(\prod_v\varepsilon_\tau(\{v,L_i(v)\})\)
(signs: division = multiplication).  Finally condition 1 says
\(\{L_i(v):i\in A\}=V\setminus\{v\}\) for each \(v\), so multiplying
over \(i\) restores the full ordered product: \(1\). \(\square\)

**Significance, stated narrowly.**  The lemma proves global
reference-independence of the **generic partial-fiber orientation
contribution** under finite-column relabelling.  It does not include
the \(u\)- and \(\infty\)-fibers.  Independently, after all fibers are
completed inside the even-order Latin square \(Q^{i,u}\), the full
symbol-sign product is reference-independent for the elementary
reason that every reference change is repeated \(k\) times.  Neither
statement determines a sign value, and neither is an obstruction.

## Formula (F): CERTIFIED (formal assembly + machine audit)

Audit script: `audit_formula_F.py` (this directory; 1 s; all
assertions pass, zero sign discrepancies).  Verdict: for every even
\(k\), in any radius-5 structure,

\[
 \prod_{i\in A,\,u\in V}\operatorname{AT}(Q^{i,u})
 =(-1)^{k(k-1)/2}\,\operatorname{AT}(T)\,\prod_{i\in A}\delta(S_i),
 \tag{F}
\]

assembled from: cofactor lemma (C) (PROVED-BY-EXHAUSTION through
size 8; 90,200 instances) and the deletion rule (exhausted \(n\le6\));
the flag-Latin-square theorem; \(N\)-symmetry; conditions 1–2; and
\(k\) even.  The five-class partition of the flag AT product closes
exactly: items 1–2 are \(N\)-independent via (C) (exact per-\(u\)
exponent \((k-2)(k(k-1)/2-\mathrm{pos}\,u)+\binom{k-1}2\), total even
for even \(k\); per-\(i\) exponent \(k^2(k-1)/2\)); item 3 \(=+1\);
item 4 \(=\prod_i\delta(S_i)\operatorname{sgn}(L_i)\); item 5
\(=(-1)^{k(k-1)/2}C(T)\); and \(R(T)=\prod_i\operatorname{sgn}(L_i)\).
Genuine end-to-end control at \(k=2\) (the only decided parameter
with a radius-5 structure): both sides \(+1\), with condition 4
degenerating vacuously as documented in the script.

**Scope (exact).**  (F) conditionally evaluates the
reference-independent global flag AT product entirely from radius-3
\(L,M\) data.  It is a STRUCTURAL IDENTITY, not an obstruction.  The
Wallis chart makes its right side \(+1\), but no radius-5 Wallis
extension is known, so the actual left side is not realized there.
OPEN (decisive): whether a second forced evaluation of the same
invariant from the partial symbol fibers can disagree with (F).
Disagreement for one chart would exclude only that chart; a value
incompatible with every admissible \(L,M\) would close the unrestricted
\(k=16\) case.  Neither is claimed.  **#835 is not solved.**
