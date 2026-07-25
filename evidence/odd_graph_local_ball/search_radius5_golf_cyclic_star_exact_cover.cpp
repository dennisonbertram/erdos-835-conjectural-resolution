// Bit-parallel Algorithm X for one fixed-Wallis C17 radius-five star.
//
// A candidate chooses one translated triple orbit in one of the fourteen
// pair rows incident with a fixed centre.  It covers exactly five columns:
// one pair/orbit cell, three residual moving edges in that pair row, and one
// centre/orbit/phase slot.  There are 6,384 candidates and 2,800 columns.
//
// SAT is only a 14-row star, not the full radius-five layer or ER #835.
// UNKNOWN under a node/time limit has no mathematical meaning.

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
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int P = 17;
constexpr int FIXED = 15;
constexpr int PAIRS = 14;
constexpr int ORBITS = 40;
constexpr int DEPTH = PAIRS * ORBITS;
constexpr int CELL_COLUMNS = DEPTH;
constexpr int EDGE_COLUMNS = PAIRS * 120;
constexpr int CROSS_COLUMNS = ORBITS * 14;
constexpr int COLUMNS = CELL_COLUMNS + EDGE_COLUMNS + CROSS_COLUMNS;
constexpr int MAX_ROWS = 7000;
constexpr int ROW_WORDS = (MAX_ROWS + 63) / 64;
constexpr int COLUMN_WORDS = (COLUMNS + 63) / 64;

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

std::set<Edge> zero_factor(int square) {
  std::set<Edge> answer;
  for (int difference = 1; difference <= 8; ++difference) {
    int position = mod17(-FIRST_HALF[difference - 1][square]);
    answer.insert(normalized_edge(position, difference));
  }
  if (answer.size() != 8) std::abort();
  return answer;
}

struct Row {
  int outer;
  int orbit;
  int shift;
  std::array<int, 5> columns;
};

struct Instance {
  int centre;
  int pairs;
  int depth;
  int cell_columns;
  int edge_columns;
  int cross_columns;
  int primary_columns;
  int columns;
  std::vector<int> outers;
  std::vector<Row> rows;
  std::array<RowBits, COLUMNS> column_rows{};
  std::vector<RowBits> conflicts;
};

