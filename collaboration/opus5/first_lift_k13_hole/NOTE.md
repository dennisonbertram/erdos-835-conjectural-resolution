# A necessary obstruction for the first unrestricted lift, and its exact vanishing at \(k=16\)

Date: 2026-07-27.

Provenance: this package was generated in an isolated public clone by
Claude Opus 5 and then imported, replayed, and independently audited by
Codex.  The verifier is deterministic and standard-library-only.

## Scope

This note concerns exactly one question, the one left open as item 1 of
Section 6 of `collaboration/unrestricted_lift_tower/NOTE.md`: does the
prescribed-leave \(K_{13}\)-hole problem of that note's Theorem 3 always
have a solution?

It proves:

1. a **new necessary condition** — two cut inequalities — for the
   \(K_{n}\)-hole completion problem, valid for every even \(k\) with
   \(n=k-3\);
2. **explicit counterexamples** violating it, hence explicit
   locally-fan-consistent palettes with **no** completion, at
   \(k=8,10,12,14\);
3. **Theorem B**: at \(k=16\) neither cut inequality can be violated by any
   admissible palette.  Running the same exact computation for every even
   \(k\) from \(6\) to \(34\) shows the obstruction fires for
   \(k\in\{8,10,12,14\}\) and for no other \(k\) in that range;
4. that the two cut inequalities are **not sufficient**: an explicit
   locally-fan-consistent palette at \(k=10\) violates neither, yet has no
   completion.

It does **not** prove that every palette completes at \(k=16\), does not
construct a simultaneous fan or an \(LS(3,4,20)\), and does not settle
Erdős–Rosenfeld Problem #835, which remains open.  Section 7 states the
nested completion questions that remain and keeps their instance classes
separate.

Nothing here depends on the cyclic or \(C_{17}\)-equivariant assumptions.

## 0. Setting

Fix even \(k\).  In the tower of `collaboration/unrestricted_lift_tower`,
\(U\) has \(k+3\) points, \(A\) has \(n:=k-3\) points, the palette \({\cal C}\)
has \(q:=k+1=n+4\) colours, and \(P\in\binom U5\) is a fixed five-set.  At
\(k=16\): \(n=13\), \(q=17\).  Throughout \(n\) is odd.

For a fixed \(P\) the level-1 tower law asks (Theorem 3 of that note) for a
proper edge colouring of \(K_A\) in which the colours **missing** at
\(a\in A\) are exactly
\[
 S_a=S_a(P)=\{F_a(P\setminus\{x\}):x\in P\},\qquad |S_a|=5 ,
\]
equivalently for perfect matchings \(M_c\) on
\(V_c=\{a\in A: c\notin S_a\}\) partitioning \(E(K_A)\).  Write
\[
 m_c=\#\{a\in A:c\in S_a\}=n-|V_c|,\qquad h_c=|V_c|/2 .
\]
Only the \(n\times q\) incidence matrix of the sets \(S_a\) matters; the
actual values \(F_a\) do not.

### The three instance classes

They are kept strictly apart everywhere below.

* **class A** (*arbitrary even support*): row sums \(5\), every \(|V_c|\) even.
* **class B** (*column-bounded*): class A and \(m_c\le5\) for every colour.
  By König's edge-colouring theorem this is exactly the set of matrices that
  decompose into five \(A\)-saturating matchings — i.e. that admit *some*
  \(n\times5\) array of the shape equation (8) of the source note demands.
* **class B′** (*locally fan-consistent*): class B, and the five missed-colour
  four-sets \(D_x\) of such a decomposition are the face-colour sets of an
  actual proper colouring \(L\) of the ten triples of \(P\).  This is exactly
  the local data a simultaneous fan induces at the single five-set \(P\).
* **class C** (*simultaneous-fan realisable*) \(\subseteq\) class B′.  **Class
  C is not sampled anywhere in this work and is not known to be non-empty**:
  no simultaneous fan and no \(LS(3,4,20)\) exists in this repository, and its
  existence is open.

The identification of class B′ uses the complementation \(T\leftrightarrow
P\setminus T\) between the ten triples and the ten pairs of \(P\): two triples
of \(P\) meet in exactly one point iff their complementary pairs are disjoint,
so a proper \(L\) on the ten triples is exactly a partition of \(E(K_5)\) into
matchings.  There are \(332\) such partitions.

