# LS(3,4,20) and S(4,5,21): structure, audits, and a lossless branch

> **Subsequent exact improvement (2026-07-26).**  The 55-way decomposition
> below remains correct, but a four-bijection parity lemma now proves that
> every \(LS(3,4,20)\) can be relabelled into one of the 28
> even-permutation branches.  The Etzion--Hartman partial also relabels
> exactly from branch 54 to branch 0.  See
> [`LS3420_EVEN_FLAG_REDUCTION.md`](../../ls3420_structural_attack/LS3420_EVEN_FLAG_REDUCTION.md).

**Scope, stated first.** Neither target is resolved. **Erdős–Rosenfeld #835
remains open.** I found no construction and no obstruction for either
LS(3,4,20) or S(4,5,21). What is delivered is: an audit of both WLOG
normalizations (both sound), a new structure theorem for LS(3,4,20), a
provably lossless 55-way cube decomposition, and one sound CNF strengthening
that is currently missing.

Even a checked UNSAT for LS(3,4,20), or for all seven S(4,5,21) branches,
would exclude **k = 16 only** — every other prime case would remain, so #835
would still be open. A SAT witness for either is a necessary shadow, not a
solution.

Verifier (stdlib only, no solver; reads two committed files read-only and
modifies nothing under `evidence/`):

```sh
python3 -B collaboration/opus5/radius5_followup/verify_ls3420_structure_and_branching.py
```

---

## 1. Audit of the seven S(4,5,21) branches — **SOUND**

The argument in `evidence/audit_s_4_5_21_cnf.md` is correct. Re-derived
independently:

1. WLOG `01234` is a block (relabelling only).
2. The blocks through `012` induce a perfect matching on the other 18 points,
   because each of the 18 four-sets \(\{0,1,2,x\}\) lies in exactly one block
   \(\{0,1,2,x,y\}\). It contains `34` because `01234` is a block.
3. Relabelling the 16 points off the anchor normalizes the remaining eight
   edges to `56,78,…,19-20`.
4. Blocks through `013` give a second perfect matching containing `24`.
5. **Disjointness on the 16 points is forced**: a common edge \(\{x,y\}\) would
   put the 4-set \(\{0,1,x,y\}\) into both \(\{0,1,2,x,y\}\) and
   \(\{0,1,3,x,y\}\), contradicting \(t=4\).
6. Two disjoint perfect matchings on 16 points union to alternating even
   cycles of length \(\ge 4\); half-lengths partition 8 with all parts \(\ge2\).
7. Under \(\mathrm{Stab}(M_1)\) the orbit of \(M_2\) is determined by that
   partition.

The count is exactly right: partitions of 8 with all parts \(\ge 2\) number
\(p(8)-p(7)=22-15=7\), and the verifier lists them —
\((2,2,2,2),(2,2,4),(2,3,3),(2,6),(3,5),(4,4),(8)\).

**One observation, not a defect.** The normalization uses only the relabelling
of the 16 non-anchor points; the \(5!\) relabellings **within** the anchor block
`01234` are never used, and they change which pair of triples defines
\(M_1,M_2\). So the seven branches need not be pairwise non-isomorphic — the
same \(S(4,5,21)\) may satisfy several. That is harmless for exhaustiveness
(which is what an UNSAT sweep needs), but it means **seven is an upper bound**
on the number of genuinely distinct cases, and a sharper argument could
plausibly remove some. I did not carry that out.

The note's own caveat stands and is correct: the DIMACS audit does not validate
a DRAT proof, so no UNSAT case may be treated as certified without an
independent proof checker.

---

## 2. Audit of the canonical LS(3,4,20) CNF — **SOUND**, with a gap

Dimensions recomputed independently from \((v,k,t,\text{colours})=(20,4,3,17)\):

