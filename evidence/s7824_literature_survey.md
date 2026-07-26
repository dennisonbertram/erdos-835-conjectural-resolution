# Literature: exclusion state of the art for S(7,8,24) / S(6,7,23) / S(5,6,22) / S(4,5,21) and Erdős #835
Compiled 2026-07-26. Every item marked [V] was verified against a primary source (paper PDF read, arXiv abstract, GitHub raw file, or authoritative page). Items marked [NV] rest on secondary snippets only.

## Q1. Published work on the three exact parameter sets

**Bottom line: no existence proof, no nonexistence proof, and no exhaustive search is published for any of 7-(24,8,1), 6-(23,7,1), 5-(22,6,1).** What exists:

- [V] Michael Huber, "Steiner t-designs for large t", in: Mathematical Methods in Computer Science (MMICS 2008), Springer LNCS 5393, pp. 18–26; arXiv:0809.3117. States: no nontrivial Steiner t-design with t>5 has been constructed; proves/announces **no nontrivial flag-transitive Steiner 6-design exists** and "essentially also no block-transitive Steiner 6-design". Applies to 6-(23,7,1): its automorphism group cannot be flag- or (essentially) block-transitive.
- [V] Michael Huber, "On the existence of block-transitive combinatorial designs", Discrete Math. Theor. Comput. Sci. 12:1 (2010) 123–132; arXiv:1003.1879. Block-transitive Steiner 6-design impossible except possibly G = PΓL(2,p^e), p∈{2,3}, e odd prime. (Cameron–Praeger 1993 background: block-transitive ⟹ t ≤ 7, flag-transitive ⟹ t ≤ 6.) See also "Nonexistence of block-transitive 6-designs", Front. Math. China 2011, doi:10.1007/s11464-011-0154-5 [NV authors].
- [V] Evi Haberberger, Anton Betten, Reinhard Laue, "Isomorphism classification of t-designs with group theoretical localisation techniques applied to some Steiner quadruple systems on 20 points" (Bayreuth, May 2000; in Codes and Designs, Ohio State conf. volume). Verbatim: SQS(20) with prescribed A5 "are interesting as a step towards the search for 5-(22,6,1) designs. Since all known Steiner 4-designs are derived from Steiner 5-designs, it makes sense not to try to construct the Steiner 4-designs 4-(21,5,1) in the direct way." No existence/nonexistence claim for 5-(22,6,1).
- [V] GitHub google-deepmind/formal-conjectures issue
  [#3700](https://github.com/google-deepmind/formal-conjectures/issues/3700),
  "Steiner system S(6,7,23): four automorphism groups eliminated via
  Kramer-Mesner" (opened 2026-04-06, tied to Epoch AI FrontierMath;
  **not peer-reviewed**): M23 (trivial 3×4 KM matrix, no exact cover),
  AGL(1,23) (uncoverable row), Z23⋊Z11 (DLX, 11M nodes, UNSAT), and D23
  (divisibility-2 obstruction) eliminated.  The issue reports the Z23 case
  (4389×10648 KM matrix) as open and running under CP-SAT.
- [V] Prescribed-automorphism (Kramer–Mesner/DISCRETA, Bayreuth) constructions on the SAME point set: simple **7-(24,8,λ) designs exist for λ = 4,5,6,7,8** and 6-(24,8,λ) for λ = 36,...,72 (Bayreuth DISCRETA bibliography; cf. Betten–Laue–Wassermann, "Simple 7-designs with small parameters", J. Combin. Des. 7 (1999) 79–94 [NV details]). λ=1 never found; no published λ=1 KM search on 24 points located.
- 5-(24,8,1) = the Witt design S(5,8,24) (unique; Bergstrand 1982 among others) — different parameters, not confused here.

## Q2. No explicit Steiner t-design with t ≥ 6 is known; smallest admissible sets

- [V] No explicit example has been constructed as of 2026.  This is distinct
  from abstract existence: Keevash and later proofs establish systems for all
  sufficiently large admissible orders.  Sources for the explicit-construction
  frontier are Huber 2008 (above) and Epoch AI's FrontierMath open problem
  "Finding Small Block Designs", whose Open Subproblem 1 asks for an explicit
  \((n,q,r)\)-Steiner system with \(r>5\).
