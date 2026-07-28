# Independent audit of the post-\(r=0\) bridge note

Date: 2026-07-28

This file records checks performed outside the Claude Opus 5 session that
wrote `NOTE.md`. The Opus session could not execute its scripts. The checks
below were run afterward with

```text
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3
```

They audit the finite claims and identify two scope corrections. They do not
prove Erdős--Rosenfeld Problem #835.

## Commands and results

```sh
cd collaboration/opus5/post_r0_global_bridge

/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  verify_petersen_dead_prefix.py

/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  verify_coupling_reformulation.py

/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  decide_certificate_completion.py
```

All three commands exited zero.

`verify_petersen_dead_prefix.py` printed `ALL CHECKS PASS`. In particular it
checked the fourteen pairwise edge-disjoint prefix matchings, the
\(8^{10}10^1 12^3\) prefix support ledger, the seventeen-row
\((n_8,n_{10},n_{12})=(10,4,3)\) class-B instance, the class-B-prime
incidence labelling, the exact Petersen residual, all six Petersen perfect
matchings, their pairwise intersections, non-\(3\)-edge-colourability, and
the matching-deletion inequality for all \(2^{15}\) edge subsets.

`verify_coupling_reformulation.py` printed `ALL CHECKS PASS`. It checked the
coordinate bijection of Theorem A, the thirteen \(K_6\) edge-colourings and
support identities of Theorem B, and the matching counts and disjointness
identities of Theorem C on four independently selected six-subsets of the
committed \(LS(2,3,19)\) control.

`decide_certificate_completion.py` printed an explicit seventeen-matching
partition of all \(78\) edges of \(K_{13}\), followed by `COMPLETES`. Its
post-search assertions checked that the \(78\) printed edges are distinct
and that every matching covers exactly its prescribed support. Thus branch
(a) of Corollary F holds:

> The class-B-prime instance itself completes, but the particular legitimate
> fourteen-prefix in Theorem D cannot be extended past fifteen.

The positive witness is enough to establish branch (a); no exhaustive
negative search is being claimed.

## Audit corrections

### 1. General level index in Theorem A

The concrete \(j=2\) statement is indexed correctly. In the general
statement, the phrase “level-\(\le j+1\) tower datum” is off by one.

The \((j+1)\)-subsets \(D\subseteq R\mathbin{\dot\cup}A\) that meet \(R\)
correspond to pairs \((B,Q)\) with

\[
|B|\le j,\qquad |Q|=|B|+3.
\]

Their Johnson-star conditions are the tower laws at levels
\(|B|=0,\ldots,j-1\), together with top-properness at level \(j\). Thus the
precise phrase is “the tower datum through level \(j\), with
top-properness at level \(j\),” not “through level \(j+1\).” The displayed
coordinate map and the \(j=2\) proof are unaffected.

### 2. Scope of Corollary F(b)

The phrase in Corollary F(b) saying that a noncompletion would refute “the
first-lift completion route to a simultaneous \(13\)-fan” is too broad.
A simultaneous \(13\)-fan is the preceding level-\(0/1\) datum, while the
class-B-prime instance is an abstract first-lift completion instance.
Moreover the fan-realizable class C is a proper subclass of class B-prime.
Noncompletion of one class-B-prime instance would refute the universal
class-B-prime completion conjecture, but would not by itself refute every
fan-realizable instance or the existence of a simultaneous fan.

This scope issue is moot for the displayed certificate because the executed
decision script proves branch (a).

### 3. Negative completeness claim in the decision script

`perfect_matchings(..., cap=400)` truncates a branching list when more than
400 perfect matchings are available. Therefore the script's docstring should
not advertise a hypothetical `NO COMPLETION` result as an exhaustive proof
without either removing that cap or proving it never binds at a branched
state. This does not affect the observed positive result: the explicit
completion witness is independently checked by the script's final
assertions.

## Scope

The audited results sharpen the level-\(2\) formulation and give a genuine
counterexample to arbitrary-prefix extension. They do not:

- prove existential completion of an arbitrary first-lift instance;
- prove the simultaneous six-instance implication (EMI);
- construct a simultaneous \(13\)-fan;
- complete the higher lift tower; or
- construct or exclude a tight colouring of \(J(32,16)\).

The full existential Erdős--Rosenfeld problem remains open.
