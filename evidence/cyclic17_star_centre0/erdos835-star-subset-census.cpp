// Census the smallest incompatible subsets of the 13 complete centre-0
// fixed-Wallis slice families {0,j}, j=2,...,14.
//
// Each input row is 40 phase bytes.  A subset is compatible iff one row can
// be selected from every family so that no two selected rows agree in any
// coordinate.  This is the exact necessary cross-slot condition inherited
// by a full centre-0 star.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr int FAMILIES = 13;
constexpr int ORBITS = 40;
constexpr int MAX_ROWS = 1024;
constexpr int WORDS = MAX_ROWS / 64;

using Row = std::array<unsigned char, ORBITS>;
using Mask = std::array<std::uint64_t, WORDS>;

std::vector<Row> rows[FAMILIES];
std::vector<std::array<Mask, FAMILIES>> compat[FAMILIES];
std::uint64_t nodes = 0;
int choice[FAMILIES];

bool dfs(std::array<Mask, FAMILIES> &alive, std::uint16_t remaining) {
  ++nodes;
  if (!remaining) return true;

  int best = -1;
  int best_size = 0x7fffffff;
  for (int f = 0; f < FAMILIES; ++f) {
    if (!(remaining >> f & 1u)) continue;
    int size = 0;
    for (std::uint64_t word : alive[f]) {
      size += __builtin_popcountll(word);
    }
    if (size < best_size) {
      best = f;
      best_size = size;
      if (!size) break;
    }
  }
  if (best < 0 || !best_size) return false;

  const std::uint16_t next_remaining =
      remaining & ~(std::uint16_t{1} << best);
  for (int word = 0; word < WORDS; ++word) {
    std::uint64_t bits = alive[best][word];
    while (bits) {
      const int bit = __builtin_ctzll(bits);
      bits &= bits - 1;
      const int row = word * 64 + bit;
      std::array<Mask, FAMILIES> next = alive;
      for (int f = 0; f < FAMILIES; ++f) {
        if (!(next_remaining >> f & 1u)) continue;
        for (int w = 0; w < WORDS; ++w) {
          next[f][w] &= compat[best][row][f][w];
        }
      }
      choice[best] = row;
      if (dfs(next, next_remaining)) return true;
    }
  }
  return false;
}

std::string subset_string(std::uint16_t subset) {
  std::string answer = "[";
  bool first = true;
  for (int f = 0; f < FAMILIES; ++f) {
    if (!(subset >> f & 1u)) continue;
    if (!first) answer += ",";
    first = false;
    answer += "[0," + std::to_string(f + 2) + "]";
  }
  answer += "]";
  return answer;
}

}  // namespace

