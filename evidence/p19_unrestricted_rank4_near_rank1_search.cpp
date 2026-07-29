#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Search the rank-one second-moment branch of the p-vertex rank-two near-link.
//
// Put the zero-missing singleton at projective infinity, normalized to (1,0).
// If Q(x)=sum_i det(x,v_i)^2 has rank one, Q=kappa*y^2.  The paired
// directions can then be written (t,1), and the row moment identity implies
// that the squares of the 18 endpoint scales consist of every nonzero square
// exactly twice.  Also
//     sum_g (a_g^2+b_g^2) = sum_g t_g(a_g^2+b_g^2) = 0.
// The first equality is automatic from the scale multiset; this search solves
// the second equality for the final direction after every move.
//
// This remains a heuristic search in a rigorously derived subfamily.

using Point = std::array<int, 2>;

static int mod(int value, int p) {
    value %= p;
    return value < 0 ? value + p : value;
}

static int inverse(int value, int p) {
    int result = 1;
    for (int exponent = p - 2; exponent; exponent >>= 1) {
        if (exponent & 1) result = mod(result * value, p);
        value = mod(value * value, p);
    }
    return result;
}

struct State {
    int p;
    int pairs;
    std::vector<int> scales;
    std::vector<int> directions;
    std::vector<int> order;

    int weight(int group) const {
        const int left = scales[2 * group];
        const int right = scales[2 * group + 1];
        return mod(left * left + right * right, p);
    }

    bool solve_last_direction() {
        int partial = 0;
        for (int group = 0; group + 1 < pairs; ++group) {
            partial = mod(partial + weight(group) * directions[group], p);
        }
        const int last_weight = weight(pairs - 1);
        if (last_weight == 0) return false;
        directions[pairs - 1] =
            mod(-partial * inverse(last_weight, p), p);
        for (int left = 0; left < pairs; ++left) {
            for (int right = left + 1; right < pairs; ++right) {
                if (directions[left] == directions[right]) return false;
            }
        }
        return true;
    }

    Point token_point(int token) const {
        if (token == 2 * pairs) return {1, 0};
        const int group = token / 2;
        const int scale = scales[token];
        return {
            mod(scale * directions[group], p),
            scale
        };
    }

    int kappa() const {
        int result = 1;  // singleton (1,0) contributes to sum a_i^2.
        for (int group = 0; group < pairs; ++group) {
            result = mod(
                result
                + weight(group) * directions[group] * directions[group],
                p
            );
        }
        return result;
    }
};

static int determinant(const Point& left, const Point& right, int p) {
    return mod(left[0] * right[1] - left[1] * right[0], p);
}

static int edge_label(
    const State& state, int left, int right
) {
    if (left > right) std::swap(left, right);
    return determinant(
        state.token_point(state.order[left]),
        state.token_point(state.order[right]),
        state.p
    );
}

static int row_score(const State& state, int vertex) {
    std::vector<int> count(state.p);
    for (int other = 0; other < state.p; ++other) {
        if (other != vertex) {
            ++count[edge_label(state, vertex, other)];
        }
    }
    int answer = 0;
    for (int multiplicity : count) {
        answer += multiplicity * (multiplicity - 1) / 2;
    }
    return answer;
}

static int raw_score(const State& state) {
    int answer = 0;
    for (int vertex = 0; vertex < state.p; ++vertex) {
        answer += row_score(state, vertex);
    }
    return answer;
}

static bool is_nonzero_square(int value, int p) {
    value = mod(value, p);
    if (value == 0) return false;
    int power = 1;
    for (int exponent = 0; exponent < (p - 1) / 2; ++exponent) {
        power = mod(power * value, p);
    }
    return power == 1;
}

static int objective(const State& state) {
    // Q=kappa*y^2 must take negative-square values on all paired
    // directions, so -kappa must be a nonzero square.
    const int moment_penalty =
        is_nonzero_square(-state.kappa(), state.p) ? 0 : 12;
    return raw_score(state) + moment_penalty;
}

static void print_witness(const State& state) {
    std::cout << "V = [\n";
    for (int token : state.order) {
        const Point value = state.token_point(token);
        std::cout << "  [" << value[0] << ", " << value[1] << "],\n";
    }
    std::cout << "]\nmissing = [";
    for (int vertex = 0; vertex < state.p; ++vertex) {
        std::vector<bool> seen(state.p);
        for (int other = 0; other < state.p; ++other) {
            if (other != vertex) {
                seen[edge_label(state, vertex, other)] = true;
            }
        }
        int missing = -1;
        for (int value = 0; value < state.p; ++value) {
            if (!seen[value]) {
                if (missing != -1) {
                    std::cerr << "candidate is not a witness\n";
                    return;
                }
                missing = value;
            }
        }
        if (vertex) std::cout << ", ";
        std::cout << missing;
    }
    std::cout << "]\n";
}

