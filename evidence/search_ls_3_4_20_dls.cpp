// Certificate-producing search for LS(3,4,20) from the DLS 10-system core.
//
// The classical DLS construction gives ten pairwise disjoint SQS(20)s.
// Every triple then has seven unused extensions.  We use randomized
// Algorithm X to choose five further disjoint SQSs.  At that point every
// triple has two unused extensions; the remaining 570 blocks split into
// two SQSs iff the graph joining the two extensions of each triple is
// bipartite.  Thus a successful run produces all seventeen systems and a
// complete 4,845-line colouring certificate.
//
// Search failure or timeout proves nothing.  Verify any emitted certificate
// independently with verify_ls_3_4_20_certificate.py.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

constexpr int V = 20;
constexpr int NB = 4845;
constexpr int NT = 1140;
using Block = std::array<int, 4>;

uint32_t mask(std::initializer_list<int> xs) {
  uint32_t m = 0;
  for (int x : xs) m |= uint32_t{1} << x;
  return m;
}

uint32_t mask(const Block& b) {
  return mask({b[0], b[1], b[2], b[3]});
}

struct Instance {
  std::vector<Block> blocks;
  std::vector<std::array<int, 4>> row_columns;
  std::vector<std::vector<int>> column_rows;
  std::unordered_map<uint32_t, int> block_index;
  std::unordered_map<uint32_t, int> triple_index;

  Instance() {
    for (int a = 0; a < V; ++a)
      for (int b = a + 1; b < V; ++b)
        for (int c = b + 1; c < V; ++c) {
          const int ti = static_cast<int>(triple_index.size());
          triple_index.emplace(mask({a, b, c}), ti);
        }
    if (static_cast<int>(triple_index.size()) != NT)
      throw std::runtime_error("triple count");

    for (int a = 0; a < V; ++a)
      for (int b = a + 1; b < V; ++b)
        for (int c = b + 1; c < V; ++c)
          for (int d = c + 1; d < V; ++d) {
            Block block{a, b, c, d};
            block_index.emplace(mask(block), static_cast<int>(blocks.size()));
            blocks.push_back(block);
          }
    if (static_cast<int>(blocks.size()) != NB)
      throw std::runtime_error("block count");

    row_columns.resize(NB);
    column_rows.resize(NT);
    for (int r = 0; r < NB; ++r) {
      int at = 0;
      for (int omit = 0; omit < 4; ++omit) {
        uint32_t t = 0;
        for (int j = 0; j < 4; ++j)
          if (j != omit) t |= uint32_t{1} << blocks[r][j];
        const int c = triple_index.at(t);
        row_columns[r][at++] = c;
        column_rows[c].push_back(r);
      }
    }
    for (const auto& rows : column_rows)
      if (static_cast<int>(rows.size()) != 17)
        throw std::runtime_error("triple degree");
  }
};

const std::array<std::array<int, 4>, 30> kSqs10{{
    {0, 1, 2, 3}, {0, 1, 4, 5}, {0, 1, 6, 7}, {0, 1, 8, 9},
    {0, 2, 4, 7}, {0, 2, 5, 8}, {0, 2, 6, 9}, {0, 3, 4, 9},
    {0, 3, 5, 6}, {0, 3, 7, 8}, {0, 4, 6, 8}, {0, 5, 7, 9},
    {1, 2, 4, 8}, {1, 2, 5, 6}, {1, 2, 7, 9}, {1, 3, 4, 7},
    {1, 3, 5, 9}, {1, 3, 6, 8}, {1, 4, 6, 9}, {1, 5, 7, 8},
    {2, 3, 4, 6}, {2, 3, 5, 7}, {2, 3, 8, 9}, {2, 4, 5, 9},
    {2, 6, 7, 8}, {3, 4, 5, 8}, {3, 6, 7, 9}, {4, 5, 6, 7},
    {4, 7, 8, 9}, {5, 6, 8, 9},
}};

