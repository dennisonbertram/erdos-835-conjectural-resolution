# Rung-uniform intersection rigidity, and an exact tail dichotomy for large sets

Date: 2026-07-28.  Author: Claude Opus 5.

**Nothing in this note resolves Erdős–Rosenfeld Problem #835.**  Everything
asserted as a theorem below is proved by hand and can be re-derived with pencil
and paper.  **No script was executed in this session** — the interpreter was
permission-gated, as was web access — so no claim rests on a computation or on
a literature lookup made during this session.  The two scripts in this
directory are audit surface only and are labelled *unrun* throughout.

---

## 0.  What is new here, and what is not

The repository already proves, **for the top rung only** (the Steiner systems
`S(k-1,k,2k)` themselves), the following four facts, in
`../../opus5_v2/PROOF.md`:

* Theorem 1.3 — the block-intersection distribution of an \(S(k-1,k,2k)\) is
  forced;
* Theorem 2.1 — every \(S(k-1,k,2k)\) with \(k\) even is closed under
  complementation;
* Theorem 3.1 — the cross-class distribution in a tight colouring is forced;
* Theorem 3.2 — every single-block shell count reproduces exactly \(r\le k+1\)
  and nothing better.

**What is new in this note:**

1. **Theorem 1 / Theorem 2** — the same two distributions, for *every*
   \(S(t,t+1,v)\), with \(t\) and \(v\) arbitrary.  The repository's
   Theorems 1.3 and 3.1 are the single case \((t,v)=(k-1,2k)\).  The proof
   below is a corrected and shortened binomial inversion (§2.2), and §2.3
   gives a second, independent derivation from the Johnson scheme that does not
   use inversion at all.  So this is also an independent re-verification of the
   repository's top-rung results by a different method.
2. **Theorem 3 (rung-uniform delimiter)** — for *every* rung \(t\) of the
   #835 tower and *every* prime \(p\), every forced count is a nonnegative
   integer and every single-block shell count reproduces exactly \(r\le p\).
   This upgrades the repository's Theorem 3.2 from one rung at \(k=16\) to
   the whole tower at every admissible \(k\), and it closes the first-order
   counting route **uniformly in \(k\)** rather than case by case.
3. **Corollary 4** — the exact rung at which each structural phenomenon
   appears: complement-closure occurs at the top rung and *only* there;
   "no two blocks disjoint" occurs at rung \(p-3\) and *only* there.  The
   repository has the first as a standalone theorem; the second and the
   "only there" statements are new.
4. **Theorem 5 (tail dichotomy for large sets)** — an exact reduction of the
   last one, two and three systems of a large set to: automatic /
   bipartiteness / graph 3-colouring, uniformly in \((t,v)\).  This is the
   global analogue, at the level of whole Steiner systems, of the local
   Theorem E of `../post_r0_global_bridge/NOTE.md`, which is about matchings
   inside one first-lift instance.  The \(r=q-1\) case is the repository's
   gap lemma (`../../../evidence/large_set_literature_2026-07-26.md:8-19`);
   the \(r=q-2\) and \(r=q-3\) cases are new.
5. **Theorem 6** — the local Latin-rectangle characterisation, and the
   observation that it saturates to a full Latin square exactly at the top
   rung.

Facts used from the repository, not reproved here: the star reformulation of
a large set (`../unrestricted_ls3420_attack_2/NOTE.md:36-50`), the derivation
tower (`../../../erdos_835_conjectural_resolution.md:96-101`), and the
divisibility theorem \(k+1\) prime (`ibid.:56-89`).

---

## 1.  Objects and notation, fixed once

\(X\) is a \(v\)-set.  For \(0\le t<v\) an **\(S(t,t+1,v)\)** is a family
\(\mathcal D\subseteq\binom X{t+1}\) such that every \(t\)-subset of \(X\)
lies in exactly one member of \(\mathcal D\).  Write

\[
  K:=t+1,\qquad q:=v-t .
\tag{1.1}
\]

\(q\) is the parameter that controls everything below.  A **large set**
\(LS(t,t+1,v)\) is a partition of \(\binom X{t+1}\) into pairwise disjoint
\(S(t,t+1,v)\)'s; the number of classes is \(q\)
(`../../tower_automorphism_lemmas.md:9-13`).

**Lemma 1.1 (block counts).**  In an \(S(t,t+1,v)\), the number of blocks
containing a fixed \(i\)-set is
\[
  \lambda_i=\frac{\binom{v-i}{t-i}}{t+1-i}=\frac1q\binom{v-i}{K-i}
  \qquad(0\le i\le t),
\]
and \(|\mathcal D|=\lambda_0=\frac1q\binom v{K}=:N\).

*Proof.*  The first expression is the standard double count of pairs
\((T,A)\) with \(I\subseteq T\subseteq A\), \(|T|=t\).  For the second,
\[
  \binom{v-i}{K-i}
  =\binom{v-i}{t-i}\cdot\frac{(v-i)-(t-i)}{t+1-i}
  =\binom{v-i}{t-i}\cdot\frac{q}{t+1-i}. \qquad\square
\]

Two blocks are at **Johnson distance \(i\)** when \(|A\cap A_0|=K-i\).
Distance \(1\) is impossible in a Steiner system (two blocks sharing \(t\)
points would put a \(t\)-set in two blocks); distance \(K\) means disjoint.

Throughout, "the #835 tower at \(k\)" means the family of objects
\(LS(t,t+1,t+k+1)\), \(1\le t\le k-1\), forced by a tight colouring of
\(J(2k,k)\); every member has exactly \(k+1\) classes, so **\(q=k+1=p\) is
constant up the tower** and equal to the number of colours.

