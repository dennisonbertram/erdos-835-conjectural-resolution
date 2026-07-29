# Corrected ordered triple-profile equality, LP, and lattice audit

## Scope and conclusion

Assume a hypothetical \(k=16\) fibre
\({\cal C}\cong S(14,15,31)\).  Fix an ordered pair
\((B,C)\in{\cal C}^2\) with

\[
|B\cap C|=u,\qquad 1\leq u\leq13,
\]

and define

\[
\nu_{s,t}(B,C)=
\#\{D\in{\cal C}\setminus\{B,C\}:
|B\cap D|=s,\ |C\cap D|=t\},
\qquad 1\leq s,t\leq13.
\]

This note rebuilds the complete presently proved *linear* system used for
these 169 ordered triple-profile variables.  It explicitly incorporates the
proved scalar actions on \({\cal H}_1,{\cal H}_2\), the complete two-map
action on \({\cal H}_3\), the complete three-map action on
\({\cal H}_4\), the safe certified annihilators at levels \(5,6,7\), and
the elementary geometric zero cells that the earlier 169-variable audit
omitted.

The result is a closure, not a contradiction:

* every \(u=1,\ldots,13\) equality system is consistent over
  \(\mathbb Q\);
* every system has an exact rational solution which is **strictly positive
  in every geometrically possible cell** and obeys the ambient cell
  capacities;
* every system also has an exact nonnegative **integer** solution obeying
  those capacities.

Thus neither an LP/Farkas separation nor a one-profile congruence obstruction
exists in this complete local system.  The integer witnesses are local count
tables only.  They are not designs, need not couple consistently across
different ordered pairs, and do not solve Erdős--Rosenfeld problem #835.

## 1. Equations included

Write \(A_s\) for the fibre intersection matrices, \(P_a\) for the restricted
degree-\(a\) harmonic projector, and

\[
f_a(t)=(P_a)_{D,C}\quad\text{when }|D\cap C|=t.
\]

The verifier uses one common exact integer multiple of the Johnson kernel
\(f_a\), so no floating-point arithmetic enters the equality audit.

### Structural zeros and capacities

Partition the ground set into

\[
B\cap C,\quad B\setminus C,\quad C\setminus B,\quad
[31]\setminus(B\cup C)
\]

of sizes \(u,15-u,15-u,u+1\).  If \(a=|B\cap C\cap D|\), then a cell
\((s,t)\) is geometrically possible exactly when some \(0\leq a\leq u\)
satisfies

\[
0\leq s-a,t-a\leq15-u,\qquad
0\leq15-s-t+a\leq u+1.
\]

Every other cell is set to zero.  The ambient number of all \(15\)-sets in a
possible cell is

\[
p_{s,t}^{\,u}
=\sum_a
\binom ua\binom{15-u}{s-a}
\binom{15-u}{t-a}\binom{u+1}{15-s-t+a}.
\tag{1}
\]

Both persisted witness families are checked against
\(0\leq\nu_{s,t}\leq p_{s,t}^{\,u}\).

### Row and column sums

If \(n_s\) is the forced fibre intersection distribution, then

\[
\sum_t\nu_{s,t}=n_s-\mathbf1_{\{s=u\}},\qquad
\sum_s\nu_{s,t}=n_t-\mathbf1_{\{t=u\}}.
\tag{2}
\]

These are the \({\cal H}_0\) or valency equations.

### A uniform formula for every right-module relation

Let

\[
Z=z_0I+\sum_{s=1}^{13}z_sA_s,\qquad ZP_a=0.
\]

Taking the \((B,C)\) entry gives

\[
\boxed{
\sum_{s,t}z_s f_a(t)\nu_{s,t}
=-z_0f_a(u)-z_uf_a(15).
}
\tag{3}
\]

The transposed equation is included as well.  All module information below
is entered through (3).

### Exact action relations at levels 1 through 4

The complete proved action kernels have dimensions

\[
13,\quad13,\quad12,\quad11.
\]

They are generated respectively by

\[
\begin{aligned}
(A_s-b_sI)P_1&=0 &&(1\leq s\leq13),\\
(A_s-a_sI)P_2&=0 &&(1\leq s\leq13),\\
(A_s-\alpha_sI-\beta_sA_1)P_3&=0 &&(2\leq s\leq13),\\
(A_s-\gamma_sI-\delta_sA_1-\epsilon_sA_{13})P_4&=0
&&(2\leq s\leq12).
\end{aligned}
\tag{4}
\]

The \(a_s,b_s\) tables are those proved in
`general_h2_rigidity` and `joint_schreier_krein_attack`.  The level-three
table is the complete action

\[
A_sP_3=(\alpha_sI+\beta_sR)P_3,
\qquad A_{13}P_3=(372I+R)P_3,
\]

from `schreier_h3_support`.  The level-four table is

\[
A_sP_4=(\gamma_sI+\delta_sR+\epsilon_sA_{13})P_4
\]

