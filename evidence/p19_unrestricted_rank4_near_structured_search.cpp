#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Heuristic search for a p-vertex rank-two near-link, with the forced zero
// structure built in.  In any proper p-edge-colouring of K_p by F_p, every
// colour class is a maximum matching.  Thus determinant-zero consists of
// (p-1)/2 parallel pairs and one singleton.

using Point = std::array<int, 2>;

struct Token {
    int direction;
    int scale;
};

static int mod(int value, int p) {
    value %= p;
    return value < 0 ? value + p : value;
}

static Point representative(int direction, int p) {
    return direction == p ? Point{0, 1} : Point{1, direction};
}

static Point point(const Token& token, int p) {
    const Point base = representative(token.direction, p);
    return {mod(token.scale * base[0], p), mod(token.scale * base[1], p)};
}

static int determinant(const Point& left, const Point& right, int p) {
    return mod(left[0] * right[1] - left[1] * right[0], p);
}

static int edge_label(
    const std::vector<Token>& order, int left, int right, int p
) {
    if (left > right) std::swap(left, right);
    return determinant(point(order[left], p), point(order[right], p), p);
}

static int row_score(
    const std::vector<Token>& order, int vertex, int p
) {
    std::vector<int> count(p);
    for (int other = 0; other < p; ++other) {
        if (other != vertex) {
            ++count[edge_label(order, vertex, other, p)];
        }
    }
    int answer = 0;
    for (int multiplicity : count) {
        answer += multiplicity * (multiplicity - 1) / 2;
    }
    return answer;
}

static int score(const std::vector<Token>& order, int p) {
    int answer = 0;
    for (int vertex = 0; vertex < p; ++vertex) {
        answer += row_score(order, vertex, p);
    }
    return answer;
}

static void print_witness(const std::vector<Token>& order, int p) {
    std::cout << "V = [\n";
    for (const Token& token : order) {
        const Point value = point(token, p);
        std::cout << "  [" << value[0] << ", " << value[1] << "],\n";
    }
    std::cout << "]\nmissing = [";
    for (int vertex = 0; vertex < p; ++vertex) {
        std::vector<bool> seen(p);
        for (int other = 0; other < p; ++other) {
            if (other != vertex) {
                seen[edge_label(order, vertex, other, p)] = true;
            }
        }
        int missing = -1;
        for (int value = 0; value < p; ++value) {
            if (!seen[value]) {
                if (missing != -1) {
                    std::cerr << "best candidate is not a witness\n";
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
    if (p < 5 || p % 2 == 0) {
        std::cerr << "p must be odd and at least 5\n";
        return 2;
    }

    const int pairs = (p - 1) / 2;
    const int groups = pairs + 1;
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    std::vector<Token> global_order;
    std::uint64_t iterations = 0;
    int restart = 0;

    while (elapsed() < seconds) {
        ++restart;
        std::vector<int> directions(p + 1);
        for (int index = 0; index <= p; ++index) directions[index] = index;
        std::shuffle(directions.begin(), directions.end(), rng);
        directions.resize(groups);

        std::vector<Token> order;
        for (int group = 0; group < pairs; ++group) {
            order.push_back(
                {directions[group], 1 + static_cast<int>(rng() % (p - 1))}
            );
            order.push_back(
                {directions[group], 1 + static_cast<int>(rng() % (p - 1))}
            );
        }
        order.push_back(
            {directions.back(), 1 + static_cast<int>(rng() % (p - 1))}
        );
        std::shuffle(order.begin(), order.end(), rng);

        int current = score(order, p);
        const int steps = 360000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const int kind = static_cast<int>(rng() % 16);
            const int left = static_cast<int>(rng() % p);
            int right = left;
            while (right == left) right = static_cast<int>(rng() % p);
            const Token old_left = order[left];
            const Token old_right = order[right];

            int changed_direction = -1;
            if (kind < 7) {
                std::swap(order[left], order[right]);
            } else if (kind < 13) {
                int replacement = 1 + static_cast<int>(rng() % (p - 2));
                if (replacement >= order[left].scale) ++replacement;
                order[left].scale = replacement;
            } else {
                changed_direction = order[left].direction;
                std::vector<bool> used(p + 1);
                for (const Token& token : order) used[token.direction] = true;
                std::vector<int> unused;
                for (int direction = 0; direction <= p; ++direction) {
                    if (!used[direction]) unused.push_back(direction);
                }
                const int replacement =
                    unused[static_cast<std::size_t>(rng() % unused.size())];
                for (Token& token : order) {
                    if (token.direction == changed_direction) {
                        token.direction = replacement;
                    }
                }
            }

            const int candidate = score(order, p);
            const double fraction = static_cast<double>(step) / steps;
            const double temperature =
                2.8 * std::pow(0.012 / 2.8, fraction);
            const int delta = candidate - current;
            if (delta <= 0 || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else if (changed_direction != -1) {
                const int replacement = order[left].direction;
                for (Token& token : order) {
                    if (token.direction == replacement) {
                        token.direction = changed_direction;
                    }
                }
            } else {
                order[left] = old_left;
                order[right] = old_right;
            }

            // Exact scale descent: scaling one vector does not change its own
            // collision pattern, but it can repair one edge in every other row.
            if (step % 97 == 0 && current != 0) {
                int target = static_cast<int>(rng() % p);
                int worst = row_score(order, target, p);
                for (int trial = 0; trial < p; ++trial) {
                    const int candidate_vertex = static_cast<int>(rng() % p);
                    const int candidate_score =
                        row_score(order, candidate_vertex, p);
                    if (candidate_score > worst) {
                        target = candidate_vertex;
                        worst = candidate_score;
                    }
                }
                const int old_scale = order[target].scale;
                int best_scale = old_scale;
                int best = current;
                for (int scale = 1; scale < p; ++scale) {
                    order[target].scale = scale;
                    const int trial_score = score(order, p);
                    if (trial_score < best) {
                        best = trial_score;
                        best_scale = scale;
                    }
                }
                order[target].scale = best_scale;
                current = best;
            }

            if (current < global_best) {
                global_best = current;
                global_order = order;
                std::cerr << "p=" << p << " structured-near-best="
                          << global_best << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
            }
            if (current == 0) {
                print_witness(order, p);
                return 0;
            }
        }
    }

    std::cerr << "NO WITNESS (heuristic only); best=" << global_best
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (global_best == 0) print_witness(global_order, p);
    return 1;
}
