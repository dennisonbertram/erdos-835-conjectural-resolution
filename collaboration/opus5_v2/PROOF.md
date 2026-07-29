# Complete arguments (Opus 5, v2)

Everything in this file is a complete proof.  Nothing here was produced or
checked by a computer in this session: code execution was unavailable
(see `STATUS.md`).  Every finite number quoted below was computed by hand and
is re-derivable from the displayed formulas; independent validators are
provided in this directory but **were not run**.

> **Prior-art warning.**  §§1–3 below were written before I checked
> `collaboration/opus5/`.  They turn out to re-derive results already proved
> there in an earlier session: the closed forms of Theorems 1.3 and 3.1, and
> Corollaries 1.4 and 2.1, appear as its `n_{k-u}`, `m_u`, Corollary 6.1 and
> Corollary 6.2; and its Theorem 7a is strictly stronger than my Theorem 3.2.
> Keep §§1–3 only as an independent second proof by a different route (one
> generating-function identity, Lemma 1.2, instead of Fourier support).
> Theorem 2.3, §4 and §5 are the parts I did not find there.  See `STATUS.md`.

Throughout:

* \(k\ge 2\), \(p:=k+1\), point set \([2k]=\{1,\dots,2k\}\).
* \(J(2k,k)\) is the Johnson graph on \(\binom{[2k]}{k}\), adjacency
  \(|A\cap B|=k-1\).
* A *tight colouring* is a proper colouring \(c:\binom{[2k]}{k}\to\mathbb Z_p\).
  Equivalently (standard, and re-proved in §0) the colour classes are \(p\)
  pairwise block-disjoint Steiner systems \(S(k-1,k,2k)\), i.e. an
  \(LS(k-1,k,2k)\).
* For a Steiner system \(\mathcal D=S(k-1,k,2k)\) and \(0\le i\le k-1\),
  \(\lambda_i(\mathcal D)\) is the number of blocks containing a fixed
  \(i\)-set.

---

## 0. The star form and the class form

**Lemma 0.1.**  A map \(c:\binom{[2k]}{k}\to\mathbb Z_p\) is a proper
colouring of \(J(2k,k)\) if and only if for every \((k-1)\)-set \(B\) the
restriction of \(c\) to the *star*
\(B^{\uparrow}=\{B\cup\{x\}:x\in[2k]\setminus B\}\) is a bijection onto
\(\mathbb Z_p\).

*Proof.*  \(|[2k]\setminus B|=2k-(k-1)=k+1=p\), and two \(k\)-sets are
adjacent iff their intersection is a \((k-1)\)-set, i.e. iff they lie in a
common star.  A star is therefore a \(p\)-clique, so properness forces
injectivity on it, and injectivity of a map from a \(p\)-set to a \(p\)-set is
bijectivity.  Conversely bijectivity on every star kills every edge. \(\square\)

**Lemma 0.2.**  Under Lemma 0.1 each colour class is an \(S(k-1,k,2k)\), and
the classes are pairwise block-disjoint; conversely \(p\) pairwise disjoint
\(S(k-1,k,2k)\) systems necessarily partition \(\binom{[2k]}{k}\) and give a
tight colouring.

*Proof.*  "Every \((k-1)\)-set lies in exactly one block of colour \(a\)" is
precisely bijectivity of \(c\) on stars, read colour by colour.  The block
count of an \(S(k-1,k,2k)\) is \(\binom{2k}{k-1}/\binom{k}{k-1}
=\binom{2k}{k}/(k+1)\), so \(p\) disjoint systems already occupy all
\(\binom{2k}{k}\) sets. \(\square\)

**Lemma 0.3 (dual star form).**  If \(c\) is a tight colouring then for every
\((k+1)\)-set \(C\) the \(p\) sets \(C\setminus\{x\}\), \(x\in C\), receive
all \(p\) colours.

*Proof.*  Any two of them meet in \(k-1\) points, so they form a
\(p\)-clique. \(\square\)

Write \(\phi_B:[2k]\setminus B\to\mathbb Z_p,\ x\mapsto c(B\cup\{x\})\) for the
star bijection, and \(\psi_C:C\to\mathbb Z_p,\ x\mapsto c(C\setminus\{x\})\)
for the dual one.

---

## 1. The block-intersection distribution of an \(S(k-1,k,2k)\)

This section is self-contained and uses **one** Steiner system; no large set
is assumed.

