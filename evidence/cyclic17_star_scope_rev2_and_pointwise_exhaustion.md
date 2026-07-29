# Revision 2: repaired scope theorem, strengthened Hall theorem, and an unrestricted pointwise no-go

**Scope, stated first.** Erdős–Rosenfeld #835 remains **open**. This note
revises two claims from
`cyclic17_star_threshold_and_colour_transitive_scope.md` that did not survive
audit, and then delivers one unrestricted result. The unrestricted result is a
**no-go about a class of proof strategies**, not progress toward existence.

Each section is labelled **THEOREM**, **COMPUTATION**, or **HEURISTIC**.

Verifiers (stdlib only, no solver):

| file | covers |
|---|---|
| `evidence/verify_cyclic17_star_hall_theorem.py` | §1 Theorem D (repaired), §2 Theorem E (strengthened) |
| `evidence/verify_pointwise_moment_exhaustion.py` | §4 Theorem F, forced moment tensors, k=2 control |

---

## 0. What was wrong

1. **Theorem D assumed \(G\le\operatorname{Sym}(32)\).** At \(n=2k\) the Johnson
   graph also admits complementation \(c:B\mapsto B^{c}\), and
   \(\operatorname{Aut}(J(32,16))=\operatorname{Sym}(32)\times C_2\). The proof
   never addressed the \(C_2\) component, and the Sylow-image step was asserted
   rather than justified. **Repaired in §1.**
2. **The Hall paragraph's stated reason was false.** It claimed a violation
   requires "\(\ge12\) rows whose domains all lie inside one common 11-set".
   That covers only \(|T|=12\): at \(|T|=13\) a violation needs union \(\le12\),
   at \(|T|=14\) union \(\le13\), and neither is a common 11-set. The reason as
   written did not cover \(r=13,14\). **Withdrawn, and replaced in §2 by a
   stronger fact that is actually proved.**

---

## 1. THEOREM D, repaired

> **Theorem D.** Suppose a tight 17-colouring of \(J(32,16)\) admits an
> automorphism group \(G\le\operatorname{Aut}(J(32,16))=\operatorname{Sym}(32)\times C_2\)
> that is transitive on the seventeen colour classes. Then it admits an
> automorphism \(\sigma\) of order 17, lying in \(\operatorname{Sym}(32)\times\{1\}\),
> with cycle type \(17+1^{15}\) on the 32 points, permuting the colours in a
> 17-cycle. That is, it satisfies the cyclic ansatz.

The automorphism-group identity used here is the \(n=2i\) case proved by
Ashwin Ganesan, *On the automorphism group of a Johnson graph*,
arXiv:1412.5055.

*Proof.*

**Order of a Sylow 17-subgroup.** Exactly one multiple of 17 is \(\le32\), so
\(17^{1}\) exactly divides \(32!\); and \(17\nmid|C_2|=2\). Hence the 17-part of
\(|\operatorname{Sym}(32)\times C_2|\) is \(17\), and every Sylow 17-subgroup
\(S\le G\) has order dividing 17.

**Step 1 — the complement component is trivial.** Write \(\sigma=(\pi,\varepsilon)\)
of order 17. Since \(\varepsilon^{2}=1\) and 17 is odd,
\(\varepsilon=\varepsilon^{17}\); and \(\sigma^{17}=(\pi^{17},\varepsilon^{17})=(1,1)\)
gives \(\varepsilon^{17}=1\), so \(\varepsilon=1\). Equivalently, any odd-order
subgroup has trivial projection to \(C_2\). So
\(\sigma\in\operatorname{Sym}(32)\times\{1\}\) and \(|\pi|=17\).

**Step 2 — the Sylow image step, justified.** Let
\(\varphi:G\to\operatorname{Sym}(\text{colours})\) with kernel \(K\). For a Sylow
\(p\)-subgroup \(S\), \(\varphi(S)\) is a Sylow \(p\)-subgroup of \(G/K\):
\(|\varphi(S)|=|S|/|S\cap K|\) is a \(p\)-power, and
\[
 [G/K:\varphi(S)]=\frac{[G:S]}{[K:S\cap K]},
\]
where \([G:S]\) is prime to \(p\) because \(S\) is Sylow, and \(S\cap K\) is a
Sylow \(p\)-subgroup of \(K\) (it is a \(p\)-subgroup of \(K\) of index dividing
\([G:S]\)), so \([K:S\cap K]\) is prime to \(p\). Hence the index is prime to
\(p\).

