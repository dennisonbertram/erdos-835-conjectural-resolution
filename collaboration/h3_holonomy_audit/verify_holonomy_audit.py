#!/usr/bin/env python3
"""Independent, standard-library audit of the LS(2,3,19) holonomy layer.

The default run performs every exact structural check and a deterministic
128-one-factorization affine-rank experiment.  Use ``--full`` to replay the
reported 3,000-factorization experiment.

No solver, network access, third-party package, or repository import is used.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from itertools import combinations
from math import comb

Permutation = tuple[int, ...]
Triple = tuple[int, int, int]
Colouring = dict[Triple, int]
Edge = frozenset[int]
Factor = frozenset[Edge]
Factorization = list[Factor]

P = 17
FINITE = tuple(range(P))
LEFT = 17
INFINITY_POINT = 18
POINTS = tuple(range(19))
COLOURS = tuple(range(17))
INFINITY_COLOUR = 17

# A compact certificate for the repository's cyclic LS(2,3,19).
STARTERS = (
    (0, 2, 5, 9, 14, 16, 13, 15, 12, 4, 8, 7, 11, 10, 6, 3, 1),
    (0, 3, 1, 10, 12, 11, 15, 4, 13, 5, 14, 9, 6, 8, 7, 16, 2),
)
PHASES = (
    7,
    1,
    9,
    0,
    5,
    12,
    15,
    8,
    13,
    11,
    4,
    16,
    10,
    14,
    15,
    14,
    2,
    10,
    6,
    9,
    11,
    4,
    8,
    3,
    12,
    6,
    5,
    4,
    11,
    2,
    14,
    0,
    7,
    8,
    6,
    1,
    10,
    5,
    12,
    6,
)

CHECKS: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    """Record and print one auditable assertion."""
    condition = bool(condition)
    CHECKS.append((name, condition))
    print(("PASS  " if condition else "FAIL  ") + name)
    sys.stdout.flush()


def canonical(values: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical([(value + amount) % P for value in values])


def representatives() -> tuple[Triple, ...]:
    unseen = set(combinations(FINITE, 3))
    answer: list[Triple] = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in FINITE)
        answer.append(representative)
        for shift in FINITE:
            unseen.discard(translate(representative, shift))
    if len(answer) != 40:
        raise AssertionError("the finite triples should have forty C17 orbits")
    return tuple(answer)


def square(starter: tuple[int, ...], x: int, y: int) -> int:
    return (starter[(x - y) % P] + y) % P


def construct_cyclic_ls19() -> Colouring:
    """Reconstruct the 969 colours from two starters and forty phases."""
    colouring: Colouring = {}

    def put(raw_triple: tuple[int, int, int], colour: int) -> None:
        triple = canonical(raw_triple)
        if triple in colouring:
            raise AssertionError("triple assigned twice")
        if colour not in COLOURS:
            raise AssertionError("colour outside 0,...,16")
        colouring[triple] = colour

    for x in FINITE:
        put((LEFT, INFINITY_POINT, x), x)
    for x, y in combinations(FINITE, 2):
        put((LEFT, x, y), square(STARTERS[0], x, y))
        put((INFINITY_POINT, x, y), square(STARTERS[1], x, y))

    reps = representatives()
    if len(PHASES) != len(reps):
        raise AssertionError("one phase is required per finite triple orbit")
    for orbit, representative in enumerate(reps):
        zero_shift = (-PHASES[orbit]) % P
        for colour in FINITE:
            put(translate(representative, zero_shift + colour), colour)
    return colouring


def verify_large_set(colouring: Colouring) -> None:
    """Verify the complete LS(2,3,19) definition, not just local samples."""
    check(
        "cyclic certificate colours every one of the C(19,3)=969 triples",
        len(colouring) == comb(19, 3)
        and set(colouring) == set(combinations(POINTS, 3)),
    )
    check(
        "every colour class has 57 triples",
        Counter(colouring.values()) == Counter({colour: 57 for colour in COLOURS}),
    )

    rainbow = True
    for pair in combinations(POINTS, 2):
        values = [
            colouring[canonical([*pair, third])]
            for third in POINTS
            if third not in pair
        ]
        rainbow &= sorted(values) == list(COLOURS)
    check("every pair-star is a bijection onto the 17 colours", rainbow)

    steiner = True
    expected_pairs = Counter(combinations(POINTS, 2))
    for colour in COLOURS:
        pair_counts: Counter[tuple[int, int]] = Counter()
        for triple, value in colouring.items():
            if value == colour:
                pair_counts.update(combinations(triple, 2))
        steiner &= pair_counts == expected_pairs
    check("each colour class is an S(2,3,19)", steiner)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left composed with right."""
    return tuple(left[right[x]] for x in range(len(right)))


