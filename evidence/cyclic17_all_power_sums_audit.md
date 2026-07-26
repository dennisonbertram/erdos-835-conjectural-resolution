# Complete power-sum audit of the cyclic radius-five linear shadow

Date: 2026-07-26.  Exact verifier:
`audit_cyclic17_all_power_sums.py`.

> **Scope.**  This audit closes one necessary-condition route for the
> fixed-Wallis, \(\mathbb Z_{17}\)-equivariant radius-five layer.  It proves
> that every dependency-cancelled power-sum equation over
> \(\mathbb F_{17}\) is consistent.  It does **not** construct the joint
> layer, exclude the cyclic ansatz, or solve Erdős--Rosenfeld Problem #835.

## 1. The complete finite-field family

The compact joint layer has \(4\,200\) phase variables.  Its \(840\) slice
permutations and \(600\) cross permutations give \(1\,440\) first-moment
equations over \(\mathbb F_{17}\).  Their coefficient matrix has rank
\(1\,320\), so its left kernel has dimension \(120\).

For every degree \(m=2,\ldots,16\), replace each permutation equation by
its degree-\(m\) power-sum identity.  The leading lifted monomials
\(x_v^m\) have the same \(1\,440\)-by-\(4\,200\) coefficient matrix.
Applying the \(120\) exact left-kernel vectors therefore cancels every
degree-\(m\) monomial and leaves \(120\) linear equations in lower powers.

Degrees through \(16\) are complete: every function on
\(\mathbb F_{17}\) is represented by a polynomial of degree at most \(16\),
and \(x^{17}=x\).  Thus no additional degree can create a new
dependency-cancelled power-sum condition of this kind.

## 2. Exact result

The verifier adds the original \(1\,440\) equations and then the \(120\)
cancelled equations at each degree.  Sparse Gaussian elimination is carried
out exactly modulo \(17\).  The augmented system remains consistent at every
stage:

| maximum degree | rows | rank | status |
|---:|---:|---:|:---|
| 1 | 1,440 | 1,320 | consistent |
| 2 | 1,560 | 1,320 | consistent |
| 3 | 1,680 | 1,440 | consistent |
| 4 | 1,800 | 1,560 | consistent |
| 5 | 1,920 | 1,680 | consistent |
| 6 | 2,040 | 1,800 | consistent |
| 7 | 2,160 | 1,920 | consistent |
| 8 | 2,280 | 2,040 | consistent |
| 9 | 2,400 | 2,160 | consistent |
| 10 | 2,520 | 2,280 | consistent |
| 11 | 2,640 | 2,400 | consistent |
| 12 | 2,760 | 2,520 | consistent |
| 13 | 2,880 | 2,640 | consistent |
| 14 | 3,000 | 2,760 | consistent |
| 15 | 3,120 | 2,880 | consistent |
| 16 | 3,240 | 3,000 | consistent |

The degree-two equations are already consequences of the first-moment
system.  Every later degree contributes exactly \(120\) new independent
linear equations, but never a contradictory constant row.

## 3. What is and is not closed

This is the endpoint of the following route:

1. write the prescribed power sums of every slice and cross permutation;
2. take arbitrary \(\mathbb F_{17}\)-linear combinations;
3. cancel the highest lifted powers using all \(120\) left dependencies;
4. repeat through the complete degree-\(16\) function basis.

That entire linearized moment family is compatible.

The audit deliberately treats \(x_v,x_v^2,\ldots,x_v^{16}\) as lifted
coordinates after the power-sum expansion.  It does not enforce their
nonlinear relation to one common phase value, nor the integral
`AllDifferent` constraints themselves.  Those nonlinear conditions remain
the live content of the exact SAT and construction searches.

Reproduce with:

```bash
python3 -B evidence/audit_cyclic17_all_power_sums.py
```

The recorded terminal line is:

```text
{'status': 'CONSISTENT', 'scope': 'all dependency-cancelled power sums through degree 16; not a radius-five witness', 'first_moment_rank': 1320, 'left_dependencies_per_degree': 120, 'final_rank': 3000}
```
