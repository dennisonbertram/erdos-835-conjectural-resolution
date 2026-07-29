# Line-by-line audit: `grassmann_line_ratio_no_go.md`

**Verdict: I could not break it. Every step I checked is correct, including
the three you flagged.** No counterexample found. Its stated scope is also
accurate — it excludes one two-coordinate family and does not touch #835.

Independent census below; the finite-geometry numbers reproduce exactly.

## Decoder rigidity — CORRECT

* \(h\) restricted to the occurring ratio values is a surjection from a
  \((p+1)\)-set onto \(p\) colours, so fibre sizes sum to \(p+1\) over \(p\)
  nonempty fibres: exactly one double fibre \(\{\alpha,\beta\}\), rest
  singletons. ✓
* At a link vertex \(i\) the \(p\) incident edges are the \(p\) extensions of
  the \((k-1)\)-star \(R\cup\{i\}\) (\(|R|=k-2\), \(|X\setminus\{i\}|=p\)), so
  properness makes their ratios pairwise distinct — \(p\) of the \(p+1\)
  values, missing exactly one. If both \(\alpha,\beta\) occurred, two edges
  would share a colour; so exactly one does, and all \(p-1\) singletons occur
  exactly once each. ✓
* Hence each singleton class is a perfect matching of \(K_{p+1}\) — and
  \(p+1\) is even, so this is consistent. ✓

## Identification of the centres — CORRECT

* By (9), \(\eta_\lambda(i,j)=0\iff Z_i,Z_j,N_\lambda\) collinear, so the
  \(\lambda\)-class is the set of oval pairs on lines through \(N_\lambda\).
  A perfect matching means every oval point is paired, so **no tangent passes
  through \(N_\lambda\)** — i.e. \(N_\lambda\) is internal. ✓
* The \(p-1\) singleton parameters give \(p-1\) **distinct** points of the one
  line \(L\), since \(\lambda\mapsto N_\lambda\) is a bijection onto \(L\). ✓
* The "\(N_\lambda\) lies on a chord" step is right: if not, all \(p+1\) lines
  through \(N_\lambda\) meet \(\mathcal O\) in \(\le1\) point, and \(|\mathcal O|=p+1\)
  forces exactly one each, making \(\mathcal O\cup\{N_\lambda\}\) a
  \((p+2)\)-arc. Verified \(p+2\) odd for \(p=3,5,17\), so the pairing argument
  applies. ✓

## Segre / character bound — CORRECT, and reproduced exactly

Independent enumeration of \(\mathrm{PG}(2,p)\), conic \(Y^2-XZ\), internal =
discriminant a nonsquare:

| \(p\) | points | conic | internal | internal per line by #conic points | max | \(p-1\) | contradiction |
|---|---|---|---|---|---|---|---|
| 3 | 13 | 4 | 3 | tangent 0, secant 1, external 2 | 2 | 2 | **no** |
| 5 | 31 | 6 | 10 | 0 / 2 / 3 | 3 | 4 | yes |
| 17 | 307 | 18 | 136 | 0 / 8 / 9 | **9** | **16** | yes |

The census \(0,\;(p-1)/2,\;(p+1)/2\) for tangent / secant / external lines is
confirmed, as are \(|\mathrm{Int}|=p(p-1)/2\) and \(|\mathrm{Ext}|=p(p+1)/2\).
At \(p=17\) the required 16 internal points on one line versus the maximum 9 is
exactly the contradiction claimed.

**The \(p=3\) boundary is genuine and correctly handled**: there \(p-1=(p+1)/2=2\)
and no contradiction arises — which it must not, since \(k=2\) does admit a
tight colouring. That is a real control, and the argument passes it.

## Other steps I checked

* §3's \(0=(A+B)\wedge(A+B)=2A\wedge B\) needs \(p\) odd (used) and gives
  \(\dim W=3\); \(\dim W\ge3\) because \(A,B\) are independent. ✓
* \(\bigwedge^2W\cong W^*\otimes\det W\) for \(\dim W=3\) justifies (9). ✓
* \(Z_i\ne0\) and \(Z_i\ne Z_j\), and no two oval points on \(L\), all follow
  from the standing hypothesis \((P,Q)\ne(0,0)\). ✓
* Ovality: three collinear \(Z\)'s on \(M\ne L\) put \(M\cap L=N_\lambda\) and
  give two equal ratios at a shared vertex. ✓
* **Sign check on the contraction.** \(\iota_R\omega_\lambda(e_i,e_j)=\pm\omega_\lambda(e_R,e_i,e_j)\),
  and the reordering sign depends only on \((R,S)\), *not* on which of
  \(\omega_0,\omega_1\) is contracted. So both coordinates pick up the same
  sign and the **ratio is unaffected**. This is the one place a sign slip could
  have mattered, and it does not.

## Attempts to break it that failed

* Looking for a decoder with two double fibres — impossible by the
  \((p+1)\to p\) count once all \(p+1\) values are shown to occur.
* Looking for a link where fewer than \(p+1\) ratio values occur — blocked by
  the arc bound.
* Looking for a sign inconsistency in (9) — the contraction sign cancels in the
  ratio, as above.
* Looking for a rank-4 escape at some \(R\) — impossible for this family, since
  the *whole pencil* \(\theta\wedge(ax+by)\) is decomposable, so every
  contraction has rank \(\le2\).

## Scope check

The note's own scope statement is accurate. It excludes only the shared-\((k-1)\)-row
two-minor ratio family (a line **inside** the Grassmannian), leaves two
unrelated minors, affine pairs retaining scale, and \(\ge3\) coordinates
untouched, and is not a resolution of #835. **Erdős–Rosenfeld #835 remains
open.**
