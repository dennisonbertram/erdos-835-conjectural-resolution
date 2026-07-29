# Opus 5 research brief

This is the substantive brief supplied to Claude Opus 5 at maximum reasoning
effort. One premise in the brief—attributing sufficiently-large
\(LS(3,4,v)\) existence to Keevash—was questioned during the run and is
explicitly corrected/scoped in `NOTE.md`. The resulting work was independently
audited; see `AUDIT.md`.

> You are Claude Opus 5 doing the heavy mathematical lifting on a persistent
> research goal: fully resolve Erdős–Rosenfeld Problem #835.
>
> Operate in the Math Problem repository. Invoke and faithfully use the
> `/efficient-frontier` skill first. Work at maximum reasoning effort. Cost is
> not a stopping condition. You may use subagents for bounded audits, but
> Opus 5 must perform the core novel reasoning.
>
> Exact target:
>
> Does there exist \(k>2\) with a \((k+1)\)-colouring of the \(k\)-subsets of
> \([2k]\) such that every \((k+1)\)-subset sees all \(k+1\) colours?
> Equivalently, does some \(k>2\) have
> \(\chi(J(2k,k))=k+1\), or \(LS(k-1,k,2k)\)?
>
> The first live candidate is \(k=16\) (\(m=17\)). A construction of the
> unrestricted \(k=16\) object solves #835. A nonexistence proof for \(k=16\)
> alone does **not** settle the existential problem, though it would be major
> progress. Do not silently replace the target with a restricted cyclic,
> equivariant, fixed-link, EH-core, finite-ball, or other ansatz.
>
> Start by reading:
>
> - `erdos_835_conjectural_resolution.md`
> - `README.md`
> - `evidence/large_set_literature_2026-07-26.md`
> - `collaboration/opus5/generic_radius4_certificate_attack/NOTE.md`
> - `collaboration/h3_generic_one_point_audit/README.md`
> - `collaboration/cyclic_lsts19_extension/README.md`
> - `collaboration/opus5/cyclic_lsts19_extension_attack/NOTE.md`
> - `collaboration/opus5/derivation_tower_obstruction/NOTE.md`
> - `evidence/solver_reconnaissance_2026-07-27.md`
>
> Important corrections you must preserve:
>
> 1. The generic one-point lift G1 is valid, including \(s=1\), for labelled
>    colour classes. It classifies each fixed-root/fixed-retained-set
>    restriction after taking the link and complementing. It does not erase
>    simultaneous compatibility across multiple roots or overlapping
>    restrictions.
> 2. \(D(10)=5\) and the \(S(4,5,11)\) packing maximum 2 are classical
>    Kramer–Mesner results, independently reproduced here. Do not claim
>    novelty.
> 3. Keep “explicit construction” distinct from existence, and verify any
>    general-existence attribution before relying on it.
> 4. An `UNKNOWN` or unfinished solver run is not mathematical evidence.
> 5. Symmetry-restricted UNSAT is not unrestricted UNSAT.
>
> Attack the actual unrestricted \(k=16/LS(3,4,20)\) frontier, prioritizing
> routes that could yield a complete construction or a rigorous unrestricted
> theorem. The independent audit identified the still-open possibility that
> simultaneous compatibility among several fixed-root/overlapping
> restrictions is stronger than any one restriction. Explore that exact
> compatibility structure, but do not assume it is the only route. Seek a
> decisive mathematical invariant, construction, lossless reduction, or
> independently certifiable finite certificate.
>
> Continuously falsify your own claims. Check small analogues and genuine
> repository objects. Search primary literature before any priority statement.
> If you obtain a construction, provide a deterministic semantic verifier. If
> you obtain nonexistence, provide a solver-independent proof or a
> certificate-producing exact pipeline and scope the theorem precisely.
>
> Write all new work only under
> `collaboration/opus5/unrestricted_ls3420_attack_2/`. Create a self-contained
> `NOTE.md` and standard-library verifiers/certificates as warranted. Do not
> edit other repository files. Do not commit or push. If a route fails, record
> the exact no-go theorem or counterexample only when it is rigorous and
> genuinely new to this repository. Do not pad the repository with
> speculation.
>
> Do not stop merely because the problem is difficult. Stop only with either:
>
> - a fully checked solution/construction;
> - a fully checked unrestricted nonexistence theorem with exact scope; or
> - after exhausting a substantial, clearly documented line of attack and
>   producing a rigorous route delimiter that materially changes the frontier.
>
> Your final report must begin with one of:
>
> - `SOLVED #835`
> - `K16 UNRESTRICTED NEGATIVE ONLY`
> - `RIGOROUS PROGRESS, #835 OPEN`
> - `NO NEW RIGOROUS PROGRESS, #835 OPEN`
>
> Never say “solved” unless the complete existential problem is actually
> resolved.