def inverse(permutation: Permutation) -> Permutation:
    answer = [0] * len(permutation)
    for source, image in enumerate(permutation):
        answer[image] = source
    return tuple(answer)


def cycle_type(permutation: Permutation) -> tuple[int, ...]:
    seen: set[int] = set()
    parts: list[int] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1
        parts.append(length)
    return tuple(sorted(parts, reverse=True))


def permutation_sign(permutation: Permutation) -> int:
    return -1 if (len(permutation) - len(cycle_type(permutation))) % 2 else 1


def sequence_sign(values: list[int]) -> int:
    inversions = sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def root_edges(
    colouring: Colouring,
    root: int,
    ground: tuple[int, ...] = POINTS,
) -> tuple[tuple[int, ...], dict[Edge, int]]:
    vertices = tuple(point for point in ground if point != root)
    edge_colours = {
        frozenset((a, b)): colouring[canonical((root, a, b))]
        for a, b in combinations(vertices, 2)
    }
    return vertices, edge_colours


def holonomy(
    vertices: tuple[int, ...],
    edge_colours: dict[Edge, int],
    a: int,
    b: int,
    m: int = 17,
) -> Permutation:
    """Compute sigma(a,b) from a labelled one-factorization."""
    inverse_star = {edge_colours[frozenset((a, x))]: x for x in vertices if x != a}
    common = edge_colours[frozenset((a, b))]
    answer: list[int] = []
    for colour in range(m):
        point = inverse_star[colour]
        answer.append(common if point == b else edge_colours[frozenset((b, point))])
    return tuple(answer)


def local_exact_h(
    vertices: tuple[int, ...],
    edge_colours: dict[Edge, int],
) -> Counter[Permutation]:
    exact: Counter[Permutation] = Counter()
    for a in vertices:
        for b in vertices:
            if a != b:
                exact[holonomy(vertices, edge_colours, a, b)] += 1
    return exact


def partitions(total: int) -> int:
    counts = [0] * (total + 1)
    counts[0] = 1
    for part in range(1, total + 1):
        for value in range(part, total + 1):
            counts[value] += counts[value - part]
    return counts[total]


def fixed_point_free_partitions(
    total: int,
    maximum: int | None = None,
) -> list[tuple[int, ...]]:
    """Partitions of total into parts at least two, in reverse lexicographic order."""
    if total == 0:
        return [()]
    maximum = total if maximum is None else min(maximum, total)
    answer: list[tuple[int, ...]] = []
    for first in range(maximum, 1, -1):
        for tail in fixed_point_free_partitions(total - first, first):
            answer.append((first, *tail))
    return answer


