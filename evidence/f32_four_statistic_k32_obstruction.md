# A \(K_{32}\) in the four-statistic \(F_{32}\) quotient

This note strengthens the low-coefficient obstruction for a natural
finite-field construction at \(k=16\).  It is an exact finite certificate,
not a failed heuristic search.

Let
\[
 F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1).
\]
For a \(16\)-set \(S\subset F\), define
\[
 \sigma(S)=
 \bigl(e_1(S),e_2(S),e_3(S),e_8(S)+e_1(S)^8\bigr)\in F^4. \tag{1}
\]
Join two elements of \(F^4\) when they are realized by adjacent
\(16\)-sets, where adjacency means intersection size \(15\).

## Theorem

The actual-edge quotient graph of (1) contains a \(K_{32}\).  Consequently,
if
\[
 c(S)=G\bigl(e_1(S),e_2(S),e_3(S),
                  e_8(S)+e_1(S)^8\bigr) \tag{2}
\]
is a proper colouring of \(J(32,16)\), then \(G\) uses at least \(32\)
values.  In particular, no \(17\)-colouring has the form (2), regardless
of how nonlinear or irregular \(G\) is.

## The 32 states

Put
\[
 \lambda(a)=
 \begin{cases}
 1,&a=0\text{ or }\operatorname {Tr}_{F/\mathbb F_2}(a)=1,\\
 0,&\text{otherwise}.
 \end{cases} \tag{3}
\]
The claimed clique is
\[
 {\cal K}_{32}
 =\{(a,a^2,a^3,\lambda(a)):a\in F\}. \tag{4}
\]
Its states are distinct because their first coordinates are distinct.

## Static certificate

For every unordered pair \(a<b\) in the standard five-bit encoding of
\(F\), the verifier contains a 32-bit mask for a \(17\)-set \(R_{a,b}\).
Direct expansion gives
\[
 \begin{aligned}
 \sigma(R_{a,b}\setminus\{a\})
   &=(a,a^2,a^3,\lambda(a)),\\
 \sigma(R_{a,b}\setminus\{b\})
   &=(b,b^2,b^3,\lambda(b)).
 \end{aligned} \tag{5}
\]
Each mask has exactly seventeen set bits and contains \(a\) and \(b\).
The two deletions in (5) therefore share exactly fifteen points and
constitute an actual Johnson edge.

The certificate has one mask for every one of the
\(\binom{32}{2}=496\) unordered pairs.  Thus (4) is an actual-edge
\(K_{32}\).  Properness forces all its states to receive different colours,
which proves the theorem.

## Verification and provenance

Run

```bash
python3 -B evidence/f32_four_statistic_k32_verifier.py
```

The checker implements multiplication in \(F\) by polynomial long division,
recomputes all elementary symmetric coefficients from the roots, verifies
all 496 masks and deletion pairs, and then checks every edge of the claimed
clique.  It contains the static masks but no search code.

The masks were found by exact meet-in-the-middle enumeration.  The 32 field
points were split into two halves.  All subset generating polynomials
\(\prod(1+xt)\) were tabulated through degree eight and indexed by subset
size and their first three coefficients.  For each claimed source state,
matching halves were filtered by the eighth-coefficient condition, and its
256 one-point exchanges were tested.  This search method is not part of the
proof: the static checker independently recomputes every assertion needed
for (5).

This theorem rules out every formula using only the four statistics in
(1).  It does **not** rule out a formula that retains \(e_4\), later
coefficients, or different invariants.  It is neither a construction nor a
nonexistence proof for a tight \(17\)-colouring of \(J(32,16)\), and hence
does not by itself resolve Erdős--Rosenfeld Problem #835.
