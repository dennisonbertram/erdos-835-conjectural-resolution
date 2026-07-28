# STATUS — Opus 5 full-problem resume, 2026-07-28

## Verdict

**Erdős–Rosenfeld Problem #835 is OPEN.**  Nothing in this directory resolves
it, constructs a \(17\)-colouring of \(J(32,16)\), or refutes one.  \(k=16\) is
not settled here either.

**Session constraint, stated up front:** the Python interpreter and web/search
access were both permission-gated in this session and never became available.
So this is a pencil-and-paper session: **no script was executed and no
literature lookup was performed**.  Every claim in `PROOF.md` is proved by hand
there.  The two scripts in this directory are audit surface only and are
labelled *unrun*.  Literature facts quoted below are quoted **from the
repository's own committed notes**, with file:line, not from any search made
this session.

## Strongest new result

**Rung-uniform intersection rigidity, and the exact tail dichotomy for large
sets.**  Precisely (`PROOF.md` §§2–6):

1. **Theorem 1 / Theorem 2.**  For *every* \(S(t,t+1,v)\) — all \(t\), all
   \(v\) — the block-intersection distribution is forced by the parameters:
   with \(K=t+1\), \(q=v-t\), the number of blocks meeting a fixed block in
   \(K-i\) points is
   \[
     N_{(i)}=\frac{\binom Ki\bigl[\binom{q-1}{i}+(-1)^i(q-1)\bigr]}{q},
     \qquad
     N^{(b)}_{(i)}=\frac{\binom Ki\bigl[\binom{q-1}{i}-(-1)^i\bigr]}{q}
   \]
   for same-class and cross-class counts respectively.
2. **Theorem 3 (the delimiter).**  At *every* rung \(t\) of the #835 tower and
   for *every* prime \(p=k+1\), all of these are nonnegative integers, the
   one-base-block Delsarte moment system after imposing the Steiner design
   equations has a **unique** feasible point, and every
   non-degenerate single-block shell count returns exactly \(r\le p\) with no
   slack.  (Exactly one shell is degenerate — \(i=p-1\), which occurs only at
   the top rung — and it bounds nothing; it is the complement-closure
   identity.)
3. **Theorem 5 (tail dichotomy).**  For any \(LS(t,t+1,v)\) with \(q=v-t\)
   classes: the last class is automatic; the last two are **exactly** a
   bipartiteness question on an explicit \((t+1)\)-regular conflict graph; the
   last three are **exactly** a graph \(3\)-colouring question on an explicit
   \(2(t+1)\)-regular graph whose edges decompose into \(\binom vt\) canonical
   triangles (additional graph triangles can occur).  Hence
   \[
     LS(t,t+1,v)\ \text{exists}\iff
     \text{some }q-2\text{ disjoint systems have bipartite leftover conflict graph.}
   \]

### Why this matters relative to the repository's prior state

The repository already proves items 1 and 2 **for the top rung only** — the
systems \(S(k-1,k,2k)\) themselves — in `../../opus5_v2/PROOF.md` Theorems
1.3, 2.1, 3.1 and 3.2.  What is new is that the same rigidity holds at *every*
rung and for *every* admissible \(k\), with the same closed forms.  That
converts a per-case observation into a **route closure that is uniform in
\(k\)** for the single-base-block same-class and cross-class shell
inequalities computed here: each returns only \(r\le p\).  Joint statistics
based at several blocks, higher-order intersections and strengthened LP/SDP
hierarchies are not ruled out.  It also
supplies a second, independent derivation (Johnson scheme, `PROOF.md` §2.3) of
the repository's top-rung Theorems 1.3 and 3.1, which previously rested on a
single binomial-inversion computation.

Item 3 is the global analogue, at the level of whole Steiner systems, of
Theorem E of `../post_r0_global_bridge/NOTE.md`, which locates a related
frontier for matchings inside one first-lift instance.  The two are independent
statements about different objects.  Here the exact unresolved information is
bipartiteness for the last two classes and \(3\)-colourability for the last
three; elementary degree, vertex and edge counts do not decide it.  The
\(r=q-1\) case is the repository's own gap lemma
(`../../../evidence/large_set_literature_2026-07-26.md:8-19`); \(r=q-2\) and
\(r=q-3\) are new.

