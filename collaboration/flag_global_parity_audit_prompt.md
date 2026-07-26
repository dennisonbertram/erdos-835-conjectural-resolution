# Priority audit: finish the flag-Latin global sign calculation

We now have a symbolic theorem: every radius-5 \(L,M,N\) structure gives,
for each flag \((i,u)\), a Latin square \(Q^{i,u}\) of even order \(k\).
The triple sign is universal and therefore vacuous; the only potentially
contentful quantity is the Alon--Tarsi sign
\[
  \operatorname{AT}(Q^{i,u})=\rho(Q^{i,u})\gamma(Q^{i,u}).
\]
Please do the heavy mathematical work on the unrestricted problem, not on the
fixed Wallis/cyclic ansatz.

## New exact cancellation to audit

For a relabelling \(\tau\) of the finite column set, write
\(\varepsilon_\tau(\{a,b\})=-1\) precisely when \(\tau\) reverses the
relative order of \(a,b\).  At flag \((i,u)\), the residual factor from the
generic symbol fibers is
\[
 R_\tau(i,u)=
 \prod_{\substack{x\in V\\x\ne u,L_i(u)}}
 \varepsilon_\tau\!\left(
 \{L_i^{-1}(x),p_{i,x}(u)\}\right),
\]
where \(p_{i,x}(u)\) is the mate of \(u\) in the \(x\)-class of \(M_i\).

For fixed \(i,x\), that \(x\)-class is a perfect matching on
\(V\setminus\{x,L_i^{-1}(x)\}\).  Hence, putting
\(v=L_i^{-1}(x)\) and multiplying over every admissible \(u\), each endpoint
of that matching occurs exactly once:
\[
 \prod_u R_\tau(i,u)
 =\prod_{v\in V}\prod_{z\ne v,L_i(v)}
   \varepsilon_\tau(\{v,z\})
 =\prod_{v\in V}\varepsilon_\tau(\{v,L_i(v)\}).
\]
The full directed complete graph product is \(1\), and division is the same
as multiplication for signs.  Finally condition 1 says that for each fixed
\(v\), \(\{L_i(v):i\in A\}=V\setminus\{v\}\), so
\[
 \prod_{i,u}R_\tau(i,u)
 =\prod_{v}\prod_{z\ne v}\varepsilon_\tau(\{v,z\})=1.
\]

Please check every quantifier, endpoint multiplicity, and exceptional color.
If correct, turn it into a short rigorous lemma.  Its significance should be
stated narrowly: the full flag symbol-sign product is globally
reference-independent.  It does not determine its value.

## Main requested calculation

Choose explicit canonical orders and compute, without handwaving,
\[
 \prod_{i\in A,u\in V}\operatorname{AT}(Q^{i,u})
\]
by pairing:

1. the existing row \(j\) of \(Q^{i,u}\) with the existing row \(i\) of
   \(Q^{j,u}\);
2. the existing column \(v\) of \(Q^{i,u}\) with the existing column \(u\)
   of \(Q^{i,v}\);
3. all dummy \(m\)-rows, dummy \(l\)-rows, and dummy \(*\)-columns.

Track all deletion/cofactor signs.  A plausible but **unproved** schematic
outcome is
\[
  \prod_{i,u}\operatorname{AT}(Q^{i,u})
  =(-1)^{k(k-1)/2}\,C_L\,\prod_i\delta(S_i),
\]
or a nearby variant, where \(C_L\) is a column-sign product of the Latin
square obtained from the identity row plus the \(L_i\), and \(S_i\) is the
symmetric Latin object associated with the \(M_i\) one-factorization.
Do not accept this formula: derive the correct one from definitions and
either prove it or give a concrete counterexample.

Then ask the decisive question: do conditions 1--4 plus the forced
radius-5 trace force the two sides to incompatible signs at \(k=16\)?
Use exact small-\(k\) enumeration or symbolic scripts as controls.  A universal
Latin identity is not an obstruction.  A fixed-Wallis computation is not an
unrestricted theorem.

Write any audited theorem/counterexample and verifier into your existing
collaboration output directory.  Clearly label PROVED, COMPUTATION, CONJECTURE,
and OPEN.  Do not claim Erdős--Rosenfeld #835 solved unless the unrestricted
existential problem is actually closed.
