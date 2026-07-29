# Fixed-rung large sets exist asymptotically

Date of independent literature correction: 2026-07-29.

## Theorem

Fix \(t\ge1\).  There is a constant \(P_t\) such that, for every prime
\(p>P_t\),

\[
LS(t,t+1,t+p)
\]

exists.

Consequently, for

\[
\tau(p)=\max\{s:LS(s,s+1,s+p)\text{ exists}\},
\]

one has \(\tau(p)\to\infty\) along the primes.  In particular, no absolute
upper bound such as \(\tau(p)\le3\) can be true, and no fixed rung \(t=3\),
\(t=4\), or any other constant \(t\) can give a nonexistence obstruction for
all sufficiently large primes.

## Proof

Use Keevash's large-set existence theorem, Theorem 1.2 of
["The existence of designs II"](https://arxiv.org/abs/1802.05900).
In that theorem take

\[
q=t+1,\qquad r=t,\qquad \lambda=1,\qquad n=t+p.
\]

Here \(q,r,\lambda\) are fixed while \(p\), hence \(n\), tends to infinity.
The theorem requires

\[
\lambda\mid \binom{n-r}{q-r}
\quad\text{and}\quad
\binom{q-i}{r-i}\mid
\lambda\binom{n-i}{r-i}
\qquad(0\le i\le r).
\tag{1}
\]

The first condition is automatic because \(\lambda=1\).  For the second,
put \(m=t+1-i\), so \(1\le m\le t+1\).  It becomes

\[
m\mid \binom{p+m-1}{m-1}.
\tag{2}
\]

For a prime \(p>t+1\), the identity

\[
\frac1m\binom{p+m-1}{m-1}
=\frac1p\binom{p+m-1}{m}
\tag{3}
\]

shows (2): the numerator of \(\binom{p+m-1}{m}\) contains the factor \(p\),
while none of \(1,\ldots,m\) is divisible by \(p\), so that binomial
coefficient is divisible by \(p\).

Thus all divisibility conditions (1) hold for every prime \(p>t+1\).
Keevash's theorem supplies the required large set once
\(n=t+p>n_0(t+1,t)\).  Taking
\(P_t>\max(t+1,n_0(t+1,t)-t)\) proves the first claim.

For every fixed \(T\), applying the first claim with \(t=T\) gives
\(\tau(p)\ge T\) for all sufficiently large primes \(p\).  This is exactly
\(\tau(p)\to\infty\) along the primes.  \(\square\)

## Scope for #835

This does **not** construct the top rung
\(LS(p-2,p-1,2p-2)\), because Keevash's threshold holds with \(t\) and
\(t+1\) fixed, whereas #835 makes them grow linearly with \(p\).

It does close a proposed negative strategy.  A universal contradiction at
the fixed rung \(LS(3,4,p+3)\) or \(LS(4,5,p+4)\) is impossible: those large
sets exist for every sufficiently large prime.  A negative solution of #835
must force a failing rung \(t=t(p)\) that tends to infinity with \(p\), or
work directly at the growing top of the tower.

For Steiner quadruple systems this distinction is recorded explicitly by
Etzion and Zhou,
["An improved Recursive Construction for Disjoint Steiner Quadruple
Systems"](https://arxiv.org/abs/1912.04489): no explicit nontrivial large set
was known, but Keevash proves nonconstructive existence for all sufficiently
large admissible orders.
