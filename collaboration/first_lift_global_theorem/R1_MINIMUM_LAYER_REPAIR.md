# Exact one-layer repair of the \(r=1\) dead prefix

Date: 2026-07-28.

## Result and scope

For the dead seven-prefix in `R1_DEAD_SEVEN_PREFIX.md`, define the
**complete-layer repair distance** to be the least number of its seven
selected colour matchings that must be replaced by different perfect
matchings on the same prescribed supports before some eighth prescribed
support admits a matching disjoint from the repaired prefix.

The exact repair distance is
\[
 \boxed{1}. \tag{1}
\]
In fact, every one of the seven selected colour layers has at least one
valid one-layer replacement.  A smallest concrete repair changes only two
edges within the unique selected size-twelve layer.

Here "repair" means only that an eighth prescribed support becomes
matchable.  It does not mean that the resulting eight-prefix extends through
all seventeen colours.  The distinct full-completion repair distance is
proved to be three in `R1_MINIMUM_FULL_REPAIR.md`.

This is a coordinated-prefix result for one explicit class-B instance.  It
does not prove a universal one-layer switching theorem, class-B-prime or
fan realizability, full completion by switching, or Problem #835.

## A minimum switch

In the ordering of `verify_r1_dead_seven_prefix.py`, selected colour zero is
the size-twelve matching
\[
 M_0=\{05,14,23,7\,12,8\,11,9\,10\}. \tag{2}
\]
Replace it by
\[
 M'_0=\{05,14,27,3\,12,8\,11,9\,10\}. \tag{3}
\]
This preserves exactly the same twelve-vertex support and is disjoint from
the other six selected matchings.  It is the alternating four-cycle switch
\[
 \{23,7\,12\}\longmapsto\{27,3\,12\}. \tag{4}
\]

The first remaining size-ten support has complement \(\{7,8,9\}\).
After the switch it admits
\[
 N=\{06,1\,10,23,4\,11,5\,12\}. \tag{5}
\]
The matching \(N\) is disjoint from \(M'_0\) and from all six unchanged
layers.  Notice that it uses the released edge \(23\).

The original prefix blocks all ten remaining supports, so distance zero is
impossible.  Equations (3)--(5) give distance at most one, proving (1).

The switch is also edge-minimal inside its changed layer.  The symmetric
difference of two different perfect matchings on the same vertex set is a
nonempty disjoint union of alternating even cycles.  Its shortest possible
component is a four-cycle, so at least two old matching edges must change.
The switch (4) attains this lower bound.

## Exact one-layer census

For each selected colour \(i\), fix the other six original layers.  The
second column below counts alternative perfect matchings on colour \(i\)'s
support that enable at least one remaining support.  The third counts
pairs consisting of such a replacement and an enabled remaining support;
it does not multiply by the number of possible eighth matchings.

\[
\begin{array}{c|c|r|r}
i&|V_i|&\text{repairing replacements}&
\text{replacement/support pairs}\\ \hline
0&12&954&9{,}492\\
1&8&32&296\\
2&8&32&296\\
3&10&168&1{,}496\\
4&8&32&296\\
5&8&32&300\\
6&10&196&1{,}752
\end{array} \tag{6}
\]

Thus the one-layer repair is not tied to a specially chosen selected
colour: each of the seven layers can be changed, while retaining the other
six verbatim, to admit an eighth support matching.

## Exhaustive verification

`verify_r1_minimum_layer_repair.py` reconstructs the original supports and
seven-prefix.  For a support of order \(s\), it generates all
\((s-1)!!\) perfect matchings, with no solver or randomness.  For each
selected colour it:

1. fixes the other six original matchings;
2. enumerates every different matching on the selected colour's prescribed
   support;
3. retains exactly those disjoint from the fixed six;
4. exhausts every perfect matching of all ten remaining supports; and
5. reproduces the two exact count columns in (6).

It separately rechecks the distance-zero obstruction, the explicit
four-cycle switch, the eighth matching (5), and the two-edge secondary
minimum.
