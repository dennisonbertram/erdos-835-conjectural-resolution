# The binary Hamming-weight bridge cannot give an `O_16` perfect code

## The tempting count

Label the 31 coordinates of the binary Hamming code `Ham(5,2)` by the
nonzero elements of `F_2^5`.  A support is a codeword precisely when its
label sum (XOR) is zero.  Its weight enumerator gives

\[
A_{14}=8,280,720,\qquad A_{15}=9,398,115,
\]

and hence

\[
A_{14}+A_{15}=17,678,835
 =\frac{\binom{31}{14}}{15}
 =\frac{\binom{31}{15}}{17}.
\]

This is exactly the cardinality of a Steiner system `S(14,15,31)`, or,
equivalently, one perfect 1-code in the odd graph `O_16`.  It suggests the
following support-preserving construction:

* keep every weight-15 Hamming support as a 15-block; and
* for every weight-14 Hamming support `C`, choose a coordinate
  `c(C) notin C` and use `C union {c(C)}` as another 15-block.

The count is real, but the construction is impossible for every choice of
the added coordinates.

## No-go theorem

**Theorem.**  There is no family obtained by the two rules above which is a
packing of `O_16` of minimum graph distance 3.  In particular it cannot be
an `O_16` perfect code or an `S(14,15,31)`.

**Proof.**  Fix a weight-14 Hamming support `C` and write `c=c(C)`.  Thus
`sum(C)=0`, `c notin C`, and `B=C union {c}` is one of the proposed blocks.
For any `y in C`, put

\[
T=B\setminus\{y\}= (C\setminus\{y\})\cup\{c\}.
\]

The label sum of `T` is `c+y`.  If `c+y` is not in `T`, then

\[
D=T\cup\{c+y\}
\]

is a *distinct* weight-15 Hamming support: its label sum is zero.  It is
therefore retained by the first rule.  The two proposed blocks `B` and `D`
share the 14-set `T`.  Equivalently, the 15-set
complement of `B union D` in the 31-coordinate set is a common neighbour of
`B` and `D` in `O_16`.  Thus the
proposed family has minimum graph distance at most 2.

Consequently, avoiding this obstruction for every `y in C` would require
`c+y in T`, hence `c+y in C`, for every `y in C`.  This says

\[
C+c=C. \tag{1}
\]

But (1) is impossible.  It implies first that `c notin C` (otherwise
`0=c+c` belongs to `C`), and then partitions the 14 elements of `C` into
seven pairs `{x,x+c}`.  The XOR of the members of each pair is `c`, so

\[
\sum_{x\in C}x = 7c=c\ne0,
\]

contradicting that `C` is a Hamming support.  Hence for every `C` and every
possible added coordinate `c`, some `y` produces the conflicting retained
weight-15 block `D`.  QED.

This is stronger than a failure of a particular canonical choice: no
choice function `C mapsto c(C)` can repair the construction while all
weight-15 supports remain their natural blocks.

## Exact extensions of the no-go

### Every Hamming coset

For a syndrome `h` in `F_2^5`, let `H_h` denote the supports with label sum `h`; `H_0`
is the Hamming code and the other 31 sets are its cosets.  The analogous
proposal for a fixed `h` retains every 15-support in `H_h` and enlarges each
14-support `C` in `H_h` to `C union {c(C)}`.

The preceding proof applies word-for-word.  Indeed, the 14-face formed by
removing `y` from `C` and adding `c` has sum `h+c+y`; adding `c+y` produces
a 15-support of sum `h`.  The only way this local conflict could be avoided
for all `y` is again `C+c=C`.  Pairing its elements now gives

\[
\sum C=7c=c,
\]

so a locally compatible core would have to satisfy both `c=h` and
`C+h=C`.  For `h=0` this is impossible because `c` must be a nonzero
coordinate.  For nonzero `h`, there are only

\[
\binom{15}{7}=6,435
\]

such 14-supports: choose seven of the 15 translation-by-`h` pairs on the
coordinates other than `0,h`.  A nonzero coset instead has

\[
N_h(14)=8,287,155,\qquad N_h(15)=9,391,680,
\]

