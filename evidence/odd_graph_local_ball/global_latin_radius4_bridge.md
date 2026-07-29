# Bridging the L/M/N certificate to the unrestricted generic radius-4 CNF

`../global_latin_radius4_certificate.py` constructs an exact colouring of the
radius-four ball using the coordinates in `radius4_reduction.md`.  This note
records the coordinate change which turns it into a model of the fully generic
CNF emitted by `generate_radius4_generic_sinz_cnf.py`.

The generic ball has root

\[
A=\{0,\ldots,14\},\qquad B=\{15,\ldots,30\},
\]

and lists the root neighbours `B - {15+u}` in increasing `u`.  Its normal form
sets the root colour to `0`, those sixteen colours to `1,...,16`, and then sets
the branch vertices adjacent to `B - {15}` to `2,...,16` in increasing omitted
point order.  The L/M/N construction instead has root colour `infinity=16`
and colour `u` on `B - {u}` for `u=0,...,15`.

The colour relabelling is forced:

\[
16\mapsto0,\qquad u\mapsto u+1\quad(0\le u<16).
\]

There remains the free permutation of the fifteen ground points of `A`.  For
the L/M/N golf witness, the values `L_i(0)` as `i` ranges over the fifteen
squares are exactly `1,...,15`.  Map generic point `i` to the unique L/M/N
square whose value is `L(0)=i+1`.  This makes the generic branch colour at
position `i` equal to `i+2`; it is precisely the remaining normal-form action,
not an additional restriction.  The bundled cyclic witness happens to make
this permutation the identity, but the emitter derives it rather than assuming
it.

`emit_global_latin_radius4_generic_model.py` reconstructs all 120 deterministic
`N_uv` edge-colourings, applies that ground-point and colour relabelling to
every subset in the generic BFS ball, and emits a complete assignment for all
483,681 variables.  Its Sinz auxiliary state at index `j` is true exactly when
the selected primary colour is at most `j`.

Reproduction:

```sh
python3 evidence/odd_graph_local_ball/emit_global_latin_radius4_generic_model.py \
  --model /private/tmp/er835-global-latin-radius4.model \
  --colouring /private/tmp/er835-global-latin-radius4.colouring.json \
  --manifest /private/tmp/er835-global-latin-radius4.manifest.json
python3 evidence/odd_graph_local_ball/verify_radius4_generic_sinz_model.py \
  --model /private/tmp/er835-global-latin-radius4.model
python3 evidence/odd_graph_local_ball/verify_radius4_generic_sinz_assignment.py \
  --model /private/tmp/er835-global-latin-radius4.model \
  --cnf /private/tmp/radius4-cnf-audit/instance.cnf
```

The last verifier independently reconstructs the ball and normal form, checks
the semantic local-cover property, and streams all 738,537 DIMACS clauses
without importing either construction program.  In the recorded run it checked
the canonical CNF hash

```
0e66e3d7f4e15bd155db737092b8387b10540fd0e5bbcb56127c650baf6c54dc
```

and passed.  The deterministic generated model, semantic colouring, and
manifest have SHA-256 respectively

```
522d0d69a24eb4170bb35e223e03c7f6ce1d11ca9dc65bc0b8db805d7eb23fda
91ac1623f5f89115d5f07192214dd7d5023d6735a386162b9ec8df5b22446024
168015fd88b7f04abd6c0163e4fc51aab4b10b64cd9941e07558db1331ae7a3e
```

This proves only that the complete radius-four ball around one vertex of
`O_16` has a locally bijective 17-colouring.  It does not extend the colouring
to radius five and does not resolve Erdős--Rosenfeld Problem #835.
