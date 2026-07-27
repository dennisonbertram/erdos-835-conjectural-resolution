#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <utility>
#include <vector>

using Sparse = std::vector<std::pair<int16_t, int8_t>>;

struct Move {
  int q;
  int positive;
  int negative;
  Sparse value;
  uint64_t hash;
};

static uint64_t mix(uint64_t z) {
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
  return z ^ (z >> 31);
}

static uint64_t hash_value(const Sparse& value, uint64_t seed) {
  uint64_t result = 0;
  for (auto [row, coefficient] : value) {
    result += uint64_t(int64_t(coefficient)) *
              mix(uint64_t(row) + seed);
  }
  return result;
}

static Sparse vector_of(
    const std::vector<std::array<int, 4>>& tc,
    const std::vector<int>& positive,
    const std::vector<int>& negative) {
  std::array<int8_t, 912> coefficient{};
  std::vector<int> touched;
  for (int cell : positive) {
    for (int row : tc[cell]) {
      if (!coefficient[row]) touched.push_back(row);
      ++coefficient[row];
    }
  }
  for (int cell : negative) {
    for (int row : tc[cell]) {
      if (!coefficient[row]) touched.push_back(row);
      --coefficient[row];
    }
  }
  std::sort(touched.begin(), touched.end());
  touched.erase(std::unique(touched.begin(), touched.end()), touched.end());
  Sparse result;
  for (int row : touched) {
    if (coefficient[row]) result.emplace_back(row, coefficient[row]);
  }
  return result;
}

static Sparse negate(Sparse value) {
  for (auto& entry : value) entry.second = -entry.second;
  return value;
}

static bool subtract(
    const Sparse& target,
    const Sparse& move,
    int coefficient_bound,
    size_t support_bound,
    Sparse& result) {
  result.clear();
  size_t i = 0;
  size_t j = 0;
  while (i < target.size() || j < move.size()) {
    int row;
    int coefficient;
    if (j == move.size() ||
        (i < target.size() && target[i].first < move[j].first)) {
      row = target[i].first;
      coefficient = target[i++].second;
    } else if (i == target.size() || move[j].first < target[i].first) {
      row = move[j].first;
      coefficient = -move[j++].second;
    } else {
      row = target[i].first;
      coefficient = target[i++].second - move[j++].second;
    }
    if (coefficient < -coefficient_bound ||
        coefficient > coefficient_bound) {
      return false;
    }
    if (coefficient) result.emplace_back(row, coefficient);
  }
  return result.size() <= support_bound;
}

static std::pair<int, int> choose_posting(
    const Sparse& target,
    const std::array<std::array<std::vector<int>, 2>, 912>& posting) {
  int best_row = -1;
  int best_sign = 0;
  int best_magnitude = -1;
  size_t best_size = 0;
  for (auto [row, coefficient] : target) {
    int sign = coefficient > 0;
    int magnitude = std::abs(int(coefficient));
    size_t size = posting[row][sign].size();
    if (magnitude > best_magnitude ||
        (magnitude == best_magnitude && size < best_size)) {
      best_row = row;
      best_sign = sign;
      best_magnitude = magnitude;
      best_size = size;
    }
  }
  return {best_row, best_sign};
}

