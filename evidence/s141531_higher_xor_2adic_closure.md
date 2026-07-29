# Δ-lemma, tail collapse, and finite-window closure of the 2-adic XOR hierarchy

Date: 2026-07-26.  Status: **proved and independently computation-certified** —
companion to
`s141531_higher_xor_hierarchy.md` (which is not modified).  Verifier:
`verify_s141531_higher_xor_2adic_closure.py` (deterministic; default
mode ≈ 1–2 min runs the lemma checks and the r=9 end-to-end control;
`--window` runs the full r=15 finite-window computation).

Everything proved directly here concerns the **2-adic** conditions
(\(2^{31}\mid\) the \(a_j(D)\) numerators).  The companion
`s141531_xor_divisibility_reduction.md` proves from the forced constants that
this one family implies both \(A_j\)-integrality and \(b\mid jA_j\).

## 1. The Δ-lemma (PROVED, noncircular, sharp)

**Lemma.**  For every j ≥ 0, \(2^{15}\mid\Delta_j:=K_j(F_1)-K_j(F_0)\),
where \(F_1=F_0-2^{15}\) are the two middle-layer branch values.

*Proof.*  \(F_1\) decreases \(P\) by \(2^{14}\) and increases \(Q\) by
\(2^{14}\), so
\(-\Delta_j=[z^j](1+z)^{P-2^{14}}(1-z)^Q\bigl[(1+z)^{2^{14}}
-(1-z)^{2^{14}}\bigr]\) (the sign is irrelevant to divisibility), and
the bracket is \(2\sum_{i\text{ odd}}\binom{2^{14}}iz^i\) with
\(v_2\binom{2^{14}}i=14\) for every odd i, hence \(2^{15}\cdot\)(integer
series). ∎

