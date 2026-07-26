# The k=4 case is a Klein-family parity, not a coincidence

Date: 2026-07-26.  Verifier: `verify_sqs8_klein_family_parity.py`
(stdlib, exact, ~30 s).  Status: **PROVED** and fully machine-checked.

## What this adds

`verify_k4.py` establishes by exhaustive search that the maximum number of
pairwise block-disjoint \(S(3,4,8)\) is \(2\), hence no \(LS(3,4,8)\) and
\(\chi(J(8,4))\ge6\).  That is a brute-force fact with no stated mechanism.

This note supplies the mechanism.  It also settles, at \(k=4\), the
Disjointness–Parity conjecture of `collaboration/opus5_v2/IDEAS.md` §A by
exhibiting the sign \(\varepsilon\) explicitly rather than merely reporting that
no counterexample was found.

## 1. Systems, codes, and a quadratic form (PROVED)

Let \(V=\mathbb F_2^8\) with coordinates indexed by the point set.

**Lemma 1.**  For every \(S(3,4,8)\) \(D\), the \(\mathbb F_2\)-span \(C_D\) of
the characteristic vectors of its 14 blocks is a self-dual \([8,4,4]\) code
(the extended Hamming code), it contains the all-ones word \(\mathbf 1\), and
its 14 weight-4 words are exactly the blocks of \(D\).  The map \(D\mapsto C_D\)
is a bijection onto the 30 such codes.

Let \(E\subset V\) be the even-weight code, \(\dim E=7\), and put

\[
 q(u)=\tfrac{\operatorname{wt}(u)}2 \bmod 2 \qquad (u\in E).
\]

**Lemma 2.**  \(q\) is a quadratic form on \(E\) whose polarization is the
standard inner product:
\(q(u+v)=q(u)+q(v)+\langle u,v\rangle\), because
\(\operatorname{wt}(u+v)=\operatorname{wt}(u)+\operatorname{wt}(v)
-2\langle u,v\rangle\).  The radical of \(\langle\cdot,\cdot\rangle\) on \(E\)
is \(\langle\mathbf 1\rangle\), and \(q(u+\mathbf 1)=4-q(u)\equiv q(u)\), so
\(q\) descends to a nondegenerate quadratic form on
\(\overline E=E/\langle\mathbf 1\rangle\cong\mathbb F_2^6\).

**Lemma 3.**  \(\overline E\) carries the **hyperbolic** form: its nonzero
singular vectors are the classes of weights \(0,4,8\), of which there are
\(35=(2^2+1)(2^3-1)\), the \(O_6^+(2)\) count.  (The elliptic count is 27.)

Consequently \(\overline U_D:=C_D/\langle\mathbf 1\rangle\) is a **maximal
totally singular** 3-space of \(O_6^+(2)\) — every word of \(C_D\) has weight
\(0,4\) or \(8\).  There are \(2\cdot3\cdot5=30\) such subspaces, matching the
30 systems exactly.

## 2. Disjointness is opposite-family (PROVED)

