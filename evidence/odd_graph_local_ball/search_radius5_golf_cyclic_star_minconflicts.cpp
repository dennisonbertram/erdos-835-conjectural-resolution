// Min-conflicts search for one exact fixed-Wallis C17 radius-five star.
//
// There are 14*40 cells.  Choosing one allowed phase in a cell covers three
// residual-edge columns and one centre/orbit/phase column.  Since every
// choice covers four columns, an assignment is an exact star precisely when
// all 2,240 non-cell columns have multiplicity one.
//
// This program is only a witness finder.  Failure under a time limit proves
// nothing.  A zero-cost output is still only one star in the fixed-Wallis
// cyclic ansatz, and must be independently checked.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int P = 17;
constexpr int FIXED = 15;
constexpr int PAIRS = 14;
constexpr int ORBITS = 40;
constexpr int VARIABLES = PAIRS * ORBITS;
constexpr int EDGE_COLUMNS = PAIRS * 120;
constexpr int CROSS_COLUMNS = ORBITS * 14;
constexpr int COLUMNS = EDGE_COLUMNS + CROSS_COLUMNS;

using Triple = std::array<int, 3>;
using Edge = std::pair<int, int>;

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
    Triple representative = seed;
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

struct Candidate {
  int variable;
  int pair_index;
  int orbit;
  int shift;
  std::array<int, 4> columns;
};

struct Instance {
  int centre = 0;
  std::vector<int> outers;
  std::vector<Candidate> candidates;
  std::array<std::vector<int>, VARIABLES> choices;
  std::array<std::array<int, P>, VARIABLES> candidate_for_shift{};
  std::array<std::vector<int>, COLUMNS> column_candidates;
};

Instance build_instance(int centre) {
  Instance instance;
  for (auto &row : instance.candidate_for_shift) row.fill(-1);
  instance.centre = centre;
  for (int fixed = 0; fixed < FIXED; ++fixed) {
    if (fixed != centre) instance.outers.push_back(fixed);
  }
  if (instance.outers.size() != PAIRS) std::abort();

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
            EDGE_COLUMNS + orbit * 14 + rank++;
      }
    }
    if (rank != 14) std::abort();
  }

  for (int pair_index = 0; pair_index < PAIRS; ++pair_index) {
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
          pair_index * 120 + index;
    }

    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      int variable = pair_index * ORBITS + orbit;
      for (int shift = 0; shift < P; ++shift) {
        Triple triple = translated(reps[orbit], shift);
        std::array<int, 4> columns{};
        int slot = 0;
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
        columns[3] = cross;
        int candidate = static_cast<int>(instance.candidates.size());
        instance.candidates.push_back(
            {variable, pair_index, orbit, shift, columns});
        instance.choices[variable].push_back(candidate);
        instance.candidate_for_shift[variable][shift] = candidate;
        for (int column : columns) {
          instance.column_candidates[column].push_back(candidate);
        }
      }
      if (instance.choices[variable].size() < 11 ||
          instance.choices[variable].size() > 14) {
        std::abort();
      }
    }
  }
  if (instance.candidates.size() != 6384) std::abort();
  for (const auto &rows : instance.column_candidates) {
    if (rows.empty()) std::abort();
  }
  return instance;
}

std::vector<int> parse_integer_array(
    const std::string &text, std::size_t start, int expected) {
  std::vector<int> values;
  std::size_t cursor = text.find('[', start);
  if (cursor == std::string::npos) return values;
  ++cursor;
  while (cursor < text.size() && values.size() < expected) {
    while (cursor < text.size() &&
           !(text[cursor] == '-' ||
             (text[cursor] >= '0' && text[cursor] <= '9'))) {
      if (text[cursor] == ']') return values;
      ++cursor;
    }
    if (cursor >= text.size()) break;
    char *end = nullptr;
    long value = std::strtol(text.c_str() + cursor, &end, 10);
    if (end == text.c_str() + cursor) break;
    values.push_back(static_cast<int>(value));
    cursor = static_cast<std::size_t>(end - text.c_str());
  }
  return values;
}