from `schreier_h4_support`.

The verifier independently checks that these four explicit action families
span exactly the same certified annihilator spaces obtained from the
staircase support plus the strength-\(14\) identity
\(17\iota^*E_a\iota P_a=P_a\).  Consequently, writing the scalar
\({\cal H}_2\) action explicitly is essential for audit clarity but does not
add a hidden rank increment: its thirteen relations were already spanned by
the thirteen safe level-two annihilators.

### Safe levels 5 through 7

No exact image-rank claim is used at these levels.  The verifier includes
only the staircase-support annihilators and the strength-\(14\) relation.
Their certified dimensions are

\[
10,\quad9,\quad8.
\tag{5}
\]

Thus the base system has

\[
26+2(13+13+12+11+10+9+8)=178
\]

displayed equations before the \(u\)-dependent structural zeros.  The
twenty-eight earlier equations
\((\iota^*E_j\iota P_a)_{BC}=0\), in both orientations, are checked to lie
in these same annihilator spans and are therefore redundant rather than
additional constraints.

## 2. Exact ranks after the missing geometric zeros

The raw 178-equation system has rank \(114\) for every \(u\), agreeing with
the earlier elimination after its redundant rows are removed.  Adding the
necessary structural zero cells changes the rank sharply:

| \(u\) | possible cells | equations | rank | affine dimension |
|---:|---:|---:|---:|---:|
| 1 | 48 | 299 | 169 | 0 |
| 2 | 69 | 278 | 169 | 0 |
| 3 | 88 | 259 | 167 | 2 |
| 4 | 103 | 244 | 165 | 4 |
| 5 | 114 | 233 | 163 | 6 |
| 6 | 121 | 226 | 161 | 8 |
| 7 | 124 | 223 | 159 | 10 |
| 8 | 123 | 224 | 160 | 9 |
| 9 | 118 | 229 | 162 | 7 |
| 10 | 109 | 238 | 164 | 5 |
| 11 | 96 | 251 | 166 | 3 |
| 12 | 79 | 268 | 168 | 1 |
| 13 | 59 | 288 | 169 | 0 |

Every augmented row reduction is consistent over \(\mathbb Q\).

## 3. Exact rational and integer feasibility

SciPy/HiGHS was used only to discover convenient interior rational
parameters.  OR-Tools CP-SAT was used only to discover integer parameters.
Neither solver is trusted by the certificate.

The committed verifier stores at most ten free coordinates per \(u\),
reconstructs all 169 entries by deterministic exact rational RREF, and then
checks:

1. every displayed equality exactly;
2. every structural zero exactly;
3. \(0\leq\nu_{s,t}\leq p_{s,t}^{\,u}\);
4. strict positivity of the rational witness in every possible cell;
5. integrality and nonnegativity of the integer witness.

The certificate summary is:

| \(u\) | rational minimum on possible cells | rational max denominator | integer support | integer minimum positive |
|---:|---:|---:|---:|---:|
| 1 | 35 | 1 | 48 | 35 |
| 2 | 9 | 1 | 69 | 9 |
| 3 | \(9/2\) | 2 | 86 | 18 |
| 4 | \(15/2\) | 2 | 101 | 2 |
| 5 | \(45/4\) | 8 | 106 | 35 |
| 6 | 15 | 1540 | 114 | 2 |
| 7 | 14 | 3 | 117 | 1 |
| 8 | \(29/2\) | 840 | 118 | 1 |
| 9 | \(51/4\) | 104 | 112 | 3 |
| 10 | \(35/4\) | 24 | 107 | 2 |
| 11 | \(13/3\) | 3 | 95 | 1 |
| 12 | 3 | 1 | 78 | 12 |
| 13 | 5 | 1 | 59 | 5 |

The unique systems at \(u=1,2,13\) already have nonnegative integral
solutions.  For all other \(u\), the explicit integral parameters prove that
the affine lattice meets the nonnegative capacity box.  This is stronger
than merely observing that no individual coordinate is fixed.

## 4. What remains open

The witnesses certify only one ordered-pair profile at a time.  They do not
enforce:

* simultaneous compatibility of the profiles for all ordered pairs;
* the existence of actual \(15\)-subsets realising the chosen counts
  simultaneously;
* the Steiner uniqueness equations beyond those already compressed into the
  module and valency identities;
* zero-one incidence tensors or the partition into seventeen fibres.

The next viable obstruction must couple multiple roots/pairs or restore
zero-one incidence information.  The local equality, LP, and congruence
routes audited here are closed.

## 5. Verification

The default audit uses only the Python standard library and exact
`Fraction` arithmetic:

```sh
python3 -B \
  collaboration/corrected_triple_profile_lp/verify_corrected_triple_profile_lp.py
```

The optional `--solve-all` and `--integer-solve-all` modes reproduce the
floating discovery searches when SciPy or OR-Tools is installed.  Their
outputs are not needed for, and are not accepted in place of, the default
exact reconstruction.
