# Triangle closure is a derived-design statement, and its small-case proof does not extend

Date: 2026-07-26.  Verifier: `verify_triangle_closure_reduction.py`
(stdlib, exact integers, < 20 s).  Labels: **PROVED** / **COMPUTED** /
**OPEN** as marked.

## What this note settles

`boundary_triangle_closure.md` records the

> **Triangle closure law.**  Let \(A\) be an \(S(r-1,r,2r+1)\), \(r\) odd.  If
> \(B_1,B_2\in A\) satisfy \(|B_1\cap B_2|=(r-1)/2\), then
> \((B_1\Delta B_2)^c\in A\).

as FINITE-VERIFIED (21/21 at \(r=3\), 660/660 at \(r=5\)), CONJECTURAL at
\(r=15\), with the explicit caveat that "the two verified scales are unique
designs with large groups, so accidental rigidity is a live possibility".

This note **proves** the law at \(r=3\) and \(r=5\), identifies the mechanism
exactly, and shows the mechanism is **absent from \(r=9\) onwards**.  The
consequence is negative for the programme in that note's "Why it matters"
paragraph: the two exhaustive verifications carry **no** inductive weight for
\(r=15\).

## 1. The reduction (PROVED)

Write \(r=2m+1\), let \(X\) be the \((2r+1)\)-set, \(A\) an \(S(r-1,r,2r+1)\),
and let \(B_1,B_2\in A\) with \(|B_1\cap B_2|=m\).  Put

\[
 I=B_1\cap B_2,\quad S_i=B_i\setminus I,\quad W=X\setminus(B_1\cup B_2).
\]

Then \(|I|=m\), \(|S_1|=|S_2|=|W|=m+1\), \(S_1\cap S_2=\emptyset\),
\(|X\setminus I|=3m+3\), and

\[
 (B_1\Delta B_2)^c=I\cup W,\qquad |I\cup W|=2m+1=r .
\]

**Lemma 1.**  \(A_I:=\{B\setminus I: I\subseteq B\in A\}\) is an
\(S(m,m+1,3m+3)\) on \(X\setminus I\); \(S_1,S_2\) are two of its blocks and
they are disjoint; \(W\) is exactly the complement of \(S_1\sqcup S_2\) in
\(X\setminus I\); and

\[
 (B_1\Delta B_2)^c\in A\iff W\in A_I. \tag{1}
\]

*Proof.*  Deriving an \(S(t,k,v)\) at an \(m\)-set gives an
\(S(t-m,k-m,v-m)\): every \((t-m)\)-set of the remaining points, together with
\(I\), is a \(t\)-set and so lies in a unique block, which then contains \(I\).
Here \(t=r-1=2m\), \(k=r=2m+1\), \(v=2r+1=4m+3\), giving
\(S(m,m+1,3m+3)\).  \(I\subseteq B_i\) so \(S_i\in A_I\), and
\(S_1\cap S_2=(B_1\cap B_2)\setminus I=\emptyset\).  Finally \(I\subseteq
I\cup W\), so \(I\cup W\in A\) iff \((I\cup W)\setminus I=W\in A_I\). ∎

So the law is entirely a statement about the derived design: **do two disjoint
blocks of an \(S(m,m+1,3m+3)\) have their complementary \((m+1)\)-set as a third
block?**

## 2. The mechanism (PROVED)

Let \(N_0(k)\) denote the number of blocks of an \(S(k-1,k,3k)\) disjoint from a
fixed block.  It is determined by the parameters.

**Lemma 2.**  If \(N_0(m+1)=2\), then \(W\in A_I\); hence triangle closure holds
at that \(r\).

*Proof.*  \(W\) has exactly \(m+1\) subsets \(T\) of size \(m\), and each lies in
a unique block \(B_T\) of \(A_I\).

If some \(B_T\subseteq W\) then \(B_T=W\) (both have \(m+1\) points) and we are
done.  So assume every \(B_T=T\cup\{x_T\}\) with \(x_T\in S_1\cup S_2\).

