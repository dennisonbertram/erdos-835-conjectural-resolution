# The e4 refinement of the moment-curve quotient: edge law and exact structure

Date: 2026-07-25.  Everything in the theorem/lemma/corollary blocks of this
file is proved in full, by hand, with no machine computation.  The final
section lists the finite decisions that remain computational and points to
the scripts that settle them; computational results are reported in
[`JUDGMENT.md`](JUDGMENT.md), not here.  Nothing in this file solves
Erdős–Rosenfeld Problem #835.

## Setting and conventions

\(F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1)\), with the 5-bit integer
encoding of the earlier evidence files.  Points of the Johnson graph
\(J(32,16)\) are 16-subsets of \(F\); \(S\sim T\) iff \(|S\cap T|=15\).
For a finite subset \(U\subset F\) define the generating polynomial
\[
 E_U(t)=\prod_{u\in U}(1+ut)=\sum_{j\ge0}e_j(U)\,t^j ,
\]
so \(e_j(U)\) is the \(j\)-th elementary symmetric function of the
elements of \(U\), \(e_0=1\).  This definition involves no signs in any
characteristic; all identities below are stated in characteristic two,
where \(-1=+1\), and each proof tracks the char-2 cancellations explicitly.

The five-statistic map is
\[
 \sigma_5(S)=\bigl(e_1(S),e_2(S),e_3(S),e_4(S),\,e_8(S)+e_1(S)^8\bigr)\in F^5 .
\]
The **actual-edge quotient** joins two values of \(\sigma_5\) iff they are
realized by adjacent 16-sets.  A **refined moment-curve state** with
parameter \(r\in F\) is a value
\[
 \bigl(a,\;a^2,\;a^3,\;a^4+r,\;\lambda\bigr),\qquad a,\lambda\in F .
\]
\(G_r\) denotes the actual-edge graph on refined moment-curve states with
parameter \(r\) (all \(a,\lambda\) realizable by 16-sets).

## Lemma 0 (deletion identities, char-2 form)

Let \(R\) be a \((k{+}1)\)-set, \(x\in R\), \(S=R\setminus\{x\}\).  Then
\(E_R(t)=E_S(t)\,(1+xt)\), hence for every \(j\ge1\)
\[
 e_j(R)=e_j(S)+x\,e_{j-1}(S), \tag{L0.1}
\]
and, inverting the factor as the formal power series
\((1+xt)^{-1}=\sum_{m\ge0}x^mt^m\) (char 2), for every \(m\ge0\)
\[
 e_m(S)=\sum_{j=0}^{m}e_j(R)\,x^{m-j}. \tag{L0.2}
\]

*Proof.*  The product formula is the definition.  (L0.1) is the
coefficient of \(t^j\).  (L0.2) is the coefficient of \(t^m\) in
\(E_S=E_R\cdot\sum_m x^mt^m\); it also follows from (L0.1) by induction on
\(m\).  \(\square\)

## Lemma 1 (adjacent sets: \(e_1\) separates, and \(e_2\) locates the deleted points)

Let \(S\sim T\) in \(J(32,16)\), \(R=S\cup T\) (a 17-set), and write
\(S=R\setminus\{x\}\), \(T=R\setminus\{y\}\) with \(x\ne y\)
(\(x\in T\setminus S\), \(y\in S\setminus T\)).  Put \(a=e_1(S)\),
\(b=e_1(T)\).  Then:

1. \(x+y=a+b\) and \(a\ne b\).  (Adjacent 16-sets never share their
   \(e_1\); every fibre of \(e_1\) is an independent set.)
2. The deleted points are *determined* by the four field elements
   \(a,b,e_2(S),e_2(T)\):
   \[
    x=\frac{e_2(S)+e_2(T)+b(a+b)}{a+b},\qquad y=x+a+b. \tag{L1.1}
   \]

*Proof.*  By (L0.1) with \(j=1\): \(e_1(R)=a+x=b+y\), so \(x+y=a+b\); and
\(x\ne y\) forces \(a\ne b\).  For (2), by (L0.1) with \(j=2\),
\(e_2(R)=e_2(S)+xa=e_2(T)+yb\).  Substituting \(y=x+a+b\):
\[
 e_2(S)+xa=e_2(T)+xb+b(a+b)
 \;\Longrightarrow\;
 x(a+b)=e_2(S)+e_2(T)+b(a+b),
\]
and \(a+b\ne0\) allows division.  \(\square\)

## Theorem A (the edge law; task 1)

Let \(S\sim T\) be adjacent 16-sets whose states satisfy the moment-curve
hypotheses
\[
 e_2(S)=a^2,\quad e_3(S)=a^3,\qquad e_2(T)=b^2,\quad e_3(T)=b^3,
\]
where \(a=e_1(S)\), \(b=e_1(T)\).  Let \(R=S\cup T\).  Then:

