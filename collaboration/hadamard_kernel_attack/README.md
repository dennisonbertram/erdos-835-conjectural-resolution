# Deleted-colour Hadamard kernels

Date: 2026-07-26.

## Status

This note proves a new unrestricted **necessary condition** for a tight
prime colouring and verifies that its quadratic relaxation:

* passes the true \(k=2\) control;
* already rejects the false \(k=4\) control; and
* rejects every design-valued pair in the false \(k=6\) control.

It does **not** prove the condition impossible at \(k=16\), construct a
colouring, or resolve Erdős--Rosenfeld Problem #835.

The exact verifier is
`collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py`.
It uses only integer arithmetic modulo the relevant prime and the
repository's deterministic Algorithm X implementation.

## 1. The exact finite-field formulation

Let \(k\ge2\), let \(p=k+1\) be prime (so \(p\ge3\)), and let
\[
 X=\binom{[2k]}k,\qquad
 Y=\binom{[2k]}{k-1},\qquad
 W=W_{k-1,k}(2k),
\]
and suppose that \(g:X\to\mathbb F_p\) is a tight colouring.  Every
\((k-1)\)-star contains each field value exactly once.  Therefore
\[
 W(g^{\circ m})=0\quad(1\le m\le p-2),\qquad
 W(g^{\circ(p-1)})=-\mathbf1.                    \tag{1}
\]
Conversely, (1), together with \(g(X)\subseteq\mathbb F_p\), forces every
star to be a permutation.  Newton's identities first give
\(e_1=\cdots=e_{p-2}=0\) and \(e_{p-1}=-1\).  The star polynomial is
therefore \(T^p-T-e_p\).  Since each of its roots lies in \(\mathbb F_p\),
\(e_p=0\), so it is \(T^p-T\).

Fix the zero class
\[
 D=g^{-1}(0).
\]
It is an \(S(k-1,k,2k)\).  Delete its columns and put
\[
 M_D=W[:,X\setminus D].
\]
For \(x,y\in\mathbb F_p^{X\setminus D}\), define the vector-valued
Hadamard form
\[
 \Phi_D(x,y)
 =M_D(x\circ y)\pmod{\langle\mathbf1\rangle}.     \tag{2}
\]

### Deleted-colour Hadamard-kernel theorem

If \(D\) extends to a tight \(p\)-colouring, then there is a subspace
\[
 U\le\ker M_D,\qquad \dim U=p-2,                  \tag{3}
\]
such that
\[
 \Phi_D(U,U)=0.                                   \tag{4}
\]
Moreover the scalar form \(b\) defined by
\[
 M_D(x\circ y)=b(x,y)\mathbf1\qquad(x,y\in U)     \tag{5}
\]
is nondegenerate.

**Proof.**  On \(X\setminus D\), put
\[
 u_r=g^{\circ r},\qquad 1\le r\le p-2.
\]
The functions \(z,z^2,\ldots,z^{p-2}\) are linearly independent on
\(\mathbb F_p^\*\), so the \(u_r\)'s are independent.  Equation (1) gives
\(U=\langle u_1,\ldots,u_{p-2}\rangle\le\ker M_D\).

For basis elements,
\[
 M_D(u_r\circ u_s)
 =
 \begin{cases}
 -\mathbf1,&r+s=p-1,\\
 0,&r+s\ne p-1.
 \end{cases}                                      \tag{6}
\]
When \(r+s>p-1\), reduce the exponent modulo \(p-1\) on
\(\mathbb F_p^\*\); the resulting exponent is between \(1\) and \(p-3\).
Thus (4) holds and the matrix of \(b\) is the anti-diagonal matrix with
entries \(-1\), hence is nondegenerate. \(\square\)

This uses all colours simultaneously: a single Steiner system does not
supply \(U\).  It is also stronger than a rank test on \(\ker M_D\);
the required subspace must be totally singular for the whole
vector-valued quadratic system (2), with a nondegenerate surviving scalar
form.

## 2. Local simplex interpretation

For a row \(B\in Y\), restrict functions in \(U\) to the \(p-1\) blocks
of the deleted star.  The restriction map
\[
 \rho_B:U\longrightarrow
 H_0=\{(z_1,\ldots,z_{p-1}):\textstyle\sum z_i=0\}
\]
is an isomorphism: both spaces have dimension \(p-2\), and (5) is
nondegenerate.  Relative to \(b^{-1}\), the \(p-1\) evaluation vectors
in every deleted star have Gram matrix
\[
 I+J:
 \qquad \langle v_i,v_i\rangle=2,\quad
 \langle v_i,v_j\rangle=1\ (i\ne j).              \tag{7}
\]
Thus the quadratic condition asks for one globally coherent
\((p-2)\)-dimensional orthogonal simplex frame on every deleted star.
This is a finite-field, low-rank Gram-completion obstruction.

There is an exact higher-degree endpoint.  A fixed \(D\) extends to a
tight colouring if and only if one can choose a space \(U\) as in (3),
with one (hence every) \(\rho_B\) injective, such that for every
\(x\in U\)
\[
 M_D(x^{\circ r})\in\langle\mathbf1\rangle
 \qquad(2\le r\le p-1).                            \tag{8}
\]
The forward implication is the same power calculation.  Conversely,
choose \(x\in U\) whose values on one deleted star are the elements of
\mathbb F_p^\*\).  Newton's identities applied to (8) show that every
deleted star has the same multiset of values.  Adding the unique
\(D\)-block of value zero gives a tight colouring.  Hence degree two is
a genuine relaxation, while the complete degree-\((p-1)\) hierarchy is
equivalent to the original extension problem.

