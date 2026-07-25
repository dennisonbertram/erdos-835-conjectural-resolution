// Bit-parallel Algorithm X for one fixed-pair cyclic radius-five slice.
//
// This solves only one prescribed-link LSTS(19) slice of the fixed Wallis
// golf design.  A solution is not a joint radius-five layer: the 105 slices
// still have to satisfy the shared-N phase constraints.  Search exhaustion
// under a time/node limit has no mathematical status.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int P = 17;
constexpr int ORBITS = 40;
constexpr int COLUMNS = 160;
constexpr int MAX_ROWS = 512;
constexpr int ROW_WORDS = MAX_ROWS / 64;
constexpr int COLUMN_WORDS = 3;

using Triple = std::array<int, 3>;
using Edge = std::pair<int, int>;
using RowBits = std::array<std::uint64_t, ROW_WORDS>;
using ColumnBits = std::array<std::uint64_t, COLUMN_WORDS>;

constexpr int FIRST_HALF[8][15] = {
    {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16},
    {5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12},
    {9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6},
    {14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11},
    {16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9},
    {13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2},
    {15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8},
    {12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5},
};

int mod17(int value) {
  value %= P;
  return value < 0 ? value + P : value;
}

Triple translated(Triple triple, int shift) {
  for (int &value : triple) value = mod17(value + shift);
  std::sort(triple.begin(), triple.end());
  return triple;
}

std::vector<Triple> representatives() {
  std::set<Triple> unseen;
  for (int x = 0; x < P; ++x) {
    for (int y = x + 1; y < P; ++y) {
      for (int z = y + 1; z < P; ++z) unseen.insert({x, y, z});
    }
  }
  std::vector<Triple> answer;
  while (!unseen.empty()) {
    Triple seed = *unseen.begin();
    Triple representative = translated(seed, 0);
    for (int shift = 1; shift < P; ++shift) {
      representative = std::min(representative, translated(seed, shift));
    }
    answer.push_back(representative);
    for (int shift = 0; shift < P; ++shift) {
      unseen.erase(translated(representative, shift));
    }
  }
  if (answer.size() != ORBITS) std::abort();
  return answer;
}

std::array<Edge, 3> triple_edges(const Triple &triple) {
  return {{{triple[0], triple[1]},
           {triple[0], triple[2]},
           {triple[1], triple[2]}}};
}

Edge normalized_edge(int position, int difference) {
  int other = mod17(position + difference);
  return std::minmax(position, other);
}

struct Row {
  int orbit;
  int shift;
  std::array<int, 4> columns;
  int weight = 0;
};

struct Instance {
  std::vector<Row> rows;
  std::array<RowBits, COLUMNS> column_rows{};
  std::vector<RowBits> conflicts;
};

