# Audit and algebraic attack on the fixed cyclic \(LS(2,3,19)\) extension

## 0. Scope, stated first

**Erdős–Rosenfeld problem #835 remains OPEN.**  No SAT or UNSAT verdict is
asserted here, and none from any solver is used.  Exact scopes:

* **SAT** for the fixed-link instance would construct a complete
  \(LS(3,4,20)\) — a genuine object and a necessary shadow of \(k=16\) — but
  would **not** settle #835.
* **UNSAT** for the fixed-link instance would exclude every \(LS(3,4,20)\)
  possessing, **at any point**, a link isomorphic to this one as a coloured
  design (i.e. up to relabelling points *and* colours).  It would say nothing
  about \(LS(3,4,20)\) with only non-isomorphic links, nor about \(k=16\) or
  #835.
* The \(C_{17}\)-equivariant subproblem is a **restricted ansatz**; its UNSAT
  would exclude only equivariant completions of this one link.

**Reading convention.**  Statements below are marked as *written proofs*
(mathematics, argued here) or as *executable checks* (arithmetic and finite
enumeration on the artifacts, performed by the verifier).  Where an external
theorem is cited, it is cited and not re-proved.  The verifier
`verify_cyclic_lsts19_extension_attack.py` runs **63 checks**, standard library
only, no solver, Ruff clean.

## 1. Audit of the committed artifacts

`collaboration/cyclic_lsts19_extension/{generate_fixed_link_cnf.py,
verify_fixed_link_cnf.py,README.md}` were re-run and independently re-derived.
*Executable checks*, all passing:

* the generator reproduces both committed digests exactly — units
  `fdf715ea…81846`, augmented CNF `a187094a…3c65c` — and the written file
  really hashes to the second;
* header `p cnf 159885 252909` with \(252\,909=251\,957+952\): parent clauses
  untouched, exactly \(952\) units appended;
* \(159\,885=4845\cdot33\), i.e. \(17\) primary plus \(16\) auxiliary variables
  per quadruple.  *Not audited: the parent CNF's internal encoding, referenced
  by hash and outside the three named files.*
* the committed verifier returns `status: PASS` and itself asserts no verdict;
* the fixed link is independently re-verified to be a genuine
  \(LS(2,3,19)\) — \(17\) colour classes of \(57\) triples, each covering all
  \(171\) pairs once — and to be \(C_{17}\)-**covariant**;
* both Wallis starters are idempotent symmetric Latin squares:
  \(s[0]=0\), \(s\) a permutation, \(s[d]-s[-d]\equiv d\).

I found no error in the three audited files.

**Notation.** \(19=\mathbb Z_{17}\sqcup\{L,\infty\}\), colours
\(\mathbb Z_{17}\), starters \(s_0\) (for \(L\)), \(s_1\) (for \(\infty\)):
\[
\{L,\infty,x\}\mapsto x,\quad
\{L,x,y\}\mapsto s_0[x-y]+y,\quad
\{\infty,x,y\}\mapsto s_1[x-y]+y,
\]
finite triples coloured by orbit phase.  The \(LS(3,4,20)\) root is point \(0\).

## 2. Theorem A: which symmetries are without loss of generality

> **Theorem A** *(written proof; the arithmetic is executable).*
> **(i)** Fixing *which* point of \([20]\) is the root **is** WLOG:
> \(S_{20}\) is transitive on points.
> **(ii)** Fixing the root link to *this* cyclic \(LS(2,3,19)\) is **not known
> or justified to be** WLOG.  It would be WLOG exactly if every
> \(LS(3,4,20)\) had some point whose link is isomorphic to it; whether that
> holds is unknown, and no claim is made either way.
> **(iii)** Imposing \(C_{17}\)-equivariance is **not** WLOG, but it is not
> arbitrary: the fixed link is \(C_{17}\)-covariant, so the group acts on the
> set \(X\) of completions, and since \(17\) is prime every orbit has size
> \(1\) or \(17\), giving
> \[
> \boxed{\;|X|\equiv\bigl|X^{C_{17}}\bigr|\pmod{17}.\;}
> \]