std::vector<std::vector<int>> dls_core(const Instance& in) {
  constexpr int n = 5;
  std::array<std::array<int, 10>, 10> latin{};
  for (int i = 0; i < 10; ++i)
    for (int j = 0; j < 10; ++j) {
      if (i < n && j < n)
        latin[i][j] = (i - j + n) % n;
      else if (i < n)
        latin[i][j] = n + (i + (j - n)) % n;
      else if (j < n)
        latin[i][j] = n + ((i - n) + j - 1 + n) % n;
      else
        latin[i][j] = ((i - n) - (j - n) + n) % n;
    }

  // Verify the Latin and intercalate-free properties used by DLS.
  for (int i = 0; i < 10; ++i) {
    std::array<int, 10> seen_row{};
    std::array<int, 10> seen_col{};
    for (int j = 0; j < 10; ++j) {
      ++seen_row[latin[i][j]];
      ++seen_col[latin[j][i]];
    }
    for (int x = 0; x < 10; ++x)
      if (seen_row[x] != 1 || seen_col[x] != 1)
        throw std::runtime_error("Latin square");
  }
  for (int i = 0; i < 10; ++i)
    for (int k = i + 1; k < 10; ++k)
      for (int j = 0; j < 10; ++j)
        for (int l = j + 1; l < 10; ++l)
          if (latin[i][j] == latin[k][l] &&
              latin[i][l] == latin[k][j])
            throw std::runtime_error("Latin intercalate");

  std::vector<std::vector<int>> systems(10);
  std::vector<int> owner(NB, -1);
  for (int i = 0; i < 10; ++i) {
    const auto& alpha = latin[i];
    std::array<int, 10> inverse{};
    for (int x = 0; x < 10; ++x) inverse[alpha[x]] = x;

    std::vector<uint8_t> selected(NB, 0);
    auto add = [&](uint32_t m) {
      const int r = in.block_index.at(m);
      if (!selected[r]) {
        selected[r] = 1;
        systems[i].push_back(r);
      }
    };

    for (const auto& base : kSqs10) {
      for (int singled = 0; singled < 4; ++singled) {
        uint32_t first = uint32_t{1} << (10 + alpha[base[singled]]);
        uint32_t second = uint32_t{1} << inverse[base[singled]];
        for (int j = 0; j < 4; ++j) {
          if (j == singled) continue;
          first |= uint32_t{1} << base[j];
          second |= uint32_t{1} << (10 + base[j]);
        }
        add(first);
        add(second);
      }
    }
    for (int x = 0; x < 10; ++x)
      for (int y = x + 1; y < 10; ++y)
        add(mask({x, y, 10 + alpha[x], 10 + alpha[y]}));

    if (static_cast<int>(systems[i].size()) != 285)
      throw std::runtime_error("DLS class size");
    std::array<int, NT> cover{};
    for (int r : systems[i])
      for (int c : in.row_columns[r]) ++cover[c];
    for (int c : cover)
      if (c != 1) throw std::runtime_error("DLS class is not SQS");
    for (int r : systems[i]) {
      if (owner[r] >= 0) throw std::runtime_error("DLS overlap");
      owner[r] = i;
    }
  }
  return systems;
}

using Pair = std::array<int, 2>;
using Factor = std::array<Pair, 5>;
using FactorTriple = std::array<Factor, 3>;

const std::array<FactorTriple, 3> kR{{
    {{
        {{{6, 7}, {8, 9}, {1, 2}, {3, 4}, {0, 5}}},
        {{{2, 3}, {0, 4}, {5, 6}, {1, 9}, {7, 8}}},
        {{{0, 1}, {3, 7}, {4, 6}, {5, 9}, {2, 8}}},
    }},
    {{
        {{{7, 9}, {2, 4}, {5, 8}, {1, 3}, {0, 6}}},
        {{{2, 9}, {1, 4}, {6, 8}, {0, 3}, {5, 7}}},
        {{{3, 8}, {1, 5}, {0, 2}, {6, 9}, {4, 7}}},
    }},
    {{
        {{{0, 7}, {3, 9}, {4, 8}, {1, 6}, {2, 5}}},
        {{{4, 9}, {1, 7}, {2, 6}, {0, 8}, {3, 5}}},
        {{{2, 7}, {1, 8}, {0, 9}, {4, 5}, {3, 6}}},
    }},
}};

const std::array<FactorTriple, 3> kT{{
    {{
        {{{6, 7}, {8, 9}, {1, 2}, {3, 4}, {0, 5}}},
        {{{2, 3}, {0, 4}, {5, 9}, {1, 6}, {7, 8}}},
        {{{0, 1}, {3, 8}, {2, 7}, {4, 9}, {5, 6}}},
    }},
    {{
        {{{7, 9}, {2, 4}, {5, 8}, {1, 3}, {0, 6}}},
        {{{1, 4}, {0, 3}, {6, 9}, {5, 7}, {2, 8}}},
        {{{6, 8}, {4, 5}, {1, 7}, {3, 9}, {0, 2}}},
    }},
    {{
        {{{0, 7}, {4, 6}, {1, 8}, {2, 9}, {3, 5}}},
        {{{1, 9}, {3, 6}, {0, 8}, {2, 5}, {4, 7}}},
        {{{1, 5}, {3, 7}, {0, 9}, {2, 6}, {4, 8}}},
    }},
}};

