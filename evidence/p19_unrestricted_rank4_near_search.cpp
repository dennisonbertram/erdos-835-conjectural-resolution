#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Heuristic search for the rank-two "near link" that would lift to an
// unrestricted rank-four ordered link on p+1 vertices.
//
// We seek p ordered vectors v_i in F_p^2 such that the symmetric edge labels
//     C_ij = det(v_i,v_j), i<j,
// are distinct in every row.  Then every row misses one field element, and
// the missing elements are automatically all distinct: every colour class is
// a matching in K_p, hence has at most (p-1)/2 edges, while the p colour
// classes contain p(p-1)/2 edges in total.
//
// The normalization below covers:
//   (a) row 0 missing 0, with C_01=1; and
//   (b) row 0 missing 1, with C_01=r != 0,1.
// It does not cover the separate C_01=0 branch of (b).

using Point = std::array<int, 2>;

static int mod(int value, int p) {
    value %= p;
    return value < 0 ? value + p : value;
}

static int determinant(const Point& left, const Point& right, int p) {
    return mod(left[0] * right[1] - left[1] * right[0], p);
}

static int edge_label(
    const std::vector<Point>& points, int left, int right, int p
) {
    if (left > right) std::swap(left, right);
    return determinant(points[left], points[right], p);
}

static int row_score(
    const std::vector<Point>& points, int vertex, int p
) {
    std::vector<int> count(p);
    for (int other = 0; other < p; ++other) {
        if (other == vertex) continue;
        ++count[edge_label(points, vertex, other, p)];
    }
    int answer = 0;
    for (int multiplicity : count) {
        answer += multiplicity * (multiplicity - 1) / 2;
    }
    return answer;
}

static int score(const std::vector<Point>& points, int p) {
    int answer = 0;
    for (int vertex = 0; vertex < p; ++vertex) {
        answer += row_score(points, vertex, p);
    }
    return answer;
}

static void print_witness(const std::vector<Point>& points, int p) {
    std::cout << "V = [\n";
    for (const Point& point : points) {
        std::cout << "  [" << point[0] << ", " << point[1] << "],\n";
    }
    std::cout << "]\nmissing = [";
    for (int vertex = 0; vertex < p; ++vertex) {
        std::vector<bool> seen(p);
        for (int other = 0; other < p; ++other) {
            if (other != vertex) {
                seen[edge_label(points, vertex, other, p)] = true;
            }
        }
        int missing = -1;
        for (int value = 0; value < p; ++value) {
            if (!seen[value]) {
                if (missing != -1) {
                    std::cerr << "internal error: non-rainbow witness\n";
                    std::exit(2);
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
        std::cerr << "p must be an odd prime at least 5\n";
        return 2;
    }

    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    std::vector<Point> global_points;
    std::uint64_t iterations = 0;
    int restart = 0;

    while (elapsed() < seconds) {
        ++restart;
        // Roughly one quarter of restarts use the missing-zero branch.
        const bool missing_zero = (rng() & 3U) == 0;
        const int row0_missing = missing_zero ? 0 : 1;
        int r = 1;
        if (!missing_zero) {
            do {
                r = 1 + static_cast<int>(rng() % (p - 1));
            } while (r == 1);
        }

        std::vector<Point> points(p);
        points[0] = {1, 0};
        points[1] = {0, r};

        std::vector<int> y_pool;
        for (int value = 0; value < p; ++value) {
            if (value != row0_missing && value != r) y_pool.push_back(value);
        }
        std::shuffle(y_pool.begin(), y_pool.end(), rng);

        int excluded_x = 0;
        do {
            excluded_x = static_cast<int>(rng() % p);
        } while (excluded_x == p - 1);
        std::vector<int> x_pool;
        for (int value = 0; value < p; ++value) {
            if (value != p - 1 && value != excluded_x) {
                x_pool.push_back(value);
            }
        }
        std::shuffle(x_pool.begin(), x_pool.end(), rng);
        for (int index = 2; index < p; ++index) {
            points[index] = {x_pool[index - 2], y_pool[index - 2]};
        }

        int current = score(points, p);
        const int steps = 260000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const int kind = static_cast<int>(rng() % 12);
            const int left = 2 + static_cast<int>(rng() % (p - 2));
            int right = left;
            while (right == left) {
                right = 2 + static_cast<int>(rng() % (p - 2));
            }

            const Point old_left = points[left];
            const Point old_right = points[right];
            const int old_excluded_x = excluded_x;
            if (kind < 4) {
                std::swap(points[left][0], points[right][0]);
            } else if (kind < 8) {
                std::swap(points[left][1], points[right][1]);
            } else if (kind < 11) {
                std::swap(points[left], points[right]);
            } else {
                std::swap(points[left][0], excluded_x);
            }

            const int candidate = score(points, p);
            const double fraction = static_cast<double>(step) / steps;
            const double temperature =
                2.4 * std::pow(0.018 / 2.4, fraction);
            const int delta = candidate - current;
            if (delta <= 0 || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else {
                points[left] = old_left;
                points[right] = old_right;
                excluded_x = old_excluded_x;
            }

            // A small exact best-swap pass supplies a useful low-temperature
            // descent without changing the normalized search space.
            if (step % 503 == 0 && current != 0) {
                int best = current;
                int best_kind = -1;
                int best_left = -1;
                int best_right = -1;
                for (int trial = 0; trial < 96; ++trial) {
                    const int a = 2 + static_cast<int>(rng() % (p - 2));
                    int b = a;
                    while (b == a) {
                        b = 2 + static_cast<int>(rng() % (p - 2));
                    }
                    const int coordinate = static_cast<int>(rng() & 1U);
                    std::swap(points[a][coordinate], points[b][coordinate]);
                    const int trial_score = score(points, p);
                    std::swap(points[a][coordinate], points[b][coordinate]);
                    if (trial_score < best) {
                        best = trial_score;
                        best_kind = coordinate;
                        best_left = a;
                        best_right = b;
                    }
                }
                if (best_kind != -1) {
                    std::swap(points[best_left][best_kind],
                              points[best_right][best_kind]);
                    current = best;
                }
            }

            if (current < global_best) {
                global_best = current;
                global_points = points;
                std::cerr << "p=" << p << " near-best=" << global_best
                          << " missing0=" << row0_missing
                          << " r=" << r
                          << " excluded-x=" << excluded_x
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
            }
            if (current == 0) {
                print_witness(points, p);
                return 0;
            }
        }
    }

    std::cerr << "NO WITNESS (heuristic only); best=" << global_best
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (!global_points.empty()) print_witness(global_points, p);
    return 1;
}