bool load_hint(
    const std::string &path,
    const Instance &instance,
    std::array<int, VARIABLES> &selected) {
  std::ifstream input(path);
  if (!input) return false;
  std::ostringstream buffer;
  buffer << input.rdbuf();
  const std::string text = buffer.str();
  for (int pair_index = 0; pair_index < PAIRS; ++pair_index) {
    int outer = instance.outers[pair_index];
    int left = std::min(instance.centre, outer);
    int right = std::max(instance.centre, outer);
    std::string key =
        "\"" + std::to_string(left) + "," + std::to_string(right) + "\"";
    std::size_t found = text.find(key);
    if (found == std::string::npos) return false;
    auto phases = parse_integer_array(text, found + key.size(), ORBITS);
    if (phases.size() != ORBITS) return false;
    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      int variable = pair_index * ORBITS + orbit;
      int shift = mod17(-phases[orbit]);
      int chosen = -1;
      for (int candidate : instance.choices[variable]) {
        if (instance.candidates[candidate].shift == shift) {
          chosen = candidate;
          break;
        }
      }
      if (chosen < 0) return false;
      selected[variable] = chosen;
    }
  }
  return true;
}

struct SearchState {
  std::array<int, VARIABLES> selected{};
  std::array<int, COLUMNS> count{};
  std::array<int, COLUMNS> weight{};
  std::array<std::int64_t, VARIABLES> tabu_until{};
  int raw_cost = 0;
  std::int64_t weighted_cost = 0;
};

int raw_term(int count) { return std::abs(count - 1); }

void rebuild(const Instance &instance, SearchState &state) {
  state.count.fill(0);
  for (int variable = 0; variable < VARIABLES; ++variable) {
    for (int column :
         instance.candidates[state.selected[variable]].columns) {
      ++state.count[column];
    }
  }
  state.raw_cost = 0;
  state.weighted_cost = 0;
  for (int column = 0; column < COLUMNS; ++column) {
    state.raw_cost += raw_term(state.count[column]);
    state.weighted_cost +=
        static_cast<std::int64_t>(state.weight[column]) *
        raw_term(state.count[column]);
  }
}

struct Delta {
  int raw = 0;
  std::int64_t weighted = 0;
};

Delta move_delta(
    const Instance &instance,
    const SearchState &state,
    int variable,
    int replacement) {
  std::array<int, 8> touched{};
  std::array<int, 8> changes{};
  int used = 0;
  auto add_change = [&](int column, int change) {
    for (int index = 0; index < used; ++index) {
      if (touched[index] == column) {
        changes[index] += change;
        return;
      }
    }
    touched[used] = column;
    changes[used] = change;
    ++used;
  };
  for (int column :
       instance.candidates[state.selected[variable]].columns) {
    add_change(column, -1);
  }
  for (int column : instance.candidates[replacement].columns) {
    add_change(column, 1);
  }
  Delta delta;
  for (int index = 0; index < used; ++index) {
    int column = touched[index];
    int before = raw_term(state.count[column]);
    int after = raw_term(state.count[column] + changes[index]);
    delta.raw += after - before;
    delta.weighted +=
        static_cast<std::int64_t>(state.weight[column]) * (after - before);
  }
  return delta;
}

void apply_move(
    const Instance &instance,
    SearchState &state,
    int variable,
    int replacement,
    Delta delta) {
  for (int column :
       instance.candidates[state.selected[variable]].columns) {
    --state.count[column];
  }
  state.selected[variable] = replacement;
  for (int column : instance.candidates[replacement].columns) {
    ++state.count[column];
  }
  state.raw_cost += delta.raw;
  state.weighted_cost += delta.weighted;
}

struct PairDelta {
  int raw = 0;
  std::int64_t weighted = 0;
};

