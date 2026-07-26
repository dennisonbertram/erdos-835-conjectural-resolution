# Required correction to the post-closure response

Your exported note conflicts with the checkpoint you were explicitly told to
use.

1. The single maximal-minor construction is already proved impossible for
   **every admissible \(k>2\)**, including \(k=16\), by the union of the
   \(p\equiv1\pmod4\), \(p\equiv3\pmod8\), and
   \(p\equiv7\pmod8\) link theorems.  Therefore it is false to state that
   the determinant ansatz is open at \(k=16\), or that finding such an
   \(A\) remains a viable construction route.

2. Conditions “every row of \(A\) and \(A^{-1}\) is
   \(\mathbb F_p\setminus\{1\}\)” are necessary but not sufficient, as your
   own \(k=6\) sample says.  They are not an “exact matrix criterion” and do
   not reduce the full ansatz to those conditions.

Correct `collaboration/opus5/unrestricted_post_closure/NOTE.md` and its
verifier banners/output so that:

- the artifact is explicitly marked superseded by the complete
  single-maximal-minor no-go;
- it claims only the two elementary necessary conditions and controls;
- it does not call the \(k=16\) determinant ansatz open;
- it does not imply orthogonality can be imposed without loss;
- it states that no new unrestricted progress resulted from this attempt.

Then, if you have remaining reasoning budget, inspect the independently found
two-coordinate theorem in
`collaboration/multi_plucker_construction/grassmann_line_ratio_no_go.md`.
Try to break its projective-geometric proof, especially the decoder-rigidity
step, the identification of centers, and the Segre/character bound.  Record a
line-by-line audit or exact counterexample under
`collaboration/opus5/unrestricted_post_closure/`.  Do not commit.
