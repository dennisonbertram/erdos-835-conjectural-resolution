# S(7,8,24): exact audit of the classical necessary conditions

Date: 2026-07-26.  Verifier: `verify_s7824_conditions.py` (stdlib, exact
Fractions).  Status: **no nonexistence proof found.  Every classical condition
passes.**  This note records exactly which tests were run, what they give, and
why the method that worked one level up does not transfer.

## 0. Why the target matters, and how strong it is

A hypothetical \(S(14,15,31)\) derived at a \(7\)-set is an \(S(7,8,24)\), so
nonexistence of \(S(7,8,24)\) kills \(k=16\).  But deriving \(S(7,8,24)\) at a
\(3\)-set gives \(S(4,5,21)\), so

\[
 \text{no }S(4,5,21)\ \Longrightarrow\ \text{no }S(7,8,24)
 \ \Longrightarrow\ \text{no }S(14,15,31).
\]

**Nonexistence of \(S(7,8,24)\) is therefore a strictly weaker statement than
nonexistence of \(S(4,5,21)\)**, the famous open case.  It is a legitimate target
only if the extra structure at \(t=7\) provides leverage that \(t=4\) lacks.
§3 argues that the most promising such leverage is exactly what fails.

## 1. Parameters (COMPUTED, exact)

\(b=\binom{24}{7}/8=43\,263\), and

\[
 (\lambda_0,\dots,\lambda_7)=
 (43263,\,14421,\,4389,\,1197,\,285,\,57,\,9,\,1),
\]

all integral, so the divisibility conditions hold.  Factorisations:
\(43263=3^2\cdot11\cdot19\cdot23\), \(14421=3\cdot11\cdot19\cdot23\),
\(4389=3\cdot7\cdot11\cdot19\), \(1197=3^2\cdot7\cdot19\), \(285=3\cdot5\cdot19\),
\(57=3\cdot19\), \(9=3^2\).  No prime obstruction is visible.

## 2. Every classical test passes

For \(k=t+1\) the intersection distribution of a fixed \(k\)-set is determined by
\(\sum_j\binom js a_j=\binom ks\lambda_s\) \((0\le s\le t)\) together with
\(a_k=[\,S\text{ is a block}\,]\).  The two solutions differ by the kernel vector
\(\bigl((-1)^{k-j}\binom kj\bigr)_j\).  (Sign note: the exponent is \(k-j\), not
\(j\); they agree only for even \(k\), and getting it wrong produces spurious
negative entries at odd \(k\).)

| | distribution \(a_0,\dots,a_8\) |
|---|---|
| fixed **block** | \(758,\,5376,\,13216,\,14336,\,7560,\,1792,\,224,\,0,\,1\) |
| fixed **non-block** 8-set | \(757,\,5384,\,13188,\,14392,\,7490,\,1848,\,196,\,8,\,0\) |

Both are non-negative and integral, so no contradiction.  Two independent
self-checks confirm the arithmetic: a non-block 8-set must meet exactly
\(a_7=8\) blocks in 7 points (its eight 7-subsets lie in distinct blocks), and
\(a_7=0\) for a block; both hold.  The same routine reproduces the known
\(n_0=1-[K\in A]\) law at \(S(14,15,31)\), \(S(2,3,7)\) and \(S(4,5,11)\).

Other tests, all satisfied:

- **Ray-Chaudhuri–Wilson** (\(t=2s+1\), \(s=3\)): \(b\ge 2\binom{23}{3}=3542\);
  actual \(43263\).
- **Tits/Fisher**: \(v\ge(t+1)(k-t+1)=16\); actual \(24\).
- Non-negativity and integrality of the \(s\)-set distributions for every
  \(s\le t\).

The same audit run along the whole tower — \(S(6,7,23)\), \(S(5,6,22)\),
\(S(4,5,21)\), \(S(3,4,20)\), \(S(2,3,19)\) — produces **no** negative forced
count anywhere.

## 3. Why the S(14,15,31) method does not transfer (PROVED)

The refutation of triangle closure worked because the weight enumerator of the
even point-code of \(S(14,15,31)\) is **forced**, which in turn worked because
\(v=31\) is odd and blocks have odd size \(15\): then

\[
 |B\cap S^c|=15-|B\cap S|\ \Longrightarrow\ F(S^c)=-F(S),
\]

so size \(m\) is tied to size \(31-m\), only the middle pair \(m=15,16\) is
uncertain, and the number of \(16\)-sets taking each value is itself forced
(exactly \(b\) of them).  One unforced layer, with its split known.

At \(S(7,8,24)\) both \(v=24\) and \(k=8\) are even, so
\(F(S^c)=+F(S)\): size \(m\) is tied to \(24-m\), and

\[
 F(S)=\sum_{i=0}^{7}\binom mi(-2)^i\lambda_i+(-2)^8\cdot\#\{\text{blocks}\subseteq S\}.
\]

So \(F\) is forced only for \(m\le7\) (and by symmetry \(m\ge17\)); across
\(8\le m\le16\) it depends on the block-content distribution.  Layers \(m=8,9\)
are still forced (\(b\) blocks; \(16b\) nine-sets containing one, and no
nine-set contains two since two blocks meet in at most 6 points), and the
*second* moment at each layer is forced by the pair distribution.  But the
**third** moment needs the number of \(m\)-sets containing three blocks — which
is exactly the unforced triple data.  **No MacWilliams-forced dual count is
available**, so the census argument has no analogue here.

For completeness, the objects it would have counted: a weight-3 word of the
\(S(7,8,24)\) point code is three blocks with every point in \(0\) or \(2\) of
them; since \(|B_1|=|B_1\cap B_2|+|B_1\cap B_3|=8\) and likewise for the others,
all three pairwise intersections equal \(4\) and the triple intersection is
empty.  Such pairs exist (\(a_4=7560>0\)), but their completion count is not
forced.

## 4. What a proof would need

Any nonexistence proof for \(S(7,8,24)\) must use something beyond: divisibility,
the intersection distributions of one or two blocks, RCW/Fisher/Tits, and the
Delsarte LP — the last being dead at every tower level by
`collaboration/opus5/PROOF.md` Thm 7/7a.  The candidates that remain are the
ones that are genuinely harder: an argument that settles \(S(4,5,21)\), or a
\(t=7\)-specific structure (block-triple counts, the \(v=3k\) partition
structure with \(n_0=758\), or a 2-rank/code argument on the span of the 43263
blocks) for which no forced input currently exists.

## 5. Scope

This is a negative audit: it records that the cheap conditions are all
satisfied and that one specific promising method provably does not transfer.
It is **not** a nonexistence proof, **not** an existence proof, and has no
bearing on Problem #835 beyond narrowing where to look.
