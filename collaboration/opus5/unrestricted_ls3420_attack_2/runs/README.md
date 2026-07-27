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
- `j15_branches.log`: interrupted command
  `python3 -B run_branches.py 15 4 13 runs/j15_branches 900 4`.
  Exactly eight branches returned `UNKNOWN`; the remaining 48 were not
  completed. The temporary branch CNFs are ignored.
- `j19_sat.log`: empty output from an interrupted unbranched attempt and
  intentionally not staged.

## SHA-256 at capture

```text
2fcc483e2a1eb7d1fcf66781b927e104c6090d48552314231f1b08077d1fd210  calib_anneal_ls2313.txt
59f86150c2391e5697e8b932ef0a16a722e15931364254c7339e66180900dee3  calib_tabu_j12.txt
28b62aaf18da0cb1c0380559a7bb8d4a3e7632628832af278a456a28164b9cea  calib_tabu_j18.txt
8221ac66be71558c921fb44cfb66f7997699aea754d917763882d6d9eddc836e  calib_done.txt
1affe25b966899ca38d10ffdd84b89289fdb879690a2cd72a35456e2c9f84349  j15_branches.log
```

The reproducible base CNFs are intentionally retained under `../cnf/`:

```text
0b1aa8f20e32c08d6d86b7bb064e89682cdf216cdd46ce9bda5ef7b0f61ee563  j15_4_m13.cnf
c75f23a838b80278b7239bd7ab1b55a8c609b9232b539df3d24c5daa86e03755  j19_4_m17.cnf
```
