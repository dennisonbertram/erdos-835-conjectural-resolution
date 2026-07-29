# Independent root replay audit: orbit 10

Date: 2026-07-29

## Verdict

The orbit-10 deterministic certificate package passed a fresh, independent
end-to-end replay from the repository root:

```sh
DRAT_TRIM=/private/tmp/drat-trim-erdos835/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit10_fixed_pair_cnf/verify_certificates.sh
```

The command completed at `2026-07-29T12:38:24Z` with exit status zero.  This
replay was invoked independently of the processes that generated and packaged
the certificates.

## Authenticated package

The package contains 250 files, of which 235 are compressed proof artifacts.
The compressed manifest has 249 entries and SHA-256
`da010c2e0b1b1fb4ca14701f1dd3091744c684cc2c64860a0797417c257aff82`.
The raw-artifact manifest has 235 entries and SHA-256
`f708f1b3ce7ff65afa069375e33e8f18176cb59ff740fe8a416ee53bc8584ca5`.
Every compressed and reconstructed-raw hash check passed.

The frozen toolchain record has SHA-256
`3b54d551881e74c20673283fa079a9223841d5d66e4d30604da8376a7d311c91`.
The replay used upstream `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, with checker-binary SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`.

## Gates observed

The replay:

1. verified both package hash layers and all gzip streams;
2. deterministically reconstructed the merged worker results;
3. independently rebuilt all 4,124 positive capacity cuts and the exact
   526/3,598 encoded/automatic split;
4. enumerated all 570,780 labelled compatible pairs and matched the 47
   invariant buckets with the 47 components of the eight-generator action
   graph;
5. reconstructed all 47 static formulas and semantically checked all
   6,073,966 learned simultaneous-triple clauses; and
6. decompressed and independently replayed all 47 DRAT traces.

Every proof replay printed `s VERIFIED`; there were no semantic mismatches,
hash failures, or proof failures.

## Scope

This independently certifies only the orbit-10 prescribed-colour
cut-sufficiency theorem in `2026-07-28_orbit10_cut_sufficiency.md`.  It does
not certify another support orbit, coordinated nine as a whole, the later
first-lift or fan-realizability layers, or Erdős--Rosenfeld Problem #835.
