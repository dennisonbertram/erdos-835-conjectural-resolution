# Independent root replay audit: orbit 11

Date: 2026-07-29

## Verdict

The orbit-11 deterministic certificate package passed a fresh, independent
end-to-end replay from the repository root:

```sh
DRAT_TRIM=/private/tmp/drat-trim-erdos835/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit11_fixed_pair_cnf/verify_certificates.sh
```

The command completed at `2026-07-29T12:59:18Z` with exit status zero. This
replay was invoked independently of the processes that generated and packaged
the certificates.

## Authenticated package

The package contains 484 files, of which 465 are compressed proof artifacts,
and has exact size 648,908,902 bytes. The compressed manifest has 483 entries
and SHA-256
`52cc4b198db5191270c501c248656789ff58b4899bafe2af886a0fac73cd8ee2`.
The raw-artifact manifest has 465 entries and SHA-256
`8245fb8e599b59399ef3a5e53a6e9b456f7007ce53e7944255d4c5901d7a3e8c`.
Every compressed and reconstructed-raw hash check passed.

The frozen toolchain record has SHA-256
`b5f354062877756e4c6eaef01e0cc33e96aadbcabefe3f0bfc0ccb51f69ebc50`.
The replay used upstream `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, with checker-binary SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`.

## Gates observed

The replay:

1. verified all 483 package hashes, all 465 gzip streams, and all 465
   reconstructed-raw hashes;
2. deterministically reconstructed the merged worker results;
3. independently rebuilt all 4,325 positive capacity cuts and the exact
   538/3,787 encoded/automatic split;
4. enumerated all 570,780 labelled compatible pairs and matched the 93
   invariant buckets with the 93 components of the eight-generator action
   graph;
5. reconstructed all 93 static formulas and semantically checked all
   11,441,006 learned simultaneous-triple clauses; and
6. decompressed and independently replayed all 93 DRAT traces.

Every proof replay printed `s VERIFIED`; there were no semantic mismatches,
hash failures, or proof failures.

## Scope

This independently certifies only the orbit-11 prescribed-colour
cut-sufficiency theorem in `2026-07-28_orbit11_cut_sufficiency.md`. It does
not certify another support orbit, coordinated nine as a whole, the later
first-lift or fan-realizability layers, or Erdős--Rosenfeld Problem #835.