**Lemma 1.1.**  \(\displaystyle\lambda_i=\frac{1}{k+1}\binom{2k-i}{k-i}\)
for \(0\le i\le k-1\).

*Proof.*  \(\lambda_i=\binom{2k-i}{(k-1)-i}\big/\binom{k-i}{(k-1)-i}
=\binom{2k-i}{k-1-i}/(k-i)\).  From
\(\binom{2k-i}{k-i}=\binom{2k-i}{k-1-i}\cdot\frac{(2k-i)-(k-1-i)}{k-i}
=\binom{2k-i}{k-1-i}\cdot\frac{k+1}{k-i}\)
the two expressions agree. \(\square\)

In particular \(\lambda_0=\binom{2k}{k}/(k+1)\) (the Catalan number \(C_k\))
and \(\lambda_{k-1}=\binom{k+1}{1}/(k+1)=1\).

**Lemma 1.2 (binomial-transform identity).**  For \(0\le m\le k\),
\[
  \sum_{s=0}^{m}(-1)^s\binom{m}{s}\binom{k+m-s}{\,m-s\,}=\binom{k}{m}.
\]

*Proof.*  \(\binom{k+r}{r}=[x^r](1-x)^{-(k+1)}\).  Hence the sum equals
\([x^m]\bigl((1-x)^m(1-x)^{-(k+1)}\bigr)=[x^m](1-x)^{-(k+1-m)}
=\binom{(k-m)+m}{m}=\binom{k}{m}\), the last step using \(k+1-m\ge 1\).
\(\square\)

**Theorem 1.3 (closed form).**  Let \(\mathcal D\) be an \(S(k-1,k,2k)\) and
fix a block \(A_0\in\mathcal D\).  For \(0\le j\le k-1\) let \(N_j\) be the
number of blocks \(A\in\mathcal D\), \(A\ne A_0\), with \(|A\cap A_0|=j\).
Then
\[
  \boxed{\;N_j=\frac{\binom{k}{j}\Bigl(\binom{k}{j}+(-1)^{k-j}\,k\Bigr)}{k+1}\;}
  \qquad(0\le j\le k-1).
\]

*Proof.*  Set \(N_k:=0\).  Counting pairs \((I,A)\) with \(I\subseteq A_0\),
\(|I|=i\le k-1\), \(A\in\mathcal D\setminus\{A_0\}\), \(I\subseteq A\), in two
ways gives
\[
  \sum_{j}N_j\binom{j}{i}=\binom{k}{i}\bigl(\lambda_i-1\bigr),
  \qquad 0\le i\le k-1,
\]
and for \(i=k\) both sides are \(0\).  Binomial inversion
(\(N_j=\sum_{i\ge j}(-1)^{i-j}\binom{i}{j}R_i\) with \(R_i\) the right-hand
sides, \(R_k=0\)) gives
\[
  N_j=\underbrace{\sum_{i=j}^{k-1}(-1)^{i-j}\binom{i}{j}\binom{k}{i}\lambda_i}_{S_1}
     -\underbrace{\sum_{i=j}^{k-1}(-1)^{i-j}\binom{i}{j}\binom{k}{i}}_{S_2}.
\]
Use \(\binom{i}{j}\binom{k}{i}=\binom{k}{j}\binom{k-j}{i-j}\).

*Second sum.*  Extended to \(i=k\) the sum is
\(\binom{k}{j}(1-1)^{k-j}=0\) (for \(j\le k-1\)), so
\(S_2=-(-1)^{k-j}\binom{k}{j}\).

*First sum.*  By Lemma 1.1, \(pS_1=\sum_{i=j}^{k-1}(-1)^{i-j}\binom{i}{j}
\binom{k}{i}\binom{2k-i}{k-i}\).  Extended to \(i=k\) and with
\(m:=k-j\), \(s:=i-j\), the full sum is
\(\binom{k}{j}\sum_{s=0}^{m}(-1)^s\binom{m}{s}\binom{k+m-s}{m-s}
=\binom{k}{j}\binom{k}{m}=\binom{k}{j}^2\) by Lemma 1.2.  Its \(i=k\) term is
\((-1)^{k-j}\binom{k}{j}\binom{k}{k}\binom{k}{0}=(-1)^{k-j}\binom{k}{j}\).
Hence \(pS_1=\binom{k}{j}^2-(-1)^{k-j}\binom{k}{j}\).

