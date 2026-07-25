# The first overlap-sensitive \(2\)-adic lift of the triple tensor

This note continues `triple_polytabloid_tensor_support_audit.md`.  It
identifies the exact \(2\)-adic level at which the cubic contraction first
sees the overlap of two constituents.  At the first open parameter this is
the quotient after twenty-eight forced zero bits.

The resulting congruence is a genuine necessary condition on a disjoint
pair, but it is **not** a contradiction and does not solve
Erdős--Rosenfeld Problem 835.  Exact \(k=2\) and \(k=4\) controls show both
that the overlap term is real and that disjoint pairs can realize either
parity of the normalized quotient.

## Setup

Let \(k\) be even, put \(p=k+1\), and let
\(\mathcal F,\mathcal G\) be two \(S(k-1,k,2k)\)'s.  Write \(f,g\) for
their block indicators.  For oriented perfect matchings \(M,N,L\), use
the top polytabloids \(e_M\) and the tensor

\[
 T_{MNL}=\sum_{S\in\binom{[2k]}k}e_M(S)e_N(S)e_L(S).
\tag{1}
\]

Define

\[
\begin{aligned}
 \Delta_M(f)&=\langle e_M,f\rangle,&
 \Omega_M(f,g)&=\langle e_M,fg\rangle,\\
 d_M(f)&=\frac{\Delta_M(f)}2,&
 \omega_M(f,g)&=\frac{\Omega_M(f,g)}2,\qquad
 \tau_{MNL}=\frac{T_{MNL}}2.
\end{aligned}
\tag{2}
\]

All the quantities on the second line are integers.  Indeed, every block
of an \(S(k-1,k,2k)\) occurs together with its complement.  To see this,
fix a block \(B\).  Inclusion--exclusion gives the number of design blocks
disjoint from \(B\).  For \(i<k\), the number through a fixed \(i\)-set is

\[
 \lambda_i=\frac1p\binom{2k-i}{k-i},
\]

and

\[
 \sum_{i=0}^{k}(-1)^i\binom ki\binom{2k-i}{k-i}=1.
\tag{3}
\]

The last identity is the coefficient of \(x^k\) in

\[
 (1+x)^{2k}
 \left(1-\frac1{1+x}\right)^k=x^k(1+x)^k.
\]

Because \(k\) is even, inclusion--exclusion therefore gives one disjoint
block, necessarily \(B^c\).  Also
\(e_M(B^c)=(-1)^ke_M(B)=e_M(B)\), proving that both
\(\Delta_M(f)\) and \(\Omega_M(f,g)\) are even.  Finally, the support
theorem for (1) gives \(T_{MNL}\in2\mathbb Z\).

Put

\[
 s=v_2(k!),\qquad u=\frac{k!}{2^s}.
\tag{4}
\]

Thus \(u\) is odd.

## Exact threshold identity

Let \(E\) be the matrix whose rows are the \(e_N\)'s.  The exact frame
identity is

\[
 E^{\mathsf T}E=p!P_K.
\tag{5}
\]

Since \(f\) is an exact design,

\[
 E^{\mathsf T}Ef=k!(pf-\boldsymbol1),
\tag{6}
\]

and the same holds for \(g\).  Contracting their pointwise product against
\(e_M\) gives

\[
\begin{aligned}
 \sum_{N,L}\Delta_N(f)\Delta_L(g)T_{MNL}
 &=k!^2\langle e_M,(pf-\boldsymbol1)(pg-\boldsymbol1)\rangle\\
 &=p\,k!^2\bigl(p\Omega_M(f,g)
                 -\Delta_M(f)-\Delta_M(g)\bigr).
\end{aligned}
\tag{7}
\]

Substitute (2) and \(k!=2^su\) into (7).  After cancelling the termwise
factor \(8\), one obtains the exact integer identity

\[
\boxed{\displaystyle
 A_M(f,g):=
 \sum_{N,L}d_N(f)d_L(g)\tau_{MNL}
 =
 2^{\,2s-2}p u^2
 \bigl(p\omega_M(f,g)-d_M(f)-d_M(g)\bigr).}
\tag{8}
\]

This locates the first overlap-sensitive layer precisely:

* every pair of exact designs, disjoint or not, satisfies
  \(A_M(f,g)\equiv0\pmod {2^{2s-2}}\);
* after division by this forced power, the residue contains the signed
  overlap derivative \(\omega_M(f,g)\);
* for a block-disjoint pair, \(\omega_M(f,g)=0\), so (8) specializes to