def audit_holonomies(
    colouring: Colouring,
) -> tuple[
    Counter[tuple[int, ...]],
    Counter[Permutation],
    dict[int, int],
    dict[int, tuple[tuple[int, ...], dict[Edge, int]]],
]:
    census: Counter[tuple[int, ...]] = Counter()
    exact_oriented: Counter[Permutation] = Counter()
    root_odd_counts: dict[int, int] = {}
    roots: dict[int, tuple[tuple[int, ...], dict[Edge, int]]] = {}
    unique_fixed = True
    fixed_is_common = True

    for root in POINTS:
        vertices, edge_colours = root_edges(colouring, root)
        roots[root] = vertices, edge_colours
        root_odd = 0
        for a, b in combinations(vertices, 2):
            sigma = holonomy(vertices, edge_colours, a, b)
            sigma_inverse = holonomy(vertices, edge_colours, b, a)
            fixed = [colour for colour, image in enumerate(sigma) if image == colour]
            common = edge_colours[frozenset((a, b))]
            unique_fixed &= len(fixed) == 1
            fixed_is_common &= fixed == [common]
            unique_fixed &= sigma_inverse == inverse(sigma)
            kind = cycle_type(sigma)
            census[kind] += 1
            exact_oriented[sigma] += 1
            exact_oriented[sigma_inverse] += 1
            root_odd += permutation_sign(sigma) == -1
        root_odd_counts[root] = root_odd

    check("every cyclic-example holonomy has exactly one fixed colour", unique_fixed)
    check("that fixed colour is the common edge colour", fixed_is_common)
    check(
        "the unordered holonomy census has 19*C(18,2)=2907 entries",
        sum(census.values()) == 19 * comb(18, 2) == 2907,
    )
    check(
        "the oriented exact H has 5814 summands and 5814 distinct permutations",
        sum(exact_oriented.values()) == 5814
        and len(exact_oriented) == 5814
        and set(exact_oriented.values()) == {1},
    )
    check(
        "the central census has 34 nonzero coordinates",
        len(census) == 34,
    )
    check(
        "exactly 17 of the 55 central coordinates are odd",
        sum(count % 2 for count in census.values()) == 17,
    )

    odd_total = sum(count for kind, count in census.items() if (17 - len(kind)) % 2)
    weighted_twos = sum(kind.count(2) * count for kind, count in census.items())
    check("cyclic control: O=1530 odd holonomies", odd_total == 1530)
    check(
        "cyclic control: the 2-cycle-weighted census is 1938",
        weighted_twos == 1938,
    )
    check(
        "cyclic control: root odd-count multiset is 17*73, 136, 153",
        Counter(root_odd_counts.values()) == Counter({73: 17, 136: 1, 153: 1}),
    )
    return census, exact_oriented, root_odd_counts, roots


def audit_type_count(census: Counter[tuple[int, ...]]) -> list[tuple[int, ...]]:
    types = [(*parts, 1) for parts in fixed_point_free_partitions(16)]
    check(
        "p(16)=231 and p(15)=176, hence exactly-one-fixed types number 55",
        partitions(16) == 231
        and partitions(15) == 176
        and partitions(16) - partitions(15) == 55
        and len(types) == 55
        and len(set(types)) == 55,
    )
    check(
        "all 34 observed cyclic types lie in the corrected 55-type universe",
        set(census) <= set(types),
    )
    return types


def audit_cross_root_cocycle(
    roots: dict[int, tuple[tuple[int, ...], dict[Edge, int]]],
) -> None:
    exact_ok = True
    sign_ok = True
    profiles: Counter[int] = Counter()
    for i, j, k in combinations(POINTS, 3):
        vertices_i, edges_i = roots[i]
        vertices_j, edges_j = roots[j]
        vertices_k, edges_k = roots[k]
        sigma_i_jk = holonomy(vertices_i, edges_i, j, k)
        sigma_k_ij = holonomy(vertices_k, edges_k, i, j)
        sigma_j_ik = holonomy(vertices_j, edges_j, i, k)
        exact_ok &= compose(sigma_k_ij, sigma_i_jk) == sigma_j_ik
        odd = sum(
            permutation_sign(sigma) == -1
            for sigma in (sigma_i_jk, sigma_k_ij, sigma_j_ik)
        )
        profiles[odd] += 1
        sign_ok &= odd in (0, 2)

    check(
        "all 969 cyclic point-triples satisfy sigma_k(i,j)sigma_i(j,k)=sigma_j(i,k)",
        exact_ok,
    )
    check("every cyclic point-triple has zero or two odd holonomies", sign_ok)
    check(
        "cyclic control: triangle profile is 204 with zero odd and 765 with two",
        profiles == Counter({0: 204, 2: 765}),
    )