Instance build_instance(int first, int second) {
  std::array<std::array<int, 9>, 15> zero{};
  for (int square = 0; square < 15; ++square) {
    for (int difference = 1; difference <= 8; ++difference) {
      // For edge {x,x+d}, S_i(x,x+d)=a_i[d]+x.
      zero[square][difference] =
          mod17(-FIRST_HALF[difference - 1][square]);
    }
  }

  std::set<Edge> forbidden;
  for (int difference = 1; difference <= 8; ++difference) {
    forbidden.insert(normalized_edge(zero[first][difference], difference));
    forbidden.insert(normalized_edge(zero[second][difference], difference));
  }
  if (forbidden.size() != 16) std::abort();

  std::vector<Edge> residual;
  for (int x = 0; x < P; ++x) {
    for (int y = x + 1; y < P; ++y) {
      if (!forbidden.count({x, y})) residual.push_back({x, y});
    }
  }
  if (residual.size() != 120) std::abort();
  std::array<std::array<int, P>, P> edge_column{};
  for (auto &row : edge_column) row.fill(-1);
  for (int index = 0; index < static_cast<int>(residual.size()); ++index) {
    auto [x, y] = residual[index];
    edge_column[x][y] = edge_column[y][x] = ORBITS + index;
  }

  Instance instance;
  auto reps = representatives();
  for (int orbit = 0; orbit < ORBITS; ++orbit) {
    for (int shift = 0; shift < P; ++shift) {
      Triple triple = translated(reps[orbit], shift);
      bool allowed = true;
      std::array<int, 4> columns{};
      columns[0] = orbit;
      int slot = 1;
      for (Edge edge : triple_edges(triple)) {
        int column = edge_column[edge.first][edge.second];
        if (column < 0) {
          allowed = false;
          break;
        }
        columns[slot++] = column;
      }
      if (allowed) instance.rows.push_back({orbit, shift, columns, 0});
    }
  }
  if (instance.rows.size() > MAX_ROWS) std::abort();

  for (int row = 0; row < static_cast<int>(instance.rows.size()); ++row) {
    for (int column : instance.rows[row].columns) {
      instance.column_rows[column][row / 64] |=
          std::uint64_t{1} << (row % 64);
    }
  }
  instance.conflicts.resize(instance.rows.size());
  for (int row = 0; row < static_cast<int>(instance.rows.size()); ++row) {
    RowBits conflict{};
    for (int column : instance.rows[row].columns) {
      for (int word = 0; word < ROW_WORDS; ++word) {
        conflict[word] |= instance.column_rows[column][word];
      }
    }
    instance.conflicts[row] = conflict;
  }
  return instance;
}

bool column_is_covered(const ColumnBits &bits, int column) {
  return bits[column / 64] & (std::uint64_t{1} << (column % 64));
}

void cover_column(ColumnBits &bits, int column) {
  bits[column / 64] |= std::uint64_t{1} << (column % 64);
}

int intersection_size(const RowBits &left, const RowBits &right) {
  int answer = 0;
  for (int word = 0; word < ROW_WORDS; ++word) {
    answer += __builtin_popcountll(left[word] & right[word]);
  }
  return answer;
}

struct Search {
  const Instance &instance;
  std::mt19937_64 random;
  std::uint64_t nodes = 0;
  std::uint64_t node_limit;
  std::chrono::steady_clock::time_point deadline;
  std::vector<int> solution;
  std::vector<int> best_solution;
  int best_cost = std::numeric_limits<int>::max();
  bool timed_out = false;
  bool weighted = false;
  bool optimize_weight = false;
  bool min_weight_positive = false;
  int solution_limit = 0;
  std::vector<std::vector<int>> enumerated_solutions;

  bool expired() {
    if (++nodes >= node_limit) {
      timed_out = true;
      return true;
    }
    if ((nodes & 0x3fff) == 0 &&
        std::chrono::steady_clock::now() >= deadline) {
      timed_out = true;
      return true;
    }
    return false;
  }

