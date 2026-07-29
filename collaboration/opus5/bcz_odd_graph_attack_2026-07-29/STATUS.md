# STATUS — full two-equitable-partition system on the Odd graph

**NOT SOLVED.**  Erdős--Rosenfeld #835 remains open.  No \(k\) is eliminated,
no construction is produced, and \(k=16\) is not decided.  The concrete
Bailey--Cameron--Zhou systems specialize to the projection/intertwining
identities proved here.  Ranging over all auxiliary equitable partitions is
logically equivalent to design quadrature because the singleton partition
recovers the original perfect-code equations.  This is an exact
specialization, not a proof that every strategic auxiliary partition is
vacuous.

Date 2026-07-29.  Author: Claude Opus 5.  All arguments in `PROOF.md`; routes and
boundaries in `IDEAS.md`.

---

## Source caveat — read before using this package

**The Opus author could not retrieve arXiv:2605.17376 in its session.**  `WebFetch`,
`WebSearch` and outbound `curl` were all refused by the permission layer.  It
did not see Theorem 2.3, Corollary 2.4, or systems (6)--(8) or (13).

The later independent audit retrieved the primary source and checked the exact
systems; see `INDEPENDENT_AUDIT.md`.  The specialization is valid, but several
methodological overclaims in the original Opus prose were retracted.  The
derivation below remains independent of the paper: it derives from scratch the
constraint system that a pair of equitable partitions imposes through
\((B_\pi,B_\tau,S)\).  A theorem using data outside that —
triple intersections, a normal-Cayley group algebra, or a non-equitable common
refinement — is **not** covered, and `PROOF.md` §12.3 says so explicitly.

No Python interpreter was permitted to the Opus author.  Every theorem is proved by hand;
every numerical table was computed twice by two independent routes.
The independent audit executed `verify_bcz_odd_graph.py`; all checks passed,
including every admissible \(k\le200\).

---

## Classification of every result, per the anti-overclaim rule

