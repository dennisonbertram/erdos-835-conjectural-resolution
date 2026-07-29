// Fast heuristic master over a finite pool of exact cyclic-17 star rows.
//
// The input pool is the JSON emitted by search_cyclic17_star_row_pool.py.
// Every candidate is assumed to have been independently audited as an exact
// residual row.  The objective is the exact number of equal phase pairs
// across the 91 pairs of outer rows.  Objective zero is a one-star witness
// after independent verification.  A positive result proves nothing, and an
// exhaustive statement never follows from a finite pool.

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
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int LABELS = 14;
constexpr int ORBITS = 40;
constexpr int P = 17;
using Row = std::array<int, ORBITS>;

std::string read_file(const std::string &path) {
  std::ifstream input(path);
  if (!input) {
    std::cerr << "cannot read " << path << "\n";
    std::exit(2);
  }
  std::ostringstream buffer;
  buffer << input.rdbuf();
  return buffer.str();
}

void skip_space_and_commas(const std::string &text, std::size_t &cursor) {
  while (cursor < text.size() &&
         (text[cursor] == ' ' || text[cursor] == '\n' ||
          text[cursor] == '\r' || text[cursor] == '\t' ||
          text[cursor] == ',')) {
    ++cursor;
  }
}

int parse_int(const std::string &text, std::size_t &cursor) {
  skip_space_and_commas(text, cursor);
  char *end = nullptr;
  long value = std::strtol(text.c_str() + cursor, &end, 10);
  if (end == text.c_str() + cursor) {
    std::cerr << "expected integer at byte " << cursor << "\n";
    std::exit(2);
  }
  cursor = static_cast<std::size_t>(end - text.c_str());
  return static_cast<int>(value);
}

std::vector<Row> parse_rows_for_key(
    const std::string &text, const std::string &key) {
  std::string quoted = "\"" + key + "\"";
  std::size_t cursor = text.find(quoted);
  if (cursor == std::string::npos) {
    std::cerr << "missing key " << key << "\n";
    std::exit(2);
  }
  cursor = text.find('[', cursor + quoted.size());
  if (cursor == std::string::npos) std::exit(2);
  ++cursor;
  std::vector<Row> rows;
  while (true) {
    skip_space_and_commas(text, cursor);
    if (cursor >= text.size()) std::exit(2);
    if (text[cursor] == ']') {
      ++cursor;
      break;
    }
    if (text[cursor] != '[') {
      std::cerr << "expected candidate array for " << key << "\n";
      std::exit(2);
    }
    ++cursor;
    Row row{};
    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      row[orbit] = parse_int(text, cursor);
      if (row[orbit] < 0 || row[orbit] >= P) std::exit(2);
    }
    skip_space_and_commas(text, cursor);
    if (cursor >= text.size() || text[cursor] != ']') std::exit(2);
    ++cursor;
    if (std::find(rows.begin(), rows.end(), row) == rows.end()) {
      rows.push_back(row);
    }
  }
  if (rows.empty()) {
    std::cerr << "empty pool " << key << "\n";
    std::exit(2);
  }
  return rows;
}

Row parse_state_row(const std::string &text, const std::string &key) {
  std::string quoted = "\"" + key + "\"";
  std::size_t cursor = text.find(quoted);
  if (cursor == std::string::npos) std::exit(2);
  cursor = text.find('[', cursor + quoted.size());
  if (cursor == std::string::npos) std::exit(2);
  ++cursor;
  Row row{};
  for (int orbit = 0; orbit < ORBITS; ++orbit) {
    row[orbit] = parse_int(text, cursor);
  }
  return row;
}

struct CostMatrix {
  int right_size = 0;
  std::vector<std::uint8_t> values;
  int get(int left, int right) const {
    return values[left * right_size + right];
  }
};

struct Instance {
  std::array<std::vector<Row>, LABELS> pool;
  std::array<std::array<CostMatrix, LABELS>, LABELS> costs;
};

Instance build_instance(const std::string &pool_path) {
  Instance instance;
  const std::string text = read_file(pool_path);
  for (int label = 0; label < LABELS; ++label) {
    instance.pool[label] =
        parse_rows_for_key(text, "0," + std::to_string(label + 1));
  }
  for (int left = 0; left < LABELS; ++left) {
    for (int right = left + 1; right < LABELS; ++right) {
      CostMatrix matrix;
      matrix.right_size = static_cast<int>(instance.pool[right].size());
      matrix.values.reserve(
          instance.pool[left].size() * instance.pool[right].size());
      for (const Row &left_row : instance.pool[left]) {
        for (const Row &right_row : instance.pool[right]) {
          int equal = 0;
          for (int orbit = 0; orbit < ORBITS; ++orbit) {
            equal += left_row[orbit] == right_row[orbit];
          }
          matrix.values.push_back(static_cast<std::uint8_t>(equal));
        }
      }
      instance.costs[left][right] = std::move(matrix);
    }
  }
  return instance;
}