Instance build_instance(
    int centre,
    const std::vector<int> &chosen_outers) {
  Instance instance;
  instance.centre = centre;
  instance.outers = chosen_outers;
  instance.pairs = static_cast<int>(instance.outers.size());
  instance.depth = instance.pairs * ORBITS;
  instance.cell_columns = instance.depth;
  instance.edge_columns = instance.pairs * 120;
  instance.cross_columns = CROSS_COLUMNS;
  instance.primary_columns =
      instance.cell_columns + instance.edge_columns;
  instance.columns =
      instance.primary_columns + instance.cross_columns;
  if (instance.pairs <= 0 || instance.pairs > PAIRS ||
      instance.columns > COLUMNS) {
    std::abort();
  }

  const auto reps = representatives();
  const auto centre_factor = zero_factor(centre);

  std::array<std::array<int, P>, ORBITS> cross_column{};
  for (auto &row : cross_column) row.fill(-1);
  for (int orbit = 0; orbit < ORBITS; ++orbit) {
    int rank = 0;
    for (int shift = 0; shift < P; ++shift) {
      Triple triple = translated(reps[orbit], shift);
      bool forbidden = false;
      for (Edge edge : triple_edges(triple)) {
        if (centre_factor.count(edge)) forbidden = true;
      }
      if (!forbidden) {
        cross_column[orbit][shift] =
            instance.primary_columns + orbit * 14 + rank++;
      }
    }
    if (rank != 14) std::abort();
  }

  for (int pair_index = 0; pair_index < instance.pairs; ++pair_index) {
    int outer = instance.outers[pair_index];
    std::set<Edge> leave = centre_factor;
    const auto outer_factor = zero_factor(outer);
    leave.insert(outer_factor.begin(), outer_factor.end());
    if (leave.size() != 16) std::abort();

    std::vector<Edge> residual;
    for (int x = 0; x < P; ++x) {
      for (int y = x + 1; y < P; ++y) {
        if (!leave.count({x, y})) residual.push_back({x, y});
      }
    }
    if (residual.size() != 120) std::abort();
    std::array<std::array<int, P>, P> edge_column{};
    for (auto &row : edge_column) row.fill(-1);
    for (int index = 0; index < 120; ++index) {
      auto [x, y] = residual[index];
      edge_column[x][y] = edge_column[y][x] =
          instance.cell_columns + pair_index * 120 + index;
    }

    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      for (int shift = 0; shift < P; ++shift) {
        Triple triple = translated(reps[orbit], shift);
        std::array<int, 5> columns{};
        columns[0] = pair_index * ORBITS + orbit;
        int slot = 1;
        bool allowed = true;
        for (Edge edge : triple_edges(triple)) {
          int column = edge_column[edge.first][edge.second];
          if (column < 0) {
            allowed = false;
            break;
          }
          columns[slot++] = column;
        }
        if (!allowed) continue;
        int cross = cross_column[orbit][shift];
        if (cross < 0) std::abort();
        columns[4] = cross;
        instance.rows.push_back({outer, orbit, shift, columns});
      }
    }
  }
  if (instance.rows.empty() || instance.rows.size() > MAX_ROWS) {
    std::abort();
  }

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
  for (int column = 0; column < instance.primary_columns; ++column) {
    bool nonempty = false;
    for (std::uint64_t word : instance.column_rows[column]) nonempty |= word;
    if (!nonempty) std::abort();
  }
  return instance;
}

bool covered(const ColumnBits &bits, int column) {
  return bits[column / 64] & (std::uint64_t{1} << (column % 64));
}

void cover(ColumnBits &bits, int column) {
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
  bool timed_out = false;
  std::vector<int> solution;

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

  bool solve(RowBits active, ColumnBits done, int depth) {
    if (expired()) return false;
    if (depth == instance.depth) return true;

    int best_column = -1;
    int best_size = std::numeric_limits<int>::max();
    for (int column = 0; column < instance.primary_columns; ++column) {
      if (covered(done, column)) continue;
      int size = intersection_size(active, instance.column_rows[column]);
      if (size < best_size) {
        best_size = size;
        best_column = column;
        if (size <= 1) break;
      }
    }
    if (best_column < 0 || best_size == 0) return false;

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
    for (int row : candidates) {
      RowBits next_active{};
      for (int word = 0; word < ROW_WORDS; ++word) {
        next_active[word] =
            active[word] & ~instance.conflicts[row][word];
      }
      ColumnBits next_done = done;
      for (int column : instance.rows[row].columns) {
        cover(next_done, column);
      }
      solution.push_back(row);
      if (solve(next_active, next_done, depth + 1)) return true;
      solution.pop_back();
      if (timed_out) return false;
    }
    return false;
  }
};

struct DlxSearch {
  const Instance &instance;
  std::uint64_t nodes = 0;
  std::uint64_t node_limit;
  std::chrono::steady_clock::time_point deadline;
  bool timed_out = false;
  std::vector<int> solution;
  std::vector<int> left, right, up, down, column, row, size;
  int next = 0;

