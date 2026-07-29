#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

// Exhaustive even-moment obstruction for the p=19 rank-two near-link.
//
// A hypothetical near-link is forced into the rank-one quadratic-moment
// normal form
//     singleton=(1,0), pair directions=(t_g,1), Q_2=kappa*y^2.
// Choose rho with rho^2=-kappa.  The 18 missing nonzero labels, modulo sign,
// give two copies of each class 1,...,9.  If a pair direction receives classes
// a,b, put S_k(g)=a^k+b^k for even k.
//
// For k=2,4,6,8, the moment polynomial is -rho^k*y^k.  Consequently
//   sum_g S_k(g)t_g^ell = 0             (0 <= ell < k),
//   sum_g S_k(g)t_g^k = -r^(k/2)-r^k,  r=rho^2.
// For k=8 the first eight equations say
//   S_8(g)=D/P'(t_g), D=-r^4-r^8.
//
// This program enumerates every 9-subset of F_19, r in the nonzero squares,
// and every compatible pairing of the doubled sign classes.  It also reports
// the number of affine-equivalence classes as a check, but does not quotient
// by that symmetry when counting survivors.  A zero survivor count is a
// complete obstruction to the near-link bridge (not to arbitrary rank-four
// links).

static constexpr int P = 19;
static constexpr int H = 9;

struct PairType {
    int first;
    int second;
    std::array<int, 4> sums;  // powers 2,4,6,8
};

static int mod(int value) {
    value %= P;
    return value < 0 ? value + P : value;
}

static int power(int base, int exponent) {
    int answer = 1;
    while (exponent) {
        if (exponent & 1) answer = mod(answer * base);
        base = mod(base * base);
        exponent >>= 1;
    }
    return answer;
}

// A positive control at p=7.  These seven vectors really do form a near-link:
// each row has six distinct labels under the same upper-triangle convention.
// Its quadratic moment is nonzero of rank one, exactly as the proof predicts.
static bool check_p7_control() {
    constexpr int p = 7;
    const std::array<std::array<int, 2>, 7> vectors{{
        {{1, 0}}, {{0, 1}}, {{0, 6}}, {{4, 2}},
        {{3, 5}}, {{2, 3}}, {{1, 0}}
    }};
    const auto reduce = [](int value) {
        value %= p;
        return value < 0 ? value + p : value;
    };
    const auto determinant = [&](int left, int right) {
        return reduce(
            vectors[left][0] * vectors[right][1]
            - vectors[left][1] * vectors[right][0]
        );
    };

    std::array<bool, p> missing_seen{};
    for (int row = 0; row < p; ++row) {
        std::array<bool, p> seen{};
        for (int column = 0; column < p; ++column) {
            if (row == column) continue;
            const int left = std::min(row, column);
            const int right = std::max(row, column);
            const int label = determinant(left, right);
            if (seen[label]) return false;
            seen[label] = true;
        }
        int missing = -1;
        for (int label = 0; label < p; ++label) {
            if (!seen[label]) {
                if (missing != -1) return false;
                missing = label;
            }
        }
        if (missing == -1 || missing_seen[missing]) return false;
        missing_seen[missing] = true;
    }

    // Q(x,y)=A*x^2+B*x*y+C*y^2.
    int a_coefficient = 0;
    int b_coefficient = 0;
    int c_coefficient = 0;
    for (const auto& vector : vectors) {
        a_coefficient = reduce(
            a_coefficient + vector[1] * vector[1]
        );
        b_coefficient = reduce(
            b_coefficient - 2 * vector[0] * vector[1]
        );
        c_coefficient = reduce(
            c_coefficient + vector[0] * vector[0]
        );
    }
    const bool nonzero =
        a_coefficient != 0 || b_coefficient != 0 || c_coefficient != 0;
    const int discriminant = reduce(
        b_coefficient * b_coefficient
        - 4 * a_coefficient * c_coefficient
    );
    return nonzero && discriminant == 0;
}

