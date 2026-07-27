#include <algorithm>
#include <array>
#include <cstdint>
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
};

struct TwoGroups {
  int first = -1;
  int second = -1;
};

static std::string sparse_key(const Sparse& vector) {
  std::string result;
  result.reserve(3 * vector.size());
  for (auto [row, coefficient] : vector) {
    result.push_back(static_cast<char>(row & 255));
    result.push_back(static_cast<char>((row >> 8) & 255));
    result.push_back(static_cast<char>(coefficient + 4));
  }
  return result;
}

static Sparse negate(const Sparse& vector) {
  Sparse result = vector;
  for (auto& term : result) term.second = -term.second;
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

static std::string subset_signature(
    const std::vector<std::array<int, 4>>& tc,
    const std::array<int, 4>& cells) {
  std::array<int16_t, 16> rows;
  int index = 0;
  for (int cell : cells) {
    for (int row : tc[cell]) rows[index++] = row;
  }
  std::sort(rows.begin(), rows.end());
  std::string result;
  result.reserve(32);
  for (int row : rows) {
    result.push_back(static_cast<char>(row & 255));
    result.push_back(static_cast<char>((row >> 8) & 255));
  }
  return result;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: verify_cyclic_support8_cases_compact COLUMN_FILE\n";
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

  uint64_t four_subsets = 0;
  uint64_t four_signature_collisions = 0;
  for (const auto& group : q_groups) {
    std::unordered_map<std::string, std::array<int, 4>> seen;
    for (int a = 0; a < 13; ++a) {
      for (int b = a + 1; b < 13; ++b) {
        for (int c = b + 1; c < 13; ++c) {
          for (int d = c + 1; d < 13; ++d) {
            ++four_subsets;
            std::array<int, 4> subset{
                group[a], group[b], group[c], group[d]};
            if (!seen.emplace(subset_signature(tc, subset), subset).second) {
              ++four_signature_collisions;
            }
          }
        }
      }
    }
  }
  if (four_signature_collisions) {
    std::cerr << "four-subset signature collision\n";
    return 6;
  }

  std::unordered_map<std::string, Move> single_moves;
  for (int q = 0; q < 228; ++q) {
    for (int positive : q_groups[q]) {
      for (int negative : q_groups[q]) {
        if (positive == negative) continue;
        Sparse vector = make_vector(tc, {positive}, {negative});
        if (
            !single_moves
                 .emplace(
                     sparse_key(vector), Move{q, positive, negative})
                 .second) {
          std::cerr << "duplicate oriented swap vector\n";
          return 7;
        }
      }
    }
  }

  uint64_t triple_pair_configurations = 0;
  for (int q = 0; q < 228; ++q) {
    const auto& group = q_groups[q];
    for (int pa = 0; pa < 13; ++pa) {
      for (int pb = pa + 1; pb < 13; ++pb) {
        for (int pc = pb + 1; pc < 13; ++pc) {
          for (int na = 0; na < 13; ++na) {
            if (na == pa || na == pb || na == pc) continue;
            for (int nb = na + 1; nb < 13; ++nb) {
              if (nb == pa || nb == pb || nb == pc) continue;
              for (int nc = nb + 1; nc < 13; ++nc) {
                if (nc == pa || nc == pb || nc == pc) continue;
                ++triple_pair_configurations;
                Sparse vector = make_vector(
                    tc,
                    {group[pa], group[pb], group[pc]},
                    {group[na], group[nb], group[nc]});
                auto found = single_moves.find(sparse_key(negate(vector)));
                if (
                    found != single_moves.end() &&
                    found->second.q != q) {
                  std::cout << "FOUND case 3+1\n";
                  return 1;
                }
              }
            }
          }
        }
      }
    }
  }

  uint64_t double_pair_configurations = 0;
  std::unordered_map<std::string, TwoGroups> double_vectors;
  for (int q = 0; q < 228; ++q) {
    const auto& group = q_groups[q];
    for (int pa = 0; pa < 13; ++pa) {
      for (int pb = pa + 1; pb < 13; ++pb) {
        for (int na = 0; na < 13; ++na) {
          if (na == pa || na == pb) continue;
          for (int nb = na + 1; nb < 13; ++nb) {
            if (nb == pa || nb == pb) continue;
            ++double_pair_configurations;
            Sparse vector = make_vector(
                tc,
                {group[pa], group[pb]},
                {group[na], group[nb]});
            auto opposite = double_vectors.find(sparse_key(negate(vector)));
            if (
                opposite != double_vectors.end() &&
                (opposite->second.first != q ||
                 (opposite->second.second != -1 &&
                  opposite->second.second != q))) {
              std::cout << "FOUND case 2+2\n";
              return 1;
            }

            TwoGroups& groups = double_vectors[sparse_key(vector)];
            if (groups.first == -1) {
              groups.first = q;
            } else if (groups.first != q && groups.second == -1) {
              groups.second = q;
            }
          }
        }
      }
    }
  }

  std::cout << "case 4: NONE\n";
  std::cout << "four-subsets: " << four_subsets << "\n";
  std::cout << "same-signature collisions: "
            << four_signature_collisions << "\n";
  std::cout << "case 3+1: NONE\n";
  std::cout << "triple-pair configurations: "
            << triple_pair_configurations << "\n";
  std::cout << "case 2+2: NONE\n";
  std::cout << "double-pair configurations: "
            << double_pair_configurations << "\n";
  return 0;
}
