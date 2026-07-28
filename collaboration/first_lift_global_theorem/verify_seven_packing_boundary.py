#!/usr/bin/env python3
"""Audit SEVEN_PACKING_NONZERO_R_NOTE.md.

Standard library only.  Checks the finite Tutte/profile arithmetic and keeps
the exceptional r=0 equality cases explicit.
"""


def odd_partitions(total, minimum=1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1, 2):
        for rest in odd_partitions(total - first, first):
            yield (first,) + rest


def barriers(order, deletion_degree):
    out = []
    for size_s in range(order):
        for parts in odd_partitions(order - size_s):
            if len(parts) <= size_s or (len(parts) - size_s) % 2:
                continue
            if max(order - size_s - part for part in parts) > deletion_degree:
                continue
            cross = sum(
                parts[i] * parts[j]
                for i in range(len(parts))
                for j in range(i + 1, len(parts))
            )
            out.append((size_s, parts, cross))
    return sorted(out)


def verify_profiles():
    choices = {}
    for count_12 in range(1, 6):
        counts = {8: 7 + count_12, 10: 10 - 2 * count_12, 12: count_12}
        if count_12 == 1:
            choice = (8, 8, 8, 8, 10, 10)
        elif count_12 < 5:
            choice = (8, 8, 8, 8, 10, 12)
        else:
            choice = (8, 8, 8, 8, 12, 12)
        assert all(choice.count(size) <= counts[size] for size in counts)
        assert counts[12] - choice.count(12) >= 1
        choices[count_12] = choice
    return choices


def verify_five_plus_five_row_argument():
    capacities = [4, 4, 4, 4, 5, 5]
    assert sum(capacities) == 26
    required = 25
    assert sum(capacities) - required == 1

    # If an 8-support is deficient, five other supports avoid all 3 outside
    # vertices.  Its forced outside attendance leaves only 5 vertices in V,
    # while three crossing edges need 6.
    assert 8 - 3 == 5
    assert 2 * (4 - 1) == 6
    assert 5 < 6

    # If a 10-support is deficient, the same argument leaves 7 vertices in V,
    # while four crossing edges need 8.
    assert 10 - 3 == 7
    assert 2 * (5 - 1) == 8
    assert 7 < 8


def main():
    twelve = barriers(12, 6)
    assert twelve == [(5, (1, 1, 1, 1, 1, 1, 1), 21)]
    assert 6 * 3 < 21
    print("PASS K12 deletion has only the impossible seven-singleton barrier")

    choices = verify_profiles()
    assert len(choices) == 5
    print("PASS every r=1..5 choice leaves a size-12 support")

    ten = barriers(10, 6)
    expected = [
        (0, (5, 5), 25),
        (1, (3, 3, 3), 27),
        (3, (1, 1, 1, 1, 1, 1, 1), 21),
        (3, (1, 1, 1, 1, 3), 18),
        (4, (1, 1, 1, 1, 1, 1), 15),
    ]
    assert ten == expected
    assert 6 * 4 < 27
    assert 6 * 3 < 21
    print("PASS r=0 Tutte arithmetic leaves three capacity-clean shapes")

    verify_five_plus_five_row_argument()
    print("PASS class-B row sums eliminate the 5+5 shape")
    print("SCOPE: seven-pack proved for r>=1; r=0 has two open equality cases.")


if __name__ == "__main__":
    main()
