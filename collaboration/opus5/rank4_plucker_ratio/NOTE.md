# The rank-four two-coordinate Plücker ratio: exact frontier

## Scope, stated first

**This does not solve Erdős–Rosenfeld #835.** It does not prove a no-go for the
rank-four family, and it does not construct a colouring. What it establishes:
an exact classification of the local pencil (PROVED), an exact translation of
the colouring condition into geometry on the Segre quadric (PROVED), a
**local positive link at \(p=3\)** (exhibited), and a **sharp frontier**: at
\(p=5,7,11\) no local link was found under broad search, but that is
COMPUTATION, not a theorem. Local links are also strictly weaker than a global
pair of Plücker systems — see §5.

Verifier: `verify_rank4_ratio.py` (stdlib, dependency-free, assertion-enabled).

---

## 1. PROVED — classification of the local pencil

Let \(P,Q\) be decomposable \(k\)-forms, \(R\) a \((k-2)\)-face,
\(\eta_0=\iota_RP\), \(\eta_1=\iota_RQ\), \(X\) the remaining \(p+1\)
coordinates.

> **Lemma 1.** Contraction of a decomposable form is decomposable, so
> \(\eta_0\) and \(\eta_1\) each have alternating rank \(\le2\)
> *individually*. Only the pencil members \(a\eta_0+b\eta_1\) reach rank 4.

> **Lemma 2.** Write \(\eta_0=f\wedge g\), \(\eta_1=u\wedge v\). Then
> \(\operatorname{rank}(a\eta_0+b\eta_1)=4\) for some \((a,b)\) iff
> \(\eta_0\wedge\eta_1\ne0\) iff \(f,g,u,v\) are independent. In that case
> \((\eta_0,\eta_1)\cong(e_1\wedge e_2,\;e_3\wedge e_4)\): **one congruence
> orbit**. The Pfaffian of the pencil is \(ab\) up to scalar — two simple
> roots — so **exactly two members have rank 2**, namely \(\eta_0,\eta_1\)
> themselves, and the other \(p-1\) have rank 4.

If \(f,g,u,v\) span only 3 dimensions the pencil is entirely decomposable:
that is precisely the Grassmann-line case, already closed. Span 2 means
\(\eta_0\propto\eta_1\), excluded. So the rank-four case is a single orbit and
there are no common-radical or repeated-Pfaffian-root subcases to treat.

## 2. PROVED — exact translation of the colouring condition

Each \(i\in X\) becomes \(w_i\in\mathbb F_p^4\) and
\(\eta_\mu(i,j)=B_\mu(w_i,w_j)\) with \(B_\mu=a\Omega_{12}+b\Omega_{34}\).
Writing \(A_i=[x_i:y_i]\), \(B_i=[z_i:t_i]\in\mathbb P^1\):

* \((x_i,y_i)\ne(0,0)\) and \((z_i,t_i)\ne(0,0)\), else vertex \(i\) sees one
  ratio only;
* the ratio is well defined iff \(i\mapsto(A_i,B_i)\) is **injective**, i.e.
  \(X\) embeds into \(\mathbb P^1\times\mathbb P^1\) — the **Segre quadric** in
  \(\mathrm{PG}(3,p)\);
* after absorbing scalings into \(\lambda_i\in\mathbb F_p^\ast\),
  \[
   \rho(ij)=\bigl[\det(A_i,A_j)\;:\;\lambda_i\lambda_j\det(B_i,B_j)\bigr].
  \]

> **Lemma 3.** The colouring condition is exactly: \(h\circ\rho\) is a
> **one-factorization of \(K_{p+1}\)**. Indeed each vertex has \(p\) incident
> edges and must see all \(p\) colours, and \(p+1\) is even, so every colour
> class is a perfect matching.

> **Lemma 4.** \(\rho^{-1}([0:1])\) is the union of the cliques on the
> \(A\)-fibres, and \(\rho^{-1}([1:0])\) likewise for \(B\). A clique of size
> \(\ge3\) can never lie in a matching, so **all \(A\)-fibres and all
> \(B\)-fibres have size \(\le2\)**.

So the rank-four escape is real: unlike the Grassmann-line case, a *general*
pencil member has rank 4 and its zero set is not a union of cliques. Only the
two Pfaffian-root members retain the clique structure, and Lemma 4 is exactly
what survives of the old rigidity.

## 3. COMPUTATION — a local positive link at \(p=3\), and the frontier

**\(p=3\) escape, exhibited and checked:**
\(A=[(1,1),(0,1),(0,1),(1,1)]\), \(B=[(0,1),(0,1),(1,2),(1,2)]\),
\(\lambda=(1,1,1,2)\) gives three ratio classes, each a perfect matching of
\(K_4\) — a one-factorization. So the rank-four family is **not** empty, and
the Grassmann-line proof genuinely does not extend to it.

**Frontier, and it is only computation:** the reproducible checker performs
60,000 seeded random trials in the general fibre-size-\(\le2\) family at each
of \(p=5,7,11\), and finds no local link.  Additional exploratory campaigns
in the interactive session also found none, but are not promoted to evidence
because no exhaustive certificate was produced.

**This is not a proof.** The searches are randomized, not exhaustive, and the
sample spaces are large. No no-go at \(p\ge5\) is claimed, and in particular
nothing is claimed at \(p=17\): I neither constructed a local link there nor
excluded one.

The \(p=3\) / \(p\ge5\) split matches the Grassmann-line theorem's own
boundary, where \(p-1=(p+1)/2\) exactly at \(p=3\) and the argument correctly
gives no contradiction for the \(k=2\) case that does admit a tight colouring.
That is suggestive of a real threshold, not evidence of one.

## 4. What a proof would have to do

Lemma 4 leaves \(A,B:X\to\mathbb P^1\) with fibres \(\le2\) and \((A,B)\)
injective, plus the scalars \(\lambda_i\), and asks that the \(p+1\) ratio
classes group into \(p\) perfect matchings with exactly one double decoder
fibre. The counting is consistent at every level I checked — total edges,
per-vertex missing-ratio incidences \(\sum_\nu(p+1-2|C_\nu|)=p+1\) — so a
no-go must come from the multiplicative structure of
\(\lambda_i\lambda_j\det(B_i,B_j)/\det(A_i,A_j)\), not from counting. I did
not find such an argument.

## 5. Local link versus global Plücker systems

A local link is **strictly weaker** than the object needed. What is missing:

* one link fixes a single \((k-2)\)-face \(R\); a colouring needs *every* \(R\)
  simultaneously, with the same \(P,Q\);
* the \(w_i\) at different \(R\) are contractions of the *same* two decomposable
  \(k\)-forms, so the Segre-quadric configurations across faces are heavily
  coupled — none of that coupling is used or verified here;
* the decoder \(h\) is global: one map \(\mathbb P^1\to\mathbb F_p\) must work
  at every face at once, whereas §3 exhibits a link with its own \(h\);
* \(h\circ\rho\) being a one-factorization at every link is necessary, not
  sufficient, for a tight colouring of \(J(2k,k)\).

So the \(p=3\) item is a **local positive control**, not a construction, and it
is consistent with \(k=2\) being the one solved case.

## 6. Scope, restated

Solves #835: **no**. Proves a no-go for the rank-four family: **no**.
Constructs a colouring: **no**. What is proved is the local classification
(§1) and the exact geometric translation (§2); what is exhibited is a local
\(p=3\) escape; what is reported as computation only is the absence of local
links at \(p=5,7,11\). **Erdős–Rosenfeld #835 remains open.**