---

## 2.  Theorem 1: the forced intersection distribution of any \(S(t,t+1,v)\)

> **Theorem 1.**  Let \(\mathcal D\) be an \(S(t,t+1,v)\), let \(A_0\in\mathcal D\)
> and for \(0\le i\le K\) let \(N_{(i)}\) be the number of blocks
> \(A\in\mathcal D\) with \(|A\cap A_0|=K-i\) (so \(N_{(0)}=1\) counts \(A_0\)).
> Then
> \[
>   \boxed{\;
>   N_{(i)}=\frac{\binom{K}{i}\Bigl[\binom{q-1}{i}+(-1)^i\,(q-1)\Bigr]}{q}\;}
>   \qquad (0\le i\le K),
> \tag{2.1}
> \]
> with \(K=t+1\), \(q=v-t\).  In particular the distribution depends only on
> the parameters, never on which system or which block is chosen.

### 2.1  Immediate specialisations and checks

* \(i=0\): \(\bigl[1+(q-1)\bigr]/q=1\).  ✔
* \(i=1\): \(K\bigl[(q-1)-(q-1)\bigr]/q=0\).  ✔  (no two blocks share \(t\)
  points).
* \(\sum_{i=0}^{K}N_{(i)}
   =\frac1q\Bigl[\sum_i\binom Ki\binom{q-1}i+(q-1)\sum_i(-1)^i\binom Ki\Bigr]
   =\frac1q\binom{K+q-1}{K}=\frac1q\binom v{K}=N\), using Vandermonde and
  \((1-1)^K=0\) for \(K\ge1\).  ✔
* \((t,v)=(k-1,2k)\), so \(K=k\), \(q=k+1\): writing \(j=K-i\) for the
  intersection size, \(\binom Ki=\binom kj\) and \(\binom{q-1}i=\binom ki=\binom kj\),
  so (2.1) reads \(N_{(i)}=\frac{\binom kj(\binom kj+(-1)^{k-j}k)}{k+1}\).
  This is **exactly** Theorem 1.3 of `../../opus5_v2/PROOF.md`.  ✔
* \(S(2,3,9)=\mathrm{AG}(2,3)\): \(t=2,K=3,v=9,q=7\).
  \(N_{(0)}=1\), \(N_{(1)}=0\),
  \(N_{(2)}=3(15+6)/7=9\), \(N_{(3)}=(20-6)/7=2\); total \(12=|\mathcal D|\).
  A line of \(\mathrm{AG}(2,3)\) meets nine lines in a point and is parallel to
  two.  ✔
* \(S(4,5,11)\) (Mathieu): \(t=4,K=5,v=11,q=7\).
  \(N_{(5)}=\bigl[\binom65-6\bigr]/7=0\): **no two blocks are disjoint**, the
  known fact that pentads of \(S(4,5,11)\) meet in \(1,2,3\) points.  ✔
* \(S(5,6,12)\) (Mathieu): \(t=5,K=6,v=12,q=7\).
  \(N_{(6)}=\bigl[\binom66+6\bigr]/7=1\): every hexad has exactly one disjoint
  hexad, namely its complement.  ✔

### 2.2  Proof of Theorem 1 (binomial inversion)

Fix \(A_0\in\mathcal D\).  For \(0\le j\le K\) let \(N_j\) be the number of
\(A\in\mathcal D\setminus\{A_0\}\) with \(|A\cap A_0|=j\); so \(N_K=0\) and
\(N_{(i)}=N_{K-i}\) for \(i\ge1\).

Count pairs \((I,A)\) with \(I\subseteq A_0\), \(|I|=i\),
\(A\in\mathcal D\setminus\{A_0\}\), \(I\subseteq A\), in two ways.  By \(I\)
first: each \(i\)-subset of \(A_0\) lies in \(\lambda_i\) blocks, one of which
is \(A_0\).  Hence for \(0\le i\le t\)
\[
  \sum_{j}N_j\binom ji=\binom Ki(\lambda_i-1)=:R_i ,
\tag{2.2}
\]
and for \(i=K\) both sides are \(0\); put \(R_K:=0\).  Binomial inversion of
(2.2) gives
\[
  N_j=\sum_{i=j}^{K}(-1)^{i-j}\binom ij R_i .
\tag{2.3}
\]
Set \(\lambda_K:=1\), so that \(R_i=\binom Ki(\lambda_i-1)\) holds uniformly for
\(0\le i\le K\) (at \(i=K\) it reads \(R_K=1\cdot(1-1)=0\) ✔).  Use the
absorption identity \(\binom ij\binom Ki=\binom Kj\binom{K-j}{i-j}\) and write
\(m:=K-j\), \(s:=i-j\).  Then (2.3) splits as
\[
  N_j=\underbrace{\sum_{i=j}^{K}(-1)^{i-j}\binom Kj\binom{K-j}{i-j}\lambda_i}_{S_1}
     -\underbrace{\binom Kj\sum_{s=0}^{m}(-1)^s\binom ms}_{S_2},
\qquad
  S_2=\binom Kj\,[\,m=0\,],
\tag{2.4}
\]
the value of \(S_2\) being \(\binom Kj(1-1)^{m}\).

*Evaluation of \(S_1\).*  Write \(\lambda_i=\frac1q\binom{v-i}{K-i}\), valid by
Lemma 1.1 for \(0\le i\le t\).  At \(i=K\) that expression would give
\(\frac1q\binom{v-K}{0}=\frac1q\), whereas the true value is
\(\lambda_K=1=\frac1q+\frac{q-1}{q}\).  Hence
\[
  S_1=\frac{\binom Kj}{q}\,\Sigma+(-1)^m\binom Kj\,\frac{q-1}{q},
  \qquad
  \Sigma:=\sum_{s=0}^{m}(-1)^s\binom ms\binom{v-j-s}{\,m-s\,},
\tag{2.5}
\]
the second term being the single \(i=K\) correction, whose sign is
\((-1)^{K-j}=(-1)^m\) and whose absorption factor is
\(\binom Kj\binom{K-j}{K-j}=\binom Kj\).