**Step 3.** \(G\) colour-transitive \(\Rightarrow\) \(G/K\le\operatorname{Sym}(17)\)
is transitive \(\Rightarrow 17\mid|G/K|\Rightarrow\) its Sylow 17-subgroups are
nontrivial \(\Rightarrow\varphi(S)\ne1\), so \(|S|=17\). As 17 is prime,
\(\varphi\) is injective on \(S\), so every \(\sigma\ne1\) in \(S\) has image of
order 17 in \(\operatorname{Sym}(17)\) — a 17-cycle, hence colour-transitive.

**Step 4.** By Step 1, \(\pi\) has order 17, so its cycles have length 1 or 17;
\(2\cdot17=34>32\) forces exactly one 17-cycle \(A\) and \(|F|=15\) fixed points.
Relabelling colours by \(\mathbb Z_{17}\) so that \(\sigma\) sends \(q\) to
\(q+1\) is the ansatz. \(\square\)

**Scope, unchanged.** A no-go over **all** golf designs of \(\mathbb Z_{17}\)
would refute every **colour-transitive** tight 17-colouring of \(J(32,16)\). It
would not refute colourings whose automorphism group is not colour-transitive,
so it would not settle #835. A no-go for one chart excludes only that chart.

---

## 2. THEOREM E, strengthened (replaces the withdrawn Hall paragraph)

> **Theorem E.** Fix **any** golf design of \(\mathbb Z_{17}\), any centre \(i\),
> any orbit \(q\), and any set \(T\) of star rows. Then
> \(\bigl|\bigcup_{j\in T}D_{ij}(q)\bigr|\ge|T|\). Hall's condition holds at
> every orbit of every star.

*Proof.* \(D_{ij}(q)=(\mathbb Z_{17}\setminus F_i(q))\setminus F_j(q)\), so
\[
 \bigcup_{j\in T}D_{ij}(q)
 =(\mathbb Z_{17}\setminus F_i(q))\setminus\bigcap_{j\in T}F_j(q),
\]
and \(c\in\bigcap_{j\in T}F_j(q)\) iff \(T\subseteq B_c(q):=\{j:c\in F_j(q)\}\).
Now \(|B_c(q)|\in\{1,3\}\): the translate \(T_q+c\) is a triangle, its edges
avoiding \(0\) lie in **distinct** starters because a starter is a matching and
cannot own two edges of a triangle; if \(0\in T_q+c\) exactly one edge avoids
\(0\), otherwise all three do. Hence:

* \(|T|\ge4\): the intersection is empty, so the union is all of
  \(\mathbb Z_{17}\setminus F_i(q)\), of size \(14\ge|T|\) since a star has 14 rows;
* \(|T|\le3\): the union contains one domain, of size
  \(17-|F_i(q)\cup F_j(q)|\ge17-6=11\ge3\ge|T|\). \(\square\)

This uses only \(|B_c(q)|\le3\) and \(|F_i(q)|=3\), both forced by the
golf-design axioms, so it is **chart-independent** — strictly stronger than the
previous exhaustive check on two charts.

**COMPUTATION (control).** The verifier also checks Hall exhaustively over all
subsets of the 14 rows, all 15 centres, all 40 orbits, on the Wallis and
\((-1)\)-symmetric charts: 0 failures, minimum slack 0. It reports how many
additional golf designs its randomised greedy found (0 in the recorded run) so
the control's coverage is not overstated.

**Consequence.** The star infeasibility is not a single-orbit phenomenon for
*any* golf design. No Hall/SDR argument at one orbit can prove it; any proof
must couple the 40 orbits.

---

## 3. The break-even model is unchanged and still HEURISTIC

§3–§4 of the previous note are untouched: break-even family sizes
\(F^*(5)=586\), \(F^*(6)=3{,}731\) against actual families of mean 486, locating
the minimum obstruction at six rows, and agreeing to three significant figures
on the \((-1)\)-symmetric chart. It remains a model, not a proof: it gives
\(E\approx10^{-0.4}\) at \(m=5\) where every 5-subset is SAT, and predicts
\(\approx0.008\) SAT 6-subsets where 4 exist.

