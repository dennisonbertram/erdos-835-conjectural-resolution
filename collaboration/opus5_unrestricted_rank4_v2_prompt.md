Work as a pure mathematician. Do not inspect files or use tools. Return at
most 10,000 tokens, with complete proofs separated sharply from conjectures.

We are attacking the remaining unrestricted rank-four ordered-link problem
over F_19. Let C be a symmetric 20x20 array with ignored diagonal such that
every off-diagonal row is exactly F_19. Define the alternating matrix B by
B_ij=C_ij for i<j and B_ji=-C_ij. We need either construct rank(B)=4 or prove
rank(B)>4.

Equivalently B_ij=<u_i,u_j> for twenty spanning vectors in a 4-dimensional
symplectic F_19-space. Every vertex has one orthogonal mate; in each raw row
the two values in every nonzero sign class {a,-a} may be concordant or
discordant. The displayed-row ordering rule forces concordant neighbours to
straddle the vertex and discordant neighbours to lie on the same side.
Consequently the first and last vertices are panoramic: their raw pairings
are bijections F_19.

For even k=2,4,...,16,

    M_k(x)=sum_j <x,u_j>^k

vanishes at every u_i. In particular all twenty projective points lie on the
quadratic Q=M_2 (possibly Q=0). Exploit the rank/type of Q rigorously.

Endpoint reduction: put a=B_0,19.

If a != 0, scale a=1 and for 1<=i<=18 put

    x_i=B_0i,  y_i=B_i,19.

Both x and y are permutations of F_19\{1}. Moreover

    R_ij = B_ij - (y_i*x_j-x_i*y_j)

is alternating of rank at most 2. Use this together with every even moment
and the displayed order constraints.

If a=0, endpoints are orthogonal mates and require a separate analysis
(proportional versus independent).

Already rigorously excluded:

1. determinant/near-link lifts (an even-moment exhaustion of all 92,378
   slope sets gives zero survivors);
2. paired-doubling half-links for one principal anchor, with an unconditional
   all-210-anchor exhaustive sweep currently running;
3. lifted normal rational curves and rank-four circulants.

A universal rank lower bound is false: a genuine p=7 rank-four ordered link
exists. So any no-go must use p=19.

Try to finish the unrestricted p=19 theorem. Promising tasks:

- classify Q=M_2 and show every nonzero rank/type contradicts the row
  bijections, then exploit Q=0 with M_4,...;
- turn the endpoint rank-two residual into a determinant-link-style moment
  obstruction;
- derive a construction if the identities instead suggest one.

Check signs carefully. A computational proposal is not a proof unless its
finite search space and WLOG reductions are complete and small enough to
certify. End with the single strongest proved statement and exact remaining
gap.
