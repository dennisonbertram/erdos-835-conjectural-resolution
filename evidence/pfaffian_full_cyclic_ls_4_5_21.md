# Reproducible cyclic LS(4,5,21) search

The exact-cover search now accepts deterministic seeds, optional randomized
search, a final-run JSON checkpoint, and a JSON witness export. A checkpoint
records only the completed run result; CP-SAT cannot resume its internal
branch-and-bound state from it.

Example: python3 search_cyclic_ls_4_5_21.py --seconds 60 --workers 1
--seed 835 --checkpoint evidence/pfaffian_full_cyclic_ls_4_5_21_seed835.json

If the solver reports FEASIBLE, it first calls its internal verifier and then
can export with --output. Verify the exported witness independently with:
python3 evidence/verify_cyclic_ls_4_5_21.py witness.json

## Sound residual symmetries

After fixing the zero-colour anchor
\(\{0,\infty_1,\infty_2,\infty_3,\infty_4\}\), the remaining normalizer
contains \(S_4\) on the fixed points and \(\mathbb F_{17}^{\times}\) on the
cyclic points. For a multiplier \(a\), the transformed phase is

\[
\phi'(B)=a^{-1}\phi(aB),
\]

with the translation shift folded back into the orbit representative. This
preserves the convention \(c(B+t)=c(B)+t\) and preserves the anchor. Thus
these groups may be used for post-search isomorph rejection or a fully
encoded lex-leader constraint.

No lex-leader was imposed here: a partial signature constraint would not be
a sound WLOG reduction unless it canonically orders the entire transformed
solution. The existing anchor is sound because each constituent Steiner
system has its unique block through the four fixed points.

The separate phase-variable model has 1,197 variables and 353
all-different star-orbit constraints; the Boolean exact-cover model has
20,349 choices, one per five-set. Both are exact encodings. A timeout or
UNKNOWN result is merely an incomplete search, never evidence of existence
or nonexistence. A cyclic witness remains only a necessary shadow for
Erdos--Rosenfeld #835, not a solution of it.

The phase model now takes the same --seed, --randomized, and --output
arguments. It is the preferred bounded probe because it retains all
seventeen colours in each representative star at once, rather than retaining
only the zero-colour exact cover.
