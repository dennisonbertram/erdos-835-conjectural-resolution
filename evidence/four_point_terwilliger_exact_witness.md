# An exact feasible witness beyond the triple layer at \(k=16\)

This note records an exact rational feasible point for a strong necessary
relaxation of the first open case of Erdős--Rosenfeld Problem #835.  It is a
rigorous **no-go result for this proof strategy**, not a coloring and not a
solution of the problem.

The first open case asks whether the Odd graph

\[
O_{16}=K(31,15)
\]

can be partitioned into \(17\) perfect codes, equivalently whether it has a
locally bijective graph map to \(K_{17}\).  Such a map would assign a color
to every \(15\)-subset of \([31]\), with every closed neighborhood containing
all \(17\) colors exactly once.

## 1. The exact triple-orbit variables

Fix a vertex \(x\).  The stabilizer of \(x\) has \(3\,876\) orbits on ordered
pairs \((y,z)\).  Write an orbit as

\[
g=(i,j,s,t),
\]

where

\[
i=|x\cap y|,\quad j=|x\cap z|,\quad
s=|x\cap y\cap z|,\quad t=|\bar x\cap y\cap z|.
\]

Thus \(u=s+t=|y\cap z|\).  The exact orbit size is the product of the two
corresponding multinomial coefficients; the verifier regenerates it rather
than trusting stored orbit data.

For each orbit \(g\), introduce five color-equality probabilities

\[
q_g(\mathrm{AAA}),\ q_g(\mathrm{AAB}),\
q_g(\mathrm{ABA}),\ q_g(\mathrm{ABB}),\ q_g(\mathrm{ABC}).
\]

They partition the orbit according to the equality pattern of
\((c(x),c(y),c(z))\).

For relation \(i\), put

\[
v_i=\binom{15}{i}\binom{16}{i+1},\qquad
\eta_i=(-1)^{i+1}\binom{15}{i},
\]

\[
a_i=\frac{v_i+16\eta_i}{17},\qquad
\alpha_i=\frac{a_i}{v_i}.
\]

The number \(\alpha_i\) is the forced same-color proportion on relation
\(i\).

## 2. A compact exact solution

Full \(S_3\)-symmetry reduces the all-equal coordinate to

\[
t_g=q_g(\mathrm{AAA})
  =t_{\bigl(\operatorname{sort}(i,j,u),\,s\bigr)}.
\]

There are only \(885\) such coordinates.  Replacing \(z\) by each of its
\(16\) neighbors gives exact transition counts \(n_{gh}\) and the recurrence

\[
t_g+\sum_h n_{gh}t_h=\alpha_i. \tag{1}
\]

Together with one forced zero on an orbit containing an adjacent pair, these
equations have a unique rational solution.  The stored certificate contains
those \(885\) fractions.  Their numerators use at most \(24\) bits and their
denominators at most \(33\) bits.

All five coordinates are then

\[
\begin{aligned}
q_g(\mathrm{AAA})&=t_g,\\
q_g(\mathrm{AAB})&=\alpha_i-t_g,\\
q_g(\mathrm{ABA})&=\alpha_j-t_g,\\
q_g(\mathrm{ABB})&=\alpha_u-t_g,\\
q_g(\mathrm{ABC})&=1-\alpha_i-\alpha_j-\alpha_u+2t_g.
\end{aligned} \tag{2}
\]

Every value in (2) is nonnegative.  Exact substitution verifies:

1. all \(3\,876\) recurrences (1);
2. every orbit sum and equality/adjacency support zero;
3. all transposition identities;
4. all three pair marginals; and
5. every three-point local-bijection equation obtained when one selected pair
   is an edge.

No floating-point reconstruction is used by the verifier.

## 3. Every color-reduced Terwilliger block is PSD

The fixed-base triple moments decompose under the two Johnson harmonic
actions and under the color action of \(S_{17}\).  For every harmonic label
\((\ell,m)\), the verifier constructs the exact trivial and standard color
blocks using the integer coefficients

\[
2^\ell\binom{n-2\ell}{a-\ell}
\]

and the corresponding exact Johnson harmonic transition coefficients.

There are \(144\) resulting rational symmetric matrices.  The certificate
makes \(115\) of them zero and \(29\) rank-one positive semidefinite.  For
each nonzero block \(M\), the checker chooses a positive diagonal pivot
\(M_{pp}\) and verifies, entry by entry,

