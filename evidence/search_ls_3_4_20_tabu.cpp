// Heuristic TabuCol search for a large set LS(3,4,20).
//
// Vertices are the 4-subsets of a 20-set.  Two vertices are adjacent when
// they share a triple, so this is precisely J(20,4).  A proper 17-colouring
// partitions all quadruples into seventeen SQS(20)s.
//
// This program is only a witness finder.  A timeout is not evidence of
// nonexistence.  Any emitted witness must be checked independently with
// verify_ls_3_4_20_certificate.py.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

namespace {

constexpr int V = 20;
constexpr int K = 4;
constexpr int Q = 17;
constexpr int N = 4845;
constexpr int DEG = 64;

using Block = std::array<int, K>;

uint32_t mask_of(const Block& b) {
  uint32_t m = 0;
  for (int x : b) m |= uint32_t{1} << x;
  return m;
}

struct Instance {
  std::vector<Block> blocks;
  std::vector<std::array<int, DEG>> adj;
  std::array<int, Q> fixed_star{};

  Instance() {
    blocks.reserve(N);
    std::unordered_map<uint32_t, int> index;
    for (int a = 0; a < V; ++a)
      for (int b = a + 1; b < V; ++b)
        for (int c = b + 1; c < V; ++c)
          for (int d = c + 1; d < V; ++d) {
            Block block{a, b, c, d};
            index.emplace(mask_of(block), static_cast<int>(blocks.size()));
            blocks.push_back(block);
          }
    if (static_cast<int>(blocks.size()) != N) throw std::runtime_error("N");

    std::vector<std::vector<int>> tmp(N);
    for (int a = 0; a < V; ++a)
      for (int b = a + 1; b < V; ++b)
        for (int c = b + 1; c < V; ++c) {
          std::array<int, Q> star{};
          int at = 0;
          const uint32_t tri =
              (uint32_t{1} << a) | (uint32_t{1} << b) | (uint32_t{1} << c);
          for (int x = 0; x < V; ++x) {
            if (tri & (uint32_t{1} << x)) continue;
            star[at++] = index.at(tri | (uint32_t{1} << x));
          }
          if (at != Q) throw std::runtime_error("star");
          for (int i = 0; i < Q; ++i)
            for (int j = i + 1; j < Q; ++j) {
              tmp[star[i]].push_back(star[j]);
              tmp[star[j]].push_back(star[i]);
            }
        }

    adj.resize(N);
    for (int i = 0; i < N; ++i) {
      std::sort(tmp[i].begin(), tmp[i].end());
      tmp[i].erase(std::unique(tmp[i].begin(), tmp[i].end()), tmp[i].end());
      if (static_cast<int>(tmp[i].size()) != DEG)
        throw std::runtime_error("degree");
      std::copy(tmp[i].begin(), tmp[i].end(), adj[i].begin());
    }

    for (int x = 3; x < V; ++x) {
      const uint32_t m =
          (uint32_t{1} << 0) | (uint32_t{1} << 1) |
          (uint32_t{1} << 2) | (uint32_t{1} << x);
      fixed_star[x - 3] = index.at(m);
    }
  }
};

struct Search {
  const Instance& in;
  std::mt19937_64 rng;
  std::vector<uint8_t> initial_colour;
  std::vector<uint8_t> colour;
  std::vector<std::array<uint8_t, Q>> count;
  std::vector<std::array<int, Q>> tabu;
  std::vector<uint8_t> fixed;
  std::vector<int> bad;
  std::vector<int> bad_pos;
  int conflicts = 0;
  int best = std::numeric_limits<int>::max();
  std::vector<uint8_t> best_colour;

  Search(const Instance& instance, uint64_t seed,
         const std::vector<uint8_t>& initial)
      : in(instance),
        rng(seed),
        initial_colour(initial),
        colour(N),
        count(N),
        tabu(N),
        fixed(N, 0),
        bad_pos(N, -1) {
    // With a supplied near-solution we leave every vertex movable.  The
    // reference star is only a colour-symmetry break for random starts.
    if (initial_colour.empty())
      for (int c = 0; c < Q; ++c) fixed[in.fixed_star[c]] = 1;
  }