def augmented_transition(
    vertices: tuple[int, ...],
    edge_colours: dict[Edge, int],
    a: int,
    b: int,
) -> Permutation:
    chart_a = {
        point: (INFINITY_COLOUR if point == a else edge_colours[frozenset((a, point))])
        for point in vertices
    }
    chart_b = {
        point: (INFINITY_COLOUR if point == b else edge_colours[frozenset((b, point))])
        for point in vertices
    }
    inverse_a = {symbol: point for point, symbol in chart_a.items()}
    return tuple(chart_b[inverse_a[symbol]] for symbol in range(18))


def transposition(n: int, a: int, b: int) -> Permutation:
    answer = list(range(n))
    answer[a], answer[b] = answer[b], answer[a]
    return tuple(answer)


def audit_augmented_cocycle(
    roots: dict[int, tuple[tuple[int, ...], dict[Edge, int]]],
) -> None:
    cocycle_ok = True
    relation_ok = True
    autocorrelation_ok = True
    derangement_ok = True
    identity18 = tuple(range(18))

    for vertices, edge_colours in roots.values():
        transitions: dict[tuple[int, int], Permutation] = {}
        for a in vertices:
            for b in vertices:
                if a == b:
                    continue
                tau = augmented_transition(vertices, edge_colours, a, b)
                transitions[a, b] = tau
                sigma = holonomy(vertices, edge_colours, a, b) + (INFINITY_COLOUR,)
                common = edge_colours[frozenset((a, b))]
                predicted = compose(
                    transposition(18, INFINITY_COLOUR, common),
                    sigma,
                )
                relation_ok &= tau == predicted
                derangement_ok &= all(
                    source != image for source, image in enumerate(tau)
                )

        for a, b, c in combinations(vertices, 3):
            cocycle_ok &= (
                compose(transitions[b, c], transitions[a, b]) == transitions[a, c]
            )
            cocycle_ok &= (
                compose(transitions[c, b], transitions[a, c]) == transitions[a, b]
            )

        reference = vertices[0]
        gauges = {
            a: (identity18 if a == reference else transitions[reference, a])
            for a in vertices
        }
        gram: Counter[Permutation] = Counter()
        for left in gauges.values():
            for right in gauges.values():
                gram[compose(left, inverse(right))] += 1
        transition_sum: Counter[Permutation] = Counter(transitions.values())
        transition_sum[identity18] += 18
        autocorrelation_ok &= gram == transition_sum

    check("augmented transitions satisfy tau(b,c)tau(a,b)=tau(a,c)", cocycle_ok)
    check("tau=(infinity common-colour)sigma with the audited orientation", relation_ok)
    check("every augmented transition is a derangement", derangement_ok)
    check(
        "the exact augmented autocorrelation identity holds at every root",
        autocorrelation_ok,
    )


def pair_star_sign(colouring: Colouring, i: int, j: int) -> int:
    values = [colouring[canonical((i, j, x))] for x in POINTS if x not in (i, j)]
    return sequence_sign(values)