Therefore
\[
  N_j=\frac{\binom kj^2-(-1)^{k-j}\binom kj}{p}+(-1)^{k-j}\binom kj
     =\frac{\binom kj\bigl[\binom kj+(p-1)(-1)^{k-j}\bigr]}{p},
\]
and \(p-1=k\). \(\square\)

**Checks (hand-computed).**
\(k=4\): \((N_0,N_1,N_2,N_3)=(1,0,12,0)\); total \(13=\lambda_0-1\).  This is
the known intersection pattern of \(S(3,4,8)=\mathrm{AG}(3,2)\) (two distinct
affine planes meet in \(0\) or \(2\) points).
\(k=6\): \((N_0,\dots,N_5)=(1,0,45,40,45,0)\); total \(131=\lambda_0-1=132-1\).
This is the known hexad-intersection pattern of \(S(5,6,12)\) (intersections
\(0,2,3,4\) only).

### 1.1 Consequences

**Corollary 1.4 (parity of \(k\)).**  For odd \(k\ge 3\) no \(S(k-1,k,2k)\)
exists.

*Proof.*  \(N_0=\bigl(1+(-1)^k k\bigr)/(k+1)\).  For odd \(k\) this is
\((1-k)/(k+1)<0\) when \(k\ge 3\), contradicting \(N_0\ge0\). \(\square\)

(For \(k=3\) this is the familiar nonexistence of \(S(2,3,6)\).)

**Corollary 1.5 (integrality sieve).**  A necessary condition for the
existence of an \(S(k-1,k,2k)\) is
\[
  (k+1)\ \Bigm|\ \binom kj\Bigl(\binom kj+(-1)^{k-j}k\Bigr)
  \qquad\text{for all } 0\le j\le k-1 .
\]
If \(k+1\) is prime this holds automatically; the condition is violated for
\(k=8,14,20\).

*Proof.*  Necessity is Theorem 1.3.  If \(p=k+1\) is prime then
\(\binom kj=\binom{p-1}{j}\equiv(-1)^j\pmod p\) and \(k\equiv-1\pmod p\); with
\(k\) even, \((-1)^{k-j}=(-1)^j\), so the bracket is
\(\equiv(-1)^j-(-1)^j=0\pmod p\).
Violations (hand-computed):
\(k=8,\ j=3\): \(\binom83=56\), bracket \(=56-8=48\), \(56\cdot 48=2688\),
and \(2688/9=298.\overline{6}\).
\(k=14,\ j=3\): \(\binom{14}3=364\), bracket \(=364-14=350\),
\(364\cdot350=127400\), and \(127400=15\cdot 8493+5\).
\(k=20,\ j=7\): \(\binom{20}7=77520\), bracket \(=77520-20=77500\),
\(77520\cdot77500=6{,}007{,}800{,}000\), and
\(6{,}007{,}800{,}000=21\cdot 286{,}085{,}714+6\). \(\square\)

This gives an independent second proof of nonexistence in those cases;
it does **not** claim to be equivalent to primality of \(k+1\).

**Corollary 1.6 (symmetry).**  For even \(k\), \(N_j=N_{k-j}\) for
\(0\le j\le k\) (with \(N_k:=1\) counting \(A_0\)).

*Proof.*  \(N_{k-j}=\binom{k}{k-j}\bigl(\binom{k}{k-j}+(-1)^{j}k\bigr)/(k+1)\)
and \(\binom{k}{k-j}=\binom kj\); for even \(k\), \((-1)^{k-j}=(-1)^{j}\).
\(\square\)

---

## 2. Complement-closure of every single system

**Theorem 2.1.**  Let \(k\ge 2\) be even and let \(\mathcal D\) be any
\(S(k-1,k,2k)\).  Then \(\mathcal D\) is closed under complementation:
\(A\in\mathcal D\Rightarrow [2k]\setminus A\in\mathcal D\).

*Proof.*  By Theorem 1.3 with \(j=1\) and \(k\) even,
\[
  N_1=\frac{k\bigl(k+(-1)^{k-1}k\bigr)}{k+1}=\frac{k(k-k)}{k+1}=0 ,
\]
i.e. **no two distinct blocks meet in exactly one point.**