*Proof of (iii).*  Let \(\sigma\) fix the root and \(L,\infty\), translate the
finite points by one, and send colours \(c\mapsto c+1\).  Covariance makes
\(\sigma\) an automorphism of the fixed link as a coloured object, so it
permutes completions; orbits in a group of prime order have size \(1\) or
\(17\). \(\square\)

Consequences: equivariant UNSAT gives \(17\mid|X|\), so *if any completion
exists, at least seventeen do*; and proving \(|X|\not\equiv0\pmod{17}\) would
force an equivariant completion, upgrading the small search from restricted to
complete.

**On (ii) and the UNSAT scope.**  Because both points and colours may be
relabelled, an UNSAT verdict is stronger than "this labelled link fails": it
excludes every \(LS(3,4,20)\) having a link isomorphic to this one *at any of
its twenty points*.  It remains silent about large sets all of whose links are
non-isomorphic to it.

## 3. Theorem B: no first-moment obstruction over \(\mathbb F_{17}\)

For a triple \(T\subset[19]\) the \(16\) quadruples \(T\cup\{x\}\subset[19]\)
must carry the \(16\) colours other than \(\mathrm{link}(T)\).  Since
\(\sum_{c\in\mathbb Z_{17}}c=136\equiv0\), summing gives the linear condition
\[
\sum_{x\in[19]\setminus T}\mathrm{colour}(T\cup\{x\})\equiv-\mathrm{link}(T)
\pmod{17},
\]
i.e. \(969\) equations in \(3876\) unknowns with matrix \(W=W_{3,4}(19)\).

> **Theorem B** *(written proof; eigenvalues executable).*  \(W\) has full row
> rank \(969\) over \(\mathbb F_{17}\).  Hence the first-moment system is
> consistent **for every link whatsoever**, with solution space of dimension
> \(3876-969=2907\).  Thus **this linear first-moment system alone cannot
> obstruct the fixed-link problem.**

*Proof.*  \(WW^{\!\top}=16I+A\) with \(A\) the adjacency matrix of \(J(19,3)\),
whose eigenvalues are \(3\cdot16-j(20-j)\), \(j=0,\dots,3\).  So
\(WW^{\!\top}\) has eigenvalues \(64,45,28,13\) with multiplicities
\(1,18,152,798\) (summing to \(969\)), which mod \(17\) are \(13,11,11,13\) —
all nonzero.  So \(WW^{\!\top}\) is invertible over \(\mathbb F_{17}\) and
\(W\) has full row rank. \(\square\)

**Tower remark (cited, not proved here).**  Wilson's diagonal form of
\(W_{t,t+1}(n)\) has diagonal entries \(1,2,\dots,t+1\).  In the \(k=16\) tower
the colour count is the prime \(17\) at every level while \(t+1\le15<17\), so
all those entries are units mod \(17\) and the first-moment relaxation is
vacuous at every level.  **The verifier does not prove Wilson's theorem**; the
rank fact actually used above is proved directly by the eigenvalue
computation.

**The moment conditions do not stop at \(k=1\), and \(k\le15\) is not enough.**
The rainbow condition at \(T\) is equivalent to the product identity
\[
\prod_{i=1}^{16}(z-v_i)=\frac{z^{17}-z}{z-m},\qquad m=\mathrm{link}(T),
\]
equivalently to the power sums \(p_k\equiv-m^k\) for \(k=1,\dots,16\) — all of
\(1,\dots,16\) are invertible mod \(17\), so Newton's identities recover
\(e_1,\dots,e_{16}\) from \(p_1,\dots,p_{16}\).  **The range \(k=1,\dots,15\)
alone is not equivalent**: with \(m=0\) the all-zero assignment gives
\(p_k=0=-m^k\) for every \(k\le15\) yet is not rainbow.  It is \(k=16\) that
separates: the target is \(\sum_{c}c^{16}-m^{16}=16-0=-1\), while the all-zero
assignment gives \(0\).  (Alternatively one may keep \(k\le15\) and add the
hypothesis \(m\notin\{v_i\}\).)  Only \(k=1\) is linear, which is why
Theorem B kills exactly that layer and no more.

## 4. Theorem C: the type-(i) layer