1. **(deleted points)** \(S=R\setminus\{a\}\) and \(T=R\setminus\{b\}\);
   in particular \(a\notin S\), \(a\in T\), \(b\in S\), \(b\notin T\),
   and \(a\ne b\) automatically (Lemma 1.1).
2. **(union statistics)** \(e_1(R)=e_2(R)=e_3(R)=0\).
3. **(common \(e_4\))**
   \[
    e_4(S)+a^4\;=\;e_4(R)\;=\;e_4(T)+b^4 .
   \]

*Proof.*  (1)  Insert \(e_2(S)=a^2\), \(e_2(T)=b^2\) into (L1.1):
\[
 x(a+b)=a^2+b^2+b(a+b)=(a+b)^2+b(a+b)=(a+b)(a+b+b)=(a+b)\,a,
\]
using \((a+b)^2=a^2+b^2\) (char 2, Frobenius).  Since \(a+b \neq 0\),
\(x=a\), and \(y=x+a+b=b\).

(2)  \(e_1(R)=e_1(S)+x=a+a=0\).  By (L0.1),
\(e_2(R)=e_2(S)+x\,e_1(S)=a^2+a\cdot a=0\) and
\(e_3(R)=e_3(S)+x\,e_2(S)=a^3+a\cdot a^2=0\), the last step using the
hypothesis \(e_3(S)=a^3\).

(3)  \(e_4(R)=e_4(S)+x\,e_3(S)=e_4(S)+a\cdot a^3=e_4(S)+a^4\); by the
symmetric computation through \(y=b\), \(e_4(R)=e_4(T)+b^4\).
\(\square\)

### Exactly which hypotheses are needed

*   \(a\ne b\) is **not** a hypothesis: adjacency forces it (Lemma 1.1).
*   The two \(e_2\) hypotheses are exactly what force \(x=a,y=b\); without
    them the deleted point is the genuinely different value (L1.1).
*   Given \(x=a,y=b\), the \(e_3\) hypotheses are exactly what give
    parts 2–3.  Quantitatively, if both \(e_2\) hypotheses hold but
    \(e_3(T)\) is unrestricted, then (L0.1) gives the **defect identity**
    \[
     \bigl(e_4(T)+b^4\bigr)+e_4(R)
     \;=\;b\,\bigl(e_3(T)+b^3\bigr), \tag{A.1}
    \]
    so the common-\(e_4\) conclusion fails for every such edge with
    \(b\ne0\), \(e_3(T)\ne b^3\).  (Realizability of such edges is a
    finite existence fact, checked exhaustively in a small field by
    [`verify_edge_law_smallfield.py`](verify_edge_law_smallfield.py); the
    identity (A.1) itself is proved.)
*   Nothing about \(e_8+e_1^8\) is used; the law is blind to \(\lambda\).
*   The proof uses only \(|R|=|S|+1\) and char 2; it holds verbatim in any
    \(\mathbb F_{2^m}\) for \(k\)-sets, \(k\ge4\).  The small-field
    checker exploits this to validate every identity exhaustively in
    \(\mathbb F_{16}\) (all 9-sets \(R\), all 411{,}840 adjacent pairs of
    8-sets).

### Corollary A1 (common \(r\); the clique law)

Define \(h(S)=e_4(S)+e_1(S)^4\).  Along **every single actual edge**
between refined moment-curve states, \(h\) takes the same value at both
endpoints, namely \(e_4(S\cup T)\).  Hence on any connected set of
pairwise-moment-curve states — in particular on any clique, with or
without a vertex over each \(a\) — \(h\) is a single constant \(r\).
Moreover, two distinct states with the same first coordinate are never
adjacent (Lemma 1.1), so a clique meets each fibre \(\{e_1=a\}\) at most
once and has at most 32 vertices.

This proves (and strengthens, from cliques to single edges) the proposed
common-\(r\) implication.

## Theorem B (exact structure of \(G_r\); task 2)

For \(r\in F\) put
\[
 \mathcal R_r=\bigl\{R\subset F:\ |R|=17,\
 e_1(R)=e_2(R)=e_3(R)=0,\ e_4(R)=r\bigr\},
\]
and for \(R\in\mathcal R_r\) define the **label quartic**
\[
 \lambda_R(a)=r\,a^4+e_5(R)\,a^3+e_6(R)\,a^2+e_7(R)\,a+e_8(R).
\]
Then:

1. For every \(R\in\mathcal R_r\) and \(a\in R\),
   \[
    \sigma_5(R\setminus\{a\})
    =\bigl(a,\;a^2,\;a^3,\;a^4+r,\;\lambda_R(a)\bigr).
   \]
2. For \(a\ne b\in R\) the deletions \(R\setminus\{a\}\sim
   R\setminus\{b\}\), so \(\{(a,\lambda_R(a)):a\in R\}\) is a 17-clique
   of \(G_r\).
3. Conversely **every** edge of \(G_r\) arises this way: if adjacent
   \(S,T\) realize refined states \((a,\dots,\lambda)\),
   \((b,\dots,\mu)\) with the same parameter \(r\), then
   \(R=S\cup T\in\mathcal R_r\), \(S=R\setminus\{a\}\),
   \(T=R\setminus\{b\}\), \(\lambda=\lambda_R(a)\),
   \(\mu=\lambda_R(b)\).  (States with different parameters are never
   adjacent, by Corollary A1.)

Hence, as an edge set,
\[
 G_r=\bigcup_{R\in\mathcal R_r}K_{17}\bigl(\{(a,\lambda_R(a)):a\in R\}\bigr),
\]
an exact, finite, static description: the e4-refined moment-curve sector
of the five-statistic quotient is the disjoint union over \(r\in F\) of
the 32 graphs \(G_r\), and each \(G_r\) is the union of the
\(|\mathcal R_r|\) labelled 17-cliques above.

*Proof.*  (1)  By (L0.2) with \(x=a\in R\), \(S=R\setminus\{a\}\), for
\(m\le4\):
\[
 e_m(S)=\sum_{j=0}^{m}e_j(R)a^{m-j}
 =a^m+\underbrace{e_1(R)}_{0}a^{m-1}+\underbrace{e_2(R)}_{0}a^{m-2}
 +\underbrace{e_3(R)}_{0}a^{m-3}+e_4(R)\,[m{=}4],
\]
giving \(e_1(S)=a\), \(e_2(S)=a^2\), \(e_3(S)=a^3\),
\(e_4(S)=a^4+r\).  For \(m=8\), (L0.2) gives
\(e_8(S)=\sum_{j=0}^{8}e_j(R)a^{8-j}\); the \(j=0\) term is \(a^8\), the
\(j=1,2,3\) terms vanish, so
\[
 e_8(S)+a^8=r\,a^4+e_5(R)a^3+e_6(R)a^2+e_7(R)a+e_8(R)=\lambda_R(a).
\]
(2)  \(|R\setminus\{a\}\cap R\setminus\{b\}|=15\).
(3)  Theorem A applies (the endpoint states satisfy its hypotheses) and
gives \(S=R\setminus\{a\}\), \(T=R\setminus\{b\}\),
\(e_1(R)=e_2(R)=e_3(R)=0\), \(e_4(R)=e_4(S)+a^4=r\); so
\(R\in\mathcal R_r\), and part 1 identifies the \(\lambda\)-coordinates.
\(\square\)

### Corollary B1 (what a colour rule must do)

Every vertex \((a,\lambda_R(a))\) is realized by the 16-set
\(R\setminus\{a\}\), and pairwise-adjacent realizable states must get
pairwise distinct colours under any proper colouring of \(J(32,16)\) of
the form \(c(S)=G(\sigma_5(S))\).  Hence such a 17-colour rule restricts
to a proper 17-colouring of every \(G_r\).  Consequently a **single**
\(r\) with \(\omega(G_r)\ge18\) or \(\chi(G_r)\ge18\) refutes every
17-colour rule using the five statistics
\((e_1,e_2,e_3,e_4,e_8+e_1^8)\).  (The converse is not claimed:
17-colourability of every \(G_r\) would leave the off-moment-curve states
unresolved.)

## Theorem C (symmetries; reduction to \(G_0\) and \(G_1\))

Let \(c\in F^\times\).  The scaling bijection \(x\mapsto cx\) of \(F\)
maps 16-sets to 16-sets preserving adjacency, sends \(\mathcal R_r\)
bijectively onto \(\mathcal R_{c^4r}\), and induces a graph isomorphism
\[
 G_r\;\xrightarrow{\ \cong\ }\;G_{c^4r},\qquad
 (a,\lambda)\mapsto(ca,\;c^8\lambda).
\]
Since \(\gcd(4,31)=1\), \(x\mapsto x^4\) is a bijection of
\(F^\times\); taking \(c=r^8\) (so \(c^4=r^{32}=r\)) gives
\(G_1\cong G_r\) for every \(r\ne0\).  Likewise Frobenius
\(x\mapsto x^2\) induces \(G_r\cong G_{r^2}\),
\((a,\lambda)\mapsto(a^2,\lambda^2)\).  Hence every exact question about
the \(G_r\) reduces to the two graphs \(G_0\), \(G_1\), and \(G_0\)
carries a scaling action of the full \(F^\times\) (order 31) plus
Frobenius.