std::array<std::array<int, 10>, 3> random_disjoint_sqs10(
    std::mt19937_64& rng) {
  std::array<std::array<int, 10>, 3> permutations{};
  std::array<uint8_t, 210> used{};
  std::unordered_map<uint32_t, int> small_block_index;
  int next = 0;
  for (int a = 0; a < 10; ++a)
    for (int b = a + 1; b < 10; ++b)
      for (int c = b + 1; c < 10; ++c)
        for (int d = c + 1; d < 10; ++d)
          small_block_index.emplace(mask({a, b, c, d}), next++);
  if (next != 210) throw std::runtime_error("small block count");

  int accepted = 0;
  for (int attempt = 0; attempt < 2'000'000 && accepted < 3; ++attempt) {
    std::array<int, 10> permutation{};
    std::iota(permutation.begin(), permutation.end(), 0);
    std::shuffle(permutation.begin(), permutation.end(), rng);
    std::array<int, 30> rows{};
    bool disjoint = true;
    int at = 0;
    for (const auto& base : kSqs10) {
      uint32_t m = 0;
      for (int x : base) m |= uint32_t{1} << permutation[x];
      const int r = small_block_index.at(m);
      rows[at++] = r;
      disjoint &= !used[r];
    }
    if (!disjoint) continue;
    permutations[accepted++] = permutation;
    for (int r : rows) used[r] = 1;
  }
  if (accepted != 3) throw std::runtime_error("disjoint SQS(10) sampling");
  return permutations;
}

void add_db_extensions(const Instance& in,
                       std::vector<std::vector<int>>& systems,
                       const std::array<std::array<int, 10>, 3>&
                           base_permutations,
                       int count) {
  if (systems.size() != 10) throw std::runtime_error("DB input");
  if (count < 0 || count > 3) throw std::runtime_error("DB count");
  std::vector<int> owner(NB, -1);
  for (int c = 0; c < static_cast<int>(systems.size()); ++c)
    for (int r : systems[c]) owner[r] = c;

  // The last three rows of the H_9 Latin rectangle.  At the coarse
  // 3-by-3 level they are the row (T_2,T_3,T_1), expanded cyclically.
  for (int e = 0; e < count; ++e) {
    std::vector<uint8_t> selected(NB, 0);
    std::vector<int> system;
    auto add = [&](uint32_t m) {
      const int r = in.block_index.at(m);
      if (!selected[r]) {
        selected[r] = 1;
        system.push_back(r);
      }
    };

    const auto& permutation = base_permutations[e];
    for (const auto& base : kSqs10) {
      uint32_t lower = 0;
      uint32_t upper = 0;
      for (int x : base) {
        lower |= uint32_t{1} << permutation[x];
        upper |= uint32_t{1} << (10 + permutation[x]);
      }
      add(lower);
      add(upper);
    }

    for (int coarse_column = 0; coarse_column < 3; ++coarse_column) {
      const int coarse_symbol = (coarse_column + 1) % 3;
      for (int subcolumn = 0; subcolumn < 3; ++subcolumn) {
        const Factor& lower_factor = kR[coarse_column][subcolumn];
        const Factor& upper_factor =
            kT[coarse_symbol][(subcolumn + e) % 3];
        for (const Pair& lower_pair : lower_factor)
          for (const Pair& upper_pair : upper_factor)
            add(mask({lower_pair[0], lower_pair[1],
                      10 + upper_pair[0], 10 + upper_pair[1]}));
      }
    }

    if (system.size() != 285) throw std::runtime_error("DB class size");
    std::array<int, NT> cover{};
    for (int r : system) {
      if (owner[r] >= 0) throw std::runtime_error("DB overlap");
      for (int c : in.row_columns[r]) ++cover[c];
    }
    for (int c : cover)
      if (c != 1) throw std::runtime_error("DB class is not SQS");
    const int colour = static_cast<int>(systems.size());
    for (int r : system) owner[r] = colour;
    systems.push_back(std::move(system));
  }
}

struct ExactCover {
  const Instance& in;
  std::mt19937_64& rng;
  std::vector<uint8_t> active;
  std::vector<uint8_t> covered;
  std::vector<int> solution;
  uint64_t nodes = 0;
  uint64_t node_limit;
  std::chrono::steady_clock::time_point deadline;