---

## 4. Pivot: an unrestricted pointwise no-go

**Where the frontier actually is.** Two facts fix it. The exact rational
five-point certificate is **feasible** — verified with zero rational tolerance —
so that LP is not an obstruction. And `collaboration/opus5/PROOF.md` Thm 7/7a
gives that any \(S(k-1,k,v)\) with \(v\ge2k-1\) has Fourier support in
\(\{E_0,E_k\}\), so every necessary condition that is a linear functional of the
inner or dual distribution, of slice degree \(\le k-1\), is automatically
satisfied. That file states the residual frontier as: a functional of full slice
degree \(k\) **together with** at least a third-order use of idempotence.

> **THEOREM F (unrestricted).** Let \(c\) be any tight \((k+1)\)-colouring of
> \(J(2k,k)\), with colour classes \(C_0,\dots,C_k\), indicators \(f_q\),
> \(N=\binom{2k}{k}\), \(p=k+1\). For any multiset \(a_1,\dots,a_m\) of colours,
> \[
>  \sum_x f_{a_1}(x)\cdots f_{a_m}(x)=
>  \begin{cases} N/p,&\text{all }a_i\text{ equal},\\ 0,&\text{otherwise.}\end{cases}
> \]

*Proof.* The colour classes partition the vertex set, so the indicators are
idempotent with pairwise disjoint supports, \(f_af_b=\delta_{ab}f_a\). The
product therefore collapses to \(f_a\) when all indices agree, and to 0
otherwise; summing gives \(|C_a|=N/p\) or 0. \(\square\)

**Consequence — the pointwise algebra is totally exhausted.** Every polynomial
in the indicators evaluated pointwise and summed is a constant determined by
\(k\) alone, at **every** order — not merely at order \(\le k-1\). So no purely
pointwise functional, of any degree, can separate a hypothetical tight colouring
from an existing one. Any obstruction must pair the indicators against the
Johnson scheme operators; multiplying them pointwise can never suffice. This
sharpens the opus5 frontier statement in a different direction from Thm 7a:
opus5 bounds the *degree* of linear functionals of the distribution; Theorem F
kills the whole pointwise algebra at all degrees.

**Forced centred moments at \(k=16\)** (\(g_a=f_a-1/p\), \(N=601{,}080{,}390\)),
which any degree-16 cubic attempt needs as its baseline:

| quantity | value |
|---|---|
| \(\langle g_a,g_a\rangle\) | \(16\,N/17^{2}\) |
| \(\langle g_a,g_b\rangle,\ a\ne b\) | \(-N/17^{2}\) |
| \(T_{aaa}\) | \(240\,N/17^{3}\) |
| \(T_{aac},\ a\ne c\) | \(-15\,N/17^{3}\) |
| \(T_{abc}\) all distinct | \(2\,N/17^{3}\) |
| \(Q_{abcd}\) all distinct | \(-3\,N/17^{4}\) |

The verifier confirms these sum to zero over all colour tuples for \(m=2,3,4\)
(since \(\sum_a g_a=0\)).

**COMPUTATION (control).** All raw and centred moments up to order 5 are checked
in exact rational arithmetic against the genuine tight 3-colouring of \(J(4,2)\)
at \(k=2\) — 363 tuples, all matching the closed form. This is a case where a
tight colouring really exists, so the control can fire.

**Honest scoped no-result.** Theorem F is unrestricted and proved, but it is a
no-go about proof strategies. It does not construct a colouring, does not
refute one, and does not settle #835. I did **not** find a new complete finite
obstruction or a constructive mechanism on the unrestricted side; the third and
fourth centred moments turn out to be forced, which is why the pointwise route
closes rather than opens. The live frontier remains what opus5 states: a
full-slice-degree-16 functional combined with third-order idempotence, i.e. the
cross-matching cubic family, which this note does not advance.

---

## 5. Reproduce

```sh
python3 -B evidence/verify_cyclic17_star_hall_theorem.py
python3 -B evidence/verify_pointwise_moment_exhaustion.py
```

## Reference

- Ashwin Ganesan, “On the automorphism group of a Johnson graph,”
  arXiv:1412.5055 (2014), https://arxiv.org/abs/1412.5055.