Summing row sums gives \(\sum_c m_c=5n\), and \(m_c\) is odd because
\(|V_c|=n-m_c\) is even (Theorem 4 of the source note).  With \(m_c\le5\) and
\(q=n+4\) colours this forces, at \(k=16\), exactly six possible multiplicity
profiles \((n_5,n_3,n_1)\) with
\[
 n_3=24-2n_5,\qquad n_1=n_5-7,\qquad 7\le n_5\le12 ,
\]
so \(|V_c|\in\{8,10,12\}\), at most five colours have \(|V_c|=12\), and
\(\sum_c|V_c|=156\), \(\sum_c h_c=78=\binom{13}2\).

## 1. Lemma 1: two cut inequalities

> **Lemma 1.**  If the \(K_A\)-completion exists then for every \(X\subseteq A\),
> writing \(s_c=|V_c\cap X|\),
> \[
> \sum_{c}\max\bigl(0,\;s_c-h_c\bigr)\;\le\;\binom{|X|}2
> \tag{forced-inside}
> \]
> \[
> \sum_{c}\Bigl\lfloor \tfrac{s_c}{2}\Bigr\rfloor\;\ge\;\binom{|X|}2 .
> \tag{capacity}
> \]

### Proof

Let \(e_c\) be the number of edges of \(M_c\) lying inside \(X\).  Since
\(M_c\) is a perfect matching on \(V_c\), each of the \(s_c\) vertices of
\(V_c\cap X\) is matched either inside \(X\) or to one of the
\(|V_c|-s_c=2h_c-s_c\) vertices of \(V_c\setminus X\); hence
\(s_c-2e_c\le 2h_c-s_c\), i.e. \(e_c\ge s_c-h_c\), and trivially
\(e_c\ge0\) and \(e_c\le\lfloor s_c/2\rfloor\).  The matchings partition
\(E(K_A)\), so \(\sum_c e_c=\binom{|X|}2\) exactly.  Both displayed
inequalities follow. \(\square\)

Neither is implied by Theorem 4 of the source note.  That theorem proves
\(|V_c|\) even, which is exactly the statement that each \(M_c\) can exist
*on its own*; Lemma 1 instead couples the seventeen matchings through the
fixed edge budget \(\binom{|X|}2\) of every vertex subset.  Taking
\(X=A\) in Lemma 1 gives only the identity \(\sum_ch_c=\binom n2\), so all of
its content is at proper subsets.

Two identities make the inequalities easy to evaluate.  Summing \(s_c\) over
colours counts, for each \(a\in X\), the \(n-1\) colours available at \(a\):
\(\sum_c s_c=(n-1)|X|\); and \(\sum_c h_c=\binom n2\).  Hence, with
\(x=|X|\),
\[
 \sum_c\max(0,s_c-h_c)
 =\Bigl[(n-1)x-\tbinom n2\Bigr]+\sum_c\max(0,h_c-s_c).
\tag{1}
\]

## 2. Theorem A: the obstruction really fires

> **Theorem A.**  For \(k=8,10,12,14\) there are class-B′ palettes — i.e.
> palettes with exactly the local shape a simultaneous fan induces at a single
> five-set — with **no** completion.  Explicit instances are stored in
> `certificates/counterexample_n05.json`, `…n07.json`, `…n09.json`,
> `…n11.json`, each with its class-B′ witness (the \(n\times5\) array, the
> partition of \(E(K_5)\), and the colours carrying its parts).

The \(k=12\) and \(k=14\) instances are transparent.

**\(k=12\)** (\(n=9\), \(q=13\)).  Split \(A=X\mathbin{\dot\cup}Y\) with
\(|X|=4\), \(|Y|=5\), and let every vertex of \(Y\) forbid the same five
colours \(c_0,\dots,c_4\).  Then \(V_{c_i}=X\) exactly, so each \(c_i\) must
be a perfect matching on \(X\), using \(2\) of the \(\binom42=6\) edges inside
\(X\); five colours need \(10>6\).  The stored certificate has
\(S_a=\{0,1,2,3,4\}\) for the five vertices of \(Y=\{4,\dots,8\}\) and
\(X=\{0,1,2,3\}\); it violates ten cut inequalities in all, including exactly
the predicted \(\text{forced}(X)=10>6=\binom42\), and also
\(\text{forced}(Y)=14>10\) and \(\text{forced}(\{0,1,2\})=5>3\).