- [V] For t=5 explicit systems ARE known beyond Witt: derived S(4,5,v) exist for v = 23,35,47,71,83,107,131,167,243 from known S(5,6,v) (Östergård–Pottonen 2008, citing Colbourn–Mathon, Handbook of Combinatorial Designs, 2nd ed., 2007, Chap. II.5). The known/unknown boundary is exactly t=6.
- [V, computed + published exclusions] Admissible Steiner parameter sets (divisibility only), ascending v:
  - t=6: (7,17), (7,19), (7,23), (7,25), (7,29), (8,29), ...
  - t=7: (8,18), (8,20), (8,24), (8,26), (8,30), (9,30), ...
  Derived-tower exclusions: S(6,7,17) and S(7,8,18) die via S(4,5,15) (Mendelsohn–Hung 1972, the S(t,t+1,t+11) tower); S(6,7,19) and S(7,8,20) die via S(4,5,17) (Östergård–Pottonen 2008; their paper states verbatim: "no S(t,t+1,t+13) exists for 4 ≤ t ≤ 11; for t ≥ 12 the nonexistence was already known" — b(S(12,13,25)) non-integral).
  ⟹ **6-(23,7,1) and 7-(24,8,1) are exactly the smallest admissible parameter sets not excluded for t=6 and t=7.** (This composite statement is my computation + the two published towers; I found no single published source stating it in this form. Standard reference for open-case tables: Khosrovshahi–Laue, "t-designs with t ≥ 3", Handbook 2nd ed., Chap. II.1 [NV].)
  Same logic for t=5: (6,12) Witt, (6,16)†M-H, (6,18)†Ö-P, (6,22) open ⟹ S(5,6,22) is the smallest open t=5 set; and S(4,5,21) smallest open t=4 (k=5). The whole tower S(4,5,21)⊂S(5,6,22)⊂S(6,7,23)⊂S(7,8,24) is the tower of smallest open cases.

## Q3. Methods that ever excluded a specific design (portable mechanisms)

1. **Mendelsohn–Hung 1972** — N. S. Mendelsohn, S. H. Y. Hung, "On the Steiner systems S(3,4,14) and S(4,5,15)", Utilitas Math. 1 (1972) 5–95. Classified the (four) SQS(14) and proved no S(4,5,15) exists. [V citation via Ö-P ref list; internal proof structure NV — original paper is print-only. The standing citation chain (Ö-P [12]) confirms only the results.]
   - **The "Mendelsohn equations"** [V from Kiermaier–Pavčević]: for a t-(v,k,λ) design D and an s-subset S with intersection numbers α_j = #{B : |B∩S| = j}: for i = 0,...,t,  Σ_{j≥i} C(j,i) α_j = C(s,i) λ_i,  with λ_i = λ·C(v−i,t−i)/C(k−i,t−i). Source: N. S. Mendelsohn, "Intersection numbers of t-designs", in: Studies in Pure Mathematics (L. Mirsky, ed.), Academic Press, 1971, pp. 145–150 (S required to be a block); general S independently: W. Oberschelp, "Lotto-Garantiesysteme und Blockpläne", Math.-Phys. Semesterber. 19 (1972) 55–67. Parametrized solution ("Köhler equations"): E. Köhler, "Allgemeine Schnittzahlen in t-designs", Discrete Math. 73 (1988–89) 133–142: α_i expressed by α_{t+1},...,α_k; nonnegativity+integrality of the whole vector is the feasibility test. Higher-order version: Trung–Wu–Mesner, "High order intersection numbers of t-designs", J. Statist. Plann. Inference 56 (1996) 257–268. Modern statement + q-analog: M. Kiermaier, M. O. Pavčević, "Intersection numbers for subspace designs", J. Combin. Des. 23 (2015) 463–480, arXiv:1405.6110 (Th. 2.4 = Mendelsohn, Th. 2.6 = Köhler) [V, PDF read].
   - Concrete other exclusion by these equations: M. Dehon, "Non-existence d'un 3-design de paramètres λ=2, k=5, v=11", Discrete Math. 15 (1976) 23–25 [V citation from Kiermaier ref list].
