#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

using Vec = std::array<int, 4>;

static constexpr int P = 19;
static constexpr int TARGET_SIZE = 10;

static int mod(int x) {
    x %= P;
    return x < 0 ? x + P : x;
}

static int pairing(const Vec& x, const Vec& y) {
    return mod(x[0] * y[2] - x[2] * y[0]
             + x[1] * y[3] - x[3] * y[1]);
}

static int sign_class(int x) {
    x = mod(x);
    return std::min(x, P - x);
}

struct Search {
    std::vector<Vec> candidates;
    std::vector<Vec> selected{{1, 0, 0, 0}, {0, 0, 1, 0}};
    std::vector<int> used{1 << 1, 1 << 1};
    std::mt19937_64 rng;
    std::chrono::steady_clock::time_point start;
    double seconds;
    std::uint64_t nodes = 0;
    int deepest = 2;

    explicit Search(double limit, std::uint64_t seed)
        : rng(seed), start(std::chrono::steady_clock::now()), seconds(limit) {
        for (int a = 0; a < P; ++a) {
            for (int b = 0; b < P; ++b) {
                for (int c = 0; c < P; ++c) {
                    for (int d = 0; d < P; ++d) {
                        Vec value{a, b, c, d};
                        int first = 0;
                        while (first < 4 && value[first] == 0) ++first;
                        if (first == 4 || value[first] > (P - 1) / 2) continue;
                        candidates.push_back(value);
                    }
                }
            }
        }
    }

