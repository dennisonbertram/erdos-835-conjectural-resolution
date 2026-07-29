# Operational run snapshots

These files have no mathematical weight unless explicitly stated otherwise.
They are retained because the repository records negative and inconclusive
work, not because they prove existence or nonexistence.

CaDiCaL version: `3.0.1`.

## Files

- `calib_anneal_ls2313.txt`: completed 120.1-second operational calibration,
  command
  `./anneal_ls 13 2 11 120 none 0.55 0.9999995`.
  It ended at cost 9 on the known-positive \(LS(2,3,13)\) instance.
- `calib_tabu_j12.txt`: completed 120.0-second calibration,
  command `./tabucol_johnson 12 3 11 11 120`; it ended at 11
  monochromatic edges on the known-positive \(LS(2,3,13)\) equivalent.
- `calib_tabu_j18.txt`: completed 120.0-second calibration,
  command `./tabucol_johnson 18 3 17 11 120`; it ended at 38
  monochromatic edges on the known-positive \(LS(2,3,19)\) equivalent.
- `calib_done.txt`: completion marker written after all three calibration
  commands returned.
- `j15_branches.log` and `j15_branches/verdicts.json`: completed command
  `python3 -B run_branches.py 15 4 13 runs/j15_branches 900 4`.
  All 56 branches returned `UNKNOWN(exit 0)`.  This is a complete sweep of
  the symmetry branches but is mathematically inconclusive.  Temporary branch
  CNFs were deleted by the runner.
- `j19_sat.log` and `j19_sat.model`: terminal progress plus the ten-byte
  solver output `c UNKNOWN` from the unbranched \(J(19,4)\) attempt.  They
  contain no model and no verdict.

## SHA-256 at capture

```text
2fcc483e2a1eb7d1fcf66781b927e104c6090d48552314231f1b08077d1fd210  calib_anneal_ls2313.txt
59f86150c2391e5697e8b932ef0a16a722e15931364254c7339e66180900dee3  calib_tabu_j12.txt
28b62aaf18da0cb1c0380559a7bb8d4a3e7632628832af278a456a28164b9cea  calib_tabu_j18.txt
8221ac66be71558c921fb44cfb66f7997699aea754d917763882d6d9eddc836e  calib_done.txt
e1c57491501f6e2b6203862656c97290fa63a80d7b07172ae39683e1a2047f97  j15_branches.log
10305e6f828c17f0f9d912c839b5822be33eb0fd8e419be413dd54ffc9c0aa24  j15_branches/verdicts.json
adbaac3bf7aed3452861472546db1e5b7a03bc9ce170d70f49a06859ff6be0e8  j19_sat.log
8fba55cea0f98be36fab7b65349dda867a58aabfcf974a46098f5123830ac5cb  j19_sat.model
```

The reproducible base CNFs are intentionally retained under `../cnf/`:

```text
0b1aa8f20e32c08d6d86b7bb064e89682cdf216cdd46ce9bda5ef7b0f61ee563  j15_4_m13.cnf
c75f23a838b80278b7239bd7ab1b55a8c609b9232b539df3d24c5daa86e03755  j19_4_m17.cnf
```