Fix \(A_0\in\mathcal D\) and suppose \(A_0^{c}:=[2k]\setminus A_0\notin
\mathcal D\).  Pick any \(x\in A_0^{c}\).  The \((k-1)\)-set
\(A_0^{c}\setminus\{x\}\) lies in a unique block \(B_x\in\mathcal D\), and
\(B_x=(A_0^{c}\setminus\{x\})\cup\{y\}\) for some
\(y\in A_0\cup\{x\}\), \(y\ne x\); hence \(y\in A_0\).  Then
\(|B_x\cap A_0|=1\), and \(B_x\ne A_0\) because \(B_x\) contains the
\(k-1\ge1\) points of \(A_0^c\setminus\{x\}\).  This contradicts \(N_1=0\).
\(\square\)

**Remark.**  The repository's note proves complement-closure only for the
colour classes of a hypothetical tight colouring, via the polytabloid basis of
\(\ker M\) and the \((-1)^k\) action of complementation.  Theorem 2.1 is
strictly stronger (no large set, no colouring) and elementary.  The result is
consistent with the two known cases: the affine planes of \(\mathrm{AG}(3,2)\)
occur in parallel pairs, and the \(132\) hexads of \(S(5,6,12)\) form \(66\)
complementary pairs.

**Corollary 2.2.**  For even \(k\), fix \(\infty\in[2k]\).  Then
\(\mathcal D\mapsto\{A\setminus\{\infty\}: A\in\mathcal D,\ \infty\in A\}\) is
an injection from \(S(k-1,k,2k)\) systems to \(S(k-2,k-1,2k-1)\) systems, and
it maps block-disjoint systems to block-disjoint systems.

