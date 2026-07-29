#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Fast heuristic companion to p19_unrestricted_rank4_half_labels_cpsat.py.
// It searches both the nine factor magnitudes and the 36 unfixed edge signs
// of the round-robin one-factorization, using all 210 principal 6-Pfaffians
// as the objective.  A score of zero is an exact rank-at-most-four witness;
// any positive score has no mathematical no-go status.

static constexpr int P = 19;
static constexpr int N = 10;
static constexpr int EDGES = 45;
static constexpr int FACTORS = 9;

struct Term {
    int sign;
    std::array<int, 3> edges;
};

struct Pfaffian {
    std::array<int, 15> terms;
};

static int mod(int value) {
    value %= P;
    return value < 0 ? value + P : value;
}

static int distance_zero(int value) {
    value = mod(value);
    return std::min(value, P - value);
}

static std::vector<std::pair<int, int>> all_edges() {
    std::vector<std::pair<int, int>> result;
    for (int left = 0; left < N; ++left) {
        for (int right = left + 1; right < N; ++right) {
            result.emplace_back(left, right);
        }
    }
    return result;
}

static std::vector<int> factorization(
    const std::vector<std::pair<int, int>>& edges
) {
    std::vector<int> factor(EDGES, -1);
    for (int round = 0; round < 9; ++round) {
        std::vector<std::pair<int, int>> pairs{{9, round}};
        for (int offset = 1; offset <= 4; ++offset) {
            pairs.emplace_back(
                (round + offset) % 9,
                (round - offset + 9) % 9
            );
        }
        for (auto [left, right] : pairs) {
            if (left > right) std::swap(left, right);
            const auto iterator =
                std::find(edges.begin(), edges.end(), std::pair{left, right});
            factor[static_cast<int>(iterator - edges.begin())] = round;
        }
    }
    return factor;
}

static void enumerate_matchings(
    const std::vector<int>& vertices,
    const std::vector<std::pair<int, int>>& edges,
    int sign,
    std::vector<int> chosen,
    std::vector<Term>& terms
) {
    if (vertices.empty()) {
        terms.push_back({sign, {chosen[0], chosen[1], chosen[2]}});
        return;
    }
    const int first = vertices[0];
    for (int position = 1; position < static_cast<int>(vertices.size());
         ++position) {
        const int second = vertices[position];
        auto edge_iterator = std::find(
            edges.begin(), edges.end(),
            std::pair{std::min(first, second), std::max(first, second)}
        );
        std::vector<int> remainder;
        for (int index = 1; index < static_cast<int>(vertices.size()); ++index) {
            if (index != position) remainder.push_back(vertices[index]);
        }
        auto next = chosen;
        next.push_back(static_cast<int>(edge_iterator - edges.begin()));
        enumerate_matchings(
            remainder, edges,
            position % 2 == 1 ? sign : -sign,
            std::move(next), terms
        );
    }
}

struct SearchState {
    std::array<int, FACTORS> magnitude{};
    std::array<int, EDGES> edge_sign{};
    std::vector<int> term_value;
    std::vector<int> pfaffian_value;
    int objective = 0;
    int nonzero = 0;
};

static int contribution(int value) {
    const int distance = distance_zero(value);
    return (value % P == 0 ? 0 : 20) + distance * distance;
}

static void recompute(
    SearchState& state,
    const std::vector<int>& edge_factor,
    const std::vector<Term>& terms,
    const std::vector<Pfaffian>& pfaffians
) {
    state.term_value.resize(terms.size());
    for (int index = 0; index < static_cast<int>(terms.size()); ++index) {
        int value = terms[index].sign;
        for (int edge : terms[index].edges) {
            value = mod(
                value
                * state.magnitude[edge_factor[edge]]
                * state.edge_sign[edge]
            );
        }
        state.term_value[index] = value;
    }
    state.pfaffian_value.assign(pfaffians.size(), 0);
    state.objective = 0;
    state.nonzero = 0;
    for (int pf = 0; pf < static_cast<int>(pfaffians.size()); ++pf) {
        int value = 0;
        for (int term : pfaffians[pf].terms) {
            value = mod(value + state.term_value[term]);
        }
        state.pfaffian_value[pf] = value;
        state.objective += contribution(value);
        state.nonzero += value != 0;
    }
}

