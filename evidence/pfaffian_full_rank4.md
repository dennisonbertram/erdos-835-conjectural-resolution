# Rank-four normalization of the full Pfaffian descendant

This is an exact reduction for the rank-four portion of the descended
\(20\times20\) alternating-matrix problem over \(\mathbb F_{17}\).

If \(\operatorname{rank}A=4\), factor \(A=UJU^T\), where \(U\) has four
columns and \(J\) is nonsingular alternating.  For every four-set \(I\),

\[
\operatorname{Pf}(A[I])=\operatorname{Pf}(J)\det(U[I]).
\]

The scalar is harmless because multiplying all colours by a nonzero field
element preserves the rainbow predicate.  A successful matrix has a nonzero
4-Pfaffian, so after vertex relabelling choose four independent rows of
\(U\), and apply a \(GL_4(17)\) change of coordinates to make them
\(e_0,e_1,e_2,e_3\).

For the star on the three basis points other than \(e_c\), the determinant
against a tail point is \((-1)^{3-c}\) times its \(c\)-th coordinate (all
tail vertices are ordered after the basis vertices).  The fourth basis point
contributes \(1\).  Therefore, among the remaining sixteen points the
\(c\)-th coordinates are exactly

\[
\mathbb F_{17}\setminus\{(-1)^{3-c}\}.
\]

Thus, after using the remaining permutation of the sixteen non-basis
vertices to sort coordinate 0, every rank-four candidate lies in the exact
finite space \((16!)^3\) of three permutations.  The script tests the full
1,140-star predicate using determinants, not low moments:

```bash
python3 evidence/search_pfaffian_full_rank4.py
python3 evidence/search_pfaffian_full_rank4.py --sample 100000 --seed 835
```

The normalization is a genuine reduction but the sample is not exhaustive.
An exhaustive traversal or a SAT/CP encoding of the remaining permutation
variables would settle **rank four only**.  It says nothing yet about ranks
6 through 18 or about lifting a descended matrix back to the original
\(32\times32\) principal-Pfaffian problem.