  ExactCover(const Instance& instance, const std::vector<uint8_t>& allowed,
             std::mt19937_64& generator, uint64_t limit, double seconds)
      : in(instance),
        rng(generator),
        active(allowed),
        covered(NT, 0),
        node_limit(limit),
        deadline(std::chrono::steady_clock::now() +
                 std::chrono::duration_cast<std::chrono::steady_clock::duration>(
                     std::chrono::duration<double>(seconds))) {}

  bool search(int depth = 0) {
    if (++nodes > node_limit || std::chrono::steady_clock::now() > deadline)
      return false;
    if (depth == 285) return true;

    int chosen_column = -1;
    int minimum = std::numeric_limits<int>::max();
    for (int c = 0; c < NT; ++c) {
      if (covered[c]) continue;
      int count = 0;
      for (int r : in.column_rows[c]) count += active[r];
      if (count < minimum) {
        minimum = count;
        chosen_column = c;
        if (minimum <= 1) break;
      }
    }
    if (chosen_column < 0) return depth == 285;
    if (minimum == 0) return false;

    std::vector<int> candidates;
    for (int r : in.column_rows[chosen_column])
      if (active[r]) candidates.push_back(r);
    std::shuffle(candidates.begin(), candidates.end(), rng);

    for (int r : candidates) {
      if (!active[r]) continue;
      bool legal = true;
      for (int c : in.row_columns[r]) legal &= !covered[c];
      if (!legal) continue;

      std::vector<int> disabled;
      for (int c : in.row_columns[r]) {
        covered[c] = 1;
        for (int rr : in.column_rows[c]) {
          if (active[rr]) {
            active[rr] = 0;
            disabled.push_back(rr);
          }
        }
      }
      solution.push_back(r);
      if (search(depth + 1)) return true;
      solution.pop_back();
      for (int rr : disabled) active[rr] = 1;
      for (int c : in.row_columns[r]) covered[c] = 0;
    }
    return false;
  }
};

struct ResidualTabu {
  static constexpr int q = 7;
  const Instance& in;
  const std::vector<std::vector<int>>& dls;
  std::mt19937_64 rng;
  std::vector<int> residual;
  std::vector<int> local_of;
  std::vector<std::array<int, 24>> adj;
  std::vector<uint8_t> colour;
  std::vector<std::array<uint8_t, q>> count;
  std::vector<std::array<int, q>> tabu;
  std::vector<int> bad;
  std::vector<int> bad_pos;
  int conflicts = 0;
  int global_best = std::numeric_limits<int>::max();

  ResidualTabu(const Instance& instance,
               const std::vector<std::vector<int>>& core, uint64_t seed)
      : in(instance), dls(core), rng(seed), local_of(NB, -1) {
    std::vector<uint8_t> unused(NB, 1);
    for (const auto& system : dls)
      for (int r : system) unused[r] = 0;
    for (int r = 0; r < NB; ++r)
      if (unused[r]) {
        local_of[r] = static_cast<int>(residual.size());
        residual.push_back(r);
      }
    if (residual.size() != 1995) throw std::runtime_error("DLS residual");

    std::vector<std::vector<int>> tmp(residual.size());
    for (int c = 0; c < NT; ++c) {
      std::array<int, q> star{};
      int at = 0;
      for (int r : in.column_rows[c])
        if (unused[r]) star[at++] = local_of[r];
      if (at != q) throw std::runtime_error("residual star");
      for (int i = 0; i < q; ++i)
        for (int j = i + 1; j < q; ++j) {
          tmp[star[i]].push_back(star[j]);
          tmp[star[j]].push_back(star[i]);
        }
    }
    adj.resize(residual.size());
    for (int v = 0; v < static_cast<int>(residual.size()); ++v) {
      std::sort(tmp[v].begin(), tmp[v].end());
      tmp[v].erase(std::unique(tmp[v].begin(), tmp[v].end()), tmp[v].end());
      if (tmp[v].size() != 24) throw std::runtime_error("residual degree");
      std::copy(tmp[v].begin(), tmp[v].end(), adj[v].begin());
    }
    colour.resize(residual.size());
    count.resize(residual.size());
    tabu.resize(residual.size());
    bad_pos.resize(residual.size(), -1);
  }

  int random_int(int n) {
    return static_cast<int>(rng() % static_cast<uint64_t>(n));
  }

