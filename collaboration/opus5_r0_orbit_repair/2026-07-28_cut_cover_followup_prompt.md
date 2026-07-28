# Claude Opus 5 max: audit the residual obstruction-cut covering

Work tool-free and independently.  Return at most 20,000 tokens.  Give a
complete proof, a completely explicit counterexample, or the earliest exact
gap.  Every claimed overlap or coverage inequality must be derived.

## Setting

Use the full \(r=0\) class-B setting:

- \(D\) is the union of six edge-disjoint prefix matchings of sizes
  \(4,4,4,5,5,5\);
- \(|D|=27\) and \(1\le d_D(v)\le5\);
- seven triple rows and four five-set rows satisfy
  \(\rho(v)=d_D(v)-1\);
- \(G=K_{13}-D\).

For a cut \(U\), write
\[
A_U=\{R\text{ among the seven triple rows}:R\subseteq V\setminus U\}
\]
and
\[
B_U=\{R:|R\cap U|=1\}.
\]

We seek three triple occurrences satisfying all capacity cuts.  Assume the
individual blockers have been repaired and the selected candidates must be
pairwise compatible.

## Audited obstruction types

Only the following cuts can create a genuinely three-way failure:

1. \(|U|=6,\ e(G[U])=2\): the selected three rows all lie in \(A_U\).
2. \(|U|=7,\ e(G[U])=4\): either all three lie in \(A_U\), or two lie in
   \(A_U\) and the third lies in \(B_U\).
3. \(|U|=7,\ e(G[U])=5\): all three lie in \(A_U\).
4. \(|U|=8,\ e(G[U])=8\): all three rows lie in the complementary five-set.

The row budget gives respectively
\[
|A_U|\le7,\quad |A_U|\le4,\quad |A_U|\le5,\quad |A_U|\le3.
\]
There is at most one tight eight-set.

The branch \(|U|=6,\ |A_U|=7\) is already proved: one legal cross-switch
makes every row triple cut-feasible.  Do not re-prove it.

## Primary target

Audit and settle the next claimed branch.

> Suppose a six-set \(U_0\) has \(e(G[U_0])=2\) and
> \(|A_{U_0}|=6\), with missing row occurrence \(R_p\).  Prove that some
> triple \(\{R_p,R_x,R_y\}\), \(R_x,R_y\in A_{U_0}\), survives every
> obstruction cut, or give a full class-B counterexample.

A previous response asserted but did not prove:

\[
3|A_{U_1}\cap A_{U_2}|
\le (|U_1\cap U_2|-1)^2
\]
for two dense six-set cuts, several uniqueness statements for partners
meeting in four, five, or six vertices, and a reduction of the remaining
15 pairs \(\{x,y\}\) to unions of \(K_4\)'s, \(K_3\)'s, and at most one
edge.  Re-derive each statement from the actual row incidences, edge counts,
and degree cap.  If any is false, retract it and give a counterconfiguration
or the corrected bound.

## Secondary target

If the \(|A|=6\) branch closes, attack the residual covering problem in which
every obstruction cut has \(|A_U|\le5\).  Determine whether mixed
\(5+5+4+4+\cdots\) cut families can cover all 35 row triples while remaining
realisable by one \(D\) and one full row inventory.

Return:

1. exact verdict on the \(|A|=6\) branch;
2. complete derivations or explicit counterexample;
3. exact verdict on the \(|A|\le5\) residual;
4. earliest remaining gap without optimism inflation.
