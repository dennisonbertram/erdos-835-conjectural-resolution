# Certified \(WW\)-switch lemma for the \(r=1\) \(K_7\) terminal

Date: 2026-07-28.

## Statement

Let \(U,S,W\) have orders \(7,5,6\), with \(S\subset W\).  Let \(D\) be
a graph on \(U\cup W\) with \(\Delta(D)\le5\), and let \(M_0,M_1\) be
edge-disjoint five-edge matchings, also edge-disjoint from \(D\).  Put
\[
F=D\cup M_0\cup M_1
\]
and assume
\[
F[U]=K_U. \tag{1}
\]
For \(s\in S\), put
\[
A_s=\{u\in U:us\in F\}.
\]
Assume \(|A_s|\le6\) for every \(s\in S\), and assume that some \(M_i\)
has an edge entirely in \(W\).

Then there are an index \(i\), a core edge \(e=uv\in M_i[U]\), and a
\(WW\)-edge \(q=pq\in M_i[W]\) such that:

1. the bipartite graph with parts \(U-\{u,v\}\) and \(S\), whose edges
   are the cross edges outside \(F\), has a perfect matching; and
2. one of
   \[
   \{up,vq\},\qquad\{uq,vp\}
   \]
   is disjoint from \(F\).

Thus a size-twelve matching may use \(e\), after which the owner of \(e\)
is repaired by replacing \(e,q\) with the two available cross edges.

The statement is deliberately stronger than the class-B application:
it does not use the six-prefix decomposition, row sums, \(|E(D)|=26\),
or the absence of a \(K_6\).

## Hall reduction

Every \(u\in U\) is incident with the six core edges in (1), while
\(d_D(u)\le5\) and each old matching contributes at most one incident
edge.  In particular, \(u\) has at most one neighbour in \(W\) through
\(F\).  Hence the sets \(A_s\) are pairwise disjoint, and every left
vertex of the residual bipartite graph has degree at least four.

For a core edge \(e=uv\), Hall's theorem says that the residual
\((U-\{u,v\},S)\) graph fails to have a perfect matching if and only if
\[
U-\{u,v\}\subseteq A_s
\]
for some \(s\in S\).  Indeed, every left vertex misses at most one
right vertex, so a proper left subset cannot violate Hall; the only
possible violation is that all five left vertices have a common missing
right vertex.

Call \(e\) **good** when no such \(s\) exists.  If \(|A_s|=5\), the
single bad edge is the complement of \(A_s\); if \(|A_s|=6\), the bad
edges form a star at the vertex outside \(A_s\); smaller classes produce
no bad edge.  Because the \(A_s\) are disjoint, the bad-edge graph has
matching number at most one.

The remaining local assertion is that some old colour which owns a
\(WW\)-edge also owns a good core edge whose two-switch is available.
The tempting argument "each endpoint misses at most one target" is not
enough by itself: both endpoints might miss the same endpoint of the
\(WW\)-edge.  The committed SAT/DRAT certificate checks exactly this
common-target exception.

## CNF semantics

The dependency-free generator creates one CNF with:

* edge variables for \(D,M_0,M_1\);
* exact size five and matching constraints for each \(M_i\);
* the degree bound \(\Delta(D)\le5\);
* pairwise edge-disjointness and (1);
* the five proper-star bounds \(|A_s|\le6\);
* the assertion that some \(M_i[W]\) is nonempty;
* exact variables for every Hall-good core edge; and
* clauses negating both orientations of every good owner two-switch.

The CNF is unsatisfiable.  CaDiCaL produces the committed DRAT proof,
and the standard DRAT-trim checker independently returns `s VERIFIED`.

## Reproduction

Generate and solve:

```sh
python3 collaboration/coordinated_nine_r1_terminal_k7_ww_sat/generate_certificate.py \
  --output /tmp/k7_ww_switch.cnf
cadical /tmp/k7_ww_switch.cnf /tmp/k7_ww_switch.drat
```

Audit the exact committed CNF and proof:

```sh
python3 collaboration/coordinated_nine_r1_terminal_k7_ww_sat/audit_certificate.py \
  --drat-trim /path/to/drat-trim
```

## Application to the terminal

For a good edge \(e=uv\), take the perfect cross matching supplied by
Hall and add \(e\); this is a perfect matching \(N\) on
\(X=U\mathbin{\dot\cup}S\).  If \(e,q\in M_i\), replace them in \(M_i\)
by the available oriented cross pair from the lemma.  Those new edges
avoid \(D\), the other old matching, and \(N\): the matching \(N\) uses
\(e\), so it uses no other edge at \(u\) or \(v\).  The repaired
\(M_i\), the untouched other old matching, and \(N\) are therefore
mutually edge-disjoint.

The excluded equality \(|A_s|=7\) is handled by the direct \(K_8\)
construction in `../coordinated_nine_r1_terminal_k7/NOTE.md`.
