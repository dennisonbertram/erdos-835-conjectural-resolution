// Exact centre star master over completely enumerated slice families.
//
// Families are binary files of 40-byte solutions (phase per orbit, seed-JSON
// convention).  Constraint: pick one solution per selected family so that for
// every orbit the picked phases are pairwise distinct (no shared
// (orbit, phase) slot).  For the 14-family centre stars this equals the tight
// 560-slot partition because every |A_k| = 14 (verified externally).
//
// Modes:
//   default            exhaustive DFS on all loaded families
//   --census k         sweep every subset of the loaded families of size<=k,
//                      existence check (cap 1) per subset, JSON line each
//
// Family selection:
//   --families i1,i2   load <dir>/sols_0_<i>.bin for each listed outer index
//   positional files   explicit family file paths (any centre)
//   (neither)          default centre-0 files sols_0_1.bin .. sols_0_14.bin

#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace {

constexpr int MAX_FAMILIES = 14;
constexpr int ORBITS = 40;
constexpr int MAX_ROWS = 1024;
constexpr int WORDS = MAX_ROWS / 64;

using Mask = std::array<std::uint64_t, WORDS>;

int n_families = 0;
std::vector<std::array<unsigned char, ORBITS>> rows[MAX_FAMILIES];
std::vector<std::array<Mask, MAX_FAMILIES>> compat[MAX_FAMILIES];

std::uint64_t solutions, nodes;
std::uint64_t cap = 20000000;
bool capped;
FILE *store = nullptr;
std::uint64_t store_limit = 100000;
std::uint64_t stored = 0;
std::uint32_t run_mask = 0;
int chosen[MAX_FAMILIES];
FILE *trace = nullptr;

void record() {
  ++solutions;
  if (store && stored < store_limit) {
    for (int f = 0; f < n_families; ++f) {
      if (run_mask >> f & 1) {
        std::fwrite(rows[f][chosen[f]].data(), 1, ORBITS, store);
      }
    }
    ++stored;
  }
  if (solutions % 1000000 == 0) {
    std::fprintf(stderr, "progress: %llu star solutions\n",
                 static_cast<unsigned long long>(solutions));
  }
  if (solutions >= cap) capped = true;
}

void dfs(std::array<Mask, MAX_FAMILIES> &alive, std::uint32_t remaining) {
  ++nodes;
  if (capped) return;
  if (!remaining) {
    record();
    return;
  }
  int best = -1, best_size = 0x7fffffff;
  for (int f = 0; f < n_families; ++f) {
    if (!(remaining >> f & 1)) continue;
    int size = 0;
    for (int w = 0; w < WORDS; ++w) size += __builtin_popcountll(alive[f][w]);
    if (size < best_size) {
      best_size = size;
      best = f;
      if (size == 0) break;
    }
  }
  if (trace) {
    std::fprintf(trace, "node=%llu branch_family=%d alive=%d\n",
                 static_cast<unsigned long long>(nodes), best, best_size);
  }
  if (best_size == 0) return;
  std::uint32_t next_remaining = remaining & ~(1u << best);
  int row_count = static_cast<int>(rows[best].size());
  for (int w = 0; w < WORDS; ++w) {
    std::uint64_t bits = alive[best][w];
    while (bits) {
      int bit = __builtin_ctzll(bits);
      bits &= bits - 1;
      int r = w * 64 + bit;
      if (r >= row_count) break;
      std::array<Mask, MAX_FAMILIES> next = alive;
      for (int f = 0; f < n_families; ++f) {
        if (!(next_remaining >> f & 1)) continue;
        for (int v = 0; v < WORDS; ++v) {
          next[f][v] &= compat[best][r][f][v];
        }
      }
      chosen[best] = r;
      if (trace) std::fprintf(trace, "try family=%d row=%d\n", best, r);
      dfs(next, next_remaining);
      if (trace) std::fprintf(trace, "backtrack family=%d row=%d\n", best, r);
      if (capped) return;
    }
  }
}

// Exhaustive DFS on the given subset of loaded families.
void run(std::uint32_t subset) {
  solutions = nodes = 0;
  capped = false;
  run_mask = subset;
  std::array<Mask, MAX_FAMILIES> alive;
  for (int f = 0; f < n_families; ++f) {
    alive[f].fill(0);
    if (!(subset >> f & 1)) continue;
    for (int r = 0; r < static_cast<int>(rows[f].size()); ++r) {
      alive[f][r / 64] |= std::uint64_t{1} << (r % 64);
    }
  }
  dfs(alive, subset);
}

}  // namespace

