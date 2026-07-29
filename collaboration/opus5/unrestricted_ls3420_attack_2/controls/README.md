# Retained positive control

`j8_3_m7.model` is a complete CaDiCaL 3.0.1 model for the root-normalized
seven-colouring of \(J(8,3)\). It is not trusted as a certificate by itself:

```sh
python3 -B verify_solution.py 8 3 7 controls/j8_3_m7.model
```

reconstructs the colouring independently, checks every Johnson star, performs
the G1 lift, and checks every class of the resulting \(LS(2,3,9)\) as a
Steiner system.

SHA-256:

```text
40087d46ca5d166b88d4417fb89eb03747bbc245f673809bff5eca30c44de22c  j8_3_m7.model
```
