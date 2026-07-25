# Local one-factorization Pfaffian signs: an exact scalar no-go

This note audits the proposed local one-factorization sign obstruction for a
tight colouring at the prime parameter

\[
k=p-1,\qquad |V|=2k=2p-2.
\]

It proves the exact local identities and then shows precisely what their
products do and do not imply. The result is a **no-go for the scalar sign
route**, not a solution of Erdős--Rosenfeld Problem #835.

Throughout, order both \(V\) and the \(p\) colours. Suppose, only for the
purpose of deriving necessary conditions, that

\[
c:\binom V{p-1}\longrightarrow [p]
\tag{0}
\]

is tight: every \((p-2)\)-star sees each colour exactly once. Thus each
colour class \(\mathcal B_a\) is an \(S(p-2,p-1,2p-2)\).

## 1. The local factorization and its flag sign

For \(R\in\binom V{p-3}\), put \(W=V\setminus R\), so
\(|W|=p+1=2m\), where \(m=(p+1)/2\). For a colour \(a\), set

\[
M_{R,a}=\bigl\{\{x,y\}\subset W:c(R\cup\{x,y\})=a\bigr\}.
\]

Every \(M_{R,a}\) is a perfect matching of \(W\), and the \(p\) matchings
form a one-factorization of \(K_W\). Let
\(\varepsilon_{R,a}\in\{\pm1\}\) be the Pfaffian sign of this matching:
orient every edge increasingly, order the edges by their first endpoint,
flatten, and take the permutation sign.

For \(T\in\binom V{p-2}\), define the colour-to-extension bijection

\[
\pi_T:[p]\longrightarrow V\setminus T,
\qquad
\pi_T(a)=y\quad\Longleftrightarrow\quad c(T\cup\{y\})=a,
\]

and write \(\delta_T=\operatorname{sgn}(\pi_T)\).

**Lemma 1 (flag-transposition identity).** For every \(R\),

\[
\boxed{
\prod_{a=1}^{p}\varepsilon_{R,a}
=(-1)^{\binom m2}\prod_{x\in W}\delta_{R\cup\{x\}}.}
\tag{1}
\]

**Proof.** The \(2m(2m-1)\) flags \((x,a)\) can be ordered vertex-major,
which contributes the product of the signs of the maps
\(a\mapsto\pi_{R\cup\{x\}}(a)\), or factor-major, which contributes the
product of the Pfaffian signs of the factors. Transposing the
\(2m\)-by-\((2m-1)\) flag rectangle is even. The remaining change from the
edge-major directed-edge order to the vertex-major directed-edge order has
parity \(\binom m2\). This gives (1). \(\square\)

Multiplication over all \(R\) gives the exact direct global identity

\[
\boxed{
\prod_{R,a}\varepsilon_{R,a}
=(-1)^{\binom{(p+1)/2}{2}\binom{2p-2}{p-3}}
\prod_{T\in\binom V{p-2}}\delta_T.}
\tag{2}
\]

Indeed, each \(T\) occurs for its \(p-2\) choices of \(x\in T\), and
\(p-2\) is odd. Thus the direct product does *not* eliminate the star
signs.

## 2. Pinned descent to Steiner triple systems

For this descent assume \(p\ge5\). Fix \(\infty\in V\), write
\(X=V\setminus\{\infty\}\), and put

\[
r=p-2.
\]

For each colour \(a\), the blocks through \(\infty\), with \(\infty\)
removed, form

\[
\mathcal D_a=S(r-1,r,2r+1)
=S(p-3,p-2,2p-3).
\tag{3}
\]

For \(A\in\binom X{r-2}=\binom X{p-4}\), its \(p\) matching links are the
same \(M_{\{\infty\}\cup A,a}\) as above. In (1), multiply now only over
these \(A\)'s. Each pinned \((p-2)\)-star occurs \(p-3\) times, an even
number. Therefore

\[
\boxed{
\prod_{A,a}\varepsilon_{\{\infty\}\cup A,a}
=(-1)^{\binom{(p+1)/2}{2}\binom{2p-3}{p-4}}.}
\tag{4}
\]

The apparent extra information comes from one more descent. Fix a colour
and \(Q\in\binom X{p-5}\). The derived design
\(\mathcal D_a/Q\) is an \(\operatorname{STS}(p+2)\). For an ordered odd
set \(U\), every \(\operatorname{STS}(U)\) satisfies the universal
Pfaffian identity

\[
\prod_{x\in U}\operatorname{pfsgn}(\text{link matching at }x)
=(-1)^{\binom{|U|}{4}}.
\tag{5}
\]

