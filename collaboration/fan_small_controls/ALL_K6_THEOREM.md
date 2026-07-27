# The universal simultaneous-fan obstruction at \(k=6\)

## Theorem

> **Theorem.** No labelled \(LS(2,3,9)\) admits a simultaneous \(3\)-fan of
> \(LS(3,4,10)\)'s. Consequently the \(378\)-cell fixed-link conflict graph
> is not \(3\)-colourable for every \(LS(2,3,9)\), and
> \[
> \chi(J(12,6))\ge 8.
> \]

This is a complete small-parameter theorem, not a solution of
Erdős--Rosenfeld Problem #835. The first unresolved parameter of that problem
is \(k=16\), where the analogous link is \(LS(2,3,19)\) and the unresolved
target is a simultaneous \(13\)-fan.

No novelty or literature-priority claim is made for the \(k=6\) chromatic
bound. The point of this proof is that it isolates a very small obstruction
inside the new simultaneous-fan formulation.

## 1. Why a \(7\)-colouring would give a fan

Let \(V=U\mathbin{\dot\cup}A\), with \(|U|=9\) and \(|A|=3\). Suppose
\(J(12,6)\) had a proper colouring \(c\) with seven colours. For
\(T\in\binom U3\), \(a\in A\), and
\(Q\in\binom{U\cup\{a\}}4\), define
\[
L(T)=c(U\setminus T),\qquad
F_a(Q)=c((U\cup\{a\})\setminus Q).
\]
The seven triples through a fixed pair, after complementation in \(U\), form
a \(K_7\). Hence \(L\) is an \(LS(2,3,9)\). Similarly, each \(F_a\) is an
\(LS(3,4,10)\), and
\[
F_a(\{a\}\cup T)=L(T).
\]

For each \(Q\in\binom U4\), the seven extensions of the three-set
\(U\setminus Q\) form another \(K_7\). Four have colours
\[
\{L(Q\setminus\{x\}):x\in Q\},
\]
and the other three have colours \(\{F_a(Q):a\in A\}\). Thus the latter
three colours are distinct and are exactly the complement of the former
four. This is the simultaneous \(3\)-fan condition.

It remains to prove that no possible link \(L\) supports such a fan.

## 2. Exhausting the possible links

There are exactly two point-isomorphism types of \(LS(2,3,9)\). This classical
classification is also independently reproduced by the standard-library
verifier:

1. enumerate every exact triangle decomposition of \(K_9\), obtaining all
   \(840\) labelled \(STS(9)\)'s;
2. enumerate exact covers of the \(84\) triples by seven disjoint systems,
   obtaining \(15,360\) large sets on the fixed labelled point set (with
   their seven systems unordered);
3. compute the automorphism orders of the two displayed representatives as
   \(42\) and \(54\);
4. orbit--stabilizer gives two distinct orbits of sizes
   \[
   \frac{9!}{42}=8,640,\qquad
   \frac{9!}{54}=6,720;
   \]
5. their sum is \(15,360\), so the two orbits exhaust every large set.

