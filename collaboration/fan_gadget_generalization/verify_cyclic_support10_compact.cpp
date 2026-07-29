#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using Sparse = std::vector<std::pair<int16_t, int8_t>>;

struct GroupPair {
  int first = -1;
  int second = -1;
};

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

static std::string sparse_key(const Sparse& vector, bool negate = false) {
  std::string result;
  result.reserve(3 * vector.size());
  for (auto [row, coefficient] : vector) {
    result.push_back(static_cast<char>(row & 255));
    result.push_back(static_cast<char>((row >> 8) & 255));
    int value = negate ? -coefficient : coefficient;
    result.push_back(static_cast<char>(value + 5));
  }
  return result;
}

static std::string five_subset_signature(
    const std::vector<std::array<int, 4>>& tc,
    const std::array<int, 5>& cells) {
  std::array<int16_t, 20> rows;
  int index = 0;
  for (int cell : cells) {
    for (int row : tc[cell]) rows[index++] = row;
  }
  std::sort(rows.begin(), rows.end());
  std::string result;
  result.reserve(40);
  for (int row : rows) {
    result.push_back(static_cast<char>(row & 255));
    result.push_back(static_cast<char>((row >> 8) & 255));
  }
  return result;
}

static bool disjoint(
    const std::array<int, 5>& left,
    const std::array<int, 5>& right) {
  for (int a : left) {
    for (int b : right) {
      if (a == b) return false;
    }
  }
  return true;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: verify_cyclic_support10_compact COLUMN_FILE\n";
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

  uint64_t five_subsets = 0;
  uint64_t five_signature_collisions = 0;
  for (const auto& group : q_groups) {
    std::unordered_map<
        std::string,
        std::vector<std::array<int, 5>>>
        seen;
    for (int a = 0; a < 13; ++a) {
      for (int b = a + 1; b < 13; ++b) {
        for (int c = b + 1; c < 13; ++c) {
          for (int d = c + 1; d < 13; ++d) {
            for (int e = d + 1; e < 13; ++e) {
              ++five_subsets;
              std::array<int, 5> subset{
                  group[a], group[b], group[c], group[d], group[e]};
              auto& old = seen[five_subset_signature(tc, subset)];
              for (const auto& prior : old) {
                ++five_signature_collisions;
                if (disjoint(prior, subset)) {
                  std::cout << "FOUND case 5\n";
                  return 1;
                }
              }
              old.push_back(subset);
            }
          }
        }
      }
    }
  }

  std::unordered_map<std::string, int> single_moves;
  for (int q = 0; q < 228; ++q) {
    for (int positive : q_groups[q]) {
      for (int negative : q_groups[q]) {
        if (positive == negative) continue;
        if (
            !single_moves
                 .emplace(
                     sparse_key(make_vector(tc, {positive}, {negative})),
                     q)
                 .second) {
          std::cerr << "duplicate oriented swap vector\n";
          return 6;
        }
      }
    }
  }

  uint64_t four_pair_configurations = 0;
  uint64_t four_pair_unit_bounded = 0;
  for (int q = 0; q < 228; ++q) {
    const auto& group = q_groups[q];
    for (int pa = 0; pa < 13; ++pa) {
      for (int pb = pa + 1; pb < 13; ++pb) {
        for (int pc = pb + 1; pc < 13; ++pc) {
          for (int pd = pc + 1; pd < 13; ++pd) {
            for (int na = 0; na < 13; ++na) {
              if (na == pa || na == pb || na == pc || na == pd) continue;
              for (int nb = na + 1; nb < 13; ++nb) {
                if (nb == pa || nb == pb || nb == pc || nb == pd) continue;
                for (int nc = nb + 1; nc < 13; ++nc) {
                  if (nc == pa || nc == pb || nc == pc || nc == pd) {
                    continue;
                  }
                  for (int nd = nc + 1; nd < 13; ++nd) {
                    if (nd == pa || nd == pb || nd == pc || nd == pd) {
                      continue;
                    }
                    ++four_pair_configurations;
                    Sparse vector = make_vector(
                        tc,
                        {
                            group[pa],
                            group[pb],
                            group[pc],
                            group[pd],
                        },
                        {
                            group[na],
                            group[nb],
                            group[nc],
                            group[nd],
                        });
                    bool unit_bounded = true;
                    for (auto [row, coefficient] : vector) {
                      if (coefficient < -1 || coefficient > 1) {
                        unit_bounded = false;
                      }
                    }
                    if (!unit_bounded) continue;
                    ++four_pair_unit_bounded;
                    auto found =
                        single_moves.find(sparse_key(vector, true));
                    if (
                        found != single_moves.end() &&
                        found->second != q) {
                      std::cout << "FOUND case 4+1\n";
                      return 1;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  std::unordered_map<std::string, GroupPair> double_moves;
  for (int q = 0; q < 228; ++q) {
    const auto& group = q_groups[q];
    for (int pa = 0; pa < 13; ++pa) {
      for (int pb = pa + 1; pb < 13; ++pb) {
        for (int na = 0; na < 13; ++na) {
          if (na == pa || na == pb) continue;
          for (int nb = na + 1; nb < 13; ++nb) {
            if (nb == pa || nb == pb) continue;
            std::string vector_key = sparse_key(
                make_vector(
                    tc,
                    {group[pa], group[pb]},
                    {group[na], group[nb]}));
            GroupPair& groups = double_moves[vector_key];
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

  uint64_t triple_pair_configurations = 0;
  uint64_t triple_pair_double_bounded = 0;
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
                bool double_bounded = true;
                for (auto [row, coefficient] : vector) {
                  if (coefficient < -2 || coefficient > 2) {
                    double_bounded = false;
                  }
                }
                if (!double_bounded) continue;
                ++triple_pair_double_bounded;
                auto found = double_moves.find(sparse_key(vector, true));
                if (
                    found != double_moves.end() &&
                    (found->second.first != q ||
                     (found->second.second != -1 &&
                      found->second.second != q))) {
                  std::cout << "FOUND case 3+2\n";
                  return 1;
                }
              }
            }
          }
        }
      }
    }
  }

  std::cout << "case 5: NONE\n";
  std::cout << "five-subsets: " << five_subsets << "\n";
  std::cout << "same-signature collisions: "
            << five_signature_collisions << "\n";
  std::cout << "case 4+1: NONE\n";
  std::cout << "four-pair configurations: "
            << four_pair_configurations << "\n";
  std::cout << "unit-bounded four-pair vectors: "
            << four_pair_unit_bounded << "\n";
  std::cout << "case 3+2: NONE\n";
  std::cout << "triple-pair configurations: "
            << triple_pair_configurations << "\n";
  std::cout << "double-bounded triple-pair vectors: "
            << triple_pair_double_bounded << "\n";
  std::cout << "consequence: any support-10 trade spans at least three "
               "Q-groups\n";
  return 0;
}
