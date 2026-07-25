#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Heuristic construction search for the nonorthogonal-endpoint branch of
// the unrestricted p=19 rank-four ordered link.
//
// We normalize u_0=e_1, u_19=f_1 with <e_1,f_1>=1.  For the middle vectors
//
//   u_i=(y_i,s_i,x_i,t_i),
//
// both (x_i) and (y_i) must be permutations of F_19\{1}; this makes the
// first and last displayed rows exact by construction.  The remaining
// pairing is
//
//   <u_i,u_j> = y_i x_j-x_i y_j+s_i t_j-t_i s_j.
//
// A score-zero output is a genuine unrestricted rank-at-most-four link and
// is verified before being printed.  Failure is heuristic only.

static constexpr int P = 19;
static constexpr int N = 20;
static constexpr int FIRST_MIDDLE = 1;
static constexpr int LAST_MIDDLE = 18;

using Vec = std::array<int, 4>;
using Configuration = std::array<Vec, N>;

static int mod(int value) {
    value %= P;
    return value < 0 ? value + P : value;
}

static int pairing(const Vec& left, const Vec& right) {
    return mod(
        left[0] * right[2] - left[2] * right[0]
        + left[1] * right[3] - left[3] * right[1]
    );
}

static int displayed(
    const Configuration& vectors, int left, int right
) {
    if (left > right) std::swap(left, right);
    return pairing(vectors[left], vectors[right]);
}

static int row_score(const Configuration& vectors, int row) {
    std::array<int, P> count{};
    for (int other = 0; other < N; ++other) {
        if (other != row) ++count[displayed(vectors, row, other)];
    }
    int answer = 0;
    for (int multiplicity : count) {
        answer += multiplicity * (multiplicity - 1) / 2;
    }
    return answer;
}

static int score(const Configuration& vectors) {
    int answer = 0;
    for (int row = 0; row < N; ++row) answer += row_score(vectors, row);
    return answer;
}

static bool verify(const Configuration& vectors) {
    if (pairing(vectors[0], vectors[19]) != 1) return false;
    for (int row = 0; row < N; ++row) {
        std::array<bool, P> seen{};
        for (int other = 0; other < N; ++other) {
            if (other == row) continue;
            const int value = displayed(vectors, row, other);
            if (seen[value]) return false;
            seen[value] = true;
        }
        if (std::find(seen.begin(), seen.end(), false) != seen.end()) {
            return false;
        }
    }
    return true;
}

static void print_witness(const Configuration& vectors) {
    std::cout << "U = [\n";
    for (const auto& vector : vectors) {
        std::cout << "  [" << vector[0] << "," << vector[1] << ","
                  << vector[2] << "," << vector[3] << "],\n";
    }
    std::cout << "]\n";
    std::cout << "verification="
              << (verify(vectors) ? "PASS" : "FAIL") << "\n";
}

int main(int argc, char** argv) {
    const double seconds = argc > 1 ? std::atof(argv[1]) : 600.0;
    const std::uint64_t seed = argc > 2
        ? std::strtoull(argv[2], nullptr, 10) : 190419ULL;
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start
        ).count();
    };

    int global_best = 1 << 30;
    Configuration global_vectors{};
    std::uint64_t iterations = 0;
    int restarts = 0;

    while (elapsed() < seconds) {
        ++restarts;
        Configuration vectors{};
        vectors[0] = {1, 0, 0, 0};
        vectors[19] = {0, 0, 1, 0};
        std::vector<int> x_values, y_values;
        for (int value = 0; value < P; ++value) {
            if (value != 1) {
                x_values.push_back(value);
                y_values.push_back(value);
            }
        }
        std::shuffle(x_values.begin(), x_values.end(), rng);
        std::shuffle(y_values.begin(), y_values.end(), rng);
        for (int vertex = FIRST_MIDDLE; vertex <= LAST_MIDDLE; ++vertex) {
            vectors[vertex] = {
                y_values[vertex - 1],
                static_cast<int>(rng() % P),
                x_values[vertex - 1],
                static_cast<int>(rng() % P)
            };
        }

        int current = score(vectors);
        static constexpr int STEPS = 240000;
        for (int step = 0; step < STEPS && elapsed() < seconds; ++step) {
            ++iterations;
            const double fraction = static_cast<double>(step) / STEPS;
            const double temperature =
                3.2 * std::pow(0.015 / 3.2, fraction);

            int first = FIRST_MIDDLE
                + static_cast<int>(rng() % (LAST_MIDDLE - FIRST_MIDDLE + 1));
            if ((rng() & 3U) != 0) {
                int total = 0;
                for (int vertex = FIRST_MIDDLE;
                     vertex <= LAST_MIDDLE; ++vertex) {
                    total += 1 + row_score(vectors, vertex);
                }
                int ticket = static_cast<int>(rng() % total);
                for (int vertex = FIRST_MIDDLE;
                     vertex <= LAST_MIDDLE; ++vertex) {
                    ticket -= 1 + row_score(vectors, vertex);
                    if (ticket < 0) {
                        first = vertex;
                        break;
                    }
                }
            }

            const int kind = static_cast<int>(rng() % 12);
            int second = first;
            while (second == first) {
                second = FIRST_MIDDLE
                    + static_cast<int>(
                        rng() % (LAST_MIDDLE - FIRST_MIDDLE + 1)
                    );
            }
            const Vec old_first = vectors[first];
            const Vec old_second = vectors[second];

            if (kind < 3) {
                std::swap(vectors[first][0], vectors[second][0]);
            } else if (kind < 6) {
                std::swap(vectors[first][2], vectors[second][2]);
            } else if (kind < 8) {
                std::swap(vectors[first][1], vectors[second][1]);
            } else if (kind < 10) {
                std::swap(vectors[first][3], vectors[second][3]);
            } else {
                const int coordinate = kind == 10 ? 1 : 3;
                int replacement = static_cast<int>(rng() % (P - 1));
                if (replacement >= vectors[first][coordinate]) ++replacement;
                vectors[first][coordinate] = replacement;
            }

            const int candidate = score(vectors);
            const int delta = candidate - current;
            if (delta <= 0
                || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else {
                vectors[first] = old_first;
                vectors[second] = old_second;
            }

            // Exact coordinate descent in the residual symplectic plane.
            if (step % 251 == 0 && current != 0) {
                const int target = FIRST_MIDDLE
                    + static_cast<int>(
                        rng() % (LAST_MIDDLE - FIRST_MIDDLE + 1)
                    );
                const int old_s = vectors[target][1];
                const int old_t = vectors[target][3];
                int best_s = old_s;
                int best_t = old_t;
                int best_score = current;
                for (int s = 0; s < P; ++s) {
                    for (int t = 0; t < P; ++t) {
                        vectors[target][1] = s;
                        vectors[target][3] = t;
                        const int candidate_score = score(vectors);
                        if (candidate_score < best_score) {
                            best_score = candidate_score;
                            best_s = s;
                            best_t = t;
                        }
                    }
                }
                vectors[target][1] = best_s;
                vectors[target][3] = best_t;
                current = best_score;
            }

            if (current < global_best) {
                global_best = current;
                global_vectors = vectors;
                std::cerr << "endpoint-rank4 best=" << global_best
                          << " restart=" << restarts
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
                if (global_best == 0) {
                    if (!verify(global_vectors)) {
                        std::cerr << "internal verification failed\n";
                        return 2;
                    }
                    print_witness(global_vectors);
                    return 0;
                }
            }
        }
    }

    std::cerr << "NO WITNESS (heuristic only); best=" << global_best
              << " restarts=" << restarts
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    print_witness(global_vectors);
    return 1;
}
