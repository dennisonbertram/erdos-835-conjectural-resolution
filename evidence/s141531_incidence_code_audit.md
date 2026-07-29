# The forced point-incidence code of a hypothetical \(S(14,15,31)\)

Status: **exact necessary conditions and closed code-bound tests; not a
nonexistence proof and not a solution of Problem #835.**

This note records a binary-code consequence of one colour class in a
hypothetical tight colouring.  The complete weight enumerator of its
point-incidence code is forced.  Its first 250 MacWilliams coefficients
are nonnegative integers, and the ordinary Griesmer bound remains feasible
both before and after three natural simplex shortenings.  Thus this exact
code layer supplies useful parameters but no contradiction.

The independent executable audit is
`explore_s141531_incidence_code.py`.

## 1. Fourier values forced by the Steiner property

Let \({\cal A}\) be a hypothetical \(S(14,15,31)\) on a point set \(X\).
Its number of blocks is
\[
 b=\frac{\binom{31}{14}}{15}=17\,678\,835,
\]
and its derived parameters are
\[
 \lambda_j
 =\frac{\binom{31-j}{14-j}}{15-j}
 \quad(0\leq j\leq14).
                                                        \tag{1}
\]
Explicitly,
\[
\begin{split}
(\lambda_0,\ldots,\lambda_{14})={}&
(17678835,8554275,3991995,1789515,766935,\\
&312455,120175,43263,14421,4389,1197,285,57,9,1).
\end{split}                                             \tag{2}
\]

For \(S\subseteq X\), define
\[
 F(S)=\sum_{B\in{\cal A}}(-1)^{|B\cap S|}.
                                                        \tag{3}
\]
If \(s=|S|\leq14\), inclusion--exclusion gives
\[
 F_s=\sum_{j=0}^s(-2)^j\binom{s}{j}\lambda_j.           \tag{4}
\]
If \(s=15\), the same expression through \(j=14\) is the
**external** value; it receives the additional term
\((-2)^{15}\) exactly when \(S\in{\cal A}\).  Since every block has odd
size,
\[
 F(X\setminus S)=-F(S).                                \tag{5}
\]
Equations (4)--(5) determine every Fourier value, with only the stated
internal/external split in the middle two layers.

## 2. The complete forced weight enumerator

Let \(P\) be the \(31\)-by-\(b\) point--block incidence matrix over
\(\mathbb F_2\), and let \(C\) be its row space.  The full-rank theorem in
`mersenne_spin_functional_audit.md` proves
\[
 \dim C=31.                                             \tag{6}
\]
For the codeword
\[
 c_S=\sum_{x\in S}P_x,
\]
the coordinate at \(B\) is \(|B\cap S|\bmod2\), so
\[
 \operatorname{wt}(c_S)=\frac{b-F(S)}2.                \tag{7}
\]
Full rank makes \(S\mapsto c_S\) injective.  Equations (4)--(7), together
with the fact that exactly \(b\) of the \(15\)-sets are blocks, therefore
force the entire weight enumerator of the binary \([b,31]\) code \(C\).
It has only twenty distinct weights.

The checker applies the exact Krawtchouk recurrence to this enumerator.
The first coefficients of the dual enumerator are
\[
\begin{array}{c|rrrrrrrr}
j&0&1&2&3&4&5&6&7\\ \hline
A_j^\perp&
1&0&0&0&
3\,793\,226\,637\,448\,341\,180&
0&
39\,490\,202\,682\,224\,904\,419\,269\,612\,470\,360&
0 .
\end{array}                                             \tag{8}
\]
All coefficients through degree \(250\) are exact nonnegative integers.
This is only a passed necessary test: MacWilliams positivity does not
construct \({\cal A}\).

## 3. The even point subcode

Let
\[
 C_0=\{c_S:|S|\ \hbox{is even}\}.
\]
By (6), \(\dim C_0=30\).  Its possible nonzero weights are obtained from
the even subset sizes \(2,4,\ldots,30\), with separate internal and
external values at size \(16\).  Their minimum is
\[
 d(C_0)=8\,809\,920,                                   \tag{9}
\]
attained by every \(4\)-set and its \(28\)-set complement.  Hence
\[
 C_0\text{ has parameters }
 [17\,678\,835,30,8\,809\,920].                        \tag{10}
\]
Every weight is divisible by \(16\), and \(C_0\) is self-orthogonal
because \(PP^{\mathsf T}=J_{31}\) and its indexing subsets have even
size.

