You are assisting on a narrowly defined finite-geometry problem. Work at maximum
mathematical rigor. We need either an explicit construction at p=19 or a proof
of nonexistence; restricted-family evidence is not enough.

Let p be an odd prime, n=p+1, and let C be a symmetric n by n array over F_p
whose diagonal is ignored and whose off-diagonal entries in every row are
exactly F_p. Equivalently, the p colors form a 1-factorization of K_{p+1}.
Given the total order 0<1<...<p, define the alternating matrix

    B_ij = C_ij for i<j,   B_ji = -C_ij,   B_ii=0.

Question: can rank_F19(B)=4?

Equivalently, do there exist twenty vectors u_0,...,u_19 in a four-dimensional
symplectic F_19-space such that C_ij=<u_i,u_j> for i<j and every off-diagonal
row of C is F_19? Projectively, every point has exactly one orthogonal mate,
but that zero-graph condition alone is not sufficient.

Facts already proved:

1. This is exactly the unrestricted remaining rank-four ordered-link case in
   the p=19 principal-Pfaffian descent for Erdos-Rosenfeld Problem #835.
2. All lifted normal-rational-curve configurations and all diagonally lifted
   alternating circulant rank<=4 configurations are rigorously excluded.
3. Squaring removes order signs: A_ij=B_ij^2=C_ij^2. Every row of A has two
   zeros and each nonzero square twice, and rank(A)<=dim Sym^2(F_19^4)=10.
   This necessary condition has not yet yielded a lower bound.
4. If H has H_ij=1 for i<j and -1 for i>j, then
   Pf(B+tH) has degree 10. Rank(B)=4 forces divisibility by t^8.
5. If B_0,19=a is nonzero, scale a=1. Put x_i=B_0i and y_i=B_i,19 for
   1<=i<=18. Each of x and y is a permutation of F_19\\{1}, and

       R_ij = B_ij - (y_i x_j - x_i y_j)

   is alternating of rank at most 2. If a=0, endpoints are orthogonal mates
   and need a separate treatment.

Critical negative control: a proposed universal rank bound rank(B)>=p-1 is
false. At p=7 the following C has rank(B)=4 and every row is F_7:

0 1 4 6 2 5 3 0
1 0 2 0 3 4 5 6
4 2 0 5 6 1 0 3
6 0 5 0 4 3 2 1
2 3 6 4 0 0 1 5
5 4 1 3 0 0 6 2
3 5 0 2 1 6 0 4
0 6 3 1 5 2 4 0

So do not assert a p-independent lower bound contradicted by this witness.

Seek a p=19-specific theorem. Promising routes include:

- show the rank<=10 squared frequency matrix is impossible specifically for
  q=19 using character sums, quadratic forms, or p-rank;
- exploit the endpoint Schur rank-two residual and permutation constraints;
- prove rank-four forces the twenty projective rows into a classified family
  (but account for repeated projective points: the p=7 witness can have them);
- use the t^8 divisibility of Pf(B+tH) and identities forced by a
  one-factorization;
- construct a genuine p=19 example.

Return a complete chain with every sign checked. Clearly distinguish theorem,
conjecture, and computational proposal. A finite exhaustive proof must state
safe WLOG reductions and a reproducible certificate strategy.