Since \(v-j=v-K+m=(q-1)+m\), we have
\(\binom{v-j-s}{m-s}=\binom{q-1+(m-s)}{m-s}=[x^{m-s}](1-x)^{-q}\), so
\[
  \Sigma=[x^m]\bigl((1-x)^m(1-x)^{-q}\bigr)=[x^m](1-x)^{-(q-m)}
        =\binom{q-1}{m}.
\tag{2.6}
\]
(For \(q>m\) this is \([x^m](1-x)^{-(q-m)}=\binom{(q-m-1)+m}{m}=\binom{q-1}m\);
for \(q\le m\) the function \((1-x)^{m-q}\) is a polynomial of degree
\(m-q<m\), so \(\Sigma=0=\binom{q-1}{m}\).)

Substituting (2.6) into (2.5),
\[
  S_1=\frac{\binom Kj\Bigl[\binom{q-1}{m}+(-1)^m(q-1)\Bigr]}{q},
\tag{2.7}
\]
and \(N_j=S_1-S_2\).  For \(m\ge1\), i.e. \(0\le j\le K-1\), \(S_2=0\) and
\(N_j=S_1\), which is (2.1) with \(i=m\).  For \(m=0\), i.e. \(j=K\),
\(S_1=\frac{1+(q-1)}{q}=1\) and \(S_2=1\), so \(N_K=0\) ✔, while
\(N_{(0)}=1=S_1\) is the same count taken *including* \(A_0\).  Hence (2.1)
holds for all \(0\le i\le K\) under the stated convention.  \(\square\)

> **Where the boundary term matters.**  The \(i=K\) row of (2.2) is degenerate
> and must be handled in **both** sums: \(\lambda_K=1\) rather than
> \(\frac1q\), and \(S_2\) is \(\binom Kj\) rather than \(0\), exactly when
> \(m=0\).  The repository's Theorem 1.3 sidesteps this by truncating the
> inversion at \(i=K-1\); the all-\(i\) statement (2.1) has to carry it.

### 2.3  Second, independent proof (Johnson scheme)

This derivation uses no inversion and is included as an independent check of
(2.1) — and hence of the repository's Theorem 1.3.

Work in the Johnson scheme \(J(v,K)\) on \(\Omega=\binom XK\),
\(M:=|\Omega|=\binom vK\), with distance-\(i\) adjacency matrices \(A_i\) and
eigenspaces \(V_0,\dots,V_K\).  Two standard facts:

* **(J1)** A family \(\mathcal D\subseteq\Omega\) is a \(t\)-design iff its
  characteristic vector satisfies \(\chi^{(j)}=0\) for \(1\le j\le t\), where
  \(\chi=\sum_j\chi^{(j)}\) is the decomposition into the \(V_j\).
* **(J2)** The eigenvalue of \(A_i\) on the top eigenspace \(V_K\) is
  \[
    P_i(K)=\sum_{h=0}^i(-1)^h\binom Kh\binom{K-K}{i-h}\binom{v-2K}{i-h}
          =(-1)^i\binom Ki ,
  \]
  because \(\binom{0}{i-h}\) vanishes unless \(h=i\).  (Sanity check at
  \(i=1\): the Johnson graph eigenvalue \((K-m)(v-K-m)-m\) at \(m=K\) is
  \(-K=(-1)^1\binom K1\).  ✔)

An \(S(t,t+1,v)\) is a \(t\)-design with \(K=t+1\), so by (J1)
\(\chi=\chi^{(0)}+\chi^{(K)}\) — only two components survive.  Now
\(\chi^{(0)}=\frac NM\mathbf 1\) and \(\frac NM=\frac{1}{q}\) by Lemma 1.1, so
\[
  \|\chi^{(0)}\|^2=\frac{N^2}{M}=\frac Nq,\qquad
  \|\chi^{(K)}\|^2=\|\chi\|^2-\|\chi^{(0)}\|^2=N\Bigl(1-\frac1q\Bigr).
\tag{2.10}
\]
Hence the number of *ordered* pairs of blocks at distance \(i\) is
\[
  \chi^{\mathsf T}A_i\chi
   =P_i(0)\|\chi^{(0)}\|^2+P_i(K)\|\chi^{(K)}\|^2
   =\binom Ki\binom{q-1}{i}\frac Nq+(-1)^i\binom Ki\,N\frac{q-1}{q},
\]
using \(P_i(0)=v_i=\binom Ki\binom{v-K}{i}=\binom Ki\binom{q-1}{i}\).  Dividing
by \(N\) gives exactly (2.1).  \(\square\)

> **Remark.**  The two proofs are genuinely independent: §2.2 uses only
> Lemma 1.1 and binomial identities, §2.3 uses only (J1)–(J2).  They agree,
> and both agree with the four hand checks in §2.1.

---

## 3.  Theorem 2: the forced cross-class distribution

> **Theorem 2.**  Let \(\mathcal D_a\ne\mathcal D_b\) be two block-disjoint
> \(S(t,t+1,v)\)'s, let \(A_0\in\mathcal D_a\), and let \(N^{(b)}_{(i)}\) be the
> number of blocks of \(\mathcal D_b\) at distance \(i\) from \(A_0\).  Then
> \[
>   \boxed{\;
>   N^{(b)}_{(i)}=\frac{\binom Ki\Bigl[\binom{q-1}{i}-(-1)^i\Bigr]}{q}\;}
>   \qquad(0\le i\le K).
> \tag{3.1}
> \]
> This does not depend on \(b\), nor on \(A_0\), nor on the systems.

