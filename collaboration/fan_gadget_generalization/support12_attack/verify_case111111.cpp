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

static uint64_t weight(int row) {
  uint64_t z = uint64_t(row) + 0x9e3779b97f4a7c15ULL;
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
  return z ^ (z >> 31);
}

static uint64_t hash_value(const Sparse& value) {
  uint64_t result = 0;
  for (auto [row, coefficient] : value) {
    result += uint64_t(int64_t(coefficient)) * weight(row);
  }
  return result;
}

static Sparse difference(
    const std::vector<std::array<int, 4>>& tc, int positive, int negative) {
  std::array<int8_t, 912> coefficient{};
  for (int row : tc[positive]) ++coefficient[row];
  for (int row : tc[negative]) --coefficient[row];
  Sparse result;
  for (int row = 0; row < 912; ++row) {
    if (coefficient[row]) result.emplace_back(row, coefficient[row]);
  }
  return result;
}

static Sparse negate(Sparse value) {
  for (auto& entry : value) entry.second = -entry.second;
  return value;
}

static bool add(
    const Sparse& partial,
    const Sparse& move,
    int coefficient_bound,
    size_t support_bound,
    Sparse& result) {
  result.clear();
  size_t i = 0;
  size_t j = 0;
  while (i < partial.size() || j < move.size()) {
    int row;
    int coefficient;
    if (j == move.size() ||
        (i < partial.size() && partial[i].first < move[j].first)) {
      row = partial[i].first;
      coefficient = partial[i++].second;
    } else if (
        i == partial.size() || move[j].first < partial[i].first) {
      row = move[j].first;
      coefficient = move[j++].second;
    } else {
      row = partial[i].first;
      coefficient = partial[i++].second + move[j++].second;
    }
    if (coefficient < -coefficient_bound ||
        coefficient > coefficient_bound) {
      return false;
    }
    if (coefficient) result.emplace_back(row, coefficient);
  }
  return result.size() <= support_bound;
}

static std::pair<int, int> choose_cancelling_posting(
    const Sparse& partial,
    const std::array<std::array<std::vector<int>, 2>, 912>& posting) {
  int best_row = -1;
  int best_sign = 0;
  int best_magnitude = -1;
  size_t best_size = 0;
  for (auto [row, coefficient] : partial) {
    int cancelling_sign = coefficient < 0;
    int magnitude = std::abs(int(coefficient));
    size_t size = posting[row][cancelling_sign].size();
    if (magnitude > best_magnitude ||
        (magnitude == best_magnitude && size < best_size)) {
      best_row = row;
      best_sign = cancelling_sign;
      best_magnitude = magnitude;
      best_size = size;
    }
  }
  return {best_row, best_sign};
}

static void print_witness(const std::array<const Move*, 6>& moves) {
  std::cout << "FOUND 1+1+1+1+1+1\nP";
  for (const Move* move : moves) std::cout << ' ' << move->positive;
  std::cout << "\nN";
  for (const Move* move : moves) std::cout << ' ' << move->negative;
  std::cout << "\nQ";
  for (const Move* move : moves) std::cout << ' ' << move->q;
  std::cout << '\n';
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

  std::vector<Move> moves;
  std::vector<std::vector<int>> moves_by_q(228);
  std::unordered_map<uint64_t, std::vector<int>> by_hash;
  std::array<std::array<std::vector<int>, 2>, 912> posting;
  for (int q = 0; q < 228; ++q) {
    for (int positive : groups[q]) {
      for (int negative : groups[q]) {
        if (positive == negative) continue;
        Sparse value = difference(tc, positive, negative);
        if (value.empty()) {
          std::cerr << "zero single swap\n";
          return 3;
        }
        uint64_t hash = hash_value(value);
        int index = int(moves.size());
        moves.push_back({q, positive, negative, value, hash});
        moves_by_q[q].push_back(index);
        by_hash[hash].push_back(index);
        for (auto [row, coefficient] : value) {
          posting[row][coefficient > 0].push_back(index);
        }
      }
    }
  }

  uint64_t outer = 0;
  uint64_t second_moves = 0;
  uint64_t third_moves = 0;
  uint64_t fourth_moves = 0;
  uint64_t pair_probes = 0;
  uint64_t full_hash_hits = 0;
  uint64_t exact_checks = 0;
  Sparse sum_two;
  Sparse sum_three;
  Sparse pair_negative;
  Sparse final_negative;

  for (int q = q_begin; q < q_end; ++q) {
    for (int first_index : moves_by_q[q]) {
      ++outer;
      const Move& first = moves[first_index];
      auto [first_row, first_sign] =
          choose_cancelling_posting(first.value, posting);
      for (int second_index : posting[first_row][first_sign]) {
        const Move& second = moves[second_index];
        if (second.q <= q ||
            !add(first.value, second.value, 4, 32, sum_two)) {
          continue;
        }
        ++second_moves;
        if (sum_two.empty()) {
          std::cerr << "cross-Q opposite single swaps\n";
          return 4;
        }
        auto [second_row, second_sign] =
            choose_cancelling_posting(sum_two, posting);
        for (int third_index : posting[second_row][second_sign]) {
          const Move& third = moves[third_index];
          if (third.q <= q || third.q == second.q ||
              !add(sum_two, third.value, 3, 24, sum_three)) {
            continue;
          }
          ++third_moves;
          if (sum_three.empty()) {
            std::cerr << "zero three-single sum\n";
            return 5;
          }
          auto [third_row, third_sign] =
              choose_cancelling_posting(sum_three, posting);
          for (int fourth_index : posting[third_row][third_sign]) {
            const Move& fourth = moves[fourth_index];
            if (fourth.q <= q || fourth.q == second.q ||
                fourth.q == third.q ||
                !add(sum_three, fourth.value, 2, 16, pair_negative)) {
              continue;
            }
            ++fourth_moves;
            if (pair_negative.empty()) {
              std::cerr << "zero four-single sum\n";
              return 6;
            }
            uint64_t partial_hash = hash_value(pair_negative);
            auto [fourth_row, fourth_sign] =
                choose_cancelling_posting(pair_negative, posting);
            for (int fifth_index : posting[fourth_row][fourth_sign]) {
              const Move& fifth = moves[fifth_index];
              if (fifth.q <= q || fifth.q == second.q ||
                  fifth.q == third.q || fifth.q == fourth.q) {
                continue;
              }
              ++pair_probes;
              uint64_t wanted = uint64_t(0) - partial_hash - fifth.hash;
              auto found = by_hash.find(wanted);
              if (found == by_hash.end()) continue;
              ++full_hash_hits;
              if (!add(
                      pair_negative, fifth.value, 1, 8, final_negative)) {
                continue;
              }
              Sparse final_value = negate(final_negative);
              for (int sixth_index : found->second) {
                ++exact_checks;
                const Move& sixth = moves[sixth_index];
                if (sixth.value != final_value || sixth.q <= q ||
                    sixth.q == second.q || sixth.q == third.q ||
                    sixth.q == fourth.q || sixth.q == fifth.q) {
                  continue;
                }
                print_witness(
                    {&first, &second, &third, &fourth, &fifth, &sixth});
                return 0;
              }
            }
          }
        }
      }
    }
  }
  std::cout << "NONE q " << q_begin << ':' << q_end
            << " outer " << outer
            << " second_moves " << second_moves
            << " third_moves " << third_moves
            << " fourth_moves " << fourth_moves
            << " pair_probes " << pair_probes
            << " full_hash_hits " << full_hash_hits
            << " exact_checks " << exact_checks << '\n';
}
