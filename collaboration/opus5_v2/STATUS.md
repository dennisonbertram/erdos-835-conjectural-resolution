# STATUS — Opus 5, v2

**Date:** 2026-07-25.
**Problem:** Erdős–Rosenfeld #835 — does any \(k>2\) admit a tight
\((k+1)\)-colouring of \(J(2k,k)\), equivalently an \(LS(k-1,k,2k)\)?

## Verdict

**Not resolved.**  No \(k\) with \(k\) even and \(k+1\) prime is excluded by
anything in this directory, and no construction is offered.  \(k=16\) remains
the first open case.

## Environment caveat — read this before trusting any number here

Code execution was **blocked** for the entire session: `python3` required an
approval that a non-interactive session cannot grant, and the same applied to
subagents and to the Codex tool.  Consequently:

* **Nothing in this directory was executed.**  The three validator scripts
  were written but **never run**.
* Every numerical statement in `PROOF.md` was computed by hand and is
  re-derivable from a displayed closed formula.  No number was carried over
  from memory or from another file in this repository.
* No previously recorded result in this repository was re-verified, and none
  is restated here as if it had been.

## Prior art inside this repository — correction to an earlier draft

I wrote `PROOF.md` before checking `collaboration/opus5/`, because the brief
said to inspect only the artifacts relevant to the chosen attack.  On checking
afterwards, **§§1–3 of `PROOF.md` reproduce results that a previous session in
this same repository had already proved.**  Specifically
`collaboration/opus5/PROOF.md` already contains:

* the closed forms \(n_{k-u}\) and \(m_u\) (my Theorems 1.3 and 3.1),
* Corollary 6.1 = my Corollary 1.4 (odd \(k\) excluded),
* Corollary 6.2 = my Theorem 2.1 (complement-closure of a single system),
* Theorem 7a, which is **stronger** than my Theorem 3.2: it proves the whole
  Delsarte LP is feasible at exact size at *every* tower level, not just that
  single-block shell counts are tight.

So those sections are an **independent re-derivation, not new work**.  They are
worth keeping only as a second, differently-routed proof (mine goes through one
generating-function identity, Lemma 1.2, rather than through Fourier support).
The novelty claims below are what survives that check.

## Results proved here that I did not find in the prior artifacts

1. **No \(S(k-1,k,2k)\) with \(k\) even has a transposition as an
   automorphism** (`PROOF.md` Thm 2.3); equivalently an automorphism fixing
   \(2k-2\) or more points is the identity.  Two lines from \(N_{k-1}=0\).
   Prior sessions have automorphism results at specific tower levels
   (involutions of an \(LS(4,5,21)\) fix exactly one point, etc.); this one is
   about a *single* system, uniform in \(k\), and is the first step of the
   condition \(\operatorname{Aut}(\mathcal D)\le A_{2k}\).

2. **The global star sign is a well-defined invariant and cannot decide the
   problem** (`PROOF.md` Thm 4.2, 4.3).  \(E(c)=\prod_B\operatorname{sgn}\phi_B\)
   is invariant under all point and all colour permutations, and its
   "down-star" dual is *literally the same function* once complement-closure
   is known.  A proof of a failure boundary, not a bound.

3. **The reduction of \(E(c)\) to local 1-factorization row parities**
   (`IDEAS.md` §B): \(E(c)=\pm\prod_{T}\epsilon_{\mathrm{row}}(L_T)\) over all
   \((k-2)\)-sets, with the symbol parity forced to \((-1)^{(p+1)/2}\) and
   \(\epsilon_{\mathrm{row}}\) proved invariant under relabelling *and* under
   every cycle switch.  The prior session listed "Latin-square signs and
   Alon–Tarsi" as **untried**; this makes it concrete and reduces it to one
   finite question (is \(\epsilon_{\mathrm{row}}\) constant on 1-factorizations
   of \(K_8\)?) that a single script decides.

4. **A uniform no-go for all additive colourings** (`PROOF.md` Thm 5.1), over
   any abelian group and any \(k\): \(c(A)=\sum_{a\in A}f(a)\) forces
   \(2k\le k+1\).  Three lines, no divisibility hypothesis; the repository's
   recorded additive/XOR exclusions are for specific families over specific
   fields.

5. **A hand counterexample killing a tempting sharpening** (`IDEAS.md` §A.4b):
   "\(|F\cap\pi F|\) odd iff \(\pi\) even" is false — \(\pi=(6\,7)\) on the
   standard Fano plane gives \(|F\cap\pi F|=3\) with \(\pi\) odd.

6. **A complete hand verification of the disjointness–parity mechanism on the
   \(\mathbb F_8\) power-map family** (`IDEAS.md` §A.4): for
   \(\pi_m(x)=x^m\), even \(\iff m\in\{1,2,4\}\) \(\iff\) line-preserving, and
   odd \(\iff m\in\{3,5,6\}\) \(\iff\) block-disjoint, on the nose.

## Exact remaining gap

Result 1 and its corollaries constrain a *single* Steiner system and are
automatically satisfied whenever \(k\) is even and \(k+1\) is prime.  Results
4–6 are proofs that specific attack families cannot work.  So the gap is
unchanged in substance:

> For \(k\) even with \(k+1\) prime and \(k\ge16\), nothing here decides
> whether \(k+1\) pairwise block-disjoint \(S(k-1,k,2k)\) systems exist.

The route in `IDEAS.md` §A — prove that **no three** \(S(k-1,k,2k)\) systems
are pairwise block-disjoint — is **not new either**: the prior session records
it as the "two-disjoint conjecture", true at \(k=4\) and \(k=6\), and the
project has already pushed hard on it through the \(|B\cap C|\equiv b\)
parity conjectures P and E.  What is new here is only the proposed *mechanism*
for it (a sign-equivariant \(\pm1\) invariant, §A.3), the hand evidence for
that mechanism (§A.4), the hand refutation of the obvious sharpening (§A.4b),
and the proved fragment \(\operatorname{Aut}\not\ni\) transposition (§A.4c).
The mechanism itself is **conjectural** and its cheapest falsification test
has not been run.

## Immediate falsification test (not run)

`verify_disjointness_parity.py` — enumerate all labelled \(S(2,3,7)\),
\(S(3,4,8)\), \(S(4,5,11)\); tag each by \(A_n\)-orbit; count block-disjoint
pairs by same/different orbit.  **A single same-orbit disjoint pair kills the
conjecture.**  `verify_intersection_numbers.py` re-checks the closed form of
Result 1 by brute force on the two known systems and re-runs the integrality
sieve.  `verify_onefactorization_row_parity.py` settles the one open lever in
`IDEAS.md` §B by deciding whether the row parity of a 1-factorization of
\(K_8\) is constant.

Run order, cheapest first:
```bash
python3 -B collaboration/opus5_v2/verify_intersection_numbers.py
python3 -B collaboration/opus5_v2/verify_onefactorization_row_parity.py
python3 -B collaboration/opus5_v2/verify_disjointness_parity.py
```

## Why this does not prove the full problem

Nothing here is a universal theorem about tight colourings.  Result 2 is a
universal theorem about single Steiner systems.  Results 4–6 are universal
theorems about *attack families*, i.e. restricted no-gos.  Neither a
construction nor a nonexistence proof for any open \(k\) is claimed.