*Proof.*  Let \(T\subseteq[2k]\setminus\{\infty\}\) with \(|T|=k-2\).  The
\((k-1)\)-set \(T\cup\{\infty\}\) lies in a unique block \(A\), which contains
\(\infty\); so \(A\setminus\{\infty\}\) is the unique image block containing
\(T\).  Hence the image is an \(S(k-2,k-1,2k-1)\).  Injectivity: by
Theorem 2.1 the blocks of \(\mathcal D\) are exactly the sets \(A\) and
\(A^{c}\) for \(A\) ranging over the blocks through \(\infty\), so
\(\mathcal D\) is recovered from its image.  Disjointness is preserved
because a shared image block \(A'\) would give the shared block
\(A'\cup\{\infty\}\). \(\square\)

**Theorem 2.3 (no small-support automorphisms).**  Let \(k\ge2\) be even and
\(\mathcal D\) an \(S(k-1,k,2k)\).  Then no transposition is an automorphism of
\(\mathcal D\); equivalently, any \(\pi\in\operatorname{Aut}(\mathcal D)\)
fixing at least \(2k-2\) points is the identity.

*Proof.*  By Theorem 1.3 with \(j=k-1\) and \(k\) even,
\(N_{k-1}=\bigl(k(k-k)\bigr)/(k+1)=0\): **no two distinct blocks meet in
exactly \(k-1\) points.**

Let \(\pi=(u\,v)\).  The number of blocks containing exactly one of \(u,v\) is
\(2(\lambda_1-\lambda_2)\), and by Lemma 1.1
\[
  \frac{\lambda_1}{\lambda_2}
  =\frac{\binom{2k-1}{k-1}}{\binom{2k-2}{k-2}}
  =\frac{2k-1}{k-1}>1 \qquad(k\ge2),
\]
so some block \(A\) has, say, \(u\in A\), \(v\notin A\).  Then
\(\pi A=(A\setminus\{u\})\cup\{v\}\) is a block, \(\pi A\ne A\), and
\(|A\cap\pi A|=k-1\), contradicting \(N_{k-1}=0\).  A permutation fixing at
least \(2k-2\) points is the identity or a transposition. \(\square\)

This is the first step of the necessary condition
\(\operatorname{Aut}(\mathcal D)\le A_{2k}\) discussed in `IDEAS.md` §A.3.  It
is consistent with the known cases: \(\mathrm{AGL}(3,2)\) and \(M_{12}\)
contain no transpositions.

---

## 3. Colour-refined rigidity, and why first-order counting is exactly tight

Assume now a tight colouring exists, with classes
\(\mathcal D_0,\dots,\mathcal D_{p-1}\).

**Theorem 3.1.**  Let \(A\) be a block of colour \(a\) and let \(b\ne a\).
For \(0\le j\le k\) the number \(N^{(b)}_j\) of colour-\(b\) sets meeting
\(A\) in exactly \(j\) points is
\[
  N^{(b)}_j=\frac{\binom kj\Bigl(\binom kj-(-1)^{k-j}\Bigr)}{k+1}.
\]

*Proof.*  Identical to Theorem 1.3 except that \(A\notin\mathcal D_b\), so the
count of pairs \((I,A')\) is \(\binom ki\lambda_i\) with no \(-1\), and
\(N^{(b)}_k=0\) is automatic.  The same two sums give
\(N^{(b)}_j=\bigl(\binom kj^2-(-1)^{k-j}\binom kj\bigr)/p\). \(\square\)

**Consistency (a genuine check, not an assumption).**
\(N_j+\sum_{b\ne a}N^{(b)}_j
 =\frac{\binom kj}{p}\bigl[\binom kj+(-1)^{k-j}k+k\binom kj-k(-1)^{k-j}\bigr]
 =\binom kj^2\), which is exactly the total number of \(k\)-sets meeting
\(A\) in \(j\) points.  Also \(N^{(b)}_0=0\) (no other colour class contains a
set disjoint from \(A\)), which re-derives Theorem 2.1 inside the colouring,
and \(N^{(b)}_{k-1}=k(k+1)/p=k\), which is exactly the statement that the
\(k^2\) Johnson-neighbours of \(A\) split evenly among the \(k\) other
colours.

**Theorem 3.2 (first-order counting cannot beat the clique bound).**
Let \(\mathcal D_1,\dots,\mathcal D_r\) be pairwise block-disjoint
\(S(k-1,k,2k)\) systems, \(k\) even.  For every \(1\le j\le k-1\) the
"\(j\)-shell" count around a fixed block gives exactly \(r\le k+1\), with no
slack.

*Proof.*  Fix \(A\in\mathcal D_1\).  Theorem 1.3 applies to \(\mathcal D_1\)
and Theorem 3.1's computation applies verbatim to each \(\mathcal D_s\),
\(s\ge2\) (it used only that \(\mathcal D_s\) is a Steiner system not
containing \(A\)).  Summing and bounding by the total number \(\binom kj^2\)
of \(k\)-sets meeting \(A\) in \(j\) points:
\[
 \frac{\binom kj\bigl(\binom kj+\sigma k\bigr)}{p}
 +(r-1)\frac{\binom kj\bigl(\binom kj-\sigma\bigr)}{p}\ \le\ \binom kj^2,
 \qquad \sigma:=(-1)^{k-j}=(-1)^j .
\]
Dividing by \(\binom kj/p\) and using \(p=k+1\):
\((r-1)\bigl(\binom kj-\sigma\bigr)\le k\bigl(\binom kj-\sigma\bigr)\).
For \(1\le j\le k-1\) we have \(\binom kj\ge k>1\ge\sigma\), so the factor is
positive and the inequality is exactly \(r\le k+1\). \(\square\)

So every single-block shell count reproduces the clique bound and nothing
better.  Any improvement must use at least two blocks simultaneously.

---

## 4. The global star sign, and a proof that it cannot decide the problem

Fix the natural order on \([2k]\) and on \(\mathbb Z_p=\{0,1,\dots,p-1\}\).
For a \((k-1)\)-set \(B\) let \(\epsilon(B)\in\{\pm1\}\) be the sign of the
bijection \(\phi_B\) read against those two orders, and put
\[
  E(c):=\prod_{B\in\binom{[2k]}{k-1}}\epsilon(B).
\]

**Lemma 4.1.**  For \(\pi\in S_{2k}\) acting by \(c\mapsto c\circ\pi^{-1}\),
\[
  E(c\circ\pi^{-1})=E(c)\cdot\prod_{C\in\binom{[2k]}{k+1}}\operatorname{sgn}(\pi|_C),
\]
where \(\operatorname{sgn}(\pi|_C)\) is the sign of the order-index permutation
of the bijection \(C\to\pi(C)\).

*Proof.*  With \(B'=\pi B\) we have \(\phi'_{B'}=\phi_B\circ\pi^{-1}\), hence
\(\epsilon'(\pi B)=\epsilon(B)\operatorname{sgn}(\pi^{-1}|_{\overline{\pi B}})
=\epsilon(B)\operatorname{sgn}(\pi|_{\bar B})\).  Take the product over all
\(B\) and substitute \(C=\bar B\). \(\square\)

**Theorem 4.2.**  For even \(k\), \(E(c)\) is invariant under all point
permutations and all colour permutations.

*Proof.*  *Points.*  It suffices to treat \(\pi=(i,i+1)\).  Then
\(\operatorname{sgn}(\pi|_C)=-1\) exactly when \(\{i,i+1\}\subseteq C\), and
\(+1\) otherwise (if \(C\) contains exactly one of \(i,i+1\), the induced map
\(C\to\pi(C)\) is order-preserving).  Hence the correction factor is
\((-1)^{\binom{2k-2}{k-1}}\), and \(\binom{2m}{m}=2\binom{2m-1}{m-1}\) is even,
so it equals \(+1\).
*Colours.*  Replacing \(c\) by \(\tau\circ c\) multiplies each
\(\epsilon(B)\) by \(\operatorname{sgn}\tau\), hence \(E\) by
\(\operatorname{sgn}(\tau)^{\binom{2k}{k-1}}\).  For even \(k\) both \(k-1\)
and \(k+1\) are odd, so their binary expansions both have a \(1\) in the
units place; adding them carries, so by Kummer's theorem
\(\binom{2k}{k-1}\) is even and the factor is \(+1\). \(\square\)

**Theorem 4.3 (failure boundary: the star sign has no dual partner).**
Define the dual sign \(E^{*}(c):=\prod_{C\in\binom{[2k]}{k+1}}
\operatorname{sgn}(\psi_C)\) using Lemma 0.3.  Then for every tight colouring
with \(k\) even,
\[
  E^{*}(c)=E(c)\quad\text{identically.}
\]
Consequently no contradiction can be extracted by evaluating the global star
sign in the "up" and "down" directions and comparing.

*Proof.*  Let \(B\) be a \((k-1)\)-set and \(C=\bar B\), a \((k+1)\)-set.
For \(x\in C\), \(C\setminus\{x\}=\overline{B\cup\{x\}}\).  By Theorem 2.1
every colour class is complement-closed, i.e. \(c(A)=c(A^{c})\) for all \(A\);
hence
\(\psi_{C}(x)=c(C\setminus\{x\})=c(B\cup\{x\})=\phi_B(x)\).
The two bijections have the same domain \(C=\bar B\), the same codomain and
the same reference orders, so \(\operatorname{sgn}\psi_C=\epsilon(B)\).  Taking
the product over the bijection \(B\leftrightarrow\bar B\) gives
\(E^{*}=E\). \(\square\)

This closes, with a proof rather than a search, the "compare the two natural
scalar signs" route: the two functionals are *literally the same function*.

---

## 5. A uniform no-go for all additive colourings

**Theorem 5.1.**  Let \((G,+)\) be any abelian group, \(f:[2k]\to G\), and
suppose \(c(A)=\sum_{a\in A}f(a)\) for all \(A\in\binom{[2k]}{k}\).  If \(c\)
is a proper colouring of \(J(2k,k)\) with any set of \(p=k+1\) colours, then
\(k\le 1\).

*Proof.*  For a \((k-1)\)-set \(B\) put \(\sigma(B)=\sum_{b\in B}f(b)\).  Then
\(c(B\cup\{x\})=\sigma(B)+f(x)\), so by Lemma 0.1 the map \(x\mapsto f(x)\)
must be injective on \([2k]\setminus B\).  As \(B\) ranges over all
\((k-1)\)-sets, \([2k]\setminus B\) ranges over all \((k+1)\)-subsets of
\([2k]\).  Since \(k+1\ge2\), any two points of \([2k]\) lie in a common
\((k+1)\)-set, so \(f\) is injective on \([2k]\); its image has \(2k\) elements
and lies in the \(p=k+1\) colours, forcing \(2k\le k+1\). \(\square\)

The statement is uniform in \(k\), independent of the field or group, and
needs no divisibility hypothesis.  It contains, as special cases, the
"additive syndrome'' exclusions recorded elsewhere in the repository, and it
shows that any construction must be genuinely non-additive in the point
labels.

---

## 6. What all of the above does **not** prove

Sections 1–5 are unconditional theorems.  None of them excludes any \(k\)
with \(k\) even and \(k+1\) prime.  Specifically:

* Corollary 1.5 is satisfied automatically whenever \(k+1\) is prime, so it
  cannot reach \(k=16\) or \(k=18\).
* Theorem 3.2 proves that the first-order shell counts are *exactly* tight,
  i.e. it is a proof that a whole family of counting attacks cannot work.
* Theorem 4.3 proves that the global scalar star sign cannot yield a
  contradiction.
* Theorem 5.1 excludes a construction family, not arbitrary colourings.

The exact remaining gap is stated in `STATUS.md`.
