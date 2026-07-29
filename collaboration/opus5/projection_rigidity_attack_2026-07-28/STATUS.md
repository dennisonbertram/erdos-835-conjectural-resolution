# STATUS — two-valued top-module projections for Erdős–Rosenfeld #835

Date: 2026-07-28.  Author: Claude Opus 5.  All arguments in `PROOF.md`.

## Verdict

**This projection attack does not yield (1) a uniform nonexistence theorem,
does not yield (2) a construction, and does not yet yield (3) a rigidity lemma
that reduces the problem.**  The formulation is an exact re-encoding of the
already-committed perfect-code condition; its graph-free projector identities
have zero slack, while top-module containment remains exactly the hard graph
condition.

Of the three outcomes requested, the honest result is a partial route audit.
#835 remains open.  The note closes the graph-free two-valued-idempotent
relaxation and one basic Krein-support test, but does not close every
projection, Schur, Terwilliger, or semidefinite attack.

## Strongest new results

1. **Theorem C1 (route vacuity), `PROOF.md` §3.**  The map
   \(\mathcal C\mapsto P=(qR-J)/N\) is a bijection between equipartitions of
   \(V(O_k)\) into \(q=k+1\) classes and symmetric matrices with entries in
   \(\{k/N,-1/N\}\) satisfying \(P^2=P\).  Under it, the *only* condition in
   the whole projection package that refers to \(O_k\) is \(AP=-P\), which is
   literally \((A+I)R=J\), the perfect-code partition condition and is
   equivalent to top-module containment \(P=E_{k-1}PE_{k-1}\).  Rank \(k\),
   trace \(k\), \(P\mathbf 1=0\), positive semidefiniteness, the Schur identity
   \(P\circ P=\frac{k-1}NP+\frac k{N^2}J\), **all** higher Schur powers, and the
   \(0/1\) equivalence condition on \((NP+J)/q\) hold identically for an
   arbitrary equipartition of an arbitrary finite set.  They are therefore
   information-free.

2. **Theorem B (the equivalence-class proviso is redundant), `PROOF.md` §2.**
   Any symmetric matrix with entries in \(\{k/N,-1/N\}\) and \(P^2=P\)
   *automatically* has its \(k/N\)-relation an equivalence relation with
   exactly \(q\) classes, each of size \(N/q\).  The attack statement assumes
   this as a side condition; it is a theorem.  Consequence: dropping only the
   equivalence-relation proviso does not enlarge the feasible set.  A
   contradiction that also uses top-module containment is not ruled out,
   because that containment is exactly the hard graph condition.

3. **Theorem G (one Krein-support test is closed), `PROOF.md` §5.**  Pushing
   the Schur identity through the Krein parameters yields a genuine new
   necessary condition — \(q^{\,k-1}_{k-1,k-1}\ne0\) in the Johnson scheme
   \(J(2k-1,k-1)\) (Proposition F) — and then proves it can never fire: for
   every even \(k>2\), if a single \(S(k-2,k-1,2k-1)\) exists then
   \(\tau(y_C,y_C,y_C)=N(q-1)(q-2)/q^3>0\), which forces \(q^{k-1}_{k-1,k-1}>0\);
   and if no such Steiner system exists, no partition exists for a trivial
   reason.  This is an exact statement of why one perfect code is enough to
   satisfy this scalar Krein-support condition.  It does not close stronger
   Schur, Terwilliger, or semidefinite constraints on the full
   \(k\)-dimensional simplex subspace.

4. **Corollary I2 (one equitable-partition comparison is not stronger),
   `PROOF.md` §6.**  For the colour partition, the cell-indicator spectral
   comparison lemma is the special case of design quadrature obtained by
   restricting the test vectors to equitable-partition cell indicators.  It is
   a subset of the same linear conditions, never a strictly stronger one.
   The independent audit retrieved arXiv:2605.17376 and confirms that its
   Corollary 2.4(a), specialised to a perfect code, contains this same
   quotient-eigenspace condition.  The paper's full Theorem 2.3 and Corollary
   2.4(b) use more general systems (6)--(8), so this note does not close those
   statements as an obstruction route.

5. **Proposition H (cubic normal form).**  On \(W=\operatorname{span}\{y_a\}\),
   the ambient invariant quadratic and cubic forms restrict to \(\frac Nq\)
   times the standard \(A_{q-1}\) forms.  This is graph-free once an
   equipartition is given; whether embedding such a subspace in the top module
   yields a stronger obstruction remains open.

## Exact remaining gap

Everything above is about the *method*.  The problem itself is untouched:

* No \(k\) is eliminated.  The first open case remains \(k=16\), i.e.
  \(LS(15,16,32)\) equivalently \(LS(14,15,31)\), equivalently a partition of
  \(O_{16}=KG(31,15)\) into 17 perfect codes.
* Any future argument must use the hard condition \(AP=-P\), equivalently
  \(P=E_{k-1}PE_{k-1}\), together with the \(0/1\) geometry of multiple colour
  classes.  It cannot rely only on the graph-free projector identities.
  Theorem G eliminates only the scalar test \(q^{k-1}_{k-1,k-1}\ne0\);
  stronger subspace-orientation, Schur, Terwilliger, or SDP constraints remain
  open.

## Independent audit surface

Every claim can be checked without re-deriving anything upstream:

