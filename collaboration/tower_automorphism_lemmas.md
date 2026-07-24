# Automorphism lemmas for the k=16 large-set tower

Scope: the tower \(LS(t,t+1,t+17)\), \(2\le t\le15\), whose members are
forced by a hypothetical tight colouring of \(J(32,16)\); every member has
exactly \(17\) classes.  All proofs are complete and self-contained.

## Lemma 1 (extension–class bijection)

Let \(\mathcal L\) be an \(LS(t,t+1,v)\) with classes
\(\mathcal C_1,\dots,\mathcal C_{v-t}\), and let \(A\) be a \(t\)-set.  Then
the map sending the class \(\mathcal C_i\) to its unique block through
\(A\) is a bijection from classes to the \(v-t\) extensions
\(A\cup\{z\}\), \(z\notin A\).

**Proof.**  Each class is a Steiner system \(S(t,t+1,v)\), so it has exactly
one block containing \(A\); that block is an extension of \(A\).  Every
extension of \(A\) is a \((t+1)\)-set, hence a block of exactly one class,
because the classes partition all \((t+1)\)-sets.  The two assignments are
mutually inverse. \(\square\)

## Lemma 2 (fixed-class count; the \(h=f-a\) identity)

Let \(\sigma\) be an automorphism of \(\mathcal L\), let \(f\) be its number
of fixed points and \(h\) its number of fixed classes.  Then for every
\(\sigma\)-invariant \(t\)-set \(A\) containing exactly \(a\) fixed points,
\[
 h=f-a .
\]
In particular all invariant \(t\)-sets contain the same number of fixed
points.

**Proof.**  By Lemma 1, classes correspond to extensions of \(A\).  The
extension \(A\cup\{z\}\) of the invariant set \(A\) is
\(\sigma\)-invariant iff \(\sigma(z)=z\), i.e. iff \(z\) is one of the
\(f-a\) fixed points outside \(A\).  On the other hand, the extension
belonging to class \(\mathcal C_i\) is invariant iff \(\mathcal C_i\) is a
fixed class: if \(\sigma\mathcal C_i=\mathcal C_i\), uniqueness of the block
through \(A\) inside \(\mathcal C_i\) forces invariance; conversely an
invariant extension lies in \(\mathcal C_i\) and in
\(\sigma^{-1}\mathcal C_i\), which are then equal.  Counting invariant
extensions both ways gives \(h=f-a\). \(\square\)

*Remark.*  This is the argument of the large-set involution theorem in the
main note, stated at full generality: it needs no assumption on the order
of \(\sigma\).

## Lemma 3 (overlapping-orbit lemma)

Let \(\sigma\) be an automorphism of \(\mathcal L\) and let \(S\) be a
\((t+1)\)-set with \(\sigma S\ne S\) and \(|S\cap\sigma S|=t\).  Then the
class containing \(S\) is not fixed by \(\sigma\).

Consequently, if every class is fixed — automatic when \(\sigma\) has prime
order \(q>v-t\), since the induced permutation of the \(v-t\) classes has
order dividing \(q\) and degree less than \(q\) — then no such \(S\)
exists.  Such an \(S\) exists precisely when \(\sigma\) admits one
"incomplete run plus invariant filler": a set consisting of \(r\ge1\)
consecutive points of one cycle of length \(\ge r+1\), together with
\(t+1-r\) points forming a union of fixed points and full cycles.  Two
special cases: a cycle of length \(\ge t+2\) (take \(t+1\) consecutive
elements), and a moved point together with \(t\) fixed points.

**Proof.**  If the class \(\mathcal C\) of \(S\) satisfied
\(\sigma\mathcal C=\mathcal C\), then \(\sigma S\in\mathcal C\), and
\(S,\sigma S\) would be two distinct blocks of one Steiner system sharing
a \(t\)-set, contradicting uniqueness.  For the characterization: if
\(S\) decomposes as an invariant part plus a single maximal run
\(x_i,\dots,x_{i+r-1}\) inside a cycle of length \(\ge r+1\), then
\(\sigma S\) differs from \(S\) exactly by exchanging \(x_i\) for
\(x_{i+r}\), so \(|S\cap\sigma S|=t\) and \(\sigma S\ne S\).  Conversely
\(|S\cap\sigma S|=t\) means exactly one point of \(S\) leaves under
\(\sigma\); decomposing \(S\) into maximal runs along cycles, each
incomplete run of length \(r\) loses its initial point, so there is
exactly one incomplete run and the rest of \(S\) is
\(\sigma\)-invariant. \(\square\)

## Theorem 4 (no large prime orders anywhere in the tower)

No member \(LS(t,t+1,t+17)\), \(2\le t\le15\), admits an automorphism of
prime order \(q\ge19\).

**Proof.**  Such a \(\sigma\) has a \(q\)-cycle.  Since \(q>17\), Lemma 3's
hypothesis holds (all 17 classes fixed), and since
\(q\ge19\ge t+2\) for \(t\le17\), a run of \(t+1\) consecutive points of
the \(q\)-cycle produces the forbidden \(S\). \(\square\)