  bool solve(
      RowBits active,
      ColumnBits covered,
      int depth,
      int current_cost) {
    if (expired()) return false;
    if (optimize_weight && current_cost >= best_cost) return false;
    if (depth == ORBITS) {
      if (solution_limit > 0) {
        enumerated_solutions.push_back(solution);
        return static_cast<int>(enumerated_solutions.size()) >= solution_limit;
      }
      if (min_weight_positive && current_cost == 0) return false;
      if (current_cost < best_cost) {
        best_cost = current_cost;
        best_solution = solution;
      }
      return !optimize_weight;
    }

    int best_column = -1;
    int best_size = std::numeric_limits<int>::max();
    for (int column = 0; column < COLUMNS; ++column) {
      if (column_is_covered(covered, column)) continue;
      int size = intersection_size(
          active, instance.column_rows[column]);
      if (size < best_size) {
        best_size = size;
        best_column = column;
        if (size <= 1) break;
      }
    }
    if (best_size == 0 || best_column < 0) return false;
    if (optimize_weight && best_cost < std::numeric_limits<int>::max()) {
      int lower_bound = 0;
      for (int orbit = 0; orbit < ORBITS; ++orbit) {
        if (column_is_covered(covered, orbit)) continue;
        int minimum = std::numeric_limits<int>::max();
        for (int word = 0; word < ROW_WORDS; ++word) {
          std::uint64_t bits =
              active[word] & instance.column_rows[orbit][word];
          while (bits) {
            int bit = __builtin_ctzll(bits);
            int row = word * 64 + bit;
            minimum = std::min(minimum, instance.rows[row].weight);
            bits &= bits - 1;
          }
        }
        if (minimum == std::numeric_limits<int>::max()) return false;
        lower_bound += minimum;
      }
      if (current_cost + lower_bound >= best_cost) return false;
    }

    std::vector<int> candidates;
    for (int word = 0; word < ROW_WORDS; ++word) {
      std::uint64_t bits =
          active[word] & instance.column_rows[best_column][word];
      while (bits) {
        int bit = __builtin_ctzll(bits);
        candidates.push_back(word * 64 + bit);
        bits &= bits - 1;
      }
    }
    std::shuffle(candidates.begin(), candidates.end(), random);
    if (weighted) {
      std::stable_sort(
          candidates.begin(), candidates.end(), [&](int left, int right) {
            return instance.rows[left].weight <
                   instance.rows[right].weight;
          });
    }
    for (int row : candidates) {
      RowBits next_active{};
      for (int word = 0; word < ROW_WORDS; ++word) {
        next_active[word] =
            active[word] & ~instance.conflicts[row][word];
      }
      ColumnBits next_covered = covered;
      for (int column : instance.rows[row].columns) {
        cover_column(next_covered, column);
      }
      solution.push_back(row);
      if (solve(
              next_active,
              next_covered,
              depth + 1,
              current_cost + instance.rows[row].weight)) {
        return true;
      }
      solution.pop_back();
      if (timed_out) return false;
    }
    return false;
  }
};

std::pair<int, int> parse_pair(const std::string &text) {
  auto comma = text.find(',');
  if (comma == std::string::npos) std::abort();
  int first = std::stoi(text.substr(0, comma));
  int second = std::stoi(text.substr(comma + 1));
  if (!(0 <= first && first < second && second < 15)) std::abort();
  return {first, second};
}

}  // namespace

