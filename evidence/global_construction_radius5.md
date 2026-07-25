# A staged radius-five construction route from the cyclic golf chart

This is a constructive route toward, but not a claim of, a cover
\(O_{16}\to K_{17}\).  It uses the explicit cyclic \(G(17)\) witness and
the radius-four \(L/M/N\) partition, rather than a derived Steiner system.
The latter is only necessary for a global cover and is not used as a
success criterion here.

## Exact stage equation

For an index pair \(ij\in\binom{[15]}2\) and a finite pair
\(uv\in\binom{[16]}2\), the 14 sphere-five vertices over \(ij,uv\) are
indexed by the third point \(w\notin\{u,v\}\).  Their colours must be the
14-element set
\[
 \mathcal C\setminus\{N_{uv}(ij),M_i(uv),M_j(uv)\}. \tag{1}
\]
Consequently, for a fixed \(ij\), assigning a colour to every finite
triple \(uvw\) is exactly a list triangle-decomposition problem: the
colours on the 14 triples containing a fixed edge \(uv\) must be
all-different.  Equation (1) is both necessary and sufficient for every
closed neighbourhood centred on the corresponding sphere-four vertex to
be rainbow.  The independent checker in
`global_construction_radius5.py` recomputes those full 17-colour lists.

## Staged search

The first mode fixes the deterministic 120 radius-four \(N_{uv}\)
edge-colourings from `global_latin_radius4_certificate.py` and asks for
the 560 triple colours for each \(ij\).  On 2026-07-24 its first instance
was exactly infeasible:

```text
python3 -B evidence/global_construction_radius5.py \
  --seconds-per-pair 60 --limit-pairs 1
RuntimeError: P_(0, 1): INFEASIBLE
```

This is a counterexample to that *particular deterministic radius-four
choice*, not an obstruction to a radius-five ball: the \(N\) values were
arbitrarily selected independently for each finite pair.

The second mode keeps the construction positive.  It jointly chooses all
120 trace values \(N_{uv}(ij)\) for one fixed \(ij\), together with its
560 triple colours.  Each selected trace value is then completed, and
checked, as a full \(K_{15}\) list edge-colouring \(N_{uv}\).  Thus a
successful output is an independently checkable radius-five **ray**.
It still does not synchronize the choices for the other 104 index pairs;
the remaining global task is a single coupled CSP over the common
\(N_{uv}\) tables and all 58,800 triple colours.

```bash
python3 -B evidence/global_construction_radius5.py \
  --adaptive-one-pair --seconds-per-pair 120
```

No success from this adaptive search is claimed in this record.

The current implementation removes the 120 explicit trace variables: for
each finite edge the all-different triple list determines its unique
omitted (N_{uv}(ij)) value.  Colours which cannot be that omitted value
are forced to occur, so this is equivalent but avoids a large artificial
branching factor.  A 10-second one-worker run reached `UNKNOWN` after
93,255 conflicts and 492,226 branches.  A completed bounded run without
a witness is therefore only a search limit, not an infeasibility result.

## Adversarial controls

The golf/partition route has the intended sharp behaviour in the already
settled cases.

* For \(k=4\), the first golf transition is impossible: the exhaustive
  reduced-Latin comparison has at least two forbidden equal interior
  cells.  Independently, the full design check finds no partition into
  five \(S(3,4,8)\) systems.
* For \(k=6\), local design ingredients do exist (the Witt system), so
  that weaker necessary shadow is deliberately not treated as a solution.
  The exhaustive Witt exact-cover control nevertheless rules out the
  required seven disjoint colour classes.

Run the checks with:

```bash
python3 -B evidence/global_latin_audit.py
python3 -B verify_k4.py
python3 -B evidence/verify_nilpotent_shift_obstruction.py
```

These controls test the actual tight-colouring consequence, rather than
mistaking existence of an individual Steiner system for a cover.
