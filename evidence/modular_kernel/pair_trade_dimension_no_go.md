# Pair-trade dimension no-go at \(r=15\)

## Theorem

Assume two block-disjoint \(S(14,15,31)\) systems exist.  Let \(U\) be
the set of 15-subsets outside their two block sets, let \(A\) be the
14-subset-by-\(U\) inclusion matrix over \(\mathbb F_2\), and put
\[
C=\ker A.
\]
Then
\[
\dim C\ge119\,759\,850,\qquad
\dim\operatorname{rad}(C)\le35\,357\,670.
\]
In particular, \(C\) is neither self-orthogonal nor doubly even.

## Proof

Let \(W\) be the inclusion matrix with all 15-subsets as columns and
write
\[
W=[\,A\ R\,],
\]
where \(R\) consists of the columns in the two deleted Steiner systems.
With
\[
b=\frac{\binom{31}{15}}{17}=17\,678\,835
\]
blocks in one system, \(R\) has \(2b=35\,357\,670\) columns and
\[
|U|=15b=265\,182\,525.
\]

The mod-two rank of the full simplex boundary is
\[
r_0:=\operatorname{rank}W=\binom{30}{14}=145\,422\,675.
\]
The row space of \(W\) is nondegenerate for the standard dot product.
For completeness, if \(D\) is the next boundary matrix, the mod-two
simplex Laplacian identity is
\[
W^{\mathsf T}W+DD^{\mathsf T}=I
\]
because the ground-set size 31 is odd, while \(WD=0\).  A vector in
\(\operatorname{row}W\cap\ker W\) is therefore killed by both summands
on the left and hence is zero.  Equivalently,
\[
\operatorname{rank}(WW^{\mathsf T})=r_0.
\]

Since \(\operatorname{rank}A\le r_0\),
\[
\dim C=|U|-\operatorname{rank}A
 \ge |U|-r_0
 =119\,759\,850.
\]

For an arbitrary binary matrix \(A\), the radical of the dot product
restricted to \(\ker A\) has dimension
\[
\delta=\operatorname{rank}A-\operatorname{rank}(AA^{\mathsf T}).
\]
Here
\[
AA^{\mathsf T}=WW^{\mathsf T}+RR^{\mathsf T},
\]
so the rank inequality for a perturbation gives
\[
\begin{aligned}
\operatorname{rank}(AA^{\mathsf T})
&\ge r_0-\operatorname{rank}(RR^{\mathsf T})\\
&\ge r_0-\operatorname{rank}R\\
&\ge r_0-2b.
\end{aligned}
\]
Consequently
\[
\delta
\le \operatorname{rank}A-r_0+2b
\le2b
=35\,357\,670.
\]

If \(C\) were self-orthogonal, every element of \(C\) would lie in the
radical of the restricted form, forcing
\(\dim C=\delta\), contrary to the two displayed bounds.  A doubly even
binary code is self-orthogonal, so \(C\) is not doubly even either.
\(\square\)

## Consequence

This is a no-go theorem for the proposed claim that every pair-trade
code at \(r\equiv3\pmod4\) is doubly even.  It is not an obstruction to
the exact Steiner legs themselves: the words arising from exact-cover
mates form a much narrower nonlinear subset of \(C\).