Two systems \(D,D'\) are block-disjoint iff \(C_D\cap C_{D'}\) contains no
weight-4 word, i.e. iff \(C_D\cap C_{D'}=\{0,\mathbf 1\}\), i.e. iff
\(\overline U_D\cap\overline U_{D'}=0\).

The 30 maximal totally singular subspaces of \(O_{2m}^+\) fall into two
families, and two of them lie in the **same** family iff
\(\dim(U\cap U')\equiv m\pmod 2\).  Here \(m=3\), so

\[
 \text{same family}\iff \dim(U\cap U')\ \text{odd}.
\]

Block-disjointness gives \(\dim=0\), which is even.

**Theorem A.**  Block-disjoint \(S(3,4,8)\) lie in opposite Klein families.
Since there are only two families, **no three \(S(3,4,8)\) are pairwise
block-disjoint**; the maximum is \(2\).  Hence no \(LS(3,4,8)\), and
\(\chi(J(8,4))\ge6\).

The count is sharp and checks out: for a fixed \(U\) in one family, the 15
subspaces of the other meet it in dimension 0 or 2, and exactly 8 meet it in 0
(under the Klein correspondence with \(PG(3,2)\): 15 points and 15 planes, each
plane containing 7 of the points and missing 8).  So there are
\(15\times8=120\) block-disjoint pairs — the number the exhaustive search also
reports.

## 3. Disjointness–Parity at k=4 (PROVED)

\(A_8\cong\Omega_6^+(2)\) preserves the two families and odd permutations swap
them.  So

\[
 \varepsilon(D):=\pm1\ \text{according to the family of }\overline U_D
\]

satisfies \(\varepsilon(\pi D)=\operatorname{sgn}(\pi)\varepsilon(D)\) and
\(D\cap D'=\emptyset\Rightarrow\varepsilon(D)\varepsilon(D')=-1\).  This is
exactly the conjectured sign of `opus5_v2/IDEAS.md` §A, realized concretely at
\(k=4\); the two families are the two \(A_8\)-orbits of size 15.

`collaboration/opus5_v2/verify_disjointness_parity.py` (run 2026-07-26) reports
the same orbit split and zero same-orbit disjoint pairs at \(S(2,3,7)\),
\(S(3,4,8)\) and \(S(4,5,11)\), so the conjecture is consistent at every
parameter where it can be tested.

## 4. Scope — and why this does not transfer to k=16

The mechanism is entirely a property of length-8 binary self-dual codes.  It
uses:

- that an \(S(3,4,8)\) has only 14 blocks, so that its blocks *span a code*
  whose weight-4 words are exactly the blocks; and
- the accidental isomorphism \(A_8\cong\Omega_6^+(2)\).

At \(k=16\) an \(S(15,16,32)\) has \(\binom{32}{16}/17=35{,}357{,}670\) blocks.
For the argument to run one would need a linear code whose weight-16 words are
**exactly** the blocks; at \(k=4\) that is supplied by the extended Hamming
weight enumerator \(1+14z^4+z^8\), where the 14 weight-4 words are precisely
the 14 blocks.  No such statement is available at \(k=16\), and nothing here
supplies one: the span of the blocks would need dimension at least 26 to hold
that many words, and the mechanism gives no reason for its weight-16 layer to
close on the block set.  Independently, the family invariant here comes from
the exceptional isomorphism \(A_8\cong\Omega_6^+(2)\), which has no analogue
for \(A_{32}\).  **This note gives no information about \(k=16\).**

What it does establish is that Disjointness–Parity is not a numerological
accident at the one parameter where its mechanism can be exhibited, which is
the only positive evidence the conjecture currently has beyond
counterexample-freeness.  Whether \(\operatorname{Aut}(D)\le A_{2k}\) — the
conjecture's own stated necessary condition — holds at \(k=16\) remains open;
`collaboration/opus5_v2/PROOF.md` Thm 2.3 (no transposition is an automorphism)
is the only fragment known.

## 5. What the verifier checks

`verify_sqs8_klein_family_parity.py` builds the 30 systems by exact cover and
then verifies, with no third-party imports: Lemma 1 for all 30; that \(q\)
polarizes to the inner product on all \(128^2\) pairs; the radical; the
descent; the count 35 (hyperbolic); that all 30 \(\overline U_D\) are distinct
maximal totally singular 3-spaces; that "\(\dim\) odd" is a consistent
2-colouring into two classes of 15; that block-disjoint \(\iff\dim=0\) on all
ordered pairs; that all 120 disjoint pairs cross families; that the
disjointness graph has no triangle; and the equivariance
\(\varepsilon(\pi D)=\operatorname{sgn}(\pi)\varepsilon(D)\).

Recorded output is in `verification.txt` under 2026-07-26.
