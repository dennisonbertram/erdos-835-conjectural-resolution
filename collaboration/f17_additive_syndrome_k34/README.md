# A \(K_{34}\) obstruction to the two-layer additive syndrome

## Result

Label the \(32\) points by

\[
P=\mathbb F_{17}^{\!*}\times\{0,1\}\subset\mathbb F_{17}^2
\]

and, for a \(16\)-set \(S\subset P\), retain only its additive syndrome

\[
\sigma(S)=\sum_{z\in S}z\in\mathbb F_{17}^2.
\]

Let \(h:\mathbb F_{17}^2\to\Omega\) be completely arbitrary.  If

\[
c(S)=h(\sigma(S))
\]

is a proper colouring of \(J(32,16)\), then

\[
\boxed{|\Omega|\ge 34.}
\]

In particular, no arbitrary decoder of this natural two-coordinate additive
syndrome can give the required \(17\)-colouring.

This is an obstruction to one construction family.  It does not constrain a
colouring which retains other statistics, and it does **not** solve
Erdős--Rosenfeld problem #835.

## Proof

Form the syndrome quotient graph \(H\) on \(\mathbb F_{17}^2\): join \(u\ne v\)
when there are adjacent \(16\)-sets \(S,S'\) of \(J(32,16)\) with
\(\sigma(S)=u\) and \(\sigma(S')=v\).  Any postprocessing \(h\) which properly
colours the Johnson graph must properly colour \(H\).

The set

\[
Q=\mathbb F_{17}\times\{7,8\}
\]

has \(34\) elements.  The exact finite certificate proves that every one of
the

\[
\binom{34}{2}=561
\]

pairs in \(Q\) is an edge of \(H\).  For each pair it constructs a
\(15\)-set \(T\subset P\) and two distinct points \(x,y\in P\setminus T\)
such that

\[
S=T\cup\{x\},\qquad S'=T\cup\{y\}
\]

have the prescribed syndromes.  The two sets differ by the single exchange
\(x\leftrightarrow y\), so they are adjacent in \(J(32,16)\).  Thus
\(H[Q]=K_{34}\), forcing \(34\) distinct decoder values on \(Q\).

The witness construction is exhaustive but elementary.  For every unordered
pair \(x,y\in P\), it uses exact subset-sum dynamic programming to retain one
explicit \(15\)-subset of \(P\setminus\{x,y\}\) at every reachable syndrome.
It then independently checks the resulting \(561\) pairs as actual Johnson
edges.  No SAT/SMT solver, floating point, randomness, or unverified
inference is used.

## Verification

Run:

```sh
python3 -B \
  collaboration/f17_additive_syndrome_k34/verify_f17_additive_syndrome_k34.py
```

The standard-library verifier checks:

1. the \(32\) ground labels are distinct;
2. every recorded core has exactly \(15\) points and omits both exchanged
   points;
3. both completed sets have size \(16\) and symmetric difference \(2\);
4. their syndromes are the requested two vertices of \(Q\); and
5. all \(561\) unordered pairs of \(Q\) occur.

The deterministic canonical witness digest is

```text
8693f164a9986ad6baa58baaf1689fcc12889bec1d0cf552e0d43a155ea4497e
```

## Scope

Proved: a \(K_{34}\) in the exact quotient of the two-layer additive
\(\mathbb F_{17}^2\) syndrome, robust to arbitrary postprocessing.

Not proved: anything about unrelated two-coordinate statistics, higher-order
statistics, arbitrary \(17\)-colourings, the existence of
\(LS(14,15,31)\), or problem #835.