  void set_bad(int v, bool value) {
    if (value && bad_pos[v] < 0) {
      bad_pos[v] = static_cast<int>(bad.size());
      bad.push_back(v);
    } else if (!value && bad_pos[v] >= 0) {
      const int p = bad_pos[v];
      const int w = bad.back();
      bad[p] = w;
      bad_pos[w] = p;
      bad.pop_back();
      bad_pos[v] = -1;
    }
  }

  void initialize() {
    std::fill(colour.begin(), colour.end(), uint8_t{255});

    // Seed with the three exact DB classes, then deliberately perturb them.
    // Without the perturbation they form a maximal 13-system core and a
    // conflict-only walk could never move one of their blocks.
    auto seeded = dls;
    const auto permutations = random_disjoint_sqs10(rng);
    add_db_extensions(in, seeded, permutations, 3);
    for (int c = 0; c < 3; ++c)
      for (int r : seeded[10 + c]) colour[local_of[r]] = c;

    std::vector<int> order;
    for (int v = 0; v < static_cast<int>(residual.size()); ++v)
      if (colour[v] >= q) order.push_back(v);
    std::shuffle(order.begin(), order.end(), rng);
    for (int v : order) {
      std::array<int, q> score{};
      for (int u : adj[v])
        if (colour[u] < q) ++score[colour[u]];
      const int minimum = *std::min_element(score.begin(), score.end());
      std::array<int, q> choices{};
      int nchoices = 0;
      for (int c = 0; c < q; ++c)
        if (score[c] == minimum) choices[nchoices++] = c;
      colour[v] = choices[random_int(nchoices)];
    }
    for (int j = 0; j < 24; ++j) {
      const int v = random_int(static_cast<int>(residual.size()));
      colour[v] = random_int(q);
    }

    for (auto& row : count) row.fill(0);
    for (auto& row : tabu) row.fill(0);
    conflicts = 0;
    for (int v = 0; v < static_cast<int>(residual.size()); ++v)
      for (int u : adj[v]) ++count[v][colour[u]];
    for (int v = 0; v < static_cast<int>(residual.size()); ++v)
      conflicts += count[v][colour[v]];
    conflicts /= 2;
    bad.clear();
    std::fill(bad_pos.begin(), bad_pos.end(), -1);
    for (int v = 0; v < static_cast<int>(residual.size()); ++v)
      set_bad(v, count[v][colour[v]] != 0);
    global_best = std::min(global_best, conflicts);
  }

  void make_move(int v, int nc, int iteration) {
    const int oc = colour[v];
    const int delta = int(count[v][nc]) - int(count[v][oc]);
    for (int u : adj[v]) {
      --count[u][oc];
      ++count[u][nc];
    }
    colour[v] = nc;
    conflicts += delta;
    tabu[v][oc] =
        iteration + 5 + random_int(10) + std::min<int>(100, bad.size() / 8);
    set_bad(v, count[v][colour[v]] != 0);
    for (int u : adj[v]) set_bad(u, count[u][colour[u]] != 0);
    global_best = std::min(global_best, conflicts);
  }

  bool run(uint64_t iterations) {
    initialize();
    int local_best = conflicts;
    uint64_t last_improvement = 0;
    for (uint64_t it64 = 1; it64 <= iterations; ++it64) {
      if (conflicts == 0) return true;
      const int it = static_cast<int>(
          std::min<uint64_t>(it64, std::numeric_limits<int>::max() / 2));
      int chosen_v = -1;
      int chosen_c = -1;
      int chosen_delta = std::numeric_limits<int>::max();
      int ties = 0;
      for (int v : bad) {
        const int oc = colour[v];
        for (int c = 0; c < q; ++c) {
          if (c == oc) continue;
          const int delta = int(count[v][c]) - int(count[v][oc]);
          const bool aspiration = conflicts + delta < global_best;
          if (tabu[v][c] > it && !aspiration) continue;
          if (delta < chosen_delta) {
            chosen_delta = delta;
            chosen_v = v;
            chosen_c = c;
            ties = 1;
          } else if (delta == chosen_delta && random_int(++ties) == 0) {
            chosen_v = v;
            chosen_c = c;
          }
        }
      }
      if (chosen_v < 0) {
        const int v = bad[random_int(static_cast<int>(bad.size()))];
        const int oc = colour[v];
        for (int c = 0; c < q; ++c)
          if (c != oc) {
            const int delta = int(count[v][c]) - int(count[v][oc]);
            if (delta < chosen_delta) {
              chosen_delta = delta;
              chosen_v = v;
              chosen_c = c;
            }
          }
      }
      make_move(chosen_v, chosen_c, it);
      if (conflicts < local_best) {
        local_best = conflicts;
        last_improvement = it64;
        if (local_best <= 100 || local_best % 100 == 0)
          std::cerr << "residual Tabu best " << local_best << " at "
                    << it64 << '\n';
      }
      if (it64 - last_improvement > 1'000'000) {
        initialize();
        local_best = conflicts;
        last_improvement = it64;
      }
    }
    return false;
  }

