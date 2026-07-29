# Verification receipt

Run on 27 July 2026 after the independent audit corrections.

## Exact mathematics and controls

```text
python3 -B verify_star_sign.py
44/44 checks passed

python3 -B second_star_split.py
d=11: 56 branches
d=15: 176 branches

python3 -B verify_solution.py 8 3 7 controls/j8_3_m7.model
VERIFIED  LS(2,3,9) exists
```

The retained witness SHA-256 is
`40087d46ca5d166b88d4417fb89eb03747bbc245f673809bff5eca30c44de22c`.

## Static checks

```text
ruff check .
All checks passed!

ruff format --check *.py
8 files already formatted
```

Both C search helpers compiled with:

```sh
cc -O3 -std=c11 -Wall -Wextra -Werror anneal_ls.c -lm
cc -O3 -std=c11 -Wall -Wextra -Werror tabucol_johnson.c -lm
```

## Deterministic CNF regeneration

Both retained CNFs were regenerated from `g1_cnf.py` and compared byte for
byte with `cmp`.

```text
J(15,4), m=13: 17,745 variables; 498,237 clauses
0b1aa8f20e32c08d6d86b7bb064e89682cdf216cdd46ce9bda5ef7b0f61ee563

J(19,4), m=17: 65,892 variables; 2,507,788 clauses
c75f23a838b80278b7239bd7ab1b55a8c609b9232b539df3d24c5daa86e03755
```

No SAT or UNSAT verdict was obtained for either open target. The CNFs and
operational logs are research artifacts, not a resolution of #835.