PairDelta pair_move_delta(
    const Instance &instance,
    const SearchState &state,
    int first_variable,
    int first_replacement,
    int second_variable,
    int second_replacement) {
  std::array<int, 16> touched{};
  std::array<int, 16> changes{};
  int used = 0;
  auto add_change = [&](int column, int change) {
    for (int index = 0; index < used; ++index) {
      if (touched[index] == column) {
        changes[index] += change;
        return;
      }
    }
    touched[used] = column;
    changes[used] = change;
    ++used;
  };
  for (int column :
       instance.candidates[state.selected[first_variable]].columns) {
    add_change(column, -1);
  }
  for (int column : instance.candidates[first_replacement].columns) {
    add_change(column, 1);
  }
  for (int column :
       instance.candidates[state.selected[second_variable]].columns) {
    add_change(column, -1);
  }
  for (int column : instance.candidates[second_replacement].columns) {
    add_change(column, 1);
  }
  PairDelta delta;
  for (int index = 0; index < used; ++index) {
    int column = touched[index];
    int before = raw_term(state.count[column]);
    int after = raw_term(state.count[column] + changes[index]);
    delta.raw += after - before;
    delta.weighted +=
        static_cast<std::int64_t>(state.weight[column]) * (after - before);
  }
  return delta;
}

void apply_pair_move(
    const Instance &instance,
    SearchState &state,
    int first_variable,
    int first_replacement,
    int second_variable,
    int second_replacement,
    PairDelta delta) {
  for (int column :
       instance.candidates[state.selected[first_variable]].columns) {
    --state.count[column];
  }
  for (int column :
       instance.candidates[state.selected[second_variable]].columns) {
    --state.count[column];
  }
  state.selected[first_variable] = first_replacement;
  state.selected[second_variable] = second_replacement;
  for (int column : instance.candidates[first_replacement].columns) {
    ++state.count[column];
  }
  for (int column : instance.candidates[second_replacement].columns) {
    ++state.count[column];
  }
  state.raw_cost += delta.raw;
  state.weighted_cost += delta.weighted;
}

void write_best(
    const std::string &path,
    const Instance &instance,
    const std::array<int, VARIABLES> &selected,
    int raw_cost,
    std::uint64_t seed,
    std::int64_t steps) {
  std::ofstream output(path);
  if (!output) {
    std::cerr << "cannot write " << path << "\n";
    std::exit(2);
  }
  output << "{\n"
         << "  \"centre\": " << instance.centre << ",\n"
         << "  \"raw_l1\": " << raw_cost << ",\n"
         << "  \"seed\": " << seed << ",\n"
         << "  \"steps\": " << steps << ",\n"
         << "  \"rows\": {\n";
  for (int pair_index = 0; pair_index < PAIRS; ++pair_index) {
    int outer = instance.outers[pair_index];
    int left = std::min(instance.centre, outer);
    int right = std::max(instance.centre, outer);
    output << "    \"" << left << "," << right << "\": [";
    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      if (orbit) output << ", ";
      int variable = pair_index * ORBITS + orbit;
      int shift = instance.candidates[selected[variable]].shift;
      output << mod17(-shift);
    }
    output << "]";
    output << (pair_index + 1 == PAIRS ? "\n" : ",\n");
  }
  output << "  }\n}\n";
}

struct Options {
  int centre = 0;
  double seconds = 600.0;
  std::uint64_t seed = 835;
  std::string hint;
  std::string output = "/private/tmp/cyclic17-star-minconflicts.json";
  bool preserve_cross = false;
};

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    std::string argument = argv[index];
    auto value = [&]() -> std::string {
      if (++index >= argc) {
        std::cerr << "missing value after " << argument << "\n";
        std::exit(2);
      }
      return argv[index];
    };
    if (argument == "--centre") {
      options.centre = std::stoi(value());
    } else if (argument == "--seconds") {
      options.seconds = std::stod(value());
    } else if (argument == "--seed") {
      options.seed = std::stoull(value());
    } else if (argument == "--hint") {
      options.hint = value();
    } else if (argument == "--output") {
      options.output = value();
    } else if (argument == "--preserve-cross") {
      options.preserve_cross = true;
    } else {
      std::cerr << "unknown argument " << argument << "\n";
      std::exit(2);
    }
  }
  if (options.centre < 0 || options.centre >= FIXED) {
    std::cerr << "--centre must lie in 0,...,14\n";
    std::exit(2);
  }
  return options;
}

struct PairMove {
  int first_variable = -1;
  int first_replacement = -1;
  int second_variable = -1;
  int second_replacement = -1;
  PairDelta delta;
};

