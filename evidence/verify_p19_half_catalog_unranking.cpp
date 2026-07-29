#define main p19_half_catalog_search_program_main
#include "p19_unrestricted_rank4_half_catalog_search.cpp"
#undef main

#include <iostream>
#include <set>

int main() {
    std::set<std::array<int, FACTORS>> seen;
    for (std::uint64_t rank = 0; rank < 40320; ++rank) {
        const auto magnitudes = unrank_magnitudes(rank);
        if (magnitudes[0] != 1) {
            throw std::runtime_error("first normalized magnitude is not one");
        }
        std::array<bool, 10> used{};
        for (int factor = 1; factor < FACTORS; ++factor) {
            const int value = magnitudes[factor];
            if (value < 2 || value > 9 || used[value]) {
                throw std::runtime_error("tail is not a permutation");
            }
            used[value] = true;
        }
        if (!seen.insert(magnitudes).second) {
            throw std::runtime_error("duplicate unranked permutation");
        }
    }
    if (seen.size() != 40320) {
        throw std::runtime_error("unranking is not exhaustive");
    }
    std::cout << "normalized_first_magnitude=PASS\n";
    std::cout << "distinct_tail_permutations=" << seen.size() << "\n";
    std::cout << "factoradic_unranking=PASS\n";
}
