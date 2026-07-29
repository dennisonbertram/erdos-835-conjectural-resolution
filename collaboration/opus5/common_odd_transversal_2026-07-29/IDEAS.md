# Ideas, rejected routes, countermodels, and the one remaining lemma

Companion to `PROOF.md` and `STATUS.md`.  Nothing here is claimed as proved.

---

## 1.  The single best remaining lemma

### Lemma LLS (Local Link Sufficiency) — the converse of Corollary 3.4

> At a rung `(t, n, p)` with `p` odd and `p-2` pairwise disjoint
> `S(t,t+1,n)`'s: the residual conflict graph `G` is bipartite **if and only
> if** for every `A_0` in `C(X,t-1)` the link 2-factor `R(A_0)` is a disjoint
> union of even cycles.

"only if" is **proved** (Corollary 3.4).  "if" is the open half.

**Why this is strictly stronger than the current equivalence.**  The audited
equivalence replaces one global question by another global question: a
solvability test for a `binom(n,t+2)`-by-`|D|` system over F_2, or equivalently
a search for an odd cycle in a graph on `2 lambda_0` vertices.  LLS would
replace it by `binom(n,t-1)` **independent local** questions, each of which
asks only whether `p-2` pairwise disjoint one-factors of `K_{p+1}` leave a
bipartite 2-factor.  That is a statement about one-factorisation deficiency
in a complete graph on `p+1` points — no Steiner data survives into it beyond
the `p-2` matchings.  A global condition would become a finite, uniform,
parameter-sized condition.

**Equivalent linear-algebra form.**  Let `Z_1(G;F_2)` be the cycle space and
let `L <= Z_1(G;F_2)` be the span of the link cycles of Theorem 3.3.  Let
`l : Z_1 -> F_2` be the length-parity functional.  Then LLS for a given family
says `l|_L = 0  =>  l = 0`.  A sufficient condition, uniform in the family, is

> **LLS-span.**  The link cycles span `Z_1(G;F_2)`.

LLS-span is a purely combinatorial, checkable statement.  It is the concrete
thing to test.

**Evidence for.**
* LLS is **true at `t = 1`**, and there trivially: `C(X,0) = {empty}`, the
  single link is the whole residual 2-factor, and `G` is literally its line
  graph (Corollary 3.5).  So LLS is a genuine generalisation of a true base
  case, not a guess.
* The repository's only authenticated negative certificate at any rung is a
  link cycle (Proposition 3.6).  If odd cycles could occur away from links, it
  is mildly surprising that the one found example is local.

**Evidence against / what could break it.**
* The link cycles are highly non-independent: each edge of `G` lies in
  exactly `t` links, so there are many relations, and the span could fall
  short by a subspace on which `l` is nonzero.
* The independent verifier confirms that this span does fall short on both
  available controls: `11 < 13` on the positive `LS(2,3,9)` example and
  `467 < 587` on the negative Etzion--Hartman example. Thus the proposed
  sufficient statement **LLS-span is false**, even though LLS itself remains
  consistent with both controls.
* No proof strategy is visible that does not amount to a local-to-global
  (sheaf / `H^1`-vanishing) argument, and the obstruction to such arguments is
  exactly the failure of the link cover to be simply connected.

**How to decide it, today, with objects the repository already owns.**
1. `LS(2,3,9)` positive control, `(t,n,p) = (2,9,7)`, take 5 of the 7 systems.
   `A_0` ranges over the 9 points; `Y` has 8 points; each `R(A_0)` is a
   2-factor on 8 vertices.  `G` has 24 vertices and 36 edges.  Compute
   `dim Z_1(G)` and `dim L`.  If they are equal, LLS-span holds on a genuine
   bipartite instance.
2. Etzion--Hartman fixed partial, `(3,20,17)`, 15 systems, at
   `collaboration/ls3420_branch0_search/eh15_branch0_partial.txt`.  Here `G`
   is known non-bipartite and a link odd cycle is known.  Compute `dim L`
   versus `dim Z_1(G)` on the same instance.
3. The decisive experiment: search the repository's other 15-system
   `LS(3,4,20)` partials for one where **every** `R(A_0)` is a union of even
   cycles but `G` is still non-bipartite.  That is a countermodel to LLS with
   real Steiner data at a real rung.

`verify_common_odd_transversal.py` implements (1) and (2). The independent
run passed after correction of the Part E colour parser and produced the
dimensions above; see `STATUS.md`.

---

## 2.  Routes tried and rejected

### 2.1  Abstract partition countermodel — rejected as non-evidence

It is easy to build `k-1` partitions of an abstract set into cells of size `k`,
pairwise meeting in at most one point, with no common odd transversal.  The
smallest interesting shape is already visible in the link: three pairwise
disjoint one-factors of `K_6` whose residual is two triangles (the complement
of two disjoint triangles in `K_6` is `K_{3,3}`, which one-factorises into
exactly three matchings).  That is a legitimate deficiency configuration.

It is **not** a countermodel to (COT), for a reason that turned out to be
decisive rather than technical: at `k = 4` the top-rung hypothesis does not
hold at all (Theorem 5.1).  So the abstract configuration cannot be lifted.
Every attempt to build a countermodel from abstract partitions ran into the
same wall — the Steiner and complement geometry is not an extra constraint on
top of an otherwise-satisfiable problem, it is the *only* thing that decides
whether the problem has an instance.