int main(int argc, char **argv) {
  std::string dir = ".";
  std::string store_path;
  std::vector<std::string> family_files;
  std::vector<int> family_indices;
  int census_max = 0;
  for (int arg = 1; arg < argc; ++arg) {
    std::string option = argv[arg];
    if (option == "--dir" && arg + 1 < argc) dir = argv[++arg];
    else if (option == "--store" && arg + 1 < argc) store_path = argv[++arg];
    else if (option == "--cap" && arg + 1 < argc) cap = std::stoull(argv[++arg]);
    else if (option == "--store-limit" && arg + 1 < argc)
      store_limit = std::stoull(argv[++arg]);
    else if (option == "--census" && arg + 1 < argc)
      census_max = std::stoi(argv[++arg]);
    else if (option == "--trace" && arg + 1 < argc) {
      trace = std::fopen(argv[++arg], "w");
      if (!trace) { std::fprintf(stderr, "cannot open trace file\n"); return 2; }
    } else if (option == "--families" && arg + 1 < argc) {
      std::string list = argv[++arg];
      size_t position = 0;
      while (position < list.size()) {
        size_t comma = list.find(',', position);
        if (comma == std::string::npos) comma = list.size();
        family_indices.push_back(
            std::stoi(list.substr(position, comma - position)));
        position = comma + 1;
      }
    } else if (option[0] != '-') {
      family_files.push_back(option);
    } else {
      std::fprintf(stderr,
                   "usage: %s [--dir d] [--families i1,i2,...] [--census k]"
                   " [--store f] [--cap n] [--store-limit n] [--trace f]"
                   " [file...]\n",
                   argv[0]);
      return 2;
    }
  }
  if (!family_files.empty() && !family_indices.empty()) {
    std::fprintf(stderr, "--families and positional files are exclusive\n");
    return 2;
  }
  if (family_files.empty()) {
    if (family_indices.empty()) {
      for (int j = 1; j <= 14; ++j) family_indices.push_back(j);
    }
    for (int index : family_indices) {
      char path[4096];
      std::snprintf(path, sizeof path, "%s/sols_0_%d.bin", dir.c_str(), index);
      family_files.push_back(path);
    }
  }
  n_families = static_cast<int>(family_files.size());
  if (n_families < 1 || n_families > MAX_FAMILIES) {
    std::fprintf(stderr, "need 1..%d families, got %d\n", MAX_FAMILIES,
                 n_families);
    return 2;
  }

  for (int f = 0; f < n_families; ++f) {
    FILE *in = std::fopen(family_files[f].c_str(), "rb");
    if (!in) { std::fprintf(stderr, "missing %s\n", family_files[f].c_str()); return 2; }
    std::array<unsigned char, ORBITS> buffer;
    while (std::fread(buffer.data(), 1, ORBITS, in) == ORBITS) {
      rows[f].push_back(buffer);
    }
    std::fclose(in);
    if (rows[f].empty() || rows[f].size() > MAX_ROWS) {
      std::fprintf(stderr, "bad family size %zu for %s\n", rows[f].size(),
                   family_files[f].c_str());
      return 2;
    }
  }

  for (int a = 0; a < n_families; ++a) compat[a].resize(rows[a].size());
  for (int a = 0; a < n_families; ++a) {
    for (int b = 0; b < n_families; ++b) {
      if (a == b) continue;
      for (int r = 0; r < static_cast<int>(rows[a].size()); ++r) {
        Mask &mask = compat[a][r][b];
        mask.fill(0);
        const unsigned char *pa = rows[a][r].data();
        for (int s = 0; s < static_cast<int>(rows[b].size()); ++s) {
          const unsigned char *pb = rows[b][s].data();
          bool ok = true;
          for (int k = 0; k < ORBITS; ++k) {
            if (pa[k] == pb[k]) { ok = false; break; }
          }
          if (ok) mask[s / 64] |= std::uint64_t{1} << (s % 64);
        }
      }
    }
  }

  if (census_max > 0) {
    std::uint64_t compatible_by_size[MAX_FAMILIES + 1] = {};
    std::uint64_t total_by_size[MAX_FAMILIES + 1] = {};
    std::uint64_t saved_cap = cap;
    std::printf("[");
    bool first_line = true;
    for (std::uint32_t subset = 1; subset < (1u << n_families); ++subset) {
      int size = __builtin_popcount(subset);
      if (size > census_max) continue;
      cap = 1;  // existence only
      run(subset);
      cap = saved_cap;
      ++total_by_size[size];
      if (solutions > 0) ++compatible_by_size[size];
      std::printf("%s\n{\"subset\":[", first_line ? "" : ",");
      first_line = false;
      bool first = true;
      for (int f = 0; f < n_families; ++f) {
        if (subset >> f & 1) {
          std::printf("%s%d", first ? "" : ",",
                      family_indices.empty() ? f : family_indices[f]);
          first = false;
        }
      }
      std::printf("],\"compatible\":%s,\"nodes\":%llu}",
                  solutions > 0 ? "true" : "false",
                  static_cast<unsigned long long>(nodes));
    }
    std::printf("\n]\n");
    for (int size = 1; size <= census_max; ++size) {
      std::fprintf(stderr,
                   "size=%d total=%llu compatible=%llu incompatible=%llu\n",
                   size,
                   static_cast<unsigned long long>(total_by_size[size]),
                   static_cast<unsigned long long>(compatible_by_size[size]),
                   static_cast<unsigned long long>(total_by_size[size] -
                                                   compatible_by_size[size]));
    }
    return 0;
  }

  if (!store_path.empty()) {
    store = std::fopen(store_path.c_str(), "wb");
    if (!store) { std::fprintf(stderr, "cannot open %s\n", store_path.c_str()); return 2; }
  }
  auto started = std::chrono::steady_clock::now();
  run((1u << n_families) - 1);
  double elapsed = std::chrono::duration<double>(
                       std::chrono::steady_clock::now() - started).count();
  if (store) std::fclose(store);

  std::printf("{\"families\":[");
  for (int f = 0; f < n_families; ++f) {
    std::printf("%s\"%s\"", f ? "," : "", family_files[f].c_str());
  }
  std::printf("],\"family_sizes\":[");
  for (int f = 0; f < n_families; ++f)
    std::printf("%s%zu", f ? "," : "", rows[f].size());
  std::printf("],\"star_solutions\":%llu,\"capped\":%s,\"nodes\":%llu,"
              "\"seconds\":%.3f,\"stored\":%llu}\n",
              static_cast<unsigned long long>(solutions),
              capped ? "true" : "false",
              static_cast<unsigned long long>(nodes), elapsed,
              static_cast<unsigned long long>(stored));
  return 0;
}
