# Opus 5 holonomy-followup prompt

Model: `claude-opus-5`

Effort: `max`

The following is a Markdown-normalized transcript of the prompt supplied to
the external Claude Code run on 2026-07-27.  The initial sandboxed call failed
before inference with `ENOTFOUND`; the identical prompt was then relaunched
with approved external network access.  The prompt's original count of 231
fixed-point types is preserved below as historical input; the run and
independent audit corrected it to 55 because the fixed point is unique.

---

You are Claude Opus 5 continuing the heavy mathematical attack on the
persistent goal of fully resolving Erdős–Rosenfeld Problem #835.

Operate in `/Users/dennison/Documents/Math Problem`. Invoke and faithfully use
the `/efficient-frontier` skill first. Work at maximum reasoning effort. Cost
is not a stopping condition. Opus 5 must perform the core novel reasoning.

The exact target remains unrestricted:

Does there exist \(k>2\) with \(\chi(J(2k,k))=k+1\), equivalently
\(LS(k-1,k,2k)\)? The first live candidate is \(k=16\). A construction of
\(LS(15,16,32)\) solves #835. Nonexistence for \(k=16\) alone does not settle
the existential quantifier.

Start by reading:

- `collaboration/opus5/unrestricted_ls3420_attack_2/NOTE.md`
- `collaboration/opus5/unrestricted_ls3420_attack_2/AUDIT.md`
- `collaboration/opus5/unrestricted_ls3420_attack_2/VERIFICATION.md`
- `collaboration/simultaneous_ls3420_fan/README.md`
- `collaboration/h3_simultaneous_fan_audit/README.md`
- `collaboration/opus5/derivation_tower_obstruction/NOTE.md`
- `evidence/solver_reconnaissance_2026-07-27.md`

Preserve the independent audit corrections exactly:

1. The general star-sign parity law is indexed by \((t-2)\)-subsets \(W\) and
   \((t-1)\)-subset signs \(\epsilon(W\cup\{p\})\). At \(t=15\) it has
   \(\binom{32}{13}\) equations of rank \(\binom{31}{13}\), not one graph per
   13-subset.
2. The 20 degree equations at \(LS(3,4,20)\) have rank 19.
3. The odd-\(t\) invariance statement is scoped to \(1\le t\le15\).
4. Solver `UNKNOWN` is no evidence, and solver `UNSAT` needs an independently
   checked proof.
5. The holonomy tower identity is valid but tautological on a genuine object;
   it is not by itself an obstruction.

Research task:

Attack the concrete successor frontier exposed by the audited note. For an
\(LS(3,4,20)\), the 20 derived \(LS(2,3,19)\) have holonomy census vectors
over the 231 fixed-point cycle types of \(S_{17}\), and their sum is even
componentwise. Determine whether universal congruences,
representation-theoretic identities, orientation constraints, or overlap
compatibility of attainable \(LS(2,3,19)\) holonomy vectors can make this
condition contradictory. Seek a rigorous obstruction, a construction, or a
lossless reduction. Explore non-abelian/group-algebra refinements if cycle
type loses essential data. Connect the result to the simultaneous 13-fan
shadow if useful.

Do not launch another long SAT/CP-SAT/DLX run; several certificate-producing
searches are already consuming disk and CPU. Bounded exact computations and
small analogues are welcome. Continuously falsify every conjecture against
the genuine cyclic \(LS(2,3,19)\), \(LS(2,3,9)\), and small controls. Search
primary literature before any priority claim.

Write all new work only under:

`collaboration/opus5/holonomy_followup/`

Create a self-contained `NOTE.md` and standard-library verifiers when there
is a rigorous result. Do not edit other repository files. Do not commit or
push. Do not claim #835 solved unless the complete existential problem is
genuinely resolved.

Your final report must begin with exactly one of:

```text
SOLVED #835
K16 UNRESTRICTED NEGATIVE ONLY
RIGOROUS PROGRESS, #835 OPEN
NO NEW RIGOROUS PROGRESS, #835 OPEN
```