Also new and fully proved: **Corollary 4**, which pins down which rung produces
which structure — complement-closure occurs at the top rung and *only* there,
"no two blocks disjoint" occurs at rung \(p-3\) and *only* there — and
**Theorem 6**, the local Latin-rectangle characterisation, which saturates to a
full Latin square of order \(k\) exactly at the top rung.

## Exact gap

Unchanged in substance, and now stated in the tower-uniform language.  Define
\[
  \tau(p):=\max\{\,t:\ LS(t,t+1,t+p)\ \text{exists}\,\}.
\]
#835 asks whether \(\tau(p)=p-2\) for some prime \(p>3\).  What is known, all
quoted from the repository's committed notes:

| \(p\) | \(k=p-1\) | status | first **known** failing rung | source |
|---|---|---|---|---|
| 5 | 4 | excluded | \(t=2\): \(LS(2,3,7)\) fails | `erdos_835_conjectural_resolution.md:361-364` |
| 7 | 6 | excluded | \(t=3\): \(LS(3,4,10)\), \(D(10)=5<7\) | `collaboration/opus5/generic_radius4_certificate_attack/NOTE.md:293` |
| 11 | 10 | excluded | \(t=4\): \(S(4,5,15)\) does not exist | `erdos_835_conjectural_resolution.md:368-369` (Mendelsohn–Hung) |
| 13 | 12 | excluded | \(t=4\): \(S(4,5,17)\) does not exist | `erdos_835_conjectural_resolution.md:370-372` (Östergård–Pottonen) |
| — | 14 | excluded | none — \(k+1=15\) is composite | `erdos_835_conjectural_resolution.md:78-87` |
| 17 | 16 | **OPEN** | none known | — |
| 19 | 18 | **OPEN** | none known | — |

"First **known** failing rung" is deliberate: for \(k=10\) and \(k=12\) the
rung-3 objects \(LS(3,4,14)\) and \(LS(3,4,16)\) are *not* known to fail —
\(LS(3,4,16)\) is recorded as open at
`collaboration/opus5/unrestricted_ls3420_attack_2/NOTE.md:374-380` — and those
two \(k\) die one rung higher, at the level of the Steiner system itself rather
than the large set.

So the exact gap is: **no upper bound on \(\tau(p)\) below \(p-2\) is known for
any prime \(p\ge17\)**, and this note does not supply one.  Theorem 3 shows
that the single-base-block shell inequalities computed here will not supply
one either.

For \(k=16\) specifically the first two open rungs are \(LS(3,4,20)\) and
\(LS(4,5,21)\), and the repository records both as open, with the sharper fact
that **no nontrivial large set of Steiner quadruple systems has ever been
constructed at any order** (`evidence/large_set_literature_2026-07-26.md:49`)
and that \(D(20)\in\{15,17\}\) (`ibid.:29-32`).

## Independent audit surface

Everything in `PROOF.md` §§2–7 is proved by hand and can be re-derived with
pencil and paper.  The audit list is `PROOF.md` §8, items (A1)–(A7).  The
highest-value hand checks, in order:

* **(A2)/(A3)** Theorem 1 against four systems an auditor can build by hand —
  \(S(2,3,9)\) gives \((1,0,9,2)\), \(S(4,5,11)\) gives \(N_{(5)}=0\),
  \(S(5,6,12)\) gives \(N_{(6)}=1\), and the \((t,v)=(k-1,2k)\) specialisation
  reproduces the repository's \((1,0,12,0)\) and \((1,0,45,40,45,0)\) at
  `../../opus5_v2/PROOF.md:142-148`.
* **(A4)** The completeness identity
  \(N_{(i)}+(q-1)N^{(b)}_{(i)}=\binom Ki\binom{q-1}{i}\), which cross-validates
  Theorems 1 and 2 against each other.
* **(A5)** Theorem 3's integrality, which reduces to
  \(\binom{p-1}{i}\equiv(-1)^i\pmod p\).
* **(A6)** Theorem 5 part 2 on \(LS(2,3,9)\): delete five of the seven
  classes and check the leftover \(24\) triples form a \(3\)-regular bipartite
  graph under "share a pair".

