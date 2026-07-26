// Count ALL exact-cover solutions of one fixed-pair cyclic radius-five slice.
//
// Instance construction is copied verbatim from
// evidence/odd_graph_local_ball/search_radius5_golf_cyclic_slice_exact_cover.cpp
// (whose FIRST_HALF table equals FIRST_HALF_COLUMNS in
// evidence/global_latin_audit.py, the audited Wallis source).
//
// Counts every exact cover (one translate per each of the 40 moving-triple
// orbits covering the 120 residual edges exactly once), with a hard cap,
// progress every 1e6 solutions, and optional storage of solutions as
// 40 phase bytes each (phase = (17 - shift) % 17, the seed-JSON convention).

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <set>
#include <string>
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
      if (allowed) instance.rows.push_back({orbit, shift, columns});
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

int intersection_size(const RowBits &left, const RowBits &right) {
  int answer = 0;
  for (int word = 0; word < ROW_WORDS; ++word) {
    answer += __builtin_popcountll(left[word] & right[word]);
  }
  return answer;
}

struct Counter {
  const Instance &instance;
  std::uint64_t cap;
  bool alt = false;  // alternate tie-breaking: completeness cross-check
  std::uint64_t count = 0;
  std::uint64_t nodes = 0;
  bool capped = false;
  FILE *store = nullptr;
  std::uint64_t store_limit = 0;
  std::uint64_t stored = 0;
  std::vector<int> solution;
  std::chrono::steady_clock::time_point started =
      std::chrono::steady_clock::now();

  void record() {
    ++count;
    if (store && stored < store_limit) {
      unsigned char phases[ORBITS];
      for (int row : solution) {
        const Row &selected = instance.rows[row];
        phases[selected.orbit] =
            static_cast<unsigned char>((P - selected.shift) % P);
      }
      std::fwrite(phases, 1, ORBITS, store);
      ++stored;
    }
    if (count % 1000000 == 0) {
      double elapsed = std::chrono::duration<double>(
                           std::chrono::steady_clock::now() - started)
                           .count();
      std::fprintf(stderr,
                   "progress: %llu solutions, %.1f s, %.0f sol/s\n",
                   static_cast<unsigned long long>(count), elapsed,
                   count / elapsed);
      std::fflush(stderr);
    }
    if (count >= cap) capped = true;
  }

  void solve(const RowBits &active, const ColumnBits &covered, int depth) {
    if (capped) return;
    ++nodes;
    if (depth == ORBITS) {
      record();
      return;
    }
    int best_column = -1;
    int best_size = 0x7fffffff;
    if (!alt) {
      for (int column = 0; column < COLUMNS; ++column) {
        if (column_is_covered(covered, column)) continue;
        int size = intersection_size(active, instance.column_rows[column]);
        if (size < best_size) {
          best_size = size;
          best_column = column;
          if (size <= 1) break;
        }
      }
    } else {
      // Alternate: scan columns high->low, prefer the LAST minimal column.
      for (int column = COLUMNS - 1; column >= 0; --column) {
        if (column_is_covered(covered, column)) continue;
        int size = intersection_size(active, instance.column_rows[column]);
        if (size < best_size) {
          best_size = size;
          best_column = column;
          if (size <= 1) break;
        }
      }
    }
    if (best_size == 0 || best_column < 0) return;
    int word_begin = alt ? ROW_WORDS - 1 : 0;
    int word_step = alt ? -1 : 1;
    for (int word = word_begin; word >= 0 && word < ROW_WORDS;
         word += word_step) {
      std::uint64_t bits =
          active[word] & instance.column_rows[best_column][word];
      while (bits) {
        int bit = alt ? 63 - __builtin_clzll(bits) : __builtin_ctzll(bits);
        int row = word * 64 + bit;
        bits &= ~(std::uint64_t{1} << bit);
        RowBits next_active;
        for (int inner = 0; inner < ROW_WORDS; ++inner) {
          next_active[inner] =
              active[inner] & ~instance.conflicts[row][inner];
        }
        ColumnBits next_covered = covered;
        for (int column : instance.rows[row].columns) {
          next_covered[column / 64] |= std::uint64_t{1} << (column % 64);
        }
        solution.push_back(row);
        solve(next_active, next_covered, depth + 1);
        solution.pop_back();
        if (capped) return;
      }
    }
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
  std::uint64_t cap = 20000000;
  std::string store_path;
  std::uint64_t store_limit = 500000;
  bool alt = false;
  for (int arg = 1; arg < argc; ++arg) {
    std::string option = argv[arg];
    if (option == "--pair" && arg + 1 < argc) {
      std::tie(first, second) = parse_pair(argv[++arg]);
    } else if (option == "--cap" && arg + 1 < argc) {
      cap = std::stoull(argv[++arg]);
    } else if (option == "--store" && arg + 1 < argc) {
      store_path = argv[++arg];
    } else if (option == "--store-limit" && arg + 1 < argc) {
      store_limit = std::stoull(argv[++arg]);
    } else if (option == "--alt") {
      alt = true;
    } else {
      std::fprintf(stderr,
                   "usage: %s [--pair i,j] [--cap n] [--store path]"
                   " [--store-limit n]\n",
                   argv[0]);
      return 2;
    }
  }

  Instance instance = build_instance(first, second);
  Counter counter{instance, cap};
  counter.store_limit = store_limit;
  if (!store_path.empty()) {
    counter.store = std::fopen(store_path.c_str(), "wb");
    if (!counter.store) {
      std::fprintf(stderr, "cannot open store file: %s\n",
                   store_path.c_str());
      return 2;
    }
  }

  RowBits active{};
  for (int row = 0; row < static_cast<int>(instance.rows.size()); ++row) {
    active[row / 64] |= std::uint64_t{1} << (row % 64);
  }
  ColumnBits covered{};
  counter.solve(active, covered, 0);
  double elapsed = std::chrono::duration<double>(
                       std::chrono::steady_clock::now() - counter.started)
                       .count();
  if (counter.store) std::fclose(counter.store);

  std::printf(
      "{\"pair\":[%d,%d],\"rows\":%zu,\"count\":%llu,\"capped\":%s,"
      "\"nodes\":%llu,\"seconds\":%.3f,\"stored\":%llu,"
      "\"store_complete\":%s}\n",
      first, second, instance.rows.size(),
      static_cast<unsigned long long>(counter.count),
      counter.capped ? "true" : "false",
      static_cast<unsigned long long>(counter.nodes), elapsed,
      static_cast<unsigned long long>(counter.stored),
      (!store_path.empty() && counter.stored == counter.count) ? "true"
                                                               : "false");
  return 0;
}