The case \(t=3\), \(q=19\) is the motivating instance: an
\(LS(3,4,20)\) cannot have a 19-cycle, because \(\{0,1,2,3\}\) and
\(\{1,2,3,4\}\) would be blocks of the same fixed class sharing the triple
\(\{1,2,3\}\).  For \(LS(4,5,21)\) and order 19 there is also a second
proof: the automorphism fixes at least two points, and deriving at a fixed
point yields an order-19 automorphism of an \(LS(3,4,20)\).

## Theorem 5 (order 17 always cycles the classes)

For every \(2\le t\le15\), any order-17 automorphism of
\(LS(t,t+1,t+17)\) permutes the 17 classes in a single 17-cycle.

**Proof.**  A nonidentity order-17 permutation of \(t+17\le32<34\) points
has exactly one 17-cycle, hence exactly \(f=t\) fixed points.  An
invariant \((t+1)\)-set is a union of point orbits; since
\(t+1\le16<17\), it would consist of \(t+1\) fixed points, impossible as
\(f=t<t+1\).  So a fixed class would have no invariant blocks, and its
\(b_t=\binom{t+17}{t}/(t+1)\) blocks would split into orbits of size 17,
forcing \(17\mid b_t\).  But by Lucas' theorem
\(\binom{t+17}{t}\equiv\binom10\binom tt=1\pmod{17}\), so
\(b_t\equiv(t+1)^{-1}\not\equiv0\pmod{17}\).  Hence no class is fixed;
the 17 classes split into orbits of size 17, i.e. a single
17-cycle. \(\square\)

## Theorem 6 (involutions along the tower)

Let \(\tau\ne\mathrm{id}\) be an involution of \(LS(t,t+1,v)\) with \(f\)
fixed points, \(m=(v-f)/2\) transpositions, and \(h\) fixed classes
(\(h\equiv v-t\pmod2\)).  Lemma 2 forces all invariant \(t\)-sets to have
the same fixed-point count \(a=f-h\).  Invariant \(t\)-sets with
\(a=t-2j\) exist whenever \(f\ge t-2j\), \(m\ge j\), \(t-2j\ge0\).  Hence
two distinct values of \(j\) are realizable — a contradiction — unless the
realizable \(j\) is unique.  For the tower (\(v=t+17\), 17 classes):

- \(v=21\) (\(t=4\)): \(f\) odd; realizable \(a\in\{4,2,0\}\) as
  \(f,m\) permit; uniqueness forces \(f=1\) (then only \(a=0\), giving
  \(h=1\)).  Every involution of an \(LS(4,5,21)\) fixes exactly one point
  and one class.
- \(v=31\) (\(t=14\)): the same analysis forces \(f=1\), \(h=1\).
- \(v=32\) (\(t=15\)): \(f\) is even, and \(a=15-2j\) is odd with
  \(j\le m=(32-f)/2\), \(a\le f\).  For \(4\le f\le18\) both \(a=1\)
  (\(j=7\le m\)) and \(a=3\) are realizable; for \(20\le f\le30\) two
  consecutive odd values \(a,a+2\) are realizable (e.g. \(f=30\):
  \(a=13,15\)).  Hence \(f\in\{0,2\}\): either fixed-point-free (no
  invariant 15-sets, Lemma 2 vacuous), or exactly two fixed points with
  the unique realizable \(a=1\), giving \(h=1\).  The \(f=2\) case is not
  excluded by single-system constraints (the induced structure on the
  fixed pair is the trivial \(S(1,2,2)\)).
- \(v=20\) (\(t=3\)): \(f\) even; \(f\ge4\) realizes \(a=3\) and \(a=1\),
  contradiction; so \(f\in\{0,2\}\), with \(h=1\) when \(f=2\).

## Theorem 7 (combining with single-system spectra)

If \(h\ge1\), each fixed class is a single Steiner system admitting
\(\tau|_{\text{points}}\).  The fixed-substructure theorem (session notes:
a prime-order automorphism of an \(S(t,t+1,v)\) induces
\(S(s,s+1,f)\)-structures on its fixed set) then applies.  Sample
consequences at \(v=21\): order-3 automorphisms of a single
\(S(4,5,21)\) are fixed-point-free, so an order-3 automorphism of an
\(LS(4,5,21)\) with \(f=3\) (which would force \(h=2\ge1\) fixed classes
by Lemma 2 and the class-count congruence) is impossible; hence order-3
automorphisms of \(LS(4,5,21)\) are fixed-point-free with
\(h\equiv2\pmod3\).  Order-5: \(f\in\{1,11\}\), with \(h=7\) at \(f=11\).

## Summary table for \(LS(4,5,21)\)

| prime order | fixed points | fixed classes |
|---|---|---|
| 2 | 1 | 1 |
| 3 | 0 | 2, 5, 8, 11, 14, or 17 |
| 5 | 1 or 11 | (f=11: 7) |
| 7 | 0 | 3, 10, or 17 |
| 11, 13 | impossible (single-system spectrum via any fixed class; and no fixed-class-free action exists since 17≢0 mod 11,13 forces h≥1) | — |
| 17 | 4 (cycle type 17+4) | 0 (single 17-cycle on classes) |
| ≥19 | impossible (Theorem 4) | — |

Provenance: Lemmas 1–3 and Theorems 4–6 are proved above in full.
Theorem 7 and the table combine them with the fixed-substructure theorem
proved in the session transcript of 2026-07-24; the order-19 exclusion at
\(LS(3,4,20)\) that motivated Lemma 3 is due to the collaborator's note of
the same date.
