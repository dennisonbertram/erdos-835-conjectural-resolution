#!/usr/bin/env python3
"""Per-tuple perfect-information Griesmer margins for all 1,450 dim-2 profiles.

Derived from evidence/verify_s141531_dim2_subcodes.py (functions copied
verbatim).  For every valid labelled tuple computes:
  L_lo, L_up   : shortened length bounds (exact iff 16 not in weights_H)
  D_exact      : min exact realized coset weight (16-free coset, 16-free H)
  D_fallback   : min over ALL cosets of floor((base_upper - sumF_lower)/8)
                 (rigorous upper endpoint on that word's realized weight)
  D_up         : D_exact if it exists else D_fallback
  G28          : Griesmer sum with k = 28 (max possible image dimension:
                 kernel always contains H, dim >= 2, so image dim <= 28)
  margin_up    = G28 - L_up   (task's stated L convention)
  margin_lo    = G28 - L_lo   (rigorous: contradiction needs G > L_true >= L_lo)
"""
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import time

POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
EVEN_CODE_DIMENSION = 30
MIDDLE_CORRECTION = 1 << BLOCK_SIZE
EXPECTED_CSV_SHA256 = (
    "0982008c066a55a0fb436b75710b9997696a6bfe1c4a41ad840894f69bf1b578"
)

LAMBDA = tuple(
    comb(POINTS - level, DESIGN_T - level) // (BLOCK_SIZE - level)
    for level in range(DESIGN_T + 1)
)


def fourier_external(size: int) -> int:
    if size > BLOCK_SIZE:
        return -fourier_external(POINTS - size)
    return sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, DESIGN_T) + 1)
    )


FOURIER_LOWER = tuple(fourier_external(size) for size in range(POINTS + 1))
FOURIER_UPPER = tuple(
    value + (MIDDLE_CORRECTION if size == BLOCK_SIZE + 1 else 0)
    for size, value in enumerate(FOURIER_LOWER)
)


def griesmer(distance: int, dimension: int) -> int:
    return sum(
        (distance + (1 << power) - 1) // (1 << power)
        for power in range(dimension)
    )


