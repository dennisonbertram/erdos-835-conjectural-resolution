# Opus 5 correction and finite-layer completion

Your second-pass conjecture \(H_\infty=(-1)^{k/2}\) is false. Independently
verified exact \(k=16\) two-sided layers now give both signs:

- XOR: \(V=\mathbb F_2^4\), \(A=V\setminus\{0\}\),
  \(\Psi(uv)=u+v\), and \(D^{ij}\) is translation by \(i+j\):
  \(H_\infty=+1\).
- Round-robin \(\Psi\), with a Bose \(STS(15)\) selecting \(D^{ij}\):
  \(H_\infty=-1\).

Read and audit:

- `collaboration/infinity_layer_theorem/README.md`
- `collaboration/infinity_layer_theorem/verify_infinity_layer_theorem.py`
- `collaboration/global_h_parity/` when its export stabilizes

The sharper theorem appears to be that \(H_\infty=\rho(\Psi)\), independent
of \(D\) but genuinely dependent on the one-factorization \(\Psi\). Reconcile
this rigorously with your \(\prod_i AT(L^{(i)})\) formula and remove the false
conjecture and false \(k=8\) evidence from `NOTE.md`.

More importantly, Priority 3 *does* have a canonical completion. For a finite
colour \(x\), put \(a_i=L_i^{-1}(x)\):

1. Complete each per-\(ij\) matching by adding
   \(\{a_i,a_j\}\).
2. Add a dummy index `*`; on edge \(i*\), use the completed \(x\)-class
   \(M_i^{-1}(x)\cup\{\{x,a_i\}\}\).
3. On a fixed \(uv\), the original dual matching holes complete by
   \(\{i_u,i_v\}\) and \(\{i_M,*\}\), with the evident degeneration when
   \(x=u\) or \(x=v\).

This produces a no-hole \(K_k\times K_k\) matching tensor for every finite
colour. The global link-sign product of every no-hole tensor is \(+1\).
Deleting the canonical added entries gives a second explicit
\(H_{\rm predicted}(L,M)\).

An independent scratch calculation has already found:

- all 11,760 \(k=6\) chart/root cases:
  \(H_{\rm predicted}=H_{\rm required}\);
- 20 random \(LS(2,3,9)\) charts, all 9 roots (180 cases): equality;
- all 17 Wallis roots: equality.

Do the heavy lifting now:

- prove the finite augmentation and no-hole tensor theorem;
- derive every deletion/cofactor sign and simplify
  \(H_{\rm predicted}(L,M)\);
- determine whether equality with formula (F) is an identity for every
  admissible chart or a new necessary condition;
- retain the stronger per-colour equations even if the total product
  collapses;
- update `NOTE.md` and the verifier, with no overclaim about #835.
