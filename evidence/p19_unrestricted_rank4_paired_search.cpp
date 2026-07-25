#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
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

static int sign_class(int x, int p) {
    x = mod(x, p);
    return std::min(x, p - x);
}

static int row_score(const std::vector<Vec>& u, int p, int i) {
    const int h = (p - 1) / 2;
    std::vector<int> count(h + 1);
    for (int j = 0; j < static_cast<int>(u.size()); ++j) {
        if (i == j) continue;
        ++count[sign_class(pairing(u[i], u[j], p), p)];
    }
    int answer = 4 * count[0];
    for (int value = 1; value <= h; ++value) {
        answer += count[value] * (count[value] - 1) / 2;
    }
    return answer;
}

static int score(const std::vector<Vec>& u, int p) {
    int answer = 0;
    for (int i = 0; i < static_cast<int>(u.size()); ++i) {
        answer += row_score(u, p, i);
    }
    return answer;
}

static int pair_descent(std::vector<Vec>& u, int p) {
    int current = score(u, p);
    bool improved = true;
    while (improved && current != 0) {
        improved = false;
        for (int left = 2; left < static_cast<int>(u.size()) && !improved; ++left) {
            for (int right = left + 1; right < static_cast<int>(u.size()) && !improved; ++right) {
                const int old_ls = u[left][1];
                const int old_lt = u[left][3];
                const int old_rs = u[right][1];
                const int old_rt = u[right][3];
                int best = current;
                int best_ls = old_ls;
                int best_lt = old_lt;
                int best_rs = old_rs;
                int best_rt = old_rt;
                for (int ls = 0; ls < p; ++ls) {
                    for (int lt = 0; lt < p; ++lt) {
                        u[left][1] = ls;
                        u[left][3] = lt;
                        for (int rs = 0; rs < p; ++rs) {
                            for (int rt = 0; rt < p; ++rt) {
                                u[right][1] = rs;
                                u[right][3] = rt;
                                const int candidate = score(u, p);
                                if (candidate < best) {
                                    best = candidate;
                                    best_ls = ls;
                                    best_lt = lt;
                                    best_rs = rs;
                                    best_rt = rt;
                                }
                            }
                        }
                    }
                }
                u[left][1] = best_ls;
                u[left][3] = best_lt;
                u[right][1] = best_rs;
                u[right][3] = best_rt;
                if (best < current) {
                    current = best;
                    improved = true;
                } else {
                    u[left][1] = old_ls;
                    u[left][3] = old_lt;
                    u[right][1] = old_rs;
                    u[right][3] = old_rt;
                }
            }
        }
    }
    return current;
}

static void print_witness(const std::vector<Vec>& u, int p) {
    std::cout << "U = [\n";
    for (const auto& row : u) {
        std::cout << "  [" << row[0] << ", " << row[1] << ", "
                  << row[2] << ", " << row[3] << "],\n";
    }
    std::cout << "]\nA = [\n";
    for (int i = 0; i < static_cast<int>(u.size()); ++i) {
        std::cout << "  [";
        for (int j = 0; j < static_cast<int>(u.size()); ++j) {
            if (j) std::cout << ", ";
            std::cout << (i == j ? 0 : pairing(u[i], u[j], p));
        }
        std::cout << "],\n";
    }
    std::cout << "]\n";
}