This is pure Krawtchouk arithmetic — no design assumed.  It is sharp
(min \(v_2(\Delta_j)=15\) over \(j\le1200\), attained 64 times) and
reproduces the recorded \(j=3\) split: \(-\Delta_3/2^{15}=145\,938\,438\).
Consequence: the internal/external branch difference
\(a_j(D_{\rm int})-a_j(D_{\rm ext})=\mp\Delta_j/2^{15}\in\mathbb Z\) for
**every** j — that sub-family of integrality conditions is closed
unconditionally.  The same telescoping gives the general 2-adic
Lipschitz bound \(v_2\bigl(K_j(F)-K_j(F')\bigr)\ge v_2(F-F')\).

## 2. The tail-collapse reduction (PROVED, control-validated)

Notation: \(b=17\,678\,835=31\mu\), \(\mu=570\,285\); the layer
generating functions are \((1+z)^{P_w}(1-z)^{Q_w}\),
\(P_w=(b+\varphi(w))/2\).  Let \(M'=\max\) nontrivial \(|F|\); at r=15
the committed spectrum bound gives \(M'=\mu\) (note \(|F_1|=31\,219\le\mu\)).
Set \(A=(b-M')/2\).

1. **Factorization.**  Every nontrivial layer GF equals
   \((1-z^2)^{A}\,U_F(z)\) with
   \(U_F=(1+z)^{(M'+F)/2}(1-z)^{(M'-F)/2}\) of degree \(M'\); the
   Δ-correction cofactors factor identically.  The trivial layers are
   \((1+z)^b=(1-z^2)^A(1+z)^{M'}t^{A}\) and
   \((1-z)^b=(1-z^2)^A(1-z)^{M'}t^{-A}\), \(t=(1+z)/(1-z)\).
2. **Unit cancellation is initial-segment-safe.**
   \(u=(1-z^2)^{-A}\) is a triangular unit (series in \(z^2\), constant
   term 1), so multiplying the condition series by u preserves
   "coefficients \(\equiv0\bmod2^{31}\) for all \(j\le b\)" in both
   directions; no conditions leak in from \(j>b\).
3. **t-truncation.**  With \(S(z)=(1+z)^{M'}t^{A}\), the substitution
   \(z\to-z\) (which maps \(t\to t^{-1}\)) gives
   \(R_d(z)=S(z)+(-1)^dS(-z)\): off parity zero, on parity
   \([z^j]R_d=\sum_{r=0}^{29}2^{\,r+1}\binom Ar\,[z^{j-r}]
   (1+z)^{M'}(1-z)^{-r}\pmod{2^{31}}\) (the \(r\ge30\) terms carry
   \(2^{31}\)).
4. **Tail vanishing (the collapse).**  Writing
   \((1+z)^{M'}=(2-(1-z))^{M'}\), every contribution to
   \([z^n]\) with \(n>M'\) carries \(2^{M'-s}\) with \(s\le28\), and
   \(M'-s\gg31\).  Hence \([z^j]R_d\equiv0\pmod{2^{31}}\) for **all**
   \(j\ge M'+30\).  Since the polynomial part (layer cofactors plus
   parity-gated Δ-corrections) has degree \(\le M'\):

   > **Theorem (tail collapse).**  The 2-adic integrality conditions
   > hold automatically for every
   > \(j\ge M'+30=\boxed{570\,315}\).
   > The entire all-j frontier reduces to the finite window
   > \(j\le M'+29=570\,314\).

   The theorem is **noncircular**: it uses only table facts (the
   spectrum bound \(|F|\le\mu\), \(b=31\mu\), the \(2^{15}\) branch
   shift) — no block set, no dual code, no design existence.

**Two amendments discovered by the r=9 end-to-end control** (the r=9
table is complete enough to test every claim exactly, and its full
hierarchy is known to pass at all j):

- *(a) General exponent.*  The clean bound \(|F|\le b/v\) is special to
  r=15.  At r=9 the internal branch \(F_1=-454\) exceeds
  \(b/19=442\), so the correct general statement uses
  \(M'=\max\) nontrivial \(|F|\) (here \(454\)), \(A=(b-M')/2\).
- *(b) Parity gate on corrections.*  The Δ-correction cofactor enters
  as \(2\,\varphi_{\rm ext}(d)\,(U_{F_1}-U_{F_0})_j\) on parity and 0
  off parity (Theorem A's \([1+(-1)^{j+d}]\)); omitting the gate
  produces thousands of spurious violations (observed, then fixed).

With both amendments the r=9 control reproduces the exact full sweep:
8 550 on-parity conditions, **0 violations**; off-parity polynomial
part \(\equiv0\bmod2^{19}\) throughout; 3 830 automatic-tail pairs
confirmed identically zero.

## 3. Controls already in hand

- r=5 table (design exists): full exact hierarchy, all j, all layers,
  both branches — passes.
- r=9 table (design **provably nonexistent** via S(4,5,15)): same full
  exact sweep — **also passes** (0 violations, every j = 0..8398).  So
  the integrality/nonnegativity family cannot detect nonexistence at
  r=9, and any claimed "automatic integrality" theorem must be judged
  on noncircularity, not on its conclusion.

## 4. The finite window at r=15 (`--window`)

Computation: all conditions for \(0\le j\le570\,344\)
(window + collapse threshold margin), every layer \(d=0..31\), external
branch (the internal branch follows from §1).  Pipeline, all exact:

- The distinct nontrivial cofactors \(U_F\): exactly **nine** distinct
  absolute values occur (verified):
  \(\{570285, 58995, 31219, 10925, 3059, 1549, 1197, 627, 429\}\);
  negatives via \(U_{-F}(z)=U_F(-z)\).  Each \(U_{|F|}\) is one
  degree-μ convolution of the two binomial halves
  (\(\mu+1\le2^{20}\), so **NTT length \(2^{20}\)** suffices).
  Implemented with four classical primes 998244353, 754974721,
  469762049, 167772161, inputs mod \(2^{47}\): sound since the true
  coefficient bound \((\mu{+}1)(2^{47})^2<2^{113.2}\) is below the
  prime product \(\approx2^{115.5}\); 9 products × 4 primes = 36
  prime-convolutions = 108 transforms.  Leaner documented alternative:
  inputs as representatives mod \(2^{31}\), bound
  \((\mu{+}1)(2^{31}{-}1)^2<2^{81.1}\), three primes 998244353,
  1004535809, 469762049 (product \(>2^{88.6}\)): 27 prime-convolutions
  / 81 transforms.
- \(R\)-series by the prefix-sum scheme (\(A_r=A_{r-1}/(1-z)\) is a
  cumulative sum), \(O(30\mu)\).
- Assembly per layer with 16/31-bit split multiplies (no int64
  overflow), then the test \(\equiv0\bmod2^{31}\).
- **Certificates and controls**: the hardened Python verifier emits the
  full SHA-256 of every \(U_F\) coefficient vector and a certificate over
  those hashes plus every per-layer violation count.  It checks all nine
  positive and negative cofactors and the trivial residual against
  independent big-integer expansions through \(j=400\), and checks the
  uncancelled formula on five sentinel layers through \(j=400\).
  The preserved Python run predates this output-only hardening and therefore
  records 16-hex hash prefixes; its arithmetic path is unchanged.
  A second implementation,
  `verify_s141531_higher_xor_window.cpp`, independently uses coefficients
  modulo \(2^{31}\), three NTT primes, exact 128-bit CRT, paired-layer
  assembly, and `cpp_int` checks on **all 32 layers** through \(j=400\).

Python complexity: 9 cofactor products, 36 prime convolutions, 108 transforms
of length \(2^{20}\), plus \(O(30\mu)\) prefix work and vectorized layer
assembly.  The recorded Python run took 15:52.50 wall.  The independent C++
run took 38.823 seconds.

## 5. Coverage statement (exact)

- Branch-difference integrality: ALL j (Δ-lemma, §1) — closed,
  noncircular.
- 2-adic integrality, \(j\ge570\,315\): ALL such j (tail collapse,
  §2) — closed, noncircular.
- 2-adic integrality, \(j\le570\,314\): finite computation (§4);
  0..20 000 already verified by the committed sweep; the `--window`
  run covers the whole window.  Together with §2 this covers **all**
  \(0\le j\le b\).
  **Executed 2026-07-26: WINDOW VERDICT PASS** — zero violations, all
  32 layers, on- and off-parity, every \(j\le570\,344\); all three
  cross-checks green; runtime 15:52.50 wall (566.22 s user); full
  stdout and certificate preserved in
  `s141531_higher_xor_window_run_log.txt`.  **The 2-adic integrality
  family is therefore closed for every \(0\le j\le b\)**: window
  computation (\(j\le570\,314\)) + tail collapse (\(j\ge570\,315\)) +
  Δ-lemma (branch differences).  This family can never produce a
  contradiction; it is exhausted exactly as at r=9.
  The independent C++ run also passed all \(9\,125\,520\) on-parity
  conditions with zero violations; its full coefficient hashes, exact
  per-layer counts, source/build provenance, and certificate
  `1314b8cf68397219e2c1294027bef3185c5d0bd4812f2a22444d7af375c404bf`
  are preserved in `s141531_higher_xor_window_cpp_run_log.txt`.
- Nine direct large-\(j\) spot tests (50 000 … 17 600 000, both
  parities) have now reported, on fully independent machinery
  (odd-factorial tables mod \(2^{64}\); Granville factorial units per
  odd prime power of \(b=3^2\cdot5\cdot19\cdot23\cdot29\cdot31\)):
  **all nine PASS every condition** — C1 16/16 layers each,
  \(v_2(\Delta_j)\in[23,36]\) (all \(\ge15\), consistent with §1), and
  \(b\mid jA_j\) at every value (at \(j\in\{50000,12000000,
  17600000\}\) the factor \(j\) supplies a missing factor 5, i.e.
  \(b\nmid A_j\) alone there — recorded residues).  Controls: exact
  recurrence agreement at \(j=700,997\); \(\Delta_3,A_3\) reproduced;
  \(j=19999,20000\) (inside the committed sweep) PASS.  They are not
  used in the proof or in the closure claim; note the mod-b passes are
  the first data on the odd-modulus family beyond \(j=20\,000\).
  Preserved: `verify_s141531_spot_integrality.py`,
  `s141531_spot_integrality_results.txt`.  An independent root rerun passed;
  the final script and transcript SHA-256 values are respectively
  `39c83010546fce25ae25072a9de80dd3743d6ae9a74b509c7e9319a202604619`
  and `2844f216883b3010d27f98fe0ceae5d70d7a60c0cdd97877dfea2c6bbd6a88e1`.
- **Not proved inside this note**: the odd-modulus family \(b\mid jA_j\).
  It is nevertheless closed by the formal reduction in
  `s141531_xor_divisibility_reduction.md`, because condition (1) is now
  proved here.  Nonnegativity was already closed by Theorem B of the hierarchy
  note.  Thus the complete higher-XOR necessary-condition route is closed.

## 6. Scope

Nothing here bears on the existence of S(14,15,31) or on #835 except
as route closure: the two executed window runs, together with the proved
tail and branch lemmas, show that the entire 2-adic integrality family is
unable to produce a contradiction.  These necessary conditions are now
exhausted tests, exactly as at r=9.