*Executable orbit census.*  All \(C_{17}\) orbits have size exactly \(17\)
(\(17\) is prime and fixed-point-free on \(\mathbb Z_{17}\); no block fits in
\(\{L,\infty\}\)):

| | \(|Q\cap\{L,\infty\}|=2\) | \(=1\) | \(=0\) | total |
|---|---|---|---|---|
| quadruple orbits | 8 | 40 + 40 | 140 | **228** |
| triple orbits | 1 | 8 + 8 | 40 | **57** |

Call the \(8\) orbits of blocks \(\{L,\infty,x,y\}\) the **type-(i) layer**.

> **Theorem C** *(written proof; feasibility executable).*  Write the covariant
> colour of \(\{L,\infty,x,y\}\) as \(t[x-y]+y\) and set \(a_d:=t[d]-d\).
> **(a)** Well-definedness forces \(t[d]-t[-d]\equiv d\), i.e. \(a_{-d}=a_d+d\).
> **(b)** The triple orbit \(\{L,\infty,x\}\), whose \(16\) extensions are
> *exactly* the type-(i) blocks, forces \(d\mapsto a_d\) to be a bijection of
> \(\mathbb Z_{17}^{*}\).
> **(c)** The triples \(\{L,x,y\}\), \(\{\infty,x,y\}\) each contribute one
> type-(i) extension, forcing \(t[d]\ne s_0[d]\), \(t[d]\ne s_1[d]\); by the
> starter symmetry \(s[d]-d=s[-d]\) these collapse to
> \(a_d\ne s_0[-d]\), \(a_d\ne s_1[-d]\).
> **(d)** So \(a_d\notin\{0,-d,s_0[-d],s_1[-d]\}\) for \(d=1,\dots,8\), and the
> eight dominoes \(\{a_d,a_d+d\}\) must partition \(\mathbb Z_{17}^{*}\).
> **(e)** This eight-variable exact cover is **feasible**.
> **(f)** The midpoint colouring \((x+y)/2\), i.e. \(t[d]=9d\), is **excluded**:
> it clashes with the \(\infty\)-starter at \(d\in\{2,3,5,12,14,15\}\) (never
> with the \(L\)-starter).

*Proof of (b).*  The extensions of \(\{L,\infty,x\}\) are \(\{L,\infty,x,y\}\),
\(y\ne x\); with \(d=x-y\) the colour is \(t[d]+x-d=x+a_d\), and these must be
\(\mathbb Z_{17}\setminus\{x\}\). \(\square\)

**On (e), stated precisely.**  The routine used is **complete backtracking
stopped at its first witness** — not an enumeration.  It returns
\[
(a_1,\dots,a_8)=(3,5,9,11,13,8,16,2),\qquad
t[0..16]=(0,4,7,12,15,1,14,6,10,2,16,8,13,11,9,5,3).
\]
The executable's **complete enumeration** of the same domino cover finds
**\(1326\) solutions**, so the layer is far from rigid.

Theorem C solves exactly the sub-system carried by the type-(i) layer: the
whole triple orbit \(\{L,\infty,x\}\), plus the single \(\ne\) condition each of
the \(16\) orbits \(\{L,x,y\}\), \(\{\infty,x,y\}\) imposes on that layer.  It
leaves the other \(220\) quadruple orbits untouched.

## 5. Audit of the exact-cover formulation

*Executable checks* on
`collaboration/cyclic_lsts19_extension/search_c17_equivariant_exact_cover.py`:

* **2964 rows, 1140 columns; every row has 5 columns, every column 13 rows**,
  and \(2964\cdot5=1140\cdot13=14\,820\);
* \(2964=228\cdot13\): each block orbit forbids exactly four *distinct* phases,
  one per face, leaving thirteen;
* \(1140=228+57\cdot16\): one column per block orbit, plus one per
  (triple orbit, non-root colour) demand;
* **every row meets exactly one orbit column**, so any exact cover selects
  exactly one phase per orbit — precisely \(228\) rows;
* consequently the exact cover is **equivalent** to a \(C_{17}\)-equivariant
  completion: per triple orbit the sixteen extensions then carry sixteen
  distinct non-root colours, which is the rainbow condition.

## 6. Theorem D: the type-(i) witness is a valid branch

