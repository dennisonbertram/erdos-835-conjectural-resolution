# Independent check of the deleted-colour Hadamard-kernel theorem, and the k=16 layer determinations

Date: 2026-07-26.  Labels: **PROVED / COMPUTATION / OPEN**.  Scripts in
this directory: `verify_layer_capacity_facts.py` (passes).  The parent
verifier `collaboration/hadamard_kernel_attack/verify_hadamard_kernel_attack.py`
was re-run: recorded output reproduced exactly (k=2 and k=4 controls;
`ALL ... CHECKS PASSED`).

## 1. Independent verification of the theorem (PROVED — audit clean)

Every step of the deleted-colour Hadamard-kernel theorem checks:
(1) the per-star power sums give \(W(g^{\circ m})=0\) for
\(1\le m\le p-2\) and \(-\mathbf1\) at \(m=p-1\) (full-field power
sums); the zero class is an \(S(k-1,k,2k)\); the D-columns contribute
\(0^r=0\), so \(u_r=g^{\circ r}\) lies in \(\ker M_D\) for
\(r\le p-2\); the \(u_r\) are independent because \(z\mapsto z^r\) are
independent on \(\mathbb F_p^\*\) and \(g\) is surjective onto
\(\mathbb F_p^\*\) off \(D\); the product rule (6) follows from
exponent reduction mod \(p-1\) with the reduced exponent in
\([1,p-3]\); and the scalar form is the anti-diagonal \(-1\) matrix,
nondegenerate.  The Newton-identity converse (star polynomial
\(T^p-T\)) also checks.  No gaps found.

## 2. Determination (a): repeated derivation (PROVED — yes)

The derived \(LS(4,5,21)\) (or \(LS(3,4,20)\)) layer of a hypothetical
\(k=16\) colouring is again a tight \(p\)-colouring of the same
combinatorial shape: every 4-star (resp. 3-star) has exactly
\(p=17\) blocks, one per colour.  The theorem's proof uses only that
shape, so it applies verbatim: the derived layer carries a forced
\(U\) of full dimension \(p-2=15\) inside \(\ker M_D\) with
\(\Phi_D(U,U)=0\) and the **same nondegenerate anti-diagonal scalar
pairing**.  Repeated derivation loses neither the dimension nor the
nondegeneracy — the quadratic space descends intact to the smallest
layer.

## 3. Determination (c): modular inclusion rank (PROVED — no bound)

The Wilson diagonal entries of \(W_{4,5}(21)\) are \(5,4,3,2,1\) and
of \(W_{3,4}(20)\) are \(4,3,2,1\) — all coprime to 17.  Hence both
inclusion matrices have **full** rank mod 17 (5,985 resp. 1,140), and
for **every possible** member \(D\),
\(\dim\ker M_D\ge19{,}152-5{,}985=13{,}167\) (resp.
\(4{,}560-1{,}140=3{,}420\)) — vastly above 15
(`verify_layer_capacity_facts.py`).  The modular inclusion-matrix rank
therefore yields **no universal capacity bound at any derived layer**:
any impossibility proof must use the quadratic structure, not linear
rank.

## 4. Determination (b): local \(I+J\) simplex frames (OPEN, structure derived)

Before deleting \(D\), two 4-stars whose defining sets meet in three
points share exactly the one block \(B\cup B'\) (verified).  In the
deleted incidence structure their frames share that evaluation vector
when \(B\cup B'\notin D\), and share no vector when
\(B\cup B'\in D\).  Thus the forced structure is a coherent system of
\((p-2)\)-dimensional \(I+J\)-Gram simplex frames, one per star, glued
along at most one shared evaluation vector over the 4-set/5-set incidence
geometry.  A single shared vector between two frames is not locally
contradictory; whether the **global** gluing over all \(\binom{21}4\)
stars is impossible for every possible \(S(4,5,21)\) zero class is the
genuine open question, and by §3 it cannot be settled by rank counting.
The k=4 control
(capacity 1 < required 3, complete projective enumeration) shows the
quadratic obstruction is real at small parameters; the k=6
design-sector control is exhausted but its full quadratic relaxation
is explicitly not closed.

## 5. Verdict and scope

The theorem is verified; the quadratic space descends to the
\(LS(4,5,21)\)/\(LS(3,4,20)\) layers at full strength (a); no linear
capacity bound exists (c); the decisive global-gluing question (b)
remains **OPEN** — no member of any layer has been shown incapable of
supporting the space, and no universal negative theorem is proved.
Computation was treated only as computation; no classified or
symmetric Steiner system was assumed.  **Neither k=16 nor
Erdős–Rosenfeld #835 is resolved here.**
