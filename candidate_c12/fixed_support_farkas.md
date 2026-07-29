# Exact Farkas certificates for two fixed \(A=45\) supports

This note records two exact, solver-free contradictions for fixed quadruple
degree patterns arising in the \(A=45\), \(z_Q\in\{0,1,3\}\) relaxation of a
hypothetical \(40\)-block \(C(12,6,4)\).

These certificates rule out the two supplied fixed supports.  They do **not**
by themselves prove that the two supports exhaust the global problem, and
they do not address patterns containing \(z_Q=2\).

## Linear formulation

For every \(6\)-subset \(B\subset[12]\), let \(x_B\geq0\).  For every
\(4\)-subset \(Q\), prescribe the degree

\[
d_Q=1+z_Q
\]

and impose

\[
\sum_{B\supset Q}x_B=d_Q.
\]

A genuine block family would give a \(0\)-\(1\) solution, so infeasibility
even over nonnegative real \(x_B\) is sufficient.

A Farkas certificate is a rational weight \(w_Q\) for every quadruple such
that

\[
c_B:=\sum_{Q\subset B}w_Q\geq0
\quad\text{for every }6\text{-subset }B,
\]

but

\[
R:=\sum_Qd_Qw_Q<0.
\]

Indeed, weighting and summing all quadruple-degree equations would give

\[
R
=\sum_Qw_Q\sum_{B\supset Q}x_B
=\sum_Bx_B\sum_{Q\subset B}w_Q
=\sum_Bx_Bc_B\geq0,
\]

contradicting \(R<0\).

## The two certificates

The fixed supports are:

- [`a45_split_witness.json`](a45_split_witness.json);
- [`a45_collapsed_witness.json`](a45_collapsed_witness.json).

The exact verifier
[`verify_fixed_support_farkas.py`](verify_fixed_support_farkas.py) stores each
weight function by rational weights on automorphism orbits of quadruples.  It
then:

1. reconstructs the stabilizer of the standard perfect matching;
2. filters it to the automorphism group of the full fixed degree pattern;
3. expands every listed orbit representative;
4. checks the expected orbit size and prescribed quadruple degree;
5. checks \(c_B\geq0\) for all \(\binom{12}{6}=924\) blocks using exact
   `Fraction` arithmetic; and
6. checks the exact negative value of \(R\).

For the split support, the full pattern has \(32\) matching-preserving
automorphisms and the certificate gives

\[
R=-24.
\]

For the collapsed support, the full pattern has \(192\)
matching-preserving automorphisms and the certificate gives

\[
R=-16.
\]

No LP or constraint solver is used by the verifier.

## One weight for both supports

After applying the matching-preserving permutation

\[
(0,1,2,3,4,5,6,7,8,9,10,11)
\longmapsto
(0,1,2,3,8,9,6,7,4,5,10,11)
\]

to the collapsed support, one can use a single weight for both patterns.
Let \(w^{\rm s}\) be the split certificate above and let
\(\widetilde w^{\rm c}\) be the aligned collapsed certificate.  Both have
nonnegative block coefficients, so their sum

\[
w^*=w^{\rm s}+\widetilde w^{\rm c}
\]

does too.  The four exact pairings are

\[
\begin{array}{c|cc}
 &w^{\rm s}&\widetilde w^{\rm c}\\ \hline
\text{split degrees}&-24&8\\
\text{aligned collapsed degrees}&0&-16
\end{array}
\]

and consequently

\[
\langle d^{\rm split},w^*\rangle
=\langle d^{\rm collapsed},w^*\rangle=-16.
\]

Thus \(w^*\) is one uniform rational inequality excluding both aligned
fixed supports.  The solver-free script
[`verify_common_fixed_support_farkas.py`](verify_common_fixed_support_farkas.py)
checks the alignment, all four pairings, and all \(924\) nonnegative block
coefficients exactly.

## Reproduce

Run:

```bash
python3 candidate_c12/verify_fixed_support_farkas.py \
  split candidate_c12/a45_split_witness.json

python3 candidate_c12/verify_fixed_support_farkas.py \
  collapsed candidate_c12/a45_collapsed_witness.json

python3 candidate_c12/verify_common_fixed_support_farkas.py \
  candidate_c12/a45_split_witness.json \
  candidate_c12/a45_collapsed_witness.json
```

The first command ends with:

```text
degree_weighted_rhs -24
CONTRADICTION: nonnegative block sum equals negative rhs
```

The second ends with:

```text
degree_weighted_rhs -16
CONTRADICTION: nonnegative block sum equals negative rhs
```

The common verifier ends with:

```text
split_pairing -16
collapsed_pairing -16
CONTRADICTION for both aligned supports
```

The weight lists in the verifier are rationalized Farkas duals originally
found by an LP solver.  Their validity is established independently by the
finite exact checks above.
