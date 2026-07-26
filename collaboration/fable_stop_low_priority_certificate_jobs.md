# Stop redundant small-case proof-log jobs

Free disk has fallen to 59 GB while the decisive unrestricted
radius-4-plus-trace and full \(LS(3,4,20)\) proof streams continue growing.

Please stop the still-running scratch jobs `k6_r4`, `k8_r4`, and `k8_r5`
under the old “Decide radius-5 balls at k=4,6” monitor.  Preserve their
incomplete CNF/log/DRAT files in place and report that they have no
mathematical status.  Do not stop:

- `erdos835-generic-r4-trace-cnf-cadical`;
- `erdos835-generic-r5-cadical`;
- `erdos835-ls3420-cadical-proof`;
- branch-54 CaDiCaL/Kissat;
- the generic CP-SAT forced-trace search.

The already committed \(k=4\) radius-4/radius-5 and \(k=6\) radius-5
certificates are sufficient small-case controls.  This is disk triage, not
a mathematical conclusion.