*Proof.*  Identical to §2.2 with \(R_i=\binom Ki\lambda_i\) for \(i\le t\) (no
\(-1\), because \(A_0\notin\mathcal D_b\)) and \(R_K=0\).  The subtracted sum
\(S_2\) is now absent entirely, and in \(S_1\) the \(i=K\) correction runs the
other way: the Lemma 1.1 expression would give \(\frac1q\) there whereas the
true contribution is \(0\), so \(S_1=\frac{\binom Kj}{q}\Sigma
-(-1)^m\binom Kj\frac1q\).  With \(\Sigma=\binom{q-1}{m}\) from (2.6) this is
(3.1).  Equivalently, by §2.3: \(\chi_a^{\mathsf T}A_i\chi_b
=P_i(0)\frac{N}{q}+P_i(K)\langle\chi_a^{(K)},\chi_b^{(K)}\rangle\) with
\(\langle\chi_a^{(K)},\chi_b^{(K)}\rangle=\langle\chi_a,\chi_b\rangle
-\frac{N^2}M=-\frac Nq\), which is (3.1).  \(\square\)

*Checks.*
\(N^{(b)}_{(0)}=\bigl[1-1\bigr]/q=0\) ✔ (the systems are disjoint).
\(N^{(b)}_{(1)}=K\bigl[(q-1)+1\bigr]/q=K=t+1\) ✔ (of the \(K(q-1)\) Johnson
neighbours of \(A_0\), each of the \(q-1\) other classes takes exactly \(t+1\)).
**Completeness identity:**
\[
  N_{(i)}+(q-1)N^{(b)}_{(i)}
  =\frac{\binom Ki}{q}\Bigl[q\binom{q-1}{i}\Bigr]
  =\binom Ki\binom{q-1}{i}=v_i ,
\tag{3.2}
\]
the total number of \(K\)-sets at distance \(i\) from \(A_0\).  ✔  At
\((t,v)=(k-1,2k)\), (3.1) is Theorem 3.1 of `../../opus5_v2/PROOF.md`.  ✔

---

## 4.  Theorem 3: the rung-uniform delimiter

> **Theorem 3.**  Let \(p\) be an odd prime and let \(1\le t\le p-2\), so that
> \(\bigl(t,\,v=t+p\bigr)\) is a rung of the #835 tower at \(k=p-1\)
> (here \(q=p\)).  Then:
>
> 1. **(Integrality.)**  Every \(N_{(i)}\) of (2.1) and every
>    \(N^{(b)}_{(i)}\) of (3.1) is an integer.
> 2. **(Nonnegativity.)**  Every \(N_{(i)}\) and \(N^{(b)}_{(i)}\) is
>    \(\ge 0\).
> 3. **(No slack.)**  If \(\mathcal D_1,\dots,\mathcal D_r\) are pairwise
>    block-disjoint \(S(t,t+1,t+p)\)'s, then for every \(i\) with
>    \(1\le i\le\min(t+1,\,p-2)\), the shell count around a fixed block yields
>    exactly \(r\le p\) and nothing stronger.  The single remaining index,
>    \(i=p-1\) (which occurs only at the top rung \(t=p-2\)), is **degenerate**:
>    there \(N^{(b)}_{(p-1)}=0\) and the shell inequality is \(0\le0\), giving
>    no bound at all.  That degenerate shell is exactly the complement-closure
>    statement of Corollary 4.
>
> Consequently **the single-base-block same-class and cross-class shell
> inequalities computed in Theorems 1–2 cannot obstruct #835 at any rung,
> for any prime \(p\)**: every one of them returns only the trivial packing
> bound \(r\le p\).  This does not rule out joint statistics based at several
> blocks, higher-order intersection data, or strengthened LP/SDP hierarchies.

*Proof.*  1.  For \(p\) prime, \(\binom{p-1}{i}\equiv(-1)^i\pmod p\)
(each factor \(\frac{p-\ell}{\ell}\equiv-1\)).  Hence in (2.1) the bracket is
\(\equiv(-1)^i+(-1)^i(p-1)=(-1)^i\cdot p\equiv0\), and in (3.1) it is
\(\equiv(-1)^i-(-1)^i=0\).

2.  For (3.1): \(\binom{p-1}{i}\ge1\ge(-1)^i\) for \(0\le i\le p-1\), and
\(i\le t+1\le p-1\).  For (2.1) with \(i\) even the bracket is positive.  For
\(i\) odd the bracket is \(\binom{p-1}{i}-(p-1)\); on \(1\le i\le p-2\) the
binomial \(\binom{p-1}{i}\) attains its minimum \(p-1\) exactly at \(i=1\) and
\(i=p-2\), so the bracket is \(\ge0\) there.  The only index in
\(0\le i\le t+1\le p-1\) not covered by that range is \(i=p-1\), which is even
because \(p\) is odd; so no odd index escapes, and every bracket is \(\ge0\).

