#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using Term = std::pair<int16_t, int8_t>;
using Sparse = std::vector<Term>;

struct Move {
  int q;
  int positive;
  int negative;
  Sparse vector;
};

static std::string key(const Sparse& vector) {
  std::string result;
  result.reserve(3 * vector.size());
  for (auto [row, coefficient] : vector) {
    result.push_back(static_cast<char>(row & 255));
    result.push_back(static_cast<char>((row >> 8) & 255));
    result.push_back(static_cast<char>(coefficient + 3));
  }
  return result;
}

static Sparse cell_difference(
    const std::vector<std::array<int, 4>>& tc,
    int positive,
    int negative) {
  std::array<int8_t, 912> counts{};
  for (int row : tc[positive]) ++counts[row];
  for (int row : tc[negative]) --counts[row];
  Sparse result;
  for (int row = 0; row < 912; ++row) {
    if (counts[row]) result.emplace_back(row, counts[row]);
  }
  return result;
}

static bool add_bounded(
    const Sparse& left_vector,
    const Sparse& right_vector,
    int bound,
    Sparse& result) {
  result.clear();
  size_t left = 0;
  size_t right = 0;
  while (left < left_vector.size() || right < right_vector.size()) {
    int row;
    int value;
    if (
        right == right_vector.size() ||
        (left < left_vector.size() &&
         left_vector[left].first < right_vector[right].first)) {
      row = left_vector[left].first;
      value = left_vector[left].second;
      ++left;
    } else if (
        left == left_vector.size() ||
        right_vector[right].first < left_vector[left].first) {
      row = right_vector[right].first;
      value = right_vector[right].second;
      ++right;
    } else {
      row = left_vector[left].first;
      value = left_vector[left].second + right_vector[right].second;
      ++left;
      ++right;
    }
    if (value < -bound || value > bound) return false;
    if (value) result.emplace_back(row, value);
  }
  return true;
}

static Sparse negate(const Sparse& vector) {
  Sparse result = vector;
  for (auto& term : result) term.second = -term.second;
  return result;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: verify_cyclic_support8_case_1111 COLUMN_FILE\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  int cell_count;
  if (!(input >> cell_count) || cell_count != 2964) {
    std::cerr << "wrong cell count\n";
    return 3;
  }
  std::vector<std::array<int, 4>> tc(cell_count);
  std::vector<std::vector<int>> q_groups(228);
  for (int cell = 0; cell < cell_count; ++cell) {
    int q;
    if (
        !(input >> q >> tc[cell][0] >> tc[cell][1] >> tc[cell][2] >>
          tc[cell][3]) ||
        q < 0 || q >= 228) {
      std::cerr << "malformed column file\n";
      return 4;
    }
    q_groups[q].push_back(cell);
  }
  for (const auto& group : q_groups) {
    if (group.size() != 13) {
      std::cerr << "wrong Q-group size\n";
      return 5;
    }
  }

  std::vector<Move> moves;
  std::vector<std::vector<int>> q_moves(228);
  std::array<std::array<std::vector<int>, 2>, 912> signed_index;
  std::unordered_map<std::string, int> by_key;
  for (int q = 0; q < 228; ++q) {
    for (int positive : q_groups[q]) {
      for (int negative : q_groups[q]) {
        if (positive == negative) continue;
        Sparse vector = cell_difference(tc, positive, negative);
        int move = static_cast<int>(moves.size());
        moves.push_back({q, positive, negative, vector});
        q_moves[q].push_back(move);
        if (!by_key.emplace(key(vector), move).second) {
          std::cerr << "duplicate oriented swap vector\n";
          return 6;
        }
        for (auto [row, coefficient] : vector) {
          signed_index[row][coefficient > 0 ? 1 : 0].push_back(move);
        }
      }
    }
  }
  if (moves.size() != 35568) {
    std::cerr << "wrong oriented-swap count\n";
    return 7;
  }

  uint64_t second_hits = 0;
  uint64_t third_hits = 0;
  uint64_t exact_lookups = 0;
  Sparse sum_two;
  Sparse sum_three;
  for (int first_q = 0; first_q < 228; ++first_q) {
    for (int first : q_moves[first_q]) {
      const Move& first_move = moves[first];

      // Fix the least row of the first move.  In a zero sum, at least one
      // of the other three moves has the opposite sign there.  Requiring
      // its Q-index to exceed first_q fixes first_q as the minimum without
      // losing any candidate.
      auto [root_row, root_value] = first_move.vector.front();
      const auto& seconds = signed_index[root_row][root_value < 0 ? 1 : 0];
      for (int second : seconds) {
        const Move& second_move = moves[second];
        if (second_move.q <= first_q) continue;
        ++second_hits;
        if (!add_bounded(
                first_move.vector, second_move.vector, 2, sum_two)) {
          continue;
        }
        if (sum_two.empty()) {
          std::cerr << "found a smaller two-swap zero sum\n";
          return 8;
        }

        // Two single swaps remain.  At every nonzero partial-sum row at
        // least one must contribute the opposite sign.  Magnitude two is
        // most restrictive; ties use the shortest exact signed index.
        int chosen_row = -1;
        int chosen_sign = 0;
        int chosen_magnitude = -1;
        size_t chosen_size = 0;
        for (auto [row, coefficient] : sum_two) {
          int sign = coefficient < 0 ? 1 : 0;
          int magnitude = std::abs(static_cast<int>(coefficient));
          size_t size = signed_index[row][sign].size();
          if (
              magnitude > chosen_magnitude ||
              (magnitude == chosen_magnitude && size < chosen_size)) {
            chosen_row = row;
            chosen_sign = sign;
            chosen_magnitude = magnitude;
            chosen_size = size;
          }
        }
        for (int third : signed_index[chosen_row][chosen_sign]) {
          const Move& third_move = moves[third];
          if (third_move.q <= first_q || third_move.q == second_move.q) {
            continue;
          }
          ++third_hits;
          if (!add_bounded(sum_two, third_move.vector, 1, sum_three)) continue;
          ++exact_lookups;
          auto found = by_key.find(key(negate(sum_three)));
          if (found == by_key.end()) continue;
          const Move& fourth_move = moves[found->second];
          if (
              fourth_move.q <= first_q ||
              fourth_move.q == second_move.q ||
              fourth_move.q == third_move.q) {
            continue;
          }
          std::cout << "FOUND\n";
          std::cout << "P " << first_move.positive << ' '
                    << second_move.positive << ' ' << third_move.positive
                    << ' ' << fourth_move.positive << "\n";
          std::cout << "N " << first_move.negative << ' '
                    << second_move.negative << ' ' << third_move.negative
                    << ' ' << fourth_move.negative << "\n";
          return 1;
        }
      }
    }
  }
  std::cout << "case 1+1+1+1: NONE\n";
  std::cout << "second-move hits: " << second_hits << "\n";
  std::cout << "third-move hits: " << third_hits << "\n";
  std::cout << "exact residual lookups: " << exact_lookups << "\n";
  return 0;
}