  DlxSearch(
      const Instance &source,
      std::uint64_t limit,
      std::chrono::steady_clock::time_point end,
      std::uint64_t seed,
      const std::array<std::array<int, ORBITS>, FIXED> &hints)
      : instance(source), node_limit(limit), deadline(end) {
    const int capacity =
        1 + instance.columns +
        5 * static_cast<int>(instance.rows.size());
    left.resize(capacity);
    right.resize(capacity);
    up.resize(capacity);
    down.resize(capacity);
    column.resize(capacity);
    row.resize(capacity, -1);
    size.resize(instance.columns + 1);

    next = instance.columns + 1;
    left[0] = instance.primary_columns;
    right[0] = instance.primary_columns ? 1 : 0;
    for (int header = 1; header <= instance.columns; ++header) {
      if (header <= instance.primary_columns) {
        left[header] = header - 1;
        right[header] =
            header == instance.primary_columns ? 0 : header + 1;
      } else {
        // Secondary columns enforce at-most-one but are not required.
        left[header] = right[header] = header;
      }
      up[header] = down[header] = header;
      column[header] = header;
    }

    std::vector<int> order(instance.rows.size());
    std::iota(order.begin(), order.end(), 0);
    std::mt19937_64 random(seed);
    std::shuffle(order.begin(), order.end(), random);
    std::stable_sort(
        order.begin(), order.end(), [&](int left_row, int right_row) {
          const Row &left_candidate = instance.rows[left_row];
          const Row &right_candidate = instance.rows[right_row];
          bool left_match =
              hints[left_candidate.outer][left_candidate.orbit] ==
              left_candidate.shift;
          bool right_match =
              hints[right_candidate.outer][right_candidate.orbit] ==
              right_candidate.shift;
          return left_match > right_match;
        });
    for (int row_id : order) {
      int first = -1;
      for (int raw_column : instance.rows[row_id].columns) {
        int header = raw_column + 1;
        int node = next++;
        column[node] = header;
        row[node] = row_id;
        up[node] = up[header];
        down[node] = header;
        down[up[header]] = node;
        up[header] = node;
        ++size[header];
        if (first < 0) {
          first = node;
          left[node] = right[node] = node;
        } else {
          left[node] = left[first];
          right[node] = first;
          right[left[first]] = node;
          left[first] = node;
        }
      }
    }
    if (next != capacity) std::abort();
  }

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

  void cover(int header) {
    right[left[header]] = right[header];
    left[right[header]] = left[header];
    for (int i = down[header]; i != header; i = down[i]) {
      for (int j = right[i]; j != i; j = right[j]) {
        down[up[j]] = down[j];
        up[down[j]] = up[j];
        --size[column[j]];
      }
    }
  }

  void uncover(int header) {
    for (int i = up[header]; i != header; i = up[i]) {
      for (int j = left[i]; j != i; j = left[j]) {
        ++size[column[j]];
        down[up[j]] = j;
        up[down[j]] = j;
      }
    }
    right[left[header]] = header;
    left[right[header]] = header;
  }

  bool solve() {
    if (expired()) return false;
    if (right[0] == 0) return true;
    int best = right[0];
    for (int header = right[best]; header != 0; header = right[header]) {
      if (size[header] < size[best]) best = header;
      if (size[best] <= 1) break;
    }
    if (size[best] == 0) return false;
    cover(best);
    for (int candidate = down[best];
         candidate != best;
         candidate = down[candidate]) {
      solution.push_back(row[candidate]);
      for (int j = right[candidate]; j != candidate; j = right[j]) {
        cover(column[j]);
      }
      if (solve()) return true;
      for (int j = left[candidate]; j != candidate; j = left[j]) {
        uncover(column[j]);
      }
      solution.pop_back();
      if (timed_out) break;
    }
    uncover(best);
    return false;
  }
};

}  // namespace

