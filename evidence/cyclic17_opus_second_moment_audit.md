# Audit of the proposed Opus second-moment identity

This note concerns only the fixed-Wallis, \(C_{17}\)-equivariant
radius-five quotient.  It is not a solution or obstruction for the full
Erdős–Rosenfeld problem.

Choose the unique representative of each moving-triple orbit whose point
sum is zero.  Write \(z_{i,d}\) for the cyclic position of the zero edge of
difference \(d\in\{1,\ldots,8\}\) in Wallis square \(i\).  If a triple edge
has cyclic coordinate \((d,p)\), its forbidden phase is
\[
 f=z_{i,d}-p.
\]

Across the 40 normalized representatives, difference \(d\) occurs 15 times,
the corresponding positions sum to \(d\) in \(\mathbb F_{17}\), and the sum
of all position squares is zero.  Hence
\[
 \Phi_i^{(2)}
 =\sum_q\sum_{f\in F_i(q)}f^2
 =-2\sum_{d=1}^8(z_{i,d}^2+d z_{i,d}).
\]

Let \(a_{i,d}=-z_{i,d}\) be the first half of the cyclic starter.  Symmetry
gives \(a_{i,17-d}=a_{i,d}-d\), and the full starter is a permutation of
\(\mathbb F_{17}\).  Comparing its second moment with that of the field gives
\[
 0=\sum_{d=1}^8\left(a_{i,d}^2+(a_{i,d}-d)^2\right)
   =2\sum_d a_{i,d}^2-2\sum_d d a_{i,d},
\]
because \(\sum_{d=1}^8d^2=0\).  Therefore
\[
 \Phi_i^{(2)}
 =2\left(\sum_d d a_{i,d}-\sum_d a_{i,d}^2\right)=0
\]
for every square \(i\).

The only natural \(i\)-indexed scalar supplied by this expansion is the
zero-factor first moment
\[
 s_i=\sum_{d=1}^8z_{i,d}
\]
(or its sign-reversed starter convention).  The starter's first-moment
identity forces \(\sum_d a_{i,d}=1\), so \(s_i=-1\) for every \(i\).
Thus
\[
 \Phi_i^{(2)}-\Phi_j^{(2)}
   +5(s_i^2-s_j^2)=0
\]
is valid under that interpretation but is just \(0=0\); the coefficient
\(5\) is immaterial.  If \(s_i\) is instead intended to be the varying
Wallis label \(a_{i,1}\), the formula is false for 98 of the 105 square
pairs.  With \(s_i\) left undefined, the claim has no independent
mathematical content.

The executable check is
`evidence/audit_cyclic17_opus_second_moment.py`.
