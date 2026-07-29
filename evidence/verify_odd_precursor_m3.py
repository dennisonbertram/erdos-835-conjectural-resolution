#!/usr/bin/env python3
"""Exhaustive control for the m=3 odd-precursor colouring problem.

A hypothetical tight 5-colouring of J(6,3) has a missing-colour map on
the edges of K_6.  That map is a one-factorisation.  The script enumerates
all six labelled-one-set one-factorisations of K_6 (we quotient only the
irrelevant permutation of the five colour names).  For each, every
complementary pair of triples has exactly two possible colours, and the two
triples must take the two different possibilities.

There are ten complementary pairs, hence only 2^10 assignments left.  This
script checks every one and prints the exact zero count.  It is deliberately
stand-alone: it uses only Python's standard library and checks the original
four-triples-at-an-edge rainbow condition directly.
"""

from itertools import combinations, product


POINTS = tuple(range(6))
COLOURS = tuple(range(5))
EDGES = tuple(combinations(POINTS, 2))
TRIPLES = tuple(combinations(POINTS, 3))

def perfect_matchings(available: tuple[int, ...] = POINTS) -> tuple[tuple[tuple[int, int], ...], ...]:
    """All 15 perfect matchings of K_6."""
    if not available:
        return ((),)
    first = available[0]
    result = []
    for index in range(1, len(available)):
        second = available[index]
        rest = available[1:index] + available[index + 1 :]
        for matching in perfect_matchings(rest):
            result.append(tuple(sorted(((first, second),) + matching)))
    return tuple(result)


def one_factorisations() -> tuple[tuple[tuple[tuple[int, int], ...], ...], ...]:
    """All six one-factorisations of K_6, with factor order canonicalised."""
    matchings = perfect_matchings()
    by_edge = {edge: tuple(index for index, matching in enumerate(matchings) if edge in matching) for edge in EDGES}
    result = set()

    def search(remaining: frozenset[tuple[int, int]], chosen: tuple[int, ...]) -> None:
        if not remaining:
            result.add(tuple(sorted(chosen)))
            return
        edge = min(remaining)
        for index in by_edge[edge]:
            matching = matchings[index]
            if set(matching) <= remaining:
                search(remaining - frozenset(matching), chosen + (index,))

    search(frozenset(EDGES), ())
    return tuple(tuple(matchings[index] for index in factorisation) for factorisation in sorted(result))


def complement(triple: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(point for point in POINTS if point not in triple)


def allowed(triple: tuple[int, int, int], missing: dict[tuple[int, int], int]) -> tuple[int, int]:
    forbidden = {missing[edge] for edge in combinations(triple, 2)}
    answer = tuple(colour for colour in COLOURS if colour not in forbidden)
    assert len(answer) == 2
    return answer


def complementary_representatives() -> tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...]:
    result = []
    seen = set()
    for triple in TRIPLES:
        mate = complement(triple)
        pair = tuple(sorted((triple, mate)))
        if pair not in seen:
            seen.add(pair)
            result.append(pair)
    assert len(result) == 10
    return tuple(result)


def is_rainbow_at_every_edge(
    colouring: dict[tuple[int, int, int], int], missing: dict[tuple[int, int], int]
) -> bool:
    for edge in EDGES:
        star = tuple(
            colouring[tuple(sorted(edge + (point,)))]
            for point in POINTS
            if point not in edge
        )
        # Exactly the four colours other than the missing colour of this edge
        # must occur around it.
        if len(set(star)) != 4 or missing[edge] in star:
            return False
    return True


def main() -> None:
    representatives = complementary_representatives()
    factorisations = one_factorisations()
    assert len(perfect_matchings()) == 15
    assert len(factorisations) == 6
    attempted = 0
    satisfying = 0
    for factors in factorisations:
        missing = {edge: colour for colour, factor in enumerate(factors) for edge in factor}
        assert all(allowed(first, missing) == allowed(second, missing) for first, second in representatives)
        for bits in product((0, 1), repeat=len(representatives)):
            attempted += 1
            colouring: dict[tuple[int, int, int], int] = {}
            for bit, (first, second) in zip(bits, representatives):
                options = allowed(first, missing)
                colouring[first] = options[bit]
                colouring[second] = options[1 - bit]
            satisfying += is_rainbow_at_every_edge(colouring, missing)

    assert attempted == 6 * 2**10
    assert satisfying == 0
    print(f"K_6 one-factorisations checked: {len(factorisations)}")
    print("complementary triple pairs: 10")
    print(f"orientation assignments checked: {attempted} (= 6 * 2^10)")
    print(f"satisfying tight 5-colourings of J(6,3): {satisfying}")
    print("PASS: no tight 5-colouring of J(6,3)")


if __name__ == "__main__":
    main()