3.  Fix \(A_0\in\mathcal D_1\).  Theorem 1 applies to \(\mathcal D_1\) and
Theorem 2's computation applies verbatim to each \(\mathcal D_s\), \(s\ge2\)
(it used only that \(\mathcal D_s\) is a Steiner system not containing
\(A_0\)).  Summing and bounding by \(v_i\):
\[
  \frac{\binom Ki\bigl[\binom{p-1}i+(-1)^i(p-1)\bigr]}{p}
  +(r-1)\frac{\binom Ki\bigl[\binom{p-1}i-(-1)^i\bigr]}{p}
  \ \le\ \binom Ki\binom{p-1}{i}.
\]
Divide through by \(\binom Ki/p>0\) (valid for \(0\le i\le K=t+1\)) and put
\(\beta:=\binom{p-1}i-(-1)^i\).  The inequality becomes
\(\binom{p-1}i+(-1)^i(p-1)+(r-1)\beta\le p\binom{p-1}{i}\); moving the first
two terms to the right,
\[
  (r-1)\beta\ \le\ p\binom{p-1}i-\binom{p-1}i-(-1)^i(p-1)
              =(p-1)\Bigl[\binom{p-1}i-(-1)^i\Bigr]=(p-1)\beta .
\]
Now \(\beta=0\) iff \(\binom{p-1}i=(-1)^i\), which forces \(i\) even and
\(\binom{p-1}i=1\), i.e. \(i\in\{0,p-1\}\).  So for
\(1\le i\le\min(t+1,p-2)\) we have \(\beta>0\) (at \(i=1\),
\(\beta=(p-1)+1=p\); for \(2\le i\le p-2\), \(\binom{p-1}i\ge p-1>1\ge|(-1)^i|\)),
and dividing gives \(r-1\le p-1\), i.e. \(r\le p\) — no shell gives anything
sharper.  At \(i=p-1\), which is in range only when \(t=p-2\), \(\beta=0\) and
the inequality reads \(0\le0\): that shell is degenerate and yields no bound,
consistent with \(N^{(b)}_{(p-1)}=0\) (Corollary 4).  \(\square\)

> **Corollary 3.1 (route closure, uniform in \(k\)).**  The "first-order
> counting" route is closed for the whole problem, not merely at \(k=16\):
> for every admissible \(k=p-1\) and every rung \(t\), the Delsarte moment
> system **after imposing the \(S(t,t+1,v)\) design equations** has a unique
> inner distribution, namely (2.1), and it is nonnegative and integral; the
> dual distribution is \(B^*_0=1\), \(B^*_j=0\) for \(1\le j\le t\),
> \(B^*_{t+1}=q-1\).  Thus this particular one-base-block moment system has no
> residual feasible region to cut; stronger multi-block or semidefinite
> systems are not addressed.

*Proof of the dual values.*  \(B^*_j=\frac{M}{N^2}\|\chi^{(j)}\|^2\); by
(2.10), \(B^*_0=1\) and \(B^*_{K}=\frac MN\cdot\frac{q-1}{q}=q-1\), and (J1)
kills \(1\le j\le t\).  \(\square\)

---

## 5.  Corollary 4: which rung produces which structure

> **Corollary 4.**  In the #835 tower at \(k=p-1\), let \(D_t:=N_{(t+1)}\) be
> the number of blocks of a class disjoint from a given block of that class.
> Then
> \[
>   D_t=\frac{\binom{p-1}{t+1}+(-1)^{t+1}(p-1)}{p} .
> \tag{5.1}
> \]
> In particular, over the whole tower \(1\le t\le p-2\):
>
> * \(D_{p-2}=\dfrac{1+(p-1)}{p}=1\): **at the top rung every class is closed
>   under complementation** (the unique disjoint block must be the
>   complement, since \(v=2k\)).  This recovers
>   `../../opus5_v2/PROOF.md` Theorem 2.1.
> * \(D_{p-3}=\dfrac{(p-1)-(p-1)}{p}=0\): **at rung \(p-3\) every class is an
>   intersecting family** — no two of its blocks are disjoint, although
>   \(2(p-2)\le 2p-3=v\) leaves room for disjoint pairs.
> * \(D_{p-4}=\dfrac{\binom{p-1}{2}+(p-1)}{p}=\dfrac{p-1}{2}\).
> * For \(1\le t\le p-5\), \(D_t\ge2\).  No monotonicity is asserted: the
>   binomial term is symmetric and generally rises and then falls.
> * Hence \(D_t=1\) **only** at \(t=p-2\) and \(D_t=0\) **only** at \(t=p-3\).

*Proof.*  (5.1) is (2.1) at \(i=K=t+1\) with \(q=p\).  The three displayed
values are direct substitutions.  For the last two claims: \(D_t=0\) forces
\(\binom{p-1}{t+1}=p-1\) with \(t+1\) odd, i.e. \(t+1\in\{1,p-2\}\); \(t+1=1\)
is excluded because \(t\ge1\); so \(t=p-3\).  \(D_t=1\) forces
\(\binom{p-1}{t+1}+(-1)^{t+1}(p-1)=p\).  With \(t+1\) even this needs
\(\binom{p-1}{t+1}=1\), i.e. \(t+1\in\{0,p-1\}\), so \(t=p-2\).  With \(t+1\)
odd it needs \(\binom{p-1}{t+1}=2p-1\).  For odd \(i\) in the range
\(1\le i\le p-2\), either \(i\in\{1,p-2\}\) and \(\binom{p-1}i=p-1\ne2p-1\), or
\(3\le i\le p-4\) and
\(\binom{p-1}i\ge\binom{p-1}3=\frac{(p-1)(p-2)(p-3)}6\), which exceeds
\(2p-1\) for every \(p\ge7\) (at \(p=7\): \(20>13\), and the left side grows
cubically while the right grows linearly).  For \(p=5\) the only odd \(t+1\)
with \(1\le t\le3\) is \(t+1=3\), where \(D_2=(\binom43-4)/5=0\ne1\).  Hence
\(t=p-2\) is the only solution.  \(\square\)