int run_preserving_cross(
    const Options &options,
    const Instance &instance,
    SearchState &state,
    std::mt19937_64 &rng) {
  std::array<std::array<int, P>, ORBITS> holder{};
  for (auto &row : holder) row.fill(-1);
  for (int variable = 0; variable < VARIABLES; ++variable) {
    const Candidate &candidate =
        instance.candidates[state.selected[variable]];
    if (holder[candidate.orbit][candidate.shift] >= 0) {
      std::cerr << "--preserve-cross hint has a repeated phase\n";
      return 2;
    }
    holder[candidate.orbit][candidate.shift] = variable;
  }
  for (int column = EDGE_COLUMNS; column < COLUMNS; ++column) {
    if (state.count[column] != 1) {
      std::cerr << "--preserve-cross requires an exact cross hint\n";
      return 2;
    }
  }

  auto best = state.selected;
  int best_cost = state.raw_cost;
  std::int64_t step = 0;
  std::int64_t last_best = 0;
  write_best(
      options.output, instance, best, best_cost, options.seed, step);
  std::cout << "{\"status\":\"START_CROSS_EXACT\",\"raw_l1\":"
            << best_cost << "}\n";
  const auto started = std::chrono::steady_clock::now();
  auto expired = [&]() {
    return std::chrono::duration<double>(
               std::chrono::steady_clock::now() - started)
               .count() >= options.seconds;
  };

  std::vector<PairMove> proposals;
  proposals.reserve(256);
  auto add_swap = [&](int first_variable, int first_replacement) {
    const Candidate &old_first =
        instance.candidates[state.selected[first_variable]];
    const Candidate &new_first =
        instance.candidates[first_replacement];
    int second_variable =
        holder[new_first.orbit][new_first.shift];
    if (second_variable < 0 || second_variable == first_variable) return;
    int second_replacement =
        instance.candidate_for_shift[second_variable][old_first.shift];
    if (second_replacement < 0) return;
    PairMove move;
    move.first_variable = first_variable;
    move.first_replacement = first_replacement;
    move.second_variable = second_variable;
    move.second_replacement = second_replacement;
    move.delta = pair_move_delta(
        instance,
        state,
        first_variable,
        first_replacement,
        second_variable,
        second_replacement);
    proposals.push_back(move);
  };

  while (!expired() && best_cost != 0) {
    ++step;
    int target = -1;
    bool seek_zero = (rng() % 100) < 72;
    for (int attempt = 0; attempt < 100; ++attempt) {
      int column = static_cast<int>(rng() % EDGE_COLUMNS);
      if ((seek_zero && state.count[column] == 0) ||
          (!seek_zero && state.count[column] > 1)) {
        target = column;
        break;
      }
    }
    if (target < 0) {
      for (int column = 0; column < EDGE_COLUMNS; ++column) {
        if (state.count[column] != 1) {
          target = column;
          break;
        }
      }
    }
    if (target < 0) break;

    proposals.clear();
    if (state.count[target] == 0) {
      for (int replacement : instance.column_candidates[target]) {
        int variable = instance.candidates[replacement].variable;
        if (state.selected[variable] != replacement) {
          add_swap(variable, replacement);
        }
      }
    } else {
      for (int selected_candidate :
           instance.column_candidates[target]) {
        int variable =
            instance.candidates[selected_candidate].variable;
        if (state.selected[variable] != selected_candidate) continue;
        for (int replacement : instance.choices[variable]) {
          if (replacement != selected_candidate) {
            add_swap(variable, replacement);
          }
        }
      }
    }
    if (proposals.empty()) {
      for (int attempt = 0; attempt < 100 && proposals.empty(); ++attempt) {
        int variable = static_cast<int>(rng() % VARIABLES);
        const auto &choices = instance.choices[variable];
        int replacement =
            choices[rng() % static_cast<std::uint64_t>(choices.size())];
        if (replacement != state.selected[variable]) {
          add_swap(variable, replacement);
        }
      }
      if (proposals.empty()) continue;
    }

    int chosen = -1;
    std::int64_t best_score = std::numeric_limits<std::int64_t>::max();
    bool random_walk = (rng() % 1000) < 30;
    for (int index = 0; index < static_cast<int>(proposals.size());
         ++index) {
      const PairMove &move = proposals[index];
      bool aspiration =
          state.raw_cost + move.delta.raw < best_cost;
      if ((state.tabu_until[move.first_variable] > step ||
           state.tabu_until[move.second_variable] > step) &&
          !aspiration) {
        continue;
      }
      std::int64_t score = move.delta.weighted;
      if (random_walk) score = static_cast<std::int64_t>(rng() % 17);
      if (score < best_score ||
          (score == best_score && (rng() & 1))) {
        best_score = score;
        chosen = index;
      }
    }
    if (chosen < 0) chosen = static_cast<int>(rng() % proposals.size());
    const PairMove move = proposals[chosen];
    const Candidate old_first =
        instance.candidates[state.selected[move.first_variable]];
    const Candidate old_second =
        instance.candidates[state.selected[move.second_variable]];
    apply_pair_move(
        instance,
        state,
        move.first_variable,
        move.first_replacement,
        move.second_variable,
        move.second_replacement,
        move.delta);
    holder[old_first.orbit][old_first.shift] = move.second_variable;
    holder[old_second.orbit][old_second.shift] = move.first_variable;
    state.tabu_until[move.first_variable] =
        step + 7 + static_cast<std::int64_t>(rng() % 19);
    state.tabu_until[move.second_variable] =
        step + 7 + static_cast<std::int64_t>(rng() % 19);

    if (state.raw_cost < best_cost) {
      best_cost = state.raw_cost;
      best = state.selected;
      last_best = step;
      write_best(
          options.output, instance, best, best_cost, options.seed, step);
      std::cout << "{\"status\":\"IMPROVEMENT_CROSS_EXACT\","
                << "\"step\":" << step
                << ",\"raw_l1\":" << best_cost << "}\n"
                << std::flush;
    }
    if (step - last_best > 0 && (step - last_best) % 50000 == 0) {
      for (int column = 0; column < EDGE_COLUMNS; ++column) {
        if (state.count[column] != 1) ++state.weight[column];
      }
      rebuild(instance, state);
    }
  }

  write_best(options.output, instance, best, best_cost, options.seed, step);
  std::cout << "{\"status\":\""
            << (best_cost == 0 ? "STAR_WITNESS"
                               : "NO_STAR_WITNESS_CROSS_EXACT")
            << "\",\"raw_l1\":" << best_cost
            << ",\"steps\":" << step
            << ",\"scope\":\"one fixed-Wallis C17 star only\","
            << "\"mathematical_status\":\""
            << (best_cost == 0 ? "independent verification required"
                               : "heuristic only")
            << "\"}\n";
  return best_cost == 0 ? 0 : 1;
}

}  // namespace

