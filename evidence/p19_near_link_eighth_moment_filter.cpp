#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <unordered_set>
#include <vector>

// Exact finite filter forced by the eighth moment of a hypothetical p=19
// rank-two near-link.
//
// The preceding algebraic reduction is:
//   * the zero colour gives nine parallel pairs and one singleton;
//   * Q_2(x)=sum_i det(x,v_i)^2 must have rank one;
//   * normalize the singleton to (1,0), the pair directions to (t_g,1),
//     and Q_2=kappa*y^2, with rho^2=-kappa;
//   * the endpoint scale eighth-powers are rho^-8 times m^8, where the
//     missing labels m run through F_19^*;
//   * Q_8 is constant on the nine pair directions, hence equals
//     -rho^8*y^8 identically.
//
// Writing P(X)=prod_g(X-t_g), the first eight coefficient equations imply
//     alpha_g^8+beta_g^8 = lambda/P'(t_g).
// After multiplying by rho^8, each left side is a sum of a pair from the
// multiset {m^8:m in F_19^*}.  The final coefficient gives
//     rho^8 lambda = -R(R+K),  R=rho^8, K=c^8.
// This program exhausts all 9-subsets of F_19 and all pair-sum multisets.

static constexpr int P = 19;
static constexpr int H = 9;

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

static std::uint64_t pack_sorted(std::array<int, H> values) {
    std::sort(values.begin(), values.end());
    std::uint64_t packed = 0;
    for (int value : values) {
        packed = (packed << 5) | static_cast<std::uint64_t>(value);
    }
    return packed;
}

static void enumerate_pair_sums(
    std::array<int, P>& count,
    int pairs_done,
    std::array<int, H>& sums,
    std::unordered_set<std::uint64_t>& patterns
) {
    if (pairs_done == H) {
        patterns.insert(pack_sorted(sums));
        return;
    }
    int first = 1;
    while (first < P && count[first] == 0) ++first;
    if (first == P) return;
    --count[first];
    for (int second = first; second < P; ++second) {
        if (count[second] == 0) continue;
        --count[second];
        sums[pairs_done] = mod(first + second);
        // -1 is a nonsquare modulo 19, so two nonzero eighth powers cannot
        // sum to zero.  Keep the assertion explicit for auditability.
        if (sums[pairs_done] != 0) {
            enumerate_pair_sums(
                count, pairs_done + 1, sums, patterns
            );
        }
        ++count[second];
    }
    ++count[first];
}

static void examine_slope_set(
    const std::array<int, H>& slopes,
    const std::unordered_set<std::uint64_t>& patterns,
    const std::vector<int>& allowed_scalars,
    std::uint64_t& examined,
    std::uint64_t& survivors
) {
    ++examined;
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

    for (int scalar : allowed_scalars) {
        std::array<int, H> target{};
        for (int index = 0; index < H; ++index) {
            target[index] = mod(scalar * barycentric[index]);
        }
        if (patterns.contains(pack_sorted(target))) {
            ++survivors;
            if (survivors <= 20) {
                std::cout << "survivor slopes=[";
                for (int index = 0; index < H; ++index) {
                    if (index) std::cout << ",";
                    std::cout << slopes[index];
                }
                std::cout << "] scalar=" << scalar << " weights=[";
                std::sort(target.begin(), target.end());
                for (int index = 0; index < H; ++index) {
                    if (index) std::cout << ",";
                    std::cout << target[index];
                }
                std::cout << "]\n";
            }
        }
    }
}

static void enumerate_slope_sets(
    int next,
    int depth,
    std::array<int, H>& slopes,
    const std::unordered_set<std::uint64_t>& patterns,
    const std::vector<int>& allowed_scalars,
    std::uint64_t& examined,
    std::uint64_t& survivors
) {
    if (depth == H) {
        examine_slope_set(
            slopes, patterns, allowed_scalars, examined, survivors
        );
        return;
    }
    for (int value = next; value <= P - (H - depth); ++value) {
        slopes[depth] = value;
        enumerate_slope_sets(
            value + 1, depth + 1, slopes, patterns, allowed_scalars,
            examined, survivors
        );
    }
}

int main() {
    std::array<int, P> eighth_power_count{};
    std::vector<int> eighth_powers;
    for (int value = 1; value < P; ++value) {
        const int eighth = power(value, 8);
        ++eighth_power_count[eighth];
        eighth_powers.push_back(eighth);
    }
    for (int value = 1; value < P; ++value) {
        if (eighth_power_count[value] != 0
            && eighth_power_count[value] != 2) {
            std::cerr << "unexpected eighth-power multiplicity\n";
            return 2;
        }
    }

    std::unordered_set<std::uint64_t> patterns;
    patterns.reserve(1 << 20);
    std::array<int, H> sums{};
    enumerate_pair_sums(eighth_power_count, 0, sums, patterns);
    std::cout << "distinct pair-sum multisets=" << patterns.size() << "\n";

    std::vector<int> image;
    for (int value = 1; value < P; ++value) {
        const int eighth = power(value, 8);
        if (std::find(image.begin(), image.end(), eighth) == image.end()) {
            image.push_back(eighth);
        }
    }
    std::sort(image.begin(), image.end());
    std::vector<int> allowed_scalars;
    for (int r : image) {
        for (int k : image) {
            const int scalar = mod(-r * (r + k));
            if (scalar != 0
                && std::find(
                    allowed_scalars.begin(), allowed_scalars.end(), scalar
                ) == allowed_scalars.end()) {
                allowed_scalars.push_back(scalar);
            }
        }
    }
    std::sort(allowed_scalars.begin(), allowed_scalars.end());
    std::cout << "allowed barycentric scalars=[";
    for (std::size_t index = 0; index < allowed_scalars.size(); ++index) {
        if (index) std::cout << ",";
        std::cout << allowed_scalars[index];
    }
    std::cout << "]\n";

    std::array<int, H> slopes{};
    std::uint64_t examined = 0;
    std::uint64_t survivors = 0;
    enumerate_slope_sets(
        0, 0, slopes, patterns, allowed_scalars, examined, survivors
    );
    std::cout << "slope_sets_examined=" << examined << "\n";
    std::cout << "eighth_moment_survivors=" << survivors << "\n";
    if (examined != 92378) {
        std::cerr << "wrong slope-set count\n";
        return 2;
    }
    return survivors == 0 ? 0 : 1;
}
