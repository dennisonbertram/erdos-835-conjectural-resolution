# Opus 5 follow-up: decide the full shared-\(N\) sign

The corrected state is now committed at `d291215`.

Read:

- `evidence/odd_graph_local_ball/partial_fiber_sign_head.md`
- `evidence/odd_graph_local_ball/flag_at_exact_formula.md`
- `evidence/odd_graph_local_ball/radius4_dual_trace_forced.md`
- `evidence/odd_graph_local_ball/radius5_minimal_trace_forced.md`

We now know, for every even-\(k\) admissible chart,
\[
E(L,M)=1,\qquad
H_{\rm observed}=(-1)^{k(k-1)/2}\operatorname{AT}(T)
                  \prod_i\delta(S_i)
\]
on any genuine radius-5 extension.  The one-sided cyclic-\(k=6\) controls
show only that separate \(ij\)-slices do not determine individual fiber
signs; they do not decide the full shared table.

Do the heavy lifting on the real remaining head:

1. Treat a colour-\(x\) \(N\)-layer as a family of selected squares in
   \(K_A\square K_V\).  Express the product of all vertex-link
   partial-bijection signs by regrouping the same oriented incidences
   first per \(ij\), then per \(uv\).  Track every deleted row/column
   cofactor.
2. Determine whether full two-sided compatibility forces
   \(H_{\rm observed}\) to a universal constant, to a second explicit
   function of \(L,M\), or leaves both signs possible.
3. Build the smallest exact jointly compatible synthetic models if a
   theorem is unclear.  A countermodel must state every satisfied and
   omitted condition.  Do not use nonexistent \(k=6\) radius-5 objects.
4. Check whether changing the root vertex or distinguished root colour
   couples the sign equations strongly enough to exclude every
   \(k=16\) chart, not merely Wallis.

Export a proof/countermodel note and assertion-enabled stdlib verifier under
`collaboration/opus5/full_n_sign/`.  Keep `H_required` and `H_observed`
separate.  No #835 solution claim without an unrestricted theorem or
construction.