  int random_int(int n) {
    return static_cast<int>(rng() % static_cast<uint64_t>(n));
  }

  void set_bad(int v, bool is_bad) {
    if (is_bad && bad_pos[v] < 0) {
      bad_pos[v] = static_cast<int>(bad.size());
      bad.push_back(v);
    } else if (!is_bad && bad_pos[v] >= 0) {
      const int p = bad_pos[v];
      const int w = bad.back();
      bad[p] = w;
      bad_pos[w] = p;
      bad.pop_back();
      bad_pos[v] = -1;
    }
  }

  void initialize() {
    if (!initial_colour.empty()) {
      colour = initial_colour;
    } else {
      std::fill(colour.begin(), colour.end(), uint8_t{255});
      for (int c = 0; c < Q; ++c) colour[in.fixed_star[c]] = c;

      // A randomized greedy start is substantially closer than an iid start.
      std::vector<int> order;
      order.reserve(N - Q);
      for (int v = 0; v < N; ++v)
        if (!fixed[v]) order.push_back(v);
      std::shuffle(order.begin(), order.end(), rng);
      for (int v : order) {
        std::array<int, Q> used{};
        for (int u : in.adj[v])
          if (colour[u] < Q) ++used[colour[u]];
        int score = *std::min_element(used.begin(), used.end());
        std::array<int, Q> choices{};
        int nchoices = 0;
        for (int c = 0; c < Q; ++c)
          if (used[c] == score) choices[nchoices++] = c;
        colour[v] = choices[random_int(nchoices)];
      }
    }

    for (auto& row : count) row.fill(0);
    for (auto& row : tabu) row.fill(0);
    conflicts = 0;
    for (int v = 0; v < N; ++v)
      for (int u : in.adj[v]) ++count[v][colour[u]];
    for (int v = 0; v < N; ++v) conflicts += count[v][colour[v]];
    conflicts /= 2;

    bad.clear();
    std::fill(bad_pos.begin(), bad_pos.end(), -1);
    for (int v = 0; v < N; ++v)
      if (!fixed[v]) set_bad(v, count[v][colour[v]] != 0);
    if (conflicts < best) {
      best = conflicts;
      best_colour = colour;
    }
  }

  void move(int v, int nc, int iteration) {
    const int oc = colour[v];
    const int delta = int(count[v][nc]) - int(count[v][oc]);
    for (int u : in.adj[v]) {
      --count[u][oc];
      ++count[u][nc];
    }
    colour[v] = nc;
    conflicts += delta;

    // Forbid undoing the move.  The tenure is reactive: long in the rough
    // phase, short near a putative colouring.
    const int tenure =
        7 + random_int(10) + std::min(250, static_cast<int>(bad.size()) / 6);
    tabu[v][oc] = iteration + tenure;

    set_bad(v, count[v][colour[v]] != 0);
    for (int u : in.adj[v])
      if (!fixed[u]) set_bad(u, count[u][colour[u]] != 0);

    if (conflicts < best) {
      best = conflicts;
      best_colour = colour;
    }
  }

  bool verify() const {
    if (conflicts != 0) return false;
    for (int v = 0; v < N; ++v)
      for (int u : in.adj[v])
        if (colour[v] == colour[u]) return false;
    return true;
  }