2. **Östergård–Pottonen 2008** [V — full paper read]: P. R. J. Östergård, O. Pottonen, "There exists no Steiner system S(4,5,17)", J. Combin. Theory Ser. A 115(8) (2008) 1570–1573, doi:10.1016/j.jcta.2008.04.005. Mechanism: point set Z17; a putative S(4,5,17) represented as a list (Q16,...,Q0) of labelled derived SQS(16); "seeds" = pairs (Q16,Q15) sharing the derived STS(15) (Q16,15 = Q15,16); built on the complete classification of the 1,054,163 SQS(16) (Kaski–Östergård–Pottonen, JCTA 113 (2006) 1764–1770 — several years of CPU; the expensive step) and the 80 STS(15); 5,194,881 seeds; each seed extended to a full design as an **exact cover problem** (libexact, Knuth dancing links); all searches < 2 days; no completion ⟹ nonexistence. Two independent seed-generation algorithms; nauty for isomorphism. Prior structural input: R. H. F. Denniston, "No S(4,5,17) could have automorphisms", 6th British Combinatorial Conf., 1977 (talk). Corroborated: unique S(4,5,11), no S(4,5,15).
3. **Lam–Thiel–Swiercz 1989** [V via Wikipedia "Lam's problem" + standard]: C. W. H. Lam, L. Thiel, S. Swiercz, "The non-existence of finite projective planes of order 10", Canad. J. Math. 41 (1989) 1117–1123. Mechanism: binary code of the incidence matrix; Assmus (1970): weight enumerator fully determined by A12, A15, A16; eliminations: w15 — MacWilliams–Sloane–Thompson, JCTA 1973; w12 (ovals) — Lam–Thiel–Swiercz–McKay, Discrete Math. 1983; w16 — Lam–Thiel–Swiercz, JCTA 1986; w19 — LTS 1989 (~3 months Cray-1A) ⟹ enumerator contradiction ⟹ no plane. Independent verification with proof certificates: C. Bright, K. K. H. Cheung, B. Stevens, I. Kotsireas, V. Ganesh, "A SAT-based resolution of Lam's problem", AAAI 2021.
4. **Delsarte-LP / polynomial-method exclusions of designs ("tight designs")** [V via search snippets; standard results]: Peterson 1976 (no nontrivial tight 6-designs); Bannai 1977 (finitely many tight 2s-designs per s ≥ 5); Enomoto–Ito–Noda 1979; Bremner 1979 (the only nontrivial tight 4-design is the Witt 4-(23,7,1) and complement); Dukes–Short-Gershman, "Nonexistence results for tight block designs", J. Algebraic Combin. 38 (2013), settling s = 5..9. These exclude λ>1 designs meeting a Fisher/RCW-type bound — never a Steiner system at our parameters, but they are the genuine published precedent for "LP/eigenvalue machinery kills a design".
5. **p-rank / Smith normal form**: this survey found no published case of an
   SNF/p-rank argument excluding a Steiner system.  Usage located was as an
   invariant for classification: Zinoviev(–Zinoviev), SQS(16) of rank 14
   (Probl. Inf. Transm. 2006); P. Sin, SNF of incidence matrices (survey);
   Brouwer–van Eijl, p-ranks of SRG adjacency matrices.  This makes the route
   comparatively unexplored for these targets, not proved unprecedented.
6. **ILP/SAT at configuration level**: routine inside classification papers (and the 2021 Lam SAT verification; DLX in Ö-P); no standalone precedent for a Steiner system of strength ≥ 4 beyond Ö-P's exact-cover framework.

## Q4. Keevash / GKLO: asymptotic only — but now with an explicit constant

