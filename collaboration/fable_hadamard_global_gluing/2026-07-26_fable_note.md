# Global \(I+J\) frame gluing: a finite coset-CSP reformulation

Date: 2026-07-26. Labels: **PROVED / ATTEMPTED COMPUTATION / OPEN**.
Context: the deleted-colour Hadamard-kernel theorem, its frame
reformulation, and the established facts that linear rank gives no capacity
bound and the clique corollary is vacuous. No symmetry or classified
\(S(4,5,21)\) is assumed.

## 1. PROVED — gauge reduction to a finite coset CSP

Each deleted star is an \(I+J\)-Gram spanning frame of the same
nondegenerate space \((U,b)\), with the single relation
\(\sum v=0\). Consequently:

1. **All local frames are isometric.** The Gram matrix
   \(I+J_{p-1}\), together with its one-dimensional sum-zero kernel,
   determines the spanning frame up to \(O(b)\). One base star may therefore
   be fixed.
2. **Only shared-vector synchronization remains.** For every star \(B\),
   choose an isometry \(g_B\in O(b)\) carrying a fixed standard simplex to
   its local frame. If two stars share a nondeleted block \(S\), the two
   marked standard-frame vectors representing \(S\) must have the same image
   under \(g_B\) and \(g_{B'}\). If their union block lies in the deleted
   design \(D\), there is no shared evaluation vector.

Conversely, any collection of local isometries satisfying all these
shared-vector equalities assigns one well-defined vector \(v_S\) to every
nondeleted block. Every star then has Gram \(I+J\) and zero sum. Defining
\(x(S)=b(v_S,x)\) embeds \(U\) into \(\ker M_D\), and the local frame-operator
identity gives
\[
 M_D(x\circ y)=b(x,y)\mathbf1.
\]
Thus the required quadratic space exists if and only if this finite
orthogonal-group coset constraint problem is feasible.

The overlap graph has many cycles, especially inside pencils through a
\((k-2)\)-set. Products of permitted transition cosets around those cycles
are a natural place to seek an obstruction. This note does **not** reduce the
nonabelian coset CSP to one defined cohomology or holonomy class; that further
reduction remains open.

## 2. PROVED — interpretation of the controls

At \(k=2\) the coset CSP is feasible. At \(k=4\) it is infeasible: the parent
verifier completely enumerates the relevant projective lines and proves
capacity \(1<3\). At \(k=6\), prior work exhausts only the design-valued
sector; it does not decide the full quadratic frame CSP.

## 3. ATTEMPTED COMPUTATION — no \(k=6\) verdict

A delegated Fable subagent was asked to decide the full \(k=6\) CSP for a
Witt \(S(5,6,12)\) zero class over \(\mathbb F_7\). The task terminated when
the connected Fable account reached its monthly spend limit. It produced no
witness, no infeasibility certificate, and no verifier.

The initial draft also misstated the model size as 660 blocks. The correct
numbers are
\[
 \binom{12}{6}=924,\qquad |D|=132,\qquad
 |X\setminus D|=792.
\]
No reduction from 792 to 660 variables was proved. Therefore the attempted
computation has **no mathematical status** and must not be cited as a
decision of the full \(k=6\) relaxation.

## 4. OPEN — the \(k=16\) statement

At the \(LS(4,5,21)\) layer, the unresolved question is whether the coset CSP
is infeasible for every possible \(S(4,5,21)\) zero class. A hypothetical
top \(S(15,16,32)\) colour class would produce one such derived zero class,
but the converse lifting implication is not asserted. A universal negative
must cover every zero class that could occur in a derived large set.

## 5. Scope

The proved contribution is the exact finite coset-CSP equivalence and the
identification of pencil cycles as a possible next target. The attempted
\(k=6\) decision failed operationally and proves nothing. Neither \(k=16\)
nor Erdős--Rosenfeld Problem #835 is resolved.