*Checks.*  \(p=7\): rung \(p-2=5\) is \(S(5,6,12)\) — hexads pair off into
complements ✔; rung \(p-3=4\) is \(S(4,5,11)\) — pentads pairwise meet ✔.

> **Corollary 4.1 (why the top rung is the only self-dual one).**
> Complementation \(B\mapsto X\setminus B\) maps \(\binom XK\) to itself iff
> \(v=2K\), i.e. \(t=p-2\).  So the forced complement-closure of Corollary 4
> is available at the top rung and nowhere else in the tower; it is not a
> constraint that propagates downwards.

---

## 6.  Theorem 5: the exact tail dichotomy for large sets

Let \(\mathcal D_1,\dots,\mathcal D_r\) be pairwise block-disjoint
\(S(t,t+1,v)\)'s and let \(\mathcal E:=\binom X{t+1}\setminus\bigcup_s\mathcal D_s\)
be the leftover, \(|\mathcal E|=(q-r)N\).

**Lemma 5.1 (leftover star count).**  Every \(t\)-set \(T\subseteq X\) lies in
exactly \(q-r\) members of \(\mathcal E\).

*Proof.*  The star \(\{T\cup\{y\}:y\notin T\}\) has \(q\) members; each
\(\mathcal D_s\) contains exactly one of them, and these \(r\) blocks are
distinct because the systems are disjoint.  \(\square\)