- [V] P. Keevash, "The existence of designs", arXiv:1401.3665 (2014): ∃ v_0(t,k,λ); no explicit bound in the paper.
- [V] S. Glock, D. Kühn, A. Lo, D. Osthus, "The existence of designs via iterative absorption", arXiv:1611.06827 (Memoirs AMS 2023): combinatorial proof, still no explicit v_0.
- [V] M. Delcourt, L. Postle, "Refined absorption: a new proof of the existence conjecture", arXiv:2402.17855 (+ expanded arXiv:2510.19978): third proof; no explicit v_0 claimed.
- [V, NEW] P. Keevash, "A short proof of the existence of designs", arXiv:2411.18291 (Nov 2024): Theorem 1.1 with an EXPLICIT threshold for K_q^r-decompositions of K_n^r (= Steiner systems S(r,q,n), λ=1): with k = C(q,r), ρ = (6k)^{-2}, α = (2q)^{-r}ρ:  **n₀ = (4q)^{90q/α} = (4q)^{90q·(2q)^r·(6C(q,r))²}**.
  For (r,q) = (7,8): exponent = 90·8·16⁷·48² = 445,302,209,249,280 ≈ 4.45×10^14, so n₀ = 32^(4.45×10^14) ≈ 10^(6.7×10^14). Utterly silent about v = 24. (The Epoch AI doc quotes this as "number of exceptions ≤ q^O(...)" and misattributes 2411.18291 to Kuperberg–Lovett–Peled; the arXiv page shows Keevash as author.)

## Q5. S(4,5,21)

- [V verbatim, Ö-P 2008]: "The next v for which existence of S(4,5,v) remains open is 21." Classification route infeasible: 11,084,874,829 STS(19) (Kaski–Östergård, Math. Comp. 73 (2004) 2075–2092).
- [V via RG snippet] E. Kolotoğlu, S. S. Magliveras, "On the possible automorphism groups of a Steiner quintuple system of order 21", J. Combin. Des. 22(12) (2014), doi:10.1002/jcd.21370: if S(4,5,21) exists then |Aut| ∈ {1,2,3,4,5,6,7,10}. Confirms S(4,5,21) is the smallest order with Steiner quintuple-system existence unknown.
- Nothing newer through mid-2026 found (multiple searches). Still open.

## Q6. Erdős #835 and connections to the tower

