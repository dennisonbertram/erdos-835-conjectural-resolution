# A dense-support packing lemma at the order-18 first lift

Date: 2026-07-27.

## Setting

Let \(A\) be the thirteen vertices of the uncoloured hole and let
\(V_c\subseteq A\) be the support still unmatched in colour \(c\).  In the
order-\(18\) first-lift problem every support has size \(8\), \(10\), or
\(12\).  A completion requires a perfect matching on each \(V_c\), with all
seventeen matchings pairwise edge-disjoint.

The following lemma gives a uniform, solver-free piece of that packing
problem.

> **Dense-support prefix lemma.**  Let
> \(V_1,\ldots,V_r\) be even subsets of the vertex set of a complete graph.
> If
> \[
>     |V_i|\geq 2i\qquad(1\leq i\leq r),
> \tag{1}
> \]
> then there are pairwise edge-disjoint perfect matchings
> \(M_i\subseteq E(K[V_i])\).

### Proof

Choose the matchings in the displayed order.  Suppose
\(M_1,\ldots,M_{i-1}\) have already been chosen and put
\[
 G_i=K[V_i]-\bigcup_{j<i}M_j .
\]
Each earlier matching deletes at most one edge incident with any fixed
vertex.  Consequently
\[
 \delta(G_i)\ \geq\ |V_i|-1-(i-1)
                 \ =\ |V_i|-i
                 \ \geq\ |V_i|/2,
\]
where the final inequality is (1).  Dirac's theorem gives a Hamilton cycle
in \(G_i\) when \(|V_i|\geq4\).  Since \(|V_i|\) is even, alternate edges
of that cycle form a perfect matching \(M_i\).  The only smaller case allowed
by (1) is \(i=1\) and \(|V_1|=2\); then \(K[V_1]\) itself is the required
single-edge matching.  Induction completes the proof. \(\square\)

## Exact order-18 consequences

After ordering a selected subfamily by nondecreasing support size, condition
(1) immediately gives:

1. every subfamily of at most four target colours can be packed;
2. every five-colour subfamily containing a colour of support at least ten
   can be packed;
3. every six-colour subfamily whose largest support is twelve and whose
   second-largest support is at least ten can be packed.

The possible complete support profiles are
\[
 (n_8,n_{10},n_{12})=(7+q,\ 10-2q,\ q),
 \qquad 0\leq q\leq5.
\tag{2}
\]
Thus every target instance has a packable five-colour prefix.  Every profile
with \(q\geq1\) has a packable six-colour prefix as well.  Explicitly, for
\(0\leq q\leq4\), four support-eight colours followed by one support-ten
colour give a five-prefix; for \(q=5\), use four support-eight colours and
one support-twelve colour.  For \(1\leq q\leq4\), append a support-twelve
colour to the former choice to get a six-prefix.  For \(q=5\), use four
support-eight colours followed by two support-twelve colours.

This rules out any target analogue of the order-\(12\) obstruction in which
two small supports force the same edge: in fact, any four target supports
can be matched simultaneously.  It does **not** complete all seventeen
colours.  The remaining difficulty is global compatibility after the dense
prefix, so neither the first-lift theorem nor Erdős--Rosenfeld Problem #835
is claimed solved here.

## Reproducible arithmetic check

Run

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_dense_support_prefix/verify_prefix_criteria.py
```

The script exhaustively checks the support-profile formula (2) and the
finite numerical consequences of condition (1).  The mathematical content
of the lemma itself is the proof above.