int main(int argc, char **argv) {
  int first = 0;
  int second = 1;
  double seconds = 60.0;
  std::uint64_t node_limit = 100000000;
  std::uint64_t seed = 835;
  std::string weights_path;
  bool optimize_weight = false;
  bool min_weight_positive = false;
  int enumerate = 0;
  for (int arg = 1; arg < argc; ++arg) {
    std::string option = argv[arg];
    if (option == "--pair" && arg + 1 < argc) {
      std::tie(first, second) = parse_pair(argv[++arg]);
    } else if (option == "--seconds" && arg + 1 < argc) {
      seconds = std::stod(argv[++arg]);
    } else if (option == "--nodes" && arg + 1 < argc) {
      node_limit = std::stoull(argv[++arg]);
    } else if (option == "--seed" && arg + 1 < argc) {
      seed = std::stoull(argv[++arg]);
    } else if (option == "--weights" && arg + 1 < argc) {
      weights_path = argv[++arg];
    } else if (option == "--optimize-weight") {
      optimize_weight = true;
    } else if (option == "--min-weight-positive") {
      min_weight_positive = true;
    } else if (option == "--enumerate" && arg + 1 < argc) {
      enumerate = std::stoi(argv[++arg]);
    } else {
      std::cerr << "usage: " << argv[0]
                << " [--pair i,j] [--seconds n] [--nodes n] [--seed n]"
                << " [--weights path] [--optimize-weight]"
                << " [--min-weight-positive] [--enumerate n]\n";
      return 2;
    }
  }
  if (enumerate < 0 || (enumerate > 0 && optimize_weight)) return 2;

  Instance instance = build_instance(first, second);
  bool weighted = !weights_path.empty();
  if (weighted) {
    std::ifstream input(weights_path);
    if (!input) {
      std::cerr << "cannot open weights file: " << weights_path << '\n';
      return 2;
    }
    std::array<std::array<int, P>, ORBITS> weights{};
    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      for (int shift = 0; shift < P; ++shift) {
        if (!(input >> weights[orbit][shift])) {
          std::cerr << "weights file must contain 40*17 integers\n";
          return 2;
        }
      }
    }
    for (Row &row : instance.rows) {
      row.weight = weights[row.orbit][row.shift];
    }
  }
  RowBits active{};
  for (int row = 0; row < static_cast<int>(instance.rows.size()); ++row) {
    active[row / 64] |= std::uint64_t{1} << (row % 64);
  }
  ColumnBits covered{};
  Search search{
      instance,
      std::mt19937_64(seed),
      0,
      node_limit,
      std::chrono::steady_clock::now() +
          std::chrono::milliseconds(
              static_cast<long long>(seconds * 1000.0)),
      {},
      {},
      std::numeric_limits<int>::max(),
      false,
      weighted,
      optimize_weight,
      min_weight_positive,
      enumerate,
      {},
  };
  auto started = std::chrono::steady_clock::now();
  bool stopped_on_first = search.solve(active, covered, 0, 0);
  bool found = stopped_on_first || !search.best_solution.empty() ||
               !search.enumerated_solutions.empty();
  double elapsed = std::chrono::duration<double>(
                       std::chrono::steady_clock::now() - started)
                       .count();

  std::cout << "{\"pair\":[" << first << ',' << second << ']'
            << ",\"rows\":" << instance.rows.size()
            << ",\"nodes\":" << search.nodes
            << ",\"seconds\":" << elapsed;
  if (!found) {
    std::cout << ",\"status\":\""
              << (search.timed_out ? "UNKNOWN" : "INFEASIBLE")
              << "\"}\n";
    return search.timed_out ? 0 : 1;
  }

  if (enumerate > 0) {
    std::cout << ",\"status\":\"SAT\",\"solutions\":[";
    for (int solution_index = 0;
         solution_index < static_cast<int>(search.enumerated_solutions.size());
         ++solution_index) {
      if (solution_index) std::cout << ',';
      std::array<int, ORBITS> phases{};
      phases.fill(-1);
      for (int row : search.enumerated_solutions[solution_index]) {
        const Row &selected = instance.rows[row];
        phases[selected.orbit] = selected.shift;
      }
      if (std::find(phases.begin(), phases.end(), -1) != phases.end()) {
        std::abort();
      }
      std::cout << '[';
      for (int orbit = 0; orbit < ORBITS; ++orbit) {
        if (orbit) std::cout << ',';
        std::cout << phases[orbit];
      }
      std::cout << ']';
    }
    std::cout << "]}\n";
    return 0;
  }

  std::array<int, ORBITS> phases{};
  phases.fill(-1);
  const std::vector<int> &selected_rows =
      search.best_solution.empty() ? search.solution : search.best_solution;
  for (int row : selected_rows) {
    const Row &selected = instance.rows[row];
    phases[selected.orbit] = selected.shift;
  }
  if (std::find(phases.begin(), phases.end(), -1) != phases.end()) {
    std::abort();
  }
  int total_weight = 0;
  for (int row : selected_rows) total_weight += instance.rows[row].weight;
  std::cout << ",\"status\":\"SAT\",\"weight\":" << total_weight
            << ",\"optimal\":"
            << ((optimize_weight && !search.timed_out) ? "true" : "false")
            << ",\"timed_out\":"
            << (search.timed_out ? "true" : "false")
            << ",\"selected_shifts\":[";
  for (int orbit = 0; orbit < ORBITS; ++orbit) {
    if (orbit) std::cout << ',';
    std::cout << phases[orbit];
  }
  std::cout << "]}\n";
  return 0;
}