def audit_tournament(
    colouring: Colouring,
    roots: dict[int, tuple[tuple[int, ...], dict[Edge, int]]],
    root_odd_counts: dict[int, int],
) -> None:
    pair_sign = {
        frozenset((i, j)): pair_star_sign(colouring, i, j)
        for i, j in combinations(POINTS, 2)
    }

    def tournament_sign(i: int, j: int) -> int:
        exponent = i + j + (1 if i > j else 0)
        return (-1 if exponent % 2 else 1) * pair_sign[frozenset((i, j))]

    skew_ok = all(
        tournament_sign(i, j) == -tournament_sign(j, i)
        for i, j in combinations(POINTS, 2)
    )
    check("the normalized pair signs define a tournament", skew_ok)

    formula_ok = True
    degrees: dict[int, int] = {}
    for i in POINTS:
        vertices, edge_colours = roots[i]
        degrees[i] = sum(tournament_sign(i, j) == 1 for j in vertices)
        for j, k in combinations(vertices, 2):
            sigma = holonomy(vertices, edge_colours, j, k)
            formula_ok &= permutation_sign(sigma) == -tournament_sign(
                i, j
            ) * tournament_sign(i, k)
    check("sgn sigma_i(j,k) = -t_ij*t_ik for all cyclic triples", formula_ok)

    local_formula = all(
        root_odd_counts[i]
        == comb(degrees[i], 2) + comb(18 - degrees[i], 2)
        == 72 + (degrees[i] - 9) ** 2
        for i in POINTS
    )
    check("each root odd count obeys 72+(d_i-9)^2", local_formula)

    odd_total = sum(root_odd_counts.values())
    transitive_triangles = sum(comb(degree, 2) for degree in degrees.values())
    square_sum = sum((degree - 9) ** 2 for degree in degrees.values())
    check(
        "O=2*sum C(d_i,2)=1368+sum(d_i-9)^2=1530",
        odd_total == 2 * transitive_triangles == 1368 + square_sum == 1530,
    )
    check(
        "the universal numerical window 1368<=O<=1938 is respected",
        1368 <= odd_total <= 1938 and odd_total % 2 == 0,
    )


def count_four_cycle_components(
    vertices: tuple[int, ...],
    edge_colours: dict[Edge, int],
) -> int:
    colour_edges: dict[int, set[Edge]] = {colour: set() for colour in COLOURS}
    for edge, colour in edge_colours.items():
        colour_edges[colour].add(edge)

    total = 0
    for first, second in combinations(COLOURS, 2):
        adjacency: dict[int, list[int]] = {vertex: [] for vertex in vertices}
        for edge in colour_edges[first] | colour_edges[second]:
            a, b = tuple(edge)
            adjacency[a].append(b)
            adjacency[b].append(a)
        unseen = set(vertices)
        while unseen:
            start = min(unseen)
            stack = [start]
            component: set[int] = set()
            while stack:
                vertex = stack.pop()
                if vertex in component:
                    continue
                component.add(vertex)
                stack.extend(adjacency[vertex])
            unseen -= component
            total += len(component) == 4
    return total


def audit_two_cycle_double_count(
    census: Counter[tuple[int, ...]],
    roots: dict[int, tuple[tuple[int, ...], dict[Edge, int]]],
) -> None:
    weighted_twos = sum(kind.count(2) * count for kind, count in census.items())
    four_cycles = sum(
        count_four_cycle_components(vertices, edge_colours)
        for vertices, edge_colours in roots.values()
    )
    check(
        "2-cycle holonomies double-count alternating 4-cycles",
        weighted_twos == 2 * four_cycles == 1938,
    )
    check("therefore the 2-cycle-weighted census is even", weighted_twos % 2 == 0)