*Proof.*  \(e_j(cU)=c^j e_j(U)\) (each monomial of \(e_j\) is a product
of \(j\) elements).  So \(R\in\mathcal R_r\Rightarrow
e_{1,2,3}(cR)=0\), \(e_4(cR)=c^4r\), i.e.
\(cR\in\mathcal R_{c^4r}\), bijectively (inverse: scale by
\(c^{-1}\)).  A 16-set \(S\) with
\(\sigma_5(S)=(a,a^2,a^3,a^4+r,\lambda)\) maps to \(cS\) with
\(e_1=ca\), \(e_2=c^2a^2=(ca)^2\), \(e_3=(ca)^3\),
\(e_4=c^4(a^4+r)=(ca)^4+c^4r\), and
\(e_8(cS)+e_1(cS)^8=c^8\bigl(e_8(S)+a^8\bigr)=c^8\lambda\).  Adjacency
is preserved because \(x\mapsto cx\) is a bijection of \(F\).  Label
check: \(\lambda_{cR}(ca)=c^4r(ca)^4+c^5e_5(ca)^3+c^6e_6(ca)^2
+c^7e_7(ca)+c^8e_8=c^8\lambda_R(a)\).  The Frobenius case is identical
with \(e_j(U^{(2)})=e_j(U)^2\).  \(\square\)

## Task 4 reduction (the \(K_{32}\) under the e4 refinement)

Let \(L(a)=1\) if \(a=0\) or \(\operatorname{Tr}(a)=1\), else \(0\) (the
layer function of the four-statistic \(K_{32}\)).  A \(K_{18}\) inside
the \(K_{32}\) **survives the e4 refinement** iff there are 18 values
\(a\) and one parameter \(r\) such that the states
\((a,a^2,a^3,a^4+r,L(a))\) are pairwise adjacent.  By Corollary A1 the
single common \(r\) is forced, and by Theorem B this holds iff the
induced subgraph
\[
 H_r=G_r\bigl[\{(a,L(a)):a\in F\}\bigr]
\]
has \(\omega(H_r)\ge18\) for some \(r\in F\).  Each \(H_r\) has at most
32 vertices, and every edge again requires a witness
\(R\in\mathcal R_r\) with \(\lambda_R(a)=L(a)\), \(\lambda_R(b)=L(b)\).
(The scaling isomorphism does **not** preserve the constraint
\(\lambda=L(a)\), so all 32 values of \(r\) must be checked; the check is
finite and small.)

## What remains computational (exact finite decisions)

All of the following are decided exactly by
[`remote_run_e4.py`](remote_run_e4.py) (self-contained; identical logic in
[`enumerate_e4_refinement.py`](enumerate_e4_refinement.py)), whose
enumeration of \(\mathcal R_r\) is meet-in-the-middle over two 16-point
halves, confirmed by (i) a full re-run on a different half-split,
(ii) from-scratch recomputation of \(e_1,\dots,e_8\) for every reported
\(R\), and (iii) the requirement that all 496 static \(K_{32}\) witness
masks appear among the \(\mathcal R_r\) with layer-consistent labels
(they must, by Theorem A — each is the union of two adjacent
moment-curve realizations):

1. \(|\mathcal R_r|\) for all \(r\), and the vertex/edge counts of every
   \(G_r\);
2. \(\omega(G_0)\), \(\omega(G_1)\) exactly (17-class-span peeling plus
   Tomita branch-and-bound), which by Theorem C determines
   \(\omega(G_r)\) for all \(r\);
3. \(\omega(H_r)\) for all 32 \(r\) (task 4);
4. colouring upper bounds for \(G_0,G_1\) (DSATUR + randomized greedy);
   exact \(\chi\) decision at 17 is escalated separately only if the
   bounds leave it open.

The algebraic identities behind the enumeration are validated
exhaustively in \(\mathbb F_{16}\) by
[`verify_edge_law_smallfield.py`](verify_edge_law_smallfield.py), which
checks (L0.1), (L0.2), (L1.1), Theorem A, the defect identity (A.1), and
Theorem B parts 1–3 over **all** 11{,}440 nine-sets and all 411{,}840
adjacent pairs of 8-sets, and confirms that dropped hypotheses really do
break the law (existence of counterexamples, task 1's "exactly what is
needed").

Computational outcomes, when obtained, are recorded with provenance in
[`JUDGMENT.md`](JUDGMENT.md); this file's theorems stand independently of
them.
