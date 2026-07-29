# Complete new lemmas: the polarization boundary of the cross-matching cubic

Date: 2026-07-25.  Everything in this file is proved in full.  Nothing here
solves Erdős–Rosenfeld Problem #835; the theorems delimit exactly which uses
of the projected-idempotence cubic system cannot work and reduce the system
to a single residual decision problem.

## Setting

Let \(p=k+1\) be prime, \(X=\binom{[2k]}{k}\), \(W=W_{k-1,k}(2k)\) the
inclusion matrix, \(K=\ker_{\mathbb Q}W\subset\mathbb R^X\), and \(P_K\)
the orthogonal projection onto \(K\).  Products of functions on \(X\) are
pointwise.  Write \(d=\tfrac1p\binom{2k}{k}\) and
\[
 \beta(x,y)=P_K(xy)\qquad(x,y\in\mathbb R^X),
\]
a symmetric bilinear map.  Note \(\boldsymbol1\in K^\perp\), because the
column sums of \(W\) all equal \(k\), so
\(\boldsymbol1=k^{-1}W^{\mathsf T}\boldsymbol1\in\operatorname{row}(W)\).

**System \(C_p\)** (from
[`../../evidence/top_degree_cross_matching_cubic_audit.md`](../../evidence/top_degree_cross_matching_cubic_audit.md)):
find \(q_a\in K\) for \(a\in\mathbb F_p\) with

1. \(\sum_a q_a=0\);
2. Gram: \(\langle q_a,q_b\rangle=pd(p-1)\) if \(a=b\), \(-pd\) otherwise;
3. cubic: \(\beta(q_a,q_b)=(p-2)q_a\) if \(a=b\), and
   \(-q_a-q_b\) if \(a\ne b\).

A tight \(p\)-colouring gives a solution via
\(q_a=p\boldsymbol1_{C_a}-\boldsymbol1\).

## Lemma 1 (the cubic alone forces the Gram shape)

Let \(q_a\in K\setminus\{0\}\) satisfy only condition 3.  Then all norms
\(\|q_a\|^2\) are equal to a common value \(\nu>0\), and
\(\langle q_a,q_b\rangle=-\nu/(p-1)\) for all \(a\ne b\).

*Proof.*  Pointwise multiplication is commutative and associative, so for
\(a\ne b\)
\[
 \langle q_a^2,q_b\rangle=\sum_{S\in X}q_a(S)^2q_b(S)
 =\langle q_aq_b,q_a\rangle .
\]
Both \(q_a,q_b\in K\), so each side may be computed through \(P_K\) and
condition 3:
\[
 \langle\beta(q_a,q_a),q_b\rangle=(p-2)\langle q_a,q_b\rangle,
 \qquad
 \langle\beta(q_a,q_b),q_a\rangle=-\|q_a\|^2-\langle q_a,q_b\rangle .
\]
Equating gives \((p-1)\langle q_a,q_b\rangle=-\|q_a\|^2\).  Exchanging
\(a\) and \(b\) gives \((p-1)\langle q_a,q_b\rangle=-\|q_b\|^2\).  Hence
all norms agree and the off-diagonal entries are \(-\nu/(p-1)\).
\(\square\)

**Remark (scale rigidity).**  If \(\{q_a\}\) satisfies condition 3, then
\(\{tq_a\}\) does iff \(t^2=t\), i.e. \(t=1\).  So \(\nu\) is an invariant
of a solution, not a free normalization; condition 2 adds to condition 3
exactly the single scalar demand \(\nu=pd(p-1)\), nothing else.  In
particular the entire quadratic Gram data of the earlier audits is, up to
this one scalar, a *consequence* of the cubic.

## Lemma 2 (all triple contractions are determined)

Under condition 3 (with the common norm \(\nu\) of Lemma 1) and
condition 1, the fully symmetric quantities
\(\tau_{abc}=\langle q_aq_b,q_c\rangle\) are determined:
\[
 \tau_{aaa}=(p-2)\nu,\qquad
 \tau_{aab}=-\frac{(p-2)\nu}{p-1}\ (a\ne b),\qquad
 \tau_{abc}=\frac{2\nu}{p-1}\ (a,b,c\text{ distinct}).
\]

*Proof.*  \(q_c\in K\) allows \(\tau_{abc}=\langle\beta(q_a,q_b),q_c\rangle\);
insert condition 3 and Lemma 1.  Full symmetry holds because the pointwise
product is commutative and associative, and the three resulting evaluations
agree: e.g. \(\langle\beta(q_a,q_a),q_b\rangle=(p-2)\langle q_a,q_b\rangle
=-(p-2)\nu/(p-1)\) equals
\(\langle\beta(q_a,q_b),q_a\rangle=-\nu+\nu/(p-1)=-(p-2)\nu/(p-1)\).
\(\square\)

