# Erdős–Rosenfeld Problem #835

A researched conjectural resolution of Erdős–Rosenfeld Problem #835, with
rigorous reductions and reproducible computational evidence.

## Status

The full problem remains open. This repository does **not** claim a complete
proof. It advances and precisely formulates the negative conjecture

\[
\chi(J(2k,k)) \geq k+2 \qquad (k>2),
\]

and proves several consequences and restricted obstructions. The first
unresolved case is \(k=16\).

The main result established here is:

> An \(S(4,5,21)\) Steiner system cannot admit an involution fixing exactly
> five points.

This rules out the natural dihedral/affine-symmetric construction at \(k=16\).
The cyclic-only case remains unresolved.

## Contents

- [`erdos_835_conjectural_resolution.md`](erdos_835_conjectural_resolution.md):
  the complete mathematical note, literature review, proofs, conjecture, and
  explicit limitations.
- [`verify_k4.py`](verify_k4.py): exhaustively generates the 30 labelled
  \(S(3,4,8)\) systems and verifies that at most two are pairwise disjoint.
- [`search_cyclic_ls_4_5_21.py`](search_cyclic_ls_4_5_21.py): a CP-SAT exact
  cover model for a cyclic \(LS(4,5,21)\), including the reflection-restricted
  case.
- [`evidence/verification.txt`](evidence/verification.txt): recorded output
  from the reproducibility checks.

## Reproduce the checks

Python 3.11 or newer is recommended.

```bash
python3 verify_k4.py
python3 -m pip install -r requirements.txt
python3 search_cyclic_ls_4_5_21.py --reflection --seconds 30
python3 search_cyclic_ls_4_5_21.py --seconds 300
```

Expected decisive outputs:

- `verify_k4.py`: maximum pairwise disjoint systems = `2`, so no required
  five-colouring exists for \(k=4\).
- Reflection-restricted \(k=16\) model: `INFEASIBLE`.
- Unrestricted cyclic \(k=16\) model: currently `UNKNOWN` after the bounded
  five-minute search. This is neither an existence nor a nonexistence result.

## Primary references

- [Erdős Problem #835](https://www.erdosproblems.com/835)
- J. Ma and Q. Tang,
  [A Note on Erdős Problem #835](https://github.com/QuanyuTang/erdos-problem-835/blob/main/On_Problem_835.pdf)
- M. Kiermaier, V. Krčadinac, and A. Wassermann,
  [Steiner 3-designs as extensions](https://arxiv.org/abs/2509.23483)

Additional references are listed in the main note.