Define the **conflict graph** \(G_{\mathcal E}\): vertex set \(\mathcal E\),
with \(A\sim A'\) iff \(|A\cap A'|=t\).  By Lemma 5.1 each \(t\)-set
contributes a clique of size \(q-r\) on the \(q-r\) leftover blocks above it,
these cliques are edge-disjoint (an edge determines \(A\cap A'\)), and every
edge arises this way.  Each block lies above exactly \(t+1\) \(t\)-sets, so

\[
  G_{\mathcal E}\ \text{is}\ (t+1)(q-r-1)\text{-regular},\qquad
  |E(G_{\mathcal E})|=\binom vt\binom{q-r}{2}.
\tag{6.1}
\]

> **Theorem 5 (tail dichotomy).**  With the notation above:
>
> 1. **\(r=q-1\).**  \(\mathcal E\) is itself an \(S(t,t+1,v)\); the last
>    system is automatic, and \(D\ne q-1\).  *(This is the repository's gap
>    lemma, `evidence/large_set_literature_2026-07-26.md:8-19`; it is the case
>    \(q-r=1\) of Lemma 5.1.)*
> 2. **\(r=q-2\).**  \(G_{\mathcal E}\) is \((t+1)\)-regular with
>    \(\binom vt\) edges on \(2N\) vertices, and
>    \[
>      \mathcal E\ \text{splits into two disjoint}\ S(t,t+1,v)
>      \iff G_{\mathcal E}\ \text{is bipartite}.
>    \]
> 3. **\(r=q-3\).**  \(G_{\mathcal E}\) is \(2(t+1)\)-regular on \(3N\)
>    vertices and is the edge-disjoint union of \(\binom vt\) triangles, each
>    vertex in \(t+1\) of them, and
>    \[
>      \mathcal E\ \text{splits into three disjoint}\ S(t,t+1,v)
>      \iff \chi(G_{\mathcal E})\le3 .
>    \]
>
> Consequently
> \[
>   LS(t,t+1,v)\ \text{exists}\iff
>   \exists\ q-2\ \text{pairwise disjoint}\ S(t,t+1,v)\ \text{whose leftover
>   conflict graph is bipartite.}
> \]

*Proof.*  1.  \(q-r=1\): every \(t\)-set lies in exactly one member of
\(\mathcal E\), which is the definition.

2.  \(q-r=2\): every \(t\)-set lies in exactly two members of \(\mathcal E\),
and they are adjacent in \(G_{\mathcal E}\).  If \(\mathcal E=\mathcal F_1\sqcup\mathcal F_2\)
with both \(\mathcal F_i\) Steiner systems then each \(t\)-set has one member
in each part, so no edge is monochromatic: \(G_{\mathcal E}\) is bipartite
with parts \(\mathcal F_1,\mathcal F_2\).  Conversely a proper \(2\)-colouring
of \(G_{\mathcal E}\) gives each \(t\)-set exactly one leftover block of each
colour — because its two leftover blocks are adjacent, hence differently
coloured — so each colour class covers every \(t\)-set exactly once and is an
\(S(t,t+1,v)\).  The parameters are (6.1) at \(q-r=2\), and
\(|\mathcal E|=2N\); the edge count \(\binom vt\cdot1\) agrees with
\(\tfrac12\cdot 2N(t+1)=N(t+1)=\binom vt\) by Lemma 1.1.

3.  \(q-r=3\): the three leftover blocks above each \(t\)-set are pairwise
adjacent, giving a triangle; the same argument shows that proper
\(3\)-colourings correspond exactly to splittings, the triangles being exactly
the "rainbow" constraints.  Degrees and edge count are (6.1) at \(q-r=3\).

The final equivalence: if a large set exists, delete any \(q-2\) of its
classes — the leftover is the union of the remaining two, which \(2\)-colours
\(G_{\mathcal E}\) properly.  Conversely apply part 2.  \(\square\)

> **Corollary 5.2 (the remaining graph-theoretic information).**
> Bipartiteness of \(G_{\mathcal E}\) is equivalent to the absence of an odd
> cycle, while part 3 is an exact \(3\)-colourability condition.  The degree,
> vertex-count and edge-count identities in (6.1) alone do not decide either
> condition.  Theorem 5 therefore identifies the extra information still
> needed after those elementary counts; it does **not** rule out stronger
> cut, LP, SDP, or other graph-colouring formulations.

> **Corollary 5.3 (a parity test that is available but never fires here).**
> A \(d\)-regular bipartite graph has parts of equal size, hence an even number
> of vertices.  In part 2 of Theorem 5, \(|\mathcal E|=2N\) is even, so this
> test is vacuous.  After folding by complementation at the top rung
> (\(t=p-2\), where every class and hence \(\mathcal E\) is complement-closed
> by Corollary 4, and any splitting must be complement-closed too), the folded
> conflict graph is \(k\)-regular on \(N=C_k\) vertices, where
> \(C_k=\binom{2k}{k}/(k+1)\) is the Catalan number.  A Catalan number \(C_k\)
> is odd iff \(k=2^m-1\); since \(k=p-1\) is even, \(C_k\) is always even and
> the test is vacuous again.  **The parity route through Theorem 5 is
> therefore closed**, for every admissible \(k\).

*Proof of the folding claim.*  At \(t=p-2\), \(v=2k\), Corollary 4 gives
\(\sigma(\mathcal D_s)=\mathcal D_s\) for every class, so
\(\sigma(\mathcal E)=\mathcal E\); \(\sigma\) is fixed-point-free on
\(\binom X k\) and is an automorphism of \(G_{\mathcal E}\) because
\(|\bar A\cap\bar A'|=|A\cap A'|\).  No block is adjacent to its complement
(\(|A\cap\bar A|=0\ne k-1\) for \(k\ge2\)), so the quotient is a graph on
\(|\mathcal E|/2=N\) vertices in which \([A]\sim[A']\) iff
\(|A\cap A'|\in\{k-1,1\}\), and it is simple because the two cases are mutually
exclusive for \(k\ge3\).

For the degree, fix \(A\in\mathcal E\).  By Theorem 5 part 2 with \(t=k-1\),
\(G_{\mathcal E}\) is \(k\)-regular, so \(A\) has exactly \(k\) neighbours
\(A'_1,\dots,A'_k\in\mathcal E\) with \(|A\cap A'_j|=k-1\).  The blocks
\(A'\in\mathcal E\) with \(|A\cap A'|=1\) are exactly the complements
\(\bar A'_1,\dots,\bar A'_k\), since \(|A\cap\bar A'|=k-|A\cap A'|\) and
\(\mathcal E\) is complement-closed.  But \([\bar A'_j]=[A'_j]\), so these
contribute **no new quotient neighbours**: the quotient neighbours of \([A]\)
are exactly \([A'_1],\dots,[A'_k]\), which are pairwise distinct (if
\(A'_i=\bar A'_j\) with \(i\ne j\) then \(|A\cap A'_i|\) would be both \(k-1\)
and \(1\)).  Hence the quotient is \(k\)-regular, not \(2k\)-regular.

A splitting of \(\mathcal E\) into two \(S(k-1,k,2k)\)'s has both parts
complement-closed by Corollary 4, so it is \(\sigma\)-invariant and descends to
a proper \(2\)-colouring of the quotient; conversely a proper \(2\)-colouring
of the quotient lifts to a \(\sigma\)-invariant one, which is proper on
\(G_{\mathcal E}\) because \(A\sim A'\) implies \([A]\ne[A']\).  \(\square\)

---

## 7.  Theorem 6: the local Latin-rectangle characterisation

> **Theorem 6.**  Let \(c\) be an \(LS(t,t+1,v)\) colouring with colour set
> \(\mathcal C\), \(|\mathcal C|=q\), and let \(B\) be a block.  Index the
> Johnson neighbours of \(B\) by \((x,y)\in B\times(X\setminus B)\) via
> \(B-x+y\).  Then
> \[
>   L_B(x,y):=c(B-x+y)
> \]
> is a \((t+1)\times(q-1)\) **Latin rectangle** on the symbol set
> \(\mathcal C\setminus\{c(B)\}\): every row is a bijection onto that
> \((q-1)\)-set and every column has \(t+1\) distinct entries.  Conversely, a
> map \(c:\binom X{t+1}\to\mathcal C\) is an \(LS(t,t+1,v)\) colouring iff
> \(L_B\) is such a Latin rectangle for every \(B\).
>
> The rectangle is a full **Latin square of order \(q-1=k\)** exactly when
> \(t+1=q-1\), i.e. exactly at the top rung \(v=2k\).

*Proof.*  The neighbours of \(B\) are exactly the \(B-x+y\), and
\(B-x+y=B-x'+y'\) forces \((x,y)=(x',y')\); the induced subgraph on them is the
rook's graph, since \(|(B-x+y)\cap(B-x'+y')|=t\) iff \(x=x'\) or \(y=y'\).
Row \(x\) is the up-star at the \(t\)-set \(B\setminus\{x\}\) with the member
\(B\) removed: that star has \(q\) members, all differently coloured
(`../unrestricted_ls3420_attack_2/NOTE.md:36-50`), one of which is \(B\); so
the remaining \(q-1\) entries are a bijection onto
\(\mathcal C\setminus\{c(B)\}\).  Column \(y\) is the down-star at the
\((t+2)\)-set \(B\cup\{y\}\) with \(B\) removed: its \(t+2\) members are
pairwise adjacent, hence pairwise differently coloured, so the \(t+1\) entries
are distinct.  Conversely, ranging over all \(B\) covers every up-star, and
"every up-star rainbow" is the star reformulation.  Finally the rectangle has
\(t+1\) rows and \(q-1\) columns, and \(t+1=q-1\iff v=2t+2=2k\).  \(\square\)

> **Corollary 6.1.**  At the top rung, \(L_{\bar B}=L_B^{\mathsf T}\) for every
> block \(B\).

*Proof.*  \(L_{\bar B}(y,x)=c(\bar B-y+x)=c(\overline{B-x+y})=c(B-x+y)=L_B(x,y)\),
using Corollary 4 for the middle equality; the row index set of \(L_{\bar B}\)
is \(\bar B\), the column index set of \(L_B\), and the symbol sets agree
because \(c(\bar B)=c(B)\).  \(\square\)

---

## 8.  Independent audit surface

Everything in §§2–7 is proved by hand and can be re-derived with pencil and
paper.  An auditor should re-check, in this order:

* **(A1)** Lemma 1.1's second form, \(\lambda_i=\frac1q\binom{v-i}{K-i}\), on
  \(S(2,3,9)=\mathrm{AG}(2,3)\), where \(t=2,K=3,v=9,q=7\):
  \(\lambda_0=\frac17\binom93=\frac{84}{7}=12\) lines ✔;
  \(\lambda_1=\frac17\binom82=\frac{28}{7}=4\) lines through a point ✔;
  \(\lambda_2=\frac17\binom71=1\) line through a pair ✔.
  Note the upper index is \(v-i\) and the lower is \(K-i\); using \(t-i\) in
  the lower slot gives the *first* form and needs the extra division by
  \(t+1-i\).
* **(A2)** Theorem 1 on \(S(2,3,9)\), \(S(4,5,11)\), \(S(5,6,12)\),
  \(S(3,4,8)\) — the four checks of §2.1, plus the row-sum identity
  \(\sum_iN_{(i)}=N\).
* **(A3)** Theorem 1 against `../../opus5_v2/PROOF.md` Theorem 1.3 at
  \((t,v)=(k-1,2k)\) for \(k=4,6\): \((N_0,\dots,N_3)=(1,0,12,0)\) and
  \((1,0,45,40,45,0)\) in their indexing.
* **(A4)** The completeness identity (3.2) at several \((t,v,i)\).
* **(A5)** Theorem 3's integrality via \(\binom{p-1}{i}\equiv(-1)^i\bmod p\)
  for \(p=5,7,11,13,17\) and all \(i\).
* **(A6)** Theorem 5 part 2 on the smallest nontrivial instance available to
  an auditor: \(LS(2,3,9)\) has \(q=7\) classes; delete any five, and check
  that the leftover \(24\) triples form a \(3\)-regular bipartite graph under
  "share a pair".
* **(A7)** Corollary 5.3's Catalan parity: \(C_k\) odd iff \(k=2^m-1\);
  \(C_4=14\), \(C_6=132\), \(C_{16}=35357670\) — all even.

Two scripts are provided, both standard-library only and deterministic.
**Neither was executed in this session**, because no interpreter was
available; their output is therefore *not* evidence for any claim above, and
every claim above is proved without them.

```sh
cd "<repo root>"
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_intersection_distribution.py
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_tail_dichotomy.py
```

The first re-derives (2.1) and (3.1) by brute force from explicitly
constructed Steiner systems \(S(1,2,v)\), \(S(2,3,7)\), \(S(2,3,9)\),
\(S(3,4,8)\), \(S(4,5,11)\), \(S(5,6,12)\), and re-checks Theorem 3 for all
primes \(p\le61\) and all rungs.  The second builds \(LS(2,3,9)\) and
\(LS(1,2,v)\) explicitly and verifies Lemma 5.1, (6.1) and Theorem 5 parts
1–3.

---

## 9.  Gap audit

**Proved here, unconditionally and solver-free:**

* Theorem 1 (forced intersection distribution of any \(S(t,t+1,v)\)), by two
  independent methods.
* Theorem 2 (forced cross-class distribution), with the completeness
  identity (3.2).
* Theorem 3 and Corollary 3.1 (rung-uniform integrality, nonnegativity, and
  no-slack; after imposing the Steiner design equations, the one-base-block
  Delsarte moment system has a unique feasible point at every rung for every
  prime).
* Corollary 4 and 4.1 (\(D_t\) formula; complement-closure exactly at the top
  rung; intersecting-family exactly at rung \(p-3\); no downward propagation).
* Theorem 5 and Corollaries 5.2, 5.3 (tail dichotomy; the parity test through
  the folded conflict graph is vacuous for every admissible \(k\)).
* Theorem 6 and Corollary 6.1 (local Latin-rectangle characterisation;
  saturation to a Latin square exactly at the top rung).

**Not proved here:**

* Existence or nonexistence of \(LS(3,4,20)\), \(LS(4,5,21)\), or any rung of
  the \(k=16\) tower.
* Any bound of the form \(\tau(p)<p-2\), where
  \(\tau(p):=\max\{t:LS(t,t+1,t+p)\ \text{exists}\}\).
* Any statement about \(k\ge16\) beyond what the tower and the divisibility
  theorem already give.
* Whether the conflict graph \(G_{\mathcal E}\) of Theorem 5 can be shown
  non-bipartite for the tower parameters.  Corollary 5.3 shows the one global
  parity invariant available (regular-bipartite ⟹ even order) is vacuous;
  nothing here rules out a finer odd-cycle argument.

**Provenance of every number used above.**  \(C_4=14\), \(C_6=132\),
\(C_{16}=\binom{32}{16}/17=601080390/17=35357670\); \(\binom93=84\),
\(\binom82=28\), \(\binom71=7\); \(\binom65=6\), \(\binom66=1\);
\((N_0,\dots,N_3)=(1,0,12,0)\) and \((1,0,45,40,45,0)\) are quoted from
`../../opus5_v2/PROOF.md:142-148`.  All other arithmetic is displayed in the
text.  **No number in this note was taken from a program run or from a web
search.**