**\(k=14\)** (\(n=11\), \(q=15\)), closed form, `counterexample_n11()`.  Split
\(A=X\mathbin{\dot\cup}Y\), \(|X|=6\), \(|Y|=5\).  Colours: four \(c_i\)
forbidden by every vertex of \(Y\); six \(g_j\) indexed by \(X\) with
\(S_a=\{g_i:i\ne a\}\) for \(a\in X\); five \(e_a\) with
\(S_a=\{c_0,\dots,c_3,e_a\}\) for \(a\in Y\).  Then \(V_{c_i}=X\),
\(V_{g_j}=Y\cup\{j\}\), \(V_{e_a}=A\setminus\{a\}\), and
\[
 \text{forced}(X)=4\cdot3+5\cdot1=17>15=\tbinom62,
 \qquad
 \text{forced}(Y)=6\cdot2=12>10=\tbinom52 .
\]
Its class-B′ witness is explicit: \(L\) is the rotational
near-one-factorisation \(F_x=\{\{x+1,x+4\},\{x+2,x+3\}\}\pmod5\) of \(K_5\)
with \(F_x\) carried by colour \(e_{Y[x]}\), the \(Y\)-block of the array is
the fixed-point-free shift decomposition of a \(5\times5\) off-diagonal, and
the \(X\)-block is the shift \(j\mapsto g_{j+x+1}\bmod 6\).

**What Theorem A does and does not say.**  It says the first lift is a
genuine constraint: the local data a fan induces at one five-set does *not*
automatically complete, and the parity theorem of the source note is far from
enough.  It says nothing about class C at those \(k\).  Indeed at \(k=14\)
class C is **empty** for an independent reason: the level-0 layer forces every
colour class of \(L\) to be a partial Steiner triple system on \(k+3=17\)
points, of which there are at most
\(\lfloor 17\cdot\lfloor16/2\rfloor/3\rfloor=45\), so the \(15\) classes cover
at most \(675<680=\binom{17}3\) triples.  At \(k=8\) the same count fails
(\(9\cdot18=162<165\)).  At \(k=10\) and \(k=12\) the count is exactly tight
(\(11\cdot26=286\), \(13\cdot35=455\)) so it excludes nothing, but this note
has **not** checked whether the stored local \(L\)-patterns occur inside an
actual large set, nor whether the fan values are globally realisable.  At
\(k=16\) the count is likewise exactly tight (\(17\cdot57=969\)) and an
explicit \(LS(2,3,19)\) does exist in this repository; it was re-verified here
directly (\(17\) colour classes, \(57\) triples each, every one of the \(171\)
pairs covered exactly once per class).

## 3. Theorem B: the obstruction cannot fire at \(k=16\)

> **Theorem B.**  Let \(k=16\), so \(n=13\) and \(q=17\).  No class-B palette
> — hence no class-B′ palette, hence no palette induced by any simultaneous
> \(13\)-fan — violates either inequality of Lemma 1, for any \(X\subseteq A\).
> The same exact computation, run for every even \(k\) with \(6\le k\le34\),
> shows a violation is possible for \(k\in\{8,10,12,14\}\) and for no other
> \(k\) in that range.

### Proof

