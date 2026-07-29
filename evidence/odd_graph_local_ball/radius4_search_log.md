# Radius-4 construction search log

Status as of 2026-07-24: **UNKNOWN**.  No run in this file is an
infeasibility result and no radius-4 witness has yet been found.

> **Update, 2026-07-26.**  This historical status has been superseded:
> [`global_latin_radius4_bridge.md`](global_latin_radius4_bridge.md)
> gives a deterministic radius-four witness and an independently checked
> complete assignment for the unrestricted generic CNF.  Thus the radius-four
> instance is **SAT**.  The bounded runs below remain useful only as a record
> of the earlier restricted search; the unresolved local frontier is radius
> five.

The searched ansatz is
\[
L_i(u)=u\mathbin{\mathtt{XOR}}i
\]
on \(\mathbb F_2^4\), with the \(\infty\)-coloured edges of \(M_i\)
fixed to the translation matching
\(\{\{u,u+i\}:u\in\mathbb F_2^4\}\).  This is a restricted
construction family, not a without-loss-of-generality specialization
of every radius-4 colouring.

## CP-SAT runs

The unanchored ansatz ran for 600 seconds:

| status | branches | conflicts |
|---|---:|---:|
| `UNKNOWN` | 13,738,257 | 1,499,695 |

Within this ansatz, a linear relabelling may fix
\[
M_2(\{0,1\})=4.
\]
After that normalization, the stabilizer has five orbits on the allowed
value of \(M_1(\{0,2\})\), represented by \(4,5,6,7,8\).  Each branch
was run for 180 seconds with eight workers:

| second anchor | status | branches | conflicts |
|---:|---|---:|---:|
| 4 | `UNKNOWN` | 3,242,687 | 547,350 |
| 5 | `UNKNOWN` | 21,650,412 | 1,222,098 |
| 6 | `UNKNOWN` | 32,707,227 | 1,873,053 |
| 7 | `UNKNOWN` | 13,118,575 | 1,275,619 |
| 8 | `UNKNOWN` | 417,005 | 54 |

The first anchor is without loss inside the ansatz because, at
\(\{0,1\}\), any chosen index \(i\ne1\) and its colour \(c=M_i(01)\)
satisfy \(c\notin\operatorname{span}\{1,i\}\).  A member of
\(GL(4,2)\) can send the independent triple \((1,i,c)\) to
\((1,2,4)\).  The five second-anchor representatives are the orbits of
the remaining stabilizer on the allowed value.

`UNKNOWN` means only that the time bound expired.  In particular, the
five-row table is not a proof that the ansatz is impossible.

## Independent SAT encoding

`search_radius4_sat.py` expresses the same exact-one conditions as a CNF
with 23,640 variables and 581,882 clauses.  It is intended to run the
five residual branches under independent PySAT backends and then pass
any witness through the same \(L/M/N\) and 14,657-vertex ball verifier.
Its outcomes must be appended here only after the solver processes
return.

The first bounded SAT wave returned:

| second anchor | backend | status | conflicts | decisions | propagations |
|---:|---|---|---:|---:|---:|
| 6 | MapleChrono | `UNKNOWN` | 3,595,581 | 8,750,368 | 753,450,071 |
| 7 | Glucose 4.2 | `UNKNOWN` | 3,613,993 | 43,147,668 | 754,250,532 |
| 8 | MapleSAT | `UNKNOWN` | 4,163,646 | 29,632,474 | backend reported 0 |

Each ran for 600 seconds.  CaDiCaL and Kissat branches 4 and 5 were
manually interrupted after their PySAT bindings revealed that they do
not implement the requested interrupt operation; they provide no
bounded solver status and are not counted as mathematical outcomes.
The script now exposes only the three backends above, whose interrupt
support was exercised successfully.