| # | Result | Class |
|---|---|---|
| Thm 1--3 | Intertwining \(B_\pi^{\mathsf T}S=SB_\tau\); both orders identical; specialization \((B_\pi+I)T=J\) with complete solution space \(\frac1qJ+Z\), \(\dim=\varepsilon_\pi(q-1)\) | exact symbolic specialization |
| Thm 4 | The whole system, over all \(\pi\), both orders, all families = design quadrature.  \(\pi=\){singletons} recovers \((A+I)X_\tau=J\) exactly | **restatement of design quadrature** |
| Cor 4.2 | One distance partition = design quadrature read at one vertex; all \(N\) of them = the full problem | restatement |
| Thm 5 | The projected linear equations decouple over colours apart from the zero-one partition identity | exact structural delimiter; not a proof that disjointness is invisible |
| Thm 6 / Cor 6.1 | \(\mathbf1_P\perp V_{k-1}\Rightarrow q\mid|P|\), unconditionally.  So the \(\varepsilon_\pi=0\) divisibility test can never fire, for any \(k\) | **uniform proof that a route is vacuous** |
| Thm 7 | \(q\mid\binom{2k-1-m}{k-1-j}\) for \(0\le j\le m\le k-2\) (Kummer).  Stabilizer-orbit family non-obstructive for every \(k\) | uniform vacuity (independent of Thm 6) |
| Thm 8 / 8.1 | Closed form for \(\lvert P_j\cap C_a\rvert\) in the distance partition; nonnegative integers for every admissible \(k\) | necessary but feasible constraint |
| Prop 10.1--10.3 | Gram sandwich and rank bound; both implied by design quadrature | restatement |
| **Thm 11** | Two-colour transport identity \(x_i^{a,a'}=\sum_{t\le i}[\alpha_t(a)-\alpha_{k-1-t}(a')]\) and \(0\le x_i^{a,a'}\le\alpha_i(a)\) | **new necessary condition, outside the closure** |
| Thm 11.3 | (11.2) holds at \(k=4,6,10\), all three colour cases | necessary but feasible at three \(k\) |
| **Thm 11.4** | closed form and proof that (11.2) is feasible for every admissible \(k\) | uniform closure of this scalar transport route |

Nothing in the table is an obstruction for any \(k\).  There is no uniform
obstruction and no single-\(k\) obstruction here.

---

## Answers to the five required items

1. **Specialize the system symbolically when \(M_\tau=J_q-I_q\); give the full
   solution space.**  Done: Theorem 3.  The system is the single matrix equation
   \((B_\pi+I_m)T=J_{m\times q}\) with \(T\mathbf1_q=\mathbf1_m\); its complete
   solution set is the affine space \(T=\frac1qJ+Z\) with columns of \(Z\) in
   \(\ker(B_\pi+I_m)\) and \(Z\mathbf1_q=0\), of dimension
   \(\varepsilon_\pi(q-1)\) where \(\varepsilon_\pi=\dim(U_\pi\cap V_{k-1})\).
   The column-total condition is proved automatic.

2. **Does every resulting condition follow from \(\mathbf1_{C_a}\in V_0\oplus V_{k-1}\)
   and the Steiner design equations?**  **Yes** — Theorem 4, with sharpness:
   the singleton partition turns the system back into the perfect-code condition
   itself.  For a fixed auxiliary partition, the linear equations are exactly
   a projection of those conditions.  Both orders, families of \(\pi\), joins,
   and the second-order Gram/rank conditions derived here are covered.  This
   does not prove that integrality and zero-one partition constraints for every
   proper auxiliary partition are vacuous.

3. **If not, identify the first genuinely new constraint.**  The answer to (2)
   is yes for the concrete linear systems, so §11 of `PROOF.md` steps outside them
   and constructs the cheapest condition that is not of that form — the
   two-colour transport inequality (11.2), in closed form, with both bounds
   tight somewhere.

4. **Push any new constraint to a contradiction for every admissible \(k>2\), or
   to a construction.**  **Not achieved.**  Theorem 11.4 proves that (11.2)
   holds for every admissible \(k\), including \(k=16\), so this particular
   scalar transport route is now closed.
   The two families the task named are proved non-obstructive **for every
   admissible \(k\)**, which is a negative result, not a contradiction.

5. **Small controls \(k=2,4,6\).**  Done, §9.  \(k=2\): the object exists (three
   singletons in \(K_3\)) and the machinery is consistent.  \(k=4\) and \(k=6\):
   the object provably does **not** exist (at most two disjoint Fano planes; at
   most two disjoint Witt systems, Kramer--Mesner), yet the stated stabilizer
   and distance projected systems have explicit nonnegative integer solutions.
   This demonstrates that feasibility of those projections does not imply
   existence.  It does not make the singleton system feasible; the singleton
   system is the original problem.

---

## Exact remaining gap

Unchanged from before this session: a resolution needs either an explicit
\(LS(15,16,32)\) (equivalently \(LS(14,15,31)\), equivalently a partition of
\(O_{16}=KG(31,15)\) into 17 perfect codes) or a nonexistence theorem covering
every even \(k>2\) with \(k+1\) prime.

What this package adds to the boundary: the tested stabilizer and distance
families, their elementary divisibility tests, and the scalar two-colour
distance-transport inequality are uniformly feasible.  The general BCZ
identities are projections of design quadrature; ranging through all
auxiliary partitions returns the original problem.  A useful next constraint
must therefore exploit a strategically chosen projection together with its
zero-one/integrality domain, a stronger transportation-polytope cut, or
higher-order colour coupling.

---

## Audit surface

Every claim is hand-checkable without re-deriving anything upstream.

| Claim | How to audit | Needs computation? |
|---|---|---|
| Thm 1 | compute \(X_\pi^{\mathsf T}AX_\sigma\) two ways | no |
| Thm 2 | the three forms differ by multiplication by \(D_\pi^{\pm1},D_\sigma^{\pm1}\) and transposition | no |
| Thm 3 | substitute \(TJ_q=J_{m\times q}\); kernel dimension count; \(p^{\mathsf T}\) is a left \(k\)-eigenvector so \(p^{\mathsf T}z=0\) | no |
| Thm 4 | \(\Pi_{U_\pi}\) commutes with \(A\); singleton partition has \(B_\pi=A\) | no |
| Cor 4.2 | \(\dim(V_i)^{\mathrm{Stab}(M)}=1\) and \((E_i)_{MM}>0\) | no |
| Thm 5 | Thm 3 is column-by-column | no |
| Thm 6 | Wilson's diagonal form (cited); \(\gcd(\mathrm{lcm}(1..k-1),k+1)=1\); \(W\mathbf1=q\mathbf1\) | no |
| Thm 7 | Kummer: \(k-1-j\) and \(k-m+j\) are digits in \([1,q-1]\) summing to \(\ge q\) | no |
| Thm 8 | Möbius inversion of \(\sum_j\binom ji\alpha_j=\binom{k-1}i\lambda_i\), plus \(\alpha_{k-1}=[M\in C_a]\) | no |
| Thm 8.1 | \(\binom{q-1}{s}\equiv(-1)^s\pmod q\); \(\binom ks\ge k\) for \(1\le s\le k-1\) | no |
| Prop 10.1/10.2 | \(0\preceq Y^{\mathsf T}\Pi Y\preceq Y^{\mathsf T}Y\); Cauchy--Schwarz | no |
| Thm 11 | Lemma 11.1 (neighbours of \(u\in P_i\) split by whether the deleted point is in \(M\)); \(\sigma_{a'}\) bijective | no |
| Thm 11.3 | three small tables, each row cross-checked against \(\sum_i\alpha_i=N/q\) and \(\alpha_i(1)+(q-1)\alpha_i(0)=|P_i|\) | arithmetic only |
| Thm 11.4 | telescoping identity (11.4), closed form (11.5), and three explicit slack formulas (11.6) | no |

**No theorem depends on a program.**  The standard-library exact verifier is
redundant.  The independent audit ran it with Python 3.14: 0 failures.  Part F
found no violation of (11.2) for all 45 admissible \(k\le200\), and Theorem
11.4 now proves that observation uniformly.

---

## Scope relative to the full #835

* The object studied is the covering projection \(O_k\to K_{k+1}\), i.e. a large
  set \(LS(k-2,k-1,2k-1)\).  Its equivalence with \(\chi(J(2k,k))=k+1\) is the
  committed reduction in `erdos_835_conjectural_resolution.md` §4 and is
  **assumed, not re-proved**.
* Theorems 1--5 and 10.x hold for all even \(k\ge2\) and use no primality.
  Theorems 6, 7, 8.1 additionally assume \(q=k+1\) prime, which the Ma--Tang
  obstruction already forces.
* Odd \(k\) is out of scope: \(-1\) is then not an eigenvalue of \(O_k\), so no
  such partition exists at all, as already committed upstream.
* The independent audit corrected the scope and added Theorem 11.4.  No result
  in this package settles #835.
