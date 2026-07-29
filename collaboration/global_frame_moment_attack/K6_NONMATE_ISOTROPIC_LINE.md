# A non-mate line in the deleted \(k=6\) quadratic cone

Date: 2026-07-26.

## Exact statement

Let \(D\) be the canonical Witt system \(W_{12}=S(5,6,12)\), let \(M_D\)
be the \(792\)-by-\(792\) incidence matrix obtained by deleting the columns
of \(D\), and work over \(\mathbb F_7\).

The witness file records a set
\[
E\subseteq \binom{[12]}6\setminus D,\qquad |E|=396,
\]
such that every \(5\)-set lies in exactly three blocks of \(E\).  Thus \(E\)
is a simple \(5\!-\!(12,6,3)\) subdesign contained in the complement of
\(D\).

Define
\[
x_B=
\begin{cases}
-1=6\pmod 7,&B\in E,\\
+1,&B\notin E.
\end{cases}
\]
Every deleted star contains three values \(+1\) and three values \(-1\).
Consequently
\[
M_Dx=0,\qquad M_D(x^{\circ2})=6\mathbf1.
\]
Therefore \([x]\) is a projective isotropic line for the deleted-colour
Hadamard-kernel quadratic system.

It is not one of the 144 Steiner-mate lines.  A mate line represented by
\(h_C=\mathbf1+\mathbf1_C\) has two local values with multiplicities
\(5+1\) on every star, whereas \(x\) has multiplicities \(3+3\).

## Reproduction

Run:

```bash
python3 -B collaboration/global_frame_moment_attack/verify_k6_lambda3_witness.py
```

The verifier uses only the Python standard library.  It independently:

1. reconstructs the canonical \(W_{12}\) as the weight-six supports of the
   extended ternary Golay code;
2. verifies the \(S(5,6,12)\) property;
3. decodes the bitset in `k6_lambda3_witness.json` using the documented
   lexicographic order;
4. checks exact \(3\)-of-\(6\) incidence on all 792 deleted stars; and
5. checks the kernel, square-product, and non-mate local profiles.

The frozen bitset has SHA-256
`129aec20c13e7b1ab668576e169f21f25c202a0ca1af0f07d321267314f58669`.
It was discovered by an exact-cardinality SAT search, but verification does
not trust or invoke the solver.

## Scope

This witness proves only that the 144 Steiner-mate lines do **not** exhaust
the full \(k=6\) quadratic cone.  It does not classify that cone, construct
a five-dimensional totally constant-product subspace, or resolve
Erdős--Rosenfeld Problem #835.