static int rank_mod(std::array<std::array<int, N>, N> matrix) {
    int rank = 0;
    for (int column = 0; column < N; ++column) {
        int pivot = rank;
        while (pivot < N && matrix[pivot][column] == 0) ++pivot;
        if (pivot == N) continue;
        std::swap(matrix[pivot], matrix[rank]);
        int inverse = 1;
        for (int exponent = P - 2, base = matrix[rank][column];
             exponent; exponent >>= 1, base = mod(base * base)) {
            if (exponent & 1) inverse = mod(inverse * base);
        }
        for (int entry = 0; entry < N; ++entry) {
            matrix[rank][entry] = mod(matrix[rank][entry] * inverse);
        }
        for (int row = 0; row < N; ++row) {
            if (row == rank || matrix[row][column] == 0) continue;
            const int multiplier = matrix[row][column];
            for (int entry = 0; entry < N; ++entry) {
                matrix[row][entry] =
                    mod(matrix[row][entry] - multiplier * matrix[rank][entry]);
            }
        }
        ++rank;
    }
    return rank;
}

static void print_witness(
    const SearchState& state,
    const std::vector<std::pair<int, int>>& edges,
    const std::vector<int>& edge_factor
) {
    std::array<std::array<int, N>, N> matrix{};
    for (int edge = 0; edge < EDGES; ++edge) {
        const auto [left, right] = edges[edge];
        const int value = mod(
            state.edge_sign[edge] * state.magnitude[edge_factor[edge]]
        );
        matrix[left][right] = value;
        matrix[right][left] = mod(-value);
    }
    std::cout << "factor_magnitudes = [";
    for (int factor = 0; factor < FACTORS; ++factor) {
        if (factor) std::cout << ", ";
        std::cout << state.magnitude[factor];
    }
    std::cout << "]\nA = [\n";
    for (const auto& row : matrix) {
        std::cout << "  [";
        for (int column = 0; column < N; ++column) {
            if (column) std::cout << ", ";
            std::cout << row[column];
        }
        std::cout << "],\n";
    }
    std::cout << "]\nrank=" << rank_mod(matrix) << "\n";
}