- [V via Lean file + Ma–Tang PDF; erdosproblems.com direct fetch 403, proxy fetch consistent] **Problem** (P. Erdős, Unsolved Problems (1974), p. 283; Bloom database #835; also credited Erdős–Rosenfeld): does there exist k > 2 such that the k-subsets of [2k] can be coloured with k+1 colours so that every (k+1)-set contains all k+1 colours among its k-subsets? Equivalent: ∃ k > 2 with χ(J(2k,k)) = k+1 (trivially k+1 ≤ χ(J(2k,k)) ≤ 2k). Status: OPEN (page updated 2026-01-22).
- A (k+1)-colouring achieving k+1 forces every colour class to be an S(k-1,k,2k) (perfect packing), i.e. equality ⟺ **large set LS(k-1,k,2k)** (k+1 disjoint systems). My computation [V]: (k-1,k,2k) is admissible exactly for k ∈ {2,4,6,10,12,16,18,22,28,...} = k with k+1 prime.
- Known cases (all χ > k+1, i.e., negative): 3 ≤ k ≤ 8 (data on A. E. Brouwer's Johnson-graphs page, aeb.win.tue.nl/graphs/Johnson.html; e.g. χ(J(8,4)) ∈ {8,9}, χ(J(12,6)) ∈ {8,9} — so in particular NO large set LS(3,4,8) or LS(5,6,12)); k = 9 (χ(J(18,9)) ≥ 11); all odd k > 2 (Johnson bound); and:
- [V, PDF read] **Jie Ma, Quanyu Tang, "A note on Erdős problem #835"** (unpublished note, github.com/QuanyuTang/erdos-problem-835, late 2025; cited on erdosproblems.com; formalized in google-deepmind/formal-conjectures FormalConjectures/ErdosProblems/835.lean): Prop. 2.1: χ(J(2k,k)) = k+1 ⟹ t | C(k+t,t-1) for all 1 ≤ t ≤ k (double count over (k−t)-subsets; colour classes give perfect K_t^(t-1)-packings of K_{k+t}^(t-1)); Thm. 2.2: **k+1 composite ⟹ χ(J(2k,k)) ≥ k+2** (Lucas' theorem); Lemma 2.3: for k+1 = p prime all these divisibilities hold — the method provably saturates.  Thus Ma–Tang's divisibility test alone leaves even \(k\) with \(k+1\) prime, beginning \(k=10,12,16,18,22,28,\ldots\).
- **Derived-tower refinement, independently posted elsewhere.**  The tower
  excludes \(k=10\), because a colour class would derive from
  \(S(9,10,20)\) to the nonexistent \(S(4,5,15)\), and excludes \(k=12\)
  through \(S(4,5,17)\).  Hence \(k=16\), whose tower reaches the open
  \(S(4,5,21)\), is the first case surviving these checks.  This is **not a
  priority claim for this project**: KentaKitamura posted the same refinement
  on the [Erdős #835 discussion thread](https://www.erdosproblems.com/forum/thread/835)
  on 2026-05-30.  This repository reached it independently and extends the
  audit, but did not establish it first.
- Related published context: T. Etzion, A. Hartman, "Towards a large set of Steiner quadruple systems", SIAM J. Discrete Math. 4 (1991) 182–195 (D(v) ≤ v−3 disjoint SQS; no large set of SQS known for any nontrivial order); T. Etzion, S. Bitan (1996), "On the chromatic number, colorings, and codes of the Johnson graph", Discrete Appl. Math.; Brouwer–Etzion 2009 [NV exact venue]. Keevash's counting machinery gives large sets for large v (survey statements [NV]).
- Recent activity around #835 / the t≥6 problem: Epoch AI FrontierMath "Finding Small Block Designs" (any Steiner system with r > 5 as an open challenge; misattributes one reference); DeepMind formal-conjectures Lean formalization (#835.lean, with Johnson-bound lemmas and the odd-k proof kernel-checked for k ≤ 300); formal-conjectures issue #3700 (S(6,7,23) KM eliminations, ongoing).

## Attack-route precedent map

| Planned route | Published precedent | Known failure/limit at our parameters |
|---|---|---|
| Intersection-equation LPs (configuration level) | Mendelsohn 1971 / Oberschelp 1972 / Köhler 1988 equations; M-H 1972 killed S(4,5,15); Dehon 1976 killed 3-(11,5,2); Trung–Wu–Mesner 1996 higher order; Kiermaier–Pavčević 2015 modern form; Ma–Tang 2025 = same style at large-set level | Plain Mendelsohn/Köhler systems are feasible at admissible parameters (they ARE the admissibility conditions at s ≤ t); Ma–Tang Lemma 2.3 proves the pure divisibility route saturates exactly when k+1 is prime — i.e., at our k=16 case. Need genuinely configuration-level (higher-order/multi-subset) refinements — no published attempt for these parameters. |
| p-rank / Smith normal form | No Steiner-system exclusion was found in this survey (invariants only: Zinoviev 2006 SQS(16) ranks; Sin SNF survey; Brouwer–van Eijl SRG p-ranks) | No precedent or recorded failure found; comparatively unexplored, not certified absent from the entire literature. |
| Coding-theoretic enumerator forcing | Plane of order 10: Assmus 1970 → MST 1973 → LTS 1983/86/89 → SAT verification (Bright et al. AAAI 2021). Witt-design uniqueness via Golay code (Bergstrand 1982) shows the 24-point coding environment is well developed | No published attempt for 7-(24,8,1)/6-(23,7,1)/5-(22,6,1). Open field. |
| Exhaustive classification via derived designs | Ö-P 2008 (S(4,5,17) via all SQS(16) + exact cover) | Explicitly declared infeasible at v=21 by Ö-P (STS(19) count 1.1×10^10). |
| Kramer–Mesner with prescribed groups | DISCRETA (Bayreuth): 7-(24,8,4..8) found; Kolotoğlu–Magliveras 2014 (Aut of S(4,5,21) ∈ {1..7,10}); formal-conjectures #3700 (4 groups killed for S(6,7,23)) | K-M only closes group-by-group; trivial-automorphism case out of reach. |