int main(int argc, char **argv) {
  const Options options = parse_options(argc, argv);
  const Instance instance = build_instance(options.centre);
  std::mt19937_64 rng(options.seed);

  SearchState state;
  state.weight.fill(1);
  bool hinted = !options.hint.empty() &&
                load_hint(options.hint, instance, state.selected);
  if (!hinted) {
    for (int variable = 0; variable < VARIABLES; ++variable) {
      const auto &choices = instance.choices[variable];
      state.selected[variable] =
          choices[rng() % static_cast<std::uint64_t>(choices.size())];
    }
  }
  rebuild(instance, state);

  if (options.preserve_cross) {
    if (!hinted) {
      std::cerr << "--preserve-cross requires --hint\n";
      return 2;
    }
    return run_preserving_cross(options, instance, state, rng);
  }

  auto best = state.selected;
  int best_cost = state.raw_cost;
  std::int64_t step = 0;
  std::int64_t last_best = 0;
  write_best(
      options.output, instance, best, best_cost, options.seed, step);
  std::cout << "{\"status\":\"START\",\"hinted\":"
            << (hinted ? "true" : "false")
            << ",\"raw_l1\":" << state.raw_cost
            << ",\"candidates\":" << instance.candidates.size() << "}\n";

  const auto started = std::chrono::steady_clock::now();
  auto expired = [&]() {
    return std::chrono::duration<double>(
               std::chrono::steady_clock::now() - started)
               .count() >= options.seconds;
  };

  std::vector<int> proposals;
  proposals.reserve(256);
  while (!expired() && best_cost != 0) {
    ++step;
    int target = -1;
    bool seek_zero = (rng() % 100) < 72;
    for (int attempt = 0; attempt < 100; ++attempt) {
      int candidate = static_cast<int>(rng() % COLUMNS);
      if ((seek_zero && state.count[candidate] == 0) ||
          (!seek_zero && state.count[candidate] > 1)) {
        target = candidate;
        break;
      }
    }
    if (target < 0) {
      for (int column = 0; column < COLUMNS; ++column) {
        if (state.count[column] != 1) {
          target = column;
          break;
        }
      }
    }
    if (target < 0) break;

    proposals.clear();
    if (state.count[target] == 0) {
      proposals = instance.column_candidates[target];
    } else {
      for (int candidate : instance.column_candidates[target]) {
        int variable = instance.candidates[candidate].variable;
        if (state.selected[variable] != candidate) continue;
        for (int replacement : instance.choices[variable]) {
          if (replacement != candidate) proposals.push_back(replacement);
        }
      }
    }
    if (proposals.empty()) std::abort();

    int chosen = -1;
    Delta chosen_delta;
    std::int64_t best_score = std::numeric_limits<std::int64_t>::max();
    bool random_walk = (rng() % 1000) < 25;
    for (int replacement : proposals) {
      int variable = instance.candidates[replacement].variable;
      if (state.selected[variable] == replacement) continue;
      Delta delta = move_delta(instance, state, variable, replacement);
      bool aspiration = state.raw_cost + delta.raw < best_cost;
      if (state.tabu_until[variable] > step && !aspiration) continue;
      std::int64_t score = delta.weighted;
      if (random_walk) score = static_cast<std::int64_t>(rng() % 17);
      if (score < best_score ||
          (score == best_score && (rng() & 1))) {
        best_score = score;
        chosen = replacement;
        chosen_delta = delta;
      }
    }
    if (chosen < 0) {
      int replacement = proposals[rng() % proposals.size()];
      int variable = instance.candidates[replacement].variable;
      if (state.selected[variable] == replacement) continue;
      chosen = replacement;
      chosen_delta =
          move_delta(instance, state, variable, replacement);
    }

    int variable = instance.candidates[chosen].variable;
    apply_move(instance, state, variable, chosen, chosen_delta);
    state.tabu_until[variable] =
        step + 7 + static_cast<std::int64_t>(rng() % 19);

    if (state.raw_cost < best_cost) {
      best_cost = state.raw_cost;
      best = state.selected;
      last_best = step;
      write_best(
          options.output, instance, best, best_cost, options.seed, step);
      std::cout << "{\"status\":\"IMPROVEMENT\",\"step\":" << step
                << ",\"raw_l1\":" << best_cost << "}\n"
                << std::flush;
    }

    if (step - last_best > 0 && (step - last_best) % 50000 == 0) {
      for (int column = 0; column < COLUMNS; ++column) {
        if (state.count[column] != 1) ++state.weight[column];
      }
      rebuild(instance, state);
    }
    if (step - last_best > 0 && (step - last_best) % 500000 == 0) {
      state.selected = best;
      state.tabu_until.fill(0);
      rebuild(instance, state);
      for (int perturb = 0; perturb < 40; ++perturb) {
        int v = static_cast<int>(rng() % VARIABLES);
        const auto &choices = instance.choices[v];
        int replacement =
            choices[rng() % static_cast<std::uint64_t>(choices.size())];
        if (replacement == state.selected[v]) continue;
        Delta delta = move_delta(instance, state, v, replacement);
        apply_move(instance, state, v, replacement, delta);
      }
    }
  }

  write_best(options.output, instance, best, best_cost, options.seed, step);
  std::cout << "{\"status\":\""
            << (best_cost == 0 ? "STAR_WITNESS" : "NO_STAR_WITNESS")
            << "\",\"raw_l1\":" << best_cost
            << ",\"steps\":" << step
            << ",\"scope\":\"one fixed-Wallis C17 star only\","
            << "\"mathematical_status\":\""
            << (best_cost == 0 ? "independent verification required"
                               : "heuristic only")
            << "\"}\n";
  return best_cost == 0 ? 0 : 1;
}