\[
M_{ij}M_{pp}=M_{ip}M_{pj}.
\]

This is an exact rank-one PSD certificate, not a numerical eigenvalue test.

## 4. The complete one-edge four-point extension is also feasible

Now add a fourth point \(w\) with \(w\sim z\).  A four-point variable couples
the equality pattern of \((x,y,z)\) to that of \((x,y,w)\).  The relaxation
includes:

- every exact geometric transition \(g\to h\);
- both endpoint triple marginals;
- reversal of the edge \(z\leftrightarrow w\);
- all color-pattern support zeros; and
- the exact rule that the \(16\) open neighbors of \(z\) use every color
  except \(c(z)\), once each.

After elementary elimination, the only free part is a transportation problem
between the \(\mathrm{ABA}\) and \(\mathrm{ABB}\) masses.  Scaling by

\[
L=75\,751\,275\,600
\]

makes every supply, demand, and forced lower bound integral.  There are
\(53\) positive paired-edge lower bounds; in each case a zero marginal forces
its orientation.  A deterministic integer max-flow then completes the
transport.  The verifier reconstructs every allowed four-color coupling and
checks all endpoint marginals, nonnegativity inequalities, and local
transition equations over \(\mathbb Q\).

Consequently the whole one-edge four-point extension, together with all
color-reduced Terwilliger PSD constraints, is exactly feasible.

## 5. What this proves, and what it does not

This witness proves that the following information is still insufficient to
rule out a \(17\)-coloring of \(O_{16}\):

1. all color-symmetrized triple intersection data;
2. all fixed-base Terwilliger PSD constraints on those triple moments; and
3. a separately consistent four-point lift along every single Odd-graph
   edge.

It does **not** produce a coloring of the \(300\,540\,195\) vertices of
\(O_{16}\).  It does not give a joint distribution on arbitrary quadruples,
and it does not glue the separate edge couplings into a common distribution
on five or more vertices.  Therefore it neither proves nor disproves
Erdős--Rosenfeld #835.

## 6. A concrete smallest next lift: two-neighbor gluing

The first clearly new local tensor after the present edge extension keeps a
base triple \((x,y,z)\) and chooses two distinct neighbors
\(w_1,w_2\in N(z)\):

\[
(x,y,z,w_1,w_2). \tag{3}
\]

Every neighbor of \(z\) is \(\bar z\setminus\{a\}\) for one
\(a\in\bar z\).  Hence distinct \(w_1,w_2\) satisfy

\[
|w_1\cap w_2|=14.
\]

More importantly, local bijectivity says that

\[
w\longmapsto c(w)
\]

is a bijection from \(N(z)\) to the \(16\) colors other than \(c(z)\).
Thus, for fixed \(z\), ordered distinct neighbor pairs map bijectively to
ordered distinct color pairs avoiding \(c(z)\).

Lower-dimensional consequences of this fact are already present in the
triple and one-edge four-point equations.  The genuinely new condition is
**simultaneous conditional gluing**: a five-point distribution for (3) must

1. marginalize to the already certified four-point coupling for each
   \(w_i\);
2. agree with the appropriate permuted four- and three-point marginals after
   forgetting \(x\) or \(y\); and
3. put zero mass on \(c(w_1)=c(w_2)\), conditionally on the full geometric
   and color pattern of \((x,y,z)\).

The current witness chooses the one-neighbor couplings separately, so it has
no variable on which these joint conditions can even be imposed.  This
two-neighbor tensor is therefore a precise next target: either it is
infeasible and supplies a new obstruction, or an exact feasible lift would
show that still higher gluing is necessary.

## Reproduction

The compressed data file is a zlib-compressed, Base85-encoded JSON list of
the \(885\) exact rational values.  The checker verifies its decompressed
SHA-256 digest, regenerates all geometry, and uses only the Python standard
library.

```bash
python3 evidence/verify_four_point_terwilliger_exact_witness.py
```

The decisive output begins with

```text
{'status': 'PASS', 'scope': 'necessary relaxation only; not a coloring of O_16', ...}
```

Files:

- `evidence/four_point_terwilliger_exact_witness_data.b85`
- `evidence/verify_four_point_terwilliger_exact_witness.py`