int main(int argc, char** argv) {
    const int p = argc > 1 ? std::atoi(argv[1]) : 19;
    const double seconds = argc > 2 ? std::atof(argv[2]) : 60.0;
    const std::uint64_t seed = argc > 3 ? std::strtoull(argv[3], nullptr, 10)
                                        : 190835ULL;
    const int h = (p - 1) / 2;
    const int n = h + 1;
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> real(0.0, 1.0);
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    };

    int global_best = 1 << 30;
    int last_refined = 1 << 30;
    std::vector<Vec> global_u;
    std::uint64_t iterations = 0;
    int restart = 0;
    while (elapsed() < seconds) {
        ++restart;
        std::vector<Vec> u(n);
        u[0] = {1, 0, 0, 0};
        u[1] = {0, 0, 1, 0};
        std::vector<int> first;
        std::vector<int> third;
        for (int value = 2; value <= h; ++value) {
            first.push_back((rng() & 1) ? value : p - value);
            third.push_back((rng() & 1) ? value : p - value);
        }
        std::shuffle(first.begin(), first.end(), rng);
        std::shuffle(third.begin(), third.end(), rng);
        for (int i = 2; i < n; ++i) {
            u[i] = {first[i - 2], static_cast<int>(rng() % p),
                    third[i - 2], static_cast<int>(rng() % p)};
        }
        int current = score(u, p);
        const int steps = 180000;
        for (int step = 0; step < steps && elapsed() < seconds; ++step) {
            ++iterations;
            const int kind = static_cast<int>(rng() % 12);
            int i = 2 + static_cast<int>(rng() % (n - 2));
            if ((rng() & 3) != 0) {
                int total = 0;
                for (int v = 2; v < n; ++v) total += 1 + row_score(u, p, v);
                int ticket = static_cast<int>(rng() % total);
                for (int v = 2; v < n; ++v) {
                    ticket -= 1 + row_score(u, p, v);
                    if (ticket < 0) {
                        i = v;
                        break;
                    }
                }
            }
            int j = i;
            int coordinate = 0;
            int old_i = 0;
            int old_j = 0;
            if (kind < 4) {
                while (j == i) j = 2 + static_cast<int>(rng() % (n - 2));
                coordinate = kind % 2 == 0 ? 0 : 2;
                old_i = u[i][coordinate];
                old_j = u[j][coordinate];
                std::swap(u[i][coordinate], u[j][coordinate]);
            } else if (kind < 6) {
                coordinate = kind == 4 ? 0 : 2;
                old_i = u[i][coordinate];
                u[i][coordinate] = p - old_i;
            } else {
                coordinate = kind < 9 ? 1 : 3;
                old_i = u[i][coordinate];
                int replacement = static_cast<int>(rng() % (p - 1));
                if (replacement >= old_i) ++replacement;
                u[i][coordinate] = replacement;
            }

            const int candidate = score(u, p);
            const double fraction = static_cast<double>(step) / steps;
            const double temperature = 1.8 * std::pow(0.015 / 1.8, fraction);
            const int delta = candidate - current;
            if (delta <= 0 || real(rng) < std::exp(-delta / temperature)) {
                current = candidate;
            } else if (kind < 4) {
                u[i][coordinate] = old_i;
                u[j][coordinate] = old_j;
            } else {
                u[i][coordinate] = old_i;
            }

            if (step % 61 == 0) {
                const int target = 2 + static_cast<int>(rng() % (n - 2));
                int best_s = u[target][1];
                int best_t = u[target][3];
                int best_value = current;
                for (int s = 0; s < p; ++s) {
                    for (int t = 0; t < p; ++t) {
                        u[target][1] = s;
                        u[target][3] = t;
                        const int candidate_value = score(u, p);
                        if (candidate_value < best_value ||
                            (candidate_value == best_value && (rng() & 63) == 0)) {
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
                std::cerr << "p=" << p << " paired-best=" << global_best
                          << " restart=" << restart
                          << " iterations=" << iterations
                          << " elapsed=" << elapsed() << "\n";
                if (global_best == 0) {
                    print_witness(global_u, p);
                    return 0;
                }
                if (global_best <= 8 && global_best < last_refined) {
                    last_refined = global_best;
                    auto refined = global_u;
                    const int refined_score = pair_descent(refined, p);
                    if (refined_score < global_best) {
                        global_best = refined_score;
                        global_u = refined;
                        u = refined;
                        current = refined_score;
                        std::cerr << "p=" << p << " pair-refined="
                                  << global_best << " elapsed=" << elapsed()
                                  << "\n";
                        if (global_best == 0) {
                            print_witness(global_u, p);
                            return 0;
                        }
                    }
                }
            }
        }
    }
    std::cerr << "TIMEOUT p=" << p << " paired-best=" << global_best
              << " restarts=" << restart << " iterations=" << iterations
              << " elapsed=" << elapsed() << "\n";
    if (!global_u.empty()) print_witness(global_u, p);
    return 1;
}
