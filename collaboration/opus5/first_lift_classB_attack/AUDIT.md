# Import and claim audit

Date: 2026-07-27.

This directory preserves Claude Opus 5's class-B attack, including its source,
certificates, prompt, run log, and raw solver/search logs. Generated Mach-O
binaries were excluded because they are reproducible from `BUILD.md` and are
not portable.

`NOTE.md` and the current `verify_classB.py` are the authoritative statements
of scope. The historical files `logs/verify_final.out` and
`logs/verify_final2.out` contain an overbroad status line saying that one
parity obstruction is invisible to "every linear relaxation." The verified
claim is narrower: the stored instance has a strict point in the specific
fractional completion relaxation defined in `lp.py`. The raw logs are retained
unchanged as provenance.

No secrets or credentials were found by a case-insensitive scan for API keys,
passwords, bearer headers, GitHub tokens, or common token prefixes.

The imported package was rebuilt and replayed from this directory on
2026-07-27. `cbsearch11.c` was compiled locally and the generated binary was
removed after use. `python3 -B verify_classB.py` exited 0 and reported all
twelve sections `PASS`, including the exact BC threshold table, 1,200
small-instance necessity controls, independent DFS/CDCL/C-solver agreement,
the complete small-pair enumerations, and all 9,418,500 target parity checks.

The package does **not** prove completion of every target class-B instance and
does **not** settle Erdős--Rosenfeld Problem #835.
