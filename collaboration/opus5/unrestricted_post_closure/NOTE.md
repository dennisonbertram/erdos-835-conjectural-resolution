# SUPERSEDED — determinant (single Plücker coordinate) colourings

## Status, first

> **SUPERSEDED.** The single maximal-minor construction \(c(B)=\det(M_B)\) is
> already proved **impossible for every admissible \(k>2\), including
> \(k=16\)**, by the union of the \(p\equiv1\pmod4\), \(p\equiv3\pmod8\) and
> \(p\equiv7\pmod8\) link theorems (checkpoint item 3). Nothing in this file
> may be read as leaving that ansatz open.

**No new unrestricted progress resulted from this attempt.** What remains here
is two elementary necessary conditions and their small-\(k\) controls, kept
only because they are cheap, self-contained, and reproduce the known
impossibility at \(k=4\) by a shorter route than the mod-8 case analysis.

An earlier revision of this file wrongly stated that the \(k=16\) determinant
ansatz was open and that finding such an \(A\) would be a viable construction
route. **Both statements were false** and contradicted the checkpoint; they are
withdrawn. It also called the two conditions an "exact matrix criterion",
which they are not — see §3.

Verifier: `verify_determinant_colouring.py` (stdlib, assertion-enabled).

---

## 1. Setting

Let \(p=k+1\). A tight \(p\)-colouring of \(J(2k,k)\) is exactly a map \(c\) on
\(k\)-subsets such that for every \((k-1)\)-subset \(S\) the map
\(x\mapsto c(S\cup\{x\})\) is a bijection from the remaining \(p\) points onto
the \(p\) colours. For \(c(B)=\det(M_B)\) with \(M\) a \(k\times2k\) matrix
over \(\mathbb F_p\) this is linear in the column \(m_x\). Some \(k\) columns
must be independent, so write \(M=[\,I\mid A\,]\).

## 2. PROVED — two necessary conditions

> If \(c(B)=\det([I|A]_B)\) is a tight \(p\)-colouring then
> 1. every **row of \(A\)** is exactly \(\mathbb F_p\setminus\{1\}\), each
>    value once;
> 2. every **row of \(A^{-1}\)** is exactly \(\mathbb F_p\setminus\{1\}\).

*Proof.* (i) Take \(S=\{e_1,\dots,e_k\}\setminus\{e_r\}\); the remaining \(p\)
columns are \(e_r,a_1,\dots,a_k\) and \(\det(M_{S\cup\{x\}})=\varepsilon_r x_r\)
with \(\varepsilon_r\) depending only on \(S\). Bijectivity forces
\(\{1\}\cup\{A[r,s]:s\}=\mathbb F_p\), which is \(1+k=p\) values.
(ii) Take \(S=\{a_1,\dots,a_k\}\setminus\{a_s\}\); expanding along the last
column gives \((-1)^{k+r}m_{rs}\) for \(x=e_r\) and \((-1)^{k-s}\det A\) for
\(x=a_s\), and \(m_{rs}=(-1)^{r+s}\det(A)(A^{-1})[s,r]\) puts the common
nonzero factor \((-1)^{k+s}\det A\) on every value. Dividing it out forces
\(\{1\}\cup\{(A^{-1})[s,r]:r\}=\mathbb F_p\). \(\square\)

These are **necessary only**. They are not a criterion for the ansatz and do
not reduce it to a matrix condition.

## 3. COMPUTATION — controls, and the insufficiency

| \(k\) | tight colouring exists? | result |
|---|---|---|
| 2 | yes | ansatz realised: exactly 2 of the 81 matrices \(A\) over \(\mathbb F_3\) work, both satisfying (i)+(ii); \(A=\begin{pmatrix}0&2\\2&0\end{pmatrix}\) gives the three perfect matchings of \(K_4\) |
| 4 | no | **0 of 576** Latin squares on \(\mathbb F_5\setminus\{1\}\) satisfy (i)+(ii); 2000 random \(A\) give none |
| 6 | no | 13 of 3000 random Latin squares satisfy (i)+(ii), **none tight** |

The \(k=6\) row is the point: **(i)+(ii) are strictly weaker than the ansatz.**
Matrices pass them and still fail bijectivity, so they cannot serve as a
criterion, and no closure at \(k=6\) is claimed from them. The \(k=2\) row
confirms the conditions are not vacuous; the \(k=4\) row reproduces the known
impossibility cheaply.

## 4. What this does **not** say

* It does **not** leave the \(k=16\) determinant ansatz open. That ansatz is
  closed by the complete single-maximal-minor no-go, for every admissible
  \(k>2\).
* It does **not** offer a construction route: no matrix at \(k=16\) is worth
  searching for, because none exists.
* It does **not** claim orthogonality of \(A\) may be imposed without loss.
  Complement closure \(c(B)=c(B^c)\) is forced, and Jacobi's
  complementary-minor identity is *satisfied* when \(A\) is orthogonal — but
  that is a sufficient condition for one identity, not a proof that the
  orthogonal case is general. No reduction of the search space follows, and
  the question is moot anyway given the no-go.
* It does **not** touch ratios or tuples of Plücker coordinates. Only the
  single-coordinate case appears here.

## 5. Scope, restated

Solves #835: **no**. Proves an unrestricted theorem: **no**. Closes an
obstruction route: **no**. Contributes new unrestricted progress: **no** — the
one ansatz it examines was already closed. **Erdős–Rosenfeld #835 remains
open.**