def ceil_div(n: int, d: int) -> int:
    return -((-n) // d)


def dot(left: int, right: int) -> int:
    return bin(left & right).count("1") & 1


def binary_rank(vectors, dimension):
    pivots = [0] * dimension
    rank = 0
    for vector in vectors:
        row = vector
        while row:
            pivot = row.bit_length() - 1
            if pivots[pivot]:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                rank += 1
                break
    return rank


def maximum_kernel_dimension(removed_upper: int, minimum: int) -> int:
    return max(
        (
            dim
            for dim in range(EVEN_CODE_DIMENSION + 1)
            if griesmer(minimum, dim) <= removed_upper
        ),
        default=0,
    )


def original_even_code_minimum() -> int:
    candidates = []
    for size in range(2, POINTS, 2):
        values = [FOURIER_LOWER[size]]
        if size == BLOCK_SIZE + 1:
            values.append(FOURIER_UPPER[size])
        candidates.extend((BLOCKS - value) // 2 for value in values)
    return min(candidates)


def main() -> None:
    assert BLOCKS == 17_678_835
    original_minimum = original_even_code_minimum()
    assert original_minimum == 8_809_920

    start = time.time()
    order = 4
    records = []
    total_reps = 0

    for c0 in range(POINTS + 1):
        for c1 in range(POINTS - c0 + 1):
            for c2 in range(POINTS - c0 - c1 + 1):
                c3 = POINTS - c0 - c1 - c2
                counts = (c0, c1, c2, c3)
                if (c1 + c3) & 1 or (c2 + c3) & 1:
                    continue
                positive = {v for v in (1, 2, 3) if counts[v] > 0}
                if binary_rank(positive, 2) != 2:
                    continue

                weights_h = tuple(
                    sum(counts[v] for v in range(order) if dot(w, v))
                    for w in range(order)
                )
                base_lower = sum(FOURIER_LOWER[w] for w in weights_h)
                base_upper = sum(FOURIER_UPPER[w] for w in weights_h)
                length_lower = ceil_div(base_lower, order)
                length_upper = base_upper // order
                h_free = BLOCK_SIZE + 1 not in weights_h

                removed_upper = BLOCKS - length_lower
                kernel_upper = maximum_kernel_dimension(
                    removed_upper, original_minimum
                )

                subgroup_profiles = {
                    tuple(
                        counts[v] if dot(w, v) else 0 for v in range(order)
                    )
                    for w in range(order)
                }

                reps = 0
                d_exact = None
                d_fallback = None
                d_lower = None
                a_count = weights_h.count(BLOCK_SIZE + 1)
                assert base_upper - base_lower == MIDDLE_CORRECTION * a_count
                best_refined = None
                for profile in product(*(range(c + 1) for c in counts)):
                    if sum(profile) & 1 or profile in subgroup_profiles:
                        continue
                    reps += 1
                    weights = tuple(
                        sum(
                            (
                                counts[v] - profile[v]
                                if dot(w, v)
                                else profile[v]
                            )
                            for v in range(order)
                        )
                        for w in range(order)
                    )
                    sumF_lower = sum(FOURIER_LOWER[w] for w in weights)
                    sumF_upper = sum(FOURIER_UPPER[w] for w in weights)
                    lower = ceil_div(base_lower - sumF_upper, 2 * order)
                    if d_lower is None or lower < d_lower:
                        d_lower = lower
                    up_end = (base_upper - sumF_lower) // (2 * order)
                    if d_fallback is None or up_end < d_fallback:
                        d_fallback = up_end
                    if h_free and BLOCK_SIZE + 1 not in weights:
                        num = base_lower - sumF_lower
                        assert num % (2 * order) == 0
                        exact = num // (2 * order)
                        if d_exact is None or exact < d_exact:
                            d_exact = exact
                    if not h_free:
                        # Coupled bound: B = base_lower + 32768*a shifts
                        # this coset word's weight and |Z_H| together.
                        term = max(
                            griesmer(
                                (
                                    base_lower
                                    + MIDDLE_CORRECTION * a
                                    - sumF_lower
                                )
                                // (2 * order),
                                28,
                            )
                            - (base_lower + MIDDLE_CORRECTION * a) // order
                            for a in range(a_count + 1)
                        )
                        if best_refined is None or term < best_refined:
                            best_refined = term

                total_reps += reps
                d_up = d_exact if d_exact is not None else d_fallback
                g28 = griesmer(d_up, 28)
                if h_free:
                    assert length_lower == length_upper
                    margin_final = g28 - length_lower
                else:
                    margin_final = best_refined
                records.append(
                    {
                        "counts": counts,
                        "weights_h": weights_h,
                        "L_lo": length_lower,
                        "L_up": length_upper,
                        "L_exact": length_lower == length_upper,
                        "kernel_upper": kernel_upper,
                        "reps": reps,
                        "d_lower": d_lower,
                        "D_exact": d_exact,
                        "D_fallback": d_fallback,
                        "D_up": d_up,
                        "exact_realized": d_exact is not None,
                        "G28": g28,
                        "margin_up": g28 - length_upper,
                        "margin_lo": g28 - length_lower,
                        "margin_final": margin_final,
                    }
                )

    elapsed = time.time() - start
    assert len(records) == 1_450, len(records)
    assert total_reps == 1_567_276, total_reps

    # Sanity check against the committed extremal tuple.
    ext = next(r for r in records if r["counts"] == (0, 9, 9, 13))
    assert ext["L_lo"] == ext["L_up"] == 4_419_003
    assert ext["d_lower"] == 2_197_848
    assert ext["D_exact"] == 2_201_720
    assert ext["kernel_upper"] == 2

    no_exact = [r for r in records if not r["exact_realized"]]
    inexact_L = [r for r in records if not r["L_exact"]]
    h16 = [r for r in records if BLOCK_SIZE + 1 in r["weights_h"]]
    min_dlow = min(r["d_lower"] for r in records)
    min_Dup = min(r["D_up"] for r in records)
    kdist = {}
    for r in records:
        kdist[r["kernel_upper"]] = kdist.get(r["kernel_upper"], 0) + 1

    max_margin_up = max(r["margin_up"] for r in records)
    max_margin_lo = max(r["margin_lo"] for r in records)
    max_margin_final = max(r["margin_final"] for r in records)
    positives = [r for r in records if r["margin_final"] >= 0]
    top5 = sorted(records, key=lambda r: -r["margin_final"])[:5]
    assert len(h16) == len(inexact_L) == len(no_exact) == 358
    assert kdist == {2: 1_450}
    assert min_dlow == min_Dup == 1_975_240
    assert max_margin_up == max_margin_final == -14_940
    assert max_margin_lo == 9_372
    assert not positives

    print(f"tuples={len(records)} representatives={total_reps}")
    print(f"elapsed_seconds={elapsed:.1f}")
    print(f"tuples_with_16_in_weights_h={len(h16)}")
    print(f"tuples_with_inexact_L={len(inexact_L)}")
    print(f"tuples_without_16free_coset={len(no_exact)}")
    print(f"kernel_upper_distribution={kdist}")
    print(f"min_distance_lower_over_all_tuples={min_dlow}")
    print(f"min_D_up_over_all_tuples={min_Dup}")
    print(f"max_margin_G28_minus_Lup={max_margin_up}")
    print(f"max_margin_G28_minus_Llo_decoupled={max_margin_lo}")
    print(f"max_margin_final_coupled={max_margin_final}")
    print(f"tuples_with_nonnegative_final_margin={len(positives)}")
    print("top5_by_margin_final:")
    for r in top5:
        print(
            f"  counts={r['counts']} L=[{r['L_lo']},{r['L_up']}] "
            f"D_up={r['D_up']} exact_realized={r['exact_realized']} "
            f"d_lower={r['d_lower']} kernel_upper={r['kernel_upper']} "
            f"G28={r['G28']} margin_final={r['margin_final']} "
            f"margin_lo={r['margin_lo']} margin_up={r['margin_up']}"
        )
    csv_lines = [
        "c0,c1,c2,c3,L_lo,L_up,kernel_upper,d_lower,D_up,"
        "exact_realized,G28,margin_lo,margin_up,margin_final\n"
    ]
    for r in records:
        csv_lines.append(
            ",".join(
                map(
                    str,
                    (
                        *r["counts"],
                        r["L_lo"],
                        r["L_up"],
                        r["kernel_upper"],
                        r["d_lower"],
                        r["D_up"],
                        int(r["exact_realized"]),
                        r["G28"],
                        r["margin_lo"],
                        r["margin_up"],
                        r["margin_final"],
                    ),
                )
            )
            + "\n"
        )
    csv_bytes = "".join(csv_lines).encode("ascii")
    assert sha256(csv_bytes).hexdigest() == EXPECTED_CSV_SHA256
    csv_path = Path(__file__).with_name("s141531_dim2_margins.csv")
    assert csv_path.read_bytes() == csv_bytes
    print(f"csv={csv_path} sha256={EXPECTED_CSV_SHA256}")
    print("S(14,15,31) dim-2 perfect-information closure: PASS")


if __name__ == "__main__":
    main()