The binary Griesmer sum is
\[
 g_2(30,8\,809\,920)=17\,619\,853,
\]
leaving slack
\[
 17\,678\,835-17\,619\,853=58\,982.                    \tag{11}
\]
Thus the initial Griesmer test does not contradict (10).

## 4. Exact punctured quotients

There is a useful family of stronger tests.  Let \(H\) be an
\(m\)-dimensional subspace of the even subsets of \(X\), viewed inside
\(C_0\), and retain only the coordinates
\[
 Z_H=\{B\in{\cal A}:|B\cap h|\equiv0\pmod2
                     \text{ for every }h\in H\}.        \tag{12}
\]
Every word of \(H\) vanishes on \(Z_H\).  Character orthogonality gives
the exact length
\[
 n_H=|Z_H|=\frac1{|H|}\sum_{h\in H}F(h),               \tag{13}
\]
and, for \(c\in C_0\),
\[
 \operatorname{wt}_{Z_H}(c)
 =\frac{\sum_{h\in H}F(h)-\sum_{h\in H}F(c+h)}
        {2|H|}.                                        \tag{14}
\]

Take \(H\) to be the binary simplex code of dimension \(m\), supported
on \(2^m-1\) points.  Every nonzero word of \(H\) has even size
\(2^{m-1}\), so (13) is completely forced for \(m=2,3,4\).

There is one subtle middle-layer issue in (14).  All \(c+h\) are even,
so size \(15\) never occurs.  At size \(16\), however, the Fourier value
is larger by \(2^{15}\) when the complementary \(15\)-set is a block;
this **lowers** the punctured weight.  The checker obtains a rigorous
lower bound by treating every size-\(16\) translate as internal, and an
upper bound by treating every one as external.  A positive lower bound
for every \(c\notin H\) also proves that the kernel of the restriction is
exactly \(H\), so the quotient dimension is \(30-m\).

The exhaustive results are
\[
\begin{array}{c|r|r|r|r|r}
m&n_H&\dim&d_{\rm lower}&d_{\rm upper}
&n_H-g_2(\dim,d_{\rm lower})\\ \hline
2&3\,991\,995&28&1\,975\,240&1\,975\,240&41\,501\\
3&2\,261\,475&27&1\,104\,736&1\,104\,736&51\,991\\
4&1\,107\,795&26&539\,168&547\,200&29\,445
\end{array}                                             \tag{15}
\]
For \(m=2,3\), a minimizing coset contains no uncertain size-\(16\)
translate, so the displayed bounds coincide and the distances are exact.
For \(m=4\), the actual distance lies in the displayed interval.

Even the optimistic upper endpoint at \(m=4\) has
\[
 g_2(26,547\,200)=1\,094\,412<1\,107\,795.             \tag{16}
\]
Consequently no resolution of the middle-layer uncertainty can turn
this particular Griesmer test into a contradiction.

## 5. The endpoint-only strategy closes globally

The companion C++ program
`search_s141531_shortening_subcodes.cpp` deterministically samples other
even subspaces supported on fifteen points and applies the same safe
Fourier envelope.  Its random output is exploratory, not an exhaustive
certificate; a negative slack would require a separate exact verifier.
No sampled positive-rank quotient has crossed the Griesmer bound.

The subsequent theorem in
`s141531_griesmer_averaging_no_go.md` supersedes that sampling.  It takes
the exact Fourier transform of the upper radial endpoint on the full
30-dimensional even-subset group.  If \(H\) is any proper subspace, its
annihilator forces an outside \(H\)-coset whose upper Fourier sum is too
large for the endpoint-derived distance to beat Griesmer.  Quantitatively,
the principal transform is
\[
 T=9\,268\,801\,044\,480,
\]
the largest nonprincipal transform is
\[
 R=30\,930\,370\,560,
\]
and the forced outside-coset average per word of \(H\) is at least
\[
 \frac{T-R}{2^{30}}=\frac{137\,655}{16}.
\]
This proves, in every subspace dimension, that **independently**
maximizing the unresolved size-\(16\) Fourier values and applying
Griesmer to the common-zero quotient can never yield a contradiction.

The exact dimension-two classification in
`s141531_dim2_subcode_audit.md` supplies a separate finite check:
all \(1{,}450\) labelled column profiles and \(1{,}567{,}276\) subset
profiles pass the same necessary bound.

## 6. Scope and next boundary

What is proved here is the forced code enumerator, the parameters
(10), and the exact simplex tests (15).  These are necessary consequences
of one \(S(14,15,31)\), not a construction and not a nonexistence theorem.
A stronger code attack must use a bound beyond Griesmer, or couple the
middle-layer block indicators rather than treating their endpoints
independently.
