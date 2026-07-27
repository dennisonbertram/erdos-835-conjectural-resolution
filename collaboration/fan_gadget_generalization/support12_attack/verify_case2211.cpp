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
  std::vector<int> positive;
  std::vector<int> negative;
  Sparse value;
  uint64_t fingerprint;
};

static uint64_t weight(int row) {
  uint64_t z = uint64_t(row) + 0x9e3779b97f4a7c15ULL;
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
  return z ^ (z >> 31);
}

static uint64_t fingerprint(const Sparse& value) {
  uint64_t result = 0;
  for (auto [row, coefficient] : value) {
    result += uint64_t(int64_t(coefficient)) * weight(row);
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

static bool negative_sum(
    const Sparse& first,
    const Sparse& second,
    Sparse& result) {
  result.clear();
  size_t i = 0;
  size_t j = 0;
  while (i < first.size() || j < second.size()) {
    int row;
    int coefficient;
    if (j == second.size() ||
        (i < first.size() && first[i].first < second[j].first)) {
      row = first[i].first;
      coefficient = -first[i++].second;
    } else if (i == first.size() || second[j].first < first[i].first) {
      row = second[j].first;
      coefficient = -second[j++].second;
    } else {
      row = first[i].first;
      coefficient = -first[i++].second - second[j++].second;
    }
    if (coefficient < -2 || coefficient > 2) return false;
    if (coefficient) result.emplace_back(row, coefficient);
  }
  return result.size() <= 16;
}

static bool subtract_unit(
    const Sparse& target,
    const Sparse& move,
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
    if (coefficient < -1 || coefficient > 1) return false;
    if (coefficient) result.emplace_back(row, coefficient);
  }
  return true;
}

static std::pair<int, int> choose_single_posting(
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

static void print_witness(
    const Move& first_double,
    const Move& second_double,
    const Move& first_single,
    const Move& second_single) {
  std::cout << "FOUND 2+2+1+1\nP";
  for (int cell : first_double.positive) std::cout << ' ' << cell;
  for (int cell : second_double.positive) std::cout << ' ' << cell;
  for (int cell : first_single.positive) std::cout << ' ' << cell;
  for (int cell : second_single.positive) std::cout << ' ' << cell;
  std::cout << "\nN";
  for (int cell : first_double.negative) std::cout << ' ' << cell;
  for (int cell : second_double.negative) std::cout << ' ' << cell;
  for (int cell : first_single.negative) std::cout << ' ' << cell;
  for (int cell : second_single.negative) std::cout << ' ' << cell;
  std::cout << "\nQ " << first_double.q << ' ' << second_double.q << ' '
            << first_single.q << ' ' << second_single.q << '\n';
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

  std::vector<Move> singles;
  std::unordered_map<uint64_t, std::vector<int>> singles_by_fingerprint;
  std::array<std::array<std::vector<int>, 2>, 912> single_posting;
  for (int q = 0; q < 228; ++q) {
    for (int positive : groups[q]) {
      for (int negative : groups[q]) {
        if (positive == negative) continue;
        Sparse value = vector_of(tc, {positive}, {negative});
        if (value.empty()) {
          std::cerr << "zero single swap\n";
          return 3;
        }
        uint64_t hash = fingerprint(value);
        int index = int(singles.size());
        singles.push_back({q, {positive}, {negative}, value, hash});
        singles_by_fingerprint[hash].push_back(index);
        for (auto [row, coefficient] : value) {
          single_posting[row][coefficient > 0].push_back(index);
        }
      }
    }
  }

  std::vector<Move> doubles;
  std::vector<std::vector<int>> doubles_by_q(228);
  std::array<std::vector<int>, 912> double_posting;
  for (int q = 0; q < 228; ++q) {
    const auto& cells = groups[q];
    for (int a = 0; a < 13; ++a) {
      for (int b = a + 1; b < 13; ++b) {
        for (int c = 0; c < 13; ++c) {
          if (c == a || c == b) continue;
          for (int d = c + 1; d < 13; ++d) {
            if (d == a || d == b) continue;
            std::vector<int> positive{cells[a], cells[b]};
            std::vector<int> negative{cells[c], cells[d]};
            Sparse value = vector_of(tc, positive, negative);
            if (value.empty()) {
              std::cerr << "zero double swap\n";
              return 4;
            }
            int index = int(doubles.size());
            doubles.push_back(
                {q, positive, negative, value, fingerprint(value)});
            doubles_by_q[q].push_back(index);
            for (auto [row, coefficient] : value) {
              (void)coefficient;
              double_posting[row].push_back(index);
            }
          }
        }
      }
    }
  }

  std::vector<uint8_t> intersection_count(doubles.size());
  std::vector<int> touched;
  Sparse target;
  Sparse remaining_single;
  uint64_t outer = 0;
  uint64_t posting_hits = 0;
  uint64_t touched_doubles = 0;
  uint64_t overlap_candidates = 0;
  uint64_t bounded_targets = 0;
  uint64_t single_probes = 0;
  uint64_t fingerprint_hits = 0;
  uint64_t exact_checks = 0;

  for (int q = q_begin; q < q_end; ++q) {
    for (int first_index : doubles_by_q[q]) {
      ++outer;
      const Move& first = doubles[first_index];
      touched.clear();
      for (auto [row, coefficient] : first.value) {
        (void)coefficient;
        for (int second_index : double_posting[row]) {
          const Move& second = doubles[second_index];
          if (second.q <= q) continue;
          ++posting_hits;
          if (!intersection_count[second_index]) {
            touched.push_back(second_index);
          }
          ++intersection_count[second_index];
        }
      }
      touched_doubles += touched.size();
      for (int second_index : touched) {
        const Move& second = doubles[second_index];
        int threshold =
            (int(first.value.size()) + int(second.value.size()) - 15) / 2;
        if (intersection_count[second_index] < threshold) {
          intersection_count[second_index] = 0;
          continue;
        }
        ++overlap_candidates;
        intersection_count[second_index] = 0;
        if (!negative_sum(first.value, second.value, target)) continue;
        if (target.empty()) {
          std::cerr << "cross-Q opposite double swaps\n";
          return 5;
        }
        ++bounded_targets;
        uint64_t target_fingerprint = fingerprint(target);
        auto [row, sign] = choose_single_posting(target, single_posting);
        for (int single_index : single_posting[row][sign]) {
          const Move& first_single = singles[single_index];
          if (first_single.q == first.q ||
              first_single.q == second.q) {
            continue;
          }
          ++single_probes;
          uint64_t wanted =
              target_fingerprint - first_single.fingerprint;
          auto found = singles_by_fingerprint.find(wanted);
          if (found == singles_by_fingerprint.end()) continue;
          ++fingerprint_hits;
          if (!subtract_unit(
                  target, first_single.value, remaining_single)) {
            continue;
          }
          for (int last_index : found->second) {
            ++exact_checks;
            const Move& second_single = singles[last_index];
            if (second_single.value != remaining_single ||
                second_single.q == first.q ||
                second_single.q == second.q ||
                second_single.q == first_single.q) {
              continue;
            }
            print_witness(first, second, first_single, second_single);
            return 0;
          }
        }
      }
      for (int second_index : touched) {
        intersection_count[second_index] = 0;
      }
    }
  }
  std::cout << "NONE q " << q_begin << ':' << q_end
            << " outer " << outer
            << " posting_hits " << posting_hits
            << " touched " << touched_doubles
            << " overlap_candidates " << overlap_candidates
            << " bounded_targets " << bounded_targets
            << " single_probes " << single_probes
            << " fingerprint_hits " << fingerprint_hits
            << " exact_checks " << exact_checks << '\n';
}