int pair_cost(
    const Instance &instance,
    int left,
    int left_choice,
    int right,
    int right_choice) {
  if (left < right) {
    return instance.costs[left][right].get(left_choice, right_choice);
  }
  return instance.costs[right][left].get(right_choice, left_choice);
}

int objective(
    const Instance &instance,
    const std::array<int, LABELS> &selected) {
  int answer = 0;
  for (int left = 0; left < LABELS; ++left) {
    for (int right = left + 1; right < LABELS; ++right) {
      answer += pair_cost(
          instance, left, selected[left], right, selected[right]);
    }
  }
  return answer;
}

int single_delta(
    const Instance &instance,
    const std::array<int, LABELS> &selected,
    int label,
    int replacement) {
  int delta = 0;
  for (int other = 0; other < LABELS; ++other) {
    if (other == label) continue;
    delta += pair_cost(
                 instance, label, replacement, other, selected[other]) -
             pair_cost(
                 instance, label, selected[label], other, selected[other]);
  }
  return delta;
}

int pair_delta(
    const Instance &instance,
    const std::array<int, LABELS> &selected,
    int first,
    int first_replacement,
    int second,
    int second_replacement) {
  int delta =
      pair_cost(
          instance,
          first,
          first_replacement,
          second,
          second_replacement) -
      pair_cost(
          instance, first, selected[first], second, selected[second]);
  for (int other = 0; other < LABELS; ++other) {
    if (other == first || other == second) continue;
    delta +=
        pair_cost(
            instance, first, first_replacement, other, selected[other]) -
        pair_cost(
            instance, first, selected[first], other, selected[other]);
    delta +=
        pair_cost(
            instance, second, second_replacement, other, selected[other]) -
        pair_cost(
            instance, second, selected[second], other, selected[other]);
  }
  return delta;
}

int coordinate_descent(
    const Instance &instance,
    std::array<int, LABELS> &selected,
    int current,
    std::mt19937_64 &rng) {
  while (true) {
    int best_delta = 0;
    std::vector<std::pair<int, int>> moves;
    for (int label = 0; label < LABELS; ++label) {
      for (int replacement = 0;
           replacement < static_cast<int>(instance.pool[label].size());
           ++replacement) {
        if (replacement == selected[label]) continue;
        int delta =
            single_delta(instance, selected, label, replacement);
        if (delta < best_delta) {
          best_delta = delta;
          moves = {{label, replacement}};
        } else if (delta == best_delta && delta < 0) {
          moves.push_back({label, replacement});
        }
      }
    }
    if (moves.empty()) return current;
    auto [label, replacement] = moves[rng() % moves.size()];
    selected[label] = replacement;
    current += best_delta;
  }
}

void write_result(
    const std::string &path,
    const Instance &instance,
    const std::array<int, LABELS> &selected,
    int value,
    std::uint64_t seed,
    std::int64_t steps) {
  std::ofstream output(path);
  if (!output) std::exit(2);
  output << "{\n"
         << "  \"centre\": 0,\n"
         << "  \"collision_pairs\": " << value << ",\n"
         << "  \"seed\": " << seed << ",\n"
         << "  \"steps\": " << steps << ",\n"
         << "  \"rows\": {\n";
  for (int label = 0; label < LABELS; ++label) {
    output << "    \"0," << (label + 1) << "\": [";
    const Row &row = instance.pool[label][selected[label]];
    for (int orbit = 0; orbit < ORBITS; ++orbit) {
      if (orbit) output << ", ";
      output << row[orbit];
    }
    output << "]" << (label + 1 == LABELS ? "\n" : ",\n");
  }
  output << "  }\n}\n";
}

struct Options {
  std::string pool;
  std::string source;
  std::string output = "/private/tmp/cyclic17-star-pool-master.json";
  double seconds = 300.0;
  std::uint64_t seed = 835;
};

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    std::string argument = argv[index];
    auto value = [&]() -> std::string {
      if (++index >= argc) std::exit(2);
      return argv[index];
    };
    if (argument == "--pool") {
      options.pool = value();
    } else if (argument == "--source") {
      options.source = value();
    } else if (argument == "--output") {
      options.output = value();
    } else if (argument == "--seconds") {
      options.seconds = std::stod(value());
    } else if (argument == "--seed") {
      options.seed = std::stoull(value());
    } else {
      std::cerr << "unknown argument " << argument << "\n";
      std::exit(2);
    }
  }
  if (options.pool.empty()) std::exit(2);
  return options;
}

}  // namespace