static std::uint32_t affine_canonical_mask(
    const std::array<int, H>& slopes
) {
    std::uint32_t best = (1U << P) - 1;
    for (int multiplier = 1; multiplier < P; ++multiplier) {
        for (int shift = 0; shift < P; ++shift) {
            std::uint32_t mask = 0;
            for (int slope : slopes) {
                mask |= 1U << mod(multiplier * slope + shift);
            }
            best = std::min(best, mask);
        }
    }
    return best;
}

static std::uint32_t slope_mask(const std::array<int, H>& slopes) {
    std::uint32_t mask = 0;
    for (int slope : slopes) mask |= 1U << slope;
    return mask;
}

struct AssignmentSearch {
    const std::array<int, H>& slopes;
    const std::array<int, H>& target_eighth;
    const std::array<std::vector<PairType>, P>& by_eighth;
    int r;
    std::array<int, 10> remaining{};
    std::array<PairType, H> chosen{};
    std::array<int, H> position_order{};
    std::uint64_t nodes = 0;
    std::uint64_t solutions = 0;

    AssignmentSearch(
        const std::array<int, H>& slopes_value,
        const std::array<int, H>& target_value,
        const std::array<std::vector<PairType>, P>& pair_types,
        int r_value
    )
        : slopes(slopes_value),
          target_eighth(target_value),
          by_eighth(pair_types),
          r(r_value) {
        for (int sign_class = 1; sign_class <= H; ++sign_class) {
            remaining[sign_class] = 2;
        }
        for (int index = 0; index < H; ++index) position_order[index] = index;
        std::sort(
            position_order.begin(), position_order.end(),
            [&](int left, int right) {
                return by_eighth[target_eighth[left]].size()
                     < by_eighth[target_eighth[right]].size();
            }
        );
    }

    bool moment_check() const {
        const std::array<int, 4> exponents{2, 4, 6, 8};
        for (int power_index = 0; power_index < 4; ++power_index) {
            const int exponent = exponents[power_index];
            for (int moment = 1; moment < exponent; ++moment) {
                int sum = 0;
                for (int group = 0; group < H; ++group) {
                    sum = mod(
                        sum
                        + chosen[group].sums[power_index]
                            * power(slopes[group], moment)
                    );
                }
                if (sum != 0) return false;
            }
            int top = 0;
            for (int group = 0; group < H; ++group) {
                top = mod(
                    top
                    + chosen[group].sums[power_index]
                        * power(slopes[group], exponent)
                );
            }
            const int rho_power = power(r, exponent / 2);
            const int expected = mod(-rho_power - rho_power * rho_power);
            if (top != expected) return false;
        }
        return true;
    }

    void dfs(int depth) {
        ++nodes;
        if (depth == H) {
            if (!moment_check()) return;
            ++solutions;
            if (solutions <= 10) {
                std::cout << "moment survivor r=" << r << " assignment=[";
                for (int group = 0; group < H; ++group) {
                    if (group) std::cout << ",";
                    std::cout << "(" << chosen[group].first
                              << ":" << chosen[group].second << ")";
                }
                std::cout << "]\n";
            }
            return;
        }
        const int group = position_order[depth];
        for (const PairType& pair : by_eighth[target_eighth[group]]) {
            if (remaining[pair.first] == 0
                || remaining[pair.second] == 0) {
                continue;
            }
            if (pair.first == pair.second && remaining[pair.first] < 2) {
                continue;
            }
            --remaining[pair.first];
            --remaining[pair.second];
            chosen[group] = pair;
            dfs(depth + 1);
            ++remaining[pair.first];
            ++remaining[pair.second];
        }
    }
};