int main(int argc, char **argv) {
  if (argc != 3 && argc != 4) {
    std::fprintf(stderr,
                 "usage: %s FAMILY_DIR MAX_SIZE [FIVE_WITNESSES.jsonl]\n",
                 argv[0]);
    return 2;
  }
  const std::string directory = argv[1];
  const int max_size = std::stoi(argv[2]);
  if (max_size < 1 || max_size > FAMILIES) return 2;
  FILE *witnesses = nullptr;
  if (argc == 4) {
    witnesses = std::fopen(argv[3], "w");
    if (!witnesses) return 2;
  }

  for (int f = 0; f < FAMILIES; ++f) {
    const std::string path =
        directory + "/sols_0_" + std::to_string(f + 2) + ".bin";
    FILE *input = std::fopen(path.c_str(), "rb");
    if (!input) {
      std::fprintf(stderr, "cannot open %s\n", path.c_str());
      return 2;
    }
    Row row;
    while (std::fread(row.data(), 1, ORBITS, input) == ORBITS) {
      for (unsigned char phase : row) {
        if (phase > 16) {
          std::fprintf(stderr, "invalid phase in %s\n", path.c_str());
          return 2;
        }
      }
      rows[f].push_back(row);
    }
    if (!std::feof(input)) return 2;
    std::fclose(input);
    if (rows[f].empty() || rows[f].size() > MAX_ROWS) return 2;
  }

  for (int a = 0; a < FAMILIES; ++a) {
    compat[a].resize(rows[a].size());
  }
  for (int a = 0; a < FAMILIES; ++a) {
    for (int b = 0; b < FAMILIES; ++b) {
      if (a == b) continue;
      for (int r = 0; r < static_cast<int>(rows[a].size()); ++r) {
        Mask &mask = compat[a][r][b];
        mask.fill(0);
        for (int s = 0; s < static_cast<int>(rows[b].size()); ++s) {
          bool compatible = true;
          for (int orbit = 0; orbit < ORBITS; ++orbit) {
            if (rows[a][r][orbit] == rows[b][s][orbit]) {
              compatible = false;
              break;
            }
          }
          if (compatible) {
            mask[s / 64] |= std::uint64_t{1} << (s % 64);
          }
        }
      }
    }
  }

  std::array<Mask, FAMILIES> initial;
  for (int f = 0; f < FAMILIES; ++f) {
    initial[f].fill(0);
    for (int r = 0; r < static_cast<int>(rows[f].size()); ++r) {
      initial[f][r / 64] |= std::uint64_t{1} << (r % 64);
    }
  }

  std::printf("{\"family_sizes\":[");
  for (int f = 0; f < FAMILIES; ++f) {
    std::printf("%s%zu", f ? "," : "", rows[f].size());
  }
  std::printf("],\"levels\":[");
  bool first_level = true;
  for (int size = 1; size <= max_size; ++size) {
    std::uint64_t tested = 0;
    std::uint64_t unsat = 0;
    std::uint64_t level_nodes = 0;
    std::uint16_t first_unsat = 0;
    std::vector<std::uint16_t> first_sat;
    for (std::uint16_t subset = 1;
         subset < (std::uint16_t{1} << FAMILIES); ++subset) {
      if (__builtin_popcount(subset) != size) continue;
      ++tested;
      nodes = 0;
      std::fill(std::begin(choice), std::end(choice), -1);
      std::array<Mask, FAMILIES> alive = initial;
      const bool sat = dfs(alive, subset);
      level_nodes += nodes;
      if (sat) {
        if (first_sat.size() < 20) first_sat.push_back(subset);
        if (witnesses && size == 5) {
          std::fprintf(witnesses, "{\"families\":[");
          bool first = true;
          for (int f = 0; f < FAMILIES; ++f) {
            if (!(subset >> f & 1u)) continue;
            std::fprintf(witnesses, "%s%d", first ? "" : ",", f + 2);
            first = false;
          }
          std::fprintf(witnesses, "],\"rows\":[");
          first = true;
          for (int f = 0; f < FAMILIES; ++f) {
            if (!(subset >> f & 1u)) continue;
            if (choice[f] < 0) return 2;
            std::fprintf(witnesses, "%s%d", first ? "" : ",", choice[f]);
            first = false;
          }
          std::fprintf(witnesses, "]}\n");
        }
      } else {
        ++unsat;
        if (!first_unsat) first_unsat = subset;
      }
    }
    if (!first_level) std::printf(",");
    first_level = false;
    std::printf(
        "{\"size\":%d,\"tested\":%llu,\"unsat\":%llu,"
        "\"nodes\":%llu,\"first_unsat\":%s,\"sat_examples\":[",
        size,
        static_cast<unsigned long long>(tested),
        static_cast<unsigned long long>(unsat),
        static_cast<unsigned long long>(level_nodes),
        first_unsat ? subset_string(first_unsat).c_str() : "null");
    if (tested - unsat <= first_sat.size()) {
      for (std::size_t index = 0; index < first_sat.size(); ++index) {
        std::printf("%s%s", index ? "," : "",
                    subset_string(first_sat[index]).c_str());
      }
    }
    std::printf("]}");
  }
  std::printf("]}\n");
  if (witnesses) std::fclose(witnesses);
}
