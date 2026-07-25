# Claude Opus 5 xhigh assignment: break the integral parity frontier

You are the principal mathematical investigator. Work at maximum reasoning
effort. Cost is not a stopping condition. The full objective is Erdős–
Rosenfeld Problem #835:

This is a self-contained one-shot reasoning assignment. You have no
repository tools in this run. Do not announce a plan to inspect files or ask
for more context: all facts you may rely on are stated below. Spend the turn
doing the mathematics and return a substantive final answer.

> Determine whether any integer \(k>2\) admits a tight
> \((k+1)\)-colouring of \(J(2k,k)\), equivalently an
> \(LS(k-1,k,2k)\).

A construction for one \(k\) resolves the full existential question
positively. A nonexistence proof only for \(k=16\) does **not** resolve the
full question; it closes the first open case. Keep that distinction explicit.

Your core assignment in this pass is the first open case. Try to prove or
refute the following genuinely nonlinear statement.

## Exact fixed-base target

Let \(r=15\), \(X\) have \(31\) points, and let
\(A\) be an \(S(14,15,31)\). Let \(B,C\) be two further
\(S(14,15,31)\) systems, each block-disjoint from \(A\). Prove

\[
|B\cap C|\equiv1\pmod2. \tag{P}
\]

Since each system has
\[
b=\binom{31}{14}/15=17\,678\,835
\]
blocks, (P) forbids three pairwise-disjoint systems and hence forbids an
\(LS(14,15,31)\), which is a necessary derived object for the \(k=16\)
large set.

## Sphere/mate-map formulation you may use

Every non-\(A\) block belongs to a unique sphere indexed by \(P\in A\).
Each mate \(B\) chooses exactly one block in every sphere, equivalently a map
\[
\varphi_B:A\to X,\qquad \varphi_B(P)\notin P,
\]
subject to the full nonlinear Steiner exact-one constraints. Moreover
\[
|B\cap C|=\#\{P\in A:\varphi_B(P)=\varphi_C(P)\}.
\]

For each \(P\in A\), the local facet completions of a mate give a canonical
bijection
\[
\pi_P^B:P\sqcup\{*\}\longrightarrow X\setminus P.
\]
The product of relative signs factors tautologically as
\[
\prod_P\operatorname{sgn}((\pi_P^C)^{-1}\pi_P^B)=E(B)E(C).
\]
Thus the useful statement would be a genuine proof that the global
orientation \(E(B)\) is constant on the nonlinear mate space, not merely
rewriting the product.

## Closed routes: do not rediscover or use them as proof

1. Put \(h=|B\cap C|\), \(t=b-h\), and let \(a_i\) count ordered
   cross-pairs of blocks meeting in \(15-i\) points. Exact containment
   identities imply, for every \(1\le i\le15\),
   \[
   a_i\equiv1+h\equiv t\pmod2.
   \]
   Every containment moment, including the second moment, is therefore the
   same parity tautology. Proving one \(a_i\) even is exactly as hard as (P)
   unless you supply an independent involution or invariant.
2. Ambient \(\mathbb F_2\), rowspace, bilinear, and ordinary kernel/lattice
   relaxations are insufficient. At \(r=5\), exact mates satisfy the
   analogous parity, but there are explicit shaped integral kernel vectors
   of odd active-sphere count. Any valid proof must use both endpoints'
   exact-one Steiner constraints, not merely their difference lying in a
   linear kernel.
3. The norm identity
   \(\|x_B-x_C\|^2=2t\), pair-trade inner products, facet-sharing counts,
   and the sign of a disjoint union of local permutations all restate the
   desired parity unless a new global mechanism is proved.
4. Three pairwise-disjoint systems induce matchings/permutations on
   intersection-one incidences. The fact that \(b\) is odd merely forces an
   odd number of odd cycles and is consistent with disjoint mates. Cycle
   parity alone is not a contradiction.
5. Finite truth at \(r=3\) and \(r=5\) is a control, not evidence that an
   unproved uniform identity holds at \(r=15\).

## Required heavy lifting

Pursue several mathematically independent attacks, abandoning one when you
can prove it is tautological:

- an integral orientation/determinant of the exact-one boundary maps whose
  sign can be computed both locally and globally;
- torsion or Smith-normal-form information for the *nonlinear Steiner
  slice*, not the ambient incidence kernel;
- an exterior-algebra, spin, Pfaffian, or chain-complex invariant that
  couples all spheres and survives relabelling;
- a canonical fixed-point-free involution on a cross-configuration class,
  with a proof that it has no hidden exceptional cases;
- or a counterexample mechanism/construction showing (P) is false.

Also ask whether any mechanism genuinely extends to all prime candidates
\(k=p-1\). Do not claim such an extension without proof.

## Output contract

Return one of:

1. a complete proof of (P), with every map and sign convention defined and
   every parity step checked;
2. a complete counterexample/construction with an independently checkable
   certificate;
3. or the strongest new unconditional lemma, a proof, and an exact statement
   of the remaining gap.

Label speculation. Check formulas at the valid \(r=3\) control and at
\(r=5\), where the parity is true but linear relaxations fail. Do not return
only a list of ideas or a literature summary.