Fix \(X\) with \(|X|=x\) and put \(d_c=\#\{a\in X:c\in S_a\}\), so
\(s_c=x-d_c\).  Every class-B palette satisfies, and only these facts are
used:

* \(\sum_c d_c=5x\), because each of the \(x\) vertices of \(X\) forbids
  exactly five colours;
* \(d_c\le\min(m_c,x)\);
* \(d_c\ge\max\bigl(0,\;m_c-(n-x)\bigr)\), because \(m_c-d_c\) counts
  forbidding vertices outside \(X\), of which there are \(n-x\);
* \((m_c)_c\) has one of the admissible multiplicity profiles of Section 0.

Both left-hand sides of Lemma 1 are **separable** in \(c\) once
\((m_c,d_c)\) is fixed, and the only coupling is the single linear constraint
\(\sum_c d_c=5x\).  So the exact extremum of each side over the *relaxed* set
of all integer \(d\)-profiles obeying the four bullets is computed by a
knapsack dynamic program on the budget \(5x\), separately for each profile.
This is a relaxation of the achievable \(d\)-profiles, so a nonpositive margin
is a proof for every class-B palette.

Carrying this out (`cut_margins` in `first_lift.py`) gives, at \(k=16\), for
each of \(x=1,\dots,13\) and each of the six profiles, a margin \(\le0\) for
both inequalities:

| \(|X|\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| forced-inside | 0 | −1 | −3 | −6 | −2 | −1 | −1 | −2 | −6 | −3 | −1 | 0 | 0 |
| capacity | 0 | −6 | −7 | −10 | −12 | −13 | −13 | −12 | −10 | −7 | −6 | 0 | 0 |

The three zeros are equalities, not violations: at \(x=1\) both sides are
\(0\); at \(x=13\) identity (1) gives
\(\sum_c\max(0,s_c-h_c)=\sum_ch_c=78=\binom{13}2\); at \(x=12\) it gives
\(66=\binom{12}2\). \(\square\)

The same dynamic program run for \(n=3,5,\dots,31\) gives worst margins

| \(k\) | 6 | 8 | 10 | 12 | 14 | 16 | 18 | … | 34 |
|---|---|---|---|---|---|---|---|---|---|
| forced-inside | 0 | +2 | +3 | +4 | +2 | 0 | 0 | 0 | 0 |
| capacity | 0 | +1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

so the obstruction is a small-\(k\) phenomenon that switches off exactly at
\(k=16\).  The mechanism is visible in the \(k=14\) construction: it needs
colours with \(V_c=X\) exactly (each forcing \(|X|/2\) edges inside \(X\))
plus colours of multiplicity \(m_c=1\) whose single forbidding vertex lies
outside \(X\).  At \(k=16\) both budgets bind at once.  A colour with
\(V_c=X\) has \(m_c=13-|X|\le5\), so \(|X|\ge8\); take \(|X|=8\), so
\(Y=A\setminus X\) has five vertices and \(5\cdot5=25\) forbidding slots.
Five colours with \(V_c=X\) consume all \(25\) of them, forcing
\(5\cdot4=20\) edges of the \(\binom82=28\).  But then **every** other colour
has all its forbidders inside \(X\), so \(d_c=m_c\) and its contribution is
\(\max\bigl(0,8-m_c-\tfrac{13-m_c}2\bigr)=\max\bigl(0,\tfrac{3-m_c}2\bigr)\),
which is \(1\) for \(m_c=1\) and \(0\) otherwise; with at most
\(n_1=n_5-7\le5\) colours of multiplicity one this adds at most \(5\), for
\(25<28\).  The dynamic program's exact optimum over all configurations at
\(|X|=8\) is \(26\), still below \(28\).

## 4. The cut inequalities are not sufficient

> **Fact.**  At \(k=10\) (\(n=7\), \(q=11\)) there is a class-B′ palette that
> violates neither inequality of Lemma 1 for any of the \(127\) nonempty
> \(X\subseteq A\), and yet has no completion (exhaustive search).  It is
> stored in `certificates/cut_insufficient_n07.json`; its support multiset is
> \(|V_c|=(2,2,6,2,4,2,6,4,6,2,6)\).

Consequently Theorem B does **not** settle item 1 of Section 6 of the source
note.

What the samples do show, and no more.  In the verifier's \(4000\)-instance
class-B′ samples, cut-clean failures occur at \(k=10\) (\(20\) of \(4000\))
and were not observed at \(k=8\) (\(0\) of \(4000\)) or \(k=12\) (\(0\) of
\(4000\)).  The stored \(k=10\) witness has **five** colours of the minimum
support \(|V_c|=n-5=2\); such a colour is pinned to a single edge, which is
what makes these instances rigid.  At \(k=16\) the minimum support is \(8\)
out of \(13\), so every colour class is a matching missing at most five of the
thirteen vertices.  That is a difference of regime, not a proof, and the
non-cut mechanism at \(k=10\) has not been characterised.

## 5. Class B is strictly larger than class B′

The distinction matters, because a counterexample in class B need not be a
counterexample for the fan.  At \(k=10\) the pattern "all five vertices of
\(Y\) forbid the same five colours" lies in class B, but not in class B′:
each of the other six colours would have to occupy \(5-2t_c\le|X|=2\)
columns of the array, forcing \(t_c=2\) for all six and
\(\sum_ct_c=12\ne10=\binom53\).  That is why the stored \(k=10\)
certificate is a different instance from the \(k=12\) one.

## 6. Search evidence at \(k=16\)

No infeasible palette was found at \(k=16\), in class B′ or even in the
strictly larger class B.  Exact counts, reproduced verbatim in `RUN_LOG.txt`:

| driver mode | class | seed | instances | completed | not completed |
|---|---|---|---|---|---|
| `random` | B′ | 14335 | 8000 | 8000 | 0 |
| `random` | B′ | 20260727 | 8000 | 8000 | 0 |
| `climb` | B′ | 14335 | 8000 | 8000 | 0 |
| `structured` | B′ | 777 | 2000 | 2000 | 0 |
| `classb` | B | 14335 | 8000 | 8000 | 0 |
| `classb` | B | 991 | 8000 | 8000 | 0 |
| verifier smoke | B′ | 20260727 | 300 | 300 | 0 |

That is \(42{,}300\) palettes, of which \(16{,}000\) are class B but not
required to be class B′.  Every completion was re-checked from the definition.
The `structured` run was stopped at its \(2000\)-instance checkpoint rather
than its \(4000\) target, so its row reports the checkpoint, not a finished
run.  **This is evidence, not a theorem.**

One methodological point, recorded because it nearly produced a false
positive.  The deterministic value ordering of `solve` is pathological on some
highly symmetric *satisfiable* instances of the `structured` family: one such
instance exhausted a \(2\times10^7\)-node budget, and randomised restarts then
completed it in \(79\) nodes.  A `BUDGET` verdict is therefore never evidence
of infeasibility, and the search retries every `BUDGET` instance with
`solve_randomised` before recording anything.  Only `UNSAT` — a finished
exhaustive search — and a violated cut inequality are treated as proofs of
infeasibility anywhere in this note.

## 7. The nested remaining questions

Theorem B removes the only obstruction known to make the first lift fail, and
Section 4 shows that removing it is not enough.  A strong self-contained
completion question is:

> **Strong class-B question.**  Let \(A\) be a \(13\)-set,
> \({\cal C}\) a \(17\)-set, and for each \(a\in A\) let
> \(S_a\subseteq{\cal C}\) with \(|S_a|=5\), such that every colour lies
> in an odd number, at most five, of the \(S_a\).  Must \(E(K_A)\)
> partition into \(17\) matchings \(M_c\) with
> \(V(M_c)=\{a:c\notin S_a\}\)?

The parity clause is essential: it makes every
\(|V(M_c)|=13-|\{a:c\in S_a\}|\) even.  This is exactly the class-B
question defined in Section 0.

The exact **class-B′ extension question** is its restriction to incidence
matrices admitting the additional local \(K_5\) witness in Section 0.  That
restricted question is equivalent to asking whether every proper
\(17\)-edge-colouring of \(K_{18}-E(K_{13})\), in which the five vertices
outside the hole are saturated, extends to a one-factorization of
\(K_{18}\).  Equivalently, must every \(5\times18\) latin rectangle whose
\(5\times5\) principal block is symmetric with constant diagonal complete
to a symmetric latin square of order \(18\) with constant diagonal?

The tower needs still less: only the class-C instances realised by the
chosen simultaneous fan.  Thus a “yes” for class B proves the class-B′ and
class-C cases and closes item 1 of Section 6 of the source note.  A “no” in
class B alone does not refute either smaller question; the counterexample
would next have to pass the class-B′ test and then be shown fan-realisable.

Concrete next steps, in order of expected payoff:

1. Settle the Question above for class B.  It is a self-contained statement
   about completing a one-factorization of \(K_{18}\) across a \(K_{13}\)
   hole.  Two remarks on why the obvious tools do not close it, both checked
   here rather than taken on authority:

   * *Amalgamation/detachment is not directly applicable.*  Amalgamating all
     of \(A\) to a single vertex \(\alpha\) of multiplicity \(13\) does give a
     legitimate outline: colour \(c\) then has \(t_c\) edges inside \(P\),
     \(m_c=5-2t_c\) edges \(P\alpha\), and \(4+t_c\) loops at \(\alpha\), so
     \(\deg_c(\alpha)=(5-2t_c)+2(4+t_c)=13\) for every colour, exactly the
     multiplicity of \(\alpha\).  But the amalgamation **forgets which
     \(a\in A\) each cross edge attaches to**, and that assignment is
     precisely what \(\phi_P\) prescribes, so a detachment theorem returns
     *some* one-factorization with the same outline, not an extension of
     \(\phi_P\).
   * *Cruse-type embedding is the mirror image of the class-B′ extension
     problem.*  Cruse's
     theorem and its relatives assume the **known** cells form a principal
     block; here the **unknown** cells do.  In latin-square language the
     class-B′ question asks whether every \(5\times18\) latin rectangle whose
     \(5\times5\) principal block is symmetric with constant diagonal is
     completable to a symmetric latin square with constant diagonal.  The
     \(2\times n\) case of exactly this completion problem is the
     subject of Bryant and Rodger, *On the completion of latin rectangles to
     symmetric latin squares*, J. Austral. Math. Soc. **76** (2004) 109–124,
     which also treats the unipotent case separately (**pointer only — the
     abstract was read via web search, the paper was not obtained, and no
     statement of it is used anywhere in this note**).  The case needed here
     is \(r=5\), \(n=18\), unipotent.

   This repository contains no prior work on any of this (zero occurrences of
   "amalgamation", "detachment", "Cruse", "Hilton").
2. If the answer is yes for class B, item 1 of Section 6 of the source note is
   closed unconditionally and the whole first lift reduces to the coupling
   (17).
3. If a class-B counterexample exists, decide class-B′ membership for it by
   the finite test in `check_class_Bprime`, and only then ask about class C.

## 8. Verification

Run:

```sh
cd collaboration/opus5/first_lift_k13_hole && \
  python3 -B verify_first_lift_obstruction.py
```

The verifier is deterministic and standard-library-only.  In order, it

1. re-derives the admissible multiplicity profiles for \(n=3,\dots,13\) and
   the identities \(\sum_c|V_c|=156\), \(\sum_ch_c=78\), \(n_3=24-2n_5\),
   \(n_1=n_5-7\); enumerates and re-checks all \(332\) partitions of
   \(E(K_5)\) into matchings; and runs the level-0 packing count for
   \(k=6,\dots,18\), confirming that no link exists at \(k=8\) and \(k=14\);
2. cross-validates the exact completion solver against an independent
   heuristic-free brute-force search on \(600\) instances at \(k=8\), and
   against the randomised-restart solver on \(200\) instances at \(k=12\);
3. checks on \(3\times4000\) class-B′ instances at \(k=8,10,12\) that no
   completable instance ever violates Lemma 1;
4. re-checks all four Theorem-A certificates from the definitions, including
   their class-B′ witnesses, re-derives each certificate value, and runs the
   exhaustive solver on the three with \(n\le9\);
5. re-checks the cut-insufficiency certificate: all \(127\) subsets clean,
   solver UNSAT;
6. recomputes every cut margin of Theorem B by exact dynamic programming, for
   \(n=3,5,\dots,31\), and asserts the fire-set is exactly
   \(k\in\{8,10,12,14\}\);
7. checks the amalgamation-outline arithmetic and the class B versus class B′
   separation of Section 5;
8. draws \(300\) fresh class-B′ palettes at \(k=16\), verifies Lemma 1 holds
   for all of them, completes each, and re-checks each completion.

The certificates in `certificates/` were produced by `find_certificates.py`
and the \(k=16\) counts by `search_k16.py`; both are search drivers whose
output is not itself evidence — only the verifier's is.