int main(int argc, char** argv) {
    const double seconds = argc > 1 ? std::atof(argv[1]) : 300.0;
    const std::uint64_t seed = argc > 2
        ? std::strtoull(argv[2], nullptr, 10) : 190835ULL;
    const auto edges = all_edges();
    const auto edge_factor = factorization(edges);

    std::vector<Term> terms;
    std::vector<Pfaffian> pfaffians;
    for (int mask = 0; mask < (1 << N); ++mask) {
        if (__builtin_popcount(static_cast<unsigned>(mask)) != 6) continue;
        std::vector<int> vertices;
        for (int vertex = 0; vertex < N; ++vertex) {
            if (mask & (1 << vertex)) vertices.push_back(vertex);
        }
        std::vector<Term> local_terms;
        enumerate_matchings(vertices, edges, 1, {}, local_terms);
        Pfaffian pf{};
        for (int index = 0; index < 15; ++index) {
            pf.terms[index] = static_cast<int>(terms.size());
            terms.push_back(local_terms[index]);
        }
        pfaffians.push_back(pf);
    }

    std::array<std::vector<std::pair<int, int>>, EDGES> incidence;
    for (int pf = 0; pf < static_cast<int>(pfaffians.size()); ++pf) {
        for (int local = 0; local < 15; ++local) {
            const int term = pfaffians[pf].terms[local];
            for (int edge : terms[term].edges) {
                incidence[edge].emplace_back(pf, term);
            }
        }
    }

    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    int global_nonzero = 211;
    SearchState global_state;
    std::uint64_t iterations = 0;
    int restart = 0;
    while (elapsed() < seconds) {
        ++restart;
        SearchState state;
        for (int factor = 0; factor < FACTORS; ++factor) {
            state.magnitude[factor] = factor + 1;
        }
        std::shuffle(state.magnitude.begin(), state.magnitude.end(), rng);
        for (int edge = 0; edge < EDGES; ++edge) {
            state.edge_sign[edge] = (edges[edge].first == 0 || (rng() & 1U))
                ? 1 : -1;
        }
        recompute(state, edge_factor, terms, pfaffians);

        const int steps = 900000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const int current_objective = state.objective;
            const bool magnitude_move = (rng() % 20) == 0;
            const SearchState old = magnitude_move ? state : SearchState{};
            int edge = -1;
            int first_factor = -1;
            int second_factor = -1;
            int candidate_objective = state.objective;
            int candidate_nonzero = state.nonzero;

            if (magnitude_move) {
                first_factor = static_cast<int>(rng() % FACTORS);
                second_factor = first_factor;
                while (second_factor == first_factor) {
                    second_factor = static_cast<int>(rng() % FACTORS);
                }
                std::swap(
                    state.magnitude[first_factor],
                    state.magnitude[second_factor]
                );
                recompute(state, edge_factor, terms, pfaffians);
                candidate_objective = state.objective;
                candidate_nonzero = state.nonzero;
            } else {
                do {
                    edge = static_cast<int>(rng() % EDGES);
                } while (edges[edge].first == 0);
                std::vector<int> delta(pfaffians.size());
                std::vector<bool> touched(pfaffians.size());
                for (const auto [pf, term] : incidence[edge]) {
                    delta[pf] = mod(delta[pf] - 2 * state.term_value[term]);
                    touched[pf] = true;
                }
                for (int pf = 0; pf < static_cast<int>(pfaffians.size()); ++pf) {
                    if (!touched[pf]) continue;
                    const int old_value = state.pfaffian_value[pf];
                    const int new_value = mod(old_value + delta[pf]);
                    candidate_objective +=
                        contribution(new_value) - contribution(old_value);
                    candidate_nonzero +=
                        static_cast<int>(new_value != 0)
                        - static_cast<int>(old_value != 0);
                }
            }

            const double fraction = static_cast<double>(step) / steps;
            const double temperature =
                120.0 * std::pow(0.08 / 120.0, fraction);
            const int change = candidate_objective - current_objective;
            const bool accept =
                change <= 0 || real(rng) < std::exp(-change / temperature);

            if (magnitude_move) {
                if (!accept) state = old;
            } else if (accept) {
                state.edge_sign[edge] *= -1;
                for (const auto [pf, term] : incidence[edge]) {
                    state.term_value[term] = mod(-state.term_value[term]);
                }
                std::vector<bool> touched(pfaffians.size());
                for (const auto [pf, term] : incidence[edge]) {
                    (void)term;
                    touched[pf] = true;
                }
                for (int pf = 0; pf < static_cast<int>(pfaffians.size()); ++pf) {
                    if (!touched[pf]) continue;
                    int value = 0;
                    for (int term : pfaffians[pf].terms) {
                        value = mod(value + state.term_value[term]);
                    }
                    state.pfaffian_value[pf] = value;
                }
                state.objective = candidate_objective;
                state.nonzero = candidate_nonzero;
            }

            if (state.objective < global_best
                || (state.objective == global_best
                    && state.nonzero < global_nonzero)) {
                global_best = state.objective;
                global_nonzero = state.nonzero;
                global_state = state;
                std::cerr << "half-label-best objective=" << global_best
                          << " nonzero6pf=" << global_nonzero
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
            }
            if (state.nonzero == 0) {
                print_witness(state, edges, edge_factor);
                return 0;
            }
        }
    }
    std::cerr << "NO WITNESS (heuristic only); objective=" << global_best
              << " nonzero6pf=" << global_nonzero
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (global_nonzero == 0) print_witness(global_state, edges, edge_factor);
    return 1;
}