int main(int argc, char** argv) {
  if (argc < 2) return 2;
  int q_begin = argc > 2 ? std::atoi(argv[2]) : 0;
  int q_end = argc > 3 ? std::atoi(argv[3]) : 228;
  std::ifstream input(argv[1]);
  int cell_count;
  input >> cell_count;
  std::vector<std::array<int, 4>> tc(cell_count);
  std::vector<std::vector<int>> groups(228);
  for (int cell = 0; cell < cell_count; ++cell) {
    int q;
    input >> q >> tc[cell][0] >> tc[cell][1] >> tc[cell][2] >> tc[cell][3];
    groups[q].push_back(cell);
  }

  constexpr uint64_t seed = 0x9e3779b97f4a7c15ULL;
  std::vector<Move> singles;
  std::unordered_map<uint64_t, std::vector<int>> by_first_hash;
  std::array<std::array<std::vector<int>, 2>, 912> posting;
  for (int q = 0; q < 228; ++q) {
    for (int positive : groups[q]) {
      for (int negative : groups[q]) {
        if (positive == negative) continue;
        Sparse value = vector_of(tc, {positive}, {negative});
        if (value.empty()) {
          std::cerr << "zero single swap\n";
          return 3;
        }
        uint64_t hash = hash_value(value, seed);
        int index = int(singles.size());
        singles.push_back({q, positive, negative, value, hash});
        by_first_hash[hash].push_back(index);
        for (auto [row, coefficient] : value) {
          posting[row][coefficient > 0].push_back(index);
        }
      }
    }
  }

  uint64_t configurations = 0;
  uint64_t first_moves = 0;
  uint64_t second_moves = 0;
  uint64_t bounded_pairs = 0;
  uint64_t pair_probes = 0;
  uint64_t full_hash_hits = 0;
  uint64_t exact_checks = 0;
  Sparse first_residual;
  Sparse pair_target;
  Sparse final_target;

  for (int q = q_begin; q < q_end; ++q) {
    const auto& cells = groups[q];
    for (int a = 0; a < 13; ++a) {
      for (int b = a + 1; b < 13; ++b) {
        for (int c = 0; c < 13; ++c) {
          if (c == a || c == b) continue;
          for (int d = c + 1; d < 13; ++d) {
            if (d == a || d == b) continue;
            ++configurations;
            Sparse target =
                negate(vector_of(tc, {cells[a], cells[b]},
                                 {cells[c], cells[d]}));
            if (target.empty()) {
              std::cerr << "zero double-swap target\n";
              return 4;
            }
            uint64_t target_hash = hash_value(target, seed);
            auto [first_row, first_sign] = choose_posting(target, posting);
            for (int first_index : posting[first_row][first_sign]) {
              const Move& first = singles[first_index];
              if (first.q == q ||
                  !subtract(target, first.value, 3, 24, first_residual)) {
                continue;
              }
              ++first_moves;
              if (first_residual.empty()) {
                std::cerr << "zero three-single residual\n";
                return 5;
              }
              auto [second_row, second_sign] =
                  choose_posting(first_residual, posting);
              for (int second_index : posting[second_row][second_sign]) {
                const Move& second = singles[second_index];
                if (second.q == q || second.q == first.q) continue;
                ++second_moves;
                if (!subtract(
                        first_residual, second.value, 2, 16, pair_target)) {
                  continue;
                }
                ++bounded_pairs;
                if (pair_target.empty()) {
                  std::cerr << "zero two-single residual\n";
                  return 6;
                }
                uint64_t pair_hash =
                    target_hash - first.hash - second.hash;
                auto [third_row, third_sign] =
                    choose_posting(pair_target, posting);
                for (int third_index : posting[third_row][third_sign]) {
                  const Move& third = singles[third_index];
                  if (third.q == q || third.q == first.q ||
                      third.q == second.q) {
                    continue;
                  }
                  ++pair_probes;
                  uint64_t wanted = pair_hash - third.hash;
                  auto found = by_first_hash.find(wanted);
                  if (found == by_first_hash.end()) continue;
                  ++full_hash_hits;
                  if (!subtract(
                          pair_target, third.value, 1, 8, final_target)) {
                    continue;
                  }
                  for (int fourth_index : found->second) {
                    ++exact_checks;
                    const Move& fourth = singles[fourth_index];
                    if (fourth.value != final_target ||
                        fourth.q == q || fourth.q == first.q ||
                        fourth.q == second.q || fourth.q == third.q) {
                      continue;
                    }
                    std::cout << "FOUND 2+1+1+1+1\n";
                    return 0;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  std::cout << "NONE q " << q_begin << ':' << q_end
            << " configurations " << configurations
            << " first_moves " << first_moves
            << " second_moves " << second_moves
            << " bounded_pairs " << bounded_pairs
            << " pair_probes " << pair_probes
            << " full_hash_hits " << full_hash_hits
            << " exact_checks " << exact_checks << '\n';
}
