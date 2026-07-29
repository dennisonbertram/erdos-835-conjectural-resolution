# A target-order dead prefix at the first lift

Date: 2026-07-27.

## Scope

This note attacks one tempting route to the unresolved first-lift completion
theorem for Erdős--Rosenfeld Problem #835.  It gives an exact counterexample
to **arbitrary greedy extension of the dense five-colour prefix**.  It is not
a counterexample to the universal class-B or class-B-prime completion
questions, and it says nothing by itself about fan-realizable class C.

The three tiers remain distinct:

1. **aggregate graphicity:** the union degree sequence of every colour
   subfamily is graphic (already proved elsewhere in the repository);
2. **partial-factorization realization:** the supports come from a proper
   colouring of \(K_{18}-E(K_{13})\) saturating the five outside vertices;
3. **fan realization:** the partial colouring is coupled to one simultaneous
   \(13\)-fan.

The instance below is in tier 2 and has a full \(K_{13}\) completion.  No
tier-3 witness is claimed.

## The exact negative result

Let \(A=\{0,\ldots,12\}\) and let the seventeen colour-missing sets
\(B_c=A\setminus V_c\) be

\[
\begin{array}{c|l}
0&6,7,10,11,12\\
1&3,7,8,11,12\\
2&3,4,8,9,12\\
3&4,5,8,9,10\\
4&5,6,9\\
5&8,9,10,11,12\\
6&0,1,2,8,9\\
7&0,3,10,11,12\\
8&0,3,10\\
9&1,4,11\\
10&1,2,3\\
11&1,2,4\\
12&0,4,5\\
13&0,5,6\\
14&1,5,7\\
15&2,6,7\\
16&2,6,7 .
\end{array}
\tag{1}
\]

Every vertex occurs in exactly five of the \(B_c\)'s.  Seven columns have
size five and ten have size three, so the support profile is exactly
\[
 (n_8,n_{10},n_{12})=(7,10,0).
\tag{2}
\]
Thus (1) is a target-order class-B instance.

Consider colours \(0,1,2,3,4\), whose support sizes in that order are
\[
 8,8,8,8,10.
\tag{3}
\]
They satisfy \(|V_i|\ge 2(i+1)\), precisely the numerical hypothesis of the
dense-support prefix lemma.  Choose the following perfect matchings:

\[
\begin{array}{c|l}
0&03,\ 14,\ 25,\ 89\\
1&04,\ 15,\ 26,\ 9\,10\\
2&05,\ 16,\ 27,\ 10\,11\\
3&06,\ 17,\ 23,\ 11\,12\\
4&07,\ 13,\ 24,\ 8\,11,\ 10\,12 .
\end{array}
\tag{4}
\]

They are pairwise edge-disjoint and each saturates its prescribed support.
Inside the next support
\[
 V_5=\{0,1,2,3,4,5,6,7\},
\]
the matchings (4) use every edge between
\[
 X=\{0,1,2\},\qquad Y=\{3,4,5,6,7\}.
\]
Consequently the still-available graph induced by \(V_5\) is exactly
\[
 K_X\mathbin{\dot\cup}K_Y\cong K_3\mathbin{\dot\cup}K_5.
\tag{5}
\]
Both components have odd order, so (5) has no perfect matching.  The valid
five-colour prefix (4) cannot even be extended to colour \(5\).

This is a solver-free obstruction to the proposed proof rule

> choose any dense-prefix matchings first, then extend the suffix.

Any successful use of the dense-prefix lemma must coordinate the prefix with
the suffix; mere existence of a packable prefix is not an inductive state.

## Why this does not refute completion

The verifier embeds two additional exact certificates.

First, a \(13\times5\) cross-edge array together with a colouring of the ten
edges of \(K_5\) proves from the definition that (1) comes from a genuine
proper \(17\)-edge-colouring of \(K_{18}-E(K_{13})\) saturating all five
outside vertices.  Hence the instance is class B-prime, not merely class B.

Second, a different family of seventeen matchings partitions all
\(\binom{13}{2}=78\) edges and saturates exactly the supports (1).  Therefore
the support instance itself is completable.  What fails is only the specific
greedy prefix (4).

This separation is deliberate:

* aggregate graphicity remains a necessary shadow and is not challenged;
* partial-factorization realization is explicitly certified;
* a complete support-level factorization is explicitly certified;
* fan realization is not asserted or tested.

## Verification

Run:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/verify_dead_prefix.py
```

The verifier uses only the Python standard library.  It reconstructs the
support matrix, verifies class-B arithmetic, checks the proper saturated
partial \(K_{18}-E(K_{13})\) colouring, verifies every edge of (4), proves
the residual graph is exactly \(K_3\dot\cup K_5\), independently exhausts
the tiny perfect-matching recursion, and checks every edge of the explicit
full completion.

`find_dead_prefix_completion.py` records how the two displayed witnesses
were derived using the repository's exact search code and CP-SAT.  Its
output is not trusted by the theorem: the standard-library verifier checks
the resulting certificates directly.

## Remaining frontier

The strong question is unchanged: must every class-B target instance
complete?  The class-B-prime restriction and the still smaller class-C
restriction also remain open.  This note closes only one local proof route:
there is no safe arbitrary five-prefix, even at the exact target order and
even for a completable class-B-prime instance.