The representatives are the type A and type B array constructions in
[Bryant, Grannell, and Griggs (2003)](https://grannell.net/Papers/lsls9.pdf).
In a \(3\times3\) array, the rows, columns, and the two sets of cyclic
diagonals are the twelve blocks of an \(STS(9)\).

- Type A starts from
  \[
  \begin{matrix}
  7&8&0\\
  1&2&4\\
  5&6&3
  \end{matrix}
  \]
  and applies all seven shifts \(i\mapsto i+1\pmod7\), fixing \(7,8\).
- Type B consists of the array
  \[
  \begin{matrix}
  6&7&8\\
  0&2&4\\
  3&1&5
  \end{matrix}
  \]
  together with the six images of
  \[
  \begin{matrix}
  6&0&1\\
  7&2&5\\
  3&8&4
  \end{matrix}
  \]
  under \((7\ 8)(0\ 1\ 2\ 3\ 4\ 5)\), fixing \(6\).

Permuting points or the seven link colours preserves fan existence.
Therefore it is enough to exclude these two representatives.

## 3. Conflict cells and constraint cliques

For a fixed link \(L\), a cell is an allowed pair
\[
(Q,c),\qquad Q\in\binom U4,\quad
c\notin\{L(T):T\in\binom Q3\}.
\]
A fan would assign one of three extension labels to every cell. Each of the
following sets of three cells must be rainbow:

- the three allowed cells with a fixed quadruple \(Q\);
- the three allowed cells with a fixed pair \((T,c)\), where
  \(T\in\binom U3\) and \(c\ne L(T)\).

Thus every displayed three-cell set below is a \(K_3\) in the conflict graph.

## 4. Type A: an 18-cell obstruction

Use these cell names:

| cell | \((Q;c)\) | cell | \((Q;c)\) |
|---|---|---|---|
| \(A\) | \((0278;4)\) | \(J\) | \((0268;1)\) |
| \(B\) | \((0278;1)\) | \(K\) | \((0258;1)\) |
| \(C\) | \((0278;5)\) | \(L\) | \((0258;5)\) |
| \(D\) | \((0247;4)\) | \(M\) | \((0258;2)\) |
| \(E\) | \((0127;4)\) | \(N\) | \((0236;1)\) |
| \(F\) | \((0257;5)\) | \(O\) | \((0245;4)\) |
| \(G\) | \((0248;4)\) | \(P\) | \((0245;1)\) |
| \(H\) | \((0128;5)\) | \(Q\) | \((0245;5)\) |
| \(I\) | \((0268;4)\) | \(R\) | \((0256;1)\) |

The following eleven triples are genuine constraint cliques:
\[
\begin{gathered}
ABC,\ KLM,\ OPQ,\ ADE,\ AGI,\ BJK,\\
CHL,\ DGO,\ JNR,\ KPR,\ FLQ.
\end{gathered} \tag{A}
\]

Assume a proper \(3\)-colouring and normalize
\[
A=0,\qquad B=1,\qquad C=2.
\]
From \(ADE\) and \(AGI\),
\[
\{D,E\}=\{1,2\},\qquad \{G,I\}=\{1,2\}.
\]
The clique \(DGO\) forces \(D\ne G\), hence \(O=0\). From \(OPQ\),
\[
\{P,Q\}=\{1,2\}.
\]
The cliques \(BJK\) and \(CHL\) give
\[
\{J,K\}=\{0,2\},\qquad \{H,L\}=\{0,1\}.
\]

There are two cases.

- If \(K=0\), then \(J=2\). The clique \(KLM\) forces \(K\ne L\), so
  \(L=1\); then \(FLQ\) forces \(L\ne Q\), so \(Q=2,P=1\). The clique
  \(KPR\) gives \(R=2=J\), contradicting \(JNR\).
- If \(K=2\), then \(J=0\). The clique \(KPR\) forces \(P=1,Q=2,R=0=J\),
  again contradicting \(JNR\).

So the type A conflict graph is not \(3\)-colourable.

## 5. Type B: another 18-cell obstruction

Use these cells:

| cell | \((Q;c)\) | cell | \((Q;c)\) |
|---|---|---|---|
| \(A\) | \((0123;0)\) | \(J\) | \((0237;1)\) |
| \(B\) | \((0134;0)\) | \(K\) | \((0347;4)\) |
| \(C\) | \((0134;1)\) | \(L\) | \((0348;4)\) |
| \(D\) | \((0134;4)\) | \(M\) | \((0358;4)\) |
| \(E\) | \((0137;0)\) | \(N\) | \((0367;4)\) |
| \(F\) | \((0137;1)\) | \(O\) | \((0368;1)\) |
| \(G\) | \((0138;1)\) | \(P\) | \((0378;0)\) |
| \(H\) | \((0235;0)\) | \(Q\) | \((0378;1)\) |
| \(I\) | \((0237;0)\) | \(R\) | \((0378;4)\) |

The eleven constraint cliques are
\[
\begin{gathered}
BCD,\ PQR,\ ABE,\ CFG,\ AHI,\ DKL,\\
EIP,\ FJQ,\ KNR,\ GOQ,\ LMR.
\end{gathered} \tag{B}
\]

Normalize \(B=0,C=1,D=2\). The cliques \(ABE,CFG,DKL\) give
\[
\{A,E\}=\{1,2\},\qquad
\{F,G\}=\{0,2\},\qquad
\{K,L\}=\{0,1\}.
\]

Because \(I\) differs from \(A\) in \(AHI\) and from \(E\) in \(EIP\), it
differs from both \(1\) and \(2\); hence \(I=0\), and then \(EIP\) gives
\(P=A\). Similarly, \(Q\) differs from both \(F\) and \(G\) in \(FJQ\) and
\(GOQ\), so \(Q=1\). Finally, \(R\) differs from both \(K\) and \(L\) in
\(KNR\) and \(LMR\), so \(R=2\).

But \(P=A\in\{1,2\}\), while \(Q=1\) and \(R=2\). Therefore \(PQR\) cannot
be rainbow, a contradiction.

So the type B conflict graph is also not \(3\)-colourable.

## 6. Conclusion

Every \(LS(2,3,9)\) is isomorphic to type A or type B, and both conflict
graphs contain an explicit non-\(3\)-colourable 18-vertex subgraph.
Therefore no common link supports a simultaneous \(3\)-fan. Section 1 now
implies that \(J(12,6)\) has no proper \(7\)-colouring. \(\square\)

## 7. Verification

Run the complete standard-library check:

```sh
python3 -B collaboration/fan_small_controls/verify_all_k6_links.py
```

It verifies the full classification census, both representatives, all
thirty-six listed cells, all twenty-two constraint cliques, and exact
non-\(3\)-colourability of both 18-vertex graphs.

The separate DRAT certificate in this directory is an independent,
solver-generated cross-check for one deterministic link. It is no longer
needed for the universal proof.