One proof of (5) adjoins a final point and the edges \(\{x,\alpha\}\),
obtaining a one-factorization of \(K_{|U|+1}\), then applies Lemma 1. The
Steiner-quasigroup rows contribute a total positive star sign; tracking the
inserted edges gives the displayed parity.

Set

\[
G(\mathcal D_a)=
\prod_{A\in\binom X{p-4}}\varepsilon_{\{\infty\}\cup A,a}.
\]

Every \(A\) contains \(p-4\) sets \(Q\), which is odd. Applying (5) and
multiplying over all \(Q\) proves

\[
\boxed{
G(\mathcal D_a)
=(-1)^{\binom{p+2}{4}\binom{2p-3}{p-5}}.}
\tag{6}
\]

Products of (4) and (6), over the \(p\) colours, agree; their common
necessary scalar condition is

\[
(-1)^{p\binom{p+2}{4}\binom{2p-3}{p-5}}
=(-1)^{\binom{(p+1)/2}{2}\binom{2p-3}{p-4}}.
\tag{7}
\]

## 3. Why the scalar route cannot contradict \(p=17\)

At \(p=17\),

\[
\binom92=36\equiv0,
\qquad
\binom{19}{4}=3876\equiv0\pmod2.
\]

The pinned index counts are

\[
\binom{31}{13}=206{,}253{,}075,
\qquad
\binom{31}{12}=141{,}120{,}525,
\]

both odd. Nevertheless (4), (6), and (7) are all \(+1=+1\), so there is
no global Pfaffian/star-product contradiction at \(p=17\).

There is a stronger, precise statement. Encode \(+1\) by \(0\) and
\(-1\) by \(1\), and put

\[
a_p=\binom{(p+1)/2}{2}\bmod2,
\qquad h_p=\binom{p+2}{4}\bmod2.
\]

Lucas' theorem gives

\[
a_p=h_p=
\begin{cases}
1,&p\equiv3,5\pmod8,\\
0,&p\equiv1,7\pmod8.
\end{cases}
\tag{8}
\]

For every odd \(p\), the following is a formal model of all scalar
identities (1) and (5), and hence of every identity obtained merely by
multiplying them:

\[
\varepsilon_{R,a}=a_p\quad\text{for every }(R,a),
\qquad
\delta_T=0\quad\text{for every }T.
\tag{9}
\]

Indeed, (1) asks for \(p a_p=a_p\), while (5) asks for
\((p+2)a_p=h_p\), both modulo \(2\). These hold because \(p\) and \(p+2\)
are odd and (8) holds.

**Theorem (scalar one-factorization-sign no-go).** Multiplication of the
local Pfaffian signs and star-bijection signs, including the universal
Steiner-triple-system descent when it is defined, cannot force a
contradiction for \(p=17\), or for any congruence class of odd primes. More
narrowly: there is no derivation of \(-1=+1\) in the commutative sign
algebra generated by (1) and (5), since (9) satisfies every generator.

The theorem deliberately does not assert that (9) comes from actual
one-factorizations, let alone from a colouring. Pointwise restrictions on
individual local factorization signs are extra information. The controls
below show exactly why that distinction matters.

## 4. Exact controls

- **\(k=2,p=3\), true.** The unique \(K_4\) one-factorization has positive
  product of star signs and negative product of matching Pfaffian signs, as
  Lemma 1 requires. This is the standard three-colouring.
- **\(k=4,p=5\), false.** All six unordered \(K_6\) one-factorizations
  have negative product of their star signs. After pinning a point there
  are seven such links, whose product is therefore negative. But each
  pinned star occurs twice, so global compatibility would make that product
  positive: a genuine local-sign contradiction.
- **\(k=6,p=7\), false control but not detected by this sign.** The 6240
  unordered \(K_8\) one-factorizations split as 5280 with positive and 960
  with negative star-product sign. Thus the rigid \(K_6\) step is absent;
  also both bases in (7) are positive. This scalar test supplies no
  contradiction at \(k=6\).
- **\(k=16,p=17\).** The scalar equations close as described above. Any
  successful continuation must use a pointwise or nonlinear restriction on
  compatible \(K_{18}\) factorizations, or information beyond these signs.

## 5. Exact verifier

```bash
python3 evidence/local_one_factorization_sign_verify.py
```

The verifier exhaustively enumerates the unordered \(K_4\), \(K_6\), and
\(K_8\) one-factorizations and checks every claimed finite count and sign.
It proves neither a tight colouring nor its nonexistence at \(p=17\).
