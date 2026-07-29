# Affine ternary radius-five ansatz: an exact local refutation

This note tests one sharply specified finite-field idea at the first
unresolved local layer of the \(k=16\) problem. It neither proves nor
disproves Erdős–Rosenfeld Problem #835.

## The ansatz

Use the explicit cyclic golf design \(G(17)\) from the file
global_latin_compatibility.md. Its fifteen squares give the fixed radius-four
functions \(M_i(uv)\), with \(i\in\{0,\ldots,14\}\), on a 17-point colour
field \(\mathbb F_{17}\). Pick any point \(\infty\in\mathbb F_{17}\) to omit
and put \(V=\mathbb F_{17}\setminus\{\infty\}\).

For a fixed pair \(ij\), the proposed radius-five colouring is the most
general symmetric affine ternary rule

\[
P_{ij}(u,v,w)=a_{ij}(u+v+w)+b_{ij},
\qquad a_{ij}\in\mathbb F_{17}^{*},\quad b_{ij}\in\mathbb F_{17}.
\tag{1}
\]

The nonzero condition is necessary: for a fixed pair \(uv\), the fourteen
values as \(w\) ranges through \(V\setminus\{u,v\}\) must be distinct.
Those fourteen values omit precisely

\[
\{a(2u+v)+b,\ a(u+2v)+b,\ a(u+v+\infty)+b\}.
\tag{2}
\]

The exact radius-five condition requires every \(P_{ij}(u,v,w)\) to avoid
\(M_i(uv)\) and \(M_j(uv)\). Because (1) is injective in \(w\), a necessary
condition is consequently

\[
\{M_i(uv),M_j(uv)\}\subseteq
\{a(2u+v)+b,a(u+2v)+b,a(u+v+\infty)+b\}.
\tag{3}
\]

for every \(uv\in\binom V2\). The remaining omitted value would have to be
the \(N_{uv}(ij)\) colour, so (3) is a necessary condition before the
additional \(N\)-edge-colouring and triple compatibility conditions are even
considered.

## Exhaustive result

The verifier checks (3) for all

\[
17\times\binom{15}{2}\times16\times17=485{,}520
\]

choices of omitted point, index pair, and affine parameters. There are
**zero** survivors. The computation first verifies the relevant golf
transversal identity

\[
\{M_i(uv):0\le i<15\}=\mathbb F_{17}\setminus\{u,v\}.
\]

Thus no rule of the form (1) can extend the particular cyclic \(G(17)\)
radius-four chart, even at the necessary face-avoidance stage.

## A general obstruction to one shared ternary operation

There is an even simpler scope warning for the phrase “a Steiner operation
over the colour field.” Suppose a *single* ternary operation
\(\Phi(u,v,w)\), independent of \(ij\), were used for every \(P_{ij}\), and
its restriction in \(w\) had the required fourteen distinct values for each
fixed \(uv\). Let \(E_{uv}\) be the three omitted values. The radius-five
condition would give

\[
\{M_i(uv),M_j(uv)\}\subseteq E_{uv}\qquad\text{for every }i\ne j.
\tag{4}
\]

But the golf identity says that the fifteen values \(M_i(uv)\) are all
distinct. Varying the pair in (4) would put all fifteen values in the
three-element set \(E_{uv}\), an immediate contradiction. The same argument
rules out a rule depending only on \(i\) or only on \(j\): fix that index and
vary the other, which would require its fourteen-value image to omit all
fifteen transverse \(M\)-values.

Hence a radius-five construction cannot be a single Steiner ternary operation
on the colour field. It must depend essentially on the unordered index pair
\(ij\); the affine experiment above tests the smallest such pair-dependent
family.

Run the audit with:

    python3 -B evidence/verify_affine_ternary_radius5_no_go.py

## Scope

This is **not** a nonexistence proof for the radius-five ball. It leaves open
arbitrary triple rules \(P_{ij}\), non-affine algebraic rules, a different
choice of golf design, and every global construction route. In particular it
does not settle Problem #835.
