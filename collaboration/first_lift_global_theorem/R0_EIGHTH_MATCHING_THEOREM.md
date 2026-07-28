# An eighth matching in the exceptional \(r=0\) profile

Date: 2026-07-28.

## Theorem

Let \((S_1,\ldots,S_{17})\) be an \(n=13,q=17\) class-B support
instance with profile
\[
(n_8,n_{10},n_{12})=(7,10,0).
\]
Thus every vertex belongs to exactly twelve supports.  Suppose seven
pairwise edge-disjoint prescribed matchings have already been selected,
four on size-eight supports and three on size-ten supports.  Then one of
the seven remaining size-ten supports has a perfect matching edge-disjoint
from all seven selected matchings.

Equivalently:

> Every exceptional-\(r=0\) seven-prefix of profile \(8^4\,10^3\)
> extends to an eighth support matching.

In particular, the seven-prefix supplied by `SEVEN_PACKING_R0_NOTE.md`
always extends, so every exceptional-\(r=0\) class-B instance contains
eight pairwise edge-disjoint prescribed support matchings.

This is strictly an \(r=0\) eighth-matching theorem.  It does not prove an
eighth matching for the other five support profiles, does not complete the
remaining nine colours, and does not solve Erdős--Rosenfeld Problem #835.

## Proof

Let \(F\) be the union of the seven selected matchings and
\(H=K_{13}-F\).  Then
\[
|E(F)|=4\cdot4+3\cdot5=31,\qquad
2\le d_F(v)\le7. \tag{1}
\]
There remain seven size-ten and three size-eight supports.  The exact
complement-row identity is
\[
\#\{\text{remaining support complements containing }v\}
=d_F(v)-2. \tag{2}
\]

Assume for contradiction that all seven remaining size-ten supports have
no perfect matching in \(H\).  The coarsened Tutte classification in
`EIGHTH_MATCHING_CORE_CATALOGUE.md` assigns to every blocked support a
complete multipartite core contained in \(F\).  The exact row-sum
eliminations in `R0_ROW_SUM_CORE_ELIMINATION.md` remove
\[
K_{3,7},\qquad K_{5,5},\qquad K_{3,3,3}
\]
from a total-obstruction argument.  We may therefore choose for each
blocked support one certifying core of one of the four types
\[
\begin{aligned}
A&=K_{5,1,1,1},&
B&=K_{3,3,1,1},\\
C&=K_{3,1,1,1,1},&
D&=K_6.
\end{aligned} \tag{3}
\]
Their total-obstruction reuse ceilings are, respectively,
\[
3,\quad1,\quad3,\quad4. \tag{4}
\]
The \(D=K_6\) ceiling four is the strengthened total-obstruction bound in
`R0_CORE_PAIR_CATALOGUE.md`; the coarser core catalogue alone gives only
the preliminary ceiling five.

Let \(k\) be the number of distinct certifying cores used by the seven
assignments.  Every core is used positively, so \(1\le k\le7\).

The reuse ceilings (4) immediately exclude \(k=1\), since even the largest
ceiling is four.  For \(k=2\), all type pairs except
\((A,D),(C,D),(D,D)\) are capacity-trivial.  The 22 DRAT-certified
branches for the first two pairs and the overlapping \(D,D\) orbits are
UNSAT; the remaining orbit is two disjoint \(K_6\)'s, whose thirty edges
leave one vertex unable to reach the required minimum degree two with the
single remaining prefix edge.  Hence \(k\ge3\).  The remaining values are
excluded as follows.

- \(k=3\): all 16 capacity-sufficient type multisets fail the simultaneous
  complement-capacity inequalities.
- \(k=4\): all 32 capacity-sufficient type multisets fail the simultaneous
  capacity or exact complement-row inequalities.
- \(k=5\): every multiset containing \(B\) fails the simultaneous
  capacity inequalities.  The 21 multisets over \(\{A,C,D\}\) all fail
  the support-union row-rank inequality
  \[
  2|E(J)|-2|W|
  \le
  15+\sum_i t_i\min(3,|W|-|C_i|), \tag{5}
  \]
  after exact minimization of the core-union edge count for every support
  union \(W\) and maximization over every legal positive multiplicity
  vector \((t_i)\).
- \(k=6\) or \(k=7\): separate exact union classifications according to
  the number \(0,1,\ldots,7\) of non-\(D\) cores again contradict (5).
  These classifications exhaust every type multiset and both possible
  multiplicity shapes: \(2+1+1+1+1+1\) for \(k=6\), and seven ones for
  \(k=7\).

