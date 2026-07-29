# Tower-level literature status, and the "one short of a large set" lemma

Date: 2026-07-26.  Sources are cited inline; every status below was taken from a
primary source or a maintained table, not inferred.

## 1. The gap lemma (PROVED here; the SQS case is due to Etzion–Hartman)

**Lemma.**  Let \(P=v-k+1\) be the number of classes in a large set of
\(S(k-1,k,v)\).  If \(P-1\) pairwise block-disjoint \(S(k-1,k,v)\) exist, then
the \(k\)-sets covered by none of them form a further \(S(k-1,k,v)\) disjoint
from all of them, so a large set exists.

*Proof.*  Every \((k-1)\)-set lies in exactly \(v-k+1=P\) \(k\)-sets, and each
system covers it exactly once.  After \(P-1\) disjoint systems, exactly one
\(k\)-set containing it remains uncovered.  So the uncovered \(k\)-sets form a
Steiner system. ∎

**Corollary.**  The maximum number \(D\) of pairwise disjoint \(S(k-1,k,v)\) is
never exactly \(P-1\): \(D\in\{0,\dots,P-2\}\cup\{P\}\).

Etzion–Hartman state the \(v=5\cdot2^t\) SQS case
("*if there exist \(5\cdot2^t-4\) PDQs of order \(5\cdot2^t\), the unused
quadruples must form an additional disjoint system, and thus a large set
exists*", *Towards a Large Set of Steiner Quadruple Systems*, SIAM J. Discrete
Math. **4** (1991) 182–195, p. 183).  The proof above is parameter-free.

**Consequences for this repo.**

- \(LS(3,4,20)\) has \(P=17\).  So \(D(20)\ne16\): searching for 16 pairwise
  disjoint \(SQS(20)\) is provably futile.  With Etzion–Hartman's
  \(D(20)\ge15\), **\(D(20)\in\{15,17\}\)**, and \(D(20)=17\) is exactly the
  existence of \(LS(3,4,20)\).
- At \(k=16\) itself, \(P=17\): you cannot have exactly 16 pairwise disjoint
  \(S(15,16,32)\), nor exactly 16 pairwise disjoint \(S(14,15,31)\).  Combined
  with `collaboration/opus5/PROOF.md` Thm 9 (at most \(p\) pairwise disjoint,
  equality iff a large set), the maximum lies in \(\{1,\dots,15\}\cup\{17\}\).
  Any argument that rules out 17 must therefore also handle nothing in between —
  and any construction reaching 16 is already a solution.

## 2. Status of each tower level

The k=16 tower is \(LS(j-1,j,j+16)\) for \(j=1,\dots,16\), each level implied by
the next.

| level | object | status |
|---|---|---|
| j=2 | \(LS(1,2,18)\) | exists (a 1-factorization of \(K_{18}\)) |
| j=3 | \(LS(2,3,19)\) | **exists** — Lu, *On large sets of disjoint STS I–VI*, JCTA 34 (1983), 37 (1984); six residual cases by Teirlinck, JCTA **57** (1991) 302–305; shorter proof Ji, JCTA **112** (2005) 308–327.  \(v=7\) is the unique exception in the whole spectrum |
| j=4 | \(LS(3,4,20)\) | **OPEN**, and no nontrivial \(LS(3,4,v)\) has ever been constructed at **any** order |
| j=5 | \(LS(4,5,21)\) | **OPEN** — even its single constituent \(S(4,5,21)\) is open |
| j=6 | \(LS(5,6,22)\) | **OPEN** — \(S(5,6,22)\) unknown |
| j=7 | \(LS(6,7,23)\) | **OPEN** — \(S(6,7,23)\) would be the first *explicit* Steiner 6-design (existence for \(t\ge6\) is known asymptotically, not for small \(v\)) |
| … | … | … |
| j=16 | \(LS(15,16,32)\) | **OPEN** — the target |

Level 4 detail: Etzion, arXiv:2506.23860 (2025) — "*there is no known
construction for large sets of Steiner quadruple systems and the one that gets
close to it was constructed in [Etzion–Hartman 1991]*"; Etzion–Zhou,
arXiv:1912.04489 — "*No construction of nontrivial large set of SQS(n) is
known, although it is a common belief that they exist even for small n.  Using
probabilistic arguments, their existence for large enough n … was proved
recently [Keevash].*"  Their open-problem list even proposes \(n=16\) as the
easiest target, so \(LS(3,4,20)\) is strictly harder terrain than anything yet
built.  Note this cuts both ways: Keevash's non-constructive theorem means
\(LS(3,4,v)\) *does* exist for large admissible \(v\), so level 4 is not a
nonexistence barrier in general.

Level 5 detail: Kolotoğlu, *On the possible automorphism groups of a Steiner
quintuple system of order 21*, J. Combin. Designs **22** (2014) 483–490 — if an
\(S(4,5,21)\) exists its full automorphism group has order in
\(\{1,2,3,4,5,6,7,10\}\); 21 is the smallest order for which existence is
unknown.  The two smaller ones are settled negatively: \(S(4,5,15)\)
(Mendelsohn–Hung) and \(S(4,5,17)\) (Östergård–Pottonen, JCTA **115** (2008)
1570–1573).