static void examine_slope_set(
    const std::array<int, H>& slopes,
    const std::array<std::vector<PairType>, P>& by_eighth,
    const std::vector<int>& squares,
    std::uint64_t& orbit_representatives,
    std::uint64_t& assignments_examined,
    std::uint64_t& survivors
) {
    if (slope_mask(slopes) == affine_canonical_mask(slopes)) {
        ++orbit_representatives;
    }

    std::array<int, H> barycentric{};
    for (int index = 0; index < H; ++index) {
        int derivative = 1;
        for (int other = 0; other < H; ++other) {
            if (other != index) {
                derivative =
                    mod(derivative * (slopes[index] - slopes[other]));
            }
        }
        barycentric[index] = power(derivative, P - 2);
    }

    for (int r : squares) {
        const int d = mod(-power(r, 4) - power(r, 8));
        if (d == 0) continue;
        std::array<int, H> target{};
        bool possible = true;
        for (int group = 0; group < H; ++group) {
            target[group] = mod(d * barycentric[group]);
            if (by_eighth[target[group]].empty()) possible = false;
        }
        if (!possible) continue;
        AssignmentSearch search(slopes, target, by_eighth, r);
        search.dfs(0);
        assignments_examined += search.nodes;
        survivors += search.solutions;
        if (search.solutions && survivors <= 10) {
            std::cout << "slopes=[";
            for (int index = 0; index < H; ++index) {
                if (index) std::cout << ",";
                std::cout << slopes[index];
            }
            std::cout << "] D=" << d << "\n";
        }
    }
}

static void enumerate_slope_sets(
    int next,
    int depth,
    std::array<int, H>& slopes,
    const std::array<std::vector<PairType>, P>& by_eighth,
    const std::vector<int>& squares,
    std::uint64_t& all_sets,
    std::uint64_t& orbit_representatives,
    std::uint64_t& assignments_examined,
    std::uint64_t& survivors
) {
    if (depth == H) {
        ++all_sets;
        examine_slope_set(
            slopes, by_eighth, squares, orbit_representatives,
            assignments_examined, survivors
        );
        return;
    }
    for (int value = next; value <= P - (H - depth); ++value) {
        slopes[depth] = value;
        enumerate_slope_sets(
            value + 1, depth + 1, slopes, by_eighth, squares,
            all_sets, orbit_representatives, assignments_examined, survivors
        );
    }
}

int main() {
    if (!check_p7_control()) {
        std::cerr << "p=7 positive control failed\n";
        return 3;
    }
    std::cout << "p7_near_link_control=PASS\n";

    std::array<std::vector<PairType>, P> by_eighth;
    for (int first = 1; first <= H; ++first) {
        for (int second = first; second <= H; ++second) {
            PairType pair{first, second, {}};
            pair.sums = {
                mod(power(first, 2) + power(second, 2)),
                mod(power(first, 4) + power(second, 4)),
                mod(power(first, 6) + power(second, 6)),
                mod(power(first, 8) + power(second, 8))
            };
            by_eighth[pair.sums[3]].push_back(pair);
        }
    }

    std::vector<int> squares;
    for (int value = 1; value < P; ++value) {
        const int square = mod(value * value);
        if (std::find(squares.begin(), squares.end(), square) == squares.end()) {
            squares.push_back(square);
        }
    }
    std::sort(squares.begin(), squares.end());

    std::array<int, H> slopes{};
    std::uint64_t all_sets = 0;
    std::uint64_t orbit_representatives = 0;
    std::uint64_t assignments_examined = 0;
    std::uint64_t survivors = 0;
    enumerate_slope_sets(
        0, 0, slopes, by_eighth, squares, all_sets, orbit_representatives,
        assignments_examined, survivors
    );
    std::cout << "all_slope_sets=" << all_sets << "\n";
    std::cout << "affine_orbit_representatives="
              << orbit_representatives << "\n";
    std::cout << "pair_assignment_nodes=" << assignments_examined << "\n";
    std::cout << "even_moment_survivors=" << survivors << "\n";
    if (all_sets != 92378) {
        std::cerr << "wrong number of slope sets\n";
        return 2;
    }
    return survivors == 0 ? 0 : 1;
}
