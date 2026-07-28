#!/usr/bin/env python3
"""Audit SEVEN_PACKING_NONZERO_R_NOTE.md.

Standard library only.  Checks the finite Tutte/profile arithmetic and keeps
the exceptional r=0 equality cases explicit.
"""


def partitions(total, minimum=1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def barriers(order, deletion_degree):
    out = []
    for size_s in range(order):
        for parts in partitions(order - size_s):
            odd_components = sum(part % 2 for part in parts)
            if odd_components <= size_s:
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

    # Every nondeficient matching uses all support vertices inside V:
    # 4 crossing edges use all 8 vertices, and 5 use all 10.  The five
    # nondeficient prior colours plus the target colour are then all
    # forbidden at each vertex outside V, exceeding the row sum five.
    assert 2 * capacities[0] == 8
    assert 2 * capacities[-1] == 10
    nondeficient_prior_colours = len(capacities) - 1
    target_colour = 1
    assert nondeficient_prior_colours + target_colour == 6 > 5


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
        (3, (1, 1, 1, 1, 1, 2), 20),
        (3, (1, 1, 1, 1, 3), 18),
        (4, (1, 1, 1, 1, 1, 1), 15),
    ]
    assert ten == expected
    assert 6 * 4 < 27
    assert 6 * 3 < 20
    assert 6 * 3 < 21
    print("PASS r=0 Tutte arithmetic leaves three capacity-clean shapes")

    verify_five_plus_five_row_argument()
    print("PASS class-B row sums eliminate the 5+5 shape")
    print("SCOPE: seven-pack proved for r>=1; r=0 has two open equality cases.")


if __name__ == "__main__":
    main()
