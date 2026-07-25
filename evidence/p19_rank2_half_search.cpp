#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// Heuristic search for the rank-two subfamily of the ten-point p=19
// sign-class half-link.  A witness here would feed the paired-doubling
// construction, and (with adjacent +/- copies) also gives a particularly
// symmetric determinant near-link.

using Vec = std::array<int, 2>;

static constexpr int P = 19;
static constexpr int N = 10;

static int mod(int value) {
    value %= P;
    return value < 0 ? value + P : value;
}

static int sign_class(int value) {
    value = mod(value);
    return std::min(value, P - value);
}

static int det(const Vec& x, const Vec& y) {
    return mod(x[0] * y[1] - x[1] * y[0]);
}

static int score(const std::array<Vec, N>& points) {
    int answer = 0;
    for (int i = 0; i < N; ++i) {
        std::array<int, 10> counts{};
        for (int j = 0; j < N; ++j) {
            if (i == j) continue;
            ++counts[sign_class(det(points[i], points[j]))];
        }
        answer += 20 * counts[0];
        for (int value = 1; value <= 9; ++value) {
            answer += counts[value] * (counts[value] - 1) / 2;
        }
    }
    // Distinct projective directions are necessary and keep the zero penalty
    // explicit even before a row collision is counted.
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            if (det(points[i], points[j]) == 0) answer += 20;
        }
    }
    return answer;
}

static void print_witness(const std::array<Vec, N>& points) {
    std::cout << "V = [\n";
    for (const auto& point : points) {
        std::cout << "  [" << point[0] << ", " << point[1] << "],\n";
    }
    std::cout << "]\n";
}

int main(int argc, char** argv) {
    const double seconds = argc > 1 ? std::atof(argv[1]) : 300.0;
    const std::uint64_t seed = argc > 2
        ? std::strtoull(argv[2], nullptr, 10) : 190219ULL;
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    std::array<Vec, N> global_points{};
    std::uint64_t iterations = 0;
    int restart = 0;
    while (elapsed() < seconds) {
        ++restart;
        std::array<Vec, N> points{};
        points[0] = {1, 0};
        points[1] = {0, 1};
        std::vector<int> a_classes, b_classes;
        for (int value = 2; value <= 9; ++value) {
            a_classes.push_back(value);
            b_classes.push_back(value);
        }
        std::shuffle(a_classes.begin(), a_classes.end(), rng);
        std::shuffle(b_classes.begin(), b_classes.end(), rng);
        for (int i = 2; i < N; ++i) {
            const int a = (rng() & 1U)
                ? a_classes[i - 2] : P - a_classes[i - 2];
            const int b = (rng() & 1U)
                ? b_classes[i - 2] : P - b_classes[i - 2];
            points[i] = {a, b};
        }

        int current = score(points);
        const int steps = 180000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const int kind = static_cast<int>(rng() % 12);
            const int left = 2 + static_cast<int>(rng() % 8);
            int right = left;
            while (right == left) right = 2 + static_cast<int>(rng() % 8);
            const auto old_left = points[left];
            const auto old_right = points[right];
            if (kind < 4) {
                std::swap(points[left][0], points[right][0]);
            } else if (kind < 8) {
                std::swap(points[left][1], points[right][1]);
            } else if (kind < 10) {
                points[left][0] = mod(-points[left][0]);
            } else {
                points[left][1] = mod(-points[left][1]);
            }
            const int candidate = score(points);
            const double fraction = static_cast<double>(step) / steps;
            const double temperature =
                2.0 * std::pow(0.01 / 2.0, fraction);
            const int delta = candidate - current;
            if (delta <= 0 || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else {
                points[left] = old_left;
                points[right] = old_right;
            }
            if (current < global_best) {
                global_best = current;
                global_points = points;
                std::cerr << "best=" << global_best
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
            }
            if (current == 0) {
                print_witness(points);
                return 0;
            }
        }
    }
    std::cerr << "NO WITNESS (heuristic only); best=" << global_best
              << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    print_witness(global_points);
    return 1;
}