  std::vector<std::vector<int>> systems() const {
    std::vector<std::vector<int>> answer = dls;
    answer.resize(17);
    for (int v = 0; v < static_cast<int>(residual.size()); ++v)
      answer[10 + colour[v]].push_back(residual[v]);
    return answer;
  }
};

struct ResidualPartial {
  static constexpr int q = 7;
  ResidualTabu graph;
  std::mt19937_64 rng;
  std::vector<int8_t> colour;
  std::vector<std::array<uint8_t, q>> count;
  std::vector<std::array<int, q>> tabu;
  std::vector<int> uncoloured;
  std::vector<int> uncoloured_pos;
  int best = std::numeric_limits<int>::max();

  ResidualPartial(const Instance& in,
                  const std::vector<std::vector<int>>& dls, uint64_t seed)
      : graph(in, dls, seed ^ 0xa0761d6478bd642fULL),
        rng(seed),
        colour(graph.residual.size(), -1),
        count(graph.residual.size()),
        tabu(graph.residual.size()),
        uncoloured_pos(graph.residual.size(), -1) {}

  int random_int(int n) {
    return static_cast<int>(rng() % static_cast<uint64_t>(n));
  }

  void set_uncoloured(int v, bool value) {
    if (value && uncoloured_pos[v] < 0) {
      uncoloured_pos[v] = static_cast<int>(uncoloured.size());
      uncoloured.push_back(v);
    } else if (!value && uncoloured_pos[v] >= 0) {
      const int p = uncoloured_pos[v];
      const int w = uncoloured.back();
      uncoloured[p] = w;
      uncoloured_pos[w] = p;
      uncoloured.pop_back();
      uncoloured_pos[v] = -1;
    }
  }

  void assign_initial(int v, int c) {
    if (colour[v] >= 0) throw std::runtime_error("initial assignment");
    if (count[v][c] != 0) throw std::runtime_error("initial conflict");
    colour[v] = c;
    for (int u : graph.adj[v]) ++count[u][c];
  }

  void initialize() {
    std::fill(colour.begin(), colour.end(), int8_t{-1});
    for (auto& row : count) row.fill(0);
    for (auto& row : tabu) row.fill(0);

    auto seeded = graph.dls;
    const auto permutations = random_disjoint_sqs10(rng);
    add_db_extensions(graph.in, seeded, permutations, 3);
    for (int c = 0; c < 3; ++c)
      for (int r : seeded[10 + c])
        assign_initial(graph.local_of[r], c);

    std::vector<int> order;
    for (int v = 0; v < static_cast<int>(graph.residual.size()); ++v)
      if (colour[v] < 0) order.push_back(v);
    std::shuffle(order.begin(), order.end(), rng);
    for (int v : order) {
      std::array<int, q> choices{};
      int nchoices = 0;
      for (int c = 0; c < q; ++c)
        if (count[v][c] == 0) choices[nchoices++] = c;
      if (nchoices) assign_initial(v, choices[random_int(nchoices)]);
    }

    uncoloured.clear();
    std::fill(uncoloured_pos.begin(), uncoloured_pos.end(), -1);
    for (int v = 0; v < static_cast<int>(graph.residual.size()); ++v)
      set_uncoloured(v, colour[v] < 0);
    best = std::min(best, static_cast<int>(uncoloured.size()));
  }

  void move(int v, int c, int iteration) {
    if (colour[v] >= 0) throw std::runtime_error("partial move source");
    std::vector<int> displaced;
    for (int u : graph.adj[v])
      if (colour[u] == c) displaced.push_back(u);
    if (displaced.size() != count[v][c])
      throw std::runtime_error("partial count");

    colour[v] = c;
    set_uncoloured(v, false);
    for (int u : graph.adj[v]) ++count[u][c];
    for (int w : displaced) {
      colour[w] = -1;
      set_uncoloured(w, true);
      for (int u : graph.adj[w]) --count[u][c];
      tabu[w][c] = iteration + 5 + random_int(10) +
                   std::min<int>(100, uncoloured.size() / 3);
    }
    best = std::min(best, static_cast<int>(uncoloured.size()));
  }