def round_robin_labels(n: int) -> dict[Edge, int]:
    if n < 2 or n % 2:
        raise ValueError("round-robin factorization requires positive even n")
    modulus = n - 1
    fixed = n - 1
    labels: dict[Edge, int] = {}
    for label in range(modulus):
        labels[frozenset((fixed, label))] = label
        for offset in range(1, n // 2):
            edge = frozenset(((label + offset) % modulus, (label - offset) % modulus))
            if edge in labels:
                raise AssertionError("round-robin edge repeated")
            labels[edge] = label
    if len(labels) != comb(n, 2):
        raise AssertionError("round-robin factorization incomplete")
    return labels


def audit_pseudogluing(base: Colouring) -> None:
    points = tuple(range(20))
    edge_label = round_robin_labels(20)
    links: dict[int, Colouring] = {}
    links_valid = True
    for root in points:
        ground = tuple(point for point in points if point != root)
        transport = {point: edge_label[frozenset((root, point))] for point in ground}
        links_valid &= set(transport.values()) == set(POINTS)
        link = {
            canonical(block): base[canonical([transport[point] for point in block])]
            for block in combinations(ground, 3)
        }
        links[root] = link
        for pair in combinations(ground, 2):
            values = [
                link[canonical([*pair, third])] for third in ground if third not in pair
            ]
            links_valid &= sorted(values) == list(COLOURS)
    check("the pseudogluing consists of twenty genuine transported links", links_valid)

    fingerprints_match = True
    agreements = 0
    disagreements = 0
    for p, q in combinations(points, 2):
        common = tuple(point for point in points if point not in (p, q))
        left_edges = {
            frozenset((a, b)): links[p][canonical((q, a, b))]
            for a, b in combinations(common, 2)
        }
        right_edges = {
            frozenset((a, b)): links[q][canonical((p, a, b))]
            for a, b in combinations(common, 2)
        }
        fingerprints_match &= local_exact_h(common, left_edges) == local_exact_h(
            common, right_edges
        )
        for a, b in combinations(common, 2):
            left_colour = links[p][canonical((q, a, b))]
            right_colour = links[q][canonical((p, a, b))]
            if left_colour == right_colour:
                agreements += 1
            else:
                disagreements += 1

    comparisons = agreements + disagreements
    check("all 190 overlap-resolved exact-H fingerprints agree", fingerprints_match)
    check(
        "pseudogluing comparison census is 1,592 agree and 27,478 disagree",
        agreements == 1592 and disagreements == 27478,
    )
    check(
        "29,070 counts pairwise comparisons, six per one of 4,845 quadruples",
        comparisons == 29070 == 6 * comb(20, 4) == comb(20, 2) * comb(18, 2),
    )


def random_matching(
    vertices: list[int],
    edges: set[Edge],
    rng: random.Random,
) -> Factor | None:
    if not vertices:
        return frozenset()
    first = min(vertices)
    partners = [
        other
        for other in vertices
        if other != first and frozenset((first, other)) in edges
    ]
    rng.shuffle(partners)
    for partner in partners:
        remaining = [vertex for vertex in vertices if vertex not in (first, partner)]
        tail = random_matching(remaining, edges, rng)
        if tail is not None:
            return tail | {frozenset((first, partner))}
    return None


def random_factorization(n: int, rng: random.Random) -> Factorization:
    """The exact deterministic-seed generator used in the 3,000-OF audit."""
    while True:
        remaining = set(frozenset(edge) for edge in combinations(range(n), 2))
        factors: Factorization = []
        for _ in range(n - 1):
            factor = random_matching(list(range(n)), remaining, rng)
            if factor is None:
                break
            factors.append(factor)
            remaining -= factor
        if len(factors) == n - 1 and not remaining:
            return factors


def validate_factorization(factors: Factorization, n: int) -> dict[Edge, int]:
    edge_colours = {
        edge: colour for colour, factor in enumerate(factors) for edge in factor
    }
    if set(edge_colours) != set(frozenset(edge) for edge in combinations(range(n), 2)):
        raise AssertionError("factorization does not cover K_n exactly")
    for factor in factors:
        degrees: Counter[int] = Counter(vertex for edge in factor for vertex in edge)
        if degrees != Counter({vertex: 1 for vertex in range(n)}):
            raise AssertionError("factor is not a perfect matching")
    return edge_colours


def factorization_parity_vector(
    edge_colours: dict[Edge, int],
    type_index: dict[tuple[int, ...], int],
) -> int:
    vertices = tuple(range(18))
    vector = 0
    for a, b in combinations(vertices, 2):
        kind = cycle_type(holonomy(vertices, edge_colours, a, b))
        if kind not in type_index:
            raise AssertionError("holonomy outside the 55-type universe")
        vector ^= 1 << type_index[kind]
    return vector


def binary_rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def bit_parity(vector: int) -> int:
    """Parity of an integer bit mask (compatible with older Python 3)."""
    parity = 0
    while vector:
        parity ^= 1
        vector &= vector - 1
    return parity


def audit_affine_rank(types: list[tuple[int, ...]], samples: int) -> None:
    if samples < 1:
        raise ValueError("samples must be positive")
    rng = random.Random(932741)
    type_index = {kind: index for index, kind in enumerate(types)}
    all_ones = (1 << len(types)) - 1
    odd_twos = sum(1 << index for index, kind in enumerate(types) if kind.count(2) % 2)
    if odd_twos in (0, all_ones):
        raise AssertionError("the two universal affine masks must be independent")

    vectors: list[int] = []
    masks_ok = True
    for _ in range(samples):
        factorization = random_factorization(18, rng)
        edge_colours = validate_factorization(factorization, 18)
        vector = factorization_parity_vector(edge_colours, type_index)
        vectors.append(vector)
        masks_ok &= bit_parity(vector & all_ones) == 1
        masks_ok &= bit_parity(vector & odd_twos) == 0

    differences = [vector ^ vectors[0] for vector in vectors[1:]]
    rank = binary_rank(differences)
    check(
        f"{samples} generated K18 objects are independently valid one-factorizations",
        len(vectors) == samples,
    )
    check(
        "every sampled parity vector obeys total=1 and weighted-m2=0 mod 2",
        masks_ok,
    )
    check(
        f"the {samples} deterministic parity vectors are all distinct",
        len(set(vectors)) == samples,
    )
    if samples == 128:
        check("the fast 128-sample affine rank is reproducibly 51", rank == 51)
    elif samples == 3000:
        check("the reported 3,000-sample affine rank is 53", rank == 53)
        check(
            "rank 53 is maximal under the two independent affine equations",
            rank == len(types) - 2 == 53,
        )
    else:
        check(
            f"the {samples}-sample affine rank does not exceed the bound 53",
            rank <= len(types) - 2 == 53,
        )
    print(
        "      affine experiment: "
        f"seed=932741 samples={samples} distinct={len(set(vectors))} rank={rank}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sample_group = parser.add_mutually_exclusive_group()
    sample_group.add_argument(
        "--full",
        action="store_true",
        help="replay the exact reported 3,000-factorization experiment",
    )
    sample_group.add_argument(
        "--samples",
        type=int,
        help="override the default deterministic affine sample size of 128",
    )
    scope_group = parser.add_mutually_exclusive_group()
    scope_group.add_argument(
        "--core-only",
        action="store_true",
        help="skip the standalone K18 affine-rank experiment",
    )
    scope_group.add_argument(
        "--affine-only",
        action="store_true",
        help="run only the standalone K18 affine-rank experiment",
    )
    return parser.parse_args()


def main() -> None:
    if not __debug__:
        raise SystemExit("do not run this verifier with python -O")
    args = parse_args()

    colouring = construct_cyclic_ls19()
    if args.affine_only:
        types = [(*parts, 1) for parts in fixed_point_free_partitions(16)]
    else:
        verify_large_set(colouring)
        census, _exact, root_odd_counts, roots = audit_holonomies(colouring)
        types = audit_type_count(census)
        audit_cross_root_cocycle(roots)
        audit_augmented_cocycle(roots)
        audit_tournament(colouring, roots, root_odd_counts)
        audit_two_cycle_double_count(census, roots)
        audit_pseudogluing(colouring)

    if args.affine_only or not args.core_only:
        samples = 3000 if args.full else (args.samples or 128)
        audit_affine_rank(types, samples)

    failed = [name for name, passed in CHECKS if not passed]
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed")
    if failed:
        for name in failed:
            print("  FAILED:", name)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