### 2.2  Killing (COT) by a new global parity invariant — rejected

I looked for an invariant beyond the four already known to be vacuous
(row parity, column parity, Catalan parity, the `e_i + e_j` design
differences).  Three candidates were tried and all failed:

* **Symmetric-function transversals.**  Setting `a(A) = f(|A ∩ Y|)` for a
  fixed `Y` gives cell sum `m ( f(m-1) + f(m) )` where `m = |C ∩ Y|`, using
  `k` even.  This is `0` whenever `m = 0`, so it can never be `1` on all
  cells.  All such ansätze die at cells disjoint from `Y`.  (This includes the
  single-star `a(A) = [x in A]`, already known vacuous.)
* **Intersection-number / Johnson-scheme positivity.**  Theorem 2.1 shows the
  intersection distribution of a top system is *completely forced* and, worse
  for this route, is the same for every pair of systems.  Nonnegativity and
  integrality of `N_i` and `m_i` hold automatically whenever `k+1` is prime.
  So no counting contradiction is available at the pair level.  This closes
  the "quadratic refinement of the simplex boundary form" direction as a
  source of a *parameter-only* obstruction: the quadratic data is constant.
* **Pfaffian / Arf.**  The natural quadratic refinement here would live on
  `Z_1(G;F_2)` with `l` as its linear part.  But Theorem 4.1 shows the only
  canonical extra structure is the free `Z/2` action, whose invariant is a
  class in `H^1(Gbar;F_2)`, not a quadratic form.  I could not produce a
  well-defined quadratic refinement; the candidate `q(cycle) = (length/2 mod 2)`
  is not well defined on `F_2` cycle classes.

### 2.3  Bounding disjointness uniformly in `k` — attempted, incomplete

If one could show `M(k) < k-1` for **all** admissible `k` — where `M(k)` is
the maximum number of pairwise disjoint `S(k-1,k,2k)`'s — #835 would be
settled negatively, since a large set contains `k-1` disjoint systems.
Theorem 5.1 does exactly this for every decided `k`.  The obstruction to
making it uniform:

* The link tower (Theorem 6.1) has the counting upper bound `k+1` at every
  rung, and a hypothetical top large set would attain that bound after every
  derivation. Pure counting alone never gives anything below `k+1`. Thus the
  tower gives `M(k) <= min_t D(t, k+1+t)` only when an independent bound on
  the relevant packing number `D` is supplied.
* At `k = 16` the tower inputs are all satisfiable as far as anything is
  known: `LS(2,3,19)` exists, and 15 pairwise disjoint `SQS(20)` exist — that
  is precisely the Etzion--Hartman object.  So the tower cannot kill `k = 16`.
* Each of `k = 4, 6, 10, 12` dies for a *different* reason, and two of them
  (Kramer--Mesner, Östergård--Pottonen) are computations, not structure.
  There is no visible common mechanism to generalise.

Verdict: the uniform-`M(k)` route is the highest-value target, but nothing in
the link tower, the intersection numbers, or the complement quotient supplies
the missing input.

### 2.4  The complement quotient as an obstruction — partly productive

Theorem 4.1 is proved and does halve the object.  What it does **not** do:
`G` bipartite ⟺ `Gbar` bipartite means the double cover carries no extra
information about bipartiteness, so the `Z/2` class does not obstruct by
itself.  Where it *is* useful is Corollary 4.2 — the odd complement-walk
certificate.  That is a strictly larger certificate family than odd cycles
(open walks, one available at each of the `2 C_k` residual blocks), and it is
cheap to search.  Untested: no top-rung instance exists to test it on.

### 2.5  Coupling to the adjacent rung — not pursued to a conclusion

The natural coupling is Theorem 6.2 (large sets propagate down).  The upward
direction — a partial at rung `t` forcing structure at rung `t+1` — is what
the repository's post-`r0` bridge work targets.  I did not find a new handle;
the link theorem only goes down.

---

## 3.  Countermodels found, and their exact status

| Object | Real? | Refutes (COT)? | Why |
|---|---|---|---|
| Three disjoint one-factors of `K_6` with residual = two triangles | Yes, a genuine graph | **No** | It is a link at `k = 4`, where no 3 disjoint `S(3,4,8)` exist (Thm 5.1). Diagnostic only. |
| Etzion--Hartman 15-system partial at `(3,20,17)` | Yes, authenticated in-repo | **No** | Lower rung `t = 3`, not the top rung; and it is one fixed partial, not a universal statement. It *does* confirm Cor 3.4 (Prop 3.6). |
| Abstract `k-1` partitions with an odd kernel vector | Constructible | **No** | Violates Steiner/complement geometry; and the top-rung hypothesis is empty below `k = 16`. |

No countermodel to (COT) exists in the repository or was constructed here, and
Theorem 5.1 explains why: below `k = 16` there is nothing to build one from.

---

## 4.  Recommended next step, in one line

Search authenticated 15-system `S(3,4,20)` partials for a family whose every
link 2-factor is even while its global conflict graph is non-bipartite. Such
an object would refute LLS; absent one, a proof must control the parity
functional on the quotient `Z_1(G)/L`, since equality `L=Z_1(G)` is now
disproved on both controls.
