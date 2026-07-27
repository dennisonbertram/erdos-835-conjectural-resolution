# Two certified derived-point obstructions for EH retain-twelve repairs

## Exact result

Let \(\mathcal C_0,\ldots,\mathcal C_{14}\) be the fifteen authenticated
Etzion--Hartman SQS(20)s.  Neither of the following twelve-system families can
occur together in an \(LS(3,4,20)\):

- retain all systems except \(\mathcal C_0,\mathcal C_1,\mathcal C_5\);
- retain all systems except \(\mathcal C_0,\mathcal C_5,\mathcal C_{10}\).

These are two new portable exclusions among the 425 cases left by the exact
ten-point theorem in `collaboration/eh_core_symmetry_orbits`.  Together, the
results exclude exactly 32 of the 455 ways to retain twelve members of this
particular EH core, leaving 423.

This does **not** decide whether some unrelated \(LS(3,4,20)\) exists, and it
does not resolve Erdős--Rosenfeld Problem #835.

## Why one bad derived point is decisive

For either discarded triple, fix point \(0\).  Delete it from every block of
the five-fold leave that contains it.  The result is a
\(2\text{-}(19,3,5)\) design:

- 285 triples on the other nineteen points;
- every one of the \(\binom{19}{2}=171\) pairs lies in exactly five triples;
- its leave graph joins triples that share a pair and is 12-regular.

If the five-fold SQS(20) leave could be partitioned into five replacement
SQS(20)s, deriving those five systems at point 0 would partition these 285
triples into five STS(19)s.  Equivalently, the derived leave graph would have
a proper five-colouring.  Therefore uncolourability at this single point
rules out the entire retain-twelve repair.

## Transparent CNF

`point_link_cnf.py` emits a one-hot encoding.  Variable \(x_{B,c}\) says that
derived triple \(B\) has colour \(c\in\{0,\ldots,4\}\).

1. Every triple has exactly one colour.
2. For every point pair and every colour, exactly one of the five triples on
   that pair has that colour.
3. The colours on the lexicographically first five-triple pair-star are fixed
   to \(0,\ldots,4\).  This loses no solutions: every proper colouring can be
   globally relabelled to satisfy the five units.

Thus satisfying assignments are exactly partitions into five STS(19)s, up to
the harmless colour normalization.  Each committed instance has 1,425
variables and 12,545 clauses:

```text
drop (0,1,5), point 0:
ac8e2176860e5f2d002a29e2592c4dc009d0262e7674fb35c47d11c9467f3e6f

drop (0,5,10), point 0:
b0e0ebe97c289a9c44ff6ac48efbfecbf238d1b7f0dbfae2e934a9d6f1444654
```

Reproduce them:

```sh
python3 -B \
  collaboration/eh_point_link_screen/point_link_cnf.py \
  --drop 0,1,5 --point 0 \
  --cnf /tmp/drop_0_1_5_point_0.cnf

python3 -B \
  collaboration/eh_point_link_screen/point_link_cnf.py \
  --drop 0,5,10 --point 0 \
  --cnf /tmp/drop_0_5_10_point_0.cnf

cmp /tmp/drop_0_1_5_point_0.cnf \
  collaboration/eh_point_link_screen/drop_0_1_5_point_0.cnf

cmp /tmp/drop_0_5_10_point_0.cnf \
  collaboration/eh_point_link_screen/drop_0_5_10_point_0.cnf
```

## Independently replayed UNSAT certificate

CaDiCaL 3.0.1 generated the binary DRAT proofs.  Re-running these commands
produces the identical raw proofs on this machine:

```sh
cadical -q \
  collaboration/eh_point_link_screen/drop_0_1_5_point_0.cnf \
  /tmp/drop_0_1_5_point_0.drat

cadical -q \
  collaboration/eh_point_link_screen/drop_0_5_10_point_0.cnf \
  /tmp/drop_0_5_10_point_0.drat
```

Hashes and size:

```text
drop (0,1,5), point 0
raw bytes: 2,380,258
raw SHA-256:
06112a768e0892980bd02ffd21e2abca56324ee35c1c3d76be0ef828a12f63b9
gzip SHA-256:
648c029837933e1d4896b3342e6fc057c48540c2a7259e1a0c53e897745d9f51

drop (0,5,10), point 0
raw bytes: 5,902,433
raw SHA-256:
9831caf77ec2588cbcbb695837d82201a037f06e5d9fbd90883c8595a60528a7
gzip SHA-256:
195887f5ecebc335ecd80fae826d176b10c97f3122a38be1b896469666ad6f6b
```

The committed proofs are gzip-compressed and total approximately 4.1 MB.  They
were replayed with `drat-trim` at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  Because CaDiCaL's proof is
binary, force binary parsing when streaming it through standard input:

```sh
gzip -dc \
  collaboration/eh_point_link_screen/drop_0_1_5_point_0.drat.gz |
  drat-trim \
    collaboration/eh_point_link_screen/drop_0_1_5_point_0.cnf -i

gzip -dc \
  collaboration/eh_point_link_screen/drop_0_5_10_point_0.drat.gz |
  drat-trim \
    collaboration/eh_point_link_screen/drop_0_5_10_point_0.cnf -i
```

Both checks returned `s VERIFIED`; `VERIFICATION.txt` records the full
transcripts.  Both report 0 RAT lemmas.

The standard-library verifier independently rebuilds all fifteen source
SQS(20)s, the derived \(2\)-design, its 12-regular leave graph, and every CNF
clause.  It then checks the committed hashes and can stream the proof directly
to a supplied checker:

```sh
python3 -B \
  collaboration/eh_point_link_screen/verify_point_link_certificate.py \
  --drat-trim /path/to/drat-trim
```

## Reconnaissance beyond the certificate

`screen_point_links.py` ran CaDiCaL on all twenty derived points for drop
`(0,5,10)`.  All twenty returned the SAT-competition UNSAT return code 20, in
1.3--4.6 seconds each in the recorded run.  Those nineteen additional
statuses are deliberately labelled `UNSAT_RECONNAISSANCE`; no portable proof
for them is needed because the certified point-0 obstruction already excludes
the drop triple.

No result in this directory claims that a timeout or an uncertified solver
status is a theorem.