| Claim | How to audit | Depends on computation? |
|---|---|---|
| Lemma 0 (eigenvalue \(-1\) is exactly \(V_{k-1}\)) | one line: solve \((-1)^i(k-i)=-1\) | no |
| Theorem A (1)–(8) | eight one-line matrix identities using \(R^2=\frac NqR\), \(RJ=\frac NqJ\), \(J^2=NJ\) | no |
| Theorem B | two entry computations of \(P^2=P\): diagonal gives class size \(N/q\); off-diagonal gives common-count \(s\in\{0,N/q\}\) | no |
| Theorem C / C1 | \(N\,AP=qAR-kJ\); compare with \(-NP\) | no |
| Lemma D (perfect code = Steiner) | Delsarte design characterisation + \(\binom{2k-1}{k-2}=\binom{2k-1}{k-1}\frac{k-1}{k+1}\) | no |
| Lemma E (Krein sum of squares) | expand \(\operatorname{tr}((E_i\circ E_j)E_l)\) in an orthonormal basis | no |
| Proposition F | \(P\circ P=\sum_{i,j}(w_i\circ w_j)(w_i\circ w_j)^{\mathsf T}\) | no |
| Theorem G | evaluate \(\sum_p y_p^3\) for \(y=\mathbf 1_C-\frac1q\mathbf 1\) | no |
| Lemma I / I1 / I2 | orthogonal decomposition of \(\langle\mathbf 1_P,\mathbf 1_Q\rangle\); quotient matrix of the colour partition is \(J_q-I_q\) | no |

**No claim in `PROOF.md` depends on a computation.**  This was forced: Python
execution and network access were both unavailable in this session.

`verify_projection_rigidity.py` (standard library, exact rationals) is provided
as an *independent* redundant check.  Opus did not execute it; the independent
audit ran it on 29 July 2026 and obtained `RESULT: 0 failure(s)`.  Its exact
scope:

* **A** — Theorem A(1)–(8) on random equipartitions with
  \((N,q)\in\{(12,3),(20,5),(35,5),(24,3)\}\), with no graph present.
* **B** — Theorem B verified *exhaustively* at \((N,q)=(6,3)\) by enumerating
  all \(2^{15}\) symmetric \(\{k/N,-1/N\}\)-matrices and checking that the ones
  with \(P^2=P\) are exactly the 15 equipartitions into 3 classes of size 2.
  \(q=2\) is deliberately excluded: Theorem B is stated for \(k\ge2\), and at
  \(k=1\) the class-size step of its proof degenerates.
* **C** — the closed form
  \(q^{d}_{dd}=\frac{m_d^2}{|X|}\sum_i p_i(d)^3/v_i^2\) for \(J(2k-1,k-1)\),
  evaluated exactly for \(k=4,6,10,12,16\), cross-checked at \(k=4\) against a
  directly constructed primitive idempotent on 35 vertices.
* **D** — \(k=4\) control: all 30 Fano planes are perfect codes of \(KG(7,3)\);
  the maximum number of pairwise disjoint ones is computed by exact max-clique
  and compared with the required \(q=5\).
* **E** — \(k=6\) control: a cyclic \(S(4,5,11)\) is constructed from 6 base
  blocks mod 11, verified to have \(\lambda=1\) on all \(\binom{11}{4}=330\)
  quadruples, verified to be a perfect code of \(KG(11,5)\), and shown to give
  \(\tau(y_C,y_C,y_C)>0\).

Scope limits of the script: it certifies **B** only at \(N\le6\); the general
statement is Theorem B.  It certifies **C** only at the five listed \(k\); the
general statement is Theorem G, which does not need it.  It proves nothing
about \(k=16\) beyond a Krein value.

## Scope relative to the full #835

* The object studied is the covering projection \(O_k\to K_{k+1}\), which by
  Lemma D/D1 is exactly a large set \(LS(k-2,k-1,2k-1)\).  Its equivalence with
  \(\chi(J(2k,k))=k+1\), i.e. with \(LS(k-1,k,2k)\), is the committed
  Odd-cover reduction in `erdos_835_conjectural_resolution.md` §4 and is
  **assumed here, not re-proved**.
* All results are stated for all even \(k>2\).  Theorem A, Theorem B,
  Theorem C, Lemma D, Lemma E, Proposition F, Theorem G, Lemma I are uniform in
  \(k\); none is restricted to \(k=16\), and none uses primality of \(k+1\).
* The odd-\(k\) cases are outside this note: for \(k\) odd, \(-1\) is not an
  eigenvalue of \(O_k\) (Lemma 0), so no such projection exists at all, and
  that is already committed upstream.
* The \(k=6\) control is met for Proposition F: the Witt design
  \(S(4,5,11)\) alone satisfies the scalar Krein-support condition, at a
  parameter where no \(LS(4,5,11)\) exists.  Thus that condition cannot
  separate "one perfect code exists" from "\(k+1\) disjoint perfect codes
  exist".  Stronger constraints on a full simplex subspace are not tested by
  Theorem G.

## Why this does or does not prove the full problem

**It does not.**  A negative resolution of #835 requires ruling out
\(LS(k-1,k,2k)\) for every \(k>2\).  Theorem C1 shows that the graph-free
two-valued-projector identities add no information beyond equipartition.
Top-module containment is **not** automatic: by Theorem C it is exactly
\((A+I)R=J\), the perfect-code condition.  The one scalar scheme consequence
extracted here (Proposition F) is proved never to fire (Theorem G), but the
note does not exclude stronger constraints on how the full simplex subspace
sits inside the top module.

**It does not prove a construction either.**  Theorem B removes a hypothesis
but adds no existence: it says that if such a \(P\) exists it is combinatorial,
not that one exists.

**What it does establish** is a narrower boundary: the remaining content of
#835 is not present in two-valued idempotency or its graph-free Schur powers.
It remains in the requirement that the resulting equipartition projector lie
in the top Johnson module, equivalently in the joint \(0/1\) geometry and
disjointness of the constituent Steiner systems.