Two scripts are provided, standard-library only and deterministic.  **Neither
was executed in this session.**  Their output is *not* evidence for any claim;
every claim is proved without them.  The first script validates its own inputs
(it checks each constructed design really is a Steiner system before using it).

```sh
cd "<repo root>"
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_intersection_distribution.py
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_tail_dichotomy.py
```

Both print `ALL CHECKS PASS` or explicit `FAIL` lines.

## Scope relative to the full #835

* The full problem asks for **some** \(k>2\).  A negative resolution must cover
  every \(k>2\); excluding \(k=16\) alone is not a solution.  Nothing here
  excludes any \(k\).
* Theorems 1–3 are **uniform in \(k\) and in the rung**, which is what makes
  them relevant to the full problem rather than to \(k=16\).  But they are
  *negative about methods*, not about the object: they prove a family of
  routes cannot work, not that the object does not exist.
* Theorem 5 is an exact equivalence, so it neither strengthens nor weakens the
  existence question; it relocates the last two classes into an
  \(\mathbb F_2\)/odd-cycle question and the last three into a
  \(3\)-colouring question.
* Corollary 4 shows complement-closure — the strongest single structural
  constraint available at the top rung — **does not propagate down the
  tower**, because complementation maps \(\binom XK\) to itself only when
  \(v=2K\).  So it cannot be leveraged at the rungs where the tower is
  actually open (\(t=3,4\) for \(k=16\)).
* Corollary 5.3 closes the one global parity invariant this framework offers:
  a regular bipartite graph has even order, but the relevant orders are
  \(2N\) and, after folding by complementation, the Catalan number \(C_k\),
  which is odd only when \(k=2^m-1\) and hence never when \(k=p-1\) with \(p\)
  an odd prime.  **The parity route through Theorem 5 is vacuous for every
  admissible \(k\).**

## Why this does or does not prove the full problem

**It does not prove the full problem, in either direction.**  Explicitly:

* *No construction.*  No colouring, partial colouring, or candidate ansatz for
  any \(k>14\) is produced here.  The positive direction is untouched.
* *No obstruction.*  Every theorem here is either an exact reformulation
  (Theorem 5, Theorem 6), a forced-parameter identity (Theorems 1, 2,
  Corollary 4), or a proof that a class of methods is non-obstructive
  (Theorem 3, Corollaries 3.1 and 5.3).  A proof that a method cannot decide
  the problem is not a decision of the problem.
* *The load-bearing gap is unchanged.*  To settle #835 negatively one still
  needs, for every prime \(p\ge17\), a proof that some rung \(t\le p-2\) has no
  \(LS(t,t+1,t+p)\).  Theorem 3 shows that proof cannot come from the
  single-base-block same-class and cross-class shell inequalities computed
  here.  To settle it positively one still needs an actual large set, whose
  existence at rung \(t=6\) would
  entail an \(S(6,7,p+6)\) — and the repository's own literature note records
  that no Steiner system with \(t\ge6\) is known to exist
  (`evidence/large_set_literature_2026-07-26.md:145-150`, "not found — do not
  assume … any unconditional nonexistence theorem for \(t\ge6\)").
* *What would close the gap.*  Theorem 5 says the whole question reduces to:
  do \(q-2\) pairwise disjoint systems exist whose leftover conflict graph is
  bipartite?  An odd-cycle invariant for that graph, at rung \(3\) or \(4\)
  and uniform in \(p\), would resolve #835 negatively.  Corollary 5.3 shows
  the naive counting version of that invariant is vacuous; a finer one is not
  ruled out and is the concrete next attack.

## Next executable attack

1. Run the two verifier scripts when an interpreter is available.  They are
   the only unrun claims associated with this directory, and every theorem is
   already proved without them.
2. Attack the conflict-graph odd-cycle question of Theorem 5 at rung \(3\)
   (\(LS(3,4,p+3)\)) and rung \(4\) (\(LS(4,5,p+4)\)), looking for a cycle-space
   invariant that is uniform in \(p\).  This is the only route identified in
   this session that Theorem 3 does not already close.
3. Independently: settle the literature status of \(S(4,5,21)\) and
   \(LS(3,4,20)\) with a real search (both were unavailable this session).  If
   \(S(4,5,21)\) does not exist, \(k=16\) dies at rung \(4\) immediately.