## Theorem 1 (polarization / contraction no-go)

Let \(\mathfrak F\) be the family of all scalar quantities generated from
the vectors \(q_a\) by iterated application of \(\beta\) and the inner
product — that is, every expression built by bilinearity from
\(\beta\)-words in the \(q_a\) and contractions of such words against each
other.  Then:

1. \(C_p\) determines the value of every member of \(\mathfrak F\) as a
   universal polynomial in \(p\) and \(d\), independent of the ambient
   space \((K,\beta)\);
2. all of those values are *simultaneously realized* by the following
   explicit model: on \(\mathbb R^{\mathbb F_p}\) (functions on the
   \(p\)-point set) take the pointwise product, the weighted inner product
   \(\langle x,y\rangle_d=d\sum_{t}x(t)y(t)\), the projection \(\pi\) that
   kills constants, and
   \[
    q_a^{\mathrm{mod}}=\chi_a=p\,\boldsymbol1_{\{a\}}-\boldsymbol1 .
   \]

Consequently **no combination of summing, polarizing, averaging, or
contracting the cubic system against the span of the colour vectors can
derive a contradiction — for any prime \(p\), in particular \(p=17\).**

*Proof.*  (1)  Condition 3 says \(\operatorname{span}\{q_a\}\) is
\(\beta\)-closed with explicit structure constants.  By bilinearity every
\(\beta\)-word therefore reduces to an explicit linear combination of the
\(q_a\), and every contraction then reduces to Gram entries, which
conditions 2–3 fix (Lemma 1).  No datum of the ambient space survives.

(2)  On the \(p\)-point set, pointwise:
\[
 \chi_a^2=(p-2)\chi_a+(p-1)\boldsymbol1,\qquad
 \chi_a\chi_b=-\chi_a-\chi_b-\boldsymbol1\ (a\ne b),
\]
so after \(\pi\) the structure constants of condition 3 hold verbatim.
Gram: \(\sum_t\chi_a\chi_b\) equals \(p(p-1)\) if \(a=b\) and \(-p\)
otherwise, so \(\langle\chi_a,\chi_b\rangle_d\) is \(pd(p-1)\), resp.
\(-pd\): exactly condition 2.  Also \(\sum_a\chi_a=0\).  A family of
determined scalars admitting one common model is consistent; no
contradiction is derivable from it.

Spot checks of the model against Lemma 2 (with \(\nu=pd(p-1)\)):
\(\tau^{\mathrm{mod}}_{aaa}=d[(p-1)^3-(p-1)]=(p-2)\,pd(p-1)\);
\(\tau^{\mathrm{mod}}_{aab}=d[-(p-1)^2+(p-1)-(p-2)]=-pd(p-2)\);
\(\tau^{\mathrm{mod}}_{abc}=d[3(p-1)-(p-3)]=2pd\).  All agree.
\(\square\)

**Boundary of the theorem.**  \(\mathfrak F\) does *not* contain
unprojected higher moments such as \(\langle q_aq_b,q_cq_d\rangle\) or
projected triple pointwise products \(P_K(q_aq_bq_c)\): the cubic system
does not determine them (the \(K^\perp\) components of products are
unconstrained), so they cannot be used without adding genuinely new
identities.  This is the precise sense in which "stronger pointwise
information" is required.

## Lemma 3 (no nonnegative multipliers)

If \(\varphi\in K\) and \(\varphi\ge0\) pointwise, then \(\varphi=0\).

*Proof.*  \(\boldsymbol1\in K^\perp\), so
\(\sum_S\varphi(S)=\langle\varphi,\boldsymbol1\rangle=0\).  \(\square\)

**Corollary (no direct positive-form route).**  Pairing the equations of
\(C_p\) with a test vector \(\varphi\) only produces a constraint when
\(\varphi\in K\) (otherwise the unconstrained \(K^\perp\) parts of the
products enter), and \(K\) contains no nonzero nonnegative function.
Together with Theorem 1 this rules out every refutation of \(C_p\) by
summation, polarization, or integration against a nonnegative kernel.  A
genuine Positivstellensatz refutation would have to certify emptiness of
the variety of Theorem 2 below using the specific multiplication tensor of
\(K\) — not the abstract relations.

## Theorem 2 (exact residual content: an algebra-embedding problem)