Levels ≥ 7 detail: no Steiner system with \(t\ge6\) is *explicitly known*.
Existence is settled asymptotically -- Keevash (arXiv:1401.3665) and
Glock--Kuhn--Lo--Osthus prove that \(S(t,k,v)\) exists for every \(t,k\) and all
sufficiently large \(v\) satisfying the divisibility conditions -- so it is
**wrong** to say none exists; what is missing is any explicit example, and the
small cases relevant here are far below any effective threshold.  Brouwer's
table (a statement about known examples):
"*No Steiner systems are known with t larger than 5.*"  Huber, arXiv:0809.3117:
"*no non-trivial Steiner t-design with t > 5 has been constructed until now.*"
Only symmetry-restricted nonexistence theorems exist (Huber: no flag-transitive
Steiner 6-design).  **No unconditional nonexistence theorem for \(t\ge6\) was
found.**

## 3. Perfect codes in \(O_k\)

Krotov–Potapov, *Completely Regular Codes and Equitable Partitions*, ch. 1 of
Shi–Solé (eds.), CRC Press (2025), §1.2.3.5: one-perfect codes in \(O_{w+1}\)
"*are equivalent to Steiner systems \(S(w-1,w,2w+1)\), the existence of which is
known only for \(w=3\) and \(w=5\)*".  So a perfect code is known only in
\(O_4\) (Fano) and \(O_6\) (\(S(4,5,11)\)); \(O_{16}\) needs \(S(14,15,31)\),
open.

A *partition* of \(O_k\) into perfect codes is known for no \(k>2\), and for
both graphs that admit even one code it provably does not exist: for \(O_4\) it
would be \(LS(2,3,7)\), the unique exception in the LSTS spectrum; for \(O_6\)
it would be \(LS(4,5,11)\), excluded because Brouwer's table gives
\(\chi(J(12,6))\in[8,9]>7\).  \(O_{16}\) is the first index not ruled out.
(Derivation from the cited facts, not a quoted theorem.)

## 4. Erdős #835 itself

erdosproblems.com/835 is **Open** (last edited 22 January 2026), tagged
"VERIFIABLE — Open, but could be proved with a finite example".

**Ma–Tang**, *A Note on Erdős Problem #835* (GitHub PDF only; no arXiv or
journal version found as of 2026-07-26) prove: if \(\chi(J(2k,k))=k+1\) then
\(t\mid\binom{k+t}{t-1}\) for every \(1\le t\le k\) (Prop. 2.1); hence
\(\chi(J(2k,k))\ge k+2\) whenever \(k>2\) and \(k+1\) is **not** prime
(Thm. 2.2, via Lucas).  Their Lemma 2.3 shows that when \(k+1\) is prime **all**
these divisibilities hold, so the method provably cannot touch the prime case.

Independent duplicates of the same strength are recorded on the erdosproblems
forum: an AlphaProof Lean proof for \(\chi(J(18,9))\ne10\) generalised by hand,
and the observation that the recursive Johnson bound
\(A(n,4,k)\le\lfloor (n/k)A(n-1,4,k-1)\rfloor\) already yields \(\ge k+2\)
exactly when \(k+1\) is composite.  Constant-weight-code tables settle
\(3\le k\le14\); Jørgensen, arXiv:2502.15019, shows that is the best obtainable
from the recursive Johnson bound.

Two further forum items worth having:

- **KentaKitamura (30 May 2026)** independently reproduces this repo's tower:
  \(k=10\) dies via \(S(4,5,15)\), \(k=12\) via \(S(4,5,17)\), and "*the same
  derivation for \(k=16\) reaches \(S(4,5,21)\), which appears to be the
  smallest \(v\) for which the existence of an \(S(4,5,v)\) is open*".
- **athvedt (21 May 2026)**: via the Hoffman ratio bound and Eberlein
  eigenvalues, every colour class of a surviving colouring is closed under
  complementation.  This repo already has that independently
  (`collaboration/opus5/PROOF.md` Cor 6.2, `opus5_v2/PROOF.md` Thm 2.1).

Also relevant and not previously in this repo's notes: **Fiol**,
arXiv:1907.08626 (LAA **605** (2020) 1–19) shows \(O_\ell\) has no 1-perfect
code for \(\ell\) odd, which gives \(\chi(J(2k,k))\ge k+2\) for all **odd** \(k\)
(Fiol does not phrase it that way).  This is subsumed by Ma–Tang but is an
independent route.  \(k=16\) is even, so it is unaffected.

Nothing found giving \(\chi(J(2k,k))\ge k+2\) for any \(k\) with \(k+1\) prime
beyond the computational range \(k\le14\).

## 5. Not found — do not assume

Any upper bound \(D(20)\le16\) other than the gap lemma above; any nonexistence
proof for \(LS(3,4,v)\), \(S(4,5,21)\), \(S(5,6,22)\) or \(S(6,7,23)\); any
unconditional nonexistence theorem for \(t\ge6\); any arXiv or journal version
of the Ma–Tang note.
