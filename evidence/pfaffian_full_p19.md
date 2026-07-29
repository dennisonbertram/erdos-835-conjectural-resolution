# Structured p=19 principal-Pfaffian screen

For \(p=19\), the direct principal-Pfaffian route would use a
\(36\times36\) alternating matrix over \(\mathbb F_{19}\), with its
18-Pfaffians rainbow on every 17-star. This is distinct from the p=17
four-Pfaffian descendant.

search_pfaffian_full_p19.py evaluates every tested star by an exact modular
Pfaffian-elimination routine. It screens:

- named skew-circulant profiles and reproducibly seeded random projective
  circulant profiles;
- the F_19-valued entrywise trace of the Cauchy kernel
  \((x-y)/(1-xy)\) on a 36th-root coset in \(\mathbb F_{19^2}\), for all
  20 projective trace directions.

Run:

    python3 evidence/search_pfaffian_full_p19.py --trials 50 --random-circulants 25

The script begins by comparing its Pfaffian eliminator with the closed
4-by-4 Pfaffian formula on 100 seeded matrices and verifies the chosen
\(\mathbb F_{19^2}\) generator.

Each displayed counterstar is an exact rejection of that concrete
36-by-36 matrix. A survivor has only passed a finite random-star screen,
not all \(\binom{36}{17}\) stars. Conversely, failure of these structured
families says nothing about an arbitrary alternating matrix over
\(\mathbb F_{19}\).
