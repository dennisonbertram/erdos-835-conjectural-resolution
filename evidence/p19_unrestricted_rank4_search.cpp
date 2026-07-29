#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

using Vec = std::array<int, 4>;

static int mod(int x, int p) {
    x %= p;
    return x < 0 ? x + p : x;
}

static int pairing(const Vec& x, const Vec& y, int p) {
    return mod(x[0] * y[2] - x[2] * y[0]
             + x[1] * y[3] - x[3] * y[1], p);
}

static int score(const std::vector<Vec>& u, int p) {
    const int n = p + 1;
    int answer = 0;
    std::vector<int> count(p);
    for (int i = 0; i < n; ++i) {
        std::fill(count.begin(), count.end(), 0);
        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            const int value = i < j ? pairing(u[i], u[j], p)
                                    : pairing(u[j], u[i], p);
            ++count[value];
        }
        for (int value = 0; value < p; ++value) {
            answer += count[value] * (count[value] - 1) / 2;
        }
    }
    return answer;
}

static int row_score(const std::vector<Vec>& u, int p, int i) {
    const int n = p + 1;
    std::vector<int> count(p);
    for (int j = 0; j < n; ++j) {
        if (i == j) continue;
        const int value = i < j ? pairing(u[i], u[j], p)
                                : pairing(u[j], u[i], p);
        ++count[value];
    }
    int answer = 0;
    for (int value = 0; value < p; ++value) {
        answer += count[value] * (count[value] - 1) / 2;
    }
    return answer;
}

static void print_witness(const std::vector<Vec>& u, int p) {
    const int n = p + 1;
    std::cout << "U = [\n";
    for (const auto& row : u) {
        std::cout << "  [" << row[0] << ", " << row[1] << ", "
                  << row[2] << ", " << row[3] << "],\n";
    }
    std::cout << "]\nC = [\n";
    for (int i = 0; i < n; ++i) {
        std::cout << "  [";
        for (int j = 0; j < n; ++j) {
            int value = 0;
            if (i < j) value = pairing(u[i], u[j], p);
            if (j < i) value = pairing(u[j], u[i], p);
            if (j) std::cout << ", ";
            std::cout << value;
        }
        std::cout << "],\n";
    }
    std::cout << "]\n";
}

int main(int argc, char** argv) {
    const int p = argc > 1 ? std::atoi(argv[1]) : 19;
    const double seconds = argc > 2 ? std::atof(argv[2]) : 60.0;
    const std::uint64_t seed = argc > 3 ? std::strtoull(argv[3], nullptr, 10)
                                        : 835190019ULL;
    const bool duplicate_last = argc > 4 && std::string(argv[4]) == "duplicate-last";
    const int n = p + 1;
    if (p < 3 || p % 2 == 0) {
        std::cerr << "p must be an odd prime\n";
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
    std::vector<Vec> global_u;
    std::uint64_t iterations = 0;
    int restart = 0;

    while (elapsed() < seconds) {
        ++restart;
        std::vector<Vec> u(n);
        u[0] = {1, 0, 0, 0};
        u[1] = {0, 0, 1, 0};

        std::vector<int> first_values;
        std::vector<int> third_values;
        for (int value = 0; value < p; ++value) {
            if (value != p - 1) first_values.push_back(value);
            if (value != 1) third_values.push_back(value);
        }
        std::shuffle(first_values.begin(), first_values.end(), rng);
        std::shuffle(third_values.begin(), third_values.end(), rng);
        if (duplicate_last) {
            // Put b_p=0 and choose a nonzero a_p != -1, so u_p=a_p u_0.
            const int last_first = 1 + static_cast<int>(rng() % (p - 2));
            std::iter_swap(first_values.begin() + (p - 1),
                           std::find(first_values.begin(), first_values.end(), last_first));
            std::iter_swap(third_values.begin() + (p - 1),
                           std::find(third_values.begin(), third_values.end(), 0));
        }
        for (int i = 2; i < n; ++i) {
            u[i] = {first_values[i - 2], static_cast<int>(rng() % p),
                    third_values[i - 2], static_cast<int>(rng() % p)};
        }
        if (duplicate_last) {
            u[p][1] = 0;
            u[p][3] = 0;
        }

        int current = score(u, p);
        const int steps = 120000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const double fraction = static_cast<double>(step) / steps;
            const double temperature = 2.5 * std::pow(0.02 / 2.5, fraction);
            const int kind = static_cast<int>(rng() % 10);
            const int movable = duplicate_last ? n - 3 : n - 2;
            int i = 2 + static_cast<int>(rng() % movable);
            if ((rng() & 3) != 0) {
                int total_weight = 0;
                for (int v = 2; v < 2 + movable; ++v) {
                    total_weight += 1 + row_score(u, p, v);
                }
                int ticket = static_cast<int>(rng() % total_weight);
                for (int v = 2; v < 2 + movable; ++v) {
                    ticket -= 1 + row_score(u, p, v);
                    if (ticket < 0) {
                        i = v;
                        break;
                    }
                }
            }
            int j = i;
            int old_i = 0;
            int old_j = 0;

            if (kind < 4) {
                while (j == i) j = 2 + static_cast<int>(rng() % movable);
                const int coordinate = kind % 2 == 0 ? 0 : 2;
                old_i = u[i][coordinate];
                old_j = u[j][coordinate];
                std::swap(u[i][coordinate], u[j][coordinate]);
            } else {
                const int coordinate = kind < 7 ? 1 : 3;
                old_i = u[i][coordinate];
                int replacement = static_cast<int>(rng() % (p - 1));
                if (replacement >= old_i) ++replacement;
                u[i][coordinate] = replacement;
            }

            const int candidate = score(u, p);
            const int delta = candidate - current;
            if (delta <= 0 || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else if (kind < 4) {
                const int coordinate = kind % 2 == 0 ? 0 : 2;
                u[i][coordinate] = old_i;
                u[j][coordinate] = old_j;
            } else {
                u[i][kind < 7 ? 1 : 3] = old_i;
            }

            // Periodically optimize both residual coordinates of one vertex.
            if (step % 97 == 0) {
                const int target = 2 + static_cast<int>(rng() % movable);
                const int old_s = u[target][1];
                const int old_t = u[target][3];
                int best_s = old_s;
                int best_t = old_t;
                int best_value = current;
                for (int s = 0; s < p; ++s) {
                    for (int t = 0; t < p; ++t) {
                        u[target][1] = s;
                        u[target][3] = t;
                        const int candidate_value = score(u, p);
                        if (candidate_value < best_value ||
                            (candidate_value == best_value && (rng() & 31) == 0)) {
                            best_value = candidate_value;
                            best_s = s;
                            best_t = t;
                        }
                    }
                }
                u[target][1] = best_s;
                u[target][3] = best_t;
                current = best_value;
            }

            if (current < global_best) {
                global_best = current;
                global_u = u;
                std::cerr << "p=" << p << " best=" << global_best
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
                if (global_best == 0) {
                    print_witness(global_u, p);
                    return 0;
                }
            }
        }
    }

    std::cerr << "TIMEOUT p=" << p << " best=" << global_best
              << " restarts=" << restart << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (!global_u.empty()) print_witness(global_u, p);
    return 1;
}
