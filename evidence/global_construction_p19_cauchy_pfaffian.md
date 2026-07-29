# The cyclic 36th-root Cauchy-Pfaffian formula fails at (k=18)

The maximal-minor obstruction for (p\equiv1\pmod4) does not include
(p=19), so (k=18) is a separate possible route to Erdős Problem #835.
This file tests the strongest directly analogous cyclic formula, not the
already excluded (k=16) maximal-minor ansatz.

Let (K=\mathbb F_{19^2}), let (H\le K^\times) have order 36, and take
the 36 ground points to be the coset (gH), with (g) primitive.  This
choice has no Cauchy pole (xy=1) between distinct points.  For
\[
 C_{xy}=\frac{x-y}{1-xy},
\]
the two natural (\mathbb F_{19})-valued Pfaffian rules on 18-sets are
\[
 \operatorname{Tr}(\lambda\operatorname{Pf}_K(C[S]))
 \quad\hbox{and}\quad
 \operatorname{Pf}\bigl(\operatorname{Tr}(\lambda C_{xy})\bigr)_{x,y\in S},
\]
where (\lambda) ranges over the 20 projective trace directions.

`global_construction_p19_cauchy_pfaffian.py` finds the following exact
17-star for every one of those directions:
\[
T=(1,3,4,5,9,11,12,14,15,18,21,22,23,25,26,29,34).
\]
For instance, in the (K)-Pfaffian trace rule with 
\(\lambda=(0,1)\), its 19 extension colours are
\[
(16,2,14,10,3,4,8,18,4,15,2,16,10,15,14,15,12,3,3),
\]
only ten distinct values.  The program independently recomputes the
underlying (K)-Pfaffians by alternating elimination and verifies
Schur's product formula on all 19 extensions.  It separately eliminates
the entry-trace version; its ((0,1)) direction has only 12 values on
the same star.

Run:

```bash
python3 -B evidence/global_construction_p19_cauchy_pfaffian.py \
  --stars 1 --seed 83519
```

The initial 300-star screen found this same counterstar immediately for
all directions.  This is an exact counterexample to the stated cyclic
36th-root Cauchy-Pfaffian families, not a no-go theorem for arbitrary
(19)-colourings or arbitrary Pfaffian matrices.