Thus no value of \(k\) is possible.  The assumption that all seven
remaining size-ten supports are blocked is false.  Hence some remaining
size-ten support has a perfect matching in \(H\), and adding it extends
the prefix to eight pairwise edge-disjoint matchings. \(\square\)

## Exact dependency chain

The proof is computer-assisted.  Its finite classifications and
certificate replays are the following committed artifacts; the hashes
identify the repository state in which each dependency was last
established or independently hardened.

1. Tutte cores and exact reuse identities:

   - commit `f5c0970`,
     `EIGHTH_MATCHING_CORE_CATALOGUE.md`,
     `verify_eighth_matching_core_catalogue.py`;
   - commit `2b83717`,
     `R0_ROW_SUM_CORE_ELIMINATION.md`,
     `verify_r0_row_sum_core_elimination.py`;
   - commit `916a8a3`,
     `R0_CORE_PAIR_CATALOGUE.md`, section “A \(K_6\) cannot be reused
     five times”, and `verify_r0_core_pairs.py`, establishing the
     strengthened \(K_6\) total-obstruction reuse ceiling four used in
     (4).

2. One or two distinct certifying cores:

   - commit `841a79c`,
     `r0_two_core_refutations/README.md`,
     `r0_two_core_refutations/verify_two_core_refutations.py`,
     its manifest, and 22 compressed DRAT proofs.

3. Three and four distinct certifying cores:

   - commit `bbf8aff`,
     `R0_THREE_CORE_CAPACITY.md`,
     `verify_r0_three_core_capacity.py`;
   - commit `856478f`,
     `R0_ALL_FOUR_CORE_FAMILIES.md`,
     `verify_r0_four_core_capacity.py`, together with its two companion
     four-core notes.

4. Five distinct certifying cores:

   - commit `34ec83d`,
     `R0_FIVE_CORE_HIGH_B.md`,
     `verify_r0_four_core_capacity.py`;
   - commit `90e8c72`,
     `R0_FIVE_CORE_ZERO_B.md`,
     `verify_r0_four_core_capacity.py`, and
     `verify_r0_three_core_capacity.py`;
   - commit `8811b72`,
     `R0_FIVE_CORE_ZERO_B_UNION.md`,
     `verify_r0_five_core_zero_b_union.py`, an independent compact
     support-union proof of all 21 zero-\(B\) rows.

5. Six or seven distinct certifying cores:

   - commit `b4e6058`,
     `R0_SIX_SEVEN_K6.md`,
     `verify_r0_six_seven_k6.py` for at most one non-\(D\) core;
   - commit `0fd491a`,
     `R0_SIX_SEVEN_TWO_EXCEPTIONAL.md`,
     `verify_r0_six_seven_two_exceptional.py`;
   - commit `9e35a0a`,
     `R0_SIX_SEVEN_THREE_EXCEPTIONAL.md`,
     `verify_r0_six_seven_three_exceptional.py`;
   - commit `67ff117`,
     `R0_SIX_SEVEN_FOUR_EXCEPTIONAL.md`,
     `verify_r0_six_seven_four_exceptional.py`;
   - commit `516508b`,
     `R0_SIX_SEVEN_FIVE_EXCEPTIONAL.md`,
     `R0_SIX_SEVEN_SIX_SEVEN_EXCEPTIONAL.md`, and their two companion
     verifiers.

The DRAT package supplies independently replayable propositional
certificates for the two-core layer.  The later layers are exact finite
enumerations and integer optimizations checked by the cited programs;
they should be described as computer-assisted, not as a formal
proof-assistant development.

## Strict frontier

This theorem advances the universal prefix length from seven to eight for
the exceptional profile \((7,10,0)\) and after a seven-prefix of type
\(8^4\,10^3\).  Subsequent work sharpens the frontier:

1. `../coordinated_eight_r2_r5/NOTE.md` proves a coordinated eight-packing
   theorem for every profile \(r=2,3,4,5\).  Thus \(r=1\) is the only
   remaining coordinated-eight profile.
2. Literal arbitrary-prefix analogues are false for every \(r=1,2,3,4,5\),
   by the exact dead-but-fully-completable certificates in
   `R1_DEAD_SEVEN_PREFIX.md`, `R2_DEAD_SEVEN_PREFIX.md`,
   `R3_DEAD_SEVEN_PREFIXES.md`, `R4_DEAD_SEVEN_PREFIX.md`, and
   `R5_DEAD_SEVEN_PREFIX.md`.  Hence the surviving \(r=1\) proof must
   coordinate or switch the earlier choices.
3. Even after the coordinated eighth frontier is closed, a new invariant is
   needed to propagate toward all seventeen colours.