int main(int argc, char **argv) {
  int centre = 0;
  double seconds = 600.0;
  std::uint64_t node_limit = 1000000000ULL;
  std::uint64_t seed = 835;
  std::string hint_path;
  std::string outers_text;
  for (int arg = 1; arg < argc; ++arg) {
    std::string option = argv[arg];
    if (option == "--centre" && arg + 1 < argc) {
      centre = std::stoi(argv[++arg]);
    } else if (option == "--seconds" && arg + 1 < argc) {
      seconds = std::stod(argv[++arg]);
    } else if (option == "--nodes" && arg + 1 < argc) {
      node_limit = std::stoull(argv[++arg]);
    } else if (option == "--seed" && arg + 1 < argc) {
      seed = std::stoull(argv[++arg]);
    } else if (option == "--hint" && arg + 1 < argc) {
      hint_path = argv[++arg];
    } else if (option == "--outers" && arg + 1 < argc) {
      outers_text = argv[++arg];
    } else {
      std::cerr << "usage: " << argv[0]
                << " [--centre i] [--outers i,j,...]"
                << " [--seconds n] [--nodes n] [--seed n]\n";
      return 2;
    }
  }
  if (!(0 <= centre && centre < FIXED)) return 2;
  std::vector<int> outers;
  if (outers_text.empty()) {
    for (int fixed = 0; fixed < FIXED; ++fixed) {
      if (fixed != centre) outers.push_back(fixed);
    }
  } else {
    std::stringstream stream(outers_text);
    std::string token;
    while (std::getline(stream, token, ',')) {
      if (token.empty()) return 2;
      outers.push_back(std::stoi(token));
    }
    std::sort(outers.begin(), outers.end());
    if (std::adjacent_find(outers.begin(), outers.end()) !=
        outers.end()) {
      return 2;
    }
    for (int outer : outers) {
      if (!(0 <= outer && outer < FIXED) || outer == centre) return 2;
    }
  }
  if (outers.empty() || outers.size() > PAIRS) return 2;
  std::array<std::array<int, ORBITS>, FIXED> hints{};
  for (auto &row : hints) row.fill(-1);
  if (!hint_path.empty()) {
    std::ifstream input(hint_path);
    if (!input) return 2;
    int outer, orbit, shift;
    while (input >> outer >> orbit >> shift) {
      if (!(0 <= outer && outer < FIXED &&
            0 <= orbit && orbit < ORBITS &&
            0 <= shift && shift < P)) {
        return 2;
      }
      hints[outer][orbit] = shift;
    }
  }

  Instance instance = build_instance(centre, outers);
  DlxSearch search{
      instance,
      node_limit,
      std::chrono::steady_clock::now() +
          std::chrono::milliseconds(
              static_cast<long long>(seconds * 1000.0)),
      seed,
      hints,
  };
  auto started = std::chrono::steady_clock::now();
  bool found = search.solve();
  double elapsed = std::chrono::duration<double>(
                       std::chrono::steady_clock::now() - started)
                       .count();

  std::cout << "{\"centre\":" << centre
            << ",\"outers\":[";
  for (int index = 0;
       index < static_cast<int>(instance.outers.size());
       ++index) {
    if (index) std::cout << ',';
    std::cout << instance.outers[index];
  }
  std::cout << ']'
            << ",\"candidate_rows\":" << instance.rows.size()
            << ",\"primary_columns\":" << instance.primary_columns
            << ",\"secondary_columns\":" << instance.cross_columns
            << ",\"nodes\":" << search.nodes
            << ",\"seconds\":" << elapsed;
  if (!found) {
    std::cout << ",\"status\":\""
              << (search.timed_out ? "UNKNOWN" : "INFEASIBLE")
              << "\"}\n";
    return search.timed_out ? 0 : 1;
  }
  if (search.solution.size() !=
      static_cast<std::size_t>(instance.depth)) {
    std::abort();
  }
  std::sort(
      search.solution.begin(),
      search.solution.end(),
      [&](int left, int right) {
        const Row &a = instance.rows[left];
        const Row &b = instance.rows[right];
        return std::tie(a.outer, a.orbit, a.shift) <
               std::tie(b.outer, b.orbit, b.shift);
      });
  std::cout << ",\"status\":\"SAT\",\"selected\":[";
  for (int index = 0; index < static_cast<int>(search.solution.size()); ++index) {
    if (index) std::cout << ',';
    const Row &row = instance.rows[search.solution[index]];
    std::cout << '[' << row.outer << ',' << row.orbit << ',' << row.shift
              << ']';
  }
  std::cout << "]}\n";
  return 0;
}
