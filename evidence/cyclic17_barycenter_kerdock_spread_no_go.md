# A cyclic-17 barycentre ansatz fails

This is an exact exclusion of one natural positive construction for
Erdos--Rosenfeld Problem #835 at \(k=16\).  It is **not** a nonexistence
proof for an arbitrary colouring.

The identity \(17=2^4+1\) suggests taking the colours to be
\(\mathbb P^1(\mathbb F_{16})\), and using a cyclic subgroup of order
\(17\) on them.  The simplest corresponding 32-point model has a moving
17-orbit and a fixed 15-set:
\[
 X=C\sqcup Y,\qquad C=\mathbb F_{17},\quad |Y|=15.
\]
Translation acts on \(C\), fixes \(Y\), and translates the proposed colour.
Since a 16-subset contains at least one point of \(C\), its cyclic part is
never empty.

## The ansatz

For every \(r=1,\ldots,16\) and \((16-r)\)-subset \(H\subseteq Y\), choose
an arbitrary offset \(f_r(H)\in\mathbb F_{17}\).  For
\(A\subseteq C\), \(|A|=r\), define
\[
 c(A\cup H)=\frac{1}{r}\sum_{a\in A}a+f_r(H).
 \tag{1}
\]
This is more flexible than a point-additive rule: its offset may depend on
the entire selected subset of the fixed layer.  It is exactly equivariant
for the cyclic translation on the 17 moving points.

## Theorem

No choice of the offsets in (1) is a proper 17-colouring of \(J(32,16)\).

## Proof

Let \(T=A\cup H\) be a 15-set, with \(|A|=t\) and
\(|H|=15-t\).  Write \(s=\sum_{a\in A}a\).  The colours of the
extensions by the points \(x\in C\setminus A\) are
\[
 \frac{s+x}{t+1}+f_{t+1}(H).
 \tag{2}
\]
They are distinct.  Their missing \(t\) colours, namely the values that
would have resulted from the excluded \(a\in A\), are
\[
 f_{t+1}(H)+\frac{a-s/t}{t+1}\qquad(a\in A).
 \tag{3}
\]
The remaining \(t\) extensions are by the points \(y\in Y\setminus H\),
and have colours
\[
 \frac{s}{t}+f_t(H\cup\{y\}).
 \tag{4}
\]
For the star to be rainbow, (3) and (4) must agree as sets.  Hence
\[
 \bigl\{f_t(H\cup\{y\}):y\in Y\setminus H\bigr\}
 = f_{t+1}(H)+
 \left\{\frac{a-s/t}{t+1}:a\in A\right\}.
 \tag{5}
\]
The left-hand side is independent of the particular \(t\)-set \(A\).

Now take \(t=2\), and fix any 13-subset \(H\subset Y\).  For
\(A=\{0,d\}\), equation (5) says that the same two-element set on the
left must equal
\[
 f_3(H)+\left\{-\frac d6,\frac d6\right\}. \tag{6}
\]
Taking \(d=1\) and \(d=2\) gives two different sets in \(\mathbb F_{17}\):
\(\{\pm1/6\}\ne\{\pm2/6\}\).  This is a contradiction. \(\square\)

## Relation to Kerdock and spread proposals

Equation (1) is the natural ``one moving projective line plus a fixed
layer'' version of a spread/Kerdock construction: the order-17 colour
cycle is retained, while the 15 stationary coordinates may influence the
colour arbitrarily.  The theorem shows that the barycentric part cannot
be repaired merely by adding a fixed-layer Kerdock, bent-function, or
Reed--Muller signature.  A successful order-17-equivariant construction
would need the correction to depend essentially on the *shape* of the
selected cyclic subset \(A\), not only on its mean.

Run

```bash
python3 -B evidence/verify_cyclic17_barycenter_kerdock_spread_no_go.py
```

to check the finite-field identities and the explicit \(d=1,2\)
contradiction.