  bool run(uint64_t iterations) {
    initialize();
    int local_best = static_cast<int>(uncoloured.size());
    uint64_t last_improvement = 0;
    std::cerr << "partial colouring starts with " << uncoloured.size()
              << " uncoloured vertices\n";
    for (uint64_t it64 = 1; it64 <= iterations; ++it64) {
      if (uncoloured.empty()) return true;
      const int it = static_cast<int>(
          std::min<uint64_t>(it64, std::numeric_limits<int>::max() / 2));
      int chosen_v = -1;
      int chosen_c = -1;
      int chosen_delta = std::numeric_limits<int>::max();
      int ties = 0;
      for (int v : uncoloured)
        for (int c = 0; c < q; ++c) {
          const int delta = int(count[v][c]) - 1;
          const bool aspiration =
              int(uncoloured.size()) + delta < best;
          if (tabu[v][c] > it && !aspiration) continue;
          if (delta < chosen_delta) {
            chosen_delta = delta;
            chosen_v = v;
            chosen_c = c;
            ties = 1;
          } else if (delta == chosen_delta && random_int(++ties) == 0) {
            chosen_v = v;
            chosen_c = c;
          }
        }
      if (chosen_v < 0) {
        chosen_v = uncoloured[random_int(static_cast<int>(uncoloured.size()))];
        chosen_c = random_int(q);
      }
      move(chosen_v, chosen_c, it);
      if (static_cast<int>(uncoloured.size()) < local_best) {
        local_best = static_cast<int>(uncoloured.size());
        last_improvement = it64;
        if (local_best <= 50 || local_best % 25 == 0)
          std::cerr << "partial best " << local_best << " at " << it64
                    << '\n';
      }
      if (it64 - last_improvement > 1'000'000) {
        initialize();
        local_best = static_cast<int>(uncoloured.size());
        last_improvement = it64;
      }
    }
    return false;
  }

  std::vector<std::vector<int>> systems() const {
    std::vector<std::vector<int>> answer = graph.dls;
    answer.resize(17);
    for (int v = 0; v < static_cast<int>(graph.residual.size()); ++v) {
      if (colour[v] < 0) throw std::runtime_error("partial output");
      answer[10 + colour[v]].push_back(graph.residual[v]);
    }
    return answer;
  }
};

bool complete_last_two(const Instance& in, const std::vector<uint8_t>& unused,
                       std::vector<int>& left, std::vector<int>& right,
                       int& components) {
  std::vector<std::vector<int>> adj(NB);
  for (int c = 0; c < NT; ++c) {
    std::array<int, 2> rows{};
    int at = 0;
    for (int r : in.column_rows[c])
      if (unused[r]) {
        if (at >= 2) return false;
        rows[at++] = r;
      }
    if (at != 2) return false;
    adj[rows[0]].push_back(rows[1]);
    adj[rows[1]].push_back(rows[0]);
  }

  std::vector<int8_t> side(NB, -1);
  components = 0;
  for (int root = 0; root < NB; ++root) {
    if (!unused[root] || side[root] >= 0) continue;
    ++components;
    side[root] = 0;
    std::queue<int> queue;
    queue.push(root);
    while (!queue.empty()) {
      const int v = queue.front();
      queue.pop();
      for (int w : adj[v]) {
        if (side[w] < 0) {
          side[w] = 1 - side[v];
          queue.push(w);
        } else if (side[w] == side[v]) {
          return false;
        }
      }
    }
  }
  for (int r = 0; r < NB; ++r)
    if (unused[r]) (side[r] ? right : left).push_back(r);
  return left.size() == 285 && right.size() == 285;
}

