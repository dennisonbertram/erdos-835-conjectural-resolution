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

static Sparse make_vector(
    const std::vector<std::array<int, 4>>& tc,
    const std::vector<int>& positive,
    const std::vector<int>& negative) {
  std::array<int8_t, 912> counts{};
  std::vector<int> touched;
  for (int cell : positive) {
    for (int row : tc[cell]) {
      if (!counts[row]) touched.push_back(row);
      ++counts[row];
    }
  }
  for (int cell : negative) {
    for (int row : tc[cell]) {
      if (!counts[row]) touched.push_back(row);
      --counts[row];
    }
  }
  std::sort(touched.begin(), touched.end());
  touched.erase(std::unique(touched.begin(), touched.end()), touched.end());
  Sparse result;
  for (int row : touched) {
    if (counts[row]) result.emplace_back(row, counts[row]);
  }
  return result;
}

static Sparse negate(const Sparse& vector) {
  Sparse result = vector;
  for (auto& term : result) term.second = -term.second;
  return result;
}

static bool subtract_move(
    const Sparse& target,
    const Sparse& move,
    Sparse& result) {
  result.clear();
  size_t left = 0;
  size_t right = 0;
  while (left < target.size() || right < move.size()) {
    int row;
    int value;
    if (
        right == move.size() ||
        (left < target.size() && target[left].first < move[right].first)) {
      row = target[left].first;
      value = target[left].second;
      ++left;
    } else if (
        left == target.size() || move[right].first < target[left].first) {
      row = move[right].first;
      value = -move[right].second;
      ++right;
    } else {
      row = target[left].first;
      value = target[left].second - move[right].second;
      ++left;
      ++right;
    }
    if (value < -1 || value > 1) return false;
    if (value) result.emplace_back(row, value);
  }
  return true;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: verify_cyclic_support8_case_211 COLUMN_FILE\n";
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
  std::unordered_map<std::string, int> by_key;
  std::array<std::array<std::vector<int>, 2>, 912> signed_index;
  for (int q = 0; q < 228; ++q) {
    for (int positive : q_groups[q]) {
      for (int negative : q_groups[q]) {
        if (positive == negative) continue;
        Sparse vector = make_vector(tc, {positive}, {negative});
        int index = static_cast<int>(moves.size());
        moves.push_back({q, positive, negative, vector});
        if (!by_key.emplace(key(vector), index).second) {
          std::cerr << "duplicate oriented swap vector\n";
          return 6;
        }
        for (auto [row, coefficient] : vector) {
          signed_index[row][coefficient > 0 ? 1 : 0].push_back(index);
        }
      }
    }
  }
  if (moves.size() != 35568) {
    std::cerr << "wrong oriented-swap count\n";
    return 7;
  }

  uint64_t configurations = 0;
  uint64_t residual_lookups = 0;
  Sparse residual;
  for (int first_q = 0; first_q < 228; ++first_q) {
    const auto& cells = q_groups[first_q];
    for (int positive_left = 0; positive_left < 13; ++positive_left) {
      for (
          int positive_right = positive_left + 1;
          positive_right < 13;
          ++positive_right) {
        for (int negative_left = 0; negative_left < 13; ++negative_left) {
          if (
              negative_left == positive_left ||
              negative_left == positive_right) {
            continue;
          }
          for (
              int negative_right = negative_left + 1;
              negative_right < 13;
              ++negative_right) {
            if (
                negative_right == positive_left ||
                negative_right == positive_right) {
              continue;
            }
            ++configurations;
            std::vector<int> positive{
                cells[positive_left], cells[positive_right]};
            std::vector<int> negative{
                cells[negative_left], cells[negative_right]};
            Sparse target = negate(make_vector(tc, positive, negative));

            // At least one of the two remaining single swaps must contribute
            // the target sign at every nonzero target row.  Prefer a
            // coefficient of magnitude two, then the shortest exact index.
            int chosen_row = -1;
            int chosen_sign = 0;
            int chosen_magnitude = -1;
            size_t chosen_size = 0;
            for (auto [row, coefficient] : target) {
              int sign = coefficient > 0 ? 1 : 0;
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
            if (chosen_row < 0) {
              std::cerr << "zero double-swap vector\n";
              return 8;
            }

            for (int first : signed_index[chosen_row][chosen_sign]) {
              const Move& first_move = moves[first];
              if (first_move.q == first_q) continue;
              if (!subtract_move(target, first_move.vector, residual)) continue;
              ++residual_lookups;
              auto found = by_key.find(key(residual));
              if (found == by_key.end()) continue;
              const Move& second_move = moves[found->second];
              if (
                  second_move.q == first_q ||
                  second_move.q == first_move.q) {
                continue;
              }
              std::cout << "FOUND\n";
              std::cout << "P " << positive[0] << ' ' << positive[1] << ' '
                        << first_move.positive << ' ' << second_move.positive
                        << "\n";
              std::cout << "N " << negative[0] << ' ' << negative[1] << ' '
                        << first_move.negative << ' ' << second_move.negative
                        << "\n";
              return 1;
            }
          }
        }
      }
    }
  }
  std::cout << "case 2+1+1: NONE\n";
  std::cout << "double-swap configurations: " << configurations << "\n";
  std::cout << "exact residual lookups: " << residual_lookups << "\n";
  return 0;
}