The \(B_T\) are pairwise distinct: if \(B_T=B_{T'}\) for \(T\ne T'\) then
\(B_T\supseteq T\cup T'=W\), so \(B_T=W\subseteq W\), excluded.

If \(x_T\in S_1\) then \(B_T\cap S_2=\emptyset\), because \(T\subseteq W\) is
disjoint from \(S_2\).  Also \(B_T\ne S_1\), since \(B_T\) meets \(W\) and
\(S_1\) does not.  As \(S_1\) is itself disjoint from \(S_2\) and there are only
\(N_0(m+1)=2\) blocks disjoint from \(S_2\), \(B_T\) is the unique other one.
Symmetrically, if \(x_T\in S_2\) then \(B_T\) is the unique block other than
\(S_2\) disjoint from \(S_1\).

So the injective map \(T\mapsto B_T\) has image of size at most \(2\), giving
\(m+1\le 2\).  For \(m\ge2\) this is a contradiction, so the assumption fails
and \(W\in A_I\).

For \(m=1\), \(A_I\) is an \(S(1,2,6)\) — a perfect matching of six points into
three pairs — and \(W\) is the third pair, so the conclusion holds directly. ∎

## 3. Where \(N_0=2\) actually holds (COMPUTED, exact)

With \(\lambda_s=\binom{3k-s}{k-1-s}/(k-s)\) for \(s<k\) and \(\lambda_k=1\),

\[
 N_0(k)=\sum_{j=0}^{k}(-1)^j\binom kj\lambda_j .
\]

| \(m=(r-1)/2\) | \(k=m+1\) | derived design \(A_I\) | \(N_0(k)\) |
|---|---|---|---|
| 1  (\(r=3\))  | 2 | \(S(1,2,6)\)  | **2** |
| 2  (\(r=5\))  | 3 | \(S(2,3,9)\)  | **2** |
| 4  (\(r=9\))  | 5 | \(S(4,5,15)\) | 22 |
| 5  (\(r=11\)) | 6 | \(S(5,6,18)\) | 72 |
| 7  (\(r=15\)) | 8 | \(S(7,8,24)\) | **758** |
| 8  (\(r=17\)) | 9 | \(S(8,9,27)\) | 2558 |

\(k=4,7,10,12\) are not arithmetically admissible.  Over \(k\le12\),
\(N_0(k)=2\) **only** for \(k\in\{2,3\}\).

### 3a. The derived family is essentially empty beyond \(k=3\)

Sharper still: the only members of \(S(k-1,k,3k)\) known to exist are the two
with \(N_0=2\).

- \(k=2\): \(S(1,2,6)\), a perfect matching.  Exists.
- \(k=3\): \(S(2,3,9)=AG(2,3)\).  Exists, unique.
- \(k=5\): \(S(4,5,15)\) — **proved nonexistent** (Mendelsohn–Hung).
- \(k=6\): \(S(5,6,18)\) — not among the known Steiner 5-designs
  (\(v=12,24,36,48,72,84,108,132,168,244\)).
- \(k\ge8\): \(t=k-1\ge7\).  Steiner systems with \(t\ge6\) **do** exist
  abstractly -- Keevash, and Glock--Kuhn--Lo--Osthus, prove existence for all
  sufficiently large \(v\) meeting the divisibility conditions -- but no
  explicit example is known, and the small cases here sit far below any
  effective threshold, so they are open.

So the two parameters where triangle closure is provable are exactly the two
where the derived design exists at all, and \(N_0=2\) there is the resolvability
of those two designs into parallel classes of three.

### 3b. A correction: \(r=9\) is dead, not open

`fixed_base_parity_judgment.md` §3 lists the accessible parameters for
Conjecture P as "\(r=7,11,13\) are parameter-empty; \(r=9\) needs an
\(S(8,9,19)\) (existence open); \(r=15\) needs a first \(S(14,15,31)\)."

The \(r=9\) entry can be settled.  Deriving \(S(8,9,19)\) at a \(4\)-set gives
\(S(4,5,15)\), whose nonexistence is classical (Mendelsohn–Hung, 1972; the
maintained Steiner tables record \(S(4,5,15)\) as nonexistent).  Hence

\[
 \textbf{no } S(8,9,19) \textbf{ exists, and } r=9 \textbf{ is parameter-empty
 as well.}
\]

The accessible list for Conjecture P is therefore \(r\in\{3,5\}\) testable and
\(r=15\) open — with \(r=15\) surviving because its analogous derivation lands
on \(S(4,5,21)\), the smallest \(S(4,5,v)\) whose existence is unknown, rather
than on a design already excluded.

## 4. Verdict

**Theorem.**  Triangle closure holds at \(r=3\) and at \(r=5\), and Lemma 2 is a
complete proof of it there.  The proof uses only the count \(N_0=2\) — not
uniqueness of the Fano plane or of \(S(4,5,11)\), and not their automorphism
groups.

**Corollary (scope).**  The mechanism fails at every larger admissible
parameter, already at \(r=9\).  At \(r=15\) a block of the derived
\(S(7,8,24)\) is disjoint from 758 others, not 2, and Lemma 2's counting step
collapses.  Therefore the 21/21 and 660/660 verifications recorded in
`boundary_triangle_closure.md` are **explained** rather than **evidential**:
they are forced by a coincidence of the derived parameters that does not recur.

**Settled at \(r=15\), later the same day: the law is FALSE.**  A
triangle-closure triple is exactly a weight-3 word of \(C_0^\perp\), and that
count is forced: \(A_3=927\,696\,866\,625\), against \(bN_7/2\) critical pairs,
so only \(10495/162591\approx6.45\%\) of critical pairs complete.  See
`s141531_triangle_third_moment_audit.md` §2 and `triangle_census_r15.md`.  This
confirms the warning made here: the \(N_0=2\) mechanism is special to
\(r=3,5\) and is absent beyond.  The reduction remains valid and now says:
every hypothetical \(S(7,8,24)\) fails the required resolvability property.

**Restatement at \(r=15\) (now known false; stated as originally derived).**
By (1), triangle closure at \(r=15\) is equivalent to:

> in a hypothetical \(S(7,8,24)\), any two disjoint blocks have the complement
> of their union as a third block —

equivalently, the 758 blocks contained in the complement of any block are closed
under complementation inside that 16-set.  This is a strong resolvability
condition.  The later triangle census refutes it: only
\(10495/162591\) of the corresponding critical pairs close.  The observation
that \(758\) is even merely explains why the elementary parity check alone did
not detect the failure.

## 5. Scope

This is a reduction and a small-case theorem, supplemented by the later exact
triangle census that **does** decide triangle closure negatively at \(r=15\).
It is still **not** a nonexistence result for \(S(14,15,31)\), for
\(LS(15,16,32)\), or for Erdős–Rosenfeld Problem #835: the failed closure law
was only a proposed proof route, not a property required for existence.  Its
effect on the programme of `boundary_triangle_closure.md` §"Why it matters" is
to remove the finite verifications as support and then close that route.  The
equivalent statement concerns a hypothetical \(S(7,8,24)\), an object whose
existence remains open.  Existence for \(t\ge6\) is known only asymptotically
(Keevash; Glock--Kuhn--Lo--Osthus); no explicit example is known and this
small case is open.

## 6. What the verifier checks

`verify_triangle_closure_reduction.py`:

- recomputes the \(N_0\) table and the admissibility of each \(k\);
- builds the Fano plane, and an \(S(4,5,11)\) by exact cover here (not
  imported), and confirms both are Steiner systems of the stated strength;
- for **every** qualifying pair at \(r=3\) and \(r=5\): checks the set algebra of
  §1, checks that \(A_I\) really is an \(S(m,m+1,3m+3)\), that \(S_1,S_2\) are
  disjoint blocks of it, and that equivalence (1) holds — reproducing 21/21 and
  660/660 through the reduction rather than by brute force;
- checks that every block of each derived design is disjoint from exactly
  \(N_0(m+1)=2\) others, and that the map \(T\mapsto B_T\) behaves as Lemma 2
  requires;
- records the negative control \(N_0(5)=22\), \(N_0(8)=758\).

Recorded output is in `verification.txt` under 2026-07-26.