void verify_and_write(const Instance& in,
                      const std::vector<std::vector<int>>& systems,
                      const std::string& output) {
  if (systems.size() != 17) throw std::runtime_error("system count");
  std::vector<int> colour(NB, -1);
  for (int c = 0; c < 17; ++c) {
    if (systems[c].size() != 285) throw std::runtime_error("class size");
    std::array<int, NT> cover{};
    for (int r : systems[c]) {
      if (colour[r] >= 0) throw std::runtime_error("overlap");
      colour[r] = c;
      for (int t : in.row_columns[r]) ++cover[t];
    }
    for (int x : cover)
      if (x != 1) throw std::runtime_error("class verification");
  }
  for (int c : colour)
    if (c < 0) throw std::runtime_error("uncoloured block");

  std::ofstream out(output);
  if (!out) throw std::runtime_error("certificate output");
  for (int r = 0; r < NB; ++r)
    out << in.blocks[r][0] << ' ' << in.blocks[r][1] << ' '
        << in.blocks[r][2] << ' ' << in.blocks[r][3] << ' '
        << colour[r] << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  int restarts = 100;
  double stage_seconds = 10.0;
  uint64_t node_limit = 20'000'000;
  uint64_t seed = 835;
  int db_classes = 3;
  uint64_t tabu_iterations = 0;
  uint64_t partial_iterations = 0;
  std::string output = "evidence/ls_3_4_20_dls_witness.txt";
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--restarts" && i + 1 < argc)
      restarts = std::stoi(argv[++i]);
    else if (arg == "--stage-seconds" && i + 1 < argc)
      stage_seconds = std::stod(argv[++i]);
    else if (arg == "--node-limit" && i + 1 < argc)
      node_limit = std::stoull(argv[++i]);
    else if (arg == "--seed" && i + 1 < argc)
      seed = std::stoull(argv[++i]);
    else if (arg == "--db-classes" && i + 1 < argc)
      db_classes = std::stoi(argv[++i]);
    else if (arg == "--tabu-iterations" && i + 1 < argc)
      tabu_iterations = std::stoull(argv[++i]);
    else if (arg == "--partial-iterations" && i + 1 < argc)
      partial_iterations = std::stoull(argv[++i]);
    else if (arg == "--output" && i + 1 < argc)
      output = argv[++i];
    else {
      std::cerr << "usage: " << argv[0]
                << " [--restarts N] [--stage-seconds S] [--node-limit N]"
                   " [--seed N] [--db-classes 0..3]"
                   " [--tabu-iterations N] [--partial-iterations N]"
                   " [--output PATH]\n";
      return 2;
    }
  }

  const Instance in;
  const auto dls = dls_core(in);
  std::cerr << "verified DLS core: 10 pairwise disjoint SQS(20)s\n";
  if (tabu_iterations > 0) {
    ResidualTabu search(in, dls, seed);
    if (search.run(tabu_iterations)) {
      const auto systems = search.systems();
      verify_and_write(in, systems, output);
      std::cout << "FOUND and internally verified LS(3,4,20)\n"
                << "certificate: " << output << '\n';
      return 0;
    }
    std::cout << "no witness found within residual Tabu budget; best "
              << search.global_best << " conflicting edges\n";
    return 1;
  }
  if (partial_iterations > 0) {
    ResidualPartial search(in, dls, seed);
    if (search.run(partial_iterations)) {
      const auto systems = search.systems();
      verify_and_write(in, systems, output);
      std::cout << "FOUND and internally verified LS(3,4,20)\n"
                << "certificate: " << output << '\n';
      return 0;
    }
    std::cout << "no witness found within residual partial-colouring budget; "
              << "best " << search.best << " uncoloured vertices\n";
    return 1;
  }

  for (int restart = 0; restart < restarts; ++restart) {
    std::mt19937_64 rng(seed + 0x9e3779b97f4a7c15ULL * uint64_t(restart));
    auto systems = dls;
    const auto base_permutations = random_disjoint_sqs10(rng);
    add_db_extensions(in, systems, base_permutations, db_classes);
    std::cerr << "restart " << restart
              << " verified randomized core of " << systems.size()
              << " systems\n";
    std::vector<uint8_t> unused(NB, 1);
    for (const auto& system : systems)
      for (int r : system) unused[r] = 0;

    bool failed = false;
    for (int stage = static_cast<int>(systems.size()); stage < 15; ++stage) {
      ExactCover solver(in, unused, rng, node_limit, stage_seconds);
      if (!solver.search()) {
        std::cerr << "restart " << restart << " stage " << stage + 1
                  << " failed after " << solver.nodes << " nodes\n";
        failed = true;
        break;
      }
      systems.push_back(solver.solution);
      for (int r : solver.solution) unused[r] = 0;
      std::cerr << "restart " << restart << " stage " << stage + 1
                << " found after " << solver.nodes << " nodes\n";
    }
    if (failed) continue;

    std::vector<int> left, right;
    int components = 0;
    if (!complete_last_two(in, unused, left, right, components)) {
      std::cerr << "restart " << restart
                << " residual two-cover graph is non-bipartite\n";
      continue;
    }
    systems.push_back(std::move(left));
    systems.push_back(std::move(right));
    verify_and_write(in, systems, output);
    std::cout << "FOUND and internally verified LS(3,4,20)\n"
              << "residual components: " << components << '\n'
              << "certificate: " << output << '\n';
    return 0;
  }

  std::cout << "no witness found within the randomized DLS search budget\n";
  return 1;
}
