# Derivation as a homomorphism of completion problems, and why the point-link obstruction escapes every feasible screen

## 0. Scope, stated first

**Erdős–Rosenfeld problem #835 remains OPEN.**  Nothing here decides
\(LS(3,4,20)\) or \(LS(14,15,31)\), excludes \(k=16\), or constructs any large
set.  This note proves a general structural theorem about derivation, uses it
to give the exact logical value of the point-link results reported by the
solver track, and proves that whatever obstructs those point-links is **not**
of the rainbow/clique type that governs every obstruction proved in this
programme so far.

**Audit of solver-derived inputs, up front.**  The finite solver-derived inputs
arrive from the companion certificate directory and are used only at their
certified strength:

| input | strength | how it is used here |
|---|---|---|
| point-link CNFs for EH retain-twelve drops \((0,1,5)\) and \((0,5,10)\) at point \(0\) are **DRAT-UNSAT** | certified | used, and only for those two drops |
| all other \(423\) point-\(0\) links are **DRAT-UNSAT** | certified | every proof is committed, independently reconstructed, and freshly replayed by the aggregate gate |
| my own independent re-solve of the same two instances | **no verdict** | did not terminate in the budget; reported, not used |
| "SAT witnesses for three pairwise disjoint \(STS(19)\)" in both certified leaves | **a priori true** | proved unconditionally in §4c (Theorem 17); carries no information |
| "four pairwise disjoint \(STS(19)\) are UNSAT" (CaDiCaL reconnaissance) | **lead only** | equivalent to the five-colour UNSAT by Theorem 16, so it is the same claim, not a stronger one |
| aggregate \(455\)-case theorem receipt | certified | SHA-256 `312096aa…085`; binds the exact \(30+2+423\) partition, manifest, reconstruction, proof bundle, checker, and scope |

Companion: `collaboration/opus5/large_set_completion_colouring/` (Theorems 1–8,
89 checks).  Verifier here: `verify_derivation_tower_obstruction.py`.

## 1. Notation