supports of the two weights, respectively.  Thus it contains many
non-periodic 14-supports, each of which forces a conflict, and the
whole-coset proposal is impossible.

The count coincidence persists for every coset, not just the code:

\[
N_h(14)+N_h(15)=17,678,835.
\]

Here the values follow from the transitivity of `GL(5,2)` on the 31
nonzero syndromes and
`N_h(w)=(C(31,w)-A_w)/31` for nonzero `h`.

### Global relabelings and extended-Hamming punctures

The result is invariant under an arbitrary *single* coordinate permutation
`pi`: applying `pi` to every retained support and every enlarged support
preserves intersections, common neighbours, and the odd graph.  Hence it
also excludes

\[
\{\,pi(D): D\in H_h,\ |D|=15\,\}
\ \cup\
\{\,pi(C\cup\{c(C)\}): C\in H_h,\ |C|=14\,\}.
\]

This includes all linear relabelings of the nonzero `F_2^5` labels.
If a Hamming-coordinate automorphism is applied to the retained
weight-15 supports *alone* in the linear-code case, it fixes that collection
setwise, so it gives no different construction.  An arbitrary permutation
applied only to the weight-15 supports is not a common relabeling and is not
covered here.

It also includes the standard extended-Hamming route.  The extended binary
Hamming code has coordinates `F_2^5` and consists of the even supports of
XOR zero.  If it is punctured at `p`, relabel a surviving coordinate `x` by
`x+p`.  For a punctured support `S`, the extended-code condition is exactly

\[
\bigoplus_{x\in S}(x+p)=0:
\]

for even `|S|` the removed coordinate is absent, and for odd `|S|` it is
present.  Thus every puncture is the same Hamming construction in shifted
labels.  An affine translation of all 32 extended coordinates merely changes
the puncture, so it supplies no escape.

Finally, complementing in the 31-coordinate universe preserves the Hamming
code (the all-one support has XOR zero).  The original one-point extension
can therefore be written using complementary weights: the complement of
`C union {c}` is obtained by deleting `c` from the complementary
weight-17 Hamming support.  This is only a reparametrization of the same
excluded construction.  Complementing the *output* 15-blocks, however,
creates 16-subsets and is not an automorphism of `O_16`.

## Small Hamming controls

The same count and obstruction appear in the shorter binary Hamming codes.
For `n=2^m-1` and `k=2^{m-1}`, the relevant count is

\[
A_{k-2}+A_{k-1}=\binom{n}{k-2}/(k-1).
\]

| `m` | coordinates | `(A_{k-2},A_{k-1})` | outcome |
| --- | ---: | ---: | --- |
| 3 | 7 | `(0,7)` | The seven weight-3 supports are the Fano `S(2,3,7)`; no enlargement is needed. |
| 4 | 15 | `(280,435)` | Every one-coordinate enlargement of every weight-6 support conflicts with a retained weight-7 support. |
| 5 | 31 | `(8,280,720, 9,398,115)` | The theorem above rules out the proposed `O_16` construction. |

For all `m>=3` the same argument works whenever a weight-`k-2` support is
to be enlarged: an invariant support would have `(k-2)/2=2^{m-2}-1` pairs,
an odd number, and therefore nonzero XOR.

`verify_hamming_weight_bridge_no_go.py` checks the enumerator arithmetic,
the `m=3` Fano control, all 2,520 possible linear-code enlargements and all
coset cases in the `m=4` control, the coset-period count, and a concrete
`m=5` instance.  The theorem, not the finite checks, is the all-`m=5` proof.

## Scope

This closes the maximal support-preserving family described above: one fixed
Hamming syndrome class, all of its natural weight-15 supports, and one-point
extensions of all of its natural weight-14 supports, up to a common
coordinate permutation or an extended-Hamming puncture.  It does not rule
out a construction that transforms only the weight-15 supports, uses
different transformations on the two weights, deletes coordinates from
weight-16/17 supports by a new rule, or otherwise remaps the supports.  Nor
does it settle the required partition into 17 perfect codes (and thus does
not settle Erdős--Rosenfeld Problem #835).