\[
\boxed{\displaystyle
 \frac{A_M(f,g)}{2^{2s-2}}
 =-p u^2\bigl(d_M(f)+d_M(g)\bigr).}
\tag{9}
\]

Thus (9), unlike the lower vanishing congruences, really uses
constituent disjointness.

## The target \(k=16\)

Here

\[
 p=17,\qquad s=15,\qquad
 u=\frac{16!}{2^{15}}=638\,512\,875.
\]

Consequently every pair of hypothetical exact designs satisfies

\[
 A_M(f,g)\equiv0\pmod {2^{28}},
\tag{10}
\]

and

\[
 Q_M(f,g):=\frac{A_M(f,g)}{2^{28}}
 =17u^2\bigl(17\omega_M(f,g)-d_M(f)-d_M(g)\bigr).
\tag{11}
\]

In particular,

\[
 Q_M(f,g)\equiv
 \omega_M(f,g)+d_M(f)+d_M(g)\pmod2.
\tag{12}
\]

For two different constituents of a large set, (12) becomes

\[
\boxed{\displaystyle
 Q_M(f_a,f_b)\equiv
 \delta_M(a)+\delta_M(b)\pmod2,\qquad
 \delta_M(a)=d_M(f_a)\pmod2.}
\tag{13}
\]

The exact large-set colour matrix is also transparent.  Since
\(\omega_M(f_a,f_a)=d_M(f_a)\),

\[
\begin{aligned}
 Q_M(f_a,f_a)&=17u^2\cdot15\,d_M(f_a),\\
 Q_M(f_a,f_b)&=-17u^2\bigl(d_M(f_a)+d_M(f_b)\bigr)
 \quad(a\ne b).
\end{aligned}
\tag{14}
\]

Its rows sum to zero, as they must because
\(\sum_a d_M(f_a)=0\).  Modulo two, if
\(\delta=(\delta_M(a))_a\), the matrix in (14) is

\[
 \operatorname{diag}(\delta)
 +\delta\boldsymbol1^{\mathsf T}
 +\boldsymbol1\delta^{\mathsf T}.
\tag{15}
\]

In particular it kills \(\boldsymbol1\), and every triangle of distinct
colours obeys

\[
 Q_M(f_a,f_b)+Q_M(f_a,f_c)+Q_M(f_b,f_c)=0
 \pmod2.
\tag{16}
\]

These conditions are internally consistent.  They yield no parity,
rank, or row-sum contradiction at \(p=17\).  Since every odd square is
one modulo eight, (14) even gives the compatible stronger residues

\[
 Q_M(f_a,f_a)\equiv-d_M(f_a),\qquad
 Q_M(f_a,f_b)\equiv-d_M(f_a)-d_M(f_b)\pmod8.
\tag{17}
\]

## Exact controls and the dead end

The companion verifier evaluates (1) directly with signed-support
bitsets and exhausts the following controls.

* At \(k=2\), the three \(S(1,2,4)\)'s form the true large set.
  All eighteen ordered-disjoint-pair/matching instances satisfy (9).
  Twelve normalized quotients are odd and six are even.
* At \(k=4\), all thirty labelled \(S(3,4,8)\)'s are enumerated.
  Each has eight disjoint mates, giving 240 ordered disjoint pairs and
  \(240\cdot105=25\,200\) pair/matching instances.  Every instance
  satisfies (9).  Their normalized quotients include 13,440 odd and
  11,760 even values.
* Among the 69,300 overlapping-pair/matching instances at \(k=4\),
  \(\omega_M(f,g)\) is odd in 21,840.  In every case the difference
  between the normalized right side of (8) and the falsely imposed
  disjoint formula (9) is exactly \(p^2u^2\omega_M(f,g)\).  Thus the
  threshold really does detect overlap; it is not another identity of
  each design separately.

The \(k=4\) disjoint controls rule out an extra universal factor of two:
both parities in (13) genuinely occur.  They also show the limitation.
Pairwise threshold compatibility does not assemble a large set:
the disjointness graph of the thirty \(S(3,4,8)\)'s is triangle-free,
so its clique number is only two rather than the required five.

At \(k=16\), equations (10)--(17) are therefore exact new bookkeeping,
but the tensor support theorem alone supplies no contradiction.  A
successful continuation would have to constrain the normalized quotient
\(Q_M\) simultaneously across matchings in some way not already encoded
by (8), rather than merely ask for one more scalar power of two.

Run

```bash
python3 -B evidence/verify_triple_tensor_2adic_threshold.py
```

for the independent exhaustive controls and the target arithmetic.