Throughout, \(X\) is a \(v\)-set, \(t\ge2\), and the family in play is
\(S(t,t+1,v)\).  For the \(k=16\) tower, \(v=t+17\), so a large set has
\(m=v-t=17\) members at every level; \(t=14,v=31\) is the top and \(t=2,v=19\)
the bottom.  For a family \(\mathcal D=\{D_1,\dots,D_{m-j}\}\) of pairwise
disjoint copies, \(L(\mathcal D)=\binom X{t+1}\setminus\bigcup_iD_i\) is the
leave, a \(t\text{-}(v,t+1,j)\) design (companion Theorem 1(a)).  For
\(p\in X\), the **derived** family is
\[
\mathcal D^p=\{D_i^p\},\qquad D_i^p=\{B\setminus\{p\}: p\in B\in D_i\},
\]
and \(L^p=\{B\setminus\{p\}:p\in B\in L\}\).
Finally \(\nu_L(F)=\#\{B\in\binom F{t+1}:B\in L\}\) for a \((t+2)\)-set \(F\).

## 2. Theorem 9: derivation is a homomorphism of completion problems

> **Theorem 9.**  Let \(t\ge3\), let \(\mathcal D\) be a family of \(m-j\)
> pairwise disjoint \(S(t,t+1,v)\), and let \(p\in X\).  Then
> **(a)** \(\mathcal D^p\) is a family of \(m-j\) pairwise disjoint
> \(S(t-1,t,v-1)\) on \(X\setminus\{p\}\), and \(L(\mathcal D^p)=L(\mathcal D)^p\);
> **(b)** if \(\mathcal D\) completes to a large set of \(S(t,t+1,v)\), then for
> **every** \(p\in X\) the family \(\mathcal D^p\) completes to a large set of
> \(S(t-1,t,v-1)\);
> **(c)** contrapositively, if there **exists** a \(p\in X\) for which
> \(\mathcal D^p\) does not complete, then \(\mathcal D\) does not complete.
>
> The quantifiers are as written: (b) is "for every \(p\)", (c) is "there
> exists a \(p\)".  A single obstructed point kills the whole family.

*Proof.*  (a) The derived design of an \(S(t,t+1,v)\) at \(p\) is an
\(S(t-1,t,v-1)\): a \((t-1)\)-set \(T\subseteq X\setminus\{p\}\) lies in
\(D_i^p\)-blocks exactly as \(T\cup\{p\}\) lies in \(D_i\)-blocks, namely once.
Disjointness is inherited because \(B\mapsto B\setminus\{p\}\) is injective on
blocks through \(p\).  For the leave: \(B'\in L(\mathcal D^p)\) iff
\(B'\cup\{p\}\) lies in no \(D_i\), iff \(B'\cup\{p\}\in L(\mathcal D)\), iff
\(B'\in L(\mathcal D)^p\).
(b) If \(E_1,\dots,E_j\) complete \(\mathcal D\), then \(E_1^p,\dots,E_j^p\) are
pairwise disjoint \(S(t-1,t,v-1)\) and their union is \(L(\mathcal D)^p\),
which by (a) is \(L(\mathcal D^p)\); so they complete \(\mathcal D^p\).
(c) is the contrapositive of (b). \(\square\)

Iterating Theorem 9 along a set \(W\) of points gives the whole shadow tower at
once: for every \(W\subseteq X\) with \(|W|=t-2\), the blocks containing \(W\)
give a family of disjoint \(S(2,3,v-|W|)\) whose completion is implied by that
of \(\mathcal D\).  At \(t=3,v=20\) this is the point-link; at \(t=14,v=31\) the
\(12\)-subsets give \(LS(2,3,19)\)-completion problems.

**This is the exact logical value of the point-link results.**  By Theorem 9(c),
a certified UNSAT for the point-\(0\) link of a retain-twelve drop proves that
that drop does not complete — unconditionally, with no appeal to the block-level
problem.

## 3. Theorem 10: every point-link of every EH retain-twelve drop sits exactly at the derived rainbow bound

Recall from the companion note the four \(5\)-sets
\(F_1=\{0,2,5,14,17\}\), \(F_2=\{1,3,4,15,16\}\), \(F_3=\{6,8,11,13,18\}\),
\(F_4=\{7,9,10,12,19\}\): they are pairwise disjoint, they partition \([20]\),
and all twenty of their \(4\)-subsets lie in the leave of the fifteen
Etzion–Hartman systems.

> **Theorem 10.**  Let \(\mathcal S\) be **any** sub-family of the fifteen
> Etzion–Hartman \(SQS(20)\), let \(L\) be its leave, and let \(p\in[20]\) be
> **any** point.  Let \(F_{i(p)}\) be the unique \(F_i\) containing \(p\) and
> put \(G_p=F_{i(p)}\setminus\{p\}\), a \(4\)-set.  Then
> \[
> \nu_{L^p}\bigl(G_p\bigr)=4 ,
> \]
> i.e. **all four** triples of \(G_p\) lie in the derived leave at \(p\).
> Equivalently, the derived leave graph at \(p\) contains a \(K_4\), for every
> point and every retained sub-family.

*Proof.*  The four \(4\)-subsets of \(F_{i(p)}\) that contain \(p\) are
\(F_{i(p)}\setminus\{q\}\) for \(q\in G_p\).  All five \(4\)-subsets of
\(F_{i(p)}\) lie in the leave of the **fifteen**, hence in the leave of any
sub-family.  Deriving at \(p\) sends \(F_{i(p)}\setminus\{q\}\) to
\(F_{i(p)}\setminus\{p,q\}=G_p\setminus\{q\}\), and as \(q\) runs over the four
points of \(G_p\) these are exactly the four triples of \(G_p\). \(\square\)

Since the \(F_i\) partition \([20]\), every point is covered: there is no point
at which the derived instance is "generic".

**Corollary 10.1 (both clique types, and the bound is met not violated).**
Companion Theorem 3 classifies every clique of a leave graph as a **star
clique** (all blocks on one common \(t\)-set, size at most \(j\)) or a **top
clique** (all blocks inside one \((t+2)\)-set, size at most \(\nu(F)\le t+2\)).
At the derived level \(t'=2\), \(v'=19\), \(j'=5\) both types must be counted:

* **star cliques are tight \(K_5\).**  Every pair of the nineteen points lies
  in exactly \(j'=5\) triples of \(L^p\), and those five are pairwise adjacent
  (they share that pair).  So \(\omega\ge5\), attained at **every** pair.
* **top cliques have size at most \(4\).**  A \((t'+2)\)-set is a \(4\)-set and
  has only \(\binom43=4\) triples, so \(\nu\le4<5=j'\) automatically; Theorem 10
  says the bound \(4\) is **attained** at every point, by \(G_p\).

Hence \(\omega(G_{L^p})=\max(5,4)=5=j'\).  The clique lower bound
\(\chi\ge\omega\) is therefore **met exactly**, there is no \(K_6\), and no
clique certificate — of either type — can witness \(\chi>5\).  In particular
the rainbow criterion \(\nu\le j'\) is satisfied strictly at every \(4\)-set.

## 4. Theorem 11: the point-link obstruction is not of clique/rainbow type

> **Theorem 11.**  Let \(t\ge3\) and let \(\mathcal D\) have leave \(L\).  If a
> \((t+2)\)-set \(F\) satisfies \(\nu_L(F)=t+2\), then for every \(p\in F\) the
> derived leave satisfies \(\nu_{L^p}(F\setminus\{p\})=t+1\), again the maximum.
> The retention bound the rainbow criterion yields is
> \[
> \text{level }t:\ \ \text{retained}\le m-(t+2),
> \qquad
> \text{level }t-1:\ \ \text{retained}\le m-(t+1).
> \]
> With \(m=17\): level \(t\) gives \(15-t\), level \(t-1\) gives \(16-t\).
> **The derived bound is strictly weaker.**

*Proof.*  The \((t+1)\)-subsets of \(F\) containing \(p\) are \(t+1\) in number
and derive to the \(t\)-subsets of the \((t+1)\)-set \(F\setminus\{p\}\), of
which there are exactly \(t+1\); all lie in \(L^p\) because all
\((t+1)\)-subsets of \(F\) lie in \(L\).  The bounds are companion Theorem 2(b)
with \(j\ge t+2\) resp. \(j\ge t+1\). \(\square\)

**Consequence, and it is the point of this note.**  At \(t=3\) the rainbow
criterion forces retained \(\le12\) (companion Corollary R).  At the derived
level \(t=2\) it forces only retained \(\le13\).  A retain-twelve drop therefore
satisfies the derived rainbow criterion strictly.  Hence:

> **If a point-link of a retain-twelve drop is genuinely unsatisfiable, its
> obstruction is not a rainbow obstruction and not a clique obstruction, and it
> is invisible to every *feasible screen* that was actually run** — the
> \(F_i\)-local triple system (companion Theorem 5), the pair-links (companion
> Theorem 6) and the labelled cross-pair invariant (companion Theorem 8), all
> three of which are verified **satisfiable** there, together with the rainbow
> criterion, which is vacuous here by Corollary 10.1.

**Scope of that statement, stated exactly.**  It does **not** say the
obstruction is outside Theorems 1–8.  It cannot: companion Theorem 1 is the
*exact* equivalence "completable \(\iff\chi(G_L)=j\)", so an unsatisfiable
point-link is literally an instance of it; and Theorem 7 of this note is
*precisely* the point-link necessary condition, i.e. the condition now reported
to fail.  What is new is only the **type** of the obstruction and its
**invisibility to the cheap screens**: it is not a clique or rainbow
obstruction, and none of the three screens that terminate detects it.  An
earlier revision claimed the stronger "not any consequence of Theorems 1–8";
that is false and is withdrawn.

That is a statement about the *kind* of argument that can succeed, and it is
unconditional: it does not depend on whether the reported UNSATs are correct.
Given the DRAT certificates for the two named drops, such an obstruction
demonstrably exists for at least those two.

## 4b. Theorem 15: the tower is rigid only at the top

> **Theorem 15.**  In the \(k=16\) tower (level \(t\), \(v=t+17\),
> \(m=v-t=17\) designs), let \(F\) be a \((t+2)\)-set in a **full** large
> set.  Its \(t+2\) sub-blocks receive \(t+2\) distinct colours (Theorem 2(a)),
> so exactly
> \[
> \delta(t)\;=\;17-(t+2)\;=\;15-t
> \]
> colours are **absent** from \(F\).  Thus \(\delta(14)=1\) and
> \(\delta(2)=13\), and \(\delta\) decreases strictly all the way up the
> tower.

At the top, \(t=14\): a \(16\)-set carries \(16\) blocks and there are
\(17\) colours, so **exactly one colour is missing from every \(16\)-set** —
the "missing-colour" map, and the tightest possible rainbow condition.  At the
bottom, \(t=2\): a \(4\)-set carries \(4\) triples against \(17\) colours,
and \(13\) are missing — almost no constraint at all.

This one formula explains the shape of the whole programme.  Rainbow and clique
arguments are sharp exactly where the objects are astronomically large
(\(t=14\): \(17\,678\,835\) blocks per design) and are vacuous exactly where
computation is feasible (\(t=2,3\): \(57\) and \(285\) blocks).  The
point-link UNSATs live at \(t=2\), where \(\delta=13\) and every criterion of
Theorems 1–8 is slack — which is Theorem 11 again, now with a reason.  (Slack
in the *screens*; Theorem 1 itself, being an equivalence, is never slack.)

## 4c. Theorems 16–18: the packing number, and what the packing clue actually says

> **Theorem 16 (packing dichotomy).**  Let \(L\) be a \(t\text{-}(v,t+1,j)\)
> leave.  If \(L\) contains \(j-1\) pairwise disjoint \(S(t,t+1,v)\), then the
> remaining blocks form a \(j\)-th one.  Hence the packing number
> \(\pi(L)\) — the largest number of pairwise disjoint \(S(t,t+1,v)\) inside
> \(L\) — **never equals \(j-1\)**:
> \[
> \pi(L)\in\{0,1,\dots,j-2\}\cup\{j\},
> \qquad\text{and}\qquad
> \pi(L)=j \iff L\ \text{partitions}.
> \]

*Proof.*  Each \(t\)-set is covered \(j\) times in \(L\) and once in each of
the \(j-1\) disjoint systems, so the remainder covers it exactly once; a
collection of \((t+1)\)-sets covering every \(t\)-set exactly once is an
\(S(t,t+1,v)\). \(\square\)

> **Theorem 17 (the packing lower bound is free).**  For every EH retain-twelve
> drop and every point \(p\), the derived leave splits as
> \(L^p=P^p\sqcup D_{d_1}^p\sqcup D_{d_2}^p\sqcup D_{d_3}^p\), where \(P^p\)
> is the derived \(2\)-fold leave of the fifteen and the \(D_{d_i}^p\) are the
> derived discarded designs.  The three \(D_{d_i}^p\) are pairwise disjoint
> \(STS(19)\) inside \(L^p\).  Hence \(\pi(L^p)\ge3\) **unconditionally**.

*Proof.*  Theorem 9(a) applied to each discarded design; disjointness is
inherited.  \(\square\)

**Corollary 16.1.**  With \(j=5\), Theorems 16 and 17 give
\(\pi(L^p)\in\{3,5\}\).  Therefore:
* the reported **SAT witnesses for three** disjoint \(STS(19)\) are *a priori
  guaranteed* — the three derived discarded designs are such a triple — and
  carry **no information**;
* "**no four** pairwise disjoint \(STS(19)\)" and "**no partition into five**"
  are **logically equivalent**, so the four-search is neither weaker nor
  stronger than the five-colour search;
* consequently a DRAT refutation of the four-instance **certifies** the
  five-colour UNSAT, and the cheaper search may be used without loss.  This is
  the actionable content of the packing clue.

> **Theorem 18 (closure at \(j=2\)).**  Let \(L\) be a \(2\)-fold leave and
> suppose some \((t+2)\)-set \(F\) has \(\nu_L(F)=t+2\).  Then every
> \(t\)-subset of \(F\) is covered in \(L\) **only** by \((t+1)\)-subsets of
> \(F\), and \(L\) contains no \(S(t,t+1,v)\) at all.

*Proof.*  A \(t\)-subset \(T\subset F\) lies in exactly two
\((t+1)\)-subsets of \(F\), both in \(L\) by hypothesis; since \(L\) is
\(2\)-fold these are **all** of its covers in \(L\).  So a sub-design
\(S\subseteq L\) must cover every \(t\)-subset of \(F\) exactly once using
only blocks inside \(F\).  Counting incidences,
\[
\bigl|S\cap\tbinom F{t+1}\bigr|\cdot\tbinom{t+1}t
=\tbinom{t+2}t ,
\qquad\text{i.e.}\qquad
\bigl|S\cap\tbinom F{t+1}\bigr|\cdot(t+1)=\frac{(t+2)(t+1)}2 ,
\]
so \(\bigl|S\cap\binom F{t+1}\bigr|=\dfrac{t+2}2\).  Two cases.
*If \(t\) is odd*, \((t+2)/2\notin\mathbb Z\) and no such \(S\) exists.
*If \(t\) is even*, then \((t+2)/2\ge2\) because \(t\ge2\); but any two
\((t+1)\)-subsets of a \((t+2)\)-set meet in exactly \(t\) points, so that
\(t\)-set would be covered twice by \(S\).  Either way \(L\) contains no
\(S(t,t+1,v)\).  \(\square\)

*(An earlier revision of this proof asserted \(|S\cap\binom F{t+1}|=2\) in
general.  That is the value only at \(t=2\); the correct value is
\((t+2)/2\), and the odd-\(t\) branch above is genuinely needed.  The
conclusion is unchanged.)*

Applied at \(t=2\) with \(F=G_p\) (Theorem 10): **\(P^p\) contains no
\(STS(19)\)**, verified directly — every pair inside \(G_p\) is covered in
\(P^p\) by exactly two triples, both inside \(G_p\).  So the obvious candidate
partition "three discarded designs plus a split of \(P^p\)" is impossible, and
**any partition of \(L^p\) must mix \(P^p\) with the discarded designs**.
That is as far as the structural argument reaches here: it explains why the
easy partition fails, and it does **not** explain why every partition fails.
The structural cause of the reported UNSATs remains unidentified.

## 5. What follows

> **Corollary 12 (unconditional).**  The Etzion–Hartman retain-twelve drops
> \((0,1,5)\) and \((0,5,10)\) — in the indexing that lists the fifteen complete
> classes in increasing exported-colour order, i.e. exported colour triples
> \(\{1,2,6\}\) and \(\{1,6,11\}\) — do not complete to \(LS(3,4,20)\).
> *Proof:* Theorem 9(c) with \(p=0\), plus the two DRAT certificates.  The
> label translation is recorded and machine-checked in §6.

> **Corollary 13 (unconditional).**  Every one of the remaining \(423\)
> retain-twelve drops also has an unsatisfiable point-\(0\) link, certified by
> a committed DRAT proof, independent CNF reconstruction, and fresh replay.
> Together with Corollary 12 and the independent exact ten-point exclusions
> for the other \(30\) cases, Theorem 9(c) excludes all \(455\) retain-twelve
> repairs of the Etzion–Hartman core.  With companion Corollary R, the
> **repair distance of that core is at least four**: any \(LS(3,4,20)\) shares
> at most eleven of its fifteen systems.

> **Corollary 14 (unconditional).**  The
> repair distance of at least four means the best published partial large
> set of \(SQS(20)\) is farther from any solution than its \(15/17\) coverage
> suggests, and — by Theorem 9 applied \(11\) times at the top of the tower —
> would say nothing whatever about \(LS(14,15,31)\).  Derivation transports
> obstructions **downward** only.  No result about a single \(20\)-point
> configuration can constrain \(k=16\).

Corollary 14 is worth stating plainly because it bounds the ambition of this
whole line: the tower is a one-way street.  Obstructing \(LS(3,4,20)\)
altogether *would* kill \(k=16\) (the \(11\)-subsets of \([31]\) each carry one);
obstructing one \(20\)-point *configuration* does not.

## 6. Label conventions, machine-checked

The exported file
`collaboration/ls3420_branch0_search/eh15_branch0_partial.txt` (SHA-256
`06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78`, asserted by
both verifiers) uses colours \(0,\dots,16\); the fifteen **complete** classes
are \(\{1,\dots,12,14,15,16\}\) and the two incomplete ones are \(0\) and
\(13\).  Two indexings are therefore in circulation:

* **exported-colour labels** — used in the companion note and its digest;
* **rank labels** \(0,\dots,14\) — the position of a complete class in the
  increasing list, used by the solver track.

The translation is \(0\!\mapsto\!1,\ 1\!\mapsto\!2,\ 2\!\mapsto\!3,\
3\!\mapsto\!4,\ 4\!\mapsto\!5,\ 5\!\mapsto\!6,\ 6\!\mapsto\!7,\
7\!\mapsto\!8,\ 8\!\mapsto\!9,\ 9\!\mapsto\!10,\ 10\!\mapsto\!11,\
11\!\mapsto\!12,\ 12\!\mapsto\!14,\ 13\!\mapsto\!15,\ 14\!\mapsto\!16\).
So rank \((0,1,5)\) is exported \(\{1,2,6\}\) and rank \((0,5,10)\) is exported
\(\{1,6,11\}\).  The reading "raw exported colours \((0,1,5)\)" is **invalid**,
because exported colour \(0\) is one of the two incomplete classes and is not
one of the fifteen; the verifier asserts this, so the ambiguity cannot be
resolved the wrong way silently.

## 7. Independent reproduction: no verdict

An independent exact solver was written for the point-link problem (285
triples, five colours, 171 rainbow-quintuple constraints; unit and dual-unit
propagation, minimum-remaining-values branching, colour symmetry broken on one
pair).  It was run on the two named instances with a **3000-second** wall-clock
budget and was killed by the timeout (exit code 124) having written **zero
bytes** of output — so it did not even complete the *first* of the two
instances.  **No verdict is claimed from it, in either direction, and nothing
in this note rests on it.**  In particular the timeout is not weak evidence for
UNSAT: a non-terminating search distinguishes nothing, and treating elapsed
time as support would be exactly the error this programme has already made
twice (a hint read as a constraint, a single witness read as a certificate).  The DRAT certificates from the solver track stand on their own;
this note does not re-derive them.

## 8. Inventory

**Proved unconditionally here:** Theorems 16–18 and Corollary 16.1 (packing dichotomy; the packing lower bound is free; closure at \(j=2\)); Theorem 15 (rainbow defect \(15-t\), tight
only at \(t=14\)); Theorem 9 (derivation homomorphism, with the
"for every \(p\)" / "there exists \(p\)" quantifiers explicit); Theorem 10
(every point of every EH retain-twelve leave carries a derived \(K_4\));
Corollary 10.1 (the derived rainbow criterion is satisfied, hence vacuous);
Theorem 11 (the rainbow bound strictly weakens on derivation, so the
point-link obstruction is not of clique/rainbow type and is invisible to the
three feasible screens, with the scope caveat above); Corollary 12 (the two
DRAT-certified
drops do not complete); Corollary 13 (all \(455\) retain-twelve EH repairs are
excluded, so the EH-core repair distance is at least four); Corollary 14
(obstructions transport only downward).

**Not claimed:** the existence or non-existence of \(LS(3,4,20)\) or
\(LS(14,15,31)\); **and any progress on Erdős–Rosenfeld #835, which remains
open.**

## 9. Verification

```sh
python3 -B \
  collaboration/opus5/derivation_tower_obstruction/verify_derivation_tower_obstruction.py
```

Standard library only, exact arithmetic and finite enumeration, no solver, no
randomness.  The aggregate verifier separately replays every DRAT proof.
Current status: **53 checks, all passing; Ruff clean.**