The same theorem applies verbatim to any derived large set with \(p\)
blocks in every row.  In particular, a hypothetical \(k=16\) colouring
would give this \(15\)-dimensional quadratic space after fixing one member
of any derived \(LS(4,5,21)\) or \(LS(3,4,20)\).

## 3. Exact controls

Run

```bash
python3 -B collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py
```

The recorded output is

```text
k=2, p=3: |D|=2, deleted square=4, kernel=1, isotropic lines=1 (all 2 disjoint mates), max totally-constant-product dimension=1
k=4, p=5: |D|=14, deleted square=56, kernel=7, isotropic lines=8 (all 8 disjoint mates), max totally-constant-product dimension=1
ALL DELETED-COLOUR HADAMARD-KERNEL CHECKS PASSED
```

At \(k=2\), the required dimension is \(p-2=1\), so the true
one-factorisation passes.

At \(k=4\), the verifier constructs a labelled \(S(3,4,8)\), forms its
exact \(56\)-by-\(56\) deleted incidence matrix over \(\mathbb F_5\),
and enumerates all
\[
 \frac{5^7-1}{5-1}=19\,531
\]
projective lines in its seven-dimensional kernel.  Exactly eight lines
satisfy
\[
 M_D(x\circ x)\in\langle\mathbf1\rangle.          \tag{9}
\]
They are exactly the lines represented by
\[
 h_C=\mathbf1+\mathbf1_C
\]
for the eight Steiner systems \(C\) disjoint from \(D\).  No two distinct
lines satisfy the mixed condition
\[
 M_D(x\circ y)\in\langle\mathbf1\rangle.          \tag{10}
\]
Consequently the largest totally constant-product subspace has dimension
one, whereas a tight five-colouring would require dimension three.  This
is an exact quadratic obstruction, not an LP relaxation.

The stronger control

```bash
python3 -B collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py --k6
```

also reconstructs all 144 Witt mates.  The completeness of the extension
step is elementary but important.  In any \(S(5,6,12)\), fix a block \(B\)
and let \(n_i\) count the other blocks meeting it in \(i\) points.  No
intersection of size at least five is possible.  Double-counting the
\(s\)-subsets of \(B\) in other blocks gives
\[
 \sum_{i=s}^4\binom{i}{s}n_i
 =\binom6s(\lambda_s-1),\qquad
 (\lambda_0,\ldots,\lambda_4)=(132,66,30,12,4).
\]
Back-substitution yields
\[
 (n_0,n_1,n_2,n_3,n_4)=(1,0,45,40,45).
\]
Thus every block has exactly one disjoint block, necessarily its complement,
so every \(S(5,6,12)\) is complement-closed and is uniquely determined by
its derivation at one point.  Disjoint top systems are consequently in
bijection with disjoint derived \(S(4,5,11)\) systems.  The verifier's 144
boundary mates therefore exhaust the whole top Steiner-mate sector.

Their top extensions give 144 design-valued isotropic lines.  Every pair is
mixed-product incompatible:
the two systems meet in 12 or 36 blocks, so
\[
 M_D(h_C\circ h_E)
 =\mathbf1+M_D\mathbf1_{C\cap E}
\]
is nonconstant.  This exhausts the idempotent/Steiner-mate sector at
\(k=6\), but **not** every projective isotropic line in the much larger
quadratic kernel.  Therefore the full quadratic \(k=6\) relaxation is
not claimed infeasible.

## 4. Target at \(p=17\)

For the original \(k=16\) layer, a fixed zero system \(D\) would give
\[
 M_D\in\mathbb F_{17}^{565\,722\,720\times565\,722\,720}.
\]
The theorem requires a \(15\)-dimensional \(U\le\ker M_D\) on which
\(\Phi_D\) vanishes and whose scalar Gram matrix is the nondegenerate
anti-diagonal matrix from (6).

Thus either of the following would be decisive:

1. prove uniformly that every possible \(S(15,16,32)\) zero class has
   quadratic Witt capacity below \(15\); or
2. prove the analogous statement for every possible member of the much
   smaller necessary \(LS(4,5,21)\) layer.

Neither theorem is proved here.  The result is useful because its degree-two
relaxation already separates the true \(k=2\) and false \(k=4\) controls;
the previously audited pointwise moment and low-order scalar trace
relaxations did not.

## 5. Numerical cubic calibration (non-proof)

During this attack the previously unexecuted projected-cubic decision
script was run once with the exact command

```bash
python3 -B collaboration/fable_frontier/decide_cubic_embedding_k4.py --restarts 12 --maxiter 500 --seed 20260726
```

It reported:

```text
k=2 exact sanity relative residual: 2.104e-31
k=2 optimized best relative residual: 9.788171e-25
k=4 best absolute residual: 4.771063e+02
k=4 best relative residual: 2.839919e-02
```

All twelve \(k=4\) restarts stayed far above the known-feasible \(k=2\)
scale.  This is attack-selection evidence that the characteristic-zero
projected cubic may also detect \(k=4\); it is **not** an infeasibility
proof and is not used in the theorem above.

The script has a hard-coded output path and accidentally overwrote its
pre-existing tracked NPZ while saving the numerical iterate.  That binary
is deliberately not copied into this directory and is not evidence for
any claim here; the parent task is restoring the original tracked blob.

## 6. Reproducibility boundary

The verifier proves the finite \(k=2\) and \(k=4\) statements by complete
projective enumeration and the stated \(k=6\) design-sector statement by
complete exact-cover enumeration.  It does not search at \(p=17\), assume
symmetry of a colouring, or use the five-point LP relaxation.
