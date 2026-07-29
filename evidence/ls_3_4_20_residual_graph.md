# Exact residual-graph reduction for \(LS(3,4,20)\)

This note concerns only the necessary \(k=16\) shadow
\(LS(3,4,20)\).  It does **not** prove or disprove its existence, and
even a positive \(LS(3,4,20)\) would not by itself solve Erdős–Rosenfeld
Problem #835.

## Proposition

Let \(\mathcal D_1,\ldots,\mathcal D_m\) be pairwise block-disjoint
\(S(3,4,20)\) systems, where \(0\leq m\leq 15\), and let \(R\) be the
set of unused 4-subsets.  Form the graph \(G_R\) on vertex set \(R\) by
joining two unused blocks when they contain a common triple.

Then:

1. every triple is contained in exactly \(17-m\) vertices of \(G_R\),
   and those vertices form a clique;
2. \(G_R\) is \(4(16-m)\)-regular;
3. the given \(m\) systems extend to a full \(LS(3,4,20)\) if and only
   if \(G_R\) has a proper \((17-m)\)-colouring.

In particular, after fifteen disjoint systems there are 570 unused
blocks, \(G_R\) is a 4-regular graph, and completion is equivalent to
bipartiteness.  If it is bipartite with \(c\) connected components, it
has exactly \(2^{c-1}\) unordered completions into the last two systems.

## Proof

A fixed triple has seventeen extensions to a 4-subset.  Each existing
Steiner system uses exactly one of them, and block-disjointness makes
those \(m\) extensions distinct.  Thus exactly \(17-m\) unused
extensions remain.  They pairwise share the fixed triple, so they form
a clique in \(G_R\).

An unused block contains four triples.  For each of them it is adjacent
to the other \(16-m\) unused extensions.  Two distinct 4-subsets share
at most one triple, so these neighbours are all distinct.  Hence its
degree is \(4(16-m)\).

If the residual blocks split into \(17-m\) further Steiner systems,
colour each block by its system.  Blocks sharing a triple receive
different colours, so this is a proper colouring of \(G_R\).
Conversely, in a proper \((17-m)\)-colouring every clique of the first
paragraph uses all \(17-m\) colours.  Therefore every colour class
contains exactly one extension of every triple and is an
\(S(3,4,20)\).  The colour classes partition \(R\), giving the desired
completion.

For \(m=15\), a proper two-colouring is exactly a bipartition.  Each
connected component has two choices for which side belongs to the
first labelled final system.  Quotienting by the global interchange of
the two final systems gives \(2^{c-1}\) unordered completions. \(\square\)

## Computational use

`search_ls_3_4_20_dls.cpp` implements this last step as an exact
bipartiteness test.  Any successful run writes a complete certificate,
which is independently checked by
`verify_ls_3_4_20_certificate.py`.  A failed randomized search is not a
nonexistence certificate.
