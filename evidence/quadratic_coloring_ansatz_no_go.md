# A no-go theorem for quadratic finite-field colorings

This note concerns a **restricted ansatz**, not Erdos--Rosenfeld problem #835
itself.  It rules out colorings obtained by evaluating a polynomial of degree at
most two in the incidence variables of a `(p-1)`-subset.

Let `p >= 5` be prime, let `V` have size `2p-2`, and put `k=p-1`.  Choose
`c, a_i, b_ij` in `F_p`, with `b_ij=b_ji`, and define, for every `k`-subset,

```
f(S) = c + sum(i in S) a_i + sum({i,j} subset S) b_ij  in F_p.
```

There is no choice of these coefficients for which, for every `p`-subset `T`,
the `p` values `f(T - {x})` (`x in T`) are all distinct.  Consequently this
quadratic ansatz cannot produce an `LS(p-2,p-1,2p-2)`, in particular it cannot
settle #835 positively at `p=17` (`k=16`).

## Proof

For `x in T` set

```
w_T(x) = a_x + sum(y in T - {x}) b_xy.
```

There is a quantity `K_T`, independent of `x`, such that
`f(T-{x}) = K_T - w_T(x)`.  Thus the required rainbow condition says that
the `w_T(x)` are the elements of `F_p`, once each.  Their sum is zero.  (More
explicitly, summing the displayed relation over `x` gives
`sum_x f(T-{x}) = -sum_x w_T(x)`.)  Hence every `p`-subset `T` satisfies

```
0 = F(T) := sum(x in T) a_x + 2 sum({x,y} subset T) b_xy.             (1)
```

Fix distinct `i,j`, and take a `(p-1)`-set `U` disjoint from them.  Subtract
`F(U union {j})` from `F(U union {i})` to obtain

```
a_i-a_j + 2 sum(u in U) (b_iu-b_ju) = 0.                             (2)
```

Now choose distinct `r,s` outside `i,j`, and a `(p-2)`-set `W` disjoint from
`i,j,r,s`.  This is possible because `p-2 <= 2p-6` for `p>=4`.  Use (2) once
with `U=W union {r}` and once with `U=W union {s}`.  Since `2` is invertible,

```
b_ir-b_jr = b_is-b_js.                                               (3)
```

Thus for each ordered pair `i,j` there is a well-defined `delta_ij` with
`b_ir-b_jr=delta_ij` for every `r` distinct from `i,j`.  For three distinct
indices, cancellation in this identity gives
`delta_ij+delta_jl=delta_il`.  Choose a base point `q` and put
`d_i=delta_iq` (with `d_q=0`).  The cocycle identity, including the cases
involving `q` by antisymmetry, gives

```
delta_ij = d_i-d_j.                                                   (4)
```

For a fixed `r`, (4) says that `b_ir-d_i` is independent of `i != r`; call it
`h_r`.  Symmetry of `b` then gives `d_i+h_r=d_r+h_i`, so there is one constant
`C` such that `h_i=d_i+C` for every `i`.  Therefore

```
b_ij = d_i+d_j+C.                                                     (5)
```

Substitution of (4) into (2), using `|U|=p-1=-1` in `F_p`, yields
`a_i-2d_i=a_j-2d_j`.  Write their common value as `A`.  Finally, if
`D_T=sum_{y in T}d_y`, equations (5) and `a_i=A+2d_i` give

```
w_T(i) = A+2d_i + (p-1)d_i + (D_T-d_i) + (p-1)C
         = A+D_T-C,
```

which is independent of `i in T`.  This contradicts the rainbow condition.

The argument uses only the first power-sum consequence of rainbowness; it is
therefore stronger than a search over special coefficient families.  The
accompanying verifier checks each finite-field identity on deterministic
instances, including `p=17`.  It is a diagnostic check of the algebra, not a
substitute for the symbolic proof above.

## Scope

An arbitrary tight coloring need not have a degree-two representation in the
incidence variables, so this result neither proves nor disproves problem #835.
