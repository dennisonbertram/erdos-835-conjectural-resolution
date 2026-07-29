# The quadratic core of the pure-mate conjecture

Status: **proved reduction; not a proof of the pure-mate conjecture.**

This note separates the one quadratic consequence needed for the proposed
Erdos--Rosenfeld obstruction from the much stronger pure-spin conclusion.
It applies to the endpoint system in `nonlinear_spin_mates.md`.

Let
\(A,B,C\) be \(S(r-1,r,2r+1)\)'s with \(A\cap B=A\cap C=\varnothing\),
write \(b=|B|=|C|\), and put
\[
 u=x_B+x_C\in\mathbb F_2^{\binom{2r+1}r}.
\]
The addition in this definition is mod 2.  Since both endpoint words have
the same facet degrees, \(u\in C=\ker(W_{r-1,r})\pmod2\), so its class in
the basic-spin quotient is defined.

## Proposition (exact quadratic identity)

\[
 q_S([u])
 =\frac{\operatorname{wt}(u)}2
 =b-|B\cap C|\pmod2.
\tag{1}
\]
Equivalently, the condition \(q_S([u])=0\) is the single Boolean
quadratic equation
\[
 \boxed{\quad\sum_K (x_B)_K(x_C)_K=b\pmod2.\quad}
\tag{2}
\]

### Proof

The symmetric difference of two block sets has size
\[
 \operatorname{wt}(u)=|B\triangle C|=2b-2|B\cap C|.
\]
The coordinate quadratic form on the even binary trade code is
\(q_S([z])=\operatorname{wt}(z)/2\pmod2\); it descends through the radical.
Substitution gives (1).  Since
\(\sum_K(x_B)_K(x_C)_K=|B\cap C|\), (2) is the same statement. \(\square\)

## Consequence for the pure-mate route

The Clifford calculation gives
\[
 [u]=0\ \text{or}\ [u]\ \text{pure}\quad\Longrightarrow\quad q_S([u])=0.
\tag{3}
\]
Thus the pure-mate conjecture contains (2) as its first necessary
consequence.  At \(r=15\),
\[
 b=17\,678\,835\equiv1\pmod2,
\]
so (2) says exactly that every two mates of the same base have odd block
intersection.  In particular they cannot be block-disjoint.  This would
exclude three pairwise block-disjoint \(S(14,15,31)\)'s and hence rule out
the required large set.

Equation (2) is strictly weaker than purity.  In the complete \(r=3\)
audit there are singular non-pure spinors (annihilator dimension 2), while
only 30 of the 135 nonzero singular spinors are pure.  Hence proving (2)
would settle the relevant parity obstruction but would not, by itself,
prove the advertised pure-mate conjecture.

The explicit shaped \(r=3\) witness in `nonlinear_spin_mates.md` has all
linear trade and sphere-shape properties, has \(q_S=0\), and is nevertheless
non-pure.  It therefore refutes deriving the **full** pure conclusion from
those linear properties, but it does not refute the weaker equation (2).
No derivation of (2) from the simultaneous Boolean exact-degree endpoint
conditions is supplied here; nor is an ideal-membership derivation of all
Wick quadrics.
