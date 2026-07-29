# Critical correction required in Lemma 8.3

The newly appended human proof has a reversed intersection condition.

For diagonal blocks

    B_1 = (W' \ {w_1}) union {u_1,v_1},
    B_2 = (W' \ {w_2}) union {u_2,v_2},

with no shared U/V coordinate:

- if w_1 = w_2, their intersection is W' \ {w_1}, of size 13;
- if w_1 != w_2, their intersection is W' \ {w_1,w_2}, of size 12.

But the current Lemma 8.3 says "intersection 12 iff the corresponding
w-values coincide" and then defines epsilon using equality.  That is
backwards.  The trace identity needs epsilon to count the diagonal pairs
that land in A_12, so it must use inequality, not equality (unless you
systematically redefine a complementary statistic and change all formulas).

Repair NOTE.md and strengthen Section I of the verifier so it explicitly
constructs labelled W', U, V blocks for both equal and distinct omitted-point
cases and asserts their actual intersection sizes.  Also add the complete
double-count proof:

1. for an A_12 pair X,Y, all common R-neighbours are
   W union {u,v} for matching edges u-v between the two 3-sets, so any two
   such neighbours intersect exactly in W (size 13);
2. therefore unordered triples ({X,Y},{D,D'}) counted by
   binom(Q_XY,2) are in bijection with an A_13 pair {D,D'} and one of its
   epsilon(D,D') A_12 diagonal common-neighbour pairs;
3. use q^2=q+2 binom(q,2), ordered versus unordered conventions, and
   sum_XY Q_XY=10080 n to derive the factor 4 in tr(Q^2).

Rerun the verifier and Ruff.  Do not continue the H3/H4 attack until this
correction is complete and visibly recorded.
