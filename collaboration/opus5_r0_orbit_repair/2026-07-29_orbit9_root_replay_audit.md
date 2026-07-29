# Independent root replay audit: orbit 9

Date: 2026-07-29

## Verdict

The committed-form orbit-9 certificate package passed a fresh, independent
end-to-end replay from the repository root.  The replay command exited with
status zero:

```sh
DRAT_TRIM=/private/tmp/drat-trim-erdos835/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit9_fixed_pair_cnf/verify_certificates.sh
```

The run completed at `2026-07-29T12:20:43Z`.  It was invoked independently of
the process that generated and packaged the certificates.

## Gates observed

The replay:

1. authenticated the compressed package against `MANIFEST.sha256`;
2. checked all 435 gzip streams;
3. authenticated the reconstructed raw artifacts against
   `RAW_MANIFEST.sha256`;
4. deterministically reconstructed the merged worker results;
5. reran the independent semantic verifier, including all 87 static formulas,
   all 627,900 labelled compatible pairs, all 87 components of the
   seven-generator action graph, and all 13,734,283 learned clauses; and
6. decompressed and independently replayed all 87 DRAT traces with upstream
   `drat-trim`.

Every DRAT replay printed `s VERIFIED`; the aggregate replay reported zero
failures and exited with status zero.  The checker binary used in this replay
had SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`,
matching the frozen toolchain record.

The package-level aggregate is preserved in
`2026-07-28_orbit9_package_replay.json`.  It records 455 package files, 435
compressed artifacts, 749,187,194 logical bytes, zero gzip failures, zero raw
hash failures, 87 fresh proof replays, and exit status zero.

## Scope

This independently certifies the orbit-9 prescribed-colour cut-sufficiency
theorem stated in `2026-07-28_orbit9_cut_sufficiency.md`.  It does not certify
another support orbit, the complete coordinated-nine theorem, any later
first-lift or fan-realizability layer, or Erdős--Rosenfeld Problem #835.