  bool run(uint64_t max_iterations, std::atomic<bool>& stop, int worker) {
    initialize();
    uint64_t last_improvement = 0;
    int local_best = conflicts;
    for (uint64_t it64 = 1; it64 <= max_iterations && !stop.load(); ++it64) {
      const int it = static_cast<int>(
          std::min<uint64_t>(it64, std::numeric_limits<int>::max() / 2));
      if (conflicts == 0) {
        if (!verify()) throw std::runtime_error("internal verification");
        stop.store(true);
        return true;
      }
      if (bad.empty()) throw std::runtime_error("bad list");

      int chosen_v = -1;
      int chosen_c = -1;
      int chosen_delta = std::numeric_limits<int>::max();
      int ties = 0;
      const int samples = std::min<int>(320, bad.size());
      for (int s = 0; s < samples; ++s) {
        const int v = bad[random_int(static_cast<int>(bad.size()))];
        const int oc = colour[v];
        for (int c = 0; c < Q; ++c) {
          if (c == oc) continue;
          const int delta = int(count[v][c]) - int(count[v][oc]);
          const bool aspiration = conflicts + delta < best;
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

      // A fully tabu sample is rare; choose the least damaging legal move
      // without the tabu filter so the walk cannot stall.
      if (chosen_v < 0) {
        const int v = bad[random_int(static_cast<int>(bad.size()))];
        const int oc = colour[v];
        for (int c = 0; c < Q; ++c) {
          if (c == oc) continue;
          const int delta = int(count[v][c]) - int(count[v][oc]);
          if (delta < chosen_delta) {
            chosen_delta = delta;
            chosen_v = v;
            chosen_c = c;
          }
        }
      }
      move(chosen_v, chosen_c, it);

      if (conflicts < local_best) {
        local_best = conflicts;
        last_improvement = it64;
        if (worker == 0 && (local_best <= 100 || local_best % 100 == 0))
          std::cerr << "worker " << worker << " best conflicts "
                    << local_best << " at iteration " << it64 << '\n';
      }

      // Long plateaus are better escaped by a fresh greedy construction.
      if (it64 - last_improvement > 2'000'000) {
        initialize();
        local_best = conflicts;
        last_improvement = it64;
      }
    }
    return false;
  }
};

struct PartialSearch {
  const Instance& in;
  std::mt19937_64 rng;
  std::vector<int8_t> initial_colour;
  std::vector<int8_t> colour;
  std::vector<std::array<uint8_t, Q>> count;
  std::vector<std::array<int, Q>> tabu;
  std::vector<int> uncoloured;
  std::vector<int> uncoloured_pos;
  int best = std::numeric_limits<int>::max();
  std::vector<int8_t> best_colour;
  int initialization_count = 0;

  PartialSearch(const Instance& instance, uint64_t seed,
                const std::vector<int8_t>& initial)
      : in(instance),
        rng(seed),
        initial_colour(initial),
        colour(N, -1),
        count(N),
        tabu(N),
        uncoloured_pos(N, -1) {
    if (static_cast<int>(initial_colour.size()) != N)
      throw std::runtime_error("partial initial size");
  }

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

  void initialize() {
    colour = initial_colour;
    if (initialization_count++ > 0) {
      // The 72-hole Etzion--Hartman start is exceptionally rigid.  On
      // restarts, destroy several entire colour classes before randomized
      // greedy repair, producing genuinely different proper partial
      // colourings instead of replaying the same basin.
      std::array<uint8_t, Q> destroyed{};
      const int destroy_count = 3 + random_int(6);
      for (int chosen = 0; chosen < destroy_count;) {
        const int c = random_int(Q);
        if (!destroyed[c]) {
          destroyed[c] = 1;
          ++chosen;
        }
      }
      for (int v = 0; v < N; ++v)
        if (colour[v] >= 0 && destroyed[colour[v]]) colour[v] = -1;
    }
    for (auto& row : count) row.fill(0);
    for (auto& row : tabu) row.fill(0);
    for (int v = 0; v < N; ++v) {
      const int c = colour[v];
      if (c < 0) continue;
      if (c >= Q) throw std::runtime_error("partial initial colour");
      for (int u : in.adj[v]) ++count[u][c];
    }
    for (int v = 0; v < N; ++v)
      if (colour[v] >= 0 && count[v][colour[v]] != 0)
        throw std::runtime_error("partial initial is not proper");

    if (initialization_count > 1) {
      std::vector<int> order;
      for (int v = 0; v < N; ++v)
        if (colour[v] < 0) order.push_back(v);
      std::shuffle(order.begin(), order.end(), rng);
      for (int v : order) {
        std::array<int, Q> choices{};
        int nchoices = 0;
        for (int c = 0; c < Q; ++c)
          if (count[v][c] == 0) choices[nchoices++] = c;
        if (!nchoices) continue;
        const int c = choices[random_int(nchoices)];
        colour[v] = static_cast<int8_t>(c);
        for (int u : in.adj[v]) ++count[u][c];
      }
    }

    uncoloured.clear();
    std::fill(uncoloured_pos.begin(), uncoloured_pos.end(), -1);
    for (int v = 0; v < N; ++v)
      set_uncoloured(v, colour[v] < 0);
    if (static_cast<int>(uncoloured.size()) < best) {
      best = static_cast<int>(uncoloured.size());
      best_colour = colour;
    }
  }

  void move(int v, int c, int iteration) {
    if (colour[v] >= 0) throw std::runtime_error("partial move source");
    std::vector<int> displaced;
    for (int u : in.adj[v])
      if (colour[u] == c) displaced.push_back(u);
    if (displaced.size() != count[v][c])
      throw std::runtime_error("partial count");

    colour[v] = static_cast<int8_t>(c);
    set_uncoloured(v, false);
    for (int u : in.adj[v]) ++count[u][c];
    for (int w : displaced) {
      colour[w] = -1;
      set_uncoloured(w, true);
      for (int u : in.adj[w]) --count[u][c];
      tabu[w][c] =
          iteration + 5 + random_int(10) +
          std::min<int>(250, static_cast<int>(uncoloured.size()) / 2);
    }
    if (static_cast<int>(uncoloured.size()) < best) {
      best = static_cast<int>(uncoloured.size());
      best_colour = colour;
    }
  }

  bool verify() const {
    if (!uncoloured.empty()) return false;
    for (int v = 0; v < N; ++v)
      for (int u : in.adj[v])
        if (colour[v] == colour[u]) return false;
    return true;
  }

  bool run(uint64_t max_iterations, std::atomic<bool>& stop, int worker) {
    initialize();
    int local_best = static_cast<int>(uncoloured.size());
    uint64_t last_improvement = 0;
    if (worker == 0)
      std::cerr << "partial start " << local_best
                << " uncoloured vertices\n";
    for (uint64_t it64 = 1; it64 <= max_iterations && !stop.load(); ++it64) {
      if (uncoloured.empty()) {
        if (!verify()) throw std::runtime_error("partial verification");
        stop.store(true);
        return true;
      }
      const int it = static_cast<int>(
          std::min<uint64_t>(it64, std::numeric_limits<int>::max() / 2));
      int chosen_v = -1;
      int chosen_c = -1;
      int chosen_delta = std::numeric_limits<int>::max();
      int ties = 0;
      for (int v : uncoloured)
        for (int c = 0; c < Q; ++c) {
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
        chosen_v =
            uncoloured[random_int(static_cast<int>(uncoloured.size()))];
        chosen_c = random_int(Q);
      }
      move(chosen_v, chosen_c, it);

      if (static_cast<int>(uncoloured.size()) < local_best) {
        local_best = static_cast<int>(uncoloured.size());
        last_improvement = it64;
        if (worker == 0)
          std::cerr << "partial best " << local_best << " at " << it64
                    << '\n';
      }
      if (it64 - last_improvement > 500'000) {
        initialize();
        local_best = static_cast<int>(uncoloured.size());
        last_improvement = it64;
      }
    }
    return false;
  }

  std::vector<uint8_t> answer() const {
    std::vector<uint8_t> result;
    if (!uncoloured.empty()) return result;
    result.reserve(N);
    for (int8_t c : colour) {
      if (c < 0) throw std::runtime_error("partial answer");
      result.push_back(static_cast<uint8_t>(c));
    }
    return result;
  }
};

struct EquitableSearch {
  const Instance& in;
  std::mt19937_64 rng;
  std::vector<uint8_t> initial_colour;
  std::vector<uint8_t> colour;
  std::vector<std::array<uint8_t, Q>> count;
  std::vector<std::array<int, Q>> tabu;
  std::array<std::vector<int>, Q> classes;
  std::vector<int> class_pos;
  std::vector<int> bad;
  std::vector<int> bad_pos;
  int conflicts = 0;
  int best = std::numeric_limits<int>::max();
  std::vector<uint8_t> best_colour;

  EquitableSearch(const Instance& instance, uint64_t seed,
                  const std::vector<uint8_t>& initial)
      : in(instance),
        rng(seed),
        initial_colour(initial),
        colour(N),
        count(N),
        tabu(N),
        class_pos(N, -1),
        bad_pos(N, -1) {
    if (static_cast<int>(initial_colour.size()) != N)
      throw std::runtime_error("equitable initial size");
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

  bool adjacent(int v, int w) const {
    return std::find(in.adj[v].begin(), in.adj[v].end(), w) !=
           in.adj[v].end();
  }

  void initialize() {
    colour = initial_colour;
    for (auto& row : count) row.fill(0);
    for (auto& row : tabu) row.fill(0);
    for (auto& group : classes) group.clear();
    for (int v = 0; v < N; ++v) {
      if (colour[v] >= Q) throw std::runtime_error("equitable colour");
      class_pos[v] = static_cast<int>(classes[colour[v]].size());
      classes[colour[v]].push_back(v);
    }
    for (const auto& group : classes)
      if (static_cast<int>(group.size()) != 285)
        throw std::runtime_error("equitable class size");

    conflicts = 0;
    for (int v = 0; v < N; ++v)
      for (int u : in.adj[v]) ++count[v][colour[u]];
    for (int v = 0; v < N; ++v) conflicts += count[v][colour[v]];
    conflicts /= 2;

    bad.clear();
    std::fill(bad_pos.begin(), bad_pos.end(), -1);
    for (int v = 0; v < N; ++v)
      set_bad(v, count[v][colour[v]] != 0);
    if (conflicts < best) {
      best = conflicts;
      best_colour = colour;
    }
  }

  int swap_delta(int v, int w) const {
    const int a = colour[v];
    const int b = colour[w];
    if (a == b) return std::numeric_limits<int>::max() / 4;
    return int(count[v][b]) - int(count[v][a]) +
           int(count[w][a]) - int(count[w][b]) -
           (adjacent(v, w) ? 2 : 0);
  }

  void swap_vertices(int v, int w, int iteration) {
    const int a = colour[v];
    const int b = colour[w];
    const int delta = swap_delta(v, w);

    for (int u : in.adj[v]) {
      --count[u][a];
      ++count[u][b];
    }
    for (int u : in.adj[w]) {
      --count[u][b];
      ++count[u][a];
    }
    colour[v] = static_cast<uint8_t>(b);
    colour[w] = static_cast<uint8_t>(a);
    conflicts += delta;

    const int pv = class_pos[v];
    const int pw = class_pos[w];
    classes[a][pv] = w;
    classes[b][pw] = v;
    class_pos[w] = pv;
    class_pos[v] = pw;

    const int tenure =
        7 + random_int(10) + std::min(250, int(bad.size()) / 5);
    tabu[v][a] = iteration + tenure;
    tabu[w][b] = iteration + tenure;

    set_bad(v, count[v][colour[v]] != 0);
    set_bad(w, count[w][colour[w]] != 0);
    for (int u : in.adj[v]) set_bad(u, count[u][colour[u]] != 0);
    for (int u : in.adj[w]) set_bad(u, count[u][colour[u]] != 0);
    if (conflicts < best) {
      best = conflicts;
      best_colour = colour;
    }
  }

  bool verify() const {
    if (conflicts != 0) return false;
    for (int v = 0; v < N; ++v)
      for (int u : in.adj[v])
        if (colour[v] == colour[u]) return false;
    return true;
  }

  bool run(uint64_t max_iterations, std::atomic<bool>& stop, int worker) {
    initialize();
    int local_best = conflicts;
    uint64_t last_improvement = 0;
    if (worker == 0)
      std::cerr << "equitable-swap start " << conflicts << " conflicts\n";
    for (uint64_t it64 = 1; it64 <= max_iterations && !stop.load(); ++it64) {
      if (conflicts == 0) {
        if (!verify()) throw std::runtime_error("equitable verification");
        stop.store(true);
        return true;
      }
      if (bad.empty()) throw std::runtime_error("equitable bad list");
      const int it = static_cast<int>(
          std::min<uint64_t>(it64, std::numeric_limits<int>::max() / 2));
      int chosen_v = -1;
      int chosen_w = -1;
      int chosen_delta = std::numeric_limits<int>::max();
      int ties = 0;
      const int samples = 1500;
      for (int sample = 0; sample < samples; ++sample) {
        const int v = bad[random_int(static_cast<int>(bad.size()))];
        const int a = colour[v];
        int b = random_int(Q - 1);
        if (b >= a) ++b;
        const int w = classes[b][random_int(285)];
        const int delta = swap_delta(v, w);
        const bool aspiration = conflicts + delta < best;
        if ((tabu[v][b] > it || tabu[w][a] > it) && !aspiration) continue;
        if (delta < chosen_delta) {
          chosen_delta = delta;
          chosen_v = v;
          chosen_w = w;
          ties = 1;
        } else if (delta == chosen_delta && random_int(++ties) == 0) {
          chosen_v = v;
          chosen_w = w;
        }
      }
      if (chosen_v < 0) {
        chosen_v = bad[random_int(static_cast<int>(bad.size()))];
        const int a = colour[chosen_v];
        int b = random_int(Q - 1);
        if (b >= a) ++b;
        chosen_w = classes[b][random_int(285)];
      }
      swap_vertices(chosen_v, chosen_w, it);

      if (conflicts < local_best) {
        local_best = conflicts;
        last_improvement = it64;
        if (worker == 0)
          std::cerr << "equitable best " << local_best << " at " << it64
                    << '\n';
      }
      if (it64 - last_improvement > 2'000'000) {
        initialize();
        local_best = conflicts;
        last_improvement = it64;
      }
    }
    return false;
  }
};

void write_certificate(const Instance& in, const std::vector<uint8_t>& colour,
                       const std::string& path) {
  std::ofstream out(path);
  if (!out) throw std::runtime_error("cannot open certificate");
  for (int i = 0; i < N; ++i)
    out << in.blocks[i][0] << ' ' << in.blocks[i][1] << ' '
        << in.blocks[i][2] << ' ' << in.blocks[i][3] << ' '
        << int(colour[i]) << '\n';
}

std::vector<uint8_t> read_initial_certificate(const Instance& in,
                                              const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open initial certificate");
  std::vector<uint8_t> result;
  result.reserve(N);
  for (int row = 0; row < N; ++row) {
    int a, b, c, d, colour;
    if (!(input >> a >> b >> c >> d >> colour))
      throw std::runtime_error("short initial certificate");
    if (Block{a, b, c, d} != in.blocks[row])
      throw std::runtime_error("initial certificate block order");
    if (colour < 0 || colour >= Q)
      throw std::runtime_error("initial certificate colour");
    result.push_back(static_cast<uint8_t>(colour));
  }
  int extra;
  if (input >> extra)
    throw std::runtime_error("long initial certificate");
  return result;
}

std::vector<int8_t> read_partial_certificate(const Instance& in,
                                             const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open partial certificate");
  std::vector<int8_t> result;
  result.reserve(N);
  for (int row = 0; row < N; ++row) {
    int a, b, c, d, colour;
    if (!(input >> a >> b >> c >> d >> colour))
      throw std::runtime_error("short partial certificate");
    if (Block{a, b, c, d} != in.blocks[row])
      throw std::runtime_error("partial certificate block order");
    if (colour < -1 || colour >= Q)
      throw std::runtime_error("partial certificate colour");
    result.push_back(static_cast<int8_t>(colour));
  }
  int extra;
  if (input >> extra)
    throw std::runtime_error("long partial certificate");
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  uint64_t iterations = 50'000'000;
  int workers = 1;
  uint64_t seed = 835;
  std::string output = "evidence/ls_3_4_20_witness.txt";
  std::string initial_path;
  std::string partial_initial_path;
  std::string equitable_initial_path;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--iterations" && i + 1 < argc)
      iterations = std::stoull(argv[++i]);
    else if (arg == "--workers" && i + 1 < argc)
      workers = std::stoi(argv[++i]);
    else if (arg == "--seed" && i + 1 < argc)
      seed = std::stoull(argv[++i]);
    else if (arg == "--output" && i + 1 < argc)
      output = argv[++i];
    else if (arg == "--initial" && i + 1 < argc)
      initial_path = argv[++i];
    else if (arg == "--partial-initial" && i + 1 < argc)
      partial_initial_path = argv[++i];
    else if (arg == "--equitable-initial" && i + 1 < argc)
      equitable_initial_path = argv[++i];
    else {
      std::cerr << "usage: " << argv[0]
                << " [--iterations N] [--workers N] [--seed N]"
                   " [--initial PATH] [--partial-initial PATH]"
                   " [--equitable-initial PATH]"
                   " [--output PATH]\n";
      return 2;
    }
  }

  const Instance instance;
  if ((!initial_path.empty()) + (!partial_initial_path.empty()) +
          (!equitable_initial_path.empty()) >
      1)
    throw std::runtime_error("choose one initial mode");

  if (!equitable_initial_path.empty()) {
    const auto equitable =
        read_initial_certificate(instance, equitable_initial_path);
    std::atomic<bool> equitable_stop{false};
    std::vector<std::thread> equitable_threads;
    std::vector<std::vector<uint8_t>> equitable_answers(workers);
    const auto equitable_started = std::chrono::steady_clock::now();
    for (int w = 0; w < workers; ++w) {
      equitable_threads.emplace_back([&, w] {
        EquitableSearch search(
            instance,
            seed + 0x9e3779b97f4a7c15ULL * uint64_t(w),
            equitable);
        if (search.run(iterations, equitable_stop, w))
          equitable_answers[w] = search.colour;
        std::cerr << "equitable worker " << w << " global best "
                  << search.best << '\n';
      });
    }
    for (auto& thread : equitable_threads) thread.join();
    const auto elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - equitable_started).count();
    for (const auto& answer : equitable_answers) {
      if (!answer.empty()) {
        write_certificate(instance, answer, output);
        std::cout << "FOUND and internally verified LS(3,4,20)\n"
                  << "certificate: " << output << '\n'
                  << "elapsed seconds: " << elapsed << '\n';
        return 0;
      }
    }
    std::cout << "no witness found within equitable-swap budget\n"
              << "elapsed seconds: " << elapsed << '\n';
    return 1;
  }

  if (!partial_initial_path.empty()) {
    const auto partial =
        read_partial_certificate(instance, partial_initial_path);
    std::atomic<bool> partial_stop{false};
    std::vector<std::thread> partial_threads;
    std::vector<std::vector<uint8_t>> partial_answers(workers);
    const auto partial_started = std::chrono::steady_clock::now();
    for (int w = 0; w < workers; ++w) {
      partial_threads.emplace_back([&, w] {
        PartialSearch search(
            instance,
            seed + 0x9e3779b97f4a7c15ULL * uint64_t(w),
            partial);
        if (search.run(iterations, partial_stop, w))
          partial_answers[w] = search.answer();
        std::cerr << "partial worker " << w << " global best "
                  << search.best << '\n';
      });
    }
    for (auto& thread : partial_threads) thread.join();
    const auto elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - partial_started).count();
    for (const auto& answer : partial_answers) {
      if (!answer.empty()) {
        write_certificate(instance, answer, output);
        std::cout << "FOUND and internally verified LS(3,4,20)\n"
                  << "certificate: " << output << '\n'
                  << "elapsed seconds: " << elapsed << '\n';
        return 0;
      }
    }
    std::cout << "no witness found within partial-colouring budget\n"
              << "elapsed seconds: " << elapsed << '\n';
    return 1;
  }

  const std::vector<uint8_t> initial =
      initial_path.empty()
          ? std::vector<uint8_t>{}
          : read_initial_certificate(instance, initial_path);
  std::atomic<bool> stop{false};
  std::vector<std::thread> threads;
  std::vector<std::vector<uint8_t>> answers(workers);
  const auto started = std::chrono::steady_clock::now();
  for (int w = 0; w < workers; ++w) {
    threads.emplace_back([&, w] {
      Search search(instance,
                    seed + 0x9e3779b97f4a7c15ULL * uint64_t(w),
                    initial);
      if (search.run(iterations, stop, w)) answers[w] = search.colour;
      std::cerr << "worker " << w << " final/global best " << search.best
                << '\n';
    });
  }
  for (auto& thread : threads) thread.join();
  const auto elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - started).count();

  for (const auto& answer : answers) {
    if (!answer.empty()) {
      write_certificate(instance, answer, output);
      std::cout << "FOUND and internally verified LS(3,4,20)\n"
                << "certificate: " << output << '\n'
                << "elapsed seconds: " << elapsed << '\n';
      return 0;
    }
  }
  std::cout << "no witness found within heuristic budget\n"
            << "elapsed seconds: " << elapsed << '\n';
  return 1;
}