int main(int argc, char **argv) {
  const Options options = parse_options(argc, argv);
  const Instance instance = build_instance(options.pool);
  std::mt19937_64 rng(options.seed);
  std::array<int, LABELS> selected{};
  if (!options.source.empty()) {
    const std::string source = read_file(options.source);
    for (int label = 0; label < LABELS; ++label) {
      Row row = parse_state_row(
          source, "0," + std::to_string(label + 1));
      auto found = std::find(
          instance.pool[label].begin(), instance.pool[label].end(), row);
      if (found == instance.pool[label].end()) {
        std::cerr << "source row absent from pool for label "
                  << (label + 1) << "\n";
        return 2;
      }
      selected[label] =
          static_cast<int>(found - instance.pool[label].begin());
    }
  } else {
    for (int label = 0; label < LABELS; ++label) {
      selected[label] =
          static_cast<int>(rng() % instance.pool[label].size());
    }
  }
  int current = objective(instance, selected);
  current = coordinate_descent(instance, selected, current, rng);
  auto best = selected;
  int best_value = current;
  std::int64_t steps = 0;
  write_result(
      options.output, instance, best, best_value, options.seed, steps);
  std::cout << "{\"status\":\"START\",\"collision_pairs\":"
            << best_value << "}\n";

  const auto started = std::chrono::steady_clock::now();
  auto expired = [&]() {
    return std::chrono::duration<double>(
               std::chrono::steady_clock::now() - started)
               .count() >= options.seconds;
  };
  constexpr std::int64_t EPOCH = 200000;
  while (!expired() && best_value != 0) {
    ++steps;
    double position = static_cast<double>(steps % EPOCH) / EPOCH;
    double temperature = 12.0 * std::pow(0.02, position);
    bool pair_move = (rng() % 100) < 30;
    int delta = 0;
    int first = static_cast<int>(rng() % LABELS);
    int first_replacement = static_cast<int>(
        rng() % instance.pool[first].size());
    if (first_replacement == selected[first]) continue;
    int second = -1;
    int second_replacement = -1;
    if (pair_move) {
      do {
        second = static_cast<int>(rng() % LABELS);
      } while (second == first);
      second_replacement = static_cast<int>(
          rng() % instance.pool[second].size());
      if (second_replacement == selected[second]) continue;
      delta = pair_delta(
          instance,
          selected,
          first,
          first_replacement,
          second,
          second_replacement);
    } else {
      delta = single_delta(
          instance, selected, first, first_replacement);
    }
    bool accept =
        delta <= 0 ||
        std::generate_canonical<double, 53>(rng) <
            std::exp(-static_cast<double>(delta) / temperature);
    if (accept) {
      selected[first] = first_replacement;
      if (pair_move) selected[second] = second_replacement;
      current += delta;
      if (current < best_value) {
        current =
            coordinate_descent(instance, selected, current, rng);
        if (current < best_value) {
          best_value = current;
          best = selected;
          write_result(
              options.output,
              instance,
              best,
              best_value,
              options.seed,
              steps);
          std::cout << "{\"status\":\"IMPROVEMENT\",\"step\":"
                    << steps << ",\"collision_pairs\":" << best_value
                    << "}\n"
                    << std::flush;
        }
      }
    }
    if (steps % EPOCH == 0) {
      selected = best;
      current = best_value;
      int perturbations = 2 + static_cast<int>(rng() % 7);
      for (int count = 0; count < perturbations; ++count) {
        int label = static_cast<int>(rng() % LABELS);
        int replacement = static_cast<int>(
            rng() % instance.pool[label].size());
        current +=
            single_delta(instance, selected, label, replacement);
        selected[label] = replacement;
      }
    }
  }
  write_result(
      options.output, instance, best, best_value, options.seed, steps);
  std::cout << "{\"status\":\""
            << (best_value == 0 ? "STAR_WITNESS" : "NO_STAR_WITNESS")
            << "\",\"collision_pairs\":" << best_value
            << ",\"steps\":" << steps
            << ",\"scope\":\"finite exact-row pool only\","
            << "\"mathematical_status\":\""
            << (best_value == 0 ? "independent verification required"
                                : "heuristic only")
            << "\"}\n";
  return best_value == 0 ? 0 : 1;
}