| quantity | value | recomputed as |
|---|---|---|
| primary variables | 82,365 | \(4845\times17\) |
| Sinz auxiliaries | 77,520 | \(4845\times16\) |
| block at-least-one | 4,845 | one per block |
| block at-most-one | 227,715 | \(4845\times(3\cdot17-4)\) |
| star at-least-one | 19,380 | \(1140\times17\) |
| symmetry units | 17 | |
| **total clauses** | **251,957** | sums correctly |

**The symmetry breaking is lossless.** Each colour class is an \(S(3,4,20)\),
so it contains exactly one of the 17 extensions of \(\{0,1,2\}\); those 17
blocks therefore realise all 17 colours bijectively, and the free
\(\mathrm{Sym}(17)\) colour action can always put them in point order. The
README's claim that this "removes only the free global colour permutation" is
correct — it consumes the colour symmetry entirely and the \(\mathrm{Sym}(20)\)
point symmetry not at all.

### The gap: missing implied clauses

The encoding has star **at-least-one** but no star **at-most-one**. Exactly-one
per (triple, colour) *is* implied — each of the 17 extensions of a triple
carries exactly one colour and all 17 colours occur, so by pigeonhole each
occurs exactly once — but only through a global counting argument that unit
propagation cannot see.

> Adding the at-most-one side is **sound and solution-preserving**:
> \(1140\times17\times\binom{17}{2}=2{,}635{,}680\) binary clauses
> \(\neg x_{B,c}\vee\neg x_{B',c}\) for blocks \(B\ne B'\) extending a common
> triple.

This is a lossless strengthening, not a new constraint. It is the single
cheapest change likely to matter to a solver on this instance. (I did not
regenerate the committed CNF — the active evidence files were not to be
edited.)

---

## 3. New: every pair induces a one-factorization of \(K_{18}\)

> **Theorem.** Let \(c\) be an \(LS(3,4,20)\) colouring. Fix a pair
> \(\{a,b\}\subset[20]\) and put \(W=[20]\setminus\{a,b\}\), \(|W|=18\). Then
> \[
>  \varphi_{ab}(\{q,y\})=c(\{a,b,q,y\})
> \]
> is a proper edge colouring of \(K_W\) in which every vertex sees all 17
> colours — a **one-factorization of \(K_{18}\)**.

*Proof.* Fix \(q\in W\). For distinct \(y,y'\in W\setminus\{q\}\) the blocks
\(\{a,b,q,y\}\) and \(\{a,b,q,y'\}\) both contain the triple \(\{a,b,q\}\); a
colour class is an \(S(3,4,20)\) and so contains exactly one extension of that
triple, hence the two colours differ. So \(y\mapsto\varphi_{ab}(\{q,y\})\) is
injective from the 17 points of \(W\setminus\{q\}\) into 17 colours, hence
bijective. \(\square\)

> **Corollary (discordance).** If \(\{a,b\}\) and \(\{a,d\}\) share a point,
> then \(\varphi_{ab}(\{q,y\})\ne\varphi_{ad}(\{q,y\})\) for all \(q,y\) outside
> \(\{a,b,d\}\): the blocks \(\{a,b,q,y\}\) and \(\{a,d,q,y\}\) are distinct and
> share the triple \(\{a,q,y\}\). \(\square\)

So an \(LS(3,4,20)\) carries \(\binom{20}{2}=190\) one-factorizations of
\(K_{18}\), pairwise discordant whenever the index pairs intersect.

**Normalized form.** Identify the 17 colours with \(Q=[20]\setminus\{0,1,2\}\)
via \(c(\{0,1,2,q\})=q\) — exactly the CNF's symmetry units. Then for
\(\{a,b\}\in\{01,02,12\}\), setting \(S_{ab}(q,q)=q\) makes each \(S_{ab}\) a
**symmetric idempotent Latin square of order 17** on \(Q\), and the three are
pairwise discordant off the diagonal.

This is the same species of object as the radius-3 ball reduction
(`evidence/odd_graph_local_ball/lmn_large_set.md`), which needs 15 pairwise
discordant such squares. Here only 3 are required, and 3 certainly exist (the
Wallis family supplies 15), so **this is structure, not an obstruction** — I
state that explicitly to avoid it being read as a no-go.

**Checked against real data.** Against the verified Etzion–Hartman partial
(`evidence/ls_3_4_20_eh15_partial.txt`): 4,773 coloured blocks, 72 uncoloured;
15 complete colour classes of 285 each, verified to be genuine \(S(3,4,20)\)s,
plus two partial classes of 249. Over all 190 pairs, the partial
one-factorization property holds with **0 violations in 28,638 coloured cells**,
and discordance for intersecting pairs holds with **0 violations**.

---

## 4. New: a lossless 55-way cube decomposition for LS(3,4,20)

After the colour normalization the residual symmetry is
\(\mathrm{Sym}\{0,1,2\}\times\mathrm{Sym}(Q)\) with \(|Q|=17\), where
\(\mathrm{Sym}(Q)\) permutes points and colours together. \(\mathrm{Sym}(Q)\) is
transitive, so fix \(q_0\in Q\). Row \(q_0\) of \(S_{01}\) is a **derangement**
\(g\) of \(Q\setminus\{q_0\}\) (16 points), since \(S_{01}(q_0,y)\ne y\). The
stabiliser \(\mathrm{Sym}(Q\setminus\{q_0\})\) acts on \(g\) by conjugation, so
the **cycle type of \(g\) is a complete lossless branch label**.

Partitions of 16 with all parts \(\ge2\) number \(p(16)-p(15)=231-176=55\).

> A provably lossless **55-way** cube decomposition, breaking a residual
> symmetry of order \(6\cdot17!\approx2.1\times10^{15}\) down to the centralizer
> of \(g\) within each branch.

Not all 55 types need be realisable, so 55 is an upper bound on the branch
count — which is exactly what exhaustiveness requires. I checked whether the
row derangement is forced to be an involution (which would collapse this to one
branch): **it is not.** At order 5 every row is a 4-cycle; at order 7 all four
derangement types \((2,2,2),(2,4),(3,3),(6)\) occur among the 6,240 squares.

### The Etzion--Hartman near-completion lies in branch 54

The verified 4,773-block Etzion--Hartman partial assigns every block in the
chosen second-star row.  Relabel its old colours by the canonical root-star
rule \(c(\{0,1,2,q\})=q\).  The resulting permutation on
\(\{4,\ldots,19\}\) is
\[
4\mapsto19\mapsto14\mapsto7\mapsto10\mapsto9\mapsto12\mapsto5
\mapsto8\mapsto13\mapsto16\mapsto17\mapsto15\mapsto6\mapsto11
\mapsto18\mapsto4.
\]
It is one 16-cycle, which is branch 54 in the deterministic ordering.  The
verifier derives this directly from the checked partial file.  This makes
branch 54 the natural targeted completion search; it does **not** make that
branch WLOG for arbitrary solutions.

---

## 5. Controls

* **k = 4 fires correctly.** The shadow at \(k\) is \(LS(3,4,k+4)\); at \(k=4\)
  that is \(LS(3,4,8)\), needing 5 disjoint SQS(8) among the 70 quadruples.
  Exhaustively: there are 30 labelled SQS(8) and the maximum pairwise
  block-disjoint family has size **2 < 5**. So \(LS(3,4,8)\) is impossible and
  the shadow correctly excludes \(k=4\).
* **k = 2 is vacuous here.** The same shadow would need SQS(6), which does not
  exist (\(6\not\equiv2,4\bmod 6\)). So this test cannot produce a false
  positive at \(k=2\), but neither is that evidence of calibration. Stated
  plainly rather than counted as a passed control.

---

## 6. What was not achieved

* No construction of \(LS(3,4,20)\) or \(S(4,5,21)\), and no obstruction to
  either. Both remain open.
* No reduction in the seven \(S(4,5,21)\) branches, though §1 shows the
  possibility is open.
* The 55-way branch is proved lossless but was **not executed** — no solver was
  launched, per the standing instruction.
* Nothing here bears on prime cases other than \(k=16\).
