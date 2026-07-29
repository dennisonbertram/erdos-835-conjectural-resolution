# The exact autocorrelation law of a hypothetical S(14,15,31), and why it carries no new leverage

Date: 2026-07-26.  Verifier: `verify_s141531_autocorrelation_law.py`.
Status: **the law is TRUE and exact — confirmed three independent ways — but it
is equivalent to the already-forced Fourier data, so it yields no new
obstruction.**  Not a nonexistence proof and not a solution of Problem #835.

## 1. The law (PROVED)

For \(D\subseteq X=[31]\) let \(m_D\) be the number of unordered pairs of
distinct blocks \(\{B,C\}\) with \(B\triangle C=D\).  Then in any hypothetical
\(S(14,15,31)\):

| \(|D|\) | 30 | 28 | 26 | 24 | 22 | 20 | 18 | 16 | 14 | 12 | 10 | 8 | 6 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| \(m_D\) | 0 | 235980 | 174800 | 165186 | 153216 | 147972 | 144144 | * | 144144 | 147972 | 153216 | 165186 | 174800 | 235980 |

\(m_D=0\) for every odd \(|D|\) and for \(|D|\in\{0,2\}\); and at \(|D|=16\),

\[
 m_D=\begin{cases}157\,425,&D^c\ \text{is a block},\\[2pt]
                  142\,590,&\text{otherwise.}\end{cases}
\]

The table is symmetric under \(|D|\mapsto32-|D|\).

## 2. Three independent confirmations

**(a) Convexity against the forced \(A_4\).**  A weight-4 word of
\(C_0^\perp\) is four blocks with \(B_1\triangle B_2\triangle B_3\triangle
B_4=\varnothing\) (the odd alternative \(d\equiv1\) is impossible: it needs
\(a+3c=60\), \(a+c=31\), so \(2c=29\)).  Two distinct block-pairs with equal
symmetric difference are automatically disjoint, and each weight-4 word splits
into three such pairings, so

\[
 \sum_D\binom{m_D}{2}=3A_4=11\,379\,679\,912\,345\,023\,540 .
\]

Every layer total \(P_s=bN_s/2\) is exactly divisible by \(\binom{31}{30-2s}\),
so the perfectly balanced configuration is feasible; because \(\binom m2\) is
strictly convex it is the **unique** minimiser, and it attains
\(3A_4\) with difference exactly \(0\).  Equality therefore forces the table.
(\(A_4=3\,793\,226\,637\,448\,341\,180\) recomputed here from the fourth power
moment via \(N_4=3n^2-2n+24A_4\).)

**(b) Group-ring consistency.**  Since \((X,\triangle)=\mathbb F_2^{31}\) has
exponent 2, with \(\mathcal A=\sum_{B}x^B\) the law says exactly

\[
 \boxed{\ \mathcal A^2-29\,670\,x^{\mathbf 1}\mathcal A
 \in\operatorname{span}\{W_0,\dots,W_{31}\}\ }
\]

the \(W_j\) being the weight layers, i.e. the Bose–Mesner algebra of the Hamming
scheme \(H(31,2)\); here \(29\,670=2(157425-142590)\).  Applying the character
\(\chi_u\) (\(\chi_u(\mathcal A)=F(u)\), \(\chi_u(x^{\mathbf 1})=(-1)^{|u|}\),
\(\chi_u(W_j)\) a Krawtchouk value) turns this into

\[
 F(u)^2-29\,670\,(-1)^{|u|}F(u)\ \text{depends only on}\ |u|,
\]

which at \(|u|=15\) forces \(F_0+F_1=-29\,670\).  The forced values are
\(F_0=1549\) (non-block) and \(F_1=-31\,219\) (block), and indeed
\(1549-31219=-29\,670\) exactly, both sides giving \(48\,358\,231\).

**(c) Direct inverse transform — the decisive one.**  No \(A_4\) and no
convexity are needed.  Writing \(F(u)^2=\varphi(|u|)^2+c_1\mathbf 1_{\cal
A}(u)\) at \(|u|=15\) and \(+c_1\mathbf 1_{\cal A}(u+\mathbf 1)\) at
\(|u|=16\), with

\[
 c_1=F_1^2-F_0^2=(F_1-F_0)(F_1+F_0)=2^{15}\cdot29\,670=2^{16}\cdot14\,835,
\]

one inverse transform gives, for even \(|D|=d\),

\[
 2m_D=\frac1{2^{31}}\Bigl[\sum_j\varphi(j)^2K_j(d)+2c_1F(D)\Bigr].
\]

Since \(c_1/2^{15}=2\cdot14\,835\) and \(F(D)\) at \(|D|=16\) is
\(-F_0+2^{15}[D^c\in{\cal A}]\), the block-dependent part is **exactly**
\(14\,835\,[D^c\in{\cal A}]\), supported on \(|D|=16\) and nowhere else.  The
verifier reproduces all fifteen table entries, both \(|D|=16\) branches
included, from this formula alone.

## 3. Leverage assessment: none, and the reason is structural

Route (c) shows the law is **not independent information**.  It is the inverse
Fourier transform of the forced weight enumerator, so anything derived from it
is derived from data the repo already had.  Equivalently, by (b) it is the
single statement "\(F^2-29670(-1)^{|u|}F\) is a function of \(|u|\)", and that
statement is *automatically true* of the forced \(F\) — the consistency check
passes rather than constraining.

This places the law squarely inside an existing no-go.
`collaboration/fable_parity_attack_2.md` **Theorem 8.1** proves that for every
\(M\) in the Bose–Mesner algebra, \(x_B^{T}Mx_C=\alpha_M+\beta_M|B\cap C|\):
every invariant bilinear quantity merely repackages the one free parameter.
The boxed identity is exactly a Bose–Mesner statement about \(\mathcal A^2\),
so Theorem 8.1 applies and no parameter-only congruence can follow.

Specific routes checked and closed:

- **\(p=2\) rank.**  Degenerate.  \(\mathbb F_2^{31}\) has exponent 2, so by
  Frobenius \(\mathcal A^2=\sum_Bx^{2B}=b\cdot1\) in characteristic 2 — the
  identity reduces to \(b\equiv1\), true since \(b\) is odd.  No content.
- **Other primes.**  \(29\,670=2\cdot3\cdot5\cdot23\cdot43\), so modulo
  \(3,5,23,43\) the \(x^{\mathbf 1}\mathcal A\) term drops and the identity
  becomes a pure Bose–Mesner congruence — again covered by Theorem 8.1.
- **Complete regularity.**  The law says the autocorrelation of \(\mathcal A\)
  lies in the Bose–Mesner algebra modulo the \(\mathbf 1\)-translate, i.e.
  \(\mathcal A\) is a completely-regular-type object in \(H(31,2)\).  That is a
  strong regularity, but it is *forced*, hence cannot be contradicted.

## 4. What it is still good for

The law is a clean, exact, cheaply-checkable necessary condition, and that is
its real use:

- a **falsification test** for any partial or candidate construction — any
  partial block set whose pair-difference multiset deviates from the table on a
  completed layer is not extendable;
- an exact target for search heuristics (the \(|D|=16\) dichotomy
  \(157425/142590\) ties the autocorrelation directly to the block indicator);
- an independent re-derivation of the per-block triangle count \(157\,425\),
  since \(b\cdot157425=3A_3\).

## 5. Scope

Conditional on the existence of an \(S(14,15,31)\) throughout.  The law is
proved; the leverage assessment is a negative result about that law, not about
the design.  It does not construct or exclude \(S(14,15,31)\) and has no bearing
on Problem #835 beyond removing one more candidate route.