int main(int argc, char** argv) {
    const int p = argc > 1 ? std::atoi(argv[1]) : 19;
    const double seconds = argc > 2 ? std::atof(argv[2]) : 300.0;
    const std::uint64_t seed = argc > 3
        ? std::strtoull(argv[3], nullptr, 10) : 190835ULL;
    if (p < 5 || p % 4 != 3) {
        std::cerr << "this normalization expects a prime p == 3 mod 4\n";
        return 2;
    }

    const int pairs = (p - 1) / 2;
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    int global_raw_best = 1 << 30;
    State global_state{p, pairs, {}, {}, {}};
    std::uint64_t iterations = 0;
    int restart = 0;

    while (elapsed() < seconds) {
        ++restart;
        State state{p, pairs, {}, std::vector<int>(pairs), {}};
        for (int magnitude = 1; magnitude <= pairs; ++magnitude) {
            state.scales.push_back(
                (rng() & 1U) ? magnitude : p - magnitude
            );
            state.scales.push_back(
                (rng() & 1U) ? magnitude : p - magnitude
            );
        }
        std::shuffle(state.scales.begin(), state.scales.end(), rng);

        do {
            std::vector<int> slope_pool(p);
            for (int value = 0; value < p; ++value) slope_pool[value] = value;
            std::shuffle(slope_pool.begin(), slope_pool.end(), rng);
            for (int group = 0; group + 1 < pairs; ++group) {
                state.directions[group] = slope_pool[group];
            }
        } while (!state.solve_last_direction());

        state.order.resize(p);
        for (int token = 0; token < p; ++token) state.order[token] = token;
        std::shuffle(state.order.begin(), state.order.end(), rng);

        int current = objective(state);
        const int steps = 420000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const State old = state;
            const int kind = static_cast<int>(rng() % 18);
            if (kind < 8) {
                int left = static_cast<int>(rng() % p);
                int right = left;
                while (right == left) right = static_cast<int>(rng() % p);
                std::swap(state.order[left], state.order[right]);
            } else if (kind < 13) {
                const int left = static_cast<int>(rng() % (p - 1));
                int right = left;
                while (right == left) {
                    right = static_cast<int>(rng() % (p - 1));
                }
                std::swap(state.scales[left], state.scales[right]);
            } else if (kind < 16) {
                const int token = static_cast<int>(rng() % (p - 1));
                state.scales[token] = mod(-state.scales[token], p);
            } else {
                const int group =
                    static_cast<int>(rng() % (pairs - 1));
                int replacement = static_cast<int>(rng() % p);
                state.directions[group] = replacement;
            }

            bool valid = state.solve_last_direction();
            int candidate = valid ? objective(state) : 1 << 20;
            const double fraction = static_cast<double>(step) / steps;
            const double temperature =
                2.6 * std::pow(0.01 / 2.6, fraction);
            const int delta = candidate - current;
            if (valid
                && (delta <= 0
                    || real(rng) < std::exp(-delta / temperature))) {
                current = candidate;
            } else {
                state = old;
            }

            if (step % 127 == 0) {
                // Exhaustively optimize the sign of one endpoint scale.
                const int token = static_cast<int>(rng() % (p - 1));
                const State before = state;
                state.scales[token] = mod(-state.scales[token], p);
                if (state.solve_last_direction()) {
                    const int flipped = objective(state);
                    if (flipped < current) {
                        current = flipped;
                    } else {
                        state = before;
                    }
                } else {
                    state = before;
                }
            }

            const int candidate_raw = raw_score(state);
            if (current < global_best
                || (current == global_best
                    && candidate_raw < global_raw_best)) {
                global_best = current;
                global_raw_best = candidate_raw;
                global_state = state;
                std::cerr << "p=" << p << " rank1-near-best="
                          << global_best << " raw=" << global_raw_best
                          << " kappa=" << state.kappa()
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
            }
            if (candidate_raw == 0 && current == 0) {
                print_witness(state);
                return 0;
            }
        }
    }

    std::cerr << "NO WITNESS (heuristic only); objective=" << global_best
              << " raw=" << global_raw_best
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (global_raw_best == 0) print_witness(global_state);
    return 1;
}
