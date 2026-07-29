# Independent audit

This directory was independently audited after the Opus 5 pass. The audit
checked the mathematics, exact CNF encoding, second-star symmetry split,
semantic SAT-witness verifier, and retained runtime artifacts. It did not
launch a solver and does not claim to resolve Erdős–Rosenfeld #835.

## Mathematical result

The audit found no defect in Theorems 1–3, 6, or 7. In particular, the
star-sign tower identity and holonomy tower identity are correctly indexed
and proved.

It found and caused these material corrections:

1. The general form of Theorem 4 was off by one. The correct law is
   \[
     \prod_{p\in X\setminus W}\varepsilon(W\cup\{p\})=1
     \quad\text{for }W\in\binom X{t-2},
   \]
   with \(\varepsilon\) indexed by \((t-1)\)-subsets. At \(t=15\), this is
   \(347{,}373{,}600\) equations on \(471{,}435{,}600\) fourteen-subset
   signs, of exact rank \(206{,}253{,}075\). The equivalent even graphs are
   indexed by \(225{,}792{,}840\) twelve-subsets.
2. The twenty degree equations for \(LS(3,4,20)\) have rank \(19\), not
   \(20\). The cycle space describes patterns not excluded by these linear
   equations, not patterns proved realizable by a large set.
3. “Invariant exactly for odd \(t\)” is restricted to the relevant
   \(1\le t\le15\) segment. It is false without that scope.
4. Theorem 5 now limits only the displayed rigidity argument; it does not
   rule out future overlap or attainable-distribution obstructions.

## Implementation result

- `g1_cnf.py` correctly encodes proper \(m\)-colouring of \(J(n,s)\).
- Root normalization is WLOG.
- The checked CNF headers are \(17{,}745/498{,}237\) and
  \(65{,}892/2{,}507{,}788\) variables/clauses.
- The abstract second-star orbit split is complete, with 56 and 176 branches.
- `verify_solution.py` semantically reconstructs and checks a claimed large
  set. The DIMACS parser now rejects out-of-range, contradictory, or
  incomplete assignments.
- UNSAT exit codes are not certificates. `run_branches.py` now labels an
  all-UNSAT solver sweep as pending independent proof verification.
- Certificate verifiers refuse to run under `python -O`.
- Caller-supplied ground-set order is now preserved by `star_sign`.

## Runtime scope

Interrupted temporary branch CNFs, empty output, and platform-specific
binaries are not evidence and are not committed. Reproducible base CNFs,
source, a retained positive witness, and scope-labelled run snapshots are
included. `runs/README.md` records their status and hashes.

After the corrections:

- `verify_star_sign.py`: expected `44/44`.
- `second_star_split.py`: expected 56/176 branch counts after its exhaustive
  small-\(d\) orbit audit.
- Ruff lint and formatting are required to pass before commit.

The unrestricted construction or obstruction required for #835 is still
missing.