    double elapsed() const {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start).count();
    }

    bool valid(const Vec& candidate, int& new_mask) const {
        new_mask = 0;
        for (int i = 0; i < static_cast<int>(selected.size()); ++i) {
            const int value_class = sign_class(pairing(selected[i], candidate));
            if (value_class == 0) return false;
            const int bit = 1 << value_class;
            if ((new_mask & bit) || (used[i] & bit)) return false;
            new_mask |= bit;
        }
        return true;
    }

    bool old_rows_compatible(const Vec& left, const Vec& right) const {
        for (int i = 0; i < static_cast<int>(selected.size()); ++i) {
            if (sign_class(pairing(selected[i], left))
                == sign_class(pairing(selected[i], right))) {
                return false;
            }
        }
        return true;
    }

    bool close_with_pair(
        const std::vector<std::pair<int, int>>& valid_ids
    ) {
        for (std::size_t left = 0; left < valid_ids.size(); ++left) {
            if ((nodes++ & 16383U) == 0 && elapsed() >= seconds) return false;
            const auto [left_id, left_mask] = valid_ids[left];
            for (std::size_t right = left + 1; right < valid_ids.size(); ++right) {
                const auto [right_id, right_mask] = valid_ids[right];
                const Vec& x = candidates[left_id];
                const Vec& y = candidates[right_id];
                if (!old_rows_compatible(x, y)) continue;
                const int cross_class = sign_class(pairing(x, y));
                if (cross_class == 0) continue;
                const int bit = 1 << cross_class;
                if ((left_mask & bit) || (right_mask & bit)) continue;
                selected.push_back(x);
                selected.push_back(y);
                return true;
            }
        }
        return false;
    }

    bool close_with_triple(
        const std::vector<std::pair<int, int>>& valid_ids
    ) {
        for (std::size_t first = 0; first < valid_ids.size(); ++first) {
            if (elapsed() >= seconds) return false;
            const auto [first_id, first_mask] = valid_ids[first];
            const Vec& x = candidates[first_id];
            for (std::size_t second = first + 1; second < valid_ids.size(); ++second) {
                if ((nodes++ & 16383U) == 0 && elapsed() >= seconds) return false;
                const auto [second_id, second_mask] = valid_ids[second];
                const Vec& y = candidates[second_id];
                if (!old_rows_compatible(x, y)) continue;
                const int xy = sign_class(pairing(x, y));
                if (xy == 0) continue;
                const int xy_bit = 1 << xy;
                if ((first_mask & xy_bit) || (second_mask & xy_bit)) continue;

                for (std::size_t third = second + 1;
                     third < valid_ids.size(); ++third) {
                    if ((nodes++ & 1048575U) == 0
                        && elapsed() >= seconds) {
                        return false;
                    }
                    const auto [third_id, third_mask] = valid_ids[third];
                    const Vec& z = candidates[third_id];
                    if (!old_rows_compatible(x, z)
                        || !old_rows_compatible(y, z)) {
                        continue;
                    }
                    const int xz = sign_class(pairing(x, z));
                    const int yz = sign_class(pairing(y, z));
                    if (xz == 0 || yz == 0) continue;
                    const int xz_bit = 1 << xz;
                    const int yz_bit = 1 << yz;
                    if ((first_mask & xz_bit) || xz == xy) continue;
                    if ((second_mask & yz_bit) || yz == xy) continue;
                    if ((third_mask & xz_bit) || (third_mask & yz_bit)
                        || xz == yz) {
                        continue;
                    }
                    selected.push_back(x);
                    selected.push_back(y);
                    selected.push_back(z);
                    return true;
                }
            }
        }
        return false;
    }

    bool dfs(int minimum_id) {
        if ((nodes++ & 16383U) == 0 && elapsed() >= seconds) return false;
        if (static_cast<int>(selected.size()) > deepest) {
            deepest = static_cast<int>(selected.size());
            std::cerr << "depth=" << deepest << " nodes=" << nodes
                      << " elapsed=" << elapsed() << "\n";
        }
        if (selected.size() == TARGET_SIZE) return true;

        std::vector<std::pair<int, int>> valid_ids;
        for (int id = minimum_id; id < static_cast<int>(candidates.size()); ++id) {
            int mask = 0;
            if (valid(candidates[id], mask)) valid_ids.emplace_back(id, mask);
        }
        std::shuffle(valid_ids.begin(), valid_ids.end(), rng);

        if (selected.size() == TARGET_SIZE - 2) {
            return close_with_pair(valid_ids);
        }
        if (selected.size() == TARGET_SIZE - 3) {
            return close_with_triple(valid_ids);
        }

        // Wide random branching early, exhaustive branching close to closure.
        std::size_t limit = valid_ids.size();
        if (selected.size() <= 4) limit = std::min<std::size_t>(limit, 96);
        if (selected.size() == 5) limit = std::min<std::size_t>(limit, 256);
        for (std::size_t index = 0; index < limit; ++index) {
            const auto [id, mask] = valid_ids[index];
            std::vector<int> old_used = used;
            for (int i = 0; i < static_cast<int>(selected.size()); ++i) {
                const int value_class = sign_class(pairing(selected[i], candidates[id]));
                used[i] |= 1 << value_class;
            }
            selected.push_back(candidates[id]);
            used.push_back(mask);
            if (dfs(id + 1)) return true;
            selected.pop_back();
            used = std::move(old_used);
            if (elapsed() >= seconds) return false;
        }
        return false;
    }
};

int main(int argc, char** argv) {
    const double seconds = argc > 1 ? std::atof(argv[1]) : 300.0;
    const std::uint64_t seed = argc > 2 ? std::strtoull(argv[2], nullptr, 10)
                                        : 190835ULL;
    Search search(seconds, seed);
    std::cerr << "projective candidates modulo sign=" << search.candidates.size()
              << "\n";
    if (!search.dfs(0)) {
        std::cerr << "TIMEOUT/NO WITNESS depth=" << search.deepest
                  << " nodes=" << search.nodes
                  << " elapsed=" << search.elapsed() << "\n";
        return 1;
    }
    std::cout << "U = [\n";
    for (const auto& row : search.selected) {
        std::cout << "  [" << row[0] << ", " << row[1] << ", "
                  << row[2] << ", " << row[3] << "],\n";
    }
    std::cout << "]\n";
    return 0;
}