\(C_p\) is solvable iff there is a \((p-1)\)-dimensional subspace
\(V\subset K\) such that

1. \(V\) is \(\beta\)-closed: \(P_K(vw)\in V\) for all \(v,w\in V\); and
2. \((V,\beta|_V)\) is isomorphic to the *reduced \(p\)-point algebra*
   (sum-zero functions on \(p\) points under multiply-then-kill-constants)
   by an isomorphism sending \(\chi_a\mapsto q_a\) that carries the
   counting inner product scaled by \(d\) to \(\langle\cdot,\cdot\rangle\).

*Proof.*  (\(\Rightarrow\))  Given a solution, \(V=\operatorname{span}\{q_a\}\)
has dimension \(p-1\): by Lemma 1 the Gram matrix is
\(\nu\bigl(\delta_{ab}-\tfrac1p\bigr)\tfrac p{p-1}\)-shaped with
\(\nu>0\), which has rank exactly \(p-1\).  Condition 3 gives
\(\beta\)-closure on a spanning set, hence on \(V\) by bilinearity.  The
map \(\chi_a\mapsto q_a\) is well defined (each side satisfies only the
relation "sum = 0"), intertwines the products (identical structure
constants) and matches Gram matrices (Theorem 1(2)).
(\(\Leftarrow\))  Read the frame \(q_a\) back from the isomorphism; the
relations of \(C_p\) are exactly the model relations.  \(\square\)

Everything the cubic system can say beyond Theorem 1 is therefore the
single question: **does \((K,\beta)\) at a given parameter contain a
\(\beta\)-closed reduced-\(p\)-point subalgebra at norm
\(\nu=pd(p-1)\)?**  This is a finite (real-algebraic) decision problem.
At the false parameter \(k=4\) it is decidable in practice
(\(\dim K=14\)); the companion script
[`decide_cubic_embedding_k4.py`](decide_cubic_embedding_k4.py) implements
the decision search.  Both outcomes are informative — see
[`JUDGMENT.md`](JUDGMENT.md).

## Lemma 4 (trace bit formula and the analytic K\(_{17}\) sub-certificate)

In \(F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1)\) with the 5-bit integer
encoding \(x=\sum_ib_i\alpha^i\),
\[
 \operatorname{Tr}(x)=b_0\oplus b_3 .
\]

*Proof.*  \(\operatorname{Tr}\) is \(\mathbb F_2\)-linear, and
\(\operatorname{Tr}(x^2)=\operatorname{Tr}(x)\), so it suffices to
evaluate the basis.  \(\operatorname{Tr}(1)=5\cdot1=1\).
\(\operatorname{Tr}(\alpha)=\alpha+\alpha^2+\alpha^4+\alpha^8+\alpha^{16}\)
with \(\alpha^8=\alpha^3+\alpha^2+1\) and
\(\alpha^{16}=\alpha^4+\alpha^3+\alpha+1\) (both by direct reduction);
the five terms cancel pairwise to \(0\).  Hence also
\(\operatorname{Tr}(\alpha^2)=\operatorname{Tr}(\alpha^4)=0\).
\(\operatorname{Tr}(\alpha^3)
=\alpha^3+\alpha^6+\alpha^{12}+\alpha^{24}+\alpha^{17}\); reducing
\(\alpha^6=\alpha^3+\alpha\), \(\alpha^{12}=\alpha^3+\alpha^2+\alpha\),
\(\alpha^{24}=\alpha^4+\alpha^3+\alpha^2+\alpha\),
\(\alpha^{17}=\alpha^4+\alpha+1\) and summing gives \(1\).  \(\square\)

**Corollary.**  The base 17-set of the two-statistic \(K_{18}\)
certificate,
\(B=\{0,1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30\}\),
is exactly \(\{0\}\cup\{x:\operatorname{Tr}(x)=1\}\) (checked element by
element with the bit formula), i.e. \(B=R_1\) in the notation of
[`../../evidence/f32_prefix8_trace_hyperplanes.md`](../../evidence/f32_prefix8_trace_hyperplanes.md).
By the (independently re-derived) converse part of Theorem 2 there, the
seventeen deletion 16-sets \(B\setminus\{a\}\) have statistics
\((e_1,e_8+e_1^8)=(a,1)\), pairwise distinct, and are pairwise adjacent in
\(J(32,16)\).  Thus the \(K_{17}\) part of the \(K_{18}\) certificate —
136 of its 153 edges — holds by proof, with no machine computation.  The
seventeen extension edges to the state \((29,27)\) remain
machine-checkable finite arithmetic; see
[`validate_k18_independent.py`](validate_k18_independent.py).