> **Theorem D** *(executable).*  Translating the Theorem C witness into the
> exact-cover encoding gives the eight rows
> \(\{1926,3017,3532,3739,3810,3840,3849,3870\}\) — phases
> \(t[d]\) on the orbits with representatives \((0,d,L,\infty)\).  All eight are
> **allowed** rows, they are **pairwise column-disjoint**, they cover \(40\)
> distinct columns (\(8\) orbit \(+\;32\) demand), and after imposing them
> every remaining column still has a candidate row, with residual column sizes
> in \(10..13\).  Hence the witness may be imposed as a **valid branch**.

This answers the posed question affirmatively.  It does **not** show the branch
extends to a full cover, and by the \(1326\) count there are many alternative
type-(i) branches.

## 7. Theorem E: a forced phase-sum; Theorem F: no residual affine symmetry

> **Theorem E** *(written proof; constants executable).*  Sum the colours of
> all \(912\) demand columns two ways.  Per triple orbit the demanded colours
> are \(\mathbb Z_{17}\setminus\{\text{root}\}\), summing to \(-\text{root}\);
> per chosen row \((o,\varphi)\) the four demands are \(\varphi+\text{shift}_i\).
> Hence
> \[
> 4\sum_{o}\varphi_o\;\equiv\;-\sum_{\text{orbits}}\text{root}
> \;-\;\sum_{o,i}\text{shift}_{o,i}\pmod{17},
> \]
> and since \(4\) is invertible the sum of the \(228\) phases is **forced**.
> With the measured constants \(\sum\text{root}\equiv12\) and
> \(\sum\text{shift}\equiv15\),
> \[
> \boxed{\;\sum_{o=1}^{228}\varphi_o\;\equiv\;6\pmod{17}.\;}
> \]
> The Theorem D branch fixes eight phases summing to \(1\), so the remaining
> \(220\) must sum to \(5\pmod{17}\).

This is a global checksum usable as a branch filter; being one linear equation
it is satisfiable and is **not** an obstruction.

> **Theorem F** *(executable).*  The group of automorphisms of the fixed link
> of the form \(x\mapsto\lambda x+\mu\) on \(\mathbb Z_{17}\), with \(L,\infty\)
> fixed or swapped and the induced colour map, is **exactly the \(17\)
> translations**: there is no multiplier \(\lambda\ne1\) and no
> \(L\leftrightarrow\infty\) swap.

*Reason.*  Matching \(\{L,\infty,x\}\mapsto x\) forces the colour map to be the
same affine map; matching \(\{L,x,y\}\) then forces
\(\lambda s_0[d]=s_0[\lambda d]\) for all \(d\), and neither starter is
multiplicative for any \(\lambda\ne1\).

**Consequence.**  \(C_{17}\) is already quotiented out, so **no further
symmetry breaking of this kind is available** to the equivariant search.
*Scope: only affine maps with \(L,\infty\) fixed or swapped were searched; this
is not the full automorphism group of the link as an abstract design.*

## 8. What remains

* Types (ii)/(iii) (\(40+40\) orbits) and type (iv) (\(140\) orbits) are
  untouched; \(220\) of the \(228\) phases are free after Theorem D.
* Any obstruction is **not detected by the linear first-moment system**
  (Theorem B), **not visible in the type-(i) layer** (Theorem C), **not a
  phase-sum violation** (Theorem E), and **not removable by the tested affine
  symmetry breaking** (Theorem F).
* By Theorem A(iii), equivariant UNSAT would yield only \(17\mid|X|\).

## 9. Verification

```sh
python3 -B \
  collaboration/opus5/cyclic_lsts19_extension_attack/verify_cyclic_lsts19_extension_attack.py
```

Standard library only, exact arithmetic and finite enumeration, no solver, no
randomness.  It re-runs the committed generator and verifier in a temporary
directory, re-derives both digests, rebuilds the link from scratch, rebuilds the
exact cover from the committed module, and checks Theorems A–F.  Current
status: **63 checks, all passing; Ruff clean.**

**Erdős–Rosenfeld problem #835 remains open; \(k=16\) is not excluded; no
\(LS(3,4,20)\) is constructed or refuted; and nothing here transfers from the
equivariant ansatz to the unrestricted problem.**
