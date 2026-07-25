# The rank-two near-link is impossible over \(\mathbb F_{19}\)

This note closes one unrestricted-looking but ultimately rank-two route to a
rank-four ordered link.  It does **not** exclude an arbitrary rank-four
ordered link and does not by itself solve Erdős--Rosenfeld Problem #835.

## Near-link hypothesis

Let \(v_0,\ldots,v_{18}\in\mathbb F_{19}^2\).  For \(i<j\), put
\[
 C_{ij}=C_{ji}=\det(v_i,v_j).
\]
Thus, when \(j<i\), the displayed row entry is
\(C_{ij}=\det(v_j,v_i)=-\det(v_i,v_j)\).  This ordering sign disappears in
all the even-power identities below.
Suppose the eighteen labels in every row of \(C\) are distinct.  Write
\(m_i\) for the unique field element missing from row \(i\).

This would lift immediately to a rank-at-most-four ordered link on twenty
vertices.  Indeed, if \(v_i=(a_i,c_i)\), take
\[
 U_i=(a_i,m_i,c_i,0),\qquad U_{19}=(0,0,0,1)
\]
and use
\[
 \langle x,y\rangle=x_0y_2-x_2y_0+x_1y_3-x_3y_1.
\]
Then \(\langle U_i,U_j\rangle=\det(v_i,v_j)\) for \(i<j<19\), while
\(\langle U_i,U_{19}\rangle=m_i\).

We prove that the near-link hypothesis is impossible.

## The missing labels and zero pairs

Each colour class is a matching in \(K_{19}\), since a colour cannot occur
twice at one vertex.  It therefore has at most nine edges.  The nineteen
colour classes contain
\[
 \binom{19}{2}=19\cdot 9
\]
edges in total, so every colour class has exactly nine edges.  Consequently
the missing labels \(m_i\) are all distinct and hence run through
\(\mathbb F_{19}\).

In particular, determinant zero gives nine parallel pairs and one singleton.
The singleton is precisely the vertex whose missing label is zero.

## The quadratic moment has rank one

For even \(k\in\{2,4,\ldots,16\}\), define the homogeneous moment form
\[
 M_k(x)=\sum_{j=0}^{18}\det(x,v_j)^k.
\]
Since
\(\sum_{z\in\mathbb F_{19}}z^k=0\) for \(1\leq k<18\), the row condition
gives
\[
 M_k(v_i)=-m_i^k. \tag{1}
\]

Set \(Q=M_2\).  The singleton is a nonzero isotropic vector of \(Q\), so if
\(Q\) had rank two it would be split.  Choose coordinates in which the
singleton lies on one axis and
\[
 Q(x,y)=\kappa xy,\qquad \kappa\ne0.
\]
The other isotropic direction is unused.  Write every paired vector as
\(\alpha(t,1)\).  Equation (1) gives
\[
 \alpha^2\kappa t=-m^2.
\]
Summing over the eighteen paired endpoints,
\[
 \sum \alpha^2t
 =-\kappa^{-1}\sum_{m\in\mathbb F_{19}^{\times}}m^2=0. \tag{2}
\]
But the \(xy\)-coefficient in the defining expression
\(Q(x,y)=\sum_j\det((x,y),v_j)^2\) is
\(-2\sum\alpha^2t\), because the singleton contributes only a square term.
Equation (2) says this coefficient is zero, contradicting \(\kappa\ne0\).

The form \(Q\) is not zero because (1) is nonzero at every paired endpoint.
Therefore \(Q\) has rank exactly one.

## Normal form and the four even-moment systems

Apply an invertible linear change of coordinates so that the singleton is
\((1,0)\).  It only multiplies all displayed labels by one common nonzero
field element, preserving the near-link property.  The rank-one conclusion
now gives
\[
 Q(x,y)=\kappa y^2.
\]
Write the nine paired projective directions as
\[
 (t_g,1),\qquad t_g\in\mathbb F_{19}\ \text{distinct},
\quad g=1,\ldots,9.
\]
If an endpoint in direction \(g\) is \(\alpha(t_g,1)\), then (1) for
\(k=2\) says
\[
 m^2=-\kappa\alpha^2.
\]
Thus \(-\kappa=\rho^2\) for some \(\rho\ne0\), and
\(m=\pm\rho\alpha\).

For \(k=2,4,6,8\), equation (1) implies
\[
 M_k(t_g,1)=-\rho^k
\]
at all nine distinct \(t_g\).  The polynomial
\(M_k(t,1)+\rho^k\) has degree at most \(k<9\), so it vanishes identically:
\[
 M_k(x,y)=-\rho^k y^k. \tag{3}
\]

Modulo sign, the eighteen nonzero missing labels consist of two copies of
each class \(1,\ldots,9\).  If the endpoints in direction \(g\) receive
classes \(a_g,b_g\), define
\[
 S_k(g)=a_g^k+b_g^k.
\]
Put \(r=\rho^2\), a nonzero square.  Comparing coefficients in (3) gives,
for \(k=2,4,6,8\),
\[
 \sum_{g=1}^9 S_k(g)t_g^\ell=0
 \quad(0\leq\ell<k), \tag{4}
\]
and
\[
 \sum_{g=1}^9 S_k(g)t_g^k
 =-r^{k/2}-r^k. \tag{5}
\]

Explicitly, the coefficient comparison uses
\[
 M_k(x,y)
 =y^k+\rho^{-k}\sum_{g=1}^9
 S_k(g)(x-t_gy)^k.
\]
The first term is the singleton's contribution, and
\(\alpha^k=m^k/\rho^k\) for either endpoint of a paired direction.
Multiplying (3) by \(\rho^k\) and comparing
\(x^{k-\ell}y^\ell\) gives (4); the coefficient of \(y^k\) gives (5).

For \(k=8\), let
\[
 P(X)=\prod_{g=1}^9(X-t_g),\qquad
 D=-r^4-r^8.
\]
The first eight equations in (4), together with the standard barycentric
identity, force
\[
 S_8(g)=\frac{D}{P'(t_g)}. \tag{6}
\]

## Complete finite check

The dependency-free verifier
[`p19_near_link_even_moment_filter.cpp`](p19_near_link_even_moment_filter.cpp)
exhausts:

1. all \(\binom{19}{9}=92{,}378\) choices of the nine slopes;
2. all nine possible nonzero squares \(r\);
3. every pairing of the multiset containing two copies of
   \(1,\ldots,9\);
4. equations (4), (5), and (6) for \(k=2,4,6,8\).

It visits \(67{,}231{,}205\) pairing-search nodes and finds zero survivors.
No symmetry quotient is used for the survivor count.

Run:

```bash
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  evidence/p19_near_link_even_moment_filter.cpp \
  -o /tmp/p19_near_link_even_moment_filter
/tmp/p19_near_link_even_moment_filter
```

Expected final output:

```text
p7_near_link_control=PASS
all_slope_sets=92378
affine_orbit_representatives=280
pair_assignment_nodes=67231205
even_moment_survivors=0
```

The \(p=7\) line is a positive control: the verifier first checks an explicit
seven-vector near-link, including its distinct-row property, permutation of
missing labels, and nonzero rank-one quadratic moment.  The affine-orbit count
is only a consistency statistic; all \(92{,}378\) slope sets are processed.

Hence no rank-two near-link exists over \(\mathbb F_{19}\), and the proposed
one-radical-coordinate lift cannot produce the desired rank-four ordered
link.
